## Executive summary

This fourth case uses BearBrown's general testing and debugging skills as an **adjacent, transferable workflow**, not a PLC-specific product. The interesting question is whether an agent can show that its test detects wrong native control behavior and that its repair removes the cause. We execute the local mutation/repair workflow; we do not claim the source skills are compilers or that the entire course was developed test-first.

## Source and problem

Read definitions at `/Users/bear/Documents/CoWork/bear-textbooks/books/bearbrown_co/content/skills/test-driven-development/SKILL.md` and `/Users/bear/Documents/CoWork/bear-textbooks/books/bearbrown_co/content/skills/systematic-debugging/SKILL.md`. Their front matter identifies MIT licensing. Public entries: [test-driven development](https://bearbrown.co/skills/test-driven-development), [systematic debugging](https://bearbrown.co/skills/systematic-debugging). The source text is not copied here.

A green test can be meaningless if it never runs the changed code. A quick patch can hide a symptom while leaving a timing error. The adapted workflow uses source hashes, a freshly compiled binary, a deliberately wrong program and an unchanged behavioral test.

## Run the adaptation

```sh
python3 scripts/lab.py mutations
python3 scripts/lab.py mutations --apply
```

Expected: three compiled faults rejected. Follow [Lab 05](../labs/05-break-test-repair.md) to repair a copied zero-delay program. Keep the original failure, exact contract quote, minimal diff and passing rerun. The specific reasoning is: R5 requires five elapsed seconds; `PT := T#0s` cannot meet that requirement; restoring the copied preset changes behavior without altering the test.

The original Python/ST discrepancy is a second case: reproduce its two rows, trace time credit back to the first TRUE scan, and report a contract decision rather than automatically changing an expected output. This is a diagnosis exercise, not permission to change a customer's sequencing.

## Verification and limits

Actual local execution is in [VERIFICATION.md](../labs/VERIFICATION.md), with the independent learner's report alongside it. Compiler failure, test failure and expected plant failure are different outcomes and must be labeled separately. The mutation suite provides rejection evidence for three defects; it is not proof of universal test coverage. The upstream skill protocols were read as source material, not installed as executable software. Human review and all engineering gates remain unsigned.

## Your turn

Propose a fourth mutation and its smallest counterexample before changing a copied program. If the current tests miss it, add a requirement-backed test, observe failure, then repair the copy and rerun. Record whether the defect was a missing requirement, a code bug, or a weak test. Do not add production features merely to increase the number of tests.

## Attribution trail

BearBrown's catalog identifies [Jesse Vincent's obra/superpowers testing skill](https://github.com/obra/superpowers/blob/44c9b2d6e889982ac18c27d05a19fefe335194e1/skills/test-driven-development/SKILL.md) and [debugging skill](https://github.com/obra/superpowers/blob/44c9b2d6e889982ac18c27d05a19fefe335194e1/skills/systematic-debugging/SKILL.md), MIT, as primary bases for its rewritten protocols. The catalog also records additional sources; see the machine-readable attribution record alongside the inventory. Our exercise is newly written, and no source skill implementation/text is bundled.
