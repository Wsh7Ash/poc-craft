---
name: regression-verify-fix
description: "Re-run the exact reproducer on the fixed build and report the result, because a fix that changes behaviour elsewhere may not address the finding. Use when the client reports that the issue is fixed"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [regression, fix, verification]
phase: regression
---

# Verify the fix against the original reproducer

> Re-run the exact reproducer on the fixed build and report the result, because a fix that changes behaviour elsewhere may not address the finding

**Use when:** the client reports that the issue is fixed

**Avoid when:** the fix is not deployed to an environment you can reach

## Procedure

1. Run the original minimised input and oracle against the fixed build.
2. Confirm the oracle now returns false and record the new response.
3. Check that the benign control still behaves as before, so the fix did not simply block the endpoint.
4. Run the sibling endpoints from the fix scope, since a fix is often partial.

## Signals

- original-reproducer-run
- oracle-now-false
- siblings-checked

## Patterns

**1. post-fix run**

```
python poc.py; echo "exit=$?"   # expect non-zero after the fix
python control.py; echo "control exit=$?"
```

## Pitfalls

- Accepting a fix because the endpoint now returns 403 for everyone, which is a regression not a fix.
- Testing only the reported endpoint and leaving the sibling with the same defect open.

## Done when

- The original reproducer no longer satisfies the oracle and the control is unchanged.
- Sibling endpoints from the fix scope are checked and reported.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
