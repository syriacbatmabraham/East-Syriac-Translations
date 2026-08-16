"""Human-readable audit of normalized East Syriac page-states.

The normalizer answers "what canonical codepoints represent this page-state?".
This module answers the complementary human-review question: "what does the
machine believe is written on each letter?" It operates only on normalized
Syriac. Canonical transliteration may supply word labels for the report header
without changing the page-state analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import unicodedata

from .normalization import (
    BGDKPT,
    WAW,
    YODH,
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
    MARHETANA_ABOVE,
    MARHETANA_BELOW,
    OCCULTANS_ABOVE,
    OCCULTANS_BELOW,
    EAST_MULTI_DOT_VOWELS,
    WEST_SYRIAC_VOWELS,
)


LETTER_NAMES = {
    "\u0710": "Alaph",
    "\u0712": "Beth",
    "\u0713": "Gamal",
    "\u0715": "Dalath",
    "\u0716": "U+0716 dotless dalath/resh",
    "\u0717": "Heh",
    "\u0718": "Waw",
    "\u0719": "Zain",
    "\u071a": "Heth",
    "\u071b": "Teth",
    "\u071d": "Yodh",
    "\u071f": "Kaph",
    "\u0720": "Lamad",
    "\u0721": "Mim",
    "\u0722": "Nun",
    "\u0723": "Semkath",
    "\u0724": "Final semkath",
    "\u0725": "ʿE",
    "\u0726": "Pe",
    "\u0728": "Sadhe",
    "\u0729": "Qoph",
    "\u072a": "Resh",
    "\u072b": "Shin",
    "\u072c": "Taw",
}

VOWEL_NAMES = {
    "\u0732": "pṯāḥā: a",
    "\u0735": "zqāpā: ā",
    "\u0738": "zlāmā pšīqā: e",
    "\u0739": "zlāmā qašyā: ē",
}


@dataclass(frozen=True)
class PageStateIssue:
    """A suspicious normalized page-state requiring correction/review."""

    code: str
    message: str
    word: int
    letter: int
    char: str

    @property
    def codepoint(self) -> str:
        return f"U+{ord(self.char):04X}"


@dataclass(frozen=True)
class PageStateNotice:
    """A nonblocking page-check notice."""

    code: str
    message: str
    word: int
    letter: int
    char: str

    @property
    def codepoint(self) -> str:
        return f"U+{ord(self.char):04X}"


@dataclass(frozen=True)
class LetterState:
    base: str
    name: str
    marks: tuple[str, ...]
    mark_descriptions: tuple[str, ...]

    @property
    def text(self) -> str:
        return self.base + "".join(self.marks)

    def human_line(self) -> str:
        if not self.mark_descriptions:
            return self.name
        return f"{self.name} ({'; '.join(self.mark_descriptions)})"


@dataclass(frozen=True)
class WordState:
    index: int
    line: int
    text: str
    letters: tuple[LetterState, ...]


@dataclass(frozen=True)
class PageStateReport:
    words: tuple[WordState, ...]
    issues: tuple[PageStateIssue, ...]
    notices: tuple[PageStateNotice, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues


def _is_syriac_letter(char: str) -> bool:
    return unicodedata.name(char, "").startswith("SYRIAC LETTER")


def _is_mark(char: str) -> bool:
    return unicodedata.combining(char) != 0 or char == SUPERSCRIPT_ALAPH


def _mark_description(base: str, mark: str) -> str:
    if mark in VOWEL_NAMES:
        return VOWEL_NAMES[mark]
    if mark == RWAHA:
        return "rwāḥā: ō" if base == WAW else "rwāḥā codepoint on non-waw carrier"
    if mark == HBASA_ESASA_DOTTED:
        if base == YODH:
            return "ḥḇāṣā: ī"
        if base == WAW:
            return "rḇāṣā / ʾeṣāṣā: ū"
        return "ḥḇāṣā / rḇāṣā codepoint on invalid carrier"
    if mark == QUSSHAYA:
        return "qūššāyā"
    if mark == RUKKAKHA:
        return "rūkkākā"
    if mark == GENERIC_DOT_ABOVE:
        return "single point above"
    if mark == GENERIC_DOT_BELOW:
        return "single point below"
    if mark == SYAME:
        return "syāmē"
    if mark == TWO_DOTS_BELOW:
        return "two dots below"
    if mark == BREVE_BELOW:
        return "breve below"
    if mark == BETWEEN_ABOVE:
        return "single point above between this letter and the next"
    if mark == BETWEEN_BELOW:
        return "single point below between this letter and the next"
    if mark == MARHETANA_ABOVE:
        return "marheṭānā span above this letter and the next"
    if mark == MARHETANA_BELOW:
        return "two-letter spanning line below this letter and the next"
    if mark == OCCULTANS_ABOVE:
        return "one-letter line above"
    if mark == OCCULTANS_BELOW:
        return "one-letter line below"
    if mark == SUPERSCRIPT_ALAPH:
        return "superscript ʾālap̄"
    if mark in WEST_SYRIAC_VOWELS:
        return f"UNRESOLVED West Syriac vowel {unicodedata.name(mark, 'UNKNOWN')} U+{ord(mark):04X}"
    return f"UNRESOLVED {unicodedata.name(mark, 'UNKNOWN')} U+{ord(mark):04X}"


def _letter_issues(base: str, marks: tuple[str, ...], word: int, letter: int) -> list[PageStateIssue]:
    issues: list[PageStateIssue] = []

    for mark in marks:
        if mark == QUSSHAYA and base not in BGDKPT:
            issues.append(PageStateIssue("qūššāyā-invalid-carrier", "qūššāyā occurs on a non-bgdkpt carrier.", word, letter, mark))
        elif mark == RUKKAKHA and base not in BGDKPT:
            issues.append(PageStateIssue("rūkkākā-invalid-carrier", "rūkkākā occurs on a non-bgdkpt carrier.", word, letter, mark))
        elif mark == RWAHA and base != WAW:
            issues.append(PageStateIssue("rwāḥā-invalid-carrier", "rwāḥā occurs on a carrier other than waw.", word, letter, mark))
        elif mark == HBASA_ESASA_DOTTED and base not in {WAW, YODH}:
            issues.append(PageStateIssue("carrier-vowel-invalid-carrier", "U+073C occurs on a carrier other than waw or yodh.", word, letter, mark))
        elif mark in {GENERIC_DOT_ABOVE, GENERIC_DOT_BELOW} and base in BGDKPT:
            issues.append(PageStateIssue("generic-point-on-bgdkpt", "Generic single point occurs on bgdkpt; normalized carrier discipline is broken.", word, letter, mark))

    if QUSSHAYA in marks and RUKKAKHA in marks:
        issues.append(PageStateIssue("conflicting-bgdkpt-state", "The same bgdkpt letter carries both qūššāyā and rūkkākā.", word, letter, base))

    if OCCULTANS_ABOVE in marks and OCCULTANS_BELOW in marks:
        issues.append(
            PageStateIssue(
                "dual-one-letter-lines-unrepresentable",
                "The same carrier has one-letter lines both above and below; current canonical notation has no reversible representation for this state.",
                word,
                letter,
                base,
            )
        )

    if MARHETANA_ABOVE in marks and MARHETANA_BELOW in marks:
        issues.append(
            PageStateIssue(
                "dual-marhetana-spans-unrepresentable",
                "The same carrier begins spanning lines both above and below; no canonical notation is defined for this state.",
                word,
                letter,
                base,
            )
        )

    vowel_marks = [mark for mark in marks if mark in EAST_MULTI_DOT_VOWELS or mark in {RWAHA, HBASA_ESASA_DOTTED}]
    if len(vowel_marks) > 1:
        issues.append(PageStateIssue("multiple-vowels-on-carrier", "More than one East Syriac vowel page-state occurs on the same letter.", word, letter, base))

    seen: set[str] = set()
    for mark in marks:
        if mark in seen:
            issues.append(PageStateIssue("duplicate-normalized-mark", "The same normalized mark occurs more than once on one letter.", word, letter, mark))
        seen.add(mark)

    if base == "\u0716":
        issues.append(PageStateIssue("unnormalized-u0716", "U+0716 survived normalization.", word, letter, base))
    if base == "\u0724":
        issues.append(PageStateIssue("unnormalized-final-semkath", "Final semkath U+0724 survived normalization.", word, letter, base))

    return issues


def _one_letter_line_notices(word_index: int, letters: tuple[LetterState, ...]) -> list[PageStateNotice]:
    """Flag adjacent one-letter line encodings for a page check.

    Canonical normalized Syriac uses U+035E/U+035F for an actual two-letter
    span. Repeated U+0747/U+0748 therefore means separate one-letter lines in
    confirmed storage. A raw digital witness may nevertheless have used that
    repeated encoding as an approximation, so the page should still be checked.
    """

    notices: list[PageStateNotice] = []
    for index in range(len(letters) - 1):
        left = letters[index]
        right = letters[index + 1]
        for mark, side, replacement in (
            (OCCULTANS_ABOVE, "above", "U+035E"),
            (OCCULTANS_BELOW, "below", "U+035F"),
        ):
            if mark in left.marks and mark in right.marks:
                notices.append(
                    PageStateNotice(
                        "adjacent-one-letter-lines-page-check",
                        f"Adjacent one-letter lines {side}: confirmed storage means two separate lines. If the page instead shows one two-letter span, encode it with {replacement} on the first letter.",
                        word_index,
                        index + 1,
                        mark,
                    )
                )
    return notices


def inspect_normalized_text(text: str) -> PageStateReport:
    """Return every Syriac word as normalized letter+mark page-states."""

    words: list[WordState] = []
    issues: list[PageStateIssue] = []
    notices: list[PageStateNotice] = []
    current: list[LetterState] = []
    current_line = 1
    line = 1
    i = 0

    def flush() -> None:
        nonlocal current, current_line
        if not current:
            return
        word_index = len(words) + 1
        word_text = "".join(letter.text for letter in current)
        letter_tuple = tuple(current)
        words.append(WordState(word_index, current_line, word_text, letter_tuple))
        for letter_index, letter_state in enumerate(letter_tuple, start=1):
            issues.extend(_letter_issues(letter_state.base, letter_state.marks, word_index, letter_index))
            if letter_index == len(letter_tuple):
                if BETWEEN_ABOVE in letter_state.marks or BETWEEN_BELOW in letter_state.marks:
                    mark = BETWEEN_BELOW if BETWEEN_BELOW in letter_state.marks else BETWEEN_ABOVE
                    issues.append(
                        PageStateIssue(
                            "between-point-without-next-letter",
                            "A between-letter point occurs on the final letter of the word, so there is no following letter for the page-state to stand between.",
                            word_index,
                            letter_index,
                            mark,
                        )
                    )
                if MARHETANA_ABOVE in letter_state.marks or MARHETANA_BELOW in letter_state.marks:
                    mark = MARHETANA_BELOW if MARHETANA_BELOW in letter_state.marks else MARHETANA_ABOVE
                    issues.append(
                        PageStateIssue(
                            "marhetana-without-next-letter",
                            "A two-letter spanning line begins on the final letter of the word, so there is no following letter for it to span.",
                            word_index,
                            letter_index,
                            mark,
                        )
                    )

        # Two consecutive starts in the same direction would overlap on the
        # middle letter. Keep that state blocking until a real page requires it.
        for index in range(len(letter_tuple) - 1):
            left = letter_tuple[index]
            right = letter_tuple[index + 1]
            for mark, side in (
                (MARHETANA_ABOVE, "above"),
                (MARHETANA_BELOW, "below"),
            ):
                if mark in left.marks and mark in right.marks:
                    issues.append(
                        PageStateIssue(
                            "overlapping-marhetana-spans",
                            f"Two {side} spans would overlap on the middle letter; no canonical interpretation is defined for this state.",
                            word_index,
                            index + 2,
                            mark,
                        )
                    )

        notices.extend(_one_letter_line_notices(word_index, letter_tuple))
        current = []

    while i < len(text):
        char = text[i]
        if _is_syriac_letter(char):
            if not current:
                current_line = line
            marks: list[str] = []
            j = i + 1
            while j < len(text) and _is_mark(text[j]):
                marks.append(text[j])
                j += 1
            current.append(
                LetterState(
                    base=char,
                    name=LETTER_NAMES.get(char, unicodedata.name(char, "UNKNOWN")),
                    marks=tuple(marks),
                    mark_descriptions=tuple(_mark_description(char, mark) for mark in marks),
                )
            )
            i = j
            continue

        if char in "[]":
            i += 1
            continue

        flush()
        if char == "\n":
            line += 1
        i += 1

    flush()
    return PageStateReport(tuple(words), tuple(issues), tuple(notices))


def format_page_state_report(text: str, word_labels: Sequence[str] | None = None) -> str:
    """Format the page-state audit for a human checking against a source page."""

    report = inspect_normalized_text(text)
    if word_labels is not None and len(word_labels) != len(report.words):
        raise ValueError("word_labels must contain exactly one label per Syriac word")

    lines: list[str] = []
    for word in report.words:
        if word_labels is None:
            header = word.text
        else:
            header = f"*{word_labels[word.index - 1]}*"
        lines.append(f"Word {word.index}: {header}")
        lines.extend(letter.human_line() for letter in word.letters)
        lines.append("")

    if lines:
        lines.pop()
    return "\n".join(lines)
