---
name: payload-path-encoding-layers
description: "Choose percent-encoding, double-encoding or raw separators based on which component parses the path first, so a bypass claim names the layer it defeats. Use when a path-based access control check sits in front of a file read or a route match"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [payload, encoding, path]
phase: payload
---

# Encode path segments for the layer that reads them

> Choose percent-encoding, double-encoding or raw separators based on which component parses the path first, so a bypass claim names the layer it defeats

**Use when:** a path-based access control check sits in front of a file read or a route match

**Avoid when:** the path is normalised once by a single framework before any check runs

## Procedure

1. Determine how many decoding passes the request receives by sending an encoded separator and observing routing.
2. For each pass, construct the encoding that survives it and reaches the sink unchanged.
3. Verify the sink's view with a reflection endpoint or an error message that echoes the resolved path.
4. State the number of passes and the exact bytes used, because the claim depends on both.

## Signals

- pass-count-measured
- encoding-constructed
- sink-view-confirmed

## Patterns

**1. encoding ladder**

```
for p in '..%2fetc%2fpasswd' '..%252fetc%252fpasswd' '%2e%2e%2fetc%2fpasswd'; do
  curl -sS -o /dev/null -w "$p %{http_code}\n" "https://app.example.com/files/$p"
done
```

## Pitfalls

- Reporting a traversal that was blocked at the proxy when the application never saw the path.
- Using one encoding without measuring the pass count, so the payload works by luck on one deployment.

## Done when

- The number of decoding passes is measured, not assumed.
- The encoding used and the resolved sink path are both recorded.

## References

- [OWASP path traversal](https://owasp.org/www-community/attacks/Path_Traversal)
