---
description: Tactical vault sanity check — auto-fix safe frontmatter/tag issues, report unsafe issues (orphans, broken links, missing embeds) for user triage
argument-hint: "[campaign-name | ideas | (empty for all)]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
---

You are running a tactical lint over the GM's Obsidian vault. Two passes:

1. **Auto-fix safe issues silently.** Things with one obvious correct answer (missing `created` date, missing campaign tag, tags-as-string, etc.). Edit in place. Log each fix.
2. **Report unsafe issues for triage.** Things that need judgment (broken wikilinks, orphans, ambiguous types). Group them, then walk the user through them one question at a time.

**Scope discipline.** Only touch `campaigns/` and `ideas/`. Never modify files under `_sources/`, `_templates/`, `TTRPG-general-references/`, `.obsidian/`, `_assets/`, or `_scripts/`.

**Body content is sacrosanct.** Auto-fixes only edit frontmatter or append a trailing newline. Never touch body prose.

---

## Step 1 — Resolve Scope

Based on `$ARGUMENTS`:

- **Empty:** scope is `campaigns/` ∪ `ideas/`.
- **`ideas`:** scope is `/home/danny/ttrpg_campaigns/ideas/`.
- **A campaign name:** scope is `/home/danny/ttrpg_campaigns/campaigns/<name>/`.
- **A glob:** resolve it under `campaigns/` or `ideas/`.

State the scope to the user before doing anything.

---

## Step 2 — Build the Vault Index

Run the helper script to get a TSV manifest of every file in scope:

```bash
bash /home/danny/ttrpg_campaigns/_scripts/lint-vault.sh /home/danny/ttrpg_campaigns/<scope-path>
```

Each row gives you: path, folder, has-frontmatter, has-type, has-campaign, has-created, tags-form, outbound-link count, outbound-embed count. Keep this manifest in working memory for the rest of the run.

You will also need an **inbound link map** for orphan detection. For each file in scope, count how many other files reference it by basename:

```bash
# Per file (basename without .md):
grep -rl "\[\[<basename>\(\||\]\)" /home/danny/ttrpg_campaigns/campaigns /home/danny/ttrpg_campaigns/ideas 2>/dev/null
```

Cheaper alternative: do a single grep dump and bucket results in your head:

```bash
grep -rohE "\[\[[^]]+\]\]" /home/danny/ttrpg_campaigns/campaigns /home/danny/ttrpg_campaigns/ideas 2>/dev/null | sort | uniq -c | sort -rn
```

---

## Step 3 — Auto-Fix Safe Issues

For each file in scope, apply these fixes silently. Edit only the frontmatter block (or append a trailing newline). Log each fix with file path + what changed; you'll surface the list in the final report.

| Issue | Fix |
|---|---|
| Missing `created` field | Use `git log --diff-filter=A --follow --format=%aI -- "<path>" \| tail -1 \| cut -d'T' -f1`. If git returns nothing, use today's date (`date +%Y-%m-%d`). |
| `campaign:` is set but `campaign/<name>` tag missing | Add `campaign/<name>` to the `tags:` array. |
| `tags:` value is a bare string (e.g. `tags: npc`) | Convert to array form: `tags: [npc]`. If comma-separated (`tags: npc, location`), split it. |
| Missing trailing newline | Append `\n`. |
| `type:` missing AND folder is unambiguous | Set `type:` from the folder name (mapping below). |
| `campaign:` empty/missing but path is `campaigns/<name>/...` | Set `campaign: <name>`. |
| `tags:` is missing the type tag itself | Add the type tag. |

**Folder → type mapping:**

| Folder | Type |
|---|---|
| `characters` | `character` |
| `npcs` | `npc` |
| `locations` | `location` |
| `plot-hooks` | `plot-hook` |
| `factions` | `faction` |
| `items` | `item` |
| `lore` | `lore` |
| `sessions` | `session` |
| `encounters` | `encounter` |

**Important:** if a file has *no frontmatter at all* (no leading `---` block), do **not** auto-insert one. Add the file to the Step 4 report as "missing frontmatter — needs decision." A file with no frontmatter might be a draft, a template fragment, or something else the user knows about.

Use the Edit tool for each fix. Batch multiple frontmatter fixes for the same file into a single Edit when possible.

---

## Step 4 — Detect Unsafe Issues

Build a list of unsafe issues, grouped by kind. Do not edit anything yet.

### 4a. Broken wikilinks

For every outbound `[[Foo]]` link in scope, check whether `Foo.md` exists anywhere in the vault (Obsidian resolves by name). If no match, it's a broken link.

```bash
# All wikilink targets in scope:
grep -rohE "\[\[[^]]+\]\]" /home/danny/ttrpg_campaigns/campaigns /home/danny/ttrpg_campaigns/ideas 2>/dev/null \
  | sed 's/^\[\[//; s/\]\]$//' \
  | cut -d'|' -f1 \
  | cut -d'#' -f1 \
  | sort -u
```

For each unique target, check existence:
```bash
find /home/danny/ttrpg_campaigns -name "<target>.md" -not -path "*/TTRPG-general-references/*" 2>/dev/null
```

### 4b. Broken embeds

For every `![[image.png]]` (or other extension), check whether the file exists somewhere — typically `_assets/`:

```bash
find /home/danny/ttrpg_campaigns/_assets /home/danny/ttrpg_campaigns/campaigns -name "<file>" 2>/dev/null
```

### 4c. Orphans

A file is an **orphan candidate** if it has zero inbound wikilinks anywhere in scope, AND it is not referenced from any `_index.md`, AND it is not itself an `_index.md`. Use the inbound link map from Step 2.

### 4d. Missing type / ambiguous folder

If a file has `type:` missing AND it sits in an unrecognized folder (not in the Step 3 mapping), it's unsafe to auto-fix. Report it.

### 4e. Frontmatter contradictions

- `campaign:` says one campaign, path says another → conflict.
- `type:` says `npc` but `tags:` includes `location` → conflict.

### 4f. `.base` property drift

Find every `.base` file in scope. Parse its `filters:` block (look for `file.inFolder("path/x")`) and its `properties:` keys. For each property, count how many notes matched by the filter actually use that frontmatter key. If 0 of N use it, flag drift.

```bash
find /home/danny/ttrpg_campaigns/campaigns /home/danny/ttrpg_campaigns/ideas -name "*.base"
```

### 4g. Ambiguous wikilink targets

If two notes have the same basename in different folders (e.g. `ideas/npcs/Cat.md` and `campaigns/kingmaker/npcs/Cat.md`), `[[Cat]]` is ambiguous. Build a basename → paths map and flag any with >1 path.

---

## Step 5 — Interactive Triage

Present the unsafe-issue list to the user grouped by kind, with counts. Then walk through each kind one question at a time. Do not ask multiple questions at once.

**Example flow:**

> Found 3 broken wikilinks:
>   - `[[Korga the Bold]]` referenced from `campaigns/kingmaker/npcs/Vorgan.md`
>   - `[[Bridge of Sighs]]` referenced from `campaigns/kingmaker/locations/Restov.md`
>   - `[[Star Compass]]` referenced from `campaigns/kingmaker/plot-hooks/Search for the Compass.md`
>
> For each one: should I (s)tub a placeholder note, (t)reat as typo (you'll tell me the correct target), or (i)gnore?

Apply user-confirmed edits using Edit. For "stub": create a minimal frontmatter-only note in the correct subfolder. For "typo": ask the user for the correct name, then Edit the referencing file to fix the link.

**Per-kind triage options:**

| Kind | Options |
|---|---|
| Broken wikilink | `(s)tub, (t)ypo → fix link, (i)gnore` |
| Broken embed | `(r)eplace path, (i)gnore` |
| Orphan candidate | `(l)ink from nearest `_index.md`, (i)gnore` |
| Missing type | `(t)ype: <inferred from content>, (s)kip` |
| Contradiction | `(p)refer path (update frontmatter), (f)refer frontmatter (move file), (s)kip` |
| `.base` drift | `(r)emove property from .base, (i)gnore` |
| Ambiguous link | Report only — too dangerous to auto-fix |

For batched issues of the same kind, offer a "(a)pply to all" shortcut where it's safe.

---

## Step 6 — Edge Cases

- **File with no frontmatter at all:** report under "Skipped — needs decision." Ask the user separately whether to insert minimal frontmatter inferred from the folder, or leave alone.
- **`_index.md` files** are tracked but treated as roots — they are exempt from orphan detection.
- **Stub creation:** when the user picks (s)tub for a broken wikilink, create the file in the subfolder matching the inferred type, with only frontmatter (no body content). Flag it in the report so the user can `/flesh-it-out` later.
- **Auto-fix collision:** if a file has multiple safe fixes, batch them into a single Edit pass — don't re-open the file multiple times.

---

## Step 7 — Report

Format:

```
Scope: <path or "all">

Auto-fixed: <N> files
  - <path>: added created date (2025-04-12)
  - <path>: normalized tags to array, added campaign/kingmaker
  - <path>: set type: npc from folder
  ...

Needs decision: <N> issues
  Broken wikilinks (M): <list with referencing files>
  Broken embeds (M): <list>
  Orphans (M): <list>
  Missing types (M): <list>
  Contradictions (M): <list>
  Base drift (M): <list>
  Ambiguous links (M): <list>

Skipped — no frontmatter (N files):
  - <path>
  ...
```

Close with: "Run `/lint <scope>` again to confirm clean."

Do not dump file contents.
