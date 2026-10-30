---
name: automate-ci-regression
description: "Package the minimised input and oracle as a check that fails when the bug returns, so the finding stays fixed after the report is closed. Use when the client has agreed to verify the fix"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [automate, regression, ci]
phase: automate
---

# Turn the proof into a regression check

> Package the minimised input and oracle as a check that fails when the bug returns, so the finding stays fixed after the report is closed

**Use when:** the client has agreed to verify the fix

**Avoid when:** the environment cannot be reset between runs, which makes the check unreliable

## Procedure

1. Commit the minimised payload and the predicate into the target's test tree, not only into your notes.
2. Make the test set up its own preconditions and clean them up.
3. Run it against the vulnerable build to confirm it fails, and against the fixed build to confirm it passes.
4. Record both runs in the report as the acceptance criteria for the fix.

## Signals

- payload-committed
- fails-on-vulnerable
- passes-on-fixed

## Patterns

**1. regression test**

```
def test_export_traversal(client, admin_token):
    response = client.post('/v2/export', json={'filter': '../'}, headers={'Authorization': admin_token})
    assert response.status_code != 500
```

## Pitfalls

- A regression test that depends on a live third-party service and fails for unrelated reasons.
- Only running it against the fixed build, so it is never shown to detect the original bug.

## Done when

- The check fails on the vulnerable build and passes on the fixed one.
- Both results are recorded in the report.

## References

- [pytest documentation](https://docs.pytest.org/)
