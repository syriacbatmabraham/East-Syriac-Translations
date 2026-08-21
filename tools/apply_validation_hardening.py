#!/usr/bin/env python3
"""One-shot patch helper for the validation-hardening branch.

This file is removed after the branch patch has been applied. It exists only so
GitHub Actions can make exact, reviewable edits in the repository checkout.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{relative}: expected exactly one patch target, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


replace_once(
    "tools/east_syriac/glossary.py",
    'ROOT_COMPONENT_RE = re.compile(r"^[A-Za-zʾʿ]+(?:-[A-Za-zʾʿ]+)*\\??$")',
    'ROOT_COMPONENT_RE = re.compile(r"^[A-Za-zʾʿḥṭṣš]+(?:-[A-Za-zʾʿḥṭṣš]+)*\\??$")',
)

replace_once(
    "rules/General-Rules.md",
    "12. Carrier discipline — each mark carries the codepoint that names what the carrier makes it (Translit §7): U+0741 and U+0742 only on bgdkpt, U+073C only on waw and yodh, U+073F only on waw, U+0323 and U+0307 never on bgdkpt; U+035E/U+035F only begin a two-letter span with an immediately following base in the same orthographic word",
    "12. Carrier discipline — carrier-bound semantic marks remain on valid carriers: U+0741 and U+0742 only on bgdkpt, U+073C only on waw and yodh, and U+073F only on waw. U+0307 and U+0323 are generic §7 points and remain valid on any carrier, including bgdkpt, waw, and yodh; the carrier never changes their identity. U+035E/U+035F only begin a two-letter span with an immediately following base in the same orthographic word",
)

replace_once(
    "tools/east_syriac/confirmed_text.py",
    '''        try:\n            expected_display = transliterate_text(syriac).text\n        except TransliterationError:\n            expected_display = None\n        expected_lines.append(expected_display)''',
    '''        try:\n            expected_display = transliterate_text(syriac).text\n        except TransliterationError as exc:\n            # Core comparison excludes literal editorial labels.  The storage\n            # line must nevertheless be representable as a complete canonical\n            # display.  A label such as literal `(h)` collides with reserved\n            # one-letter-line syntax and therefore blocks confirmation rather\n            # than yielding ok=True with no derived transliteration.\n            issues.append(\n                ConfirmedTextIssue(\n                    "unrepresentable-editorial-apparatus",\n                    "Full Syriac storage line cannot be mechanically represented "\n                    f"in canonical transliteration ({exc.code}): {exc.message}",\n                    line=index,\n                    block="syriac",\n                )\n            )\n            expected_display = None\n        expected_lines.append(expected_display)''',
)

replace_once(
    "tools/tests/test_confirmed_text.py",
    '''    def test_invalid_utf8_is_reported(self):\n        result = check_confirmed_text_bytes(b"\\xff\\xfe", "sample.txt")''',
    '''    def test_ambiguous_editorial_label_blocks_confirmation(self):\n        text = make_file(\n            "(h) ܐܒ",\n            "(h) ʾb",\n            "(h) one",\n        )\n        result = check_confirmed_text(text, "sample.txt")\n        self.assertFalse(result.ok)\n        self.assertIn(\n            "unrepresentable-editorial-apparatus",\n            [issue.code for issue in result.issues],\n        )\n        self.assertIsNone(result.expected_transliteration_block)\n\n    def test_invalid_utf8_is_reported(self):\n        result = check_confirmed_text_bytes(b"\\xff\\xfe", "sample.txt")''',
)

replace_once(
    ".github/workflows/tools-tests.yml",
    '''      - name: Check confirmed corpus\n        run: python tools/check_confirmed_text.py confirmed-texts\n''',
    '''      - name: Check confirmed corpus\n        run: python tools/check_confirmed_text.py confirmed-texts\n      - name: Check glossary and corpus\n        run: python tools/check_glossary.py\n''',
)

replace_once(
    "tools/README.md",
    "7. **Glossary/corpus checks** — remainder of General Rules §11.",
    "7. **Glossary/corpus checks** — `check_glossary.py` implements General Rules §11.1–10 and the Glossary-facing round-trip/injectivity checks of §11.11–14; the live corpus test and CI run it on every tooling change.",
)
