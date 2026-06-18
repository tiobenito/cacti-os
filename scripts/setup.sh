#!/usr/bin/env bash
# Cacti OS — one-time setup
# Run after cloning: bash scripts/setup.sh

set -euo pipefail

echo "Setting up Cacti OS..."
echo ""

# 1. Verify Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "ERROR: Claude Code not found."
    echo "Install it at: https://claude.ai/code"
    echo ""
    echo "Then re-run: bash scripts/setup.sh"
    exit 1
fi

echo "Claude Code: found"

# 2. Create the memory directory (auto-memory system)
MEMORY_DIR="$HOME/.claude-personal/projects/$(pwd | tr '/' '-')/memory"
mkdir -p "$MEMORY_DIR"
echo "Memory directory: $MEMORY_DIR"

# 3. Install git hooks (for activity tracking)
if [ -f "scripts/install-git-hooks.sh" ]; then
    bash scripts/install-git-hooks.sh
fi

# 4. Create empty log file if it doesn't exist
mkdir -p logs
touch logs/activity.jsonl

echo ""
echo "Setup complete."
echo ""
echo "Start Claude Code from this directory and run /onboarding:"
echo ""
echo "  cd $(pwd)"
echo "  claude"
echo "  > /onboarding"
echo ""
echo "The onboarding interview takes about 10 minutes."
echo "Afterwards, your system is live."
