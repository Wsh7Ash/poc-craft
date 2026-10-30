---
name: scope-minimal-impact
description: "Decide the weakest action that still proves the finding, so the proof does not read data, send mail or change state it does not have to. Use when a finding could be demonstrated by either reading or writing and both are available"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [scope, impact, restraint]
phase: scope
---

# Choose the least invasive way to demonstrate impact

> Decide the weakest action that still proves the finding, so the proof does not read data, send mail or change state it does not have to

**Use when:** a finding could be demonstrated by either reading or writing and both are available

**Avoid when:** the vulnerability only manifests through the destructive path and the client has authorised that path

## Procedure

1. List the actions the bug would allow, ordered from read-only to state-changing.
2. Pick the first action that is distinguishable from normal behaviour and record why the weaker ones fail.
3. Bound the blast radius: one record, one message, one file, never a loop over real data.
4. State the chosen boundary in the report so the client can see what was and was not touched.

## Signals

- actions-enumerated
- weakest-chosen
- radius-bounded

## Patterns

**1. read-only proof**

```
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' https://api.example.com/v2/users/2
```

## Pitfalls

- Deleting a real record to prove an IDOR when reading one record proves the same access.
- Sending mail to a real address to prove injection when a controlled inbox would do.

## Done when

- The weakest sufficient action is chosen and justified.
- The blast radius is stated in the report.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
