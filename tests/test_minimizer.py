"""Behavioural tests for the ddmin minimiser and the harness generator."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from poccraft.minimizer import (
    MinimiseError,
    command_predicate,
    ddmin,
    minimise,
    split_units,
)
from poccraft.scaffold import Spec, generate

ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------ unit splitting


def test_split_bytes_preserves_input() -> None:
    data = b"\x00\x01\x02abc"
    units = split_units(data, "byte")
    assert len(units) == len(data)
    assert b"".join(units) == data


def test_split_lines_preserves_input() -> None:
    data = b"header\nMAGIC\ntrailer"
    units = split_units(data, "line")
    assert b"".join(units) == data
    assert len(units) == 3


def test_split_rejects_unknown_unit() -> None:
    with pytest.raises(MinimiseError):
        split_units(b"abc", "nibble")


# --------------------------------------------------------------------------- ddmin


def test_ddmin_keeps_only_the_required_marker() -> None:
    payload = b"".join(
        [b"padding-line-1\n", b"MAGIC\n", b"padding-line-2\n", b"padding-line-3\n"]
    )
    result = minimise(payload, lambda data: b"MAGIC" in data, unit="line")
    assert b"MAGIC" in result.minimal
    assert len(result.minimal) < len(payload)
    assert result.minimal_size <= len(b"MAGIC\n") + 1


def test_ddmin_keeps_two_markers_when_both_are_required() -> None:
    payload = b"AAA\nfiller1\nBBB\nfiller2\nfiller3\n"
    result = minimise(
        payload,
        lambda data: b"AAA" in data and b"BBB" in data,
        unit="line",
    )
    assert b"AAA" in result.minimal and b"BBB" in result.minimal
    assert len(result.minimal) < len(payload)


def test_ddmin_reports_predicate_calls_and_rounds() -> None:
    payload = b"".join([b"x" * 8 + b"\n" for _ in range(16)])
    result = minimise(payload, lambda data: b"xxxx" in data, unit="line")
    assert result.calls > 0
    assert result.rounds > 0
    assert result.original_size == len(payload)


def test_ddmin_refuses_when_predicate_is_false_on_input() -> None:
    with pytest.raises(MinimiseError):
        minimise(b"nothing here\n", lambda data: b"MAGIC" in data, unit="line")


def test_ddmin_on_empty_input_is_a_no_op() -> None:
    result = minimise(b"", lambda data: True)
    assert result.minimal == b""
    assert result.calls == 0


def test_ddmin_sequence_interface() -> None:
    units = [b"a\n", b"MAGIC\n", b"b\n"]
    survivors, calls, rounds = ddmin(units, lambda data: b"MAGIC" in data)
    assert b"".join(survivors) == b"MAGIC\n"
    assert calls >= 1 and rounds >= 0


def test_minimise_is_deterministic() -> None:
    payload = b"one\ntwo\nMAGIC\nthree\nfour\n"
    first = minimise(payload, lambda d: b"MAGIC" in d, unit="line")
    second = minimise(payload, lambda d: b"MAGIC" in d, unit="line")
    assert first.minimal == second.minimal
    assert first.calls == second.calls


def test_ratio_is_a_fraction_of_the_original() -> None:
    payload = b"MAGIC\n" + b"filler\n" * 10
    result = minimise(payload, lambda d: b"MAGIC" in d, unit="line")
    assert 0.0 < result.ratio < 1.0


# ------------------------------------------------------------- command predicate


def test_command_predicate_uses_placeholder(tmp_path: Path) -> None:
    checker = tmp_path / "check.py"
    checker.write_text(
        "import sys, pathlib\n"
        "data = pathlib.Path(sys.argv[1]).read_bytes()\n"
        "raise SystemExit(0 if b'MAGIC' in data else 1)\n",
        encoding="utf-8",
    )
    predicate = command_predicate([sys.executable, str(checker), "{input}"])
    assert predicate(b"...MAGIC...") is True
    assert predicate(b"nothing") is False


def test_command_predicate_appends_path_when_no_placeholder(tmp_path: Path) -> None:
    checker = tmp_path / "check.py"
    checker.write_text(
        "import sys, pathlib\n"
        "raise SystemExit(0 if b'MAGIC' in pathlib.Path(sys.argv[1]).read_bytes() else 1)\n",
        encoding="utf-8",
    )
    predicate = command_predicate([sys.executable, str(checker)])
    assert predicate(b"MAGIC") is True


def test_command_predicate_treats_timeout_as_no_match() -> None:
    predicate = command_predicate(
        [sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.2
    )
    assert predicate(b"anything") is False


# ------------------------------------------------------------------------- scaffold


def test_python_scaffold_compiles() -> None:
    source = generate(
        Spec(
            url="https://api.example.com/v2/export",
            method="POST",
            payload_path="payload.json",
            oracle="status == 500",
            repeat=3,
            header=("Content-Type: application/json",),
        )
    )
    compile(source, "<generated>", "exec")
    assert "https://api.example.com/v2/export" in source
    assert "REPEAT = 3" in source
    assert "Content-Type: application/json" in source


def test_bash_scaffold_has_header_and_oracle() -> None:
    source = generate(
        Spec(
            url="https://api.example.com/v2/export",
            method="PUT",
            payload_path="p.bin",
            oracle="status == 200",
            header=("X-Test: 1",),
        ),
        lang="bash",
    )
    assert "METHOD='PUT'" in source
    assert "X-Test: 1" in source
    assert "REPEAT=1" in source


def test_scaffold_is_deterministic() -> None:
    spec = Spec(url="https://x.example/a", method="GET", payload_path="p", oracle="status == 200")
    assert generate(spec) == generate(spec)


def test_scaffold_rejects_bad_method() -> None:
    with pytest.raises(ValueError):
        generate(Spec(url="https://x.example/a", method="TRACE", payload_path="p", oracle="x"))


def test_scaffold_rejects_non_http_url() -> None:
    with pytest.raises(ValueError):
        generate(Spec(url="file:///etc/passwd", method="GET", payload_path="p", oracle="x"))


def test_scaffold_rejects_empty_oracle() -> None:
    with pytest.raises(ValueError):
        generate(Spec(url="https://x.example/a", method="GET", payload_path="p", oracle="   "))


def test_scaffold_rejects_unknown_language() -> None:
    spec = Spec(url="https://x.example/a", method="GET", payload_path="p", oracle="status == 200")
    with pytest.raises(ValueError):
        generate(spec, lang="ruby")


# ------------------------------------------------------------------- CLI: minimise


def _write_checker(directory: Path) -> Path:
    checker = directory / "check.py"
    checker.write_text(
        "import sys, pathlib\n"
        "raise SystemExit(0 if b'MAGIC' in pathlib.Path(sys.argv[1]).read_bytes() else 1)\n",
        encoding="utf-8",
    )
    return checker


def test_cli_minimize_end_to_end(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"noise-1\nnoise-2\nMAGIC\nnoise-3\nnoise-4\n")
    checker = _write_checker(tmp_path)
    out = tmp_path / "minimal.txt"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "poccraft",
            "minimize",
            "--input",
            str(payload),
            "--predicate",
            f"{sys.executable} {checker} {{input}}",
            "--unit",
            "line",
            "--out",
            str(out),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8"},
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert b"MAGIC" in out.read_bytes()
    assert len(out.read_bytes()) < payload.stat().st_size
    assert "bytes" in result.stdout


def test_cli_minimize_fails_when_predicate_never_holds(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"nothing useful\n")
    checker = _write_checker(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "poccraft",
            "minimize",
            "--input",
            str(payload),
            "--predicate",
            f"{sys.executable} {checker} {{input}}",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8"},
        timeout=120,
    )
    assert result.returncode == 1
    assert "does not hold" in result.stderr


def test_cli_minimize_requires_arguments() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "poccraft", "minimize"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )
    assert result.returncode == 2


# ------------------------------------------------------------------ CLI: scaffold


def test_cli_scaffold_writes_compilable_python(tmp_path: Path) -> None:
    out = tmp_path / "poc.py"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "poccraft",
            "scaffold",
            "--url",
            "https://api.example.com/v2/export",
            "--method",
            "POST",
            "--payload",
            "payload.json",
            "--oracle",
            "status == 500",
            "--repeat",
            "2",
            "--out",
            str(out),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    source = out.read_text(encoding="utf-8")
    compile(source, str(out), "exec")
    assert "REPEAT = 2" in source


def test_cli_scaffold_rejects_bad_url() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "poccraft", "scaffold", "--url", "ftp://x.example"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )
    assert result.returncode == 2
    assert "error:" in result.stderr