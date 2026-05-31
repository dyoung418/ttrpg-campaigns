---
description: Capture brainstormed TTRPG content into organized, linked campaign notes
argument-hint: "[campaign-name | ideas]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are helping a GM organize TTRPG campaign content into an Obsidian vault.

## Step 1 — Resolve Target

**If `$ARGUMENTS` is `ideas`:** use `ideas/` as the target folder. Skip reading a campaign `_index.md` — instead read `ideas/_index.md`.

**If `$ARGUMENTS` names a campaign:** use `campaigns/$ARGUMENTS/` as the target.

**If `$ARGUMENTS` is empty:** list available options:
```bash
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d | sort
```
Ask: "Which campaign is this for? Or type `ideas` to capture campaign-agnostic content."

## Step 2 — Survey Existing Notes

Before creating anything, use `obsidian:obsidian-cli` to search the live vault and list existing notes in the target. If unavailable, fall back to:
```bash
# For a campaign:
find /home/danny/ttrpg_campaigns/campaigns/<name> -name "*.md" | sort

# For ideas:
find /home/danny/ttrpg_campaigns/ideas -name "*.md" | sort
```
Read the target's `_index.md` to understand what already exists.

## Step 3 — Get Content from User

If the user has already provided their brainstorm text in this message, use it directly.

Otherwise ask: "Tell me what you've got — player characters, NPCs, locations, plot hooks, lore, factions, items, encounters. Just describe it naturally."

## Step 4 — Identify Entities

Parse the user's text and identify every distinct entity:
- **Character (PC)**: a player character — someone a player controls. Track: player name, class/race, backstory hook, motivations, character arc, magic item wish list. *(Campaign targets only — not valid for ideas/)*
- **NPC**: a named non-player character with a personality or role
- **Location**: a named place — city, dungeon, building, region, room
- **Encounter**: a combat scenario, trap, or challenge concept not tied to a specific campaign
- **Plot Hook**: a story thread, quest, rumor, or unresolved tension
- **Faction**: an organization, guild, cult, government, or group
- **Item**: a named item of significance (not generic loot)
- **Lore**: world history, cosmology, cultural detail, rules of magic, etc.

## Step 5 — Check for Duplicates

For each entity, use `obsidian:obsidian-cli` to search before creating a new file — it searches by note title, content, and properties, catching matches that filename-only `find` would miss. Fall back to grep if unavailable:
```bash
# Campaign:
grep -r "Entity Name" /home/danny/ttrpg_campaigns/campaigns/<name>/ -l 2>/dev/null

# Ideas:
grep -r "Entity Name" /home/danny/ttrpg_campaigns/ideas/ -l 2>/dev/null
```
If a file already exists, plan to **update** it rather than create a duplicate.

Also check the other pool (ideas vs. campaign) — a character might reference an idea-bank location, or an idea might be better served by linking to a campaign NPC.

## Step 6 — Create or Update Files

Use the templates in `_templates/` as structure guides. Fill in only what the user actually provided — do not invent details. Leave template sections empty if the user didn't mention them.

Use `obsidian:obsidian-markdown` to write note body content so Obsidian-flavored syntax is applied correctly. For GM-only information, use callouts:
- `> [!secret] GM Only` — hidden backstory, secret motives, plot reveals
- `> [!note]` — context or background worth flagging
- `![[Note Name]]` — embed a closely related note inline (use sparingly)

**File paths for a campaign target:**
- `campaigns/<name>/characters/<Character Name>.md`
- `campaigns/<name>/npcs/<NPC Name>.md`
- `campaigns/<name>/locations/<Location Name>.md`
- `campaigns/<name>/encounters/<Encounter Name>.md`
- `campaigns/<name>/plot-hooks/<Hook Name>.md`
- `campaigns/<name>/factions/<Faction Name>.md`
- `campaigns/<name>/items/<Item Name>.md`
- `campaigns/<name>/lore/<Topic Name>.md`

**File paths for ideas target:**
- `ideas/npcs/<NPC Name>.md`
- `ideas/locations/<Location Name>.md`
- `ideas/encounters/<Encounter Name>.md`
- `ideas/plot-hooks/<Hook Name>.md`
- `ideas/factions/<Faction Name>.md`
- `ideas/items/<Item Name>.md`
- `ideas/lore/<Topic Name>.md`

**Cross-linking rules:**
- Every Character file → wikilink to NPCs they have relationships with, Plot Hooks tied to their backstory
- Every NPC file → wikilink to their home Location, their Faction, and any Plot Hooks they're involved in
- Every Location → wikilink to NPCs found there and Plot Hooks tied to it
- Every Plot Hook → wikilink to Characters and NPCs involved, and Locations
- Factions → wikilink to member NPCs and their base Location
- If a referenced entity doesn't have a file yet, create a minimal stub with just the frontmatter and a one-line description, and flag it for the user
- Cross-pool links are fine: an ideas-bank location can be wikilinked from a campaign NPC file

## Step 7 — Update Index

**Campaign target:** Open `campaigns/<name>/_index.md` and add new entities to the appropriate sections. Use wikilinks. Do not remove existing entries.

**Ideas target:** Open `ideas/_index.md` and add new entities to the appropriate sections. Use wikilinks.

## Step 8 — Report

After writing all files, open the primary new note in Obsidian using `obsidian:obsidian-cli` so the GM can see it immediately.

Tell the user concisely:
- Which files were **created** (with relative paths)
- Which files were **updated**
- Which cross-links were established
- Which entities got **stub files** that need more detail (suggest running `/capture` again)
- Any entities you weren't sure how to categorize

Do not dump file contents at the user — just summarize what changed.
