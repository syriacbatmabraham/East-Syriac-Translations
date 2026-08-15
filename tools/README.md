# Deterministic tools

The code in this directory implements mechanical parts of the East Syriac Translation workflow. The rule files remain authoritative; code is an executable implementation of those rules, not a second specification.

## Phase 1: source normalization

`normalize.py` implements source-ingestion normalization from **Transliteration Rules §16** and same-class combining-mark order from **§5.1**. It accepts a raw Syriac block and produces the normalized Syriac representation that later transliteration code will consume.

The normalizer is intentionally conservative: licensed transformations are automatic; refused/unrecognized states are preserved and flagged; West Syriac vowels are never mapped into East Syriac vowels; bare U+0716 normalizes to resh with a review flag; arbitrary unknown non-combining codepoints outside editorial apparatus are retained and flagged; malformed editorial delimiters are flagged; and persistent writes are refused while blocking source/page-state problems remain.

## Mandatory page-state audit

During validation every normalization run prints a human-readable, letter-by-letter audit to stderr. It states what the machine believes is present on each Syriac carrier:

```text
Word 1: *lʾalāhā*
Lamad
Alaph (pṯāḥā: a)
Lamad (zqāpā: ā)
Heh (zqāpā: ā)
Alaph
```

Until canonical transliteration exists, the header displays the normalized Syriac token. The audit API already accepts one canonical label per word, so forward transliteration can supply `*lʾalāhā*` automatically without changing the letter analysis.

The post-normalization audit detects contradictions Unicode normalization alone cannot catch: multiple vowels on one carrier, both qūššāyā and rūkkākā on one bgdkpt letter, invalid canonical carriers, and duplicate marks.

Adjacent occultans marks are a page-only ambiguity. Encoded Syriac cannot distinguish one spanning line from two separate adjacent lines, so the audit emits a non-blocking `PAGE CHECK`. The normalized Syriac may be stored, but the page must settle the span before forward transliteration chooses `(xy)` versus `(x)(y)`.

### Typical use

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

A page-only notice such as adjacent occultans does not make the encoded Syriac invalid and therefore does not change the normalization exit code. It must be resolved before transliteration.

The first CLI intentionally works on the **Syriac layer only**, not on a complete confirmed-text file.

### Library API

```python
from east_syriac import normalize_text, inspect_normalized_text, format_page_state_report

result = normalize_text(syriac)
audit = inspect_normalized_text(result.text)

result.text       # normalized Syriac
result.flags      # source-ingestion review conditions
audit.issues      # contradictory/suspicious normalized states
audit.notices     # page-only ambiguities such as adjacent occultans
```

## Final torture coverage

`normalization-stress-corpus.md` defines the compact human-readable torture corpus. `tests/test_normalization_coverage.py` enforces the exhaustive boundary programmatically.

The executable suite currently contains **74 deterministic tests** across baseline normalization, page-state inspection, focused stress cases, and the exhaustive coverage matrix.

Coverage includes every assigned codepoint in U+0700–U+074F; every extra generic codepoint named by the rules; all bgdkpt states; every carrier-sensitive single-point alias × carrier class; all East Syriac vowel/special states and aliases; every West Syriac vowel refusal; all assigned non-project Syriac letters/unsupported marks; editorial structure, word division, and removable debris; arbitrary unknown non-combining codepoints; malformed clusters and impossible normalized states; positional/mater pass-through forms; and the adjacent-occultans source/page asymmetry.

The suite does **not** attempt every mathematical combination of marks. It closes every finite interface where behavior can differ, then requires genuinely new/unrecognized input to raise a review flag. Coverage is exhaustive relative to the current governing rules and Unicode/source grammar; genuinely new witness-specific encodings become permanent regression cases when first encountered.

## Tests

```bash
python -m unittest discover -s tools/tests -v
```

GitHub Actions runs compilation and the deterministic test suite on tooling changes.

## Intended pipeline

1. **Normalize source codepoints to page-state**.
2. **Human page-state audit** — currently mandatory for page comparison.
3. **Canonical transliteration** — normalized Syriac → reversible Latin string; its word tokens become audit headers automatically.
4. **Inverse transliteration** — canonical string → normalized Syriac.
5. **Round-trip checks** — Transliteration Rules §12 and General Rules §11.11–14.
6. **Confirmed-text parser/checker** — validate equal blocks and derive transliteration mechanically.
7. **Glossary/corpus checks** — remainder of General Rules §11.

Each stage remains deterministic and independently testable.
