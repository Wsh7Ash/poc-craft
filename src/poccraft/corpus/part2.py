"""Part 2 of the poc-craft corpus: payload, harness, automate, verify, evidence."""

from __future__ import annotations

from typing import Any

SKILLS: list[dict[str, Any]] = [
    {
        "slug": "payload-header-smuggling-probe",
        "title": "Probe header handling without breaking the request",
        "summary": "Test whether a proxy and an origin disagree about a header by sending a syntactically valid request and reading which one acts on it",
        "use_when": "a request passes through a CDN or reverse proxy before reaching the application",
        "avoid_when": "there is no intermediary and headers are read by a single server",
        "tags": ["payload", "headers", "proxy"],
        "steps": [
            "Identify the intermediary from response headers such as server and via, and record it.",
            "Send a request with one header expressed exactly once, then with a duplicated form, and compare which value takes effect.",
            "Use a behaviour you can observe, such as a reflected value or a routing decision, rather than guessing.",
            "Report the disagreement between hops, naming both observed values.",
        ],
        "signals": ["intermediary-identified", "values-compared", "disagreement-shown"],
        "patterns": [
            (
                "duplicate header probe",
                "curl -sS -i https://app.example.com/echo \\\n  -H 'X-Forwarded-Host: a.example' \\\n  -H 'X-Forwarded-Host: b.example'",
            )
        ],
        "pitfalls": [
            "Crafting a request that neither hop parses, then reporting the resulting error as a vulnerability.",
            "Assuming a CDN strips a header because the response did not reflect it; reflection and routing differ.",
        ],
        "done_when": [
            "Both hops are identified and their handling of the header is compared with observed evidence.",
            "The disagreement is stated with the values each hop used.",
        ],
        "refs": [
            "[RFC 9110 HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110)",
        ],
        "meta": {"phase": "payload"},
    },
    {
        "slug": "payload-path-encoding-layers",
        "title": "Encode path segments for the layer that reads them",
        "summary": "Choose percent-encoding, double-encoding or raw separators based on which component parses the path first, so a bypass claim names the layer it defeats",
        "use_when": "a path-based access control check sits in front of a file read or a route match",
        "avoid_when": "the path is normalised once by a single framework before any check runs",
        "tags": ["payload", "encoding", "path"],
        "steps": [
            "Determine how many decoding passes the request receives by sending an encoded separator and observing routing.",
            "For each pass, construct the encoding that survives it and reaches the sink unchanged.",
            "Verify the sink's view with a reflection endpoint or an error message that echoes the resolved path.",
            "State the number of passes and the exact bytes used, because the claim depends on both.",
        ],
        "signals": ["pass-count-measured", "encoding-constructed", "sink-view-confirmed"],
        "patterns": [
            (
                "encoding ladder",
                "for p in '..%2fetc%2fpasswd' '..%252fetc%252fpasswd' '%2e%2e%2fetc%2fpasswd'; do\n  curl -sS -o /dev/null -w \"$p %{http_code}\\n\" \"https://app.example.com/files/$p\"\ndone",
            )
        ],
        "pitfalls": [
            "Reporting a traversal that was blocked at the proxy when the application never saw the path.",
            "Using one encoding without measuring the pass count, so the payload works by luck on one deployment.",
        ],
        "done_when": [
            "The number of decoding passes is measured, not assumed.",
            "The encoding used and the resolved sink path are both recorded.",
        ],
        "refs": [
            "[OWASP path traversal](https://owasp.org/www-community/attacks/Path_Traversal)",
        ],
        "meta": {"phase": "payload"},
    },
    {
        "slug": "harness-python-scaffold",
        "title": "Generate the harness instead of hand-writing it",
        "summary": "Emit a harness from the request specification so the proof has one request path, one oracle and a repeat count that exposes flakiness",
        "use_when": "the proof will be run more than once, including by a reviewer",
        "avoid_when": "a single curl command already captures the whole proof",
        "tags": ["harness", "scaffold", "python"],
        "steps": [
            "Write the URL, method, payload path and oracle expression into the generator.",
            "Generate the Python harness and review the oracle expression before running it.",
            "Run it once to confirm it fails on a benign payload and passes on the triggering one.",
            "Commit the generated harness beside the payload and record the generator version.",
        ],
        "signals": ["harness-generated", "oracle-reviewed", "control-run-fails"],
        "patterns": [
            (
                "generate",
                "poc-craft scaffold --url https://api.example.com/v2/export --method POST \\\n  --payload payload.json --oracle 'status == 500' --repeat 3 --out poc.py",
            )
        ],
        "pitfalls": [
            "Hand-editing a generated harness and then reporting the generator as the source of the evidence.",
            "Leaving the oracle as the default `status >= 500` when the bug is a 200 with leaked data.",
        ],
        "done_when": [
            "The generated harness runs and its oracle is specific to the finding.",
            "A benign payload is shown to fail the oracle.",
        ],
        "refs": [
            "[Python urllib.request](https://docs.python.org/3/library/urllib.request.html)",
        ],
        "meta": {"phase": "harness"},
    },
    {
        "slug": "harness-repeat-for-flakiness",
        "title": "Repeat the run to expose flakiness",
        "summary": "Run the proof several times and report the hit rate, because a race or a cache that reproduces once in five attempts is a different finding from a deterministic one",
        "use_when": "the bug involves concurrency, caching or a load balancer",
        "avoid_when": "the bug is deterministic and repetition only costs time",
        "tags": ["harness", "flakiness", "repetition"],
        "steps": [
            "Run the proof five times from a clean session for each attempt.",
            "Record the outcome of every attempt rather than a summary.",
            "If the hit rate is below 100%, describe the condition that correlates with a hit.",
            "Report the rate and the condition together, since neither is meaningful alone.",
        ],
        "signals": ["attempts-recorded", "hit-rate-computed", "condition-identified"],
        "patterns": [
            (
                "repeat",
                "poc-craft scaffold --url https://api.example.com/v2/race --payload p.json --repeat 5 --out poc.py",
            )
        ],
        "pitfalls": [
            "Reporting `intermittent` with no rate, which a triager cannot reproduce.",
            "Reusing one session across attempts so a cache makes later attempts behave differently.",
        ],
        "done_when": [
            "Per-attempt outcomes and a hit rate are recorded.",
            "Any correlated condition is stated alongside the rate.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "harness"},
    },
    {
        "slug": "harness-timeout-and-retry",
        "title": "Bound every request with a timeout and no silent retry",
        "summary": "Set an explicit timeout and disable automatic retries so a hung or retried request is visible as a failure rather than as a slow success",
        "use_when": "the target is remote, slow or behind a load balancer",
        "avoid_when": "the bug is a timeout itself, where retries must be part of the measurement",
        "tags": ["harness", "timeout", "retries"],
        "steps": [
            "Set a connect and read timeout on every request in the harness.",
            "Disable automatic retry so one attempt produces one request in the server log.",
            "Record the elapsed time per attempt alongside the outcome.",
            "Correlate the harness attempt count with the server's access log to prove no hidden retries.",
        ],
        "signals": ["timeouts-set", "retries-disabled", "attempts-correlated"],
        "patterns": [
            (
                "timeout",
                "urllib.request.urlopen(request, timeout=15)",
            )
        ],
        "pitfalls": [
            "A client library that retries on 503 turns one logical attempt into three requests and triples the impact.",
            "No timeout at all, so a hung connection looks like the harness is still running.",
        ],
        "done_when": [
            "Every request has a timeout and retries are disabled or counted.",
            "The harness attempt count matches the server's request count.",
        ],
        "refs": [
            "[urllib.request timeout](https://docs.python.org/3/library/urllib.request.html)",
        ],
        "meta": {"phase": "harness"},
    },
    {
        "slug": "harness-cleanup-fixture",
        "title": "Clean up what the harness creates",
        "summary": "Delete or revert the resources the harness creates on success and on failure, so a repeated run starts from the same state",
        "use_when": "the proof writes data, uploads files or changes settings",
        "avoid_when": "the written record is itself the evidence and must be preserved until triage",
        "tags": ["harness", "cleanup", "repeatability"],
        "steps": [
            "Enumerate every resource the harness creates or mutates and its delete endpoint or revert step.",
            "Run cleanup in a finally block so a failure mid-proof still cleans up.",
            "Verify cleanup by re-reading the resource and confirming it is gone or restored.",
            "Preserve a snapshot of what was created as evidence before deleting it.",
        ],
        "signals": ["resources-enumerated", "cleanup-in-finally", "absence-verified"],
        "patterns": [
            (
                "cleanup",
                "try:\n    run_proof()\nfinally:\n    delete_created_resources()\n",
            )
        ],
        "pitfalls": [
            "Cleaning up only on success, so a failed run leaves data that makes the next run behave differently.",
            "Deleting the evidence along with the resource.",
        ],
        "done_when": [
            "Cleanup runs on both success and failure and its effect is verified.",
            "Evidence of the created resource is preserved separately.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "harness"},
    },
    {
        "slug": "automate-bounded-loop",
        "title": "Automate enumeration with a hard bound",
        "summary": "Loop over candidate identifiers with a maximum count, a delay and a stop condition, so automation cannot walk a production table",
        "use_when": "the finding needs a sample of identifiers to show a pattern",
        "avoid_when": "a single request already proves the finding",
        "tags": ["automate", "enumeration", "bounds"],
        "steps": [
            "Set a maximum iteration count that is small enough to be defensible, such as ten.",
            "Add a delay between requests and record it.",
            "Stop on the first unexpected response so the loop does not continue past an anomaly.",
            "Record the exact range attempted, so the blast radius is a fact rather than an estimate.",
        ],
        "signals": ["bound-set", "delay-recorded", "range-recorded"],
        "patterns": [
            (
                "bounded enumeration",
                "for i in $(seq 1 10); do\n  curl -sS -o /dev/null -w \"$i %{http_code}\\n\" -H \"Authorization: Bearer $T\" https://api.example.com/v2/items/$i\n  sleep 0.5\ndone",
            )
        ],
        "pitfalls": [
            "An unbounded loop over sequential IDs that touches thousands of real records.",
            "No delay, so the automation trips a rate limit and the 429s are misread as access control working.",
        ],
        "done_when": [
            "The loop has a maximum count, a delay and a stop condition.",
            "The attempted range is recorded exactly.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "automate"},
    },
    {
        "slug": "automate-parallel-safety",
        "title": "Keep parallel runs from contaminating each other",
        "summary": "Give each parallel attempt its own account, payload and output path, so a race proof is not actually measuring cross-talk between your own workers",
        "use_when": "the proof depends on simultaneous requests",
        "avoid_when": "the proof is sequential and parallelism adds only noise",
        "tags": ["automate", "concurrency", "isolation"],
        "steps": [
            "Assign each worker a distinct identifier and a distinct output file.",
            "Synchronise the start with a barrier so the requests are genuinely simultaneous.",
            "Record per-worker timings to show the overlap that the claim depends on.",
            "Re-run the same setup with the barrier disabled as a control.",
        ],
        "signals": ["workers-isolated", "barrier-used", "overlap-recorded"],
        "patterns": [
            (
                "barrier",
                "import threading\nbarrier = threading.Barrier(n)\ndef worker(i):\n    barrier.wait()\n    send(i)\n",
            )
        ],
        "pitfalls": [
            "Workers sharing one account, so the server serialises them and the race never happens.",
            "Claiming a race from timestamps that never overlapped.",
        ],
        "done_when": [
            "Per-worker isolation and overlap are recorded.",
            "A no-barrier control run is compared against the parallel run.",
        ],
        "refs": [
            "[Python threading barrier](https://docs.python.org/3/library/threading.html#threading.Barrier)",
        ],
        "meta": {"phase": "automate"},
    },
    {
        "slug": "automate-ci-regression",
        "title": "Turn the proof into a regression check",
        "summary": "Package the minimised input and oracle as a check that fails when the bug returns, so the finding stays fixed after the report is closed",
        "use_when": "the client has agreed to verify the fix",
        "avoid_when": "the environment cannot be reset between runs, which makes the check unreliable",
        "tags": ["automate", "regression", "ci"],
        "steps": [
            "Commit the minimised payload and the predicate into the target's test tree, not only into your notes.",
            "Make the test set up its own preconditions and clean them up.",
            "Run it against the vulnerable build to confirm it fails, and against the fixed build to confirm it passes.",
            "Record both runs in the report as the acceptance criteria for the fix.",
        ],
        "signals": ["payload-committed", "fails-on-vulnerable", "passes-on-fixed"],
        "patterns": [
            (
                "regression test",
                "def test_export_traversal(client, admin_token):\n    response = client.post('/v2/export', json={'filter': '../'}, headers={'Authorization': admin_token})\n    assert response.status_code != 500\n",
            )
        ],
        "pitfalls": [
            "A regression test that depends on a live third-party service and fails for unrelated reasons.",
            "Only running it against the fixed build, so it is never shown to detect the original bug.",
        ],
        "done_when": [
            "The check fails on the vulnerable build and passes on the fixed one.",
            "Both results are recorded in the report.",
        ],
        "refs": [
            "[pytest documentation](https://docs.pytest.org/)",
        ],
        "meta": {"phase": "automate"},
    },
    {
        "slug": "verify-negative-control",
        "title": "Run a negative control before claiming success",
        "summary": "Send a benign request through the same harness and show it does not satisfy the oracle, which proves the oracle is not simply detecting any error",
        "use_when": "the oracle is an error code, a body marker or a length threshold",
        "avoid_when": "the oracle is an exact value that cannot be produced accidentally",
        "tags": ["verify", "control", "oracle"],
        "steps": [
            "Substitute the triggering value with a benign value and run the same harness.",
            "Confirm the oracle returns false for the benign request and record the response.",
            "If the control also passes, fix the oracle before continuing.",
            "Store the control result next to the positive result in the evidence bundle.",
        ],
        "signals": ["control-run", "control-fails-oracle", "both-results-stored"],
        "patterns": [
            (
                "control",
                "poc-craft scaffold --url https://api.example.com/v2/export --payload benign.json --oracle 'status == 500' --out control.py\npython control.py; echo \"control exit=$?\"",
            )
        ],
        "pitfalls": [
            "An oracle of any 5xx that also fires on a malformed benign request, making the control pass too.",
            "Recording only the positive run, so a reviewer cannot see the control.",
        ],
        "done_when": [
            "The control fails the oracle and both results are stored.",
            "The oracle is shown to distinguish the trigger from a benign request.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "verify"},
    },
    {
        "slug": "verify-oracle-specific",
        "title": "Tie the oracle to the bug's observable effect",
        "summary": "Check the specific effect the finding claims, such as another tenant's field or a command output, instead of a proxy signal like response length",
        "use_when": "the finding is about data exposure or command execution rather than a crash",
        "avoid_when": "the only observable effect genuinely is a crash or a status code",
        "tags": ["verify", "oracle", "impact"],
        "steps": [
            "Write down the exact observable that the claim depends on, such as field X containing tenant B's value.",
            "Assert on that observable with a value only the victim account could produce.",
            "Check a value that a benign request cannot return, to avoid a false positive from cached content.",
            "Record the raw response that contains the observable.",
        ],
        "signals": ["observable-named", "victim-value-asserted", "raw-response-stored"],
        "patterns": [
            (
                "assert on victim data",
                "grep -q '\"owner\":\"victim-tenant\"' response.json && echo reproduced",
            )
        ],
        "pitfalls": [
            "Using response length as the oracle, which changes when the server adds a header or an error hint.",
            "Asserting on a field the attacker account can also legitimately read.",
        ],
        "done_when": [
            "The oracle asserts on a victim-only value, not a proxy signal.",
            "The raw response containing it is stored as evidence.",
        ],
        "refs": [
            "[OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)",
        ],
        "meta": {"phase": "verify"},
    },
    {
        "slug": "verify-determinism",
        "title": "Show the result is deterministic or quantify it",
        "summary": "Repeat the proof under identical conditions and state whether it reproduces every time, most times or only with a described setup",
        "use_when": "you are about to write a report sentence containing always, sometimes or occasionally",
        "avoid_when": "the finding is explicitly about a one-shot condition that cannot be repeated",
        "tags": ["verify", "determinism", "reliability"],
        "steps": [
            "Define the exact conditions of one attempt, including state reset.",
            "Run at least five attempts and record each outcome.",
            "Compute the rate and describe any condition that separates hits from misses.",
            "Write the report sentence from the measurement rather than from memory.",
        ],
        "signals": ["conditions-defined", "attempts-recorded", "rate-stated"],
        "patterns": [
            (
                "ten attempts",
                "for i in $(seq 1 5); do python poc.py >/dev/null 2>&1; echo \"attempt $i exit=$?\"; done",
            )
        ],
        "pitfalls": [
            "Writing always reproducible after a single successful run.",
            "Resetting state between attempts for one test and not the other, which makes the rates incomparable.",
        ],
        "done_when": [
            "At least five attempts are recorded under defined conditions.",
            "The report states a rate and any separating condition.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "verify"},
    },
    {
        "slug": "verify-fresh-account",
        "title": "Verify from a freshly created account",
        "summary": "Repeat the proof with an account created after the harness was written, so the result does not depend on data you happened to have",
        "use_when": "the proof ran against an account with a long history of test data",
        "avoid_when": "creating accounts is out of scope or rate limited by the engagement",
        "tags": ["verify", "accounts", "freshness"],
        "steps": [
            "Create a new account with the minimum role the proof requires.",
            "Create only the data the proof's preconditions state, and record it.",
            "Run the harness unchanged and compare the outcome with the original run.",
            "Record both account identifiers and the creation times with the evidence.",
        ],
        "signals": ["fresh-account-created", "minimal-data-created", "outcomes-compared"],
        "patterns": [
            (
                "fresh account",
                "curl -sS -X POST https://api.example.com/v2/signup -d '{\"email\":\"poc+1@your-domain.example\"}'",
            )
        ],
        "pitfalls": [
            "Relying on data created by an earlier engagement, which the client cannot reproduce.",
            "Creating the fresh account with a higher role than the proof needs, which weakens the impact claim.",
        ],
        "done_when": [
            "The proof runs from a newly created, minimally privileged account.",
            "Both account identifiers and the comparison are recorded.",
        ],
        "refs": [
            "[OWASP testing guide](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "verify"},
    },
    {
        "slug": "verify-impact-minimal",
        "title": "Verify the smallest impact claim you can defend",
        "summary": "Check the weakest effect the bug proves and report that, rather than extrapolating to the worst case the bug might allow",
        "use_when": "the bug could plausibly lead to something larger but you only observed a small effect",
        "avoid_when": "the larger effect was directly observed and evidenced",
        "tags": ["verify", "impact", "honesty"],
        "steps": [
            "Write the impact you directly observed as one sentence with its evidence.",
            "Write the impact you infer, clearly separated and labelled as inference.",
            "Check whether one more low-risk request would confirm the inference; if not, leave it as inference.",
            "Keep the inferential sentence out of the summary line and in a clearly marked section.",
        ],
        "signals": ["observed-impact-written", "inference-separated", "confirmation-attempted"],
        "patterns": [
            (
                "observed impact",
                "grep -q '\"owner\":\"victim-tenant\"' response.json && echo 'observed: cross-tenant read of one record'",
            )
        ],
        "pitfalls": [
            "Reporting full account takeover when a single cross-tenant read was observed.",
            "Hiding the inference entirely, which undersells a real bug; separating it is better than dropping it.",
        ],
        "done_when": [
            "Observed impact and inference are written as separate statements.",
            "Any attempt to confirm the inference is recorded with its result.",
        ],
        "refs": [
            "[OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)",
        ],
        "meta": {"phase": "verify"},
    },
    {
        "slug": "evidence-raw-capture",
        "title": "Capture raw requests and responses, not screenshots",
        "summary": "Store the exact bytes of the request and response with their headers, because a screenshot cannot be replayed and cannot be diffed",
        "use_when": "the evidence will be attached to a report or a ticket",
        "avoid_when": "the client's platform only accepts images and you have already stored the raw form",
        "tags": ["evidence", "capture", "raw"],
        "steps": [
            "Capture the full request including method, path, headers and body bytes.",
            "Capture the full response including status line, headers and body bytes.",
            "Store both with a timestamp and the account used.",
            "Redact secrets in a copy, keeping the original intact in a controlled location.",
        ],
        "signals": ["request-bytes-stored", "response-bytes-stored", "redaction-separated"],
        "patterns": [
            (
                "raw capture",
                "curl -sS -D response.headers -o response.body -X POST https://api.example.com/v2/export --data-binary @payload.json\nsha256sum payload.json response.headers response.body",
            )
        ],
        "pitfalls": [
            "A screenshot of a response with the request invisible, so the reader cannot tell how it was produced.",
            "Redacting the original instead of a copy, which destroys the evidence.",
        ],
        "done_when": [
            "Raw request and response bytes are stored with hashes.",
            "Any redacted copy is separate from the original.",
        ],
        "refs": [
            "[curl write-out](https://curl.se/docs/manpage.html)",
        ],
        "meta": {"phase": "evidence"},
    },
    {
        "slug": "evidence-hash-chain",
        "title": "Hash the evidence so tampering is detectable",
        "summary": "Record a sha256 for every artifact when it is created, so a later change is visible instead of silent",
        "use_when": "evidence passes between people or sits for days before triage",
        "avoid_when": "the evidence is a live system state that cannot be hashed meaningfully",
        "tags": ["evidence", "integrity", "hashing"],
        "steps": [
            "Hash each artifact at the moment it is created, not at the end of the engagement.",
            "Store the hash list with a timestamp and the tool version used.",
            "Re-hash before attaching to the report and compare against the stored list.",
            "State any mismatch explicitly rather than regenerating the evidence silently.",
        ],
        "signals": ["hashes-recorded", "list-timestamped", "recheck-performed"],
        "patterns": [
            (
                "hash list",
                "sha256sum payload.json response.body > evidence.sha256\nsha256sum -c evidence.sha256",
            )
        ],
        "pitfalls": [
            "Hashing at submission time, which proves only that the file has not changed since submission.",
            "Re-generating the evidence when a hash mismatches, which hides the cause of the mismatch.",
        ],
        "done_when": [
            "Every artifact has a hash recorded at creation time.",
            "The pre-submission recheck is recorded and any mismatch is explained.",
        ],
        "refs": [
            "[sha256sum](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html)",
        ],
        "meta": {"phase": "evidence"},
    },
    {
        "slug": "evidence-timeline",
        "title": "Put the evidence on a timeline",
        "summary": "Order every request, response and state change by timestamp so the report can show cause before effect instead of implying it",
        "use_when": "the impact claim depends on ordering, such as a change appearing after a specific request",
        "avoid_when": "there is a single request and a single response with no ordering question",
        "tags": ["evidence", "timeline", "ordering"],
        "steps": [
            "Record a monotonic timestamp for each action in the harness and the server's clock offset.",
            "Merge client timestamps with server log timestamps, noting the offset between them.",
            "Mark the triggering request and the first observed effect on the timeline.",
            "Attach the timeline as a table with source and clock for each row.",
        ],
        "signals": ["timestamps-recorded", "offset-noted", "ordering-documented"],
        "patterns": [
            (
                "timeline rows",
                "date -u +%FT%TZ; curl -sS -o /dev/null -w 'trigger %{http_code} at %{time_total}s\\n' -X POST https://api.example.com/v2/export --data-binary @payload.json",
            )
        ],
        "pitfalls": [
            "Mixing client local time and server UTC without noting the offset, which reverses the order.",
            "Claiming a state change was caused by a request when the snapshot was taken before it.",
        ],
        "done_when": [
            "Every row has a timestamp, its source clock and the observed action.",
            "Cause and effect are ordered with the offset accounted for.",
        ],
        "refs": [
            "[RFC 3339 timestamps](https://www.rfc-editor.org/rfc/rfc3339)",
        ],
        "meta": {"phase": "evidence"},
    },
]