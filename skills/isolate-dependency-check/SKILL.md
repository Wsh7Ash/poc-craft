---
name: isolate-dependency-check
description: "Disable or replace an external dependency so the proof does not silently rely on a second service being misconfigured. Use when the trigger path crosses a queue, a webhook or a third-party API"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [isolate, dependencies, external]
phase: isolate
---

# Check whether a dependency is what makes it work

> Disable or replace an external dependency so the proof does not silently rely on a second service being misconfigured

**Use when:** the trigger path crosses a queue, a webhook or a third-party API

**Avoid when:** the dependency is the vulnerability itself and removing it removes the finding

## Procedure

1. Name every external call the trigger makes and where it is configured.
2. Replace each with a controlled endpoint you own, or disable the feature that calls it.
3. Re-run the proof and record which dependencies are required and which are incidental.
4. Report the required dependency explicitly, because it changes who has to fix the bug.

## Signals

- dependencies-named
- substitution-run
- requirements-recorded

## Patterns

**1. controlled endpoint**

```
curl -sS -X PUT https://api.example.com/v2/settings -d '{"webhook":"https://your-listener.example/hook"}'
```

## Pitfalls

- Reporting a bug that only works because a webhook pointed at an attacker-controlled host you set up earlier.
- Leaving a live third-party call in the harness, which makes the proof fail when their service changes.

## Done when

- Every external dependency is replaced or disabled and the result re-checked.
- Required versus incidental dependencies are stated in the report.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
