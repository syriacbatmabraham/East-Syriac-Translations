# Deterministic tools

The code in this directory implements mechanical parts of the East Syriac Translation workflow. The rule files remain authoritative; code is an executable implementation of those rules, not a second specification.

## Phase 1: source normalization

`normalize.py` implements source-ingestion normalization from **Transliteration Rules §16** and same-class combining-mark order from **§5.1**. It accepts a raw Syriac block and produces the normalized Syriac representation consumed by transliteration.

The normalizer is intentionally conservative: licensed transformations are automatic; refused/unrecognized states are preserved and flagged; West Syriac vowels are never mapped into East Syriac vowels; bare U+0716 normalizes to resh with a review flag; arbitrary unknown non-combining codepoints outside editorial apparatus are retained and flagged; malformed editorial delimiters are flagged; and persistent writes are refused while blocking source/page-state problems remain.

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

If a page-only ambiguity prevents automatic transliteration—currently an unresolved adjacent occultans span/separate question—the audit keeps the Syriac header and prints the required `PAGE CHECK` rather than guessing.

The post-normalization audit detects contradictions Unicode normalization alone cannot catch: multiple vowels on one carrier, both qūššāyā and rūkkākā on one bgdkpt letter, invalid canonical carriers, duplicate marks, and occultans simultaneously above and below one carrier. The last state is in-scope Unicode but has no reversible notation under the current canonical rules, so it is blocking rather than silently encoded.

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
- one-letter and page-resolved two-letter occultans notation above or below;
- strict NFC canonical strings;
- canonicality checking by re-forwarding every inverse parse.

The final-mater shorthand is deliberately narrow: a bare final ʾālap̄ is suppressed only when it immediately follows its zqāpā/zlāmā-qašyā carrier with no editorial delimiter between them. Thus `[ܡܵܐ]` gives `[mā]`, while `ܡܵ[ܐ]` gives `mā[ʾ]` and `[ܡܵ][ܐ]` gives `[mā][ʾ]`.

### Transliteration use

```bash
python tools/transliterate.py normalized.txt > canonical.txt
python tools/transliterate.py canonical.txt --reverse > normalized.txt
```

When adjacent same-direction occultans marks occur, encoded Syriac cannot say whether the page shows one span or two separate lines. Supply the page decision explicitly:

```bash
python tools/transliterate.py normalized.txt \
  --occultans-span 1:3:above

python tools/transliterate.py normalized.txt \
  --occultans-separate 1:3:above
```

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

`reverse_transliterate()` also returns the span/separate occultans decisions encoded by the canonical wrappers. Those decisions are the only page information the normalized Syriac codepoints themselves cannot recover.

## Phase 3: confirmed-text parser/checker

`east_syriac.confirmed_text` implements General Rules §9.1, §9.1.1, and §11.15–16 for authoritative confirmed-text files. `check_confirmed_text.py` is the command-line front end.

The checker validates:

- strict UTF-8, no BOM, LF-only line endings, NFC, no trailing whitespace, straight apostrophes, and `.txt`/`.md` format;
- exactly three aligned layers: Syriac, canonical transliteration, English;
- equal logical line counts across the three layers;
- identical stanza-break positions across all three layers;
- valid canonical inverse parsing on every transliteration line;
- exact canonical → Syriac reconstruction;
- fresh Syriac → canonical derivation and byte-for-byte comparison with the stored transliteration line.

Block detection does **not** assume that every blank line ends a block. A stanza break is itself a blank logical line, so the parser searches for the unique pair of separator runs that yields three equal layers with the same stanza pattern. This lets stanza breaks remain legal without making the three-layer format ambiguous.

The stored transliteration is not an authority for ordinary orthography. The checker derives Latin from Syriac. The sole exception is page-only adjacent-occultans grouping: encoded Syriac cannot recover whether the page shows one span or two separate lines. The checker may recover that decision from the stored canonical line **only when the entire canonical line already reverses exactly to the Syriac line**. If it does not, the checker requires page resolution rather than trusting stale Latin.

### Confirmed-text use

Check the whole authoritative corpus:

```bash
python tools/check_confirmed_text.py
```

Check selected files/directories:

```bash
python tools/check_confirmed_text.py confirmed-texts/Creed_in_Syriac.txt
python tools/check_confirmed_text.py confirmed-texts
```

Show the mechanically derived transliteration block when all page-only information is resolved:

```bash
python tools/check_confirmed_text.py confirmed-texts/Creed_in_Syriac.txt --show-derived
```

Exit status is `0` when every checked file passes, `1` for validation failures, and `2` for file/selection errors. The checker never rewrites a confirmed text automatically; failures remain visible for review.

### Confirmed-text library API

```python
from east_syriac import check_confirmed_text_path, parse_confirmed_text

result = check_confirmed_text_path("confirmed-texts/Creed_in_Syriac.txt")
assert result.ok
assert result.document is not None

# The expected Latin block was generated from Syriac, not copied from the file.
expected = result.expected_transliteration_block
```

The live corpus regression runs every current confirmed `.txt`/`.md` file through this same checker. Therefore a Syriac edit with stale transliteration, unequal layers, malformed stanza alignment, or file-hygiene corruption fails CI before it can enter a clean `main` branch.

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
5. live corpus regression through the full three-block checker.

GitHub Actions runs compilation and the full deterministic suite on tooling pushes and pull requests.

## Intended pipeline

1. **Normalize source codepoints to page-state**.
2. **Human page-state audit** — mandatory for page comparison.
3. **Canonical transliteration** — normalized Syriac → reversible Latin string.
4. **Inverse transliteration** — canonical string → normalized Syriac.
5. **Round-trip checks** — Transliteration Rules §12 and General Rules §11.11–14.
6. **Confirmed-text parser/checker** — equal layers, file hygiene, stanza alignment, and mechanically fresh transliteration.
7. **Glossary/corpus checks** — remainder of General Rules §11.

Each stage remains deterministic and independently testable.
