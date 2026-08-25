#!/usr/bin/env python3
"""CLI for deterministic East Syriac source-ingestion normalization."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from east_syriac.inspection import format_page_state_report, inspect_normalized_text
from east_syriac.normalization import normalize_text
from east_syriac.transliteration import TransliterationError, transliterate_text


NONBLOCKING_PAGE_STATE_ISSUES = frozenset({"multiple-vowels-on-carrier"})


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize a raw East Syriac source block according to Transliteration "
            "Rules §16 and §5.1, then print a mandatory letter-by-letter page-state "
            "audit. The input is Syriac-layer text, not a complete three-block "
            "confirmed-text file."
        )
    )
    parser.add_argument("source", help="UTF-8 Syriac file, or '-' for stdin")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("-o", "--output", help="write normalized text to this file")
    destination.add_argument("--in-place", action="store_true", help="replace SOURCE atomically")
    destination.add_argument(
        "--check",
        action="store_true",
        help="write nothing; exit 0 if already normalized, 1 if changes are needed, 2 if blocking flags/issues exist",
    )
    parser.add_argument(
        "--report-changes",
        action="store_true",
        help="print deterministic normalization changes to stderr",
    )
    return parser


def _read(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    with Path(source).open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _write_atomic(path: Path, text: str) -> None:
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(text, encoding="utf-8", newline="\n")
    temp.replace(path)


def _print_flags(result) -> None:
    for flag in result.flags:
        print(
            f"FLAG {flag.code} at {flag.line}:{flag.column}: "
            f"{flag.codepoint} {flag.unicode_name} — {flag.message}",
            file=sys.stderr,
        )


def _print_page_state_issues(audit) -> None:
    for issue in audit.issues:
        print(
            f"PAGE-STATE ISSUE {issue.code} at word {issue.word}, letter {issue.letter}: "
            f"{issue.codepoint} — {issue.message}",
            file=sys.stderr,
        )


def _print_page_state_notices(audit) -> None:
    for notice in audit.notices:
        print(
            f"PAGE CHECK {notice.code} at word {notice.word}, letter {notice.letter}: "
            f"{notice.codepoint} — {notice.message}",
            file=sys.stderr,
        )


def _blocking_page_state_issues(audit):
    return tuple(
        issue for issue in audit.issues
        if issue.code not in NONBLOCKING_PAGE_STATE_ISSUES
    )


def _word_labels(normalized: str, result, audit) -> tuple[str, ...] | None:
    if result.flags or _blocking_page_state_issues(audit) or audit.notices:
        return None
    try:
        return transliterate_text(normalized).word_labels
    except TransliterationError as exc:
        # This is intentionally visible: a clean normalized page-state can still
        # expose a canonical-grammar ambiguity such as an editorial label `(h)`.
        print(
            f"TRANSLITERATION CHECK {exc.code}: canonical audit headers deferred — {exc.message}",
            file=sys.stderr,
        )
        return None


def _print_page_state_report(text: str, labels: tuple[str, ...] | None) -> None:
    report = format_page_state_report(text, labels)
    print("PAGE-STATE AUDIT", file=sys.stderr)
    if report:
        print(report, file=sys.stderr)
    else:
        print("(no Syriac words found)", file=sys.stderr)


def _print_changes(result) -> None:
    for change in result.changes:
        before = " ".join(f"U+{ord(ch):04X}" for ch in change.before) or "∅"
        after = " ".join(f"U+{ord(ch):04X}" for ch in change.after) or "∅"
        print(f"CHANGE {change.code} at index {change.index}: {before} -> {after}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    if args.in_place and args.source == "-":
        print("error: --in-place requires a file path, not stdin", file=sys.stderr)
        return 2

    try:
        original = _read(args.source)
    except (OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result = normalize_text(original)
    audit = inspect_normalized_text(result.text)
    blocking_issues = _blocking_page_state_issues(audit)

    _print_flags(result)
    _print_page_state_issues(audit)
    _print_page_state_notices(audit)
    labels = _word_labels(result.text, result, audit)
    _print_page_state_report(result.text, labels)
    if args.report_changes:
        _print_changes(result)

    if args.check:
        if result.flags or blocking_issues:
            return 2
        return 1 if result.text != original else 0

    # Page-only notices and the verified two-vowel audit diagnostic do not make
    # the encoded Syriac structurally invalid. Other page-state issues remain
    # blocking until corrected or explicitly represented by the canonical grammar.
    if (result.flags or blocking_issues) and (args.in_place or args.output):
        print("error: refusing to write input with unresolved flags/page-state issues; review the source first", file=sys.stderr)
        return 2

    if args.in_place:
        path = Path(args.source)
        try:
            _write_atomic(path, result.text)
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.output:
        try:
            Path(args.output).write_text(result.text, encoding="utf-8", newline="\n")
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        return 0

    sys.stdout.write(result.text)
    return 2 if result.flags or blocking_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())