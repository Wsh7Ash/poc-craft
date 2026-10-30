---
name: cleanup-artifact-retention
description: "Keep the minimum evidence needed to defend the report, and delete captures that contain personal data once triage closes. Use when the evidence includes other users' personal data"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [cleanup, retention, privacy]
phase: cleanup
---

# Decide what evidence to keep and for how long

> Keep the minimum evidence needed to defend the report, and delete captures that contain personal data once triage closes

**Use when:** the evidence includes other users' personal data

**Avoid when:** the client's contract specifies a retention period that overrides your default

## Procedure

1. Classify each artifact: needed for defence, useful context, or containing personal data.
2. Keep the first, summarise the second, and delete or anonymise the third after triage.
3. Record the retention decision and the deletion date for each deleted artifact.
4. Keep hashes of deleted artifacts so their existence and integrity remain auditable.

## Signals

- artifacts-classified
- deletion-recorded
- hashes-retained

## Patterns

**1. retain hash, delete body**

```
sha256sum victim-response.json >> deleted.sha256
shred -u victim-response.json
```

## Pitfalls

- Keeping a victim's personal data indefinitely because it was convenient.
- Deleting the artifact that proves the impact before triage has accepted the finding.

## Done when

- Each artifact has a retention decision and deletions are dated.
- Hashes of deleted artifacts are retained.

## References

- [GDPR data minimisation](https://gdpr-info.eu/art-5-gdpr/)
