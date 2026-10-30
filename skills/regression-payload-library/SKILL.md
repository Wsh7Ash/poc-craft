---
name: regression-payload-library
description: "Store the minimised payload and its predicate in a fixture directory with a revision, so later findings can reuse and compare against it. Use when the same class of bug is likely to recur across endpoints"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [regression, fixtures, reuse]
phase: regression
---

# Keep the payload as a versioned fixture

> Store the minimised payload and its predicate in a fixture directory with a revision, so later findings can reuse and compare against it

**Use when:** the same class of bug is likely to recur across endpoints

**Avoid when:** the payload contains live credentials or personal data

## Procedure

1. Store the minimised payload with a name that encodes the defect class and endpoint.
2. Store the predicate beside it and a one-line note on what reproduction looks like.
3. Record the target version it was verified against.
4. Reference the fixture from the report instead of inlining the payload twice.

## Signals

- fixture-stored
- predicate-paired
- version-recorded

## Patterns

**1. fixture layout**

```
fixtures/export-traversal/
  payload.json
  check.sh
  note.md   (verified against build 2026.10.30)
```

## Pitfalls

- Naming fixtures by date only, so nobody can tell what defect class they exercise.
- Reusing a payload against a new version without re-verifying it.

## Done when

- The payload, predicate and target version are stored together.
- The report references the fixture rather than duplicating it.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
