#!/usr/bin/env bash
# Usage: ./list-campaign.sh <campaign-name>
# Prints all entity names grouped by type for a campaign.
# Called by Claude during /session to get a quick manifest before reading files.

VAULT="/home/danny/ttrpg_campaigns"
CAMPAIGN="${1:-}"

if [ -z "$CAMPAIGN" ]; then
  echo "Usage: $0 <campaign-name>"
  echo ""
  echo "Available campaigns:"
  # ideas bank (campaigns/ideas) is not a campaign; skip dot-dirs like .obsidian
  find "$VAULT/campaigns" -maxdepth 1 -mindepth 1 -type d ! -name ideas ! -name ".*" -exec basename {} \; | sort
  exit 1
fi

DIR="$VAULT/campaigns/$CAMPAIGN"

if [ ! -d "$DIR" ]; then
  echo "Campaign not found: $CAMPAIGN"
  echo ""
  echo "Available campaigns:"
  # ideas bank (campaigns/ideas) is not a campaign; skip dot-dirs like .obsidian
  find "$VAULT/campaigns" -maxdepth 1 -mindepth 1 -type d ! -name ideas ! -name ".*" -exec basename {} \; | sort
  exit 1
fi

echo "=== CAMPAIGN: $CAMPAIGN ==="
echo ""

for TYPE in characters npcs locations plot-hooks factions items lore sessions; do
  COUNT=$(find "$DIR/$TYPE" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    LABEL=$(echo "$TYPE" | tr '[:lower:]' '[:upper:]')
    echo "--- $LABEL ($COUNT) ---"
    find "$DIR/$TYPE" -name "*.md" | sort | while read -r f; do basename "$f" .md; done
    echo ""
  fi
done
