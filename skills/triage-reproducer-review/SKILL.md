---
name: triage-reproducer-review
description: "Run the reproducer from a clean machine using only what the report contains, so any missing step is found before the triager finds it. Use when the report is written and about to be submitted"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [triage, review, clarity]
phase: triage
---

# Review the reproducer as a stranger would

> Run the reproducer from a clean machine using only what the report contains, so any missing step is found before the triager finds it

**Use when:** the report is written and about to be submitted

**Avoid when:** the reproducer requires access the reviewer will obviously have

## Procedure

1. Copy only the report's reproduction section into a fresh directory.
2. Run it without opening any other notes, and note the first point where you need information that is not there.
3. Fix the report rather than the environment, then re-run from scratch.
4. Record that the clean run succeeded, including the environment used.

## Signals

- clean-dir-run
- missing-step-found
- report-fixed

## Patterns

**1. clean run**

```
tmp=$(mktemp -d) && cd "$tmp" && cp /path/to/submission/* . && python poc.py
```

## Pitfalls

- Running from your working directory where the extra file happens to exist.
- Silently fixing the environment, which leaves the report unusable for the next reader.

## Done when

- The reproducer runs from a clean directory using only submitted files.
- Any missing step found was added to the report, not worked around.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
