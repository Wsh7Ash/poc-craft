---
name: report-reproduction-steps
description: "Number the steps so each one has a command, an expected result and the artifact it produces, with no step that assumes unstated state. Use when the report includes a reproduction section"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [report, reproduction, steps]
phase: report
---

# Write reproduction steps that run in order

> Number the steps so each one has a command, an expected result and the artifact it produces, with no step that assumes unstated state

**Use when:** the report includes a reproduction section

**Avoid when:** the finding is demonstrated by a single request that needs no steps

## Procedure

1. Start from account creation or token issuance so the reader has the same starting point.
2. Give each step one command, the expected output and the artifact it should produce.
3. State the environment and version at the top, including any feature flags.
4. End with the step that shows the impact and the artifact that proves it.

## Signals

- ordered-steps
- expected-outputs
- artifacts-linked

## Patterns

**1. step**

```
3. Send the trigger request:
   curl ... --data-binary @payload.json
   expect: HTTP 500 with a stack trace
   artifact: response.body
```

## Pitfalls

- Starting at step 3 because steps 1 and 2 were obvious to you.
- Steps without expected output, so the reader cannot tell a success from a failure.

## Done when

- Every step has a command, an expected result and an artifact.
- The environment and flags are stated before the steps.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
