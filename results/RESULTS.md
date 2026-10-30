# Results

Reproducible evidence for the claims in `README.md`.

## Environment

- OS: Windows (MSYS2 shell), Python 3.14
- Runtime: Python 3.10+ standard library only; `pytest` as a dev dependency
- Network: not required

## 1. Corpus validation

```
$ PYTHONPATH=src python -m poccraft validate
50/50 skills valid

$ PYTHONPATH=src python -m poccraft build
Built 52 artifacts, 10514 rendered skill words
```

## 2. Test suite

```
$ python -m pytest -q
................................................                         [100%]
```

48 tests. Beyond the corpus and artifact checks shared with every pack in this series, the
following behaviour is exercised for real:

- `split_units` round-trips the input for both `byte` and `line`, and rejects an unknown unit.
- `ddmin` reduces `padding / MAGIC / padding / padding` to the marker alone.
- `ddmin` keeps two markers when the predicate requires both.
- `ddmin` raises when the predicate does not hold on the original input.
- `ddmin` on empty input performs no predicate calls.
- Minimisation is deterministic: same bytes, same call count on a second run.
- `command_predicate` handles `{input}` substitution, implicit trailing path, and treats a
  timeout as "no match".
- The generated Python harness compiles (`compile(source, ..., 'exec')`), carries the URL,
  headers and repeat count, and is byte-identical across two generations.
- Bad method, non-HTTP URL and empty oracle are rejected; an unknown language is rejected.
- CLI `minimize` end to end: 77-byte payload in, a file containing only `MAGIC: yes` out.
- CLI `minimize` exits 1 with `does not hold` when the predicate never passes.
- CLI `scaffold` writes a file that compiles.

## 3. Real minimisation run

`results/demo_transcript.txt` records a run on a 5-line payload where the predicate requires the
line containing `MAGIC`:

```
$ poccraft minimize --input results/demo/payload.txt --predicate 'python results/demo/check.py {input}' --unit line --out results/demo/minimal.txt
minimal input written to results/demo/minimal.txt
77 -> 11 bytes (14.3%) in 6 predicate calls, 2 rounds

$ cat results/demo/minimal.txt
MAGIC: yes
```

The negative control in the same transcript shows a predicate that never holds:

```
$ poccraft minimize --input results/demo/payload.txt --predicate 'false'
error: the predicate does not hold on the unmodified input
exit=1
```

`results/demo/payload.txt` and `results/demo/check.py` are committed so the run is reproducible.

## What was not run

- **No HTTP request was sent by the test suite.** The generated harness is compiled and its
  command line is tested; its request path is not executed.
- **The bash harness is generated but not executed**; only the Python harness is compiled.
- **No structured-format minimisation** (JSON, XML, protobuf) is implemented; the corpus documents
  the procedure instead.
- **No performance claim.** The call counts printed by the CLI are the measurement.
