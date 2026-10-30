---
name: payload-type-confusion
description: "Send the same logical value as a string, number, array and object to find where the validator and the consumer disagree about its type. Use when a field is validated in one place and consumed in another, such as a JSON body and a database query"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [payload, type, coercion]
phase: payload
---

# Test type confusion deliberately, one coercion at a time

> Send the same logical value as a string, number, array and object to find where the validator and the consumer disagree about its type

**Use when:** a field is validated in one place and consumed in another, such as a JSON body and a database query

**Avoid when:** the field's type is enforced by a strict schema at every hop, which the docs or a probe confirm

## Procedure

1. Pick one field and send it as each JSON type in turn: string, number, boolean, array, object and null.
2. Record which types pass validation and which change downstream behaviour.
3. For the type that behaves differently, check the stored value and the rendered value separately.
4. Report the specific coercion, for example an array accepted where a string is expected.

## Signals

- types-sent
- validation-results-recorded
- storage-checked

## Patterns

**1. type matrix**

```
for v in '"1"' '1' 'true' '[1]' '{"a":1}' 'null'; do
  printf '{"id":%s}' "$v" > t.json
  curl -sS -o /dev/null -w "$v %{http_code}\n" --data-binary @t.json https://api.example.com/v2/items
done
```

## Pitfalls

- Testing six types in one request, so the response cannot be attributed to a single coercion.
- Assuming a 200 means the value was handled correctly rather than silently coerced.

## Done when

- Each JSON type was sent separately and its result recorded.
- The stored and rendered values are checked for the divergent type.

## References

- [JSON RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)
