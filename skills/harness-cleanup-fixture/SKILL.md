---
name: harness-cleanup-fixture
description: "Delete or revert the resources the harness creates on success and on failure, so a repeated run starts from the same state. Use when the proof writes data, uploads files or changes settings"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [harness, cleanup, repeatability]
phase: harness
---

# Clean up what the harness creates

> Delete or revert the resources the harness creates on success and on failure, so a repeated run starts from the same state

**Use when:** the proof writes data, uploads files or changes settings

**Avoid when:** the written record is itself the evidence and must be preserved until triage

## Procedure

1. Enumerate every resource the harness creates or mutates and its delete endpoint or revert step.
2. Run cleanup in a finally block so a failure mid-proof still cleans up.
3. Verify cleanup by re-reading the resource and confirming it is gone or restored.
4. Preserve a snapshot of what was created as evidence before deleting it.

## Signals

- resources-enumerated
- cleanup-in-finally
- absence-verified

## Patterns

**1. cleanup**

```
try:
    run_proof()
finally:
    delete_created_resources()
```

## Pitfalls

- Cleaning up only on success, so a failed run leaves data that makes the next run behave differently.
- Deleting the evidence along with the resource.

## Done when

- Cleanup runs on both success and failure and its effect is verified.
- Evidence of the created resource is preserved separately.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
