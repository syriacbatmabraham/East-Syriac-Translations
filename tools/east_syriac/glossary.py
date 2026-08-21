"""Deterministic parser and corpus validator for the project Glossary.

Implements General Rules §11.1–10 and the Glossary-facing portion of §11.11–14.
The human-readable Glossary remains authoritative data; this module checks that
its machine-readable conventions agree with the confirmed corpus.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata
from collections import defaultdict
from typing import Iterable, Mapping

from .confirmed_text import ConfirmedTextDocument, check_confirmed_text_path
from .provenance import SourceRegistry, parse_source_registry
from .transliteration import TransliterationError, transliterate_text
from .transliteration_inverse import reverse_transliterate


HEADER_RE = re.compile(
    r"^(?P<syriac>.+?)\s{2,}\[(?P<root>[^\]]*)\]\s{2,}"
    r"\{(?P<morph>[^}]*)\}\s{2,}\(search:\s*(?P<search>[^)]*)\)$"
)
DETAIL_RE = re.compile(r"^(?P<canonical>.+?) \((?P<total>\d+)\) — (?P<renderings>.+)$")
RENDERING_RE = re.compile(
    r"^(?P<text>.+?) \((?P<count>\d+(?:\+\d+)?)\)(?: (?P<binding>\[[^\]]+\]))?$"
)
BULLET_RE = re.compile(
    r'^\* (?P<attested>.+?) · "(?P<context>.*)" \((?P<citation>.+)\)'
    r'(?: → (?P<pointer>.+))?$'
)
PAREN_RE = re.compile(r"\([^()]*\)")
SYRIAC_RANGE_RE = re.compile(r"[\u0700-\u074f]")
CITATION_RE = re.compile(r"^(?P<label>.+?)(?:,)?\s+Line\s+(?P<line>\d+)$")

STEMS = frozenset({
    "Peal", "Ethpeel", "Pael", "Ethpaal", "Aphel", "Ettaphal", "Shaphel", "Eshtaphal"
})
GENDERS = frozenset({"m", "f", "c"})
NUMBERS = frozenset({"sg", "pl"})
STATES = frozenset({"abs", "cst", "emph"})
FINITE_TENSES = frozenset({"perf", "impf", "impv"})
ROOT_MARKERS = frozenset({"—", "prop. noun", "Gk. loan"})
ROOT_COMPONENT_RE = re.compile(r"^[A-Za-zʾʿḥṭṣš]+(?:-[A-Za-zʾʿḥṭṣš]+)*\??$")
PERSON_FEATURE_RE = re.compile(r"^[123](?:m|f|c)?(?:sg|pl)$|^[123]c?p(?:l)?$|^[123](?:m|f|c)p$")
SUFFIX_RE = re.compile(r"^[123](?:m|f|c)?(?:s|p|sg|pl)?\s+(?:suff\.|encl\.)$")


@dataclass(frozen=True)
class GlossaryIssue:
    code: str
    message: str
    line: int | None = None
    entry: str | None = None


@dataclass(frozen=True)
class GlossaryRendering:
    text: str
    base: int
    extra: int
    binding: str | None = None

    @property
    def total(self) -> int:
        return self.base + self.extra


@dataclass(frozen=True)
class GlossaryOccurrence:
    attested: str
    context: str
    citation: str
    phrase_pointer: str | None
    line: int


@dataclass(frozen=True)
class GlossaryEntry:
    section: str
    syriac_headword: str
    root: str
    morphology: str
    search_key: str
    canonical: str
    decision_total: int
    renderings: tuple[GlossaryRendering, ...]
    occurrences: tuple[GlossaryOccurrence, ...]
    line: int


@dataclass(frozen=True)
class GlossaryCheckResult:
    entries: tuple[GlossaryEntry, ...]
    issues: tuple[GlossaryIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


@dataclass(frozen=True)
class CitationTarget:
    filename: str
    line: int
    witness: str | None


@dataclass(frozen=True)
class CorpusToken:
    canonical: str
    syriac: str
    in_brackets: bool


@dataclass(frozen=True)
class CorpusLine:
    filename: str
    line: int
    canonical_text: str
    english_text: str
    tokens: tuple[CorpusToken, ...]

    @property
    def signature(self) -> tuple[str, ...]:
        return tuple(token.canonical for token in self.tokens)


@dataclass(frozen=True)
class _ParsedEntry:
    entry: GlossaryEntry | None
    next_index: int
    issues: tuple[GlossaryIssue, ...]


def _parse_count(text: str) -> tuple[int, int]:
    if "+" in text:
        base, extra = text.split("+", 1)
        return int(base), int(extra)
    return int(text), 0


def _parse_entry(lines: list[str], index: int, section: str) -> _ParsedEntry:
    header = lines[index]
    header_match = HEADER_RE.match(header)
    if header_match is None:
        return _ParsedEntry(
            None,
            index + 1,
            (GlossaryIssue("glossary-entry-format", "Expected a Glossary entry header.", index + 1),),
        )

    detail_index = index + 1
    if detail_index >= len(lines):
        return _ParsedEntry(
            None,
            detail_index,
            (GlossaryIssue("glossary-entry-format", "Entry has no canonical/rendering line.", index + 1),),
        )
    detail_match = DETAIL_RE.match(lines[detail_index])
    if detail_match is None:
        return _ParsedEntry(
            None,
            detail_index + 1,
            (GlossaryIssue("glossary-entry-format", "Expected canonical transliteration, decision total, and renderings.", detail_index + 1),),
        )

    renderings: list[GlossaryRendering] = []
    parse_issues: list[GlossaryIssue] = []
    for part in detail_match.group("renderings").split(", "):
        match = RENDERING_RE.match(part)
        if match is None:
            parse_issues.append(
                GlossaryIssue(
                    "glossary-rendering-format",
                    f"Could not parse rendering/count segment {part!r}.",
                    detail_index + 1,
                    detail_match.group("canonical"),
                )
            )
            continue
        base, extra = _parse_count(match.group("count"))
        renderings.append(GlossaryRendering(match.group("text"), base, extra, match.group("binding")))

    occurrences: list[GlossaryOccurrence] = []
    cursor = detail_index + 1
    while cursor < len(lines) and lines[cursor].startswith("* "):
        match = BULLET_RE.match(lines[cursor])
        if match is None:
            parse_issues.append(
                GlossaryIssue(
                    "glossary-bullet-format",
                    "Could not parse occurrence bullet.",
                    cursor + 1,
                    detail_match.group("canonical"),
                )
            )
        else:
            occurrences.append(
                GlossaryOccurrence(
                    match.group("attested"),
                    match.group("context"),
                    match.group("citation"),
                    match.group("pointer"),
                    cursor + 1,
                )
            )
        cursor += 1

    entry = GlossaryEntry(
        section=section,
        syriac_headword=header_match.group("syriac"),
        root=header_match.group("root").strip(),
        morphology=header_match.group("morph").strip(),
        search_key=header_match.group("search").strip(),
        canonical=detail_match.group("canonical"),
        decision_total=int(detail_match.group("total")),
        renderings=tuple(renderings),
        occurrences=tuple(occurrences),
        line=index + 1,
    )
    return _ParsedEntry(entry, cursor, tuple(parse_issues))


def parse_glossary(text: str) -> tuple[tuple[GlossaryEntry, ...], tuple[GlossaryIssue, ...]]:
    lines = text.splitlines()
    entries: list[GlossaryEntry] = []
    issues: list[GlossaryIssue] = []
    section: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if line == "## Phrases":
            section = "phrases"
            index += 1
            continue
        if line == "## Forms":
            section = "forms"
            index += 1
            continue
        if section is None or not line or line == "---":
            index += 1
            continue
        if line.startswith("#"):
            index += 1
            continue
        parsed = _parse_entry(lines, index, section)
        issues.extend(parsed.issues)
        if parsed.entry is not None:
            entries.append(parsed.entry)
        index = parsed.next_index
        while index < len(lines) and not lines[index]:
            index += 1
    return tuple(entries), tuple(issues)


def _editorial_labels_from_syriac(line: str) -> tuple[str, ...]:
    labels: list[str] = []
    for match in PAREN_RE.finditer(line):
        label = match.group(0)
        if SYRIAC_RANGE_RE.search(label):
            continue
        if not any(ch.isalpha() for ch in label):
            continue
        labels.append(label)
    return tuple(labels)


def _strip_labels(line: str, labels: Iterable[str]) -> str:
    result = line
    for label in labels:
        result = result.replace(label, "", 1)
    result = re.sub(r" {2,}", " ", result)
    return result.strip()


def _strip_interpretive_supplements(english: str, source_bracket_count: int) -> str:
    """Remove English-only square-bracket supplements, retaining source variants.

    Source-bracket groups are ordered in the same line in all three layers. English
    may collapse a source variant, so at most the first N English groups (where N is
    the Syriac source-bracket count) are retained; later groups are interpretive.
    """
    seen = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal seen
        seen += 1
        if seen <= source_bracket_count:
            return match.group(0)
        return ""

    result = re.sub(r"\[[^\[\]]*\]", replace, english)
    result = re.sub(r" {2,}", " ", result)
    return result.strip()


def _tokenize_layer(text: str) -> tuple[tuple[str, bool], ...]:
    tokens: list[tuple[str, bool]] = []
    current: list[str] = []
    depth = 0
    token_bracketed = False

    def flush() -> None:
        nonlocal current, token_bracketed
        if current:
            tokens.append(("".join(current), token_bracketed))
        current = []
        token_bracketed = False

    for ch in text:
        if ch == " ":
            flush()
            continue
        if ch == "[":
            depth += 1
            token_bracketed = True
            continue
        if ch == "]":
            token_bracketed = True
            depth = max(0, depth - 1)
            continue
        if depth:
            token_bracketed = True
        current.append(ch)
    flush()
    return tuple(tokens)


def build_corpus(documents: Mapping[str, ConfirmedTextDocument]) -> tuple[CorpusLine, ...]:
    corpus: list[CorpusLine] = []
    for filename, document in documents.items():
        for line_no, (syriac, canonical, english) in enumerate(
            zip(document.syriac_lines, document.transliteration_lines, document.english_lines, strict=True),
            start=1,
        ):
            if not syriac and not canonical and not english:
                continue
            labels = _editorial_labels_from_syriac(syriac)
            clean_syriac = _strip_labels(syriac, labels)
            clean_canonical = _strip_labels(canonical, labels)
            clean_english = _strip_labels(english, labels)
            clean_english = _strip_interpretive_supplements(clean_english, clean_syriac.count("["))
            syriac_tokens = _tokenize_layer(clean_syriac)
            canonical_tokens = _tokenize_layer(clean_canonical)
            if len(syriac_tokens) != len(canonical_tokens):
                size = min(len(syriac_tokens), len(canonical_tokens))
                syriac_tokens = syriac_tokens[:size]
                canonical_tokens = canonical_tokens[:size]
            tokens = tuple(
                CorpusToken(can[0], syr[0], can[1] or syr[1])
                for syr, can in zip(syriac_tokens, canonical_tokens, strict=True)
            )
            corpus.append(CorpusLine(filename, line_no, clean_canonical, clean_english, tokens))
    return tuple(corpus)


def _resolve_citation(citation: str, registry: SourceRegistry) -> CitationTarget | None:
    match = CITATION_RE.match(citation)
    if match is None:
        return None
    label_part = match.group("label").rstrip()
    line = int(match.group("line"))
    candidates = sorted(
        (entry for entry in registry.confirmed_texts if entry.citation_label),
        key=lambda entry: len(entry.citation_label or ""),
        reverse=True,
    )
    for entry in candidates:
        label = entry.citation_label or ""
        if label_part == label:
            return CitationTarget(entry.filename, line, None)
        suffix = " " + label
        if label_part.endswith(suffix):
            witness = label_part[: -len(suffix)].strip()
            if witness:
                return CitationTarget(entry.filename, line, witness)
    return None


def _normalize_attested(text: str) -> tuple[str, ...]:
    return tuple(token for token, _ in _tokenize_layer(text) if token)


def _sequence_matches(line: CorpusLine, attested: tuple[str, ...]) -> list[tuple[int, int]]:
    if not attested or len(attested) > len(line.tokens):
        return []
    canon = [token.canonical for token in line.tokens]
    n = len(attested)
    return [
        (start, start + n)
        for start in range(0, len(canon) - n + 1)
        if tuple(canon[start : start + n]) == attested
    ]


def _syriac_bases(text: str) -> str:
    return "".join(ch for ch in text if "SYRIAC LETTER" in unicodedata.name(ch, ""))


def _is_negative_or_proclitic(token: CorpusToken) -> bool:
    bases = _syriac_bases(token.syriac)
    if not bases:
        return False
    if len(bases) == 1 and bases in {"ܘ", "ܕ", "ܒ", "ܠ"}:
        return True
    negative = "ܠܐ"
    if bases.endswith(negative):
        prefix = bases[: -len(negative)]
        return not prefix or all(ch in {"ܘ", "ܕ", "ܒ", "ܠ"} for ch in prefix)
    return False


def _is_acclamation(token: CorpusToken) -> bool:
    bases = _syriac_bases(token.syriac)
    for acclamation in ("ܐܡܝܢ", "ܗܠܠܘܝܐ"):
        if bases.endswith(acclamation):
            prefix = bases[: -len(acclamation)]
            if not prefix or all(ch in {"ܘ", "ܕ", "ܒ", "ܠ"} for ch in prefix):
                return True
    return False


def _valid_root(root: str) -> bool:
    if root in ROOT_MARKERS:
        return True
    if root in {"particle", "prep.", "conj.", "adv."}:
        return True
    parts = root.split(" + ")
    return bool(parts) and all(ROOT_COMPONENT_RE.fullmatch(part) for part in parts)


def _split_gender_number_state(token: str) -> tuple[str, str, str] | None:
    parts = [part for part in token.split(".") if part]
    if len(parts) != 3:
        return None
    if parts[0] not in GENDERS or parts[1] not in NUMBERS or parts[2] not in STATES:
        return None
    return parts[0], parts[1], parts[2]


def _valid_person_gender_number(token: str) -> bool:
    return re.fullmatch(r"([123])([mfc])\.(sg|pl)\.", token) is not None


def _valid_nominal_morph(base: str) -> bool:
    if base.endswith(" indecl."):
        return base.startswith(("noun ", "adj. ", "prop. n."))
    prefixes = ("noun ", "adj. ", "verbal noun ", "referent noun ", "referent adj. ")
    for prefix in prefixes:
        if base.startswith(prefix):
            return _split_gender_number_state(base[len(prefix):]) is not None
    if base.startswith("num. "):
        rest = base[len("num. "):]
        if _split_gender_number_state(rest) is not None:
            return True
        return rest in {"m.", "f."}
    return False


def _valid_pronominal_morph(base: str) -> bool:
    if base.startswith("pron. "):
        return re.fullmatch(r"[123][mfc]\.(?:sg|pl)\.", base[len("pron. "):]) is not None
    if base.startswith(("dem. pron. ", "rel. pron. ")):
        rest = base.split("pron. ", 1)[1]
        return re.fullmatch(r"[mfc]\.(?:sg|pl)\.", rest) is not None
    if base in {"interrog. pron.", "indef. pron."}:
        return True
    return False


def _valid_verbal_morph(base: str) -> bool:
    stem, sep, rest = base.partition(" ")
    if not sep or stem not in STEMS:
        return False
    if rest == "inf.":
        return True
    for tense in FINITE_TENSES:
        prefix = tense + ". "
        if rest.startswith(prefix):
            return _valid_person_gender_number(rest[len(prefix):])
    for ptcp in ("active ptcp. ", "passive ptcp. ", "ptcp. "):
        if rest.startswith(ptcp):
            return _split_gender_number_state(rest[len(ptcp):]) is not None
    return False


def _valid_simple_class(base: str) -> bool:
    if base in {"particle", "adv.", "prep.", "conj.", "quant.", "poss.", "prop. n."}:
        return True
    if base in {"interrog. adv."}:
        return True
    return False


def _valid_suffix_component(component: str) -> bool:
    if SUFFIX_RE.fullmatch(component):
        return True
    if component.startswith("prep. ") and len(component.split()) == 2:
        return True
    return False


def _valid_morphology(morphology: str, section: str) -> bool:
    if not morphology:
        return False
    if section == "phrases":
        return morphology.endswith(" phrase") and len(morphology.split()) >= 2
    components = morphology.split(" + ")
    base = components[0]
    if not (
        _valid_nominal_morph(base)
        or _valid_pronominal_morph(base)
        or _valid_verbal_morph(base)
        or _valid_simple_class(base)
    ):
        if len(components) > 1 and (_valid_simple_class(base) or _valid_nominal_morph(base)):
            pass
        else:
            return False
    for component in components[1:]:
        if _valid_suffix_component(component):
            continue
        if _valid_nominal_morph(component) or _valid_simple_class(component) or _valid_pronominal_morph(component):
            continue
        return False
    return True


def _rendering_traceable(rendering: str, contexts: Iterable[str]) -> bool:
    if rendering == "⌀" or rendering.startswith("→"):
        return True
    expanded = re.sub(r"\(([^()]*)\)", r"\1", rendering)
    pieces = [piece.strip().casefold() for piece in expanded.split("...") if piece.strip()]
    if not pieces:
        return False
    for context in contexts:
        haystack = context.casefold()
        pos = 0
        ok = True
        for piece in pieces:
            found = haystack.find(piece, pos)
            if found < 0:
                ok = False
                break
            pos = found + len(piece)
        if ok:
            return True
    return False


def _context_intervals(context: str, line: str) -> list[tuple[int, int]]:
    pieces = context.split("...")
    nonempty = [(i, piece) for i, piece in enumerate(pieces) if piece]
    if not nonempty:
        return []
    candidates: list[tuple[int, int, int]] = [(0, 0, 0)]
    starts_with_ellipsis = context.startswith("...")
    ends_with_ellipsis = context.endswith("...")
    placements: list[tuple[int, int]] = []

    def walk(piece_index: int, search_from: int, first_start: int | None, last_end: int) -> None:
        if piece_index == len(nonempty):
            assert first_start is not None
            if first_start > 0 and not starts_with_ellipsis:
                return
            if last_end < len(line) and not ends_with_ellipsis:
                return
            placements.append((first_start, last_end))
            return
        _, piece = nonempty[piece_index]
        start = line.find(piece, search_from)
        while start >= 0:
            end = start + len(piece)
            walk(piece_index + 1, end, start if first_start is None else first_start, end)
            start = line.find(piece, start + 1)

    walk(0, 0, None, 0)
    return placements


def _line_map(corpus: Iterable[CorpusLine]) -> dict[tuple[str, int], CorpusLine]:
    return {(line.filename, line.line): line for line in corpus}


def _duplicate_line_exemptions(
    corpus: tuple[CorpusLine, ...],
    covered: set[tuple[str, int, int]],
    intrinsic: set[tuple[str, int, int]],
) -> set[tuple[str, int, int]]:
    groups: dict[tuple[str, ...], list[CorpusLine]] = defaultdict(list)
    for line in corpus:
        if line.signature:
            groups[line.signature].append(line)
    exempt: set[tuple[str, int, int]] = set()
    for lines in groups.values():
        if len(lines) < 2:
            continue
        for index in range(len(lines[0].tokens)):
            loci = {(line.filename, line.line, index) for line in lines}
            if loci & (covered | intrinsic):
                exempt.update(loci - covered)
    return exempt


def _inline_repetition_exemptions(
    corpus: tuple[CorpusLine, ...],
    covered: set[tuple[str, int, int]],
    intrinsic: set[tuple[str, int, int]],
) -> set[tuple[str, int, int]]:
    exempt: set[tuple[str, int, int]] = set()
    for line in corpus:
        seq = list(line.signature)
        length = len(seq)
        for width in range(length // 2, 0, -1):
            for start in range(0, length - 2 * width + 1):
                if seq[start : start + width] != seq[start + width : start + 2 * width]:
                    continue
                first = {(line.filename, line.line, i) for i in range(start, start + width)}
                second = {(line.filename, line.line, i) for i in range(start + width, start + 2 * width)}
                if first <= (covered | intrinsic | exempt):
                    exempt.update(second - covered)
    return exempt


def check_glossary(
    glossary_text: str,
    documents: Mapping[str, ConfirmedTextDocument],
    registry: SourceRegistry,
) -> GlossaryCheckResult:
    entries, parse_issues = parse_glossary(glossary_text)
    issues: list[GlossaryIssue] = list(parse_issues)

    for line_no, line in enumerate(glossary_text.splitlines(), start=1):
        for ch in line:
            name = unicodedata.name(ch, "")
            if "GREEK" in name or "CYRILLIC" in name:
                issues.append(
                    GlossaryIssue(
                        "glossary-homoglyph",
                        f"Suspicious {name} U+{ord(ch):04X} in Glossary text.",
                        line_no,
                    )
                )

    if unicodedata.normalize("NFC", glossary_text) != glossary_text:
        issues.append(GlossaryIssue("glossary-non-nfc", "Glossary is not NFC normalized."))

    for entry in entries:
        base_sum = sum(rendering.base for rendering in entry.renderings)
        total_sum = sum(rendering.total for rendering in entry.renderings)
        if len(entry.occurrences) != base_sum:
            issues.append(
                GlossaryIssue(
                    "entry-base-count-mismatch",
                    f"{len(entry.occurrences)} bullets != Σbase {base_sum}.",
                    entry.line,
                    entry.canonical,
                )
            )
        if entry.decision_total != total_sum:
            issues.append(
                GlossaryIssue(
                    "entry-decision-total-mismatch",
                    f"Decision total {entry.decision_total} != Σ(base+extra) {total_sum}.",
                    entry.line,
                    entry.canonical,
                )
            )

    identities: dict[tuple[str, str, str], GlossaryEntry] = {}
    for entry in entries:
        identity = (entry.canonical, entry.root, entry.morphology)
        previous = identities.get(identity)
        if previous is not None:
            issues.append(
                GlossaryIssue(
                    "duplicate-entry-identity",
                    f"Duplicate canonical headword + root + morphology; first entry is line {previous.line}.",
                    entry.line,
                    entry.canonical,
                )
            )
        else:
            identities[identity] = entry
        if not _valid_root(entry.root):
            issues.append(
                GlossaryIssue(
                    "invalid-root-field",
                    f"Root field {entry.root!r} is neither a project root nor a declared marker.",
                    entry.line,
                    entry.canonical,
                )
            )
        if not _valid_morphology(entry.morphology, entry.section):
            issues.append(
                GlossaryIssue(
                    "invalid-morphology-field",
                    f"Morphology {entry.morphology!r} does not satisfy the project field grammar.",
                    entry.line,
                    entry.canonical,
                )
            )

    corpus = build_corpus(documents)
    lines_by_locus = _line_map(corpus)
    assignment_count: dict[tuple[str, int, tuple[str, ...]], int] = defaultdict(int)
    covered: set[tuple[str, int, int]] = set()
    valid_contexts: dict[int, list[str]] = defaultdict(list)
    context_records: list[tuple[GlossaryOccurrence, CitationTarget, CorpusLine, tuple[int, int]]] = []

    for entry_index, entry in enumerate(entries):
        for occurrence in entry.occurrences:
            target = _resolve_citation(occurrence.citation, registry)
            if target is None:
                issues.append(
                    GlossaryIssue(
                        "orphan-glossary-occurrence",
                        f"Citation {occurrence.citation!r} does not resolve to a registered confirmed text.",
                        occurrence.line,
                        entry.canonical,
                    )
                )
                continue
            corpus_line = lines_by_locus.get((target.filename, target.line))
            if corpus_line is None:
                issues.append(
                    GlossaryIssue(
                        "orphan-glossary-occurrence",
                        f"Citation {occurrence.citation!r} points outside the confirmed text.",
                        occurrence.line,
                        entry.canonical,
                    )
                )
                continue

            attested = _normalize_attested(occurrence.attested)
            matches = _sequence_matches(corpus_line, attested)
            key = (target.filename, target.line, attested)
            ordinal = assignment_count[key]
            assignment_count[key] += 1
            if ordinal >= len(matches):
                issues.append(
                    GlossaryIssue(
                        "attested-form-not-in-line",
                        f"Attested form {occurrence.attested!r} is not available as an unclaimed token sequence in {occurrence.citation}.",
                        occurrence.line,
                        entry.canonical,
                    )
                )
                issues.append(
                    GlossaryIssue(
                        "orphan-glossary-occurrence",
                        "Glossary bullet claims no corresponding corpus occurrence.",
                        occurrence.line,
                        entry.canonical,
                    )
                )
            else:
                start, end = matches[ordinal]
                bracketed = any(corpus_line.tokens[i].in_brackets for i in range(start, end))
                if target.witness and not bracketed:
                    issues.append(
                        GlossaryIssue(
                            "witness-citation-not-in-apparatus",
                            f"Witness-qualified citation {occurrence.citation!r} resolves to non-bracketed source text.",
                            occurrence.line,
                            entry.canonical,
                        )
                    )
                if bracketed and not target.witness:
                    issues.append(
                        GlossaryIssue(
                            "apparatus-occurrence-missing-witness",
                            "Bracketed witness occurrence must carry its witness qualifier in the citation.",
                            occurrence.line,
                            entry.canonical,
                        )
                    )
                if entry.section == "forms":
                    for token_index in range(start, end):
                        covered.add((target.filename, target.line, token_index))

            intervals = _context_intervals(occurrence.context, corpus_line.english_text)
            if not intervals:
                issues.append(
                    GlossaryIssue(
                        "context-not-in-line",
                        f"Context {occurrence.context!r} is not a correctly ellipsized literal span of the cited English line.",
                        occurrence.line,
                        entry.canonical,
                    )
                )
            else:
                interval = intervals[0]
                context_records.append((occurrence, target, corpus_line, interval))
                valid_contexts[entry_index].append(occurrence.context)

    intrinsic: set[tuple[str, int, int]] = set()
    for line in corpus:
        for token_index, token in enumerate(line.tokens):
            locus = (line.filename, line.line, token_index)
            if _is_negative_or_proclitic(token) or _is_acclamation(token):
                intrinsic.add(locus)
            if token.in_brackets:
                for other_index, other in enumerate(line.tokens):
                    if other_index == token_index or other.in_brackets:
                        continue
                    if other.canonical == token.canonical and (line.filename, line.line, other_index) in covered:
                        intrinsic.add(locus)
                        break

    repeated = _inline_repetition_exemptions(corpus, covered, intrinsic)
    duplicate_lines = _duplicate_line_exemptions(corpus, covered, intrinsic | repeated)
    exempt = intrinsic | repeated | duplicate_lines

    for line in corpus:
        for token_index, token in enumerate(line.tokens):
            locus = (line.filename, line.line, token_index)
            if locus not in covered and locus not in exempt:
                issues.append(
                    GlossaryIssue(
                        "missing-corpus-occurrence",
                        f"Confirmed token {token.canonical!r} at {line.filename} Line {line.line} has no Glossary occurrence and no §11.4 exemption.",
                    )
                )

    for entry_index, entry in enumerate(entries):
        contexts = valid_contexts.get(entry_index, [])
        for rendering in entry.renderings:
            if not _rendering_traceable(rendering.text, contexts):
                issues.append(
                    GlossaryIssue(
                        "rendering-not-traceable",
                        f"Rendering {rendering.text!r} is not traceable in this entry's valid context strings.",
                        entry.line,
                        entry.canonical,
                    )
                )

    by_locus: dict[tuple[str, int], list[tuple[str, tuple[int, int], int, str]]] = defaultdict(list)
    for occurrence, target, _line, interval in context_records:
        by_locus[(target.filename, target.line)].append((occurrence.context, interval, occurrence.line, occurrence.citation))
    for records in by_locus.values():
        for i, (context_a, interval_a, line_a, citation) in enumerate(records):
            for context_b, interval_b, line_b, _ in records[i + 1 :]:
                if interval_a == interval_b:
                    continue
                if interval_a[1] <= interval_b[0] or interval_b[1] <= interval_a[0]:
                    continue
                issues.append(
                    GlossaryIssue(
                        "overlapping-contexts",
                        f"Contexts {context_a!r} and {context_b!r} overlap without coinciding at {citation} (other bullet line {line_b}).",
                        line_a,
                    )
                )

    syriac_to_canonical: dict[str, str] = {}
    canonical_to_syriac: dict[str, str] = {}
    for entry in entries:
        try:
            forward = transliterate_text(entry.syriac_headword).text
        except TransliterationError as exc:
            issues.append(
                GlossaryIssue(
                    "glossary-headword-transliteration-error",
                    f"Syriac headword is not a valid normalized page-state ({exc.code}): {exc.message}",
                    entry.line,
                    entry.canonical,
                )
            )
            continue
        if forward != entry.canonical:
            issues.append(
                GlossaryIssue(
                    "glossary-headword-forward-mismatch",
                    f"Stored canonical headword {entry.canonical!r} != mechanically derived {forward!r}.",
                    entry.line,
                    entry.canonical,
                )
            )
        try:
            reverse = reverse_transliterate(entry.canonical).text
        except TransliterationError as exc:
            issues.append(
                GlossaryIssue(
                    "glossary-headword-invalid-canonical",
                    f"Canonical headword does not invert ({exc.code}): {exc.message}",
                    entry.line,
                    entry.canonical,
                )
            )
        else:
            if reverse != entry.syriac_headword:
                issues.append(
                    GlossaryIssue(
                        "glossary-headword-reverse-mismatch",
                        f"Canonical headword reconstructs {reverse!r}, not stored Syriac {entry.syriac_headword!r}.",
                        entry.line,
                        entry.canonical,
                    )
                )
        previous_canonical = syriac_to_canonical.setdefault(entry.syriac_headword, entry.canonical)
        if previous_canonical != entry.canonical:
            issues.append(
                GlossaryIssue(
                    "syriac-spelling-maps-multiple-ways",
                    f"One Syriac headword maps to both {previous_canonical!r} and {entry.canonical!r}.",
                    entry.line,
                    entry.canonical,
                )
            )
        previous_syriac = canonical_to_syriac.setdefault(entry.canonical, entry.syriac_headword)
        if previous_syriac != entry.syriac_headword:
            issues.append(
                GlossaryIssue(
                    "canonical-maps-multiple-spellings",
                    "One canonical headword maps to more than one Syriac spelling.",
                    entry.line,
                    entry.canonical,
                )
            )

    return GlossaryCheckResult(entries, tuple(issues))


def check_glossary_path(
    glossary_path: str | Path,
    confirmed_dir: str | Path,
    registry_path: str | Path,
) -> GlossaryCheckResult:
    glossary_path = Path(glossary_path)
    confirmed_dir = Path(confirmed_dir)
    registry_path = Path(registry_path)
    registry = parse_source_registry(registry_path.read_text(encoding="utf-8"))
    documents: dict[str, ConfirmedTextDocument] = {}
    preflight: list[GlossaryIssue] = []
    for path in sorted(confirmed_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in {".txt", ".md"}:
            continue
        checked = check_confirmed_text_path(path)
        if not checked.ok or checked.document is None:
            for issue in checked.issues:
                preflight.append(
                    GlossaryIssue(
                        "confirmed-corpus-preflight-failed",
                        f"{path.name}: {issue.code}: {issue.message}",
                        issue.line,
                    )
                )
            continue
        documents[path.name] = checked.document
    result = check_glossary(glossary_path.read_text(encoding="utf-8"), documents, registry)
    if preflight:
        return GlossaryCheckResult(result.entries, tuple(preflight) + result.issues)
    return result
