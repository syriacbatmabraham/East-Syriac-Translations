# Final normalization torture corpus

This corpus is deliberately synthetic. None of the strings need to be lexical Syriac. The goal is **complete input/state coverage**, not one fake word per rule.

The executable suite currently contains **74 deterministic tests** across baseline normalization, page-state inspection, focused stress cases, and the exhaustive coverage matrix.

## Coverage contract

The torture test is complete when all of the following are true:

1. Every assigned codepoint in the core Syriac block **U+0700–U+074F** has an explicit expected disposition: pass, normalize, remove, refuse/flag, or unsupported-letter/mark flag.
2. Every extra generic codepoint named by the rules is exercised: U+0307, U+0323, U+0308, U+0324, U+032E, U+1DF8, U+1DFA, U+0640, U+200C, U+200D, and U+FEFF.
3. Every carrier-sensitive single-point alias is tested on every carrier class that changes its meaning.
4. Every canonical page-state has at least one legal example.
5. Every known impossible or contradictory normalized state has an explicit negative example.
6. Editorial apparatus and word-boundary behavior are exercised.
7. Any arbitrary non-combining codepoint outside the licensed source grammar is retained **and flagged**, never silently admitted.
8. The known encoded-source ambiguity of adjacent occultans lines is surfaced as a mandatory page check before transliteration.

`tools/tests/test_normalization_coverage.py` enforces this contract programmatically. The older focused tests remain because they are useful regression tests, but this file is the compact human description of the final torture set.

---

## T1 — consonant and bgdkpt sweep

One synthetic run contains the complete canonical consonant inventory:

`ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ`

The test then mechanically cycles **all six bgdkpt letters** through the three normalized states:

- unmarked;
- qūššāyā;
- rūkkākā.

This is better than inventing eighteen separate pseudo-words: the loop proves that the carrier set itself is complete.

### Input-only letter forms

The same suite separately forces:

- U+0724 FINAL SEMKATH → U+0723 SEMKATH;
- U+0716 + syāmē → resh, without a flag;
- bare U+0716 → resh **with** `bare-u0716`.

---

## T2 — complete single-point matrix

There are three source encodings for a point above and three for a point below. Their meaning depends on carrier, so the test generates the full matrix instead of writing twenty-four visible pseudo-words.

### Above aliases

Each of U+0741, U+073F, U+0307 is placed on:

- bgdkpt → qūššāyā;
- waw → rwāḥā `ō`;
- yodh → generic single point above;
- ordinary non-bgdkpt consonant → generic single point above.

### Below aliases

Each of U+0742, U+073C, U+0323 is placed on:

- bgdkpt → rūkkākā;
- waw → `ū` carrier vowel;
- yodh → `ī` carrier vowel;
- ordinary non-bgdkpt consonant → generic single point below.

All six bgdkpt letters are also checked explicitly with generic source dots so a membership mistake in the carrier set cannot hide behind a single beth example.

---

## T3 — one “monster” legal page-state word

Rather than one word per mark, the machine is exercised on a dense synthetic token whose successive letters carry different maximal combinations. Conceptually it includes:

1. a consonant with pṯāḥā;
2. a consonant with zqāpā plus syāmē and an occultans line above;
3. a consonant with zlāmā pšīqā plus single point below, two dots below, breve below, and occultans line below;
4. a consonant with zlāmā qašyā;
5. waw + rwāḥā + syāmē;
6. waw + `ū` point + syāmē;
7. yodh + `ī` point + syāmē;
8. U+0716 + intervening vowel + syāmē, which must become resh;
9. superscript ʾālap̄ mixed with below and above marks so CCC 36/220/230 ordering is exercised;
10. a between-letter point above;
11. a between-letter point below;
12. final semkath input.

The marks are deliberately supplied in hostile order where possible. Expected output is the §5.1 canonical order.

The automated suite also checks all three two-dots-below inputs—U+0324, U+0740, U+0744—against the one canonical output U+0324.

---

## T4 — positional/mater pass-through set

These small tokens are intentionally retained because they are the seam between normalization and transliteration:

- final zqāpā without written alaph;
- final zqāpā followed by written alaph;
- final zlāmā qašyā without written alaph;
- final zlāmā qašyā followed by written alaph;
- zlāmā qašyā followed by written yodh.

The normalizer must **not infer anything**. The page-state report simply shows the literal letters and marks. Later forward transliteration applies the word-final `ā/ă` and `ē/ĕ` conventions.

This ensures that the human audit remains a check of the page, not a check of linguistic analysis.

---

## T5 — editorial apparatus, word division, and removable debris

One structural input combines:

- `(Witness A: 2)` — parenthesized label preserved literally;
- `ܐ[ܒ]ܐ` — square brackets preserved while remaining transparent to word division;
- spaces and line breaks;
- every Syriac punctuation codepoint U+0700–U+070D;
- U+070F abbreviation mark;
- `. , : ;` as Latin punctuation substitutes;
- tatweel U+0640;
- ZWNJ U+200C;
- ZWJ U+200D;
- U+0749 MUSIC;
- U+074A BARREKH.

All licensed debris disappears outside the parenthesized editorial label. The report still sees `ܐ[ܒ]ܐ` as one orthographic word.

Malformed apparatus is tested separately because combining it would obscure which boundary failed:

- unclosed `(`;
- unmatched `)`;
- unclosed `[`;
- unmatched `]`.

Each is preserved and flagged.

---

## T6 — complete refusal/unknown sweep

### Every West Syriac vowel

Each of U+0730, 0731, 0733, 0734, 0736, 0737, 073A, 073B, 073D, 073E is attached to a legal carrier in turn.

Expected result for every one:

- preserved;
- `west-syriac-vowel` flag;
- never mapped into an East Syriac vowel.

### Unsupported Syriac letters

Every assigned Syriac-block letter outside the project inventory is exercised:

- U+0714 GAMAL GARSHUNI;
- U+071C TETH GARSHUNI;
- U+071E YUDH HE;
- U+0727 REVERSED PE;
- U+072D PERSIAN BHETH;
- U+072E PERSIAN GHAMAL;
- U+072F PERSIAN DHALATH;
- U+074D SOGDIAN ZHAIN;
- U+074E SOGDIAN KHAPH;
- U+074F SOGDIAN FE.

Each is retained and receives `unrecognized-syriac-letter`.

### Unsupported Syriac marks

U+0743 TWO VERTICAL DOTS ABOVE, U+0745 THREE DOTS ABOVE, and U+0746 THREE DOTS BELOW are retained and receive `unrecognized-combining-mark`.

### Arbitrary unknowns

The catch-all is explicitly tested with:

- unassigned U+074B and U+074C;
- Greek alpha;
- Cyrillic a;
- an emoji.

All survive for inspection and receive `unexpected-codepoint`. This closes the possibility that an unanticipated non-combining character could silently enter normalized Syriac.

Latin letters/digits outside parenthesized apparatus retain the more specific `unexpected-non-syriac-text` guard used to catch accidental whole-file input.

---

## T7 — malformed clusters and impossible normalized states

These remain small, separate negative cases because combining them would make the diagnosis ambiguous.

### Source-level malformed input

- orphan syāmē;
- orphan generic dot above;
- orphan generic dot below;
- orphan unknown Syriac mark;
- two above aliases on one carrier;
- two below aliases on one carrier;
- BOM U+FEFF.

### Post-normalization contradictions

The invariant checker is called directly with normalized-looking but impossible strings:

- bgdkpt carrying both qūššāyā and rūkkākā;
- one ordinary consonant carrying two East Syriac vowels;
- waw carrying both `ō` and `ū`;
- duplicate syāmē;
- canonical qūššāyā injected onto a non-bgdkpt carrier;
- canonical U+073C carrier vowel injected onto an invalid carrier.

These tests intentionally bypass `normalize_text()`. Their purpose is to prove that later code cannot manufacture an invalid normalized string behind the normalizer's back.

---

## T8 — occultans ambiguity: page-only resolution

Two adjacent letters are tested with U+0747 on both, and again with U+0748 on both.

Encoded Syriac can tell us only:

- letter 1 has an occultans line;
- letter 2 has an occultans line.

It **cannot** tell us whether the page shows one line spanning the pair or two independent lines. Therefore this is not a normalization error. The audit emits:

`PAGE CHECK adjacent-occultans-page-check`

The normalized Syriac may still be stored, but forward transliteration must not choose `(xy)` versus `(x)(y)` until the page has been checked.

This is the one known place where the human page audit carries information that the normalized Unicode source itself cannot.

---

## T9 — things text alone cannot synthesize

Two source situations cannot be truthfully represented by an invented Unicode token:

1. **an unreadable mark on the physical page**;
2. **the visual distinction between one spanning occultans line and two separate adjacent lines**.

The second is represented by T8 as an encoded ambiguity and resolved from the page. The first is never converted into a placeholder codepoint: it is stopped before transcription/confirmation and flagged for source review, as required by Translit §10.

---

## Why this counts as exhaustive

The suite does **not** attempt every combinatorial arrangement of every mark. That would be enormous and mostly meaningless. Instead it closes the finite interfaces where behavior can differ:

- every canonical consonant class;
- every bgdkpt state;
- every East Syriac vowel state;
- every carrier-sensitive point alias × carrier class;
- every in-scope special mark;
- every alias normalization;
- every project combining-class order;
- every assigned character in U+0700–U+074F;
- every extra Unicode character explicitly named by the rules;
- all known contradictory normalized states;
- editorial structure and word division;
- a catch-all path for anything genuinely new.

If a future source reveals a new page-state or encoding, the rule is simple: add the smallest new case that represents it and keep it forever as a regression test.
