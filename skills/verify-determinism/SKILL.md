---
name: verify-determinism
description: "Repeat the proof under identical conditions and state whether it reproduces every time, most times or only with a described setup. Use when you are about to write a report sentence containing always, sometimes or occasionally"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [verify, determinism, reliability]
phase: verify
---

# Show the result is deterministic or quantify it

> Repeat the proof under identical conditions and state whether it reproduces every time, most times or only with a described setup

**Use when:** you are about to write a report sentence containing always, sometimes or occasionally

**Avoid when:** the finding is explicitly about a one-shot condition that cannot be repeated

## Procedure

1. Define the exact conditions of one attempt, including state reset.
2. Run at least five attempts and record each outcome.
3. Compute the rate and describe any condition that separates hits from misses.
4. Write the report sentence from the measurement rather than from memory.

## Signals

- conditions-defined
- attempts-recorded
- rate-stated

## Patterns

**1. ten attempts**

```
for i in $(seq 1 5); do python poc.py >/dev/null 2>&1; echo "attempt $i exit=$?"; done
```

## Pitfalls

- Writing always reproducible after a single successful run.
- Resetting state between attempts for one test and not the other, which makes the rates incomparable.

## Done when

- At least five attempts are recorded under defined conditions.
- The report states a rate and any separating condition.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
