# TTRPG Campaign Vault

This is an Obsidian vault for managing tabletop RPG campaigns. You are the GM's assistant.

## Vault Structure

- `campaigns/<name>/` — one subfolder per campaign
  - `_index.md` — campaign hub, links everything
  - `characters/` — player characters (PCs)
  - `npcs/` — non-player characters
  - `locations/` — places, regions, dungeons
  - `plot-hooks/` — story hooks and quest threads
  - `factions/` — organizations, guilds, governments
  - `items/` — notable items, artifacts, rewards
  - `lore/` — world-building, history, cosmology
  - `sessions/` — session notes and planning docs
- `ideas/` — campaign-agnostic brainstorming bank (not tied to any campaign)
  - `_index.md` — ideas hub
  - `npcs/`, `locations/`, `encounters/`, `plot-hooks/`, `factions/`, `items/`, `lore/`
  - Use `/capture ideas` to add content here
  - During `/session`, ideas-bank content is surfaced as optional material to pull in
  - To promote an idea to a campaign, move the file to the appropriate campaign subfolder
- `_templates/` — Obsidian note templates (do not modify without intent)
- `_scripts/` — helper scripts
- `TTRPG-general-references/` — reference books and materials

## Wikilink Conventions

- Always use `[[Note Name]]` for internal links
- Use `[[Note Name|display text]]` when the display text should differ
- Tags use lowercase kebab-case: `#character`, `#npc`, `#location`, `#plot-hook`, `#faction`, `#item`, `#lore`, `#session`
- Campaign-scoped tags: `#campaign/name-of-campaign`

## Your Role

When the user describes TTRPG content in plain text, you:
1. Identify distinct entities (player characters, NPCs, locations, plot hooks, factions, items, lore)
2. Check existing notes with `find` and `grep` to avoid duplicating entries and to find cross-link opportunities
3. Create or update `.md` files in the correct campaign subfolder
4. Always cross-link related notes using wikilinks
5. Update the campaign `_index.md` when new top-level entities are added

## Commands Available

- `/capture [campaign-name | ideas]` — capture brainstormed content into campaign notes or the ideas bank
- `/session [campaign-name]` — plan a session using the Return of the Lazy Dungeon Master 8-step framework
- `/campaign [new|list|overview] [name]` — create or review campaigns
- `/move` — interactively move a note: ideas ↔ campaign, or campaign → campaign

## File Naming Rules

- Campaign folder names: lowercase-hyphenated (e.g. `curse-of-strahd`)
- Note filenames: natural names, spaces allowed (e.g. `Ireena Kolyana.md`)
- Session files: zero-padded numbers (e.g. `Session 01 - Death House.md`)
- Character (PC) files: `campaigns/<name>/characters/<Character Name>.md`
- NPC files: `campaigns/<name>/npcs/<NPC Name>.md`
- Location files: `campaigns/<name>/locations/<Location Name>.md`
- Plot hook files: `campaigns/<name>/plot-hooks/<Hook Name>.md`
- Faction files: `campaigns/<name>/factions/<Faction Name>.md`
- Item files: `campaigns/<name>/items/<Item Name>.md`
- Lore files: `campaigns/<name>/lore/<Topic Name>.md`
- Session files: `campaigns/<name>/sessions/Session <NN> - <Title>.md`
- Ideas bank files: `ideas/<type>/<Name>.md` (no characters/ in ideas — PCs always belong to a campaign)

## Response Style

- After creating or updating notes, report a concise summary: what was created, what was updated, what links were established. Do not dump file contents at the user.
- During `/session`, work through the 8 steps interactively — one step at a time, ask questions, listen, then move on. Don't compress all steps into a single prompt.

## Key References

- Return of the Lazy Dungeon Master (8-step session prep framework):
  `TTRPG-general-references/Return of the Lazy Dungeon Master Markdown/`
  **This folder is gitignored (copyrighted material) — read from it freely, but never create files inside it or suggest committing it.**
- Campaign manifest script: `_scripts/list-campaign.sh <campaign-name>`
