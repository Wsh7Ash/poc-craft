---
name: minimize-predicate-design
description: "Tie the oracle to the specific behaviour the bug causes, so minimisation cannot drift into a different failure that happens to exit non-zero. Use when you are about to hand a predicate to a minimiser or a regression suite"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, oracle, predicate]
phase: minimize
---

# Write a predicate that cannot be gamed

> Tie the oracle to the specific behaviour the bug causes, so minimisation cannot drift into a different failure that happens to exit non-zero

**Use when:** you are about to hand a predicate to a minimiser or a regression suite

**Avoid when:** any observable difference is acceptable, for example when searching for any crash at all

## Procedure

1. Write the oracle as a check on a specific status code, body marker or state change, not on any error.
2. Assert the oracle fails on a benign input, which proves it is not just detecting malformed requests.
3. Run the predicate twice on the same input and confirm it is stable before minimising.
4. Record the predicate source next to the payload so a reviewer can judge the oracle.

## Signals

- oracle-specific
- negative-control-fails
- predicate-stable

## Patterns

**1. strict oracle**

```
status=$(curl -sS -o body.txt -w '%{http_code}' --data-binary @"$1" https://api.example.com/v2/items)
[ "$status" = "500" ] && grep -q 'stack trace' body.txt
```

## Pitfalls

- Using a predicate that passes on any 4xx, so minimisation reduces toward a request the server rejects for syntax.
- A predicate that depends on a timestamp or a random value and therefore flips between runs.

## Done when

- The oracle names the exact behaviour and fails on a benign input.
- Two consecutive runs agree on the same input.

## References

- [Zeller & Hildebrandt, simplifying failure-inducing input](https://doi.org/10.1109/32.988710)
