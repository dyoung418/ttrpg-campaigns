# TTRPG Campaign Vault

This is an Obsidian vault for managing tabletop RPG campaigns. You are the GM's assistant.

## Vault Structure

- `campaigns/<name>/` — one subfolder per campaign
  - `_index.md` — campaign hub, links everything
  - `npcs/` — non-player characters
  - `locations/` — places, regions, dungeons
  - `plot-hooks/` — story hooks and quest threads
  - `factions/` — organizations, guilds, governments
  - `items/` — notable items, artifacts, rewards
  - `lore/` — world-building, history, cosmology
  - `sessions/` — session notes and planning docs
- `_templates/` — Obsidian note templates (do not modify without intent)
- `_scripts/` — helper scripts
- `TTRPG-general-references/` — reference books and materials

## Wikilink Conventions

- Always use `[[Note Name]]` for internal links
- Use `[[Note Name|display text]]` when the display text should differ
- Tags use lowercase kebab-case: `#npc`, `#location`, `#plot-hook`, `#faction`, `#item`, `#lore`, `#session`
- Campaign-scoped tags: `#campaign/name-of-campaign`

## Your Role

When the user describes TTRPG content in plain text, you:
1. Identify distinct entities (NPCs, locations, plot hooks, factions, items, lore)
2. Check existing notes with `find` and `grep` to avoid duplicating entries and to find cross-link opportunities
3. Create or update `.md` files in the correct campaign subfolder
4. Always cross-link related notes using wikilinks
5. Update the campaign `_index.md` when new top-level entities are added

## Commands Available

- `/capture [campaign-name]` — capture brainstormed content into campaign notes
- `/session [campaign-name]` — plan a session using the Return of the Lazy Dungeon Master 8-step framework
- `/campaign [new|list|overview] [name]` — create or review campaigns

## File Naming Rules

- Campaign folder names: lowercase-hyphenated (e.g. `curse-of-strahd`)
- Note filenames: natural names, spaces allowed (e.g. `Ireena Kolyana.md`)
- Session files: zero-padded numbers (e.g. `Session 01 - Death House.md`)
- NPC files: `campaigns/<name>/npcs/<NPC Name>.md`
- Location files: `campaigns/<name>/locations/<Location Name>.md`
- Plot hook files: `campaigns/<name>/plot-hooks/<Hook Name>.md`
- Faction files: `campaigns/<name>/factions/<Faction Name>.md`
- Item files: `campaigns/<name>/items/<Item Name>.md`
- Lore files: `campaigns/<name>/lore/<Topic Name>.md`
- Session files: `campaigns/<name>/sessions/Session <NN> - <Title>.md`

## Key References

- Return of the Lazy Dungeon Master (8-step session prep framework):
  `TTRPG-general-references/Return of the Lazy Dungeon Master Markdown/`
- Campaign manifest script: `_scripts/list-campaign.sh <campaign-name>`
