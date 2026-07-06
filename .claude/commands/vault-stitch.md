---
description: Govern the vault's cross-cutting layer — adjudicate the _meta/tags.md registry (promote/reject/merge proposed tags) and gate tags coming in from /ingest
argument-hint: "[reconcile | intake <note> <tags...>] (empty = reconcile)"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are governing the vault's connective/cross-cutting layer: the tag registry in `_meta/tags.md`. Policy: `_meta/conventions.md` §3 — tags are controlled, retrievable, cross-cutting axes; never a note's type; never silently invented.

**Scope boundary.** General hygiene (orphans, broken links, off-vocab statuses) belongs to `/lint`. This command owns only tags: the registry, and the notes' `tags:` fields insofar as adjudication rewrites them.

Two modes, chosen from `$ARGUMENTS`:

---

## Mode 1 — Registry reconcile (default; `$ARGUMENTS` empty or `reconcile`)

Adjudicate every tag under `## Proposed` in `_meta/tags.md`, one at a time, interactively.

### 1a. Gather evidence first

Read `_meta/tags.md`. For each proposed tag, find its real usage before asking anything:

```bash
grep -rln -- "- <tag>$" campaigns ideas          # block-list form in note frontmatter
cat "_index/by-tag/<tag>.md" 2>/dev/null         # current index page, if any
```

Also read the registry row's own merge/synonym hint — it was recorded at proposal time and is usually the right starting recommendation.

### 1b. Walk the proposals one at a time

For each proposed tag present the GM: the tag, how many notes carry it (list them if ≤ 5), what axis it would be, and your recommendation. Offer exactly three outcomes:

- **Promote** — it's a real, reusable cross-cutting axis. Add a row to the `## Active` table (tag, axis, one-line note), delete the `## Proposed` row. Carrying notes keep the tag unchanged.
- **Merge → `<existing-tag>`** — synonym or subset of an active tag. For each carrying note, rewrite its tag list with the replacement via the script (replace mode with the full final list, or `--remove <tag>` then `--add <target>`):
  ```bash
  python3 _scripts/vault-set-tags.py --remove "<note>" <tag>
  python3 _scripts/vault-set-tags.py --add "<note>" <target>
  ```
  Then delete the `## Proposed` row.
- **Reject** — vague one-off, duplicates `type:`, or not worth an axis. `--remove` it from every carrying note, delete the `## Proposed` row. If the concept still matters, suggest where it belongs instead (note body, `type:`, a `.base` view).

Cluster handling: when several proposals form one family (e.g. the bestiary cluster `humanoid`/`giant`/`hag`/`construct`/`aberration`), present the family as a single decision first — formalize a shared axis vs. keep/reject individually — then apply the outcome per tag.

Edit `_meta/tags.md` directly for registry rows (it is authored data, not derived). Never leave a tag adjudicated in the registry but still un-rewritten in notes, or vice versa — finish each tag completely before moving to the next.

### 1c. Close out

After the last proposal:

1. Rebuild the derived index so `_index/by-tag/` matches the new reality:
   ```bash
   python3 _scripts/vault-rebuild-index.py
   ```
2. Report: per tag — decision, notes rewritten; registry rows added/removed; the rebuild summary. Remind the GM the changes are git-visible and should be committed together.

---

## Mode 2 — Intake gate (`$ARGUMENTS` = `intake <note> <tags...>`)

Called from `/ingest` (or directly) when new content wants tags. The gate is mostly enforced by the script — your job is judgment before invoking it:

1. **Normalize** each candidate to lowercase-kebab-case.
2. **Check the registry** (`_meta/tags.md`): if an active tag already covers the concept (e.g. candidate `villainous` with active `enemy`), use the active tag instead — don't create near-duplicates. Ask the GM only when the mapping is genuinely unclear.
3. **Drop** candidates that duplicate the note's `type:` or are vague one-offs.
4. **Apply** through the script — never hand-edit `tags:`:
   ```bash
   python3 _scripts/vault-set-tags.py --add "<note>" <tags...>
   ```
   The script refuses type-name tags and auto-files anything unknown under `## Proposed` (date + source note) while applying it provisionally — that's the paper trail for the next reconcile pass.
5. In the calling command's report, mention how many tags are now waiting under `## Proposed`, and suggest `/vault-stitch` when the count grows past a handful.
