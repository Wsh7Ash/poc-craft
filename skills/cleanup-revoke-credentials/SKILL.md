---
name: cleanup-revoke-credentials
description: "Invalidate tokens, API keys and sessions created during the engagement so a leaked attachment cannot be used later. Use when the engagement created credentials or captured tokens in evidence"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [cleanup, credentials, revocation]
phase: cleanup
---

# Revoke every credential the test minted

> Invalidate tokens, API keys and sessions created during the engagement so a leaked attachment cannot be used later

**Use when:** the engagement created credentials or captured tokens in evidence

**Avoid when:** the credentials belong to the client and are still needed for verification

## Procedure

1. List every token, key and session created or captured, with its scope and expiry.
2. Revoke each one through the documented endpoint and record the response.
3. Attempt one request with a revoked token to confirm it now fails.
4. Record the revocation time with the evidence so the window is known.

## Signals

- credentials-listed
- revocation-confirmed
- reuse-blocked

## Patterns

**1. revoke**

```
curl -sS -X POST -H "Authorization: Bearer $TOKEN" https://api.example.com/v2/tokens/revoke -d '{"token":"..."}'
```

## Pitfalls

- Revoking the API key but leaving a refresh token that can mint a new one.
- Leaving a token in a submitted attachment after the engagement closes.

## Done when

- Every created or captured credential is revoked and a reuse attempt fails.
- The revocation time is recorded with the evidence.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
