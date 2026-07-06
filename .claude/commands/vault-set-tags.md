---
description: Set or normalize a note's tags, validated against the _meta/tags.md registry — unknown tags are filed under ## Proposed, never silently invented
argument-hint: "<note> <tag> [<tag> ...] — prefix with --add or --remove to adjust instead of replace"
allowed-tools: Bash, Read, Grep, Glob
---

Thin wrapper around `_scripts/vault-set-tags.py`. Tag policy: `_meta/conventions.md` §3.

1. Resolve the note from `$ARGUMENTS`. If given a bare name instead of a path, find it: `find campaigns -name "<name>.md"`. If ambiguous, ask which one.
2. Run it (from the vault root):

   ```bash
   python3 _scripts/vault-set-tags.py [--add|--remove] "<note-path>" <tags...>
   ```

   Default mode **replaces** the tag list; `--add` / `--remove` adjust it. Use `--dry-run` first if the effect is unclear.
3. Report what changed. If the script filed a tag under `## Proposed` in `_meta/tags.md`, tell the user it awaits `/vault-stitch` adjudication.
4. The script refuses type-name tags (`npc`, `location`, …) by design — if that happens, don't work around it; type belongs in the `type:` field.
