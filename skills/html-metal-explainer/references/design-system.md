# HTML Metal Explainer — Design System

## Full CSS

Copy this CSS block verbatim into every generated HTML file's `<style>` tag. Do not modify colors, font sizes, or spacing — consistency across reports matters.

```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface2: #1c2333;
  --border: #30363d;
  --text: #e6edf3;
  --text-dim: #8b949e;
  --accent: #58a6ff;
  --accent2: #7ee787;
  --accent3: #d2a8ff;
  --accent4: #ffa657;
  --red: #ff7b72;
  --yellow: #e3b341;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  font-size: 16px;
}
.container { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }

/* Header */
header {
  text-align: center;
  padding: 3rem 0 2rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 3rem;
}
header h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
header .subtitle { color: var(--text-dim); font-size: 1.1rem; }
header .meta {
  margin-top: 1rem;
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  font-size: 0.85rem;
  color: var(--text-dim);
}
header .meta span { display: flex; align-items: center; gap: 0.3rem; }

/* Sections */
section { margin-bottom: 3rem; }
h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--accent);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
h2 .num {
  background: var(--accent);
  color: var(--bg);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;
}
h3 {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 1.5rem 0 0.75rem;
  color: var(--accent3);
}
h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 1.2rem 0 0.5rem;
  color: var(--accent4);
}
p { margin-bottom: 1rem; }

/* Code blocks */
pre {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  overflow-x: auto;
  font-size: 0.82rem;
  line-height: 1.55;
  margin-bottom: 1rem;
}
code {
  font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', Consolas, monospace;
  font-size: 0.88em;
}
:not(pre) > code {
  background: var(--surface);
  padding: 0.15em 0.4em;
  border-radius: 4px;
  color: var(--accent);
}

/* Concept boxes */
.concept {
  background: var(--surface2);
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.25rem;
  margin: 1.2rem 0;
}
.concept.warn { border-left-color: var(--yellow); }
.concept.good { border-left-color: var(--accent2); }
.concept.danger { border-left-color: var(--red); }
.concept .label {
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.3rem;
  color: var(--accent);
}
.concept.warn .label { color: var(--yellow); }
.concept.good .label { color: var(--accent2); }
.concept.danger .label { color: var(--red); }

/* Diagrams */
.diagram {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.2rem 0;
  font-family: 'SF Mono', 'Fira Code', Consolas, monospace;
  font-size: 0.78rem;
  line-height: 1.5;
  overflow-x: auto;
  white-space: pre;
}

/* Comparison table */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}
th, td {
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--border);
  text-align: left;
}
th {
  background: var(--surface2);
  font-weight: 600;
  color: var(--accent);
}
tr:nth-child(even) { background: var(--surface); }

/* Decision box */
.decision {
  background: linear-gradient(135deg, #1a2332, #1c2838);
  border: 2px solid var(--accent2);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}
.decision h4 {
  color: var(--accent2);
  font-size: 1.1rem;
  margin-top: 0;
}
.verdict {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.85rem;
  margin-right: 0.5rem;
}
.verdict.yes { background: #1a3a2a; color: var(--accent2); border: 1px solid var(--accent2); }
.verdict.maybe { background: #2a2a1a; color: var(--yellow); border: 1px solid var(--yellow); }
.verdict.no { background: #2a1a1a; color: var(--red); border: 1px solid var(--red); }

/* Lists */
ul, ol { margin-bottom: 1rem; padding-left: 1.5rem; }
li { margin-bottom: 0.4rem; }

/* Highlight spans */
.hl { color: var(--accent); font-weight: 600; }
.hl2 { color: var(--accent2); font-weight: 600; }
.hl3 { color: var(--accent3); font-weight: 600; }
.hl4 { color: var(--accent4); font-weight: 600; }
.dim { color: var(--text-dim); }

/* TOC */
.toc {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
}
.toc h3 { margin-top: 0; color: var(--text); font-size: 1rem; }
.toc ol { margin-bottom: 0; }
.toc li { margin-bottom: 0.3rem; }
.toc a { color: var(--accent); text-decoration: none; }
.toc a:hover { text-decoration: underline; }

/* Footer */
footer {
  border-top: 1px solid var(--border);
  padding-top: 2rem;
  margin-top: 3rem;
  color: var(--text-dim);
  font-size: 0.85rem;
  text-align: center;
}

/* Responsive */
@media (max-width: 640px) {
  .container { padding: 1rem; }
  header h1 { font-size: 1.5rem; }
  pre { font-size: 0.75rem; }
  .diagram { font-size: 0.7rem; }
}
```

## HTML Skeleton

Every report starts with this structure. Fill in title, subtitle, meta, TOC, sections, and footer.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TITLE — vllm-metal</title>
<style>
  /* paste full CSS above */
</style>
</head>
<body>
<div class="container">

<header>
  <h1>TITLE</h1>
  <div class="subtitle">SUBTITLE</div>
  <div class="meta">
    <span>vllm-metal</span>
    <span>DATE</span>
    <span>AUDIENCE</span>
  </div>
</header>

<nav class="toc">
  <h3>Contents</h3>
  <ol>
    <li><a href="#sec1">Section 1</a></li>
    <!-- ... -->
  </ol>
</nav>

<section id="sec1">
<h2><span class="num">1</span> Section Title</h2>
<!-- content -->
</section>

<!-- more sections -->

<footer>
  <p>Generated for vllm-project/vllm-metal</p>
  <p>Key files: <code>path/to/relevant/files</code></p>
</footer>

</div>
</body>
</html>
```

## Component Examples

### Concept Box Variants

```html
<!-- Neutral info (blue) -->
<div class="concept">
  <div class="label">Key Concept: SIMD Lockstep</div>
  <p>All 32 lanes execute the same instruction simultaneously.</p>
</div>

<!-- Warning/caveat (yellow) -->
<div class="concept warn">
  <div class="label">Why This Matters</div>
  <p>If the kernel is bandwidth-bound, compute savings are invisible.</p>
</div>

<!-- Positive insight (green) -->
<div class="concept good">
  <div class="label">The Key Insight</div>
  <p>V equals kv_norm — no separate V load needed.</p>
</div>

<!-- Danger/risk (red) -->
<div class="concept danger">
  <div class="label">Risk</div>
  <p>Register spills will tank performance silently.</p>
</div>
```

### Decision Box

```html
<div class="decision">
  <h4>Decision: Should We Switch to exp2?</h4>
  <p><span class="verdict yes">Yes — Do in P2</span> Low risk, 1.2-1.5x gain.</p>
  <!-- alternatives: -->
  <p><span class="verdict maybe">Defer to P3</span> Need benchmarks first.</p>
  <p><span class="verdict no">No</span> The maintenance tax outweighs the gain.</p>
</div>
```

### ASCII Diagram

```html
<div class="diagram">
Memory Hierarchy (Apple M-series GPU)

Registers   ──  ~0 cycles   ──  ~256 slots/thread  ──  private
    │
Shmem       ──  ~1-5 cycles ──  32-64 KB            ──  per threadgroup
    │
Device DRAM ──  ~100+ cycles ──  16-128 GB           ──  global
</div>
```

### Before/After Code Comparison

Use two `<pre>` blocks with `<h4>` labels:

```html
<h4>Before (scalar loads):</h4>
<pre><code>for (int j = 0; j < 16; j++)
    k[j] = float(ptr[lane * 16 + j]);
// 16 load instructions</code></pre>

<h4>After (vectorized):</h4>
<pre><code>for (int j = 0; j < 4; j++)
    k_v[j] = *reinterpret_cast&lt;const device half4 *&gt;(ptr + lane * 16 + j * 4);
// 4 load instructions</code></pre>
```

### Regime Impact Table

```html
<table>
  <tr><th>Regime</th><th>Bottleneck</th><th>Optimization Helps?</th></tr>
  <tr>
    <td>G=1, B=1 (bandwidth-bound)</td>
    <td>DRAM load latency</td>
    <td><span class="verdict no">No</span></td>
  </tr>
  <tr>
    <td>G=4, B=8 (compute-shifted)</td>
    <td>Per-token arithmetic</td>
    <td><span class="verdict yes">Yes</span> 10-15%</td>
  </tr>
</table>
```
