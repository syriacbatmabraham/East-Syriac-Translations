"""Forward reversible canonical East Syriac transliteration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
import unicodedata

from .normalization import (
    PROJECT_LETTERS, BGDKPT, WAW, YODH, SUPERSCRIPT_ALAPH, SYAME,
    QUSSHAYA, RUKKAKHA, RWAHA, HBASA_ESASA_DOTTED,
    GENERIC_DOT_ABOVE, GENERIC_DOT_BELOW, TWO_DOTS_BELOW, BREVE_BELOW,
    BETWEEN_ABOVE, BETWEEN_BELOW, MARHETANA_ABOVE, MARHETANA_BELOW,
    OCCULTANS_ABOVE, OCCULTANS_BELOW, normalize_text,
)
from .inspection import inspect_normalized_text

ALAPH = "\u0710"
PTHAHA = "\u0732"
ZQAPHA = "\u0735"
ZLAMA_PSHIQA = "\u0738"
ZLAMA_QASHYA = "\u0739"

MARHETANA_TIE_ABOVE = "\u2040"  # CHARACTER TIE
MARHETANA_TIE_BELOW = "\u203f"  # UNDERTIE

Direction = Literal["above", "below"]


class TransliterationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class TransliterationResult:
    text: str
    word_labels: tuple[str, ...]


@dataclass(frozen=True)
class ReverseTransliterationResult:
    text: str


@dataclass
class _SourceToken:
    kind: str
    text: str
    base: str | None = None
    marks: tuple[str, ...] = ()
    word: int | None = None
    letter: int | None = None
    bracket_depth: int = 0
    suppressed: bool = False
    core: str = ""


@dataclass
class _ParsedToken:
    kind: str
    text: str
    base: str | None = None
    marks: tuple[str, ...] = ()
    word: int | None = None
    letter: int | None = None
    bracket_depth: int = 0
    occultans: Direction | None = None
    occultans_group: int | None = None
    marhetana: Direction | None = None
    vowel_token: str | None = None


CONSONANT = {
    "\u0710": "ʾ", "\u0717": "h", "\u0718": "w", "\u0719": "z",
    "\u071a": "ḥ", "\u071b": "ṭ", "\u071d": "y", "\u0720": "l",
    "\u0721": "m", "\u0722": "n", "\u0723": "s", "\u0725": "ʿ",
    "\u0728": "ṣ", "\u0729": "q", "\u072a": "r", "\u072b": "š",
}
BGDKPT_BARE = {"\u0712":"b","\u0713":"g","\u0715":"d","\u071f":"k","\u0726":"p","\u072c":"t"}
BGDKPT_HARD = {"\u0712":"ḃ","\u0713":"ġ","\u0715":"ḋ","\u071f":"k̇","\u0726":"ṗ","\u072c":"ṫ"}
BGDKPT_SOFT = {"\u0712":"ḇ","\u0713":"ḡ","\u0715":"ḏ","\u071f":"ḵ","\u0726":"p̄","\u072c":"ṯ"}
CLASS_B = {PTHAHA:"a", ZQAPHA:"ā", ZLAMA_PSHIQA:"e", ZLAMA_QASHYA:"ē"}
EXCEPTION_VOWEL = {ZQAPHA:"ă", ZLAMA_QASHYA:"ĕ"}
VISUAL_MARK_TO_LATIN = {TWO_DOTS_BELOW:"\u0324", BREVE_BELOW:"\u032e", SYAME:"\u0308"}


def _is_syriac_letter(ch: str) -> bool:
    return ch in PROJECT_LETTERS


def _is_mark(ch: str) -> bool:
    return unicodedata.combining(ch) != 0 or ch == SUPERSCRIPT_ALAPH


def _parse_source(text: str) -> list[_SourceToken]:
    tokens: list[_SourceToken] = []
    i = 0
    word = 0
    current_word: int | None = None
    letter_in_word = 0
    bracket_depth = 0
    while i < len(text):
        ch = text[i]
        if _is_syriac_letter(ch):
            if current_word is None:
                word += 1
                current_word = word
                letter_in_word = 0
            letter_in_word += 1
            marks=[]
            j=i+1
            while j < len(text) and _is_mark(text[j]):
                marks.append(text[j]); j+=1
            tokens.append(_SourceToken("letter", text[i:j], ch, tuple(marks), current_word, letter_in_word, bracket_depth))
            i=j
            continue
        if ch == "[":
            tokens.append(_SourceToken("literal", ch, word=current_word, bracket_depth=bracket_depth))
            bracket_depth += 1
            i += 1
            continue
        if ch == "]":
            bracket_depth = max(0, bracket_depth-1)
            tokens.append(_SourceToken("literal", ch, word=current_word, bracket_depth=bracket_depth))
            i += 1
            continue
        tokens.append(_SourceToken("literal", ch, bracket_depth=bracket_depth))
        current_word = None
        letter_in_word = 0
        i += 1
    return tokens


def _validate_forward_input(text: str) -> None:
    norm = normalize_text(text)
    if norm.text != text or norm.flags:
        raise TransliterationError("input-not-normalized", "Forward transliteration requires clean normalized Syriac input.")
    audit = inspect_normalized_text(text)
    blocking = [issue for issue in audit.issues if issue.code != "multiple-vowels-on-carrier"]
    if blocking:
        raise TransliterationError("invalid-page-state", "Forward transliteration refuses contradictory normalized page-states.")


def _letter_base_symbol(base: str, marks: set[str]) -> tuple[str, set[str], bool]:
    remaining=set(marks)
    carrier_vowel=False
    if base in BGDKPT:
        if QUSSHAYA in remaining:
            symbol=BGDKPT_HARD[base]; remaining.remove(QUSSHAYA)
        elif RUKKAKHA in remaining:
            symbol=BGDKPT_SOFT[base]; remaining.remove(RUKKAKHA)
        else:
            symbol=BGDKPT_BARE[base]
    elif base == WAW and RWAHA in remaining:
        symbol="ō"; remaining.remove(RWAHA); carrier_vowel=True
    elif base == WAW and HBASA_ESASA_DOTTED in remaining:
        symbol="ū"; remaining.remove(HBASA_ESASA_DOTTED); carrier_vowel=True
    elif base == YODH and HBASA_ESASA_DOTTED in remaining:
        symbol="ī"; remaining.remove(HBASA_ESASA_DOTTED); carrier_vowel=True
    else:
        symbol=CONSONANT.get(base) or BGDKPT_BARE.get(base)
    if symbol is None:
        raise TransliterationError("unsupported-letter", f"Unsupported normalized Syriac letter U+{ord(base):04X}.")
    return symbol, remaining, carrier_vowel


def _render_core(tok: _SourceToken, final_letter: bool, has_suppressed_mater: bool) -> str:
    marks=set(tok.marks)
    if OCCULTANS_ABOVE in marks and OCCULTANS_BELOW in marks:
        raise TransliterationError("dual-one-letter-lines", "A carrier with one-letter lines both above and below has no canonical notation.")
    if MARHETANA_ABOVE in marks and MARHETANA_BELOW in marks:
        raise TransliterationError("dual-marhetana", "A carrier beginning spans both above and below has no canonical notation.")
    if tok.base == WAW and RWAHA in marks and HBASA_ESASA_DOTTED in marks:
        raise TransliterationError(
            "conflicting-carrier-vowels",
            "Waw cannot carry both Class-A carrier-vowel states in the current canonical notation.",
        )
    prefix = "ᵃ" if SUPERSCRIPT_ALAPH in marks else ""
    marks.discard(SUPERSCRIPT_ALAPH)
    marks.discard(OCCULTANS_ABOVE); marks.discard(OCCULTANS_BELOW)
    marks.discard(MARHETANA_ABOVE); marks.discard(MARHETANA_BELOW)
    symbol, remaining, carrier_vowel = _letter_base_symbol(tok.base or "", marks)

    visuals=[]
    for m in (TWO_DOTS_BELOW, BREVE_BELOW, SYAME):
        if m in remaining:
            visuals.append(VISUAL_MARK_TO_LATIN[m]); remaining.remove(m)
    decorated=unicodedata.normalize("NFC", symbol+"".join(visuals))

    on=""
    if GENERIC_DOT_BELOW in remaining:
        on += "_"; remaining.remove(GENERIC_DOT_BELOW)
    if GENERIC_DOT_ABOVE in remaining:
        on += "^"; remaining.remove(GENERIC_DOT_ABOVE)

    found=[m for m in tok.marks if m in CLASS_B and m in remaining]
    total_vowels = len(found) + (1 if carrier_vowel else 0)
    if total_vowels > 2:
        raise TransliterationError(
            "too-many-vowels-on-carrier",
            "More than two distinct vowel page-states occur on one carrier; no attested canonical rule covers that state.",
        )
    for m in found:
        remaining.remove(m)
    vowel_parts=[CLASS_B[m] for m in found]
    if final_letter and not has_suppressed_mater:
        eligible=[i for i,m in enumerate(found) if m in EXCEPTION_VOWEL]
        if eligible:
            i=eligible[-1]
            vowel_parts[i]=EXCEPTION_VOWEL[found[i]]
    vowel="".join(vowel_parts)

    between=""
    if BETWEEN_BELOW in remaining:
        between += "__"; remaining.remove(BETWEEN_BELOW)
    if BETWEEN_ABOVE in remaining:
        between += "^^"; remaining.remove(BETWEEN_ABOVE)

    if remaining:
        cp=next(iter(remaining))
        raise TransliterationError("unsupported-mark", f"Normalized mark U+{ord(cp):04X} has no canonical transliteration.")
    return unicodedata.normalize("NFC", prefix+decorated+on+vowel+between)


def _matching_parenthesis(text: str, start: int) -> int:
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    raise TransliterationError("unclosed-parenthesis", "Normalized input contains an unclosed editorial parenthesis.")


def _validate_source_parentheses(text: str) -> None:
    from .transliteration_inverse import parse_reserved_line_payload
    i = 0
    while i < len(text):
        if text[i] != "(":
            i += 1
            continue
        end = _matching_parenthesis(text, i)
        content = text[i + 1:end]
        if parse_reserved_line_payload(content) is not None:
            raise TransliterationError(
                "ambiguous-editorial-parenthesis",
                f"Editorial apparatus {text[i:end+1]!r} is indistinguishable from reserved line-mark syntax; disambiguate the label.",
            )
        i = end + 1


def _validate_marhetana_adjacency(tokens: list[_SourceToken], letters_by_word: dict[int, list[int]]) -> None:
    for word, inds in letters_by_word.items():
        for pos, index in enumerate(inds):
            tok = tokens[index]
            marks = set(tok.marks)
            span_marks = marks & {MARHETANA_ABOVE, MARHETANA_BELOW}
            if not span_marks:
                continue
            if pos == len(inds) - 1:
                raise TransliterationError(
                    "marhetana-without-next-letter",
                    f"Word {word}, letter {tok.letter} begins a two-letter span but has no following letter.",
                )
            next_index = inds[pos + 1]
            if next_index != index + 1:
                raise TransliterationError(
                    "marhetana-crosses-editorial-boundary",
                    f"Word {word}, letter {tok.letter} begins a two-letter span across editorial material; canonical notation does not permit that state.",
                )


def transliterate_text(text: str) -> TransliterationResult:
    """Transliterate clean normalized Syriac to the canonical reversible string."""
    _validate_forward_input(text)
    _validate_source_parentheses(text)

    tokens=_parse_source(text)
    letters_by_word: dict[int,list[int]]={}
    for idx,t in enumerate(tokens):
        if t.kind=="letter" and t.word is not None:
            letters_by_word.setdefault(t.word,[]).append(idx)

    _validate_marhetana_adjacency(tokens, letters_by_word)

    # Final mater convention: suppress only a bare final alaph that is literally
    # adjacent to its vowel-bearing carrier and is not the second base of a
    # marheṭānā/double-diacritic span.
    suppressed_by_prev: set[int]=set()
    for word, inds in letters_by_word.items():
        if len(inds) < 2:
            continue
        last=tokens[inds[-1]]
        prev=tokens[inds[-2]]
        if (
            last.base == ALAPH
            and not last.marks
            and inds[-1] == inds[-2] + 1
            and not ({MARHETANA_ABOVE, MARHETANA_BELOW} & set(prev.marks))
            and (ZQAPHA in prev.marks or ZLAMA_QASHYA in prev.marks)
        ):
            last.suppressed = True
            suppressed_by_prev.add(inds[-2])

    for word, inds in letters_by_word.items():
        visible=[i for i in inds if not tokens[i].suppressed]
        last_visible=visible[-1] if visible else None
        for i in inds:
            t=tokens[i]
            if t.suppressed:
                continue
            t.core=_render_core(t, i==last_visible, i in suppressed_by_prev)

    out=[]
    word_label_parts: dict[int,list[str]]={w:[] for w in letters_by_word}
    active_word: int | None = None
    i=0
    while i < len(tokens):
        t=tokens[i]
        if t.kind=="literal":
            out.append(t.text)
            # Square editorial brackets are transparent to word division and
            # therefore belong in the canonical word label when they occur
            # inside/around that word. Other literals terminate a word.
            if t.text in "[]":
                candidate = t.word if t.word is not None else active_word
                if candidate is None:
                    j=i+1
                    while j < len(tokens) and tokens[j].kind=="literal" and tokens[j].text in "[]":
                        j+=1
                    if j < len(tokens) and tokens[j].kind=="letter":
                        candidate=tokens[j].word
                if candidate is not None:
                    word_label_parts[candidate].append(t.text)
                    active_word=candidate
            else:
                active_word=None
            i+=1
            continue

        if t.suppressed:
            active_word=t.word
            i+=1
            continue

        direction=None
        if OCCULTANS_ABOVE in t.marks:
            direction="above"
        if OCCULTANS_BELOW in t.marks:
            direction="below"

        rendered=t.core
        if direction:
            rendered=f"({'_' if direction=='below' else ''}{rendered})"

        if MARHETANA_ABOVE in t.marks:
            rendered += MARHETANA_TIE_ABOVE
        elif MARHETANA_BELOW in t.marks:
            rendered += MARHETANA_TIE_BELOW

        out.append(rendered)
        if t.word is not None:
            word_label_parts[t.word].append(rendered)
            active_word=t.word
        i+=1

    labels=tuple("".join(word_label_parts[w]) for w in sorted(word_label_parts))
    return TransliterationResult(unicodedata.normalize("NFC","".join(out)), labels)


def round_trip(text: str) -> bool:
    from .transliteration_inverse import reverse_transliterate
    forward = transliterate_text(text)
    return reverse_transliterate(forward.text).text == text
