---
name: evidence-hash-chain
description: "Record a sha256 for every artifact when it is created, so a later change is visible instead of silent. Use when evidence passes between people or sits for days before triage"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [evidence, integrity, hashing]
phase: evidence
---

# Hash the evidence so tampering is detectable

> Record a sha256 for every artifact when it is created, so a later change is visible instead of silent

**Use when:** evidence passes between people or sits for days before triage

**Avoid when:** the evidence is a live system state that cannot be hashed meaningfully

## Procedure

1. Hash each artifact at the moment it is created, not at the end of the engagement.
2. Store the hash list with a timestamp and the tool version used.
3. Re-hash before attaching to the report and compare against the stored list.
4. State any mismatch explicitly rather than regenerating the evidence silently.

## Signals

- hashes-recorded
- list-timestamped
- recheck-performed

## Patterns

**1. hash list**

```
sha256sum payload.json response.body > evidence.sha256
sha256sum -c evidence.sha256
```

## Pitfalls

- Hashing at submission time, which proves only that the file has not changed since submission.
- Re-generating the evidence when a hash mismatches, which hides the cause of the mismatch.

## Done when

- Every artifact has a hash recorded at creation time.
- The pre-submission recheck is recorded and any mismatch is explained.

## References

- [sha256sum](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html)
