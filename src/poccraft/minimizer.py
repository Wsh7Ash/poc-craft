"""Delta-debugging minimisation of a proof-of-concept input.

The algorithm is Zeller's ddmin, restricted to contiguous removal. The only
contract is a predicate: it must exit 0 when the input still reproduces the
finding. Everything else — whether the input is a request body, a payload or
a file — is opaque to the minimiser.

Reference: Zeller & Hildebrandt, "Simplifying and Isolating Failure-Inducing
Input", IEEE TSE 28(2), 2002. https://doi.org/10.1109/32.988710
"""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

Predicate = Callable[[bytes], bool]


class MinimiseError(RuntimeError):
    """Raised when the minimiser cannot make a safe decision about the input."""


@dataclass
class MinimiseResult:
    """Outcome of a minimisation run."""

    original: bytes
    minimal: bytes
    calls: int
    rounds: int
    history: list[tuple[int, int, bool]] = field(default_factory=list)

    @property
    def original_size(self) -> int:
        return len(self.original)

    @property
    def minimal_size(self) -> int:
        return len(self.minimal)

    @property
    def ratio(self) -> float:
        """Fraction of the original input that survived. 1.0 means nothing shrank."""
        if not self.original:
            return 1.0
        return self.minimal_size / self.original_size


def split_units(data: bytes, unit: str) -> list[bytes]:
    """Split input into the units ddmin will try to remove.

    ``byte`` splits into single bytes; ``line`` keeps the line terminator on
    each unit so joining the survivors reconstructs the original exactly.
    """
    if unit == "byte":
        return [data[i : i + 1] for i in range(len(data))]
    if unit == "line":
        units: list[bytes] = []
        start = 0
        while start < len(data):
            end = data.find(b"\n", start)
            if end == -1:
                units.append(data[start:])
                break
            units.append(data[start : end + 1])
            start = end + 1
        return units
    raise MinimiseError(f"unknown unit: {unit!r} (expected 'byte' or 'line')")


def ddmin(units: Sequence[bytes], predicate: Predicate) -> tuple[list[bytes], int, int]:
    """Return (surviving units, predicate calls, rounds).

    Sequence form of ddmin: repeatedly try to halve the input while the
    predicate still holds, then try removing single units.
    """
    current = list(units)
    calls = 0
    rounds = 0

    def holds(candidate: list[bytes]) -> bool:
        nonlocal calls
        calls += 1
        return predicate(b"".join(candidate))

    if not holds(current):
        raise MinimiseError("the predicate does not hold on the unmodified input")

    granularity = 2
    while len(current) >= 2:
        rounds += 1
        chunk = max(1, len(current) // granularity)
        reduced = False
        start = 0
        while start < len(current):
            candidate = current[:start] + current[start + chunk :]
            if candidate and holds(candidate):
                current = candidate
                reduced = True
                granularity = max(2, granularity - 1)
            else:
                start += chunk
        if not reduced:
            if granularity >= len(current):
                break
            granularity = min(len(current), granularity * 2)

    # Final pass: every remaining unit must be necessary.
    index = 0
    while index < len(current):
        candidate = current[:index] + current[index + 1 :]
        if candidate and holds(candidate):
            current = candidate
        else:
            index += 1

    return current, calls, rounds


def minimise(
    data: bytes,
    predicate: Predicate,
    unit: str = "line",
) -> MinimiseResult:
    """Minimise ``data`` while ``predicate`` keeps holding."""
    units = split_units(data, unit)
    if not units:
        return MinimiseResult(original=data, minimal=data, calls=0, rounds=0)
    survivors, calls, rounds = ddmin(units, predicate)
    return MinimiseResult(
        original=data,
        minimal=b"".join(survivors),
        calls=calls,
        rounds=rounds,
    )


def command_predicate(
    command: Sequence[str],
    timeout: float = 30.0,
    cwd: str | Path | None = None,
) -> Predicate:
    """Build a predicate that writes the candidate to a temp file and runs ``command``.

    ``{input}`` in any argument is replaced with the temp file path; otherwise
    the path is appended as the last argument. Exit code 0 means "still
    reproduces".
    """
    template = list(command)
    if not template:
        raise MinimiseError("empty predicate command")

    def predicate(candidate: bytes) -> bool:
        with tempfile.NamedTemporaryFile(prefix="poccraft-", delete=False) as handle:
            handle.write(candidate)
            path = handle.name
        try:
            argv = [arg.replace("{input}", path) for arg in template]
            if not any("{input}" in arg for arg in template):
                argv.append(path)
            completed = subprocess.run(
                argv,
                capture_output=True,
                timeout=timeout,
                cwd=cwd,
            )
            return completed.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        finally:
            Path(path).unlink(missing_ok=True)

    return predicate


__all__ = [
    "MinimiseError",
    "MinimiseResult",
    "Predicate",
    "split_units",
    "ddmin",
    "minimise",
    "command_predicate",
]