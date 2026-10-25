#!/usr/bin/env python3
"""Build and exercise actual MatIEC-compiled code in a local deterministic C harness."""
import argparse
import csv
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import select
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / 'labs/toolchain.lock.json').read_text())
SRC = ROOT / '.toolchain/src' / ('matiec-' + LOCK['matiec_commit'])
IEC = ROOT / '.toolchain/prefix/bin/iec2c'
DEFAULT_BUILD = ROOT / 'build/reference'
INPUTS = ['fs1_off', 'fs2_lead', 'fs3_lag', 'fs4_high', 'p1_auto', 'p2_auto',
          'p1_seal_fail', 'p2_seal_fail', 'p1_overtemp', 'p2_overtemp']
OUTPUTS = ['p1_run', 'p2_run', 'high_alarm', 'invalid_alarm', 'no_pump_alarm', 'lead', 'demand', 'lag_latched']
MUTANTS = {
    'ignore-health': ('available1 := p1_auto AND NOT p1_seal_fail AND NOT p1_overtemp;', 'available1 := p1_auto;'),
    'instant-lag': ('PT := T#5s', 'PT := T#0s'),
    'no-alternation': ('IF lead = 1 THEN lead := 2; ELSE lead := 1; END_IF;', 'lead := 1;'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compiler():
    return os.environ.get('CC') or (str(Path('/opt/homebrew/opt/llvm/bin/clang'))
        if Path('/opt/homebrew/opt/llvm/bin/clang').exists() else shutil.which('cc'))


def build(target, apply=False, mutant=None, source=None):
    target = target.resolve()
    if not target.is_relative_to(ROOT / 'build'):
        raise ValueError('Build outputs must stay in this repository build/ directory.')
    source = (source or ROOT / 'labs/plc/station.st').resolve()
    print(f'{"BUILD" if apply else "DRY RUN"}: copy sources -> {target}; MatIEC -> C -> native executable')
    if mutant:
        print('Deliberate fault on build COPY:', mutant)
    if not apply:
        print('Use --apply to create build artifacts; source programs are never edited.')
        return
    if not IEC.exists():
        raise SystemExit('Compiler missing. Follow labs/00-setup.md and run scripts/bootstrap.py --apply.')
    target.mkdir(parents=True, exist_ok=True)
    for stale in ('plc-sim', 'build.json'):
        (target / stale).unlink(missing_ok=True)
    station = source.read_text()
    if mutant:
        old, new = MUTANTS[mutant]
        if station.count(old) != 1:
            raise ValueError('Mutation anchor must occur exactly once')
        station = station.replace(old, new)
    sources = [ROOT / 'labs/plc/foundations.st', source, ROOT / 'project/plc/lead_lag.st', ROOT / 'labs/runtime/harness.c']
    (target / 'combined.st').write_text(sources[0].read_text() + '\n' + station + '\n' + sources[2].read_text())
    shutil.copyfile(sources[3], target / 'harness.c')
    commands = [[str(IEC), '-I', str(SRC / 'lib'), '-T', str(target), str(target / 'combined.st')],
                [compiler(), '-std=c99', '-O2', '-Wno-unused-function', '-I', str(SRC / 'lib/C'),
                 '-I', str(target), str(target / 'harness.c'), '-lm', '-o', str(target / 'plc-sim')]]
    with (target / 'compile.log').open('w') as log:
        for cmd in commands:
            log.write('+ ' + ' '.join(cmd) + '\n'); log.flush()
            result = subprocess.run(cmd, cwd=target, stdout=log, stderr=subprocess.STDOUT)
            if result.returncode:
                print((target / 'compile.log').read_text(), file=sys.stderr)
                raise SystemExit(result.returncode)
    meta = {'matiec_commit': LOCK['matiec_commit'], 'mutant': mutant,
            'sources': {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): digest(p) for p in sources},
            'commands': commands, 'compiler': subprocess.check_output([compiler(), '--version'], text=True).splitlines()[0],
            'platform': platform.platform(), 'python': platform.python_version(),
            'combined_st_sha256': digest(target / 'combined.st'),
            'executable_sha256': digest(target / 'plc-sim')}
    (target / 'build.json').write_text(json.dumps(meta, indent=2) + '\n')
    print('Compiled:', target / 'plc-sim')


class Native:
    """Pipe to the compiled binary, not a Python reimplementation of the controller."""
    def __init__(self, build_dir=DEFAULT_BUILD, mode='station'):
        receipt = json.loads((build_dir / 'build.json').read_text())
        if digest(build_dir / 'plc-sim') != receipt['executable_sha256']:
            raise ValueError('Executable differs from build receipt; rebuild.')
        for name, expected in receipt['sources'].items():
            if digest(ROOT / name) != expected:
                raise ValueError('Source changed since compilation; rebuild: ' + name)
        self.process = subprocess.Popen([str(build_dir / 'plc-sim'), mode], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.t = -100
    def scan(self, bits, ms=None, reset=False):
        self.t = self.t + 100 if ms is None else ms
        bits = list(bits) + [0] * (10-len(bits))
        self.process.stdin.write(' '.join(map(str, [self.t, int(reset)] + bits)) + '\n')
        self.process.stdin.flush()
        if not select.select([self.process.stdout], [], [], 5)[0]:
            self.process.kill()
            raise TimeoutError('Compiled scan exceeded five seconds; process stopped.')
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError('Native harness stopped: ' + self.process.stderr.read())
        return tuple(map(int, line.strip().split(',')))
    def close(self):
        self.process.stdin.close()
        self.process.wait(timeout=5)
        error = self.process.stderr.read()
        self.process.stdout.close(); self.process.stderr.close()
        if self.process.returncode:
            raise RuntimeError(error)
    def __enter__(self): return self
    def __exit__(self, *exc): self.close()


def inputs(level=0, **overrides):
    if type(level) is not int or not 0 <= level <= 4:
        raise ValueError('level must be an integer from 0 through 4')
    unknown = set(overrides) - set(INPUTS)
    if unknown:
        raise ValueError('Unknown input keys: ' + ', '.join(sorted(unknown)))
    for key, value in overrides.items():
        if type(value) not in (int, bool) or value not in (0, 1):
            raise ValueError(f'{key} must be Boolean or integer 0/1')
    values = dict(zip(INPUTS, [int(level >= n) for n in range(1,5)] + [1,1,0,0,0,0]))
    values.update({key:int(value) for key,value in overrides.items()})
    return [values[k] for k in INPUTS]


def foundations(build_dir):
    with Native(build_dir, 'starter') as n:
        for start, stop, healthy in itertools.product((0,1), repeat=3):
            actual = n.scan([start, stop, healthy], reset=True)
            assert actual == (start & stop & healthy,), (start, stop, healthy, actual)
        trace = [n.scan(b, reset=(i == 0))[0] for i,b in enumerate([[1,1,1],[0,1,1],[1,0,1],[0,1,1],[1,1,0]])]
        assert trace == [1,1,0,0,0], trace
    with Native(build_dir, 'timing') as n:
        rows = [n.scan([1,0], ms=t, reset=(t == 0)) for t in range(0,701,100)]
        assert rows[0] == (1,1,0,0), rows[0]
        assert rows[4] == (0,1,0,400), rows[4]
        assert rows[5] == (0,1,1,500), rows[5]
        assert n.scan([0,0], ms=800) == (0,1,0,0)
        assert n.scan([1,0], ms=900) == (1,2,0,0)
        assert n.scan([1,1], ms=1000)[1] == 0
    print('PASS foundations: 8 truth rows, latch/stop precedence, R_TRIG, CTU, TON boundary/reset')
    return rows


def station_tests(build_dir):
    with Native(build_dir) as n:
        assert n.scan(inputs(), reset=True)[:2] == (0,0)
        assert n.scan(inputs(2))[:2] == (1,0)
        assert n.scan(inputs(1))[:2] == (1,0)
        assert n.scan(inputs(0))[5:7] == (2,0), 'drained cycle must select lead 2 and clear demand'
        assert n.scan(inputs(2))[:2] == (0,1), 'alternation'
        assert n.scan(inputs(2,p2_overtemp=1))[:2] == (1,0), 'fallback'
        assert n.scan(inputs(2,p1_seal_fail=1,p2_overtemp=1))[:5] == (0,0,0,0,1), 'both tripped: pumps off and no-pump alarm'
        assert n.scan(inputs(4,fs1_off=0))[:5] == (0,0,1,1,0), 'invalid input inhibition'
        assert n.scan(inputs(2), reset=True)[:2] == (1,0), 'cold reset'
        lag = [n.scan(inputs(3), ms=t, reset=(t == 0)) for t in range(0,5101,100)]
        assert lag[49][:2] == (1,0), 'lag too early'
        assert lag[50][:2] == (1,1), 'lag missing at 5s'
        assert n.scan(inputs(1), ms=5200)[:2] == (1,1), 'lag must latch until drained'
        assert n.scan(inputs(0), ms=5300)[:2] == (0,0)
        for t in range(0,10001,100):
            row = n.scan(inputs(3 if (t//1000)%2 == 0 else 2), ms=t, reset=(t == 0))
            assert row[1] == 0, 'interrupted timer accumulated incorrectly'
        # TON resets if all pumps become unavailable during the delay.
        n.scan(inputs(3), ms=0, reset=True)
        n.scan(inputs(3), ms=4900)
        n.scan(inputs(3,p1_auto=0,p2_auto=0), ms=5000)
        assert n.scan(inputs(3), ms=5100)[:2] == (1,0)
        assert n.scan(inputs(3), ms=10000)[:2] == (1,0)
        assert n.scan(inputs(3), ms=10100)[:2] == (1,1)
        # Independent invariants, every fresh-start Boolean input image.
        for bits in itertools.product((0,1), repeat=10):
            o = n.scan(bits, reset=True)
            invalid = any(bits[j] and not bits[j-1] for j in (1,2,3))
            assert not o[0] or (bits[4] and not bits[6] and not bits[8]), ('p1 permissive',bits,o)
            assert not o[1] or (bits[5] and not bits[7] and not bits[9]), ('p2 permissive',bits,o)
            assert not invalid or not (o[0] or o[1]), ('invalid',bits,o)
            assert o[2] == bits[3]
            assert o[3] == int(invalid)
    print('PASS station: cycle, alternation, fallback, faults, restart, 5s boundary, chatter, 1024 input images')


def replay(build_dir, scenario, output):
    data = json.loads(scenario.read_text())
    mode = data.get('mode', 'station')
    fields = OUTPUTS if mode == 'station' else ['edge','count','done','elapsed_ms']
    rows = []
    with Native(build_dir, mode) as n:
        for j, step in enumerate(data['scans']):
            bits = inputs(**step['inputs']) if mode == 'station' else step['bits']
            actual = n.scan(bits, ms=step['ms'], reset=step.get('reset',j == 0))
            if 'expected' in step:
                for field, expected in step['expected'].items():
                    assert actual[fields.index(field)] == expected, (j,field,expected,actual)
            rows.append({'ms':step['ms'], **dict(zip(fields,actual))})
    save_csv(output, rows)
    print(f'PASS replay {scenario.name}: {len(rows)} scans -> {output}')


def save_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w',newline='') as f:
        w = csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def plant(build_dir, output, fault='none', scans=1800):
    # A toy wet well: integer millilitres, 100ms scan. Not hydraulics or equipment sizing.
    volume = 20000
    rows = []
    overflow = 0
    with Native(build_dir) as n:
        for k in range(scans):
            t = k*100
            level = sum(volume >= threshold for threshold in (10000,40000,65000,85000))
            extra = {}
            active = 400 <= k < 900
            if active and fault == 'pump1-trip': extra['p1_overtemp'] = 1
            if active and fault == 'both-trip': extra.update(p1_overtemp=1,p2_overtemp=1)
            if active and fault == 'bad-float': extra['fs1_off'] = 0
            sensed = inputs(level, **extra)
            command = n.scan(sensed, ms=t, reset=k==0)
            inflow = 450 if 600 <= k < 1100 else 120
            pumped = 300 * (command[0]+command[1])
            # A blocked pump has no feedback in this controller. Show the missing requirement.
            if active and fault == 'blocked-pump1': pumped -= 300*command[0]
            next_volume = max(0,volume+inflow-pumped)
            spilled = max(0,next_volume-100000); overflow += spilled
            rows.append({'ms':t,'volume_ml':volume,'physical_level_index':level,
                **dict(zip(INPUTS,sensed)), **dict(zip(OUTPUTS,command)),
                'inflow_ml_per_scan':inflow,'pumped_ml_per_scan':pumped,'spill_ml':spilled})
            volume = min(100000,next_volume)
    save_csv(output, rows)
    summary = {'fault':fault,'scans':scans,'max_volume_ml':max(r['volume_ml'] for r in rows),
        'spill_ml':overflow,'p1_on_scans':sum(r['p1_run'] for r in rows),
        'p2_on_scans':sum(r['p2_run'] for r in rows),'high_alarm_scans':sum(r['high_alarm'] for r in rows),
        'invalid_alarm_scans':sum(r['invalid_alarm'] for r in rows),
        'no_pump_alarm_scans':sum(r['no_pump_alarm'] for r in rows)}
    output.with_suffix('.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
    return rows,summary


def compare_original(build_dir, output):
    sys.path.insert(0,str(ROOT / 'project/tools'))
    from vectors import generate
    rows = []; prior = None
    with Native(build_dir, 'original') as n:
        for vector in generate():
            reset = vector['scenario'] != prior
            prior = vector['scenario']
            actual = n.scan([vector[k] for k in INPUTS],ms=vector['t_s']*1000,reset=reset)
            rows.append({'scenario':prior,'t_s':vector['t_s'],
                'python_p1':vector['exp_p1_run'],'python_p2':vector['exp_p2_run'],
                'compiled_p1':actual[0],'compiled_p2':actual[1],
                'pump_match':int(actual[:2] == (vector['exp_p1_run'],vector['exp_p2_run']))})
    save_csv(output,rows)
    mismatches = [r for r in rows if not r['pump_match']]
    print(f'OBSERVED original comparison: {len(rows)} rows, {len(mismatches)} pump-output differences -> {output}')
    for row in mismatches: print(json.dumps(row))
    observed = {(r['scenario'].split()[0],r['t_s'],r['python_p1'],r['python_p2'],
                 r['compiled_p1'],r['compiled_p2']) for r in mismatches}
    expected = {('T02',5,1,1,1,0), ('T07',5,1,1,1,0)}
    assert observed == expected, ('Changed baseline differences: inspect, do not bless automatically', observed)
    print('Alarm sets are NOT equivalent: original ST exposes only 3 aggregate alarms; Python has individual trip alarms.')


def test_all(build_dir):
    foundations(build_dir); station_tests(build_dir)
    replay(build_dir, ROOT/'labs/scenarios/cycle.json', build_dir/'cycle.csv')
    replay(build_dir, ROOT/'labs/scenarios/timer.json', build_dir/'timer.csv')
    rows, summary = plant(build_dir, build_dir/'plant.csv')
    assert summary['spill_ml'] == 0 and summary['p1_on_scans'] > 0 and summary['p2_on_scans'] > 0
    again,_ = plant(build_dir, build_dir/'plant-repeat.csv')
    assert rows == again, 'non-deterministic plant trace'
    _, failed = plant(build_dir, build_dir/'both-trip.csv','both-trip')
    assert failed['spill_ml'] > 0 and failed['high_alarm_scans'] > 0 and failed['no_pump_alarm_scans'] > 0
    fault_rows,_ = plant(build_dir, build_dir/'bad-float.csv','bad-float')
    for k,row in enumerate(fault_rows):
        assert row['fs1_off'] == (0 if 400 <= k < 900 else int(row['physical_level_index'] >= 1))
        sensed_invalid = any(row[INPUTS[j]] and not row[INPUTS[j-1]] for j in (1,2,3))
        assert row['invalid_alarm'] == int(sensed_invalid), ('trace input/output mismatch', k, row)
    compare_original(build_dir,build_dir/'original-comparison.csv')
    print('PASS all compiled labs (includes known original-model discrepancy, not equivalence)')


def main():
    if sys.flags.optimize:
        raise SystemExit('Do not run lab tests with Python -O: assertions must remain enabled.')
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command',required=True)
    b = sub.add_parser('build'); b.add_argument('--apply',action='store_true'); b.add_argument('--mutant',choices=MUTANTS)
    b.add_argument('--source',type=Path,help='build a learner COPY of Station, without editing it')
    for name in ('test','foundations','station','compare','replay','plant','mutations'):
        sub.add_parser(name)
    for child in sub.choices.values(): child.add_argument('--build-dir',type=Path,default=DEFAULT_BUILD)
    sub.choices['replay'].add_argument('scenario',type=Path)
    for name in ('replay','plant','compare'):
        sub.choices[name].add_argument('--output',type=Path)
    sub.choices['plant'].add_argument('--fault',choices=['none','pump1-trip','both-trip','bad-float','blocked-pump1'],default='none')
    sub.choices['mutations'].add_argument('--apply',action='store_true')
    args = p.parse_args(); out = args.build_dir
    if args.command == 'build': build(out,args.apply,args.mutant,args.source)
    elif args.command == 'test': test_all(out)
    elif args.command == 'foundations': foundations(out)
    elif args.command == 'station': station_tests(out)
    elif args.command == 'compare': compare_original(out,args.output or out/'original-comparison.csv')
    elif args.command == 'replay': replay(out,args.scenario,args.output or out/'replay.csv')
    elif args.command == 'plant': plant(out,args.output or out/'plant.csv',args.fault)
    elif args.command == 'mutations':
        if not args.apply:
            print(f'DRY RUN: would build and test 3 deliberately faulty copies under {out}/mutants/. Use --apply.')
            return
        for mutant in MUTANTS:
            folder = out/'mutants'/mutant
            build(folder,True,mutant)
            try: station_tests(folder)
            except AssertionError as e: print('KILLED',mutant,repr(e))
            else: raise AssertionError('SURVIVED mutant '+mutant)
        print('PASS mutations: all 3 compiled faults rejected')


if __name__ == '__main__':
    main()
