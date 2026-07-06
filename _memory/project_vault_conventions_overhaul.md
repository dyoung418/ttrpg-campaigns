---
name: project_vault_conventions_overhaul
description: Adoption of "Andrew's Vault Edits" conventions — canonical _meta docs, frontmatter/tag normalization, and the phased rollout (Phase 1 done; 2 & 3 pending)
metadata:
  type: project
---

Adopting the vault-management conventions from `Andrew's Vault Edits.md` (root). Core idea:
**file type is structured metadata (`type:`), never a tag**; tags/links/indexes exist for
discovery/retrieval. Rules now live in three canonical files: `CLAUDE.md` (router),
`_meta/conventions.md` (detailed rules), `_meta/tags.md` (tag registry). Plan file:
`_plans/` / `~/.claude/plans/i-d-like-to-adopt-dapper-koala.md`.

**Phase 1 — DONE.** Created `_meta/conventions.md` + `_meta/tags.md`; slimmed `CLAUDE.md` to a
router; updated all 9 `_templates/` (dropped type-name tag → `tags: []`, added `sources: []` /
`related: []`, controlled `status` defaults). Ran a one-time Python migration over all **208
notes**: removed type-name tags, normalized `status` to a controlled per-type vocabulary
(see conventions §2), renamed singular `source:`→`sources:` list (30 sessions), added empty
`sources`/`related`. Verified: 0 leftover type tags, 0 off-vocab statuses, 0 singular `source:`.

**GM decisions made (non-obvious):**
- **rp-scene** (30 session notes): use a `rp-scene` **tag** + `status: complete` — NOT a
  `session_type` field. `rp-scene` is registered Active in `_meta/tags.md`.
- **`#campaign/<name>` tag**: kept as a registered structural exception (useful for graph
  filtering) even though it duplicates the `campaign:` field; `campaign:` values normalized to
  folder form (`lost-memories`, unquoted `kingmaker`).
- Prose statuses (Golden Talons, Ovinrbaane, Willowshade, Almon's Hunt) mapped to enums; narrative
  detail was already in each note body, so no body edits were needed.

**Phase 2 — DONE (2026-07-05).** Stdlib-only Python scripts sharing `_scripts/vaultlib.py`
(textual frontmatter editing): `vault-set-tags.py` (validates vs registry, files unknowns under
`## Proposed`, refuses type-name tags), `vault-add-source.py` (idempotent), 
`vault-rebuild-backlinks.py` (`related:` = outbound ∪ inbound; `_index.md` hubs excluded from
graph), `vault-rebuild-index.py` (wipes/rebuilds `_index/by-tag/`, `/`→`--` in filenames). Thin
`.claude/commands/` wrappers for all four; CLAUDE.md updated. `lint-vault.sh` gained
TYPE/STATUS/STATUS_OK/HAS_SOURCES/HAS_RELATED/TYPE_TAG columns; `/lint` rewired (obsolete
"add type tag" fix removed). Rebuilds run: 204 `related:` populated, 21 tag pages; idempotent.
**Known finding left for `/lint`:** 17 notes have a status-requiring type but no `status:`
field (needs per-entity GM judgment).

**Phase 3 — DONE (2026-07-05). All phases complete.** `/vault-stitch` authored (reconcile mode:
promote/merge/reject one tag at a time, clusters as family decisions, rewrites via
vault-set-tags.py, then index rebuild; intake mode: judgment rules + script-enforced registry).
`/ingest` now routes tags through the intake gate, and its pre-Phase-1 drift was fixed (it was
still writing type-name tags, `status: rp-scene`, singular `source:`). `/vault-enrich` stays
documented-only (conventions §6). README gained a "Vault maintenance commands" section.

**First `/vault-stitch` reconcile pass — DONE (2026-07-05).** GM rulings: `villain` merged →
`enemy`; `dangerous` **promoted** (hazard axis, contra the drop hint); bestiary formalized as a
nested **`creature-type/` axis** with `dragon` and `fey` migrated into it too (7 values:
aberration, construct, dragon, fey, giant, hag, humanoid); `deity` promoted; `timeline`
rejected. `## Proposed` is now empty.

**Outstanding follow-ups (not part of the overhaul phases):**
- 17 notes have a status-requiring type but no `status:` field — surface via `/lint`.
- ~~Andrew's Vault Edits.md~~ — done: both files moved to `_sources/processed/` (2026-07-05).

Related: [[project_vault_setup]].
