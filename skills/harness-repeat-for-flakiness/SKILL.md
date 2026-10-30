---
name: harness-repeat-for-flakiness
description: "Run the proof several times and report the hit rate, because a race or a cache that reproduces once in five attempts is a different finding from a deterministic one. Use when the bug involves concurrency, caching or a load balancer"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [harness, flakiness, repetition]
phase: harness
---

# Repeat the run to expose flakiness

> Run the proof several times and report the hit rate, because a race or a cache that reproduces once in five attempts is a different finding from a deterministic one

**Use when:** the bug involves concurrency, caching or a load balancer

**Avoid when:** the bug is deterministic and repetition only costs time

## Procedure

1. Run the proof five times from a clean session for each attempt.
2. Record the outcome of every attempt rather than a summary.
3. If the hit rate is below 100%, describe the condition that correlates with a hit.
4. Report the rate and the condition together, since neither is meaningful alone.

## Signals

- attempts-recorded
- hit-rate-computed
- condition-identified

## Patterns

**1. repeat**

```
poc-craft scaffold --url https://api.example.com/v2/race --payload p.json --repeat 5 --out poc.py
```

## Pitfalls

- Reporting `intermittent` with no rate, which a triager cannot reproduce.
- Reusing one session across attempts so a cache makes later attempts behave differently.

## Done when

- Per-attempt outcomes and a hit rate are recorded.
- Any correlated condition is stated alongside the rate.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
