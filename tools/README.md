# Deterministic tools

The code in this directory implements mechanical parts of the East Syriac Translation workflow. The rule files remain authoritative; code is an executable implementation of those rules, not a second specification.

## Phase 1: source normalization

`normalize.py` implements source-ingestion normalization from **Transliteration Rules §16** and same-class combining-mark order from **§5.1**. It accepts a raw Syriac block and produces the normalized Syriac representation that later transliteration code will consume.

The normalizer is intentionally conservative:

- transformations explicitly licensed by the rules are automatic;
- refused or unrecognized page-states are preserved and flagged;
- West Syriac vowels are never mapped into East Syriac vowels;
- bare U+0716 becomes resh but always raises the required review flag;
- arbitrary unknown non-combining codepoints outside editorial apparatus are retained and flagged rather than silently admitted;
- malformed editorial brackets/parentheses are flagged;
- persistent writes are refused while any blocking review flag/page-state issue exists;
- Latin text outside parenthesized editorial apparatus is flagged, which also protects against accidentally running the tool in-place on a complete three-block confirmed text.

## Mandatory page-state audit

During the validation phase every normalization run prints a human-readable, letter-by-letter audit to stderr. It states what the machine believes is present on each Syriac carrier, for example:

```text
Word 1: *lʾalāhā*
Lamad
Alaph (pṯāḥā: a)
Lamad (zqāpā: ā)
Heh (zqāpā: ā)
Alaph
```

Until canonical transliteration is implemented, the header displays the normalized Syriac token instead. The audit API already accepts one canonical label per word, so forward transliteration can supply `*lʾalāhā*` automatically without changing the letter analysis.

The post-normalization audit also detects contradictions that Unicode normalization alone cannot catch, such as two vowels on one carrier, both qūššāyā and rūkkākā on one bgdkpt letter, invalid canonical carriers, and duplicate marks.

Adjacent occultans marks are different: encoded Syriac cannot distinguish one spanning line from two separate adjacent lines. They therefore emit a non-blocking `PAGE CHECK` notice. The normalized Syriac may be stored, but the page must settle the span before forward transliteration chooses `(xy)` versus `(x)(y)`.

### Typical use

Inspect normalization without changing a file:

```bash
python tools/normalize.py source.txt > normalized.txt
```

The normalized Syriac goes to stdout; flags, page-state issues/notices, and the mandatory audit go to stderr.

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

- `0` — already normalized, no blocking flags/issues;
- `1` — deterministic normalization changes are needed, no blocking flags/issues;
- `2` — at least one condition requires correction/review (or a CLI/file error occurred).

A page-only notice such as adjacent occultans does not make the encoded Syriac invalid and therefore does not change the normalization exit code. It must be resolved before transliteration.

The first CLI intentionally works on the **Syriac layer only**, not on a complete confirmed-text file. Confirmed-text parsing belongs in the later check-suite layer, where all three blocks can be validated together without risking the transliteration or English blocks.

### Library API

```python
from east_syriac import normalize_text, inspect_normalized_text, format_page_state_report

result = normalize_text(syriac)
audit = inspect_normalized_text(result.text)

result.text       # normalized Syriac
result.flags      # source-ingestion conditions requiring review
audit.issues      # contradictory/suspicious normalized states
audit.notices     # page-only ambiguities such as adjacent occultans
```

Keeping the engine separate from the CLI is deliberate. The same functions can later be called by transliteration, round-trip validation, repository checks, or an interactive application without shelling out to a script.

## Final torture coverage

`normalization-stress-corpus.md` defines the compact human-readable torture corpus. `tests/test_normalization_coverage.py` enforces the exhaustive boundary programmatically.

The coverage contract includes:

- every assigned codepoint in U+0700–U+074F;
- every extra generic codepoint named by the rules;
- all six bgdkpt letters in hard, soft, and unmarked states;
- every single-point source alias across every carrier class that changes its meaning;
- every East Syriac vowel and special mark;
- every two-dots-below alias;
- every West Syriac vowel refusal;
- all assigned non-project Syriac letters and unsupported Syriac marks;
- editorial structure, word division, and all explicitly removable debris;
- arbitrary unknown non-combining codepoints;
- malformed clusters and impossible normalized states;
- word-final/mater shapes that must remain literal for later transliteration;
- adjacent occultans as the known encoded-source/page asymmetry.

The suite deliberately does **not** attempt every combinatorial arrangement of every mark. It closes every finite interface where behavior can differ, then requires genuinely new/unrecognized input to raise a review flag.

## Tests

Run:

```bash
python -m unittest discover -s tools/tests -v
```

GitHub Actions runs compilation and the deterministic test suite on tooling changes.

## Intended pipeline

1. **Normalize source codepoints to page-state** — current phase.
2. **Human page-state audit** — currently mandatory for page comparison.
3. **Canonical transliteration** — normalized Syriac → reversible Latin string; its word tokens become the audit headers automatically.
4. **Inverse transliteration** — canonical string → normalized Syriac.
5. **Round-trip checks** — enforce Transliteration Rules §12 and General Rules §11.11–14.
6. **Confirmed-text parser/checker** — validate the three equal line blocks and derive transliteration mechanically.
7. **Glossary/corpus checks** — coverage, identity, citations, contexts, morphology, and the remainder of General Rules §11.

Each stage remains deterministic and independently testable.
