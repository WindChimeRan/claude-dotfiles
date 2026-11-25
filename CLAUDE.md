# Global agent instructions

Applies to every project. Repo-level AGENTS.md or CLAUDE.md files add to this and win on conflict. This file is `~/.claude/CLAUDE.md`; `~/.codex/AGENTS.md` is a symlink to it. When I change a fact recorded here, update this file.

## Writing

For PR descriptions, reviews, issues and reports:

- Open with the goal and the decision, then the first-principles reason, then only the evidence that carries the argument, then trade-offs.
- Leave out process history (failed or repeated runs), anything CI checks (test counts, lint), per-run tables, and command or raw-data dumps.
- State each result plainly ("this PR is N% faster than main") and say whether it was measured and where. Don't hedge it or follow it with a sentence that takes it back.
- Where something wasn't measured, give the first-principles expectation and call it a prediction.
- Use plain words. Spell out each reason in short, concrete steps instead of jargon.
- Show changes as Before/After bullets. Avoid the "X is Y, not Z" construction.
- Keep each PR to one claim a reviewer must verify. Propose only the first step of a larger plan.
- Keep benchmark protocol and change history out of user docs.

## Reasoning

- Answer design and performance questions from first principles before proposing experiments: what the code does, a simple hardware model, and numbers already published. Then name the smallest measurement still missing. Don't re-offer an experiment I passed over.
- Before judging a direction or an abstraction, fetch all the context. For a vllm-metal PR that changes an abstraction, check upstream vLLM's design and, where relevant, vllm-omni's, including their issues and PRs. Add sglang and sglang-omni when needed.
- Apple GPUs: M1 to M4 differ mainly in core count; M5 adds NAX.
- Prefer a principled rule to an ad-hoc exception such as a device, SKU or shape gate.

## Git and GitHub

- I work from more than one Mac, each with its own agent sessions: a Mac Studio (M5 Max with a 40-core GPU and 128 GB), an M2 Max laptop (30-core GPU, 64 GB) and an M1 Pro laptop (14-core GPU, 32 GB). Before editing a PR description, fetch the current body. Before pushing, fetch the branch and compare. Never push over a remote head that moved without asking. Fold another machine's results into the existing tables rather than a separate section.
- When I say "supersede", we write the replacement PR ourselves instead of asking the author for changes.
- No AI co-author trailers or "Generated with" footers. If a managed setting requires a commit trailer, don't commit: stage the change, write the message to a file and give me the one-line `git commit -F <file>`.

## This Mac (Mac Studio, M5 Max, 128 GB)

- This is an M5, so NAX is available here and not on the M1/M2 laptops.
- Hugging Face: the cache is `HF_HUB_CACHE=/Volumes/bunch/ckpt/huggingface/hub`, exported in `~/.zshenv`. It is on an 8-bay NAS reached over a direct 10 GbE link and mounted over SMB at `/Volumes/bunch`. It is meant for e2e model testing, so on a cache miss, download the checkpoint there without asking. If `/Volumes/bunch` is not mounted, stop and tell me instead of downloading to the internal disk. If the sandbox blocks or stalls the download, run it outside the sandbox.
