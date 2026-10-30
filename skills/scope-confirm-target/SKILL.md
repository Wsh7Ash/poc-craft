---
name: scope-confirm-target
description: "Check the host, path and asset against the written scope so a proof of concept is never crafted against something the engagement does not cover. Use when the engagement has multiple assets and it is tempting to test the one that is reachable"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [scope, authorisation, target]
phase: scope
---

# Confirm the target before building anything

> Check the host, path and asset against the written scope so a proof of concept is never crafted against something the engagement does not cover

**Use when:** the engagement has multiple assets and it is tempting to test the one that is reachable

**Avoid when:** you are working on your own lab target where scope is not a concept that applies

## Procedure

1. Write the asset identifier as the scope defines it: hostname, path prefix and account boundary.
2. Resolve the value you are about to test against that identifier and record both.
3. Stop when they differ, and report the near miss instead of testing the neighbouring asset.
4. Re-check after any redirect, because a redirect can move the request to an out-of-scope host.

## Signals

- asset-recorded
- target-compared
- out-of-scope-refused

## Patterns

**1. scope check**

```
python -c "import urllib.parse as u; print(u.urlsplit('https://api.example.com/v2/items').netloc)"
```

## Pitfalls

- Testing a staging host because it was easier to reach, when only production is in scope.
- Following a redirect without re-checking the host, which quietly moves the request out of scope.

## Done when

- The asset and the tested target are recorded and match.
- Any out-of-scope candidate was refused and documented.

## References

- [PTES scoping](https://www.pentest-standard.org/index.php/Scoping)
