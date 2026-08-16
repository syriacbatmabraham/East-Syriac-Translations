from __future__ import annotations

import sys
from pathlib import Path
import unittest
import unicodedata

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.normalization import normalize_text


class NormalizationTests(unittest.TestCase):
    def test_removes_out_of_scope_characters(self):
        source = "ܐܵܒܵܐ: ܡـܪܝ\u200dܐ\u0749"
        result = normalize_text(source)
        self.assertEqual(result.text, "ܐܵܒܵܐ ܡܪܝܐ")
        self.assertFalse(result.flags)

    def test_preserves_punctuation_inside_parenthesized_editorial_label(self):
        source = "(Witness A:) [ܐܵܒܵܐ:]"
        result = normalize_text(source)
        self.assertEqual(result.text, "(Witness A:) [ܐܵܒܵܐ]")

    def test_final_semkath_normalizes(self):
        result = normalize_text("\u0724")
        self.assertEqual(result.text, "\u0723")
        self.assertFalse(result.flags)

    def test_single_point_states_preserve_explicit_identity(self):
        cases = (
            "ܒ\u0741", "ܕ\u0742", "ܘ\u073f", "ܘ\u073c", "ܝ\u073c",
            "ܒ\u0307", "ܒ\u0323", "ܘ\u0307", "ܘ\u0323",
            "ܝ\u0307", "ܝ\u0323", "ܡ\u0307", "ܡ\u0323",
        )
        for source in cases:
            with self.subTest(source=source):
                result = normalize_text(source)
                self.assertEqual(result.text, source)
                self.assertFalse(result.flags)

    def test_two_dots_below_aliases_normalize(self):
        for mark in ("\u0324", "\u0740", "\u0744"):
            with self.subTest(mark=f"U+{ord(mark):04X}"):
                self.assertEqual(normalize_text("ܬ" + mark).text, "ܬ\u0324")

    def test_u0716_with_syame_is_resh_without_flag(self):
        result = normalize_text("\u0716\u0739\u0308")
        self.assertEqual(result.text[0], "ܪ")
        self.assertFalse(result.flags)

    def test_bare_u0716_is_resh_and_flagged(self):
        result = normalize_text("\u0716")
        self.assertEqual(result.text, "ܪ")
        self.assertEqual([flag.code for flag in result.flags], ["bare-u0716"])

    def test_west_syriac_vowel_is_refused_not_mapped(self):
        source = "ܡ\u0730"
        result = normalize_text(source)
        self.assertEqual(result.text, source)
        self.assertIn("west-syriac-vowel", [flag.code for flag in result.flags])

    def test_unknown_syriac_mark_is_flagged_and_retained(self):
        source = "ܡ\u0745"
        result = normalize_text(source)
        self.assertEqual(result.text, source)
        self.assertIn("unrecognized-combining-mark", [flag.code for flag in result.flags])

    def test_class_230_project_order(self):
        source = "ܡ\u0747\u0308\u0307\u0735"
        result = normalize_text(source)
        self.assertEqual(result.text, "ܡ\u0735\u0307\u0308\u0747")
        self.assertFalse(result.flags)

    def test_class_220_project_order(self):
        source = "ܡ\u0748\u032e\u0324\u0323\u0738"
        result = normalize_text(source)
        self.assertEqual(result.text, "ܡ\u0738\u0323\u0324\u032e\u0748")
        self.assertFalse(result.flags)

    def test_different_combining_classes_sort_ascending(self):
        source = "ܡ\u0307\U00001dfa\u0323"
        result = normalize_text(source)
        classes = [unicodedata.combining(ch) for ch in result.text[1:]]
        self.assertEqual(classes, sorted(classes))

    def test_normalization_is_idempotent(self):
        source = "ܒ\u0307ܬ\u0740 ܡ\u0748\u032e\u0323\u0738"
        once = normalize_text(source)
        twice = normalize_text(once.text)
        self.assertEqual(twice.text, once.text)
        self.assertFalse(twice.flags)

    def test_orphan_combining_mark_is_flagged(self):
        result = normalize_text("\u0308ܡ")
        self.assertIn("orphan-combining-mark", [flag.code for flag in result.flags])

    def test_distinct_single_point_identities_are_not_collapsed(self):
        result = normalize_text("ܒ\u0307\u0741")
        self.assertEqual(result.text, "ܒ\u0741\u0307")
        self.assertFalse(result.flags)

    def test_latin_text_outside_editorial_label_is_flagged(self):
        result = normalize_text("ܐܒܐ\naba")
        self.assertIn("unexpected-non-syriac-text", [flag.code for flag in result.flags])

    def test_latin_text_inside_editorial_label_is_allowed(self):
        result = normalize_text("(Witness A:) ܐܒܐ")
        self.assertNotIn("unexpected-non-syriac-text", [flag.code for flag in result.flags])

    def test_non_syriac_carrier_does_not_absorb_syame(self):
        result = normalize_text(" [\u0308ܐ")
        self.assertIn("orphan-combining-mark", [flag.code for flag in result.flags])

    def test_bom_is_flagged_and_retained(self):
        source = "\ufeffܐܒܐ"
        result = normalize_text(source)
        self.assertEqual(result.text, source)
        self.assertIn("byte-order-mark", [flag.code for flag in result.flags])


if __name__ == "__main__":
    unittest.main()
