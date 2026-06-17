---
name: memstat-bench
description: Capture a per-second memory timeline (wired / used / active / pressure) during a vllm-metal benchmark and plot it. Supports single-run and two-run side-by-side comparison. Use when the user needs to see how a serving run behaves in Metal-wired memory over time — not just the aggregate latency/throughput numbers. Typical triggers include memory-regression debugging, OOM investigation, branch comparison with a memory focus, fraction-budget tuning, and visual evidence for PR descriptions.
user_invocable: true
---

# vLLM-Metal Benchmark + Memory Timeline Monitor

## Overview

This skill wraps a `vllm serve` run with `metalstat run --capture` so you can see how Metal-wired memory and system memory pressure behave *during* the benchmark — not just the aggregate latency/throughput numbers the plain `benchmark` skill reports. The output is a PNG with either a 2-panel single-run layout or a 4-panel side-by-side comparison.

`metalstat run` handles the sampler lifecycle, server-log capture, and exit-code propagation in one invocation; the skill just drives the workflow and feeds the resulting JSONL to the plotter.

## Capabilities (not use cases)

The skill provides these primitives. Any problem that needs one or more of them is a candidate for this skill, regardless of the branch or PR context.

- **Wired-memory timeline**: 1 Hz samples of `mem_wired_gb`, the best single proxy for MLX-managed Metal memory on Apple Silicon. Shows growth patterns, plateaus, reclaim drops.
- **Pressure-zone tracking**: 1 Hz samples of `mem_pressure_pct`, bucketed into green (0–33) / yellow (33–66) / red (66–100). Tells you whether a run is about to trigger OS reclamation.
- **Used / active overlay**: captures total system memory and active-page counts alongside wired, so you can tell whether growth is coming from Metal or from other parts of the process.
- **Side-by-side shape comparison**: two runs (branches, configs, models, fractions — anything) plotted on shared axes so *shape* differences become visually obvious, not just peak deltas.

## When to use this vs. the plain `benchmark` skill

- Use **`benchmark`** when the user only wants throughput / TPOT / TTFT numbers and a bar-chart comparison. No memory monitoring.
- Use **`memstat-bench`** (this skill) when the user needs *shape over time*, not aggregate numbers — any time the question is "what is memory doing *during* the run?" rather than "how fast was the run?".

Both skills run the same `vllm bench serve` workload; this skill adds the metalstat wrapper around the server and the timeline plot on top.

## Prerequisites

- `metalstat >= 0.1.6` on `PATH`. Verify with `metalstat --version`.
- `sonnet.txt` at repo root (download from `https://raw.githubusercontent.com/vllm-project/vllm/main/benchmarks/sonnet.txt` if missing).
- `matplotlib` in the vllm-metal venv. `pip install matplotlib` if missing.
- Apple Silicon Mac (M-series), otherwise `metalstat` doesn't have anything meaningful to report.

## Files in this skill

Inside `$SKILL_DIR` (the directory containing this SKILL.md):

- **`plot_timeline.py`** — parses one or two JSONL logs and produces a PNG. CLI: `python plot_timeline.py --out FILE.png --title TITLE --pair "A=A.jsonl" [--pair "B=B.jsonl"]`. One pair → 2-panel single-run layout. Two pairs → 4-panel comparison layout.

Sampling and server-log capture are handled by `metalstat run --capture`; no wrapper script lives in this skill.

## Standard configuration

Unless the user overrides, use the same config as the sibling `benchmark` skill so results are comparable:

```
Model:            Qwen/Qwen3-0.6B
Max model len:    2048
Dataset:          sonnet
Input len:        1024
Output len:       128
Num prompts:      100
Request rate:     10
Max concurrency:  32
Memory fraction:  0.3
```

### Wrapped server command

```bash
source .venv-vllm-metal/bin/activate
PYTHONPATH=. \
VLLM_METAL_USE_PAGED_ATTENTION=1 \
VLLM_METAL_MEMORY_FRACTION=0.3 \
metalstat run -o /tmp/run_<label> -i 1 --capture -- \
  vllm serve Qwen/Qwen3-0.6B \
    --max-model-len 2048 \
    --host 127.0.0.1 \
    --port 8000
```

`metalstat run` writes three files under the `-o` prefix:
- `/tmp/run_<label>.meta.json` — hostname, chip, total memory (captured before the server starts)
- `/tmp/run_<label>.jsonl` — per-second samples with flat schema (`mem_wired_gb`, `mem_used_gb`, `mem_active_gb`, `mem_pressure_pct`, plus CPU / GPU / power fields)
- `/tmp/run_<label>.log` — vllm server stdout+stderr (merged); replaces the old manual `> /tmp/server_<label>.log` redirect

### Client command

```bash
vllm bench serve \
  --backend vllm \
  --base-url http://127.0.0.1:8000 \
  --model Qwen/Qwen3-0.6B \
  --endpoint /v1/completions \
  --dataset-name sonnet \
  --dataset-path sonnet.txt \
  --sonnet-input-len 1024 \
  --sonnet-output-len 128 \
  --num-prompts 100 \
  --request-rate 10 \
  --max-concurrency 32
```

## Workflow

### Step 1: Ask the user

Before running, confirm:
1. **What to compare**: one run or two? For two runs, what's varying — branches, fractions, models, env flags, something else? The skill is agnostic; it just needs two sets of (label, config) pairs.
2. **Labels**: short identifiers used for file names and plot legends. Pick something descriptive for the axis of variation (e.g., `main` vs `feature-branch`, or `fraction_0.3` vs `fraction_0.6`, or `qwen3-0.6b` vs `qwen3-4b`).
3. **Any config overrides**: different model, prompt count, concurrency, fraction, etc. Default to the sibling `benchmark` skill config unless told otherwise.

### Step 2: Preflight

Run these checks in parallel:
- `metalstat --version` — confirm >= 0.1.6; bail with an install/upgrade hint if missing or older.
- `ls sonnet.txt` — download if missing.
- `pgrep -fl "metalstat run"` — if a stale wrapper is running from a previous session, kill it first (`pkill -INT -f "metalstat run"`).
- `pgrep -fl "vllm serve"` — if a bare server leaked somehow (user killed the wrapper uncleanly), kill it too.
- `git branch --show-current` — note the starting branch so you can restore it at the end.

### Step 3: Per-run capture loop

For **each** run in the comparison, do this sequence. Runs must be sequential — the machine can only host one server at a time.

1. `git checkout <branch>` (if switching branches)
2. `rm -f ~/.cache/vllm-metal/_paged_ops*` — clean the cached native extension
3. **Start the wrapped server** (`run_in_background: true`). `metalstat run` starts sampling immediately, writes its meta file, and spawns vllm serve with SIGINT/SIGTERM/SIGHUP forwarding wired up:
   ```bash
   source .venv-vllm-metal/bin/activate && \
     PYTHONPATH=. VLLM_METAL_USE_PAGED_ATTENTION=1 VLLM_METAL_MEMORY_FRACTION=<fraction> \
     metalstat run -o /tmp/run_<label> -i 1 --capture -- \
       vllm serve Qwen/Qwen3-0.6B --max-model-len 2048 \
         --host 127.0.0.1 --port 8000
   ```
4. **Poll for health** with a curl loop:
   ```bash
   for i in $(seq 1 90); do
     curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health 2>&1 | grep -q "200" && \
       echo "READY after ${i}s" && break
     sleep 1
   done
   ```
   Grep `/tmp/run_<label>.log` for the `Paged attention memory breakdown` line and the `init engine` timing — useful to note the KV budget, num_blocks, and any reported overhead for your report.
5. **Run the benchmark** (foreground, `tee` to log file):
   ```bash
   vllm bench serve \
     --backend vllm --base-url http://127.0.0.1:8000 \
     --model Qwen/Qwen3-0.6B --endpoint /v1/completions \
     --dataset-name sonnet --dataset-path sonnet.txt \
     --sonnet-input-len 1024 --sonnet-output-len 128 \
     --num-prompts 100 --request-rate 10 --max-concurrency 32 \
     2>&1 | tee /tmp/bench_<label>.log
   ```
6. **Stop the wrapped server**. One SIGINT to `metalstat run` forwards to vllm serve, waits for it to exit, flushes the JSONL, and closes the log file:
   ```bash
   pkill -INT -f "metalstat run"
   ```
7. **Confirm sample count**: `wc -l /tmp/run_<label>.jsonl` — expect roughly 160–200 lines for a 100-prompt run (server boot ~10s + bench ~200s + teardown, at 1 Hz).

### Step 4: Generate the plot

For a **comparison** (two runs):

```bash
source .venv-vllm-metal/bin/activate && \
python $SKILL_DIR/plot_timeline.py \
  --out /tmp/memory_timeline_compare.png \
  --title "vllm-metal · <label_a> vs <label_b> · <axis-of-variation>" \
  --pair "<label_a>=/tmp/run_<label_a>.jsonl" \
  --pair "<label_b>=/tmp/run_<label_b>.jsonl"
```

The plotter prints a per-run summary (wired min/max/delta, used min/max/delta, pressure min/max) and saves a 4-panel PNG:

1. **Top-left**: run A timeline (`mem_wired_gb` solid, `mem_used_gb` dashed)
2. **Top-right**: run B timeline (shared y-axis)
3. **Bottom-left**: wired overlay — the headline. Directly compares the *shape* of memory growth between the two runs.
4. **Bottom-right**: memory pressure (%) overlay with green / yellow / red bands (0-33, 33-66, 66-100).

For a **single run**:

```bash
python $SKILL_DIR/plot_timeline.py \
  --out /tmp/memory_timeline.png \
  --title "vllm-metal · <label>" \
  --pair "<label>=/tmp/run_<label>.jsonl"
```

The plotter falls back to a 2-panel layout (memory timeline + pressure timeline).

### Step 5: Report to the user

Produce a report section with the shape summary and the plot path:

```markdown
## Memory timeline

| Metric | <label_a> | <label_b> | Δ |
|---|---:|---:|---:|
| **wired peak** | A | B | ΔGB |
| wired delta during bench | +A GB | +B GB | — |
| used peak | A | B | ΔGB |
| **pressure peak** | A% (zone) | B% (zone) | Δpts |
| Output tok/s | A | B | +Δ% |
| Mean TPOT (ms) | A | B | −Δ% |

Headline plot: /tmp/memory_timeline_compare.png
```

When describing the wired-memory behavior, prefer *shape* language (monotonic climb, bounded oscillation, staircase, plateau, sawtooth drop) over numeric deltas alone. The shape is what makes the comparison visually convincing; the deltas are supporting evidence.

### Step 6: Cleanup

- `pkill -INT -f "metalstat run"` — in case a wrapper leaked from a failed run
- `pgrep -fl "vllm serve"` — if anything lingers after killing the wrapper, clean it up with `pkill -f "vllm serve"`
- `git checkout <original_branch>` — restore the starting branch state

## Gotchas

These are skill-level facts that apply to any invocation. Keep them all in mind.

1. **`gpu_mem_allocated_gb` in metalstat is often 0.** metalstat tracks Metal memory via an API that doesn't always see MLX allocations. Use `mem_wired_gb` as the primary MLX memory indicator — it captures Metal-wired pages including model weights, KV cache, and the MLX buffer-cache free-list.
2. **`vllm_rss` (python process RSS) will not reflect MLX GPU memory.** MLX memory lives in wired pages, not the Python heap. `ps`-style monitoring is blind to it. Don't use process RSS as your memory signal.
3. **Exit code 130 (or 143) on the backgrounded `metalstat run` task is expected.** When you SIGINT the wrapper, it forwards the signal to vllm serve, which exits with a signal-derived code; `metalstat run` propagates that. The task reports a non-zero exit — that's cleanup, not a failure to flag to the user.
4. **Always `git checkout` back to the starting branch** after a comparison that switched branches — the user expects their working state restored.
5. **Don't run the bench client through `metalstat run`** — the server is the long-lived process whose memory we want to track, and wrapping the client would start a second sampler on the same machine. Wrap the server; run the client as a plain foreground command.

## Example use case: validating a memory cap (issue #234, PR #247 / memory_cap_v2)

This is the worked example the skill was originally built for. A successor PR wants to cap MLX's userspace buffer cache via `mx.set_cache_limit` to bound the 40→62 GB sawtooth observed in sustained serving. The skill's job is to produce visual evidence that the cap works.

**What to compare**: `main` vs the memory-cap branch, both running the standard benchmark.

**Labels**: `main` and `memory_cap_v2` (or whatever the branch is named).

**Fraction tip**: at `VLLM_METAL_MEMORY_FRACTION=0.3` (the sibling `benchmark` default), the difference is visible but both runs may end up in the yellow/red pressure zone and visually overlap. Lowering the fraction to `0.25` or similar gives each run more baseline headroom, which makes an unbounded-free-list run's pressure cross from yellow into red while a capped run stays in yellow. The qualitative "across a threshold" shape is the strongest visual evidence — recommend the lower fraction to the user when the goal is cap validation specifically.

**What the plot should show**:

- **main**: `mem_wired_gb` climbs monotonically during the benchmark (a staircase), then drops sharply when the bench ends and the OS reclaimer kicks in — one sawtooth tooth.
- **memcap branch**: `mem_wired_gb` oscillates in a narrow band with no upward trend — the cap is actively trimming the free-list to its configured ceiling.
- **Pressure**: main crosses into red, memcap stays yellow.

**Notable gotcha specific to this case**: if the branch uses a `profile_run()` method to measure the cap value dynamically, two consecutive runs of the same branch can report different measured overhead values (e.g. 0.75 GB vs 1.42 GB) depending on the allocator state when the profile runs. This is expected variance, not a regression — the cap is a relative measurement, not an absolute invariant.

## Other scenarios this skill is suitable for

These aren't worked examples — just reminders that the skill's primitives apply beyond the memory-cap case. If any of them match what the user is asking for, adapt Steps 1-5 to the relevant axis of variation.

- **Peak-memory comparison of two attention kernels.** Swap in different branches and label them by kernel. The wired overlay shows which kernel has a higher steady-state wired footprint.
- **OOM / memory-pressure regression debug.** Single-run mode. Identify where in the timeline pressure crosses into red, correlate with server log lines from the same timestamp in `/tmp/run_<label>.log`.
- **`VLLM_METAL_MEMORY_FRACTION` tuning.** Run the same branch at two fractions, compare headroom vs. KV budget. Useful for picking the largest fraction that stays in yellow.
- **Paged vs. legacy MLX path.** Run with `VLLM_METAL_USE_PAGED_ATTENTION=1` vs `=0`, label accordingly. Shows how wired memory usage differs between the two cache strategies.
- **Larger-vs-smaller model peak footprint.** Run different models through the same workload, label by model name. Useful for capacity planning.

In each case: the helper script is the same, only the labels, fraction, and (optionally) model change. Do not hardcode case-specific assumptions into the workflow.
