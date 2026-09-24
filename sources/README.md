# Sources and provenance

This directory is reserved for source-of-record and baseline-source metadata and provenance documentation.

The project distinguishes between:

- a **source of record or baseline source**: for Psalms and liturgics, the designated source governs the canonical Syriac subject to explicit editorial apparatus; for Scripture other than Psalms, the East Syriac Mosul Peshitta is the baseline witness from which documented textual harmonizations may depart under General Rules §§1.1–1.2 and 4.2;
- other **witnesses**, which may preserve variants or different pointing/codepoint conventions and, where explicitly adopted under the General Rules, may supply an attested scriptural reading or liturgical addition; and
- **reference corpora and lexica**, which may be consulted for distribution, meaning, morphology, roots, and comparison but do not by themselves replace a designated governing or baseline source.

The source hierarchy, scriptural textual-harmonization policy, and rules for witness collation are defined in `rules/General-Rules.md`.

## What belongs here

Machine-readable source-of-record/baseline designations are stored in `sources.yaml`. Only explicit designations belong there; the absence of a text from the mapping must never be interpreted as an inferred source choice. For Scripture other than Psalms, the `source_of_record` field names the Mosul baseline and does not erase explicitly documented departures adopted under General Rules §4.2.

Do not add scans, PDFs, fonts, downloaded corpora, or other third-party source files to this public repository unless their redistribution rights permit it. A local copy used for page checking or consultation but not licensed for redistribution is simply a **local non-redistributable source copy**; keep it outside version control. This is a licensing distinction, not a claim that the source itself is private or confidential.

## Alternatives supplied by the source

A seasonal or other alternative already supplied by a text's source of record is distinct from an external witness reading. Keep its words in square brackets in all three text layers and register its location under that text:

```yaml
    source_alternatives:
      - line: 4
        bracket: 1
        label: Den'ha
        reading: "[ʾāw dʾeṯ‿ʿmeḏ lan]"
```

`line` is the logical text line, not the physical file line. `bracket` is the one-based bracket-group number on that line after editorial labels are removed. `reading` is the exact bracketed canonical transliteration. The declaration is validated against the text; whole-word, non-nested groups are required. Each location can be declared once. The label describes the alternative and is not a witness citation qualifier.

The Glossary uses the text's existing citation label and indexes the alternative's words normally. An undeclared bracketed reading still requires a witness-qualified citation. Witness apparatus retains its existing `editorial_apparatus` records. English-only interpretive supplements are not source alternatives.
