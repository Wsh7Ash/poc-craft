---
name: regression-closeout-note
description: "Record the fix version, the verification result and the residual risk in one note, so the finding can be closed without rereading the whole thread. Use when the finding is verified fixed and the ticket is being closed"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [regression, closeout, record]
phase: regression
---

# Close the finding with what changed

> Record the fix version, the verification result and the residual risk in one note, so the finding can be closed without rereading the whole thread

**Use when:** the finding is verified fixed and the ticket is being closed

**Avoid when:** the finding is still open or disputed

## Procedure

1. Record the build or version where the fix was observed.
2. State the verification result for the original reproducer and the sibling sweep.
3. Name any residual risk, such as a route that was not reachable for testing.
4. Link the fixture and the post-fix capture so the note is self-contained.

## Signals

- fix-version-recorded
- verification-summarised
- residual-risk-named

## Patterns

**1. closeout**

```
fix verified in build 2026.11.2
original reproducer: blocked (403)
sibling sweep: 2 blocked, 1 unverified (route disabled)
residual: import route untested
```

## Pitfalls

- Closing with fixed without naming the version, which makes the claim untraceable.
- Omitting the residual risk so a later regression looks like a new finding.

## Done when

- The fix version, verification result and residual risk are recorded.
- The note links to the fixture and the post-fix capture.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
