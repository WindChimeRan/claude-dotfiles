---
name: benchmark
description: Run vLLM serving benchmarks on the vllm-metal project. Handles server startup, benchmark execution, branch comparison (git checkout), and generates PR-ready markdown with GitHub summary/detail blocks and matplotlib comparison figures. Use when the user asks to benchmark, compare performance, or generate benchmark results for a PR.
user_invocable: true
---

# vLLM-Metal Serving Benchmark

## Overview

This skill runs serving benchmarks for the vllm-metal project, compares results across branches or configurations, and produces PR-ready output.

## Standard Benchmark Configuration

Always use these settings unless the user explicitly overrides:

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

### Server Command (paged path)

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

### Server Command (mlx_lm path — no paged attention)

```bash
source .venv-vllm-metal/bin/activate
PYTHONPATH=. \
vllm serve Qwen/Qwen3-0.6B \
  --max-model-len 2048 \
  --host 127.0.0.1 \
  --port 8000
```

### Client Command

```bash
source .venv-vllm-metal/bin/activate
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

### Step 1: Ask the User

Before running, confirm:
1. **What to compare**: current branch vs main? current branch vs mlx_lm path? two specific branches?
2. **Log file names**: suggest names like `bench_<branch>.log` (e.g., `bench_main.log`, `bench_primitive.log`, `bench_mlx.log`)
3. **Any overrides**: different model, prompt count, concurrency, etc.

### Step 2: Run Benchmarks

For each configuration:
1. `git checkout <branch>` (if comparing branches)
2. Clean the cached extension: `bash -c 'rm -f ~/.cache/vllm-metal/_paged_ops*'`
3. Start the server in the background
4. Wait for health check: `curl --retry 15 --retry-all-errors -s http://127.0.0.1:8000/health`
5. Run the client command, pipe output to `tee <logfile>`
6. Kill the server: `pkill -f "vllm serve"`
7. Switch to next branch/config and repeat

### Step 3: Extract Results

Parse each log file for these metrics:
- Benchmark duration (s)
- Output token throughput (tok/s)
- Total token throughput (tok/s)
- Mean TTFT (ms)
- Mean TPOT (ms)
- P99 TPOT (ms)
- Mean ITL (ms)

### Step 4: Generate PR-Ready Output

Produce two outputs:

#### 4a. Markdown Summary (for PR description)

Use GitHub `<details><summary>` blocks:

```markdown
### Benchmark (sonnet 1024+128, 100 prompts, concurrency 32)

| Metric | main | this PR | Change |
|---|---:|---:|---:|
| Output tok/s | X | Y | +Z% |
| Total tok/s | X | Y | +Z% |
| Mean TTFT (ms) | X | Y | -Z% |
| Mean TPOT (ms) | X | Y | -Z% |

<details>
<summary>Full benchmark output</summary>

**main**
```
[paste raw vllm bench serve output]
```

**this PR**
```
[paste raw vllm bench serve output]
```
</details>

<details>
<summary>Benchmark config</summary>

- Model: Qwen/Qwen3-0.6B
- Dataset: sonnet (1024 input + 128 output)
- Prompts: 100, rate: 10, concurrency: 32
- Memory fraction: 0.3
- Hardware: [detect from `sysctl -n machdep.cpu.brand_string` and `sysctl -n hw.memsize`]
</details>
```

#### 4b. Comparison Figure

Generate a Python matplotlib script following this pattern (adapted from existing bench_plot_*.py files in the repo):

```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.size"] = 11

labels = ["main", "this PR"]  # adapt to comparison
colors = ["#5b9bd5", "#e06030"]  # blue=baseline, orange=new

# Fill in from benchmark results
output_tput = [X, Y]
mean_tpot_ms = [X, Y]
mean_ttft_ms = [X, Y]

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
x = np.arange(len(labels))

def draw_bar(ax, data, title, ylabel, unit=""):
    bars = ax.bar(x, data, width=0.45, color=colors, edgecolor="white", linewidth=1.2)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(data) * 1.30)
    for bar, val in zip(bars, data):
        txt = f"{val:.1f}{unit}" if val >= 1 else f"{val:.2f}{unit}"
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                txt, ha="center", va="bottom", fontsize=10, fontweight="bold")

draw_bar(axes[0], mean_ttft_ms, "Mean TTFT", "Milliseconds", "ms")
draw_bar(axes[1], output_tput, "Output Throughput", "Tokens / sec", " tok/s")
draw_bar(axes[2], mean_tpot_ms, "Mean TPOT", "Milliseconds", "ms")

fig.suptitle(
    "Title · Qwen3-0.6B · Sonnet · 100 reqs, rate=10, concurrency=32",
    fontsize=13, fontweight="bold", y=1.02)

plt.tight_layout()
plt.savefig("bench_comparison.png", dpi=180, bbox_inches="tight", facecolor="white")
plt.savefig("bench_comparison.pdf", bbox_inches="tight", facecolor="white")
```

**Adapt the figure based on:**
- Number of bars (2 for A vs B, 3 for A vs B vs C)
- Which metrics the user wants to highlight (user may request different metrics)
- Color scheme: gray `#9ca3af` for mlx_lm baseline, blue `#5b9bd5` for main/before, orange `#e06030` for the new/this PR
- Title reflecting what's being compared

Run the script to generate the PNG, then tell the user the file path so they can upload it to the PR.

## Important Notes

- Always use `PYTHONPATH=.` when running from the repo root
- Always kill the server between benchmark runs
- Always clean the cached extension (`rm -f ~/.cache/vllm-metal/_paged_ops*`) when switching branches that modify `paged_ops.cpp`
- If you encounter OOM or server crash, **stop and ask the user** — don't retry with lower settings without asking
- The `sonnet.txt` file should exist at repo root. If not, download: `wget https://raw.githubusercontent.com/vllm-project/vllm/main/benchmarks/sonnet.txt`
- After benchmarking, `git checkout` back to the original branch
