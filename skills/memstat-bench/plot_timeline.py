"""Plot memory timelines captured by metalstat_logger.

Usage
-----
    # Single run
    python plot_timeline.py --out timeline.png \\
        --pair "memory_cap_v2=/tmp/metalstat.jsonl"

    # Two-run comparison (the most common use case)
    python plot_timeline.py --out compare.png \\
        --title "vllm-metal · memory_cap_v2 vs main · fraction=0.25" \\
        --pair "main=/tmp/metalstat_main.jsonl" \\
        --pair "memory_cap_v2=/tmp/metalstat_memcap.jsonl"

The comparison layout is a 2x2 grid:
  top-left:     per-branch timeline for run A (wired_gb + used_gb)
  top-right:    per-branch timeline for run B (wired_gb + used_gb)
  bottom-left:  wired_gb overlay (the headline — shape comparison)
  bottom-right: memory pressure overlay with green/yellow/red bands

Single-run layout is a 1x2 grid:
  left:  wired_gb / used_gb / active_gb timeline
  right: memory pressure timeline with zone bands
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.size"] = 10

# Paired colors: blue = baseline, orange = PR / new config
COLORS = ["#5b9bd5", "#e06030"]


def load(path: str) -> list[dict]:
    """Load a JSONL file produced by metalstat_logger, skipping error lines."""
    out: list[dict] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "elapsed_s" in d and "memory" in d:
                out.append(d)
    return out


def series(samples: list[dict]) -> dict[str, list[float]]:
    return {
        "t": [s["elapsed_s"] for s in samples],
        "used": [s["memory"]["used_gb"] for s in samples],
        "wired": [s["memory"]["wired_gb"] for s in samples],
        "active": [s["memory"]["active_gb"] for s in samples],
        "press": [s["memory"]["pressure_percent"] for s in samples],
    }


def print_summary(label: str, d: dict[str, list[float]]) -> None:
    w, u, p = d["wired"], d["used"], d["press"]
    print(f"== {label} ==")
    print(
        f"  wired_gb:  min={min(w):.2f}  max={max(w):.2f}  "
        f"delta={max(w) - min(w):+.2f}"
    )
    print(
        f"  used_gb:   min={min(u):.2f}  max={max(u):.2f}  "
        f"delta={max(u) - min(u):+.2f}"
    )
    print(f"  pressure%: min={min(p):.0f}  max={max(p):.0f}")


def add_pressure_bands(ax: plt.Axes) -> None:
    ax.axhspan(0, 33, color="#b7e1a1", alpha=0.2, label="green")
    ax.axhspan(33, 66, color="#fde68a", alpha=0.2, label="yellow")
    ax.axhspan(66, 100, color="#f4b5b5", alpha=0.2, label="red")


def plot_single(label: str, s: dict, title: str, out: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax1 = axes[0]
    ax1.plot(s["t"], s["wired"], label="wired_gb", color=COLORS[0], linewidth=2)
    ax1.plot(
        s["t"],
        s["used"],
        label="used_gb",
        color=COLORS[0],
        linewidth=1.2,
        linestyle="--",
        alpha=0.7,
    )
    ax1.plot(
        s["t"],
        s["active"],
        label="active_gb",
        color="#4daf4a",
        linewidth=1.2,
        alpha=0.7,
    )
    ax1.set_title(f"{label} · memory timeline", fontweight="bold")
    ax1.set_xlabel("Elapsed seconds")
    ax1.set_ylabel("Memory (GB)")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower right", fontsize=9)

    ax2 = axes[1]
    add_pressure_bands(ax2)
    ax2.plot(s["t"], s["press"], color=COLORS[0], linewidth=2.2)
    ax2.set_title(f"{label} · memory pressure", fontweight="bold")
    ax2.set_xlabel("Elapsed seconds")
    ax2.set_ylabel("Pressure (%)")
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right", fontsize=8)

    if title:
        fig.suptitle(title, fontsize=13, fontweight="bold", y=1.02)

    plt.tight_layout()
    plt.savefig(out, dpi=170, bbox_inches="tight", facecolor="white")
    print(f"Saved plot: {out}")


def plot_compare(runs: list[tuple[str, dict]], title: str, out: str) -> None:
    if len(runs) != 2:
        raise ValueError(
            f"plot_compare expects exactly 2 runs, got {len(runs)}"
        )
    (label_a, a), (label_b, b) = runs
    fig = plt.figure(figsize=(16, 9))

    # Top row: per-branch timelines (shared y-axis for visual comparability)
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(a["t"], a["wired"], label="wired_gb", color=COLORS[0], linewidth=2)
    ax1.plot(
        a["t"],
        a["used"],
        label="used_gb",
        color=COLORS[0],
        linewidth=1.2,
        linestyle="--",
        alpha=0.7,
    )
    ax1.set_title(f"{label_a} · memory timeline", fontweight="bold", color=COLORS[0])
    ax1.set_ylabel("Memory (GB)")
    ax1.set_xlabel("Elapsed seconds")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower right", fontsize=9)

    ax2 = fig.add_subplot(2, 2, 2, sharey=ax1)
    ax2.plot(b["t"], b["wired"], label="wired_gb", color=COLORS[1], linewidth=2)
    ax2.plot(
        b["t"],
        b["used"],
        label="used_gb",
        color=COLORS[1],
        linewidth=1.2,
        linestyle="--",
        alpha=0.7,
    )
    ax2.set_title(f"{label_b} · memory timeline", fontweight="bold", color=COLORS[1])
    ax2.set_ylabel("Memory (GB)")
    ax2.set_xlabel("Elapsed seconds")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right", fontsize=9)

    # Bottom-left: wired overlay — the headline panel
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(a["t"], a["wired"], label=label_a, color=COLORS[0], linewidth=2.2)
    ax3.plot(b["t"], b["wired"], label=label_b, color=COLORS[1], linewidth=2.2)
    ax3.set_title("wired_gb overlay (Metal-wired memory)", fontweight="bold")
    ax3.set_ylabel("Wired memory (GB)")
    ax3.set_xlabel("Elapsed seconds")
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc="lower right", fontsize=10)

    # Bottom-right: pressure overlay
    ax4 = fig.add_subplot(2, 2, 4)
    add_pressure_bands(ax4)
    ax4.plot(a["t"], a["press"], label=label_a, color=COLORS[0], linewidth=2.2)
    ax4.plot(b["t"], b["press"], label=label_b, color=COLORS[1], linewidth=2.2)
    ax4.set_title("memory pressure (%)", fontweight="bold")
    ax4.set_ylabel("Pressure (%)")
    ax4.set_xlabel("Elapsed seconds")
    ax4.set_ylim(0, 100)
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc="lower right", fontsize=9)

    if title:
        fig.suptitle(title, fontsize=14, fontweight="bold", y=1.00)

    plt.tight_layout()
    plt.savefig(out, dpi=170, bbox_inches="tight", facecolor="white")
    print(f"Saved plot: {out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot memory timelines from metalstat_logger JSONL.",
    )
    parser.add_argument(
        "--pair",
        action="append",
        required=True,
        help="LABEL=PATH — one per run, repeat for comparison (max 2)",
    )
    parser.add_argument(
        "--title",
        default="",
        help="figure suptitle (optional)",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="output PNG path",
    )
    args = parser.parse_args()

    if len(args.pair) not in (1, 2):
        parser.error("provide 1 (single) or 2 (comparison) --pair entries")

    runs: list[tuple[str, dict]] = []
    for spec in args.pair:
        if "=" not in spec:
            parser.error(f"--pair must be LABEL=PATH, got: {spec!r}")
        label, _, path = spec.partition("=")
        if not label or not path:
            parser.error(f"--pair must be LABEL=PATH, got: {spec!r}")
        if not Path(path).exists():
            parser.error(f"log file not found: {path}")
        samples = load(path)
        if not samples:
            parser.error(f"log file has no valid samples: {path}")
        s = series(samples)
        print_summary(label, s)
        runs.append((label, s))

    if len(runs) == 1:
        plot_single(runs[0][0], runs[0][1], args.title, args.out)
    else:
        plot_compare(runs, args.title, args.out)


if __name__ == "__main__":
    main()
