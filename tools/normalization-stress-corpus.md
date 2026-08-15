# Synthetic normalization stress corpus

These are deliberately **imaginary pseudo-words**, not lexical Syriac. Their only purpose is to force the normalization and page-state audit machinery through combinations that ordinary texts may never supply. The rendered form is convenient for human inspection; the codepoint recipe is authoritative because fonts may conceal the distinctions being tested.

The corpus has two classes:

- **clean cases** — bizarre but mechanically interpretable states that must normalize deterministically and pass the page-state audit;
- **review cases** — states that must remain visible as flags/issues and must prevent a persistent write.

As new source material reveals a strange encoding or page-state, add a minimal synthetic case here and a regression test in `tests/test_normalization_stress.py`.

## A. Carrier-sensitive single points

1. **Bgdkpt aliases** — pseudo-word `ܒ̇ܕ݂ܓ݁ܬ̣`
   - recipe: `BETH+U+0307 DALATH+U+073C GAMAL+U+0741 TAW+U+0323`
   - expected: all four single points re-encode by carrier as canonical qūššāyā/rūkkākā.

2. **Non-bgdkpt aliases** — pseudo-word `ܡ݁ܢ݂`
   - recipe: `MIM+U+0741 NUN+U+0742`
   - expected: generic single point above/below (`U+0307`, `U+0323`).

3. **Waw/yodh ambiguity forced by carrier**
   - recipe: `WAW+U+0307 WAW+U+0323 YODH+U+0742 YODH+U+073F`
   - expected: `ō`, `ū`, `ī`, then generic point above respectively.

## B. Positional and alias normalization

4. **Final semkath in mid-token**
   - recipe: `MIM U+0724 ALAPH`
   - expected: U+0724 → ordinary semkath U+0723 regardless of position in this synthetic input.

5. **All two-dots-below encodings together**
   - recipe: `TAW+U+0740 MIM+U+0744 NUN+U+0324`
   - expected: all three → U+0324.

6. **U+0716 with intervening vowel and syāmē**
   - recipe: `E YODH+U+073C U+0716+U+0739+U+0308 ALAPH`
   - expected: U+0716 → resh, no flag because syāmē is present even with the vowel between base and syāmē.

7. **Between-letter point above**
   - recipe: `QAPH+U+1DF8 E`
   - expected: retained as the distinct between-letter-above state.

8. **Between-letter point below**
   - recipe: `MIM+U+1DFA NUN`
   - expected: retained as the distinct between-letter-below state.

## C. Combining-order torture cases

9. **CCC 230 in reverse project order**
   - recipe on one mim: `occultans-above, syāmē, single-point-above, zqāpā`
   - expected canonical order: `zqāpā, single point, syāmē, occultans`.

10. **CCC 220 in reverse project order**
    - recipe on one mim: `occultans-below, breve-below, two-dots-below, single-point-below, zlāmā-pšīqā`
    - expected canonical order: `vowel, single point, two dots, breve, occultans`.

11. **Superscript alaph mixed with below and above marks**
    - recipe on one mim: `occultans-above, U+0711, single-point-below, zqāpā`
    - expected: CCC 36 superscript alaph first, then CCC 220, then ordered CCC 230.

12. **Dense legal above stack on beth**
    - recipe: `BETH + zqāpā + qūššāyā + syāmē + occultans-above`, supplied in reverse order.
    - expected: all four states preserved and ordered; no review issue.

13. **Dense legal below stack on pe**
    - recipe: `PE + zlāmā-pšīqā + rūkkākā + two-dots-below + breve-below + occultans-below`, supplied in reverse order.
    - expected: all five states preserved and ordered; no review issue.

14. **Marks both above and below one non-bgdkpt letter**
    - recipe: `MIM + zqāpā + single-point-below + syāmē`.
    - expected: all states remain distinct; different CCCs sort mechanically.

## D. Dense but valid vowel/carrier combinations

15. **Waw carrying rwāḥā plus syāmē**
    - recipe: `WAW+U+073F+U+0308`.
    - expected report: `Waw (rwāḥā: ō; syāmē)`.

16. **Yodh carrying ḥḇāṣā plus syāmē**
    - recipe: `YODH+U+073C+U+0308`.
    - expected report: `Yodh (ḥḇāṣā: ī; syāmē)`.

17. **Bgdkpt with vowel plus qūššāyā**
    - recipe: `DALATH + pṯāḥā + qūššāyā`.
    - expected: legal; a vowel and a bgdkpt state are different classes of information.

18. **Bgdkpt with vowel plus rūkkākā**
    - recipe: `TAW + zlāmā-pšīqā + rūkkākā`.
    - expected: legal.

## E. Out-of-scope noise

19. **Pseudo-word broken by typesetting debris**
    - recipe: `MIM TATWEEL RISH ZWJ YODH SYRIAC-MUSIC ':' ALAPH`.
    - expected normalized token: plain `MIM RISH YODH ALAPH`; all licensed debris silently removed.

20. **Punctuation inside an English editorial label**
    - recipe: `(Witness A:) [SYRIAC...]`.
    - expected: punctuation in the parenthesized label survives; punctuation inside active Syriac is removed.

## F. Mandatory source-review cases

21. **Bare U+0716**
    - recipe: `MIM U+0716 ALAPH`.
    - expected: normalize U+0716 to resh **and flag** `bare-u0716`; persistent write prohibited.

22. **Any West Syriac vowel**
    - recipe: one pseudo-word for each of U+0730, 0731, 0733, 0734, 0736, 0737, 073A, 073B, 073D, 073E.
    - expected: each sign remains unmapped and raises `west-syriac-vowel`.

23. **Unknown Syriac combining mark**
    - recipe: `MIM+U+0745 ALAPH`.
    - expected: mark retained, `unrecognized-combining-mark` flag.

24. **Orphan syāmē**
    - recipe: `U+0308 MIM ALAPH`.
    - expected: `orphan-combining-mark` flag.

25. **Two source encodings for the same single point above on one beth**
    - recipe: `BETH+U+0307+U+0741 ALAPH`.
    - expected: both collapse to qūššāyā; normalization flags duplicate input and the post-normalization audit also sees a duplicated mark.

26. **Two source encodings for the same single point below on one dalath**
    - recipe: `DALATH+U+0323+U+0742 ALAPH`.
    - expected: duplicate-input flag plus duplicate normalized mark issue.

## G. Syntactically normalized but implausible page-states

These are especially important. Unicode normalization alone cannot reject them; the **post-normalization page-state audit** must.

27. **Beth simultaneously hard and soft**
    - recipe: `BETH+qūššāyā+rūkkākā ALAPH`.
    - expected issue: `conflicting-bgdkpt-state`; persistent write prohibited.

28. **Two ordinary East Syriac vowels on one mim**
    - recipe: `MIM+pṯāḥā+zqāpā ALAPH`.
    - expected issue: `multiple-vowels-on-carrier`.

29. **Waw simultaneously carrying ō and ū**
    - recipe: `WAW+U+073F+U+073C ALAPH`.
    - expected issue: `multiple-vowels-on-carrier`.

30. **Duplicate syāmē on one mim**
    - recipe: `MIM+U+0308+U+0308 ALAPH`.
    - expected issue: `duplicate-normalized-mark`.

31. **Injected normalized qūššāyā on a non-bgdkpt carrier**
    - recipe for audit-layer invariant test: `MIM+U+0741`.
    - expected issue: `qūššāyā-invalid-carrier`.

32. **Injected carrier-vowel codepoint on the wrong carrier**
    - recipe for audit-layer invariant test: `MIM+U+073C`.
    - expected issue: `carrier-vowel-invalid-carrier`.

The final two are not expected outputs from `normalize_text()`; they directly test the invariant checker so that later code cannot accidentally construct an invalid normalized string behind the normalizer's back.
