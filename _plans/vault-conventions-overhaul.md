---
type: plan
tags: []
status: complete
created: 2026-07-05
---

# Plan — Vault Conventions Overhaul ("Andrew's Vault Edits")

Resume-able, cross-machine plan for adopting the conventions proposed in `Andrew's Vault Edits.md`
(vault root). This doc is committed to git so any session on any PC can pick up where the last one
left off. Companion memory: `_memory/project_vault_conventions_overhaul.md`.

## Core idea

File **type is structured metadata (`type:`), never a tag**. Tags/links/indexes/skills exist only
to make content **discoverable and retrievable**. Rules live in three non-overlapping canonical
files: `CLAUDE.md` (thin router) → `_meta/conventions.md` (detailed rules) → `_meta/tags.md` (tag
registry). Full detail already written into `_meta/conventions.md` — read that first.

## GM decisions locked in (do not re-litigate)

1. **Rollout is phased:** Phase 1 (docs+templates+normalize) → Phase 2 (automation) → Phase 3
   (new skills).
2. **Automation = scripts + `_index/`, NO symlinks.** Commands already live in-vault at
   `.claude/commands/` and work as project skills; there is no `~/.claude` symlink layer.
3. **New skills:** author `/vault-stitch` now; `/vault-enrich` is documented in the taxonomy but
   NOT authored yet.
4. **rp-scene** (30 session notes): a `rp-scene` **tag** + `status: complete` (not a `session_type`
   field). `rp-scene` is registered Active in `_meta/tags.md`.
5. **`#campaign/<name>` tag:** kept as a registered structural exception (graph filtering) even
   though it duplicates the `campaign:` field. `campaign:` values normalized to folder form.
6. **Status vocabulary:** controlled per-type enums — the authoritative table is
   `_meta/conventions.md` §2.

---

## Phase 1 — Canonical docs, templates, normalization  ✅ DONE (uncommitted)

All work applied to the working tree; **not yet committed**.

- [x] `_meta/conventions.md` created (frontmatter schema, status vocab, tag policy, splitting +
  body modes, scripts/index policy, skill taxonomy).
- [x] `_meta/tags.md` created (`## Active` + `## Proposed` seeded from audited tags).
- [x] `CLAUDE.md` slimmed to a router: added `_meta/`+`_index/` to structure, router pointer, fixed
  command-list drift (`/ideate`, `/flesh-it-out`, `/vault-stitch`), replaced type-name-tag guidance.
- [x] All 9 `_templates/*.md` updated: `tags: []` (no type tag), `sources: []`, `related: []`,
  controlled `status` defaults.
- [x] Migrated **208 notes** (one-time Python script, dry-run reviewed, applied): stripped type-name
  tags; normalized `status` (57 notes); `rp-scene` tag + `complete` (30 sessions); singular
  `source:`→`sources:` list (30 sessions); added empty `sources`/`related`; normalized `campaign:`.
- [x] Verified: 0 leftover type tags, 0 off-vocab statuses, 0 singular `source:`, 208/208 valid YAML.
- [x] Memory recorded (`_memory/project_vault_conventions_overhaul.md` + `_memory/MEMORY.md` index).

### → Commit Phase 1 (first action on the new machine)

Working tree = 220 modified + 2 new paths. Suggested:

```bash
cd <vault>
git checkout -- .claude/settings.local.json   # pre-existing, UNRELATED to this work — do not commit
git add _meta/ _templates/ CLAUDE.md _memory/ _plans/vault-conventions-overhaul.md campaigns ideas
git status   # confirm only the overhaul files are staged
git commit   # message below
```

Suggested commit message:
```
Adopt vault conventions Phase 1: _meta docs + frontmatter/tag normalization

- Add _meta/conventions.md (rules) and _meta/tags.md (registry); slim CLAUDE.md to a router
- Templates: drop type-name tag, add sources/related, controlled status defaults
- Normalize 208 notes: strip type tags, controlled status vocab, source->sources list,
  rp-scene tag + status:complete, campaign field cleanup
```
The one-time migration script lived in a scratchpad (not synced) and is no longer needed — the
migration is already applied.

---

## Phase 2 — Automation: scripts + `_index/` (NO symlinks)  ✅ DONE (2026-07-05)

Implemented as stdlib-only Python 3 (portable to Windows Git Bash) sharing
`_scripts/vaultlib.py` (textual frontmatter editing — only the targeted key is rewritten, so
formatting elsewhere is preserved byte-for-byte). Each script has a thin `.claude/commands/*.md`
wrapper and is listed in CLAUDE.md.

- [x] **`vault-set-tags.py`** — replace/`--add`/`--remove` tags; normalizes to kebab-case;
  refuses type-name tags; unknown tags auto-filed under `## Proposed` in `_meta/tags.md`
  (date + source note) and applied provisionally. `--dry-run` supported (all scripts).
- [x] **`vault-add-source.py`** — idempotent append to `sources:` (dedupe by wikilink target,
  ignoring `|alias`).
- [x] **`vault-rebuild-backlinks.py`** — `related:` = sorted union of **outbound + inbound**
  wikilink connections (per conventions §1/§4), quoted wikilinks. Graph always spans
  `campaigns/` + `ideas/`; optional scope arg limits which notes are rewritten. **`_index.md`
  hub files are excluded from the graph** (they link everywhere → noise). Alias-aware
  resolution; links read from note bodies only (frontmatter `related`/`sources` never feed back).
- [x] **`vault-rebuild-index.py`** — wipes & rebuilds `_index/by-tag/`: one page per tag
  (grouped by campaign, with `type`), plus `_index.md` overview. Hub `_index.md` files excluded.
  Tag `/` → `--` in filenames (`campaign--kingmaker.md`).
- [x] `vault-set-body` **skipped** (optional; `obsidian:obsidian-markdown` covers body writes).
- [x] **`lint-vault.sh` upgraded** — new columns TYPE, STATUS, STATUS_OK (per-type vocab from
  conventions §2; missing-but-required counts as 0; only `lore` may omit), HAS_SOURCES,
  HAS_RELATED, TYPE_TAG. Now also excludes `_index/`, `_memory/`, `_plans/`, `_meta/`.
  `/lint` command updated: new columns documented, obsolete "add the type tag" auto-fix
  **removed**, type-name-tag removal + missing `sources:`/`related:` added as safe fixes,
  off-vocab/missing `status` added as a triage kind.
- [x] Ran both rebuilds: 204 notes' `related:` populated; 21 tag pages + overview written.
  Re-run is idempotent (0 updates). All frontmatter still parses as valid YAML (0 errors).
- [x] Verified: Nyrissa's `related:` = her outbound links ∪ inbound linkers; `_index/by-tag/fey.md`
  lists exactly the fey-tagged notes.

**Finding for a later `/lint` run:** 17 notes (items/locations/npcs, e.g. Nyrissa, Briar,
Thousandbreaths) have a status-requiring `type` but **no `status:` field at all** — needs
GM judgment per entity, so left for `/lint` triage, not auto-fixed.

---

## Phase 3 — `/vault-stitch` skill (+ document `/vault-enrich`)  ✅ DONE (2026-07-05)

- [x] **Authored `.claude/commands/vault-stitch.md`** (house command style). Two modes:
  1. **Registry reconcile (default):** gathers usage evidence per proposed tag, walks the GM
     through promote / merge / reject one at a time (clusters presented as a single family
     decision first), rewrites notes via `vault-set-tags.py`, edits registry rows directly
     (registry is authored data), then reruns `vault-rebuild-index.py`. Never leaves a tag
     half-adjudicated.
  2. **Intake gate (`intake <note> <tags...>`):** judgment rules (normalize, map to active
     near-synonyms, drop type-duplicates/one-offs) + apply via `vault-set-tags.py`, which
     enforces the registry and auto-files unknowns under `## Proposed`.
- [x] **`.claude/commands/ingest.md` edited** to route tags through the intake gate — and its
  pre-Phase-1 drift fixed: was still instructing `tags: [<type>, campaign/<x>]`,
  `status: rp-scene`, and singular `source:`; now conventions-compliant (`rp-scene` tag +
  `status: complete`, `sources:` list via `vault-add-source.py`).
- [x] `/vault-enrich` — documented in `_meta/conventions.md` §6 (Phase 1); intentionally NOT
  authored.
- [x] CLAUDE.md `(planned)` marker removed; README gained a "Vault maintenance commands"
  section covering the four vault-* commands + `/vault-stitch`.
- [x] Verified: merge mechanics dry-run (`villain`→`enemy` on Nyrissa) produce the correct
  tag rewrites; registry row edits are plain Edits. Commit Phase 3.

**The actual reconcile pass over the seeded proposals (villain/dangerous→enemy, bestiary
cluster, deity, timeline) is GM-interactive — run `/vault-stitch` when ready.**

---

## Post-adoption cleanup

- [x] Once all phases land, `Andrew's Vault Edits.md` (vault root) is superseded by the three
  canonical files — moved to `_sources/processed/` (with the `(original)` copy) on 2026-07-05.

## Key references

- Detailed rules: `_meta/conventions.md` · Tag registry: `_meta/tags.md`
- Status vocabulary table: `_meta/conventions.md` §2
- Existing command style to mirror: `.claude/commands/*.md` (e.g. `capture.md`)
- Manifest scripts: `_scripts/list-campaign.sh`, `_scripts/lint-vault.sh`
- Memory: `_memory/project_vault_conventions_overhaul.md`
