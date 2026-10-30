# Changelog

## 1.0.0 — 2026-10-30

Initial release.

- 50 authored skills across 13 phases: scope, reproduce, isolate, minimize, payload, harness,
  automate, verify, evidence, triage, report, cleanup, regression.
- `ddmin` minimiser over byte or line units with a command predicate, refusal when the predicate
  does not hold on the original input, and a timeout mapped to no-match.
- Harness generator for Python and bash with a validated spec and a builtins-free oracle.
- `validate`, `list`, `show`, `render`, `catalog`, `build` alongside `minimize` and `scaffold`.
- 48 tests including real minimisation runs and compile checks on generated harnesses.
