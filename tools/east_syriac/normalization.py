"""Deterministic East Syriac source-ingestion normalization.

Implements the page-state normalization required by Transliteration Rules §16
and combining-mark ordering required by §5.1.  This module deliberately does
not transliterate: it produces the normalized Syriac representation that the
transliteration layer will consume.
"""

from __future__ import annotations

from dataclasses import dataclass
import unicodedata


# Syriac letters used by the project's consonant inventory (§3), plus U+0716
# and U+0724 which are accepted only as ingestion inputs and normalized below.
PROJECT_LETTERS = frozenset(
    {
        "\u0710",  # ALAPH
        "\u0712",  # BETH
        "\u0713",  # GAMAL
        "\u0715",  # DALATH
        "\u0716",  # DOTLESS DALATH RISH (ingestion artifact)
        "\u0717",  # HE
        "\u0718",  # WAW
        "\u0719",  # ZAIN
        "\u071a",  # HETH
        "\u071b",  # TETH
        "\u071d",  # YUDH
        "\u071f",  # KAPH
        "\u0720",  # LAMADH
        "\u0721",  # MIM
        "\u0722",  # NUN
        "\u0723",  # SEMKATH
        "\u0724",  # FINAL SEMKATH (ingestion artifact)
        "\u0725",  # E
        "\u0726",  # PE
        "\u0728",  # SADHE
        "\u0729",  # QAPH
        "\u072a",  # RISH
        "\u072b",  # SHIN
        "\u072c",  # TAW
    }
)

BGDKPT = frozenset("\u0712\u0713\u0715\u071f\u0726\u072c")
WAW = "\u0718"
YODH = "\u071d"
RISH = "\u072a"
DOTLESS_DALATH_RISH = "\u0716"
FINAL_SEMKATH = "\u0724"
SEMKATH = "\u0723"

SUPERSCRIPT_ALAPH = "\u0711"
SYAME = "\u0308"

# §16.1: single-dot source encodings collapse to a page-state and are then
# re-encoded by carrier.  The output codepoints satisfy General Rules §11.12.
SINGLE_ABOVE_INPUTS = frozenset({"\u0741", "\u073f", "\u0307"})
SINGLE_BELOW_INPUTS = frozenset({"\u0742", "\u073c", "\u0323"})
QUSSHAYA = "\u0741"
RUKKAKHA = "\u0742"
RWAHA = "\u073f"
HBASA_ESASA_DOTTED = "\u073c"
GENERIC_DOT_ABOVE = "\u0307"
GENERIC_DOT_BELOW = "\u0323"

# §16.1 / §§17–18.
TWO_DOTS_BELOW_INPUTS = frozenset({"\u0324", "\u0740", "\u0744"})
TWO_DOTS_BELOW = "\u0324"
BREVE_BELOW = "\u032e"
BETWEEN_ABOVE = "\U00001df8"
BETWEEN_BELOW = "\U00001dfa"

# East Syriac multi-dot vowels that pass through unchanged (§16.1).
EAST_MULTI_DOT_VOWELS = frozenset({"\u0732", "\u0735", "\u0738", "\u0739"})

# West Syriac vowels are refused, never mapped (§16.6).
WEST_SYRIAC_VOWELS = frozenset(
    {
        "\u0730",
        "\u0731",
        "\u0733",
        "\u0734",
        "\u0736",
        "\u0737",
        "\u073a",
        "\u073b",
        "\u073d",
        "\u073e",
    }
)

OCCULTANS_ABOVE = "\u0747"
OCCULTANS_BELOW = "\u0748"

# Explicitly out of scope at ingestion (§10, §16.1).
SYRIAC_PUNCTUATION = frozenset(chr(cp) for cp in range(0x0700, 0x070E))
SYRIAC_ABBREVIATION_MARK = "\u070f"
PRESENTATIONAL = frozenset({"\u0640", "\u200c", "\u200d"})
ACCENT_CANTILLATION = frozenset({"\u0749", "\u074a"})  # MUSIC, BARREKH
LATIN_PUNCTUATION_SUBSTITUTES = frozenset(".,:;")

# Marks understood by the normalized representation after carrier recoding.
KNOWN_MARKS = frozenset(
    {
        SUPERSCRIPT_ALAPH,
        SYAME,
        QUSSHAYA,
        RUKKAKHA,
        RWAHA,
        HBASA_ESASA_DOTTED,
        GENERIC_DOT_ABOVE,
        GENERIC_DOT_BELOW,
        TWO_DOTS_BELOW,
        BREVE_BELOW,
        BETWEEN_ABOVE,
        BETWEEN_BELOW,
        OCCULTANS_ABOVE,
        OCCULTANS_BELOW,
        *EAST_MULTI_DOT_VOWELS,
    }
)

# §5.1 project tie-break order for equal canonical combining classes.
ORDER_220 = {
    "\u0738": 0,  # vowel: dotted zlama horizontal
    "\u0739": 0,  # vowel: dotted zlama angular
    HBASA_ESASA_DOTTED: 0,  # carrier-borne vowel on waw/yodh
    RUKKAKHA: 1,
    GENERIC_DOT_BELOW: 2,
    TWO_DOTS_BELOW: 3,
    BREVE_BELOW: 4,
    OCCULTANS_BELOW: 5,
}
ORDER_230 = {
    "\u0732": 0,  # vowel: pthaha dotted
    "\u0735": 0,  # vowel: zqapha dotted
    RWAHA: 0,       # carrier-borne vowel on waw
    QUSSHAYA: 1,
    GENERIC_DOT_ABOVE: 2,
    SYAME: 3,
    OCCULTANS_ABOVE: 4,
}


@dataclass(frozen=True)
class NormalizationFlag:
    """A condition requiring human/source review."""

    code: str
    message: str
    index: int
    line: int
    column: int
    char: str

    @property
    def codepoint(self) -> str:
        return f"U+{ord(self.char):04X}"

    @property
    def unicode_name(self) -> str:
        return unicodedata.name(self.char, "UNKNOWN")


@dataclass(frozen=True)
class NormalizationChange:
    """A deterministic transformation licensed by the rules."""

    code: str
    index: int
    before: str
    after: str


@dataclass(frozen=True)
class NormalizationResult:
    text: str
    flags: tuple[NormalizationFlag, ...]
    changes: tuple[NormalizationChange, ...]

    @property
    def changed(self) -> bool:
        return bool(self.changes)

    @property
    def ok(self) -> bool:
        return not self.flags


def _line_column(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_break = text.rfind("\n", 0, index)
    column = index + 1 if last_break < 0 else index - last_break
    return line, column


def _flag(text: str, index: int, char: str, code: str, message: str) -> NormalizationFlag:
    line, column = _line_column(text, index)
    return NormalizationFlag(code, message, index, line, column, char)


def _canonical_single_point(base: str, mark: str) -> str:
    if mark in SINGLE_ABOVE_INPUTS:
        if base in BGDKPT:
            return QUSSHAYA
        if base == WAW:
            return RWAHA
        return GENERIC_DOT_ABOVE

    if base in BGDKPT:
        return RUKKAKHA
    if base in {WAW, YODH}:
        return HBASA_ESASA_DOTTED
    return GENERIC_DOT_BELOW


def _sort_marks(marks: list[str]) -> list[str]:
    """Sort a combining sequence according to §5.1 without inventing order.

    Different CCCs always sort ascending.  For CCC 220/230, the project tie-break
    is applied only when every mark in that same-class bucket is recognized by
    the corresponding project order.  Refused/unknown same-class marks retain
    their source-relative order because the rules define no canonical tie-break
    for them; their presence is flagged separately.
    """

    buckets: dict[int, list[tuple[int, str]]] = {}
    for pos, mark in enumerate(marks):
        buckets.setdefault(unicodedata.combining(mark), []).append((pos, mark))

    out: list[str] = []
    for ccc in sorted(buckets):
        bucket = buckets[ccc]
        order = ORDER_220 if ccc == 220 else ORDER_230 if ccc == 230 else None
        if order is not None and all(mark in order for _, mark in bucket):
            bucket = sorted(bucket, key=lambda item: (order[item[1]], item[0]))
        out.extend(mark for _, mark in bucket)
    return out


def _is_combining(char: str) -> bool:
    return unicodedata.combining(char) != 0 or char == SUPERSCRIPT_ALAPH


def normalize_text(text: str) -> NormalizationResult:
    """Normalize a raw East Syriac source block deterministically.

    Parenthesized editorial labels are treated as non-Syriac apparatus: their
    punctuation is preserved and their contents are not page-state interpreted.
    Square-bracketed Syriac remains active input and is normalized normally.
    """

    flags: list[NormalizationFlag] = []
    changes: list[NormalizationChange] = []

    # Step 1: remove explicitly out-of-scope source characters before any
    # page-state interpretation (§16.1).  Parenthetical editorial labels are
    # opaque so their punctuation is not mistaken for Syriac punctuation.
    kept: list[tuple[str, int, bool]] = []
    paren_depth = 0
    unexpected_lines: set[int] = set()
    for index, char in enumerate(text):
        if char == "(":
            paren_depth += 1
            kept.append((char, index, True))
            continue
        if char == ")" and paren_depth:
            kept.append((char, index, True))
            paren_depth -= 1
            continue

        removable = (
            char in SYRIAC_PUNCTUATION
            or char == SYRIAC_ABBREVIATION_MARK
            or char in PRESENTATIONAL
            or char in ACCENT_CANTILLATION
            or (paren_depth == 0 and char in LATIN_PUNCTUATION_SUBSTITUTES)
        )
        if removable:
            changes.append(NormalizationChange("remove-out-of-scope", index, char, ""))
            continue

        # A raw Syriac block can contain English only as parenthesized editorial
        # apparatus.  Flagging Latin text elsewhere makes --in-place safe even
        # if somebody accidentally points the normalizer at a full confirmed
        # three-block file.  The text is preserved for inspection.
        if paren_depth == 0 and (
            "LATIN" in unicodedata.name(char, "") and unicodedata.category(char).startswith("L")
            or char.isascii() and char.isdigit()
        ):
            line, _ = _line_column(text, index)
            if line not in unexpected_lines:
                flags.append(
                    _flag(
                        text,
                        index,
                        char,
                        "unexpected-non-syriac-text",
                        "Latin text or digits occur outside parenthesized editorial apparatus; raw Syriac block expected.",
                    )
                )
                unexpected_lines.add(line)

        if char == "\ufeff":
            flags.append(
                _flag(
                    text,
                    index,
                    char,
                    "byte-order-mark",
                    "U+FEFF BOM is not part of the Syriac block; file hygiene requires UTF-8 without BOM.",
                )
            )

        kept.append((char, index, paren_depth > 0))

    # Step 2: split into base+combining clusters while retaining original
    # indices for diagnostics.  Editorial/non-Syriac characters simply pass.
    out: list[str] = []
    i = 0
    while i < len(kept):
        base, base_index, base_editorial = kept[i]

        # An orphan combining mark cannot be interpreted by carrier.
        if _is_combining(base):
            flags.append(
                _flag(
                    text,
                    base_index,
                    base,
                    "orphan-combining-mark",
                    "Combining mark has no preceding carrier; source review required.",
                )
            )
            out.append(base)
            i += 1
            continue

        marks: list[tuple[str, int, bool]] = []
        j = i + 1
        while j < len(kept) and _is_combining(kept[j][0]):
            marks.append(kept[j])
            j += 1

        # Parenthesized editorial labels are not Syriac orthography.  Preserve
        # their combining sequences for the later whole-file NFC hygiene pass.
        if base_editorial:
            out.append(base)
            out.extend(mark for mark, _, _ in marks)
            i = j
            continue

        is_syriac_carrier = unicodedata.name(base, "").startswith("SYRIAC LETTER")
        if marks and not is_syriac_carrier:
            out.append(base)
            for mark, mark_index, _ in marks:
                flags.append(
                    _flag(
                        text,
                        mark_index,
                        mark,
                        "orphan-combining-mark",
                        "Combining mark is not attached to a Syriac letter; source review required.",
                    )
                )
                out.append(mark)
            i = j
            continue

        normalized_base = base
        if base == FINAL_SEMKATH:
            normalized_base = SEMKATH
            changes.append(NormalizationChange("final-semkath", base_index, base, normalized_base))
        elif base == DOTLESS_DALATH_RISH:
            normalized_base = RISH
            has_syame = any(mark == SYAME for mark, _, _ in marks)
            changes.append(NormalizationChange("dotless-dalath-rish", base_index, base, normalized_base))
            if not has_syame:
                flags.append(
                    _flag(
                        text,
                        base_index,
                        base,
                        "bare-u0716",
                        "Bare U+0716 normalized to resh, but the source-level anomaly requires manual review.",
                    )
                )

        # Flag Syriac letters outside the project's consonant inventory.
        if "SYRIAC LETTER" in unicodedata.name(base, "") and base not in PROJECT_LETTERS:
            flags.append(
                _flag(
                    text,
                    base_index,
                    base,
                    "unrecognized-syriac-letter",
                    "Syriac letter is outside the canonical consonant inventory.",
                )
            )

        normalized_marks: list[str] = []
        above_count = 0
        below_count = 0
        for mark, mark_index, _ in marks:
            new_mark = mark
            if mark in SINGLE_ABOVE_INPUTS:
                new_mark = _canonical_single_point(normalized_base, mark)
                above_count += 1
            elif mark in SINGLE_BELOW_INPUTS:
                new_mark = _canonical_single_point(normalized_base, mark)
                below_count += 1
            elif mark in TWO_DOTS_BELOW_INPUTS:
                new_mark = TWO_DOTS_BELOW
            elif mark in WEST_SYRIAC_VOWELS:
                flags.append(
                    _flag(
                        text,
                        mark_index,
                        mark,
                        "west-syriac-vowel",
                        "West Syriac vowel codepoint is refused and has been left unmapped.",
                    )
                )
            elif mark not in KNOWN_MARKS:
                flags.append(
                    _flag(
                        text,
                        mark_index,
                        mark,
                        "unrecognized-combining-mark",
                        "Combining mark is not represented by the current canonical system.",
                    )
                )

            if new_mark != mark:
                changes.append(NormalizationChange("normalize-page-state", mark_index, mark, new_mark))
            normalized_marks.append(new_mark)

        if above_count > 1:
            first_index = next(idx for mark, idx, _ in marks if mark in SINGLE_ABOVE_INPUTS)
            first_char = next(mark for mark, _, _ in marks if mark in SINGLE_ABOVE_INPUTS)
            flags.append(
                _flag(
                    text,
                    first_index,
                    first_char,
                    "duplicate-single-point-above",
                    "More than one single-point-above encoding occurs on one carrier.",
                )
            )
        if below_count > 1:
            first_index = next(idx for mark, idx, _ in marks if mark in SINGLE_BELOW_INPUTS)
            first_char = next(mark for mark, _, _ in marks if mark in SINGLE_BELOW_INPUTS)
            flags.append(
                _flag(
                    text,
                    first_index,
                    first_char,
                    "duplicate-single-point-below",
                    "More than one single-point-below encoding occurs on one carrier.",
                )
            )

        ordered_marks = _sort_marks(normalized_marks)
        if ordered_marks != normalized_marks:
            before = "".join(normalized_marks)
            after = "".join(ordered_marks)
            changes.append(NormalizationChange("mark-order", base_index, before, after))

        out.append(normalized_base)
        out.extend(ordered_marks)
        i = j

    pre_nfc = "".join(out)
    normalized = unicodedata.normalize("NFC", pre_nfc)
    if normalized != pre_nfc:
        # One aggregate record is enough: exact character-level NFC edits are
        # implementation details, whereas the resulting string is normative.
        changes.append(NormalizationChange("nfc", 0, pre_nfc, normalized))

    return NormalizationResult(normalized, tuple(flags), tuple(changes))
