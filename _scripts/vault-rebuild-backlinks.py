#!/usr/bin/env python3
"""Regenerate every note's `related:` field from the vault's wikilink graph.

Usage:
  vault-rebuild-backlinks.py [--dry-run] [scope-dir]

`related` is derived data (_meta/conventions.md §1/§5): for each note it is
the sorted union of
  - outbound: notes this note wikilinks to, and
  - inbound:  notes that wikilink to this note (its backlinks),
rendered as quoted wikilinks. Always regenerate, never hand-edit.

Graph rules:
  - Scope of the graph is all of campaigns/ + ideas/ (scope-dir only limits
    which notes get *rewritten*, not what counts as a link).
  - `_index.md` hub files are excluded from the graph entirely: they link to
    everything by design, so counting them would put noise in every note.
  - Self-links and links that resolve outside the content dirs are ignored.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vaultlib as vl


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("scope", nargs="?", type=Path,
                    help="only rewrite notes under this directory")
    args = ap.parse_args()

    vault = vl.vault_root()
    notes = [p for p in vl.iter_notes(vault) if p.name != "_index.md"]
    resolver = vl.build_resolver(notes)

    # outbound[path] / inbound[path] -> set of connected note paths
    outbound: dict[Path, set[Path]] = {p: set() for p in notes}
    inbound: dict[Path, set[Path]] = {p: set() for p in notes}
    parsed: dict[Path, tuple[str | None, str]] = {}

    for path in notes:
        fm, rest = vl.split_frontmatter(path.read_text(encoding="utf-8"))
        parsed[path] = (fm, rest)
        # Links are read from the body only — frontmatter `related`/`sources`
        # must not feed back into the graph.
        for target in vl.parse_wikilinks(rest):
            hit = vl.resolve_link(resolver, target)
            if hit and hit != path:
                outbound[path].add(hit)
                inbound[hit].add(path)

    scope = args.scope.resolve() if args.scope else None
    changed = unchanged = skipped = 0
    for path in notes:
        if scope and not path.is_relative_to(scope):
            continue
        fm, rest = parsed[path]
        if fm is None:
            skipped += 1
            print(f"skipped (no frontmatter): {path.relative_to(vault)}")
            continue
        related = sorted((outbound[path] | inbound[path]),
                         key=lambda p: p.stem.lower())
        values = [f"[[{p.stem}]]" for p in related]
        if (vl.get_list_field(fm, "related") or []) == values:
            unchanged += 1
            continue
        if not args.dry_run:
            path.write_text(
                vl.join_frontmatter(vl.set_list_field(fm, "related", values), rest),
                encoding="utf-8")
        changed += 1

    verb = "would update" if args.dry_run else "updated"
    print(f"{verb} {changed} note(s); {unchanged} already current; "
          f"{skipped} skipped; graph size {len(notes)} notes")


if __name__ == "__main__":
    main()
