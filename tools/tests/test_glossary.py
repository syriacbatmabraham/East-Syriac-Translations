from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.confirmed_text import ConfirmedTextDocument
from east_syriac.glossary import check_glossary, check_glossary_path
from east_syriac.provenance import ConfirmedTextProvenance, SourceRegistry


BASE = """# Glossary

## Phrases

---

## Forms

ܐܲܒ݂ܵܐ   [ʾ-b]   {noun m.sg.emph.}   (search: aba)
ʾaḇā (1) — Father (1)
* ʾaḇā · \"The Father...\" (Sample Line 1)

ܛܵܒ݂ܵܐ   [ṭ-w-b]   {adj. m.sg.emph.}   (search: taba)
ṭāḇā (1) — good (1)
* ṭāḇā · \"...good\" (Sample Line 1)
"""

DOCS = {
    "Sample.txt": ConfirmedTextDocument(
        ("ܐܲܒ݂ܵܐ ܛܵܒ݂ܵܐ",),
        ("ʾaḇā ṭāḇā",),
        ("The Father is good",),
    )
}
REGISTRY = SourceRegistry(
    frozenset({"sample"}),
    (ConfirmedTextProvenance("Sample.txt", "Sample", "sample"),),
)


class GlossaryAdversarialChecks(unittest.TestCase):
    def codes(self, text: str) -> set[str]:
        return {issue.code for issue in check_glossary(text, DOCS, REGISTRY).issues}

    def test_clean_fixture_passes(self):
        result = check_glossary(BASE, DOCS, REGISTRY)
        self.assertTrue(result.ok, result.issues)

    def test_check_01_homoglyph(self):
        corrupted = BASE.replace("(search: aba)", "(search: аba)", 1)
        self.assertIn("glossary-homoglyph", self.codes(corrupted))

    def test_check_02_nfc(self):
        corrupted = "# a\u0304\n" + BASE
        self.assertIn("glossary-non-nfc", self.codes(corrupted))

    def test_check_03_base_count(self):
        corrupted = BASE.replace("ʾaḇā (1) — Father (1)", "ʾaḇā (2) — Father (2)")
        self.assertIn("entry-base-count-mismatch", self.codes(corrupted))

    def test_check_03_decision_total(self):
        corrupted = BASE.replace("ʾaḇā (1) — Father (1)", "ʾaḇā (2) — Father (1)")
        self.assertIn("entry-decision-total-mismatch", self.codes(corrupted))

    def test_check_04_missing_corpus_occurrence(self):
        second = """ܛܵܒ݂ܵܐ   [ṭ-w-b]   {adj. m.sg.emph.}   (search: taba)
ṭāḇā (1) — good (1)
* ṭāḇā · \"...good\" (Sample Line 1)
"""
        corrupted = BASE.replace(second, "")
        self.assertIn("missing-corpus-occurrence", self.codes(corrupted))

    def test_check_05_orphan_glossary_occurrence(self):
        corrupted = BASE.replace(
            '* ʾaḇā · "The Father..." (Sample Line 1)',
            '* ʾaḇā · "The Father..." (Sample Line 1)\n* ʾaḇā · "The Father..." (Sample Line 1)',
        ).replace("ʾaḇā (1) — Father (1)", "ʾaḇā (2) — Father (2)")
        self.assertIn("orphan-glossary-occurrence", self.codes(corrupted))

    def test_check_06_duplicate_identity(self):
        duplicate = """
ܐܲܒ݂ܵܐ   [ʾ-b]   {noun m.sg.emph.}   (search: aba)
ʾaḇā (0) — Father (0)
"""
        self.assertIn("duplicate-entry-identity", self.codes(BASE + duplicate))

    def test_check_07_attested_sequence(self):
        corrupted = BASE.replace('* ʾaḇā · "The Father..."', '* x · "The Father..."')
        self.assertIn("attested-form-not-in-line", self.codes(corrupted))

    def test_check_08_rendering_traceability(self):
        corrupted = BASE.replace("— Father (1)", "— Creator (1)")
        self.assertIn("rendering-not-traceable", self.codes(corrupted))

    def test_check_09_morphology_structure(self):
        corrupted = BASE.replace("{noun m.sg.emph.}", "{noun m.sg.}", 1)
        self.assertIn("invalid-morphology-field", self.codes(corrupted))

    def test_check_09_root_structure(self):
        corrupted = BASE.replace("[ʾ-b]", "[noun m.sg.emph.]", 1)
        self.assertIn("invalid-root-field", self.codes(corrupted))

    def test_check_10a_context_literal_span(self):
        corrupted = BASE.replace('"...good"', '"...kind"')
        self.assertIn("context-not-in-line", self.codes(corrupted))

    def test_check_10b_context_overlap(self):
        corrupted = BASE.replace('"...good"', '"...Father is good"')
        self.assertIn("overlapping-contexts", self.codes(corrupted))


class LiveGlossaryCorpusTests(unittest.TestCase):
    def test_authoritative_glossary_reconciles_with_confirmed_corpus(self):
        result = check_glossary_path(
            ROOT / "glossary" / "Glossary.md",
            ROOT / "confirmed-texts",
            ROOT / "sources" / "sources.yaml",
        )
        self.assertTrue(
            result.ok,
            "\n".join(
                f"{issue.code}{' line ' + str(issue.line) if issue.line else ''}: {issue.message}"
                for issue in result.issues
            ),
        )


if __name__ == "__main__":
    unittest.main()
