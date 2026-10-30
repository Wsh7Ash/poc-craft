---
name: evidence-timeline
description: "Order every request, response and state change by timestamp so the report can show cause before effect instead of implying it. Use when the impact claim depends on ordering, such as a change appearing after a specific request"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [evidence, timeline, ordering]
phase: evidence
---

# Put the evidence on a timeline

> Order every request, response and state change by timestamp so the report can show cause before effect instead of implying it

**Use when:** the impact claim depends on ordering, such as a change appearing after a specific request

**Avoid when:** there is a single request and a single response with no ordering question

## Procedure

1. Record a monotonic timestamp for each action in the harness and the server's clock offset.
2. Merge client timestamps with server log timestamps, noting the offset between them.
3. Mark the triggering request and the first observed effect on the timeline.
4. Attach the timeline as a table with source and clock for each row.

## Signals

- timestamps-recorded
- offset-noted
- ordering-documented

## Patterns

**1. timeline rows**

```
date -u +%FT%TZ; curl -sS -o /dev/null -w 'trigger %{http_code} at %{time_total}s\n' -X POST https://api.example.com/v2/export --data-binary @payload.json
```

## Pitfalls

- Mixing client local time and server UTC without noting the offset, which reverses the order.
- Claiming a state change was caused by a request when the snapshot was taken before it.

## Done when

- Every row has a timestamp, its source clock and the observed action.
- Cause and effect are ordered with the offset accounted for.

## References

- [RFC 3339 timestamps](https://www.rfc-editor.org/rfc/rfc3339)
