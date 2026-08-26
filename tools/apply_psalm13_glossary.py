from pathlib import Path
import unicodedata

PATH = Path("glossary/Glossary.md")
text = PATH.read_text(encoding="utf-8")
blocks = text.rstrip("\n").split("\n\n")


def replace_entry(headword: str, morphology: str, new_block: str) -> None:
    matches = [
        i
        for i, block in enumerate(blocks)
        if block.startswith(headword + "   ")
        and ("{" + morphology + "}") in block.splitlines()[0]
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one entry for {headword!r} {{{morphology}}}, found {len(matches)}"
        )
    blocks[matches[0]] = new_block.strip()


def find_block_start(headword: str) -> int:
    matches = [i for i, block in enumerate(blocks) if block.startswith(headword + "   ")]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one block for {headword!r}, found {len(matches)}")
    return matches[0]


# Non-compositional interrogative phrase.
phrase = """ܥܕܲܡܵܐ ܠܐܸܡܲܬ݂ܝ   [ʿ-d-m + ʾ-m-t-y]   {interrog. phrase}   (search: dama lematy)
ʿdamā lʾemaṯy (4) — how long (4)
* ʿdamā lʾemaṯy · \"How long, Mar Yah? Will You forget me for Eternity?\" (Psalm 13 Line 1)
* ʿdamā lʾemaṯy · \"How long will You turn Your Face from me?\" (Psalm 13 Line 2)
* ʿdamā lʾemaṯy · \"How long will You place sorrow in my soul?\" (Psalm 13 Line 6)
* ʿdamā lʾemaṯy · \"How long will my enemy be exalted over me?\" (Psalm 13 Line 8)"""
phrase_anchor = find_block_start("ܚܲܕ݂ ܒܫܲܒ݂ܥܵܐ")
blocks.insert(phrase_anchor + 1, phrase)

# Existing form entries updated by Psalm 13.
replace_entry(
    "ܥܕܲܡܵܐ",
    "prep.",
    """ܥܕܲܡܵܐ   [ʿ-d-m]   {prep.}   (search: dama)
ʿdamā (5) — unto (1), → ʿdamā lʾemaṯy (4)
* waʿdamā · \"From Eternity and unto Eternity, amen amen\" (Our Father Line 16)
* ʿdamā · \"How long, Mar Yah? Will You forget me for Eternity?\" (Psalm 13 Line 1) → ʿdamā lʾemaṯy
* ʿdamā · \"How long will You turn Your Face from me?\" (Psalm 13 Line 2) → ʿdamā lʾemaṯy
* ʿdamā · \"How long will You place sorrow in my soul?\" (Psalm 13 Line 6) → ʿdamā lʾemaṯy
* ʿdamā · \"How long will my enemy be exalted over me?\" (Psalm 13 Line 8) → ʿdamā lʾemaṯy""",
)

replace_entry(
    "ܡܵܪܝܵܐ",
    "noun m.sg.emph.",
    """ܡܵܪܝܵܐ   [m-r-ʾ]   {noun m.sg.emph.}   (search: marya)
māryā (16) — Mar Yah (16)
* māryā · \"And to One Mar Yah...\" (Creed Line 3)
* bmāryā · \"In Mar Yah I have hoped...\" (Psalm 11 Line 1)
* māryā · \"...in You, Mar Yah, I have hoped\" (Psalm 11 Line 3)
* māryā · \"Mar Yah, in the Haykla of His holiness\" (Psalm 11 Line 11)
* māryā · \"Mar Yah, in Heaven, His Seat\" (Psalm 11 Line 12)
* māryā · \"Mar Yah is examining the righteous and the unrighteous\" (Psalm 11 Line 14)
* māryā · \"For Mar Yah is righteous, and He loves righteousness\" (Psalm 11 Line 19)
* māryā · \"Save, Mar Yah, for good has come to an end\" (Psalm 12 Line 1)
* māryā · \"Mar Yah destroys all divided lips\" (Psalm 12 Line 9)
* māryā · \"Mar Yah has said: I will now arise\" (Psalm 12 Line 14)
* dmāryā · \"The utterance of Mar Yah is a pure utterance\" (Psalm 12 Line 16)
* māryā · \"And You, Mar Yah, keep them\" (Psalm 12 Line 19)
* māryā · \"How long, Mar Yah? Will You forget me for Eternity?\" (Psalm 13 Line 1)
* māryā · \"Be reconciled to me and save me; that I may confess unto You, Mar Yah\" (Psalm 13 Line 3)
* māryā · \"Look and answer me, Mar Yah my God\" (Psalm 13 Line 9)
* lmāryā · \"And I glorify Mar Yah, who has saved me\" (Psalm 13 Line 15)""",
)

replace_entry(
    "ܥܵܠܲܡ",
    "noun m.sg.abs.",
    """ܥܵܠܲܡ   [ʿ-l-m]   {noun m.sg.abs.}   (search: alam)
ʿālam (4) — Eternity (4)
* ʿālam · \"From Eternity and unto Eternity, amen amen\" (Our Father Line 16)
* lʿālam · \"From Eternity and unto Eternity, amen amen\" (Our Father Line 16)
* lʿālam · \"Rescue me and deliver me for Eternity from this generation\" (Psalm 12 Line 20)
* lʿālam · \"How long, Mar Yah? Will You forget me for Eternity?\" (Psalm 13 Line 1)""",
)

replace_entry(
    "ܠܵܟ݂",
    "prep. + 2ms suff.",
    """ܠܵܟ݂   [l]   {prep. + 2ms suff.}   (search: lak)
lāḵ (4) — to You (2), You (1), unto You (1)
* lāḵ · \"Watchers and men cry out to You...\" (Our Father Line 6)
* lāḵ · \"Early they come to You, my Lord\" (Ferial Slotha d'Sapra II, Line 1)
* lāḵ · \"Who call and beseech You\" (Slotha d'Marmitha 4, Line 6)
* lāḵ · \"Be reconciled to me and save me; that I may confess unto You, Mar Yah\" (Psalm 13 Line 3)""",
)

replace_entry(
    "ܠܝܼ",
    "prep. + 1cs suff.",
    """ܠܝܼ   [l]   {prep. + 1cs suff.}   (search: li)
lī (3) — against me (1), to me (1), over me (1)
* lī · \"Sinners have schemed against me...\" (Psalm 11 Line 3)
* lī · \"Be reconciled to me and save me; that I may confess unto You, Mar Yah\" (Psalm 13 Line 3)
* lī · \"Nor my oppressors rejoice over me when I tremble\" (Psalm 13 Line 12)""",
)

replace_entry(
    "ܢܲܦ̮ܫܝ",
    "noun f.sg.emph. + 1cs suff.",
    """ܢܲܦ̮ܫܝ   [n-p-š]   {noun f.sg.emph. + 1cs suff.}   (search: napshy)
nap̮šy (2) — my soul (2)
* lnap̮šy · \"...how are you saying to my soul:\" (Psalm 11 Line 1)
* bnap̮šy · \"How long will You place sorrow in my soul?\" (Psalm 13 Line 6)""",
)

replace_entry(
    "ܕܹܝܢ",
    "conj.",
    """ܕܹܝܢ   [d-y-n]   {conj.}   (search: deyn)
dēyn (2) — but (1), nevertheless (1)
* dēyn · \"But the Righteous One, what is He doing?\" (Psalm 11 Line 10)
* dēyn · \"Nevertheless, I have trusted in Your grace\" (Psalm 13 Line 13)""",
)

replace_entry(
    "ܥܲܠ",
    "prep.",
    """ܥܲܠ   [ʿ-l]   {prep.}   (search: al)
ʿal (5) — on (1), upon (3), in (1)
* wʿal · \"And on earth, peace and good hope to the sons of men\" (Teshbhotha l'Alaha Line 2)
* ʿal · \"Wander and dwell upon the mountains like a bird\" (Psalm 11 Line 2)
* ʿal · \"And have set their arrows upon the string\" (Psalm 11 Line 7)
* ʿal · \"Snares have come down upon the wicked like rain\" (Psalm 11 Line 16)
* ʿal · \"Nevertheless, I have trusted in Your grace\" (Psalm 13 Line 13)""",
)

replace_entry(
    "ܛܲܝܒ݁ܘܼܬ݂ܵܟ݂",
    "noun f.sg.emph. + 2ms suff.",
    """ܛܲܝܒ݁ܘܼܬ݂ܵܟ݂   [ṭ-w-b]   {noun f.sg.emph. + 2ms suff.}   (search: taybutak)
ṭayḃūṯāḵ (2) — Your grace (2)
* wṭayḃūṯāḵ · \"Let Your grace absolve our sins\" (Slotha d'Marmitha 4, Line 3)
* ṭayḃūṯāḵ · \"Nevertheless, I have trusted in Your grace\" (Psalm 13 Line 13)""",
)

# Root correction established while studying Psalm 13; the existing Psalm 11 form is the same face lexeme.
replace_entry(
    "ܐܲܦܵܘ̈ܗܝ",
    "noun f.pl.emph. + 3ms suff.",
    """ܐܲܦܵܘ̈ܗܝ   [ʾ-p-ʾ]   {noun f.pl.emph. + 3ms suff.}   (search: apawhy)
ʾapāẅhy (1) — His Face (1)
* ʾapāẅhy · \"And His Face is seeing uprightness\" (Psalm 11 Line 20)""",
)

# New component entry for the interrogative phrase.
new_entries = [
    """ܐܸܡܲܬ݂ܝ   [ʾ-m-t-y]   {interrog. adv.}   (search: ematy)
ʾemaṯy (4) — → ʿdamā lʾemaṯy (4)
* lʾemaṯy · \"How long, Mar Yah? Will You forget me for Eternity?\" (Psalm 13 Line 1) → ʿdamā lʾemaṯy
* lʾemaṯy · \"How long will You turn Your Face from me?\" (Psalm 13 Line 2) → ʿdamā lʾemaṯy
* lʾemaṯy · \"How long will You place sorrow in my soul?\" (Psalm 13 Line 6) → ʿdamā lʾemaṯy
* lʾemaṯy · \"How long will my enemy be exalted over me?\" (Psalm 13 Line 8) → ʿdamā lʾemaṯy""",
    """ܬܸܛܥܹܝܢܝ   [ṭ-ʿ-ʾ]   {Peal impf. 2m.sg. + 1cs suff.}   (search: teteyny)
teṭʿēyny (1) — will You forget me (1)
* teṭʿēyny · \"How long, Mar Yah? Will You forget me for Eternity?\" (Psalm 13 Line 1)""",
    """ܬܲܗܦܸܟ݂   [h-p-k]   {Peal impf. 2m.sg.}   (search: tahpek)
tahpeḵ (1) — will You turn (1)
* tahpeḵ · \"How long will You turn Your Face from me?\" (Psalm 13 Line 2)""",
    """ܐܲܦܲܝ̈ܟ   [ʾ-p-ʾ]   {noun f.pl.emph. + 2ms suff.}   (search: apayk)
ʾapaÿk (1) — Your Face (1)
* ʾapaÿk · \"How long will You turn Your Face from me?\" (Psalm 13 Line 2)""",
    """ܡܹܢܝ   [m-n]   {prep. + 1cs suff.}   (search: meny)
mēny (1) — from me (1)
* mēny · \"How long will You turn Your Face from me?\" (Psalm 13 Line 2)""",
    """ܐܸܬ݂ܪܲܥܵܐ   [r-ʿ-ʾ]   {Ethpaal impv. 2m.sg.}   (search: etraa)
ʾeṯraʿā (1) — be reconciled (1)
* ʾeṯraʿā · \"Be reconciled to me and save me; that I may confess unto You, Mar Yah\" (Psalm 13 Line 3)""",
    """ܦܪܘܿܩܲܝܢܝ   [p-r-q]   {Peal impv. 2m.sg. + 1cs suff.}   (search: proqayny)
prōqayny (1) — save me (1)
* waprōqayny · \"Be reconciled to me and save me; that I may confess unto You, Mar Yah\" (Psalm 13 Line 3)""",
    """ܐܵܘܕܸܐ   [y-d-ʾ]   {Aphel impf. 1c.sg.}   (search: awde)
ʾāwdeʾ (1) — I may confess (1)
* dʾāwdeʾ · \"Be reconciled to me and save me; that I may confess unto You, Mar Yah\" (Psalm 13 Line 3)""",
    """ܬܣܝܼܡ   [s-w-m]   {Peal impf. 2m.sg.}   (search: tsim)
tsīm (1) — will You place (1)
* tsīm · \"How long will You place sorrow in my soul?\" (Psalm 13 Line 6)""".replace("tsīm", "tsīm"),
    """ܬܲܟ݂ܪܝܼܬ݂ܵܐ   [k-r-ʾ]   {noun f.sg.emph.}   (search: takrita)
taḵrīṯā (1) — sorrow (1)
* taḵrīṯā · \"How long will You place sorrow in my soul?\" (Psalm 13 Line 6)""",
    """ܕܵܘܘܿܢܵܐ   [d-w-y]   {noun m.sg.emph.}   (search: dawona)
dāwōnā (1) — misery (1)
* wḏāwōnā · \"And misery in my heart every day?\" (Psalm 13 Line 7)""",
    """ܠܹܒ݁ܝ   [l-b-b]   {noun m.sg.emph. + 1cs suff.}   (search: leby)
lēḃy (2) — my heart (2)
* blēḃy · \"And misery in my heart every day?\" (Psalm 13 Line 7)
* lēḃy · \"My heart exults in Your salvation\" (Psalm 13 Line 14)""",
    """ܟܠܝܘܿܡ   [k-l + y-w-m]   {quant. + noun m.sg.abs.}   (search: klyom)
klyōm (1) — every day (1)
* klyōm · \"And misery in my heart every day?\" (Psalm 13 Line 7)""",
    """ܢܸܬ݁ܬ݁ܪܝܼܡ   [r-w-m]   {Ettaphal impf. 3m.sg.}   (search: nettrim)
neṫṫrīm (1) — will...be exalted (1)
* neṫṫrīm · \"How long will my enemy be exalted over me?\" (Psalm 13 Line 8)""",
    """ܒܥܸܠܕܒ݂ܵܒ݂ܝ   [b-ʿ-l + d-b-b]   {noun m.sg.emph. + 1cs suff.}   (search: beldbaby)
bʿeldḇāḇy (2) — my enemy (2)
* bʿeldḇāḇy · \"How long will my enemy be exalted over me?\" (Psalm 13 Line 8)
* bʿeldḇāḇy · \"And that my enemy may not say: I have conquered him\" (Psalm 13 Line 11)""",
    """ܥܠܲܝ   [ʿ-l]   {prep. + 1cs suff.}   (search: lay)
ʿlay (1) — over me (1)
* ʿlay · \"How long will my enemy be exalted over me?\" (Psalm 13 Line 8)""",
    """ܚܘܼܪ   [ḥ-w-r]   {Peal impv. 2m.sg.}   (search: hur)
ḥūr (1) — look (1)
* ḥūr · \"Look and answer me, Mar Yah my God\" (Psalm 13 Line 9)""",
    """ܥܢܝܼܢܝ   [ʿ-n-ʾ]   {Peal impv. 2m.sg. + 1cs suff.}   (search: niny)
ʿnīny (1) — answer me (1)
* waʿnīny · \"Look and answer me, Mar Yah my God\" (Psalm 13 Line 9)""",
    """ܐܲܠܵܗܝ   [ʾ-l-h]   {noun m.sg.emph. + 1cs suff.}   (search: alahy)
ʾalāhy (1) — my God (1)
* ʾalāhy · \"Look and answer me, Mar Yah my God\" (Psalm 13 Line 9)""",
    """ܐܲܢܗܲܪ   [n-h-r]   {Aphel impv. 2m.sg.}   (search: anhar)
ʾanhar (1) — enlighten (1)
* wʾanhar · \"And enlighten my eyes, that I may not sleep unto death\" (Psalm 13 Line 10)""",
    """ܥܲܝ̈ܢܝܼ   [ʿ-y-n]   {noun f.pl.emph. + 1cs suff.}   (search: ayni)
ʿaÿnī (1) — my eyes (1)
* ʿaÿnī · \"And enlighten my eyes, that I may not sleep unto death\" (Psalm 13 Line 10)""",
    """ܐܸܕ݂ܡܲܟ݂   [d-m-k]   {Peal impf. 1c.sg.}   (search: edmak)
ʾeḏmaḵ (1) — I may...sleep (1)
* dlā ʾeḏmaḵ · \"And enlighten my eyes, that I may not sleep unto death\" (Psalm 13 Line 10)""",
    """ܡܵܘܬܵܐ   [m-w-t]   {noun m.sg.emph.}   (search: mawta)
māwtā (1) — death (1)
* lmāwtā · \"And enlighten my eyes, that I may not sleep unto death\" (Psalm 13 Line 10)""",
    """ܢܹܐܡܲܪ   [ʾ-m-r]   {Peal impf. 3m.sg.}   (search: nemar)
nēʾmar (1) — may...say (1)
* wlā nēʾmar · \"And that my enemy may not say: I have conquered him\" (Psalm 13 Line 11)""",
    """ܙܟܹܝ̇ܬܹܗ   [z-k-ʾ]   {Peal perf. 1c.sg. + 3ms suff.}   (search: zkeyteh)
zkēy^tēh (1) — I have conquered him (1)
* dazkēy^tēh · \"And that my enemy may not say: I have conquered him\" (Psalm 13 Line 11)""",
    """ܐܵ̇ܠܘܿܨܲܝ̈   [ʾ-l-ṣ]   {noun m.pl.emph. + 1cs suff.}   (search: alosay)
ʾ^ālōṣaÿ (1) — my oppressors (1)
* wʾ^ālōṣaÿ · \"Nor my oppressors rejoice over me when I tremble\" (Psalm 13 Line 12)""",
    """ܢܸܚܕܘܿܢ   [ḥ-d-y]   {Peal impf. 3m.pl.}   (search: nehdon)
neḥdōn (1) — rejoice (1)
* neḥdōn · \"Nor my oppressors rejoice over me when I tremble\" (Psalm 13 Line 12)""",
    """ܟܲܕ݂   [k-d]   {conj.}   (search: kad)
kaḏ (1) — when (1)
* kaḏ · \"Nor my oppressors rejoice over me when I tremble\" (Psalm 13 Line 12)""",
    """ܐܹܙܘܼܥ   [z-w-ʿ]   {Peal impf. 1c.sg.}   (search: ezu)
ʾēzūʿ (1) — I tremble (1)
* ʾēzūʿ · \"Nor my oppressors rejoice over me when I tremble\" (Psalm 13 Line 12)""",
    """ܐܸܢܵܐ   [ʾ-n-ʾ]   {pron. 1c.sg.}   (search: ena)
ʾenā (1) — I (1)
* ʾenā · \"Nevertheless, I have trusted in Your grace\" (Psalm 13 Line 13)""",
    """ܐܸܬ݁ܬܲܟ݂ܠܹ̇ܬ݂   [t-k-l]   {Ethpaal perf. 1c.sg.}   (search: ettaklet)
ʾeṫtaḵl^ēṯ (1) — I have trusted (1)
* ʾeṫtaḵl^ēṯ · \"Nevertheless, I have trusted in Your grace\" (Psalm 13 Line 13)""",
    """ܢܸܪܘܲܙ   [r-w-z]   {Peal impf. 3m.sg.}   (search: nerwaz)
nerwaz (1) — exults (1)
* nerwaz · \"My heart exults in Your salvation\" (Psalm 13 Line 14)""",
    """ܦܘܼܪܩܵܢܵܟ݂   [p-r-q]   {noun m.sg.emph. + 2ms suff.}   (search: purqanak)
pūrqānāḵ (1) — Your salvation (1)
* bpūrqānāḵ · \"My heart exults in Your salvation\" (Psalm 13 Line 14)""",
    """ܐܹܫܲܒܲܚ   [š-b-ḥ]   {Pael impf. 1c.sg.}   (search: eshabah)
ʾēšabaḥ (1) — I glorify (1)
* wʾēšabaḥ · \"And I glorify Mar Yah, who has saved me\" (Psalm 13 Line 15)""",
    """ܦܲܪܩܲܢܝ   [p-r-q]   {Peal perf. 3m.sg. + 1cs suff.}   (search: parqany)
parqany (1) — has saved me (1)
* dparqany · \"And I glorify Mar Yah, who has saved me\" (Psalm 13 Line 15)""",
]

# Do not create an entry for lā: General Rules §10.2 treats it exactly as a proclitic.
blocks.extend(entry.strip() for entry in new_entries)

new_text = "\n\n".join(blocks) + "\n"
new_text = unicodedata.normalize("NFC", new_text)
PATH.write_text(new_text, encoding="utf-8", newline="\n")
