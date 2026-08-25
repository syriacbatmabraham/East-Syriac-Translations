from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.inspection import inspect_normalized_text
from east_syriac.normalization import normalize_text
from east_syriac.transliteration import TransliterationError, transliterate_text
from east_syriac.transliteration_inverse import reverse_transliterate


class DoubleVowelTests(unittest.TestCase):
    def assert_round_trip(self, source: str, expected: str) -> None:
        normalized = normalize_text(source)
        self.assertFalse(normalized.flags)
        forward = transliterate_text(normalized.text)
        self.assertEqual(forward.text, expected)
        self.assertEqual(reverse_transliterate(expected).text, normalized.text)
        self.assertEqual(transliterate_text(reverse_transliterate(expected).text).text, expected)

    def test_attested_iala_mixed_carrier_and_class_b_vowel(self):
        source = "ܐܝ\u073c\u0735ܠ\u0735ܐ"
        normalized = normalize_text(source)
        audit = inspect_normalized_text(normalized.text)
        self.assertIn("multiple-vowels-on-carrier", [issue.code for issue in audit.issues])
        self.assert_round_trip(source, "ʾīālā")

    def test_two_distinct_class_b_vowels_round_trip(self):
        source = "ܡ\u0738\u0735ܢ"
        normalized = normalize_text(source)
        audit = inspect_normalized_text(normalized.text)
        self.assertIn("multiple-vowels-on-carrier", [issue.code for issue in audit.issues])
        self.assert_round_trip(source, "meān")

    def test_final_mater_shorthand_with_double_vowel_state(self):
        self.assert_round_trip("ܡ\u0738\u0735", "meă")
        self.assert_round_trip("ܡ\u0738\u0735ܐ", "meā")

    def test_three_vowel_states_remain_unrepresented(self):
        source = normalize_text("ܡ\u0738\u0732\u0735ܢ").text
        with self.assertRaises(TransliterationError) as caught:
            transliterate_text(source)
        self.assertEqual(caught.exception.code, "too-many-vowels-on-carrier")

    def test_conflicting_waw_class_a_states_remain_blocking(self):
        source = normalize_text("ܘ\u073c\u073fܢ").text
        with self.assertRaises(TransliterationError) as caught:
            transliterate_text(source)
        self.assertEqual(caught.exception.code, "conflicting-carrier-vowels")


if __name__ == "__main__":
    unittest.main()
