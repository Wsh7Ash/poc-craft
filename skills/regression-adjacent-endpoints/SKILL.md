---
name: regression-adjacent-endpoints
description: "Test the sibling routes that use the same handler or middleware, so a fix applied to one route does not leave the class open. Use when the finding came from a shared middleware or handler"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [regression, siblings, coverage]
phase: regression
---

# Check the endpoints that share the defect

> Test the sibling routes that use the same handler or middleware, so a fix applied to one route does not leave the class open

**Use when:** the finding came from a shared middleware or handler

**Avoid when:** the defect is provably local to one route's own code

## Procedure

1. List every route that uses the same handler, middleware or template.
2. Send the same minimised payload to each, adapted only in the route name.
3. Record which routes reproduce, which are blocked and which behave differently.
4. Report the full set, marking unverified routes as unverified rather than assuming.

## Signals

- siblings-listed
- payloads-sent
- results-recorded

## Patterns

**1. sibling sweep**

```
for route in export import backup; do
  curl -sS -o /dev/null -w "$route %{http_code}\n" -X POST -H "Authorization: Bearer $T" --data-binary @payload.json "https://api.example.com/v2/$route"
done
```

## Pitfalls

- Assuming a sibling is fixed because the reported route is, without testing it.
- Sending the payload to every route in the product and calling it scope.

## Done when

- Every route sharing the handler is tested and its result recorded.
- Unverified routes are labelled rather than assumed safe.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
