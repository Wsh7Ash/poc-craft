# Security

## Scope

poc-craft generates text and runs a predicate command you supply. Running `minimize` executes that
command with the privileges of your shell, so only pass predicates you trust.

## Generated harnesses

The generated Python harness evaluates the oracle expression with builtins disabled. That is a
guard against accidental calls, not a sandbox. Treat a harness as code to read before running it.

## Intended use

The skills and the harness generator describe testing systems you are authorised to test. Using
them against a target without written permission may be unlawful; the `scope` phase exists to make
that boundary checkable before any request is sent.

## Reporting a problem

Open an issue naming the skill or module and the observed behaviour. Include the Python version and
platform. Do not include live credentials from an engagement.
