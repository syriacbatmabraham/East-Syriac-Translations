from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.inspection import inspect_normalized_text
from east_syriac.normalization import WEST_SYRIAC_VOWELS, normalize_text


class SyntheticNormalizationStressTests(unittest.TestCase):
    """Imaginary forms designed to force unusual codepoint/page-state paths."""

    def assert_clean(self, source: str, expected: str) -> None:
        result = normalize_text(source)
        self.assertEqual(result.text, expected)
        self.assertFalse(result.flags)
        self.assertFalse(inspect_normalized_text(result.text).issues)

    def test_bgdkpt_single_point_aliases(self):
        self.assert_clean(
            "ܒ\u0307ܕ\u073cܓ\u0741ܬ\u0323",
            "ܒ\u0741ܕ\u0742ܓ\u0741ܬ\u0742",
        )

    def test_non_bgdkpt_single_point_aliases(self):
        self.assert_clean("ܡ\u0741ܢ\u0742", "ܡ\u0307ܢ\u0323")

    def test_waw_and_yodh_carrier_resolution(self):
        self.assert_clean(
            "ܘ\u0307ܘ\u0323ܝ\u0742ܝ\u073f",
            "ܘ\u073fܘ\u073cܝ\u073cܝ\u0307",
        )

    def test_final_semkath_inside_imaginary_word(self):
        self.assert_clean("ܡ\u0724ܐ", "ܡ\u0723ܐ")

    def test_all_two_dots_below_aliases_collapse(self):
        self.assert_clean("ܬ\u0740ܡ\u0744ܢ\u0324", "ܬ\u0324ܡ\u0324ܢ\u0324")

    def test_u0716_with_intervening_vowel_and_syame(self):
        self.assert_clean("ܥܝ\u073c\u0716\u0739\u0308ܐ", "ܥܝ\u073cܪ\u0739\u0308ܐ")

    def test_extreme_class_230_reordering(self):
        self.assert_clean(
            "ܡ\u0747\u0308\u0307\u0735",
            "ܡ\u0735\u0307\u0308\u0747",
        )

    def test_extreme_class_220_reordering(self):
        self.assert_clean(
            "ܡ\u0748\u032e\u0324\u0323\u0738",
            "ܡ\u0738\u0323\u0324\u032e\u0748",
        )

    def test_mixed_combining_classes_and_superscript_alaph(self):
        self.assert_clean(
            "ܡ\u0747\u0711\u0323\u0735",
            "ܡ\u0711\u0323\u0735\u0747",
        )

    def test_between_letter_points_survive_as_distinct_states(self):
        self.assert_clean("ܩ\U00001df8ܥ ܡ\U00001dfaܢ", "ܩ\U00001df8ܥ ܡ\U00001dfaܢ")

    def test_legal_dense_above_stack(self):
        self.assert_clean(
            "ܒ\u0747\u0308\u0741\u0735",
            "ܒ\u0735\u0741\u0308\u0747",
        )

    def test_legal_dense_below_stack(self):
        self.assert_clean(
            "ܦ\u0748\u032e\u0324\u0742\u0738",
            "ܦ\u0738\u0742\u0324\u032e\u0748",
        )

    def test_legal_marks_above_and_below_same_letter(self):
        self.assert_clean("ܡ\u0308\u0323\u0735", "ܡ\u0323\u0735\u0308")

    def test_carrier_vowels_with_syame(self):
        self.assert_clean("ܘ\u073f\u0308 ܝ\u073c\u0308", "ܘ\u073f\u0308 ܝ\u073c\u0308")

    def test_bgdkpt_vowel_plus_hard_or_soft_is_legal(self):
        self.assert_clean("ܕ\u0732\u0741 ܬ\u0738\u0742", "ܕ\u0732\u0741 ܬ\u0738\u0742")

    def test_out_of_scope_noise_is_removed_from_imaginary_word(self):
        source = "ܡـܪ\u200dܝ\u0749:ܐ"
        result = normalize_text(source)
        self.assertEqual(result.text, "ܡܪܝܐ")
        self.assertFalse(result.flags)
        self.assertFalse(inspect_normalized_text(result.text).issues)

    def test_bare_u0716_requires_source_review(self):
        result = normalize_text("ܡ\u0716ܐ")
        self.assertEqual(result.text, "ܡܪܐ")
        self.assertIn("bare-u0716", [flag.code for flag in result.flags])

    def test_every_west_syriac_vowel_is_refused(self):
        for vowel in WEST_SYRIAC_VOWELS:
            with self.subTest(codepoint=f"U+{ord(vowel):04X}"):
                result = normalize_text("ܡ" + vowel + "ܐ")
                self.assertEqual(result.text, "ܡ" + vowel + "ܐ")
                self.assertIn("west-syriac-vowel", [flag.code for flag in result.flags])

    def test_unknown_syriac_combining_mark_requires_review(self):
        result = normalize_text("ܡ\u0745ܐ")
        self.assertEqual(result.text, "ܡ\u0745ܐ")
        self.assertIn("unrecognized-combining-mark", [flag.code for flag in result.flags])

    def test_orphan_mark_requires_review(self):
        result = normalize_text("\u0308ܡܐ")
        self.assertIn("orphan-combining-mark", [flag.code for flag in result.flags])

    def test_unsupported_nonbreaking_space_requires_review(self):
        result = normalize_text("ܐ\u00a0ܒ")
        self.assertIn("unsupported-whitespace", [flag.code for flag in result.flags])

    def test_unsupported_tab_requires_review_even_in_editorial_label(self):
        result = normalize_text("(Witness\tA) ܐ")
        self.assertIn("unsupported-whitespace", [flag.code for flag in result.flags])

    def test_duplicate_single_point_above_aliases_require_review(self):
        result = normalize_text("ܒ\u0307\u0741ܐ")
        self.assertIn("duplicate-single-point-above", [flag.code for flag in result.flags])
        audit = inspect_normalized_text(result.text)
        self.assertIn("duplicate-normalized-mark", [issue.code for issue in audit.issues])

    def test_duplicate_single_point_below_aliases_require_review(self):
        result = normalize_text("ܕ\u0323\u0742ܐ")
        self.assertIn("duplicate-single-point-below", [flag.code for flag in result.flags])
        audit = inspect_normalized_text(result.text)
        self.assertIn("duplicate-normalized-mark", [issue.code for issue in audit.issues])

    def test_contradictory_hard_and_soft_state_is_caught_after_normalization(self):
        result = normalize_text("ܒ\u0741\u0742ܐ")
        self.assertFalse(result.flags)
        audit = inspect_normalized_text(result.text)
        self.assertIn("conflicting-bgdkpt-state", [issue.code for issue in audit.issues])

    def test_two_vowels_on_same_consonant_are_caught_after_normalization(self):
        result = normalize_text("ܡ\u0732\u0735ܐ")
        self.assertFalse(result.flags)
        audit = inspect_normalized_text(result.text)
        self.assertIn("multiple-vowels-on-carrier", [issue.code for issue in audit.issues])

    def test_two_carrier_vowels_on_waw_are_caught_after_normalization(self):
        result = normalize_text("ܘ\u073f\u073cܐ")
        self.assertFalse(result.flags)
        audit = inspect_normalized_text(result.text)
        self.assertIn("multiple-vowels-on-carrier", [issue.code for issue in audit.issues])

    def test_duplicate_syame_is_caught_after_normalization(self):
        result = normalize_text("ܡ\u0308\u0308ܐ")
        self.assertFalse(result.flags)
        audit = inspect_normalized_text(result.text)
        self.assertIn("duplicate-normalized-mark", [issue.code for issue in audit.issues])


if __name__ == "__main__":
    unittest.main()
