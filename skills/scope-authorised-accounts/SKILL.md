---
name: scope-authorised-accounts
description: "Create or use accounts inside the agreed tenant and record their identity, so a two-account test never touches a real customer. Use when the finding needs two accounts to demonstrate cross-tenant access"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [scope, accounts, tenancy]
phase: scope
---

# Use accounts you are authorised to control

> Create or use accounts inside the agreed tenant and record their identity, so a two-account test never touches a real customer

**Use when:** the finding needs two accounts to demonstrate cross-tenant access

**Avoid when:** the engagement explicitly supplies accounts and creating new ones would break the agreement

## Procedure

1. Register or receive two accounts in the agreed tenant and record their identifiers and creation time.
2. Confirm both accounts see only their own data before attempting the cross-account request.
3. Attempt the cross-account request and capture both the request and the victim account's view of the data.
4. Delete or disable the accounts at the end if the scope requires it, and record the cleanup.

## Signals

- accounts-recorded
- baseline-isolation-confirmed
- cross-request-captured

## Patterns

**1. two-account check**

```
curl -sS -H "Authorization: Bearer $A" https://api.example.com/v2/me
curl -sS -H "Authorization: Bearer $B" https://api.example.com/v2/users/<a-id>
```

## Pitfalls

- Reusing a colleague's real account as the victim, which turns a test into an incident.
- Skipping the baseline isolation check, so a shared-data design looks like an IDOR.

## Done when

- Both accounts are recorded with identifiers and creation time.
- The cross-account request and the victim's own view are both captured.

## References

- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
