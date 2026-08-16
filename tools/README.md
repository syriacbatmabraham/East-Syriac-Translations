# Deterministic tools

The code in this directory implements mechanical parts of the East Syriac Translation workflow. The rule files remain authoritative; code is an executable implementation of those rules, not a second specification.

## Phase 1: source normalization

`normalize.py` implements source-ingestion normalization from **Transliteration Rules §16** and combining-mark order from **§5.1**. It accepts a raw Syriac block and produces the normalized Syriac representation consumed by transliteration after the mandatory page-state audit.

The normalizer is intentionally conservative: licensed transformations are automatic; refused/unrecognized states are preserved and flagged; West Syriac vowels are never mapped into East Syriac vowels; bare U+0716 normalizes to resh with a review flag; arbitrary unknown non-combining codepoints outside editorial apparatus are retained and flagged; malformed editorial delimiters are flagged; and persistent writes are refused while blocking source/page-state problems remain. Project text whitespace is deliberately narrow: only U+0020 SPACE and U+000A LF are accepted; tabs, non-breaking spaces and other Unicode whitespace are retained and flagged for review.

**Single-point identity is direct.** U+0741 qūššāyā, U+0742 rūkkākā, U+073F rwāḥā, U+073C the Class-A carrier-vowel mark, and generic U+0307/U+0323 are not aliases for one another. In particular, a generic point on waw, yodh, or a bgdkpt letter remains generic; the normalizer never turns it into a vowel or hard/soft point merely from its carrier. If a raw witness used the wrong codepoint for the shape actually visible on the page, the mandatory human page audit corrects the canonical Syriac codepoint before confirmation.

Canonical two-letter spanning lines are represented directly in the Syriac layer:

- **U+035E COMBINING DOUBLE MACRON** after the first base = one upper span over that base and the next;
- **U+035F COMBINING DOUBLE MACRON BELOW** after the first base = one lower span over that base and the next;
- U+0747/U+0748 remain one-letter line marks.

## Mandatory page-state audit

During validation every normalization run prints a human-readable letter-by-letter audit to stderr. It states what the machine believes is present on each Syriac carrier.

With the transliteration engine available, clean input receives canonical word headers automatically:

```text
Word 1: *lʾalāhā*
Lamad
Alaph (pṯāḥā: a)
Lamad (zqāpā: ā)
Heh (zqāpā: ā)
Alaph
```

A raw digital witness may use repeated U+0747/U+0748 to approximate one printed spanning line. The audit therefore emits a nonblocking page notice when same-direction one-letter line codepoints occur on adjacent letters. Compare the page before confirmation:

- if the page shows one physical span, correct the canonical Syriac page-state to U+035E/U+035F after the first base;
- if the page shows two separate one-letter lines, retain the two U+0747/U+0748 marks.

Once that page decision is incorporated into normalized Syriac, **no span/separate metadata exists outside the Syriac string**. The confirmed qoph–nun case is stored as `ܫܒܲܩ̣͞ܢ`, whose U+035E span is the page-confirmed upper marheṭānā over the pronounced vowelless `qn` cluster.

The post-normalization audit also detects contradictions Unicode normalization alone cannot catch: multiple vowels on one carrier, both qūššāyā and rūkkākā on one bgdkpt letter, invalid canonical carriers, duplicate marks, one-letter lines both above and below the same carrier, a two-letter span with no following base, overlapping spans, and simultaneous upper/lower span starts.

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

A page notice does not make the encoded string structurally invalid and therefore does not change the normalization exit code. It still requires human comparison with the page before a text is confirmed.

## Phase 2: reversible canonical transliteration

`east_syriac.transliteration` implements normalized Syriac → canonical Latin. `east_syriac.transliteration_inverse` implements the exact inverse. Forward transliteration never normalizes, repairs, or linguistically infers its input: it accepts only a clean normalized page-state produced by Phase 1 and the page audit.

The implementation includes:

- all canonical consonants and the three bgdkpt states;
- Class A and Class B vowels;
- word-final `ā/ă` and `ē/ĕ` conventions;
- syāmē, the distinguishing point, between-letter points, two dots below, breve below, and superscript ʾālap̄;
- editorial square brackets and parenthesized source/witness apparatus;
- one-letter line wrappers above/below;
- direct two-letter spans encoded by U+035E/U+035F and transliterated with `⁀`/`‿`;
- strict NFC canonical strings;
- canonicality checking by re-forwarding every inverse parse.

The final-mater shorthand is deliberately narrow: a bare final ʾālap̄ is suppressed only when it immediately follows its zqāpā/zlāmā-qašyā carrier with no editorial delimiter and is not the second base of a two-letter span. Thus `[ܡܵܐ]` gives `[mā]`, while `ܡܵ[ܐ]` gives `mā[ʾ]` and `[ܡܵ][ܐ]` gives `[mā][ʾ]`.

### One-letter lines and marheṭānā spans

A wrapper around one canonical letter-unit, such as `(h)`, records a line carried by that one letter. The project does not infer from the graphic stroke alone whether a traditional one-letter line is functioning as *mṭalqānā* or *mhaggyānā*.

A physical two-letter span is **not parenthesized**:

- upper U+035E span → `x⁀y` using U+2040 CHARACTER TIE;
- lower U+035F span → `x‿y` using U+203F UNDERTIE.

The confirmed example is:

```text
ܫܒܲܩ̣͞ܢ  ⇄  šbaq_⁀n
```

The page-confirmed upper line is marheṭānā joining qoph and nun as a pronounced vowelless cluster. Neither consonant is suppressed. By contrast, adjacent one-letter marks remain visibly separate, e.g. `ܡ݇ܢ݇ ⇄ (m)(n)`.

The retired two-letter parenthetical syntax such as `(mn)` or `šba(q_n)` is rejected by the inverse parser with a migration error rather than accepted as editorial apparatus.

### Transliteration use

```bash
python tools/transliterate.py normalized.txt > canonical.txt
python tools/transliterate.py canonical.txt --reverse > normalized.txt
```

There are **no `--occultans-span` or `--occultans-separate` options**. Span versus separate is already encoded in the normalized Syriac before transliteration begins.

The forward CLI prints the letter-by-letter audit with canonical headers to stderr and the canonical transliteration to stdout.

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

`reverse_transliterate()` returns the normalized Syriac itself. There is no auxiliary span-resolution field because the Syriac codepoints carry the complete page-state distinction.

## Phase 3: confirmed-text parser/checker

`east_syriac.confirmed_text` implements General Rules §9.1, §9.1.1, and §11.15–16 for authoritative confirmed-text files. `east_syriac.provenance` validates the source registry, and `check_confirmed_text.py` is the command-line front end for the combined corpus check.

The checker validates:

- strict UTF-8, no BOM, LF-only line endings, NFC, no trailing whitespace, straight apostrophes, `.txt`/`.md` format, and U+0020/LF as the only whitespace;
- exactly three aligned layers: Syriac, canonical transliteration, English;
- equal logical line counts across the three layers;
- identical stanza-break positions across all three layers;
- valid canonical inverse parsing on every transliteration line;
- exact canonical → Syriac reconstruction;
- **independent fresh Syriac → canonical derivation** and byte-for-byte comparison with the stored transliteration line;
- one `sources/sources.yaml` record for every confirmed file and no stale registry records;
- one declared `source_of_record` and one unique stable `citation_label` for every confirmed text.

Block detection does **not** assume that every blank line ends a block. A stanza break is itself a blank logical line, so the parser searches for the unique pair of separator runs that yields three equal layers with the same stanza pattern. This lets stanza breaks remain legal without making the three-layer format ambiguous.

The stored transliteration supplies **no page-state information** to the checker. The checker can always derive the expected Latin independently from the Syriac because direct two-letter spans are encoded with U+035E/U+035F in that Syriac layer. A stale or malformed stored Latin line is therefore diagnosable without losing the mechanically expected result. This removes the former circular exception for adjacent-line grouping.

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

Show the mechanically derived transliteration block:

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

1. focused normalization/transliteration rule and edge-case tests, including direct upper/lower spans and adjacent separate one-letter marks;
2. generated canonical-unit coverage with collision detection and exact round trips;
3. a prefix/segmentation proof that concatenated canonical units cannot acquire a second parse;
4. hostile confirmed-text structure/hygiene/staleness tests, including stale marheṭānā Latin derived independently from Syriac;
5. source-registry/provenance identity tests;
6. live corpus regression through the full three-block checker and provenance registry.

GitHub Actions runs compilation and the full deterministic suite on tooling pushes and pull requests.

## Intended pipeline

1. **Normalize source codepoints to preliminary page-state without carrier-based point inference**.
2. **Human page-state audit** — mandatory for comparison with the source page; where a raw witness approximates a span with repeated one-letter codepoints, correct the normalized Syriac to U+035E/U+035F here.
3. **Canonical transliteration** — resolved normalized Syriac → reversible Latin string. No page metadata is supplied separately.
4. **Inverse transliteration** — canonical string → resolved normalized Syriac.
5. **Round-trip checks** — Transliteration Rules §12 and General Rules §11.11–14.
6. **Confirmed-text parser/checker** — equal layers, file hygiene, stanza alignment, independently fresh transliteration, and source-registry provenance.
7. **Glossary/corpus checks** — remainder of General Rules §11.

Each stage remains deterministic and independently testable.
