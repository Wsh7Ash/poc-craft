---
name: isolate-variable-bisect
description: "Change one field at a time across the request so the claim names the parameter that causes the bug instead of the request that contains it. Use when a request triggers the bug but you cannot say which field is responsible"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [isolate, bisect, variables]
phase: isolate
---

# Bisect the input to find the triggering variable

> Change one field at a time across the request so the claim names the parameter that causes the bug instead of the request that contains it

**Use when:** a request triggers the bug but you cannot say which field is responsible

**Avoid when:** the bug requires several fields to change together, which a one-at-a-time bisect cannot show

## Procedure

1. List every field in the request and the value used in the successful reproduction.
2. Revert one field to a benign value, resend, and record whether the bug still triggers.
3. Keep the fields whose reversion stops the bug and discard the rest.
4. State the minimal set of fields and values in the report rather than the whole request.

## Signals

- fields-enumerated
- one-at-a-time-run
- minimal-set-identified

## Patterns

**1. bisect a field**

```
curl -sS -X POST https://api.example.com/v2/export -d '{"format":"csv","filter":"../"}'
curl -sS -X POST https://api.example.com/v2/export -d '{"format":"csv","filter":"safe"}'
```

## Pitfalls

- Changing two fields in one iteration, which makes the result unattributable.
- Assuming the first field that breaks it is the only one that can, when the service accepts several paths.

## Done when

- Every field was reverted individually at least once.
- The minimal triggering field set is stated in the report.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
