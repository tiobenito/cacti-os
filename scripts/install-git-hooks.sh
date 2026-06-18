#!/usr/bin/env bash
# install-git-hooks.sh — Install post-commit hooks for activity tracking
# Run: bash ~/cacti/scripts/install-git-hooks.sh
# Safe to re-run — skips repos already hooked.
#
# After installation, every git commit in your project directories will
# append a JSON line to ~/cacti/logs/activity.jsonl.
# This powers the git activity summary in /weekly-review.
#
# PERSONALIZE: Update SCAN_DIRS below to match where you keep your projects.

set -euo pipefail

CACTI_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ACTIVITY_LOG="$CACTI_ROOT/logs/activity.jsonl"
HOOK_MARKER="# cacti-activity-tracker"

# Directories to scan for git repos — update to match your project layout
SCAN_DIRS=(
  "$HOME/projects"
  "$HOME/work"
  "$HOME/code"
  "$HOME/freelance"
  "$CACTI_ROOT"
)

installed=0
skipped=0

for scan_dir in "${SCAN_DIRS[@]}"; do
  [ -d "$scan_dir" ] || continue

  while IFS= read -r gitdir; do
    repo_dir=$(dirname "$gitdir")
    hooks_dir="$repo_dir/.git/hooks"
    hook_file="$hooks_dir/post-commit"

    # Skip if already installed
    if [ -f "$hook_file" ] && grep -q "$HOOK_MARKER" "$hook_file" 2>/dev/null; then
      skipped=$((skipped + 1))
      continue
    fi

    mkdir -p "$hooks_dir"

    HOOK_CONTENT=$(cat << HOOK

$HOOK_MARKER
_cacti_log_commit() {
  local repo_name=\$(basename "\$(git rev-parse --show-toplevel)")
  local repo_path="\$(git rev-parse --show-toplevel)"
  local branch=\$(git rev-parse --abbrev-ref HEAD)
  local msg=\$(git log -1 --pretty=%s)
  local files=\$(git diff-tree --no-commit-id --name-only -r HEAD | wc -l | tr -d ' ')
  local ts=\$(date -u +"%Y-%m-%dT%H:%M:%S")
  echo "{\\"ts\\":\\"\$ts\\",\\"repo\\":\\"\$repo_name\\",\\"path\\":\\"\$repo_path\\",\\"branch\\":\\"\$branch\\",\\"msg\\":\\"\$msg\\",\\"files\\":\$files}" >> "$ACTIVITY_LOG"
}
_cacti_log_commit
HOOK
)

    if [ -f "$hook_file" ]; then
      echo "$HOOK_CONTENT" >> "$hook_file"
    else
      printf '#!/usr/bin/env bash\n%s\n' "$HOOK_CONTENT" > "$hook_file"
    fi

    chmod +x "$hook_file"
    installed=$((installed + 1))
    echo "Installed hook: $(basename "$repo_dir")"

  done < <(find "$scan_dir" -maxdepth 3 -name ".git" -type d 2>/dev/null)
done

echo ""
echo "Done. Installed: $installed | Already hooked: $skipped"
echo "Activity log: $ACTIVITY_LOG"
