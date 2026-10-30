---
name: harness-python-scaffold
description: "Emit a harness from the request specification so the proof has one request path, one oracle and a repeat count that exposes flakiness. Use when the proof will be run more than once, including by a reviewer"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [harness, scaffold, python]
phase: harness
---

# Generate the harness instead of hand-writing it

> Emit a harness from the request specification so the proof has one request path, one oracle and a repeat count that exposes flakiness

**Use when:** the proof will be run more than once, including by a reviewer

**Avoid when:** a single curl command already captures the whole proof

## Procedure

1. Write the URL, method, payload path and oracle expression into the generator.
2. Generate the Python harness and review the oracle expression before running it.
3. Run it once to confirm it fails on a benign payload and passes on the triggering one.
4. Commit the generated harness beside the payload and record the generator version.

## Signals

- harness-generated
- oracle-reviewed
- control-run-fails

## Patterns

**1. generate**

```
poc-craft scaffold --url https://api.example.com/v2/export --method POST \
  --payload payload.json --oracle 'status == 500' --repeat 3 --out poc.py
```

## Pitfalls

- Hand-editing a generated harness and then reporting the generator as the source of the evidence.
- Leaving the oracle as the default `status >= 500` when the bug is a 200 with leaked data.

## Done when

- The generated harness runs and its oracle is specific to the finding.
- A benign payload is shown to fail the oracle.

## References

- [Python urllib.request](https://docs.python.org/3/library/urllib.request.html)
