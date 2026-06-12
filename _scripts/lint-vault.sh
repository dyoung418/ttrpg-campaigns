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
#   HAS_CREATED    1 if frontmatter has a "created:" key, else 0
#   TAGS_FORM       "array" | "inline" | "string" | "none"
#   OUTBOUND_LINKS  count of [[wikilinks]] in the body
#   OUTBOUND_EMBEDS count of ![[embeds]] in the body

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

# Emit header so consumers can parse defensively.
printf "PATH\tFOLDER\tHAS_FM\tHAS_TYPE\tHAS_CAMPAIGN\tHAS_CREATED\tTAGS_FORM\tOUTBOUND_LINKS\tOUTBOUND_EMBEDS\n"

find "$SCOPE" -name "*.md" -type f \
  -not -path "*/_templates/*" \
  -not -path "*/.obsidian/*" \
  -not -path "*/.claude/*" \
  -not -path "*/_sources/*" \
  -not -path "*/_assets/*" \
  -not -path "*/_scripts/*" \
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
      tags_form="none"

      first_line=$(head -n 1 "$f" 2>/dev/null || echo "")
      if [ "$first_line" = "---" ]; then
        has_fm=1
        # Extract just the frontmatter block.
        fm=$(awk 'NR==1 && /^---$/ {in_fm=1; next} in_fm && /^---$/ {exit} in_fm {print}' "$f")

        echo "$fm" | grep -q "^type:" && has_type=1
        echo "$fm" | grep -q "^campaign:" && has_campaign=1
        echo "$fm" | grep -q "^created:" && has_created=1

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

      printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
        "$f" "$folder" "$has_fm" "$has_type" "$has_campaign" "$has_created" "$tags_form" "$links" "$embeds"
    done
