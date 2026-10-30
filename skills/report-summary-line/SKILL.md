---
name: report-summary-line
description: "Lead with what is broken and where, in one sentence a triager can route, instead of a narrative that buries the finding. Use when you are writing the title or the first line of the report"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [report, summary, routing]
phase: report
---

# Write a summary line that states the defect

> Lead with what is broken and where, in one sentence a triager can route, instead of a narrative that buries the finding

**Use when:** you are writing the title or the first line of the report

**Avoid when:** the platform generates titles from fields you fill in separately

## Procedure

1. Name the component, the missing check and the observed impact in one sentence.
2. Avoid adjectives such as critical or severe in the title; those belong in the severity field.
3. Include the condition that makes it reachable, such as an authenticated tenant user.
4. Check the sentence against the evidence and remove any clause you cannot prove.

## Signals

- component-named
- impact-stated
- condition-included

## Patterns

**1. summary**

```
Export filter path traversal allows a tenant user to read files outside the tenant export root
```

## Pitfalls

- A title of possible RCE that the body never demonstrates.
- A title with no component, so two different bugs look like the same report.

## Done when

- The summary names the component, the defect and the observed impact.
- Every clause in it is backed by an artifact.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
