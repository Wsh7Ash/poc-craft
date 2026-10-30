"""poc-craft: craft minimal, reproducible proof-of-concept artifacts."""

from __future__ import annotations

from .cli import main
from .minimizer import MinimiseError, MinimiseResult, command_predicate, ddmin, minimise
from .model import Skill, skill_from_dict
from .render import (
    build_pack,
    render_catalog,
    render_description,
    render_skill,
    sha256_of,
    word_count,
)
from .scaffold import Spec, generate
from .validate import (
    MIN_PATTERNS,
    MIN_PITFALLS,
    MIN_SIGNALS,
    MIN_STEPS,
    MIN_WORDS,
    PHASES,
    validate_pack,
    validate_skill,
)

__all__ = [
    "main",
    "MinimiseError",
    "MinimiseResult",
    "command_predicate",
    "ddmin",
    "minimise",
    "Skill",
    "skill_from_dict",
    "build_pack",
    "render_catalog",
    "render_description",
    "render_skill",
    "sha256_of",
    "word_count",
    "Spec",
    "generate",
    "validate_pack",
    "validate_skill",
    "PHASES",
    "MIN_STEPS",
    "MIN_SIGNALS",
    "MIN_PATTERNS",
    "MIN_PITFALLS",
    "MIN_WORDS",
]
