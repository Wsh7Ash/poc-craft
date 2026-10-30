"""poc-craft corpus: pack metadata plus 50 authored PoC-crafting skills."""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "poc-craft",
    "version": "1.0.0",
    "category": "bug-bounty-poc",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated skills for crafting a proof of concept that survives triage: "
        "scope checks, honest reproduction, isolation, delta-debugged minimisation, "
        "harness generation, controls, evidence bundling and post-fix verification."
    ),
    "expected_skills": 50,
}

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]
BY_SLUG: dict[str, Any] = {skill.slug: skill for skill in SKILLS}

__all__ = ["PACK", "SKILLS", "BY_SLUG"]