---
name: html-metal-explainer
description: Generate educational HTML reports that explain Metal GPU kernel internals, optimizations, and parallelism for the vllm-metal project. Use when the user asks to explain a kernel concept, compare kernel implementations, document an optimization proposal, or create onboarding material about Metal shaders, simdgroups, threadgroups, online softmax, paged attention, or any Apple Silicon GPU topic in vllm-metal. Also trigger when someone asks for a "tutorial", "explainer", "guide", or "report" about Metal kernels, or when they want to hand off kernel analysis to someone less familiar with GPU programming.
user_invocable: true
---

# HTML Metal Explainer

Generate polished, dark-themed HTML educational reports about Metal GPU kernel topics in vllm-metal. The output is a single self-contained `.html` file that opens in any browser — no build step, no dependencies.

## When to Use

- Explaining a kernel optimization (proposed or existing)
- Comparing two kernel implementations (e.g., MLA vs GQA paged attention)
- Creating onboarding docs for someone unfamiliar with GPU/Metal programming
- Documenting a PR's kernel changes for review or handoff
- Any request for a "tutorial", "guide", or "explainer" about Metal kernel internals

## Output Location

Save the HTML file to `research/` in the project root (create the directory if needed). Use a descriptive kebab-case filename:
- `research/mla-block-batching-explainer.html`
- `research/simdgroup-parallelism-guide.html`
- `research/gqa-vs-mla-comparison.html`

Open in the browser after writing: `open <path>`

## Research Before Writing

Before generating the HTML, read the relevant source files to ground the explanation in real code. Key locations in vllm-metal:

- `vllm_metal/metal/kernels_v2/pagedattention.metal` — GQA paged attention kernel (production, mature)
- `vllm_metal/metal/kernels_v2/mla.metal` — MLA paged attention kernel (if it exists)
- `vllm_metal/metal/kernels_v2/utils.metal` — shared utilities
- `vllm_metal/metal/paged_ops.cpp` — C++ nanobind dispatcher
- `vllm_metal/metal/__init__.py` — Python entry points
- `vllm_metal/paged_attention_backend/mla.py` — MLA wrapper / routing
- MLX reference kernels at `.venv-vllm-metal/lib/python3.12/site-packages/mlx/include/mlx/backend/metal/kernels/`

Also read `CLAUDE.md` for project architecture context.

## Document Structure

Every report follows this skeleton. Adapt section count and titles to the topic, but keep the progression from "background concepts" → "the specific topic" → "decision / summary":

1. **Background sections** (1-3) — build up prerequisite knowledge. Start from what the reader needs to know, not what you want to teach. For kernel topics, this usually means: GPU thread hierarchy, memory hierarchy, and the specific algorithm (attention, softmax, etc.).

2. **Core analysis sections** (1-3) — the actual topic. Show current code, explain the problem or comparison, propose or evaluate alternatives. Use concrete code from the repo, not hypothetical examples.

3. **Decision / Summary section** (1) — a clear verdict table and actionable next steps. Include a validation protocol (what tests to run, what to benchmark).

## Design System

Use this exact CSS and HTML structure. The dark theme with GitHub-inspired colors is deliberate — it matches the terminal-centric workflow of kernel developers. See `references/design-system.md` for the full CSS and component catalog.

### Core Components

**Numbered section headers:**
```html
<h2><span class="num">1</span> Section Title</h2>
```

**Concept callout boxes** (4 variants):
```html
<div class="concept">           <!-- blue: neutral info -->
<div class="concept warn">      <!-- yellow: gotcha or caveat -->
<div class="concept good">      <!-- green: key insight or win -->
<div class="concept danger">    <!-- red: pitfall or risk -->
  <div class="label">Label Text</div>
  <p>Content...</p>
</div>
```

**ASCII diagrams** (for parallelism layouts, memory hierarchies, data flow):
```html
<div class="diagram">
Threadgroup (1024 threads)
├── Simdgroup 0 (32 lanes)
│   ├── Lane 0 → dims [0..15]
│   └── Lane 31 → dims [496..511]
└── Simdgroup 31
</div>
```

**Decision boxes** (for recommendations):
```html
<div class="decision">
  <h4>Decision: Should We Do X?</h4>
  <p><span class="verdict yes">Yes</span> Explanation...</p>
  <!-- or: <span class="verdict maybe">Defer</span> -->
  <!-- or: <span class="verdict no">No</span> -->
</div>
```

**Comparison tables:**
```html
<table>
  <tr><th>Feature</th><th>Kernel A</th><th>Kernel B</th></tr>
  <tr><td>exp function</td><td>fast::exp</td><td>fast::exp2</td></tr>
</table>
```

**Inline highlights** for key terms:
```html
<span class="hl">blue highlight</span>
<span class="hl2">green highlight</span>
<span class="hl3">purple highlight</span>
<span class="hl4">orange highlight</span>
```

## Writing Style

- **Progressive disclosure**: start from what the reader knows, build up. Don't dump all concepts at once.
- **Concrete over abstract**: always show real code from the repo, with file paths and line numbers. Never invent hypothetical kernels.
- **Why before what**: explain *why* a design choice was made before showing the code. GPU kernel decisions are driven by hardware constraints — surface those constraints.
- **Quantify claims**: "16 FMAs per token" not "many operations". "32 KB shmem limit on M1" not "limited memory".
- **Use diagrams liberally**: ASCII art in `<div class="diagram">` blocks. GPU parallelism is inherently spatial — draw it.
- **One concept per callout box**: don't overload `.concept` boxes. Each should teach exactly one thing.

## Content Guidelines by Topic Type

### Optimization Proposals
Structure: Problem → Current Code → The Idea (with diagram) → Concrete Fix (code sketch) → Expected Impact (table by regime) → Risks → Decision Box

### Kernel Comparisons
Structure: What Each Kernel Does → Shared Concepts → Feature-by-Feature Table → Unique Contributions of Each → Summary

### Concept Explainers (onboarding)
Structure: Analogy/Intuition → Formal Definition → How It Appears in This Codebase → Common Pitfalls → Exercises/Questions

### PR Kernel Reviews
Structure: What Changed → Why It Matters → Algorithm Deep-Dive → Correctness Analysis → Performance Analysis → Decision

## Regime Awareness

When discussing performance, always distinguish between:
- **Bandwidth-bound** (decode, G=1, small batch): memory load latency dominates. Compute savings are invisible.
- **Compute-bound** (prefill, G=4, large batch): arithmetic throughput dominates. Instruction count matters.
- **Transitional** (G=2, medium batch): both contribute. Measure to know which dominates.

Never claim an optimization "helps" without specifying the regime. Use tables with regime columns.
