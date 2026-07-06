#!/usr/bin/env bash
# Usage: ./lint-vault.sh [scope-dir]
# Emits a TSV manifest of every vault .md file in scope. Used by /lint.
#
# Columns (tab-separated):
#   PATH            absolute path to the .md file
#   FOLDER          immediate parent folder name (e.g. npcs, locations)
#   HAS_FM          1 if file opens with "---" frontmatter, else 0
#   HAS_TYPE        1 if frontmatter has a "type:" key, else 0
#   HAS_CAMPAIGN    1 if frontmatter has a "campaign:" key, else 0
#   HAS_CREATED     1 if frontmatter has a "created:" key, else 0
#   TAGS_FORM       "array" | "inline" | "string" | "none"
#   OUTBOUND_LINKS  count of [[wikilinks]] in the body
#   OUTBOUND_EMBEDS count of ![[embeds]] in the body
#   TYPE            frontmatter "type:" value, or "-"
#   STATUS          frontmatter "status:" value, or "-"
#   STATUS_OK       1 status valid for type | 0 off-vocab or missing-but-required
#                   | "-" type has no status vocabulary
#                   (vocabulary: _meta/conventions.md §2; lore may omit status)
#   HAS_SOURCES     1 if frontmatter has a "sources:" key, else 0
#   HAS_RELATED     1 if frontmatter has a "related:" key, else 0
#   TYPE_TAG        1 if any tag is a deprecated type-name tag (npc, location,
#                   ...), else 0 — type lives in type:, never tags (§3)

set -u

# Auto-detect the vault root from this script's location, falling back
# to the legacy hardcoded POSIX path. Working on either Linux/WSL or Git
# Bash on Windows.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ ! -d "$VAULT/campaigns" ] && [ -d "/home/danny/ttrpg_campaigns/campaigns" ]; then
  VAULT="/home/danny/ttrpg_campaigns"
fi

SCOPE="${1:-$VAULT}"

if [ ! -d "$SCOPE" ]; then
  echo "Scope not found: $SCOPE" >&2
  exit 1
fi

# Per-type status vocabulary (_meta/conventions.md §2). Echoes the allowed
# values, or "" when the type has no vocabulary (status unchecked).
status_vocab() {
  case "$1" in
    npc)        echo "alive deceased missing captive unknown" ;;
    character)  echo "active retired deceased" ;;
    location)   echo "accessible hostile contested cleared ruined" ;;
    plot-hook)  echo "open active resolved abandoned" ;;
    faction)    echo "active defeated destroyed unknown" ;;
    item)       echo "unacquired held lost destroyed" ;;
    lore)       echo "stub established" ;;
    session)    echo "planned complete" ;;
    *)          echo "" ;;
  esac
}

TYPE_NAMES="npc character location plot-hook faction item lore session encounter"

# Emit header so consumers can parse defensively.
printf "PATH\tFOLDER\tHAS_FM\tHAS_TYPE\tHAS_CAMPAIGN\tHAS_CREATED\tTAGS_FORM\tOUTBOUND_LINKS\tOUTBOUND_EMBEDS\tTYPE\tSTATUS\tSTATUS_OK\tHAS_SOURCES\tHAS_RELATED\tTYPE_TAG\n"

find "$SCOPE" -name "*.md" -type f \
  -not -path "*/_templates/*" \
  -not -path "*/.obsidian/*" \
  -not -path "*/.claude/*" \
  -not -path "*/_sources/*" \
  -not -path "*/_assets/*" \
  -not -path "*/_scripts/*" \
  -not -path "*/_index/*" \
  -not -path "*/_memory/*" \
  -not -path "*/_plans/*" \
  -not -path "*/_meta/*" \
  -not -path "*/node_modules/*" \
  -not -path "$VAULT/CLAUDE.md" \
  -not -path "$VAULT/README.md" \
  | sort | while read -r f; do
      folder=$(basename "$(dirname "$f")")

      # Frontmatter block: lines between the first and second "---" if present.
      # If the file does not start with "---", treat as no frontmatter.
      has_fm=0
      has_type=0
      has_campaign=0
      has_created=0
      has_sources=0
      has_related=0
      tags_form="none"
      ntype="-"
      status="-"
      status_ok="-"
      type_tag=0

      first_line=$(head -n 1 "$f" 2>/dev/null || echo "")
      if [ "$first_line" = "---" ]; then
        has_fm=1
        # Extract just the frontmatter block.
        fm=$(awk 'NR==1 && /^---$/ {in_fm=1; next} in_fm && /^---$/ {exit} in_fm {print}' "$f")

        echo "$fm" | grep -q "^type:" && has_type=1
        echo "$fm" | grep -q "^campaign:" && has_campaign=1
        echo "$fm" | grep -q "^created:" && has_created=1
        echo "$fm" | grep -q "^sources:" && has_sources=1
        echo "$fm" | grep -q "^related:" && has_related=1

        # type: and status: scalar values (quotes stripped).
        if [ "$has_type" = "1" ]; then
          ntype=$(echo "$fm" | sed -n 's/^type:[[:space:]]*//p' | head -n 1 | sed "s/^[\"']//; s/[\"']$//")
          [ -z "$ntype" ] && ntype="-"
        fi
        if echo "$fm" | grep -q "^status:"; then
          status=$(echo "$fm" | sed -n 's/^status:[[:space:]]*//p' | head -n 1 | sed "s/^[\"']//; s/[\"']$//")
          [ -z "$status" ] && status="-"
        fi

        # STATUS_OK: check against the per-type vocabulary.
        vocab=$(status_vocab "$ntype")
        if [ -n "$vocab" ]; then
          if [ "$status" = "-" ]; then
            # Only lore may omit status.
            if [ "$ntype" = "lore" ]; then status_ok=1; else status_ok=0; fi
          else
            status_ok=0
            for v in $vocab; do
              [ "$status" = "$v" ] && status_ok=1 && break
            done
          fi
        fi

        # Detect tags form. Three accepted shapes:
        #   tags: [a, b]                  -> inline
        #   tags:\n  - a\n  - b           -> array
        #   tags: a                       -> string
        if echo "$fm" | grep -qE "^tags:[[:space:]]*\["; then
          tags_form="inline"
        elif echo "$fm" | grep -qE "^tags:[[:space:]]*$"; then
          # Array form needs at least one "- " on the next non-blank line.
          if echo "$fm" | awk '/^tags:[[:space:]]*$/{found=1; next} found && /^[[:space:]]*-[[:space:]]+/{print; exit}' | grep -q .; then
            tags_form="array"
          else
            tags_form="none"
          fi
        elif echo "$fm" | grep -qE "^tags:[[:space:]]+[^[:space:]]"; then
          tags_form="string"
        fi

        # TYPE_TAG: flag any surviving deprecated type-name tag.
        tag_values=$(echo "$fm" | awk '
          /^tags:[[:space:]]*\[/ {
            line=$0; sub(/^tags:[[:space:]]*\[/,"",line); sub(/\].*$/,"",line)
            n=split(line,a,","); for(i=1;i<=n;i++){gsub(/^[[:space:]"'\''#]+|["'\''[:space:]]+$/,"",a[i]); if(a[i]!="")print a[i]}
            exit
          }
          /^tags:[[:space:]]*$/ {in_tags=1; next}
          in_tags && /^[[:space:]]+-[[:space:]]+/ {t=$0; sub(/^[[:space:]]+-[[:space:]]+/,"",t); gsub(/^["'\''#]+|["'\'']+$/,"",t); print t; next}
          in_tags && !/^[[:space:]]/ {exit}
        ')
        if [ -n "$tag_values" ]; then
          while IFS= read -r t; do
            for name in $TYPE_NAMES; do
              [ "$t" = "$name" ] && type_tag=1 && break
            done
            [ "$type_tag" = "1" ] && break
          done <<EOF
$tag_values
EOF
        fi
      fi

      # Body = everything after the closing frontmatter "---" (or the whole file if no fm).
      if [ "$has_fm" = "1" ]; then
        body=$(awk 'NR==1 && /^---$/ {in_fm=1; next} in_fm && /^---$/ {in_fm=0; next} !in_fm {print}' "$f")
      else
        body=$(cat "$f")
      fi

      # Count [[wikilinks]] (excluding embeds) and ![[embeds]].
      embeds=$(echo "$body" | grep -oE '!\[\[[^]]+\]\]' | wc -l | tr -d ' ')
      all_links=$(echo "$body" | grep -oE '\[\[[^]]+\]\]' | wc -l | tr -d ' ')
      links=$(( all_links - embeds ))
      [ "$links" -lt 0 ] && links=0

      printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
        "$f" "$folder" "$has_fm" "$has_type" "$has_campaign" "$has_created" "$tags_form" "$links" "$embeds" \
        "$ntype" "$status" "$status_ok" "$has_sources" "$has_related" "$type_tag"
    done
