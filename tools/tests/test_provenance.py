from __future__ import annotations

import sys
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from east_syriac.provenance import check_source_registry, parse_source_registry


REGISTRY = """\
source_records:
  hours:
    title: Hours
    governs: Hours
  qurbana:
    title: Qurbana
    governs: Qurbana

confirmed_texts:
  Our_Father.txt:
    citation_label: Our Father
    source_of_record: hours
  Creed.txt:
    citation_label: Creed
    source_of_record: qurbana
    editorial_apparatus:
      - line: 17
        witness_label: Catholic
        reading: "[waḇrā]"
"""


class ProvenanceTests(unittest.TestCase):
    def test_clean_registry_matches_corpus(self):
        issues = check_source_registry(REGISTRY, {"Our_Father.txt", "Creed.txt"})
        self.assertEqual(issues, ())

    def test_nested_editorial_apparatus_does_not_require_separate_source_record(self):
        registry = parse_source_registry(REGISTRY)
        self.assertEqual(
            {entry.filename for entry in registry.confirmed_texts},
            {"Our_Father.txt", "Creed.txt"},
        )

    def test_missing_provenance_is_reported(self):
        issues = check_source_registry(REGISTRY, {"Our_Father.txt", "Creed.txt", "Extra.txt"})
        self.assertIn("missing-provenance", [issue.code for issue in issues])

    def test_stale_provenance_is_reported(self):
        issues = check_source_registry(REGISTRY, {"Our_Father.txt"})
        self.assertIn("stale-provenance", [issue.code for issue in issues])

    def test_unknown_source_record_is_reported(self):
        text = REGISTRY.replace("source_of_record: qurbana", "source_of_record: missing")
        issues = check_source_registry(text, {"Our_Father.txt", "Creed.txt"})
        self.assertIn("unknown-source-of-record", [issue.code for issue in issues])

    def test_missing_citation_label_is_reported(self):
        text = REGISTRY.replace("    citation_label: Creed\n", "")
        issues = check_source_registry(text, {"Our_Father.txt", "Creed.txt"})
        self.assertIn("missing-citation-label", [issue.code for issue in issues])

    def test_duplicate_citation_label_is_reported(self):
        text = REGISTRY.replace("citation_label: Creed", "citation_label: Our Father")
        issues = check_source_registry(text, {"Our_Father.txt", "Creed.txt"})
        self.assertIn("duplicate-citation-label", [issue.code for issue in issues])

    def test_tab_indentation_is_rejected(self):
        issues = check_source_registry("source_records:\n\thours:\nconfirmed_texts:\n", set())
        self.assertEqual([issue.code for issue in issues], ["tab-indentation"])


if __name__ == "__main__":
    unittest.main()
