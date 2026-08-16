from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class MarhetanaRepositoryMigrationTests(unittest.TestCase):
    def test_confirmed_and_glossary_data_use_direct_span_encoding(self):
        confirmed = (ROOT / "confirmed-texts" / "Our_Father.txt").read_text(encoding="utf-8")
        glossary = (ROOT / "glossary" / "Glossary.md").read_text(encoding="utf-8")

        old_syriac = "ܫܒܲܩ̣" + "݇" + "ܢ" + "݇"
        old_latin = "šba" + "(q_n)"
        new_syriac = "ܫܒܲܩ̣͞ܢ"
        new_latin = "šbaq_⁀n"

        for name, text in (("Our Father", confirmed), ("Glossary", glossary)):
            with self.subTest(file=name):
                self.assertNotIn(old_syriac, text)
                self.assertNotIn(old_latin, text)
                self.assertIn(new_syriac, text)
                self.assertIn(new_latin, text)

    def test_temporary_migration_workflow_is_gone(self):
        self.assertFalse((ROOT / ".github" / "workflows" / "migrate-marhetana-glossary.yml").exists())


if __name__ == "__main__":
    unittest.main()
