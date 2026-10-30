---
name: verify-negative-control
description: "Send a benign request through the same harness and show it does not satisfy the oracle, which proves the oracle is not simply detecting any error. Use when the oracle is an error code, a body marker or a length threshold"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [verify, control, oracle]
phase: verify
---

# Run a negative control before claiming success

> Send a benign request through the same harness and show it does not satisfy the oracle, which proves the oracle is not simply detecting any error

**Use when:** the oracle is an error code, a body marker or a length threshold

**Avoid when:** the oracle is an exact value that cannot be produced accidentally

## Procedure

1. Substitute the triggering value with a benign value and run the same harness.
2. Confirm the oracle returns false for the benign request and record the response.
3. If the control also passes, fix the oracle before continuing.
4. Store the control result next to the positive result in the evidence bundle.

## Signals

- control-run
- control-fails-oracle
- both-results-stored

## Patterns

**1. control**

```
poc-craft scaffold --url https://api.example.com/v2/export --payload benign.json --oracle 'status == 500' --out control.py
python control.py; echo "control exit=$?"
```

## Pitfalls

- An oracle of any 5xx that also fires on a malformed benign request, making the control pass too.
- Recording only the positive run, so a reviewer cannot see the control.

## Done when

- The control fails the oracle and both results are stored.
- The oracle is shown to distinguish the trigger from a benign request.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
