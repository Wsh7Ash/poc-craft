---
name: automate-bounded-loop
description: "Loop over candidate identifiers with a maximum count, a delay and a stop condition, so automation cannot walk a production table. Use when the finding needs a sample of identifiers to show a pattern"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [automate, enumeration, bounds]
phase: automate
---

# Automate enumeration with a hard bound

> Loop over candidate identifiers with a maximum count, a delay and a stop condition, so automation cannot walk a production table

**Use when:** the finding needs a sample of identifiers to show a pattern

**Avoid when:** a single request already proves the finding

## Procedure

1. Set a maximum iteration count that is small enough to be defensible, such as ten.
2. Add a delay between requests and record it.
3. Stop on the first unexpected response so the loop does not continue past an anomaly.
4. Record the exact range attempted, so the blast radius is a fact rather than an estimate.

## Signals

- bound-set
- delay-recorded
- range-recorded

## Patterns

**1. bounded enumeration**

```
for i in $(seq 1 10); do
  curl -sS -o /dev/null -w "$i %{http_code}\n" -H "Authorization: Bearer $T" https://api.example.com/v2/items/$i
  sleep 0.5
done
```

## Pitfalls

- An unbounded loop over sequential IDs that touches thousands of real records.
- No delay, so the automation trips a rate limit and the 429s are misread as access control working.

## Done when

- The loop has a maximum count, a delay and a stop condition.
- The attempted range is recorded exactly.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
