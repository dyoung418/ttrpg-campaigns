---
description: Capture brainstormed TTRPG content into organized, linked campaign notes
argument-hint: "[campaign-name]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

You are helping a GM organize TTRPG campaign content into an Obsidian vault.

## Step 1 — Resolve Campaign

If `$ARGUMENTS` names a campaign, use `campaigns/$ARGUMENTS/` as the target.

If `$ARGUMENTS` is empty, list existing campaigns:
```bash
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d | sort
```
Then ask: "Which campaign is this for?" (or offer to create a new one with `/campaign new <name>`).

## Step 2 — Survey Existing Notes

Before creating anything, run:
```bash
find /home/danny/ttrpg_campaigns/campaigns/<name> -name "*.md" | sort
```
Read `campaigns/<name>/_index.md` to understand what already exists.

## Step 3 — Get Content from User

If the user has already provided their brainstorm text in this message, use it directly.

Otherwise ask: "Tell me what you've got — NPCs, locations, plot hooks, lore, factions, items. Just describe it naturally."

## Step 4 — Identify Entities

Parse the user's text and identify every distinct entity:
- **NPC**: a named person, creature, or being with a personality or role
- **Location**: a named place — city, dungeon, building, region, room
- **Plot Hook**: a story thread, quest, rumor, or unresolved tension
- **Faction**: an organization, guild, cult, government, or group
- **Item**: a named item of significance (not generic loot)
- **Lore**: world history, cosmology, cultural detail, rules of magic, etc.

## Step 5 — Check for Duplicates

For each entity, grep existing notes before creating a new file:
```bash
grep -r "Entity Name" /home/danny/ttrpg_campaigns/campaigns/<name>/ -l 2>/dev/null
```
If a file already exists, plan to **update** it rather than create a duplicate.

## Step 6 — Create or Update Files

Use the templates in `_templates/` as structure guides. Fill in only what the user actually provided — do not invent details. Leave template sections empty if the user didn't mention them.

**File paths:**
- `campaigns/<name>/npcs/<NPC Name>.md`
- `campaigns/<name>/locations/<Location Name>.md`
- `campaigns/<name>/plot-hooks/<Hook Name>.md`
- `campaigns/<name>/factions/<Faction Name>.md`
- `campaigns/<name>/items/<Item Name>.md`
- `campaigns/<name>/lore/<Topic Name>.md`

**Cross-linking rules:**
- Every NPC file → wikilink to their home Location, their Faction, and any Plot Hooks they're involved in
- Every Location → wikilink to NPCs found there and Plot Hooks tied to it
- Every Plot Hook → wikilink to NPCs and Locations involved
- Factions → wikilink to member NPCs and their base Location
- If a referenced entity doesn't have a file yet, create a minimal stub with just the frontmatter and a one-line description, and flag it for the user

## Step 7 — Update Campaign Index

Open `campaigns/<name>/_index.md` and add new entities to the appropriate sections (Key NPCs, Key Locations, Active Plot Hooks, Factions). Use wikilinks. Do not remove existing entries.

## Step 8 — Report

Tell the user concisely:
- Which files were **created** (with relative paths)
- Which files were **updated**
- Which cross-links were established
- Which entities got **stub files** that need more detail (suggest running `/capture` again)
- Any entities you weren't sure how to categorize

Do not dump file contents at the user — just summarize what changed.
