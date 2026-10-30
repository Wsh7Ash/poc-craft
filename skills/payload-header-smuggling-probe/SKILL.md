---
name: payload-header-smuggling-probe
description: "Test whether a proxy and an origin disagree about a header by sending a syntactically valid request and reading which one acts on it. Use when a request passes through a CDN or reverse proxy before reaching the application"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [payload, headers, proxy]
phase: payload
---

# Probe header handling without breaking the request

> Test whether a proxy and an origin disagree about a header by sending a syntactically valid request and reading which one acts on it

**Use when:** a request passes through a CDN or reverse proxy before reaching the application

**Avoid when:** there is no intermediary and headers are read by a single server

## Procedure

1. Identify the intermediary from response headers such as server and via, and record it.
2. Send a request with one header expressed exactly once, then with a duplicated form, and compare which value takes effect.
3. Use a behaviour you can observe, such as a reflected value or a routing decision, rather than guessing.
4. Report the disagreement between hops, naming both observed values.

## Signals

- intermediary-identified
- values-compared
- disagreement-shown

## Patterns

**1. duplicate header probe**

```
curl -sS -i https://app.example.com/echo \
  -H 'X-Forwarded-Host: a.example' \
  -H 'X-Forwarded-Host: b.example'
```

## Pitfalls

- Crafting a request that neither hop parses, then reporting the resulting error as a vulnerability.
- Assuming a CDN strips a header because the response did not reflect it; reflection and routing differ.

## Done when

- Both hops are identified and their handling of the header is compared with observed evidence.
- The disagreement is stated with the values each hop used.

## References

- [RFC 9110 HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110)
