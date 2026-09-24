from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.confirmed_text import ConfirmedTextDocument
from east_syriac.glossary import _derive_search_key, _rendering_traceable, check_glossary, check_glossary_path
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

    def test_check_03_rendering_count(self):
        corrupted = BASE.replace("ʾaḇā (1) — Father (1)", "ʾaḇā (2) — Father (2)")
        self.assertIn("entry-rendering-count-mismatch", self.codes(corrupted))

    def test_check_03_plus_count_is_invalid(self):
        corrupted = BASE.replace("Father (1)", "Father (1+1)", 1)
        self.assertIn("glossary-rendering-format", self.codes(corrupted))

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

    def test_check_08_rendering_traceability_ignores_apparatus_brackets(self):
        self.assertTrue(_rendering_traceable("Your Truth", ["...in [Your] Truth"]))
        self.assertTrue(_rendering_traceable("[Your] Truth", ["...in Your Truth"]))
        self.assertFalse(_rendering_traceable("Your Truth", ["...in Your grace"]))

    def test_check_09_morphology_structure(self):
        corrupted = BASE.replace("{noun m.sg.emph.}", "{noun m.sg.}", 1)
        self.assertIn("invalid-morphology-field", self.codes(corrupted))

    def test_check_09_state_unspecified_noun_is_valid(self):
        explicit = BASE.replace(
            "{noun m.sg.emph.}",
            "{noun m.sg.state-unspecified.}",
            1,
        )
        self.assertNotIn("invalid-morphology-field", self.codes(explicit))

    def test_check_09_root_structure(self):
        corrupted = BASE.replace("[ʾ-b]", "[noun m.sg.emph.]", 1)
        self.assertIn("invalid-root-field", self.codes(corrupted))

    def test_search_key_is_deterministically_derived(self):
        cases = {
            "ʿḇāḋ̈ē": "bade",
            "ʿ_naytāny": "naytany",
            "p^ārōqā": "paroqa",
            "šbaq_⁀n": "shbaqn",
            "ʾīšōʿ": "isho",
            "ḥaḏ bšaḇʿā": "had bshaba",
        }
        for canonical, expected in cases.items():
            with self.subTest(canonical=canonical):
                self.assertEqual(_derive_search_key(canonical), expected)

    def test_search_key_mismatch_is_rejected(self):
        corrupted = BASE.replace("(search: aba)", "(search: wrong)", 1)
        self.assertIn("invalid-search-key", self.codes(corrupted))

    def test_check_10a_context_literal_span(self):
        corrupted = BASE.replace('"...good"', '"...kind"')
        self.assertIn("context-not-in-line", self.codes(corrupted))

    def test_check_10b_context_overlap(self):
        corrupted = BASE.replace('"...good"', '"...Father is good"')
        self.assertIn("overlapping-contexts", self.codes(corrupted))


class PhraseOccurrenceTests(unittest.TestCase):
    PHRASE = '''# Glossary

## Phrases

ܕܵܪ ܕܵܪ̈ܝܼܢ   [d-w-r + d-w-r]   {noun phrase}   (search: dar darin)
dār dār̈īn (1) — generations upon generations (1)
* walḏārdār̈īn · "And unto generations upon generations" (Sample Line 1)

## Forms
'''

    def check(self, text=None, attested="walḏārdār̈īn"):
        documents = {"Sample.txt": ConfirmedTextDocument(
            (" ".join(["ܕܵܪ"] * len(attested.split())),), (attested,),
            ("And unto generations upon generations",))}
        return check_glossary(self.PHRASE if text is None else text, documents, REGISTRY)

    def test_solid_occurrence_covers_text_without_matching_spaced_headword(self):
        result = self.check()
        self.assertTrue(result.ok, result.issues)

    def test_spaced_occurrence_covers_all_components(self):
        result = self.check(self.PHRASE.replace("* walḏārdār̈īn", "* walḏār dār̈īn"),
                            "walḏār dār̈īn")
        self.assertTrue(result.ok, result.issues)

    def test_headword_does_not_substitute_for_wrong_occurrence(self):
        result = self.check(self.PHRASE.replace("* walḏārdār̈īn", "* dār dār̈īn"))
        self.assertIn("attested-form-not-in-line", {i.code for i in result.issues})
        self.assertIn("missing-corpus-occurrence", {i.code for i in result.issues})

    def test_duplicate_solid_occurrence_is_rejected(self):
        text = self.PHRASE.replace("(1)", "(2)")
        text = text.replace("\n## Forms", '* walḏārdār̈īn · "And unto generations upon generations" (Sample Line 1)\n\n## Forms')
        self.assertIn("orphan-glossary-occurrence", {i.code for i in self.check(text).issues})

    def test_phrase_component_overlap_is_rejected_in_either_order(self):
        component = '''
ܕܵܪ̈ܝܼܢ   [d-w-r]   {noun m.pl.abs.}   (search: darin)
dār̈īn (1) — generations (1)
* dār̈īn · "And unto generations upon generations" (Sample Line 1)
'''
        phrase = self.PHRASE.replace("* walḏārdār̈īn", "* walḏār dār̈īn")
        for text in (phrase + component, "## Forms\n" + component + phrase):
            result = self.check(text, "walḏār dār̈īn")
            self.assertIn("overlapping-glossary-occurrences", {i.code for i in result.issues})

    def test_legacy_component_pointer_is_rejected(self):
        text = BASE.replace("— Father (1)", "— → example phrase (1)")
        result = check_glossary(text, DOCS, REGISTRY)
        self.assertIn("duplicate-phrase-component-entry", {i.code for i in result.issues})

    def test_independent_component_on_same_line_remains_available(self):
        component = '''
ܕܵܪ̈ܝܼܢ   [d-w-r]   {noun m.pl.abs.}   (search: darin)
dār̈īn (1) — generations (1)
* dār̈īn · "And unto generations upon generations" (Sample Line 1)
'''
        phrase = self.PHRASE.replace("* walḏārdār̈īn", "* walḏār dār̈īn")
        for text in (phrase + component, "## Forms\n" + component + phrase):
            result = self.check(text, "walḏār dār̈īn dār̈īn")
            self.assertTrue(result.ok, result.issues)


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
