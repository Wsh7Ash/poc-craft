---
name: automate-parallel-safety
description: "Give each parallel attempt its own account, payload and output path, so a race proof is not actually measuring cross-talk between your own workers. Use when the proof depends on simultaneous requests"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [automate, concurrency, isolation]
phase: automate
---

# Keep parallel runs from contaminating each other

> Give each parallel attempt its own account, payload and output path, so a race proof is not actually measuring cross-talk between your own workers

**Use when:** the proof depends on simultaneous requests

**Avoid when:** the proof is sequential and parallelism adds only noise

## Procedure

1. Assign each worker a distinct identifier and a distinct output file.
2. Synchronise the start with a barrier so the requests are genuinely simultaneous.
3. Record per-worker timings to show the overlap that the claim depends on.
4. Re-run the same setup with the barrier disabled as a control.

## Signals

- workers-isolated
- barrier-used
- overlap-recorded

## Patterns

**1. barrier**

```
import threading
barrier = threading.Barrier(n)
def worker(i):
    barrier.wait()
    send(i)
```

## Pitfalls

- Workers sharing one account, so the server serialises them and the race never happens.
- Claiming a race from timestamps that never overlapped.

## Done when

- Per-worker isolation and overlap are recorded.
- A no-barrier control run is compared against the parallel run.

## References

- [Python threading barrier](https://docs.python.org/3/library/threading.html#threading.Barrier)
