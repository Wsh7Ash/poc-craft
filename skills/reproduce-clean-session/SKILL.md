---
name: reproduce-clean-session
description: "Run the proof with a fresh browser profile or token so cached state, service workers or an old session cannot be the thing that makes it work. Use when the bug reproduces in your browser but not in a script, or only on your machine"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, session, isolation]
phase: reproduce
---

# Reproduce from a clean session

> Run the proof with a fresh browser profile or token so cached state, service workers or an old session cannot be the thing that makes it work

**Use when:** the bug reproduces in your browser but not in a script, or only on your machine

**Avoid when:** the bug is explicitly about persistent state that a clean session removes

## Procedure

1. Clear cookies, local storage, service workers and the cache, or use a fresh profile.
2. Obtain a new token and confirm the account state matches the recorded precondition.
3. Re-run the exact request and compare with the previous result.
4. Record the session origin (fresh profile, API token, script) with the proof.

## Signals

- session-cleared
- fresh-token-used
- result-compared

## Patterns

**1. fresh profile**

```
google-chrome --user-data-dir=$(mktemp -d) --incognito https://app.example.com
```

## Pitfalls

- Concluding the bug is not reproducible when a service worker was still serving a cached response.
- Using a token minted before the precondition was set, so the request runs against stale permissions.

## Done when

- The proof runs from a cleared session and a fresh token.
- The session origin is recorded with the proof.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
