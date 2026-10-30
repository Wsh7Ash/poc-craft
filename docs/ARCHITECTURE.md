# Architecture

Three ideas hold the repository together: skills are data, generation is pure, and the
minimiser only trusts a predicate.

```
corpus/part1..part3.py --skill_from_dict--> Skill --validate--> issues
                                            |
                                            +--render--> skills/, pack.json, catalog
minimizer.py: units + predicate --> ddmin --> MinimiseResult
scaffold.py: Spec --> source (python | bash)
```

## Skills as data

Each skill is a dict with required keys; `skill_from_dict` validates the shape once and returns a
frozen `Skill`. Everything downstream — renderer, validator, CLI — reads that frozen object, so a
skill cannot be half-mutated in one code path and not another.

## Deterministic rendering

`render_skill` is a pure function of `(pack, skill)`. Front-matter key order is fixed and the
description is JSON-escaped, so a summary containing quotes cannot corrupt the YAML block.
`build_pack` returns `{relative path: text}` and writes only when given a root, which lets tests
compare committed artifacts with a fresh render without touching disk.

## The minimiser

`ddmin` is implemented as a sequence algorithm over removable units rather than a byte buffer.
That choice keeps the algorithm independent of the input format: the caller supplies units and a
predicate over the reconstructed bytes.

Two invariants are enforced rather than assumed:

1. the predicate must hold on the original input before any reduction (otherwise the run aborts);
2. every accepted candidate must itself satisfy the predicate.

The final pass removes any unit whose removal still satisfies the predicate, so the result is
1-minimal with respect to the chosen unit granularity — not globally minimal, which ddmin does not
promise.

`command_predicate` adapts a shell command to the predicate signature. A timeout is mapped to
"does not reproduce", because treating a hang as a match would let the minimiser converge on an
input that simply stalls the target.

## The scaffold generator

`Spec` is validated before generation: method must be a known HTTP verb, URL must be http(s),
oracle must be non-empty, repeat must be at least one. Generation is a pure function of the spec,
so the committed harness and a fresh generation are byte-identical — the same drift check used for
skill files applies to harnesses.

The generated Python harness evaluates the oracle with `{"__builtins__": {}}`, so an oracle
expression cannot call arbitrary functions. This is a guard against a copied oracle carrying
unintended behaviour, not a security boundary: the harness is code you are expected to read.

## Non-goals

- poc-craft does not send requests itself; the generated harness does.
- It does not know your payload format; structure-aware reduction is a documented skill.
- It does not store evidence; it tells you what to store and how to prove it has not changed.
