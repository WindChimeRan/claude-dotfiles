---
name: paper_rebuttal
description: "Strategic patterns for writing strong author rebuttals to academic peer reviews. Use when drafting, planning, or revising a response to reviewer comments on a conference or journal paper — especially ML/NLP venues (NeurIPS/ICML/ICLR/ACL/COLM/EMNLP/CVPR/etc.). Triggers on 'rebuttal', 'response to reviewers', 'author response', 'reply to reviewer', 'reviewer feedback', or when the user shares review text and wants help drafting a reply. Covers venue calibration, two postures (defend a consensus vs. flip a reject-leaning reviewer), 10 named rhetorical patterns, hard-case handling (contradictory/factually-wrong reviewers, length limits), a fill-in scaffold, and a process workflow. Rhetorical patterns are distilled from Tri Dao et al.'s FlashAttention NeurIPS 2022 rebuttal."
---

# Paper Rebuttal Strategy

## Core idea

The real audience of a rebuttal is the **Area Chair**, not the reviewers. Reviewers may not change scores; the AC writes the metareview and weighs *whether each concern was substantively addressed*, not just the final numbers. So even a reviewer you cannot flip can be **neutralized**: if the AC sees the concern was answered with evidence, they discount it. Every move should make the AC's job of writing "accept" easier.

Two things must be calibrated before any pattern below applies: **the venue's mechanics** (can you revise the PDF? one shot or discussion phase? length limit?) and **your posture** (are you defending a consensus, or trying to flip a reject?). Get those wrong and good rhetoric is wasted.

## Calibrate to your venue first

Rebuttal mechanics vary enough to invalidate specific tactics. Before drafting, answer:

- **Can you revise the PDF / add appendices during rebuttal?** NeurIPS/ICLR often allow a revision; CVPR/ACL/COLM often do **not**. This decides whether you can write "see new Appendix E.5" or must report results inline.
- **One-shot or multi-round discussion?** Single-shot → front-load everything, hold nothing back. Discussion phase → you can stage follow-ups and add results mid-thread.
- **Hard length limit?** (characters/words/one page) Dictates how hard you triage (see *Hard cases*).
- **Per-reviewer replies, one global response, or both?** If global-only, the Common Response *is* the rebuttal; structure it by theme.
- **Double-blind?** Keep the rebuttal anonymous — no links to your repo, no "in our prior NeurIPS paper," nothing that deanonymizes.
- **Can you see and answer reviewer follow-ups before the decision?**

Then map mechanics → tactics: no PDF revision ⇒ report new numbers **inline in the response text** and *commit specific additions to the camera-ready*, rather than citing a fresh appendix. Tight char limit ⇒ batch minor fixes into one line. Global-only ⇒ skip per-reviewer cross-references.

### COLM 2026 (pre-filled — verify exact limits in the author portal)

From the COLM 2026 CfP:

- **PDF is locked during review**: *"Changes to the paper will not be allowed while the paper is being reviewed."* ⇒ **No new appendices.** Report new results inline in the rebuttal text; commit concrete additions to the camera-ready. Main text is capped at **9 pages** (+ unlimited references; optional ethics/repro/ack ≤1 page each don't count), so budget that space when promising additions.
- **Double-blind** ⇒ keep the response anonymous.
- **Rebuttal window: May 22 – June 8, 2026. Decisions: July 8, 2026.**
- OpenReview-based, so per-reviewer threaded comments are likely, and discussion may continue after the initial response. The CfP did **not** specify a character limit or the exact discussion mechanics — confirm those in the portal/author guide before finalizing length.

## Pre-work: triage every concern

Before writing a single sentence, classify each reviewer concern into one bucket:

- **Existential** — "techniques are well known", "you're optimizing the wrong thing", "contribution is unclear." Must be **reframed**, not just answered. Carries the most score weight.
- **Substantive** — missing baseline, experiment, or ablation. Run it; report the result.
- **Specific** — typos, clarifications, notation, minor presentation. Concede and fix. Cheap credibility deposits.
- **Misunderstanding** — answer with a precise text pointer ("described in Sec X.Y, lines AAA–BBB"). If multiple reviewers misread the same thing, that's a writing problem — fix the text and say so; don't blame the reader.

The first two drive score changes. The last two build the trust on which the first two land.

## Read the score, pick the game: defend vs. flip

The FlashAttention rebuttal was played **from ahead** (all reviews ≥ Weak Accept). Most of its moves assume you're maintaining a consensus. If you have reject-leaning scores you must *convert*, the game is different. Decide which mode you're in per reviewer.

### Defend (reviewer is already at/above bar)
Maintain consensus; hand the AC quotable wins; stay gracious; **don't open new attack surface**. The main failure mode here is over-arguing a minor point and manufacturing doubt where there was none. Answer cleanly, concede small things, move on.

### Flip (reviewer is reject-leaning: 3–5 / borderline)
Changing a mind is harder than reinforcing one. Playbook:

1. **Find the load-bearing objection.** For each negative reviewer, identify the *one* concern that, if fully resolved, removes their stated reason to reject. Test: "if I completely answer X, does their review still justify this score?" If yes, you found the wrong X. Address satellite complaints only after the load-bearing one.
2. **Lead with the score-changing content**, not thanks-and-throat-clearing. A reject-leaning reviewer skims — put the strongest refutation or new result in the first two sentences.
3. **Concede fast and visibly on everything non-load-bearing.** Agreement on four minor points buys the standing to push back on the one major one.
4. **Give a face-saving offramp.** Reviewers rarely flip if it means admitting error. Frame the resolution as "the reviewer's question prompted a clarification/experiment that strengthens the paper" — they raise their score because the paper *improved*, not because they were wrong.
5. **Make the ask implicit and concrete:** "We believe this resolves the central concern about X, and we're glad to clarify anything still open." Never "please raise your score."
6. **Spend effort by convertibility.** A borderline 5 with specific, addressable concerns is worth more words than a vague 3 or an entrenched Confidence-5 reject. But never *visibly* neglect anyone — the AC reads every thread, so an unconvertible reviewer still gets a substantive, on-record answer (that's the neutralize move from *Core idea*).

## The 10 strategic patterns

(Distilled from the FlashAttention rebuttal; see `references/flash_attention_analysis.md` for the source quotes.)

### 1. The "elegant rediscovery" reframe
When critiqued for using known techniques, do **not** deny it. Two-step move:
1. **Concede the strawman**: "if this were a new problem, a simple solution might suggest obviousness."
2. **Deny the premise**: "but this problem has been studied intensively for [N] years with [substantial] headroom remaining."

Then reframe novelty as **taste**, not invention: "showing that a classic viewpoint was even competitive, and in fact missing from the state of the art, is elegant." Reviewers can argue with novelty claims; they cannot argue with "you missed this gap."

### 2. Weaponize other people's published work
The most persuasive counterexamples come from **named, peer-reviewed work by others**. When asked whether tiling alone explains the speedup, FA points to Rabe & Staats — a published algorithm with tiling but no fusion that runs *40% slower*. The reviewer can verify it. A third party's result beats your own counterfactual every time. Apply to: ablation defenses, baseline justifications, "have you considered X?" deflections.

### 3. Replace adjectives with coefficients
Every numerical claim gets a coefficient and a reference. "Much faster" → "5.7× speedup (Fig 2 Left)". Build at least one **compressed thesis sentence** with 3+ numbers that prove the design philosophy in one line:

> "FlashAttention incurs more FLOPs (13% more) due to recomputation but reduces IOs by 9.1×, leading to 5.7× speedup."

The 13% / 9.1× / 5.7× pattern collapses the whole thesis into one quotable line. Make one for your paper — reviewers copy these into metareviews.

### 4. Reframe existential critiques causally
When a reviewer says "you're optimizing the wrong thing," don't defend the choice — argue that **the thing they think matters more is itself caused by what you fix**. FA on "FFN dominates runtime, not attention": *models are scaled by hidden dimension because existing attention is slow on long sequences; our work changes that calculus.* The objection becomes evidence of the paper's importance. Pattern: name the constraint that makes the reviewer's claim true today, then show your paper removes it.

### 5. Answer substantive asks with results, and anchor them concretely
Every surviving substantive/existential critique gets either (a) a **new result**, (b) a **published counterexample**, or (c) a **precise pointer** to text the reviewer missed. Never a bare argument.

**Anchor depends on the venue (see Calibrate):**
- *If you can revise the PDF* (NeurIPS-style): "we have added X to Appendix E.Y." Trackable and AC-readable. FA added several new appendices and tables during its window (the analysis lists all 8) — the AC's metareview specifically praised this.
- *If the PDF is locked* (COLM/CVPR/ACL-style): report the numbers **inline** in the response ("New experiment: on [setting], we obtain [coefficients]") and **commit** the addition to the camera-ready ("we will add this as Appendix X"). You lose the live appendix pointer but keep the evidence and the responsiveness signal.

### 6. Own bugs as credibility deposits
If a small bug or inconsistency exists, declare it precisely and fix it: *"we put weight decay on LayerNorm by accident, causing a 0.1 perplexity gap; fixed, now matches."* Low cost; high return — every other number reads as more credible once you've shown you'll cop to a mistake. Also covers figure/table inconsistencies a reviewer catches, batch-size mismatches, citation errors.

### 7. Forward-looking statements as evidence, not promises *(situational)*
When you genuinely have external validation, cite it as present-tense reality — it signals the field has already voted, and the AC infers ratification:
- "We are working with the [framework] developers to integrate X."
- "X has been independently reimplemented in [other framework] / verified by [authority]."

**Caveat:** FlashAttention had this because it was a viral open release. Most papers under review do **not**, and inventing or inflating adoption backfires. If you have no such validation, skip this entirely — its absence is normal and hurts nothing. Don't manufacture a weak version.

### 8. Handle unconvertible reviewers for the AC, not for conversion
A Confidence-5 reviewer at Weak Accept rarely flips. Optimize what the AC sees: answer every question (even throwaways); if there's a discussion phase, add new results to follow-ups; own any inconsistency they catch immediately; sign off "thank you for the productive discussion." Their final acknowledgment — even "thanks for the clarifications" — becomes evidence *for* you.

### 9. Reciprocity costs nothing
Even when an experiment was already planned, credit the reviewer: *"thanks to your suggestion, we added..."* Converts their question into their contribution; they become invested in the paper landing. (In *flip* mode this doubles as the face-saving offramp.) Use once or twice per reviewer — more reads as pandering.

### 10. Close with a viewpoint, not a plea
Never end with "we hope the reviewers will reconsider." End with a line that positions the paper as the opening of a broader program:

> "FlashAttention is an example where exciting opportunities open up at the intersection of hardware & algorithms."

This is what the AC quotes. Make the last line do work.

## Hard cases

**Contradictory reviewers** (R1: too much X; R2: too little X). Surface the tension explicitly and neutrally, ideally in the Common Response: "R1 and R2 offered complementary views on X; we believe the right balance is Y because [reason tied to the paper's goal]." Pick a principled middle and *own* it. Never silently side with one — the other notices, and the AC sees you pandering.

**Factually-wrong reviewer.** Correct via evidence, never assertion, and never make them feel stupid. Pattern: *"We may not have made this clear — [precise fact], shown in [location / new result]. We've revised the text to prevent this reading."* Take the blame for the miscommunication even when they misread; it costs nothing and avoids a defensive spiral. If the error is consequential and they're dug in, make sure the **correction is legible to the AC** (state the fact cleanly once) — the AC is the arbiter.

**Prioritization under a hard length limit.** When concerns exceed space:
1. Every **existential** concern gets real space — non-negotiable.
2. **Score-blocking** concerns from reject-leaning reviewers next.
3. Batch all **minor** fixes into one line: "We also fixed [typo L54], [notation in Eq 3], [missing ref p23] — thank you."
4. For anything cut, leave a one-line "addressed in camera-ready" pointer rather than silence.
5. Cut your own adjectives and throat-clearing before you cut content — this is where coefficients earn their keep (one number replaces a sentence of praise).

## Anti-patterns to avoid

- **Pure defense.** Every point adds data, a reframe, or a counterexample. Never "we disagree" alone.
- **Adjective-heavy claims.** "Significantly/much better" without coefficients.
- **Apologetic openings.** "We apologize for the confusion" weakens before strengthening. Fix and move on.
- **Score begging.** Never explicitly ask for a number change. The AC notices.
- **Repeating the abstract.** They've read the paper.
- **Ignoring an existential critique** or deflecting it to "see paper."
- **Singling out a reviewer publicly as wrong.** Route shared misreads through the Common Response.
- **Per-reviewer repetition of common points.** Cross-reference the Common Response.
- **Pages of math.** Point to the appendix; the rebuttal is a roadmap, not the proof.
- **Inventing external validation** to force Pattern 7. Absence is normal.
- **Promising PDF changes the venue forbids.** At a locked-PDF venue, say "camera-ready," not "see revised Appendix."

## Concrete scaffold

Fill this in; delete the parts your venue's format doesn't support.

```
=== COMMON RESPONSE (use if 3+ reviewers or any shared theme) ===
[1 sentence: consensus framing for the AC — what reviewers agreed is good]
[1 sentence: roadmap of what follows]
[ONLY if genuinely true: concrete external validation since submission]

Theme A (raised by R1, R3): <bold one-line restatement of the shared concern>
  <reframe (Pattern 1/4) OR new result with coefficients (Pattern 3/5) +
   camera-ready commitment if PDF is locked>
Theme B (raised by R2, R4): ...

=== RESPONSE TO R1 (rating, confidence — note defend vs. flip) ===
We thank R1 for <specific, genuine point>.  [If shared: "On X, see the Common Response."]
Q1: <bold restatement of their question>
  <new data inline / published counterexample / precise text pointer>
Q2: ...
[If a major review: close with a forward-looking line (Pattern 10).]

=== repeat per reviewer ===
```

Ordering tips: if responses are visible to all reviewers, lead with your most supportive reviewer to set a positive frame. In *flip* mode, spend your best material on the most convertible reject-leaner. In each reply, the **first sentence after thanks** should be the highest-impact content for that reviewer.

## Process workflow

When the user shares reviews and asks for a rebuttal:

0. **Calibrate to the venue** (PDF-revisable? discussion phase? length limit? blind?). This gates every later choice.
1. **Read all reviews twice.** Tag every concern with reviewer ID + category + (defend/flip).
2. **Triage** into existential / substantive / specific / misunderstanding.
3. **Per reviewer, pick the game** (defend vs. flip) and, for flips, name the load-bearing objection.
4. **Identify shared themes** (raised by 2+ reviewers) → Common Response.
5. **Draft existential reframes first** — the reframe determines what data you need.
6. **List every new experiment needed** and start them in parallel; the window is short.
7. **Draft the Common Response**: consensus line → roadmap → (optional) external validation → themes.
8. **Draft per-reviewer replies**, cross-referencing the Common Response; each Q a bold-prefixed paragraph; flips lead with score-changing content.
9. **Adjective→coefficient pass.** Replace "much/significantly better" with number + reference.
10. **Evidence pass.** Every existential/substantive point has new data, a published counterexample, or a text pointer — never a bare argument. Anchor per venue (appendix vs. inline+camera-ready).
11. **Viewpoint pass.** Each major section closes with a forward-looking line.
12. **Length pass.** Cut adjectives, throat-clearing, "we believe" hedges; enforce the venue limit; batch minor fixes.
13. **Anonymity pass** (if double-blind): no identifying links or self-references.

## Canonical example — with a caveat

The rhetorical patterns are illustrated in Tri Dao et al.'s FlashAttention NeurIPS 2022 rebuttal (Accept; the AC praised the rebuttal additions).

- Raw PDF: [references/flash_attention_rebuttal.pdf](references/flash_attention_rebuttal.pdf)
- Sentence-level analysis + per-reviewer playbook: [references/flash_attention_analysis.md](references/flash_attention_analysis.md)

**Caveat (read before over-indexing on it):** this is a single example (n=1) of a paper that was *already above the bar* — all five reviews were ≥ Weak Accept, and it could revise its PDF mid-rebuttal at a venue with a full discussion phase. So its strengths are the **transferable rhetoric** (Patterns 1–4, 6, 9, 10 — venue- and posture-independent). Its **non-transferable parts** are the posture (defending a consensus, not flipping a reject — see *Read the score*) and the mechanics (live appendix additions, multi-round discussion, real industry adoption — see *Calibrate* and Patterns 5, 7). Use the analysis for *how a sentence is built*, and this skill's earlier sections for *which game you're actually playing*.
