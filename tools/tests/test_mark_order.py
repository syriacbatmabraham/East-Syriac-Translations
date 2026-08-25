from __future__ import annotations

import itertools
import sys
from pathlib import Path
import unittest
import unicodedata

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.normalization import (
    CANONICAL_MARK_ORDER,
    HBASA_ESASA_DOTTED,
    KNOWN_MARKS,
    RWAHA,
    normalize_text,
)
from east_syriac.transliteration import transliterate_text
from east_syriac.transliteration_inverse import reverse_transliterate


MIM = "\u0721"
NUN = "\u0722"
YODH = "\u071d"
WAW = "\u0718"
PTHAHA = "\u0732"
ZQAPHA = "\u0735"
ZLAMA_PSHIQA = "\u0738"
ZLAMA_QASHYA = "\u0739"


class CanonicalMarkOrderTests(unittest.TestCase):
    def test_total_order_ranks_every_supported_mark_once(self):
        self.assertEqual(frozenset(CANONICAL_MARK_ORDER), KNOWN_MARKS)
        self.assertEqual(len(CANONICAL_MARK_ORDER), len(KNOWN_MARKS))

    def test_total_order_names_every_relevant_combining_class(self):
        classes = tuple(dict.fromkeys(unicodedata.combining(mark) for mark in CANONICAL_MARK_ORDER))
        self.assertEqual(classes, (36, 218, 220, 228, 230, 233, 234))

    def test_reversed_complete_inventory_normalizes_to_total_order(self):
        source = MIM + "".join(reversed(CANONICAL_MARK_ORDER))
        expected = MIM + "".join(CANONICAL_MARK_ORDER)
        result = normalize_text(source)
        self.assertFalse(result.flags)
        self.assertEqual(result.text, expected)

    def test_every_supported_mark_pair_converges_to_rank_order(self):
        for left, right in itertools.combinations(CANONICAL_MARK_ORDER, 2):
            with self.subTest(left=f"U+{ord(left):04X}", right=f"U+{ord(right):04X}"):
                result = normalize_text(MIM + right + left)
                self.assertFalse(result.flags)
                self.assertEqual(result.text, MIM + left + right)

    def assert_double_vowel_permutations(
        self,
        carrier: str,
        first: str,
        second: str,
        expected_latin: str,
    ) -> None:
        normalized_forms = {
            normalize_text(carrier + "".join(order) + NUN).text
            for order in ((first, second), (second, first))
        }
        self.assertEqual(len(normalized_forms), 1)
        normalized = normalized_forms.pop()
        canonical = transliterate_text(normalized).text
        self.assertEqual(canonical, expected_latin)
        self.assertEqual(reverse_transliterate(canonical).text, normalized)

    def test_same_class_220_class_b_vowels_converge(self):
        self.assert_double_vowel_permutations(
            MIM, ZLAMA_PSHIQA, ZLAMA_QASHYA, "meēn"
        )

    def test_same_class_230_class_b_vowels_converge(self):
        self.assert_double_vowel_permutations(
            MIM, PTHAHA, ZQAPHA, "maān"
        )

    def test_same_class_220_carrier_plus_class_b_vowel_converges(self):
        self.assert_double_vowel_permutations(
            YODH, HBASA_ESASA_DOTTED, ZLAMA_PSHIQA, "īen"
        )

    def test_same_class_230_carrier_plus_class_b_vowel_converges(self):
        self.assert_double_vowel_permutations(
            WAW, RWAHA, PTHAHA, "ōan"
        )


if __name__ == "__main__":
    unittest.main()
