# claude-dotfiles

Personal Claude Code configuration: slash commands, skills, and global config, symlinked into `~/.claude/`.

## What's included

### Commands (`commands/`)

| Command | Description |
|---|---|
| `/discuss` | Discussion mode — no code edits, just talk |
| `/pr-artifact-explain` | Explain a PR from scratch for a newcomer, published as an Artifact (read-only) |
| `/pr-rebuttal` | Investigate PR review comments, give a structured verdict per point (no edits/posting) |
| `/sync-upstream` | Sync local main with upstream main, then push to origin |

### Skills (`skills/`)

| Skill | Description |
|---|---|
| `ako4all` | Agentic loop to iteratively optimize/benchmark a GPU kernel for max speedup *(git submodule → [TongmingLAIC/AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL))* |
| `benchmark` | Run vLLM serving benchmarks with PR-ready output |
| `bibtex-collector` | Collect BibTeX from Google Scholar via Chrome |
| `fast-mlx` | Optimize MLX code for performance and memory |
| `html-metal-explainer` | Generate educational HTML explainers for Metal GPU kernels (vllm-metal) |
| `jekyll-post-preview` | Build & screenshot a Jekyll/al-folio post (light + dark) to verify rendering |
| `memstat-bench` | Plot a per-second memory timeline during a vllm-metal benchmark |
| `no-ai-slop` | Edit drafts sharper while keeping the writer's voice, or detect AI-slop without rewriting *(vendored from [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop), MIT)* |
| `paper_rebuttal` | Strategic patterns for writing strong academic peer-review rebuttals |
| `refactor-pr-check` | Checklist for preparing or reviewing a refactor PR — faithful, minimal, reviewable, verified |
| `writing-style` | Technical writing style guide for editing prose |

### Global config (repo root)

| File | Linked to | Description |
|---|---|---|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Global working principles (source-truth / honest provenance) |
| `statusline-script.sh` | `~/.claude/statusline-script.sh` | Status line script (time · dir · git branch · model) |
| `settings.json` | `~/.claude/settings.json` | Global settings — model, effort level, theme, status line, attribution |

`~/.claude/settings.local.json` is deliberately **not** tracked: it holds per-machine
permission grants (this host allows `nvidia-smi`, `systemctl status`, …), which do not
transfer to another machine. Keep host-specific settings there.

## Setup

```bash
# --recurse-submodules pulls in the ako4all skill
git clone --recurse-submodules git@github.com:WindChimeRan/claude-dotfiles.git ~/workspace/claude-dotfiles
cd ~/workspace/claude-dotfiles
chmod +x install.sh
./install.sh
```

`install.sh` symlinks `commands/`, `skills/`, `CLAUDE.md`, `statusline-script.sh`, and `settings.json` into `~/.claude/`. Any pre-existing real file/dir is moved aside to `*.bak` first — so on a machine that already has a `settings.json`, check `settings.json.bak` for anything worth merging back. Edits in either location are then reflected immediately.

If you cloned without `--recurse-submodules`, initialize the `ako4all` submodule afterward:

```bash
git submodule update --init --recursive
```

## Adding new commands or skills

- **Command**: Add a `.md` file to `commands/`. It becomes a `/command-name` slash command.
- **Skill**: Add a directory to `skills/` with a `SKILL.md` file. See [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for the skill format.

Because everything is symlinked, new files land in the repo automatically — just `git add`, commit, and push.
