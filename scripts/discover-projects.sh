#!/usr/bin/env bash
# discover-projects.sh — Scan for projects and seed registry.md
# Run: bash ~/cacti/scripts/discover-projects.sh
#
# Scans common project root directories for subdirectories that look like
# projects (have a CLAUDE.md or are git repos) and appends them to registry.md.
#
# PERSONALIZE: Update SCAN_DIRS below to match where you keep your projects.

set -euo pipefail

CACTI_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$CACTI_ROOT/knowledge/registry.md"

# Directories to scan — update these to match your project layout
SCAN_DIRS=(
  "$HOME/projects"
  "$HOME/work"
  "$HOME/code"
  "$HOME/freelance"
)

echo "Scanning for projects..."
echo ""

found=0

for scan_dir in "${SCAN_DIRS[@]}"; do
  [ -d "$scan_dir" ] || continue

  for dir in "$scan_dir"/*/; do
    [ -d "$dir" ] || continue
    dirname=$(basename "$dir")

    # Skip common non-project directories
    case "$dirname" in
      .*|node_modules|venv|__pycache__|_temp|archive) continue ;;
    esac

    # Only include directories that look like projects
    if [ -f "$dir/CLAUDE.md" ] || [ -d "$dir/.git" ]; then
      has_claude="No"
      has_handover="No"
      [ -f "$dir/CLAUDE.md" ] && has_claude="Yes"
      [ -f "$dir/HANDOVER.md" ] && has_handover="Yes"

      echo "Found: $dirname ($dir)"
      echo "  CLAUDE.md: $has_claude | HANDOVER.md: $has_handover"
      found=$((found + 1))
    fi
  done
done

echo ""
echo "Found $found projects."
echo ""
echo "To register these in your registry, add them to knowledge/registry.md"
echo "or ask Claude: 'Add [project-name] at [path] to my registry'"
