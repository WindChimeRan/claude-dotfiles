---
name: memstat-bench
description: Capture a per-second memory timeline (wired / used / active / pressure) during a vllm-metal benchmark and plot it. Supports single-run and two-run side-by-side comparison. Use when the user needs to see how a serving run behaves in Metal-wired memory over time — not just the aggregate latency/throughput numbers. Typical triggers include memory-regression debugging, OOM investigation, branch comparison with a memory focus, fraction-budget tuning, and visual evidence for PR descriptions.
user_invocable: true
---

# vLLM-Metal Benchmark + Memory Timeline Monitor

## Overview

This skill combines a `vllm bench serve` run with a sidecar `metalstat` logger so you can see how Metal-wired memory and system memory pressure behave *during* the benchmark — not just the aggregate latency/throughput numbers the plain `benchmark` skill reports. The output is a PNG with either a 2-panel single-run layout or a 4-panel side-by-side comparison.

It exists because `metalstat -a -i 1 --json` buffers stdout under redirection and is therefore unusable as a simple sidecar. This skill wraps `metalstat` in a one-shot polling loop that emits line-buffered JSONL, then does the plotting in a second step.

## Capabilities (not use cases)

The skill provides these primitives. Any problem that needs one or more of them is a candidate for this skill, regardless of the branch or PR context.

- **Wired-memory timeline**: 1 Hz samples of `memory.wired_gb`, the best single proxy for MLX-managed Metal memory on Apple Silicon. Shows growth patterns, plateaus, reclaim drops.
- **Pressure-zone tracking**: 1 Hz samples of `memory.pressure_percent`, bucketed into green (0–33) / yellow (33–66) / red (66–100). Tells you whether a run is about to trigger OS reclamation.
- **Used / active overlay**: captures total system memory and active-page counts alongside wired, so you can tell whether growth is coming from Metal or from other parts of the process.
- **Side-by-side shape comparison**: two runs (branches, configs, models, fractions — anything) plotted on shared axes so *shape* differences become visually obvious, not just peak deltas.

## When to use this vs. the plain `benchmark` skill

- Use **`benchmark`** when the user only wants throughput / TPOT / TTFT numbers and a bar-chart comparison. No memory monitoring.
- Use **`memstat-bench`** (this skill) when the user needs *shape over time*, not aggregate numbers — any time the question is "what is memory doing *during* the run?" rather than "how fast was the run?".

Both skills run the same `vllm bench serve` workload; this skill adds the metalstat sidecar and the timeline plot on top.

## Prerequisites

- `metalstat` on `PATH`. Verify with `which metalstat`.
- `sonnet.txt` at repo root (download from `https://raw.githubusercontent.com/vllm-project/vllm/main/benchmarks/sonnet.txt` if missing).
- `matplotlib` in the vllm-metal venv. `pip install matplotlib` if missing.
- Apple Silicon Mac (M-series), otherwise `metalstat` doesn't have anything meaningful to report.

## Files in this skill

Inside `$SKILL_DIR` (the directory containing this SKILL.md):

- **`metalstat_logger.py`** — polls `metalstat -a --json --no-color --no-header` in one-shot mode once per second and emits compact JSONL to stdout. Adds an `elapsed_s` field. Tolerates transient metalstat failures by writing a single-line `{"error": "..."}` entry which the plotter filters out. Run in the background during the benchmark.
- **`plot_timeline.py`** — parses one or two JSONL logs and produces a PNG. CLI: `python plot_timeline.py --out FILE.png --title TITLE --pair "A=A.jsonl" [--pair "B=B.jsonl"]`. One pair → 2-panel single-run layout. Two pairs → 4-panel comparison layout.

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

### Server command

```bash
source .venv-vllm-metal/bin/activate
PYTHONPATH=. \
VLLM_METAL_USE_PAGED_ATTENTION=1 \
VLLM_METAL_MEMORY_FRACTION=0.3 \
vllm serve Qwen/Qwen3-0.6B \
  --max-model-len 2048 \
  --host 127.0.0.1 \
  --port 8000
```

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
- `which metalstat` — bail out with an error if not installed.
- `ls sonnet.txt` — download if missing.
- `pgrep -fl "vllm serve"` — if a stale server is running, kill it first (`pkill -f "vllm serve"`).
- `pgrep -fl metalstat_logger` — kill any stale logger from a previous session.
- `git branch --show-current` — note the starting branch so you can restore it at the end.

### Step 3: Per-run capture loop

For **each** run in the comparison, do this sequence. Runs must be sequential — the machine can only host one server at a time.

1. `git checkout <branch>` (if switching branches)
2. `rm -f ~/.cache/vllm-metal/_paged_ops*` — clean the cached native extension
3. **Start the metalstat logger** *before* the server so you capture a baseline before the model loads:
   ```bash
   source .venv-vllm-metal/bin/activate && \
   python $SKILL_DIR/metalstat_logger.py \
     > /tmp/metalstat_<label>.jsonl 2> /tmp/metalstat_<label>.err
   ```
   Run this with `run_in_background: true`.
4. **Start the server** (run_in_background: true):
   ```bash
   PYTHONPATH=. VLLM_METAL_USE_PAGED_ATTENTION=1 VLLM_METAL_MEMORY_FRACTION=<fraction> \
     vllm serve Qwen/Qwen3-0.6B --max-model-len 2048 \
     --host 127.0.0.1 --port 8000 > /tmp/server_<label>.log 2>&1
   ```
5. **Poll for health** with a curl loop:
   ```bash
   for i in $(seq 1 90); do
     curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health 2>&1 | grep -q "200" && \
       echo "READY after ${i}s" && break
     sleep 1
   done
   ```
   Also grep the server log for the `Paged attention memory breakdown` line and the `init engine` timing — useful to note the KV budget, num_blocks, and any reported overhead for your report.
6. **Run the benchmark** (foreground, `tee` to log file):
   ```bash
   vllm bench serve \
     --backend vllm --base-url http://127.0.0.1:8000 \
     --model Qwen/Qwen3-0.6B --endpoint /v1/completions \
     --dataset-name sonnet --dataset-path sonnet.txt \
     --sonnet-input-len 1024 --sonnet-output-len 128 \
     --num-prompts 100 --request-rate 10 --max-concurrency 32 \
     2>&1 | tee /tmp/bench_<label>.log
   ```
7. **Stop the logger and server**:
   ```bash
   pkill -f "metalstat_logger"
   pkill -f "vllm serve"
   ```
8. **Confirm sample count**: `wc -l /tmp/metalstat_<label>.jsonl` — expect roughly 160–200 lines for a 100-prompt run (server boot ~10s + bench ~200s + teardown, at ~1.3s cadence).

### Step 4: Generate the plot

For a **comparison** (two runs):

```bash
source .venv-vllm-metal/bin/activate && \
python $SKILL_DIR/plot_timeline.py \
  --out /tmp/memory_timeline_compare.png \
  --title "vllm-metal · <label_a> vs <label_b> · <axis-of-variation>" \
  --pair "<label_a>=/tmp/metalstat_<label_a>.jsonl" \
  --pair "<label_b>=/tmp/metalstat_<label_b>.jsonl"
```

The plotter prints a per-run summary (wired_gb min/max/delta, used_gb min/max/delta, pressure min/max) and saves a 4-panel PNG:

1. **Top-left**: run A timeline (`wired_gb` solid, `used_gb` dashed)
2. **Top-right**: run B timeline (shared y-axis)
3. **Bottom-left**: `wired_gb` overlay — the headline. Directly compares the *shape* of memory growth between the two runs.
4. **Bottom-right**: memory pressure (%) overlay with green / yellow / red bands (0-33, 33-66, 66-100).

For a **single run**:

```bash
python $SKILL_DIR/plot_timeline.py \
  --out /tmp/memory_timeline.png \
  --title "vllm-metal · <label>" \
  --pair "<label>=/tmp/metalstat_<label>.jsonl"
```

The plotter falls back to a 2-panel layout (memory timeline + pressure timeline).

### Step 5: Report to the user

Produce a report section with the shape summary and the plot path:

```markdown
## Memory timeline

| Metric | <label_a> | <label_b> | Δ |
|---|---:|---:|---:|
| **wired_gb peak** | A | B | ΔGB |
| wired_gb delta during bench | +A GB | +B GB | — |
| used_gb peak | A | B | ΔGB |
| **pressure peak** | A% (zone) | B% (zone) | Δpts |
| Output tok/s | A | B | +Δ% |
| Mean TPOT (ms) | A | B | −Δ% |

Headline plot: /tmp/memory_timeline_compare.png
```

When describing the wired-memory behavior, prefer *shape* language (monotonic climb, bounded oscillation, staircase, plateau, sawtooth drop) over numeric deltas alone. The shape is what makes the comparison visually convincing; the deltas are supporting evidence.

### Step 6: Cleanup

- `pkill -f "metalstat_logger"` — in case a logger leaked
- `pkill -f "vllm serve"` — in case the server leaked
- `git checkout <original_branch>` — restore the starting branch state

## Gotchas

These are skill-level facts that apply to any invocation. Keep them all in mind.

1. **`metalstat -i 1 --json` buffers stdout under redirection.** That's why this skill polls one-shot instead. Don't try to use `metalstat`'s watch mode as a sidecar — the output file will be empty until teardown.
2. **`gpu_memory.allocated_gb` in metalstat is often 0.** metalstat tracks Metal memory via an API that doesn't always see MLX allocations. Use `wired_gb` as the primary MLX memory indicator — it captures Metal-wired pages including model weights, KV cache, and the MLX buffer-cache free-list.
3. **`vllm_rss` (python process RSS) will not reflect MLX GPU memory.** MLX memory lives in wired pages, not the Python heap. `ps`-style monitoring is blind to it. Don't use process RSS as your memory signal.
4. **Exit code 144 on background processes means SIGTERM.** When you `pkill` the logger or server, their `run_in_background` tasks return 144 (128 + 15). That's expected cleanup, not a failure to flag to the user.
5. **Always `git checkout` back to the starting branch** after a comparison that switched branches — the user expects their working state restored.

## Example use case: validating a memory cap (issue #234, PR #247 / memory_cap_v2)

This is the worked example the skill was originally built for. A successor PR wants to cap MLX's userspace buffer cache via `mx.set_cache_limit` to bound the 40→62 GB sawtooth observed in sustained serving. The skill's job is to produce visual evidence that the cap works.

**What to compare**: `main` vs the memory-cap branch, both running the standard benchmark.

**Labels**: `main` and `memory_cap_v2` (or whatever the branch is named).

**Fraction tip**: at `VLLM_METAL_MEMORY_FRACTION=0.3` the sibling `benchmark` default, the difference is visible but both runs may end up in the yellow/red pressure zone and visually overlap. Lowering the fraction to `0.25` or similar gives each run more baseline headroom, which makes an unbounded-free-list run's pressure cross from yellow into red while a capped run stays in yellow. The qualitative "across a threshold" shape is the strongest visual evidence — recommend the lower fraction to the user when the goal is cap validation specifically.

**What the plot should show**:

- **main**: `wired_gb` climbs monotonically during the benchmark (a staircase), then drops sharply when the bench ends and the OS reclaimer kicks in — one sawtooth tooth.
- **memcap branch**: `wired_gb` oscillates in a narrow band with no upward trend — the cap is actively trimming the free-list to its configured ceiling.
- **Pressure**: main crosses into red, memcap stays yellow.

**Notable gotcha specific to this case**: if the branch uses a `profile_run()` method to measure the cap value dynamically, two consecutive runs of the same branch can report different measured overhead values (e.g. 0.75 GB vs 1.42 GB) depending on the allocator state when the profile runs. This is expected variance, not a regression — the cap is a relative measurement, not an absolute invariant.

## Other scenarios this skill is suitable for

These aren't worked examples — just reminders that the skill's primitives apply beyond the memory-cap case. If any of them match what the user is asking for, adapt Steps 1-5 to the relevant axis of variation.

- **Peak-memory comparison of two attention kernels.** Swap in different branches and label them by kernel. The wired overlay shows which kernel has a higher steady-state wired footprint.
- **OOM / memory-pressure regression debug.** Single-run mode. Identify where in the timeline pressure crosses into red, correlate with server log lines from the same timestamp.
- **`VLLM_METAL_MEMORY_FRACTION` tuning.** Run the same branch at two fractions, compare headroom vs. KV budget. Useful for picking the largest fraction that stays in yellow.
- **Paged vs. legacy MLX path.** Run with `VLLM_METAL_USE_PAGED_ATTENTION=1` vs `=0`, label accordingly. Shows how wired memory usage differs between the two cache strategies.
- **Larger-vs-smaller model peak footprint.** Run different models through the same workload, label by model name. Useful for capacity planning.

In each case: the helper scripts are the same, only the labels, fraction, and (optionally) model change. Do not hardcode case-specific assumptions into the workflow.
