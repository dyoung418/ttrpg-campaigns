#!/usr/bin/env python3
"""Append an entry to a note's `sources:` list. Idempotent.

Usage:
  vault-add-source.py <note.md> <source-entry> [<source-entry> ...]

A source entry is typically a wikilink to a file under _sources/, e.g.
  '[[_sources/processed/roleplay/RP10 ...|RP10 — ...]]'
but any string is accepted (URLs, book citations). An entry already present
(exact match, or same wikilink target ignoring the |alias) is skipped.
Policy: _meta/conventions.md §1 — `sources` is always a list.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vaultlib as vl


def link_target(entry: str) -> str:
    """Comparison key: the wikilink target without alias, else the raw string."""
    e = entry.strip()
    if e.startswith("[[") and e.endswith("]]"):
        return e[2:-2].split("|")[0].strip().lower()
    return e.lower()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("note", type=Path)
    ap.add_argument("entries", nargs="+")
    args = ap.parse_args()

    vault = vl.vault_root()
    note = args.note.resolve()
    if not note.is_file():
        raise SystemExit(f"note not found: {note}")
    try:
        rel = note.relative_to(vault)
    except ValueError:
        raise SystemExit(f"note is outside the vault: {note}")

    text = note.read_text(encoding="utf-8")
    fm, rest = vl.split_frontmatter(text)
    if fm is None:
        raise SystemExit(f"{rel} has no frontmatter; refusing to invent one")

    sources = vl.get_list_field(fm, "sources") or []
    have = {link_target(s) for s in sources}
    added = []
    for entry in args.entries:
        if link_target(entry) in have:
            print(f"already present, skipped: {entry}")
            continue
        sources.append(entry)
        have.add(link_target(entry))
        added.append(entry)

    if not added:
        print(f"unchanged: {rel}")
        return
    if not args.dry_run:
        note.write_text(
            vl.join_frontmatter(vl.set_list_field(fm, "sources", sources), rest),
            encoding="utf-8")
    verb = "would add" if args.dry_run else "added"
    print(f"{verb} {len(added)} source(s) to {rel}:")
    for entry in added:
        print(f"  + {entry}")


if __name__ == "__main__":
    main()
