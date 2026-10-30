---
name: payload-boundary-values
description: "Pick lengths, counts and indexes at the edges of what the code expects, because off-by-one and truncation bugs live at boundaries rather than in the middle. Use when the bug is suspected to be a length, count or index handling defect"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [payload, boundary, off-by-one]
phase: payload
---

# Use boundary values instead of random noise

> Pick lengths, counts and indexes at the edges of what the code expects, because off-by-one and truncation bugs live at boundaries rather than in the middle

**Use when:** the bug is suspected to be a length, count or index handling defect

**Avoid when:** the bug is semantic, for example an authorisation check, where length is irrelevant

## Procedure

1. Find the documented or observed limit for the field, from validation messages or documentation.
2. Send values at limit-1, limit and limit+1, and record the response for each.
3. Include the empty value and a value one byte over the maximum encoded length.
4. Report the exact boundary that misbehaves rather than a range.

## Signals

- limit-identified
- boundary-values-sent
- exact-edge-recorded

## Patterns

**1. boundary payloads**

```
for n in 0 63 64 65 1024 1025; do
  python -c "print('A'*$n, end='')" > v.bin
  curl -sS -o /dev/null -w "$n %{http_code}\n" --data-binary @v.bin https://api.example.com/v2/echo
done
```

## Pitfalls

- Sending a 10 MB payload when the limit is 64 bytes, which tests the proxy rather than the parser.
- Reporting only the failing case without the passing neighbour, so the boundary is not visible.

## Done when

- The limit is identified from evidence, not guessed.
- Values either side of the boundary are recorded with their responses.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
