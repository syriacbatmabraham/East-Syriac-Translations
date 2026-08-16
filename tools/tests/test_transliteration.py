from __future__ import annotations

import sys
from pathlib import Path
import unittest
import unicodedata

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.normalization import (
    BGDKPT,
    BETWEEN_ABOVE,
    BETWEEN_BELOW,
    BREVE_BELOW,
    GENERIC_DOT_ABOVE,
    GENERIC_DOT_BELOW,
    HBASA_ESASA_DOTTED,
    MARHETANA_ABOVE,
    MARHETANA_BELOW,
    OCCULTANS_ABOVE,
    OCCULTANS_BELOW,
    QUSSHAYA,
    RUKKAKHA,
    RWAHA,
    SUPERSCRIPT_ALAPH,
    SYAME,
    TWO_DOTS_BELOW,
    normalize_text,
)
from east_syriac.transliteration import TransliterationError, transliterate_text
from east_syriac.transliteration_inverse import UNIT_REVERSE, reverse_transliterate


class TransliterationTests(unittest.TestCase):
    def assert_round_trip(self, source: str, expected: str | None = None):
        normalized = normalize_text(source)
        self.assertFalse(normalized.flags)
        forward = transliterate_text(normalized.text)
        if expected is not None:
            self.assertEqual(forward.text, expected)
        reverse = reverse_transliterate(forward.text)
        self.assertEqual(reverse.text, normalized.text)
        self.assertEqual(transliterate_text(reverse.text).text, forward.text)
        return forward, reverse

    def test_alaha_exact(self):
        self.assert_round_trip("ܠܐܲܠܵܗܵܐ", expected="lʾalāhā")

    def test_bare_consonant_inventory(self):
        self.assert_round_trip(
            "ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ",
            expected="ʾbgdhwzḥṭyklmnsʿpṣqršt",
        )

    def test_every_bgdkpt_state_round_trips(self):
        for base in BGDKPT:
            for mark in ("", QUSSHAYA, RUKKAKHA):
                with self.subTest(base=base, mark=mark):
                    self.assert_round_trip(base + mark)

    def test_all_vowel_classes_round_trip(self):
        for source in (
            "ܡ\u0732",
            "ܡ\u0735",
            "ܡ\u0738",
            "ܡ\u0739",
            "ܘ" + RWAHA,
            "ܘ" + HBASA_ESASA_DOTTED,
            "ܝ" + HBASA_ESASA_DOTTED,
        ):
            with self.subTest(source=source):
                self.assert_round_trip(source)

    def test_word_final_mater_conventions(self):
        cases = {
            "ܡܵܐ": "mā",
            "ܡܵ": "mă",
            "ܡܹܐ": "mē",
            "ܡܹ": "mĕ",
            "ܡܲܐ": "maʾ",
            "ܡܸܐ": "meʾ",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assert_round_trip(source, expected=expected)

    def test_marked_final_alaph_remains_explicit(self):
        self.assert_round_trip("ܡܵܐ̈", expected="māʾ̈")

    def test_editorial_boundary_prevents_mater_suppression(self):
        cases = {
            "[ܡܵܐ]": "[mā]",
            "ܡܵ[ܐ]": "mā[ʾ]",
            "[ܡܵ]ܐ": "[mā]ʾ",
            "[ܡܵ][ܐ]": "[mā][ʾ]",
            "ܡܵ[]ܐ": "mā[]ʾ",
            "[[ܡܵܐ]]": "[[mā]]",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                forward, _ = self.assert_round_trip(source, expected=expected)
                self.assertEqual(forward.word_labels, (expected,))

    def test_syame_and_precomposition(self):
        self.assert_round_trip("ܒܝܵܘ̈ܡܲܝ", expected="byāẅmay")

    def test_on_letter_and_between_letter_points(self):
        self.assert_round_trip("ܡ̣ܢ", expected="m_n")
        self.assert_round_trip("ܩ᷸ܵܥܹܝܢ", expected="qā^^ʿēyn")

    def test_special_marks_round_trip(self):
        for mark in (
            SYAME,
            TWO_DOTS_BELOW,
            BREVE_BELOW,
            SUPERSCRIPT_ALAPH,
            BETWEEN_ABOVE,
            BETWEEN_BELOW,
            MARHETANA_ABOVE,
            MARHETANA_BELOW,
        ):
            with self.subTest(mark=f"U+{ord(mark):04X}"):
                needs_next = mark in {BETWEEN_ABOVE, BETWEEN_BELOW, MARHETANA_ABOVE, MARHETANA_BELOW}
                source = "ܡ" + mark + ("ܢ" if needs_next else "")
                self.assert_round_trip(source)

    def test_dense_legal_state_round_trips(self):
        source = (
            "ܡ"
            + BETWEEN_BELOW
            + GENERIC_DOT_BELOW
            + TWO_DOTS_BELOW
            + BREVE_BELOW
            + BETWEEN_ABOVE
            + GENERIC_DOT_ABOVE
            + SYAME
            + "ܢ"
        )
        self.assert_round_trip(source)

    def test_single_occultans_examples(self):
        self.assert_round_trip("ܘܐ݇ܢܵܫܵ̈ܐ", expected="w(ʾ)nāš̈ā")
        self.assert_round_trip("ܗ݇ܝܼ", expected="(h)ī")

    def test_adjacent_one_letter_lines_are_deterministic(self):
        self.assert_round_trip("ܡ݇ܢ݇", expected="(m)(n)")
        source = "ܡ" + OCCULTANS_BELOW + "ܢ" + OCCULTANS_BELOW
        self.assert_round_trip(source, expected="(_m)(_n)")

    def test_direct_marhetana_spans(self):
        self.assert_round_trip("ܡ" + MARHETANA_ABOVE + "ܢ", expected="m⁀n")
        self.assert_round_trip("ܡ" + MARHETANA_BELOW + "ܢ", expected="m‿n")
        self.assert_round_trip("ܫܒܲܩ̣͞ܢ", expected="šbaq_⁀n")

    def test_marhetana_cannot_cross_editorial_boundary(self):
        source = normalize_text("ܡ" + MARHETANA_ABOVE + "[ܢ]").text
        with self.assertRaises(TransliterationError) as caught:
            transliterate_text(source)
        self.assertEqual(caught.exception.code, "marhetana-crosses-editorial-boundary")

    def test_legacy_two_letter_wrapper_is_rejected(self):
        with self.assertRaises(TransliterationError) as caught:
            reverse_transliterate("(mn)")
        self.assertEqual(caught.exception.code, "legacy-two-letter-line-wrapper")

    def test_editorial_apparatus_is_preserved(self):
        self.assert_round_trip(
            "(Witness A: 2) ܐ[ܒ]ܐ",
            expected="(Witness A: 2) ʾ[b]ʾ",
        )
        self.assert_round_trip(
            "(Assyrian Ferial adds:) [ܘܚܵܕ݂ܝܵ̈ܢ]",
            expected="(Assyrian Ferial adds:) [wḥāḏÿān]",
        )

    def test_editorial_parenthesis_that_collides_with_occultans_is_rejected(self):
        with self.assertRaises(TransliterationError) as caught:
            transliterate_text("(h) ܐ")
        self.assertEqual(caught.exception.code, "ambiguous-editorial-parenthesis")

    def test_generic_points_round_trip_on_all_carrier_classes(self):
        cases = {
            "ܘ\u0307ܠ": "w^l",
            "ܘ\u0323ܠ": "w_l",
            "ܝ\u0323ܠ": "y_l",
            "ܒ\u0307ܠ": "b^l",
            "ܕ\u0323ܠ": "d_l",
            "ܘ\u0735\u0307\u0308ܠ": "ẅ^āl",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assert_round_trip(source, expected=expected)

    def test_forward_requires_clean_normalized_input(self):
        with self.assertRaises(TransliterationError) as caught:
            transliterate_text("ܬ\u0740")
        self.assertEqual(caught.exception.code, "input-not-normalized")

    def test_reverse_requires_nfc(self):
        decomposed = unicodedata.normalize("NFD", "ḃ")
        self.assertNotEqual(decomposed, "ḃ")
        with self.assertRaises(TransliterationError) as caught:
            reverse_transliterate(decomposed)
        self.assertEqual(caught.exception.code, "canonical-not-nfc")

    def test_final_exception_vowel_is_rejected_internally(self):
        with self.assertRaises(TransliterationError) as caught:
            reverse_transliterate("măn")
        self.assertEqual(caught.exception.code, "final-vowel-exception-not-final")

    def test_ascii_conveniences_are_not_canonical(self):
        for text in ("m:", "m%"):
            with self.subTest(text=text):
                with self.assertRaises(TransliterationError):
                    reverse_transliterate(text)

    def test_representative_confirmed_forms(self):
        pairs = (
            ("ܡܗܲܝܡܢܝܼܢܲܢ ܒܚܲܕ ܐܲܠܵܗܵܐ ܐܲܒ݂ܵܐ ܐܲܚܝܼܕ ܟܠ", "mhaymnīnan bḥad ʾalāhā ʾaḇā ʾaḥīd kl"),
            ("ܒܘܼܟ݂ܪܵܐ ܕܟ݂ܠܗܹܝܢ ܒܸܪ̈ܝܵܬ݂ܵܐ", "būḵrā dḵlhēyn ber̈yāṯā"),
            ("ܘܚܲܫ ܘܐܸܙܕ݁ܩܸܦ ܒܝܵܘ̈ܡܲܝ ܦܲܢܛܝܼܘܿܣ ܦܝܼܠܵܛܘܿܣ", "wḥaš wʾezḋqep byāẅmay panṭīōs pīlāṭōs"),
            ("ܕܲܦܬ݂ܝܼܚܘܼ ܬܲܪܥܹܗ ܠܬܲܝܵ̇ܒܹ̈ܐ", "dapṯīḥū tarʿēh ltay^āb̈ē"),
            ("ܘܙܵܡ̇ܪܵ̈ܢ ܘܲܡܗܲܠ̈ܠܵܢ", "wzām^r̈ān wamhal̈lān"),
        )
        for source, expected in pairs:
            with self.subTest(expected=expected):
                self.assert_round_trip(source, expected=expected)

    def test_every_generated_canonical_unit_round_trips(self):
        for canonical, spec in UNIT_REVERSE.items():
            with self.subTest(canonical=canonical):
                has_between = BETWEEN_ABOVE in spec.marks or BETWEEN_BELOW in spec.marks
                text = canonical + ("n" if has_between else "")
                reverse = reverse_transliterate(text)
                self.assertEqual(transliterate_text(reverse.text).text, text)

    def test_unit_grammar_has_no_prefix_segmentation_collision(self):
        starts = {key[0] for key in UNIT_REVERSE}
        keys = set(UNIT_REVERSE)
        for key in keys:
            for cut in range(1, len(key)):
                if key[:cut] in keys and key[cut] in starts:
                    self.fail(
                        f"canonical segmentation collision: {key!r} begins with "
                        f"unit {key[:cut]!r} and leaves unit-starting suffix {key[cut:]!r}"
                    )


if __name__ == "__main__":
    unittest.main()
