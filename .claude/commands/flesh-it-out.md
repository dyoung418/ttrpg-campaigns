---
description: Relentlessly interview the GM to fill gaps in campaign notes, then capture all answers and refactor files as needed
argument-hint: "[campaign-name]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are helping a GM develop their TTRPG campaign by surfacing and filling gaps in their notes.

## Step 1 — Resolve Campaign

**If `$ARGUMENTS` names a campaign:** use `campaigns/$ARGUMENTS/` as the target.

**If `$ARGUMENTS` is empty:** list available campaigns:
```bash
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d | sort
```
Ask which campaign to work on.

## Step 2 — Survey Gaps

Read all existing notes in the campaign to build a picture of what's missing, unresolved, or underdeveloped:

```bash
find /home/danny/ttrpg_campaigns/campaigns/<name> -name "*.md" | sort
```

Read every file. Look specifically for:

- **Placeholder names**: "The Wizard", "The Merchant", "Unknown", "TBD", generic labels used in place of real names
- **Empty or unfilled template fields**: blank Description, Personality, Background sections in NPC files; empty Aspects in Location files; etc.
- **Open design questions**: lines marked `- [ ]`, phrases like "TBD", "decide before", "to determine", "open question"
- **Stubs**: files with only frontmatter and a single line, or that are referenced by wikilink but don't exist yet
- **Thin plot hooks**: hooks with no "What's Actually Happening" or no "Possible Outcomes"
- **Disconnected entities**: NPCs with no location, locations with no NPCs, plot hooks with no NPCs involved
- **Unresolved tensions explicitly noted**: things the GM flagged as needing a decision
- **Property-level gaps**: use `obsidian:obsidian-cli` to query notes with missing or empty frontmatter properties (e.g., NPCs with no `faction`, locations with no `region`), notes with no backlinks (orphaned notes nothing links to), and property values still set to placeholder strings (`unknown`, `TBD`, etc.)

Build a ranked list of gaps, most impactful first. An unnamed primary antagonist matters more than a missing room description.

## Step 3 — Interview

Work through the gaps as a relentless but collaborative interviewer. Rules:

- **One question at a time.** Never ask multiple questions in a single message.
- **Start with the highest-impact gap** — usually the thing that most other details depend on (e.g., the antagonist's name and core motivation before their appearance).
- **Offer a suggested answer** whenever you have enough context to make a reasonable one. Frame it as a springboard, not a prescription: *"What's the wizard's name? I'm thinking something like Valdris Sorn — scholarly but sinister — but what feels right to you?"*
- **Push past vague answers.** If the user says "he's evil and wants power," ask what kind of power, why he wants it, what he gave up to pursue it.
- **Accept uncertainty gracefully.** If the user says "I don't know yet," note it and move on to the next gap. Don't circle back to the same unanswered question in the same session.
- **Connect the dots aloud.** When an answer to one question resolves or changes something else, say so: *"That means the ritual chamber is probably in the highest tower level — want me to update the prison notes to reflect that?"*
- **Keep going.** Don't ask "should I continue?" Just continue. The user will say when they're done.
- **Stop when the user signals done** — "that's enough", "let's stop here", "capture what we have", or similar.

## Step 4 — Capture and Refactor

Once the interview is complete (user signals done, or all major gaps are exhausted):

**4a — Rename placeholder files if a real name was established.**

For each placeholder that got a real name (e.g., "The Wizard" → "Malachite Vorn"):
1. Create the new file at the correct path with the real name
2. Copy content from the placeholder file, updated with the new name throughout
3. Delete the placeholder file
4. Find and update every wikilink across the campaign that referenced the old name:
   ```bash
   grep -rl "The Wizard" /home/danny/ttrpg_campaigns/campaigns/<name>/ 2>/dev/null
   ```
   Edit each occurrence — both `[[The Wizard]]` wikilinks and prose references.

**4b — Fill in answers to empty fields.**

For each file that had gaps the interview resolved, edit the file to fill in the relevant sections. Only write what the user actually said — do not invent details.

**4c — Create new files for any entities that emerged.**

If the interview surfaced new NPCs, locations, factions, items, or lore that don't have files yet, create them using the templates in `_templates/` as structure guides.

**4d — Update the campaign `_index.md`.**

Add any new entities. Update any entries that changed (e.g., renamed NPCs).

## Step 5 — Report

Tell the user concisely:
- Which **placeholder names were replaced** (old → new) and how many files were updated
- Which **files were filled in** with new detail
- Which **new files were created**
- Which gaps remain **unanswered** (the user said "I don't know yet") — list them so the user knows what to think about before next time
- Suggest: "Run `/flesh-it-out $ARGUMENTS` again whenever you're ready to tackle the remaining gaps."

Do not dump file contents at the user.
