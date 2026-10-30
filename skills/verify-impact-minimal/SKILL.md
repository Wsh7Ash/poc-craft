---
name: verify-impact-minimal
description: "Check the weakest effect the bug proves and report that, rather than extrapolating to the worst case the bug might allow. Use when the bug could plausibly lead to something larger but you only observed a small effect"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [verify, impact, honesty]
phase: verify
---

# Verify the smallest impact claim you can defend

> Check the weakest effect the bug proves and report that, rather than extrapolating to the worst case the bug might allow

**Use when:** the bug could plausibly lead to something larger but you only observed a small effect

**Avoid when:** the larger effect was directly observed and evidenced

## Procedure

1. Write the impact you directly observed as one sentence with its evidence.
2. Write the impact you infer, clearly separated and labelled as inference.
3. Check whether one more low-risk request would confirm the inference; if not, leave it as inference.
4. Keep the inferential sentence out of the summary line and in a clearly marked section.

## Signals

- observed-impact-written
- inference-separated
- confirmation-attempted

## Patterns

**1. observed impact**

```
grep -q '"owner":"victim-tenant"' response.json && echo 'observed: cross-tenant read of one record'
```

## Pitfalls

- Reporting full account takeover when a single cross-tenant read was observed.
- Hiding the inference entirely, which undersells a real bug; separating it is better than dropping it.

## Done when

- Observed impact and inference are written as separate statements.
- Any attempt to confirm the inference is recorded with its result.

## References

- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
