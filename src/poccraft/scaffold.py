"""Generate a runnable PoC harness from a small, explicit specification.

The scaffold is deliberately boring: one request, one oracle, one exit code,
and a repeat count so a flaky result is visible rather than averaged away.
Anything the operator changes by hand should be visible in a diff against the
generated file, which is why generation is deterministic and takes no hints
from the environment.
"""

from __future__ import annotations

from dataclasses import dataclass

LANGUAGES = ("python", "bash")
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")


@dataclass(frozen=True)
class Spec:
    """What the harness should send and what counts as reproduction."""

    url: str
    method: str
    payload_path: str
    oracle: str
    repeat: int = 1
    header: tuple[str, ...] = ()

    def validated(self) -> "Spec":
        if self.method.upper() not in METHODS:
            raise ValueError(f"unsupported method: {self.method}")
        if not self.url.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        if not self.oracle.strip():
            raise ValueError("oracle must not be empty")
        if self.repeat < 1:
            raise ValueError("repeat must be >= 1")
        return self


def _python(spec: Spec) -> str:
    headers = "".join(f"    {h!r},\n" for h in spec.header)
    return f'''#!/usr/bin/env python3
"""Generated PoC harness. Edit the oracle, not the request plumbing."""

from __future__ import annotations

import sys
import pathlib
import urllib.error
import urllib.request

URL = {spec.url!r}
METHOD = {spec.method.upper()!r}
PAYLOAD = pathlib.Path({spec.payload_path!r})
ORACLE = {spec.oracle!r}
REPEAT = {spec.repeat}
HEADERS = [
{headers}]


def send(body: bytes) -> tuple[int, bytes]:
    request = urllib.request.Request(URL, data=body, method=METHOD)
    for header in HEADERS:
        name, _, value = header.partition(":")
        request.add_header(name.strip(), value.strip())
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def reproduces(status: int, body: bytes) -> bool:
    scope = {{"status": status, "length": len(body), "body": body}}
    return bool(eval(ORACLE, {{"__builtins__": {{}}}}, scope))


def main() -> int:
    body = PAYLOAD.read_bytes() if PAYLOAD.exists() else b""
    hits = 0
    for attempt in range(1, REPEAT + 1):
        status, response = send(body)
        hit = reproduces(status, response)
        hits += hit
        print(f"attempt {{attempt}}/{{REPEAT}} status={{status}} len={{len(response)}} hit={{hit}}")
    print(f"reproduced {{hits}}/{{REPEAT}}")
    return 0 if hits == REPEAT else 1


if __name__ == "__main__":
    sys.exit(main())
'''


def _bash(spec: Spec) -> str:
    header_args = "".join(f"  -H {h!r} \\\n" for h in spec.header)
    padded = spec.oracle.replace('"', '\\"')
    return f'''#!/usr/bin/env bash
# Generated PoC harness. Edit the oracle, not the request plumbing.
set -uo pipefail

URL={spec.url!r}
METHOD={spec.method.upper()!r}
PAYLOAD={spec.payload_path!r}
ORACLE={padded!r}
REPEAT={spec.repeat}

hits=0
for attempt in $(seq 1 "$REPEAT"); do
  body=$(curl -sS -o /tmp/poc-body -w '%{{http_code}}' -X "$METHOD" \\
{header_args}  --data-binary "@$PAYLOAD" "$URL")
  length=$(wc -c < /tmp/poc-body | tr -d ' ')
  if eval "[[ $ORACLE ]]"; then
    hits=$((hits + 1))
    hit=1
  else
    hit=0
  fi
  echo "attempt $attempt/$REPEAT status=$body len=$length hit=$hit"
done

echo "reproduced $hits/$REPEAT"
[[ "$hits" -eq "$REPEAT" ]]
'''


def generate(spec: Spec, lang: str = "python") -> str:
    """Return the harness source for ``lang``. Deterministic for a given spec."""
    spec = spec.validated()
    if lang == "python":
        return _python(spec)
    if lang == "bash":
        return _bash(spec)
    raise ValueError(f"unsupported language: {lang!r} (expected one of {LANGUAGES})")


__all__ = ["LANGUAGES", "METHODS", "Spec", "generate"]