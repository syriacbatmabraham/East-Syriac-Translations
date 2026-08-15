# Deterministic tools

The code in this directory implements mechanical parts of the East Syriac Translation workflow. The rule files remain authoritative; code is an executable implementation of those rules, not a second specification.

## Phase 1: source normalization

`normalize.py` implements source-ingestion normalization from **Transliteration Rules §16** and same-class combining-mark order from **§5.1**. It accepts a raw Syriac block and produces the normalized Syriac representation that later transliteration code will consume.

The normalizer is intentionally conservative:

- transformations explicitly licensed by the rules are automatic;
- refused or unrecognized page-states are preserved and flagged;
- West Syriac vowels are never mapped into East Syriac vowels;
- bare U+0716 becomes resh but always raises the required review flag;
- persistent writes are refused while any review flag exists;
- Latin text outside parenthesized editorial apparatus is flagged, which also protects against accidentally running the tool in-place on a complete three-block confirmed text.

### Typical use

Inspect normalization without changing a file:

```bash
python tools/normalize.py source.txt > normalized.txt
```

Show every deterministic codepoint change as well:

```bash
python tools/normalize.py source.txt --report-changes > normalized.txt
```

Normalize a clean, review-free source in place:

```bash
python tools/normalize.py source.txt --in-place
```

Check whether a source is already normalized without writing anything:

```bash
python tools/normalize.py source.txt --check
```

`--check` exit status:

- `0` — already normalized, no flags;
- `1` — deterministic normalization changes are needed, no flags;
- `2` — at least one condition requires review (or a CLI/file error occurred).

The first CLI intentionally works on the **Syriac layer only**, not on a complete confirmed-text file. Confirmed-text parsing belongs in the later check-suite layer, where all three blocks can be validated together without risking the transliteration or English blocks.

### Library API

The reusable implementation lives in `east_syriac.normalization`:

```python
from east_syriac.normalization import normalize_text

result = normalize_text(syriac)
result.text       # normalized Syriac
result.flags      # conditions requiring source review
result.changes    # deterministic transformations performed
```

Keeping the engine separate from the CLI is deliberate. The same function can later be called by transliteration, round-trip validation, repository checks, or an interactive application without shelling out to a script.

## Tests

The normalization layer uses only the Python standard library. Run:

```bash
python -m unittest discover -s tools/tests -v
```

The tests cover carrier-sensitive single-point normalization, U+0716, final semkath, two-dots-below aliases, West Syriac refusal, unrecognized marks, §5.1 order for combining classes 220 and 230, NFC behavior, idempotence, and write-safety guards.

## Intended pipeline

The machinery is being built in stages:

1. **Normalize source codepoints to page-state** — current phase.
2. **Canonical transliteration** — normalized Syriac → reversible Latin string.
3. **Inverse transliteration** — canonical string → normalized Syriac.
4. **Round-trip checks** — enforce Transliteration Rules §12 and General Rules §11.11–14.
5. **Confirmed-text parser/checker** — validate the three equal line blocks and derive transliteration mechanically.
6. **Glossary/corpus checks** — coverage, identity, citations, contexts, morphology, and the remainder of General Rules §11.

Each stage should remain deterministic and independently testable.
