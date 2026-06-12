---
description: Plan a session using the Return of the Lazy Dungeon Master 8-step framework
argument-hint: "[campaign-name]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are helping a GM plan a TTRPG session using the 8-step framework from *Return of the Lazy Dungeon Master* (RLDM). The full text is at `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/` — consult it if the user wants guidance on any step.

Work through the steps **interactively**, one at a time. Ask questions, listen to answers, then move to the next step. Don't rush through everything at once.

---

## RLDM 8-Step Framework (Embedded Reference)

*This summary is embedded here so you can run effective session prep even if the reference files at `_sources/processed/do-not-commit/` are unavailable.*

**Step 1 — Review the Characters.** Before anything else, re-read each PC's name, background, and motivations. The goal is to prime your mind so every other prep decision flows from what these specific characters want. Wire the characters into your head first; then every scene, secret, location, and item you create can tie back to them.

**Step 2 — Create a Strong Start.** Write a single vivid sentence (or short paragraph) describing exactly how the session opens. Frame it around three questions: *What's happening?* (a live event in the world), *What's the point?* (the hook that propels the characters forward), and *Where's the action?* (start as close to it as possible — *in medias res*). When in doubt, start with combat.

**Step 3 — Outline Potential Scenes.** Jot a few words per likely scene — just enough to feel prepared, not so much you can't bear to throw it away. One or two scenes per hour of play is sufficient. These can be sequential, parallel, or branching. Expect to improvise; the list exists for your peace of mind, not as a script.

**Step 4 — Define Secrets and Clues.** Write up to 10 single-sentence secrets the characters might discover — facts about NPCs, world history, or the current situation that *matter* to the story. Crucially, keep secrets **abstract from their delivery method**: don't decide which NPC says what or which item holds which clue. Improvise the discovery at the table. Secrets only become real when revealed; unused ones are fine to discard.

**Step 5 — Develop Fantastic Locations.** For each scene backdrop, give it an *evocative name* and *three aspects* (short, interactable features). Aim for 1–2 locations per hour of play. Scale — vast size, great age, strange history — is the fastest way to make a location feel fantastic. Don't over-invest in any single location; you may never use it.

**Step 6 — Outline Important NPCs.** For NPCs critical to this session (quest-givers, villains, key contacts), note their name, their role, and a **character archetype from popular fiction** (the further outside fantasy the better) to anchor your portrayal. Keep notes brief; a name + role + archetype is usually enough. Be ready to reassign information to a different NPC if the planned one falls out of play.

**Step 7 — Choose Relevant Monsters.** List monsters that fit the story, situation, and location — don't balance encounters mathematically. Use challenge rating only as a rough gauge of difficulty. Let the narrative guide encounter size and composition. For boss fights, think about what would make the fight memorable without negating the characters' strengths; add minions, use terrain, and account for the boss having fewer actions than the party.

**Step 8 — Select Magic Item Rewards.** Aim to drop one interesting item per session. Consult each player's wish list (collect these at campaign start and revisit every six sessions). Choose an item that fits the story, ties to a secret or clue, or spotlights a specific character. You can also roll randomly and curate the result for surprise and flavor.

---

## Setup

**Resolve campaign:**
If `$ARGUMENTS` names a campaign, use it. Otherwise list available campaigns:
```bash
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d | sort
```

**Determine session number:**
```bash
find /home/danny/ttrpg_campaigns/campaigns/<name>/sessions -name "*.md" 2>/dev/null | wc -l
```
New session number = count + 1, zero-padded to 2 digits (01, 02, … 10, 11).

**Read story state:**
- Read `campaigns/<name>/_index.md`
- Read the most recent session note (highest number) if one exists
- Run `bash /home/danny/ttrpg_campaigns/_scripts/list-campaign.sh <name>` for a quick entity manifest

---

## Step 1 — Review the Characters

Read all character files:
```bash
find /home/danny/ttrpg_campaigns/campaigns/<name>/characters -name "*.md" 2>/dev/null | sort
```

Read each one. For each PC, extract: name, player, class, backstory hook, motivations, character arc, and magic item wish list.

If no character files exist yet, read the Party table from `_index.md` as a fallback and suggest creating proper character files with `/capture`.

Present a brief summary of each PC to the user — remind them who everyone is and what they want. Then ask: "Has anything changed since last session? New goals, updated wish lists, anything I should know?"

Goal: wire each character into your mind before the rest of prep. As you work through Steps 2–8, keep asking: how does this connect to a specific character's backstory, goals, or arc?

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/05_review_the_characters.md`*

---

## Step 2 — Create a Strong Start

Ask: "How do you want to open this session? Think: what's happening, what's the hook, where's the action?"

Guide toward specificity. Push for *in medias res* — start as close to the action as possible. Aim for a single vivid sentence or short paragraph. Ask the three questions if needed:
- What's happening? (an event frames the scene)
- What's the point? (the hook that sends characters into the adventure)
- Where's the action? (start close to it — when in doubt, start with combat)

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/06_create_a_strong_start.md`*

---

## Step 3 — Outline Potential Scenes

Ask: "Sketch 3–6 scenes you think might happen — just a few words each. These are disposable, just to help you feel prepared."

Remind the user: 1–2 scenes per hour of play is enough. They don't need to be sequential. Be ready to throw them away.

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/07_outline_potential_scenes.md`*

---

## Step 4 — Define Secrets and Clues

Read existing plot hook files to identify active threads:
```bash
grep -rl "status: open\|status: active" /home/danny/ttrpg_campaigns/campaigns/<name>/plot-hooks/ 2>/dev/null
```

Also check the ideas bank for unassigned plot hooks that might fit:
```bash
find /home/danny/ttrpg_campaigns/ideas/plot-hooks -name "*.md" 2>/dev/null | sort
```
If any ideas-bank hooks feel relevant, mention them to the user as potential material to pull in.

Then collaboratively brainstorm up to 10 single-sentence secrets the characters might discover this session. Each is a piece of story, history, or world the characters can uncover. Suggest some based on active hooks; ask the user for more.

Key rule: keep secrets **abstract from their discovery method** — don't decide how they'll be found. That gets improvised at the table.

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/08_define_secrets_and_clues.md`*

---

## Step 5 — Develop Fantastic Locations

For each key location this session, define:
1. An **evocative name** (something that fires the imagination)
2. **Three aspects** — short descriptive tags for interactable features

Check existing campaign location files and link them where applicable:
```bash
find /home/danny/ttrpg_campaigns/campaigns/<name>/locations -name "*.md" 2>/dev/null | sort
```

Also check the ideas bank for unassigned locations that might fit this session:
```bash
find /home/danny/ttrpg_campaigns/ideas/locations -name "*.md" 2>/dev/null | sort
```
If any ideas-bank locations feel relevant, surface them for the user. If they choose to use one, move it into `campaigns/<name>/locations/` and update the ideas index.

Create stubs for new locations.

Aim for 1–2 locations per hour of play. Tip: scale (huge/ancient things) makes locations fantastic.

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/09_develop_fantastic_locations.md`*

---

## Step 6 — Outline Important NPCs

For NPCs critical to this session (quest givers, villains, key contacts), note:
- Name and wikilink to their file
- Their role in this session
- A **character archetype from popular fiction** to anchor their portrayal (the further from fantasy, the better)

Check `campaigns/<name>/npcs/` for existing files. Also check the ideas bank for unassigned NPCs who might slot into this session:
```bash
find /home/danny/ttrpg_campaigns/ideas/npcs -name "*.md" 2>/dev/null | sort
```
Surface any relevant ideas-bank NPCs to the user. Create stubs for new NPCs and offer to `/capture` them afterward.

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/10_outline_important_npcs.md`*

---

## Step 7 — Choose Relevant Monsters

Ask: "What monsters make sense for the story, situation, and locations this session?"

Use challenge rating only as a loose gauge of difficulty — don't balance encounters mathematically. Choose what fits the fiction.

If there's a boss fight, ask a few extra questions about the boss's capabilities and what would make it memorable.

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/11_choose_relevant_monsters.md`*

---

## Step 8 — Select Magic Item Rewards

Check the "Magic Item Wish List" section from each character file in `campaigns/<name>/characters/`. Fall back to the Party table in `_index.md` if character files don't have wish lists yet.

Suggest 1 magic item that fits the session's story. Consider:
- Does it match a character's wish list?
- Can it be tied to a secret or clue from Step 4?
- Has it been a while since the party received magic?

Can also suggest rolling randomly if the user prefers surprise.

*Reference: `_sources/processed/do-not-commit/Return of the Lazy Dungeon Master Markdown/12_select_magic_item_rewards.md`*

---

## Compile Session Note

Once all 8 steps are complete, create the session file at:
`campaigns/<name>/sessions/Session <NN> - <Title>.md`

Use `_templates/Session.md` as the structure. Fill in all 8 sections with the content gathered. Add wikilinks to every NPC, Location, and Plot Hook mentioned.

Use `obsidian:obsidian-markdown` when writing the session note. Key callout sections:
- Strong Start → `> [!info] Read-Aloud` callout wrapping the opening text
- Secrets & Clues → `> [!secret] GM Only` label before the secrets list
- GM Notes → `> [!warning] GM Only` wrapping private prep notes

After creating the session file, open it in Obsidian using `obsidian:obsidian-cli`.

## Wrap Up

- If any plot hook is being concluded this session, update its `status:` to `resolving`
- If new entities (NPCs, locations, etc.) came up during planning that don't have notes yet, offer to run `/capture` to create them
