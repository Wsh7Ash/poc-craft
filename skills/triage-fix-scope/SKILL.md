---
name: triage-fix-scope
description: "Name the component and the check that must change so the report helps the fix without turning into a patch the client did not ask for. Use when the report includes a remediation section"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [triage, fix, scope]
phase: triage
---

# Describe the fix scope without prescribing code

> Name the component and the check that must change so the report helps the fix without turning into a patch the client did not ask for

**Use when:** the report includes a remediation section

**Avoid when:** the client explicitly asked for a patch

## Procedure

1. Identify the component where the check is missing or wrong, using the request path as evidence.
2. State the invariant that should hold, for example every export filter is resolved inside the tenant root.
3. List the sibling endpoints likely to share the defect, marked as unverified.
4. Stop at the invariant; leave the implementation to the owner.

## Signals

- component-named
- invariant-stated
- siblings-listed

## Patterns

**1. fix statement**

```
component: export handler
invariant: resolved path must remain under the tenant export root
suspected siblings: import, backup (unverified)
```

## Pitfalls

- Pasting a patch that touches files you have never compiled.
- Naming the wrong component because the request path differs from the internal handler.

## Done when

- The component and invariant are stated with the evidence that located them.
- Unverified siblings are labelled as such.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
