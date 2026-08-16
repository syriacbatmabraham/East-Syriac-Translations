# Final normalization torture corpus

This corpus is deliberately synthetic. None of the strings need to be lexical Syriac. The goal is **complete input/state coverage**, not one fake word per rule.

## Coverage contract

The normalization torture test is complete when all of the following are true:

1. Every assigned codepoint in the core Syriac block **U+0700–U+074F** has an explicit expected disposition: pass, normalize, remove, refuse/flag, or unsupported-letter/mark flag.
2. Every extra generic codepoint named by the rules is exercised: U+0307, U+0323, U+0308, U+0324, U+032E, **U+035E, U+035F**, U+1DF8, U+1DFA, U+0640, U+200C, U+200D, and U+FEFF.
3. Every carrier-sensitive single-point alias is tested on every carrier class that changes its meaning.
4. Every canonical page-state has at least one legal example.
5. Every known impossible, contradictory, or presently unrepresentable normalized state has an explicit negative example.
6. Editorial apparatus and word-boundary behavior are exercised.
7. Any arbitrary non-combining codepoint outside the licensed source grammar is retained **and flagged**, never silently admitted.
8. Adjacent U+0747/U+0748 one-letter marks are surfaced as a page check at ingestion because a raw digital witness may have used repetition to approximate a printed span; canonical confirmed storage itself distinguishes the two states directly.

`tools/tests/test_normalization_coverage.py` freezes the Unicode/source boundary programmatically. Focused normalization tests and the transliteration boundary tests remain as permanent regressions.

---

## T1 — consonant and bgdkpt sweep

One synthetic run contains the complete canonical consonant inventory:

`ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ`

All six bgdkpt letters are cycled through unmarked, qūššāyā, and rūkkākā. Input-only forms are exercised separately:

- U+0724 FINAL SEMKATH → U+0723 SEMKATH;
- U+0716 + syāmē → resh without a flag;
- bare U+0716 → resh with `bare-u0716`.

## T2 — complete single-point matrix

Each source encoding for a point above (U+0741, U+073F, U+0307) and below (U+0742, U+073C, U+0323) is placed on every carrier class whose interpretation differs:

- bgdkpt;
- waw;
- yodh;
- ordinary non-bgdkpt consonant.

All six bgdkpt letters are also checked explicitly so carrier-set mistakes cannot hide behind one beth example.

## T3 — dense legal page-state combinations

Synthetic carriers combine the legal marks rather than isolating each one in a fake word. Coverage includes:

- pṯāḥā, zqāpā, zlāmā pšīqā, zlāmā qašyā;
- waw `ō`, waw `ū`, yodh `ī`;
- syāmē;
- superscript ʾālap̄;
- generic point above/below;
- between-letter point above/below;
- all three two-dots-below encodings;
- breve below;
- one-letter lines above/below (U+0747/U+0748);
- direct two-letter spans above/below (U+035E/U+035F);
- hostile mark order across CCC 36/220/230/233/234.

Expected output always satisfies Transliteration Rules §5.1 and NFC.

## T4 — positional/mater pass-through

Normalization deliberately does **not** infer final matres. Small boundary tokens therefore cover:

- final zqāpā without written ʾālap̄;
- final zqāpā + written ʾālap̄;
- final zlāmā qašyā without written ʾālap̄;
- final zlāmā qašyā + written ʾālap̄;
- zlāmā qašyā + yodh;
- a final written ʾālap̄ serving as the second base of a U+035E/U+035F span, which must remain explicit in later transliteration.

The page-state report shows only what is literally encoded. The later transliteration layer applies `ā/ă` and `ē/ĕ` only where the span rule does not require the second base to remain visible.

## T5 — editorial apparatus, word division, and removable debris

Structural tests combine:

- parenthesized labels such as `(Witness A: 2)`;
- `ܐ[ܒ]ܐ`, with square brackets transparent to word division;
- spaces and line breaks;
- every Syriac punctuation codepoint U+0700–U+070D;
- U+070F abbreviation mark;
- Latin punctuation substitutes `. , : ;`;
- tatweel U+0640;
- ZWNJ U+200C and ZWJ U+200D;
- U+0749 MUSIC and U+074A BARREKH.

Malformed apparatus remains separate so each diagnosis is exact: unclosed/opening or unmatched closing parentheses/brackets.

## T6 — refusal and unknown sweep

Every West Syriac vowel (U+0730, 0731, 0733, 0734, 0736, 0737, 073A, 073B, 073D, 073E) is retained and refused, never mapped.

Every assigned Syriac-block letter outside the project inventory is retained and flagged, including Garshuni, Persian, and Sogdian letters. Unsupported Syriac marks U+0743, U+0745, and U+0746 are retained and flagged.

The catch-all is tested with unassigned U+074B/U+074C, Greek and Cyrillic homoglyphs, and emoji. Latin letters/digits outside parenthesized apparatus retain the more specific whole-file safety flag.

## T7 — malformed clusters and impossible normalized states

Source-level negative cases include orphan marks, duplicate point aliases, and BOM.

The post-normalization invariant checker is also attacked directly so later code cannot manufacture an invalid state behind the normalizer. It must reject or flag:

- qūššāyā + rūkkākā on one bgdkpt carrier;
- multiple East Syriac vowels on one carrier;
- waw carrying both `ō` and `ū`;
- duplicate normalized marks;
- qūššāyā/rūkkākā on invalid carriers;
- U+073C on an invalid carrier;
- **one-letter lines both above and below on the same carrier** (`dual-one-letter-lines-unrepresentable`);
- a between-letter point on the final orthographic letter with no following letter (`between-point-without-next-letter`);
- U+035E/U+035F on the final orthographic letter with no following base (`marhetana-without-next-letter`);
- U+035E and U+035F beginning on the same base (`dual-marhetana-spans-unrepresentable`);
- consecutive same-direction U+035E/U+035F starts that would overlap on the middle base (`overlapping-marhetana-spans`).

These are blocking page states rather than occasions to invent nested or overlapping syntax.

## T8 — one-letter adjacency versus direct spans

Two adjacent letters carrying U+0747, and again U+0748, produce a non-blocking:

`PAGE CHECK adjacent-one-letter-lines-page-check`

In **canonical confirmed storage**, this sequence means two separate one-letter lines and transliterates as `(x)(y)` / `(_x)(_y)`. The notice exists because a **raw digital witness** may have used repeated U+0747/U+0748 merely to approximate one continuous printed line. The page audit must settle that before confirmation.

A page-confirmed span is then encoded directly:

- `ܡ͞ܢ` (U+035E after mim) ↔ `m⁀n`;
- `ܡ͟ܢ` (U+035F after mim) ↔ `m‿n`.

The confirmed live case is `ܫܒܲܩ̣͞ܢ` ↔ `šbaq_⁀n`. Once the Syriac has this direct span state, transliteration needs no auxiliary page decision.

## T9 — things text alone cannot synthesize

One source situation cannot truthfully be represented by an invented Unicode token: **an unreadable mark on the physical page**. It is stopped before confirmation and never replaced by a guessed placeholder.

The former span/separate problem no longer belongs in this category. Unicode U+035E/U+035F gives canonical storage a direct two-base page state; only a lossy **raw witness encoding** may require human correction during the page audit.

---

## Why this counts as exhaustive

The suite does not attempt every mathematical permutation of marks. It closes every finite interface where behavior can differ—canonical carriers, bgdkpt states, vowel states, carrier-sensitive aliases, special marks, source aliases, combining order, every assigned U+0700–U+074F character, rule-named extra codepoints including U+035E/U+035F, editorial structure, known contradictory states, and a catch-all for genuinely new input.

If a future witness reveals a new page-state or encoding, add the smallest case that represents it and retain it permanently as a regression test.
