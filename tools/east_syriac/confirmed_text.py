"""Parser and validator for fixed three-block confirmed-text files.

A confirmed text is authoritative Syriac, mechanically derived canonical
transliteration, and settled English in three aligned blocks.  This module
checks the structural and file-hygiene requirements from General Rules §9.1,
§9.1.1, and §11.15–16, then re-derives transliteration from the Syriac layer.

The stored transliteration is never treated as authority for ordinary
orthography.  Its only reusable information is the page-only occultans
span/separate decision, and even that is trusted only when the stored canonical
line reverses exactly to the Syriac line.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePath
import unicodedata

from .inspection import inspect_normalized_text
from .normalization import OCCULTANS_ABOVE, OCCULTANS_BELOW
from .transliteration import (
    OccultansResolutionKey,
    OccultansResolutions,
    TransliterationError,
    transliterate_text,
)
from .transliteration_inverse import reverse_transliterate


BLOCK_NAMES = ("syriac", "transliteration", "english")
CURLY_APOSTROPHES = frozenset({"\u2018", "\u2019", "\u201b"})
ALLOWED_SUFFIXES = frozenset({".txt", ".md"})


class ConfirmedTextFormatError(ValueError):
    """A structural condition that prevents a reliable three-block parse."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class ConfirmedTextIssue:
    code: str
    message: str
    line: int | None = None
    block: str | None = None


@dataclass(frozen=True)
class ConfirmedTextDocument:
    syriac_lines: tuple[str, ...]
    transliteration_lines: tuple[str, ...]
    english_lines: tuple[str, ...]

    @property
    def line_count(self) -> int:
        return len(self.syriac_lines)

    @property
    def stanza_breaks(self) -> tuple[int, ...]:
        return tuple(i + 1 for i, line in enumerate(self.syriac_lines) if line == "")


@dataclass(frozen=True)
class ConfirmedTextCheckResult:
    document: ConfirmedTextDocument | None
    issues: tuple[ConfirmedTextIssue, ...]
    expected_transliteration_lines: tuple[str | None, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues

    @property
    def expected_transliteration_block(self) -> str | None:
        if not self.expected_transliteration_lines:
            return None
        if any(line is None for line in self.expected_transliteration_lines):
            return None
        return "\n".join(line or "" for line in self.expected_transliteration_lines)


def _blank_runs(lines: list[str]) -> list[tuple[int, int]]:
    """Return half-open runs of completely blank logical lines."""

    runs: list[tuple[int, int]] = []
    i = 0
    while i < len(lines):
        if lines[i] != "":
            i += 1
            continue
        start = i
        while i < len(lines) and lines[i] == "":
            i += 1
        runs.append((start, i))
    return runs


def _blank_positions(block: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(i for i, line in enumerate(block) if line == "")


def _segments_for_runs(
    lines: list[str],
    first: tuple[int, int],
    second: tuple[int, int],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    return (
        tuple(lines[: first[0]]),
        tuple(lines[first[1] : second[0]]),
        tuple(lines[second[1] :]),
    )


def _valid_partition(
    blocks: tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]
) -> bool:
    if any(not block for block in blocks):
        return False
    lengths = {len(block) for block in blocks}
    if len(lengths) != 1:
        return False
    blank_patterns = {_blank_positions(block) for block in blocks}
    return len(blank_patterns) == 1


def parse_confirmed_text(text: str) -> ConfirmedTextDocument:
    """Parse a confirmed-text string without assuming blank lines are only separators.

    A stanza break is itself a blank logical line and may appear inside every
    block.  Block boundaries are therefore inferred by searching for the unique
    pair of blank-line runs that yields three equal-length blocks with identical
    stanza-break positions.
    """

    if not text:
        raise ConfirmedTextFormatError("empty-file", "Confirmed text is empty.")

    # One terminal LF is ordinary file termination rather than a logical line.
    # Additional terminal blank lines remain visible and make the structure fail.
    body = text[:-1] if text.endswith("\n") else text
    if not body:
        raise ConfirmedTextFormatError("empty-file", "Confirmed text has no content lines.")

    lines = body.split("\n")
    runs = _blank_runs(lines)
    if len(runs) < 2:
        raise ConfirmedTextFormatError(
            "three-block-structure",
            "Expected three blocks separated by two blank-line runs.",
        )

    candidates: list[tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = []
    for i, first in enumerate(runs[:-1]):
        if first[0] == 0:
            continue
        for second in runs[i + 1 :]:
            if second[1] == len(lines):
                continue
            blocks = _segments_for_runs(lines, first, second)
            if _valid_partition(blocks):
                candidates.append(blocks)

    # De-duplicate partitions that can arise only from identical run boundaries.
    unique: list[tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = []
    for candidate in candidates:
        if candidate not in unique:
            unique.append(candidate)

    if len(unique) == 1:
        syriac, transliteration, english = unique[0]
        return ConfirmedTextDocument(syriac, transliteration, english)

    if len(unique) > 1:
        raise ConfirmedTextFormatError(
            "ambiguous-block-boundaries",
            "More than one three-block partition satisfies equal-line and stanza alignment; block boundaries are ambiguous.",
        )

    # Give more specific diagnostics for the common no-stanza case.
    if len(runs) == 2:
        blocks = _segments_for_runs(lines, runs[0], runs[1])
        lengths = tuple(len(block) for block in blocks)
        if any(length == 0 for length in lengths):
            raise ConfirmedTextFormatError(
                "three-block-structure",
                "One of the three required blocks is empty.",
            )
        if len(set(lengths)) != 1:
            raise ConfirmedTextFormatError(
                "unequal-block-length",
                f"Three blocks have unequal line counts: {lengths[0]}, {lengths[1]}, {lengths[2]}.",
            )
        if len({_blank_positions(block) for block in blocks}) != 1:
            raise ConfirmedTextFormatError(
                "stanza-break-mismatch",
                "Stanza-break positions do not match across the three blocks.",
            )

    # If any pair gives equal lengths but stanza positions disagree, name that
    # failure rather than reducing it to a generic parse error.
    for i, first in enumerate(runs[:-1]):
        for second in runs[i + 1 :]:
            blocks = _segments_for_runs(lines, first, second)
            if any(not block for block in blocks):
                continue
            if len({len(block) for block in blocks}) == 1:
                raise ConfirmedTextFormatError(
                    "stanza-break-mismatch",
                    "Equal-length block candidates exist, but their stanza-break positions do not match.",
                )

    raise ConfirmedTextFormatError(
        "three-block-structure",
        "Could not identify three equal aligned blocks from the file structure.",
    )


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _hygiene_issues(text: str, filename: str | None) -> list[ConfirmedTextIssue]:
    issues: list[ConfirmedTextIssue] = []

    if filename is not None:
        suffix = PurePath(filename).suffix.lower()
        if suffix not in ALLOWED_SUFFIXES:
            issues.append(
                ConfirmedTextIssue(
                    "unsupported-extension",
                    f"Confirmed texts must be .txt or .md, not {suffix or '(no extension)' }.",
                )
            )

    if text.startswith("\ufeff"):
        issues.append(
            ConfirmedTextIssue(
                "byte-order-mark",
                "Confirmed UTF-8 text must not contain a BOM.",
                line=1,
            )
        )

    if "\r" in text:
        first = text.index("\r")
        issues.append(
            ConfirmedTextIssue(
                "non-lf-line-ending",
                "Confirmed text must use LF line endings only.",
                line=_line_number(text, first),
            )
        )

    if unicodedata.normalize("NFC", text) != text:
        issues.append(
            ConfirmedTextIssue(
                "non-nfc",
                "Confirmed text is not NFC normalized.",
            )
        )

    for line_no, line in enumerate(text.replace("\r\n", "\n").replace("\r", "\n").split("\n"), start=1):
        if line != line.rstrip():
            issues.append(
                ConfirmedTextIssue(
                    "trailing-whitespace",
                    "Line has trailing whitespace.",
                    line=line_no,
                )
            )

    for index, char in enumerate(text):
        if char in CURLY_APOSTROPHES:
            issues.append(
                ConfirmedTextIssue(
                    "curly-apostrophe",
                    "Confirmed text uses a curly apostrophe; use ASCII straight apostrophe U+0027.",
                    line=_line_number(text, index),
                )
            )

    return issues


def _preview(text: str, limit: int = 90) -> str:
    if len(text) <= limit:
        return repr(text)
    return repr(text[: limit - 1] + "…")


def _occultans_keys_for_source(line: str) -> set[OccultansResolutionKey]:
    keys: set[OccultansResolutionKey] = set()
    audit = inspect_normalized_text(line)
    for notice in audit.notices:
        if notice.code != "adjacent-occultans-page-check":
            continue
        if notice.char == OCCULTANS_ABOVE:
            direction = "above"
        elif notice.char == OCCULTANS_BELOW:
            direction = "below"
        else:
            continue
        keys.add((notice.word, notice.letter, direction))
    return keys


def _check_aligned_document(
    document: ConfirmedTextDocument,
) -> tuple[list[ConfirmedTextIssue], tuple[str | None, ...]]:
    issues: list[ConfirmedTextIssue] = []
    expected_lines: list[str | None] = []

    for index, (syriac, canonical, english) in enumerate(
        zip(
            document.syriac_lines,
            document.transliteration_lines,
            document.english_lines,
            strict=True,
        ),
        start=1,
    ):
        if syriac == canonical == english == "":
            expected_lines.append("")
            continue

        reverse = None
        reverse_exact = False
        try:
            reverse = reverse_transliterate(canonical)
        except TransliterationError as exc:
            issues.append(
                ConfirmedTextIssue(
                    "invalid-canonical-transliteration",
                    f"Canonical transliteration is invalid ({exc.code}): {exc.message}",
                    line=index,
                    block="transliteration",
                )
            )
        else:
            reverse_exact = reverse.text == syriac
            if not reverse_exact:
                issues.append(
                    ConfirmedTextIssue(
                        "reverse-round-trip-mismatch",
                        "Stored canonical transliteration does not reconstruct the Syriac line exactly: "
                        f"reconstructed {_preview(reverse.text)}; Syriac is {_preview(syriac)}.",
                        line=index,
                        block="transliteration",
                    )
                )

        source_occultans = _occultans_keys_for_source(syriac)
        resolutions: OccultansResolutions | None = None
        if source_occultans:
            # Encoded Syriac cannot tell span from separate adjacent lines.  The
            # confirmed Latin may carry that page fact only when it otherwise
            # proves itself by reversing exactly to this Syriac line.
            if reverse is not None and reverse_exact:
                resolutions = reverse.occultans_resolutions
            else:
                issues.append(
                    ConfirmedTextIssue(
                        "occultans-page-resolution-required",
                        "Syriac contains adjacent occultans whose span/separate state is page-only, but the stored Latin cannot be trusted to supply it because the line does not reverse exactly.",
                        line=index,
                        block="syriac",
                    )
                )
                expected_lines.append(None)
                continue

        try:
            forward = transliterate_text(syriac, resolutions)
        except TransliterationError as exc:
            issues.append(
                ConfirmedTextIssue(
                    "syriac-transliteration-error",
                    f"Syriac line cannot be mechanically transliterated ({exc.code}): {exc.message}",
                    line=index,
                    block="syriac",
                )
            )
            expected_lines.append(None)
            continue

        expected = forward.text
        expected_lines.append(expected)
        if expected != canonical:
            issues.append(
                ConfirmedTextIssue(
                    "stale-transliteration",
                    "Stored transliteration differs from the transliteration mechanically derived from Syriac: "
                    f"stored {_preview(canonical)}; expected {_preview(expected)}.",
                    line=index,
                    block="transliteration",
                )
            )

    return issues, tuple(expected_lines)


def check_confirmed_text(text: str, filename: str | None = None) -> ConfirmedTextCheckResult:
    """Check an already-decoded confirmed text.

    CRLF/CR and a leading BOM are diagnosed, then normalized only in the private
    analysis copy so structural/transliteration diagnostics can still be given.
    The returned document therefore represents the logical content, never a
    silently rewritten file.
    """

    issues = _hygiene_issues(text, filename)

    analysis = text
    if analysis.startswith("\ufeff"):
        analysis = analysis[1:]
    analysis = analysis.replace("\r\n", "\n").replace("\r", "\n")

    try:
        document = parse_confirmed_text(analysis)
    except ConfirmedTextFormatError as exc:
        issues.append(ConfirmedTextIssue(exc.code, exc.message))
        return ConfirmedTextCheckResult(None, tuple(issues), ())

    content_issues, expected = _check_aligned_document(document)
    issues.extend(content_issues)
    return ConfirmedTextCheckResult(document, tuple(issues), expected)


def check_confirmed_text_bytes(data: bytes, filename: str | None = None) -> ConfirmedTextCheckResult:
    """Decode strict UTF-8 and run the complete confirmed-text checker."""

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        issue = ConfirmedTextIssue(
            "invalid-utf8",
            f"File is not valid UTF-8: byte offset {exc.start}.",
        )
        return ConfirmedTextCheckResult(None, (issue,), ())
    return check_confirmed_text(text, filename)


def check_confirmed_text_path(path: str | Path) -> ConfirmedTextCheckResult:
    path = Path(path)
    return check_confirmed_text_bytes(path.read_bytes(), path.name)
