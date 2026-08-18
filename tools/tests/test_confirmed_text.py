from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.confirmed_text import (
    ConfirmedTextFormatError,
    check_confirmed_text,
    check_confirmed_text_bytes,
    parse_confirmed_text,
)


def make_file(syriac: str, canonical: str, english: str, separator: str = "\n\n") -> str:
    return f"{syriac}{separator}{canonical}{separator}{english}\n"


class ConfirmedTextParserTests(unittest.TestCase):
    def test_basic_three_block_parse(self):
        text = make_file("ܐܒ\nܓܕ", "ʾb\ngd", "one\ntwo")
        doc = parse_confirmed_text(text)
        self.assertEqual(doc.syriac_lines, ("ܐܒ", "ܓܕ"))
        self.assertEqual(doc.transliteration_lines, ("ʾb", "gd"))
        self.assertEqual(doc.english_lines, ("one", "two"))
        self.assertEqual(doc.line_count, 2)
        self.assertEqual(doc.stanza_breaks, ())

    def test_stanza_breaks_are_not_mistaken_for_block_boundaries(self):
        text = make_file(
            "ܐܒ\n\nܓܕ",
            "ʾb\n\ngd",
            "one\n\ntwo",
        )
        doc = parse_confirmed_text(text)
        self.assertEqual(doc.line_count, 3)
        self.assertEqual(doc.stanza_breaks, (2,))
        self.assertEqual(doc.transliteration_lines[1], "")
        self.assertEqual(doc.english_lines[1], "")

    def test_misaligned_stanza_breaks_are_rejected(self):
        text = "ܐܒ\n\nܓܕ\n\nʾb\ngd\nx\n\none\n\ntwo\n"
        with self.assertRaises(ConfirmedTextFormatError) as caught:
            parse_confirmed_text(text)
        self.assertEqual(caught.exception.code, "stanza-break-mismatch")

    def test_separator_runs_may_have_more_than_one_blank_line(self):
        text = make_file("ܐܒ", "ʾb", "one", separator="\n\n\n")
        doc = parse_confirmed_text(text)
        self.assertEqual(doc.line_count, 1)

    def test_unequal_blocks_are_rejected(self):
        text = "ܐܒ\nܓܕ\n\nʾb\n\none\ntwo\n"
        with self.assertRaises(ConfirmedTextFormatError) as caught:
            parse_confirmed_text(text)
        self.assertEqual(caught.exception.code, "unequal-block-length")

    def test_missing_blocks_are_rejected(self):
        with self.assertRaises(ConfirmedTextFormatError) as caught:
            parse_confirmed_text("ܐܒ\nʾb\none\n")
        self.assertEqual(caught.exception.code, "three-block-structure")


class ConfirmedTextValidationTests(unittest.TestCase):
    def test_clean_file_passes_and_derives_transliteration(self):
        text = make_file("ܐܒ\nܓܕ", "ʾb\ngd", "one\ntwo")
        result = check_confirmed_text(text, "sample.txt")
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.expected_transliteration_block, "ʾb\ngd")

    def test_rubrical_label_is_preserved_but_ignored_in_text_comparison(self):
        text = make_file(
            "(Qanona) ܐܒ",
            "(Qanona) ʾb",
            "(Qanona) one",
        )
        result = check_confirmed_text(text, "sample.txt")
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.expected_transliteration_block, "(Qanona) ʾb")

    def test_rubrical_label_may_move_within_english_apparatus(self):
        text = make_file(
            "ܐܒ (Witness:) [ܓ]",
            "ʾb (Witness:) [g]",
            "(Witness:) [variant]",
        )
        result = check_confirmed_text(text, "sample.txt")
        self.assertTrue(result.ok, result.issues)

    def test_missing_rubrical_label_in_transliteration_is_reported(self):
        text = make_file(
            "(Qanona) ܐܒ",
            "ʾb",
            "(Qanona) one",
        )
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("editorial-label-mismatch", [issue.code for issue in result.issues])

    def test_missing_rubrical_label_in_english_is_reported(self):
        text = make_file(
            "(Qanona) ܐܒ",
            "(Qanona) ʾb",
            "one",
        )
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("editorial-label-mismatch", [issue.code for issue in result.issues])

    def test_stale_transliteration_is_detected_from_syriac(self):
        text = make_file("ܐܒ", "ʾg", "one")
        result = check_confirmed_text(text, "sample.txt")
        codes = [issue.code for issue in result.issues]
        self.assertIn("reverse-round-trip-mismatch", codes)
        self.assertIn("stale-transliteration", codes)
        self.assertEqual(result.expected_transliteration_block, "ʾb")

    def test_invalid_canonical_syntax_does_not_block_expected_derivation(self):
        text = make_file("ܐܒ", "x", "one")
        result = check_confirmed_text(text, "sample.txt")
        codes = [issue.code for issue in result.issues]
        self.assertIn("invalid-canonical-transliteration", codes)
        self.assertIn("stale-transliteration", codes)
        self.assertEqual(result.expected_transliteration_block, "ʾb")

    def test_non_normalized_syriac_is_refused_by_forward_layer(self):
        text = make_file("ܬ\u0740", "t̤", "one")
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("syriac-transliteration-error", [issue.code for issue in result.issues])

    def test_direct_marhetana_is_derived_from_syriac(self):
        source = "ܡ\u035eܢ"
        text = make_file(source, "m⁀n", "one")
        result = check_confirmed_text(text, "sample.txt")
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.expected_transliteration_block, "m⁀n")

    def test_stale_marhetana_latin_does_not_block_expected_derivation(self):
        source = "ܡ\u035eܢ"
        text = make_file(source, "m⁀g", "one")
        result = check_confirmed_text(text, "sample.txt")
        codes = [issue.code for issue in result.issues]
        self.assertIn("reverse-round-trip-mismatch", codes)
        self.assertIn("stale-transliteration", codes)
        self.assertEqual(result.expected_transliteration_block, "m⁀n")

    def test_adjacent_one_letter_lines_need_no_page_metadata(self):
        source = "ܡ\u0747ܢ\u0747"
        text = make_file(source, "(m)(n)", "one")
        result = check_confirmed_text(text, "sample.txt")
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.expected_transliteration_block, "(m)(n)")

    def test_single_one_letter_line_parentheses_are_not_rubrical(self):
        source = "ܗ\u0747ܘ\u0323"
        text = make_file(source, "(h)w_", "one")
        result = check_confirmed_text(text, "sample.txt")
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.expected_transliteration_block, "(h)w_")

    def test_bom_is_reported_but_file_is_still_analyzed(self):
        data = ("\ufeff" + make_file("ܐܒ", "ʾb", "one")).encode("utf-8")
        result = check_confirmed_text_bytes(data, "sample.txt")
        self.assertIn("byte-order-mark", [issue.code for issue in result.issues])
        self.assertIsNotNone(result.document)

    def test_crlf_is_reported_but_file_is_still_analyzed(self):
        text = make_file("ܐܒ", "ʾb", "one").replace("\n", "\r\n")
        result = check_confirmed_text_bytes(text.encode("utf-8"), "sample.txt")
        self.assertIn("non-lf-line-ending", [issue.code for issue in result.issues])
        self.assertIsNotNone(result.document)

    def test_trailing_whitespace_is_reported(self):
        text = make_file("ܐܒ ", "ʾb", "one")
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("trailing-whitespace", [issue.code for issue in result.issues])

    def test_non_ascii_whitespace_is_reported(self):
        text = make_file("ܐܒ", "ʾb", "one\u00a0two")
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("unsupported-whitespace", [issue.code for issue in result.issues])

    def test_tab_is_reported(self):
        text = make_file("ܐܒ", "ʾb", "one\ttwo")
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("unsupported-whitespace", [issue.code for issue in result.issues])

    def test_non_nfc_is_reported(self):
        text = make_file("ܐܒ", "ʾb", "Cafe\u0301")
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("non-nfc", [issue.code for issue in result.issues])

    def test_curly_apostrophe_is_reported(self):
        text = make_file("ܐܒ", "ʾb", "God’s")
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("curly-apostrophe", [issue.code for issue in result.issues])

    def test_extension_is_checked(self):
        text = make_file("ܐܒ", "ʾb", "one")
        result = check_confirmed_text(text, "sample.rtf")
        self.assertIn("unsupported-extension", [issue.code for issue in result.issues])

    def test_invalid_utf8_is_reported(self):
        result = check_confirmed_text_bytes(b"\xff\xfe", "sample.txt")
        self.assertIsNone(result.document)
        self.assertEqual([issue.code for issue in result.issues], ["invalid-utf8"])


if __name__ == "__main__":
    unittest.main()
