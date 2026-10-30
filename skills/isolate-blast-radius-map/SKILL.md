---
name: isolate-blast-radius-map
description: "Trace the trigger to every downstream effect so the proof does not send mail, write logs or notify a customer you did not intend to involve. Use when the trigger is on a path that fans out to notifications, audits or third parties"
pack: poc-craft
version: 1.0.0
category: bug-bounty-poc
tags: [isolate, side-effects, radius]
phase: isolate
---

# Map what else the trigger path touches

> Trace the trigger to every downstream effect so the proof does not send mail, write logs or notify a customer you did not intend to involve

**Use when:** the trigger is on a path that fans out to notifications, audits or third parties

**Avoid when:** the path is a pure read with no side effects at all

## Procedure

1. Read the response and check the account's notification settings before triggering.
2. Disable outbound email and webhooks for the test account where the product allows it.
3. Trigger once and enumerate the observed effects from audit logs and inboxes you control.
4. Record every effect, including ones you believe are harmless, because they are still impact.

## Signals

- effects-enumerated
- notifications-disabled
- audit-reviewed

## Patterns

**1. disable notifications**

```
curl -sS -X PATCH https://api.example.com/v2/settings -d '{"email_notifications":false}'
```

## Pitfalls

- Triggering a password-reset flow against a real address to prove enumeration.
- Missing an audit entry that records the action and later looks like unauthorised activity.

## Done when

- Side effects are enumerated from an independent source such as audit logs.
- Notification paths were disabled before the trigger where possible.

## References

- [OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)
