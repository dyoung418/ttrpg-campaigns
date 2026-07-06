---
description: Regenerate the _index/ collections (by-tag) from note frontmatter — _index/ is derived data, committed to git, never hand-edited
argument-hint: "(no arguments)"
allowed-tools: Bash, Read, Grep, Glob
---

Thin wrapper around `_scripts/vault-rebuild-index.py`. Policy: `_meta/conventions.md` §5.

1. Run it (from the vault root):

   ```bash
   python3 _scripts/vault-rebuild-index.py
   ```

   It wipes and rebuilds `_index/by-tag/` — one page per tag plus an `_index.md` overview. `--dry-run` previews the tag list and counts.
2. Report the summary (how many tag pages). If a surprising tag shows up (a one-off, or something that should be merged), point the user at `/vault-stitch` — the registry in `_meta/tags.md` is where tags are adjudicated.
3. Remind the user `_index/` is committed content: the rebuild should ride along with the commit that changed the underlying tags.
