## Executive summary

Assemble a synthetic duplex-station review packet using the original design tools and the new compiled labs. Your deliverable is a traceable, reproducible classroom design, not a construction package or approved commissioning procedure. Time: 4–6 hours. Prerequisites: Labs 00–07 and original Modules 01–03, 07–10.

## The assignment

A fictional owner asks for the behavior in SPEC R1–R8. Deliver normal operation plus pump-1-trip, both-trip and inconsistent-float scenarios. The owner also asks whether a blocked pump can be detected. Your correct response must identify the absent feedback requirement; do not pretend the current controller diagnoses it.

Use `project/variants/a-baseline.toml` for the original document-generation exercises. The electrical sizing and parts catalog are **unverified** and are separate from the invented plant quantities. You may not turn them into an approved panel design. The new ST contract is not a claim that every option in the older variant system is implemented in the controller.

## Work sequence

1. Read the exact requirement quotes in SPEC. Create a matrix with one row per R1–R8, code location, test and limitation. Add a proposed feedback requirement, marked HUMAN DECISION PENDING, without implementing it.
2. Generate and inspect the original I/O list and BOM. Compare their engineering intent with the narrower simulation interface; document missing feedback, Hand mode, acknowledgement and real addresses.
3. Build and run the compiled controller. Preserve source hashes and failing mutation evidence.
4. Run the closed-loop scenarios. Identify normal drainage, fallback, spill and what the alarm signals do and do not prove.
5. Run the old/new model comparison. Explain the timing discrepancy without changing the old model to hide it.
6. Hand the packet to a fresh learner agent or another learner. Repair missing instructions and rerun affected steps. Human review still remains.

Commands for a reference submission:

```sh
mkdir -p scratch/capstone
python3 project/tools/apd.py check project/variants/a-baseline.toml
python3 project/tools/apd.py io project/variants/a-baseline.toml > scratch/capstone/io.csv
python3 project/tools/apd.py bom project/variants/a-baseline.toml > scratch/capstone/bom.csv
python3 scripts/lab.py build --apply
python3 scripts/lab.py test
python3 scripts/lab.py mutations --apply
python3 scripts/lab.py plant --fault pump1-trip --output build/reference/pump1-trip.csv
python3 scripts/lab.py plant --fault both-trip --output build/reference/both-trip.csv
python3 scripts/lab.py plant --fault bad-float --output build/reference/bad-float.csv
python3 scripts/lab.py plant --fault blocked-pump1 --output build/reference/blocked-pump1.csv
./check.sh
```

The BOM file begins with an unverified banner; it is not a clean procurement CSV. Keep that disclosure. The reference scenario/solution files are a starting point for comparison, not a substitute for your own review.

## Assessment rubric, 100 points

| Evidence | Points | Observable standard |
|---|---:|---|
| Requirements and safety boundary | 20 | Exact quotes/sections, synthetic policy identified, unsigned human decisions |
| Working compiled logic | 20 | Fresh native build, hashes, normal/fault traces; no Python-runtime mislabeling |
| Timing and state | 15 | 499/500 ms and 4900/5000 ms reasoning, alternation, reset, chatter |
| Fault finding and repair | 15 | Three compiled mutations rejected; one copied repair with before/after evidence |
| Closed-loop reasoning | 15 | Repeatable plant, spill reported, command versus feedback distinguished |
| Agent review discipline | 10 | Evidence packet, fresh learner findings, missing steps repaired |
| Communication | 5 | Plain-language disclosure, absolute artifact paths, NOT VERIFIED list |

Passing classroom score: 80/100 **and** no hard-rule violation. A score cannot sign engineering gates. Any fabricated execution, live-device action, false verification flag or forged gate signature invalidates the submission.

## Reference answer and extension

See [solutions](solutions/README.md) after submitting predictions. The reference controller and tests implement the explicit contract. A stretch assignment can add a simulated run-feedback timeout, but first write the proposed contract, quote the approved classroom requirement, and create a new program copy. Do not infer a real timeout from these invented volumes or scan counts. This extension is **NOT IMPLEMENTED / NOT VERIFIED** here.

## Final handoff

List what was executed, what was only written and what cannot be determined. Ask the human to review the synthetic contract and the missing production features. Stop; no deployment, hardware download, code-table verification or gate signature is part of the capstone.
