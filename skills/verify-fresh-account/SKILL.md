---
name: verify-fresh-account
description: "Repeat the proof with an account created after the harness was written, so the result does not depend on data you happened to have. Use when the proof ran against an account with a long history of test data"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [verify, accounts, freshness]
phase: verify
---

# Verify from a freshly created account

> Repeat the proof with an account created after the harness was written, so the result does not depend on data you happened to have

**Use when:** the proof ran against an account with a long history of test data

**Avoid when:** creating accounts is out of scope or rate limited by the engagement

## Procedure

1. Create a new account with the minimum role the proof requires.
2. Create only the data the proof's preconditions state, and record it.
3. Run the harness unchanged and compare the outcome with the original run.
4. Record both account identifiers and the creation times with the evidence.

## Signals

- fresh-account-created
- minimal-data-created
- outcomes-compared

## Patterns

**1. fresh account**

```
curl -sS -X POST https://api.example.com/v2/signup -d '{"email":"poc+1@your-domain.example"}'
```

## Pitfalls

- Relying on data created by an earlier engagement, which the client cannot reproduce.
- Creating the fresh account with a higher role than the proof needs, which weakens the impact claim.

## Done when

- The proof runs from a newly created, minimally privileged account.
- Both account identifiers and the comparison are recorded.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
