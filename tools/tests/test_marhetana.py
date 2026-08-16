from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.transliteration import transliterate_text
from east_syriac.transliteration_inverse import reverse_transliterate


MARHETANA_SOURCE = "ܫܒܲܩ̣݇ܢ݇"
MARHETANA_CANONICAL = "šba(q_n)"
SEPARATE_CANONICAL = "šba(q_)(n)"


class MarhetanaModelTests(unittest.TestCase):
    def test_confirmed_qoph_nun_marhetana_span_round_trips(self):
        reverse = reverse_transliterate(MARHETANA_CANONICAL)
        self.assertEqual(reverse.text, MARHETANA_SOURCE)
        self.assertEqual(reverse.occultans_resolutions, {(1, 3, "above"): "span"})
        self.assertEqual(
            transliterate_text(MARHETANA_SOURCE, reverse.occultans_resolutions).text,
            MARHETANA_CANONICAL,
        )

    def test_span_and_two_separate_lines_share_unicode_but_not_page_metadata(self):
        span = reverse_transliterate(MARHETANA_CANONICAL)
        separate = reverse_transliterate(SEPARATE_CANONICAL)

        self.assertEqual(span.text, separate.text)
        self.assertEqual(span.text, MARHETANA_SOURCE)
        self.assertEqual(span.occultans_resolutions[(1, 3, "above")], "span")
        self.assertEqual(separate.occultans_resolutions[(1, 3, "above")], "separate")

        self.assertEqual(
            transliterate_text(MARHETANA_SOURCE, span.occultans_resolutions).text,
            MARHETANA_CANONICAL,
        )
        self.assertEqual(
            transliterate_text(MARHETANA_SOURCE, separate.occultans_resolutions).text,
            SEPARATE_CANONICAL,
        )


if __name__ == "__main__":
    unittest.main()
