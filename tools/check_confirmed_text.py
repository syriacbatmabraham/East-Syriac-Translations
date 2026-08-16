#!/usr/bin/env python3
"""Validate confirmed East Syriac three-block text files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from east_syriac.confirmed_text import check_confirmed_text_path


ALLOWED_SUFFIXES = {".txt", ".md"}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check fixed three-block confirmed texts: UTF-8/LF/NFC hygiene, "
            "equal aligned blocks and stanza breaks, exact inverse round-trip, "
            "and mechanically derived transliteration from the Syriac block."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["confirmed-texts"],
        help="confirmed text file(s) or directories; default: confirmed-texts",
    )
    parser.add_argument(
        "--show-derived",
        action="store_true",
        help="print the mechanically derived transliteration block for files whose page-only state is fully resolved",
    )
    return parser


def _expand(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            found.extend(
                candidate
                for candidate in sorted(path.rglob("*"))
                if candidate.is_file() and candidate.suffix.lower() in ALLOWED_SUFFIXES
            )
        else:
            found.append(path)

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in found:
        key = path.resolve() if path.exists() else path.absolute()
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def _format_issue(path: Path, issue) -> str:
    location = str(path)
    if issue.block is not None:
        location += f":{issue.block}"
    if issue.line is not None:
        location += f":{issue.line}"
    return f"{location}: {issue.code}: {issue.message}"


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    paths = _expand(args.paths)
    if not paths:
        print("error: no confirmed .txt/.md files found", file=sys.stderr)
        return 2

    failed = False
    for path in paths:
        try:
            result = check_confirmed_text_path(path)
        except OSError as exc:
            print(f"{path}: file-error: {exc}", file=sys.stderr)
            failed = True
            continue

        if result.ok:
            count = result.document.line_count if result.document is not None else 0
            print(f"OK {path} ({count} aligned lines)")
        else:
            failed = True
            for issue in result.issues:
                print(_format_issue(path, issue), file=sys.stderr)

        if args.show_derived:
            derived = result.expected_transliteration_block
            if derived is None:
                print(
                    f"{path}: derived transliteration unavailable until blocking/page-only issues are resolved",
                    file=sys.stderr,
                )
            else:
                print(f"--- {path} derived transliteration ---")
                print(derived)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
