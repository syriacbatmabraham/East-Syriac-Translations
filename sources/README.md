# Sources and provenance

This directory is reserved for source-of-record metadata and provenance documentation.

The project distinguishes between:

- a **source of record**, which governs the confirmed Syriac text;
- other **witnesses**, which may preserve variants or different pointing/codepoint conventions; and
- **reference corpora and lexica**, which may be consulted for distribution, meaning, morphology, roots, and comparison but do not replace the designated source of record.

The source hierarchy and rules for witness collation are defined in `rules/General-Rules.md`.

## What belongs here

Machine-readable source-of-record designations are stored in `sources.yaml`. Only explicit designations belong there; the absence of a text from the mapping must never be interpreted as an inferred source choice.

Do not add scans, PDFs, fonts, downloaded corpora, or other third-party source files to this public repository unless their redistribution rights permit it. A local copy used for page checking or consultation but not licensed for redistribution is simply a **local non-redistributable source copy**; keep it outside version control. This is a licensing distinction, not a claim that the source itself is private or confidential.
