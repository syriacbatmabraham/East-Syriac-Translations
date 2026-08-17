# Word-by-Word Standard

## Purpose

This file governs the **word-by-word** stage of the translation workflow: what must be researched for each source token and how that evidence is presented for review. General Rules governs the larger translation method and source hierarchy; this file makes the word-by-word display fixed and repeatable.

The aim is **evidence before interpretation**. The reviewer should be able to see the relevant Syriac usages and established project precedent before being asked to accept an inferred English rendering.

## 1. Working Unit

1. Work **one source line or clause at a time** by default. Where several lines are supplied, treat each separately unless syntax requires a larger unit or the user asks otherwise.
2. Show only the line currently under review.
3. Begin with the pointed Syriac line, then its canonical transliteration.
4. Address **every source token in order, repeats included**. No word is omitted because its meaning seems trivial or already settled.
5. The amount of evidence varies with uncertainty; token coverage does not.

## 2. Per-Word Heading

Each token receives its own numbered block in source order. The heading contains:

`Syriac form — canonical transliteration — provisional/basic English value`

The transliteration and English are the primary review forms. Syriac script remains visible for identification, pointing, and textual questions, but repeated evidence examples should normally be shown in **transliterated Syriac + English + citation**, not Syriac script alone.

A proclitic remains attached in the attested transliteration of the source token. Discussion may identify the stripped head lexeme where Glossary comparison requires it (General Rules §10.2).

## 3. Project Precedent

Every token is checked against the current Glossary and confirmed corpus before presentation.

Show relevant project precedent near the beginning of the word block because it tells the reviewer immediately whether the project has encountered the form or lexeme before. This is a **consistency record, not independent proof of lexical meaning**; the research hierarchy of General Rules §12 remains controlling.

Present, where available, in this order:

1. **Exact Glossary form** — the current rendering or renderings and relevant confirmed occurrences.
2. **Same lexeme in another inflected form** — when useful to the present reading.
3. **Compound containing the lexeme** — never discard a compound merely because its Glossary identity is separate. If a source token contains or corresponds to a lexeme already encountered inside a compound, show that occurrence and its established English. Example: a bare `medem` study must surface project precedent from `klmeḋem` where relevant.
4. **Closely related derivation or root form** — only when it materially assists the present word.

Project examples use the standard evidence-line format of §5.

If no relevant project precedent exists, say so briefly rather than leaving the question implicit.

## 4. Attestation Priority

The appearances are more important than commentary. Gather and display attested usage before interpretive discussion.

Within the research hierarchy of General Rules §12, prefer evidence in this order:

1. **Exact word form in the same construction**, where available.
2. **Exact word form in other constructions.**
3. **Same lexeme in another inflected form.**
4. **Compound containing the lexeme.**
5. **Closely related derivation.**
6. **Broader root evidence**, only where the more direct levels are insufficient.

Never present a related form as though it were an exact-form occurrence. Label the relationship plainly.

For Peshitta work, search the whole relevant corpus when exhaustive retrieval is available (General Rules §12.1). For patristic and liturgical evidence, favor East Syriac witnesses and the registers specified there.

## 5. Evidence-Line Format

Ordinary occurrences are shown compactly as:

`transliterated Syriac — “English” — citation`

The quoted English may be an established project rendering, a published translation used as evidence, or a deliberately literal working gloss. Its status must be clear from the surrounding label; do not make a provisional gloss look like a confirmed project translation.

Examples should give enough surrounding transliterated Syriac to make the construction visible. Do not quote a single isolated token where the surrounding phrase is needed to understand its force.

Syriac script may be added where spelling, pointing, orthography, a textual variant, or a codepoint question matters. It is not required for every parallel once the form has been identified.

For each searched corpus:

- state the corpus;
- state the relevant token count when reliable;
- state any scope caveat;
- report what material resource was not checked.

Raw counts contaminated by homographs or proper nouns are not treated as semantic evidence without contextual review (General Rules §12.2).

## 6. Secure Words

A familiar or apparently trivial token still receives a word block.

A reading may be marked **Secure** when the checked evidence gives no material lexical, morphological, or contextual alternative relevant to the present construction. Security should normally rest on a combination of consistent occurrences, unambiguous construction, established morphology/lexical data, and, where available, stable project precedent.

For a secure word:

1. show the exact project precedent if one exists;
2. cite enough external occurrence evidence to demonstrate the consistency;
3. give only the necessary lexical or morphological identification;
4. mark **Status: Secure**;
5. stop. Do not expand a settled preposition or particle into an essay merely to make every block the same length.

Do not call a reading Secure merely because it is familiar. If corpus coverage is incomplete or a material alternative remains, use §8 instead.

## 7. Full Study

Where a word is not secure, give a fuller evidence block. The ordinary order is:

1. **Project precedent** — exact form, then relevant related forms.
2. **Exact-form attestations** — Peshitta first where applicable, then patristic/liturgical evidence under General Rules §12.
3. **Related-form attestations** — only as needed, clearly labeled by relationship.
4. **Lexical and morphological data** — SEDRA/CAL root and analysis, lexicon senses, and other factual data that materially bear on the choice.
5. **Status** — §8.

The study section should read primarily like a **mini-concordance**, not an essay. Keep inferred commentary out of the evidence stream unless a short note is necessary to explain why an occurrence belongs to a category.

Questions of how the evidence should be synthesized into English belong principally under **Suggested Rendering** and **Notes/Flags** after all word blocks.

## 8. Status Labels

Every word block ends with one of three statuses:

- **Secure** — the checked evidence leaves no material alternative for the present construction.
- **Probable** — one reading is clearly favored, but a real lexical, morphological, syntactic, or contextual alternative remains.
- **Open** — the evidence does not yet justify choosing between material alternatives, or a required resource/source check remains unresolved.

A status describes the present **reading in context**, not the inherent simplicity of the lexeme. A polysemous word can be Secure in an unambiguous construction; a common word can remain Probable or Open where syntax or pointing creates a real question.

## 9. Lexica, Morphology, and Roots

Lexical and morphological data support the attested evidence; they do not replace it.

1. Use SEDRA root conventions as governed by General Rules §10.20.
2. Consult SEDRA/CAL or the standing lexical resources before asserting an etymology, root, stem, or morphological analysis when it bears on the decision.
3. Give morphology only to the level relevant to identifying the form and its force. The eventual Glossary `{...}` field remains governed by General Rules §10.1.
4. A lexicon's list of possible senses does not by itself establish which sense is active in the clause. Attested constructions carry greater weight.

## 10. Research Order and Presentation Order

These are deliberately different.

**Research order:** follow General Rules §12 — external Syriac evidence and lexica establish meaning; project files are checked last for consistency so that the Glossary cannot prove itself.

**Presentation order:** show project precedent first, then the external attestations and lexical data. This lets the reviewer see immediately what has already been done while still receiving non-circular evidence for whether it should be retained.

The presentation order never promotes project precedent above external evidence as authority.

## 11. Standard Line Response

For an ordinary translation line, the response order is fixed:

1. **Syriac line**
2. **Canonical transliteration**
3. **Word-by-word** — one numbered block for every token, following this file
4. **Suggested Rendering** — synthesize the evidence into one or more defensible English possibilities; interpretive commentary belongs here
5. **Notes/Flags** — textual, grammatical, theological, harmonization, source, or unresolved issues

Do not insert a running interpretive essay between evidence occurrences. If the reviewer proposes a rendering after seeing the evidence, evaluate that proposal against the evidence in Suggested Rendering / Notes rather than retrofitting the word-study record.

## 12. Relationship to the Glossary

The word-by-word is a **review stage**, not a Glossary write.

- Existing Glossary entries and confirmed occurrences are shown as precedent under §3.
- A new form is not entered merely because its study is complete.
- English is confirmed first; Glossary entry construction follows General Rules §§7 and 10.
- Compound identity remains governed by General Rules §10.12, but compounds remain relevant related-form evidence under §§3–4 of this file.
