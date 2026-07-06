---
description: Append an entry to a note's sources list (idempotent — duplicates are skipped)
argument-hint: "<note> <source-entry> [<source-entry> ...]"
allowed-tools: Bash, Read, Grep, Glob
---

Thin wrapper around `_scripts/vault-add-source.py`. `sources` policy: `_meta/conventions.md` §1 (always a list).

1. Resolve the note from `$ARGUMENTS` (bare name → `find campaigns -name "<name>.md"`; ask if ambiguous).
2. Source entries are usually wikilinks to files under `_sources/` — quote them, e.g. `'[[_sources/processed/roleplay/RP10 …|RP10 — …]]'` — but URLs or citations are fine too.
3. Run it (from the vault root):

   ```bash
   python3 _scripts/vault-add-source.py "<note-path>" '<entry>' [...]
   ```

4. Report what was added and what was skipped as already present.
