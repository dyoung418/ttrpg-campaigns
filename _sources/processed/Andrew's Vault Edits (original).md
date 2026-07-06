## Tags Usage

I have some ideas and pointers around the vault, I think the use of tags as file types loses the ability to group items tighter with tags, and I believe the association of two files as the "same type" isn't as important that deserves a TAG.

Tags will be up to you to decide which to suggest, promote, and ignore. They should all be in an effort to collect relevant information together, giving the graph view more shape and easier discover-ability via tags. 

Type of files will remain a very important part of file meta data.

Vault tags are controlled, retrievable labels, not free-form keywords. Use lowercase-kebab tags in YAML frontmatter, and track active tags in ## Active in .meta/tags.md.

Create a new tag only when it is a real reusable retrieval axis. Avoid tags that duplicate `type:` avoid vague one-offs.

If intake needs a new tag, add it under ## Proposed in .meta/tags with date, source path, and likely synonym/merge candidates. You can apply it provisionally to the note, but do not silently invent tags.

Create a new skill, /vault-stitch, which is the review path for proposed tags to make it into active, be rejected, or merged. 

At the core, tags are for discovery and indexing.

## File size caps and spread

File size is a signal, not a rule. Split when content has independently useful topics, not just because the file is too long.

Default split guide:
- Multi-file source with a routing table: SPLIT
- Single file with a routing table: strongly consider SPLIT
- lines < 200 and h2_count < 4: usually FLAT for characters
- lines < 200 and h2_count < 3: usually FLAT for locations
- lines >= 500 or h2_count >= 4: inspect structure, and decide by topic boundaries
- Otherwise split, only if sections would be useful as separate  retrieval targets

For skills, splitting means: keep skills/slug.md as a thin router, and move durable content to normal file areas, such as /campaigns/kingmaker/<domain>/<domain>-<topic>.md. Do not make the router carry the full knowledge payload.

For references, do not shrink just to look compact. A reference may be deep and long if that is its natural scope. Compactness comes from curated router tables, not artificially short files.

Use body modes to control size:

- copy: full original, only for short/fragile/ephemeral sources
- verbose: deep structured note when agents should answer without re-fetching.
- summary: stable source where details and be re-fetched
- brief: pointer only for live docs, dashboards, repos, or tickets

These modes define how much source content the vault stores locally inside a note.

When adding new material, fold into an existing reference as a new H2 if it strengthens the same topic. Create a new reference only when it is a durable, reusable topic of its own.

## Core Contract

We need to include in CLAUDE.md, .meta/convensions, .meta/tags.md all info for managing the vault, and read those before doing work. Treat those as data. 

## Frontmatter

Frontmatter is canonical. Indexes, staleness, search, and graph behavior derive from frontmatter. Maintain `type`, `status`, `tags`, `sources`, and `related` (references to other documents) carefully. 

## Scripts

Use scripts for graph work

Do not hand edit derived indexes. Create python scripts for `.index/by-tag` note collection, backlinks, tag-rewrites, skill symlinks, and add them to vault skills. For body/frontmatter changes, write and prefer helpers like vault-set-body, vault-set-tags, vault-add-source, vault-rebuild-index and vault-rebuild-backlinks. 

## New Content

I want a /vault-enrich skill, that takes a domain, and seeks to EXPAND it, dreaming up new characters, locations, lore. Everything must be cleared by the user, make it an active conversation with them to create new content with their guidance.



