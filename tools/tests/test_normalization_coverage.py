from __future__ import annotations

import sys
from pathlib import Path
import unittest
import unicodedata

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.inspection import inspect_normalized_text
from east_syriac.normalization import (
    ACCENT_CANTILLATION,
    BGDKPT,
    BETWEEN_ABOVE,
    BETWEEN_BELOW,
    BREVE_BELOW,
    EAST_MULTI_DOT_VOWELS,
    FINAL_SEMKATH,
    GENERIC_DOT_ABOVE,
    GENERIC_DOT_BELOW,
    HBASA_ESASA_DOTTED,
    LATIN_PUNCTUATION_SUBSTITUTES,
    OCCULTANS_ABOVE,
    OCCULTANS_BELOW,
    PRESENTATIONAL,
    PROJECT_LETTERS,
    QUSSHAYA,
    RISH,
    RUKKAKHA,
    RWAHA,
    SEMKATH,
    SINGLE_ABOVE_INPUTS,
    SINGLE_BELOW_INPUTS,
    SUPERSCRIPT_ALAPH,
    SYAME,
    SYRIAC_ABBREVIATION_MARK,
    SYRIAC_PUNCTUATION,
    TWO_DOTS_BELOW,
    TWO_DOTS_BELOW_INPUTS,
    WAW,
    WEST_SYRIAC_VOWELS,
    YODH,
    normalize_text,
)

MIM = "\u0721"
NUN = "\u0722"
BETH = "\u0712"
DOTLESS_DALATH_RISH = "\u0716"


class ExhaustiveNormalizationCoverageTests(unittest.TestCase):
    def test_every_assigned_core_syriac_codepoint_is_classified(self):
        unsupported_letters = {
            0x0714, 0x071C, 0x071E, 0x0727, 0x072D, 0x072E, 0x072F,
            0x074D, 0x074E, 0x074F,
        }
        handled = (
            set(range(0x0700, 0x070E))
            | {0x070F}
            | {ord(ch) for ch in PROJECT_LETTERS}
            | {ord(SUPERSCRIPT_ALAPH)}
            | {ord(ch) for ch in EAST_MULTI_DOT_VOWELS}
            | {ord(HBASA_ESASA_DOTTED), ord(RWAHA)}
            | {ord(ch) for ch in WEST_SYRIAC_VOWELS}
            | {0x0740, 0x0741, 0x0742, 0x0743, 0x0744, 0x0745, 0x0746, 0x0747, 0x0748, 0x0749, 0x074A}
            | unsupported_letters
        )
        assigned = {cp for cp in range(0x0700, 0x0750) if unicodedata.name(chr(cp), "")}
        self.assertEqual(assigned, handled)

    def test_canonical_consonant_inventory_passes(self):
        canonical = "".join(chr(cp) for cp in (
            0x0710, 0x0712, 0x0713, 0x0715, 0x0717, 0x0718, 0x0719,
            0x071A, 0x071B, 0x071D, 0x071F, 0x0720, 0x0721, 0x0722,
            0x0723, 0x0725, 0x0726, 0x0728, 0x0729, 0x072A, 0x072B, 0x072C,
        ))
        result = normalize_text(canonical)
        self.assertEqual(result.text, canonical)
        self.assertFalse(result.flags)

    def test_all_bgdkpt_letters_take_hard_soft_and_unmarked_states(self):
        for base in BGDKPT:
            with self.subTest(base=base, state="unmarked"):
                self.assertEqual(normalize_text(base).text, base)
            with self.subTest(base=base, state="hard"):
                result = normalize_text(base + "\u0307")
                self.assertEqual(result.text, base + QUSSHAYA)
                self.assertFalse(result.flags)
            with self.subTest(base=base, state="soft"):
                result = normalize_text(base + "\u0323")
                self.assertEqual(result.text, base + RUKKAKHA)
                self.assertFalse(result.flags)

    def test_every_single_point_alias_on_every_carrier_class(self):
        above_expected = {BETH: QUSSHAYA, WAW: RWAHA, YODH: GENERIC_DOT_ABOVE, MIM: GENERIC_DOT_ABOVE}
        below_expected = {BETH: RUKKAKHA, WAW: HBASA_ESASA_DOTTED, YODH: HBASA_ESASA_DOTTED, MIM: GENERIC_DOT_BELOW}
        for alias in SINGLE_ABOVE_INPUTS:
            for carrier, expected in above_expected.items():
                with self.subTest(direction="above", alias=ord(alias), carrier=carrier):
                    result = normalize_text(carrier + alias)
                    self.assertEqual(result.text, carrier + expected)
                    self.assertFalse(result.flags)
        for alias in SINGLE_BELOW_INPUTS:
            for carrier, expected in below_expected.items():
                with self.subTest(direction="below", alias=ord(alias), carrier=carrier):
                    result = normalize_text(carrier + alias)
                    self.assertEqual(result.text, carrier + expected)
                    self.assertFalse(result.flags)

    def test_every_east_vowel_and_special_mark_has_a_legal_case(self):
        cases = [
            MIM + "\u0732", MIM + "\u0735", MIM + "\u0738", MIM + "\u0739",
            WAW + "\u073f", WAW + "\u073c", YODH + "\u073c",
            MIM + SYAME, MIM + BREVE_BELOW,
            MIM + BETWEEN_ABOVE + NUN,
            MIM + BETWEEN_BELOW + NUN,
            MIM + OCCULTANS_ABOVE, MIM + OCCULTANS_BELOW,
            MIM + SUPERSCRIPT_ALAPH,
        ]
        for source in cases:
            with self.subTest(source=source):
                result = normalize_text(source)
                self.assertFalse(result.flags)
                self.assertFalse(inspect_normalized_text(result.text).issues)

    def test_all_two_dots_below_aliases_have_one_output(self):
        for alias in TWO_DOTS_BELOW_INPUTS:
            with self.subTest(alias=ord(alias)):
                result = normalize_text(MIM + alias)
                self.assertEqual(result.text, MIM + TWO_DOTS_BELOW)
                self.assertFalse(result.flags)

    def test_ingestion_only_letters_have_defined_outcomes(self):
        final = normalize_text(FINAL_SEMKATH)
        self.assertEqual(final.text, SEMKATH)
        self.assertFalse(final.flags)
        resh = normalize_text(DOTLESS_DALATH_RISH + "\u0739" + SYAME)
        self.assertEqual(resh.text[0], RISH)
        self.assertFalse(resh.flags)
        bare = normalize_text(DOTLESS_DALATH_RISH)
        self.assertEqual(bare.text, RISH)
        self.assertIn("bare-u0716", [flag.code for flag in bare.flags])

    def test_all_explicitly_out_of_scope_inputs_are_removed(self):
        debris = set(SYRIAC_PUNCTUATION) | {SYRIAC_ABBREVIATION_MARK} | set(PRESENTATIONAL) | set(ACCENT_CANTILLATION) | set(LATIN_PUNCTUATION_SUBSTITUTES)
        for char in debris:
            with self.subTest(codepoint=f"U+{ord(char):04X}"):
                result = normalize_text(MIM + char + NUN)
                self.assertEqual(result.text, MIM + NUN)
                self.assertFalse(result.flags)

    def test_every_west_syriac_vowel_is_preserved_and_refused(self):
        for mark in WEST_SYRIAC_VOWELS:
            with self.subTest(codepoint=f"U+{ord(mark):04X}"):
                source = MIM + mark
                result = normalize_text(source)
                self.assertEqual(result.text, source)
                self.assertIn("west-syriac-vowel", [flag.code for flag in result.flags])

    def test_every_nonproject_syriac_letter_is_retained_and_flagged(self):
        unsupported = ["\u0714", "\u071c", "\u071e", "\u0727", "\u072d", "\u072e", "\u072f", "\u074d", "\u074e", "\u074f"]
        for char in unsupported:
            with self.subTest(codepoint=f"U+{ord(char):04X}"):
                result = normalize_text(char)
                self.assertEqual(result.text, char)
                self.assertIn("unrecognized-syriac-letter", [flag.code for flag in result.flags])

    def test_unrepresented_syriac_marks_are_retained_and_flagged(self):
        for mark in ("\u0743", "\u0745", "\u0746"):
            with self.subTest(codepoint=f"U+{ord(mark):04X}"):
                source = MIM + mark
                result = normalize_text(source)
                self.assertEqual(result.text, source)
                self.assertIn("unrecognized-combining-mark", [flag.code for flag in result.flags])

    def test_unknown_noncombining_codepoints_cannot_pass_silently(self):
        for char in ("\u074b", "\u074c", "α", "а", "🙂"):
            with self.subTest(value=repr(char)):
                result = normalize_text(MIM + char + NUN)
                self.assertEqual(result.text, MIM + char + NUN)
                self.assertIn("unexpected-codepoint", [flag.code for flag in result.flags])

    def test_latin_letters_and_digits_outside_labels_are_flagged(self):
        for source in ("ܐ\nabc", "ܐ\n123"):
            result = normalize_text(source)
            self.assertIn("unexpected-non-syriac-text", [flag.code for flag in result.flags])

    def test_editorial_structures_are_preserved_and_balanced(self):
        clean = normalize_text("(Witness A: 2) ܐ[ܒ]ܐ")
        self.assertEqual(clean.text, "(Witness A: 2) ܐ[ܒ]ܐ")
        self.assertFalse(clean.flags)
        self.assertEqual(len(inspect_normalized_text(clean.text).words), 1)
        malformed = {
            "(Witness": "unclosed-editorial-parenthesis",
            ")": "unmatched-closing-parenthesis",
            "[ܐ": "unclosed-editorial-bracket",
            "ܐ]": "unmatched-closing-bracket",
        }
        for source, expected in malformed.items():
            with self.subTest(source=source):
                result = normalize_text(source)
                self.assertIn(expected, [flag.code for flag in result.flags])

    def test_bom_and_orphan_marks_are_review_cases(self):
        bom = normalize_text("\ufeffܐ")
        self.assertIn("byte-order-mark", [flag.code for flag in bom.flags])
        for mark in (SYAME, "\u0307", "\u0323", "\u0745"):
            with self.subTest(mark=f"U+{ord(mark):04X}"):
                result = normalize_text(mark + MIM)
                self.assertIn("orphan-combining-mark", [flag.code for flag in result.flags])

    def test_post_normalization_contradictions_are_detected(self):
        cases = {
            BETH + QUSSHAYA + RUKKAKHA: "conflicting-bgdkpt-state",
            MIM + "\u0732" + "\u0735": "multiple-vowels-on-carrier",
            WAW + RWAHA + HBASA_ESASA_DOTTED: "multiple-vowels-on-carrier",
            MIM + SYAME + SYAME: "duplicate-normalized-mark",
            MIM + QUSSHAYA: "qūššāyā-invalid-carrier",
            MIM + HBASA_ESASA_DOTTED: "carrier-vowel-invalid-carrier",
            MIM + OCCULTANS_BELOW + OCCULTANS_ABOVE: "dual-occultans-unrepresentable",
            MIM + BETWEEN_ABOVE: "between-point-without-next-letter",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                audit = inspect_normalized_text(source)
                self.assertIn(expected, [issue.code for issue in audit.issues])

    def test_adjacent_occultans_is_a_page_only_notice(self):
        for mark in (OCCULTANS_ABOVE, OCCULTANS_BELOW):
            with self.subTest(mark=f"U+{ord(mark):04X}"):
                source = MIM + mark + NUN + mark
                audit = inspect_normalized_text(source)
                self.assertFalse(audit.issues)
                self.assertIn("adjacent-occultans-page-check", [notice.code for notice in audit.notices])

    def test_mater_and_word_final_shapes_remain_literal_for_later_transliteration(self):
        source = "ܡܵ ܡܵܐ ܡܹ ܡܹܐ ܡܹܝ"
        result = normalize_text(source)
        self.assertFalse(result.flags)
        audit = inspect_normalized_text(result.text)
        self.assertEqual([len(word.letters) for word in audit.words], [1, 2, 1, 2, 2])


if __name__ == "__main__":
    unittest.main()
