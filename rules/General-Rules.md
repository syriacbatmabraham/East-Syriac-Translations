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
- **Page audit and canonical Syriac** — the user performs the page-against-source audit. The assistant normalizes the supplied Syriac and reports the letter-by-letter page-state required by §7 and Translit §16; the user then corrects or confirms it against the page. Once the user confirms the normalized Syriac and its mechanically derived canonical transliteration, that pair is authoritative for subsequent translation, Glossary, and repository work. Do not reopen the source page unless the user explicitly directs a new page audit or a later internal contradiction requires the canonical Syriac itself to be questioned.
- **Audit target** — before Syriac confirmation, the user audits the normalized text against the governing source or adopted apparatus. After Syriac confirmation, project translation and Glossary audits run against the confirmed canonical Syriac and canonical transliteration. For non-Psalm Scripture, every adopted departure from Mosul remains documented under §4.2.

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

## 6. Sense
Preserve the Syriac sense. Do not force Syriac morphological tense, aspect, or verbal category into a one-to-one English tense. The morphology remains recorded exactly in the Glossary; the English renders its contextual force. Any interpretive shift in Psalms or prayer must be cautious and justified.

## 7. Working Sequence
1. **Receive the Syriac.** The user supplies the source text to be prepared.
2. **Normalize and expose the page-state.** Normalize mechanically under Translit §16 and return the normalized Syriac together with the required letter-by-letter list of every letter and the marks currently carried by it. Do not treat this output as page-confirmed.
3. **User page audit.** The user compares that normalized/page-state output against the governing page and supplies every correction needed.
4. **Confirm the Syriac layer.** Apply the user's corrections, return the updated normalized Syriac and its mechanically derived canonical transliteration, and obtain the user's confirmation. This is the **Syriac confirmation**: the confirmed script and transliteration become the authoritative textual basis for all later translation work (§1.2; §9.2).
5. **Begin word-by-word only when prompted.** The user selects the first line or lines. Review every token in order under the **Word-by-Word Standard**, including repeats where relevant.
6. **Translate slowly through the text.** For each working unit, check existing Glossary precedent, gather external evidence under §12 and Word-by-Word §§3–5, present the evidence/status, suggest a render, and flag material ambiguity or concern. Continue clause by clause until the text is complete.
7. **Confirm the English text.** Once every line is settled, present the whole translation for the user's confirmation. This is the **English confirmation**; do not build the new Glossary entries before it.
8. **Draft Glossary entries.** After English confirmation, draft every required new or updated Glossary entry, phrase entry, count, rendering, morphology, root, and citation context. Present the draft to the user without committing it.
9. **Confirm the Glossary entries.** Incorporate the user's corrections and obtain approval of the Glossary draft. This completes the second confirmation layer: settled English plus approved Glossary entries.
10. **Commit and validate atomically.** Add or update the complete three-block text, source registry entry where needed, approved Glossary entries, and any required major-decision record together; then run the full check suite (§11). Only the passing repository state is citable as a repository-confirmed text.

## 8. Standard Clause Response
1. Syriac line
2. Transliteration
3. Word-by-word — every token in order, following the **Word-by-Word Standard**
4. Suggested render
5. Notes/flags

## 9. Project Files

**Glossary** (the concordance), **General Rules** (this file), **Transliteration Rules**, **Word-by-Word Standard**, and **Major Interpretive Decisions** (`decisions/Major-Interpretive-Decisions.md`).

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

### 9.2 Confirmation states

There are two substantive confirmation layers before final repository confirmation.

1. **Syriac confirmation.** After normalization, the assistant returns the letter-by-letter page-state and the user audits it against the page. The user then confirms the corrected normalized Syriac together with its mechanically derived canonical transliteration. That confirmed pair is thereafter the authoritative textual basis for translation and Glossary work; it is not to be re-collated against a page unless the user explicitly reopens the Syriac layer.
2. **English and Glossary confirmation.** Translation proceeds from the confirmed Syriac. When all English lines are settled, the user confirms the complete English translation. Only then are new Glossary entries drafted. The user reviews and confirms those entries before any repository commit.

Before the final commit, the completed text remains a working text and is not a citable Glossary source. The complete three-block text, source registry entry where required, approved Glossary entries, and any material decision record are committed together. The full check suite then validates the combined repository state. A passing state is **repository-confirmed** and citable; mechanical validation is not a third substantive human confirmation.

A repository-confirmed text is not edited without reopening the affected confirmation layer and rerunning §11. A Syriac change reopens the Syriac layer and everything downstream from it. An English-only change reopens the English/Glossary layer and every affected Glossary decision.

The text files carry no header of their own, which would break the three-block parse. Provenance is stored separately in `sources/sources.yaml`; every repository-confirmed filename has one registry entry containing its stable `citation_label` and `source_of_record`. The source-of-record field is designated per §1.1 and interpreted according to the material-specific rules there; accepted departures or additions are recorded as editorial apparatus rather than silently redefining the source. The deterministic confirmed-corpus checker verifies the filename/registry correspondence and source designation.

### 9.3 Major interpretive decisions

`decisions/Major-Interpretive-Decisions.md` preserves only **material settled interpretive decisions that a later translator or adversarial audit is reasonably likely to reopen**. It is not a research notebook, does not duplicate ordinary Glossary decisions, and never replaces the evidence required by §12 when genuinely new evidence appears.

Each entry is a short bullet naming the text and line or lines, the date, the settled choice, and a one- or two-sentence reason. If the original date of a legacy decision is not securely known, record the date on which it was **affirmed** rather than inventing an earlier date. When substantive new evidence warrants reopening a recorded decision, investigate it and obtain the user's judgment before altering the text; record the new dated decision so that the reason for the change remains visible.

A decision recorded here is a working premise in later translation and audit work. Do not reopen it merely because another translation tradition, lexicon gloss, or smoother English alternative exists; reopen it only when materially new Syriac, textual, grammatical, patristic, or project evidence bears against it.

## 10. Glossary Principle

1. Each form of every word makes one entry. **Entry identity is canonical headword + root + `{...}` morphology.** The root is a field for comparing words of one root; morphology is part of identity because two genuinely distinct forms may be orthographically identical and share a root. **Part of speech is a separate field**, written `{...}` — never standing in the root field. It records the class of the **form** and its morphology: for a noun or adjective, gender, number and state; for a finite verb, stem, tense, person, gender and number; for a participle, stem, voice where the stem distinguishes it, gender, number and state. A **`verbal noun`** is a deverbal nominal lexeme, not an infinitive or finite verb form; it takes ordinary nominal gender, number, state, and pronominal-suffix morphology. A SEDRA `Participle Adjective` is recorded here as `adj.` when the attested form belongs to that lexical category; a homographic form parsed as a verb with active/passive participle tense remains `ptcp.`.
2. **Proclitics are stripped from the headword and retained on each occurrence.** Prefixes `w-`, `d-`, `b-`, `l-` are stripped where they are productive proclitics rather than part of the lexical form; combinations of them are stripped as a unit. The occurrence bullet always preserves the attested canonical form exactly. Do not strip material merely because it resembles a proclitic if doing so destroys the lexical form.
3. **Glossary entries follow confirmed English, not provisional glosses.** A lexical study can suggest many senses; the entry records only renderings actually adopted in repository-confirmed text.
4. **Variance is information.** Where one form has materially different confirmed English values, record them separately with counts and occurrences. Do not force one English gloss merely to simplify the Glossary.
5. **Compounds are their own form identity.** A compound or fused lexical unit receives its own entry rather than being silently split for identity. Its components may still be cited as related evidence during word study.
6. **Phrases may govern component renderings.** A phrase entry records a multiword expression whose English cannot responsibly be assigned word-by-word without distortion. Each component still receives its form entry and occurrence, but uses `→ phrase` in place of an independent rendering at that locus.
7. **Zero rendering.** A Syriac form deliberately represented by no separate English word is recorded as `⌀`, not omitted from the Glossary. This is distinct from a phrase pointer.
8. **Parse exclusions.** If an in-scope source mark cannot yet be represented in canonical transliteration, record that exclusion explicitly in the affected entry until the notation is extended. A parse exclusion is not permission to silently drop the mark from confirmed Syriac.
9. **Counts are indexed decisions, not corpus frequencies.** The number after a headword is the total of its rendering decision counts, not the number of raw tokens in the corpus.
10. **One occurrence bullet per indexed decision.** Every base count ordinarily has one occurrence bullet. Exceptions are governed by §§10.11–10.18.
11. **`+n` records indexed decisions omitted from bullets.** It may be used only when the same decision has already been evidenced by another bullet under a licensed omission rule; it is not a substitute for an unattested claim.
12. **A compound remains relevant evidence for its components.** During word study, surface a compound occurrence where the bare lexeme is under review and the compound materially bears on meaning.
13. **Repetition and context.** A written-out repetition is cited once — at its first line, or at its first occurrence within the line where the repetition is written inline. A repetition is the same text said again; a form recurring in a different grammatical role is not one, and is cited at each occurrence.

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
13. Combining-mark order follows the **complete Translit §5.1 rank** for every in-scope sequence. The supported inventory spans CCC **36, 218, 220, 228, 230, 233, and 234**, and every supported mark has one explicit project rank, including equal-CCC vowel states. Raw permutations of the same supported page marks must normalize to one identical stored sequence before NFC comparison and round-trip validation
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