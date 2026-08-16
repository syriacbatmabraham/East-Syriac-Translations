# Deterministic tools

The code in this directory implements mechanical parts of the East Syriac Translation workflow. The rule files remain authoritative; code is an executable implementation of those rules, not a second specification.

## Phase 1: source normalization

`normalize.py` implements source-ingestion normalization from **Transliteration Rules §16** and same-class combining-mark order from **§5.1**. It accepts a raw Syriac block and produces the normalized Syriac representation consumed by transliteration.

The normalizer is intentionally conservative: licensed transformations are automatic; refused/unrecognized states are preserved and flagged; West Syriac vowels are never mapped into East Syriac vowels; bare U+0716 normalizes to resh with a review flag; arbitrary unknown non-combining codepoints outside editorial apparatus are retained and flagged; malformed editorial delimiters are flagged; and persistent writes are refused while blocking source/page-state problems remain. Project text whitespace is deliberately narrow: only U+0020 SPACE and U+000A LF are accepted; tabs, non-breaking spaces and other Unicode whitespace are retained and flagged for review.

## Mandatory page-state audit

During validation every normalization run prints a human-readable letter-by-letter audit to stderr. It states what the machine believes is present on each Syriac carrier.

With the transliteration engine available, clean unambiguous input receives canonical word headers automatically:

```text
Word 1: *lʾalāhā*
Lamad
Alaph (pṯāḥā: a)
Lamad (zqāpā: ā)
Heh (zqāpā: ā)
Alaph
```

If adjacent same-direction line codepoints occur, normalized Unicode alone cannot tell whether the page shows two separate one-letter strokes or one physical line spanning the pair. The audit therefore keeps the Syriac header and requires a `PAGE CHECK` rather than guessing. A page-confirmed upper span joining a consonant cluster is treated as **marheṭānā**, not as a two-letter occultans. The confirmed `q-n` span in `šba(q_n)` is the standing example.

The post-normalization audit detects contradictions Unicode normalization alone cannot catch: multiple vowels on one carrier, both qūššāyā and rūkkākā on one bgdkpt letter, invalid canonical carriers, duplicate marks, and the same carrier bearing both an upper and lower line mark. The last state is in-scope Unicode but has no reversible notation under the current canonical rules, so it is blocking rather than silently encoded.

### Normalization use

```bash
python tools/normalize.py source.txt > normalized.txt
python tools/normalize.py source.txt --report-changes > normalized.txt
python tools/normalize.py source.txt --in-place
python tools/normalize.py source.txt --check
```

Normalized Syriac goes to stdout; flags, page-state issues/notices, and the mandatory audit go to stderr.

`--check` exit status:

- `0` — already normalized, no blocking flags/issues;
- `1` — deterministic normalization changes are needed, no blocking flags/issues;
- `2` — at least one condition requires correction/review (or a CLI/file error occurred).

A page-only notice does not make the encoded Syriac invalid and therefore does not change the normalization exit code. It must be resolved before canonical transliteration.

## Phase 2: reversible canonical transliteration

`east_syriac.transliteration` implements normalized Syriac → canonical Latin. `east_syriac.transliteration_inverse` implements the exact inverse. Forward transliteration never normalizes, repairs, or linguistically infers its input: it accepts only a clean normalized page-state produced by Phase 1.

The implementation includes:

- all canonical consonants and the three bgdkpt states;
- Class A and Class B vowels;
- word-final `ā/ă` and `ē/ĕ` conventions;
- syāmē, the distinguishing point, between-letter points, two dots below, breve below, and superscript ʾālap̄;
- editorial square brackets and parenthesized source/witness apparatus;
- one-letter line wrappers above/below and page-resolved two-letter spanning-line wrappers;
- strict NFC canonical strings;
- canonicality checking by re-forwarding every inverse parse.

The final-mater shorthand is deliberately narrow: a bare final ʾālap̄ is suppressed only when it immediately follows its zqāpā/zlāmā-qašyā carrier with no editorial delimiter between them. Thus `[ܡܵܐ]` gives `[mā]`, while `ܡܵ[ܐ]` gives `mā[ʾ]` and `[ܡܵ][ܐ]` gives `[mā][ʾ]`.

### One-letter lines and marheṭānā spans

A wrapper around one canonical letter-unit, such as `(h)`, records a line carried by that one letter. The project does not infer from the graphic stroke alone whether a traditional one-letter line is functioning as *mṭalqānā* or *mhaggyānā*.

A wrapper around **two** canonical letter-units, such as `(q_n)`, records **one page-confirmed physical line spanning the two letters**. Where the page establishes the familiar upper cluster line, this is marheṭānā: the two consonants are read as a vowelless cluster rather than either consonant being suppressed. Therefore `šba(q_n)` must not be normalized to a one-letter line on qoph.

The normalized Syriac storage convention uses the available Syriac line codepoint on both covered letters for a span, so that same Unicode sequence is also capable of representing two separate adjacent one-letter lines. The physical page resolves that grouping. The canonical wrappers preserve the resolution: `(xy)` is one span; `(x)(y)` is two separate lines.

### Transliteration use

```bash
python tools/transliterate.py normalized.txt > canonical.txt
python tools/transliterate.py canonical.txt --reverse > normalized.txt
```

When adjacent same-direction line marks occur, supply the page grouping explicitly:

```bash
python tools/transliterate.py normalized.txt \
  --occultans-span 1:3:above

python tools/transliterate.py normalized.txt \
  --occultans-separate 1:3:above
```

The `--occultans-*` option names are retained for compatibility with the first transliteration-engine release. They now mean **line grouping**, not a claim that a two-letter span is occultans. `span` selects one physical two-letter line (marheṭānā for the attested upper cluster case); `separate` selects two adjacent one-letter lines.

Coordinates are `WORD:LETTER:above|below`, with the letter being the left member of the adjacent pair. The forward CLI prints the letter-by-letter audit with canonical headers to stderr and the canonical transliteration to stdout.

### Library API

```python
from east_syriac import (
    normalize_text,
    inspect_normalized_text,
    transliterate_text,
    reverse_transliterate,
)

normalized = normalize_text(raw)
audit = inspect_normalized_text(normalized.text)
canonical = transliterate_text(normalized.text)
reversed_text = reverse_transliterate(canonical.text)

assert reversed_text.text == normalized.text
```

`reverse_transliterate()` also returns the page grouping encoded by adjacent wrappers. The current public field/API retains the historical `occultans_resolutions` name for compatibility; semantically it is span/separate **line-grouping metadata**.

## Phase 3: confirmed-text parser/checker

`east_syriac.confirmed_text` implements General Rules §9.1, §9.1.1, and §11.15–16 for authoritative confirmed-text files. `east_syriac.provenance` validates the source registry, and `check_confirmed_text.py` is the command-line front end for the combined corpus check.

The checker validates:

- strict UTF-8, no BOM, LF-only line endings, NFC, no trailing whitespace, straight apostrophes, `.txt`/`.md` format, and U+0020/LF as the only whitespace;
- exactly three aligned layers: Syriac, canonical transliteration, English;
- equal logical line counts across the three layers;
- identical stanza-break positions across all three layers;
- valid canonical inverse parsing on every transliteration line;
- exact canonical → Syriac reconstruction;
- fresh Syriac → canonical derivation and byte-for-byte comparison with the stored transliteration line;
- one `sources/sources.yaml` record for every confirmed file and no stale registry records;
- one declared `source_of_record` and one unique stable `citation_label` for every confirmed text.

Block detection does **not** assume that every blank line ends a block. A stanza break is itself a blank logical line, so the parser searches for the unique pair of separator runs that yields three equal layers with the same stanza pattern. This lets stanza breaks remain legal without making the three-layer format ambiguous.

The stored transliteration is not an authority for ordinary orthography. The checker derives Latin from Syriac. The sole exception is page-only grouping metadata for adjacent same-direction line marks: normalized Syriac cannot recover whether the page showed one span or two separate lines. The checker may recover that grouping from the stored canonical line **only when the entire canonical line already reverses exactly to the Syriac line**. In the confirmed Our Father, this preserves the page-confirmed marheṭānā grouping of `šba(q_n)` without treating the Latin as an independent orthographic authority.

### Confirmed-text use

Check the whole authoritative corpus and its provenance registry:

```bash
python tools/check_confirmed_text.py
```

Check selected files/directories (the corpus-level provenance registry is still checked):

```bash
python tools/check_confirmed_text.py confirmed-texts/Creed.txt
python tools/check_confirmed_text.py confirmed-texts
```

Show the mechanically derived transliteration block when all page-only information is resolved:

```bash
python tools/check_confirmed_text.py confirmed-texts/Creed.txt --show-derived
```

Exit status is `0` when every checked file and corpus provenance pass, `1` for validation failures, and `2` for file/selection errors. The checker never rewrites a confirmed text automatically; failures remain visible for review.

### Confirmed-text and provenance library APIs

```python
from east_syriac import (
    check_confirmed_text_path,
    check_source_registry_path,
    parse_confirmed_text,
)

result = check_confirmed_text_path("confirmed-texts/Creed.txt")
assert result.ok
assert result.document is not None

provenance_issues = check_source_registry_path(
    "sources/sources.yaml",
    "confirmed-texts",
)
assert not provenance_issues

# The expected Latin block was generated from Syriac, not copied from the file.
expected = result.expected_transliteration_block
```

The live corpus regression runs every current confirmed `.txt`/`.md` file through the same content checker and separately verifies the source registry. Therefore a Syriac edit with stale transliteration, unequal layers, malformed stanza alignment, file-hygiene corruption, a missing source designation, or a stale confirmed filename fails CI.

## Validation

Run the complete suite with:

```bash
python -m unittest discover -s tools/tests -v
```

The normalization torture corpus remains in `normalization-stress-corpus.md`. Transliteration and confirmed-text tests add independent protections:

1. focused normalization/transliteration rule and edge-case tests;
2. generated canonical-unit coverage with collision detection and exact round trips;
3. a prefix/segmentation proof that concatenated canonical units cannot acquire a second parse;
4. hostile confirmed-text structure/hygiene/staleness tests;
5. source-registry/provenance identity tests;
6. live corpus regression through the full three-block checker and provenance registry.

GitHub Actions runs compilation and the full deterministic suite on tooling pushes and pull requests.

## Intended pipeline

1. **Normalize source codepoints to page-state**.
2. **Human page-state audit** — mandatory for page comparison, including span/separate grouping when Unicode is lossy.
3. **Canonical transliteration** — normalized Syriac → reversible Latin string, preserving one-letter lines and page-confirmed marheṭānā spans.
4. **Inverse transliteration** — canonical string → normalized Syriac plus any page-only line-grouping metadata.
5. **Round-trip checks** — Transliteration Rules §12 and General Rules §11.11–14.
6. **Confirmed-text parser/checker** — equal layers, file hygiene, stanza alignment, mechanically fresh transliteration, and source-registry provenance.
7. **Glossary/corpus checks** — remainder of General Rules §11.

Each stage remains deterministic and independently testable.
