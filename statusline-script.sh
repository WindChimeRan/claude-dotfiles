#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Extract data using jq
model_name=$(echo "$input" | jq -r '.model.display_name')
current_dir=$(echo "$input" | jq -r '.workspace.current_dir')

# Get current time
current_time=$(date +%H:%M:%S)

# Format directory (show full path and replace home with ~)
formatted_dir=$(echo "$current_dir" | sed "s|^$HOME|~|")

# Get git branch (suppress error output if not in git repo)
git_branch=""
if git -C "$current_dir" rev-parse --git-dir >/dev/null 2>&1; then
    git_branch=$(git -C "$current_dir" branch --show-current 2>/dev/null)
    if [ -n "$git_branch" ]; then
        git_branch=$(printf " \033[93m(%s)\033[0m" "$git_branch")
    fi
fi

# Output with colors: time, directory, git branch, model
printf "\033[90m%s\033[0m \033[1;32m➜\033[0m \033[36m%s\033[0m%s \033[90m[%s]\033[0m" "$current_time" "$formatted_dir" "$git_branch" "$model_name"