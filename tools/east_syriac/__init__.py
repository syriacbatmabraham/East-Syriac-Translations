"""Deterministic tooling for the East Syriac Translation project."""

from .normalization import (
    NormalizationChange,
    NormalizationFlag,
    NormalizationResult,
    normalize_text,
)

__all__ = [
    "NormalizationChange",
    "NormalizationFlag",
    "NormalizationResult",
    "normalize_text",
]
