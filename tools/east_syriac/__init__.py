"""Deterministic tooling for the East Syriac Translation project."""

from .inspection import (
    LetterState,
    PageStateIssue,
    PageStateNotice,
    PageStateReport,
    WordState,
    format_page_state_report,
    inspect_normalized_text,
)
from .normalization import (
    NormalizationChange,
    NormalizationFlag,
    NormalizationResult,
    normalize_text,
)

__all__ = [
    "LetterState",
    "NormalizationChange",
    "NormalizationFlag",
    "NormalizationResult",
    "PageStateIssue",
    "PageStateNotice",
    "PageStateReport",
    "WordState",
    "format_page_state_report",
    "inspect_normalized_text",
    "normalize_text",
]
