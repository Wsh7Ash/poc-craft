---
name: triage-severity-evidence
description: "Map each severity claim to an artifact, so a high rating rests on observed access rather than on a plausible chain of guesses. Use when you are about to assign a severity rating"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [triage, severity, evidence]
phase: triage
---

# Justify severity with the evidence you actually have

> Map each severity claim to an artifact, so a high rating rests on observed access rather than on a plausible chain of guesses

**Use when:** you are about to assign a severity rating

**Avoid when:** the platform assigns severity automatically from the finding type

## Procedure

1. Write the impact sentence first, then the severity it implies.
2. Attach the artifact that proves each clause of the sentence.
3. Downgrade any clause without an artifact to an inference, and rate the observed part.
4. Record the rating rationale in the report so a disagreement can be about facts.

## Signals

- impact-written
- artifacts-mapped
- inferences-downgraded

## Patterns

**1. mapping**

```
impact: read one record from another tenant
evidence: response.body (owner=victim-tenant)
severity basis: cross-tenant confidentiality, single record
```

## Pitfalls

- Rating critical on a chain that was never executed end to end.
- Leaving the severity basis implicit, so the first reviewer to disagree cannot see what was assumed.

## Done when

- Every severity clause maps to an artifact or is labelled inference.
- The rating basis is written in the report.

## References

- [CVSS specification](https://www.first.org/cvss/v4-0/specification-document)
