---
name: report-attachment-hygiene
description: "Redact tokens, cookies and personal data from every attachment while keeping the request replayable with placeholders. Use when the evidence contains an authorization header or personal data"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [report, redaction, hygiene]
phase: report
---

# Keep credentials out of the report

> Redact tokens, cookies and personal data from every attachment while keeping the request replayable with placeholders

**Use when:** the evidence contains an authorization header or personal data

**Avoid when:** the program explicitly requires a live token and provides a dedicated test account

## Procedure

1. List every secret and personal field in the captured requests and responses.
2. Replace each with a placeholder that names its type, such as TOKEN or VICTIM_EMAIL.
3. Add a note that the placeholder is redacted so a reader does not try to replay it literally.
4. Re-scan the attachments for the original values before submitting.

## Signals

- secrets-listed
- placeholders-used
- rescan-clean

## Patterns

**1. redaction**

```
sed -E 's/(Authorization: Bearer )[A-Za-z0-9._-]+/\1<TOKEN>/' request.txt > request.redacted.txt
grep -nE 'eyJ[A-Za-z0-9_-]{10,}' request.redacted.txt || echo clean
```

## Pitfalls

- Redacting the header but leaving the token in a response body or an error message.
- Submitting a live token that remains valid after the report is closed.

## Done when

- Every secret and personal field is replaced with a typed placeholder.
- A rescan of the attachments finds no original value.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
