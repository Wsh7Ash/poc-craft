---
name: minimize-preserve-preconditions
description: "Pin account state, headers and sequence so a minimiser does not remove the context that makes the payload meaningful. Use when the trigger needs a specific account, header or ordering that sits outside the payload"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, preconditions, context]
phase: minimize
---

# Keep the preconditions the minimiser cannot see

> Pin account state, headers and sequence so a minimiser does not remove the context that makes the payload meaningful

**Use when:** the trigger needs a specific account, header or ordering that sits outside the payload

**Avoid when:** the payload alone is the whole trigger and no external state is involved

## Procedure

1. List every precondition outside the payload: account role, feature flag, header and prior request.
2. Fix those in the harness so minimisation only varies the payload.
3. Re-test the minimised payload against the fixed harness and then against the real environment.
4. Report the preconditions as part of the finding, because a payload alone does not reproduce.

## Signals

- preconditions-pinned
- harness-fixed
- real-environment-confirmed

## Patterns

**1. pinned context**

```
curl -sS -H "Authorization: Bearer $ADMIN_TOKEN" -H 'X-Tenant: t-42' --data-binary @"$1" https://api.example.com/v2/admin/import
```

## Pitfalls

- Minimising away the admin token and then reporting a bug that needs admin rights as if it were unauthenticated.
- Leaving the tenant header out of the harness so the bug reproduces only in one tenant by accident.

## Done when

- Every external precondition is fixed in the harness and stated in the report.
- The minimised payload reproduces in the real environment with those preconditions.

## References

- [Zeller & Hildebrandt, simplifying failure-inducing input](https://doi.org/10.1109/32.988710)
