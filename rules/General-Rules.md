# General Rules

## Purpose
The project's working constitution. Apply the whole of it, silently, on every translation task. Do not restate unless a rule bears on the current clause or is asked for.

## Project Aim
A liturgically resonant English translation of the East Syriac Peshitta and liturgics, preserving Syriac theological continuity, literary logic, and inter-Testamental resonance.

## Interpretive Stance
Where interpretation bears on rendering, follow the Church Fathers and the Orthodox/Catholic tradition, with favor to the Syrian Fathers.

## Governing Principle
Work thoroughly. Do not skip source checking, Syriac verification, transliteration, glossary review, prior-text consistency, or reference-gathering.

Where the page is ambiguous, sources disagree, or a mark cannot be securely read — flag it. Never resolve by silent inference; an inference presented as a finding stops being visible.

Where the working environment holds a resource bearing on a question (§12.1), use it before offering a judgment or handing over an open question.

## Output
- Minimum complete output for accurate review.
- Do not restate stable rules, source hierarchy, transliteration policy, or settled entries unless relevant.
- Brief bullets and short sections. Show only the line referenced.
- Answer in conversation. No file unless asked.

## 1. Source Hierarchy

### 1.1 Designated sources of record and scriptural baseline

| Material | Governing source |
|---|---|
| Psalms | **Ksawa d-Mazmore** — source of record |
| The Hours (Ramsha, Lelya, Sapra, and the rest) | **Breviarium Chaldaicum** — source of record |
| Qurbana, including the Anaphoras | **Editio Typica of the Syro-Malabar Church** — source of record |
| All other Scripture | **East Syriac Mosul Peshitta** — baseline textual witness, subject to §§1.2 and 4.2 |

The `source_of_record` field remains the stable provenance field in `sources/sources.yaml`, but its force differs by material. For the Psalms and liturgics it designates the controlling source text, subject only to explicitly adopted apparatus or additions. For Scripture other than Psalms, the East Syriac Mosul Peshitta is the **presumptive starting text and pointing witness**, not an absolute textual ceiling: the canonical Syriac may depart from Mosul by an explicit, evidenced decision under §4.2 in order to preserve the coherence of Scripture and the received Tradition.

A text falling outside the four classes above has its source of record designated explicitly **before entries are built** and recorded in `sources/sources.yaml`.

### 1.2 Other provisions

- **Reference use** — any Syriac text may illustrate usage so long as it exists. Never fabricate citations.
- **Psalms** — the *Ksawa d-Mazmore* governs the canonical Syriac. A differing witness is recorded as a variant rather than silently substituted.
- **Liturgics** — the designated liturgical source remains controlling. Material deliberately supplied from an Assyrian Hudra or another established liturgical witness may enter as explicit editorial apparatus under §9.1; the supplying witness is named and the addition never masquerades as wording of the source of record.
- **Scripture other than Psalms** — begin with Mosul, but collate where a textual, inter-Testamental, patristic, liturgical, or harmonization question is material. A reading may be adopted from another ancient Syriac witness or revision under §4.2. Mosul's displaced reading and the evidence for the adopted reading must remain visible in the apparatus/provenance record.
- **Witnesses and majority** — one text may exist in several digital or manuscript witnesses differing in pointing, codepoint convention, or wording. Never resolve a substantive reading by raw majority vote. Normalize per Translit §16 before comparing, or encoding differences masquerade as textual ones.
- **Audit target** — for Psalms and liturgics, the audit runs against the source of record plus any explicitly adopted apparatus. For non-Psalm Scripture, audit Mosul as the baseline and every witness that supplies an adopted departure. Pointing or wording absent from the supplying witness may not be silently invented.

## 2. Transliteration Policy
Governed in full by the Transliteration Rules. Apply silently.

## 3. Translation Priorities
- Prefer Syriac logic over smoother English idiom, so long as English stays readable.
- Prefer defensible inter-Testamental resonance when present.
- Keep repeated Syriac terms stable in English unless context clearly requires otherwise; keep recurring English idioms consistent where the Syriac recurs.

## 4. Harmonization

### 4.1 Translation harmonization
In scope where it improves coherence without violating the Syriac sense. Note material harmonizations rather than folding them silently into the confirmed text.

### 4.2 Scriptural textual harmonization
For **Scripture other than Psalms**, harmonization may operate at the Syriac textual level as well as in English. The purpose is not to make Mosul uniform mechanically, but to preserve the coherent witness of Scripture and the Tradition where the Syriac textual history gives responsible grounds to do so.

A textual harmonization may include a departure from Mosul in a quotation, parallel passage, divine or personal name, formula, theological expression, or other locus where broader evidence materially favors coherence. It is a **textual decision**, not normalization, and is made locus by locus.

Before adopting such a reading:

1. establish the Mosul reading exactly;
2. examine relevant Peshitta manuscripts and critical editions where available;
3. examine other ancient Syriac evidence that bears directly on the locus — including Old Syriac material, the Syro-Hexapla, revisions such as Jacob of Edessa's, and patristic or liturgical biblical citations as applicable;
4. compare the Hebrew and Greek textual traditions where they bear on the Syriac divergence;
5. prefer an actually attested Syriac reading over an invented retroversion whenever the evidence permits;
6. state what is being harmonized, what witness supplies or supports the adopted Syriac, and why the coherence gained is textually and traditionally defensible; and
7. preserve Mosul's displaced reading in the editorial apparatus/provenance record.

Ancient attestation does not compel adoption, and a later witness is not rejected merely for being later if it demonstrably preserves an older reading. No one version — Peshitta, Septuagint/Syro-Hexapla, or a revisional text — automatically overrides the others outside the designated roles of §1.1. The decision weighs provenance, antiquity, textual relationship, Syriac reception, canonical coherence, and the Tradition rather than counting witnesses.

This provision does **not** make Psalms or liturgical texts eclectic. Their governing sources remain as specified in §1.1; liturgical additions continue to use the explicit apparatus mechanism of §1.2.

## 5. English Style
Elevated, formal, readable, prayer-capable, not artificially archaic. Do not flatten strong theological language.

## 6. Tense
Preserve the Syriac tense. Past narrative stays past. Any shift in Psalms or prayer must be cautious and justified.

## 7. Working Sequence
1. Read the text given
2. Establish the Syriac: confirm the governing source from §1.1; for non-Psalm Scripture begin from Mosul and determine whether §4.2 requires broader textual collation before fixing the canonical line
3. **Codepoint audit of the source text(s) supplying the canonical Syriac, before transliterating** (Translit §16). Non-negotiable. Run silently; report only what it surfaces
4. Give canonical transliteration
5. Review every token, in order, repeats included, under the **Word-by-Word Standard** — a repeat is often pointed differently
6. Check each word against Glossary entries, including relevant related forms and compounds
7. Gather references and evidence under §12 and Word-by-Word §§3–5
8. Present every token's evidence and status under Word-by-Word §§3–8
9. Present suggested render
10. Lay out anything of note
11. Flag anything erroneous, ambiguous, or concerning
12. Enter glossary entries only after the English is confirmed
13. Run the check suite (§11)

## 8. Standard Clause Response
1. Syriac line
2. Transliteration
3. Word-by-word — every token in order, following the **Word-by-Word Standard**
4. Suggested render
5. Notes/flags

## 9. Project Files

**Glossary** (the concordance), **General Rules** (this file), **Transliteration Rules**, **Word-by-Word Standard**.

**Citing a section always names its file** — "Translit §10", "General Rules §10", "Word-by-Word §4". Section numbers are stable; reserved sections are not renumbered.

### 9.1 Confirmed texts

Kept separate from the project files. Format is fixed:

- **Plain UTF-8** (`.txt` or `.md`), no BOM, **LF** endings, no trailing whitespace. The only permitted whitespace codepoints are **U+0020 SPACE** within a line and **U+000A LF** between lines; tabs, non-breaking spaces, thin spaces, and other Unicode whitespace are invalid
- **NFC normalized**, mark order per Translit §5.1
- **One file per text.** Lines numbered by position; the line is the citation unit
- **Punctuation and all other out-of-scope characters removed at ingestion** (Translit §10, Translit §16.1), except editorial apparatus. Clause division is carried by line breaks
- **Editorial apparatus is preserved across all three blocks.** Syriac and transliteration carry the full variant; English may collapse shared wording and mark only what differs. A full English insertion from another source is used only for a whole line or clause.
- **Rubrical labels are preserved across all three blocks as parenthesized editorial apparatus.** They are not prayed text and are excluded from ingestion, tokenization, lexical comparison, and context strings. A rubric directing repetition is retained as a label and also executed: the repeated clause is written out in full, one line per repetition.
- **Straight apostrophes** (`'`), never curly

### 9.1.1 The three-layer structure

Three blocks in fixed order: pointed Syriac, canonical transliteration, English.

- All three hold the **same number of lines**; line *n* of each is the same clause
- The transliteration block **reproduces mechanically from the Syriac** (Translit §12), never typed independently. A transliteration left behind by a revision to the Syriac is the most damaging error this format admits, because every block still reads correctly alone
- Stanza breaks, if used, appear identically in all three blocks
- **Square brackets mark added or inserted material.** Material bracketed in the Syriac block is bracketed correspondingly in transliteration. English may collapse a variant into shared wording and bracket only what differs; a full bracketed insertion from another source is used only for a whole line or clause. Material bracketed only in the English block is an interpretive supplement — `And [we are faithful] to One Mar Yah` — and never enters one (§10.13).
- **Parentheses in the Syriac/English apparatus mark editorial material**, including rubrical labels such as `(Qanona)` and source/witness labels. They are preserved literally in all three blocks but ignored by text ingestion and lexical comparison; they are never prayed text and never a context string. In the canonical transliteration block, parentheses also have the narrowly defined one-letter line use of Translit §6.1; two-letter spans use `⁀`/`‿`, not parentheses.

Rich-text formats are never the authoritative copy — they can split a letter from its combining marks. Display is separate from storage: the file is correct regardless of whether a font can draw every mark.

### 9.2 Draft and confirmed

A text under work is a **draft** and is not citable: no entry may name one. It becomes confirmed when its governing source or baseline is designated (§1.1), every adopted textual departure is documented under §4.2, its codepoint audit is run (§7), its blocks round-trip (§11.11), its English is settled, and the check suite passes. Entries are built only then, and a confirmed text is not edited without rerunning §11.

The text files carry no header of their own, which would break the three-block parse. Provenance is stored separately in `sources/sources.yaml`; every confirmed filename has one registry entry containing its stable `citation_label` and `source_of_record`. The source-of-record field is designated per §1.1 and interpreted according to the material-specific rules there; accepted departures or additions are recorded as editorial apparatus rather than silently redefining the source. The deterministic confirmed-corpus checker verifies the filename/registry correspondence and source designation.

## 10. Glossary Principle

1. Each form of every word makes one entry. **Entry identity is canonical headword + root + `{...}` morphology.** The root is a field for comparing words of one root; morphology is part of identity because two genuinely distinct forms may be orthographically identical and share a root. **Part of speech is a separate field**, written `{...}` — never standing in the root field. It records the class of the **form** and its morphology: for a noun or adjective, gender, number and state; for a finite verb, stem, tense, person, gender and number; for a participle, stem, voice where the stem distinguishes it, gender, number and state. A **`verbal noun`** is a deverbal nominal lexeme, not an infinitive or finite verb form; it takes ordinary nominal gender, number, state, and pronominal-suffix morphology. A SEDRA **`Participle Adjective`** is recorded as `adj.` where the attested form belongs to that lexical category; a homographic form parsed by SEDRA as a verb with active/passive participle tense remains `ptcp.`. An indeclinable loan carries `indecl.` rather than invented inflectional features. Pronominal suffixes and enclitics are named after `+`. An invariable word carries its class alone. **The field records what the form is, not what it does** — `yāwmānā` is a noun working adverbially, `mīẗē` and `ḥayābaÿn` adjectives standing as nouns; function belongs to the rendering. **`referent`** prefixes any class where the form names one specific referent rather than a general one. Verb stems are named, not explained; the Glossary preamble tables what each does.
2. **Proclitics** (w- d- b- l- etc.) are stripped from the headword; each occurrence retains them. Where a proclitic softens the initial bgdkpt letter, the softening belongs to the proclitic: recorded on the occurrence, headword written unmarked (§10.17). A bare form attested later joins that entry.

   **Where a proclitic carries a vowel belonging to the head lexeme, the headword restores it** — ܘܒܲܐܡܝܼܢܘܼ *wbaʾmīnū* gives the headword *ʾamīnū*, not *ʾmīnū*.

   **The negative particle ܠܵܐ *lā* takes no entry**, and is handled exactly as a proclitic — retained on the attested form of the word it negates, absent from the headword, not counted separately. Whether written solid or separate.
3. Each occurrence records its English context and a citation. **A citation names the text and the line.** Standing alone: `(Creed Line 5)`, `(Teshbhotha l'Alaha Line 2)`. One file, one text, one stable label. The label is the `citation_label` recorded for that confirmed file in `sources/sources.yaml`. A unit belonging to an office carries the office in its label: `(Ferial Slotha d'Ramsha, Line 3)`. An office name alone is not a label — the unit is. Where a text's own numbering is standard, it is used instead. **A citation string, once written, is reused exactly**; a label is fixed by first use, changing only for a rendering change or correction.

   **A word inserted from another witness carries that witness's name in front of the complete text label** — `(Assyrian Ferial Slotha d'Sapra II, Line 4)`. The witness qualifier preserves any distinction needed to identify the alternate office or day-class (`Ferial`, `Sunday`, `Festive`, etc.). The qualifier marks the word, not the text: there is no separate confirmed text for the witness, and the citation points at the same line of the same file as an unqualified one.
4. Variance is recorded, not suppressed. Each rendering carries its own **decision count**. Glossary counts measure indexed translation decisions under these rules, not raw corpus-token frequency. Keep repeated terms stable (§3), but do not flatten a genuine split.
5. Variant spellings form their own entry, connected by root.
6. **A non-compositional phrase is tabled in its own section and governs its components.** It carries the same fields as a form. Each component records the occurrence and points to the phrase with `→` in place of a rendering of its own; the occurrence still counts toward the component's total. A phrase takes precedence when a rendering is derived, and token coverage (§11.4) is satisfied by the components, not the phrase. **The test is whether a component is rendered differently inside the phrase than it would be on its own**, to carry the phrase's meaning. Where every component keeps its own rendering, the phrase is translated directly and takes no entry. Frequency, formulaic use, and solid writing are not evidence; those show univerbation (§10.12). `ʿālam ʿālmīn` qualifies — *ʿālam* is "Eternity" alone but "Age" inside it. `m_n ʿālam waʿdamā lʿālam` does not, nor does `b-ḵl ʿedān`. A phrase headword contains a space, which the entry parser must allow.
7. A form attested in the Syriac but not separately rendered in English records the rendering **⌀**. Still cited, still counts. ⌀ marks a decision not to render, not an omission.
8. **The parse field records exclusions and nothing else.** Ingestion removes out-of-scope characters before transliteration. If an in-scope mark survives ingestion but cannot be represented by the canonical system, record that exclusion and flag it rather than inventing notation. Gemination and unmarked hardness or softness are pronunciation and are recorded nowhere; homographs are separated by the identity fields of §10.1. The principle that a secure reading needs no parse-field note is scoped to this field alone — it does not bear on `{...}` (§10.1), which exists to record what English cannot carry.
9. **Capitalization is three-way.** *Positional* capitals normalize to lowercase in the rendering slot. *Reverential* capitals (Firstborn, True, Holy) do not split a rendering. *Semantic* capitals (Heaven against heavens, Watchers, the Evil One, Age against Eternity) do split it.
10. **Articles never distinguish renderings.** An article may stand in the rendering slot where it belongs to the received English form (the Evil One, the Right Hand) or to a construct (the greatness of), but may never be the only difference between two counted renderings.
11. **Decision-count cap.** For a high-frequency form with a settled rendering, cite roughly 10 indexed decisions for an obvious word or 15–20 for a less common one, then accrue additional indexed decisions as `+n`, written `rendering (base+extra)`. Base is the number of cited bullets; the headword total is the sum of indexed decisions, **not raw token occurrences**. Repetitions, same-locus witness duplicates, and common liturgical units excluded by §§10.13 and 10.18 do not increment it. The cap never applies to a new or minority rendering, or to an occurrence that itself bears a new decision.
12. **Compound forms.** Where the source writes two lexemes solid, the result is **one form** and **one entry**, with a compound root field: `bnaÿnāšā` [b-r + ʾ-n-š], `klmeḋem` [k-l + m-d-m]. Word division follows the source (Translit §9.2 conv. 4), so the same lexemes written separately are indexed under each component, and the two spellings link by root as variants (§10.5). Orthography, not meaning; contrast §10.6.
13. **Context strings.** The English context quotes a **span of the confirmed line**, verbatim from the English block, with parenthesized editorial labels and interpretive supplements removed, but words inserted from another witness retained. A whole-line quote takes no ellipsis. A partial quote marks omission with `...` at the point of omission — three ASCII periods, not U+2026, not four.

    **Two spans of one line either coincide exactly or do not overlap at all.** Once a phrase is the context for one word, every word inside it takes the same phrase. A line may carry several contexts; they partition it, never overlap. Enforced by §11.10b.

    **A written-out repetition is cited once** — at its first line, or at its first occurrence within the line where the repetition is written inline. A repetition is the same text said again; a form recurring in a different grammatical role is not one, and is cited at each occurrence.

    **An alternate witness at the same textual locus does not create a second occurrence when it repeats the same form in the same grammatical role.** Count and cite it once. A different form or role is indexed separately.
14. **Headword identity and search.** The canonical headword string itself is the exact reversible **orthographic** key for the indexed form, including any deliberate §10.17 merge normalization; no second exact orthographic key is stored. Full Glossary entry identity is **canonical headword + root + `{...}` morphology** (§10.1). Each headword carries one additional fold key, written `(search: alaha)` — lowercase, diacritics stripped, `ʾ` and `ʿ` dropped, `š` folded to `sh`, and notation characters (`^` `_` `(` `)` `[` `]` `⁀` `‿`) dropped (Translit §11.2). Fold-key collisions are acceptable.
15. **Where two Syriac words render as one English word**, the rendering names the other in square brackets after it: `metḥaz̈yān (2) — seen (1), (un)seen (1) [wadlā]`. **The bracket binds to the rendering it immediately follows**, not to the entry.

    Narrow. Only where English is **one word doing the work of two Syriac words**. Not where English simply lacks a separate word for a Syriac one — that is ⌀ (§10.7) — nor where two Syriac words render as two English words, however tightly bound.
16. **Acclamations that are never translated take no entry** — ܐܵܡܹܝܢ *ʾāmēyn*, ܗܲܠܹܠܘܼܝܵܐ *hallēlūyā*. They hold no rendering to record and no variance to track. Check 4 is satisfied without them.
17. **Rūkkākā and qūššāyā do not by themselves make a second entry.** Two spellings of one form differing only in an environmentally varying bgdkpt point are **one entry**, each spelling recorded on its own occurrence. Spirantization is realization in environment, not a property of the lexeme.

    **The headword is written unmarked at every point deliberately merged under this rule.** Where one merged spelling is itself unmarked, that spelling heads the entry. Where none is — the proclitic-softened initials of §10.2 are the standing case — the headword is written without the point as an **index form**, which is not a claim that any page shows a bare letter.

    **All other points remain as attested.** A headword is the spelling of the indexed form, not a stripped skeleton.

    **Where a bgdkpt point carries a form distinction, preserve it.** If the point is the only written signal of a different morphological analysis, the spellings are different forms and take separate entries with distinct `{...}` analyses under §10.1. Merging is the default; splitting is a morphological claim. Once that claim is made in the headwords, the checker does not strip the point again.
18. **A common liturgical unit takes one set of entries.** A unit recurring across the office unchanged — the standard closing ܡܵܪܵܐ ܕܟܼܠ ܐܲܒ̣ܵܐ ܘܲܒ̣ܪܵܐ ܘܪܘܼܚܵܐ ܕܩܘܼܕ̣ܫܵܐ ܠܥܵܠܡܝܼܢ is the standing case — records its occurrences once, at the text where first confirmed. Check 4 is satisfied without it. Where a later witness differs in content, it is not the same unit and takes its own entries.
19. **A rendering interrupted by other words takes `...` at the break** — `May...come`, `Your...Trinity`. Three ASCII periods, as §10.13. The rendering names only the English belonging to this form; the intervening words belong to their own entries.
20. **The root field follows SEDRA** (§12.1), transliterated into this project's hyphenated form. Consult it; do not reconstruct from memory or cognate reasoning.

    **Three standing departures, all writing the root out more fully than SEDRA does.** Hollow roots keep the middle radical — [r-w-m], [q-w-m] against SEDRA's ܪܡ, ܩܡ. Geminate roots keep both — [h-l-l], [ʿ-m-m] against ܗܠ, ܥܡ. A noun SEDRA treats as its own root keeps its consonantal root — [š-m-y], [ʿ-l-m]. Writing in full is what lets the project carry a distinction SEDRA marks only by homonym id: [ʿ-l-l] enter/cause against [ʿ-l] the preposition.

    Everything else takes SEDRA's reading, including every III-weak root, which SEDRA writes with final alaph.

    **Where SEDRA carries no root**, establish it from the Peshitta or patristic usage (§12) and write it plainly; where only the nominal pattern supports it, mark the root provisional with `?` until external evidence establishes it.

    **Where no root applies, the field holds a declared marker instead**: `[—]` not yet established, `[prop. noun]`, `[Gk. loan]`, or the word class where naming it says more than a bare dash. A marker is not a part of speech standing in the root field (§10.1); it is a statement that no root governs the form.

## 11. Check Suite
Run after every glossary write, and after any edit to a confirmed text. **Diagnose a flag before calling it a defect.** A check reports a condition for review; it does not by itself establish that the data are wrong.

**Glossary**
1. Greek/Cyrillic homoglyph scan
2. NFC normalization
3. Per-entry bullets == Σbase, and decision total == Σ(base+extra)
4. Every source token has an attested form, except proclitics and *lā* (§10.2), untranslated acclamations (§10.16), repetitions and same-locus witness duplicates already cited (§10.13), and members of a common liturgical unit already entered (§10.18). Phrase-section bullets do not count toward coverage (§10.6). Parenthesized editorial and rubrical labels are apparatus, not source tokens.
5. The converse of 4 — every non-exempt occurrence in the corpus carries a bullet, and no bullet claims an occurrence its line does not contain
6. No two entries share the same canonical headword string, root, **and `{...}` morphology** (Translit §12). Compare the headwords exactly as stored; §10.17 has already removed only the bgdkpt distinctions that the Glossary has deliberately merged
7. Every attested form is a token sequence of its cited transliteration line
8. Every recorded rendering is traceable in that entry's own context strings, with `...` (§10.19) and the §10.15 bracket resolved first. A `→` phrase pointer is not a rendering and is exempt
9. Every form entry has exactly one nonempty `{...}` field satisfying §10.1; the root field holds a root or a marker declared in §10.20, never a part of speech doing a root's work; the `{...}` field never holds a root
10. Context strings: **10a** — every context is a literal span of its cited line, taken from the English block with editorial labels and interpretive supplements removed and `...` stripped; **10b** — two contexts citing one line are identical or disjoint

**Syriac — in the Glossary and in every confirmed text**
11. Round-trip: the pointing reconstructs from the canonical string, and the canonical string from the pointing
12. Carrier discipline — carrier-bound semantic marks remain on valid carriers: U+0741 and U+0742 only on bgdkpt, U+073C only on waw and yodh, and U+073F only on waw. U+0307 and U+0323 are generic §7 points and remain valid on any carrier, including bgdkpt, waw, and yodh; the carrier never changes their identity. U+035E/U+035F only begin a two-letter span with an immediately following base in the same orthographic word
13. Combining-mark order follows Translit §5.1 for every in-scope sequence. Check class 220 and class 230 project tie-breaks explicitly; canonical Unicode ordering places the U+035F/U+035E span states in classes 233/234 after those marks
14. One Syriac spelling transliterates one way across the corpus, and one transliteration maps back to one spelling. In particular, a direct two-letter span and two adjacent one-letter lines must remain distinct in **both** layers (`ܡ͞ܢ` ↔ `m⁀n`; `ܡ݇ܢ݇` ↔ `(m)(n)`)

**Files**
15. Three blocks of equal length in every confirmed text, the transliteration derived from the Syriac (§9.1.1)
16. Hygiene per §9.1 — UTF-8 without BOM, LF endings, U+0020/LF as the only whitespace, no trailing whitespace, NFC, straight apostrophes

Corruption here is silent rather than noisy — a wrong codepoint renders correctly, a dropped mark reverses without complaint, a stale citation points at a section that still exists.

## 12. Research Method for Word-by-Word

Research and presentation deliberately have different orders. **Research leads with external evidence**, not this project's files. The Glossary records what has been decided; it cannot confirm a meaning, and reasoning from it in a circle is the failure this section prevents. **Presentation is governed by Word-by-Word §10**, which shows project precedent first for review without treating that precedent as lexical proof.

Order of resort:
1. **Peshitta distribution** — where the form occurs, in what construction, and what it renders
2. **Patristic and liturgical usage**, especially East Syriac. A Father glossing his own phrase outranks any inference
3. **Lexica.** Consult before offering an etymology or a root field, and before raising a root question as open
4. **Cognate languages** — Hebrew, Greek, Arabic, Ge'ez, Church Slavonic — where the versions bear on the reading
5. **Project files last**, as a consistency check

### 12.1 Standing corpora and lexica

Bulk-downloadable and greppable. Grep the whole relevant corpus; do not sample when exhaustive retrieval is available. Read each repository's own documentation for contents and licence before use.

- **`ETCBC/peshitta`** — prefer the repository's current `plain/0.2/<Book>.txt` plain-text release rather than the older `plain/0.1` snapshot. **Unvocalized Old Testament only.** The electronic text follows the VTS main text for books whose VTS editions are available and Codex Ambrosianus for the remaining books; it is therefore not accurately described as one manuscript base. Good for lexical distribution and translation equivalence. **Never for East Syriac pointing, and not the Mosul source of record** — re-check every reading against §1 before it enters an entry. The upstream project describes this repository as stable/unsupported, so do not assume a newer path without checking its README.
- **`ETCBC/syriac`** — a newer Text-Fabric Syriac dataset with word-level morphology and a growing selection of Peshitta and other Syriac texts. Useful as a secondary morphology/distribution cross-check where the relevant book is actually present. It is explicitly a work in progress and does **not** contain the complete Peshitta, so its absence of a form is never negative evidence for the whole corpus and it never replaces the source of record.
- **`srophe/syriac-corpus`** — `data/tei/*.xml`. Strip tags after splitting on `<text`; author and title sit in `<author>` and `<title>`. **Narsai** is fully vocalized East Syriac and the highest-value witness here; **Ishoʿyahb III** is the closest register to the hymns. Otherwise **mostly West Syriac vocalization** — see Translit §16.6 on what may be cited from a West-vocalized token.
- **`peshitta/sedrajs`** — `sedra/`. Comma-delimited, ASCII-transliterated: `A`=ܐ `B`=ܒ `G`=ܓ `D`=ܕ `H`=ܗ `O`=ܘ `Z`=ܙ `K`=ܚ `Y`=ܛ `;`=ܝ `C`=ܟ `L`=ܠ `M`=ܡ `N`=ܢ `S`=ܣ `E`=ܥ `I`=ܦ `/`=ܨ `X`=ܩ `R`=ܪ `W`=ܫ `T`=ܬ. ENGLISH links by id to LEXEMES, LEXEMES by id to ROOTS. Verbs are glossed without "to". Glosses are **NT-particular**; liturgical and OT vocabulary may be absent. Root conventions differ from this project's — see §10.20. The conversion code is MIT-licensed, but the bundled SEDRA III database carries its own academic-use and redistribution conditions; preserve those terms.
- **SEDRA 4 API** — `sedra.bethmardutho.org`, for what the local file does not cover. A remote call.

### 12.2 Reporting
State the corpus, the token counts, and the caveat. Report what was *not* checked. An etymology asserted from a tertiary source is flagged as such and never hardens into a root field by repetition.

Corpus counts are contaminated by homographs and proper nouns; report from contextual sampling, not raw frequency.