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
- **Canonical Unicode form.** The canonical Latin string is stored in NFC. A canonically equivalent decomposed Latin string is not a second accepted spelling.

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

Case is not a feature of the Syriac page. The **Syriac-derived transliteration is lowercase**; all capitalization of Syriac words belongs to the English layer. Māryā is written `māryā` in the canonical string and capitalized only on the English side. Literal editorial apparatus (§2) is not Syriac-derived transliteration and preserves its supplied case exactly, e.g. `(Assyrian Ferial adds:)`.

---

## 2. Notation Beyond the Letter Tables

Editorial apparatus is preserved literally alongside the letter-for-letter mapping.

| Notation | Meaning | On reversal |
|---|---|---|
| `(x)` | one-letter line above (§6.1) | restore U+0747 on that letter |
| `(_x)` | one-letter line below (§6.1) | restore U+0748 on that letter |
| `x⁀y` | one physical two-letter line above (§6.2) | restore U+035E after the first Syriac base |
| `x‿y` | one physical two-letter line below (§6.2) | restore U+035F after the first Syriac base |
| `[…]` | editorial addition or alternate | preserve the brackets |
| `(English label:)` | source or witness label | preserve the label |

`⁀` is U+2040 CHARACTER TIE. `‿` is U+203F UNDERTIE. They are canonical transliteration symbols, not combining marks on the Latin letters.

Syriac inside editorial brackets transliterates normally. English-only interpretive brackets have no transliteration counterpart.

Example: `ʾaḇā [waḇrā] nāpēq`

### 2.1 Parenthesis grammar

Parentheses have two in-scope uses, so the inverse grammar must distinguish them mechanically.

- A parenthetical payload that parses **completely as exactly one canonical Syriac letter-unit**, optionally preceded by `_` for a line below, is one-letter line notation (§6.1).
- Any other balanced parenthetical payload is editorial apparatus and is preserved literally, **except** a retired two-unit line wrapper such as `(mn)` or `(_mn)`, which is invalid canonical transliteration and must be migrated to direct span encoding plus `⁀`/`‿` notation.

Therefore an editorial label whose entire contents would itself be legal one-letter line syntax is ambiguous and is prohibited until disambiguated. For example, literal editorial `(h)` cannot coexist with the one-letter line notation `(h)` as two meanings of the same canonical string. Ordinary source labels such as `(Witness A: 2)` and `(Assyrian Ferial adds:)` are unambiguous and remain literal.

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
| yodh + U+073C ḥḇāṣā sign | ḥḇāṣā | `ī` |
| waw + U+073F rwāḥā sign | rwāḥā | `ō` |
| waw + U+073C rḇāṣā / ʾeṣāṣā sign | rḇāṣā / ʾeṣāṣā | `ū` |

These identities are established by the **normalized mark itself**, not from the fact that a dot happens to sit on yodh or waw. A generic U+0307/U+0323 point on either carrier remains the §7 single point and transliterates as `^`/`_`.

**There is no carrierless Class-A notation.** `ĭ`, `ŏ`, and `ŭ` are not valid canonical symbols. An explicit U+073C/U+073F on an impossible carrier is **flagged at ingestion, not repaired by inference**. Establish the page-state from the witness before confirming any such form (§16).

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

#### Exact boundary of the final-mater shorthand

The implied-final-ʾālap̄ convention suppresses **only a bare final ʾālap̄ immediately following its zqāpā or zlāmā-qašyā carrier, with no editorial delimiter between the two letters and with no U+035E/U+035F span joining the carrier to that ʾālap̄**. This restriction is required for reversibility.

- `[ܡܵܐ]` → `[mā]`
- `ܡܵ[ܐ]` → `mā[ʾ]`
- `[ܡܵ]ܐ` → `[mā]ʾ`
- `[ܡܵ][ܐ]` → `[mā][ʾ]`
- a final ʾālap̄ carrying any in-scope mark is explicit, never suppressed
- a final ʾālap̄ that is the second base of a two-letter span is explicit, because `⁀`/`‿` must stand between two visible canonical letter-units

The inverse inserts the implied bare ʾālap̄ immediately after the final vowel carrier, so editorial placement is reconstructed exactly.

**Word-final `e` (and `a`) followed by a written ʾālap̄.** `a` and `e` take no matres, but a written ʾālap̄ is still a letter on the page and is recorded as `ʾ` per §3.1 — it is not analyzed as a mater. Nothing else in the system produces word-final `eʾ`, so the sequence is unambiguous and reverses cleanly. Worked: `tēʾteʾ`, `nehweʾ` (Our Father).

**Two dots below is not always a vowel.** The same page position carries the mark of §17. Distinguish by shape: zlāmā is two dots level or angular; §17's mark is the two-dot mark that is neither.

#### Verified double-vowel page-states

A carrier may bear **two distinct East Syriac vowel page-states** when the audited page actually shows both. This is unusual and therefore remains a page-check condition, but it is not intrinsically contradictory and is not a reason to delete either mark after confirmation.

Canonical serialization is mechanical and begins with the normalized Syriac mark order of §5.1:

- raw witnesses carrying the same two supported marks in different codepoint orders normalize to **one canonical Syriac sequence first**;
- a Class-A carrier-vowel symbol (`ī`, `ō`, `ū`) is written once, followed in Latin by the Class-B vowel sign on that same carrier;
- two distinct Class-B signs on one carrier are written consecutively in their normalized Syriac order;
- this includes equal-CCC pairs such as `e+ē` and `a+ā`, and equal-CCC Class-A/Class-B pairs such as `ī+e` and `ō+a`;
- the attested spelling `ܐܝܼܵܠܵܐ` therefore gives `ʾīālā`, with `ܝܼܵ` → `īā`.

The final-mater convention applies to the vowel cluster as a whole. Where a final double-vowel carrier contains zqāpā or zlāmā qašyā and has no following bare ʾālap̄, the last such eligible vowel receives the existing `ă`/`ĕ` exception form. With the bare final ʾālap̄ present, the ordinary `ā`/`ē` form remains and the ʾālap̄ is suppressed under the usual convention.

The page-state checker continues to flag more than one vowel on one carrier so the source is deliberately verified before confirmation. That diagnostic is **nonblocking for normalization persistence and canonical transliteration** because the complete two-vowel page-state is representable; human page verification is still required before the text is confirmed. Duplicate identical marks remain invalid. Three or more vowel page-states on one carrier remain unsupported until attested and explicitly specified.

One state is still specifically contradictory under the present grammar: the same waw carrying both Class-A U+073C (`ū`) and U+073F (`ō`). A single Latin carrier unit cannot encode that state injectively without colliding with two separate waw carriers, so it remains blocking pending an attested need and an explicit notation extension.

### 4.3 Diphthongs

True diphthongs preserve the consonantal carrier: `aw`, `ay`.
Distinguished from `ō`/`ū`/`ī`, where the carrier bears the vowel point.

A written yodh after `ē` and a consonantal yodh are the same page-state and receive the same string; the analysis is not recorded.

### 4.4 Unpointed consonants

A consonant written with **no vowel point** is transliterated as the bare consonant. This is a page-state, not an assertion of vocal shewa. Inferred but unwritten vowels are not recorded.

---

## 5. Syāmē and Canonical Mark Serialization

Syāmē are a page-mark and must be represented.

**Notation:** combining diaeresis (U+0308) over the **carrying letter**.

- `ber̈yāṯā` — syāmē carried by the resh
- `ber̈yāṯā` ≠ `beryāṯā` — the second asserts no syāmē on the page

Placement follows the page strictly and is not normalized to a conventional position.

### 5.1 Syriac mark order — the general rule

Where a Syriac letter carries more than one combining mark, storage order is deterministic. **Every supported normalized mark has one explicit project rank.** Raw codepoint order in a digital witness never creates a second canonical spelling.

The rank is globally compatible with Unicode canonical combining classes: lower CCC values necessarily precede higher ones under NFC, and the project rank fixes the order of every supported mark that shares a CCC. After the project ordering is applied, store the result in **NFC**.

The complete in-scope rank is:

| Rank | CCC | Normalized mark | Project identity |
|---:|---:|---|---|
| 1 | 36 | U+0711 | superscript ʾālap̄ |
| 2 | 218 | U+1DFA | §7 point below between this carrier and the next |
| 3 | 220 | U+073C | Class-A `ī`/`ū` carrier-vowel mark |
| 4 | 220 | U+0738 | zlāmā pšīqā `e` |
| 5 | 220 | U+0739 | zlāmā qašyā `ē` |
| 6 | 220 | U+0742 | rūkkākā |
| 7 | 220 | U+0323 | §7 generic point below on the carrier |
| 8 | 220 | U+0324 | two dots below (§17) |
| 9 | 220 | U+032E | breve below (§18) |
| 10 | 220 | U+0748 | one-letter line below (§6.1) |
| 11 | 228 | U+1DF8 | §7 point above between this carrier and the next |
| 12 | 230 | U+073F | Class-A `ō` carrier-vowel mark |
| 13 | 230 | U+0732 | pṯāḥā `a` |
| 14 | 230 | U+0735 | zqāpā `ā` |
| 15 | 230 | U+0741 | qūššāyā |
| 16 | 230 | U+0307 | §7 generic point above on the carrier |
| 17 | 230 | U+0308 | syāmē |
| 18 | 230 | U+0747 | one-letter line above (§6.1) |
| 19 | 233 | U+035F | lower two-letter span (§6.2) |
| 20 | 234 | U+035E | upper two-letter span (§6.2) |

The sequence is a **storage convention, not a claim about phonological or visual priority**. In particular, U+1DFA/U+1DF8 are between-letter page-states semantically but occupy CCC 218/228 in Syriac storage; their later Latin placement is governed separately by §5.3.

A newly supported combining mark may not simply be added to the accepted inventory. It must be assigned one explicit place in this table, and the permutation regressions must prove that all raw orders converge to the same normalized Syriac sequence. This is what makes equal-CCC double-vowel states canonical rather than merely reversible in whichever source order happened to arrive.

After §16 has normalized source codepoints to page-states, two canonically equivalent witnesses containing the same supported marks must therefore produce the same combining sequence before comparison or round-trip validation.

### 5.2 Syāmē against a vowel on the same letter

- **Carrier-borne vowel (`ī`, `ō`, `ū`).** The vowel sits on the mater and is written as a precomposed letter; syāmē follows it: `ī̈`, `ō̈`, `ṻ`. Worked: `ʾī̈dāwhy`.
- **Consonant-borne vowel (`a`, `e`, `ā`, `ē`).** The vowel is a separate letter following the consonant; syāmē attaches to the consonant and therefore stands **before** the vowel letter: `m̈ē`, never `mē̈`. Worked: `ʿālm̈ē`, `ḥaÿē`, `paḡr̈ē`, `lmīẗē`, `daḥṭāḧē`, `šmaÿā`, `nāš̈ā`.

### 5.3 Canonical Latin unit order

For inversion to have one grammar, all marks belonging to one Syriac carrier serialize in this order:

1. superscript ʾālap̄ `ᵃ`, if present;
2. the consonant/bgdkpt/carrier-vowel symbol with graphical combining marks (§§5, 17, 18), stored in NFC;
3. §7 point **on** the carrier — below `_` before above `^` if both occur;
4. the Class-B vowel sign or signs, if present, in normalized Syriac mark order (§§4.2, 5.1);
5. §7 point **between** this carrier and the next — below `__` before above `^^` if both occur;
6. a one-letter line wrapper (§6.1), if present, surrounds that complete one-letter unit;
7. a two-letter span tie (§6.2), if present, follows the complete first unit and precedes the complete second unit: upper `⁀`, lower `‿`.

Examples already in force follow this order: `m_n`, `qā^^ʿēyn`, `šbaq_⁀n`.

---

## 6. One-Letter Lines and Two-Letter Spans

The project distinguishes **where the physical line is drawn** before asking what traditional function it serves. A line belonging to one letter and one physical line joining two letters are different normalized Syriac page-states and therefore different canonical transliterations.

### 6.1 One-letter line

A line clearly belonging to one letter is recorded as a one-letter line. The same graphic stroke is traditionally described with names such as *mṭalqānā* and *mhaggyānā* in different functions. **The canonical string records the visible one-letter mark and does not infer its phonological function merely from the stroke.**

| Page-state | Normalized Syriac | Notation |
|---|---|---|
| line above one letter | U+0747 on that letter | `(x)` |
| line below one letter | U+0748 on that letter | `(_x)` |

- `md(n)ītā` — the nun is on the page carrying a one-letter line
- `w(ʾ)nāš̈ā`, `(h)ī` — prosthetic ʾālap̄ and enclitic hē, each carrying a one-letter line above

The `_` at the head of the wrap marks a line below and cannot be confused with §7's `_`, which always follows its carrier.

Two adjacent one-letter lines remain two marks: `(x)(y)` or `(_x)(_y)`. Their adjacency never creates a span automatically.

### 6.2 Two-letter spanning line; attested marheṭānā

Unicode's general-use double-diacritic mechanism supplies a direct normalized encoding for one physical line spanning two adjacent bases. The combining mark is stored after the **first** base and extends over the immediately following base.

| Page-state | Normalized Syriac | Notation |
|---|---|---|
| one line above spanning two letters | U+035E COMBINING DOUBLE MACRON after the first base | `x⁀y` |
| one line below spanning two letters | U+035F COMBINING DOUBLE MACRON BELOW after the first base | `x‿y` |

The Latin tie is deliberately not parenthetical. Both consonants remain visibly part of the word, and the tie records that the page joins them with one physical line.

**Attested marheṭānā:**

- `ܫܒܲܩ̣͞ܢ` → `šbaq_⁀n` — one upper line spans qoph and nun; qoph also carries the §7 point below. On the confirmed page this is marheṭānā marking the pronounced vowelless `qn` cluster. Neither qoph nor nun is omitted in pronunciation.

The span must **not** be collapsed to a one-letter line on qoph. That would change the page-state and would falsely erase the joining relation shown by the source.

The project may call an upper span *marheṭānā* where its function is established from the source and linguistic context, as in `šbaq_⁀n`. A future span whose function is not securely established is still encoded graphically with U+035E/U+035F and transliterated with `⁀`/`‿`; the notation itself does not invent a function.

### 6.3 Raw witness ambiguity versus canonical storage

**Canonical normalized Syriac is not ambiguous about span versus separate.**

- U+035E/U+035F after the first base = **one physical two-letter span**.
- U+0747/U+0748 on two adjacent bases = **two separate one-letter lines** in canonical confirmed storage.

A raw digital witness may nevertheless approximate one printed spanning line by repeating U+0747 or U+0748 on both letters. Such a raw sequence is therefore a **page-check condition at ingestion**, not a second canonical encoding of a span. Compare against the page:

- if the page has one physical span, canonicalize the page-state to U+035E/U+035F on the first base;
- if the page has two separate one-letter lines, retain the two U+0747/U+0748 marks.

The transliteration engine receives only the resolved normalized Syriac. It takes **no external span/separate metadata** and never asks the stored Latin to decide the Syriac page-state.

A two-letter span may not cross an editorial square-bracket boundary. If a page ever establishes a span across editorial material, the notation must be extended explicitly rather than guessed.

---

## 7. The Single Point

A single point above or below a letter, or standing between two letters, that is **not** identifiable as a vowel sign or a bgdkpt point.

The test is positional, not functional. Purpose is not recorded.

**Identity is direct, not carrier-inferred.** The canonical Syriac codepoint records which point the page audit has established. A carrier never changes that identity automatically:

| Normalized mark | Identity |
|---|---|
| U+0307 COMBINING DOT ABOVE | §7 generic point above |
| U+0323 COMBINING DOT BELOW | §7 generic point below |
| U+0741 SYRIAC QUSHSHAYA | qūššāyā (§3.2) |
| U+0742 SYRIAC RUKKAKHA | rūkkākā (§3.2) |
| U+073F SYRIAC RWAHA | rwāḥā `ō` on waw (§4.1) |
| U+073C SYRIAC HBASA-ESASA DOTTED | `ī` on yodh or `ū` on waw (§4.1) |

U+0307/U+0323 remain §7 even on bgdkpt, waw, or yodh. Conversely, U+0741/U+0742/U+073F/U+073C are not converted to generic points merely because they occur on an unexpected carrier; that is a page-state problem to review. If a digital witness has used the wrong point codepoint as a visual approximation, the **human page audit corrects the canonical Syriac codepoint before confirmation** (§16). The normalizer does not guess the intended identity from the carrier.

A point standing **between** two letters is never a vowel or a bgdkpt point, whatever the letters are, and is always §7.

| Page-state | Notation |
|---|---|
| point above the carrying letter | `^` |
| point below the carrying letter | `_` |
| point above, between this letter and the next | `^^` |
| point below, between this letter and the next | `__` |

**Placement against a vowel.** A marker for a point *on* a letter follows the decorated carrier and precedes the Class-B vowel. A marker for a point *between* letters follows the whole carrier-plus-vowel unit. Where both above and below occur in the same position, below precedes above as fixed by §5.3: on-letter `_^`, between-letter `__^^`.

Worked: ܡ̣ܢ → `m_n`, distinct from ܡܲܢ → `man`. · ܩ᷸ܵܥܹܝܢ → `qā^^ʿēyn` (Our Father), the point standing between qoph and ʿē.

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

1. **Word-final `ā` implies a bare immediately-following mater ʾālap̄ in the same editorial sequence.** Exception form: `ă`. Exact boundary: §4.2.
2. **Word-final `ē` implies a bare immediately-following mater ʾālap̄ in the same editorial sequence.** Exception form: `ĕ`. An explicitly written yodh gives `ēy` and is not an exception. Exact boundary: §4.2.
3. **Prosthetic ʾālap̄ is written `ʾ`** and requires no special mark. *(No exception form needed: this is a letter mapping, not a prediction.)*
4. **Word division follows the source.** Prefixed particles are written solid unless the source separates them. Editorial brackets do not divide words. The canonical string never strips proclitics; the glossary may index a headword with them stripped, but that is a glossary convention and does not touch the string.
5. **Retired as a predictive convention.** Adjacent one-letter line marks never imply a span. Canonical normalized Syriac encodes a two-letter span directly with U+035E/U+035F (§6.2); repeated U+0747/U+0748 therefore remains separate in confirmed storage (§6.3).

### 9.3 Reserved

Reserved.

---

## 10. Scope

### In scope
Consonants, vowel points, bgdkpt pointing, syāmē, one-letter line marks and page-confirmed two-letter spanning lines (§6), the distinguishing point, two dots below (§17), the breve below (§18), matres, and project editorial apparatus (§2).

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

Each glossary headword carries **one additional, non-authoritative fold key**. It is lowercase; all diacritics are stripped; `ʾ` and `ʿ` are dropped; notation characters `^ _ ( ) [ ] ⁀ ‿` are dropped. It is written in the entry as `(search: alaha)`.

The fold key is deliberately ambiguous. Collisions are expected and acceptable — `brā` "Son" and `brā` "he created" both fold to `bra`, and the root field separates their entries. This key exists only so that a human can find a form by typing an approximate Latin spelling. It is never used for identity, decisions, citation, or display.

---

## 12. Round-Trip Validation

A canonical string is **valid** if and only if:

1. Applying the inverse tables while preserving §2 editorial apparatus literally reproduces the normalized Syriac block **exactly**, setting aside anything excluded under §10 and recorded per General Rules §10.8; and
2. No two distinct entries in the glossary share a canonical headword string, root, *and* `{...}` morphology.

Condition 2 is the Glossary-identity check. A collision means either an entry has been duplicated or the morphology/root analysis has not yet separated two genuinely distinct forms.

**No span/separate asymmetry remains.** One physical two-letter span and two separate adjacent one-letter lines are different normalized Syriac strings and different canonical Latin strings:

- `ܡ͞ܢ` ↔ `m⁀n`
- `ܡ݇ܢ݇` ↔ `(m)(n)`

Round-trip validation therefore proves the encoded grouping as well as the letters and marks. The source-page audit is still required at ingestion to establish which normalized page-state the witness actually shows; it is not supplementary metadata to transliteration.

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

Digital witnesses may use an inappropriate Unicode point codepoint as a visual approximation. Canonical normalization therefore establishes **page-state first**, but it does **not** reinterpret a single point from the letter carrying it. Reading the carrier as a semantic disambiguator is prohibited. Where the digital encoding and the printed page disagree, the human page audit corrects the canonical Syriac codepoint before confirmation.

### 16.1 Normalize to page-state

The six in-scope single-point codepoints retain direct identities:

- **U+0307** — generic single point above (§7), on any carrier;
- **U+0323** — generic single point below (§7), on any carrier;
- **U+0741** — qūššāyā (§3.2);
- **U+0742** — rūkkākā (§3.2);
- **U+073F** — rwāḥā (§4.1);
- **U+073C** — ḥḇāṣā / rḇāṣā-ʾeṣāṣā carrier-vowel mark (§4.1).

There is **no automatic conversion among these six marks**. An explicit semantic mark on an impossible carrier is retained and flagged by the page-state checker; a generic U+0307/U+0323 remains generic on bgdkpt, waw, and yodh. If a raw witness encoded a visually similar but semantically wrong point, page review supplies the correction before transliteration.

Multi-dot signs (U+0732 pṯāḥā, U+0735 zqāpā, U+0738 zlāmā pšīqā, U+0739 zlāmā qašyā) are unambiguous single codepoints and pass through unchanged.

A normalized carrier with two distinct vowel signs is likewise retained exactly after §5.1 has canonicalized their ordering. The page-state audit flags the stack for human verification, but the diagnostic is nonblocking for normalization persistence and canonical transliteration because the complete state is represented; ingestion never deletes one vowel merely because another is present. Duplicate identical marks, three-or-more vowel states, and the conflicting dual-Class-A waw state remain blocking as specified in §4.2 and §16.7.

**Removed at ingestion, before any other step.** Out-of-scope characters (§10) never enter the stored line:

- Syriac punctuation **U+0700–U+070D**, the abbreviation mark **U+070F**, and any Latin character standing in for them — a full stop, comma, colon, or semicolon inside a Syriac line is a typist's substitute, not the page's mark, and is removed on the same footing.
- Tatweel **U+0640**, zero-width joiner **U+200D**, zero-width non-joiner **U+200C**, and line-fill strokes.
- Accent and cantillation points, if ever encountered.

Removal is silent and needs no record; §10 licenses it and the stored line is the result. An **unrecognized** codepoint is not removed — it is flagged and left for decision.

Also normalized at ingestion:

- **U+0724 FINAL SEMKATH → U+0723.** A positional shape, not a distinct letter.
- **U+1DF8 and U+1DFA remain the normalized between-letter page-states.** They transliterate later as `^^` and `__` respectively (§7); ingestion does not replace Syriac-layer codepoints with ASCII notation.
- **U+035E remains the normalized upper two-letter spanning-line page-state** and is stored after the first of the two bases (§6.2).
- **U+035F remains the normalized lower two-letter spanning-line page-state** and is stored after the first of the two bases (§6.2).
- **U+0324, U+0740, U+0744 → the two-dots-below page-state** (§17).
- **U+032E → the breve-below page-state** (§18).

### 16.2 U+0716

**ܖ (U+0716) carrying syāmē is resh.** The resh point and syāmē occupy the same position and the script suppresses the former; some typists encode the result with U+0716, others with U+072A. Both are resh. Normalize to ܪ and transliterate `r̈`. This holds whether or not a vowel point stands between the two in the stored sequence — in ܥܝܼܖܹ̈ܐ the zlāmā qašyā intervenes, and the rule applies.

**Bare U+0716 normalizes to resh and raises a flag.** Treat the normalization as a source-level anomaly, not as evidence for a new consonant. If the lexical context permits dalath or otherwise leaves the reading uncertain, require manual source review before confirmation.

### 16.3 Combining-mark order

Normalize every combining sequence to the complete §5.1 rank **before** comparison or round-trip validation (§12). Unicode NFC orders different canonical combining classes but does not repair equal-class order. Ingestion therefore assigns every supported mark its explicit project rank, covering CCC **36, 218, 220, 228, 230, 233, and 234**, and sorts by that canonical sequence before NFC.

No supported mark is exempt from the rank merely because its CCC currently contains only one project mark. If a future mark enters the inventory, §5.1 and the permutation regressions must be extended at the same time. Raw witnesses that differ only in the serialization order of the same supported marks must normalize to one identical Syriac sequence.

### 16.4 Per-block ingestion

**The audit runs per block, not per file.** A single file may contain blocks drawn from different digital sources or encoding conventions. Audit each block whose provenance may differ, and record where the seams fall.

### 16.5 Witness collation

Ingestion is per-witness. Where witnesses disagree after normalization, the disagreement is textual and belongs to the source hierarchy (General Rules §1), not to this file.

**Do not resolve by majority vote.** Witnesses may share an ancestor or encoding source, so a vote can count copies rather than independent readings. The designated source of record governs; variants are recorded rather than averaged.

### 16.6 West Syriac vowel codepoints — refused, never mapped

The East Syriac vowels are the **dotted** forms: U+0732, U+0735, U+0738, U+0739, U+073C, U+073F. The West Syriac equivalents are separate characters: U+0730, U+0731, U+0733, U+0734, U+0736, U+0737, U+073A, U+073B, U+073D, U+073E.

**These are never normalized into East Syriac vowels.** A West Syriac sign is a different mark, not a different encoding of the same mark, and mapping one to the other fabricates a reading the page does not contain.

- **In a source of record:** raises a flag. Either the source is not what it was taken to be, or the block has a seam (§16.4).
- **In a corpus search:** a West-vocalized token **carries no evidence about East Syriac pointing**. Distribution and lexical range may be cited from it; a vowel or a bgdkpt point may not.

### 16.7 Page-state corrections and blocking span states

A canonical two-letter span is **not source-lossy**: U+035E/U+035F distinguishes it directly from two U+0747/U+0748 one-letter marks (§6.3).

Raw witnesses can still be lossy. If a digital witness repeats U+0747/U+0748 on adjacent letters while the printed page might show one continuous line, the page-state audit must compare against the source page before confirmation. The page decides whether canonical normalized Syriac receives one U+035E/U+035F after the first base or retains two separate U+0747/U+0748 marks. This human page-state correction occurs **before transliteration**.

The confirmed Our Father example is therefore stored directly as `ܫܒܲܩ̣͞ܢ`, not as repeated U+0747, and transliterates `šbaq_⁀n` with no external resolution argument.

Blocking span states:

- U+035E/U+035F on the final orthographic letter of a word with no following base;
- a span crossing an editorial square-bracket boundary;
- consecutive same-direction span starts that would overlap on the middle letter;
- both U+035E and U+035F beginning on the same base under the present notation.

A carrier bearing both one-letter U+0747 and U+0748 simultaneously likewise has no canonical notation in the present system and is blocking.

Likewise, U+1DF8/U+1DFA on the final orthographic letter of a word with no following letter is not a coherent "between-letter" page-state and is blocking. (Where final `ā`/`ē` suppresses a written mater under §4.2, that ʾālap̄ is present in the normalized Syriac and therefore satisfies the following-letter requirement.)

For vowel stacks, the generic `multiple-vowels-on-carrier` diagnostic is a **nonblocking page-audit flag**, not a normalization-write or transliteration ban. Two supported vowel page-states are first put into the canonical §5.1 mark order and can then be stored and transliterated reversibly while the user verifies the page. **Three or more** vowel page-states on one carrier remain unsupported, and a waw carrying both Class-A U+073C (`ū`) and U+073F (`ō`) remains specifically contradictory and blocking under the current notation.

---

## 17. Two Dots Below

Two dots beneath a letter, distinct from zlāmā by shape and environment.

**Notation:** combining diaeresis below (U+0324) on the transliterated letter — `ẗ` above for syāmē, `t̤` below for this. The two are deliberately symmetric: the string mirrors the page.

**Encodings normalized to this page-state:** U+0324, U+0740 SYRIAC FEMININE DOT, U+0744 SYRIAC TWO VERTICAL DOTS BELOW. In East Syriac and Estrangela the feminine dot takes the form of two dots below, which is why the Syriac-specific codepoint and the generic one both occur for one appearance.

**Function is not recorded.** The same graphical page-state receives the same notation regardless of grammatical interpretation.

ASCII convenience for search/input aids: `:` after the carrying letter. **This is not canonical transliteration, is never stored as the canonical string, and is not accepted by the canonical inverse parser.**

---

## 18. The Breve Below

An arc beneath a letter, opening downward. Graphically distinct from rūkkākā, which is a dot.

**Notation:** combining breve below (U+032E) on the transliterated letter — `p̮`. Encoded U+032E at source, so ingestion passes it through unchanged.

**No collision.** Every other mark in the system occupies a different position or shape: macron above for soft `p̄` and `ḡ`, macron below for soft `ḇ ḏ ḵ ṯ`, breve *above* for the word-final Class-B exceptions `ă ĕ`, dot above for hard, diaeresis above for syāmē, diaeresis below for §17. The space below a pe is free precisely because pe is one of the two letters whose soft form takes a macron above.

ASCII convenience for search/input aids: `%` after the carrying letter. **This is not canonical transliteration, is never stored as the canonical string, and is not accepted by the canonical inverse parser.**