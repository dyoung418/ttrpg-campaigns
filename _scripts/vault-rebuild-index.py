#!/usr/bin/env python3
"""Regenerate the _index/ collections from note frontmatter.

Usage:
  vault-rebuild-index.py [--dry-run]

Currently builds _index/by-tag/: one generated page per tag listing every
note carrying it, grouped by campaign, plus an _index.md overview of all
tags. The whole directory is wiped and rebuilt each run — _index/ is derived
data, committed to git, and never hand-edited (_meta/conventions.md §5).
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vaultlib as vl

HEADER = ("> [!warning] Generated file — do not hand-edit\n"
          "> Rebuilt by `_scripts/vault-rebuild-index.py` "
          "(see `_meta/conventions.md` §5).\n\n")


def slug(tag: str) -> str:
    return tag.replace("/", "--")


def group_of(vault: Path, path: Path) -> str:
    rel = path.relative_to(vault).parts
    return rel[1] if rel[0] == "campaigns" else rel[0]  # campaign name or 'ideas' (the bank lives at campaigns/ideas/)


def scalar_field(fm: str, key: str) -> str:
    vals = vl.get_list_field(fm, key)
    return vals[0] if vals else ""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    args = ap.parse_args()

    vault = vl.vault_root()
    by_tag: dict[str, list[tuple[str, str, Path]]] = defaultdict(list)

    for path in vl.iter_notes(vault):
        if path.name == "_index.md":  # hub files are navigation, not content
            continue
        fm, _ = vl.split_frontmatter(path.read_text(encoding="utf-8"))
        if fm is None:
            continue
        ntype = scalar_field(fm, "type")
        for tag in vl.get_list_field(fm, "tags") or []:
            by_tag[tag].append((group_of(vault, path), ntype, path))

    out_dir = vault / "_index" / "by-tag"
    if args.dry_run:
        for tag in sorted(by_tag):
            print(f"would write by-tag/{slug(tag)}.md ({len(by_tag[tag])} notes)")
        print(f"would write by-tag/_index.md ({len(by_tag)} tags)")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.md"):
        old.unlink()

    for tag, entries in sorted(by_tag.items()):
        lines = [f"---\ntype: index\ntags: []\n---\n\n# Tag: `{tag}`\n\n", HEADER,
                 f"{len(entries)} note(s) tagged `{tag}`.\n"]
        by_group = defaultdict(list)
        for group, ntype, path in entries:
            by_group[group].append((ntype, path))
        for group in sorted(by_group):
            lines.append(f"\n## {group}\n\n")
            for ntype, path in sorted(by_group[group], key=lambda e: e[1].stem.lower()):
                suffix = f" — `{ntype}`" if ntype else ""
                lines.append(f"- [[{path.stem}]]{suffix}\n")
        (out_dir / f"{slug(tag)}.md").write_text("".join(lines), encoding="utf-8")

    overview = ["---\ntype: index\ntags: []\n---\n\n# Notes by Tag\n\n", HEADER]
    for tag, entries in sorted(by_tag.items()):
        overview.append(f"- [[{slug(tag)}|{tag}]] — {len(entries)} note(s)\n")
    (out_dir / "_index.md").write_text("".join(overview), encoding="utf-8")

    print(f"wrote {len(by_tag)} tag page(s) + _index.md to "
          f"{out_dir.relative_to(vault)}/")


if __name__ == "__main__":
    main()
