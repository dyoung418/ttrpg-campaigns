---
description: Plan a session using the Return of the Lazy Dungeon Master 8-step framework
argument-hint: "[campaign-name]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

You are helping a GM plan a TTRPG session using the 8-step framework from *Return of the Lazy Dungeon Master* (RLDM). The full text is at `TTRPG-general-references/Return of the Lazy Dungeon Master Markdown/` — consult it if the user wants guidance on any step.

Work through the steps **interactively**, one at a time. Ask questions, listen to answers, then move to the next step. Don't rush through everything at once.

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

Read the Party table from `_index.md`. Present each PC's name, background hook, and item wish list to the user.

Ask: "Has anything changed with the characters? Any new backgrounds, goals, or items they're after?"

Goal: wire the characters into your mind before the rest of prep. Everything else should connect back to them.

*Reference: `05_review_the_characters.md`*

---

## Step 2 — Create a Strong Start

Ask: "How do you want to open this session? Think: what's happening, what's the hook, where's the action?"

Guide toward specificity. Push for *in medias res* — start as close to the action as possible. Aim for a single vivid sentence or short paragraph. Ask the three questions if needed:
- What's happening? (an event frames the scene)
- What's the point? (the hook that sends characters into the adventure)
- Where's the action? (start close to it — when in doubt, start with combat)

*Reference: `06_create_a_strong_start.md`*

---

## Step 3 — Outline Potential Scenes

Ask: "Sketch 3–6 scenes you think might happen — just a few words each. These are disposable, just to help you feel prepared."

Remind the user: 1–2 scenes per hour of play is enough. They don't need to be sequential. Be ready to throw them away.

*Reference: `07_outline_potential_scenes.md`*

---

## Step 4 — Define Secrets and Clues

Read existing plot hook files to identify active threads:
```bash
grep -rl "status: open\|status: active" /home/danny/ttrpg_campaigns/campaigns/<name>/plot-hooks/ 2>/dev/null
```

Then collaboratively brainstorm up to 10 single-sentence secrets the characters might discover this session. Each is a piece of story, history, or world the characters can uncover. Suggest some based on active hooks; ask the user for more.

Key rule: keep secrets **abstract from their discovery method** — don't decide how they'll be found. That gets improvised at the table.

*Reference: `08_define_secrets_and_clues.md`*

---

## Step 5 — Develop Fantastic Locations

For each key location this session, define:
1. An **evocative name** (something that fires the imagination)
2. **Three aspects** — short descriptive tags for interactable features

Check existing location files and link them where applicable. Create stubs for new locations.

Aim for 1–2 locations per hour of play. Tip: scale (huge/ancient things) makes locations fantastic.

*Reference: `09_develop_fantastic_locations.md`*

---

## Step 6 — Outline Important NPCs

For NPCs critical to this session (quest givers, villains, key contacts), note:
- Name and wikilink to their file
- Their role in this session
- A **character archetype from popular fiction** to anchor their portrayal (the further from fantasy, the better)

Check `campaigns/<name>/npcs/` for existing files. Create stubs for new NPCs and offer to `/capture` them afterward.

*Reference: `10_outline_important_npcs.md`*

---

## Step 7 — Choose Relevant Monsters

Ask: "What monsters make sense for the story, situation, and locations this session?"

Use challenge rating only as a loose gauge of difficulty — don't balance encounters mathematically. Choose what fits the fiction.

If there's a boss fight, ask a few extra questions about the boss's capabilities and what would make it memorable.

*Reference: `11_choose_relevant_monsters.md`*

---

## Step 8 — Select Magic Item Rewards

Check the item wish lists in the Party table from `_index.md`.

Suggest 1 magic item that fits the session's story. Consider:
- Does it match a character's wish list?
- Can it be tied to a secret or clue from Step 4?
- Has it been a while since the party received magic?

Can also suggest rolling randomly if the user prefers surprise.

*Reference: `12_select_magic_item_rewards.md`*

---

## Compile Session Note

Once all 8 steps are complete, create the session file at:
`campaigns/<name>/sessions/Session <NN> - <Title>.md`

Use `_templates/Session.md` as the structure. Fill in all 8 sections with the content gathered. Add wikilinks to every NPC, Location, and Plot Hook mentioned.

## Wrap Up

- If any plot hook is being concluded this session, update its `status:` to `resolving`
- If new entities (NPCs, locations, etc.) came up during planning that don't have notes yet, offer to run `/capture` to create them
