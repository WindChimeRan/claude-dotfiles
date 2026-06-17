#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

mkdir -p "$CLAUDE_DIR"

# The ako4all skill is a git submodule. Warn if it wasn't checked out
# (i.e. the repo was cloned without --recurse-submodules).
if [ -d "$REPO_DIR/skills/ako4all" ] && [ -z "$(ls -A "$REPO_DIR/skills/ako4all" 2>/dev/null)" ]; then
    echo "WARNING: skills/ako4all is empty (submodule not initialized)."
    echo "         Run: git -C \"$REPO_DIR\" submodule update --init --recursive"
    echo ""
fi

# Helper: back up an existing real (non-symlink) target, then symlink from the repo.
link() {
    local name="$1"
    local src="$REPO_DIR/$name"
    local dst="$CLAUDE_DIR/$name"
    if [ -e "$dst" ] && [ ! -L "$dst" ]; then
        echo "Backing up existing $dst to ${dst}.bak"
        mv "$dst" "${dst}.bak"
    fi
    ln -sfn "$src" "$dst"
    echo "Linked $name -> $dst"
}

# Directories
for dir in commands skills; do
    link "$dir"
done

# Individual config files
for file in CLAUDE.md statusline-script.sh; do
    link "$file"
done

echo ""
echo "Done. Your commands, skills, CLAUDE.md and statusline-script.sh are now symlinked from this repo."
echo "Edits in either location are reflected immediately; commit & push from $REPO_DIR to sync."
