# Transliteration Rules v2.3.1 — Reversible Canonical Transliteration

## Purpose

This file governs **canonical transliteration** only.

Canonical transliteration is a **strict, reversible, grapheme-level rendering of East Syriac (Adiabene) pointed script into Latin**.

It is not an English-facing spelling system.
It is not readability-based transcription.
It is not a phonetic transcription.

Apply silently. Do not restate unless asked or unless a rule bears on the current line.

**Section numbering is stable.** Withdrawn sections are retained as withdrawal notes rather than renumbered, because stale cross-references have already cost this project real errors.

**Versioning.** The third digit marks a revision that changes no rule — an audit-log row, a status update, a worked example. v2.3.1 is such a revision: §§1–18 are identical to v2.3, and only §9.3 and §15 have grown. Citations to "Translit §X" are unaffected by version.

---

## 1. Governing Principle

**The canonical string records the page and nothing but the page.**

Every mark on the page is represented. Nothing not on the page is added.

The system must satisfy:

- **Reversible.** From the canonical string alone, the pointed Syriac orthography can be reconstructed exactly.
- **Injective on orthography.** Two distinct pointed spellings never yield the same string.

### What this system does *not* claim

It is **not** injective on *words*. Where the pointed script itself neutralizes a distinction, no function of the orthography can separate it:

- `brā` = ܒܪܐ "Son" (b-r) and ܒܪܐ "he created" (b-r-ʾ)

These are true homographs. The transliteration is correct in collapsing them, because the page collapses them.

The same applies wherever a grapheme serves two functions: ʾālap̄ as consonant and ʾālap̄ as mater are one letter and receive one transliteration; yodh as consonant and yodh as mater likewise. The distinction is analytical, not graphic, and does not belong in the string.

**The glossary key is form + root, not form alone.**

### Corollary — where resolution lives

- **Homographs** (§1) are separated by the **root** field.
- **Pronunciation is out of scope entirely.** Gemination, vowel quality, and hardness or softness not marked on the page are not recorded anywhere — not in the string, not in a field. The page does not mark them, so the project does not carry them.
- The **parse field** carries one thing only: an **exclusion record** — a mark that survives ingestion yet cannot be represented in the string. Since ingestion removes every out-of-scope character (§10, §16.1), this field currently has **no instances**. See General Rules §10.8.

### Case

Case is not a feature of the page. The canonical string is therefore **entirely lowercase**; all capitalization belongs to the English layer. Māryā is written `māryā` in the canonical string and capitalized only on the English side.

---

## 2. Notation Beyond the Letter Tables

Only two mechanisms depart from plain letter-for-letter mapping. Both record page features, not supplied information.

| Notation | Meaning | On reversal |
|---|---|---|
| `( )` | occultans line above (§6) | restore the line over the wrapped letter or letters |
| `-…-` | parentheses or editorial brackets **in the source text** | restore source bracketing; type not distinguished (§10) |

Example: `ʾaḇā -waḇrā- nāpēq`

There is **no mechanism for supplied information.** If a reading is not on the page, it is not recorded.

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

**Superscript ʾālap̄** (U+0711), a small ʾālap̄ written above the line as a mark rather than a letter, is transliterated `ᵃ` preceding its carrier. Recorded graphically; no function is claimed. *Untested — not encountered in worked text.*

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

*Note:* `k̇` has no precomposed Unicode form and requires U+0307 combining dot above. Flagged as a minor tooling cost.

*The v2.2 note on dalath width is withdrawn in v2.3.* It asked the transliterator to judge whether a dot under a dalath was "measurably wider" than a neighbouring plain dalath point. With digital and printed sources the codepoint decides and no width judgment arises. The provision produced one recorded error — `dḏīlāḵ` for what the page shows as `ddīlāḵ` (Abun line 14).

### 3.3 The Undotted Stroke — *withdrawn in v2.3*

v2.2.4 defined `ř` for a stroke carrying neither the resh point above nor the dalath point below, treating it as a genuine third page-state.

**Withdrawn.** The provision assumed a manuscript source. In digital and printed sources a stroke either carries a codepoint or does not, and the one case that arises in practice — U+0716 under syāmē — is an encoding question handled by §16.2. Bare U+0716 normalizes to resh with a flag (§16.2). No undotted stroke was ever encountered in worked text.

The caron notation is retired from §11 and §15 accordingly.

---

## 4. Vowels

Vowel identifications and their **representation** divide into two classes, because the two behave differently under reversibility.

### 4.1 Class A — carrier-borne vowels

The vowel sign is borne by the mater letter itself. Presence of the mater is therefore inherent in the sign.

| Sign | Identification | Plene (mater present) | Defective (no mater) |
|---|---|---|---|
| yodh + ī-sign | ḥḇāṣā | `ī` | `ĭ` |
| waw + one dot above | rwāḥā | `ō` | `ŏ` |
| waw + one dot below | rḇāṣā / ʾeṣāṣā | `ū` | `ŭ` |

The breve above marks **absence of the mater letter on the page**, not vowel length or quality.

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

**Two dots below is not always a vowel.** The same page position carries the mark of §17. Distinguish by shape: zlāmā is two dots level or angular; §17's mark is the two-dot mark that is neither, and in practice sits on taw, hē, waw, and ʾālap̄ in the environments listed there.

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

Where a letter carries more than one mark, the canonical order in the string is:

1. **By combining class, ascending.**
2. **Within a class**, in the order `[vowel, bgdkpt point, syāmē]`.

Store **NFC**.

**Unicode enforces rule 1 automatically, and only rule 2 requires care.** The marks written *below* — zlāmā pšīqā, zlāmā qašyā, ḥḇāṣā/ʾeṣāṣā, rūkkākā, and the marks of §17 and §18 — are combining class 220. The marks written *above* — pṯāḥā, zqāpā, rwāḥā, qūššāyā, syāmē, the occultans line — are class 230. A 220 mark and a 230 mark are sorted by normalization no matter how the source stored them. **Two 230 marks are not**, and must be produced in the correct order at the source; §16.3 gives the ingestion rule.

*This corrects v2.2.4, which asserted that a vowel point and syāmē were "both combining class 230" and concluded that every such pair required manual ordering. That is true only of the above-vowels. Of 21 double-marked letters in the Glossary at the time of the correction, 19 self-normalized and 2 did not.*

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

*Status: line above attested on one letter (`w(ʾ)nāš̈ā`, `(h)ī`) and spanning two (`šba(q_n)`), both in the Abun. Line below not yet attested on a securely located carrier in confirmed text.*

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

*Status: `^` and `_` attested; `^^` attested (`qā^^ʿēyn`); `__` not yet attested.*

---

## 8. Gemination — Not Represented

Syriac orthography does not mark doubling, and doubling is a fact about pronunciation. **It is therefore not recorded anywhere in this project** — not in the canonical string, and not in any field.

- ܩܲܕ݁ܝܼܫܬܵܐ → `qaḋīštā` (not `qaḋ[d]īštā`, and no note that the dalath is doubled)
- ܟܠܡܸܕܸ݁ܡ → `klmeḋem`

Where two consonant letters are actually written, both appear — that is not gemination notation, merely the page: ܐܸܬ݁ܬܲܩܲܢܘ → `ʾeṫtaqanw`.

**Note on qūššāyā.** Some forms traditionally described as geminated carry qūššāyā on the consonant in question. Whether that point marks gemination, hardness, or both is a question about scribal practice, not about notation. The system records the point as `ḋ` and claims nothing further.

*This supersedes v2.2.4, which routed gemination to the parse field.*

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
4. **Word division follows the source.** Prefixed particles are written solid unless the source separates them. Hyphens carry a canonical meaning (§2) and may not be used for word-division traceability inside the string. The canonical string never strips proclitics; the glossary may index a headword with them stripped, but that is a glossary convention and does not touch the string.
5. **An occultans line written on two adjacent letters is one spanning line.** Exception form: `(x)(y)` (§6.1).

### 9.3 Audit log

| Date | Convention | Finding |
|---|---|---|
| v2 → v2.2 | 2 (word-final ē) | **Wrong.** Stated "conventional yodh–ʾālap̄ writing." East Syriac writes ܹܐ — zlāmā qašyā + ʾālap̄, no yodh. Detected against ܥܵܠܡܹ̈ܐ, ܚܛܵܗܹ̈ܐ, ܚܲܝܹ̈ܐ, ܡܝܼܬܹ̈ܐ. Corrected. |
| v2 → v2.2 | 1 (word-final ā) | Verified against ܐܲܠܵܗܵܐ, ܪܘܼܚܵܐ, ܡܵܪܝܵܐ, ܥܹܕ݁ܬܵܐ, ܒܬ݂ܘܼܠܬܵܐ. Held. |
| v2.2 pass 2 | 1, 2 | Re-verified against the expanded Creed. New cases: internal `ēʾ` (ܠܡܹܐܬ݂ܵܐ), `ēy` (ܡܵܘܕܹ݁ܝܢܲܢ, ܐܵܡܹܝܢ), word-final `ē` (ܥܵܠܡܹ̈ܐ, ܕܲܚܛܵܗܹ̈ܐ, ܕܦܲܓ݂ܪܹ̈ܐ). Both held. |
| v2.2.2 → v2.2.3 | 1, 2 | Re-verified against the Abun across three witnesses. Both held. New case: word-final `e` + ʾālap̄ (`tēʾteʾ`, `nehweʾ`), outside both conventions; resolved by the §4.2 note without adding a convention. |
| v2.2.3 → v2.2.4 | 1, 2 | Re-verified against the Tešbōḥtā lʾalāhā. Both held. No new case reached. |
| v2.2.4 → v2.3 | 1, 2 | Re-verified against the corrected Abun (22 lines, source of record). Word-final `ā` in *dbašmayā, šmaÿā, laḥmā, bīšā, ʾarʿā, nāš̈ā*; word-final `ē` in *ʿīr̈ē*. Both held. |
| v2.2.4 → v2.3 | 5 (new) | Introduced on the attestation of `šba(q_n)`, one line spanning qoph and nun in the Abun. Exception form `(x)(y)` declared; not yet needed. |
| v2.3 → v2.3.1 | 1, 2 | Re-verified across all three confirmed texts at once — Creed 21 lines, Abun 22, Tešbōḥtā 3, 226 tokens. Every canonical string reproduced mechanically from the Syriac; both conventions held with no new case reached. |

---

## 10. Scope

### In scope
Consonants, vowel points, bgdkpt pointing, syāmē, the occultans line, the distinguishing point, two dots below (§17), the breve below (§18), matres, source parentheses.

### Out of scope at word level
**Out-of-scope characters are removed at ingestion (§16.1), not carried in the stored line.** The confirmed text contains in-scope orthography only.

- **Punctuation.** The Syriac punctuation repertoire (U+0700–U+070D) and any Latin substitute a typist has used for it. Clause division is carried by line breaks and visual layout. Where a particular working file needs punctuation for reading, it is added there by hand; it is not part of the confirmed text and no entry records it.
- **Accent and cantillation points.** None has been encountered in this project's sources.
- **Abbreviation and numeral marks.**
- **Scribal correction marks and marginalia.**
- **Presentational characters.** Tatweel / kashida elongation (ـ), zero-width joiners and non-joiners, and line-fill strokes. Artifacts of justification and typesetting, not orthography. ܒܝܵـܘ̈ܡܲܝ is ingested as ܒܝܵܘ̈ܡܲܝ and transliterates `byāẅmay`.

**Consequence for the parse field.** Because ingestion removes out-of-scope characters before anything else runs, the stored line and the canonical string agree at every point, and the round-trip (§12) has nothing to except. The exclusion record of General Rules §10.8 therefore has **no current instances** — the two tatweel notes that formerly held it are retired with this rule. The provision remains for the case it was written against: a mark that survives ingestion because it *is* in scope, yet cannot be represented. None is known.

A word's canonical string is reversible **with respect to its segmental and vocalic orthography**, which after ingestion is the whole of what the stored line contains.

### Legibility
Marks that cannot be read are not reconstructed and not invented. No notation is provided for illegible pointing: the sources of record are printed and digital, which do not produce it, and an unreadable mark in a liturgical text is dealt with case by case rather than encoded.

---

## 11. Search Keys

The canonical string is diacritic-heavy. Each glossary headword therefore carries **two** search keys, both non-authoritative and never used for decisions, citation, or display.

### 11.1 Exact key

Mechanically generated, reversible, case-sensitive. For machine comparison.

| Canonical | ASCII |
|---|---|
| ʾ | `'` |
| ʿ | `` ` `` |
| ḥ ṭ ṣ š | `H T S C` |
| marked hard bgdkpt | `b! g! d! k! p! t!` |
| marked soft bgdkpt | `b~ g~ d~ k~ p~ t~` |
| unmarked bgdkpt | `b g d k p t` |
| a e | `a e` |
| ā ē ī ō ū | `A E I O U` |
| defective (breve above) | append `*` → `A* E* I* O* U*` |
| syāmē | `#` after carrying letter |
| two dots below (§17) | `:` after carrying letter |
| breve below (§18) | `%` after carrying letter |
| superscript ʾālap̄ | `@` before carrier |
| `( )` `-…-` `^` `_` `^^` `__` | unchanged |

Where a letter carries both a defective vowel and syāmē, the defective marker precedes: `A*#`.

Example: `qaḋīštā` → `qad!ICtA`

### 11.2 Fold key

**One per headword.** Lowercase; all diacritics stripped; `ʾ` and `ʿ` dropped; notation characters dropped. Written in the entry as `(search: alaha)`.

Deliberately ambiguous. Collisions are expected and acceptable — `brā` "Son" and `brā` "he created" both fold to `bra`, and a reader distinguishes them at a glance. This key exists so that a human can find a form by typing what it sounds like.

---

## 12. Round-Trip Validation

A canonical string is **valid** if and only if:

1. Unwrapping all `(…)` and `-…-` spans and applying the inverse tables reproduces the source pointing **exactly**, after the source has been normalized per §16 and setting aside anything excluded under §10 and recorded per General Rules §10.8; and
2. No two distinct entries in the glossary share a canonical string *and* a root.

Condition 2 is the injectivity check. Violations are one of:
- a transliteration error, or
- a genuine homograph, which must be separated by the root field.

**One known asymmetry.** A spanning occultans line (§6.1) is recorded in the string but cannot be distinguished from two separate lines in the encoded source. Round-trip cannot detect a failure of that convention; only the page can.

This test is mechanical and should be automated in the eventual SQLite pipeline.

---

## 13. Difference from the Old Clean-Glossary

The project rebuilds the glossary from scratch in the new format rather than converting the old one; the old Clean-Glossary is kept only for reference.

| Change | Effect |
|---|---|
| Gemination dropped | `qaddīšā` → `qaḋīšā`; doubling not recorded at all |
| Three-state bgdkpt | inferred-soft forms must be re-checked against the page |
| Class B matres | internal `ā`/`ē` with mater respelled (`āʾ`, `ēy`, `ēʾ`) |
| Class A breve | forms with defective spelling respelled |
| Syāmē marking | all plural forms gain a carrier diaeresis, NFC ordered |
| Tier 3 root blocks | dissolved; root becomes a field on each word entry |
| Capitalization | canonical string fully lowercase; case lives on the English side |
| Parse field | reduced to exclusion records only, of which there are currently none |

---

## 14. Resolved and Withdrawn

v2.2.4 carried four open questions. All are closed in v2.3. This section is retained as the record; nothing here is open.

1. **Illegible pointing** — *no notation, deliberately.* The sources of record are printed and digital and do not produce unreadable marks. Handled case by case if it ever arises. See §10, Legibility.
2. **Unlocatable pointing** — *resolved.* The mark in *šbaqn* was not a point of ambiguous carrier but an occultans **line spanning two letters**, above, covering qoph and nun. Notation in §6.1; convention 5 in §9.2. The separate question of a point standing *between* two letters is a real page-state and is now §7's `^^` / `__`, attested in `qā^^ʿēyn`.
3. **Two dots below** — *resolved.* Now §17.
4. **Breve below on pe** — *resolved.* Confirmed as an arc, graphically distinct from rūkkākā, and carrying no accompanying rūkkākā dot. Now §18.

---

## 15. Rule Status

### Exercised against worked text

Validated by full round-trip on the Creed (two passes):

- **Three-state bgdkpt** — all three states attested in one text.
- **Class B matres** — internal `āʾ` `ēʾ` `ēy` and the word-final ā/ē conventions.
- **Syāmē on varied carriers** — resh, mem, yodh, waw, hē, taw; including carrier-plus-vowel (§5.2).
- **The distinguishing point** — `m_n`, six occurrences, distinct from `man`.
- **Source parentheses** — `-waḇrā-`.

Extended by the Abun d-ba-Shmayā (three witnesses, then the source of record):

- **The occultans line on one letter** (§6) — `w(ʾ)nāš̈ā`, `(h)ī`.
- **The occultans line spanning two letters** (§6.1) — `šba(q_n)`.
- **The single point below** (§7) — on a qoph, a carrier the Creed never exercised.
- **The point above between two letters** (§7) — `qā^^ʿēyn`.
- **Word-final `e` + ʾālap̄** (§4.2) — `tēʾteʾ`, `nehweʾ`.
- **Codepoint normalization** (§16) — four witnesses, three conventions, reconciled to one page-state reading.
- **§16.2** — U+0716 under syāmē in `ʿīr̈ē`, normalized to resh.
- **§5.1** — the 220/230 split, verified across the Glossary; two 230+230 pairs required manual ordering and nineteen 220+230 pairs did not.

Extended by the corrected texts, verified as a set (226 tokens, three texts):

- **Full mechanical reproduction.** Every canonical string in all three confirmed texts regenerates from the pointed Syriac using §§3–7 and §9.2 alone. This is the strongest test the rules have been put to, and it passed without exception.
- **`^^`** (§7) — `qā^^ʿēyn`, a point above standing between qoph and ʿē.
- **The spanning occultans line** (§6.1) — `šba(q_n)`, one line covering qoph and nun, with the §7 point below on the qoph inside the span.
- **§16.2** — U+0716 under syāmē in `ʿīr̈ē`, normalized to resh.

Extended by the Tešbōḥtā lʾalāhā:

- **§16.1 across a whole witness** — U+073F for every single point above and U+073C for every single point below, resolved by carrier throughout. Read at face value it yields *tešbōōḥtā*, *saḇĭrā*.

### Untested — treat as provisional

- `ă` / `ĕ` (§4.2) — no defective word-final ā or ē encountered.
- `ŏ` / `ŭ` / `ĭ` (§4.1) — no defective carrier-borne vowel encountered.
- `(_x)` and `(_xy)` (§6) — line below not yet on a securely located carrier in confirmed text.
- `__` (§7) — point below between two letters not yet encountered.
- `ᵃ` (§3.1) — superscript ʾālap̄ not encountered.
- `:` (§17) and `%` (§18) — attested only in **unconfirmed** Hudra material; confirm against a source of record before treating as exercised.
- `(x)(y)` (§9.2 conv. 5) — the exception form has not been needed.

### Known font limitation

U+1DF8, the encoding for a point above between two letters (§7), is absent from Meltho and from Noto Sans Syriac. Editors will show a placeholder glyph. The data is correct; the display is not. A Unicode-aware editor able to render characters as individual spacing glyphs will show the mark plainly.

---

## 16. Source Ingestion — Codepoint Normalization

Digital witnesses do not agree on which codepoint encodes a given mark. They encode by *appearance* — "a dot below" — using whatever renders correctly in their font. The canonical string records the page, so ingestion must map codepoints to page-states before §§3–7 apply.

Four witnesses of the Abun used three conventions:

| Page-state | Witness 1 / 3 | Witness 2 | Witness 4 |
|---|---|---|---|
| rūkkākā | U+0742 RUKKAKHA | U+073C HBASA-ESASA DOTTED | U+073C |
| qūššāyā | U+0741 QUSHSHAYA | U+073F RWAHA | U+073F |
| single point below (§7) | U+0323 COMBINING DOT BELOW | U+0742 RUKKAKHA | U+0742 |

Note that U+0742 means rūkkākā in one convention and the §7 point in another. Reading codepoints at face value across witnesses produces silent corruption, not an error.

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

**Bare U+0716 normalizes to resh and raises a flag.** Of 999 occurrences across the patristic corpus, 954 carry syāmē; the 45 bare cases fall in words that plainly want a resh, in files that encode resh correctly elsewhere. The reading is secure. The flag exists because what is being normalized is a *source error*, and a source that carries typing errors is a fact worth knowing about the source. If a bare U+0716 ever falls where dalath is lexically possible, the flag is the only thing between the project and a silent letter substitution.

### 16.3 Combining-mark order

Normalize to the §5.1 order before comparison or round-trip validation (§12). In practice this means checking pairs of **class 230** marks only; a 220 mark against a 230 mark is ordered by NFC without intervention.

### 16.4 Per-block ingestion

**The audit runs per block, not per file.** A single file may carry more than one codepoint convention, split along a textual seam — pasted-in psalm verses, a quoted Father, an interleaved rubric — because the compiler drew the blocks from different digital sources.

Detected in a Hudra unit on the three Doctors: the hymn body encodes rūkkākā as U+0742 and qūššāyā as U+0741, while the interleaved Psalm 34 verses encode the same two marks as U+0323 and U+0307. The split follows the seam exactly.

Audit each block whose provenance may differ, and record where the seams fall.

### 16.5 Witness collation

Ingestion is per-witness. Where witnesses disagree after normalization, the disagreement is textual and belongs to the source hierarchy (General Rules §1), not to this file.

**Do not resolve by majority vote.** Witnesses sharing a codepoint convention frequently share an ancestor and therefore share errors, so a vote counts copies rather than readings. In the Abun collation the lone dissenting witness was correct on every contested point where the majority was overruled, and the printed source of record overruled all three digital witnesses — including on the syāmē of ܕܒܲܫܡܲܝܵܐ, where every digital witness carried a mark the page does not.

### 16.6 West Syriac vowel codepoints — refused, never mapped

The East Syriac vowels are the **dotted** forms: U+0732, U+0735, U+0738, U+0739, U+073C, U+073F. The West Syriac equivalents are separate characters: U+0730, U+0731, U+0733, U+0734, U+0736, U+0737, U+073A, U+073B, U+073D, U+073E.

**These are never normalized into East Syriac vowels.** A West Syriac sign is a different mark, not a different encoding of the same mark, and mapping one to the other fabricates a reading the page does not contain.

- **In a source of record:** raises a flag. Either the source is not what it was taken to be, or the block has a seam (§16.4).
- **In a corpus search:** expected and harmless, but the token is West-vocalized and **carries no evidence about pointing**. Distribution and lexical range may be cited from it; a vowel or a bgdkpt point may not. The patristic corpus is overwhelmingly West-vocalized apart from Narsai, so this is the ordinary case, not the exception.

### 16.7 Unrepresentable page-states

A spanning occultans line (§6.1) is encoded U+0747 on both letters because no single character exists for it. The encoded source is therefore lossy at that point, and the canonical string carries information the stored Syriac does not. This is the only known case; it is recorded here so that a mismatch between string and source at such a word is recognized as expected rather than treated as an error.

---

## 17. Two Dots Below

Two dots beneath a letter, distinct from zlāmā by shape and environment.

**Notation:** combining diaeresis below (U+0324) on the transliterated letter — `ẗ` above for syāmē, `t̤` below for this. The two are deliberately symmetric: the string mirrors the page.

**Encodings normalized to this page-state:** U+0324, U+0740 SYRIAC FEMININE DOT, U+0744 SYRIAC TWO VERTICAL DOTS BELOW. In East Syriac and Estrangela the feminine dot takes the form of two dots below, which is why the Syriac-specific codepoint and the generic one both occur for one appearance.

**Function is not recorded.** On the final taw of a 3fs perfect the mark is the feminine dot in the ordinary grammatical sense; on waw and hē in the pronouns it is evidently something else. Both are the same mark on the page, and §§6–7's graphical principle applies: position and shape are enough to write it, and identification is not a prerequisite for transcription.

Attested on taw (*zāʿat, naṭrat, ʾagnat, negdat, ʾeṫtnīḥat*), on waw and hē (*hū, hī, hwā, hwaw, hwaytōn*), and on ʾālap̄ — 14+ occurrences across five Hudra texts, all **unconfirmed**. Confirm against a source of record before treating as exercised.

ASCII: `:` after the carrying letter.

---

## 18. The Breve Below

An arc beneath a letter, opening downward. Graphically distinct from rūkkākā, which is a dot.

**Notation:** combining breve below (U+032E) on the transliterated letter — `p̮`. Encoded U+032E at source, so ingestion passes it through unchanged.

**No collision.** Every other mark in the system occupies a different position or shape: macron above for soft `p̄` and `ḡ`, macron below for soft `ḇ ḏ ḵ ṯ`, breve *above* for the defective vowels `ă ĕ ĭ ŏ ŭ`, dot above for hard, diaeresis above for syāmē, diaeresis below for §17. The space below a pe is free precisely because pe is one of the two letters whose soft form takes a macron above.

Attested only on **pe**, in a narrow lexical environment — *napš̮ā*, *napš̮āṯā*, *takšap̮tā* — eight occurrences across the Hudra texts and Ps 97:22, all **unconfirmed**. In every case the pe carries the arc **and no rūkkākā dot**; earlier project transliterations writing `p̄` in these words recorded an inference, not the page.

ASCII: `%` after the carrying letter.
