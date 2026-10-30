# Contributing

## Adding a skill

1. Add a dict to `src/poccraft/corpus/part1.py`, `part2.py` or `part3.py`.
2. Meet every floor: 3+ steps, 2+ signals, 1+ pattern, 2+ pitfalls, a phase from the closed set
   of 13, one or more HTTPS-labelled references, and 80+ rendered words.
3. Run `poc-craft validate` — it must print `50/50 skills valid`.
4. Run `poc-craft build` to regenerate artifacts.
5. Run `python -m pytest -q`.

## Changing the minimiser

Any change to `ddmin` must keep these properties, which are tested:

- the predicate must hold on the original input;
- the result must satisfy the predicate;
- the same input and predicate must produce the same result and the same call count;
- a predicate timeout must not count as a match.

## Changing the scaffold generator

Generated output is committed and drift-checked. If you change a template, regenerate the demo
harness and keep the generated Python compiling under 3.10.

## What will be rejected

- A skill that duplicates an existing title or summary.
- A skill added without a rebuild, leaving stale artifacts.
- Lowering a floor in `validate.py` to make a thin skill pass.
