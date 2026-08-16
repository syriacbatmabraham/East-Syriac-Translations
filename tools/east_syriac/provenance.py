"""Deterministic provenance checks for confirmed-text source metadata.

The project deliberately keeps source-of-record designations outside the three-block
confirmed text files. This module parses the small, controlled YAML subset used by
`sources/sources.yaml` without introducing a runtime YAML dependency, then verifies
that the authoritative corpus and the registry agree exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConfirmedTextProvenance:
    filename: str
    citation_label: str | None
    source_of_record: str | None


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
    Deeper witness apparatus remains valid YAML data but is intentionally
    ignored by this parser; an apparatus insertion need not be promoted into a
    separate source record merely to satisfy corpus provenance.
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

    entries = tuple(
        ConfirmedTextProvenance(
            filename=filename,
            citation_label=fields.get("citation_label"),
            source_of_record=fields.get("source_of_record"),
        )
        for filename, fields in confirmed.items()
    )
    return SourceRegistry(frozenset(source_records), entries)


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
        path.name
        for path in confirmed_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".txt", ".md"}
    }
    return check_source_registry(registry_path.read_text(encoding="utf-8"), filenames)
