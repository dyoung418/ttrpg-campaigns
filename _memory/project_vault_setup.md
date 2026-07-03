---
name: vault-setup-complete
description: "TTRPG Obsidian vault at /home/danny/ttrpg_campaigns is fully set up with commands, templates, and scripts"
metadata: 
  node_type: memory
  type: project
  originSessionId: 30982fbb-9307-4dc1-a7e1-4bb7bd7da51d
---

The TTRPG campaign vault has been built and is ready to use.

**Why:** User wants to talk in plain text to Claude and have it organize content into linked Obsidian notes for TTRPG campaign management.

**How to apply:** When the user starts a new session here, the vault is ready — point them to `/campaign new`, `/capture`, and `/session` to get started.

## What's in place

- `CLAUDE.md` — standing instructions Claude reads each session
- `Home.md` — top-level hub (updated automatically by `/campaign new`)
- `.claude/commands/capture.md` — `/capture` slash command: converts plain text into organized NPC/Location/PlotHook/etc. notes with wikilinks
- `.claude/commands/session.md` — `/session` slash command: interactive 8-step session prep using *Return of the Lazy Dungeon Master* framework
- `.claude/commands/campaign.md` — `/campaign` slash command: create/list/overview campaigns
- `_templates/` — 8 templates: NPC, Location, PlotHook, Faction, Item, Lore, Session, CampaignIndex
- `_scripts/list-campaign.sh` — bash manifest script called during /session to enumerate entities
- `campaigns/` — empty, ready for first campaign
- `TTRPG-general-references/Return of the Lazy Dungeon Master Markdown/` — already present, used by /session

## The 8 RLDM steps (used in /session)
1. Review the characters
2. Create a strong start
3. Outline potential scenes
4. Define secrets and clues
5. Develop fantastic locations
6. Outline important NPCs
7. Choose relevant monsters
8. Select magic item rewards

## Decision: no Obsidian MCP
User asked about Obsidian MCP tools. Decided to skip for now — native file tools (Read/Write/Edit/Bash) are sufficient for the vault management workflow. Revisit if surgical section edits or complex metadata queries become painful.
