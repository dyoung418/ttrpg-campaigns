---
description: Regenerate every note's related field from the vault's wikilink graph (related is derived data — never hand-edited)
argument-hint: "[scope-dir] (optional; limits which notes are rewritten)"
allowed-tools: Bash, Read, Grep, Glob
---

Thin wrapper around `_scripts/vault-rebuild-backlinks.py`. Policy: `_meta/conventions.md` §1/§5 — `related` is the sorted union of a note's outbound wikilinks and inbound backlinks, script-maintained only.

1. Run it (from the vault root):

   ```bash
   python3 _scripts/vault-rebuild-backlinks.py [scope-dir]
   ```

   Pass a scope directory from `$ARGUMENTS` if given (the link *graph* always spans all of `campaigns/` + `ideas/`; scope only limits which notes get rewritten). `--dry-run` previews.
2. Report the summary line (updated / already-current / skipped counts). If any notes were skipped for missing frontmatter, list them — that's `/lint` territory.
3. Typically follow with `/vault-rebuild-index` so `_index/` stays in step, and remind the user the changes are git-visible (`git diff --stat`).
