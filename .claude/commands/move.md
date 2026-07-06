---
description: Move a note between the ideas bank and a campaign, or between campaigns
argument-hint: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

You are helping a GM move a TTRPG note between vaults (ideas bank ↔ campaign, or campaign ↔ campaign).

Work through this interactively, one question at a time. Do not ask multiple questions at once.

---

## Step 1 — Choose Source

List available sources:
```bash
echo "ideas"
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d ! -name ideas ! -name ".*" | sort | xargs -I{} basename {}
```

Ask the user: "Where are you moving FROM? (ideas bank or a campaign name)"

Wait for their answer before continuing.

---

## Step 2 — Choose Entity Type

List the subdirectories in the source that contain at least one `.md` file:

```bash
# For ideas source:
find /home/danny/ttrpg_campaigns/campaigns/ideas -mindepth 1 -maxdepth 1 -type d | while read d; do
  count=$(find "$d" -name "*.md" | wc -l)
  [ "$count" -gt 0 ] && basename "$d"
done | sort

# For campaign source:
find /home/danny/ttrpg_campaigns/campaigns/<name> -mindepth 1 -maxdepth 1 -type d | while read d; do
  count=$(find "$d" -name "*.md" | wc -l)
  [ "$count" -gt 0 ] && basename "$d"
done | sort
```

Present the list. Ask: "What type of note are you moving?" (e.g. locations, npcs, plot-hooks)

Wait for their answer before continuing.

---

## Step 3 — Choose Specific Note

List the `.md` files in `<source>/<type>/`:

```bash
# For ideas:
find /home/danny/ttrpg_campaigns/campaigns/ideas/<type> -name "*.md" | sort | xargs -I{} basename {} .md

# For campaign:
find /home/danny/ttrpg_campaigns/campaigns/<name>/<type> -name "*.md" | sort | xargs -I{} basename {} .md
```

Present the list. Ask: "Which note do you want to move?"

Wait for their answer before continuing.

---

## Step 4 — Choose Destination

List available destinations, **excluding the source**:

```bash
echo "ideas"
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d ! -name ideas ! -name ".*" | sort | xargs -I{} basename {}
```

Remove the source from this list before presenting it. Ask: "Where are you moving it TO?"

Wait for their answer before continuing.

---

## Step 5 — Confirm

Read the note to be moved so you understand its content (you'll need it for Steps 7 and 10).

Before doing anything, state clearly:

> Move **`<Note Name>`** (`<source>/<type>/`) → `<destination>/<type>/`

Ask: "Confirm?" and wait for a yes before proceeding.

---

## Step 6 — Move the File

**Guard:** If the user is moving a `characters/` note to ideas, stop and warn them: "Player characters belong to a campaign — they can't live in the ideas bank. Move it to a different campaign instead." Re-prompt Step 4.

**Create destination folder if needed:**
```bash
# Campaign destination:
mkdir -p /home/danny/ttrpg_campaigns/campaigns/<destination>/<type>

# Ideas destination (subfolders already exist, but just in case):
mkdir -p /home/danny/ttrpg_campaigns/campaigns/ideas/<type>
```

**Move the file:**
```bash
mv "/home/danny/ttrpg_campaigns/<source-path>/<Note Name>.md" \
   "/home/danny/ttrpg_campaigns/<dest-path>/<Note Name>.md"
```

---

## Step 7 — Update the Moved File's Frontmatter and Tags

Read the moved file. Update campaign-scoped metadata:

- **`campaign:` frontmatter field**: set to the destination campaign name, or remove/blank it if moving to ideas
- **`#campaign/xxx` tags**: replace `#campaign/<source-name>` with `#campaign/<destination-name>`, or remove if moving to ideas
- **`tags:` list in frontmatter**: same — update or remove the campaign-scoped tag entry

Do not change any other content in the file.

---

## Step 8 — Find All Vault References to This Note

Search the entire vault for every file that mentions the note by name:

```bash
grep -r "\[\[<Note Name>" /home/danny/ttrpg_campaigns --include="*.md" -l 2>/dev/null
```

Also search for the bare name in case it's referenced without brackets in some places:
```bash
grep -r "<Note Name>" /home/danny/ttrpg_campaigns --include="*.md" -l 2>/dev/null
```

Collect the full list of referencing files. Separate them into two groups:
- **Index files** (`_index.md`) — you will update these in Step 9
- **Non-index files** — content notes that wikilink to the moved note

---

## Step 9 — Update Every Index That References This Note

For each `_index.md` found in Step 8:

- **Source index** (`<source>/_index.md`): remove the wikilink entry for the moved note entirely.
- **Destination index** (`<destination>/_index.md`): add `- [[<Note Name>]] —` under the section matching the entity type. If the entry already exists (e.g. was cross-referenced before), leave it.
- **Any other index** (a third campaign's `_index.md` that happened to reference this note): leave the wikilink in place but note it in the report — the user may want to decide whether to keep or remove it.

Also check `Home.md` and the vault root for any references and update accordingly.

---

## Step 10 — Update Wikilinks in Non-Index Content Notes

For each non-index file from Step 8:

Obsidian resolves `[[Note Name]]` by note name, not path — so bare wikilinks **do not need updating** and will continue to resolve correctly after the move.

However, if any file contains a **path-qualified link** like `[[campaigns/old-campaign/locations/Note Name]]` or `[[campaigns/ideas/locations/Note Name]]`, update that link to reflect the new path.

```bash
# Check for path-qualified links:
grep -r "campaigns/<source-name>/<type>/<Note Name>\|campaigns/ideas/<type>/<Note Name>" \
  /home/danny/ttrpg_campaigns --include="*.md" -l 2>/dev/null
```

Fix any path-qualified links found by editing those files directly.

---

## Step 11 — Report

Tell the user:
- Where the file moved from and to
- Which frontmatter fields/tags were updated in the moved file
- Which index files were updated (source removed, destination added)
- Any third-party index files that still reference the note (let the user decide)
- Any non-index content notes that wikilink to this note (name them — wikilinks are fine, but user may want to know for context)
- Any path-qualified links that were updated
