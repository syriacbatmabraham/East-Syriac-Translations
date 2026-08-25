"""Inverse parser for canonical East Syriac transliteration."""
from __future__ import annotations

from dataclasses import dataclass
import unicodedata

from .normalization import (
    BGDKPT, WAW, YODH, SUPERSCRIPT_ALAPH, SYAME, QUSSHAYA, RUKKAKHA,
    RWAHA, HBASA_ESASA_DOTTED, GENERIC_DOT_ABOVE, GENERIC_DOT_BELOW,
    TWO_DOTS_BELOW, BREVE_BELOW, BETWEEN_ABOVE, BETWEEN_BELOW,
    MARHETANA_ABOVE, MARHETANA_BELOW,
    OCCULTANS_ABOVE, OCCULTANS_BELOW, normalize_text,
)
from .transliteration import (
    ALAPH, PTHAHA, ZQAPHA, ZLAMA_PSHIQA, ZLAMA_QASHYA, Direction,
    MARHETANA_TIE_ABOVE, MARHETANA_TIE_BELOW,
    ReverseTransliterationResult,
    TransliterationError, CONSONANT, BGDKPT_BARE, BGDKPT_HARD,
    BGDKPT_SOFT, CLASS_B, EXCEPTION_VOWEL, transliterate_text, _ParsedToken,
)


@dataclass(frozen=True)
class _UnitSpec:
    latin: str
    base: str
    marks: tuple[str,...]
    vowel_token: str | None


def _base_variants():
    out=[]
    for b,s in CONSONANT.items(): out.append((s,b,()))
    for b,s in BGDKPT_BARE.items(): out.append((s,b,()))
    for b,s in BGDKPT_HARD.items(): out.append((s,b,(QUSSHAYA,)))
    for b,s in BGDKPT_SOFT.items(): out.append((s,b,(RUKKAKHA,)))
    out += [("ō",WAW,(RWAHA,)),("ū",WAW,(HBASA_ESASA_DOTTED,)),("ī",YODH,(HBASA_ESASA_DOTTED,))]
    return out


def _allowed_on_marks(base: str, intrinsic: tuple[str,...]) -> list[tuple[str,tuple[str,...]]]:
    # §7 point identity is direct. U+0307/U+0323 remain generic points on
    # every carrier; they are not converted into bgdkpt or Class-A states.
    return [
        ("",()),("_",(GENERIC_DOT_BELOW,)),("^",(GENERIC_DOT_ABOVE,)),
        ("_^",(GENERIC_DOT_BELOW,GENERIC_DOT_ABOVE)),
    ]


def _ordered_class_b_sequences(max_length: int) -> tuple[tuple[str,...], ...]:
    # §5.1 gives every same-CCC vowel an explicit rank. Generate only that
    # canonical order; raw source permutations converge during normalization.
    below = (
        (),
        (ZLAMA_PSHIQA,),
        (ZLAMA_QASHYA,),
        (ZLAMA_PSHIQA, ZLAMA_QASHYA),
    )
    above = (
        (),
        (PTHAHA,),
        (ZQAPHA,),
        (PTHAHA, ZQAPHA),
    )
    return tuple(
        lower + upper
        for lower in below
        for upper in above
        if len(lower) + len(upper) <= max_length
    )


def _vowel_options(max_length: int) -> tuple[tuple[str,tuple[str,...],str | None], ...]:
    options: list[tuple[str,tuple[str,...],str | None]] = []
    for marks in _ordered_class_b_sequences(max_length):
        if not marks:
            options.append(("", (), None))
            continue
        parts=[CLASS_B[mark] for mark in marks]
        normal="".join(parts)
        options.append((normal, marks, normal))
        eligible=[index for index,mark in enumerate(marks) if mark in EXCEPTION_VOWEL]
        if eligible:
            index=eligible[-1]
            exception_parts=parts.copy()
            exception_parts[index]=EXCEPTION_VOWEL[marks[index]]
            exception="".join(exception_parts)
            options.append((exception, marks, exception))
    return tuple(options)


def _build_unit_reverse() -> dict[str,_UnitSpec]:
    reverse: dict[str,_UnitSpec]={}
    visual_options=[
        ("",()),("\u0324",(TWO_DOTS_BELOW,)),("\u032e",(BREVE_BELOW,)),("\u0308",(SYAME,)),
        ("\u0324\u032e",(TWO_DOTS_BELOW,BREVE_BELOW)),
        ("\u0324\u0308",(TWO_DOTS_BELOW,SYAME)),
        ("\u032e\u0308",(BREVE_BELOW,SYAME)),
        ("\u0324\u032e\u0308",(TWO_DOTS_BELOW,BREVE_BELOW,SYAME)),
    ]
    between_options=[("",()),("__",(BETWEEN_BELOW,)),("^^",(BETWEEN_ABOVE,)),("__^^",(BETWEEN_BELOW,BETWEEN_ABOVE))]
    for base_lat,base,intrinsic in _base_variants():
        carrier_vowel=RWAHA in intrinsic or HBASA_ESASA_DOTTED in intrinsic
        vowels=_vowel_options(1 if carrier_vowel else 2)
        for vis_lat,vis_marks in visual_options:
            decorated=unicodedata.normalize("NFC",base_lat+vis_lat)
            for on_lat,on_marks in _allowed_on_marks(base,intrinsic):
                for vowel_lat,vowel_marks,vowel_token in vowels:
                    for between_lat,between_marks in between_options:
                        if vowel_token is not None and any(ch in vowel_token for ch in "ăĕ") and between_marks:
                            continue
                        for prefix,prefix_marks in (("",()),("ᵃ",(SUPERSCRIPT_ALAPH,))):
                            latin=unicodedata.normalize("NFC",prefix+decorated+on_lat+vowel_lat+between_lat)
                            marks=prefix_marks+intrinsic+vis_marks+on_marks+vowel_marks+between_marks
                            spec=_UnitSpec(latin,base,marks,vowel_token)
                            old=reverse.get(latin)
                            if old is not None and old!=spec:
                                raise RuntimeError(f"Canonical unit collision: {latin!r}: {old!r} vs {spec!r}")
                            reverse[latin]=spec
    return reverse


UNIT_REVERSE = _build_unit_reverse()
UNIT_KEYS_BY_FIRST: dict[str, tuple[str, ...]] = {}
for _key in UNIT_REVERSE:
    UNIT_KEYS_BY_FIRST.setdefault(_key[0], [])
    UNIT_KEYS_BY_FIRST[_key[0]].append(_key)
UNIT_KEYS_BY_FIRST = {
    first: tuple(keys)
    for first, keys in UNIT_KEYS_BY_FIRST.items()
}
UNIT_MAX_KEY_LENGTH_BY_FIRST = {
    first: max(len(key) for key in keys)
    for first, keys in UNIT_KEYS_BY_FIRST.items()
}


def _parse_unit(s: str, pos: int) -> tuple[_UnitSpec, int]:
    if pos >= len(s):
        raise TransliterationError("invalid-canonical-unit", "Expected a canonical transliteration unit at end of input.")
    first=s[pos]
    max_length=UNIT_MAX_KEY_LENGTH_BY_FIRST.get(first)
    if max_length is None:
        raise TransliterationError("invalid-canonical-unit", f"No canonical transliteration unit begins at position {pos}.")
    end_max=min(len(s), pos + max_length)
    for end in range(end_max, pos, -1):
        spec=UNIT_REVERSE.get(s[pos:end])
        if spec is not None:
            return spec, end
    raise TransliterationError("invalid-canonical-unit", f"No canonical transliteration unit begins at position {pos}.")


def _find_close(s: str, pos: int) -> int:
    depth = 0
    for i in range(pos, len(s)):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    raise TransliterationError("unclosed-parenthesis", "Canonical transliteration contains an unclosed parenthesis.")


def parse_reserved_line_payload(content: str) -> tuple[Direction, list[_UnitSpec]] | None:
    """Parse parenthetical text that collides with one-/legacy-two-unit line syntax.

    One parsed unit is the live one-letter line notation. Two parsed units are
    reserved solely so the inverse can reject the retired spanning-parentheses
    spelling with a useful migration error rather than misreading it as literal
    editorial apparatus.
    """

    direction: Direction = "above"
    inner = content
    if inner.startswith("_"):
        direction = "below"
        inner = inner[1:]
    if not inner or "(" in inner or ")" in inner or "[" in inner or "]" in inner:
        return None
    specs: list[_UnitSpec] = []
    p = 0
    try:
        while p < len(inner):
            spec, p2 = _parse_unit(inner, p)
            specs.append(spec)
            p = p2
            if len(specs) > 2:
                return None
    except TransliterationError:
        return None
    return (direction, specs) if specs and p == len(inner) else None


def parse_occultans_payload(content: str) -> tuple[Direction, list[_UnitSpec]] | None:
    """Compatibility helper: only the live one-letter wrapper is occultans syntax."""
    parsed = parse_reserved_line_payload(content)
    if parsed is None:
        return None
    direction, specs = parsed
    return (direction, specs) if len(specs) == 1 else None


def _consume_marhetana(text: str, pos: int, token: _ParsedToken) -> int:
    if pos >= len(text):
        return pos
    ch = text[pos]
    if ch == MARHETANA_TIE_ABOVE:
        token.marhetana = "above"
    elif ch == MARHETANA_TIE_BELOW:
        token.marhetana = "below"
    else:
        return pos
    pos += 1
    if pos < len(text) and text[pos] in {MARHETANA_TIE_ABOVE, MARHETANA_TIE_BELOW}:
        raise TransliterationError(
            "dual-marhetana-ties",
            "A carrier cannot begin both an upper and lower spanning line in the current canonical grammar.",
        )
    return pos


def _parse_canonical(text:str)->list[_ParsedToken]:
    toks=[]; i=0; group=0; bracket_depth=0
    while i<len(text):
        ch=text[i]
        if ch in " \t\n\r":
            toks.append(_ParsedToken("literal",ch,bracket_depth=bracket_depth)); i+=1; continue
        if ch=="[":
            toks.append(_ParsedToken("literal",ch,bracket_depth=bracket_depth)); bracket_depth+=1; i+=1; continue
        if ch=="]":
            bracket_depth=max(0,bracket_depth-1); toks.append(_ParsedToken("literal",ch,bracket_depth=bracket_depth)); i+=1; continue
        if ch=="(":
            end=_find_close(text,i); content=text[i+1:end]
            reserved = parse_reserved_line_payload(content)
            if reserved is None:
                toks.append(_ParsedToken("editorial",text[i:end+1],bracket_depth=bracket_depth)); i=end+1; continue
            direction, specs = reserved
            if len(specs) == 2:
                replacement = "x⁀y" if direction == "above" else "x‿y"
                raise TransliterationError(
                    "legacy-two-letter-line-wrapper",
                    f"Two-letter parenthetical line wrappers are retired; encode the Syriac span with U+035E/U+035F and use tie notation like {replacement}.",
                )
            group+=1
            spec=specs[0]
            token=_ParsedToken(
                "letter",
                spec.latin,
                spec.base,
                spec.marks,
                bracket_depth=bracket_depth,
                occultans=direction,
                occultans_group=group,
                vowel_token=spec.vowel_token,
            )
            toks.append(token)
            i=_consume_marhetana(text,end+1,token)
            continue
        spec,j=_parse_unit(text,i)
        token=_ParsedToken("letter",spec.latin,spec.base,spec.marks,bracket_depth=bracket_depth,vowel_token=spec.vowel_token)
        toks.append(token)
        i=_consume_marhetana(text,j,token)
    return toks


def _assign_words(toks:list[_ParsedToken])->None:
    word=0; current=None; letter=0
    for t in toks:
        if t.kind=="letter":
            if current is None:
                word+=1; current=word; letter=0
            letter+=1; t.word=current; t.letter=letter
        elif t.kind=="literal" and t.text in "[]":
            continue
        else:
            current=None; letter=0


def _validate_marhetana_tokens(toks: list[_ParsedToken]) -> None:
    for index, token in enumerate(toks):
        if token.kind != "letter" or token.marhetana is None:
            continue
        if index + 1 >= len(toks) or toks[index + 1].kind != "letter":
            raise TransliterationError(
                "marhetana-without-adjacent-next-letter",
                "A marheṭānā tie must join directly to the immediately following canonical letter unit; it cannot end a word or cross editorial material.",
            )
        nxt=toks[index+1]
        if token.word is None or nxt.word != token.word:
            raise TransliterationError(
                "marhetana-crosses-word-boundary",
                "A marheṭānā tie cannot cross a word boundary.",
            )
        if nxt.marhetana == token.marhetana:
            raise TransliterationError(
                "overlapping-marhetana-spans",
                "Consecutive same-direction marheṭānā spans would overlap on the middle letter; that state is not canonical.",
            )


def reverse_transliterate(text: str) -> ReverseTransliterationResult:
    """Reverse a canonical transliteration into normalized Syriac exactly."""
    if unicodedata.normalize("NFC",text)!=text:
        raise TransliterationError("canonical-not-nfc","Canonical transliteration must be NFC normalized.")
    toks=_parse_canonical(text)
    _assign_words(toks)
    _validate_marhetana_tokens(toks)

    letters_by_word:dict[int,list[int]]={}
    for idx,t in enumerate(toks):
        if t.kind=="letter" and t.word is not None:
            letters_by_word.setdefault(t.word,[]).append(idx)

    # Validate exception-vowel position and insert conventionally implied bare alaph.
    insert_after:set[int]=set()
    for word,inds in letters_by_word.items():
        last=inds[-1]
        for idx in inds:
            vt=toks[idx].vowel_token or ""
            if any(ch in vt for ch in "ăĕ") and idx!=last:
                raise TransliterationError("final-vowel-exception-not-final",f"{vt} contains a final-vowel exception but is not on the final orthographic letter of a word.")
        last_vowels=toks[last].vowel_token or ""
        if not any(ch in last_vowels for ch in "ăĕ") and any(ch in last_vowels for ch in "āē"):
            insert_after.add(last)

    # Reconstruct source tokens. Span/separate grouping is now in the Syriac
    # codepoints themselves, so there is no page-resolution metadata to recover.
    out=[]
    for idx,t in enumerate(toks):
        if t.kind in {"literal","editorial"}:
            out.append(t.text); continue
        assert t.base is not None
        marks=list(t.marks)
        if t.occultans=="above": marks.append(OCCULTANS_ABOVE)
        elif t.occultans=="below": marks.append(OCCULTANS_BELOW)
        if t.marhetana=="above": marks.append(MARHETANA_ABOVE)
        elif t.marhetana=="below": marks.append(MARHETANA_BELOW)
        out.append(t.base+"".join(marks))
        if idx in insert_after:
            out.append(ALAPH)

    syriac_raw="".join(out)
    norm=normalize_text(syriac_raw)
    if norm.flags:
        raise TransliterationError("inverse-produced-invalid-source","Canonical string reverses to a source state rejected by normalization.")
    syriac=norm.text

    # Canonicality check: only accept strings that the forward engine itself
    # emits for the reconstructed normalized Syriac.
    regenerated=transliterate_text(syriac).text
    if regenerated!=text:
        raise TransliterationError("noncanonical-transliteration",f"Input is parseable but not canonical; canonical form is {regenerated!r}.")
    return ReverseTransliterationResult(syriac)