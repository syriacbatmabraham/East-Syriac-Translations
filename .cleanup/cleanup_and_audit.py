from pathlib import Path
import re, unicodedata
from collections import defaultdict

ROOT=Path('.')
GENERAL=ROOT/'rules/General-Rules.md'; TRANSLIT=ROOT/'rules/Transliteration-Rules.md'
GLOSSARY=ROOT/'glossary/Glossary.md'; README=ROOT/'README.md'
SOURCES_README=ROOT/'sources/README.md'; SOURCES_YAML=ROOT/'sources/sources.yaml'

def read(p): return p.read_text(encoding='utf-8')
def write(p,s): p.write_text(s,encoding='utf-8',newline='\n')
def sub1(s,pat,repl,label,flags=0):
    out,n=re.subn(pat,repl,s,count=1,flags=flags)
    if n!=1: raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    return out
def section(s,start,end,body,label):
    pat=rf'(?ms)^{re.escape(start)}\n.*?(?=^{re.escape(end)}\n)'
    return sub1(s,pat,body.rstrip()+'\n\n',label,re.M|re.S)

# General Rules
g=read(GENERAL)
g=g.replace('Settled here, not repeated in the Glossary. A text falling outside all four has its source of record designated explicitly **before entries are built**, and recorded with the confirmed text.','Settled here, not repeated in the Glossary. A text falling outside all four has its source of record designated explicitly **before entries are built** and recorded in `sources/sources.yaml`.')
g=g.replace('**Citing a section always names its file** — "Translit §10", "General Rules §10". Both carry a §10 and a §7. Withdrawn sections are retained as withdrawal notes, never renumbered.','**Citing a section always names its file** — "Translit §10", "General Rules §10". Both carry a §10 and a §7. Section numbers are stable; reserved sections are not renumbered.')
g=g.replace('The text files carry no header of their own, which would break the three-block parse. Provenance is not recorded in the corpus; the source of record is designated per §1.1 and checked against the page.','The text files carry no header of their own, which would break the three-block parse. Provenance is stored separately in `sources/sources.yaml`; the source of record is designated per §1.1 and checked against the page.')
g=sub1(g,r'(?m)^1\. Each form of every word makes one entry\..*?Verb stems are named, not explained; the Glossary preamble tables what each does\.$','1. Each form of every word makes one entry. **Entry identity is canonical headword + root + `{...}` morphology.** The root is a field for comparing words of one root; morphology is part of identity because two genuinely distinct forms may be orthographically identical and share a root. **Part of speech is a separate field**, written `{...}` — never standing in the root field. It records the class of the **form** and its morphology: for a noun or adjective, gender, number and state; for a finite verb, stem, tense, person, gender and number; for a participle, stem, voice where the stem distinguishes it, gender, number and state. Pronominal suffixes and enclitics are named after `+`. An invariable word carries its class alone. **The field records what the form is, not what it does** — `yāwmānā` is a noun working adverbially, `mīẗē` and `ḥayābaÿn` adjectives standing as nouns; function belongs to the rendering. **`referent`** prefixes any class where the form names one specific referent rather than a general one. Verb stems are named, not explained; the Glossary preamble tables what each does.','General §10.1',re.M)
g=g.replace('4. Variance is recorded, not suppressed. Each rendering carries its own count. Keep repeated terms stable (§3), but do not flatten a genuine split.','4. Variance is recorded, not suppressed. Each rendering carries its own **decision count**. Glossary counts measure indexed translation decisions under these rules, not raw corpus-token frequency. Keep repeated terms stable (§3), but do not flatten a genuine split.')
g=g.replace('8. **The parse field records exclusions and nothing else, and currently records nothing** — ingestion removes every out-of-scope character, so line and canonical string agree. Gemination and hardness are pronunciation and are recorded nowhere; homographs are separated by the root field. The principle that a secure reading needs no field is scoped to this field alone — it does not bear on `{...}` (§10.1), which exists to record what English cannot carry.','8. **The parse field records exclusions and nothing else.** Ingestion removes out-of-scope characters before transliteration. If an in-scope mark survives ingestion but cannot be represented by the canonical system, record that exclusion and flag it rather than inventing notation. Gemination and unmarked hardness or softness are pronunciation and are recorded nowhere; homographs are separated by the identity fields of §10.1. The principle that a secure reading needs no parse-field note is scoped to this field alone — it does not bear on `{...}` (§10.1), which exists to record what English cannot carry.')
g=g.replace('11. **Occurrence cap.** For a high-frequency form with a settled rendering, cite roughly 10 occurrences for an obvious word or 15–20 for a less common one, then accrue the rest as `+n`, written `rendering (base+extra)`. Base is the number of cited bullets; the headword total counts every occurrence. Never applies to a new or minority rendering, or to any occurrence bearing a decision.','11. **Decision-count cap.** For a high-frequency form with a settled rendering, cite roughly 10 indexed decisions for an obvious word or 15–20 for a less common one, then accrue additional indexed decisions as `+n`, written `rendering (base+extra)`. Base is the number of cited bullets; the headword total is the sum of indexed decisions, **not raw token occurrences**. Repetitions, same-locus witness duplicates, and common liturgical units excluded by §§10.13 and 10.18 do not increment it. The cap never applies to a new or minority rendering, or to an occurrence that itself bears a new decision.')
g=g.replace('14. **Headword identity and search.** The canonical headword string itself is the exact reversible key for the indexed form, including any deliberate §10.17 merge normalization; no second exact key is stored. Each headword carries one additional fold key, written `(search: alaha)` — lowercase, diacritics stripped, `ʾ` and `ʿ` dropped, `š` folded to `sh`, and notation characters (`^` `_` `(` `)` `[` `]`) dropped (Translit §11.2). Fold-key collisions are acceptable.','14. **Headword identity and search.** The canonical headword string itself is the exact reversible **orthographic** key for the indexed form, including any deliberate §10.17 merge normalization; no second exact orthographic key is stored. Full Glossary entry identity is **canonical headword + root + `{...}` morphology** (§10.1). Each headword carries one additional fold key, written `(search: alaha)` — lowercase, diacritics stripped, `ʾ` and `ʿ` dropped, `š` folded to `sh`, and notation characters (`^` `_` `(` `)` `[` `]`) dropped (Translit §11.2). Fold-key collisions are acceptable.')
g=g.replace('Run after every glossary write, and after any edit to a confirmed text. Each has caught a real error. **Diagnose a flag before calling it a defect** — a new check is new code, and these have produced more false positives than the files have produced faults.','Run after every glossary write, and after any edit to a confirmed text. **Diagnose a flag before calling it a defect.** A check reports a condition for review; it does not by itself establish that the data are wrong.')
g=g.replace('3. Per-entry bullets == Σbase, and total == Σ(base+extra)','3. Per-entry bullets == Σbase, and decision total == Σ(base+extra)')
g=g.replace('6. No two entries share the same canonical headword string **and** root (Translit §12). Compare the headwords exactly as stored; §10.17 has already removed only the bgdkpt distinctions that the Glossary has deliberately merged','6. No two entries share the same canonical headword string, root, **and `{...}` morphology** (Translit §12). Compare the headwords exactly as stored; §10.17 has already removed only the bgdkpt distinctions that the Glossary has deliberately merged')
g=g.replace('Dukhrana, CAL, and Payne Smith are blocked or image-only from a sandboxed environment, and reachable from a local build with unrestricted browsing. Check availability rather than assuming either way.\n\n','')
write(GENERAL,g)

# Transliteration Rules
t=read(TRANSLIT)
t=t.replace('**Section numbering is stable.** Withdrawn sections are retained as withdrawal notes rather than renumbered, because stale cross-references have already cost this project real errors.','**Section numbering is stable.** A retired section number remains reserved rather than shifting later cross-references.')
t=t.replace('**The glossary key is form + root, not form alone.**','**Glossary entry identity is canonical headword + root + morphology, not form alone.**')
t=t.replace('- **Homographs** (§1) are separated by the **root** field.','- **Homographs** (§1) are separated by the **root** field; if canonical headword and root are both identical, `{...}` morphology completes the Glossary identity (General Rules §10.1).')
t=t.replace('Since ingestion removes every out-of-scope character (§10, §16.1), this field currently has **no instances**. See General Rules §10.8.','See General Rules §10.8 for the exclusion rule.')
t=t.replace(' Recorded graphically; no function is claimed. *Untested — not encountered in worked text.*',' Recorded graphically; no function is claimed.')
t=t.replace('*Note:* `k̇` has no precomposed Unicode form and requires U+0307 combining dot above. Flagged as a minor tooling cost.','*Note:* `k̇` has no precomposed Unicode form and requires U+0307 combining dot above.')
t=sub1(t,r'(?ms)^\*An earlier note on dalath width is withdrawn\.\*.*?\n\n(?=### 3\.3)','**Do not infer bgdkpt state from glyph width.** Read the normalized point/page-state under §16; if the source does not encode or securely show a point, record the letter as unmarked.\n\n','Translit dalath history')
t=section(t,'### 3.3 The Undotted Stroke — *withdrawn*','---','''### 3.3 Reserved — no third resh/dalath state

No separate canonical consonant state is defined for an undotted resh/dalath-like stroke. U+0716 is handled only by the ingestion rule in §16.2.''','Translit §3.3')
t=t.replace('**There is no defective Class-A notation.** The former `ĭ`, `ŏ`, and `ŭ` forms are withdrawn because no secure source-of-record page-state has established a carrierless counterpart to these three written vowels. A sign that appears to represent `ī`, `ō`, or `ū` without the expected yodh or waw is **flagged at ingestion, not transliterated by inference**. Establish the page-state from the witness before adding or normalizing any such form (§16).','**There is no carrierless Class-A notation.** `ĭ`, `ŏ`, and `ŭ` are not valid canonical symbols. A sign that appears to represent `ī`, `ō`, or `ū` without the expected yodh or waw is **flagged at ingestion, not transliterated by inference**. Establish the page-state from the witness before adding or normalizing any such form (§16).')
t=t.replace("; §17's mark is the two-dot mark that is neither, and in practice sits on taw, hē, waw, and ʾālap̄ in the environments listed there.","; §17's mark is the two-dot mark that is neither.")
t=re.sub(r'(?m)^\*Status: line above attested.*?confirmed text\.\*\n\n','',t)
t=re.sub(r'(?m)^\*Status: `\^` and `_` attested;.*?\*\n\n','',t)
t=section(t,'### 9.3 Audit log — withdrawn','---','''### 9.3 Reserved

Reserved.''','Translit §9.3')
t=t.replace('- **Accent and cantillation points.** None has been encountered in this project\'s sources.','- **Accent and cantillation points.**')
t=sub1(t,r'(?ms)^\*\*Consequence for the parse field\.\*\*.*?\n\n(?=A word\'s canonical string)','**Consequence for the parse field.** If an in-scope mark survives ingestion but the canonical notation cannot represent it, record the exclusion under General Rules §10.8 and flag the word. Otherwise the stored line and canonical string must agree at every in-scope point.\n\n','Translit parse status')
t=sub1(t,r'(?ms)^### Legibility\n.*?\n\n(?=---)','### Legibility\nMarks that cannot be read are not reconstructed or invented. An unreadable in-scope mark is flagged for source review; no provisional canonical symbol is created merely to fill the gap.\n\n','Translit legibility')
t=t.replace('The **canonical headword string itself** is the exact reversible key for the indexed form. No second exact or ASCII surrogate key is stored. Where General Rules §10.17 deliberately merges environmentally varying bgdkpt pointing, the resulting unmarked headword is the exact identity of that **index form**; occurrence spellings remain fully pointed and reversible in their citations.','The **canonical headword string itself** is the exact reversible **orthographic** key for the indexed form. No second exact or ASCII surrogate key is stored. Where General Rules §10.17 deliberately merges environmentally varying bgdkpt pointing, the resulting unmarked headword is the orthographic identity of that **index form**; occurrence spellings remain fully pointed and reversible in their citations. Full Glossary entry identity is canonical headword + root + `{...}` morphology (General Rules §10.1).')
t=t.replace('2. No two distinct entries in the glossary share a canonical string *and* a root.','2. No two distinct entries in the glossary share a canonical headword string, root, *and* `{...}` morphology.')
t=t.replace('Condition 2 is the injectivity check. Violations are one of:\n- a transliteration error, or\n- a genuine homograph, which must be separated by the root field.','Condition 2 is the Glossary-identity check. A collision means either an entry has been duplicated or the morphology/root analysis has not yet separated two genuinely distinct forms.')
t=t.replace('**One known asymmetry.**','**Round-trip asymmetry.**')
t=t.replace('\nThis test is mechanical and should be automated in the eventual SQLite pipeline.\n','\n')
t=section(t,'## 13. Difference from the Old Clean-Glossary','---','''## 13. Reserved

Reserved.''','Translit §13')
t=section(t,'## 14. Resolved and Withdrawn','---','''## 14. Reserved

Reserved.''','Translit §14')
t=t.replace('Validation requirements are §12 and General Rules §11. Corpus size, worked-text counts, and current test status belong to test output and Git history, not this specification.','Validation requirements are §12 and General Rules §11. Corpus reports and test output do not belong in this specification.')
t=sub1(t,r'(?ms)^Digital witnesses do not agree on which codepoint encodes a given mark\..*?Reading codepoints at face value across witnesses produces silent corruption, not an error\.\n\n(?=### 16\.1)','Digital witnesses may use different codepoints for the same visible page-state, and the same codepoint may serve different page-states in different carrier environments. Canonical transliteration therefore normalizes **page-state first**, then applies §§3–7. Reading source codepoints as universal semantic labels is prohibited.\n\n','Translit §16 intro')
t=sub1(t,r'(?ms)^\*\*Bare U\+0716 normalizes to resh and raises a flag\.\*\*.*?\n\n(?=### 16\.3)','**Bare U+0716 normalizes to resh and raises a flag.** Treat the normalization as a source-level anomaly, not as evidence for a new consonant. If the lexical context permits dalath or otherwise leaves the reading uncertain, require manual source review before confirmation.\n\n','Translit §16.2 status')
t=sub1(t,r'(?ms)^### 16\.4 Per-block ingestion\n\n\*\*The audit runs per block, not per file\.\*\*.*?Audit each block whose provenance may differ, and record where the seams fall\.\n','### 16.4 Per-block ingestion\n\n**The audit runs per block, not per file.** A single file may contain blocks drawn from different digital sources or encoding conventions. Audit each block whose provenance may differ, and record where the seams fall.\n','Translit §16.4 history')
t=sub1(t,r'(?ms)^### 16\.5 Witness collation\n\nIngestion is per-witness\..*?\n\n(?=### 16\.6)','''### 16.5 Witness collation

Ingestion is per-witness. Where witnesses disagree after normalization, the disagreement is textual and belongs to the source hierarchy (General Rules §1), not to this file.

**Do not resolve by majority vote.** Witnesses may share an ancestor or encoding source, so a vote can count copies rather than independent readings. The designated source of record governs; variants are recorded rather than averaged.''','Translit §16.5 history')
t=t.replace('- **In a corpus search:** expected and harmless, but the token is West-vocalized and **carries no evidence about pointing**. Distribution and lexical range may be cited from it; a vowel or a bgdkpt point may not. The patristic corpus is overwhelmingly West-vocalized apart from Narsai, so this is the ordinary case, not the exception.','- **In a corpus search:** a West-vocalized token **carries no evidence about East Syriac pointing**. Distribution and lexical range may be cited from it; a vowel or a bgdkpt point may not.')
t=t.replace('This is the only known case; it is recorded here so that a mismatch between string and source at such a word is recognized as expected rather than treated as an error.','A mismatch caused by that lossy source encoding is expected and must be checked against the page rather than treated as an ordinary round-trip failure.')
t=sub1(t,r'(?ms)^\*\*Function is not recorded\.\*\*.*?\n\nASCII:','**Function is not recorded.** The same graphical page-state receives the same notation regardless of grammatical interpretation.\n\nASCII:','Translit §17 status')
t=sub1(t,r'(?ms)^Attested only on \*\*pe\*\*.*?\n\nASCII:','ASCII:','Translit §18 status')
write(TRANSLIT,t)

# Glossary preamble
gl=read(GLOSSARY)
gl=gl.replace('<canonical transliteration> (total) — <rendering> (n), ...','<canonical transliteration> (decision total) — <rendering> (n), ...')
gl=gl.replace('The `{...}` field records the **part of speech and the morphology of the form**, never a\nroot. `[—]` marks a root not yet established (§10.20).','The `{...}` field records the **part of speech and the morphology of the form**, never a\nroot. Together, canonical headword + root + `{...}` morphology uniquely identify an entry.\n`[—]` marks a root not yet established (§10.20).\n\nCounts are **indexed decision counts**, not raw corpus-token totals. Repetitions, same-locus\nwitness duplicates, and common liturgical units excluded by General Rules §§10.13 and 10.18\ndo not increment them; `+n` records indexed decisions omitted from bullets under §10.11.')
gl=gl.replace('| stem | force | attested |','| stem | force | example |')
write(GLOSSARY,gl)

# README / sources metadata
r=read(README)
r=r.replace('- `sources/` — provenance and source-of-record documentation. Third-party source files are not assumed to be redistributable and are not automatically included here.','- `sources/` — provenance and source-of-record documentation, with machine-readable designations in `sources/sources.yaml`. Third-party source files are not assumed to be redistributable and are not automatically included here.')
r=r.replace('- `tools/` — reserved for future validation, transliteration, ingestion, corpus, and database tooling.','- `tools/` — validation, transliteration, ingestion, corpus, and database tooling.')
r=r.replace('while future software under `tools/` is intended to use the MIT License','while software under `tools/` is intended to use the MIT License')
r=sub1(r,r'(?ms)^## Status\n\n.*?\n\n(?=## Licensing)','Confirmed means that a text has passed the project\'s internal confirmation workflow; it does not make the text immutable. Changes to a confirmed text require the validation checks to be rerun.\n\n','README status')
write(README,r)
sr=read(SOURCES_README)
sr=sub1(sr,r'(?ms)^## What belongs here\n\n.*?(?=\nDo not add scans)','''## What belongs here

Machine-readable source-of-record designations are stored in `sources.yaml`. Only explicit designations belong there; the absence of a text from the mapping must never be interpreted as an inferred source choice.
''','sources README')
write(SOURCES_README,sr)
write(SOURCES_YAML,'''# Machine-readable source-of-record metadata.
# Only explicit designations are recorded; omission is not a source inference.

source_records:
  ksawa_d_mazmore:
    title: Ksawa d-Mazmore
    governs: Psalms
  breviarium_chaldaicum:
    title: Breviarium Chaldaicum
    governs: Hours
  syro_malabar_editio_typica:
    title: Editio Typica of the Syro-Malabar Church
    governs: Qurbana and Anaphoras
  east_syriac_mosul_peshitta:
    title: East Syriac Mosul Peshitta
    governs: Scripture other than Psalms

confirmed_texts:
  Creed_in_Syriac.txt:
    source_of_record: syro_malabar_editio_typica
    editorial_apparatus:
      - line: 17
        witness_label: Catholic
        reading: "[waḇrā]"
        source: syro_malabar_editio_typica
  Ferial_Slotha_d_Sapra_I.txt:
    source_of_record: breviarium_chaldaicum
  Ferial_Slotha_d_Sapra_II.txt:
    source_of_record: breviarium_chaldaicum
  Ferial_Slotha_d_Ramsha.txt:
    source_of_record: breviarium_chaldaicum
''')

# Hygiene and snapshot-status scan
for p in [GENERAL,TRANSLIT,GLOSSARY,README,SOURCES_README,SOURCES_YAML]:
    s=read(p)
    if unicodedata.normalize('NFC',s)!=s: raise SystemExit(f'{p}: not NFC')
    if '\r' in s: raise SystemExit(f'{p}: CR line ending')
    if any(x.rstrip()!=x for x in s.splitlines()): raise SystemExit(f'{p}: trailing whitespace')
patterns=[r'\bcurrently\b',r'\bcurrent instances\b',r'\bcurrent test status\b',r'\bnot yet attested\b',r'\buntested\b',r'\bunconfirmed\b',r'\bactive scholarly\b',r'\bno current instances\b',r'\bonly known case\b',r'\bnone has been encountered\b',r'\bno undotted stroke was ever encountered\b',r'\bof 999 occurrences\b',r'\bDetected in a Hudra unit\b',r'\bIn the Abun collation\b']
for p in [GENERAL,TRANSLIT,GLOSSARY,README,SOURCES_README]:
    s=read(p)
    for pat in patterns:
        if re.search(pat,s,re.I): raise SystemExit(f'{p}: status-like prose remains: {pat}')

# Glossary audit against the resulting rules
print('=== GLOSSARY AUDIT ===')
gl=read(GLOSSARY); ls=gl.splitlines()
hr=re.compile(r'^(?P<syriac>[\u0700-\u074f].*?)\s+\[(?P<root>[^\]]+)\](?:\s+\{(?P<morph>[^}]*)\})?\s+\(search:\s*(?P<search>[^)]+)\)\s*$')
entries=[]
for i,line in enumerate(ls):
    m=hr.match(line)
    if not m or i+1>=len(ls): continue
    mm=re.match(r'^(?P<canon>.+?)\s+\((?P<total>\d+)\)\s+—\s+(?P<renders>.+)$',ls[i+1])
    if not mm: continue
    e={**m.groupdict(),**mm.groupdict(),'line':i+1,'bullets':[]}; j=i+2
    while j<len(ls) and ls[j].startswith('* '): e['bullets'].append(ls[j]); j+=1
    entries.append(e)
print('entries_parsed:',len(entries))
missing=[e for e in entries if not (e['morph'] or '').strip()]
print('missing_morphology:',len(missing))
ident=defaultdict(list); baseid=defaultdict(list)
for e in entries:
    ident[(e['canon'],e['root'],(e['morph'] or '').strip())].append(e)
    baseid[(e['canon'],e['root'])].append(e)
dups={k:v for k,v in ident.items() if len(v)>1}; shared={k:v for k,v in baseid.items() if len({(x['morph'] or '').strip() for x in v})>1}
print('duplicate_full_identity:',len(dups))
for k,v in list(dups.items())[:20]: print('  DUP',k,'lines',[x['line'] for x in v])
print('same_headword_root_distinct_morphology:',len(shared))
for k,v in list(shared.items())[:20]: print('  MORPH-SPLIT',k,[(x['morph'],x['line']) for x in v])

def pc(x):
    m=re.fullmatch(r'(\d+)(?:\+(\d+))?',x); return (int(m.group(1)),int(m.group(2) or 0)) if m else None
cr=re.compile(r'\((\d+(?:\+\d+)?)\)(?=(?:\s+\[[^\]]+\])?(?:,|$))'); bad=[]
for e in entries:
    counts=[pc(x) for x in cr.findall(e['renders'])]
    if not counts: continue
    base=sum(x[0] for x in counts); total=sum(a+b for a,b in counts)
    if base!=len(e['bullets']) or total!=int(e['total']): bad.append((e['canon'],e['line'],len(e['bullets']),base,e['total'],total,e['renders']))
print('count_arithmetic_failures:',len(bad))
for x in bad[:30]: print('  COUNT',x)

files={'Creed':'Creed_in_Syriac.txt','Catholic Creed':'Creed_in_Syriac.txt','Abun':'Our_Father_in_Syriac.txt','Tešbōḥtā':'Teshbhotha_l-Alaha.txt',"Ferial Slotha d'Sapra I":'Ferial_Slotha_d_Sapra_I.txt',"Ferial Slotha d'Sapra II":'Ferial_Slotha_d_Sapra_II.txt',"Assyrian Slotha d'Sapra II":'Ferial_Slotha_d_Sapra_II.txt',"Ferial Slotha d'Ramsha":'Ferial_Slotha_d_Ramsha.txt'}
corpus={}
for label,fn in files.items():
    if fn not in corpus:
        blocks=[b.splitlines() for b in re.split(r'\n\n+',read(ROOT/'confirmed-texts'/fn).strip())]
        corpus[fn]=blocks
    corpus[label]=corpus[fn]
br=re.compile(r'^\*\s+(?P<form>.*?)\s+·\s+"(?P<context>.*)"\s+\((?P<cite>.+)\)$'); cir=re.compile(r'^(?P<label>.+?)\s+Line\s+(?P<line>\d+)$')
citebad=[]; trace=[]; ctxbad=[]
for e in entries:
    for b in e['bullets']:
        bm=br.match(b)
        if not bm: continue
        cm=cir.match(bm['cite'])
        if not cm or cm['label'] not in corpus: citebad.append((e['canon'],b)); continue
        blocks=corpus[cm['label']]; n=int(cm['line'])
        if len(blocks)!=3 or not (len(blocks[0])==len(blocks[1])==len(blocks[2])) or n<1 or n>len(blocks[0]): citebad.append((e['canon'],b)); continue
        tr=blocks[1][n-1]; eng=blocks[2][n-1]
        if bm['form'] not in tr: trace.append((e['canon'],bm['form'],bm['cite'],tr))
        engcmp=re.sub(r'\([^)]*:\)','',eng).strip()
        if '[' not in tr: engcmp=re.sub(r'\[[^\]]*\]','',engcmp); engcmp=re.sub(r'\s+',' ',engcmp).strip()
        pos=0; ok=True
        for part in [x for x in bm['context'].split('...') if x]:
            q=engcmp.find(part,pos)
            if q<0: ok=False; break
            pos=q+len(part)
        if not ok: ctxbad.append((e['canon'],bm['cite'],bm['context'],engcmp))
print('citation_or_label_failures:',len(citebad))
for x in citebad[:20]: print('  CITE',x)
print('attested_form_trace_failures:',len(trace))
for x in trace[:30]: print('  TRACE',x)
print('literal_context_failures:',len(ctxbad))
for x in ctxbad[:30]: print('  CONTEXT',x)
print('target_creed_bra_catholic_qualifier:', '"He who from the Father [and the Son] comes forth" (Catholic Creed Line 17)' in gl)
print('target_zabne:',[x for x in ls if 'zaḇn̈ē' in x or 'ܙܲܒ݂ܢ' in x][:4])
print('target_abun_line22_occultans_nasha:',any('Abun Line 22' in x and '(ʾ)nāš' in x for x in ls))
review=[]; stems=('Peal','Ethpeel','Pael','Ethpaal','Aphel','Ettaphal','Shaphel','Eshtaphal')
for e in entries:
    m=(e['morph'] or '').strip(); reasons=[]
    if not m: continue
    if re.search(r'\bnoun\b|\badj\.\b',m) and not re.search(r'\b(?:sg|pl)\b',m): reasons.append('number')
    if 'verb' in m and not any(st in m for st in stems): reasons.append('stem')
    if m in {'prep.','pron.','adj.','verb + prep. suff.'}: reasons.append('underspecified')
    if reasons: review.append((e['canon'],m,e['line'],','.join(reasons)))
print('morphology_review_candidates_nonmissing:',len(review))
for x in review[:60]: print('  MORPH',x)
print('=== END GLOSSARY AUDIT ===')