# Transliteration Rules — Reversible Canonical Transliteration

## Purpose

This file governs **canonical transliteration** only.

Canonical transliteration is a **strict, reversible, grapheme-level rendering of East Syriac (Adiabene) pointed script into Latin**.

It is not an English-facing spelling system.
It is not readability-based transcription.
It is not a phonetic transcription.

Apply silently. Do not restate unless asked or unless a rule bears on the current line.

**Section numbering is stable.** A retired section number remains reserved rather than shifting later cross-references.

---

## 1. Governing Principle

**The canonical string records the normalized Syriac block and nothing else.**

Every in-scope mark and piece of editorial apparatus in that block is represented. Nothing not in the block is added.

The system must satisfy:

- **Reversible.** From the canonical string alone, the pointed Syriac orthography can be reconstructed exactly.
- **Injective on orthography.** Two distinct pointed spellings never yield the same string.

### What this system does *not* claim

It is **not** injective on *words*. Where the pointed script itself neutralizes a distinction, no function of the orthography can separate it:

- `brā` = ܒܪܐ "Son" (b-r) and ܒܪܐ "he created" (b-r-ʾ)

These are true homographs. The transliteration is correct in collapsing them, because the page collapses them.

The same applies wherever a grapheme serves two functions: ʾālap̄ as consonant and ʾālap̄ as mater are one letter and receive one transliteration; yodh as consonant and yodh as mater likewise. The distinction is analytical, not graphic, and does not belong in the string.

**Glossary entry identity is canonical headword + root + morphology, not form alone.**

### Corollary — where resolution lives

- **Homographs** (§1) are separated by the **root** field; if canonical headword and root are both identical, `{...}` morphology completes the Glossary identity (General Rules §10.1).
- **Pronunciation is out of scope entirely.** Gemination, vowel quality, and hardness or softness not marked on the page are not recorded anywhere — not in the string, not in a field. The page does not mark them, so the project does not carry them.
- The **parse field** carries one thing only: an **exclusion record** — a mark that survives ingestion yet cannot be represented in the string. See General Rules §10.8 for the exclusion rule.

### Case

Case is not a feature of the page. The canonical string is therefore **entirely lowercase**; all capitalization belongs to the English layer. Māryā is written `māryā` in the canonical string and capitalized only on the English side.

---

## 2. Notation Beyond the Letter Tables

Editorial apparatus is preserved literally alongside the letter-for-letter mapping.

| Notation | Meaning | On reversal |
|---|---|---|
| `(x)` | occultans line above (§6) | restore the line over the wrapped letter or letters |
| `[…]` | editorial addition or alternate | preserve the brackets |
| `(English label:)` | source or witness label | preserve the label |

Syriac inside editorial brackets transliterates normally. English-only interpretive brackets have no transliteration counterpart.

Example: `ʾaḇā [waḇrā] nāpēq`

---

## 3. Consonants

### 3.1 Non-bgdkpt

| Syriac | Translit. |
|---|---|
| ܐ | ʾ |
| ܗ | h |
| ܘ | w |
| ܙ | z |
| ܚ | ḥ |
| ܛ | ṭ |
| ܝ | y |
| ܠ | l |
| ܡ | m |
| ܢ | n |
| ܣ | s |
| ܥ | ʿ |
| ܨ | ṣ |
| ܩ | q |
| ܪ | r |
| ܫ | š |

`ܘ` = `w` only when consonantal; as vowel carrier see §4.
`ܝ` = `y` only when consonantal; as vowel carrier or mater see §4.

**Superscript ʾālap̄** (U+0711), a small ʾālap̄ written above the line as a mark rather than a letter, is transliterated `ᵃ` preceding its carrier. Recorded graphically; no function is claimed.

**ܖ (U+0716)** is not a letter of this system. It is an encoding artifact and is resolved at ingestion; see §16.2.

**ܣ final semkath (U+0724)** is a positional shape of semkath, normalized at ingestion; see §16.1.

### 3.2 Bgdkpt — three states

There are **three** page-states, because *unmarked* is distinct from *marked*.

| Letter | qūššāyā (marked hard) | rūkkākā (marked soft) | unmarked |
|---|---|---|---|
| ܒ | ḃ | ḇ | b |
| ܓ | ġ | ḡ | g |
| ܕ | ḋ | ḏ | d |
| ܟ | k̇ | ḵ | k |
| ܦ | ṗ | p̄ | p |
| ܬ | ṫ | ṯ | t |

- **Bare letter means the page carries no point.** It does not mean "hard."
- If the point is absent, the letter is written bare. A lexically secure soft or hard reading is **not** recorded, here or anywhere.
- **Never** substitute readability spellings (`v, gh, kh, ph, th`).

*Note:* `k̇` has no precomposed Unicode form and requires U+0307 combining dot above.

**Do not infer bgdkpt state from glyph width.** Read the normalized point/page-state under §16; if the source does not encode or securely show a point, record the letter as unmarked.

### 3.3 Reserved — no third resh/dalath state

No separate canonical consonant state is defined for an undotted resh/dalath-like stroke. U+0716 is handled only by the ingestion rule in §16.2.

---

## 4. Vowels

Vowel identifications and their **representation** divide into two classes, because the two behave differently under reversibility.

### 4.1 Class A — carrier-borne vowels

These are single page-states in which the vowel sign is borne by the mater letter itself. The carrier is therefore part of the written vowel: it is neither inferred nor omitted.

| Sign | Identification | Translit. |
|---|---|---|
| yodh + ī-sign | ḥḇāṣā | `ī` |
| waw + one dot above | rwāḥā | `ō` |
| waw + one dot below | rḇāṣā / ʾeṣāṣā | `ū` |

**There is no carrierless Class-A notation.** `ĭ`, `ŏ`, and `ŭ` are not valid canonical symbols. A sign that appears to represent `ī`, `ō`, or `ū` without the expected yodh or waw is **flagged at ingestion, not transliterated by inference**. Establish the page-state from the witness before adding or normalizing any such form (§16).

*Note on names.* Grammars differ: *rḇāṣā* names the /u/ vowel in one convention and the e-vowels in another, where Unicode uses *ʾeṣāṣā*. This file uses *rḇāṣā / ʾeṣāṣā* for /ū/. Nothing turns on the choice.

### 4.2 Class B — consonant-borne vowels

The vowel sign is borne by the **preceding consonant**. Any mater is a *separate following letter*, and may be ʾālap̄ or yodh.

| Sign | Identification | Translit. |
|---|---|---|
| one dot above + one below, diagonal | pṯāḥā | `a` |
| two dots above, angular | zqāpā | `ā` |
| two dots below, level | zlāmā pšīqā | `e` |
| two dots below, angular | zlāmā qašyā | `ē` |

`a` and `e` do not take matres.

For `ā` and `ē`, the mater is written as its own letter (`ʾ` or `y`) — **except word-finally**, where §9 convention 1 applies and absence is marked by breve. Position decides, mechanically:

| String | Reading |
|---|---|
| `…ā` (final) | zqāpā + mater ʾālap̄ |
| `…ă` (final) | zqāpā, no mater |
| `…ā…` (internal) | zqāpā, no mater |
| `…āʾ…` (internal) | zqāpā + ʾālap̄ |
| `…ē` (final) | zlāmā qašyā + mater ʾālap̄ |
| `…ĕ` (final) | zlāmā qašyā, no mater |
| `…ē…` (internal) | zlāmā qašyā, no mater |
| `…ēy` (any position) | zlāmā qašyā + yodh |
| `…ēʾ…` (internal) | zlāmā qašyā + ʾālap̄ |

Worked: `brēh` (internal ē, no mater) · `hēyn` (ē + yodh) · `lmēʾṯā` (internal ē + ʾālap̄; final ā + ʾālap̄ by convention) · `ʿālm̈ē` (final ē + ʾālap̄) · `nāpēq` (internal ē, no mater).

**Word-final `e` (and `a`) followed by a written ʾālap̄.** `a` and `e` take no matres, but a written ʾālap̄ is still a letter on the page and is recorded as `ʾ` per §3.1 — it is not analyzed as a mater. Nothing else in the system produces word-final `eʾ`, so the sequence is unambiguous and reverses cleanly. Worked: `tēʾteʾ`, `nehweʾ` (Abun).

**Two dots below is not always a vowel.** The same page position carries the mark of §17. Distinguish by shape: zlāmā is two dots level or angular; §17's mark is the two-dot mark that is neither.

### 4.3 Diphthongs

True diphthongs preserve the consonantal carrier: `aw`, `ay`.
Distinguished from `ō`/`ū`/`ī`, where the carrier bears the vowel point.

A written yodh after `ē` and a consonantal yodh are the same page-state and receive the same string; the analysis is not recorded.

### 4.4 Unpointed consonants

A consonant written with **no vowel point** is transliterated as the bare consonant. This is a page-state, not an assertion of vocal shewa. Inferred but unwritten vowels are not recorded.

---

## 5. Syāmē

Syāmē are a page-mark and must be represented.

**Notation:** combining diaeresis (U+0308) over the **carrying letter**.

- `ber̈yāṯā` — syāmē carried by the resh
- `ber̈yāṯā` ≠ `beryāṯā` — the second asserts no syāmē on the page

Placement follows the page strictly and is not normalized to a conventional position.

### 5.1 Mark order — the general rule

Where a Syriac letter carries more than one combining mark, storage order is deterministic:

1. **Different canonical combining classes sort in ascending class order.** NFC performs this reordering.
2. **Marks within the same class follow the project order below.** NFC does **not** reorder equal-class marks, so ingestion must do it explicitly.
3. Store the result in **NFC**.

The in-scope combining classes are:

- **36** — superscript ʾālap̄ (U+0711). It therefore sorts before the below and above marks without a project tie-break.
- **220 (below)** — use `[vowel, bgdkpt point, single point (§7), two dots below (§17), breve below (§18), occultans line below (§6)]`.
- **230 (above)** — use `[vowel, bgdkpt point, single point (§7), syāmē, occultans line above (§6)]`.

The order is a **storage convention, not a claim about phonological or visual priority**. It exists because several distinct in-scope marks share class 220 or 230. After §16 has normalized source codepoints to page-states, two canonically equivalent witnesses must therefore produce the same combining sequence before comparison or round-trip validation.

### 5.2 Syāmē against a vowel on the same letter

- **Carrier-borne vowel (`ī`, `ō`, `ū`).** The vowel sits on the mater and is written as a precomposed letter; syāmē follows it: `ī̈`, `ō̈`, `ṻ`. Worked: `ʾī̈dāwhy`.
- **Consonant-borne vowel (`a`, `e`, `ā`, `ē`).** The vowel is a separate letter following the consonant; syāmē attaches to the consonant and therefore stands **before** the vowel letter: `m̈ē`, never `mē̈`. Worked: `ʿālm̈ē`, `ḥaÿē`, `paḡr̈ē`, `lmīẗē`, `daḥṭāḧē`, `šmaÿā`, `nāš̈ā`.

---

## 6. The Occultans Line (mhaggyānā / mṭalqānā)

A line above or below a letter, or spanning two letters.

**The notation records the mark, not a phonological claim.** The two traditional names denote opposite functions — *mṭalqānā* marks a letter silent, *mhaggyānā* marks one pronounced — and they are graphically the same stroke. A transliterator cannot tell them apart by looking, so the system does not ask it to.

| Page-state | Notation |
|---|---|
| line above one letter | `(x)` |
| line above spanning two letters | `(xy)` |
| line below one letter | `(_x)` |
| line below spanning two letters | `(_xy)` |

- `md(n)ītā` — the nun is on the page, carrying the line
- `w(ʾ)nāš̈ā`, `(h)ī` — prosthetic ʾālap̄ and enclitic hē, each carrying the line above one letter
- `šba(q_n)` — one line spanning qoph and nun; the qoph also carries a §7 point below, written inside the span after its carrier

The `_` at the head of the wrap marks a line below and cannot be confused with §7's `_`, which always follows its carrier.

### 6.1 The spanning convention and its exception form

`(xy)` asserts **one** line covering two letters. Two *separate* lines on adjacent letters are written `(x)(y)`.

This exception form is required by §9.1 and is what makes the convention legal: without it, a wrong prediction would be invisible.

**Encoding limitation.** A spanning line is encoded U+0747 on **both** letters, because Unicode has no character for a line spanning two Syriac letters. The stored source therefore cannot distinguish one spanning line from two separate lines — the canonical string can, and the source cannot. This is a property of the encoding, not of the notation; see §16.6.

---

## 7. The Single Point

A single point above or below a letter, or standing between two letters, that is **not** identifiable as a vowel sign or a bgdkpt point.

The test is positional, not functional. Purpose is not recorded.

**Disambiguation by carrier.** A single point on a letter is read from the letter it sits on:

| Carrier | Point above | Point below |
|---|---|---|
| bgdkpt | qūššāyā (§3.2) | rūkkākā (§3.2) |
| waw | rwāḥā `ō` (§4.1) | rḇāṣā `ū` (§4.1) |
| yodh | §7 | ḥḇāṣā `ī` (§4.1) |
| any other letter | §7 | §7 |

A point standing **between** two letters is never a vowel or a bgdkpt point, whatever the letters are, and is always §7.

| Page-state | Notation |
|---|---|
| point above the carrying letter | `^` |
| point below the carrying letter | `_` |
| point above, between this letter and the next | `^^` |
| point below, between this letter and the next | `__` |

**Placement against a vowel.** A marker for a point *on* a letter follows the letter immediately, before the vowel. A marker for a point *between* letters follows the whole letter-plus-vowel unit, because the mark stands after everything belonging to the first letter.

Worked: ܡ̣ܢ → `m_n`, distinct from ܡܲܢ → `man`. · ܩ᷸ܵܥܹܝܢ → `qā^^ʿēyn` (Abun), the point standing between qoph and ʿē.

Above and below are kept separate because the opposition is itself the distinction being drawn (hāw / hū).

---

## 8. Gemination — Not Represented

Syriac orthography does not mark doubling, and doubling is a fact about pronunciation. **It is therefore not recorded anywhere in this project** — not in the canonical string, and not in any field.

- ܩܲܕ݁ܝܼܫܬܵܐ → `qaḋīštā` (not `qaḋ[d]īštā`, and no note that the dalath is doubled)
- ܟܠܡܸܕܸ݁ܡ → `klmeḋem`

Where two consonant letters are actually written, both appear — that is not gemination notation, merely the page: ܐܸܬ݁ܬܲܩܲܢܘ → `ʾeṫtaqanw`.

**Note on qūššāyā.** Some forms traditionally described as geminated carry qūššāyā on the consonant in question. Whether that point marks gemination, hardness, or both is a question about scribal practice, not about notation. The system records the point as `ḋ` and claims nothing further.

---

## 9. Deterministic Conventions

Reversibility permits **conventions**, not only symbols. Where a feature is fully predictable from position, it need not be marked — this is what prevents diacritic saturation.

### 9.1 Audit requirement

**Every convention must carry a marked exception form.** A convention without one is prohibited.

A convention states that some page-feature is predictable. If the prediction ever fails and there is no way to mark the failure, the string silently misrepresents the page and reversibility is lost with no error raised. The exception marker is what converts a wrong prediction into a visible, correctable one.

Conventions must be re-verified against attested text whenever new material is worked, not assumed once and trusted.

### 9.2 Conventions in force

1. **Word-final `ā` implies mater ʾālap̄.** Exception form: `ă`.
2. **Word-final `ē` implies mater ʾālap̄.** Exception form: `ĕ`. An explicitly written yodh gives `ēy` and is not an exception.
3. **Prosthetic ʾālap̄ is written `ʾ`** and requires no special mark. *(No exception form needed: this is a letter mapping, not a prediction.)*
4. **Word division follows the source.** Prefixed particles are written solid unless the source separates them. Editorial brackets do not divide words. The canonical string never strips proclitics; the glossary may index a headword with them stripped, but that is a glossary convention and does not touch the string.
5. **An occultans line written on two adjacent letters is one spanning line.** Exception form: `(x)(y)` (§6.1).

### 9.3 Reserved

Reserved.

---

## 10. Scope

### In scope
Consonants, vowel points, bgdkpt pointing, syāmē, the occultans line, the distinguishing point, two dots below (§17), the breve below (§18), matres, and project editorial apparatus (§2).

### Out of scope at word level
**Out-of-scope characters are removed at ingestion (§16.1), not carried in the stored line.** The confirmed text contains in-scope orthography only.

- **Punctuation.** The Syriac punctuation repertoire (U+0700–U+070D) and any Latin substitute a typist has used for it. Clause division is carried by line breaks and visual layout. Where a particular working file needs punctuation for reading, it is added there by hand; it is not part of the confirmed text and no entry records it.
- **Accent and cantillation points.**
- **Abbreviation and numeral marks.**
- **Scribal correction marks and marginalia.**
- **Presentational characters.** Tatweel / kashida elongation (ـ), zero-width joiners and non-joiners, and line-fill strokes. Artifacts of justification and typesetting, not orthography. ܒܝܵـܘ̈ܡܲܝ is ingested as ܒܝܵܘ̈ܡܲܝ and transliterates `byāẅmay`.

**Consequence for the parse field.** If an in-scope mark survives ingestion but the canonical notation cannot represent it, record the exclusion under General Rules §10.8 and flag the word. Otherwise the stored line and canonical string must agree at every in-scope point.

A word's canonical string is reversible **with respect to its segmental and vocalic orthography**, which after ingestion is the whole of what the stored line contains.

### Legibility
Marks that cannot be read are not reconstructed or invented. An unreadable in-scope mark is flagged for source review; no provisional canonical symbol is created merely to fill the gap.

---

## 11. Headword Identity and Search

### 11.1 Exact identity

The **canonical headword string itself** is the exact reversible **orthographic** key for the indexed form. No second exact or ASCII surrogate key is stored. Where General Rules §10.17 deliberately merges environmentally varying bgdkpt pointing, the resulting unmarked headword is the orthographic identity of that **index form**; occurrence spellings remain fully pointed and reversible in their citations. Full Glossary entry identity is canonical headword + root + `{...}` morphology (General Rules §10.1).

### 11.2 Fold key

Each glossary headword carries **one additional, non-authoritative fold key**. It is lowercase; all diacritics are stripped; `ʾ` and `ʿ` are dropped; notation characters are dropped. It is written in the entry as `(search: alaha)`.

The fold key is deliberately ambiguous. Collisions are expected and acceptable — `brā` "Son" and `brā` "he created" both fold to `bra`, and the root field separates their entries. This key exists only so that a human can find a form by typing an approximate Latin spelling. It is never used for identity, decisions, citation, or display.

---

## 12. Round-Trip Validation

A canonical string is **valid** if and only if:

1. Applying the inverse tables while preserving §2 editorial apparatus literally reproduces the normalized Syriac block **exactly**, setting aside anything excluded under §10 and recorded per General Rules §10.8; and
2. No two distinct entries in the glossary share a canonical headword string, root, *and* `{...}` morphology.

Condition 2 is the Glossary-identity check. A collision means either an entry has been duplicated or the morphology/root analysis has not yet separated two genuinely distinct forms.

**Round-trip asymmetry.** A spanning occultans line (§6.1) is recorded in the string but cannot be distinguished from two separate lines in the encoded source. Round-trip cannot detect a failure of that convention; only the page can.


---

## 13. Reserved

Reserved.

---

## 14. Reserved

Reserved.

---

## 15. Validation

Validation requirements are §12 and General Rules §11. Corpus reports and test output do not belong in this specification.

---

## 16. Source Ingestion — Codepoint Normalization

Digital witnesses may use different codepoints for the same visible page-state, and the same codepoint may serve different page-states in different carrier environments. Canonical transliteration therefore normalizes **page-state first**, then applies §§3–7. Reading source codepoints as universal semantic labels is prohibited.

### 16.1 Normalize to page-state

Collapse the single-dot marks to two classes, then read by carrier per §7:

- **single point above** — U+0741, U+073F, U+0307
- **single point below** — U+0742, U+073C, U+0323

Multi-dot signs (U+0732 pṯāḥā, U+0735 zqāpā, U+0738 zlāmā pšīqā, U+0739 zlāmā qašyā) are unambiguous single codepoints and pass through unchanged.

**Removed at ingestion, before any other step.** Out-of-scope characters (§10) never enter the stored line:

- Syriac punctuation **U+0700–U+070D**, the abbreviation mark **U+070F**, and any Latin character standing in for them — a full stop, comma, colon, or semicolon inside a Syriac line is a typist's substitute, not the page's mark, and is removed on the same footing.
- Tatweel **U+0640**, zero-width joiner **U+200D**, zero-width non-joiner **U+200C**, and line-fill strokes.
- Accent and cantillation points, if ever encountered.

Removal is silent and needs no record; §10 licenses it and the stored line is the result. An **unrecognized** codepoint is not removed — it is flagged and left for decision.

Also normalized at ingestion:

- **U+0724 FINAL SEMKATH → U+0723.** A positional shape, not a distinct letter.
- **U+1DF8 → `^^`**, **U+1DFA → `__`** (§7). These are the encodings for a point standing between two letters.
- **U+0324, U+0740, U+0744 → the two-dots-below page-state** (§17).
- **U+032E → the breve-below page-state** (§18).

### 16.2 U+0716

**ܖ (U+0716) carrying syāmē is resh.** The resh point and syāmē occupy the same position and the script suppresses the former; some typists encode the result with U+0716, others with U+072A. Both are resh. Normalize to ܪ and transliterate `r̈`. This holds whether or not a vowel point stands between the two in the stored sequence — in ܥܝܼܖܹ̈ܐ the zlāmā qašyā intervenes, and the rule applies.

**Bare U+0716 normalizes to resh and raises a flag.** Treat the normalization as a source-level anomaly, not as evidence for a new consonant. If the lexical context permits dalath or otherwise leaves the reading uncertain, require manual source review before confirmation.

### 16.3 Combining-mark order

Normalize every combining sequence to §5.1 before comparison or round-trip validation (§12). NFC orders marks of **different** canonical combining classes, but it does not repair the order of two marks that share a class. Ingestion must therefore enforce the §5.1 project order for both class **220** and class **230** sequences after page-state normalization.

### 16.4 Per-block ingestion

**The audit runs per block, not per file.** A single file may contain blocks drawn from different digital sources or encoding conventions. Audit each block whose provenance may differ, and record where the seams fall.

### 16.5 Witness collation

Ingestion is per-witness. Where witnesses disagree after normalization, the disagreement is textual and belongs to the source hierarchy (General Rules §1), not to this file.

**Do not resolve by majority vote.** Witnesses may share an ancestor or encoding source, so a vote can count copies rather than independent readings. The designated source of record governs; variants are recorded rather than averaged.### 16.6 West Syriac vowel codepoints — refused, never mapped

The East Syriac vowels are the **dotted** forms: U+0732, U+0735, U+0738, U+0739, U+073C, U+073F. The West Syriac equivalents are separate characters: U+0730, U+0731, U+0733, U+0734, U+0736, U+0737, U+073A, U+073B, U+073D, U+073E.

**These are never normalized into East Syriac vowels.** A West Syriac sign is a different mark, not a different encoding of the same mark, and mapping one to the other fabricates a reading the page does not contain.

- **In a source of record:** raises a flag. Either the source is not what it was taken to be, or the block has a seam (§16.4).
- **In a corpus search:** a West-vocalized token **carries no evidence about East Syriac pointing**. Distribution and lexical range may be cited from it; a vowel or a bgdkpt point may not.

### 16.7 Unrepresentable page-states

A spanning occultans line (§6.1) is encoded U+0747 on both letters because no single character exists for it. The encoded source is therefore lossy at that point, and the canonical string carries information the stored Syriac does not. A mismatch caused by that lossy source encoding is expected and must be checked against the page rather than treated as an ordinary round-trip failure.

---

## 17. Two Dots Below

Two dots beneath a letter, distinct from zlāmā by shape and environment.

**Notation:** combining diaeresis below (U+0324) on the transliterated letter — `ẗ` above for syāmē, `t̤` below for this. The two are deliberately symmetric: the string mirrors the page.

**Encodings normalized to this page-state:** U+0324, U+0740 SYRIAC FEMININE DOT, U+0744 SYRIAC TWO VERTICAL DOTS BELOW. In East Syriac and Estrangela the feminine dot takes the form of two dots below, which is why the Syriac-specific codepoint and the generic one both occur for one appearance.

**Function is not recorded.** The same graphical page-state receives the same notation regardless of grammatical interpretation.

ASCII: `:` after the carrying letter.

---

## 18. The Breve Below

An arc beneath a letter, opening downward. Graphically distinct from rūkkākā, which is a dot.

**Notation:** combining breve below (U+032E) on the transliterated letter — `p̮`. Encoded U+032E at source, so ingestion passes it through unchanged.

**No collision.** Every other mark in the system occupies a different position or shape: macron above for soft `p̄` and `ḡ`, macron below for soft `ḇ ḏ ḵ ṯ`, breve *above* for the word-final Class-B exceptions `ă ĕ`, dot above for hard, diaeresis above for syāmē, diaeresis below for §17. The space below a pe is free precisely because pe is one of the two letters whose soft form takes a macron above.

ASCII: `%` after the carrying letter.
