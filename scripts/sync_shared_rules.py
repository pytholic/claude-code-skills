#!/usr/bin/env python3
"""Keep shared rule blocks in sync across skills.

Canonical text lives in shared/<rule>.md. Copies elsewhere are delimited by
    <!-- BEGIN shared: <rule> --> ... <!-- END shared: <rule> -->

Usage:
    sync_shared_rules.py --check   # exit 1 if any copy drifted
    sync_shared_rules.py --fix     # rewrite drifted copies from canonical
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared"


def _pattern(rule: str) -> re.Pattern[str]:
    name = re.escape(rule)
    return re.compile(
        rf"(<!-- BEGIN shared: {name} -->\n)(.*?)(<!-- END shared: {name} -->)",
        re.DOTALL,
    )


def _canonical(path: Path) -> tuple[str, str]:
    """Return (rule name, canonical body) for a shared/<rule>.md file."""
    rule = path.stem
    match = _pattern(rule).search(path.read_text())
    if not match:
        sys.exit(f"error: {path} has no '{rule}' markers")
    return rule, match.group(2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="report drift, exit 1 if any")
    group.add_argument("--fix", action="store_true", help="rewrite copies from canonical")
    args = parser.parse_args()

    if not SHARED.is_dir():
        sys.exit(f"error: no shared/ directory at {SHARED}")

    drifted: list[str] = []
    copies = 0

    for shared_file in sorted(SHARED.glob("*.md")):
        rule, canonical = _canonical(shared_file)
        pattern = _pattern(rule)

        for target in sorted(ROOT.rglob("*.md")):
            if target == shared_file or ".git" in target.parts:
                continue
            text = target.read_text()
            match = pattern.search(text)
            if not match:
                continue
            copies += 1
            if match.group(2) == canonical:
                continue

            drifted.append(f"{target.relative_to(ROOT)} [{rule}]")
            if args.fix:
                fixed = pattern.sub(lambda m: m.group(1) + canonical + m.group(3), text)
                target.write_text(fixed)

    if not drifted:
        print(f"ok: {copies} shared-rule copies in sync")
        return 0

    verb = "synced" if args.fix else "drifted"
    print(f"{len(drifted)} of {copies} copies {verb}:", file=sys.stderr)
    for entry in drifted:
        print(f"  {entry}", file=sys.stderr)
    if args.fix:
        return 0
    print("\nrun with --fix to propagate from shared/", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
