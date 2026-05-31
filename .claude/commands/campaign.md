---
description: Create a new campaign, list all campaigns, or get an overview of an existing one
argument-hint: "new <name> | list | overview <name>"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are helping a GM manage TTRPG campaigns in an Obsidian vault.

## Parse Arguments

`$ARGUMENTS` will be one of:
- `new <campaign-name>` — create a new campaign
- `overview <campaign-name>` — summarize an existing campaign's current state
- `list` — list all campaigns with entity counts
- *(empty)* — ask the user what they want to do

---

## `list`

Run:
```bash
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d | sort
```

For each campaign, show counts of each entity type:
```bash
bash /home/danny/ttrpg_campaigns/_scripts/list-campaign.sh <name>
```

Present a clean summary table.

---

## `new <campaign-name>`

1. **Normalize the name**: lowercase, hyphens for spaces (e.g. "Curse of Strahd" → `curse-of-strahd`). Ask the user to confirm the display name (e.g. "Curse of Strahd") separately.

2. **Create folder structure**:
```bash
mkdir -p /home/danny/ttrpg_campaigns/campaigns/<name>/{characters,npcs,locations,plot-hooks,factions,items,lore,sessions}
```

3. **Create `_index.md`** from the `_templates/CampaignIndex.md` structure. Fill in:
   - Campaign display name
   - Creation date (today's date)
   - Ask the user: what system? What's the one-sentence premise?

4. **Update `Home.md`**: Add `[[campaigns/<name>/_index|<Display Name>]]` under the "All Campaigns" section.

5. **Create campaign tracker views** using `obsidian:obsidian-bases`:
   - `campaigns/<name>/NPC Tracker.base` — columns: name, status, faction, location, role
   - `campaigns/<name>/Plot Hook Board.base` — columns: name, status, priority
   - `campaigns/<name>/Session Log.base` — columns: session_number, title, date, status

6. Report success and prompt: "Use `/capture <name>` to start adding player characters, NPCs, locations, and plot hooks."

---

## `overview <campaign-name>`

1. Read `campaigns/<name>/_index.md`

2. Run the manifest script:
```bash
bash /home/danny/ttrpg_campaigns/_scripts/list-campaign.sh <name>
```

3. Read open/active plot hooks:
```bash
grep -rl "status: open\|status: active" /home/danny/ttrpg_campaigns/campaigns/<name>/plot-hooks/ 2>/dev/null
```
Read each one and summarize.

4. Read the most recent session note (highest number) for story state.

5. Present a narrative summary covering:
   - Campaign premise
   - Where the party is now and what they're facing
   - Active plot threads (brief)
   - Session count and most recent session
   - Entity counts (NPCs, locations, etc.)

Keep it scannable — this is a quick brief before a session, not an essay.
