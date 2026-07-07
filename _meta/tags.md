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
| `first-world` | setting | The First World plane and its intrusions. |
| `thousandbreaths` | setting/region | The Thousandbreaths region of the First World. |
| `creature-type/aberration` | creature-type | Aberrations. |
| `creature-type/construct` | creature-type | Constructs and animated beings. |
| `creature-type/dragon` | creature-type | Dragons and draconic beings. |
| `creature-type/fey` | creature-type | Fey creatures & the fey-touched. |
| `creature-type/giant` | creature-type | Giants. |
| `creature-type/hag` | creature-type | Hags. |
| `creature-type/humanoid` | creature-type | Humanoids (only when worth retrieving — most NPCs are humanoid). |
| `companion` | role | Party companions / allied followers. |
| `enemy` | role | Antagonists and hostile forces. |
| `artifact` | item-class | Major/legendary items. |
| `ancestor` | theme | Ancestral figures, bloodline history. |
| `backstory` | theme | Figures/content rooted in a PC's pre-campaign backstory — parents, mentors, lost loves, old enemies, home regions, origin mysteries. Applies even once they become active in play. Distinct from `ancestor` (spirit-world bloodline figures). |
| `tome` | item-class | Books, grimoires, records of note. |
| `rp-scene` | session-kind | Roleplay-scene session logs (see `_meta/conventions.md` §2). |
| `dangerous` | hazard | Hazardous items/locations worth retrieving as a group. |
| `deity` | theme | Gods and the divine — deities, holy items, temples. |

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
| *(none)* | | | |

> [!note] Not in this registry
> Type-name tags (`npc`, `location`, …) are **deprecated** — type lives in `type:` only. They are
> not tracked here and are stripped from notes during normalization.
