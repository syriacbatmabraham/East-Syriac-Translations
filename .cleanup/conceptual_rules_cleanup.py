from pathlib import Path
import re
import subprocess
import unicodedata


def replace_exact(path, old, new, expected=1):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    found = s.count(old)
    if found != expected:
        raise SystemExit(f'{path}: expected {expected} matches, found {found}: {old[:100]!r}')
    p.write_text(s.replace(old, new), encoding='utf-8')


def replace_section(path, start, end, replacement):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if s.count(start) != 1 or s.count(end) != 1:
        raise SystemExit(f'{path}: section markers not unique: {start!r} / {end!r}')
    a = s.index(start)
    b = s.index(end, a)
    p.write_text(s[:a] + replacement + s[b:], encoding='utf-8')


old_translit = Path('rules/Transliteration-Rules-v2_3_1.md')
translit = Path('rules/Transliteration-Rules.md')
general = Path('rules/General-Rules.md')

if not old_translit.exists() or translit.exists():
    raise SystemExit('unexpected transliteration-rules rename state')
subprocess.run(['git', 'mv', str(old_translit), str(translit)], check=True)

# 1. Defective Class-A vowels: withdraw unestablished carrierless forms.
replace_exact(
    translit,
    '# Transliteration Rules v2.3.1 — Reversible Canonical Transliteration',
    '# Transliteration Rules — Reversible Canonical Transliteration'
)
replace_exact(
    translit,
    '**Versioning.** The third digit marks a revision that changes no rule — an audit-log row, a status update, a worked example. v2.3.1 is such a revision: §§1–18 are identical to v2.3, and only §9.3 and §15 have grown. Citations to "Translit §X" are unaffected by version.\n\n',
    ''
)
replace_section(
    translit,
    '### 4.1 Class A — carrier-borne vowels\n',
    '\n### 4.2 Class B — consonant-borne vowels',
    '''### 4.1 Class A — carrier-borne vowels

These are single page-states in which the vowel sign is borne by the mater letter itself. The carrier is therefore part of the written vowel: it is neither inferred nor omitted.

| Sign | Identification | Translit. |
|---|---|---|
| yodh + ī-sign | ḥḇāṣā | `ī` |
| waw + one dot above | rwāḥā | `ō` |
| waw + one dot below | rḇāṣā / ʾeṣāṣā | `ū` |

**There is no defective Class-A notation.** The former `ĭ`, `ŏ`, and `ŭ` forms are withdrawn because no secure source-of-record page-state has established a carrierless counterpart to these three written vowels. A sign that appears to represent `ī`, `ō`, or `ū` without the expected yodh or waw is **flagged at ingestion, not transliterated by inference**. Establish the page-state from the witness before adding or normalizing any such form (§16).

*Note on names.* Grammars differ: *rḇāṣā* names the /u/ vowel in one convention and the e-vowels in another, where Unicode uses *ʾeṣāṣā*. This file uses *rḇāṣā / ʾeṣāṣā* for /ū/. Nothing turns on the choice.
'''
)
replace_exact(
    translit,
    '| Class A breve | forms with defective spelling respelled |',
    '| Class A carrier discipline | `ī`/`ō`/`ū` require their written yodh/waw carrier; an apparent carrierless state is flagged rather than encoded by inference |'
)
replace_exact(
    translit,
    'breve *above* for the defective vowels `ă ĕ ĭ ŏ ŭ`',
    'breve *above* for the word-final Class-B exceptions `ă ĕ`'
)

# 2. Bgdkpt identity: §10.17 owns the merge/split decision; Check 6 checks the result literally.
old17 = '''17. **Rūkkākā and qūššāyā do not by themselves make a second entry.** Two spellings of one form differing only in the bgdkpt point are **one entry**, each spelling recorded on its own occurrence. Spirantization is realization in environment, not a property of the lexeme.

    **The headword is written unmarked at the merge point.** Where one merged spelling is itself unmarked, that spelling heads the entry. Where none is — the proclitic-softened initials of §10.2 are the standing case — the headword is written without the point as an **index form**, which is not a claim that any page shows a bare letter.

    **Points elsewhere in the word are left as attested.** A headword is the spelling of the form, not a stripped skeleton.

    **Exception: where the point carries a distinction.** Where the bgdkpt point is the only signal of a different morphological analysis, the two are different forms and take separate entries under §10.1. Merging is the default; splitting is a claim, recorded in the entry per §10.15.'''
new17 = '''17. **Rūkkākā and qūššāyā do not by themselves make a second entry.** Two spellings of one form differing only in an environmentally varying bgdkpt point are **one entry**, each spelling recorded on its own occurrence. Spirantization is realization in environment, not a property of the lexeme.

    **The headword is written unmarked at every point deliberately merged under this rule.** Where one merged spelling is itself unmarked, that spelling heads the entry. Where none is — the proclitic-softened initials of §10.2 are the standing case — the headword is written without the point as an **index form**, which is not a claim that any page shows a bare letter.

    **All other points remain as attested.** A headword is the spelling of the indexed form, not a stripped skeleton.

    **Where a bgdkpt point carries a form distinction, preserve it.** If the point is the only written signal of a different morphological analysis, the spellings are different forms and take separate entries with distinct `{...}` analyses under §10.1. Merging is the default; splitting is a morphological claim. Once that claim is made in the headwords, the checker does not strip the point again.'''
replace_exact(general, old17, new17)
replace_exact(
    general,
    '6. No two entries share a canonical string **and** a root (Translit §12), comparing strings with bgdkpt points disregarded (§10.17)',
    '6. No two entries share the same canonical headword string **and** root (Translit §12). Compare the headwords exactly as stored; §10.17 has already removed only the bgdkpt distinctions that the Glossary has deliberately merged'
)

# 3. The canonical headword is already the exact reversible key; retain only a convenience fold key in addition.
replace_exact(
    general,
    '14. **Search keys.** Each headword carries a fold key, written `(search: alaha)` — lowercase, diacritics stripped, `ʾ` and `ʿ` dropped, `š` folded to `sh`, and notation characters (`^` `_` `(` `)`) dropped (Translit §11.2). Collisions are acceptable.',
    '14. **Headword identity and search.** The canonical headword string itself is the exact reversible key for the indexed form, including any deliberate §10.17 merge normalization; no second exact key is stored. Each headword carries one additional fold key, written `(search: alaha)` — lowercase, diacritics stripped, `ʾ` and `ʿ` dropped, `š` folded to `sh`, and notation characters (`^` `_` `(` `)` `[` `]`) dropped (Translit §11.2). Fold-key collisions are acceptable.'
)
replace_section(
    translit,
    '## 11. Search Keys\n',
    '\n---\n\n## 12. Round-Trip Validation',
    '''## 11. Headword Identity and Search

### 11.1 Exact identity

The **canonical headword string itself** is the exact reversible key for the indexed form. No second exact or ASCII surrogate key is stored. Where General Rules §10.17 deliberately merges environmentally varying bgdkpt pointing, the resulting unmarked headword is the exact identity of that **index form**; occurrence spellings remain fully pointed and reversible in their citations.

### 11.2 Fold key

Each glossary headword carries **one additional, non-authoritative fold key**. It is lowercase; all diacritics are stripped; `ʾ` and `ʿ` are dropped; notation characters are dropped. It is written in the entry as `(search: alaha)`.

The fold key is deliberately ambiguous. Collisions are expected and acceptable — `brā` "Son" and `brā` "he created" both fold to `bra`, and the root field separates their entries. This key exists only so that a human can find a form by typing an approximate Latin spelling. It is never used for identity, decisions, citation, or display.
'''
)

# 4. Git is the version history: remove embedded version labels and stale version prose.
replace_exact(
    translit,
    '*The v2.2 note on dalath width is withdrawn in v2.3.*',
    '*An earlier note on dalath width is withdrawn.*'
)
replace_exact(
    translit,
    '### 3.3 The Undotted Stroke — *withdrawn in v2.3*',
    '### 3.3 The Undotted Stroke — *withdrawn*'
)
replace_exact(
    translit,
    'v2.2.4 defined `ř` for a stroke carrying neither the resh point above nor the dalath point below, treating it as a genuine third page-state.',
    'An earlier rule defined `ř` for a stroke carrying neither the resh point above nor the dalath point below, treating it as a genuine third page-state.'
)
replace_exact(
    translit,
    'The caron notation is retired from §11 and §15 accordingly.',
    'The caron notation is retired entirely.'
)
replace_exact(
    translit,
    '*This supersedes v2.2.4, which routed gemination to the parse field.*\n\n',
    ''
)
replace_exact(
    translit,
    'v2.2.4 carried four open questions. All are closed in v2.3. This section is retained as the record; nothing here is open.',
    'Four formerly open questions are retained here as withdrawal notes; nothing in this section is open.'
)

# 5. Mark-order specification: total same-class order for every in-scope combining mark.
replace_section(
    translit,
    '### 5.1 Mark order — the general rule\n',
    '\n### 5.2 Syāmē against a vowel on the same letter',
    '''### 5.1 Mark order — the general rule

Where a Syriac letter carries more than one combining mark, storage order is deterministic:

1. **Different canonical combining classes sort in ascending class order.** NFC performs this reordering.
2. **Marks within the same class follow the project order below.** NFC does **not** reorder equal-class marks, so ingestion must do it explicitly.
3. Store the result in **NFC**.

The in-scope combining classes are:

- **36** — superscript ʾālap̄ (U+0711). It therefore sorts before the below and above marks without a project tie-break.
- **220 (below)** — use `[vowel, bgdkpt point, single point (§7), two dots below (§17), breve below (§18), occultans line below (§6)]`.
- **230 (above)** — use `[vowel, bgdkpt point, single point (§7), syāmē, occultans line above (§6)]`.

The order is a **storage convention, not a claim about phonological or visual priority**. It exists because several distinct in-scope marks share class 220 or 230. After §16 has normalized source codepoints to page-states, two canonically equivalent witnesses must therefore produce the same combining sequence before comparison or round-trip validation.
'''
)
replace_exact(
    translit,
    '### 16.3 Combining-mark order\n\nNormalize to the §5.1 order before comparison or round-trip validation (§12). In practice this means checking pairs of **class 230** marks only; a 220 mark against a 230 mark is ordered by NFC without intervention.',
    '### 16.3 Combining-mark order\n\nNormalize every combining sequence to §5.1 before comparison or round-trip validation (§12). NFC orders marks of **different** canonical combining classes, but it does not repair the order of two marks that share a class. Ingestion must therefore enforce the §5.1 project order for both class **220** and class **230** sequences after page-state normalization.'
)
replace_exact(
    general,
    '13. Mark order within combining class 230 is `[vowel, bgdkpt point, syāmē]` (Translit §5.1). NFC will not do this for you, and two marks above a letter render identically in the wrong order',
    '13. Same-class combining-mark order follows Translit §5.1 for every in-scope sequence. Check both class 220 and class 230 explicitly; NFC orders unlike classes but does not reorder two marks that share a class'
)

# Remove the obsolete historical correction note that the new §5.1 supersedes completely.
replace_exact(
    translit,
    '*This corrects v2.2.4, which asserted that a vowel point and syāmē were "both combining class 230" and concluded that every such pair required manual ordering. That is true only of the above-vowels. Of 21 double-marked letters in the Glossary at the time of the correction, 19 self-normalized and 2 did not.*\n\n',
    ''
)

# No embedded version labels should remain after the rename.
t = translit.read_text(encoding='utf-8')
leftovers = sorted(set(re.findall(r'\bv\d+(?:\.\d+)+\b', t)))
if leftovers:
    raise SystemExit(f'embedded version labels remain: {leftovers}')
if any(x in t for x in ('ĭ', 'ŏ', 'ŭ')):
    raise SystemExit('withdrawn defective Class-A notation remains')

# Basic hygiene for edited rule files.
for path in (translit, general):
    s = path.read_text(encoding='utf-8')
    if unicodedata.normalize('NFC', s) != s:
        raise SystemExit(f'{path}: not NFC')
    if '\r' in s:
        raise SystemExit(f'{path}: CR line ending found')
    if any(line.rstrip() != line for line in s.splitlines()):
        raise SystemExit(f'{path}: trailing whitespace found')

# New Check 13 against current confirmed Syriac blocks.
ranks_220 = {
    0x0738: 0, 0x0739: 0, 0x073C: 0,
    0x0742: 1,
    0x0323: 2,
    0x0324: 3, 0x0740: 3, 0x0744: 3,
    0x032E: 4,
    0x0748: 5,
}
ranks_230 = {
    0x0732: 0, 0x0735: 0, 0x073F: 0,
    0x0741: 1,
    0x0307: 2,
    0x0308: 3,
    0x0747: 4,
}


def check_cluster(path, line_no, cluster):
    for ccc, ranks in ((220, ranks_220), (230, ranks_230)):
        seq = [ranks.get(ord(ch)) for ch in cluster if unicodedata.combining(ch) == ccc]
        known = [x for x in seq if x is not None]
        if known != sorted(known):
            cps = ' '.join(f'U+{ord(ch):04X}' for ch in cluster)
            raise SystemExit(f'{path}:{line_no}: same-class mark order violation: {cps}')


for p in Path('confirmed-texts').glob('*.txt'):
    for n, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        chars = list(line)
        i = 0
        while i < len(chars):
            cp = ord(chars[i])
            if 0x0710 <= cp <= 0x072F:
                j = i + 1
                cluster = []
                while j < len(chars) and unicodedata.combining(chars[j]):
                    cluster.append(chars[j])
                    j += 1
                check_cluster(str(p), n, cluster)
                i = j
            else:
                i += 1

# No corpus data may depend on the withdrawn notation.
for root in (Path('confirmed-texts'), Path('glossary')):
    for p in root.rglob('*'):
        if p.is_file():
            s = p.read_text(encoding='utf-8')
            if any(x in s for x in ('ĭ', 'ŏ', 'ŭ')):
                raise SystemExit(f'{p}: withdrawn defective Class-A notation occurs in corpus data')

# Rename completeness and stale-path scan.
if not translit.exists() or old_translit.exists():
    raise SystemExit('transliteration-rules rename incomplete')
for p in Path('.').rglob('*'):
    if '.git' in p.parts or not p.is_file():
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    if 'Transliteration-Rules-v2_3_1' in s:
        raise SystemExit(f'{p}: old transliteration-rules filename still referenced')
