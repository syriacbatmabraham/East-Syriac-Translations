# Final normalization torture corpus

This corpus is deliberately synthetic. None of the strings need to be lexical Syriac. The goal is **complete input/state coverage**, not one fake word per rule.

## Coverage contract

The normalization torture test is complete when all of the following are true:

1. Every assigned codepoint in the core Syriac block **U+0700–U+074F** has an explicit expected disposition: pass, normalize, remove, refuse/flag, or unsupported-letter/mark flag.
2. Every extra generic codepoint named by the rules is exercised: U+0307, U+0323, U+0308, U+0324, U+032E, U+1DF8, U+1DFA, U+0640, U+200C, U+200D, and U+FEFF.
3. Every carrier-sensitive single-point alias is tested on every carrier class that changes its meaning.
4. Every canonical page-state has at least one legal example.
5. Every known impossible, contradictory, or presently unrepresentable normalized state has an explicit negative example.
6. Editorial apparatus and word-boundary behavior are exercised.
7. Any arbitrary non-combining codepoint outside the licensed source grammar is retained **and flagged**, never silently admitted.
8. The known encoded-source ambiguity of adjacent occultans lines is surfaced as a mandatory page check before transliteration.

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
- occultans above/below;
- hostile same-class mark order across CCC 36/220/230.

Expected output always satisfies Transliteration Rules §5.1 and NFC.

## T4 — positional/mater pass-through

Normalization deliberately does **not** infer final matres. Small boundary tokens therefore cover:

- final zqāpā without written ʾālap̄;
- final zqāpā + written ʾālap̄;
- final zlāmā qašyā without written ʾālap̄;
- final zlāmā qašyā + written ʾālap̄;
- zlāmā qašyā + yodh.

The page-state report shows only what is literally encoded. The later transliteration layer applies `ā/ă` and `ē/ĕ`.

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
- **occultans both above and below on the same carrier** (`dual-occultans-unrepresentable`);
- a between-letter point on the final orthographic letter with no following letter (`between-point-without-next-letter`).

The last case was exposed by the transliteration specification audit: both Unicode marks can coexist syntactically, but the canonical notation defines no reversible representation for both directions on one carrier. It therefore blocks before transliteration rather than inventing syntax.

## T8 — occultans ambiguity: page-only resolution

Two adjacent letters carrying U+0747, and again U+0748, produce a non-blocking:

`PAGE CHECK adjacent-occultans-page-check`

Encoded Syriac cannot distinguish one spanning line from two separate adjacent lines. Normalization may store the Unicode state, but forward transliteration must receive the page decision explicitly. This is the known point where the page contains information the encoded Syriac cannot.

## T9 — things text alone cannot synthesize

Two source situations cannot truthfully be represented by an invented Unicode token:

1. an unreadable mark on the physical page;
2. the visual span/separate occultans distinction.

The second is represented as an encoded ambiguity under T8 and settled from the page. The first is stopped before confirmation and never replaced by a guessed placeholder.

---

## Why this counts as exhaustive

The suite does not attempt every mathematical permutation of marks. It closes every finite interface where behavior can differ—canonical carriers, bgdkpt states, vowel states, carrier-sensitive aliases, special marks, source aliases, combining order, every assigned U+0700–U+074F character, rule-named extra codepoints, editorial structure, known contradictory states, and a catch-all for genuinely new input.

If a future witness reveals a new page-state or encoding, add the smallest case that represents it and retain it permanently as a regression test.
