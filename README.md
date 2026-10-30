# poc-craft

**Craft a proof of concept that survives triage: 50 validated skills, a real ddmin minimiser, and a harness generator.**

The pack covers the whole life of a PoC — scope check, honest reproduction, isolation, minimisation, harness, controls, evidence, triage, report, cleanup and post-fix verification. The tool does two things the skills describe: it shrinks an input while a predicate keeps passing, and it emits a harness with one oracle and a repeat count.

```
$ poc-craft minimize --input payload.txt --predicate 'python check.py {input}' --unit line --out minimal.txt
minimal input written to minimal.txt
77 -> 11 bytes (14.3%) in 6 predicate calls, 2 rounds

$ cat minimal.txt
MAGIC: yes
```

## Why this pack exists

A PoC fails triage for reasons that have nothing to do with whether the bug is real:

- it was built against an asset that was not in scope;
- it reproduces once and is written up as always;
- a large payload hides which field actually triggers the bug;
- the oracle is any 5xx, so minimisation produces garbage that was never the finding;
- the evidence is a screenshot that cannot be replayed;
- the fix is accepted because the endpoint now returns 403 for everyone;
- the test data and live tokens are never cleaned up.

Every skill is written against one of those failure modes.

## Install

```bash
python -m pip install -e .
poc-craft validate
```

No runtime dependencies. Python 3.10+.

## Commands

| Command | What it does |
|---|---|
| `poc-craft validate [--json]` | Run every corpus rule; exit 1 with the specific issues |
| `poc-craft list [--phase P]` | List skills, optionally filtered by one of the 13 phases |
| `poc-craft show SLUG` | Print one fully rendered `SKILL.md` |
| `poc-craft render` / `catalog` / `build` | Regenerate the committed artifacts |
| `poc-craft minimize --input F --predicate CMD [--unit line\|byte] [--out F]` | Delta-debug an input while `CMD {input}` exits 0 |
| `poc-craft scaffold --url U --payload F [--method M] [--oracle EXPR] [--lang python\|bash] [--out F]` | Emit a runnable PoC harness |

## The minimiser

`ddmin` (Zeller & Hildebrandt) over removable units. `--unit line` splits on `\n` and keeps the terminator; `--unit byte` splits per byte. The predicate is any command that exits 0 when the input still reproduces; `{input}` is replaced with the temp file path.

Properties the tests check:

- the predicate must hold on the unmodified input, or the run fails rather than returning a wrong answer;
- the minimised input still satisfies the predicate;
- two runs of the same input and predicate produce the same minimal bytes and the same call count;
- a timeout in the predicate counts as "does not reproduce", not as a match.

Deliberately **not** done: the minimiser does not parse your input format. Structure-aware reduction is described in `minimize-structure-aware`, and the byte/line minimiser is the fallback.

## The harness generator

```
$ poc-craft scaffold --url https://api.example.com/v2/export --method POST \
    --payload payload.json --oracle 'status == 500' --repeat 3 --out poc.py
```

The generated Python harness sends one request per attempt, evaluates the oracle against `status`, `length` and `body`, prints a per-attempt line, and exits non-zero unless every attempt reproduces. The oracle is evaluated with builtins disabled. `--lang bash` emits an equivalent curl harness.

The oracle expression is the part you are expected to edit: a default of `status >= 500` is almost never the right oracle for a data-exposure finding.

## The validator

Nine per-skill rules: 3+ steps, 2+ signals, 1+ pattern, 2+ pitfalls, a phase from the closed set of 13, at least one HTTPS-labelled reference, a summary of 20+ characters, an `avoid_when` of 10+ characters, and 80+ rendered words.

Package rules: exactly 50 skills, all 13 phases present, unique slugs, unique case-insensitive titles, unique summaries.

## Phases and counts

| Phase | Skills | Focus |
|---|---|---|
| `scope` | 3 | target check, least-invasive impact, authorised accounts |
| `reproduce` | 4 | from a report, single request, state snapshot, clean session |
| `isolate` | 3 | variable bisect, dependency check, blast radius |
| `minimize` | 4 | ddmin, oracle design, structure-aware, preserved preconditions |
| `payload` | 5 | encoding, boundaries, type confusion, header and path layers |
| `harness` | 4 | scaffold, repetition, timeout, cleanup fixture |
| `automate` | 3 | bounded loops, parallel safety, CI regression |
| `verify` | 5 | negative control, specific oracle, determinism, fresh account, minimal impact |
| `evidence` | 4 | raw capture, hash chain, timeline, bundle index |
| `triage` | 4 | severity basis, duplicates, fix scope, reproducer review |
| `report` | 4 | summary, steps, impact split, redaction |
| `cleanup` | 3 | test data, credentials, retention |
| `regression` | 4 | fixture library, fix verification, siblings, closeout |

## Layout

```
src/poccraft/
  model.py       immutable Skill shape
  validate.py    per-skill and package rules
  render.py      deterministic SKILL.md, catalog, manifest
  minimizer.py   ddmin, unit splitting, command predicate
  scaffold.py    Python and bash harness generation
  cli.py         validate/list/show/render/catalog/build/minimize/scaffold
  corpus/        50 authored skills
skills/          50 generated SKILL.md files
results/         catalog, demo transcript, demo payload
tests/           48 tests including real minimisation runs
```

## Limits

- **Nothing here contacts a target.** The generated harness is compiled and its CLI is tested, but no request is sent in the suite.
- **The minimiser is byte/line only.** JSON-aware or protobuf-aware reduction is a documented procedure, not an implementation.
- **The bash harness is generated but not executed in tests**, because `curl` behaviour varies by build; the Python harness is the tested path.
- **No claim about performance.** ddmin calls the predicate a number of times proportional to the reduction achieved, and the CLI prints the real count.

## License

MIT.
