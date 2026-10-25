/* Local deterministic test driver for real MatIEC-generated control code.
 * No sockets, device files, physical addresses, sleeping, or real-time scheduler.
 * One input line = one scan at a caller-supplied monotonic millisecond timestamp.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include "iec_std_lib.h"
#include "accessor.h"
#include "POUS.h"
#include "POUS.c"
TIME __CURRENT_TIME;
BOOL __DEBUG = 0;
int iec_lib_snprintf(char *s, size_t n, const char *fmt, ...) {
    va_list ap; va_start(ap, fmt); int r = vsnprintf(s, n, fmt, ap); va_end(ap); return r;
}
#define SET(obj, name, value) __SET_VAR(obj., name,, value)
#define GET(obj, name) __GET_VAR(obj.name,)
int main(int argc, char **argv) {
    if (argc != 2 || (strcmp(argv[1], "starter") && strcmp(argv[1], "timing") &&
        strcmp(argv[1], "station") && strcmp(argv[1], "original"))) return 2;
    STARTER_data__ starter = {0};
    TIMING_data__ timing = {0};
    STATION_data__ station = {0};
    DUPLEXLEADLAG_data__ original = {0};
    STARTER_init__(&starter, 0); TIMING_init__(&timing, 0);
    STATION_init__(&station, 0); DUPLEXLEADLAG_init__(&original, 0);
    char line[512]; long long ms, previous = -1; int reset, b[10];
    while (fgets(line, sizeof line, stdin)) {
        char extra;
        int n = sscanf(line, "%lld %d %d %d %d %d %d %d %d %d %d %d %c", &ms, &reset,
            &b[0], &b[1], &b[2], &b[3], &b[4], &b[5], &b[6], &b[7], &b[8], &b[9], &extra);
        if (n != 12 || ms < 0 || ms > 86400000 || (reset != 0 && reset != 1) ||
            (!reset && ms <= previous)) { fprintf(stderr, "invalid scan frame\n"); return 2; }
        for (int i = 0; i < 10; i++) if (b[i] != 0 && b[i] != 1) return 2;
        previous = ms;
        __CURRENT_TIME.tv_sec = ms / 1000;
        __CURRENT_TIME.tv_nsec = (ms % 1000) * 1000000;
        if (reset) {
            STARTER_init__(&starter, 0); TIMING_init__(&timing, 0);
            STATION_init__(&station, 0); DUPLEXLEADLAG_init__(&original, 0);
        }
        if (!strcmp(argv[1], "starter")) {
            SET(starter,START_BUTTON,b[0]); SET(starter,STOP_OK,b[1]); SET(starter,MOTOR_HEALTHY,b[2]);
            STARTER_body__(&starter);
            printf("%d\n", GET(starter,MOTOR_RUN));
        } else if (!strcmp(argv[1], "timing")) {
            SET(timing,SIGNAL,b[0]); SET(timing,RESET_COUNT,b[1]); TIMING_body__(&timing);
            TIME et = GET(timing,ELAPSED);
            printf("%d,%d,%d,%ld\n", GET(timing,EDGE),GET(timing,COUNT),GET(timing,DONE),
                (long)(et.tv_sec * 1000 + et.tv_nsec / 1000000));
        } else {
#define INPUTS(obj) \
            SET(obj,FS1_OFF,b[0]); SET(obj,FS2_LEAD,b[1]); SET(obj,FS3_LAG,b[2]); SET(obj,FS4_HIGH,b[3]); \
            SET(obj,P1_AUTO,b[4]); SET(obj,P2_AUTO,b[5]); SET(obj,P1_SEAL_FAIL,b[6]); \
            SET(obj,P2_SEAL_FAIL,b[7]); SET(obj,P1_OVERTEMP,b[8]); SET(obj,P2_OVERTEMP,b[9]);
            if (!strcmp(argv[1], "station")) {
                INPUTS(station); STATION_body__(&station);
                printf("%d,%d,%d,%d,%d,%d,%d,%d\n", GET(station,P1_RUN), GET(station,P2_RUN),
                    GET(station,HIGH_ALARM),GET(station,INVALID_ALARM),GET(station,NO_PUMP_ALARM),
                    GET(station,LEAD),GET(station,DEMAND),GET(station,LAG_LATCHED));
            } else {
                INPUTS(original); DUPLEXLEADLAG_body__(&original);
                printf("%d,%d,%d,%d,%d\n",GET(original,P1_RUN),GET(original,P2_RUN),
                    GET(original,ALM_HIGH_LEVEL),GET(original,ALM_FLOAT_FAULT),GET(original,ALM_NO_PUMP));
            }
        }
        fflush(stdout);
    }
    return ferror(stdin) ? 2 : 0;
}
