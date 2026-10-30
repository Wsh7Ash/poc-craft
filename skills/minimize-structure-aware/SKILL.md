---
name: minimize-structure-aware
description: "Reduce JSON, XML or protobuf by removing fields and elements rather than bytes, so the result stays parseable and the bug stays reachable. Use when the payload is structured and byte-level removal produces invalid documents"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, structured, format]
phase: minimize
---

# Minimise structured input without breaking the format

> Reduce JSON, XML or protobuf by removing fields and elements rather than bytes, so the result stays parseable and the bug stays reachable

**Use when:** the payload is structured and byte-level removal produces invalid documents

**Avoid when:** the bug is a parser-level defect where malformed input is exactly the trigger

## Procedure

1. Parse the document and enumerate removable units: object keys, array elements, attributes and text nodes.
2. Remove one unit at a time and re-serialise, checking the result still parses before testing the predicate.
3. Keep removals that preserve reproduction and revert those that do not.
4. Store the minimal document in its serialised form with the key order used during the test.

## Signals

- units-enumerated
- parse-validated
- minimal-document-stored

## Patterns

**1. structural removal**

```
python -c "import json,sys; d=json.load(open('payload.json')); del d['unused']; json.dump(d, open('candidate.json','w'))"
```

## Pitfalls

- Byte-minimising JSON until it no longer parses and then testing a different code path entirely.
- Changing key order during reserialisation, which can change behaviour in a signature-checked API.

## Done when

- The minimal document still parses under the same parser.
- Key order and serialisation form are recorded with the payload.

## References

- [JSON RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)
