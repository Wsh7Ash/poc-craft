# Usage

## Install

```bash
python -m pip install -e .
poc-craft --version
```

## Find the skills for the stage you are in

```bash
poc-craft list --phase scope
poc-craft list --phase reproduce
poc-craft list --phase minimize
poc-craft show minimize-predicate-design
```

## Minimise a payload

1. Write a predicate that exits 0 only when the bug reproduces. Test it on the original payload:

   ```bash
   python check.py payload.bin; echo "exit=$?"   # must be 0
   python check.py benign.bin; echo "exit=$?"    # must be non-zero
   ```

2. Run the minimiser:

   ```bash
   poc-craft minimize --input payload.bin --predicate 'python check.py {input}' --unit line --out minimal.bin
   ```

3. Re-run the predicate on the output, then re-run the real proof from a clean session. A file
   that satisfies the predicate is not the same as a bug that reproduces.

If the reduction stalls, try `--unit byte`. If byte reduction produces unparseable structured
input, follow `poc-craft show minimize-structure-aware` and remove fields instead.

## Generate a harness

```bash
poc-craft scaffold \
  --url https://api.example.com/v2/export \
  --method POST \
  --payload payload.json \
  --header 'Authorization: Bearer <TOKEN>' \
  --oracle 'status == 500' \
  --repeat 3 \
  --out poc.py
python poc.py; echo "exit=$?"
```

Guidance on the oracle:

- for a crash, `status >= 500` is reasonable;
- for data exposure, assert on a victim-only value in `body`, for example
  `b'"owner":"victim-tenant"' in body`;
- for a state change, check the response and then re-read the resource.

A harness that "passes" because the endpoint rejects malformed input is worse than no harness.

## Work the loop

1. `scope-confirm-target` — confirm the target is in scope.
2. `reproduce-single-request` — reduce to one request.
3. `minimize-ddmin` — shrink the payload.
4. `harness-python-scaffold` — generate the harness.
5. `verify-negative-control` — prove the oracle is not just detecting errors.
6. `verify-determinism` — five attempts, report a rate.
7. `evidence-bundle-index` — package it with hashes.
8. `report-impact-statement` — separate observed from inferre
