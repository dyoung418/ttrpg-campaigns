---
type: meta
tags: []
---

# Tag Registry

> [!info] The controlled tag set
> Tags are **cross-cutting retrieval axes** — never a note's type (that's `type:`). See
> `_meta/conventions.md` §3 for the policy. Only tags under `## Active` may be applied freely;
> everything else goes through `## Proposed` and is adjudicated by `/vault-stitch`.

## Active

Cross-cutting theme tags currently in real use across the vault:

| Tag | Axis | Notes |
| --- | --- | --- |
| `fey` | creature/theme | Fey creatures & the fey-touched. |
| `first-world` | setting | The First World plane and its intrusions. |
| `thousandbreaths` | setting/region | The Thousandbreaths region of the First World. |
| `dragon` | creature | Dragons and draconic beings. |
| `companion` | role | Party companions / allied followers. |
| `enemy` | role | Antagonists and hostile forces. |
| `artifact` | item-class | Major/legendary items. |
| `ancestor` | theme | Ancestral figures, bloodline history. |
| `tome` | item-class | Books, grimoires, records of note. |
| `rp-scene` | session-kind | Roleplay-scene session logs (see `_meta/conventions.md` §2). |

**Structural (allowed exception).** These duplicate a frontmatter field but are kept for graph
filtering:

| Tag | Purpose |
| --- | --- |
| `campaign/kingmaker` | Campaign scope (mirrors `campaign:`). |
| `campaign/lost-memories` | Campaign scope (mirrors `campaign:`). |

## Proposed

Awaiting `/vault-stitch` adjudication (promote → Active, reject, or merge). Format: tag — date
added — source note — merge/synonym candidates.

| Tag | Added | Source note | Merge / synonym candidate |
| --- | --- | --- | --- |
| `villain` | 2026-07-05 | `campaigns/kingmaker/npcs/Nyrissa.md` | **merge → `enemy`** |
| `dangerous` | 2026-07-05 | `campaigns/kingmaker/items/Vordakai's Eye-Gem.md` | **merge → `enemy`** or drop (vague) |
| `humanoid` | 2026-07-05 | `campaigns/kingmaker/npcs/Phomandala.md` | consolidate under a `creature-type` axis? |
| `giant` | 2026-07-05 | `campaigns/kingmaker/npcs/Kargstaad.md` | consolidate under a `creature-type` axis? |
| `hag` | 2026-07-05 | `campaigns/kingmaker/npcs/The Knurly Witch.md` | consolidate under a `creature-type` axis? |
| `construct` | 2026-07-05 | `campaigns/kingmaker/npcs/Rindle (Construct).md` | consolidate under a `creature-type` axis? |
| `aberration` | 2026-07-05 | `campaigns/kingmaker/npcs/The Wriggling Man.md` | consolidate under a `creature-type` axis? |
| `deity` | 2026-07-05 | `campaigns/kingmaker/lore/Erastil.md` | promote (durable axis for gods)? |
| `timeline` | 2026-07-05 | `campaigns/kingmaker/Campaign Timeline.md` | structural one-off; keep or drop |

> [!note] Bestiary cluster
> `humanoid`, `giant`, `hag`, `construct`, `aberration` (plus the active `dragon`, `fey`) read as
> a partial creature-type taxonomy. `/vault-stitch` should decide whether to formalize a
> `creature-type` axis or leave them as individual theme tags.

> [!note] Not in this registry
> Type-name tags (`npc`, `location`, …) are **deprecated** — type lives in `type:` only. They are
> not tracked here and are stripped from notes during normalization.
