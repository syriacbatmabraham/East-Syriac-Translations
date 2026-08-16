from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.confirmed_text import check_confirmed_text_path
from east_syriac.provenance import check_source_registry_path


class ConfirmedCorpusTransliterationTests(unittest.TestCase):
    def test_every_confirmed_text_passes_complete_checker(self):
        files = sorted(
            path
            for path in (ROOT / "confirmed-texts").iterdir()
            if path.is_file() and path.suffix.lower() in {".txt", ".md"}
        )
        self.assertTrue(files, "confirmed-texts corpus is empty")

        for path in files:
            with self.subTest(file=path.name):
                result = check_confirmed_text_path(path)
                self.assertTrue(
                    result.ok,
                    "\n".join(
                        f"{issue.code}"
                        f"{' line ' + str(issue.line) if issue.line is not None else ''}: "
                        f"{issue.message}"
                        for issue in result.issues
                    ),
                )
                self.assertIsNotNone(result.document)
                self.assertIsNotNone(result.expected_transliteration_block)

    def test_confirmed_corpus_matches_source_registry(self):
        issues = check_source_registry_path(
            ROOT / "sources" / "sources.yaml",
            ROOT / "confirmed-texts",
        )
        self.assertFalse(
            issues,
            "\n".join(
                f"{issue.code}"
                f"{' ' + issue.filename if issue.filename is not None else ''}: "
                f"{issue.message}"
                for issue in issues
            ),
        )


if __name__ == "__main__":
    unittest.main()
