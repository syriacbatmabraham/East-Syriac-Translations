from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.inspection import inspect_normalized_text
from east_syriac.normalization import MARHETANA_ABOVE, MARHETANA_BELOW, normalize_text
from east_syriac.transliteration import TransliterationError, transliterate_text
from east_syriac.transliteration_inverse import reverse_transliterate


MARHETANA_SOURCE = "ܫܒܲܩ̣͞ܢ"
MARHETANA_CANONICAL = "šbaq_⁀n"
SEPARATE_SOURCE = "ܫܒܲܩ̣݇ܢ݇"
SEPARATE_CANONICAL = "šba(q_)(n)"


class MarhetanaModelTests(unittest.TestCase):
    def test_confirmed_qoph_nun_marhetana_span_round_trips(self):
        norm = normalize_text(MARHETANA_SOURCE)
        self.assertTrue(norm.ok, norm.flags)
        self.assertEqual(norm.text, MARHETANA_SOURCE)
        self.assertEqual(transliterate_text(MARHETANA_SOURCE).text, MARHETANA_CANONICAL)
        reverse = reverse_transliterate(MARHETANA_CANONICAL)
        self.assertEqual(reverse.text, MARHETANA_SOURCE)

    def test_span_and_separate_lines_are_distinct_in_both_layers(self):
        self.assertNotEqual(MARHETANA_SOURCE, SEPARATE_SOURCE)
        self.assertNotEqual(MARHETANA_CANONICAL, SEPARATE_CANONICAL)
        self.assertEqual(transliterate_text(SEPARATE_SOURCE).text, SEPARATE_CANONICAL)
        self.assertEqual(reverse_transliterate(SEPARATE_CANONICAL).text, SEPARATE_SOURCE)
        self.assertEqual(reverse_transliterate(MARHETANA_CANONICAL).text, MARHETANA_SOURCE)

    def test_lower_span_uses_double_macron_below_and_undertie(self):
        source = "ܡ͟ܢ"
        canonical = "m‿n"
        self.assertEqual(transliterate_text(source).text, canonical)
        self.assertEqual(reverse_transliterate(canonical).text, source)

    def test_legacy_two_letter_parenthetical_span_is_rejected(self):
        with self.assertRaises(TransliterationError) as caught:
            reverse_transliterate("šba(q_n)")
        self.assertEqual(caught.exception.code, "legacy-two-letter-line-wrapper")

    def test_span_requires_following_letter(self):
        source = "ܡ" + MARHETANA_ABOVE
        report = inspect_normalized_text(source)
        self.assertIn("marhetana-without-next-letter", [issue.code for issue in report.issues])
        with self.assertRaises(TransliterationError):
            transliterate_text(source)

    def test_overlapping_spans_are_blocking(self):
        source = "ܡ" + MARHETANA_ABOVE + "ܢ" + MARHETANA_ABOVE + "ܐ"
        report = inspect_normalized_text(source)
        self.assertIn("overlapping-marhetana-spans", [issue.code for issue in report.issues])

    def test_double_diacritics_are_known_normalized_marks(self):
        for mark in (MARHETANA_ABOVE, MARHETANA_BELOW):
            source = "ܡ" + mark + "ܢ"
            result = normalize_text(source)
            self.assertTrue(result.ok, result.flags)
            self.assertEqual(result.text, source)


if __name__ == "__main__":
    unittest.main()
