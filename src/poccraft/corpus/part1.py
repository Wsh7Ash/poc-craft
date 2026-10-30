"""Part 1 of the poc-craft corpus: scope, reproduce, isolate, minimise, payload."""

from __future__ import annotations

from typing import Any

SKILLS: list[dict[str, Any]] = [
    {
        "slug": "scope-confirm-target",
        "title": "Confirm the target before building anything",
        "summary": "Check the host, path and asset against the written scope so a proof of concept is never crafted against something the engagement does not cover",
        "use_when": "the engagement has multiple assets and it is tempting to test the one that is reachable",
        "avoid_when": "you are working on your own lab target where scope is not a concept that applies",
        "tags": ["scope", "authorisation", "target"],
        "steps": [
            "Write the asset identifier as the scope defines it: hostname, path prefix and account boundary.",
            "Resolve the value you are about to test against that identifier and record both.",
            "Stop when they differ, and report the near miss instead of testing the neighbouring asset.",
            "Re-check after any redirect, because a redirect can move the request to an out-of-scope host.",
        ],
        "signals": ["asset-recorded", "target-compared", "out-of-scope-refused"],
        "patterns": [
            (
                "scope check",
                "python -c \"import urllib.parse as u; print(u.urlsplit('https://api.example.com/v2/items').netloc)\"",
            )
        ],
        "pitfalls": [
            "Testing a staging host because it was easier to reach, when only production is in scope.",
            "Following a redirect without re-checking the host, which quietly moves the request out of scope.",
        ],
        "done_when": [
            "The asset and the tested target are recorded and match.",
            "Any out-of-scope candidate was refused and documented.",
        ],
        "refs": [
            "[PTES scoping](https://www.pentest-standard.org/index.php/Scoping)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "scope-minimal-impact",
        "title": "Choose the least invasive way to demonstrate impact",
        "summary": "Decide the weakest action that still proves the finding, so the proof does not read data, send mail or change state it does not have to",
        "use_when": "a finding could be demonstrated by either reading or writing and both are available",
        "avoid_when": "the vulnerability only manifests through the destructive path and the client has authorised that path",
        "tags": ["scope", "impact", "restraint"],
        "steps": [
            "List the actions the bug would allow, ordered from read-only to state-changing.",
            "Pick the first action that is distinguishable from normal behaviour and record why the weaker ones fail.",
            "Bound the blast radius: one record, one message, one file, never a loop over real data.",
            "State the chosen boundary in the report so the client can see what was and was not touched.",
        ],
        "signals": ["actions-enumerated", "weakest-chosen", "radius-bounded"],
        "patterns": [
            (
                "read-only proof",
                "curl -sS -o /dev/null -w '%{http_code} %{size_download}\\n' https://api.example.com/v2/users/2",
            )
        ],
        "pitfalls": [
            "Deleting a real record to prove an IDOR when reading one record proves the same access.",
            "Sending mail to a real address to prove injection when a controlled inbox would do.",
        ],
        "done_when": [
            "The weakest sufficient action is chosen and justified.",
            "The blast radius is stated in the report.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "scope-authorised-accounts",
        "title": "Use accounts you are authorised to control",
        "summary": "Create or use accounts inside the agreed tenant and record their identity, so a two-account test never touches a real customer",
        "use_when": "the finding needs two accounts to demonstrate cross-tenant access",
        "avoid_when": "the engagement explicitly supplies accounts and creating new ones would break the agreement",
        "tags": ["scope", "accounts", "tenancy"],
        "steps": [
            "Register or receive two accounts in the agreed tenant and record their identifiers and creation time.",
            "Confirm both accounts see only their own data before attempting the cross-account request.",
            "Attempt the cross-account request and capture both the request and the victim account's view of the data.",
            "Delete or disable the accounts at the end if the scope requires it, and record the cleanup.",
        ],
        "signals": ["accounts-recorded", "baseline-isolation-confirmed", "cross-request-captured"],
        "patterns": [
            (
                "two-account check",
                "curl -sS -H \"Authorization: Bearer $A\" https://api.example.com/v2/me\ncurl -sS -H \"Authorization: Bearer $B\" https://api.example.com/v2/users/<a-id>",
            )
        ],
        "pitfalls": [
            "Reusing a colleague's real account as the victim, which turns a test into an incident.",
            "Skipping the baseline isolation check, so a shared-data design looks like an IDOR.",
        ],
        "done_when": [
            "Both accounts are recorded with identifiers and creation time.",
            "The cross-account request and the victim's own view are both captured.",
        ],
        "refs": [
            "[OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "reproduce-from-report",
        "title": "Reproduce a finding from someone else's report",
        "summary": "Rebuild the stated preconditions from a written report before adding anything, so the reproduction is of the reported bug and not a neighbour",
        "use_when": "you are verifying a report you did not write, including your own from an earlier session",
        "avoid_when": "the report already includes a runnable harness and your job is only to execute it",
        "tags": ["reproduce", "verification", "handoff"],
        "steps": [
            "Extract every precondition the report states: account state, feature flags, data shape and request order.",
            "Recreate them exactly and run the reported steps without improvising.",
            "Record whether the result matches the report, including partial matches.",
            "Report a difference as a difference, not as a failed reproduction, until you have ruled out drift.",
        ],
        "signals": ["preconditions-recreated", "steps-followed", "match-recorded"],
        "patterns": [
            (
                "replay recorded request",
                "curl -sS -X POST https://api.example.com/v2/items \\\n  -H 'Content-Type: application/json' \\\n  --data-binary @reported-body.json",
            )
        ],
        "pitfalls": [
            "Improving the steps while reproducing, which makes the result unattributable to the report.",
            "Assuming a mismatch means the report is wrong when a feature flag or data shape changed.",
        ],
        "done_when": [
            "Every stated precondition is recreated and recorded.",
            "The outcome is classified as match, partial or mismatch with evidence.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "reproduce"},
    },
    {
        "slug": "reproduce-single-request",
        "title": "Reproduce with a single request where possible",
        "summary": "Reduce the reproduction to one request that can be pasted into a terminal, because a multi-step script hides which step actually triggers the bug",
        "use_when": "the bug appears after a sequence of requests but might not need all of them",
        "avoid_when": "the bug genuinely requires state created by earlier requests and removing them breaks the precondition",
        "tags": ["reproduce", "minimal", "request"],
        "steps": [
            "Capture the full sequence that triggers the bug as raw requests with headers and bodies.",
            "Remove one request at a time from the front and re-run, keeping only those that are required.",
            "Confirm the surviving single request still triggers the bug from a fresh session.",
            "Publish the single request with the exact headers that matter, marked as required or optional.",
        ],
        "signals": ["sequence-captured", "steps-removed", "single-request-confirmed"],
        "patterns": [
            (
                "single request",
                "curl -sS -i -X POST https://api.example.com/v2/export \\\n  -H 'Authorization: Bearer $TOKEN' \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"format\":\"csv\",\"filter\":\"../\"}'",
            )
        ],
        "pitfalls": [
            "Keeping a login request in the proof because it was in the original capture, when a token works alone.",
            "Publishing a request that depends on a session cookie created by steps you removed.",
        ],
        "done_when": [
            "A single request reproduces the bug from a fresh session.",
            "Required and optional headers are distinguished.",
        ],
        "refs": [
            "[curl manual](https://curl.se/docs/manpage.html)",
        ],
        "meta": {"phase": "reproduce"},
    },
    {
        "slug": "reproduce-state-snapshot",
        "title": "Snapshot state before the reproduction",
        "summary": "Record the account and resource state the reproduction starts from, so a later reviewer can tell whether the bug needed that state or created it",
        "use_when": "the finding depends on data created earlier in the engagement",
        "avoid_when": "the reproduction is stateless and starts from an empty account every time",
        "tags": ["reproduce", "state", "snapshot"],
        "steps": [
            "List the resources the request will read or write and fetch their current representation.",
            "Store the snapshot with a hash and a timestamp before sending the triggering request.",
            "After the request, fetch the same resources again and diff the two snapshots.",
            "Keep both snapshots, since the diff is the impact evidence and the before-state proves the precondition.",
        ],
        "signals": ["pre-state-captured", "post-state-captured", "diff-computed"],
        "patterns": [
            (
                "snapshot",
                "curl -sS -H \"Authorization: Bearer $TOKEN\" https://api.example.com/v2/items/42 > before.json\nsha256sum before.json",
            )
        ],
        "pitfalls": [
            "Capturing only the after-state, which makes it impossible to show what changed.",
            "Comparing snapshots taken against different accounts or tenants.",
        ],
        "done_when": [
            "Pre and post snapshots exist with hashes and timestamps.",
            "The diff between them is recorded as impact evidence.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "reproduce"},
    },
    {
        "slug": "reproduce-clean-session",
        "title": "Reproduce from a clean session",
        "summary": "Run the proof with a fresh browser profile or token so cached state, service workers or an old session cannot be the thing that makes it work",
        "use_when": "the bug reproduces in your browser but not in a script, or only on your machine",
        "avoid_when": "the bug is explicitly about persistent state that a clean session removes",
        "tags": ["reproduce", "session", "isolation"],
        "steps": [
            "Clear cookies, local storage, service workers and the cache, or use a fresh profile.",
            "Obtain a new token and confirm the account state matches the recorded precondition.",
            "Re-run the exact request and compare with the previous result.",
            "Record the session origin (fresh profile, API token, script) with the proof.",
        ],
        "signals": ["session-cleared", "fresh-token-used", "result-compared"],
        "patterns": [
            (
                "fresh profile",
                "google-chrome --user-data-dir=$(mktemp -d) --incognito https://app.example.com",
            )
        ],
        "pitfalls": [
            "Concluding the bug is not reproducible when a service worker was still serving a cached response.",
            "Using a token minted before the precondition was set, so the request runs against stale permissions.",
        ],
        "done_when": [
            "The proof runs from a cleared session and a fresh token.",
            "The session origin is recorded with the proof.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "reproduce"},
    },
    {
        "slug": "isolate-variable-bisect",
        "title": "Bisect the input to find the triggering variable",
        "summary": "Change one field at a time across the request so the claim names the parameter that causes the bug instead of the request that contains it",
        "use_when": "a request triggers the bug but you cannot say which field is responsible",
        "avoid_when": "the bug requires several fields to change together, which a one-at-a-time bisect cannot show",
        "tags": ["isolate", "bisect", "variables"],
        "steps": [
            "List every field in the request and the value used in the successful reproduction.",
            "Revert one field to a benign value, resend, and record whether the bug still triggers.",
            "Keep the fields whose reversion stops the bug and discard the rest.",
            "State the minimal set of fields and values in the report rather than the whole request.",
        ],
        "signals": ["fields-enumerated", "one-at-a-time-run", "minimal-set-identified"],
        "patterns": [
            (
                "bisect a field",
                "curl -sS -X POST https://api.example.com/v2/export -d '{\"format\":\"csv\",\"filter\":\"../\"}'\ncurl -sS -X POST https://api.example.com/v2/export -d '{\"format\":\"csv\",\"filter\":\"safe\"}'",
            )
        ],
        "pitfalls": [
            "Changing two fields in one iteration, which makes the result unattributable.",
            "Assuming the first field that breaks it is the only one that can, when the service accepts several paths.",
        ],
        "done_when": [
            "Every field was reverted individually at least once.",
            "The minimal triggering field set is stated in the report.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "isolate"},
    },
    {
        "slug": "isolate-dependency-check",
        "title": "Check whether a dependency is what makes it work",
        "summary": "Disable or replace an external dependency so the proof does not silently rely on a second service being misconfigured",
        "use_when": "the trigger path crosses a queue, a webhook or a third-party API",
        "avoid_when": "the dependency is the vulnerability itself and removing it removes the finding",
        "tags": ["isolate", "dependencies", "external"],
        "steps": [
            "Name every external call the trigger makes and where it is configured.",
            "Replace each with a controlled endpoint you own, or disable the feature that calls it.",
            "Re-run the proof and record which dependencies are required and which are incidental.",
            "Report the required dependency explicitly, because it changes who has to fix the bug.",
        ],
        "signals": ["dependencies-named", "substitution-run", "requirements-recorded"],
        "patterns": [
            (
                "controlled endpoint",
                "curl -sS -X PUT https://api.example.com/v2/settings -d '{\"webhook\":\"https://your-listener.example/hook\"}'",
            )
        ],
        "pitfalls": [
            "Reporting a bug that only works because a webhook pointed at an attacker-controlled host you set up earlier.",
            "Leaving a live third-party call in the harness, which makes the proof fail when their service changes.",
        ],
        "done_when": [
            "Every external dependency is replaced or disabled and the result re-checked.",
            "Required versus incidental dependencies are stated in the report.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "isolate"},
    },
    {
        "slug": "isolate-blast-radius-map",
        "title": "Map what else the trigger path touches",
        "summary": "Trace the trigger to every downstream effect so the proof does not send mail, write logs or notify a customer you did not intend to involve",
        "use_when": "the trigger is on a path that fans out to notifications, audits or third parties",
        "avoid_when": "the path is a pure read with no side effects at all",
        "tags": ["isolate", "side-effects", "radius"],
        "steps": [
            "Read the response and check the account's notification settings before triggering.",
            "Disable outbound email and webhooks for the test account where the product allows it.",
            "Trigger once and enumerate the observed effects from audit logs and inboxes you control.",
            "Record every effect, including ones you believe are harmless, because they are still impact.",
        ],
        "signals": ["effects-enumerated", "notifications-disabled", "audit-reviewed"],
        "patterns": [
            (
                "disable notifications",
                "curl -sS -X PATCH https://api.example.com/v2/settings -d '{\"email_notifications\":false}'",
            )
        ],
        "pitfalls": [
            "Triggering a password-reset flow against a real address to prove enumeration.",
            "Missing an audit entry that records the action and later looks like unauthorised activity.",
        ],
        "done_when": [
            "Side effects are enumerated from an independent source such as audit logs.",
            "Notification paths were disabled before the trigger where possible.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "isolate"},
    },
    {
        "slug": "minimize-ddmin",
        "title": "Minimise a payload with delta debugging",
        "summary": "Shrink the input while the bug still reproduces, so the report contains the smallest trigger instead of a wall of irrelevant bytes",
        "use_when": "the payload is large and you do not know which part is load-bearing",
        "avoid_when": "the payload is a single field whose value is already the minimum",
        "tags": ["minimize", "ddmin", "payload"],
        "steps": [
            "Write a predicate that exits 0 exactly when the bug reproduces, and test it on the original payload.",
            "Run the minimiser with line units first, then byte units if the result is still large.",
            "Confirm the minimised input still reproduces from a clean session, not just from the harness.",
            "Store the minimised payload with the predicate used, so the reduction is reproducible.",
        ],
        "signals": ["predicate-stable", "reduction-measured", "reproduce-reconfirmed"],
        "patterns": [
            (
                "minimise",
                "poc-craft minimize --input payload.bin --predicate './check.sh {input}' --unit line --out minimal.bin",
            )
        ],
        "pitfalls": [
            "A predicate that matches on an error message the server returns for malformed input, which shrinks toward garbage that was never the bug.",
            "Trusting a minimised input without re-running it from a clean session.",
        ],
        "done_when": [
            "The predicate was verified on the original input before minimising.",
            "The minimised input reproduces and its size reduction is recorded.",
        ],
        "refs": [
            "[Zeller & Hildebrandt, simplifying failure-inducing input](https://doi.org/10.1109/32.988710)",
        ],
        "meta": {"phase": "minimize"},
    },
    {
        "slug": "minimize-predicate-design",
        "title": "Write a predicate that cannot be gamed",
        "summary": "Tie the oracle to the specific behaviour the bug causes, so minimisation cannot drift into a different failure that happens to exit non-zero",
        "use_when": "you are about to hand a predicate to a minimiser or a regression suite",
        "avoid_when": "any observable difference is acceptable, for example when searching for any crash at all",
        "tags": ["minimize", "oracle", "predicate"],
        "steps": [
            "Write the oracle as a check on a specific status code, body marker or state change, not on any error.",
            "Assert the oracle fails on a benign input, which proves it is not just detecting malformed requests.",
            "Run the predicate twice on the same input and confirm it is stable before minimising.",
            "Record the predicate source next to the payload so a reviewer can judge the oracle.",
        ],
        "signals": ["oracle-specific", "negative-control-fails", "predicate-stable"],
        "patterns": [
            (
                "strict oracle",
                "status=$(curl -sS -o body.txt -w '%{http_code}' --data-binary @\"$1\" https://api.example.com/v2/items)\n[ \"$status\" = \"500\" ] && grep -q 'stack trace' body.txt",
            )
        ],
        "pitfalls": [
            "Using a predicate that passes on any 4xx, so minimisation reduces toward a request the server rejects for syntax.",
            "A predicate that depends on a timestamp or a random value and therefore flips between runs.",
        ],
        "done_when": [
            "The oracle names the exact behaviour and fails on a benign input.",
            "Two consecutive runs agree on the same input.",
        ],
        "refs": [
            "[Zeller & Hildebrandt, simplifying failure-inducing input](https://doi.org/10.1109/32.988710)",
        ],
        "meta": {"phase": "minimize"},
    },
    {
        "slug": "minimize-structure-aware",
        "title": "Minimise structured input without breaking the format",
        "summary": "Reduce JSON, XML or protobuf by removing fields and elements rather than bytes, so the result stays parseable and the bug stays reachable",
        "use_when": "the payload is structured and byte-level removal produces invalid documents",
        "avoid_when": "the bug is a parser-level defect where malformed input is exactly the trigger",
        "tags": ["minimize", "structured", "format"],
        "steps": [
            "Parse the document and enumerate removable units: object keys, array elements, attributes and text nodes.",
            "Remove one unit at a time and re-serialise, checking the result still parses before testing the predicate.",
            "Keep removals that preserve reproduction and revert those that do not.",
            "Store the minimal document in its serialised form with the key order used during the test.",
        ],
        "signals": ["units-enumerated", "parse-validated", "minimal-document-stored"],
        "patterns": [
            (
                "structural removal",
                "python -c \"import json,sys; d=json.load(open('payload.json')); del d['unused']; json.dump(d, open('candidate.json','w'))\"",
            )
        ],
        "pitfalls": [
            "Byte-minimising JSON until it no longer parses and then testing a different code path entirely.",
            "Changing key order during reserialisation, which can change behaviour in a signature-checked API.",
        ],
        "done_when": [
            "The minimal document still parses under the same parser.",
            "Key order and serialisation form are recorded with the payload.",
        ],
        "refs": [
            "[JSON RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)",
        ],
        "meta": {"phase": "minimize"},
    },
    {
        "slug": "minimize-preserve-preconditions",
        "title": "Keep the preconditions the minimiser cannot see",
        "summary": "Pin account state, headers and sequence so a minimiser does not remove the context that makes the payload meaningful",
        "use_when": "the trigger needs a specific account, header or ordering that sits outside the payload",
        "avoid_when": "the payload alone is the whole trigger and no external state is involved",
        "tags": ["minimize", "preconditions", "context"],
        "steps": [
            "List every precondition outside the payload: account role, feature flag, header and prior request.",
            "Fix those in the harness so minimisation only varies the payload.",
            "Re-test the minimised payload against the fixed harness and then against the real environment.",
            "Report the preconditions as part of the finding, because a payload alone does not reproduce.",
        ],
        "signals": ["preconditions-pinned", "harness-fixed", "real-environment-confirmed"],
        "patterns": [
            (
                "pinned context",
                "curl -sS -H \"Authorization: Bearer $ADMIN_TOKEN\" -H 'X-Tenant: t-42' --data-binary @\"$1\" https://api.example.com/v2/admin/import",
            )
        ],
        "pitfalls": [
            "Minimising away the admin token and then reporting a bug that needs admin rights as if it were unauthenticated.",
            "Leaving the tenant header out of the harness so the bug reproduces only in one tenant by accident.",
        ],
        "done_when": [
            "Every external precondition is fixed in the harness and stated in the report.",
            "The minimised payload reproduces in the real environment with those preconditions.",
        ],
        "refs": [
            "[Zeller & Hildebrandt, simplifying failure-inducing input](https://doi.org/10.1109/32.988710)",
        ],
        "meta": {"phase": "minimize"},
    },
    {
        "slug": "payload-encoding-match",
        "title": "Match the encoding the server actually decodes",
        "summary": "Send the payload in the encoding the endpoint parses, so a rejected request is not mistaken for a blocked attack",
        "use_when": "the endpoint accepts several content types or the value passes through a proxy",
        "avoid_when": "the finding is specifically about encoding confusion between two parsers",
        "tags": ["payload", "encoding", "parsing"],
        "steps": [
            "Read the endpoint's accepted content types and pick the one whose parser you want to exercise.",
            "Encode the payload for that parser, including escaping rules and charset, and record the exact bytes.",
            "Compare the server's decoded view with what you sent, using a reflection or echo field where one exists.",
            "Test the second parser only as a deliberate confusion test, labelled as such.",
        ],
        "signals": ["content-type-matched", "bytes-recorded", "decoded-view-compared"],
        "patterns": [
            (
                "explicit content type",
                "curl -sS -X POST https://api.example.com/v2/import \\\n  -H 'Content-Type: application/json; charset=utf-8' \\\n  --data-binary @payload.json",
            )
        ],
        "pitfalls": [
            "Sending JSON with a form content type and concluding the payload was blocked when it was never parsed.",
            "Mixing charset assumptions between the request and the stored value, which changes the decoded bytes.",
        ],
        "done_when": [
            "The request content type and payload bytes are recorded exactly.",
            "The decoded view is compared against what was sent.",
        ],
        "refs": [
            "[MDN Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type)",
        ],
        "meta": {"phase": "payload"},
    },
    {
        "slug": "payload-boundary-values",
        "title": "Use boundary values instead of random noise",
        "summary": "Pick lengths, counts and indexes at the edges of what the code expects, because off-by-one and truncation bugs live at boundaries rather than in the middle",
        "use_when": "the bug is suspected to be a length, count or index handling defect",
        "avoid_when": "the bug is semantic, for example an authorisation check, where length is irrelevant",
        "tags": ["payload", "boundary", "off-by-one"],
        "steps": [
            "Find the documented or observed limit for the field, from validation messages or documentation.",
            "Send values at limit-1, limit and limit+1, and record the response for each.",
            "Include the empty value and a value one byte over the maximum encoded length.",
            "Report the exact boundary that misbehaves rather than a range.",
        ],
        "signals": ["limit-identified", "boundary-values-sent", "exact-edge-recorded"],
        "patterns": [
            (
                "boundary payloads",
                "for n in 0 63 64 65 1024 1025; do\n  python -c \"print('A'*$n, end='')\" > v.bin\n  curl -sS -o /dev/null -w \"$n %{http_code}\\n\" --data-binary @v.bin https://api.example.com/v2/echo\ndone",
            )
        ],
        "pitfalls": [
            "Sending a 10 MB payload when the limit is 64 bytes, which tests the proxy rather than the parser.",
            "Reporting only the failing case without the passing neighbour, so the boundary is not visible.",
        ],
        "done_when": [
            "The limit is identified from evidence, not guessed.",
            "Values either side of the boundary are recorded with their responses.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "payload"},
    },
    {
        "slug": "payload-type-confusion",
        "title": "Test type confusion deliberately, one coercion at a time",
        "summary": "Send the same logical value as a string, number, array and object to find where the validator and the consumer disagree about its type",
        "use_when": "a field is validated in one place and consumed in another, such as a JSON body and a database query",
        "avoid_when": "the field's type is enforced by a strict schema at every hop, which the docs or a probe confirm",
        "tags": ["payload", "type", "coercion"],
        "steps": [
            "Pick one field and send it as each JSON type in turn: string, number, boolean, array, object and null.",
            "Record which types pass validation and which change downstream behaviour.",
            "For the type that behaves differently, check the stored value and the rendered value separately.",
            "Report the specific coercion, for example an array accepted where a string is expected.",
        ],
        "signals": ["types-sent", "validation-results-recorded", "storage-checked"],
        "patterns": [
            (
                "type matrix",
                "for v in '\"1\"' '1' 'true' '[1]' '{\"a\":1}' 'null'; do\n  printf '{\"id\":%s}' \"$v\" > t.json\n  curl -sS -o /dev/null -w \"$v %{http_code}\\n\" --data-binary @t.json https://api.example.com/v2/items\ndone",
            )
        ],
        "pitfalls": [
            "Testing six types in one request, so the response cannot be attributed to a single coercion.",
            "Assuming a 200 means the value was handled correctly rather than silently coerced.",
        ],
        "done_when": [
            "Each JSON type was sent separately and its result recorded.",
            "The stored and rendered values are checked for the divergent type.",
        ],
        "refs": [
            "[JSON RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)",
        ],
        "meta": {"phase": "payload"},
    },
]