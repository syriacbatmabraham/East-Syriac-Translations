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
        # Each apparent layer can be made three lines long, but the blank-line
        # position differs. General Rules §9.1.1 requires stanza breaks to align.
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
        # Generic dot above on beth is a source alias; normalized Syriac must use
        # the canonical qūššāyā codepoint instead.
        text = make_file("ܒ\u0307", "ḃ", "one")
        result = check_confirmed_text(text, "sample.txt")
        self.assertIn("syriac-transliteration-error", [issue.code for issue in result.issues])

    def test_page_only_occultans_decision_may_be_recovered_from_exact_canonical(self):
        source = "ܡ\u0747ܢ\u0747"
        text = make_file(source, "(mn)", "one")
        result = check_confirmed_text(text, "sample.txt")
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.expected_transliteration_block, "(mn)")

    def test_page_only_occultans_is_not_trusted_from_stale_canonical(self):
        source = "ܡ\u0747ܢ\u0747"
        text = make_file(source, "(mg)", "one")
        result = check_confirmed_text(text, "sample.txt")
        codes = [issue.code for issue in result.issues]
        self.assertIn("reverse-round-trip-mismatch", codes)
        self.assertIn("occultans-page-resolution-required", codes)
        self.assertIsNone(result.expected_transliteration_block)

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
