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
from .transliteration import (
    OccultansResolutionKey,
    OccultansResolutions,
    ReverseTransliterationResult,
    TransliterationError,
    TransliterationResult,
    round_trip,
    transliterate_text,
)
from .transliteration_inverse import reverse_transliterate

__all__ = [
    "LetterState",
    "NormalizationChange",
    "NormalizationFlag",
    "NormalizationResult",
    "OccultansResolutionKey",
    "OccultansResolutions",
    "PageStateIssue",
    "PageStateNotice",
    "PageStateReport",
    "ReverseTransliterationResult",
    "TransliterationError",
    "TransliterationResult",
    "WordState",
    "format_page_state_report",
    "inspect_normalized_text",
    "normalize_text",
    "reverse_transliterate",
    "round_trip",
    "transliterate_text",
]
