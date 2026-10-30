"""Part 3 of the poc-craft corpus: evidence, triage, report, cleanup, regression."""

from __future__ import annotations

from typing import Any

SKILLS: list[dict[str, Any]] = [
    {
        "slug": "evidence-bundle-index",
        "title": "Ship an evidence bundle with an index",
        "summary": "Package the payload, harness, raw captures and hash list behind a short index so a triager can reproduce without asking a question",
        "use_when": "the finding is ready to submit and more than one person will read it",
        "avoid_when": "the platform accepts only inline text and attachments are not supported",
        "tags": ["evidence", "bundle", "handoff"],
        "steps": [
            "List every artifact and what claim it supports.",
            "Write an index that names each file, its hash and the step it belongs to.",
            "Include the harness and payload so the reproduction is one command.",
            "Exclude anything you cannot explain, because an unexplained file invites distrust.",
        ],
        "signals": ["artifacts-listed", "index-written", "harness-included"],
        "patterns": [
            (
                "index",
                "# index\n- payload.json  sha256:...  step 3\n- poc.py        sha256:...  step 4 (harness)\n- response.body sha256:...  step 5 (impact)",
            )
        ],
        "pitfalls": [
            "A bundle that is a zip of screenshots with no index, which nobody can reproduce from.",
            "Including a captured token or cookie that has not been revoked.",
        ],
        "done_when": [
            "The index names every artifact, its hash and the step it supports.",
            "No live credential is included in the bundle.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "evidence"},
    },
    {
        "slug": "triage-severity-evidence",
        "title": "Justify severity with the evidence you actually have",
        "summary": "Map each severity claim to an artifact, so a high rating rests on observed access rather than on a plausible chain of guesses",
        "use_when": "you are about to assign a severity rating",
        "avoid_when": "the platform assigns severity automatically from the finding type",
        "tags": ["triage", "severity", "evidence"],
        "steps": [
            "Write the impact sentence first, then the severity it implies.",
            "Attach the artifact that proves each clause of the sentence.",
            "Downgrade any clause without an artifact to an inference, and rate the observed part.",
            "Record the rating rationale in the report so a disagreement can be about facts.",
        ],
        "signals": ["impact-written", "artifacts-mapped", "inferences-downgraded"],
        "patterns": [
            (
                "mapping",
                "impact: read one record from another tenant\nevidence: response.body (owner=victim-tenant)\nseverity basis: cross-tenant confidentiality, single record",
            )
        ],
        "pitfalls": [
            "Rating critical on a chain that was never executed end to end.",
            "Leaving the severity basis implicit, so the first reviewer to disagree cannot see what was assumed.",
        ],
        "done_when": [
            "Every severity clause maps to an artifact or is labelled inference.",
            "The rating basis is written in the report.",
        ],
        "refs": [
            "[CVSS specification](https://www.first.org/cvss/v4-0/specification-document)",
        ],
        "meta": {"phase": "triage"},
    },
    {
        "slug": "triage-duplicate-check",
        "title": "Check for duplicates against known reports",
        "summary": "Search prior reports and advisories for the same root cause before submitting, so a duplicate is caught by you rather than a triager",
        "use_when": "the program has a public or internal history of reports",
        "avoid_when": "the program is brand new with no history to search",
        "tags": ["triage", "duplicates", "history"],
        "steps": [
            "Search the program's disclosed reports and the vendor's advisories for the same endpoint and defect class.",
            "Compare the root cause, not the URL, since a duplicate is the same fix.",
            "Reference any near duplicate in your submission and explain what differs.",
            "Record the searches performed, so the check is visible rather than claimed.",
        ],
        "signals": ["searched", "root-cause-compared", "near-duplicates-cited"],
        "patterns": [
            (
                "search",
                "curl -sS 'https://api.example.com/search?q=export+traversal' -H \"Authorization: Bearer $TOKEN\"",
            )
        ],
        "pitfalls": [
            "Searching only by endpoint and missing an advisory that fixed the same root cause elsewhere.",
            "Submitting without any search and having the report closed as a duplicate on day one.",
        ],
        "done_when": [
            "Searches are recorded and root causes compared.",
            "Any near duplicate is cited with the difference stated.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "triage"},
    },
    {
        "slug": "triage-fix-scope",
        "title": "Describe the fix scope without prescribing code",
        "summary": "Name the component and the check that must change so the report helps the fix without turning into a patch the client did not ask for",
        "use_when": "the report includes a remediation section",
        "avoid_when": "the client explicitly asked for a patch",
        "tags": ["triage", "fix", "scope"],
        "steps": [
            "Identify the component where the check is missing or wrong, using the request path as evidence.",
            "State the invariant that should hold, for example every export filter is resolved inside the tenant root.",
            "List the sibling endpoints likely to share the defect, marked as unverified.",
            "Stop at the invariant; leave the implementation to the owner.",
        ],
        "signals": ["component-named", "invariant-stated", "siblings-listed"],
        "patterns": [
            (
                "fix statement",
                "component: export handler\ninvariant: resolved path must remain under the tenant export root\nsuspected siblings: import, backup (unverified)",
            )
        ],
        "pitfalls": [
            "Pasting a patch that touches files you have never compiled.",
            "Naming the wrong component because the request path differs from the internal handler.",
        ],
        "done_when": [
            "The component and invariant are stated with the evidence that located them.",
            "Unverified siblings are labelled as such.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "triage"},
    },
    {
        "slug": "triage-reproducer-review",
        "title": "Review the reproducer as a stranger would",
        "summary": "Run the reproducer from a clean machine using only what the report contains, so any missing step is found before the triager finds it",
        "use_when": "the report is written and about to be submitted",
        "avoid_when": "the reproducer requires access the reviewer will obviously have",
        "tags": ["triage", "review", "clarity"],
        "steps": [
            "Copy only the report's reproduction section into a fresh directory.",
            "Run it without opening any other notes, and note the first point where you need information that is not there.",
            "Fix the report rather than the environment, then re-run from scratch.",
            "Record that the clean run succeeded, including the environment used.",
        ],
        "signals": ["clean-dir-run", "missing-step-found", "report-fixed"],
        "patterns": [
            (
                "clean run",
                "tmp=$(mktemp -d) && cd \"$tmp\" && cp /path/to/submission/* . && python poc.py",
            )
        ],
        "pitfalls": [
            "Running from your working directory where the extra file happens to exist.",
            "Silently fixing the environment, which leaves the report unusable for the next reader.",
        ],
        "done_when": [
            "The reproducer runs from a clean directory using only submitted files.",
            "Any missing step found was added to the report, not worked around.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "triage"},
    },
    {
        "slug": "report-summary-line",
        "title": "Write a summary line that states the defect",
        "summary": "Lead with what is broken and where, in one sentence a triager can route, instead of a narrative that buries the finding",
        "use_when": "you are writing the title or the first line of the report",
        "avoid_when": "the platform generates titles from fields you fill in separately",
        "tags": ["report", "summary", "routing"],
        "steps": [
            "Name the component, the missing check and the observed impact in one sentence.",
            "Avoid adjectives such as critical or severe in the title; those belong in the severity field.",
            "Include the condition that makes it reachable, such as an authenticated tenant user.",
            "Check the sentence against the evidence and remove any clause you cannot prove.",
        ],
        "signals": ["component-named", "impact-stated", "condition-included"],
        "patterns": [
            (
                "summary",
                "Export filter path traversal allows a tenant user to read files outside the tenant export root",
            )
        ],
        "pitfalls": [
            "A title of possible RCE that the body never demonstrates.",
            "A title with no component, so two different bugs look like the same report.",
        ],
        "done_when": [
            "The summary names the component, the defect and the observed impact.",
            "Every clause in it is backed by an artifact.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "report"},
    },
    {
        "slug": "report-reproduction-steps",
        "title": "Write reproduction steps that run in order",
        "summary": "Number the steps so each one has a command, an expected result and the artifact it produces, with no step that assumes unstated state",
        "use_when": "the report includes a reproduction section",
        "avoid_when": "the finding is demonstrated by a single request that needs no steps",
        "tags": ["report", "reproduction", "steps"],
        "steps": [
            "Start from account creation or token issuance so the reader has the same starting point.",
            "Give each step one command, the expected output and the artifact it should produce.",
            "State the environment and version at the top, including any feature flags.",
            "End with the step that shows the impact and the artifact that proves it.",
        ],
        "signals": ["ordered-steps", "expected-outputs", "artifacts-linked"],
        "patterns": [
            (
                "step",
                "3. Send the trigger request:\n   curl ... --data-binary @payload.json\n   expect: HTTP 500 with a stack trace\n   artifact: response.body",
            )
        ],
        "pitfalls": [
            "Starting at step 3 because steps 1 and 2 were obvious to you.",
            "Steps without expected output, so the reader cannot tell a success from a failure.",
        ],
        "done_when": [
            "Every step has a command, an expected result and an artifact.",
            "The environment and flags are stated before the steps.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "report"},
    },
    {
        "slug": "report-impact-statement",
        "title": "Separate observed impact from inferred impact",
        "summary": "State what you saw, then what it could lead to, in two labelled paragraphs, so the reader can rate the finding on evidence",
        "use_when": "the observed effect is smaller than the plausible worst case",
        "avoid_when": "the worst case was directly observed and needs no separation",
        "tags": ["report", "impact", "honesty"],
        "steps": [
            "Write the observed impact with the artifact that proves it.",
            "Write the inferred impact under a separate heading and name the assumption it depends on.",
            "Say what would be needed to confirm the inference.",
            "Keep the two paragraphs physically separate so they cannot be read as one claim.",
        ],
        "signals": ["observed-labelled", "inferred-labelled", "assumption-named"],
        "patterns": [
            (
                "impact",
                "Observed: one record from tenant B was returned to a tenant A user.\nInferred: with a valid record id the same request would return any tenant's record.\nAssumption: ids are sequential.",
            )
        ],
        "pitfalls": [
            "Blending the two into one paragraph so the inference reads as observed.",
            "Dropping the inference, which undersells a real bug and invites a low rating.",
        ],
        "done_when": [
            "Observed and inferred impacts are separate and each names its basis.",
            "The confirmation step for the inference is stated.",
        ],
        "refs": [
            "[CVSS specification](https://www.first.org/cvss/v4-0/specification-document)",
        ],
        "meta": {"phase": "report"},
    },
    {
        "slug": "report-attachment-hygiene",
        "title": "Keep credentials out of the report",
        "summary": "Redact tokens, cookies and personal data from every attachment while keeping the request replayable with placeholders",
        "use_when": "the evidence contains an authorization header or personal data",
        "avoid_when": "the program explicitly requires a live token and provides a dedicated test account",
        "tags": ["report", "redaction", "hygiene"],
        "steps": [
            "List every secret and personal field in the captured requests and responses.",
            "Replace each with a placeholder that names its type, such as TOKEN or VICTIM_EMAIL.",
            "Add a note that the placeholder is redacted so a reader does not try to replay it literally.",
            "Re-scan the attachments for the original values before submitting.",
        ],
        "signals": ["secrets-listed", "placeholders-used", "rescan-clean"],
        "patterns": [
            (
                "redaction",
                "sed -E 's/(Authorization: Bearer )[A-Za-z0-9._-]+/\\1<TOKEN>/' request.txt > request.redacted.txt\ngrep -nE 'eyJ[A-Za-z0-9_-]{10,}' request.redacted.txt || echo clean",
            )
        ],
        "pitfalls": [
            "Redacting the header but leaving the token in a response body or an error message.",
            "Submitting a live token that remains valid after the report is closed.",
        ],
        "done_when": [
            "Every secret and personal field is replaced with a typed placeholder.",
            "A rescan of the attachments finds no original value.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "report"},
    },
    {
        "slug": "cleanup-test-data",
        "title": "Remove the data the proof created",
        "summary": "Delete or revert every record, file and setting the proof touched, and verify the removal rather than assuming it",
        "use_when": "the engagement is ending and test artifacts remain in the target",
        "avoid_when": "the client wants the data preserved for their own investigation",
        "tags": ["cleanup", "data", "reversal"],
        "steps": [
            "List every resource created or modified, with its identifier and the operation used.",
            "Delete or revert each one through the documented path, recording the response.",
            "Re-read each resource to confirm it is gone or restored.",
            "Report anything that could not be removed, because that is a client action item.",
        ],
        "signals": ["resources-listed", "removal-attempted", "absence-verified"],
        "patterns": [
            (
                "delete and verify",
                "curl -sS -X DELETE -H \"Authorization: Bearer $TOKEN\" https://api.example.com/v2/items/4242 -o /dev/null -w '%{http_code}\\n'\ncurl -sS -o /dev/null -w '%{http_code}\\n' -H \"Authorization: Bearer $TOKEN\" https://api.example.com/v2/items/4242",
            )
        ],
        "pitfalls": [
            "Deleting through an undocumented path that leaves an orphaned child record.",
            "Assuming a 204 means gone without re-reading the resource.",
        ],
        "done_when": [
            "Every touched resource is removed or reverted and its absence verified.",
            "Anything not removable is reported as a client action item.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "cleanup"},
    },
    {
        "slug": "cleanup-revoke-credentials",
        "title": "Revoke every credential the test minted",
        "summary": "Invalidate tokens, API keys and sessions created during the engagement so a leaked attachment cannot be used later",
        "use_when": "the engagement created credentials or captured tokens in evidence",
        "avoid_when": "the credentials belong to the client and are still needed for verification",
        "tags": ["cleanup", "credentials", "revocation"],
        "steps": [
            "List every token, key and session created or captured, with its scope and expiry.",
            "Revoke each one through the documented endpoint and record the response.",
            "Attempt one request with a revoked token to confirm it now fails.",
            "Record the revocation time with the evidence so the window is known.",
        ],
        "signals": ["credentials-listed", "revocation-confirmed", "reuse-blocked"],
        "patterns": [
            (
                "revoke",
                "curl -sS -X POST -H \"Authorization: Bearer $TOKEN\" https://api.example.com/v2/tokens/revoke -d '{\"token\":\"...\"}'",
            )
        ],
        "pitfalls": [
            "Revoking the API key but leaving a refresh token that can mint a new one.",
            "Leaving a token in a submitted attachment after the engagement closes.",
        ],
        "done_when": [
            "Every created or captured credential is revoked and a reuse attempt fails.",
            "The revocation time is recorded with the evidence.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "cleanup"},
    },
    {
        "slug": "cleanup-artifact-retention",
        "title": "Decide what evidence to keep and for how long",
        "summary": "Keep the minimum evidence needed to defend the report, and delete captures that contain personal data once triage closes",
        "use_when": "the evidence includes other users' personal data",
        "avoid_when": "the client's contract specifies a retention period that overrides your default",
        "tags": ["cleanup", "retention", "privacy"],
        "steps": [
            "Classify each artifact: needed for defence, useful context, or containing personal data.",
            "Keep the first, summarise the second, and delete or anonymise the third after triage.",
            "Record the retention decision and the deletion date for each deleted artifact.",
            "Keep hashes of deleted artifacts so their existence and integrity remain auditable.",
        ],
        "signals": ["artifacts-classified", "deletion-recorded", "hashes-retained"],
        "patterns": [
            (
                "retain hash, delete body",
                "sha256sum victim-response.json >> deleted.sha256\nshred -u victim-response.json",
            )
        ],
        "pitfalls": [
            "Keeping a victim's personal data indefinitely because it was convenient.",
            "Deleting the artifact that proves the impact before triage has accepted the finding.",
        ],
        "done_when": [
            "Each artifact has a retention decision and deletions are dated.",
            "Hashes of deleted artifacts are retained.",
        ],
        "refs": [
            "[GDPR data minimisation](https://gdpr-info.eu/art-5-gdpr/)",
        ],
        "meta": {"phase": "cleanup"},
    },
    {
        "slug": "regression-payload-library",
        "title": "Keep the payload as a versioned fixture",
        "summary": "Store the minimised payload and its predicate in a fixture directory with a revision, so later findings can reuse and compare against it",
        "use_when": "the same class of bug is likely to recur across endpoints",
        "avoid_when": "the payload contains live credentials or personal data",
        "tags": ["regression", "fixtures", "reuse"],
        "steps": [
            "Store the minimised payload with a name that encodes the defect class and endpoint.",
            "Store the predicate beside it and a one-line note on what reproduction looks like.",
            "Record the target version it was verified against.",
            "Reference the fixture from the report instead of inlining the payload twice.",
        ],
        "signals": ["fixture-stored", "predicate-paired", "version-recorded"],
        "patterns": [
            (
                "fixture layout",
                "fixtures/export-traversal/\n  payload.json\n  check.sh\n  note.md   (verified against build 2026.10.30)",
            )
        ],
        "pitfalls": [
            "Naming fixtures by date only, so nobody can tell what defect class they exercise.",
            "Reusing a payload against a new version without re-verifying it.",
        ],
        "done_when": [
            "The payload, predicate and target version are stored together.",
            "The report references the fixture rather than duplicating it.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "regression"},
    },
    {
        "slug": "regression-verify-fix",
        "title": "Verify the fix against the original reproducer",
        "summary": "Re-run the exact reproducer on the fixed build and report the result, because a fix that changes behaviour elsewhere may not address the finding",
        "use_when": "the client reports that the issue is fixed",
        "avoid_when": "the fix is not deployed to an environment you can reach",
        "tags": ["regression", "fix", "verification"],
        "steps": [
            "Run the original minimised input and oracle against the fixed build.",
            "Confirm the oracle now returns false and record the new response.",
            "Check that the benign control still behaves as before, so the fix did not simply block the endpoint.",
            "Run the sibling endpoints from the fix scope, since a fix is often partial.",
        ],
        "signals": ["original-reproducer-run", "oracle-now-false", "siblings-checked"],
        "patterns": [
            (
                "post-fix run",
                "python poc.py; echo \"exit=$?\"   # expect non-zero after the fix\npython control.py; echo \"control exit=$?\"",
            )
        ],
        "pitfalls": [
            "Accepting a fix because the endpoint now returns 403 for everyone, which is a regression not a fix.",
            "Testing only the reported endpoint and leaving the sibling with the same defect open.",
        ],
        "done_when": [
            "The original reproducer no longer satisfies the oracle and the control is unchanged.",
            "Sibling endpoints from the fix scope are checked and reported.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "regression"},
    },
    {
        "slug": "regression-adjacent-endpoints",
        "title": "Check the endpoints that share the defect",
        "summary": "Test the sibling routes that use the same handler or middleware, so a fix applied to one route does not leave the class open",
        "use_when": "the finding came from a shared middleware or handler",
        "avoid_when": "the defect is provably local to one route's own code",
        "tags": ["regression", "siblings", "coverage"],
        "steps": [
            "List every route that uses the same handler, middleware or template.",
            "Send the same minimised payload to each, adapted only in the route name.",
            "Record which routes reproduce, which are blocked and which behave differently.",
            "Report the full set, marking unverified routes as unverified rather than assuming.",
        ],
        "signals": ["siblings-listed", "payloads-sent", "results-recorded"],
        "patterns": [
            (
                "sibling sweep",
                "for route in export import backup; do\n  curl -sS -o /dev/null -w \"$route %{http_code}\\n\" -X POST -H \"Authorization: Bearer $T\" --data-binary @payload.json \"https://api.example.com/v2/$route\"\ndone",
            )
        ],
        "pitfalls": [
            "Assuming a sibling is fixed because the reported route is, without testing it.",
            "Sending the payload to every route in the product and calling it scope.",
        ],
        "done_when": [
            "Every route sharing the handler is tested and its result recorded.",
            "Unverified routes are labelled rather than assumed safe.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "regression"},
    },
    {
        "slug": "regression-closeout-note",
        "title": "Close the finding with what changed",
        "summary": "Record the fix version, the verification result and the residual risk in one note, so the finding can be closed without rereading the whole thread",
        "use_when": "the finding is verified fixed and the ticket is being closed",
        "avoid_when": "the finding is still open or disputed",
        "tags": ["regression", "closeout", "record"],
        "steps": [
            "Record the build or version where the fix was observed.",
            "State the verification result for the original reproducer and the sibling sweep.",
            "Name any residual risk, such as a route that was not reachable for testing.",
            "Link the fixture and the post-fix capture so the note is self-contained.",
        ],
        "signals": ["fix-version-recorded", "verification-summarised", "residual-risk-named"],
        "patterns": [
            (
                "closeout",
                "fix verified in build 2026.11.2\noriginal reproducer: blocked (403)\nsibling sweep: 2 blocked, 1 unverified (route disabled)\nresidual: import route untested",
            )
        ],
        "pitfalls": [
            "Closing with fixed without naming the version, which makes the claim untraceable.",
            "Omitting the residual risk so a later regression looks like a new finding.",
        ],
        "done_when": [
            "The fix version, verification result and residual risk are recorded.",
            "The note links to the fixture and the post-fix capture.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "regression"},
    },
]