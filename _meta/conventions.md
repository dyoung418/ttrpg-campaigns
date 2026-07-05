---
type: meta
tags: []
---

# Vault Conventions

> [!info] Canonical rules — read before vault work
> This file holds the **detailed** vault-management rules. `CLAUDE.md` is a thin router that
> points here; `_meta/tags.md` is the tag registry. The three files have **non-overlapping**
> jobs, so no rule is duplicated and nothing drifts. Treat this file as **configuration/data**,
> not prose to skim.

**Core idea:** file *type* is structured metadata, not a tag. Tags, links, indexes, and skills
all exist to make content **discoverable and retrievable** — to give the graph shape and let
related material be found. Every rule below serves that goal.

---

## 1. Frontmatter

**Frontmatter is canonical.** Indexes, staleness, search, and graph behaviour all derive from
it, so it must be maintained carefully.

Five fields are **index-critical** — they drive cross-note behaviour and must be kept accurate:

| Field     | Meaning |
| --------- | ------- |
| `type`    | What kind of note this is (`npc`, `location`, `session`, …). The **sole** mechanism for expressing type — never encode type as a tag. |
| `status`  | Lifecycle state. A **controlled, per-type vocabulary** (see §2). |
| `tags`    | Cross-cutting themes only — see §3 and `_meta/tags.md`. |
| `sources` | Where the content came from. Always a **list** (plural), even for a single entry. |
| `related` | Auto-derived, script-maintained list of the note's wikilink connections — a quick-reference index of everything the note touches. **Not hand-curated** (see §5). |

Notes also carry **housekeeping fields** (`campaign`, `aliases`, `created`) and **type-specific
fields** (e.g. `player`/`class` on characters, `region` on locations, `rarity` on items). Those
are governed by the templates in `_templates/`; the five above are the ones indexing depends on.

---

## 2. Status vocabulary

`status` is a **controlled enum, scoped per type**. Only the values below are valid. Narrative
nuance ("destroyed — routed at Willowshade; Darian killed") belongs in the **note body** (e.g. a
`## Current Status` line), never in the `status` field.

| Type        | Allowed values |
| ----------- | -------------- |
| `npc`       | `alive`, `deceased`, `missing`, `captive`, `unknown` |
| `character` | `active`, `retired`, `deceased` |
| `location`  | `accessible`, `hostile`, `contested`, `cleared`, `ruined` |
| `plot-hook` | `open`, `active`, `resolved`, `abandoned` |
| `faction`   | `active`, `defeated`, `destroyed`, `unknown` |
| `item`      | `unacquired`, `held`, `lost`, `destroyed` |
| `lore`      | `stub`, `established` *(optional — lore may omit `status`)* |
| `session`   | `planned`, `complete` |

> [!note] Session sub-type
> Roleplay-scene session notes carry the `rp-scene` **tag** (a legitimate cross-cutting axis) and
> a normal lifecycle `status` (usually `complete`) — `status` is never overloaded to mark them.

When a note's real-world state doesn't match an allowed value, pick the closest enum and record
the specifics in the body. Extending a type's vocabulary is a deliberate change to this table.

---

## 3. Tags

Tags are **controlled, retrievable labels — not free-form keywords.** They exist for discovery
and indexing: to collect relevant material together and give the graph view shape. The active
set lives under `## Active` in `_meta/tags.md`.

**Type is not a tag.** `type:` already captures what a note *is*, so re-encoding it as a tag adds
nothing. Tags are reserved for **cross-cutting retrieval axes** that group *across* types — e.g.
`fey`, `first-world`, `undead`, `artifact` — connections `type:` can't express.

**Format:** lowercase-kebab-case, in YAML frontmatter (block-list style).

**Structural exception:** `campaign/<name>` scope tags are allowed even though `campaign:` is
also a field — they're kept for Obsidian graph filtering and are listed as active in the
registry.

**Creating a tag.** Only when it is a **real, reusable retrieval axis**. Do not create tags that
duplicate `type:`, or that are vague one-offs used by a single note.

**Intake of a new tag.** If work needs a tag that isn't active yet:
1. Add it under `## Proposed` in `_meta/tags.md` with the **date**, the **source note path**, and
   likely **synonym / merge candidates**.
2. You may apply it **provisionally** to the note.
3. **Never silently invent tags** — every new tag is recorded as proposed first.

**Governance — `/vault-stitch`.** The review path for cross-cutting content across notes. Runs
two ways:
- **On-demand:** reconcile the registry — walk each `## Proposed` tag and **promote → `## Active`**,
  **reject**, or **merge** into an existing tag, rewriting affected notes.
- **`/ingest` intake gate:** as content comes in, validate its tags against the registry,
  dedupe/merge, and file anything unknown under `## Proposed`.

General vault hygiene (orphans, broken links) stays in `/lint`. `/vault-stitch` owns the
connective/cross-cutting layer.

---

## 4. File size & splitting

**File size is a signal, not a rule.** Split a note when its content contains **independently
useful topics** — sections worth retrieving on their own — not merely because it's long.

**Template skeletons don't count toward splitting.** Each type's template defines a fixed set of
H2 sections (a Character always has *Backstory Hook, Motivations, Character Arc,* …). These
**skeleton** sections are expected furniture, not evidence of sprawl. Splitting logic **ignores
skeleton H2s** (a script can read the template to know which headers are structural) and looks at:
- **Added sections** — H2s beyond the type's skeleton (e.g. `## Backstory — Edina Aldori`), and
- **Section weight** — how large or self-structured any single section has become.

**Whole-file review triggers** — these don't force a split; they mean *stop and evaluate by topic
boundaries*:

| Signal | Action |
| --- | --- |
| Multi-file source **with a routing table** | **Split** |
| Single file **with a routing table** | Strongly consider **split** |
| Typed note near its template skeleton, `< ~200` lines | Keep **flat** |
| `≥ 2` **added** (non-skeleton) H2s, **or** `≥ 500` lines total | Inspect structure; split on topic boundaries |
| Any single section large (`~≥ 50–60` lines) **or** with its own H3s | Evaluate *that section* for split-off |
| Anything in between | Split only if sections are useful as **separate retrieval targets** |

> **Routing table:** a table of links/pointers to sub-files or sub-topics that stands in for the
> full content — a note whose job is to *route* the reader onward rather than hold everything.

### Splitting a section — extract, but leave a stub

The unit of splitting is the **section**, and splitting never removes it from the parent. A
section becomes a split candidate only when **both** hold:
1. **It has outgrown its home** — large (`~≥ 50–60` lines) *or* it has developed its own **H3
   sub-structure**, and
2. **It is independently useful** to link or retrieve on its own.

Skeleton sections use the **higher end** of that size bar — they're *meant* to live in the parent,
so they only leave once they clearly dominate it (e.g. a two-line "Backstory Hook" grown into a
200-line backstory).

When you extract a section:
- **Child file** — `<folder>/<Name> — <Section>.md`, a sibling in the same folder, holding the
  full content (body mode `verbose`, or `copy` for fragile source text). It links back to the
  parent, so it appears in the parent's `related`.
- **Parent stub** — keep the H2 header; replace the body with a **1–3 sentence standalone
  summary** plus a `[[<Name> — <Section>]]` link. The parent always still *has* the section — just
  in `summary`/`brief` form.

So a split is described in body-mode terms: **parent stub = `summary`/`brief`, child =
`verbose`/`copy`.** Reading the parent stays lean; full detail is one link away and independently
retrievable.

**References may be deep and long** if that's their natural scope. Do **not** shrink a reference
just to look compact — compactness comes from **curated router tables**, not artificially short
files. When adding material, **fold it into an existing reference as a new H2** if it strengthens
the same topic; create a new reference only when it's a durable, reusable topic of its own.

### Body modes — a decision vocabulary

A shared language for "how much source to store," *not* a stored field. Use it when deciding how
much of an external source a note mirrors locally:

| Mode      | Use when |
| --------- | -------- |
| `copy`    | Full original — only for short / fragile / ephemeral sources. |
| `verbose` | Deep structured note, so agents can answer without re-fetching. |
| `summary` | Stable source whose details can be re-fetched when needed. |
| `brief`   | Pointer only — for live docs, dashboards, repos, or tickets. |

---

## 5. Scripts — graph & index work

**Do graph and index work with scripts; never hand-edit derived data.** Derived artifacts
(`_index/` collections, backlinks, the `related` field, bulk tag rewrites) are generated, not
authored by hand.

- **`_index/`** holds the generated indexes (e.g. `by-tag`) and is **git-synced** across machines.
- **Helper scripts** in `_scripts/` perform all programmatic edits so notes are never
  hand-mangled. User-facing ones are exposed as `.claude/commands/` skills:
  - `vault-set-tags` — set/normalize a note's tags (validated against `_meta/tags.md`)
  - `vault-add-source` — append an entry to a note's `sources` list
  - `vault-rebuild-backlinks` — regenerate backlinks and the `related` field
  - `vault-rebuild-index` — regenerate `_index/` (e.g. `by-tag`)
- **No symlinks.** Commands already live in-vault at `.claude/commands/` and work as project
  skills; there is no `~/.claude` symlink layer to maintain.

---

## 6. Skill taxonomy

| Skill           | Role |
| --------------- | ---- |
| `/ideate`       | Muse — spark ideas and questions (no writing). |
| `/capture`      | Record already-brainstormed content into notes. |
| `/flesh-it-out` | **Deepen existing** notes by filling gaps. |
| `/vault-enrich` | **Grow new** content across a domain, weaving in existing material — user-approved. *(planned; not yet authored)* |
| `/vault-stitch` | Govern the cross-cutting/connective layer — the tag registry (see §3). |

`/vault-enrich` takes a **domain** (a bounded slice of the vault — a campaign plus a category or
theme, e.g. "Kingmaker fey" or "Brevoy politics") and works to **expand** it, traversing the vault
for inspiration and tie-ins so new content is woven into what already exists. Everything it
proposes must be cleared by the GM.
