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

## Mandatory page-state audit

Normalization is followed immediately by a **human-readable letter-by-letter audit**. During this validation phase the CLI prints this audit on every run. It goes to stderr, so normalized Syriac on stdout remains clean for redirection and later deterministic pipeline stages.

The purpose is not to tell the reviewer what a word ought to contain. It states exactly what the machine believes is present on each normalized carrier.

For example, once canonical transliteration is connected to the audit, the normalized Syriac `ܠܐܲܠܵܗܵܐ` will display as:

```text
Word 1: *lʾalāhā*
Lamad
Alaph (pṯāḥā: a)
Lamad (zqāpā: ā)
Heh (zqāpā: ā)
Alaph
```

Until the transliteration layer is implemented, the same report uses the normalized Syriac word itself as the header. The audit API already accepts one canonical label per word, so the later transliterator can replace the header automatically without changing the letter analysis.

Every mark on a letter is named. Dense states therefore remain visible, for example:

```text
Mim (zqāpā: ā; single point above; syāmē; occultans line above)
```

The audit also checks normalized-state invariants that Unicode normalization alone cannot establish. Examples include:

- qūššāyā/rūkkākā on an invalid carrier;
- both qūššāyā and rūkkākā on the same bgdkpt letter;
- more than one East Syriac vowel state on one carrier;
- duplicate normalized marks;
- canonical carrier-vowel codepoints on the wrong carrier.

A page-state issue blocks `--in-place` and `--output` exactly like a source-normalization flag. This keeps a syntactically normalized but implausible page-state from silently entering project data.

The audit is deliberately a separate layer (`east_syriac.inspection`) rather than being folded into transliteration. It can therefore remain in the workflow for as long as human page comparison is useful, even after transliteration becomes fully automatic.

### Typical use

Inspect normalization without changing a file:

```bash
python tools/normalize.py source.txt > normalized.txt
```

The normalized Syriac goes to `normalized.txt`; the letter-by-letter page-state audit appears in the terminal.

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

- `0` — already normalized, no normalization flags or page-state issues;
- `1` — deterministic normalization changes are needed, no flags/issues;
- `2` — at least one condition requires review (or a CLI/file error occurred).

The first CLI intentionally works on the **Syriac layer only**, not on a complete confirmed-text file. Confirmed-text parsing belongs in the later check-suite layer, where all three blocks can be validated together without risking the transliteration or English blocks.

### Library API

The reusable normalization implementation lives in `east_syriac.normalization`:

```python
from east_syriac.normalization import normalize_text

result = normalize_text(syriac)
result.text       # normalized Syriac
result.flags      # conditions requiring source review
result.changes    # deterministic transformations performed
```

The page-state layer lives in `east_syriac.inspection`:

```python
from east_syriac.inspection import inspect_normalized_text, format_page_state_report

audit = inspect_normalized_text(result.text)
audit.words       # structured word/letter/mark states
audit.issues      # implausible normalized page-states

print(format_page_state_report(result.text))
```

Later, canonical transliteration can supply the report headers without re-parsing the page-state:

```python
format_page_state_report(result.text, word_labels=["lʾalāhā"])
```

Keeping the engines separate from the CLI is deliberate. The same functions can later be called by transliteration, round-trip validation, repository checks, or an interactive application without shelling out to a script.

## Synthetic stress corpus

`normalization-stress-corpus.md` contains deliberately imaginary Syriac pseudo-words designed to force unusual normalization paths and implausible normalized states. It includes carrier-sensitive aliases, maximal same-class mark stacks, U+0716, between-letter points, typesetting debris, every West Syriac vowel class, contradictory bgdkpt states, multiple vowels on one carrier, and duplicate marks.

The corresponding executable regression cases live in `tests/test_normalization_stress.py`. When a real source exposes a new strange encoding or page-state, reduce it to the smallest possible synthetic case and add it to both the corpus and tests.

## Tests

The normalization layer uses only the Python standard library. Run:

```bash
python -m unittest discover -s tools/tests -v
```

The tests cover carrier-sensitive single-point normalization, U+0716, final semkath, two-dots-below aliases, West Syriac refusal, unrecognized marks, §5.1 order for combining classes 220 and 230, NFC behavior, idempotence, write-safety guards, page-state reporting, normalized-state invariants, and the synthetic torture corpus.

## Intended pipeline

The machinery is being built in stages:

1. **Normalize source codepoints to page-state** — current phase.
2. **Expose normalized page-state letter by letter for human verification** — current phase; intentionally retained during early use.
3. **Canonical transliteration** — normalized Syriac → reversible Latin string; its word tokens will become the audit headers automatically.
4. **Inverse transliteration** — canonical string → normalized Syriac.
5. **Round-trip checks** — enforce Transliteration Rules §12 and General Rules §11.11–14.
6. **Confirmed-text parser/checker** — validate the three equal line blocks and derive transliteration mechanically.
7. **Glossary/corpus checks** — coverage, identity, citations, contexts, morphology, and the remainder of General Rules §11.

Each stage should remain deterministic and independently testable.
