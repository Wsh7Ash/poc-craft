---
name: report-impact-statement
description: "State what you saw, then what it could lead to, in two labelled paragraphs, so the reader can rate the finding on evidence. Use when the observed effect is smaller than the plausible worst case"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [report, impact, honesty]
phase: report
---

# Separate observed impact from inferred impact

> State what you saw, then what it could lead to, in two labelled paragraphs, so the reader can rate the finding on evidence

**Use when:** the observed effect is smaller than the plausible worst case

**Avoid when:** the worst case was directly observed and needs no separation

## Procedure

1. Write the observed impact with the artifact that proves it.
2. Write the inferred impact under a separate heading and name the assumption it depends on.
3. Say what would be needed to confirm the inference.
4. Keep the two paragraphs physically separate so they cannot be read as one claim.

## Signals

- observed-labelled
- inferred-labelled
- assumption-named

## Patterns

**1. impact**

```
Observed: one record from tenant B was returned to a tenant A user.
Inferred: with a valid record id the same request would return any tenant's record.
Assumption: ids are sequential.
```

## Pitfalls

- Blending the two into one paragraph so the inference reads as observed.
- Dropping the inference, which undersells a real bug and invites a low rating.

## Done when

- Observed and inferred impacts are separate and each names its basis.
- The confirmation step for the inference is stated.

## References

- [CVSS specification](https://www.first.org/cvss/v4-0/specification-document)
