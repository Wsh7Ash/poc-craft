---
name: verify-oracle-specific
description: "Check the specific effect the finding claims, such as another tenant's field or a command output, instead of a proxy signal like response length. Use when the finding is about data exposure or command execution rather than a crash"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [verify, oracle, impact]
phase: verify
---

# Tie the oracle to the bug's observable effect

> Check the specific effect the finding claims, such as another tenant's field or a command output, instead of a proxy signal like response length

**Use when:** the finding is about data exposure or command execution rather than a crash

**Avoid when:** the only observable effect genuinely is a crash or a status code

## Procedure

1. Write down the exact observable that the claim depends on, such as field X containing tenant B's value.
2. Assert on that observable with a value only the victim account could produce.
3. Check a value that a benign request cannot return, to avoid a false positive from cached content.
4. Record the raw response that contains the observable.

## Signals

- observable-named
- victim-value-asserted
- raw-response-stored

## Patterns

**1. assert on victim data**

```
grep -q '"owner":"victim-tenant"' response.json && echo reproduced
```

## Pitfalls

- Using response length as the oracle, which changes when the server adds a header or an error hint.
- Asserting on a field the attacker account can also legitimately read.

## Done when

- The oracle asserts on a victim-only value, not a proxy signal.
- The raw response containing it is stored as evidence.

## References

- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
