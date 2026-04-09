#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

mkdir -p "$CLAUDE_DIR"

# Symlink commands and skills directories
for dir in commands skills; do
    if [ -e "$CLAUDE_DIR/$dir" ] && [ ! -L "$CLAUDE_DIR/$dir" ]; then
        echo "Backing up existing $CLAUDE_DIR/$dir to $CLAUDE_DIR/${dir}.bak"
        mv "$CLAUDE_DIR/$dir" "$CLAUDE_DIR/${dir}.bak"
    fi
    ln -sfn "$REPO_DIR/$dir" "$CLAUDE_DIR/$dir"
    echo "Linked $dir -> $CLAUDE_DIR/$dir"
done

echo ""
echo "Done. Your commands and skills are now symlinked from this repo."
