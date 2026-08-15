# East Syriac Translations

A working repository for East Syriac liturgical and scriptural translation, with particular attention to the Hudra, the Hours, and the Peshitta.

The project aims at a liturgically resonant English translation that preserves Syriac theological continuity, literary logic, and inter-Testamental resonance. It also maintains a reversible canonical transliteration system and a form-first glossary/concordance for consistency and linguistic study.

## Repository structure

- `rules/` — the project's working rules, including translation and canonical-transliteration policy.
- `glossary/` — the human-readable form-first concordance.
- `confirmed-texts/` — texts that have passed the project's internal confirmation process. Each file contains three aligned blocks: pointed Syriac, canonical transliteration, and English.
- `sources/` — provenance and source-of-record documentation, with machine-readable designations in `sources/sources.yaml`. Third-party source files are not assumed to be redistributable and are not automatically included here.
- `tools/` — validation, transliteration, ingestion, corpus, and database tooling.

## Source of truth

The `main` branch of this repository is the canonical project copy. Git history is used for version control; superseded rule files do not need to be retained beside current versions merely to preserve history.

Confirmed text files are plain UTF-8, NFC-normalized, LF-ended files. The project deliberately treats storage and display as separate concerns: a font's inability to render a valid Unicode mark does not make the stored data invalid.

Confirmed means that a text has passed the project's internal confirmation workflow; it does not make the text immutable. Changes to a confirmed text require the validation checks to be rerun.

## Licensing

See [`LICENSE.md`](LICENSE.md). In brief, original scholarly/textual contributions are intended for broad reuse under CC BY 4.0, while software under `tools/` is intended to use the MIT License. Third-party material retains its own rights and license status.
