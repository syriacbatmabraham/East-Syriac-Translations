# Glossary

Form-first concordance. The unit is the word **form**; the root is a field. Proclitics are
stripped from the headword and retained on each occurrence.

Format:
```
<Syriac headword>   [root]   {part of speech + morphology}   (search: <fold key>)
<canonical transliteration> (decision total) — <rendering> (n), ...
* <attested form> · "<English context>" (Text Line n)
```

The `{...}` field records the **part of speech and the morphology of the form**, never a
root. Together, canonical headword + root + `{...}` morphology uniquely identify an entry.
`[—]` marks a root not yet established (§10.20).

Counts are **indexed decision counts**, not raw corpus-token totals. Repetitions, same-locus
witness duplicates, and common liturgical units excluded by General Rules §§10.13 and 10.18
do not increment them; `+n` records indexed decisions omitted from bullets under §10.11.

Abbreviations: person `1 2 3` · gender `m f c` · number `sg pl` · state `abs cst emph` ·
`perf impf impv inf` · `active ptcp. passive ptcp.` (`ptcp.` alone where the stem does not
distinguish voice) · `suff.` pronominal suffix · `encl.` enclitic pronoun.

`referent` prefixes any class where the form names one specific referent rather than a
general one — `ʿīr̈ē` {referent noun m.pl.emph.}, the Watchers. It is a project term, not a
grammatical one, and combines with whatever class the form already belongs to.

`particle` is written out, never abbreviated, so that it cannot be read as `ptcp.` Native
Syriac grammar knows only noun, verb and particle; this field is finer, so a word SEDRA
files as a particle may be recorded here as `adv.`, `prep.` or `conj.` where that is what
it does.

`quant.` marks a quantifier such as `kl` “all/every”; a pronominal suffix is named after `+`.
`poss.` marks a possessive form such as `dīlāḵ`; an attached pronominal suffix is named after `+`.
`indecl.` marks an indeclinable loan whose form does not express the ordinary Syriac inflectional distinctions.
`verbal noun` marks a deverbal nominal lexeme, not an infinitive or finite verb form; it
takes ordinary nominal gender, number, state, and pronominal-suffix morphology.
A SEDRA `Participle Adjective` is recorded here as `adj.` when the attested form belongs
to that lexical category; a homographic form parsed as a verb with active/passive
participle tense remains `ptcp.`.

**Verb stems.** The stem is named; what it does is read from here.

| stem | force | example |
|---|---|---|
| Peal | the simple, base action | `nesġōḏ` we reverence |
| Ethpeel | passive or reflexive of Peal | `ʾeṯīleḏ` he was begotten |
| Pael | intensive, or makes a noun into a verb | `nṣaleʾ` we pray |
| Ethpaal | passive or reflexive of Pael | `ʾeṫtaqanw` they were established |
| Aphel | causative — brings the Peal action about | `naseq` we lift up, i.e. cause to go up |
| Ettaphal | passive of Aphel | — |
| Shaphel | older causative, usually lexicalized | — |
| Eshtaphal | passive of Shaphel | — |

A **phrase** is tabled in its own section below and governs the rendering of its
components. Each component entry still records the occurrence, but points to the phrase
with `→` in place of a rendering of its own (§10.6).

**Search keys** are lowercase, diacritics stripped, `ʾ` and `ʿ` dropped, `š` folded to `sh`,
and notation characters (`^` `_` `(` `)` `[` `]` `⁀` `‿`) dropped. Collisions are expected. Human discretion is expected.

---

## Phrases

ܥܵܠܲܡ ܥܵܠܡܝܼܢ   [ʿ-l-m + ʿ-l-m]   {noun phrase}   (search: alam almin)
ʿālam ʿālmīn (2) — the Age of ages (2)
* dalʿālam ʿālmīn · "...and life unto the Age of ages. Amen" (Creed Line 21)
* lʿālam ʿālmīn · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14)

ܒܠܸܒܵܐ ܘܲܒ݂ܠܸܒܵܐ   [l-b-b + l-b-b]   {prep. phrase}   (search: bleba wableba)
blebā waḇlebā (1) — in doubled hearts (1)
* blebā waḇlebā · "In doubled hearts they speak" (Psalm 12 Line 8)

ܚܲܕ݂ ܒܫܲܒ݂ܥܵܐ   [ḥ-d + š-b-ʿ]   {numeral phrase}   (search: had bshaba)
ḥaḏ bšaḇʿā (1) — seven times (1)
* ḥaḏ bšaḇʿā · "And purified seven times" (Psalm 12 Line 18)

---

## Forms

ܡܗܲܝܡܢܝܼܢܲܢ   [h-y-m-n]   {Pael active ptcp. m.pl.abs. + 1cp encl.}   (search: mhaymninan)
mhaymnīnan (1) — we are faithful (1)
* mhaymnīnan · "We are faithful to One God..." (Creed Line 1)

ܚܲܕ   [ḥ-d]   {num. m.sg.abs.}   (search: had)
ḥad (4) — one (3), → ḥaḏ bšaḇʿā (1)
* bḥad · "We are faithful to One God..." (Creed Line 1)
* wabḥad · "And to One Mar Yah..." (Creed Line 3)
* waḇḥad · "And to One Ruha d'Qudsha, the Ruha of Truth" (Creed Line 16)
* ḥaḏ · "And purified seven times" (Psalm 12 Line 18) → ḥaḏ bšaḇʿā

ܐܲܠܵܗܵܐ   [ʾ-l-h]   {noun m.sg.emph.}   (search: alaha)
ʾalāhā (5) — God (5)
* ʾalāhā · "We are faithful to One God..." (Creed Line 1)
* dʾalāhā · "...Isho M'shiha, the Son of God, the Only One" (Creed Line 3)
* ʾalāhā · "True God from True God" (Creed Line 6)
* ʾalāhā · "True God from True God" (Creed Line 6)
* lʾalāhā · "Glory to God in the heights" (Teshbhotha l'Alaha Line 1)

ܐܲܒ݂ܵܐ   [ʾ-b]   {noun m.sg.emph.}   (search: aba)
ʾaḇā (4) — Father (4)
* ʾaḇā · "...the Father, the Holder of all" (Creed Line 1)
* ʾaḇā · "He who from the Father [and the Son] comes forth" (Creed Line 17)
* lʾaḇā · "Glory to the Father, to the Son..." (Our Father Line 15)
* ʾaḇā · "The Lord of all, the Father, the Son..." (Ferial Slotha d'Sapra I, Line 10)

ܐܲܚܝܼܕ   [ʾ-ḥ-d]   {adj. m.sg.cst.}   (search: ahid)
ʾaḥīd (1) — Holder (1)
* ʾaḥīd · "...the Father, the Holder of all" (Creed Line 1)

ܟܠ   [k-l]   {quant.}   (search: kl)
kl (3) — all (2), every (1)
* kl · "...the Father, the Holder of all" (Creed Line 1)
* bḵl · "In every moment, forever" (Teshbhotha l'Alaha Line 3)
* dḵl · "The Lord of all, the Father, the Son..." (Ferial Slotha d'Sapra I, Line 10)

ܥܵܒ݂ܘܿܕ݂ܵܐ   [ʿ-b-d]   {noun m.sg.emph.}   (search: aboda)
ʿāḇōḏā (1) — Maker (1)
* ʿāḇōḏā · "Maker of all things, seen and unseen" (Creed Line 2)

ܟܠܗܹܝܢ   [k-l]   {quant. + 3fp suff.}   (search: klheyn)
klhēyn (4) — all (3), all of them (1)
* dḵlhēyn · "Maker of all things, seen and unseen" (Creed Line 2)
* dḵlhēyn · "Firstborn of all creatures" (Creed Line 4)
* klhēyn · "All of them, the creatures You have created" (Ferial Slotha d'Sapra II, Line 8)
* klhēyn · "Mar Yah destroys all divided lips" (Psalm 12 Line 9)

ܐܲܝܠܹܝܢ   [ʾ-y-n-ʾ]   {rel. pron. c.pl.}   (search: ayleyn)
ʾaylēyn (1) — things (1)
* ʾaylēyn · "Maker of all things, seen and unseen" (Creed Line 2)

ܡܸܬܚܲܙ̈ܝܵܢ   [ḥ-z-ʾ]   {Ethpeel ptcp. f.pl.abs.}   (search: methazyan)
metḥaz̈yān (2) — seen (1), (un)seen (1) [wadlā]
* dmetḥaz̈yān · "Maker of all things, seen and unseen" (Creed Line 2)
* wadlā meṯḥaz̈yān · "Maker of all things, seen and unseen" (Creed Line 2)

ܡܵܪܝܵܐ   [m-r-ʾ]   {noun m.sg.emph.}   (search: marya)
māryā (12) — Mar Yah (12)
* māryā · "And to One Mar Yah..." (Creed Line 3)
* bmāryā · "In Mar Yah I have hoped..." (Psalm 11 Line 1)
* māryā · "...in You, Mar Yah, I have hoped" (Psalm 11 Line 3)
* māryā · "Mar Yah, in the Haykla of His holiness" (Psalm 11 Line 11)
* māryā · "Mar Yah, in Heaven, His Seat" (Psalm 11 Line 12)
* māryā · "Mar Yah examines the righteous and the unrighteous" (Psalm 11 Line 14)
* māryā · "For Mar Yah is righteous, and He loves righteousness" (Psalm 11 Line 19)
* māryā · "Save, Mar Yah, for good has come to an end" (Psalm 12 Line 1)
* māryā · "Mar Yah destroys all divided lips" (Psalm 12 Line 9)
* māryā · "Mar Yah has said: I will now arise" (Psalm 12 Line 14)
* dmāryā · "The utterance of Mar Yah is a pure utterance" (Psalm 12 Line 16)
* māryā · "And You, Mar Yah, keep them" (Psalm 12 Line 19)

ܐܝܼܫܘܿܥ   [prop. noun]   {prop. n.}   (search: isho)
ʾīšōʿ (1) — Isho (1)
* ʾīšōʿ · "...Isho M'shiha, the Son of God, the Only One" (Creed Line 3)

ܡܫܝܼܚܵܐ   [m-š-ḥ]   {adj. m.sg.emph.}   (search: mshiha)
mšīḥā (2) — M'shiha (2)
* mšīḥā · "...Isho M'shiha, the Son of God, the Only One" (Creed Line 3)
* mšīḥā · "...M'shiha, do not delay" (Psalm 12 Line 3)

ܒܪܹܗ   [b-r]   {noun m.sg.emph. + 3ms suff.}   (search: breh)
brēh (1) — the Son (1)
* brēh · "...Isho M'shiha, the Son of God, the Only One" (Creed Line 3)

ܐܝܼܚܝܼܕ݂ܵܝܵܐ   [y-ḥ-d]   {adj. m.sg.emph.}   (search: ihidaya)
ʾīḥīḏāyā (1) — the Only One (1)
* ʾīḥīḏāyā · "...Isho M'shiha, the Son of God, the Only One" (Creed Line 3)

ܒܘܼܟ݂ܪܵܐ   [b-k-r]   {noun m.sg.emph.}   (search: bukra)
būḵrā (1) — Firstborn (1)
* būḵrā · "Firstborn of all creatures" (Creed Line 4)

ܒܸܪ̈ܝܵܬ݂ܵܐ   [b-r-ʾ]   {noun f.pl.emph.}   (search: beryata)
ber̈yāṯā (2) — creatures (2)
* ber̈yāṯā · "Firstborn of all creatures" (Creed Line 4)
* ber̈yāṯā · "All of them, the creatures You have created" (Ferial Slotha d'Sapra II, Line 8)

ܗܵܘ   [h-w]   {dem. pron. m.sg.}   (search: haw)
hāw (3) — He who (3)
* hāw · "He who was begotten from His Father before all ages..." (Creed Line 5)
* hāw · "He who, for the sake of us, sons of men, and for our salvation..." (Creed Line 8)
* hāw · "He who from the Father [and the Son] comes forth" (Creed Line 17)

ܡ̣ܢ   [m-n]   {prep.}   (search: mn)
m_n (13) — from (12), at (1)
* dm_n · "He who was begotten from His Father before all ages..." (Creed Line 5)
* dm_n · "True God from True God" (Creed Line 6)
* m_n · "He who, for the sake of us, sons of men, and for our salvation..." (Creed Line 8)
* m_n · "And was embodied from the Ruha d'Qudsha" (Creed Line 9)
* m_n · "And was conceived and begotten from Mariam the Virgin" (Creed Line 11)
* m_n · "...and sat at the Right Hand of His Father" (Creed Line 14)
* dm_n · "He who from the Father [and the Son] comes forth" (Creed Line 17)
* m_n · "But deliver us from the Evil One" (Our Father Line 13)
* m_n · "From Eternity and unto Eternity, amen amen" (Our Father Line 16)
* m_n · "From the house of Your treasure, rich and overflowing" (Ferial Slotha d'Sapra I, Line 7)
* m_n · "...and His gifts from the needy and afflicted..." (Ferial Slotha d'Sapra I, Line 8)
* m_n · "And faithfulness has ceased from the earth" (Psalm 12 Line 2)
* m_n · "Rescue me and deliver me unto Eternity from this generation" (Psalm 12 Line 20)

ܐܲܒ݂ܘܼܗܝ   [ʾ-b]   {noun m.sg.emph. + 3ms suff.}   (search: abuhy)
ʾaḇūhy (2) — His Father (2)
* ʾaḇūhy · "He who was begotten from His Father before all ages..." (Creed Line 5)
* dʾaḇūhy · "Son of the Nature of His Father..." (Creed Line 7)

ܐܸܬ݂ܝܼܠܸܕ݂   [y-l-d]   {Ethpeel perf. 3m.sg.}   (search: etiled)
ʾeṯīleḏ (2) — begotten (2)
* ʾeṯīleḏ · "He who was begotten from His Father before all ages..." (Creed Line 5)
* wʾeṯīleḏ · "And was conceived and begotten from Mariam the Virgin" (Creed Line 11)

ܩܕܵܡ   [q-d-m]   {prep.}   (search: qdam)
qdām (1) — before (1)
* qdām · "He who was begotten from His Father before all ages..." (Creed Line 5)

ܟܠܗܘܿܢ   [k-l]   {quant. + 3mp suff.}   (search: klhon)
klhōn (2) — all (2)
* klhōn · "He who was begotten from His Father before all ages..." (Creed Line 5)
* bḵlhōn · "In all times and seasons" (Ferial Slotha d'Sapra I, Line 9)

ܥܵܠܡܹ̈ܐ   [ʿ-l-m]   {noun m.pl.emph.}   (search: alme)
ʿālm̈ē (2) — ages (2)
* ʿālm̈ē · "He who was begotten from His Father before all ages..." (Creed Line 5)
* ʿālm̈ē · "...by whose hands the ages were established..." (Creed Line 7)

ܐܸܬ݂ܥܒܸܕ   [ʿ-b-d]   {Ethpeel perf. 3m.sg.}   (search: etbed)
ʾeṯʿbed (1) — made (1)
* wlā ʾeṯʿbed · "...and was not made" (Creed Line 5)

ܫܲܪܝܼܪܵܐ   [š-r-r]   {adj. m.sg.emph.}   (search: sharira)
šarīrā (2) — True (2)
* šarīrā · "True God from True God" (Creed Line 6)
* šarīrā · "True God from True God" (Creed Line 6)

ܒܲܪ   [b-r]   {noun m.sg.cst.}   (search: bar)
bar (1) — Son (1)
* bar · "Son of the Nature of His Father..." (Creed Line 7)

ܟܝܵܢܵܐ   [k-y-n]   {noun m.sg.emph.}   (search: kyana)
kyānā (1) — Nature (1)
* kyānā · "Son of the Nature of His Father..." (Creed Line 7)

ܐܝܼ̈ܕܵܘܗܝ   [y-d]   {noun f.pl.emph. + 3ms suff.}   (search: idawhy)
ʾī̈dāwhy (1) — whose hands (1)
* dḇʾī̈dāwhy · "...by whose hands the ages were established..." (Creed Line 7)

ܐܸܬ݁ܬܲܩܲܢܘ   [t-q-n]   {Ethpaal perf. 3m.pl.}   (search: ettaqanw)
ʾeṫtaqanw (1) — were established (1)
* ʾeṫtaqanw · "...by whose hands the ages were established..." (Creed Line 7)

ܐܸܬ݂ܒ݁ܪܝܼ   [b-r-ʾ]   {Ethpeel perf. 3m.sg.}   (search: etbri)
ʾeṯḃrī (1) — were created (1)
* wʾeṯḃrī · "...and all things were created" (Creed Line 7)

ܟܠܡܸܕܸ݁ܡ   [k-l + m-d-m]   {indef. pron.}   (search: klmedem)
klmeḋem (1) — all things (1)
* klmeḋem · "...and all things were created" (Creed Line 7)

ܡܸܛܠܵܬܲܢ   [m-ṭ-l]   {prep. + 1cp suff.}   (search: metlatan)
meṭlātan (1) — for the sake of us (1)
* dmeṭlātan · "He who, for the sake of us, sons of men, and for our salvation..." (Creed Line 8)

ܒܢܲܝ̈ܢܵܫܵܐ   [b-r + ʾ-n-š]   {noun c.pl.emph.}   (search: bnaynasha)
bnaÿnāšā (4) — sons of men (4)
* bnaÿnāšā · "He who, for the sake of us, sons of men, and for our salvation..." (Creed Line 8)
* laḇnaÿnāšā · "And on earth, peace and good hope to the sons of men" (Teshbhotha l'Alaha Line 2)
* laḇnaÿnāšā · "His eyes are seeing and His eyelids are examining the sons of men" (Psalm 11 Line 13)
* bnaÿnāšā · "The sons of men speak emptiness" (Psalm 12 Line 6)

ܡܸܛܠ   [m-ṭ-l]   {prep.}   (search: metl)
meṭl (7) — for (6), because of (1)
* wmeṭl · "He who, for the sake of us, sons of men, and for our salvation..." (Creed Line 8)
* meṭl · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14)
* meṭl · "For, behold, sinners have drawn the bow" (Psalm 11 Line 6)
* meṭl · "For what You have prepared, they have thrown down" (Psalm 11 Line 9)
* meṭl · "For Mar Yah is righteous, and He loves righteousness" (Psalm 11 Line 19)
* meṭl · "Save, Mar Yah, for good has come to an end" (Psalm 12 Line 1)
* meṭl · "Because of the plundering of the poor..." (Psalm 12 Line 13)

ܦܘܼܪܩܵܢܲܢ   [p-r-q]   {noun m.sg.emph. + 1cp suff.}   (search: purqanan)
pūrqānan (1) — our salvation (1)
* pūrqānan · "He who, for the sake of us, sons of men, and for our salvation..." (Creed Line 8)

ܢܚܸܬ݂   [n-ḥ-t]   {Peal perf. 3m.sg.}   (search: nhet)
nḥeṯ (1) — came down (1)
* nḥeṯ · "...came down from Heaven" (Creed Line 8)

ܫܡܲܝܵܐ   [š-m-y]   {noun c.sg.emph.}   (search: shmaya)
šmayā (6) — Heaven (6)
* šmayā · "...came down from Heaven" (Creed Line 8)
* lašmayā · "He ascended to Heaven..." (Creed Line 14)
* dbašmayā · "Our Father, who art in Heaven..." (Our Father Line 1)
* dbašmayā · "Our Father who art in Heaven" (Our Father Line 4)
* dbašmayā · "let Thy desire be: on earth as it is in Heaven" (Our Father Line 9)
* bašmayā · "Mar Yah, in Heaven, His Seat" (Psalm 11 Line 12)

ܐܸܬ݂ܓܲܫܲܡ   [g-š-m]   {Ethpaal perf. 3m.sg.}   (search: etgasham)
ʾeṯgašam (1) — was embodied (1)
* wʾeṯgašam · "And was embodied from the Ruha d'Qudsha" (Creed Line 9)

ܪܘܼܚܵܐ   [r-w-ḥ]   {noun c.sg.emph.}   (search: ruha)
rūḥā (7) — Ruha (6), ruha (1)
* rūḥā · "And was embodied from the Ruha d'Qudsha" (Creed Line 9)
* rūḥā · "And to One Ruha d'Qudsha, the Ruha of Truth" (Creed Line 16)
* rūḥā · "And to One Ruha d'Qudsha, the Ruha of Truth" (Creed Line 16)
* rūḥā · "The Life-Giving Ruha" (Creed Line 18)
* walrūḥā · "...and to the Ruha d'Qudsha" (Our Father Line 15)
* wrūḥā · "...and the Ruha d'Qudsha, forever" (Ferial Slotha d'Sapra I, Line 10)
* wrūḥā · "And a ruha of affliction, the portion of their cup" (Psalm 11 Line 18)

ܩܘܼܕ݂ܫܵܐ   [q-d-š]   {noun m.sg.emph.}   (search: qudsha)
qūḏšā (4) — Qudsha (4)
* dqūḏšā · "And was embodied from the Ruha d'Qudsha" (Creed Line 9)
* dqūḏšā · "And to One Ruha d'Qudsha, the Ruha of Truth" (Creed Line 16)
* dqūḏšā · "...and to the Ruha d'Qudsha" (Our Father Line 15)
* dqūḏšā · "...and the Ruha d'Qudsha, forever" (Ferial Slotha d'Sapra I, Line 10)

ܗܘܵܐ   [h-w-ʾ]   {Peal perf. 3m.sg.}   (search: hwa)
hwā (1) — became (1)
* wahwā · "And became a son of man" (Creed Line 10)

ܒܲܪܢܵܫܵܐ   [b-r + ʾ-n-š]   {noun c.sg.emph.}   (search: barnasha)
barnāšā (1) — a son of man (1)
* barnāšā · "And became a son of man" (Creed Line 10)

ܐܸܬ݂ܒ݁ܛܸܢ   [b-ṭ-n]   {Ethpeel perf. 3m.sg.}   (search: etbten)
ʾeṯḃṭen (1) — was conceived (1)
* wʾeṯḃṭen · "And was conceived and begotten from Mariam the Virgin" (Creed Line 11)

ܡܲܪܝܲܡ   [prop. noun]   {prop. n.}   (search: maryam)
maryam (1) — Mariam (1)
* maryam · "And was conceived and begotten from Mariam the Virgin" (Creed Line 11)

ܒܬ݂ܘܼܠܬܵܐ   [b-t-l]   {noun f.sg.emph.}   (search: btulta)
bṯūltā (1) — the Virgin (1)
* bṯūltā · "And was conceived and begotten from Mariam the Virgin" (Creed Line 11)

ܚܲܫ   [ḥ-š-š]   {Peal perf. 3m.sg.}   (search: hash)
ḥaš (1) — suffered (1)
* wḥaš · "He suffered and was crucified..." (Creed Line 12)

ܐܸܙܕ݁ܩܸܦ   [z-q-p]   {Ethpeel perf. 3m.sg.}   (search: ezdqep)
ʾezḋqep (1) — was crucified (1)
* wʾezḋqep · "He suffered and was crucified..." (Creed Line 12)

ܝܵܘ̈ܡܲܝ   [y-w-m]   {noun m.pl.cst.}   (search: yawmay)
yāẅmay (1) — the days of (1)
* byāẅmay · "...in the days of Panthios Pilathos" (Creed Line 12)

ܦܲܢܛܝܼܘܿܣ   [prop. noun]   {prop. n.}   (search: pantios)
panṭīōs (1) — Panthios (1)
* panṭīōs · "...in the days of Panthios Pilathos" (Creed Line 12)

ܦܝܼܠܵܛܘܿܣ   [prop. noun]   {prop. n.}   (search: pilatos)
pīlāṭōs (1) — Pilathos (1)
* pīlāṭōs · "...in the days of Panthios Pilathos" (Creed Line 12)

ܡܝܼܬ݂   [m-w-t]   {Peal perf. 3m.sg.}   (search: mit)
mīṯ (1) — died (1)
* wmīṯ · "Died and was buried..." (Creed Line 13)

ܐܸܬ݂ܩܒܲܪ   [q-b-r]   {Ethpeel perf. 3m.sg.}   (search: etqbar)
ʾeṯqbar (1) — was buried (1)
* wʾeṯqbar · "Died and was buried..." (Creed Line 13)

ܩܵܡ   [q-w-m]   {Peal perf. 3m.sg.}   (search: qam)
qām (1) — arose (1)
* wqām · "...and He arose on the third day, as it is written" (Creed Line 13)

ܬܠܵܬ݂ܵܐ   [t-l-t]   {num. m.}   (search: tlata)
tlāṯā (1) — third (1)
* laṯlāṯā · "...and He arose on the third day, as it is written" (Creed Line 13)

ܝܵܘ̈ܡܝܼܢ   [y-w-m]   {noun m.pl.abs.}   (search: yawmin)
yāẅmīn (1) — day (1)
* yāẅmīn · "...and He arose on the third day, as it is written" (Creed Line 13)

ܐܲܝܟ݂   [ʾ-y-k]   {particle}   (search: ayk)
ʾayḵ (4) — as (2), like (2)
* ʾayḵ · "...and He arose on the third day, as it is written" (Creed Line 13)
* ʾayḵ · "Wander and dwell upon the mountains like a bird" (Psalm 11 Line 2)
* ʾayḵ · "Snares have come down upon the wicked like rain" (Psalm 11 Line 16)
* ʾayḵ · "as the contemptible high place of the sons of Edom" (Psalm 12 Line 22)

ܟܬ݂ܝܼܒ݂   [k-t-b]   {Peal passive ptcp. m.sg.abs.}   (search: ktib)
kṯīḇ (1) — written (1)
* daḵṯīḇ · "...and He arose on the third day, as it is written" (Creed Line 13)

ܣܠܸܩ   [s-l-q]   {Peal perf. 3m.sg.}   (search: sleq)
sleq (1) — ascended (1)
* wasleq · "He ascended to Heaven..." (Creed Line 14)

ܝܼܬܸܒ݂   [y-t-b]   {Peal perf. 3m.sg.}   (search: iteb)
īteḇ (1) — sat (1)
* wīteḇ · "...and sat at the Right Hand of His Father" (Creed Line 14)

ܝܲܡܝܼܢܵܐ   [y-m-n]   {noun f.sg.emph.}   (search: yamina)
yamīnā (1) — the Right Hand (1)
* yamīnā · "...and sat at the Right Hand of His Father" (Creed Line 14)

ܐܲܒ݂ܘܗܝ   [ʾ-b]   {noun m.sg.emph. + 3ms suff.}   (search: abwhy)
ʾaḇwhy (1) — His Father (1)
* dʾaḇwhy · "...and sat at the Right Hand of His Father" (Creed Line 14)

ܬܘܼܒ݂   [t-w-b]   {adv.}   (search: tub)
tūḇ (1) — again (1)
* wṯūḇ · "And He will come again..." (Creed Line 15)

ܥܬ݂ܝܼܕ   [ʿ-t-d]   {Peal passive ptcp. m.sg.abs.}   (search: tid)
ʿṯīd (1) — will (1)
* ʿṯīd · "And He will come again..." (Creed Line 15)

ܡܹܐܬ݂ܵܐ   [ʾ-t-ʾ]   {Peal inf.}   (search: meta)
mēʾṯā (1) — come (1)
* lmēʾṯā · "And He will come again..." (Creed Line 15)

ܡܕ݂ܵܢ   [d-w-n]   {Peal inf.}   (search: mdan)
mḏān (1) — judge (1)
* lamḏān · "...to judge the dead and the living" (Creed Line 15)

ܡܝܼܬܹ̈ܐ   [m-w-t]   {adj. m.pl.emph.}   (search: mite)
mīẗē (1) — the dead (1)
* lmīẗē · "...to judge the dead and the living" (Creed Line 15)

ܚܲܝܹ̈ܐ   [ḥ-y-ʾ]   {adj. m.pl.emph.}   (search: haye)
ḥaÿē (1) — living (1)
* walḥaÿē · "...to judge the dead and the living" (Creed Line 15)

ܚܲܝܹ̈ܐ   [ḥ-y-ʾ]   {noun m.pl.emph.}   (search: haye)
ḥaÿē (1) — life (1)
* waḇḥaÿē · "...and life unto the Age of ages. Amen" (Creed Line 21)

ܫܪܵܪܵܐ   [š-r-r]   {noun m.sg.emph.}   (search: shrara)
šrārā (1) — Truth (1)
* dašrārā · "And to One Ruha d'Qudsha, the Ruha of Truth" (Creed Line 16)

ܢܵܦܹܩ   [n-p-q]   {Peal active ptcp. m.sg.abs.}   (search: napeq)
nāpēq (1) — comes forth (1)
* nāpēq · "He who from the Father [and the Son] comes forth" (Creed Line 17)

ܒܪܵܐ   [b-r]   {noun m.sg.emph.}   (search: bra)
brā (3) — the Son (3)
* [waḇrā] · "He who from the Father [and the Son] comes forth" (Catholic Creed Line 17)
* wlaḇrā · "Glory to the Father, to the Son..." (Our Father Line 15)
* waḇrā · "The Lord of all, the Father, the Son..." (Ferial Slotha d'Sapra I, Line 10)

ܡܲܚܝܵܢܵܐ   [ḥ-y-ʾ]   {adj. m.sg.emph.}   (search: mahyana)
maḥyānā (1) — Life-Giving (1)
* maḥyānā · "The Life-Giving Ruha" (Creed Line 18)

ܚܕ݂ܵܐ   [ḥ-d]   {num. f.sg.abs.}   (search: hda)
ḥḏā (2) — One (2)
* wbaḥḏā · "And to One holy and apostolic Catholic Church" (Creed Line 19)
* baḥḏā · "We confess One baptism for the release of sins" (Creed Line 20)

ܥܹܕ݁ܬܵܐ   [ʿ-d-t]   {noun f.sg.emph.}   (search: edta)
ʿēḋtā (1) — Church (1)
* ʿēḋtā · "And to One holy and apostolic Catholic Church" (Creed Line 19)

ܩܲܕ݁ܝܼܫܬܵܐ   [q-d-š]   {adj. f.sg.emph.}   (search: qadishta)
qaḋīštā (1) — holy (1)
* qaḋīštā · "And to One holy and apostolic Catholic Church" (Creed Line 19)

ܫܠܝܼܚܲܝܬܵܐ   [š-l-ḥ]   {adj. f.sg.emph.}   (search: shlihayta)
šlīḥaytā (1) — apostolic (1)
* wašlīḥaytā · "And to One holy and apostolic Catholic Church" (Creed Line 19)

ܩܵܬ݂ܘܿܠܝܼܩܝܼ   [Gk. loan]   {adj. indecl.}   (search: qatoliqi)
qāṯōlīqī (1) — Catholic (1)
* qāṯōlīqī · "And to One holy and apostolic Catholic Church" (Creed Line 19)

ܡܵܘܕܹ݁ܝܢܲܢ   [y-d-ʾ]   {Aphel active ptcp. m.pl.abs. + 1cp encl.}   (search: mawdeynan)
māwḋēynan (1) — we confess (1)
* māwḋēynan · "We confess One baptism for the release of sins" (Creed Line 20)

ܡܲܥܡܘܿܕ݁ܝܼܬ݂ܵܐ   [ʿ-m-d]   {noun f.sg.emph.}   (search: mamodita)
maʿmōḋīṯā (1) — baptism (1)
* maʿmōḋīṯā · "We confess One baptism for the release of sins" (Creed Line 20)

ܫܘܼܒ݂ܩܵܢܵܐ   [š-b-q]   {noun m.sg.emph.}   (search: shubqana)
šūḇqānā (1) — release (1)
* lšūḇqānā · "We confess One baptism for the release of sins" (Creed Line 20)

ܚܛܵܗܹ̈ܐ   [ḥ-ṭ-ʾ]   {noun m.pl.emph.}   (search: htahe)
ḥṭāḧē (1) — sins (1)
* daḥṭāḧē · "We confess One baptism for the release of sins" (Creed Line 20)

ܩܝܵܡܬܵܐ   [q-w-m]   {noun f.sg.emph.}   (search: qyamta)
qyāmtā (1) — resurrection (1)
* wbaqyāmtā · "the resurrection of bodies..." (Creed Line 21)

ܦܲܓ݂ܪܹ̈ܐ   [p-g-r]   {noun m.pl.emph.}   (search: pagre)
paḡr̈ē (1) — bodies (1)
* dpaḡr̈ē · "the resurrection of bodies..." (Creed Line 21)

ܥܵܠܲܡ   [ʿ-l-m]   {noun m.sg.cst.}   (search: alam)
ʿālam (2) — → ʿālam ʿālmīn (2)
* dalʿālam · "...and life unto the Age of ages. Amen" (Creed Line 21) → ʿālam ʿālmīn
* lʿālam · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14) → ʿālam ʿālmīn

ܥܵܠܲܡ   [ʿ-l-m]   {noun m.sg.abs.}   (search: alam)
ʿālam (3) — Eternity (3)
* ʿālam · "From Eternity and unto Eternity, amen amen" (Our Father Line 16)
* lʿālam · "From Eternity and unto Eternity, amen amen" (Our Father Line 16)
* lʿālam · "Rescue me and deliver me unto Eternity from this generation" (Psalm 12 Line 20)

ܥܵܠܡܝܼܢ   [ʿ-l-m]   {noun m.pl.abs.}   (search: almin)
ʿālmīn (4) — → ʿālam ʿālmīn (2), forever (2)
* ʿālmīn · "...and life unto the Age of ages. Amen" (Creed Line 21) → ʿālam ʿālmīn
* ʿālmīn · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14) → ʿālam ʿālmīn
* lʿālmīn · "In every moment, forever" (Teshbhotha l'Alaha Line 3)
* lʿālmīn · "...and the Ruha d'Qudsha, forever" (Ferial Slotha d'Sapra I, Line 10)

ܐܲܒ݂ܘܼܢ   [ʾ-b]   {noun m.sg.emph.}   (search: abun)
ʾaḇūn (2) — our Father (2)
* ʾaḇūn · "Our Father, who art in Heaven..." (Our Father Line 1)
* ʾaḇūn · "Our Father who art in Heaven" (Our Father Line 4)

ܢܸܬ݂ܩܲܕܲܫ   [q-d-š]   {Ethpaal impf. 3m.sg.}   (search: netqadash)
neṯqadaš (1) — hallowed be (1)
* neṯqadaš · "...hallowed be Thy Name" (Our Father Line 1)

ܫܡܵܟ݂   [š-m]   {noun m.sg.emph. + 2ms suff.}   (search: shmak)
šmāḵ (1) — Thy Name (1)
* šmāḵ · "...hallowed be Thy Name" (Our Father Line 1)

ܬܹܐܬܸܐ   [ʾ-t-ʾ]   {Peal impf. 3f.sg.}   (search: tete)
tēʾteʾ (1) — May...come (1)
* tēʾteʾ · "May Thy Kingdom come" (Our Father Line 2)

ܡܲܠܟ݁ܘܼܬ݂ܵܟ݂   [m-l-k]   {noun f.sg.emph. + 2ms suff.}   (search: malkutak)
malk̇ūṯāḵ (1) — Thy Kingdom (1)
* malk̇ūṯāḵ · "May Thy Kingdom come" (Our Father Line 2)

ܩܲܕܝܼܫ   [q-d-š]   {adj. m.sg.abs.}   (search: qadish)
qadīš (2) — Holy (2)
* qadīš · "Holy, Holy, Thou art Holy" (Our Father Line 3)
* qadīš · "...Holy, Holy, Thou art Holy" (Our Father Line 6)

ܩܲܕܝܼܫܲܬ݁   [q-d-š]   {adj. m.sg.abs. + 2ms encl.}   (search: qadishat)
qadīšaṫ (2) — Thou art Holy (2)
* qadīšaṫ · "Holy, Holy, Thou art Holy" (Our Father Line 3)
* qadīšaṫ · "...Holy, Holy, Thou art Holy" (Our Father Line 6)

ܡܠܹܝܢ   [m-l-ʾ]   {Peal passive ptcp. m.pl.abs.}   (search: mleyn)
mlēyn (1) — are full (1)
* damlēyn · "The heavens and the earth are full of the greatness of Thy glory" (Our Father Line 5)

ܫܡܲܝܵ̈ܐ   [š-m-y]   {noun c.pl.emph.}   (search: shmaya)
šmaÿā (1) — the heavens (1)
* šmaÿā · "The heavens and the earth are full of the greatness of Thy glory" (Our Father Line 5)

ܐܲܪܥܵܐ   [ʾ-r-ʿ]   {noun f.sg.emph.}   (search: ara)
ʾarʿā (5) — earth (5)
* wʾarʿā · "The heavens and the earth are full of the greatness of Thy glory" (Our Father Line 5)
* bʾarʿā · "let Thy desire be: on earth as it is in Heaven" (Our Father Line 9)
* ʾarʿā · "And on earth, peace and good hope to the sons of men" (Teshbhotha l'Alaha Line 2)
* ʾarʿā · "And faithfulness has ceased from the earth" (Psalm 12 Line 2)
* bʾarʿā · "Choice silver tried in the earth" (Psalm 12 Line 17)

ܪܲܒ݁ܘܼܬ݂   [r-b-b]   {noun f.sg.cst.}   (search: rabut)
raḃūṯ (1) — the greatness of (1)
* raḃūṯ · "The heavens and the earth are full of the greatness of Thy glory" (Our Father Line 5)

ܫܘܼܒ݂ܚܵܟ݂   [š-b-ḥ]   {noun m.sg.emph. + 2ms suff.}   (search: shubhak)
šūḇḥāḵ (1) — Thy glory (1)
* šūḇḥāḵ · "The heavens and the earth are full of the greatness of Thy glory" (Our Father Line 5)

ܥܝܼܪܹ̈ܐ   [ʿ-y-r]   {referent noun m.pl.emph.}   (search: ire)
ʿīr̈ē (1) — Watchers (1)
* ʿīr̈ē · "Watchers and men cry out to You..." (Our Father Line 6)

ܐ݇ܢܵܫܵ̈ܐ   [ʾ-n-š]   {noun c.pl.emph.}   (search: nasha)
(ʾ)nāš̈ā (1) — men (1)
* w(ʾ)nāš̈ā · "Watchers and men cry out to You..." (Our Father Line 6)

ܩ᷸ܵܥܹܝܢ   [q-ʿ-ʾ]   {Peal active ptcp. m.pl.abs.}   (search: qaeyn)
qā^^ʿēyn (1) — cry out (1)
* qā^^ʿēyn · "Watchers and men cry out to You..." (Our Father Line 6)

ܠܵܟ݂   [l]   {prep. + 2ms suff.}   (search: lak)
lāḵ (2) — to You (2)
* lāḵ · "Watchers and men cry out to You..." (Our Father Line 6)
* lāḵ · "Early they come to You, my Lord" (Ferial Slotha d'Sapra II, Line 1)

ܢܸܗܘܸܐ   [h-w-ʾ]   {Peal impf. 3m.sg.}   (search: nehwe)
nehweʾ (1) — let...be (1)
* nehweʾ · "let Thy desire be: on earth as it is in Heaven" (Our Father Line 9)

ܨܸܒ݂ܝܵܢܵܟ݂   [ṣ-b-ʾ]   {noun m.sg.emph. + 2ms suff.}   (search: sebyanak)
ṣeḇyānāḵ (2) — Thy desire (1), Your desire (1)
* ṣeḇyānāḵ · "let Thy desire be: on earth as it is in Heaven" (Our Father Line 9)
* waḇṣeḇyānāḵ · "And by Your desire have come to be" (Ferial Slotha d'Sapra II, Line 10)

ܐܲܝܟܲܢܵܐ   [ʾ-y-k]   {adv.}   (search: aykana)
ʾaykanā (2) — as (2)
* ʾaykanā · "let Thy desire be: on earth as it is in Heaven" (Our Father Line 9)
* ʾaykanā · "...as we have released our debtors" (Our Father Line 11)

ܐܵܦ   [ʾ-p]   {particle}   (search: ap)
ʾāp (2) — ⌀ (2)
* ʾāp · "let Thy desire be: on earth as it is in Heaven" (Our Father Line 9)
* dʾāp · "...as we have released our debtors" (Our Father Line 11)

ܗܲܒ݂   [y-h-b]   {Peal impv. 2m.sg.}   (search: hab)
haḇ (1) — give (1)
* haḇ · "Give us this day the bread we need" (Our Father Line 10)

ܠܲܢ   [l]   {prep. + 1cp suff.}   (search: lan)
lan (2) — us (2)
* lan · "Give us this day the bread we need" (Our Father Line 10)
* lan · "And release us our debts and sins..." (Our Father Line 11)

ܠܲܚܡܵܐ   [l-ḥ-m]   {noun m.sg.emph.}   (search: lahma)
laḥmā (1) — the bread (1)
* laḥmā · "Give us this day the bread we need" (Our Father Line 10)

ܣܘܼܢܩܵܢܲܢ   [s-n-q]   {noun m.sg.emph. + 1cp suff.}   (search: sunqanan)
sūnqānan (1) — we need (1)
* dsūnqānan · "Give us this day the bread we need" (Our Father Line 10)

ܝܵܘܡܵܢܵܐ   [y-w-m]   {noun m.sg.emph.}   (search: yawmana)
yāwmānā (1) — this day (1)
* yāwmānā · "Give us this day the bread we need" (Our Father Line 10)

ܫܒ݂ܘܿܩ   [š-b-q]   {Peal impv. 2m.sg.}   (search: shboq)
šḇōq (1) — release (1)
* wašḇōq · "And release us our debts and sins..." (Our Father Line 11)

ܚܵܘܒܲܝ̈ܢ   [ḥ-w-b]   {noun m.pl.emph. + 1cp suff.}   (search: hawbayn)
ḥāwbaÿn (1) — our debts (1)
* ḥāwbaÿn · "And release us our debts and sins..." (Our Father Line 11)

ܚܛܵܗܲܝ̈ܢ   [ḥ-ṭ-ʾ]   {noun m.pl.emph. + 1cp suff.}   (search: htahayn)
ḥṭāhaÿn (1) — sins (1)
* waḥṭāhaÿn · "And release us our debts and sins..." (Our Father Line 11)

ܚܢܲܢ   [ʾ-n-ʾ]   {pron. 1c.pl.}   (search: hnan)
ḥnan (1) — we (1)
* ḥnan · "...as we have released our debtors" (Our Father Line 11)

ܫܒܲܩ̣͞ܢ   [š-b-q]   {Peal perf. 1c.pl.}   (search: shbaqn)
šbaq_⁀n (1) — have released (1)
* šbaq_⁀n · "...as we have released our debtors" (Our Father Line 11)

ܚܲܝܵܒܲܝ̈ܢ   [ḥ-w-b]   {adj. m.pl.emph. + 1cp suff.}   (search: hayabayn)
ḥayābaÿn (1) — our debtors (1)
* lḥayābaÿn · "...as we have released our debtors" (Our Father Line 11)

ܬܲܥܠܲܢ   [ʿ-l-l]   {Aphel impf. 2m.sg. + 1cp suff.}   (search: talan)
taʿlan (1) — enter us (1)
* lā taʿlan · "Do not enter us into testing" (Our Father Line 12)

ܢܸܣܝܘܿܢܵܐ   [n-s-ʾ]   {noun m.sg.emph.}   (search: nesyona)
nesyōnā (1) — testing (1)
* lnesyōnā · "Do not enter us into testing" (Our Father Line 12)

ܐܸܠܵܐ   [ʾ-l-ʾ]   {conj.}   (search: ela)
ʾelā (1) — but (1)
* ʾelā · "But deliver us from the Evil One" (Our Father Line 13)

ܦܲܨܵܢ   [p-ṣ-ʾ]   {Pael impv. 2m.sg. + 1cp suff.}   (search: pasan)
paṣān (1) — deliver us (1)
* paṣān · "But deliver us from the Evil One" (Our Father Line 13)

ܒܝܼܫܵܐ   [b-ʾ-š]   {referent adj. m.sg.emph.}   (search: bisha)
bīšā (1) — the Evil One (1)
* bīšā · "But deliver us from the Evil One" (Our Father Line 13)

ܕܝܼܠܵܟ݂   [d-y-l]   {poss. + 2ms suff.}   (search: dilak)
dīlāḵ (1) — Thine (1)
* ddīlāḵ · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14)

ܗ݇ܝܼ   [h-w]   {pron. 3f.sg.}   (search: hi)
(h)ī (1) — is (1)
* (h)ī · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14)

ܡܲܠܟ݁ܘܼܬ݂ܵܐ   [m-l-k]   {noun f.sg.emph.}   (search: malkuta)
malk̇ūṯā (1) — the Kingdom (1)
* malk̇ūṯā · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14)

ܚܲܝܠܵܐ   [ḥ-y-l]   {noun m.sg.emph.}   (search: hayla)
ḥaylā (1) — the power (1)
* wḥaylā · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14)

ܬܸܫܒ݁ܘܿܚܬܵܐ   [š-b-ḥ]   {noun f.sg.emph.}   (search: teshbohta)
tešḃōḥtā (2) — glory (2)
* wtešḃōḥtā · "For Thine is the Kingdom, the power and the glory, unto the Age of ages. Amen" (Our Father Line 14)
* tešḃōḥtā · "Glory to God in the heights" (Teshbhotha l'Alaha Line 1)

ܫܘܼܒ݂ܚܵܐ   [š-b-ḥ]   {noun m.sg.emph.}   (search: shubha)
šūḇḥā (2) — glory (2)
* šūḇḥā · "Glory to the Father, to the Son..." (Our Father Line 15)
* wšūḇḥā · "And we lift up continual glory without ceasing..." (Ferial Slotha d'Ramsha, Line 4)

ܥܕܲܡܵܐ   [ʿ-d-m]   {prep.}   (search: dama)
ʿdamā (1) — unto (1)
* waʿdamā · "From Eternity and unto Eternity, amen amen" (Our Father Line 16)

ܡܪܵ̈ܘܡܹܐ   [r-w-m]   {noun m.pl.emph.}   (search: mrawme)
mr̈āwmē (1) — the heights (1)
* bamr̈āwmē · "Glory to God in the heights" (Teshbhotha l'Alaha Line 1)

ܥܲܠ   [ʿ-l]   {prep.}   (search: al)
ʿal (4) — on (1), upon (3)
* wʿal · "And on earth, peace and good hope to the sons of men" (Teshbhotha l'Alaha Line 2)
* ʿal · "Wander and dwell upon the mountains like a bird" (Psalm 11 Line 2)
* ʿal · "And have set their arrows upon the string" (Psalm 11 Line 7)
* ʿal · "Snares have come down upon the wicked like rain" (Psalm 11 Line 16)

ܫܠܵܡܵܐ   [š-l-m]   {noun m.sg.emph.}   (search: shlama)
šlāmā (2) — peace (2)
* šlāmā · "And on earth, peace and good hope to the sons of men" (Teshbhotha l'Alaha Line 2)
* šlāmā · "Let us pray. Peace be with us" (Ferial Slotha d'Ramsha, Line 1)

ܣܲܒ݂ܪܵܐ   [s-b-r]   {noun m.sg.emph.}   (search: sabra)
saḇrā (1) — hope (1)
* wsaḇrā · "And on earth, peace and good hope to the sons of men" (Teshbhotha l'Alaha Line 2)

ܛܵܒ݂ܵܐ   [ṭ-w-b]   {adj. m.sg.emph.}   (search: taba)
ṭāḇā (3) — good (2), Good One (1)
* ṭāḇā · "And on earth, peace and good hope to the sons of men" (Teshbhotha l'Alaha Line 2)
* ṭāḇā · "O Good One, who does not withhold His mercies..." (Ferial Slotha d'Sapra I, Line 8)
* ṭāḇā · "Save, Mar Yah, for good has come to an end" (Psalm 12 Line 1)

ܥܸܕܵܢ   [ʿ-d-n]   {noun m.sg.abs.}   (search: edan)
ʿedān (1) — moment (1)
* ʿedān · "In every moment, forever" (Teshbhotha l'Alaha Line 3)

ܚܲܢܵܢܵܐ   [ḥ-n-n]   {adj. m.sg.emph.}   (search: hanana)
ḥanānā (1) — Gracious One (1)
* ḥanānā · "O Gracious One, O Merciful One, O Tender One" (Ferial Slotha d'Sapra I, Line 1)

ܡܪܲܚܡܵܢܵܐ   [r-ḥ-m]   {adj. m.sg.emph.}   (search: mrahmana)
mraḥmānā (1) — Merciful One (1)
* wamraḥmānā · "O Gracious One, O Merciful One, O Tender One" (Ferial Slotha d'Sapra I, Line 1)

ܡܪܲܚܦܵܢܵܐ   [r-ḥ-p]   {adj. m.sg.emph.}   (search: mrahpana)
mraḥpānā (1) — Tender One (1)
* wamraḥpānā · "O Gracious One, O Merciful One, O Tender One" (Ferial Slotha d'Sapra I, Line 1)

ܦܬ݂ܝܼܚܘܼ   [p-t-ḥ]   {Peal passive ptcp. m.sg.abs. + 3ms encl.}   (search: ptihu)
pṯīḥū (1) — is open (1)
* dapṯīḥū · "Whose door is open to those who return" (Ferial Slotha d'Sapra I, Line 2)

ܬܲܪܥܹܗ   [t-r-ʿ]   {noun m.sg.emph. + 3ms suff.}   (search: tareh)
tarʿēh (1) — whose door (1)
* tarʿēh · "Whose door is open to those who return" (Ferial Slotha d'Sapra I, Line 2)

ܬܲܝܵ̇ܒܹ̈ܐ   [t-w-b]   {adj. m.pl.emph.}   (search: tayabe)
tay^āb̈ē (1) — those who return (1)
* ltay^āb̈ē · "Whose door is open to those who return" (Ferial Slotha d'Sapra I, Line 2)

ܐܲܡܝܼܢܘܼ   [ʾ-m-n]   {noun f.sg.abs.}   (search: aminu)
ʾamīnū (1) — continually (1)
* wbaʾmīnū · "And who continually calls sinners..." (Ferial Slotha d'Sapra I, Line 3)

ܩܵ̇ܪܹܐ   [q-r-ʾ]   {Peal active ptcp. m.sg.abs.}   (search: qare)
q^ārē (1) — calls (1)
* q^ārē · "And who continually calls sinners..." (Ferial Slotha d'Sapra I, Line 3)

ܚܲܛܵܝܹ̈ܐ   [ḥ-ṭ-ʾ]   {adj. m.pl.emph.}   (search: hataye)
ḥaṭāÿē (3) — sinners (3)
* lḥaṭāÿē · "And who continually calls sinners..." (Ferial Slotha d'Sapra I, Line 3)
* ḥaṭāÿē · "Sinners have schemed against me..." (Psalm 11 Line 3)
* ḥaṭāÿē · "For, behold, sinners have drawn the bow" (Psalm 11 Line 6)

ܨܹܐܕ݂ܵܘܗܝ   [ṣ-y-d]   {prep. + 3ms suff.}   (search: sedawhy)
ṣēʾḏāwhy (1) — unto Him (1)
* dṣēʾḏāwhy · "...that unto Him they may draw near for returning" (Ferial Slotha d'Sapra I, Line 3)

ܢܸܬ݂ܩܲܪܒ݂ܘܼܢ   [q-r-b]   {Ethpaal impf. 3m.pl.}   (search: netqarbun)
neṯqarḇūn (1) — they may draw near (1)
* neṯqarḇūn · "...that unto Him they may draw near for returning" (Ferial Slotha d'Sapra I, Line 3)

ܬܝܵܒ݂ܘܼܬ݂ܵܐ   [t-w-b]   {noun f.sg.emph.}   (search: tyabuta)
tyāḇūṯā (1) — returning (1)
* laṯyāḇūṯā · "...that unto Him they may draw near for returning" (Ferial Slotha d'Sapra I, Line 3)

ܦܬܲܚܠܵܗ̇   [p-t-ḥ]   {Peal impv. 2m.sg. + prep. l + 3fs suff.}   (search: ptahlah)
ptaḥlāh^ (1) — open (1)
* ptaḥlāh^ · "Open, our Lord and our God..." (Ferial Slotha d'Sapra I, Line 4)

ܡܵܪܲܢ   [m-r-ʾ]   {noun m.sg.emph. + 1cp suff.}   (search: maran)
māran (2) — our Lord (2)
* māran · "Open, our Lord and our God..." (Ferial Slotha d'Sapra I, Line 4)
* māran · "And our lips are our own; who is our Lord?" (Psalm 12 Line 12)

ܐܲܠܵܗܲܢ   [ʾ-l-h]   {noun m.sg.emph. + 1cp suff.}   (search: alahan)
ʾalāhan (1) — our God (1)
* wʾalāhan · "Open, our Lord and our God..." (Ferial Slotha d'Sapra I, Line 4)

ܬܲܪܥܵܐ   [t-r-ʿ]   {noun m.sg.emph.}   (search: tara)
tarʿā (1) — the door (1)
* tarʿā · "...the door of mercies to our prayer" (Ferial Slotha d'Sapra I, Line 4)

ܪܲ̈ܚܡܹܐ   [r-ḥ-m]   {noun m.pl.emph.}   (search: rahme)
r̈aḥmē (1) — mercies (1)
* dr̈aḥmē · "...the door of mercies to our prayer" (Ferial Slotha d'Sapra I, Line 4)

ܨܠܘܿܬܲܢ   [ṣ-l-ʾ]   {noun f.sg.emph. + 1cp suff.}   (search: slotan)
ṣlōtan (1) — our prayer (1)
* laṣlōtan · "...the door of mercies to our prayer" (Ferial Slotha d'Sapra I, Line 4)

ܩܲܒܸ݁ܠܹܝܗ̇   [q-b-l]   {Pael impv. 2m.sg. + 3fs suff.}   (search: qabeleyh)
qaḃelēyh^ (1) — accept (1)
* wqaḃelēyh^ · "And accept our pleading" (Ferial Slotha d'Sapra I, Line 5)

ܒܵܥܘܼܬܲܢ   [b-ʿ-ʾ]   {noun f.sg.emph. + 1cp suff.}   (search: bautan)
bāʿūtan (1) — our pleading (1)
* lḇāʿūtan · "And accept our pleading" (Ferial Slotha d'Sapra I, Line 5)

ܦܲܢܵܐ   [p-n-ʾ]   {Pael impv. 2m.sg.}   (search: pana)
panā (1) — render (1)
* wpanā · "And render, in Your mercies, our requests" (Ferial Slotha d'Sapra I, Line 6)

ܪܲ̈ܚܡܲܝܟ   [r-ḥ-m]   {noun m.pl.emph. + 2ms suff.}   (search: rahmayk)
r̈aḥmayk (1) — Your mercies (1)
* br̈aḥmayk · "And render, in Your mercies, our requests" (Ferial Slotha d'Sapra I, Line 6)

ܫܹ̈ܐܠܵܬܲܢ   [š-ʾ-l]   {noun f.pl.emph. + 1cp suff.}   (search: shelatan)
š̈ēʾlātan (1) — our requests (1)
* š̈ēʾlātan · "And render, in Your mercies, our requests" (Ferial Slotha d'Sapra I, Line 6)

ܒܹܝܬ݂   [b-y-t]   {noun m.sg.cst.}   (search: beyt)
bēyṯ (1) — the house of (1)
* bēyṯ · "From the house of Your treasure, rich and overflowing" (Ferial Slotha d'Sapra I, Line 7)

ܓܲܙܵܟ݂   [g-z]   {noun m.sg.emph. + 2ms suff.}   (search: gazak)
gazāḵ (1) — Your treasure (1)
* gazāḵ · "From the house of Your treasure, rich and overflowing" (Ferial Slotha d'Sapra I, Line 7)

ܥܲܬ݁ܝܼܪܵܐ   [ʿ-t-r]   {adj. m.sg.emph.}   (search: atira)
ʿaṫīrā (1) — rich (1)
* ʿaṫīrā · "From the house of Your treasure, rich and overflowing" (Ferial Slotha d'Sapra I, Line 7)

ܫܦܝܼܥܵܐ   [š-p-ʿ]   {adj. m.sg.emph.}   (search: shpia)
špīʿā (1) — overflowing (1)
* wašpīʿā · "From the house of Your treasure, rich and overflowing" (Ferial Slotha d'Sapra I, Line 7)

ܟܵܠܹ̇ܐ   [k-l-ʾ]   {Peal active ptcp. m.sg.abs.}   (search: kale)
kāl^ē (1) — withhold (1)
* dlā kāl^ē · "O Good One, who does not withhold His mercies..." (Ferial Slotha d'Sapra I, Line 8)

ܪܲ̈ܚܡܵܘܗܝ   [r-ḥ-m]   {noun m.pl.emph. + 3ms suff.}   (search: rahmawhy)
r̈aḥmāwhy (1) — His mercies (1)
* r̈aḥmāwhy · "O Good One, who does not withhold His mercies..." (Ferial Slotha d'Sapra I, Line 8)

ܡܵܘܗܒ݂ܵܬܹܗ̈   [y-h-b]   {noun f.pl.emph. + 3ms suff.}   (search: mawhbateh)
māwhḇātēḧ (1) — His gifts (1)
* wmāwhḇātēḧ · "...and His gifts from the needy and afflicted..." (Ferial Slotha d'Sapra I, Line 8)

ܣܢܝܼ̈ܩܹܐ   [s-n-q]   {Peal passive ptcp. m.pl.emph.}   (search: sniqe)
snī̈qē (1) — the needy (1)
* snī̈qē · "...and His gifts from the needy and afflicted..." (Ferial Slotha d'Sapra I, Line 8)

ܐܲܠܝܼܨܹ̈ܐ   [ʾ-l-ṣ]   {Peal passive ptcp. m.pl.emph.}   (search: alise)
ʾalīṣ̈ē (1) — afflicted (1)
* wʾalīṣ̈ē · "...and His gifts from the needy and afflicted..." (Ferial Slotha d'Sapra I, Line 8)

ܥܲܒ݂ܕܵܘ̈ܗܝ   [ʿ-b-d]   {noun m.pl.emph. + 3ms suff.}   (search: abdawhy)
ʿaḇdāẅhy (1) — His servants (1)
* ʿaḇdāẅhy · "...His servants who call and beseech Him" (Ferial Slotha d'Sapra I, Line 8)

ܩܵ̇ܪܹܝܢ   [q-r-ʾ]   {Peal active ptcp. m.pl.abs.}   (search: qareyn)
q^ārēyn (1) — call (1)
* dq^ārēyn · "...His servants who call and beseech Him" (Ferial Slotha d'Sapra I, Line 8)

ܡܸܬ݂ܟܲܫܦܝܼܢ   [k-š-p]   {Ethpaal ptcp. m.pl.abs.}   (search: metkashpin)
meṯkašpīn (1) — beseech (1)
* wmeṯkašpīn · "...His servants who call and beseech Him" (Ferial Slotha d'Sapra I, Line 8)

ܠܹܗ   [l]   {prep. + 3ms suff.}   (search: leh)
lēh (2) — Him (1), itself (1)
* lēh · "...His servants who call and beseech Him" (Ferial Slotha d'Sapra I, Line 8)
* lēh · "Deceit has increased, and love itself has abated..." (Psalm 12 Line 3)

ܙܲܒ݂ܢܹ̈ܐ   [z-b-n]   {noun m.pl.emph.}   (search: zabne)
zaḇn̈ē (1) — times (1)
* zaḇn̈ē · "In all times and seasons" (Ferial Slotha d'Sapra I, Line 9)

ܥܸܕܵܢܹ̈ܐ   [ʿ-d-n]   {noun m.pl.emph.}   (search: edane)
ʿedān̈ē (1) — seasons (1)
* wʿedān̈ē · "In all times and seasons" (Ferial Slotha d'Sapra I, Line 9)

ܡܵܪܵܐ   [m-r-ʾ]   {noun m.sg.abs.}   (search: mara)
mārā (1) — the Lord (1)
* mārā · "The Lord of all, the Father, the Son..." (Ferial Slotha d'Sapra I, Line 10)

ܡܵܪܝ   [m-r-ʾ]   {noun m.sg.emph. + 1cs suff.}   (search: mary)
māry (2) — my Lord (2)
* māry · "Early they come to You, my Lord" (Ferial Slotha d'Sapra II, Line 1)
* māry · "My Lord, we confess unto Your Divinity..." (Ferial Slotha d'Ramsha, Line 2)

ܡܩܲܕܡܵܢ̈   [q-d-m]   {Pael active ptcp. f.pl.abs.}   (search: mqadman)
mqadmān̈ (1) — early they come (1)
* mqadmān̈ · "Early they come to You, my Lord" (Ferial Slotha d'Sapra II, Line 1)

ܒܵܪ̈ܟܵܢ   [b-r-k]   {Peal active ptcp. f.pl.abs.}   (search: barkan)
bār̈kān (1) — they kneel (1)
* wḇār̈kān · "They kneel and reverence" (Ferial Slotha d'Sapra II, Line 2)

ܣܵ̈ܓ݂ܕܵܢ   [s-g-d]   {Peal active ptcp. f.pl.abs.}   (search: sagdan)
s̈āḡdān (1) — reverence (1)
* ws̈āḡdān · "They kneel and reverence" (Ferial Slotha d'Sapra II, Line 2)

ܙܵܡ̇ܪܵ̈ܢ   [z-m-r]   {Peal active ptcp. f.pl.abs.}   (search: zamran)
zām^r̈ān (1) — sing (1)
* wzām^r̈ān · "Sing and praise" (Ferial Slotha d'Sapra II, Line 3)

ܡܗܲܠ̈ܠܵܢ   [h-l-l]   {Pael active ptcp. f.pl.abs.}   (search: mhallan)
mhal̈lān (1) — praise (1)
* wamhal̈lān · "Sing and praise" (Ferial Slotha d'Sapra II, Line 3)

ܚܵܕ݂ܝܵ̈ܢ   [ḥ-d-y]   {Peal active ptcp. f.pl.abs.}   (search: hadyan)
ḥāḏÿān (1) — rejoice (1)
* wḥāḏÿān · "[Rejoice and exult]" (Assyrian Ferial Slotha d'Sapra II, Line 4)

ܕܵܝ̈ܨܵܢ   [d-w-ṣ]   {Peal active ptcp. f.pl.abs.}   (search: daysan)
dāÿṣān (1) — exult (1)
* wḏāÿṣān · "[Rejoice and exult]" (Assyrian Ferial Slotha d'Sapra II, Line 4)

ܫܵ̈ܐܠܵܢ   [š-ʾ-l]   {Peal active ptcp. f.pl.abs.}   (search: shalan)
š̈āʾlān (1) — ask (1)
* wš̈āʾlān · "Ask and entreat" (Ferial Slotha d'Sapra II, Line 5)

ܡܦܝܼ̈ܣܵܢ   [p-y-s]   {Aphel active ptcp. f.pl.abs.}   (search: mpisan)
mpī̈sān (1) — entreat (1)
* wampī̈sān · "Ask and entreat" (Ferial Slotha d'Sapra II, Line 5)

ܒܵܥ̈ܝܵܢ   [b-ʿ-ʾ]   {Peal active ptcp. f.pl.abs.}   (search: bayan)
bāʿ̈yān (1) — seek (1)
* wḇāʿ̈yān · "Seek and beseech" (Ferial Slotha d'Sapra II, Line 6)

ܡܸܬ݂ܟܲܫ̈ܦܵܢ   [k-š-p]   {Ethpaal ptcp. f.pl.abs.}   (search: metkashpan)
meṯkaš̈pān (1) — beseech (1)
* wmeṯkaš̈pān · "Seek and beseech" (Ferial Slotha d'Sapra II, Line 6)

ܡܵܘ̈ܕܝܵܢ   [y-d-ʾ]   {Aphel active ptcp. f.pl.abs.}   (search: mawdyan)
māẅdyān (1) — confess (1)
* wmāẅdyān · "And confess and glorify" (Ferial Slotha d'Sapra II, Line 7)

ܡܫܲܒ݁ܚܵܢ̈   [š-b-ḥ]   {Pael active ptcp. f.pl.abs.}   (search: mshabhan)
mšaḃḥān̈ (1) — glorify (1)
* wamšaḃḥān̈ · "And confess and glorify" (Ferial Slotha d'Sapra II, Line 7)

ܒܪܲܝܬ݁   [b-r-ʾ]   {Peal perf. 2m.sg.}   (search: brayt)
brayṫ (1) — You have created (1)
* daḇrayṫ · "All of them, the creatures You have created" (Ferial Slotha d'Sapra II, Line 8)

ܪܸܡܙܵܟ݂   [r-m-z]   {noun m.sg.emph. + 2ms suff.}   (search: remzak)
remzāḵ (1) — by Your beckoning (1)
* daḇremzāḵ · "[Those] who by Your beckoning have been established" (Ferial Slotha d'Sapra II, Line 9)

ܐܸܬ݁ܬܲܩܲܢ   [t-q-n]   {Ethpaal perf. 3f.pl.}   (search: ettaqan)
ʾeṫtaqan (1) — have been established (1)
* ʾeṫtaqan · "[Those] who by Your beckoning have been established" (Ferial Slotha d'Sapra II, Line 9)

ܐܲܝܠܸܝܢ   [ʾ-y-n-ʾ]   {rel. pron. c.pl.}   (search: ayleyn)
ʾayleyn (1) — those (1)
* ʾayleyn · "[Those] who by Your beckoning have been established" (Assyrian Ferial Slotha d'Sapra II, Line 9)

ܐܸܬ݁ܬܲܩܲܢܝ̈   [t-q-n]   {Ethpaal perf. 3f.pl.}   (search: ettaqany)
ʾeṫtaqanÿ (1) — have been established (1)
* ʾeṫtaqanÿ · "[Those] who by Your beckoning have been established" (Assyrian Ferial Slotha d'Sapra II, Line 9)

ܐܸܬܲܝ̈   [ʾ-t-ʾ]   {Peal perf. 3f.pl.}   (search: etay)
ʾetaÿ (1) — have come (1)
* ʾetaÿ · "And by Your desire have come to be" (Ferial Slotha d'Sapra II, Line 10)

ܗܘܵܝܵܐ   [h-w-ʾ]   {verbal noun m.sg.emph.}   (search: hwaya)
hwāyā (1) — be (1)
* lahwāyā · "And by Your desire have come to be" (Ferial Slotha d'Sapra II, Line 10)

ܐܲܢ݇ܬ݁ܘܼ   [ʾ-n-t]   {pron. 2m.sg. + 3ms encl.}   (search: antu)
ʾa(n)ṫū (1) — You are (1)
* dʾa(n)ṫū · "For You are the Cause of their being" (Ferial Slotha d'Sapra II, Line 11)

ܥܸܠܬ݂ܵܐ   [ʿ-l-l]   {noun f.sg.emph.}   (search: elta)
ʿelṯā (1) — the Cause (1)
* ʿelṯā · "For You are the Cause of their being" (Ferial Slotha d'Sapra II, Line 11)

ܗܘܵܝܗܹܝܢ   [h-w-ʾ]   {verbal noun m.sg.emph. + 3fp suff.}   (search: hwayheyn)
hwāyhēyn (1) — their being (1)
* dahwāyhēyn · "For You are the Cause of their being" (Ferial Slotha d'Sapra II, Line 11)

ܣܵܘܩܵܐ   [s-w-q]   {noun m.sg.emph.}   (search: sawqa)
sāwqā (1) — the Breathing (1)
* wsāwqā · "And the Breathing and Breath of our life" (Ferial Slotha d'Sapra II, Line 12)

ܢܫܲܡܬ݂ܵܐ   [n-š-m]   {noun f.sg.emph.}   (search: nshamta)
nšamṯā (1) — Breath (1)
* wanšamṯā · "And the Breathing and Breath of our life" (Ferial Slotha d'Sapra II, Line 12)

ܚܲܝܲܝ̈ܢ   [ḥ-y-ʾ]   {noun m.pl.emph. + 1cp suff.}   (search: hayayn)
ḥayaÿn (1) — our life (1)
* dḥayaÿn · "And the Breathing and Breath of our life" (Ferial Slotha d'Sapra II, Line 12)

ܢܨܲܠܸܐ   [ṣ-l-ʾ]   {Pael impf. 1c.pl.}   (search: nsale)
nṣaleʾ (1) — let us pray (1)
* nṣaleʾ · "Let us pray. Peace be with us" (Ferial Slotha d'Ramsha, Line 1)

ܥܲܡܲܢ   [ʿ-m-m]   {prep. + 1cp suff.}   (search: aman)
ʿaman (1) — with us (1)
* ʿaman · "Let us pray. Peace be with us" (Ferial Slotha d'Ramsha, Line 1)

ܢܵܘܕܸܐ   [y-d-ʾ]   {Aphel impf. 1c.pl.}   (search: nawde)
nāwdeʾ (1) — we confess unto (1)
* nāwdeʾ · "My Lord, we confess unto Your Divinity..." (Ferial Slotha d'Ramsha, Line 2)

ܐܲܠܵܗܘܼܬ݂ܵܟ݂   [ʾ-l-h]   {noun f.sg.emph. + 2ms suff.}   (search: alahutak)
ʾalāhūṯāḵ (1) — Your Divinity (1)
* lʾalāhūṯāḵ · "My Lord, we confess unto Your Divinity..." (Ferial Slotha d'Ramsha, Line 2)

ܢܸܣܓ݁ܘܿܕ݂   [s-g-d]   {Peal impf. 1c.pl.}   (search: nesgod)
nesġōḏ (1) — we reverence (1)
* wnesġōḏ · "We reverence Your Lordship" (Ferial Slotha d'Ramsha, Line 3)

ܡܵܪܘܼܬ݂ܵܟ݂   [m-r-ʾ]   {noun f.sg.emph. + 2ms suff.}   (search: marutak)
mārūṯāḵ (1) — Your Lordship (1)
* lmārūṯāḵ · "We reverence Your Lordship" (Ferial Slotha d'Ramsha, Line 3)

ܐܲܡܝܼܢܵܐ   [ʾ-m-n]   {adj. m.sg.emph.}   (search: amina)
ʾamīnā (1) — continual (1)
* ʾamīnā · "And we lift up continual glory without ceasing..." (Ferial Slotha d'Ramsha, Line 4)

ܫܲܠܘܵܐ   [š-l-ʾ]   {noun m.sg.emph.}   (search: shalwa)
šalwā (1) — ceasing (1)
* dlā šalwā · "And we lift up continual glory without ceasing..." (Ferial Slotha d'Ramsha, Line 4)

ܢܲܣܸܩ   [s-l-q]   {Aphel impf. 1c.pl.}   (search: naseq)
naseq (1) — we lift up (1)
* naseq · "And we lift up continual glory without ceasing..." (Ferial Slotha d'Ramsha, Line 4)

ܬܠܝܼܬ݂ܵܝܘܼܬ݂ܵܟ݂   [t-l-t]   {noun f.sg.emph. + 2ms suff.}   (search: tlitayutak)
tlīṯāyūṯāḵ (1) — Your...Trinity (1)
* laṯlīṯāyūṯāḵ · "...to Your glorious Trinity in every moment" (Ferial Slotha d'Ramsha, Line 4)

ܡܫܲܒܲܚܬܵܐ   [š-b-ḥ]   {adj. f.sg.emph.}   (search: mshabahta)
mšabaḥtā (1) — glorious (1)
* mšabaḥtā · "...to Your glorious Trinity in every moment" (Ferial Slotha d'Ramsha, Line 4)

ܟܠܥܸܕܵܢ   [k-l + ʿ-d-n]   {quant. + noun m.sg.abs.}   (search: kledan)
klʿedān (1) — every moment (1)
* bḵlʿedān · "...to Your glorious Trinity in every moment" (Ferial Slotha d'Ramsha, Line 4)

ܣܲܒ݁ܪܹܬ݂   [s-b-r]   {Peal perf. 1c.sg.}   (search: sabret)
saḃrēṯ (2) — I have hoped (2)
* saḃrēṯ · "In Mar Yah I have hoped..." (Psalm 11 Line 1)
* saḃrēṯ · "...in You, Mar Yah, I have hoped" (Psalm 11 Line 3)

ܐܲܝܟܲܢ   [ʾ-y-k]   {interrog. adv.}   (search: aykan)
ʾaykan (1) — how (1)
* ʾaykan · "...how are you saying to my soul:" (Psalm 11 Line 1)

ܐܵܡ̇ܪܝܼܬ݁ܘܿܢ   [ʾ-m-r]   {Peal active ptcp. m.pl.abs. + 2mp encl.}   (search: amriton)
ʾām^rīṫōn (1) — are you saying (1)
* ʾām^rīṫōn · "...how are you saying to my soul:" (Psalm 11 Line 1)

ܢܲܦ̮ܫܝ   [n-p-š]   {noun f.sg.emph. + 1cs suff.}   (search: napshy)
nap̮šy (1) — my soul (1)
* lnap̮šy · "...how are you saying to my soul:" (Psalm 11 Line 1)

ܢܘܼܕ݂ܝ   [n-w-d]   {Peal impv. 2f.sg.}   (search: nudy)
nūḏy (1) — wander (1)
* nūḏy · "Wander and dwell upon the mountains like a bird" (Psalm 11 Line 2)

ܫܟܲܢܝ   [š-k-n]   {Peal impv. 2f.sg.}   (search: shkany)
škany (1) — dwell (1)
* waškany · "Wander and dwell upon the mountains like a bird" (Psalm 11 Line 2)

ܛܘܼܪܹ̈ܐ   [ṭ-w-r]   {noun m.pl.emph.}   (search: ture)
ṭūr̈ē (1) — mountains (1)
* ṭūr̈ē · "Wander and dwell upon the mountains like a bird" (Psalm 11 Line 2)

ܨܸܦܪܵܐ   [ṣ-p-r]   {noun m.sg.emph.}   (search: sepra)
ṣeprā (1) — bird (1)
* ṣeprā · "Wander and dwell upon the mountains like a bird" (Psalm 11 Line 2)

ܐܸܬ݁ܛܲܟܲܢܘ   [ṭ-k-n]   {Ethpaal perf. 3m.pl.}   (search: ettakanw)
ʾeṫṭakanw (1) — schemed (1)
* ʾeṫṭakanw · "Sinners have schemed against me..." (Psalm 11 Line 3)

ܠܝܼ   [l]   {prep. + 1cs suff.}   (search: li)
lī (1) — against me (1)
* lī · "Sinners have schemed against me..." (Psalm 11 Line 3)

ܒܵܟ݂   [b]   {prep. + 2ms suff.}   (search: bak)
bāḵ (1) — in You (1)
* bāḵ · "...in You, Mar Yah, I have hoped" (Psalm 11 Line 3)

ܗܵܐ   [h-ʾ]   {particle}   (search: ha)
hā (1) — behold (1)
* dhā · "For, behold, sinners have drawn the bow" (Psalm 11 Line 6)

ܡ̇ܠܵܘ   [m-l-ʾ]   {Peal perf. 3m.pl.}   (search: mlaw)
m^lāw (1) — have drawn (1)
* m^lāw · "For, behold, sinners have drawn the bow" (Psalm 11 Line 6)

ܩܸܫܬܵܐ   [q-š-t]   {noun f.sg.emph.}   (search: qeshta)
qeštā (1) — the bow (1)
* qeštā · "For, behold, sinners have drawn the bow" (Psalm 11 Line 6)

ܐܲܬ݂ܩܸܢ̣ܘ   [t-q-n]   {Aphel perf. 3m.pl.}   (search: atqenw)
ʾaṯqen_w (1) — have set (1)
* wʾaṯqen_w · "And have set their arrows upon the string" (Psalm 11 Line 7)

ܓܹܐܪܲ̈ܝܗܘܿܢ   [—]   {noun m.pl.emph. + 3mp suff.}   (search: gerayhon)
gēʾr̈ayhōn (1) — their arrows (1)
* gēʾr̈ayhōn · "And have set their arrows upon the string" (Psalm 11 Line 7)

ܝܲܬ݂ܪܵܐ   [w-t-r]   {noun m.sg.emph.}   (search: yatra)
yaṯrā (1) — the string (1)
* yaṯrā · "And have set their arrows upon the string" (Psalm 11 Line 7)

ܡܸܫܕܵܐ   [š-d-ʾ]   {Peal inf.}   (search: meshda)
mešdā (1) — shoot (1)
* lmešdā · "To shoot in obscurity at the upright of heart" (Psalm 11 Line 8)

ܥܲܡܛܵܢܵܐ   [ʿ-m-ṭ]   {noun m.sg.emph.}   (search: amtana)
ʿamṭānā (1) — obscurity (1)
* bʿamṭānā · "To shoot in obscurity at the upright of heart" (Psalm 11 Line 8)

ܬܪ̈ܝܼܨܲܝ   [t-r-ṣ]   {adj. m.pl.cst.}   (search: trisay)
tr̈īṣay (1) — the upright of (1)
* baṯr̈īṣay · "To shoot in obscurity at the upright of heart" (Psalm 11 Line 8)

ܠܸܒܵܐ   [l-b-b]   {noun m.sg.emph.}   (search: leba)
lebā (3) — heart (1), → blebā waḇlebā (2)
* lebā · "To shoot in obscurity at the upright of heart" (Psalm 11 Line 8)
* blebā · "In doubled hearts they speak" (Psalm 12 Line 8) → blebā waḇlebā
* waḇlebā · "In doubled hearts they speak" (Psalm 12 Line 8) → blebā waḇlebā

ܡܸܕܸܡ   [m-d-m]   {indef. pron.}   (search: medem)
medem (1) — what (1)
* dmedem · "For what You have prepared, they have thrown down" (Psalm 11 Line 9)

ܥܲܬܸ݁ܕܬ݁   [ʿ-t-d]   {Pael perf. 2m.sg.}   (search: atedt)
ʿaṫedṫ (1) — You have prepared (1)
* dʿaṫedṫ · "For what You have prepared, they have thrown down" (Psalm 11 Line 9)

ܣ̣ܚܲܦܘ   [s-ḥ-p]   {Peal perf. 3m.pl.}   (search: shapw)
s_ḥapw (1) — they have thrown down (1)
* s_ḥapw · "For what You have prepared, they have thrown down" (Psalm 11 Line 9)

ܙܲܕܝܼܩܵܐ   [z-d-q]   {referent adj. m.sg.emph.}   (search: zadiqa)
zadīqā (1) — the Righteous One (1)
* zadīqā · "But the Righteous One, what is He doing?" (Psalm 11 Line 10)

ܕܹܝܢ   [d-y-n]   {conj.}   (search: deyn)
dēyn (1) — but (1)
* dēyn · "But the Righteous One, what is He doing?" (Psalm 11 Line 10)

ܡܵܢܵܐ   [m-n]   {interrog. pron.}   (search: mana)
mānā (1) — what (1)
* mānā · "But the Righteous One, what is He doing?" (Psalm 11 Line 10)

ܥܵ̇ܒܹܕ݂   [ʿ-b-d]   {Peal active ptcp. m.sg.abs.}   (search: abed)
ʿ^ābēḏ (1) — is He doing (1)
* ʿ^ābēḏ · "But the Righteous One, what is He doing?" (Psalm 11 Line 10)

ܗܲܝܟ݁ܠܵܐ   [—]   {noun m.sg.emph.}   (search: haykla)
hayk̇lā (1) — Haykla (1)
* bhayk̇lā · "Mar Yah, in the Haykla of His holiness" (Psalm 11 Line 11)

ܩܘܼܕ݂ܫܹܗ   [q-d-š]   {noun m.sg.emph. + 3ms suff.}   (search: qudsheh)
qūḏšēh (1) — His holiness (1)
* dqūḏšēh · "Mar Yah, in the Haykla of His holiness" (Psalm 11 Line 11)

ܟܘܼܪܣܝܹܗ   [—]   {noun m.sg.emph. + 3ms suff.}   (search: kursyeh)
kūrsyēh (1) — His Seat (1)
* kūrsyēh · "Mar Yah, in Heaven, His Seat" (Psalm 11 Line 12)

ܥܲܝܢܵܘ̈ܗܝ   [ʿ-y-n]   {noun f.pl.emph. + 3ms suff.}   (search: aynawhy)
ʿaynāẅhy (1) — His eyes (1)
* ʿaynāẅhy · "His eyes are seeing and His eyelids are examining the sons of men" (Psalm 11 Line 13)

ܚܵܙ̈ܝܵܢ   [ḥ-z-ʾ]   {Peal active ptcp. f.pl.abs.}   (search: hazyan)
ḥāz̈yān (2) — are seeing (1), is seeing (1)
* ḥāz̈yān · "His eyes are seeing and His eyelids are examining the sons of men" (Psalm 11 Line 13)
* ḥāz̈yān · "And His Face is seeing uprightness" (Psalm 11 Line 20)

ܬܸܡܪܵ̈ܘܗܝ   [t-m-r]   {noun m.pl.emph. + 3ms suff.}   (search: temrawhy)
temr̈āwhy (1) — His eyelids (1)
* wtemr̈āwhy · "His eyes are seeing and His eyelids are examining the sons of men" (Psalm 11 Line 13)

ܒܵܚ̇ܪܝܼܢ   [b-ḥ-r]   {Peal active ptcp. m.pl.abs.}   (search: bahrin)
bāḥ^rīn (1) — are examining (1)
* bāḥ^rīn · "His eyes are seeing and His eyelids are examining the sons of men" (Psalm 11 Line 13)

ܒܵܚܲܪ   [b-ḥ-r]   {Peal active ptcp. m.sg.abs.}   (search: bahar)
bāḥar (1) — examines (1)
* bāḥar · "Mar Yah examines the righteous and the unrighteous" (Psalm 11 Line 14)

ܙܲܕܝܼ̈ܩܹܐ   [z-d-q]   {adj. m.pl.emph.}   (search: zadike)
zadī̈qē (1) — the righteous (1)
* lzadī̈qē · "Mar Yah examines the righteous and the unrighteous" (Psalm 11 Line 14)

ܥܵܘܵ̇̈ܠܹܐ   [ʿ-w-l]   {adj. m.pl.emph.}   (search: awale)
ʿāẅ^ālē (1) — the unrighteous (1)
* walʿāẅ^ālē · "Mar Yah examines the righteous and the unrighteous" (Psalm 11 Line 14)

ܪܵ̈ܚ̇ܡܲܝ   [r-ḥ-m]   {noun m.pl.cst.}   (search: rahmay)
r̈āḥ^may (1) — the lovers of (1)
* walr̈āḥ^may · "And the lovers of unrighteousness, His soul has hated" (Psalm 11 Line 15)

ܥܵܘ̣ܠܵܐ   [ʿ-w-l]   {noun m.sg.emph.}   (search: awla)
ʿāw_lā (1) — unrighteousness (1)
* ʿāw_lā · "And the lovers of unrighteousness, His soul has hated" (Psalm 11 Line 15)

ܣܢܵܬ̤   [s-n-ʾ]   {Peal perf. 3f.sg.}   (search: snat)
snāt̤ (1) — has hated (1)
* snāt̤ · "And the lovers of unrighteousness, His soul has hated" (Psalm 11 Line 15)

ܢܲܦ̮ܫܹܗ   [n-p-š]   {noun f.sg.emph. + 3ms suff.}   (search: napsheh)
nap̮šēh (1) — His soul (1)
* nap̮šēh · "And the lovers of unrighteousness, His soul has hated" (Psalm 11 Line 15)

ܢܚܸܬ݂ܘ   [n-ḥ-t]   {Peal perf. 3m.pl.}   (search: nhetw)
nḥeṯw (1) — have come down (1)
* nḥeṯw · "Snares have come down upon the wicked like rain" (Psalm 11 Line 16)

ܪܲ̈ܫܝܼܥܹܐ   [r-š-ʿ]   {adj. m.pl.emph.}   (search: rashie)
r̈ašīʿē (2) — the wicked (2)
* r̈ašīʿē · "Snares have come down upon the wicked like rain" (Psalm 11 Line 16)
* r̈ašīʿē · "wherein the wicked circle about and walk" (Psalm 12 Line 21)

ܦܲܚܹ̈ܐ   [p-ḥ-ḥ]   {noun m.pl.emph.}   (search: pahe)
paḥ̈ē (1) — snares (1)
* paḥ̈ē · "Snares have come down upon the wicked like rain" (Psalm 11 Line 16)

ܡܸܛܪܵܐ   [m-ṭ-r]   {noun m.sg.emph.}   (search: metra)
meṭrā (1) — rain (1)
* meṭrā · "Snares have come down upon the wicked like rain" (Psalm 11 Line 16)

ܢܘܼܪܵܐ   [n-w-r]   {noun f.sg.emph.}   (search: nura)
nūrā (1) — fire (1)
* nūrā · "Fire and brimstone" (Psalm 11 Line 17)

ܟܸܒ݂ܪܝܼܬ݂ܵܐ   [—]   {noun f.sg.emph.}   (search: kebrita)
keḇrīṯā (1) — brimstone (1)
* wkeḇrīṯā · "Fire and brimstone" (Psalm 11 Line 17)

ܡܚܘܿܬ݂ܵܐ   [m-ḥ-ʾ]   {noun f.sg.emph.}   (search: mhota)
mḥōṯā (1) — affliction (1)
* damḥōṯā · "And a ruha of affliction, the portion of their cup" (Psalm 11 Line 18)

ܡܢܵܬ݂ܵܐ   [m-n-ʾ]   {noun f.sg.emph.}   (search: mnata)
mnāṯā (1) — the portion (1)
* mnāṯā · "And a ruha of affliction, the portion of their cup" (Psalm 11 Line 18)

ܟܵܣܗܘܿܢ   [—]   {noun m.sg.emph. + 3mp suff.}   (search: kashon)
kāshōn (1) — their cup (1)
* dḵāshōn · "And a ruha of affliction, the portion of their cup" (Psalm 11 Line 18)

ܙܲܕܝܼܩ   [z-d-q]   {adj. m.sg.abs.}   (search: zadiq)
zadīq (1) — righteous (1)
* dzadīq · "For Mar Yah is righteous, and He loves righteousness" (Psalm 11 Line 19)

ܗ݇ܘ̣   [h-w]   {pron. 3m.sg.}   (search: hw)
(h)w_ (1) — is (1)
* (h)w_ · "For Mar Yah is righteous, and He loves righteousness" (Psalm 11 Line 19)

ܙܲܕܝܼܩܘܼܬ݂ܵܐ   [z-d-q]   {noun f.sg.emph.}   (search: zadiquta)
zadīqūṯā (1) — righteousness (1)
* wzadīqūṯā · "For Mar Yah is righteous, and He loves righteousness" (Psalm 11 Line 19)

ܪܵܚܹ̇ܡ   [r-ḥ-m]   {Peal active ptcp. m.sg.abs.}   (search: rahem)
rāḥ^ēm (1) — He loves (1)
* rāḥ^ēm · "For Mar Yah is righteous, and He loves righteousness" (Psalm 11 Line 19)

ܬܪܝܼܨܘܼܬ݂ܵܐ   [t-r-ṣ]   {noun f.sg.emph.}   (search: trisuta)
trīṣūṯā (1) — uprightness (1)
* waṯrīṣūṯā · "And His Face is seeing uprightness" (Psalm 11 Line 20)

ܐܲܦܵܘ̈ܗܝ   [—]   {noun f.pl.emph. + 3ms suff.}   (search: apawhy)
ʾapāẅhy (1) — His Face (1)
* ʾapāẅhy · "And His Face is seeing uprightness" (Psalm 11 Line 20)

ܦܪܘܿܩ   [p-r-q]   {Peal impv. 2m.sg.}   (search: proq)
prōq (1) — save (1)
* prōq · "Save, Mar Yah, for good has come to an end" (Psalm 12 Line 1)

ܓܡܲܪ   [g-m-r]   {Peal perf. 3m.sg.}   (search: gmar)
gmar (1) — has come to an end (1)
* daḡmar · "Save, Mar Yah, for good has come to an end" (Psalm 12 Line 1)

ܒܸܛܠܲܬ̤   [b-ṭ-l]   {Peal perf. 3f.sg.}   (search: betlat)
beṭlat̤ (1) — has ceased (1)
* wbeṭlat̤ · "And faithfulness has ceased from the earth" (Psalm 12 Line 2)

ܗܲܝܡܵܢܘܼܬ݂ܵܐ   [h-y-m-n]   {noun f.sg.emph.}   (search: haymanuta)
haymānūṯā (1) — faithfulness (1)
* haymānūṯā · "And faithfulness has ceased from the earth" (Psalm 12 Line 2)

ܣܓ݂ܝܼ   [s-g-ʾ]   {Peal perf. 3m.sg.}   (search: sgi)
sḡī (1) — has increased (1)
* sḡī · "Deceit has increased, and love itself has abated..." (Psalm 12 Line 3)

ܢܸܟ݂ܠܵܐ   [n-k-l]   {noun m.sg.emph.}   (search: nekla)
neḵlā (1) — deceit (1)
* neḵlā · "Deceit has increased, and love itself has abated..." (Psalm 12 Line 3)

ܦܵܓ݂   [p-w-g]   {Peal perf. 3m.sg.}   (search: pag)
pāḡ (1) — has abated (1)
* wpāḡ · "Deceit has increased, and love itself has abated..." (Psalm 12 Line 3)

ܚܘܼܒܵܐ   [ḥ-b-b]   {noun m.sg.emph.}   (search: huba)
ḥūbā (1) — love (1)
* ḥūbā · "Deceit has increased, and love itself has abated..." (Psalm 12 Line 3)

ܬܲܗܡܸܐ   [h-m-ʾ]   {Peal impf. 2m.sg.}   (search: tahme)
tahmeʾ (1) — delay (1)
* lā tahmeʾ · "...M'shiha, do not delay" (Psalm 12 Line 3)

ܣܪܝܼܩܘܼܬ݂ܵܐ   [s-r-q]   {noun f.sg.emph.}   (search: sriquta)
srīqūṯā (1) — emptiness (1)
* srīqūṯā · "The sons of men speak emptiness" (Psalm 12 Line 6)

ܡܡܲܠܠܝܼܢ   [m-l-l]   {Pael active ptcp. m.pl.abs.}   (search: mmallin)
mmallīn (3) — speak (3)
* mmallīn · "The sons of men speak emptiness" (Psalm 12 Line 6)
* mmallīn · "In doubled hearts they speak" (Psalm 12 Line 8)
* dammallīn · "And tongues that speak great things" (Psalm 12 Line 10)

ܓܲܒ݂ܪܵܐ   [g-b-r]   {noun m.sg.emph.}   (search: gabra)
gaḇrā (1) — a man (1)
* wgaḇrā · "A man with his fellow in divided lips" (Psalm 12 Line 7)

ܥܲܡ   [ʿ-m-m]   {prep.}   (search: am)
ʿam (1) — with (1)
* ʿam · "A man with his fellow in divided lips" (Psalm 12 Line 7)

ܚܲܒ݂ܪܹܗ   [ḥ-b-r]   {noun m.sg.emph. + 3ms suff.}   (search: habreh)
ḥaḇrēh (1) — his fellow (1)
* ḥaḇrēh · "A man with his fellow in divided lips" (Psalm 12 Line 7)

ܣܸܦ̈ܘܵܬ݂ܵܐ   [s-p-t]   {noun f.pl.emph.}   (search: sepwata)
sep̈wāṯā (3) — lips (3)
* bsep̈wāṯā · "A man with his fellow in divided lips" (Psalm 12 Line 7)
* sep̈wāṯā · "Mar Yah destroys all divided lips" (Psalm 12 Line 9)
* wsep̈wāṯā · "And our lips are our own; who is our Lord?" (Psalm 12 Line 12)

ܡܦܲ̈ܠܓ݂ܵܬ݂ܵܐ   [p-l-g]   {Pael passive ptcp. f.pl.emph.}   (search: mpalgata)
mp̈alḡāṯā (2) — divided (2)
* mp̈alḡāṯā · "A man with his fellow in divided lips" (Psalm 12 Line 7)
* mp̈alḡāṯā · "Mar Yah destroys all divided lips" (Psalm 12 Line 9)

ܢܵܘܒܸ݁ܕ݂   [ʾ-b-d]   {Aphel impf. 3m.sg.}   (search: nawbed)
nāwḃeḏ (1) — destroys (1)
* nāwḃeḏ · "Mar Yah destroys all divided lips" (Psalm 12 Line 9)

ܠܸܫܵܢܹ̈ܐ   [l-š-n]   {noun m.pl.emph.}   (search: leshane)
lešān̈ē (1) — tongues (1)
* wlešān̈ē · "And tongues that speak great things" (Psalm 12 Line 10)

ܪܵܘ݈ܪ̈ܒ݂ܵܬ݂ܵܐ   [r-b-b]   {adj. f.pl.emph.}   (search: rawrbata)
rā(_w)r̈ḇāṯā (1) — great things (1)
* rā(_w)r̈ḇāṯā · "And tongues that speak great things" (Psalm 12 Line 10)

ܐܸܡ᷺ܲܪܘ   [ʾ-m-r]   {Peal perf. 3m.pl.}   (search: emarw)
ʾema__rw (1) — have said (1)
* dʾema__rw · "Who have said: We will magnify our tongue" (Psalm 12 Line 11)

ܠܸܫܵܢܲܢ   [l-š-n]   {noun m.sg.emph. + 1cp suff.}   (search: leshanan)
lešānan (1) — our tongue (1)
* lešānan · "Who have said: We will magnify our tongue" (Psalm 12 Line 11)

ܢܵܘܪܸܒ݂   [r-b-b]   {Aphel impf. 1c.pl.}   (search: nawreb)
nāwreḇ (1) — we will magnify (1)
* nāwreḇ · "Who have said: We will magnify our tongue" (Psalm 12 Line 11)

ܕܝܼܠܲܢ   [d-y-l]   {poss. + 1cp suff.}   (search: dilan)
dīlan (1) — our...our own (1)
* dīlan · "And our lips are our own; who is our Lord?" (Psalm 12 Line 12)

ܐܲܢܹܝܢ   [h-w]   {pron. 3f.pl.}   (search: aneyn)
ʾanēyn (1) — are (1)
* ʾanēyn · "And our lips are our own; who is our Lord?" (Psalm 12 Line 12)

ܡܲܢ̣ܘܼ   [m-n]   {interrog. pron. + 3ms encl.}   (search: manu)
man_ū (1) — who is (1)
* man_ū · "And our lips are our own; who is our Lord?" (Psalm 12 Line 12)

ܒܸܙܬ݂ܵܐ   [b-z-z]   {noun f.sg.emph.}   (search: bezta)
bezṯā (1) — the plundering (1)
* bezṯā · "Because of the plundering of the poor..." (Psalm 12 Line 13)

ܡܸܣܟܹ̈ܢܹܐ   [s-k-n]   {adj. m.pl.emph.}   (search: meskene)
mesk̈ēnē (1) — the poor (1)
* dmesk̈ēnē · "Because of the plundering of the poor..." (Psalm 12 Line 13)

ܐܸܢܲܩܬ݂ܵܐ   [ʾ-n-q]   {noun f.sg.emph.}   (search: enaqta)
ʾenaqṯā (1) — the groaning (1)
* wʾenaqṯā · "...and the groaning of the miserable" (Psalm 12 Line 13)

ܒܵܝ̇̈ܫܹܐ   [b-ʾ-š]   {adj. m.pl.emph.}   (search: bayshe)
bāÿ^šē (1) — the miserable (1)
* dḇāÿ^šē · "...and the groaning of the miserable" (Psalm 12 Line 13)

ܡܸܟܹ݁ܝܠ   [m-k-y-l]   {adv.}   (search: mekeyl)
mek̇ēyl (1) — now (1)
* mek̇ēyl · "Mar Yah has said: I will now arise" (Psalm 12 Line 14)

ܐܹܩܘܼܡ   [q-w-m]   {Peal impf. 1c.sg.}   (search: equm)
ʾēqūm (1) — I will...arise (1)
* ʾēqūm · "Mar Yah has said: I will now arise" (Psalm 12 Line 14)

ܐ᷸ܵܡܲܪ   [ʾ-m-r]   {Peal perf. 3m.sg.}   (search: amar)
ʾā^^mar (1) — has said (1)
* ʾā^^mar · "Mar Yah has said: I will now arise" (Psalm 12 Line 14)

ܐܸܥܒܸ݁ܕ݂   [ʿ-b-d]   {Peal impf. 1c.sg.}   (search: ebed)
ʾeʿḃeḏ (1) — I...bring about (1)
* wʾeʿḃeḏ · "And I openly bring about salvation" (Psalm 12 Line 15)

ܦܘܼܪܩܵܢܵܐ   [p-r-q]   {noun m.sg.emph.}   (search: purqana)
pūrqānā (1) — salvation (1)
* pūrqānā · "And I openly bring about salvation" (Psalm 12 Line 15)

ܓܲܠܝܵܐܝܼܬ   [g-l-ʾ]   {adv.}   (search: galyait)
galyāʾīt (1) — openly (1)
* galyāʾīt · "And I openly bring about salvation" (Psalm 12 Line 15)

ܡܹܐܡܪܹܗ   [ʾ-m-r]   {noun m.sg.emph. + 3ms suff.}   (search: memreh)
mēʾmrēh (1) — the utterance of (1)
* mēʾmrēh · "The utterance of Mar Yah is a pure utterance" (Psalm 12 Line 16)

ܡܹܐܡܪܵܐ   [ʾ-m-r]   {noun m.sg.emph.}   (search: memra)
mēʾmrā (1) — utterance (1)
* mēʾmrā · "The utterance of Mar Yah is a pure utterance" (Psalm 12 Line 16)

ܕܲܟ݂ܝܵܐ   [d-k-ʾ]   {adj. m.sg.emph.}   (search: dakya)
daḵyā (1) — pure (1)
* daḵyā · "The utterance of Mar Yah is a pure utterance" (Psalm 12 Line 16)

ܣܹܐܡܵܐ   [s-ʾ-m]   {noun m.sg.emph.}   (search: sema)
sēʾmā (1) — silver (1)
* sēʾmā · "Choice silver tried in the earth" (Psalm 12 Line 17)

ܓܲܒ݂ܝܵܐ   [g-b-ʾ]   {adj. m.sg.emph.}   (search: gabya)
gaḇyā (1) — choice (1)
* gaḇyā · "Choice silver tried in the earth" (Psalm 12 Line 17)

ܒܚܝܼܪ   [b-ḥ-r]   {adj. m.sg.abs.}   (search: bhir)
bḥīr (1) — tried (1)
* daḇḥīr · "Choice silver tried in the earth" (Psalm 12 Line 17)

ܡܕܲܟܲܝ   [d-k-ʾ]   {Pael passive ptcp. m.sg.abs.}   (search: mdakay)
mdakay (1) — purified (1)
* wamdakay · "And purified seven times" (Psalm 12 Line 18)

ܫܲܒ݂ܥܵܐ   [š-b-ʿ]   {num. m.}   (search: shaba)
šaḇʿā (1) — → ḥaḏ bšaḇʿā (1)
* bšaḇʿā · "And purified seven times" (Psalm 12 Line 18) → ḥaḏ bšaḇʿā

ܐܲܢ݇ܬ   [ʾ-n-t]   {pron. 2m.sg.}   (search: ant)
ʾa(n)t (1) — You (1)
* wʾa(n)t · "And You, Mar Yah, keep them" (Psalm 12 Line 19)

ܬܸܛܲܪ   [n-ṭ-r]   {Peal impf. 2m.sg.}   (search: tetar)
teṭar (1) — keep (1)
* teṭar · "And You, Mar Yah, keep them" (Psalm 12 Line 19)

ܐܸܢܘܿܢ   [h-w]   {pron. 3m.pl.}   (search: enon)
ʾenōn (1) — them (1)
* ʾenōn · "And You, Mar Yah, keep them" (Psalm 12 Line 19)

ܫܵܘܙܸܒܲܝܢܝ   [š-w-z-b]   {Shaphel impv. 2m.sg. + 1cs suff.}   (search: shawzebayny)
šāwzebayny (1) — rescue me (1)
* šāwzebayny · "Rescue me and deliver me unto Eternity from this generation" (Psalm 12 Line 20)

ܦܲܨܵܢܝ   [p-ṣ-ʾ]   {Pael impv. 2m.sg. + 1cs suff.}   (search: pasany)
paṣāny (1) — deliver me (1)
* wpaṣāny · "Rescue me and deliver me unto Eternity from this generation" (Psalm 12 Line 20)

ܕܵܪܵܐ   [d-w-r]   {noun m.sg.emph.}   (search: dara)
dārā (1) — generation (1)
* dārā · "Rescue me and deliver me unto Eternity from this generation" (Psalm 12 Line 20)

ܗܵܢܵܐ   [h-n]   {dem. pron. m.sg.}   (search: hana)
hānā (1) — this (1)
* hānā · "Rescue me and deliver me unto Eternity from this generation" (Psalm 12 Line 20)

ܟܪܝܼܟ݂ܝܼܢ   [k-r-k]   {Peal passive ptcp. m.pl.abs.}   (search: krikin)
krīḵīn (1) — circle about (1)
* daḵrīḵīn · "wherein the wicked circle about and walk" (Psalm 12 Line 21)

ܡܗܲܠܟ݂ܝܼܢ   [h-l-k]   {Pael active ptcp. m.pl.abs.}   (search: mhalkin)
mhalḵīn (1) — walk (1)
* wamhalḵīn · "wherein the wicked circle about and walk" (Psalm 12 Line 21)

ܪܵܘܡܵܐ   [r-w-m]   {noun m.sg.emph.}   (search: rawma)
rāwmā (1) — high place (1)
* rāwmā · "as the contemptible high place of the sons of Edom" (Psalm 12 Line 22)

ܙܲܠܝܼܠܵܐ   [z-l-l]   {adj. m.sg.emph.}   (search: zalila)
zalīlā (1) — contemptible (1)
* zalīlā · "as the contemptible high place of the sons of Edom" (Psalm 12 Line 22)

ܒܢܲܝ̈   [b-r]   {noun m.pl.cst.}   (search: bnay)
bnaÿ (1) — sons of (1)
* daḇnaÿ · "as the contemptible high place of the sons of Edom" (Psalm 12 Line 22)

ܐܲܕ݂ܘܿܡ   [prop. noun]   {prop. n.}   (search: adom)
ʾaḏōm (1) — Edom (1)
* ʾaḏōm · "as the contemptible high place of the sons of Edom" (Psalm 12 Line 22)
