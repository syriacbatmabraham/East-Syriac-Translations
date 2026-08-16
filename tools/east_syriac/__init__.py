"""Deterministic tooling for the East Syriac Translation project."""

from .confirmed_text import (
    ConfirmedTextCheckResult,
    ConfirmedTextDocument,
    ConfirmedTextFormatError,
    ConfirmedTextIssue,
    check_confirmed_text,
    check_confirmed_text_bytes,
    check_confirmed_text_path,
    parse_confirmed_text,
)
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
from .provenance import (
    ConfirmedTextProvenance,
    ProvenanceIssue,
    SourceRegistry,
    SourceRegistryFormatError,
    check_source_registry,
    check_source_registry_path,
    parse_source_registry,
)
from .transliteration import (
    ReverseTransliterationResult,
    TransliterationError,
    TransliterationResult,
    round_trip,
    transliterate_text,
)
from .transliteration_inverse import reverse_transliterate

__all__ = [
    "ConfirmedTextCheckResult",
    "ConfirmedTextDocument",
    "ConfirmedTextFormatError",
    "ConfirmedTextIssue",
    "ConfirmedTextProvenance",
    "LetterState",
    "NormalizationChange",
    "NormalizationFlag",
    "NormalizationResult",
    "PageStateIssue",
    "PageStateNotice",
    "PageStateReport",
    "ProvenanceIssue",
    "ReverseTransliterationResult",
    "SourceRegistry",
    "SourceRegistryFormatError",
    "TransliterationError",
    "TransliterationResult",
    "WordState",
    "check_confirmed_text",
    "check_confirmed_text_bytes",
    "check_confirmed_text_path",
    "check_source_registry",
    "check_source_registry_path",
    "format_page_state_report",
    "inspect_normalized_text",
    "normalize_text",
    "parse_confirmed_text",
    "parse_source_registry",
    "reverse_transliterate",
    "round_trip",
    "transliterate_text",
]
