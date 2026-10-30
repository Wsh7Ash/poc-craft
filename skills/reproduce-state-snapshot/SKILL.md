---
name: reproduce-state-snapshot
description: "Record the account and resource state the reproduction starts from, so a later reviewer can tell whether the bug needed that state or created it. Use when the finding depends on data created earlier in the engagement"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, state, snapshot]
phase: reproduce
---

# Snapshot state before the reproduction

> Record the account and resource state the reproduction starts from, so a later reviewer can tell whether the bug needed that state or created it

**Use when:** the finding depends on data created earlier in the engagement

**Avoid when:** the reproduction is stateless and starts from an empty account every time

## Procedure

1. List the resources the request will read or write and fetch their current representation.
2. Store the snapshot with a hash and a timestamp before sending the triggering request.
3. After the request, fetch the same resources again and diff the two snapshots.
4. Keep both snapshots, since the diff is the impact evidence and the before-state proves the precondition.

## Signals

- pre-state-captured
- post-state-captured
- diff-computed

## Patterns

**1. snapshot**

```
curl -sS -H "Authorization: Bearer $TOKEN" https://api.example.com/v2/items/42 > before.json
sha256sum before.json
```

## Pitfalls

- Capturing only the after-state, which makes it impossible to show what changed.
- Comparing snapshots taken against different accounts or tenants.

## Done when

- Pre and post snapshots exist with hashes and timestamps.
- The diff between them is recorded as impact evidence.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
