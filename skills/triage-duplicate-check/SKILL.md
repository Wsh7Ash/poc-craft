---
name: triage-duplicate-check
description: "Search prior reports and advisories for the same root cause before submitting, so a duplicate is caught by you rather than a triager. Use when the program has a public or internal history of reports"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [triage, duplicates, history]
phase: triage
---

# Check for duplicates against known reports

> Search prior reports and advisories for the same root cause before submitting, so a duplicate is caught by you rather than a triager

**Use when:** the program has a public or internal history of reports

**Avoid when:** the program is brand new with no history to search

## Procedure

1. Search the program's disclosed reports and the vendor's advisories for the same endpoint and defect class.
2. Compare the root cause, not the URL, since a duplicate is the same fix.
3. Reference any near duplicate in your submission and explain what differs.
4. Record the searches performed, so the check is visible rather than claimed.

## Signals

- searched
- root-cause-compared
- near-duplicates-cited

## Patterns

**1. search**

```
curl -sS 'https://api.example.com/search?q=export+traversal' -H "Authorization: Bearer $TOKEN"
```

## Pitfalls

- Searching only by endpoint and missing an advisory that fixed the same root cause elsewhere.
- Submitting without any search and having the report closed as a duplicate on day one.

## Done when

- Searches are recorded and root causes compared.
- Any near duplicate is cited with the difference stated.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
