#!/usr/bin/env python3
"""Validate the authoritative Glossary against the confirmed corpus."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from east_syriac.glossary import check_glossary_path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOSSARY = PROJECT_ROOT / "glossary" / "Glossary.md"
DEFAULT_CONFIRMED = PROJECT_ROOT / "confirmed-texts"
DEFAULT_REGISTRY = PROJECT_ROOT / "sources" / "sources.yaml"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run General Rules §11 Glossary/corpus validation: Unicode hygiene, "
            "count arithmetic, bidirectional corpus coverage, entry identity, "
            "attested-form/citation checks, rendering traceability, morphology/root "
            "structure, context-span discipline, and Glossary headword round trips."
        )
    )
    parser.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY)
    parser.add_argument("--confirmed-dir", type=Path, default=DEFAULT_CONFIRMED)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = check_glossary_path(args.glossary, args.confirmed_dir, args.registry)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if result.ok:
        print(f"OK {args.glossary} ({len(result.entries)} entries; confirmed corpus reconciled)")
        return 0

    for issue in result.issues:
        location = str(args.glossary)
        if issue.line is not None:
            location += f":{issue.line}"
        if issue.entry is not None:
            location += f" [{issue.entry}]"
        print(f"{location}: {issue.code}: {issue.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
