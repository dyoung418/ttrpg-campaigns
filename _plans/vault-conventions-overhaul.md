---
type: plan
tags: []
status: in-progress
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

## Phase 2 — Automation: scripts + `_index/` (NO symlinks)  ⏳ TODO

Durable helper scripts in `_scripts/` (git-synced); user-facing ones get thin
`.claude/commands/*.md` wrappers. Portability matters (GM uses Linux + Windows Git Bash) — prefer
Python/POSIX, null-delimited paths. Behaviour spec: `_meta/conventions.md` §5.

- [ ] **`vault-set-tags`** — set/normalize a note's `tags`; validate against `_meta/tags.md`
  Active set; unknown tags get filed under `## Proposed` (never silently invented).
- [ ] **`vault-add-source`** — append an entry to a note's `sources:` list (idempotent).
- [ ] **`vault-rebuild-backlinks`** — scan every `[[wikilink]]` across the vault; regenerate each
  note's `related:` field (currently empty everywhere). This is derived data — always regenerate,
  never hand-edit.
- [ ] **`vault-rebuild-index`** — create/regenerate `_index/` (start with `_index/by-tag/`) from
  frontmatter. `_index/` is committed & git-synced.
- [ ] (optional) **`vault-set-body`** — only if scripted callers need it; `obsidian:obsidian-markdown`
  already covers body writes.
- [ ] **Upgrade `_scripts/lint-vault.sh`** — currently emits PATH/FOLDER/HAS_FM/HAS_TYPE/
  HAS_CAMPAIGN/HAS_CREATED/TAGS_FORM/OUTBOUND_*. Add columns/checks for `status` (flag off-vocab
  per type), `sources` present+list, `related` present, and flag any surviving type-name tag. Wire
  new checks into `/lint`.
- [ ] Run `vault-rebuild-backlinks` then `vault-rebuild-index` once to populate `related:` + `_index/`.
- [ ] Verify: a well-connected note (e.g. `campaigns/kingmaker/npcs/Nyrissa.md`) has `related:`
  matching its wikilinks; `_index/by-tag` lists notes under their tags. Commit Phase 2.

---

## Phase 3 — `/vault-stitch` skill (+ document `/vault-enrich`)  ⏳ TODO

- [ ] **Author `.claude/commands/vault-stitch.md`** (match existing command style: `description`,
  `argument-hint`, `allowed-tools` frontmatter — see `.claude/commands/capture.md`). Two modes:
  1. **Registry reconcile (on-demand):** walk each `## Proposed` tag in `_meta/tags.md`; promote →
     `## Active`, reject, or merge; rewrite affected notes via `vault-set-tags`; regenerate indexes.
     First real pass targets the seeded proposals: `villain`/`dangerous`→`enemy`; the bestiary
     cluster (`humanoid`/`giant`/`hag`/`construct`/`aberration`) — decide `creature-type` axis vs
     individual; `deity` promote?; `timeline` keep/drop.
  2. **`/ingest` intake gate:** validate incoming tags against the registry, dedupe/merge, file
     unknowns under `## Proposed`. Requires a small edit to `.claude/commands/ingest.md` to call it.
  - Scope boundary: general hygiene (orphans, broken links) stays in `/lint`; `/vault-stitch` owns
    only the connective/cross-cutting (tag) layer.
- [ ] **Document `/vault-enrich`** — already listed in `_meta/conventions.md` §6 taxonomy; do NOT
  author it this effort.
- [ ] Verify: dry-run the reconcile mode against seeded proposals; confirm a merge (e.g.
  `villain`→`enemy`) rewrites affected notes + updates the registry. Commit Phase 3.

---

## Post-adoption cleanup

- [ ] Once all phases land, `Andrew's Vault Edits.md` (vault root) is superseded by the three
  canonical files — move it to `_sources/processed/` or delete it (GM's call).

## Key references

- Detailed rules: `_meta/conventions.md` · Tag registry: `_meta/tags.md`
- Status vocabulary table: `_meta/conventions.md` §2
- Existing command style to mirror: `.claude/commands/*.md` (e.g. `capture.md`)
- Manifest scripts: `_scripts/list-campaign.sh`, `_scripts/lint-vault.sh`
- Memory: `_memory/project_vault_conventions_overhaul.md`
