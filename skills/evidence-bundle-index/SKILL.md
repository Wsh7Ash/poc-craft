---
name: evidence-bundle-index
description: "Package the payload, harness, raw captures and hash list behind a short index so a triager can reproduce without asking a question. Use when the finding is ready to submit and more than one person will read it"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [evidence, bundle, handoff]
phase: evidence
---

# Ship an evidence bundle with an index

> Package the payload, harness, raw captures and hash list behind a short index so a triager can reproduce without asking a question

**Use when:** the finding is ready to submit and more than one person will read it

**Avoid when:** the platform accepts only inline text and attachments are not supported

## Procedure

1. List every artifact and what claim it supports.
2. Write an index that names each file, its hash and the step it belongs to.
3. Include the harness and payload so the reproduction is one command.
4. Exclude anything you cannot explain, because an unexplained file invites distrust.

## Signals

- artifacts-listed
- index-written
- harness-included

## Patterns

**1. index**

```
# index
- payload.json  sha256:...  step 3
- poc.py        sha256:...  step 4 (harness)
- response.body sha256:...  step 5 (impact)
```

## Pitfalls

- A bundle that is a zip of screenshots with no index, which nobody can reproduce from.
- Including a captured token or cookie that has not been revoked.

## Done when

- The index names every artifact, its hash and the step it supports.
- No live credential is included in the bundle.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
