# claude-dotfiles

Personal Claude Code configuration: slash commands and skills.

## What's included

### Commands (`commands/`)

| Command | Description |
|---|---|
| `/discuss` | Discussion mode — no code edits, just talk |
| `/sync-upstream` | Sync local main with upstream, push to origin |

### Skills (`skills/`)

| Skill | Description |
|---|---|
| `benchmark` | Run vLLM serving benchmarks with PR-ready output |
| `bibtex-collector` | Collect BibTeX from Google Scholar via Chrome |
| `fast-mlx` | Optimize MLX code for performance and memory |
| `writing-style` | Technical writing style guide for editing prose |

## Setup

```bash
git clone <this-repo> ~/workspace/claude-dotfiles
cd ~/workspace/claude-dotfiles
chmod +x install.sh
./install.sh
```

This symlinks `commands/` and `skills/` into `~/.claude/`. Edits in either location are reflected immediately.

## Adding new commands or skills

- **Command**: Add a `.md` file to `commands/`. It becomes a `/command-name` slash command.
- **Skill**: Add a directory to `skills/` with a `SKILL.md` file. See [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for the skill format.
