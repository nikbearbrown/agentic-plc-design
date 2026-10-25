# Lift station primer

## Executive summary

A one-page orientation to what a duplex lift station panel does, written so an agent (and a new designer) share the same picture. It covers the sequence of operation, the alarms and the vocabulary used in this course's reference model. It is a teaching summary, not a design standard. The reader who builds these panels for a living is the authority; correct this file where it differs from your shop's practice, and tell the agent.

## What the station does

Wastewater flows by gravity into a **wet well**. Two **pumps** lift it to a higher sewer. The panel decides when each pump runs, based on how full the wet well is, and raises alarms when something is wrong.

## Sequence of operation (the reference model)

Level is sensed by four floats (or a transducer). From lowest to highest: **off**, **lead-on**, **lag-on**, **high**.

1. Level rises to **lead-on**: the **lead** pump starts.
2. The pump keeps running as level falls. It stops only when level drops below **off** (this is *pump-down*). Stopping at the lead float would cause short cycling.
3. If level keeps rising to **lag-on** and stays there for the lag delay (5 seconds in the model; a real station uses the owner's value), the **lag** pump also starts.
4. At **high**, the high-level alarm is raised. Both pumps run if available.
5. When level drops below **off**, both stop and the lead and lag roles **alternate** so wear is shared.
6. A pump that is in Off, has a **seal failure**, or is **over temperature** is not available. The other pump becomes lead. If neither is available, raise a "no pump available" alarm.
7. Floats must be in order. Lead float up while the off float is down means a float is stuck, tangled or failed. Raise a float-fault alarm.

## Alarms in the template

high level, float fault, seal fail (each pump), over-temperature (each pump), and optionally power fail and generator running.

## Hazardous location

Wet wells are often classified as hazardous locations (see NFPA 820 and the adopted electrical code for your jurisdiction). That is why float circuits use **intrinsically safe** relays or barriers: they limit the energy that can reach the well. The template adds IS devices to the BOM when a variant says the well is hazardous. Whether a given well is classified is the engineer's call, not the agent's.

## What varies from job to job (the 10 percent)

Pump horsepower and voltage; starter type (across-the-line, soft start, VFD); level sensing (floats or a 4-20 mA transducer); control platform (relay, PLC, RTU); alarm points; generator or transfer switch; communication to SCADA. This course captures those as a **variant file** (see `project/variants/`).

## What this primer does not cover

Force mains, valve vaults, flow metering, odor control, telemetry design, surge protection, arc flash labeling, and every local utility's own standards. Those are in your head and in your customers' specs; Module 1 is about getting the relevant ones out of your head and into a file the agent reads.
