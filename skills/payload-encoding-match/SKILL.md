---
name: payload-encoding-match
description: "Send the payload in the encoding the endpoint parses, so a rejected request is not mistaken for a blocked attack. Use when the endpoint accepts several content types or the value passes through a proxy"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [payload, encoding, parsing]
phase: payload
---

# Match the encoding the server actually decodes

> Send the payload in the encoding the endpoint parses, so a rejected request is not mistaken for a blocked attack

**Use when:** the endpoint accepts several content types or the value passes through a proxy

**Avoid when:** the finding is specifically about encoding confusion between two parsers

## Procedure

1. Read the endpoint's accepted content types and pick the one whose parser you want to exercise.
2. Encode the payload for that parser, including escaping rules and charset, and record the exact bytes.
3. Compare the server's decoded view with what you sent, using a reflection or echo field where one exists.
4. Test the second parser only as a deliberate confusion test, labelled as such.

## Signals

- content-type-matched
- bytes-recorded
- decoded-view-compared

## Patterns

**1. explicit content type**

```
curl -sS -X POST https://api.example.com/v2/import \
  -H 'Content-Type: application/json; charset=utf-8' \
  --data-binary @payload.json
```

## Pitfalls

- Sending JSON with a form content type and concluding the payload was blocked when it was never parsed.
- Mixing charset assumptions between the request and the stored value, which changes the decoded bytes.

## Done when

- The request content type and payload bytes are recorded exactly.
- The decoded view is compared against what was sent.

## References

- [MDN Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type)
