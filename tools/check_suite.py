#!/usr/bin/env python3
from pathlib import Path
import re,sys,unicodedata,collections
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.'); GLOSS=ROOT/'glossary/Glossary.md'; CONF=ROOT/'confirmed-texts'
LABEL_TO_FILE={'Creed':'Creed_in_Syriac.txt','Abun':'Our_Father_in_Syriac.txt','Tešbōḥtā':'Teshbhotha_l-Alaha.txt',"Ferial Slotha d'Sapra I":'Ferial_Slotha_d_Sapra_I.txt',"Ferial Slotha d'Sapra II":'Ferial_Slotha_d_Sapra_II.txt',"Assyrian Slotha d'Sapra II":'Ferial_Slotha_d_Sapra_II.txt',"Ferial Slotha d'Ramsha":'Ferial_Slotha_d_Ramsha.txt'}
results={}; details=collections.defaultdict(list)
def fail(n,msg): details[n].append(msg)
def passfail(n): results[n]=not details[n]
def load_text(p):
 b=p.read_bytes()
 try:s=b.decode('utf-8')
 except UnicodeDecodeError as e: fail(16,f'{p.name}: not UTF-8: {e}'); s=b.decode('utf-8','replace')
 return b,s
def split3(s,pname):
 parts=s.rstrip('\n').split('\n\n')
 if len(parts)!=3: fail(15,f'{pname}: expected 3 blocks separated by single blank lines; found {len(parts)}'); return None
 blocks=[x.split('\n') for x in parts]
 if len({len(x) for x in blocks})!=1: fail(15,f'{pname}: unequal block lengths {[len(x) for x in blocks]}')
 return blocks
files={}
for p in sorted(CONF.glob('*')):
 if not p.is_file(): continue
 b,s=load_text(p); blocks=split3(s,p.name)
 if blocks: files[p.name]={'bytes':b,'text':s,'syr':blocks[0],'tr':blocks[1],'en':blocks[2]}
for name,d in files.items():
 b,s=d['bytes'],d['text']
 if b.startswith(b'\xef\xbb\xbf'): fail(16,f'{name}: UTF-8 BOM present')
 if b'\r' in b: fail(16,f'{name}: CR/CRLF present; LF required')
 for i,line in enumerate(s.splitlines(),1):
  if line.endswith((' ','\t')): fail(16,f'{name}:{i}: trailing whitespace')
 if unicodedata.normalize('NFC',s)!=s: fail(16,f'{name}: not NFC')
 if '\u2018' in s or '\u2019' in s: fail(16,f'{name}: curly apostrophe present')
passfail(16)
NON_BG={'ܐ':'ʾ','ܗ':'h','ܘ':'w','ܙ':'z','ܚ':'ḥ','ܛ':'ṭ','ܝ':'y','ܠ':'l','ܡ':'m','ܢ':'n','ܣ':'s','ܥ':'ʿ','ܨ':'ṣ','ܩ':'q','ܪ':'r','ܫ':'š'}; BG={'ܒ':('ḃ','ḇ','b'),'ܓ':('ġ','ḡ','g'),'ܕ':('ḋ','ḏ','d'),'ܟ':('k̇','ḵ','k'),'ܦ':('ṗ','p̄','p'),'ܬ':('ṫ','ṯ','t')}; BASE=set(NON_BG)|set(BG); VOWEL_MARK={'\u0732':'a','\u0735':'ā','\u0738':'e','\u0739':'ē'}; SINGLE_AB={'\u0741','\u073f','\u0307'}; SINGLE_BL={'\u0742','\u073c','\u0323'}; SYAME='\u0308'; OCCAB='\u0747'; OCCBL='\u0748'; TWODOTS={'\u0324','\u0740','\u0744'}; BREVE_B='\u032e'; BETWEEN_AB='\u1df8'; BETWEEN_BL='\u1dfa'; SUPER='\u0711'
def is_syr_seq_char(c):
 o=ord(c); return c in BASE or c=='\u0716' or (0x0730<=o<=0x074A) or c in {'\u0307','\u0323','\u0308','\u0324','\u032e','\u1df8','\u1dfa','\u0711'}
def parse_word(w):
 cs=[];i=0
 while i<len(w):
  c=w[i]
  if c=='\u0716': base='ܪ'
  elif c in BASE: base=c
  else: raise ValueError(f'unrecognized/non-base U+{ord(c):04X} {unicodedata.name(c,"?")} in {w!r}')
  i+=1;marks=[]
  while i<len(w) and w[i] not in BASE and w[i]!='\u0716': marks.append(w[i]);i+=1
  cs.append([base,marks])
 return cs
def render_cluster(base,marks,vowel_override=None):
 pre='ᵃ' if SUPER in marks else ''; single_ab=[];single_bl=[]
 if base=='ܝ' and any(m in SINGLE_BL for m in marks): stem='ī';single_ab=[m for m in marks if m in SINGLE_AB]
 elif base=='ܘ' and any(m in SINGLE_AB for m in marks): stem='ō';single_bl=[m for m in marks if m in SINGLE_BL]
 elif base=='ܘ' and any(m in SINGLE_BL for m in marks): stem='ū';single_ab=[m for m in marks if m in SINGLE_AB]
 else:
  if base in BG:
   if any(m in SINGLE_AB for m in marks): stem=BG[base][0]
   elif any(m in SINGLE_BL for m in marks): stem=BG[base][1]
   else: stem=BG[base][2]
  else:
   stem=NON_BG[base];single_ab=[m for m in marks if m in SINGLE_AB];single_bl=[m for m in marks if m in SINGLE_BL]
  if single_ab: stem+='^'*len(single_ab)
  if single_bl: stem+='_'*len(single_bl)
 if any(m in TWODOTS for m in marks): stem+='\u0324'
 if BREVE_B in marks: stem+='\u032e'
 if SYAME in marks: stem+='\u0308'
 vm=[m for m in marks if m in VOWEL_MARK]
 if vm:
  if len(vm)!=1: raise ValueError('multiple Class-B vowels on one carrier')
  stem+=vowel_override if vowel_override is not None else VOWEL_MARK[vm[0]]
 if BETWEEN_AB in marks: stem+='^^'
 if BETWEEN_BL in marks: stem+='__'
 return unicodedata.normalize('NFC',pre+stem)
def translit_word(w):
 cs=parse_word(w);skip=set();rendered=[]
 for i,(base,marks) in enumerate(cs):
  if i in skip: continue
  override=None;vm=[m for m in marks if m in VOWEL_MARK]
  if vm and vm[0] in ('\u0735','\u0739'):
   v=VOWEL_MARK[vm[0]];nextmater=(i+1<len(cs) and cs[i+1][0]=='ܐ' and not cs[i+1][1])
   if nextmater and i+1==len(cs)-1: skip.add(i+1)
   elif not nextmater and i==len(cs)-1: override='ă' if v=='ā' else 'ĕ'
  rendered.append([i,render_cluster(base,marks,override)])
 out='';j=0
 while j<len(rendered):
  idx,text=rendered[j];marks=cs[idx][1];mark=OCCAB if OCCAB in marks else (OCCBL if OCCBL in marks else None)
  if mark:
   grp=[text];k=j+1
   while k<len(rendered):
    idx2,text2=rendered[k]
    if idx2==rendered[k-1][0]+1 and mark in cs[idx2][1]: grp.append(text2);k+=1
    else: break
   inner=''.join(grp);out+=f'({inner})' if mark==OCCAB else f'(_{inner})';j=k
  else: out+=text;j+=1
 return unicodedata.normalize('NFC',out)
def translit_line(line):
 out=[];i=0
 while i<len(line):
  if is_syr_seq_char(line[i]):
   j=i+1
   while j<len(line) and is_syr_seq_char(line[j]):j+=1
   out.append(translit_word(line[i:j]));i=j
  else:out.append(line[i]);i+=1
 return ''.join(out)
BGSET=set(BG);WEST=set(chr(x) for x in [0x0730,0x0731,0x0733,0x0734,0x0736,0x0737,0x073A,0x073B,0x073D,0x073E]);rank220={'\u0738':0,'\u0739':0,'\u0742':1,'\u073c':0,'\u0323':2,'\u0324':3,'\u0740':3,'\u0744':3,'\u032e':4,'\u0748':5};rank230={'\u0732':0,'\u0735':0,'\u0741':1,'\u073f':0,'\u0307':2,'\u0308':3,'\u0747':4};spell_to_tr={};tr_to_spell={}
def token_words(line):return re.sub(r'\([^()]*:[^()]*\)','',line).replace('[',' ').replace(']',' ').split()
for name,d in files.items():
 if len(d['syr'])!=len(d['tr']):continue
 for ln,(syr,tr) in enumerate(zip(d['syr'],d['tr']),1):
  try:calc=translit_line(syr)
  except Exception as e:fail(11,f'{name} line {ln}: transliteration engine error: {e}');calc=None
  if calc is not None and calc!=tr:fail(11,f'{name} line {ln}: derived transliteration mismatch\n  expected: {tr}\n  derived:  {calc}')
  sw=token_words(syr);tw=token_words(tr)
  if len(sw)!=len(tw):fail(14,f'{name} line {ln}: Syriac/translit token count differs {len(sw)} != {len(tw)}')
  else:
   for s,t in zip(sw,tw):spell_to_tr.setdefault(s,set()).add(t);tr_to_spell.setdefault(t,set()).add(s)
  for w in sw:
   try:cs=parse_word(w)
   except Exception as e:fail(12,f'{name} line {ln}: {e}');continue
   for base,marks in cs:
    for m in marks:
     if m in WEST:fail(12,f'{name} line {ln}: West Syriac vowel U+{ord(m):04X}')
     if m in ('\u0741','\u0742') and base not in BGSET:fail(12,f'{name} line {ln}: U+{ord(m):04X} on non-bgdkpt {base}')
     if m=='\u073c' and base not in {'ܘ','ܝ'}:fail(12,f'{name} line {ln}: U+073C on {base}, not waw/yodh')
     if m=='\u073f' and base!='ܘ':fail(12,f'{name} line {ln}: U+073F on {base}, not waw')
     if m in ('\u0323','\u0307') and base in BGSET:fail(12,f'{name} line {ln}: generic dot U+{ord(m):04X} on bgdkpt {base}')
    for cls,ranks in ((220,rank220),(230,rank230)):
     seq=[m for m in marks if unicodedata.combining(m)==cls];rr=[ranks.get(m,99) for m in seq]
     if rr!=sorted(rr):fail(13,f'{name} line {ln}: class {cls} mark order violation on {base}: {[f"U+{ord(m):04X}" for m in seq]}')
  if '\u0716' in syr:
   for m in re.finditer('\u0716',syr):
    if '\u0308' not in syr[m.start()+1:m.start()+5]:fail(12,f'{name} line {ln}: bare U+0716 source anomaly')
for s,ts in spell_to_tr.items():
 if len(ts)>1:fail(14,f'one Syriac spelling transliterates multiple ways: {s!r} -> {sorted(ts)}')
for t,ss in tr_to_spell.items():
 if len(ss)>1:fail(14,f'one transliteration maps to multiple spellings: {t!r} -> {sorted(ss)}')
passfail(11);passfail(12);passfail(13);passfail(14);passfail(15)
gtext=GLOSS.read_text(encoding='utf-8')
for i,c in enumerate(gtext):
 o=ord(c)
 if (0x0370<=o<=0x03FF) or (0x1F00<=o<=0x1FFF) or (0x0400<=o<=0x052F):fail(1,f'Greek/Cyrillic char U+{o:04X} {unicodedata.name(c,"?")} at offset {i}')
passfail(1)
if unicodedata.normalize('NFC',gtext)!=gtext:fail(2,'Glossary.md is not NFC')
passfail(2)
HEAD_RE=re.compile(r'^(?P<head>\S.*?)\s{3}\[(?P<root>[^\]]+)\]\s{3}\{(?P<morph>[^}]*)\}\s{3}\(search:\s*([^)]*)\)\s*$');TRANS_RE=re.compile(r'^(?P<tr>.*?)\s+\((?P<total>\d+)\)\s+—\s+(?P<renders>.*)$');CITE_RE=re.compile(r'\((?P<label>.+?)(?:,)?\s+Line\s+(?P<line>\d+)\)$');BUL_RE=re.compile(r'^\*\s+(?P<form>.*?)\s+·\s+"(?P<context>.*)"\s+\((?P<cite>.*)\)$')
entries=[];section=None;lines=gtext.splitlines();i=0
while i<len(lines):
 if lines[i].strip()=='## Phrases':section='phrase';i+=1;continue
 if lines[i].strip()=='## Forms':section='form';i+=1;continue
 m=HEAD_RE.match(lines[i]) if section else None
 if m:
  e={'section':section,'line':i+1,'head':m.group('head'),'root':m.group('root'),'morph':m.group('morph'),'bullets':[]}
  if i+1>=len(lines) or not TRANS_RE.match(lines[i+1]):fail(9,f'Glossary line {i+1}: entry missing/invalid transliteration line');i+=1;continue
  tm=TRANS_RE.match(lines[i+1]);e['tr']=tm.group('tr');e['total']=int(tm.group('total'));e['renders']=tm.group('renders');i+=2
  while i<len(lines) and lines[i].startswith('* '):
   bm=BUL_RE.match(lines[i])
   if not bm:fail(5,f'Glossary line {i+1}: malformed bullet: {lines[i]}')
   else:
    b=bm.groupdict();b['line_no']=i+1;cm=CITE_RE.match(b['cite'])
    if not cm:fail(5,f'Glossary line {i+1}: malformed citation ({b["cite"]})')
    else:b.update(label=cm.group('label'),src_line=int(cm.group('line')))
    e['bullets'].append(b)
   i+=1
  entries.append(e);continue
 i+=1
for e in entries:
 nums=re.findall(r'\((\d+)(?:\+(\d+))?\)',e['renders'])
 if not nums:fail(3,f'Glossary line {e["line"]}: no rendering decision counts');continue
 base=sum(int(a) for a,b in nums);total=sum(int(a)+(int(b) if b else 0) for a,b in nums)
 if len(e['bullets'])!=base:fail(3,f'{e["tr"]}: {len(e["bullets"])} bullets != Σbase {base}')
 if e['total']!=total:fail(3,f'{e["tr"]}: decision total {e["total"]} != Σ(base+extra) {total}')
passfail(3)
seen={}
for e in entries:
 key=(e['head'],e['root'],e['morph'])
 if key in seen:fail(6,f'duplicate identity at Glossary lines {seen[key]} and {e["line"]}: {key}')
 else:seen[key]=e['line']
passfail(6)
pos_words={'noun','adj.','pron.','prep.','conj.','adv.','particle','verb','quant.','poss.','num.','rel. pron.','prop. n.','verbal noun'};allowed_markers={'—','prop. noun','Gk. loan'}
for e in entries:
 if e['section']=='form' and not e['morph'].strip():fail(9,f'Glossary line {e["line"]}: empty morphology')
 if not e['root'].strip():fail(9,f'Glossary line {e["line"]}: empty root')
 r=e['root'].strip()
 if r not in allowed_markers and r in pos_words:fail(9,f'Glossary line {e["line"]}: part of speech in root field [{r}]')
passfail(9)
def source_line(label,n,block):
 fn=LABEL_TO_FILE.get(label)
 if not fn:return None,f'unknown citation label {label!r}'
 if fn not in files:return None,f'citation file missing {fn}'
 arr=files[fn][block]
 if n<1 or n>len(arr):return None,f'{label} Line {n} out of range (1..{len(arr)})'
 return arr[n-1],None
def clean_editorial_label(line):return re.sub(r'\([^()]*:[^()]*\)','',line).strip()
def normalize_context_line(en,tr):
 en=clean_editorial_label(en)
 if '[' not in tr:en=re.sub(r'\[[^\]]*\]','',en)
 else:en=en.replace('[','').replace(']','')
 return re.sub(r'\s+',' ',en).strip()
def find_segments(text,context):
 segs=[s.strip() for s in context.split('...') if s.strip()];pos=0;spans=[]
 for seg in segs:
  k=text.find(seg,pos)
  if k<0:return None
  spans.append((k,k+len(seg)));pos=k+len(seg)
 return spans
claims=collections.defaultdict(list)
for e in entries:
 if e['section']!='form':continue
 for b in e['bullets']:
  if 'label' not in b:continue
  tr,err=source_line(b['label'],b['src_line'],'tr')
  if err:fail(7,f'Glossary line {b["line_no"]}: {err}');continue
  words=token_words(tr);form_words=b['form'].split();found=[]
  for k in range(len(words)-len(form_words)+1):
   if words[k:k+len(form_words)]==form_words:found.append(k)
  if not found:fail(7,f'Glossary line {b["line_no"]}: attested form {b["form"]!r} not a token sequence of {b["label"]} Line {b["src_line"]}: {tr}')
  claims[(b['label'],b['src_line'])].append((b['form'],b['line_no']))
passfail(7)
ctx_by_line=collections.defaultdict(list)
for e in entries:
 for b in e['bullets']:
  if 'label' not in b:continue
  en,err=source_line(b['label'],b['src_line'],'en');tr,_=source_line(b['label'],b['src_line'],'tr')
  if err:fail(10,f'Glossary line {b["line_no"]}: {err}');continue
  clean=normalize_context_line(en,tr);ctx=b['context'];spans=find_segments(clean,ctx)
  if spans is None:fail(10,f'10a Glossary line {b["line_no"]}: context not traceable in English line\n  context: {ctx}\n  line:    {clean}')
  else:ctx_by_line[(b['label'],b['src_line'])].append((ctx,spans,b['line_no']))
for key,arr in ctx_by_line.items():
 for a in range(len(arr)):
  for b in range(a+1,len(arr)):
   c1,s1,l1=arr[a];c2,s2,l2=arr[b]
   if c1==c2:continue
   if any(max(x1,x2)<min(y1,y2) for x1,y1 in s1 for x2,y2 in s2):fail(10,f'10b {key}: overlapping nonidentical contexts at Glossary lines {l1},{l2}: {c1!r} / {c2!r}')
passfail(10)
for e in entries:
 parts=re.split(r',\s+(?=[^,]*\(\d+(?:\+\d+)?\)(?:\s|$))',e['renders']);contexts=' || '.join(b['context'] for b in e['bullets'])
 for part in parts:
  part=re.sub(r'\s*\(\d+(?:\+\d+)?\)\s*','',part).strip();part=re.sub(r'\s*\[[^\]]+\]\s*$','',part).strip()
  if not part or part=='⌀' or part.startswith('→'):continue
  candidates={part,re.sub(r'\(([^)]*)\)',r'\1',part),re.sub(r'\([^)]*\)','',part)};ok=False
  for cand in candidates:
   segs=[x for x in cand.split('...') if x]
   if segs and all(seg in contexts for seg in segs):ok=True;break
  if not ok:fail(8,f'{e["tr"]}: rendering {part!r} not traceable in own contexts: {contexts}')
passfail(8)
def positions_for_claim(words,form_words,used):
 for k in range(len(words)-len(form_words)+1):
  idx=tuple(range(k,k+len(form_words)))
  if words[k:k+len(form_words)]==form_words and not any(x in used for x in idx):return idx
 return None
first_line_seen={}
for fn,d in files.items():
 for n,tr in enumerate(d['tr'],1):
  label_candidates=[k for k,v in LABEL_TO_FILE.items() if v==fn and not k.startswith('Assyrian ')];cleantr=clean_editorial_label(tr).strip();repeated=cleantr in first_line_seen;words=token_words(tr);used=set();claimsets=[]
  for lab in label_candidates:claimsets+=claims.get((lab,n),[])
  if fn=='Ferial_Slotha_d_Sapra_II.txt':claimsets+=claims.get(("Assyrian Slotha d'Sapra II",n),[])
  for form,lno in claimsets:
   idx=positions_for_claim(words,form.split(),used)
   if idx is not None:used.update(idx)
  for j,w in enumerate(words):
   if w.strip('[]') in {'ʾāmēyn','hallēlūyā'}:used.add(j)
  if repeated:used.update(range(len(words)))
  else:first_line_seen[cleantr]=(fn,n)
  if '[' in tr and ']' in tr:
   outside=re.sub(r'\[[^\]]*\]','',tr);inside=' '.join(re.findall(r'\[([^\]]*)\]',tr));outw=token_words(outside);inw=token_words(inside);counts=collections.Counter(outw)
   for j,w in enumerate(words):
    if w in inw and counts[w]>0 and j not in used:counts[w]-=1;used.add(j)
  missing=[(j,w) for j,w in enumerate(words) if j not in used]
  if missing:fail(4,f'{fn} line {n}: uncovered token occurrences: {missing}; line={tr}');fail(5,f'{fn} line {n}: non-exempt occurrences without Glossary bullets: {missing}')
passfail(4);passfail(5)
print('East Syriac Project §11 certification');print('Subject:',ROOT);print();names={1:'Greek/Cyrillic homoglyph scan',2:'Glossary NFC',3:'Glossary decision counts',4:'source-token coverage',5:'coverage converse / bullet validity',6:'duplicate Glossary identity',7:'attested form in cited transliteration',8:'rendering traceability',9:'entry morphology/root structure',10:'context strings',11:'round-trip / derived transliteration',12:'carrier discipline',13:'combining-mark order',14:'orthography/transliteration injectivity',15:'three equal blocks',16:'file hygiene'}
for n in range(1,17):
 status='PASS' if results.get(n,False) else 'FAIL';print(f'{n:>2}. {status}  {names[n]}')
 for msg in details[n][:40]:print('    -',msg.replace('\n','\n      '))
 if len(details[n])>40:print(f'    - ... {len(details[n])-40} more')
print();failed=[n for n in range(1,17) if not results.get(n,False)];print('FAILED CHECKS:',failed if failed else 'none');sys.exit(1 if failed else 0)
