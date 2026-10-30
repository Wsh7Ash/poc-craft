---
name: cleanup-test-data
description: "Delete or revert every record, file and setting the proof touched, and verify the removal rather than assuming it. Use when the engagement is ending and test artifacts remain in the target"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [cleanup, data, reversal]
phase: cleanup
---

# Remove the data the proof created

> Delete or revert every record, file and setting the proof touched, and verify the removal rather than assuming it

**Use when:** the engagement is ending and test artifacts remain in the target

**Avoid when:** the client wants the data preserved for their own investigation

## Procedure

1. List every resource created or modified, with its identifier and the operation used.
2. Delete or revert each one through the documented path, recording the response.
3. Re-read each resource to confirm it is gone or restored.
4. Report anything that could not be removed, because that is a client action item.

## Signals

- resources-listed
- removal-attempted
- absence-verified

## Patterns

**1. delete and verify**

```
curl -sS -X DELETE -H "Authorization: Bearer $TOKEN" https://api.example.com/v2/items/4242 -o /dev/null -w '%{http_code}\n'
curl -sS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" https://api.example.com/v2/items/4242
```

## Pitfalls

- Deleting through an undocumented path that leaves an orphaned child record.
- Assuming a 204 means gone without re-reading the resource.

## Done when

- Every touched resource is removed or reverted and its absence verified.
- Anything not removable is reported as a client action item.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
