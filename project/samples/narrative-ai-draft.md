# Control narrative: Demo Lift Station (AI first draft)

SYNTHETIC. An AI wrote this from a one-line description, with no interview. It is fluent. It contains errors a panel builder would catch. Module 1 asks you to find them.

## Sequence of operation

1. The station has two submersible pumps, Pump 1 and Pump 2, controlled by four float switches in the wet well: Off, Lead, Lag and High.
2. When the level rises to the Lead float, the lead pump starts.
3. When the level falls below the Lead float, the lead pump stops, to avoid running the pump dry.
4. If the level continues to rise to the Lag float, the lag pump starts immediately to prevent overflow.
5. The lead and lag pumps alternate each time a pump starts so that wear is equalized.
6. If a pump has a seal failure, the pump continues to run until the level reaches the Off float, and the seal-fail alarm is annunciated.
7. If a pump selector is in the Off position, that pump is out of service and the other pump serves as lead.
8. At the High float, the high-level alarm is annunciated and the beacon flashes. The alarm resets automatically when the level drops below the Off float.
9. A Hand position runs the pump while the switch is held.
10. The panel is powered at 460 V, three-phase, with a control power transformer.

## Alarms

High level, seal fail, motor over-temperature.
