---
name: reproduce-single-request
description: "Reduce the reproduction to one request that can be pasted into a terminal, because a multi-step script hides which step actually triggers the bug. Use when the bug appears after a sequence of requests but might not need all of them"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, minimal, request]
phase: reproduce
---

# Reproduce with a single request where possible

> Reduce the reproduction to one request that can be pasted into a terminal, because a multi-step script hides which step actually triggers the bug

**Use when:** the bug appears after a sequence of requests but might not need all of them

**Avoid when:** the bug genuinely requires state created by earlier requests and removing them breaks the precondition

## Procedure

1. Capture the full sequence that triggers the bug as raw requests with headers and bodies.
2. Remove one request at a time from the front and re-run, keeping only those that are required.
3. Confirm the surviving single request still triggers the bug from a fresh session.
4. Publish the single request with the exact headers that matter, marked as required or optional.

## Signals

- sequence-captured
- steps-removed
- single-request-confirmed

## Patterns

**1. single request**

```
curl -sS -i -X POST https://api.example.com/v2/export \
  -H 'Authorization: Bearer $TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"format":"csv","filter":"../"}'
```

## Pitfalls

- Keeping a login request in the proof because it was in the original capture, when a token works alone.
- Publishing a request that depends on a session cookie created by steps you removed.

## Done when

- A single request reproduces the bug from a fresh session.
- Required and optional headers are distinguished.

## References

- [curl manual](https://curl.se/docs/manpage.html)
