---
name: minimize-ddmin
description: "Shrink the input while the bug still reproduces, so the report contains the smallest trigger instead of a wall of irrelevant bytes. Use when the payload is large and you do not know which part is load-bearing"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, ddmin, payload]
phase: minimize
---

# Minimise a payload with delta debugging

> Shrink the input while the bug still reproduces, so the report contains the smallest trigger instead of a wall of irrelevant bytes

**Use when:** the payload is large and you do not know which part is load-bearing

**Avoid when:** the payload is a single field whose value is already the minimum

## Procedure

1. Write a predicate that exits 0 exactly when the bug reproduces, and test it on the original payload.
2. Run the minimiser with line units first, then byte units if the result is still large.
3. Confirm the minimised input still reproduces from a clean session, not just from the harness.
4. Store the minimised payload with the predicate used, so the reduction is reproducible.

## Signals

- predicate-stable
- reduction-measured
- reproduce-reconfirmed

## Patterns

**1. minimise**

```
poc-craft minimize --input payload.bin --predicate './check.sh {input}' --unit line --out minimal.bin
```

## Pitfalls

- A predicate that matches on an error message the server returns for malformed input, which shrinks toward garbage that was never the bug.
- Trusting a minimised input without re-running it from a clean session.

## Done when

- The predicate was verified on the original input before minimising.
- The minimised input reproduces and its size reduction is recorded.

## References

- [Zeller & Hildebrandt, simplifying failure-inducing input](https://doi.org/10.1109/32.988710)
