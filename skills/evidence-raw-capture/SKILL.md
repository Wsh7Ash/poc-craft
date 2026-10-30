---
name: evidence-raw-capture
description: "Store the exact bytes of the request and response with their headers, because a screenshot cannot be replayed and cannot be diffed. Use when the evidence will be attached to a report or a ticket"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [evidence, capture, raw]
phase: evidence
---

# Capture raw requests and responses, not screenshots

> Store the exact bytes of the request and response with their headers, because a screenshot cannot be replayed and cannot be diffed

**Use when:** the evidence will be attached to a report or a ticket

**Avoid when:** the client's platform only accepts images and you have already stored the raw form

## Procedure

1. Capture the full request including method, path, headers and body bytes.
2. Capture the full response including status line, headers and body bytes.
3. Store both with a timestamp and the account used.
4. Redact secrets in a copy, keeping the original intact in a controlled location.

## Signals

- request-bytes-stored
- response-bytes-stored
- redaction-separated

## Patterns

**1. raw capture**

```
curl -sS -D response.headers -o response.body -X POST https://api.example.com/v2/export --data-binary @payload.json
sha256sum payload.json response.headers response.body
```

## Pitfalls

- A screenshot of a response with the request invisible, so the reader cannot tell how it was produced.
- Redacting the original instead of a copy, which destroys the evidence.

## Done when

- Raw request and response bytes are stored with hashes.
- Any redacted copy is separate from the original.

## References

- [curl write-out](https://curl.se/docs/manpage.html)
