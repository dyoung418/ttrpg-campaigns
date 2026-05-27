# TTRPG Campaign Vault

An Obsidian vault for managing tabletop RPG campaigns, maintained with [Claude Code](https://claude.ai/code).

## Setup

1. Clone this repo
2. Open the folder as an vault in [Obsidian](https://obsidian.md)
3. Open the folder in Claude Code

## Usage

Talk to Claude in plain text. At the beginning, use /campaign new.  Three slash commands are available:

| Command | What it does |
|---------|-------------|
| `/campaign new <name>` | Create a new campaign with full folder structure |
| `/campaign list` | List all campaigns with entity counts |
| `/campaign overview <name>` | Summarize a campaign's current state |
| `/capture [campaign]` | Convert brainstormed ideas into organized, linked notes |
| `/session [campaign]` | Plan a session using the 8-step Lazy Dungeon Master framework |

## Session Planning Framework

The `/session` command walks through the 8 steps from *Return of the Lazy Dungeon Master* by Sly Flourish:

1. Review the characters
2. Create a strong start
3. Outline potential scenes
4. Define secrets and clues
5. Develop fantastic locations
6. Outline important NPCs
7. Choose relevant monsters
8. Select magic item rewards

> **Note:** The book text is not included in this repo (copyrighted). Add your own copy to `TTRPG-general-references/` locally — Claude will reference it during session planning.

## Vault Structure

```
campaigns/<name>/
├── _index.md          # Campaign hub
├── npcs/
├── locations/
├── plot-hooks/
├── factions/
├── items/
├── lore/
└── sessions/
```
