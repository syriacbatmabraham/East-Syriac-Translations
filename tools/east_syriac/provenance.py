"""Deterministic provenance checks for confirmed-text source metadata.

The project deliberately keeps source-of-record designations outside the three-block
confirmed text files. This module parses the small, controlled YAML subset used by
`sources/sources.yaml` without introducing a runtime YAML dependency, then verifies
that the authoritative corpus and the registry agree exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class SourceAlternative:
    line: int
    bracket: int
    label: str
    reading: str


@dataclass(frozen=True)
class ConfirmedTextProvenance:
    filename: str
    citation_label: str | None
    source_of_record: str | None
    source_alternatives: tuple[SourceAlternative, ...] = ()


@dataclass(frozen=True)
class SourceRegistry:
    source_records: frozenset[str]
    confirmed_texts: tuple[ConfirmedTextProvenance, ...]


@dataclass(frozen=True)
class ProvenanceIssue:
    code: str
    message: str
    filename: str | None = None
    line: int | None = None


class SourceRegistryFormatError(ValueError):
    def __init__(self, code: str, message: str, line: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.line = line


def _scalar(value: str) -> str:
    """Decode the simple scalar forms used by the controlled registry subset."""

    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        # Preserve Unicode literally. Only the two escapes needed by the
        # registry's human-readable strings are interpreted here; this is not a
        # general YAML parser.
        return value[1:-1].replace(r"\"", '"').replace(r"\\", "\\")
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_source_registry(text: str) -> SourceRegistry:
    """Parse the controlled top-level subset of `sources.yaml` used by checks.

    Only the top-level `source_records` and `confirmed_texts` mappings and the
    scalar fields immediately below each confirmed-text entry are needed here.
    Source alternatives are parsed separately. Legacy witness apparatus does
    not require an additional source record.
    """

    section: str | None = None
    current_key: str | None = None
    source_records: set[str] = set()
    confirmed: dict[str, dict[str, str]] = {}
    saw_source_records = False
    saw_confirmed_texts = False

    for line_no, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indentation = raw[: len(raw) - len(raw.lstrip(" \t"))]
        if "\t" in indentation:
            raise SourceRegistryFormatError(
                "tab-indentation",
                "sources.yaml must use spaces, not tabs, for indentation.",
                line_no,
            )

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if indent == 0:
            if not stripped.endswith(":"):
                raise SourceRegistryFormatError(
                    "top-level-syntax",
                    "Expected a top-level mapping name ending in ':'.",
                    line_no,
                )
            name = stripped[:-1]
            if name == "source_records":
                saw_source_records = True
                section = name
            elif name == "confirmed_texts":
                saw_confirmed_texts = True
                section = name
            else:
                section = None
            current_key = None
            continue

        if indent == 2 and stripped.endswith(":") and section is not None:
            key = stripped[:-1]
            if not key:
                raise SourceRegistryFormatError(
                    "empty-registry-key",
                    "Registry entry name may not be empty.",
                    line_no,
                )
            current_key = key
            if section == "source_records":
                if key in source_records:
                    raise SourceRegistryFormatError(
                        "duplicate-source-record",
                        f"Duplicate source record {key!r}.",
                        line_no,
                    )
                source_records.add(key)
            else:
                if key in confirmed:
                    raise SourceRegistryFormatError(
                        "duplicate-confirmed-text",
                        f"Duplicate confirmed-text registry entry {key!r}.",
                        line_no,
                    )
                confirmed[key] = {}
            continue

        if indent == 4 and section == "confirmed_texts" and current_key is not None:
            if ":" not in stripped:
                continue
            field, value = stripped.split(":", 1)
            if value.strip():
                confirmed[current_key][field.strip()] = _scalar(value)
            continue

        # Nested editorial apparatus and source-record descriptive fields are
        # outside the provenance identity needed by the checker.

    if not saw_source_records:
        raise SourceRegistryFormatError(
            "missing-source-records-section",
            "sources.yaml must contain a top-level source_records mapping.",
        )
    if not saw_confirmed_texts:
        raise SourceRegistryFormatError(
            "missing-confirmed-texts-section",
            "sources.yaml must contain a top-level confirmed_texts mapping.",
        )

    alternatives = _parse_source_alternatives(text)
    entries = tuple(
        ConfirmedTextProvenance(
            filename=filename,
            citation_label=fields.get("citation_label"),
            source_of_record=fields.get("source_of_record"),
            source_alternatives=alternatives.get(filename, ()),
        )
        for filename, fields in confirmed.items()
    )
    return SourceRegistry(frozenset(source_records), entries)


def _parse_source_alternatives(text: str) -> dict[str, tuple[SourceAlternative, ...]]:
    """Parse the explicit list; never infer an alternative from punctuation."""
    section = filename = None
    active = False
    records: dict[str, list[dict[str, str]]] = {}
    item = None
    for line_no, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        value = raw.strip()
        if indent == 0:
            section = value
            active = False
        elif indent == 2:
            filename = value[:-1]
            active = False
        elif section == "confirmed_texts:" and indent == 4:
            if value.startswith("source_alternatives:") and value != "source_alternatives:":
                raise SourceRegistryFormatError("invalid-source-alternative", "source_alternatives must be a list of mappings.", line_no)
            active = value == "source_alternatives:"
            item = None
            if active:
                if filename in records:
                    raise SourceRegistryFormatError("invalid-source-alternative", "Duplicate source_alternatives field.", line_no)
                records[filename] = []
        elif active:
            if indent == 6 and value.startswith("- "):
                item = {}
                records[filename].append(item)
                value = value[2:]
            elif indent != 8 or item is None:
                raise SourceRegistryFormatError("invalid-source-alternative", "Expected a source-alternative list item or field.", line_no)
            if ":" not in value:
                raise SourceRegistryFormatError("invalid-source-alternative", "Expected a field and value.", line_no)
            key, val = value.split(":", 1)
            if key not in {"line", "bracket", "label", "reading"} or key in item:
                raise SourceRegistryFormatError("invalid-source-alternative", f"Unknown or duplicate field {key!r}.", line_no)
            item[key] = _scalar(val)
    parsed = {}
    for filename, items in records.items():
        if not items:
            raise SourceRegistryFormatError("invalid-source-alternative", f"Empty source_alternatives declaration in {filename!r}.")
        alternatives = []
        seen = set()
        for item in items:
            if (set(item) != {"line", "bracket", "label", "reading"}
                    or not item["line"].isascii() or not item["line"].isdigit()
                    or not item["bracket"].isascii() or not item["bracket"].isdigit()
                    or int(item["line"]) < 1 or int(item["bracket"]) < 1
                    or not item["label"].strip()
                    or re.fullmatch(r"\[[^\[\]\n]+\]", item["reading"]) is None):
                raise SourceRegistryFormatError("invalid-source-alternative", f"Incomplete or invalid source alternative in {filename!r}.")
            alt = SourceAlternative(int(item["line"]), int(item["bracket"]), item["label"], item["reading"])
            if (alt.line, alt.bracket) in seen:
                raise SourceRegistryFormatError("invalid-source-alternative", f"Duplicate source-alternative location in {filename!r}.")
            seen.add((alt.line, alt.bracket))
            alternatives.append(alt)
        parsed[filename] = tuple(alternatives)
    return parsed


def source_alternative_matches(alternative, document) -> bool:
    """Require an exact, whole-word canonical bracket group at the declared locus."""
    if (document is None or alternative.line < 1 or alternative.bracket < 1
            or alternative.line > document.line_count):
        return False
    from .confirmed_text import _editorial_labels_from_syriac, _strip_known_labels
    labels = _editorial_labels_from_syriac(document.syriac_lines[alternative.line - 1])
    text = _strip_known_labels(document.transliteration_lines[alternative.line - 1], labels)
    depth = 0
    for ch in text:
        if ch == "[":
            depth += 1
            if depth > 1:
                return False
        elif ch == "]":
            depth -= 1
            if depth < 0:
                return False
    if depth:
        return False
    groups = list(re.finditer(r"\[[^\[\]]*\]", text))
    if alternative.bracket > len(groups):
        return False
    group = groups[alternative.bracket - 1]
    return (group.group() == alternative.reading
            and (group.start() == 0 or text[group.start() - 1] == " ")
            and (group.end() == len(text) or text[group.end()] == " "))


def check_source_alternatives(registry, documents) -> tuple[ProvenanceIssue, ...]:
    return tuple(
        ProvenanceIssue("source-alternative-mismatch",
                        f"Source alternative {alt.label!r}, bracket {alt.bracket}, does not match a whole-word bracketed reading.",
                        entry.filename, alt.line)
        for entry in registry.confirmed_texts for alt in entry.source_alternatives
        if not source_alternative_matches(alt, documents.get(entry.filename))
    )


def check_source_registry(
    text: str,
    confirmed_filenames: set[str] | frozenset[str],
) -> tuple[ProvenanceIssue, ...]:
    """Check source-of-record and citation identity for the confirmed corpus."""

    try:
        registry = parse_source_registry(text)
    except SourceRegistryFormatError as exc:
        return (ProvenanceIssue(exc.code, exc.message, line=exc.line),)

    issues: list[ProvenanceIssue] = []
    registered = {entry.filename for entry in registry.confirmed_texts}
    actual = set(confirmed_filenames)

    for filename in sorted(actual - registered):
        issues.append(
            ProvenanceIssue(
                "missing-provenance",
                "Confirmed text has no entry in sources/sources.yaml.",
                filename=filename,
            )
        )
    for filename in sorted(registered - actual):
        issues.append(
            ProvenanceIssue(
                "stale-provenance",
                "sources/sources.yaml names a confirmed text file that does not exist.",
                filename=filename,
            )
        )

    labels: dict[str, str] = {}
    for entry in registry.confirmed_texts:
        if not entry.source_of_record:
            issues.append(
                ProvenanceIssue(
                    "missing-source-of-record",
                    "Confirmed text must explicitly designate a source_of_record.",
                    filename=entry.filename,
                )
            )
        elif entry.source_of_record not in registry.source_records:
            issues.append(
                ProvenanceIssue(
                    "unknown-source-of-record",
                    f"source_of_record {entry.source_of_record!r} is not declared under source_records.",
                    filename=entry.filename,
                )
            )

        if not entry.citation_label:
            issues.append(
                ProvenanceIssue(
                    "missing-citation-label",
                    "Confirmed text must have one stable machine-readable citation_label.",
                    filename=entry.filename,
                )
            )
        elif entry.citation_label in labels:
            issues.append(
                ProvenanceIssue(
                    "duplicate-citation-label",
                    f"Citation label {entry.citation_label!r} is also used by {labels[entry.citation_label]!r}.",
                    filename=entry.filename,
                )
            )
        else:
            labels[entry.citation_label] = entry.filename

    return tuple(issues)


def check_source_registry_path(
    registry_path: str | Path,
    confirmed_dir: str | Path,
) -> tuple[ProvenanceIssue, ...]:
    registry_path = Path(registry_path)
    confirmed_dir = Path(confirmed_dir)
    filenames = {
        path.relative_to(confirmed_dir).as_posix()
        for path in confirmed_dir.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".txt", ".md"}
        and path.stat().st_size > 0
    }
    text = registry_path.read_text(encoding="utf-8")
    issues = check_source_registry(text, filenames)
    try:
        registry = parse_source_registry(text)
    except SourceRegistryFormatError:
        return issues
    from .confirmed_text import parse_confirmed_text, ConfirmedTextFormatError
    documents = {}
    for entry in registry.confirmed_texts:
        if entry.source_alternatives and entry.filename in filenames:
            try:
                documents[entry.filename] = parse_confirmed_text((confirmed_dir / entry.filename).read_text(encoding="utf-8"))
            except (ConfirmedTextFormatError, UnicodeError):
                pass  # Report the unmatched declaration below; corpus checks give details.
    return issues + check_source_alternatives(registry, documents)
