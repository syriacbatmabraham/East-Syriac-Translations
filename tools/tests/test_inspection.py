from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.inspection import format_page_state_report, inspect_normalized_text


class PageStateInspectionTests(unittest.TestCase):
    def test_sample_alaha_reports_every_mark(self):
        text = "ܠܐܲܠܵܗܵܐ"
        report = format_page_state_report(text, ["lʾalāhā"])
        self.assertEqual(
            report,
            "\n".join(
                [
                    "Word 1: *lʾalāhā*",
                    "Lamad",
                    "Alaph (pṯāḥā: a)",
                    "Lamad (zqāpā: ā)",
                    "Heh (zqāpā: ā)",
                    "Alaph",
                ]
            ),
        )

    def test_square_brackets_do_not_divide_word(self):
        state = inspect_normalized_text("ܐ[ܒ]ܐ")
        self.assertEqual(len(state.words), 1)
        self.assertEqual(state.words[0].text, "ܐܒܐ")

    def test_multiple_words_and_lines(self):
        state = inspect_normalized_text("ܐܒ ܓܕ\nܗܘ")
        self.assertEqual([word.text for word in state.words], ["ܐܒ", "ܓܕ", "ܗܘ"])
        self.assertEqual([word.line for word in state.words], [1, 1, 2])

    def test_carrier_vowels_are_named_by_carrier(self):
        report = format_page_state_report("ܝ\u073c ܘ\u073f ܘ\u073c")
        self.assertIn("Yodh (ḥḇāṣā: ī)", report)
        self.assertIn("Waw (rwāḥā: ō)", report)
        self.assertIn("Waw (rḇāṣā / ʾeṣāṣā: ū)", report)

    def test_multiple_marks_on_one_letter_are_all_reported(self):
        report = format_page_state_report("ܡ\u0735\u0307\u0308\u0747")
        self.assertIn(
            "Mim (zqāpā: ā; single point above; syāmē; occultans line above)",
            report,
        )

    def test_conflicting_bgdkpt_points_are_issue(self):
        state = inspect_normalized_text("ܒ\u0742\u0741")
        self.assertIn("conflicting-bgdkpt-state", [issue.code for issue in state.issues])

    def test_multiple_vowels_on_one_carrier_are_issue(self):
        state = inspect_normalized_text("ܡ\u0732\u0735")
        self.assertIn("multiple-vowels-on-carrier", [issue.code for issue in state.issues])

    def test_duplicate_normalized_mark_is_issue(self):
        state = inspect_normalized_text("ܡ\u0308\u0308")
        self.assertIn("duplicate-normalized-mark", [issue.code for issue in state.issues])

    def test_invalid_canonical_carriers_are_issue(self):
        cases = {
            "ܡ\u0741": "qūššāyā-invalid-carrier",
            "ܡ\u0742": "rūkkākā-invalid-carrier",
            "ܡ\u073f": "rwāḥā-invalid-carrier",
            "ܡ\u073c": "carrier-vowel-invalid-carrier",
            "ܒ\u0307": "generic-point-on-bgdkpt",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                state = inspect_normalized_text(source)
                self.assertIn(expected, [issue.code for issue in state.issues])

    def test_occultans_above_and_below_same_carrier_is_unrepresentable(self):
        state = inspect_normalized_text("ܡ\u0748\u0747")
        self.assertIn("dual-occultans-unrepresentable", [issue.code for issue in state.issues])

    def test_between_point_requires_following_letter(self):
        state = inspect_normalized_text("ܡ\U00001df8")
        self.assertIn("between-point-without-next-letter", [issue.code for issue in state.issues])
        self.assertNotIn(
            "between-point-without-next-letter",
            [issue.code for issue in inspect_normalized_text("ܡ\U00001df8ܢ").issues],
        )

    def test_word_labels_must_align_one_to_one(self):
        with self.assertRaises(ValueError):
            format_page_state_report("ܐ ܒ", ["ʾ"])


if __name__ == "__main__":
    unittest.main()
