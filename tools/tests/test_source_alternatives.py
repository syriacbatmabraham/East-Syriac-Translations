from __future__ import annotations

import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS)) if str(TOOLS) not in sys.path else None

from east_syriac.confirmed_text import ConfirmedTextDocument, check_confirmed_text
from east_syriac.glossary import check_glossary
from east_syriac.provenance import (
    SourceAlternative, SourceRegistry, ConfirmedTextProvenance,
    parse_source_registry, check_source_registry, check_source_registry_path,
)
from east_syriac.transliteration import transliterate_text
from east_syriac.transliteration_inverse import reverse_transliterate

GLOSSARY = '''## Forms

ܐܲܒ݂ܵܐ   [ʾ-b]   {noun m.sg.emph.}   (search: aba)
ʾaḇā (1) — Father (1)
* ʾaḇā · "The Father..." (Sample Line 1)

ܛܵܒ݂ܵܐ   [ṭ-w-b]   {adj. m.sg.emph.}   (search: taba)
ṭāḇā (1) — good (1)
* ṭāḇā · "...[good]" (Sample Line 1)
'''
DOCUMENT = ConfirmedTextDocument(
    ('ܐܲܒ݂ܵܐ [ܛܵܒ݂ܵܐ]',), ('ʾaḇā [ṭāḇā]',), ('The Father is [good] [indeed]',))
ALTERNATIVE = SourceAlternative(1, 1, 'Seasonal', '[ṭāḇā]')
REGISTRY_TEXT = '''source_records:
  sample:
    title: Sample
confirmed_texts:
  Sample.txt:
    citation_label: Sample
    source_of_record: sample
    source_alternatives:
      - line: 1
        bracket: 1
        label: Seasonal
        reading: "[ṭāḇā]"
'''


def registry(*alternatives):
    return SourceRegistry(frozenset({'sample'}), (
        ConfirmedTextProvenance('Sample.txt', 'Sample', 'sample', alternatives),))


def check(doc=DOCUMENT, glossary=GLOSSARY, alternatives=(ALTERNATIVE,)):
    return check_glossary(glossary, {'Sample.txt': doc}, registry(*alternatives))


class SourceAlternativeTests(unittest.TestCase):
    def test_declared_alternative_is_indexed_and_english_supplement_excluded(self):
        result = check()
        self.assertTrue(result.ok, result.issues)

    def test_undeclared_brackets_still_require_witness(self):
        result = check(alternatives=())
        self.assertIn('apparatus-occurrence-missing-witness', {i.code for i in result.issues})

    def test_legacy_witness_citation_still_passes(self):
        result = check(glossary=GLOSSARY.replace('"...[good]" (Sample', '"...[good]" (Assyrian Sample'), alternatives=())
        self.assertTrue(result.ok, result.issues)

    def test_source_alternative_rejects_external_witness_qualifier(self):
        result = check(glossary=GLOSSARY.replace('"...[good]" (Sample', '"...[good]" (Assyrian Sample'))
        self.assertIn('source-alternative-has-witness', {i.code for i in result.issues})

    def test_bad_location_or_reading_cannot_bypass_witness_check(self):
        for alt in (replace(ALTERNATIVE, line=2), replace(ALTERNATIVE, bracket=2), replace(ALTERNATIVE, reading='[ʾaḇā]')):
            with self.subTest(alt=alt):
                codes = {i.code for i in check(alternatives=(alt,)).issues}
                self.assertIn('source-alternative-mismatch', codes)
                self.assertIn('apparatus-occurrence-missing-witness', codes)

    def test_declaration_does_not_exempt_other_group_on_same_line(self):
        doc = ConfirmedTextDocument(('[ܐܲܒ݂ܵܐ] [ܛܵܒ݂ܵܐ]',), ('[ʾaḇā] [ṭāḇā]',), ('[The Father] is [good]',))
        result = check(doc=doc, alternatives=(replace(ALTERNATIVE, bracket=2),))
        errors = [i for i in result.issues if i.code == 'apparatus-occurrence-missing-witness']
        self.assertEqual([i.entry for i in errors], ['ʾaḇā'])

    def test_alternative_word_requires_occurrence_even_if_same_word_precedes_it(self):
        doc = ConfirmedTextDocument(('ܐܲܒ݂ܵܐ ܛܵܒ݂ܵܐ [ܐܲܒ݂ܵܐ]',), ('ʾaḇā ṭāḇā [ʾaḇā]',), ('The Father is good [Father]',))
        result = check(doc=doc, alternatives=(replace(ALTERNATIVE, reading='[ʾaḇā]'),))
        self.assertIn('missing-corpus-occurrence', {i.code for i in result.issues})

    def test_registry_parses_category_and_rejects_invalid_declarations(self):
        parsed = parse_source_registry(REGISTRY_TEXT)
        self.assertEqual(parsed.confirmed_texts[0].source_alternatives, (ALTERNATIVE,))
        for old, new in [('line: 1', 'line: 0'), ('bracket: 1', 'bracket: x'), ('label: Seasonal', 'label:'), ('reading: "[ṭāḇā]"', 'reading: ṭāḇā'), ('bracket: 1', 'unexpected: 1')]:
            with self.subTest(new=new):
                issues = check_source_registry(REGISTRY_TEXT.replace(old, new), {'Sample.txt'})
                self.assertIn('invalid-source-alternative', {i.code for i in issues})
        repeated = REGISTRY_TEXT + REGISTRY_TEXT[REGISTRY_TEXT.index('      - line:'):]
        self.assertIn('invalid-source-alternative', {i.code for i in check_source_registry(repeated, {'Sample.txt'})})

    def test_registry_path_rejects_stale_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'Sample.txt').write_text('ܐܲܒ݂ܵܐ [ܛܵܒ݂ܵܐ]\n\nʾaḇā [ṭāḇā]\n\nThe Father is [good]\n')
            reg = root/'sources.yaml'
            reg.write_text(REGISTRY_TEXT)
            self.assertEqual(check_source_registry_path(reg, root), ())
            reg.write_text(REGISTRY_TEXT.replace('[ṭāḇā]', '[ʾaḇā]'))
            self.assertIn('source-alternative-mismatch', {i.code for i in check_source_registry_path(reg, root)})

    def test_bracketed_alternative_round_trips_with_editorial_label(self):
        syriac = "(Qanona) ܠܲܢ [ܐܵܘ ܕܐܸܬ݂͟ܥܡܸܕ݂ ܠܲܢ]"
        latin = transliterate_text(syriac).text
        self.assertEqual(reverse_transliterate(latin).text, syriac)
        result = check_confirmed_text(syriac+'\n\n'+latin+'\n\n(Qanona) To us [or who was baptized to us]\n')
        self.assertTrue(result.ok, result.issues)
        label = '(Assyrian:)'
        self.assertEqual(reverse_transliterate(label).text, label)


if __name__ == '__main__':
    unittest.main()
