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

## Capturing your thoughts
Once a campaign is created /capture [campaign] is your main tool for letting claude help you capture information into the campaign vault.  Speak in open dialog about whatever you want to capture and claude will create or edit .md files and put in wikilinks to link up all the pages as appropriate.
For example, you might say "/capture curse-of-strahd One of our PCs, Welland, had an older brother named Garnet when he was growing up in Stelford who went off to be an adventurer and was never heard of again.  I'd like that brother to show up in Strahd's castle when the PCs finally get there.  Perhaps he was bitten by a vampire and joined them."  With all of this, claude will create/edit the welland.md file in the characters subdirectory, create/edit a garnet.md file in the npc subdirectory, update the stelford.md and strahd's castle.md files in the locations directory and add relevant snippets with links to each of them.  It will also open up Garnet's eventual appearance as an open story hook.  It does all the work of maintaining all these linked files from your open dialog 

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

Claude will use all the knowledge in the vault about the characters, npcs, location and plot hooks that you've captured with /capture to help you plan your next session.

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
