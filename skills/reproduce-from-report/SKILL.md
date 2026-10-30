---
name: reproduce-from-report
description: "Rebuild the stated preconditions from a written report before adding anything, so the reproduction is of the reported bug and not a neighbour. Use when you are verifying a report you did not write, including your own from an earlier session"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, verification, handoff]
phase: reproduce
---

# Reproduce a finding from someone else's report

> Rebuild the stated preconditions from a written report before adding anything, so the reproduction is of the reported bug and not a neighbour

**Use when:** you are verifying a report you did not write, including your own from an earlier session

**Avoid when:** the report already includes a runnable harness and your job is only to execute it

## Procedure

1. Extract every precondition the report states: account state, feature flags, data shape and request order.
2. Recreate them exactly and run the reported steps without improvising.
3. Record whether the result matches the report, including partial matches.
4. Report a difference as a difference, not as a failed reproduction, until you have ruled out drift.

## Signals

- preconditions-recreated
- steps-followed
- match-recorded

## Patterns

**1. replay recorded request**

```
curl -sS -X POST https://api.example.com/v2/items \
  -H 'Content-Type: application/json' \
  --data-binary @reported-body.json
```

## Pitfalls

- Improving the steps while reproducing, which makes the result unattributable to the report.
- Assuming a mismatch means the report is wrong when a feature flag or data shape changed.

## Done when

- Every stated precondition is recreated and recorded.
- The outcome is classified as match, partial or mismatch with evidence.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
