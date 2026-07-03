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
  - `*.base` — Obsidian Bases tracker views (NPC Tracker, Plot Hook Board, Session Log)
  - `*.canvas` — visual relationship maps and diagrams
- `ideas/` — campaign-agnostic brainstorming bank (not tied to any campaign)
  - `_index.md` — ideas hub
  - `npcs/`, `locations/`, `encounters/`, `plot-hooks/`, `factions/`, `items/`, `lore/`
  - Use `/capture ideas` to add content here
  - During `/session`, ideas-bank content is surfaced as optional material to pull in
  - To promote an idea to a campaign, move the file to the appropriate campaign subfolder
- `_memory/` — Claude's persistent memory, committed to git (see "Memory & Plans" below)
- `_plans/` — Claude's cross-session planning docs, committed to git (see "Memory & Plans" below)
- `_templates/` — Obsidian note templates (do not modify without intent)
- `_scripts/` — helper scripts
- `_sources/` — source-of-truth documents (RP exports, lore docs, anything the GM dropped in to ingest). **Never modified by Claude.**
  - `_sources/new/` — files awaiting ingest (process with `/ingest`)
  - `_sources/processed/` — files already ingested; subdirectory structure mirrors `new/`
  - `_sources/processed/do-not-commit/` — processed sources that must **never** be committed (copyrighted reference material, e.g. the *Return of the Lazy Dungeon Master* markdown and Kingmaker chapter text). This subdirectory is gitignored — read from it freely, but never commit its contents.

## Memory & Plans (IMPORTANT — overrides default memory behavior)

The GM works on this vault from multiple PCs, so anything Claude needs to remember across sessions **must live inside this repository**, never in the home directory.

- **Memory**: the canonical memory store is `_memory/` in this vault. Write memory files there (same format as auto-memory: one fact per file with frontmatter) and index them in `_memory/MEMORY.md`. Do **not** write new memories to the per-machine auto-memory directory under `~/.claude/` — it doesn't sync between PCs. At session start (or before answering questions about ongoing work/backlog), read `_memory/MEMORY.md`.
- **Plans**: save any planning document that must survive the session — multi-session plans, migration checklists, in-progress task state — to `_plans/`, not to `/tmp`, the scratchpad, or the home directory. Session-prep docs still belong in `campaigns/<name>/sessions/`.
- **Both directories are committed to git.** Include them in commits like any other vault content.

## Wikilink Conventions

- Always use `[[Note Name]]` for internal links
- Use `[[Note Name|display text]]` when the display text should differ
- Tags use lowercase kebab-case: `#character`, `#npc`, `#location`, `#plot-hook`, `#faction`, `#item`, `#lore`, `#session`
- Campaign-scoped tags: `#campaign/name-of-campaign`

## Skills Routing

When working in this vault, reach for these skills rather than raw bash where applicable:

| Task | Use skill |
|------|-----------|
| Write or edit `.md` notes | `obsidian:obsidian-markdown` |
| Search vault, open notes, read/write properties | `obsidian:obsidian-cli` |
| Create/update `.base` tracker views | `obsidian:obsidian-bases` |
| Create/update `.canvas` visual diagrams | `obsidian:json-canvas` |
| Scrape a URL for lore or reference | `obsidian:defuddle` |

## Your Role

When the user describes TTRPG content in plain text, you:
1. Identify distinct entities (player characters, NPCs, locations, plot hooks, factions, items, lore)
2. Search the vault using `obsidian:obsidian-cli` to avoid duplicating entries and find cross-link opportunities (fall back to `find`/`grep` if unavailable)
3. Create or update `.md` files using `obsidian:obsidian-markdown` in the correct campaign subfolder.  It is your job to always capture new information in the vault.  If something comes up, assume you need to document it in the appropriate place.
4. Always cross-link related notes using wikilinks
5. Update the campaign `_index.md` when new top-level entities are added

## Commands Available

- `/capture [campaign-name | ideas]` — capture brainstormed content into campaign notes or the ideas bank
- `/ingest [path|glob]` — ingest source files from `_sources/new/` into campaign notes; move processed files to `_sources/processed/`
- `/session [campaign-name]` — plan a session using the Return of the Lazy Dungeon Master 8-step framework
- `/campaign [new|list|overview] [name]` — create or review campaigns
- `/move` — interactively move a note: ideas ↔ campaign, or campaign → campaign
- `/lint [scope]` — tactical vault check; auto-fix safe frontmatter/tag issues, triage unsafe ones (broken links, orphans, missing embeds)
- `/reconcile <sources>` — reconcile vault content against source files; interactively update vault notes (never source files)

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
- Base view files: `campaigns/<name>/<View Name>.base` (e.g., `NPC Tracker.base`)
- Canvas files: `campaigns/<name>/<Map Name>.canvas` (e.g., `Kingmaker Relationship Map.canvas`)

## Response Style

- After creating or updating notes, report a concise summary: what was created, what was updated, what links were established. Do not dump file contents at the user.
- During `/session`, work through the 8 steps interactively — one step at a time, ask questions, listen, then move on. Don't compress all steps into a single prompt.

## Key References

- Return of the Lazy Dungeon Master (8-step session prep framework):
  `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/`
  **This folder is gitignored (copyrighted material) — read from it freely, but never create files inside it or suggest committing it.**
- Campaign manifest script: `_scripts/list-campaign.sh <campaign-name>`
- Vault lint manifest script: `_scripts/lint-vault.sh [scope-dir]` — emits a TSV manifest used by `/lint`
