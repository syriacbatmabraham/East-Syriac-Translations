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
            "Latin system, or reverse a canonical string back to normalized Syriac."
        )
    )
    parser.add_argument("source", help="UTF-8 input file, or '-' for stdin")
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="canonical transliteration -> normalized Syriac",
    )
    parser.add_argument(
        "--occultans-span",
        action="append",
        default=[],
        metavar="WORD:LETTER:above|below",
        help="page confirms one occultans line spanning this letter and the next",
    )
    parser.add_argument(
        "--occultans-separate",
        action="append",
        default=[],
        metavar="WORD:LETTER:above|below",
        help="page confirms separate occultans lines on this letter and the next",
    )
    return parser


def _read(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def _resolution_key(value: str) -> tuple[int, int, str]:
    try:
        word_text, letter_text, direction = value.split(":", 2)
        word = int(word_text)
        letter = int(letter_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid occultans coordinate {value!r}; expected WORD:LETTER:above|below"
        ) from exc
    if word < 1 or letter < 1 or direction not in {"above", "below"}:
        raise argparse.ArgumentTypeError(
            f"invalid occultans coordinate {value!r}; expected positive WORD/LETTER and above|below"
        )
    return word, letter, direction


def _resolutions(args: argparse.Namespace) -> dict[tuple[int, int, str], str]:
    out: dict[tuple[int, int, str], str] = {}
    for value, decision in (
        *((value, "span") for value in args.occultans_span),
        *((value, "separate") for value in args.occultans_separate),
    ):
        key = _resolution_key(value)
        if key in out and out[key] != decision:
            raise argparse.ArgumentTypeError(
                f"conflicting occultans decisions supplied for {key!r}"
            )
        out[key] = decision
    return out


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        text = _read(args.source)
        if args.reverse:
            if args.occultans_span or args.occultans_separate:
                parser.error("occultans resolution options apply only to forward transliteration")
            result = reverse_transliterate(text)
            sys.stdout.write(result.text)
            return 0

        resolutions = _resolutions(args)
        result = transliterate_text(text, resolutions)
        print("PAGE-STATE AUDIT", file=sys.stderr)
        report = format_page_state_report(text, result.word_labels)
        print(report if report else "(no Syriac words found)", file=sys.stderr)
        sys.stdout.write(result.text)
        return 0
    except (OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except argparse.ArgumentTypeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except TransliterationError as exc:
        print(f"TRANSLITERATION ERROR {exc.code}: {exc.message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
