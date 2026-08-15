from pathlib import Path
import re
import unicodedata

P = Path('glossary/Glossary.md')
s = P.read_text(encoding='utf-8')

# Preserve the deferred work exactly: this pass may correct populated morphology,
# but must not fill any currently missing morphology field.
def missing_heads(text):
    out = []
    in_forms = False
    for line in text.splitlines():
        if line == '## Forms':
            in_forms = True
            continue
        if not in_forms:
            continue
        if line.startswith('## ') and line != '## Forms':
            break
        if re.match(r'^\S.*?\s{3}\[[^\]]+\]\s{3}\(search:', line):
            out.append(line)
    return tuple(out)

missing_before = missing_heads(s)
assert len(missing_before) == 67, len(missing_before)

replacements = {
'ܡܗܲܝܡܢܝܼܢܲܢ   [h-y-m-n]   {Pael active ptcp. m.pl. + 1cp encl.}   (search: mhaymninan)':
'ܡܗܲܝܡܢܝܼܢܲܢ   [h-y-m-n]   {Pael active ptcp. m.pl.abs. + 1cp encl.}   (search: mhaymninan)',
'ܐܲܚܝܼܕ   [ʾ-ḥ-d]   {Peal passive ptcp. m.sg.abs.}   (search: ahid)':
'ܐܲܚܝܼܕ   [ʾ-ḥ-d]   {Peal passive ptcp. m.sg.cst.}   (search: ahid)',
'ܡܫܝܼܚܵܐ   [m-š-ḥ]   {noun m.sg.emph.}   (search: mshiha)':
'ܡܫܝܼܚܵܐ   [m-š-ḥ]   {Peal passive ptcp. m.sg.emph.}   (search: mshiha)',
'ܒܪܹܗ   [b-r]   {noun m.sg. + 3ms suff.}   (search: breh)':
'ܒܪܹܗ   [b-r]   {noun m.sg.emph. + 3ms suff.}   (search: breh)',
'ܐܲܒ݂ܘܼܗܝ   [ʾ-b]   {noun m.sg. + 3ms suff.}   (search: abuhy)':
'ܐܲܒ݂ܘܼܗܝ   [ʾ-b]   {noun m.sg.emph. + 3ms suff.}   (search: abuhy)',
'ܐܝܼ̈ܕܵܘܗܝ   [y-d]   {noun f.pl. + 3ms suff.}   (search: idawhy)':
'ܐܝܼ̈ܕܵܘܗܝ   [y-d]   {noun f.pl.emph. + 3ms suff.}   (search: idawhy)',
'ܦܘܼܪܩܵܢܲܢ   [p-r-q]   {noun m.sg. + 1cp suff.}   (search: purqanan)':
'ܦܘܼܪܩܵܢܲܢ   [p-r-q]   {noun m.sg.emph. + 1cp suff.}   (search: purqanan)',
'ܫܡܲܝܵܐ   [š-m-y]   {noun c.sg.emph.}   (search: shmaya)':
'ܫܡܲܝܵܐ   [š-m-y]   {noun c.pl.emph.}   (search: shmaya)',
'ܐܲܒ݂ܘܗܝ   [ʾ-b]   {noun m.sg. + 3ms suff.}   (search: abwhy)':
'ܐܲܒ݂ܘܗܝ   [ʾ-b]   {noun m.sg.emph. + 3ms suff.}   (search: abwhy)',
'ܡܵܘܕܹ݁ܝܢܲܢ   [y-d-ʾ]   {Aphel active ptcp. m.pl. + 1cp encl.}   (search: mawdeynan)':
'ܡܵܘܕܹ݁ܝܢܲܢ   [y-d-ʾ]   {Aphel active ptcp. m.pl.abs. + 1cp encl.}   (search: mawdeynan)',
'ܐܲܒ݂ܘܼܢ   [ʾ-b]   {noun m.sg. + 1cp suff.}   (search: abun)':
'ܐܲܒ݂ܘܼܢ   [ʾ-b]   {noun m.sg.emph. + 1cp suff.}   (search: abun)',
'ܫܡܵܟ݂   [š-m]   {noun m.sg. + 2ms suff.}   (search: shmak)':
'ܫܡܵܟ݂   [š-m]   {noun m.sg.emph. + 2ms suff.}   (search: shmak)',
'ܡܲܠܟ݁ܘܼܬ݂ܵܟ݂   [m-l-k]   {noun f.sg. + 2ms suff.}   (search: malkutak)':
'ܡܲܠܟ݁ܘܼܬ݂ܵܟ݂   [m-l-k]   {noun f.sg.emph. + 2ms suff.}   (search: malkutak)',
'ܫܘܼܒ݂ܚܵܟ݂   [š-b-ḥ]   {noun m.sg. + 2ms suff.}   (search: shubhak)':
'ܫܘܼܒ݂ܚܵܟ݂   [š-b-ḥ]   {noun m.sg.emph. + 2ms suff.}   (search: shubhak)',
'ܨܸܒ݂ܝܵܢܵܟ݂   [ṣ-b-ʾ]   {noun m.sg. + 2ms suff.}   (search: sebyanak)':
'ܨܸܒ݂ܝܵܢܵܟ݂   [ṣ-b-ʾ]   {noun m.sg.emph. + 2ms suff.}   (search: sebyanak)',
'ܣܘܼܢܩܵܢܲܢ   [s-n-q]   {noun m.sg. + 1cp suff.}   (search: sunqanan)':
'ܣܘܼܢܩܵܢܲܢ   [s-n-q]   {noun m.sg.emph. + 1cp suff.}   (search: sunqanan)',
'ܚܵܘܒܲܝ̈ܢ   [ḥ-w-b]   {noun m.pl. + 1cp suff.}   (search: hawbayn)':
'ܚܵܘܒܲܝ̈ܢ   [ḥ-w-b]   {noun m.pl.emph. + 1cp suff.}   (search: hawbayn)',
'ܚܛܵܗܲܝ̈ܢ   [ḥ-ṭ-ʾ]   {noun m.pl. + 1cp suff.}   (search: htahayn)':
'ܚܛܵܗܲܝ̈ܢ   [ḥ-ṭ-ʾ]   {noun m.pl.emph. + 1cp suff.}   (search: htahayn)',
'ܚܲܝܵܒܲܝ̈ܢ   [ḥ-w-b]   {adj. m.pl. + 1cp suff.}   (search: hayabayn)':
'ܚܲܝܵܒܲܝ̈ܢ   [ḥ-w-b]   {adj. m.pl.emph. + 1cp suff.}   (search: hayabayn)',
'ܬܲܪܥܹܗ   [t-r-ʿ]   {noun m.sg. + 3ms suff.}   (search: tareh)':
'ܬܲܪܥܹܗ   [t-r-ʿ]   {noun m.sg.emph. + 3ms suff.}   (search: tareh)',
'ܨܹܐܕ݂ܵܘܗܝ   [ṣ-y-d]   {prep.}   (search: sedawhy)':
'ܨܹܐܕ݂ܵܘܗܝ   [ṣ-y-d]   {prep. + 3ms suff.}   (search: sedawhy)',
'ܦܬܲܚܠܵܗ̇   [p-t-ḥ]   {verb + prep. suff.}   (search: ptahlah)':
'ܦܬܲܚܠܵܗ̇   [p-t-ḥ]   {Peal impv. 2m.sg. + prep. l + 3fs suff.}   (search: ptahlah)',
'ܠܹܗ   [l]   {prep.}   (search: leh)':
'ܠܹܗ   [l]   {prep. + 3ms suff.}   (search: leh)',
'ܐܲܝܠܸܝܢ   [ʾ-y-n-ʾ]   {rel. pron.}   (search: ayleyn)':
'ܐܲܝܠܸܝܢ   [ʾ-y-n-ʾ]   {rel. pron. c.pl.}   (search: ayleyn)',
'ܐܲܢ݇ܬ݁ܘܼ   [ʾ-n-t]   {pron.}   (search: antu)':
'ܐܲܢ݇ܬ݁ܘܼ   [ʾ-n-t]   {pron. 2m.sg. + 3ms encl.}   (search: antu)',
}

for old, new in replacements.items():
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'expected exactly one match, found {n}: {old}')
    s = s.replace(old, new)

old_haye = '''ܚܲܝܹ̈ܐ   [ḥ-y-ʾ]   {adj. m.pl.emph.}   (search: haye)
ḥaÿē (2) — living (1), life (1)
* walḥaÿē · "...to judge the dead and the living" (Creed Line 15)
* waḇḥaÿē · "...and life unto the Age of ages. Amen" (Creed Line 21)'''
new_haye = '''ܚܲܝܹ̈ܐ   [ḥ-y-ʾ]   {adj. m.pl.emph.}   (search: haye)
ḥaÿē (1) — living (1)
* walḥaÿē · "...to judge the dead and the living" (Creed Line 15)

ܚܲܝܹ̈ܐ   [ḥ-y-ʾ]   {noun m.pl.emph.}   (search: haye)
ḥaÿē (1) — life (1)
* waḇḥaÿē · "...and life unto the Age of ages. Amen" (Creed Line 21)'''
if s.count(old_haye) != 1:
    raise SystemExit('ḥaÿē block did not match exactly')
s = s.replace(old_haye, new_haye)

old_alam = '''ܥܵܠܲܡ   [ʿ-l-m]   {noun m.sg.abs./cst.}   (search: alam)
ʿālam (4) — → ʿālam ʿālmīn (2), Eternity (2)
* dalʿālam · "...and life unto the Age of ages. Amen" (Creed Line 21) → ʿālam ʿālmīn
* lʿālam · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Abun Line 14) → ʿālam ʿālmīn
* ʿālam · "From Eternity and unto Eternity, amen amen" (Abun Line 16)
* lʿālam · "From Eternity and unto Eternity, amen amen" (Abun Line 16)'''
new_alam = '''ܥܵܠܲܡ   [ʿ-l-m]   {noun m.sg.cst.}   (search: alam)
ʿālam (2) — → ʿālam ʿālmīn (2)
* dalʿālam · "...and life unto the Age of ages. Amen" (Creed Line 21) → ʿālam ʿālmīn
* lʿālam · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Abun Line 14) → ʿālam ʿālmīn

ܥܵܠܲܡ   [ʿ-l-m]   {noun m.sg.abs.}   (search: alam)
ʿālam (2) — Eternity (2)
* ʿālam · "From Eternity and unto Eternity, amen amen" (Abun Line 16)
* lʿālam · "From Eternity and unto Eternity, amen amen" (Abun Line 16)'''
if s.count(old_alam) != 1:
    raise SystemExit('ʿālam block did not match exactly')
s = s.replace(old_alam, new_alam)

# The 67 missing morphology entries remain exactly the same deferred entries.
missing_after = missing_heads(s)
if missing_after != missing_before:
    raise SystemExit('deferred missing-morphology set changed')

# Parse populated form identities and require uniqueness on headword+root+morphology.
identities = []
forms = 0
in_forms = False
for line in s.splitlines():
    if line == '## Forms':
        in_forms = True
        continue
    if not in_forms:
        continue
    if line.startswith('## ') and line != '## Forms':
        break
    m = re.match(r'^(\S.*?)\s{3}\[([^\]]+)\](?:\s{3}\{([^}]*)\})?\s{3}\(search:', line)
    if m:
        forms += 1
        head, root, morph = m.groups()
        if morph is not None:
            identities.append((head, root, morph))

if forms != 214:
    raise SystemExit(f'expected 214 form entries after two morphological splits, found {forms}')
if len(identities) != 147:
    raise SystemExit(f'expected 147 populated morphology entries, found {len(identities)}')
if len(set(identities)) != len(identities):
    raise SystemExit('duplicate full morphology identity created')

# The two deliberate same-orthography/same-root morphology splits must exist.
for expected in [
    ('ܚܲܝܹ̈ܐ', 'ḥ-y-ʾ', {'adj. m.pl.emph.', 'noun m.pl.emph.'}),
    ('ܥܵܠܲܡ', 'ʿ-l-m', {'noun m.sg.cst.', 'noun m.sg.abs.'}),
]:
    h, r, ms = expected
    found = {m for hh, rr, m in identities if hh == h and rr == r}
    if found != ms:
        raise SystemExit(f'expected morphology split not present for {h}: {found}')

# No already-populated noun/adjective with a suffix should remain state-less.
for head, root, morph in identities:
    if ('noun ' in morph or 'adj. ' in morph) and 'suff.' in morph:
        if not any(x in morph for x in ('.abs.', '.cst.', '.emph.')):
            raise SystemExit(f'state-less suffixed nominal remains: {head} {{{morph}}}')

# Hygiene.
if unicodedata.normalize('NFC', s) != s:
    raise SystemExit('Glossary would not be NFC')
if '\r' in s:
    raise SystemExit('CR found')
if any(line.rstrip() != line for line in s.splitlines()):
    raise SystemExit('trailing whitespace found')

P.write_text(s, encoding='utf-8', newline='\n')
print('reviewed populated morphology corrections prepared')
print('form_entries', forms)
print('populated_morphology', len(identities))
print('missing_morphology_deferred', len(missing_after))
