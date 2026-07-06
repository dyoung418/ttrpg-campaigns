---
description: Reconcile vault notes against source files — surface contradictions and interactively update vault content (never the sources)
argument-hint: "<source-path | glob | directory>"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are reconciling the GM's vault against source-of-truth documents the user has pointed you at (typically files under `_sources/processed/` or `_sources/new/`, but any path works).

**Hard rule — never modify source files.** Source files are the historical record. You can only edit vault notes under `campaigns/` and `campaigns/ideas/`. Even when the user decides the vault is wrong and the source is right, you update the vault — never the source.

**Backlink rule — always link vault notes back to their source files.** Whenever you edit a vault note to apply a reconciliation change, ensure the note has a `## Sources` section with a wikilink to the source document: `- [[_sources/processed/<filename>|<display name>]]`. If the section already exists, add the new source rather than replacing what's there. If you create a new stub via `/capture`, pass the source path so the stub is born with the backlink already present. The goal is a clear audit trail: every vault note should point back to the raw documents that shaped it.

Work through this interactively, one question at a time.

---

## Step 1 — Resolve Sources

`$ARGUMENTS` is **required**. If empty, print:

> Usage: `/reconcile <path-or-glob-or-directory>`
>
> Examples:
>   /reconcile _sources/processed/RP14 The Great Feast of Freehaven.md
>   /reconcile _sources/processed
>   /reconcile "_sources/processed/RP1*.md"

…and stop. Do not prompt the user — this command is invasive enough that it should be explicit.

Otherwise resolve the argument:

- **File path:** one file.
- **Directory:** walk `*.md` recursively under it.
- **Glob:** expand it under the cwd.

```bash
# Single file:
ls -1 "<path>"

# Directory:
find "<path>" -type f -name "*.md" | sort
```

Show the user the source list and total count.

---

## Step 2 — Resolve Target Campaign

Ask once: "Which campaign am I reconciling against?"

```bash
find /home/danny/ttrpg_campaigns/campaigns -maxdepth 1 -mindepth 1 -type d ! -name ideas ! -name ".*" | sort | xargs -I{} basename {}
```

If a source file's path strongly suggests a campaign (e.g. lives under a campaign-named subfolder), pre-suggest that — but always confirm with the user.

Wait for an answer.

---

## Step 3 — Extract Claims

Read each source file and build a **claim set**. A claim is one specific fact about one entity. Keep claims atomic — one attribute per claim, not "Edina is alive and lives in Restov."

For each claim, capture:

- **`entity_name`** — the canonical name (Edina Aldori, not "Edina")
- **`entity_type`** — your best guess: `npc`, `character`, `location`, `faction`, `item`, `event`
- **`attribute`** — `status`, `faction`, `location`, `role`, `ownership`, `outcome`, `relationship`, `sequence`
- **`claimed_value`** — what the source asserts (e.g. "wounded", "lives in Restov", "owns the Star Compass")
- **`source_excerpt`** — 3–5 lines around the claim, verbatim, for showing the user
- **`source_path`** + line range

For **RP exports** specifically, focus on:

- Who is alive / present / wounded at the scene (status, location)
- Where the scene happens (location claims about characters)
- Who said or did what (role, relationship)
- Possessions changing hands (ownership)
- Sequence — events implied across the source file (this happened before that)

**Skip noise:** image-only entries, OOC chatter, dice rolls, mechanical clarifications. Skip anything the GM clearly doesn't intend as canon.

Show the user a count: "Extracted N claims from M source files." Do not dump the full list — they'll see them during triage.

---

## Step 4 — Resolve Each Claim Against the Vault

For each claim:

1. **Find the vault note for the entity.** Prefer `obsidian:obsidian-cli` via the Skill tool. Otherwise:
   ```bash
   find /home/danny/ttrpg_campaigns/campaigns/<campaign> -name "<entity>.md" 2>/dev/null
   # Fallback — content search:
   grep -rl "\[\[<entity>\]\]\|^aliases:.*<entity>" /home/danny/ttrpg_campaigns/campaigns/<campaign>/ 2>/dev/null
   ```
2. **Read the resolved note.** If multiple candidates match, ask the user which one is canonical.
3. **Compare claim to vault.** Categorize the outcome:
   - **Agreement** — vault asserts the same value. Skip silently (count for the report).
   - **Vault gap** — vault has no opinion on this attribute. Queue for "vault gaps."
   - **Conflict** — vault asserts something different from the source. Queue for "conflicts."
   - **Missing entity** — no vault note exists. Queue for "missing entities."

**GM-secret exception:** if the vault claims something under a `> [!secret] GM Only` callout that contradicts the source, **do not treat as a conflict** — the secret may be GM truth that the in-fiction source doesn't know yet. Only treat as a conflict when a *non-secret* vault assertion disagrees with the source.

---

## Step 5 — Interactive Triage

Three queues, walked in this order. Within each queue, walk claim-by-claim. One question per message.

### Queue A — Conflicts (highest priority)

For each conflict, present:

```
[Conflict <i> of <N>]
Entity:    Edina Aldori
Attribute: status

Vault — campaigns/kingmaker/npcs/Edina Aldori.md
  status: alive

Source — _sources/processed/RP30 Edina Falls.md, lines 12–18
  "...Edina collapsed, blood pooling beneath her as Pavel pressed both
   hands to the wound. Her eyes fluttered closed, breath shallow..."

Which is correct?
  (v) Vault is right — keep as-is
  (s) Source is right — update vault to: "wounded"
  (e) Edit manually — show me a draft I can refine
  (k) Skip — flag for later
```

On the user's choice:
- **(v):** record as resolved-vault. No edits.
- **(s):** Edit the vault note to match. Preserve frontmatter shape (don't reformat unrelated fields). Body changes: prefer adding a new bullet under an appropriate section (e.g. `## Recent Events`, `## Status History`) rather than overwriting text. Also ensure a `## Sources` section exists with a backlink to the source file.
- **(e):** propose a diff, refine with the user, then apply. Include the source backlink in the diff.
- **(k):** record as deferred.

### Queue B — Vault Gaps (medium priority)

For each gap, present similarly but with vault showing "(no assertion)". Options:

```
  (a) Add to vault — under appropriate section
  (s) Skip
  (b) Batch-add all remaining gaps for this entity
```

On (a) or (b): Edit the vault note to add the new info. For frontmatter facts (status, location, faction), update the frontmatter field. For narrative facts, add a bullet under the right section. Ensure a `## Sources` section exists with a backlink to the source file.

### Queue C — Missing Entities (lowest priority)

For each missing entity:

```
Source mentions:    Berengar of the Northern Reaches
Type guess:         NPC
First seen:         _sources/processed/RP22 The Northern Embassy.md, lines 4–9
Excerpt:            "...the courier was a tall, scarred man calling himself
                     Berengar — he claimed to ride for the Northern Reaches..."

  (c) Create stub via /capture
  (s) Skip
```

On (c): invoke `Skill(skill="capture", args="<campaign>")` and feed it the source excerpt as the brainstorm input. The resulting stub will live in the right subfolder with proper frontmatter.

---

## Step 6 — Never Modify Source Files

Restate this in your head every time you reach for the Edit tool: **source files are read-only to you.** Even when the user says "the source is right and the vault is wrong," the source itself doesn't get touched — you correct the vault to match. If the user wants the source corrected, that's a manual edit they make themselves.

If a vault edit changes a frontmatter field referenced by a `.base` view (e.g. `status:`, `faction:`, `location:`), mention it in the final report so the user can recheck their tracker views.

---

## Step 7 — Edge Cases

- **Multiple sources contradict each other** on the same claim → surface both excerpts side-by-side in the triage prompt and let the user pick canon.
- **Source references an entity by alias** ("the hooded figure" → Lady Jamandi) → require explicit user confirmation before treating the alias as a match.
- **Source references events with no session note in vault** → flag in the report as "session gap — consider `/session` or adding a session note for `<event>`."
- **A vault note has been edited mid-run** → re-read the note before applying further edits to the same file.
- **Source file is unreadable / binary / empty** → skip with a one-line reason in the report.

---

## Step 8 — Report

Format:

```
Reconciled <N source files> against <campaign>.

Claims extracted:   <X>
  Agreement:        <A>
  Conflicts:        <C> total — <C_resolved> resolved, <C_skipped> skipped
  Vault gaps:       <G> total — <G_filled> filled, <G_skipped> skipped
  Missing entities: <M> total — <M_stubbed> stubbed, <M_skipped> skipped

Vault files updated:
  - campaigns/<name>/npcs/Edina Aldori.md (status: alive → wounded)
  - campaigns/<name>/locations/Restov.md (added: known NPC)
  - campaigns/<name>/_index.md (added: Berengar of the Northern Reaches)
  ...

`.base` views to recheck:
  - NPC Tracker.base (status field changed on 3 NPCs)

Open items / deferred:
  - <claim summary> — <source path>:<lines>
  - ...

Session gaps flagged:
  - <event description> — referenced in <source path>
```

Suggest: "Run `/lint <campaign>` to catch any frontmatter side effects."

Do not dump file contents.
