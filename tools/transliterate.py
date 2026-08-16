#!/usr/bin/env python3
"""CLI for reversible canonical East Syriac transliteration."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from east_syriac.inspection import format_page_state_report
from east_syriac.transliteration import TransliterationError, transliterate_text
from east_syriac.transliteration_inverse import reverse_transliterate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Transliterate clean normalized East Syriac to the reversible canonical "
            "Latin system, or reverse a canonical string back to normalized Syriac. "
            "Two-letter spans are encoded directly in Syriac with U+035E/U+035F."
        )
    )
    parser.add_argument("source", help="UTF-8 input file, or '-' for stdin")
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="canonical transliteration -> normalized Syriac",
    )
    return parser


def _read(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        text = _read(args.source)
        if args.reverse:
            result = reverse_transliterate(text)
            sys.stdout.write(result.text)
            return 0

        result = transliterate_text(text)
        print("PAGE-STATE AUDIT", file=sys.stderr)
        report = format_page_state_report(text, result.word_labels)
        print(report if report else "(no Syriac words found)", file=sys.stderr)
        sys.stdout.write(result.text)
        return 0
    except (OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except TransliterationError as exc:
        print(f"TRANSLITERATION ERROR {exc.code}: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
