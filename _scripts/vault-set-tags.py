#!/usr/bin/env python3
"""Set or normalize a note's `tags:` field, validated against _meta/tags.md.

Usage:
  vault-set-tags.py <note.md> <tag> [<tag> ...]     replace the tag list
  vault-set-tags.py --add <note.md> <tag> [...]     add to the existing list
  vault-set-tags.py --remove <note.md> <tag> [...]  remove from the list
  vault-set-tags.py --dry-run ...                   report, write nothing

Policy (_meta/conventions.md §3):
  - Tags are normalized to lowercase-kebab-case.
  - Type-name tags (npc, location, ...) are refused outright.
  - Tags not in the registry's Active set are still applied (provisional) but
    are filed under ## Proposed in _meta/tags.md with date + source note —
    tags are never silently invented.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vaultlib as vl


def normalize(tag: str) -> str:
    tag = tag.strip().lstrip("#").lower().replace(" ", "-").replace("_", "-")
    return re.sub(r"-{2,}", "-", tag)


def propose_tag(vault: Path, tag: str, source: str, dry_run: bool) -> None:
    """Append a row to the ## Proposed table in _meta/tags.md."""
    reg = vault / "_meta" / "tags.md"
    text = reg.read_text(encoding="utf-8")
    row = (f"| `{tag}` | {datetime.date.today().isoformat()} | `{source}` | "
           f"*(new — needs adjudication)* |")
    lines = text.splitlines(keepends=True)
    # Insert after the last table row following the ## Proposed header.
    start = next(i for i, l in enumerate(lines) if l.startswith("## Proposed"))
    last_row = None
    for i in range(start, len(lines)):
        if lines[i].startswith("|"):
            last_row = i
        elif last_row is not None and not lines[i].startswith("|"):
            break
    if last_row is None:
        raise SystemExit(f"could not find the ## Proposed table in {reg}")
    if not dry_run:
        lines.insert(last_row + 1, row + "\n")
        reg.write_text("".join(lines), encoding="utf-8")
    print(f"  proposed: `{tag}` filed under ## Proposed in _meta/tags.md")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--add", action="store_true", help="add to existing tags")
    mode.add_argument("--remove", action="store_true", help="remove from existing tags")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("note", type=Path)
    ap.add_argument("tags", nargs="+")
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

    wanted = [normalize(t) for t in args.tags]
    bad = [t for t in wanted if t in vl.TYPE_NAMES]
    if bad:
        raise SystemExit(
            f"refused type-name tag(s) {bad}: type lives in `type:`, never tags "
            "(_meta/conventions.md §3)")

    current = vl.get_list_field(fm, "tags") or []
    if args.add:
        new = current + [t for t in wanted if t not in current]
    elif args.remove:
        new = [t for t in current if t not in wanted]
    else:
        new = list(dict.fromkeys(wanted))  # replace, order-preserving dedupe

    registry = vl.read_tag_registry(vault)
    known = registry["active"] | registry["proposed"]
    for tag in new:
        if tag not in known and not tag.startswith("campaign/"):
            propose_tag(vault, tag, str(rel), args.dry_run)

    if new == current:
        print(f"unchanged: {rel} tags already {current or '[]'}")
        return
    if not args.dry_run:
        note.write_text(vl.join_frontmatter(vl.set_list_field(fm, "tags", new), rest),
                        encoding="utf-8")
    verb = "would set" if args.dry_run else "set"
    print(f"{verb} {rel} tags: {current or '[]'} -> {new or '[]'}")


if __name__ == "__main__":
    main()
