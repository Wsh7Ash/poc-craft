---
name: harness-timeout-and-retry
description: "Set an explicit timeout and disable automatic retries so a hung or retried request is visible as a failure rather than as a slow success. Use when the target is remote, slow or behind a load balancer"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [harness, timeout, retries]
phase: harness
---

# Bound every request with a timeout and no silent retry

> Set an explicit timeout and disable automatic retries so a hung or retried request is visible as a failure rather than as a slow success

**Use when:** the target is remote, slow or behind a load balancer

**Avoid when:** the bug is a timeout itself, where retries must be part of the measurement

## Procedure

1. Set a connect and read timeout on every request in the harness.
2. Disable automatic retry so one attempt produces one request in the server log.
3. Record the elapsed time per attempt alongside the outcome.
4. Correlate the harness attempt count with the server's access log to prove no hidden retries.

## Signals

- timeouts-set
- retries-disabled
- attempts-correlated

## Patterns

**1. timeout**

```
urllib.request.urlopen(request, timeout=15)
```

## Pitfalls

- A client library that retries on 503 turns one logical attempt into three requests and triples the impact.
- No timeout at all, so a hung connection looks like the harness is still running.

## Done when

- Every request has a timeout and retries are disabled or counted.
- The harness attempt count matches the server's request count.

## References

- [urllib.request timeout](https://docs.python.org/3/library/urllib.request.html)
