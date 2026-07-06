---
description: Ingest source files from _sources/new/ — extract entities into campaign notes, then move processed files to _sources/processed/
argument-hint: "[file-path | glob | (empty for all)]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are helping a GM ingest source documents (Discord RP exports, lore docs, anything the user dropped into the vault) into organized campaign notes.

**Hard rule — never modify files under `_sources/`.** They are the historical record. Read them, extract their content into vault notes, then move them from `_sources/new/` to `_sources/processed/` (preserving any subdirectory structure). Never edit a source file in place. Never delete a source file.

**Backlink rule — always link vault notes back to their source files.** Every note you create or update during ingest must include a wikilink to the source file(s) it was drawn from. Use a `## Sources` section (or add to an existing one) with entries like `- [[_sources/processed/RP14 The Great Feast of Freehaven|RP14 — The Great Feast of Freehaven]]`. Link liberally — if multiple source files contributed to a note, list all of them. Also record every source in the note's `sources:` frontmatter list — use the script, it's idempotent:

```bash
python3 _scripts/vault-add-source.py "<note>" '[[_sources/processed/<file>|<display>]]'
```

The goal is a clear audit trail from every vault note back to the raw document that produced it.

**Tag rule — tags go through the `/vault-stitch` intake gate.** Never hand-write `tags:` on new notes and never invent tags. Apply tags with `python3 _scripts/vault-set-tags.py --add "<note>" <tags...>` — it validates against `_meta/tags.md`, refuses type-name tags (type lives in `type:` only), and files unknown tags under `## Proposed` automatically. Judgment rules for choosing candidate tags: `.claude/commands/vault-stitch.md` Mode 2.

Work through this interactively, one question at a time.

---

## Step 1 — Resolve Scope

Decide which source files to process based on `$ARGUMENTS`:

- **Empty:** every file under `_sources/new/` recursively.
  ```bash
  find /home/danny/ttrpg_campaigns/_sources/new -type f -name "*.md" -not -name ".gitkeep" | sort
  ```
- **Path under `_sources/new/`:** that single file.
- **Glob:** resolve under `_sources/new/`.

If the resulting list is empty, tell the user "Nothing to ingest — `_sources/new/` is empty (or your filter matched nothing)." and stop.

Show the user the list of files you're about to process and the total count.

---

## Step 2 — Resolve Target Campaign (Once Per Run)

Source filenames don't reliably encode campaign membership, so ask up front:

```bash
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d | sort | xargs -I{} basename {}
```

Ask: "Which campaign should these sources be captured into?"

Wait for an answer. Use that campaign for every file in this run — do not re-ask per file.

---

## Step 3 — Classify Each File

For each file, read its first ~30 lines. The expected pattern is a Discord RP export — message blocks that look like:

```
### Wes [Riven] — 12/19/24, 5:18 PM
[narrative or dialogue]

### Darren [Pavel] — 12/20/24, 10:02 AM
[player reaction/narrative]
```

If the file matches that pattern, treat it as **RP**. Otherwise treat it as **freeform prose** (lore doc, backstory writeup, etc.).

You don't need to confirm the classification with the user unless the file is ambiguous (e.g. a hybrid). When in doubt, ask.

---

## Step 4 — Process Each File (Loop)

For each file in the scope:

### 4a. Read the source

Read the file in full. For RP exports, also extract:

- **Scene title** from the filename — `RP14 The Great Feast of Freehaven.md` → "The Great Feast of Freehaven", source ID `RP14`.
- **Speakers/characters** from the `Player [Character]` tags — map each to the matching PC file in `campaigns/<campaign>/characters/`. If a speaker doesn't have a PC file yet, treat them as an NPC and proceed.

### 4b. Strip Discord noise before extracting

Before feeding the content to entity extraction:

- **Remove image URLs** (`https://cdn.discordapp.com/...`, `https://media.discordapp.net/...`). Note in the report that images were present but not preserved.
- **Strip raw `@mentions`** that target users, not in-fiction characters (these usually look like `<@123456789>`).
- Keep speaker tags and timestamps — they're useful context.

### 4c. Extract entities and write vault notes

**Preferred path: call `/capture` via the Skill tool.**

```
Skill(skill="capture", args="<campaign>")
```

When you invoke `/capture`, treat the cleaned source text as the brainstorm input — i.e. don't let `/capture` Step 3 prompt the user for content; you already have it. If the Skill invocation doesn't accept pre-supplied content cleanly, fall back to the inline path below.

**Fallback path: inline the capture logic.**

If you can't pass content into `/capture`, do the same work directly:

1. Search the vault for existing entities mentioned in the source. Use `obsidian:obsidian-cli` (`Skill(skill="obsidian:obsidian-cli", ...)`) if available; otherwise:
   ```bash
   grep -r "Entity Name" /home/danny/ttrpg_campaigns/campaigns/<campaign>/ -l 2>/dev/null
   ```
2. For each entity found in the source:
   - **Existing file → update it** with new details (status changes, relationship developments, scene appearances). Preserve existing content. Add new info under appropriate sections (`## Recent Events`, `## Relationships`, etc.).
   - **New entity → create a file** in the right subfolder using `_templates/` as a structural guide. Frontmatter must include `type`, `campaign: <campaign>`, `tags: [campaign/<campaign>]` (plus cross-cutting theme tags via the intake gate — never a type-name tag), `sources: []`, `related: []`, a `status` from the type's vocabulary (`_meta/conventions.md` §2), and `created: <today YYYY-MM-DD>`.
3. Cross-link aggressively. Every NPC mentioned → link their home location, faction, related plot hooks. Every location → link NPCs found there. Every event → link involved characters.
4. **Add source backlinks.** On every note created or updated, ensure a `## Sources` section exists with a wikilink to the source file: `- [[_sources/processed/<filename>|<display name>]]`. If the file is still in `new/` at this point, link to `_sources/new/<filename>` — the link will resolve correctly after the file is moved in Step 4e. If the note already has a `## Sources` section, append to it rather than replacing it.
5. Update `campaigns/<campaign>/_index.md` — add wikilinks under the appropriate sections for any newly created entities.

### 4d. RP-specific extra — session/scene note

For RP files only, also create or update a scene note under `campaigns/<campaign>/sessions/`:

1. Search existing session notes for one that closely matches this scene's content or filename.
2. **If a matching session exists:** append a `## Scene from <Source Filename>` section with a short prose summary of what happened, who was present (wikilinked), and any notable outcomes.
3. **If no matching session exists:** create `Session NN — <RP Title>.md` where `NN` is the next unused session number. Use frontmatter:
   ```yaml
   ---
   type: session
   campaign: <campaign>
   tags: [campaign/<campaign>, rp-scene]
   date: ""
   session_number: NN
   status: complete
   players_present: [<wikilinked PCs from speaker tags>]
   sources:
     - "[[_sources/processed/<filename>|<display name>]]"
   created: <today>
   ---
   ```
   Body: short summary, key beats, links to NPCs/locations/items touched. End with a `## Sources` section: `- [[_sources/processed/<filename>|<display name>]]`.

The `rp-scene` **tag** (not a status) marks roleplay-scene logs — see `_meta/conventions.md` §2.

### 4e. Move the source file on success

When the file has been fully processed (entities captured, session/scene note created or updated, no errors):

```bash
SRC="/home/danny/ttrpg_campaigns/_sources/new/<relative-path>"
DST="/home/danny/ttrpg_campaigns/_sources/processed/<relative-path>"
mkdir -p "$(dirname "$DST")"
mv "$SRC" "$DST"
```

The `<relative-path>` is whatever comes after `_sources/new/` — including any subdirectories. The `mkdir -p` ensures the matching subdirectory structure exists under `processed/`.

**Refuse to overwrite.** If `$DST` already exists, do not move. Report it as "skipped — already in processed/" and leave the file in `new/`.

### 4f. On failure, leave the file in place

If anything went wrong (couldn't classify, no entities extractable, user interrupted, extraction errored): leave the file in `_sources/new/` untouched and record a one-line reason. Continue to the next file.

---

## Step 5 — Edge Cases

- **File has no extractable entities** (blank, only image refs, only meta): ask the user "Move to `processed/` anyway, or leave in `new/`?" Don't silently move uncaptured files.
- **Entity is mentioned by alias** ("the hooded figure" → Lady Jamandi): ask the user to confirm the mapping before merging into the canonical note.
- **Source mentions a character or NPC whose status appears to change** (death, resurrection, faction switch): apply the change to the vault note, but also call it out in the final report so the user can sanity-check.
- **Discord CDN URLs**: never write them into vault files. Mention in the report that images were stripped.
- **Subdirectory in `new/`**: must be preserved in `processed/`. The `mkdir -p` in Step 4e handles this — verify the destination directory exists before `mv`.

---

## Step 6 — Report

After all files are processed, tell the user concisely:

- **Files moved** (count + names → moved to `_sources/processed/<path>`)
- **Files left in `new/`** with reasons
- **Entities created** (grouped by type, with relative paths)
- **Entities updated** (grouped by type, with relative paths)
- **Session/scene notes** touched (with relative paths)
- **Status changes flagged** (e.g. "Edina's status changed from `alive` to `injured`")
- **Images skipped** (count, if any)
- Suggestion: "Run `/lint <campaign>` to sanity-check the new notes, or `/reconcile _sources/processed/<file>` to compare specific facts against the source."

Do not dump file contents.
