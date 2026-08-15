from __future__ import annotations

import re
import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.transliteration import transliterate_text
from east_syriac.transliteration_inverse import reverse_transliterate


def _three_blocks(path: Path) -> tuple[str, str, str]:
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n{2,}", text.strip("\n"))
    if len(blocks) != 3:
        raise AssertionError(
            f"{path}: expected exactly three blocks separated by blank lines; got {len(blocks)}"
        )
    return blocks[0], blocks[1], blocks[2]


class ConfirmedCorpusTransliterationTests(unittest.TestCase):
    def test_every_confirmed_text_is_exactly_reversible(self):
        files = sorted((ROOT / "confirmed-texts").glob("*.txt"))
        self.assertTrue(files, "confirmed-texts corpus is empty")

        for path in files:
            with self.subTest(file=path.name):
                syriac, canonical, english = _three_blocks(path)
                self.assertEqual(
                    len(syriac.splitlines()),
                    len(canonical.splitlines()),
                    f"{path.name}: Syriac/transliteration line count differs",
                )
                self.assertEqual(
                    len(canonical.splitlines()),
                    len(english.splitlines()),
                    f"{path.name}: transliteration/English line count differs",
                )

                # Reverse the already-confirmed canonical block first. This both
                # proves its grammar and recovers the page-only span/separate
                # occultans decisions that encoded Syriac cannot contain.
                reverse = reverse_transliterate(canonical)
                self.assertEqual(
                    reverse.text,
                    syriac,
                    f"{path.name}: canonical block does not reconstruct Syriac exactly",
                )

                # Then regenerate the canonical block mechanically from Syriac,
                # supplying only those page-only occultans decisions.
                forward = transliterate_text(syriac, reverse.occultans_resolutions)
                self.assertEqual(
                    forward.text,
                    canonical,
                    f"{path.name}: mechanical forward transliteration differs from confirmed block",
                )


if __name__ == "__main__":
    unittest.main()
