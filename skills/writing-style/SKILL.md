---
name: writing-style
description: "Technical writing style guide for editing blog posts, research write-ups, documentation, and public-facing responses (paper rebuttals, review replies, public comments). Use when reviewing, editing, or drafting technical prose — especially when asked to 'check', 'review', 'edit', or 'fix' writing, when writing new sections for an existing post, or when drafting or trimming a response that will be posted publicly."
---

# Writing Style Guide

## Core rule

Every sentence must carry information the reader does not already have. If removing a sentence loses nothing, remove it.

## Eliminate

1. **Restating evidence as prose** — if numbers or formulas already made the point, do not add a summary sentence.
2. **Throat-clearing** — drop setup sentences ("A quick comparison helps explain...", "It is worth noting that...").
3. **Roadmap narration** — if headers or a TOC already communicate structure, do not narrate it ("We first review X. We then examine Y.").
4. **Cliche emphasis** — avoid "entirely", "surprisingly", "notably", "importantly" and similar filler adverbs. Say what it does, not how impressed the reader should be.
5. **Boilerplate sign-off sentences** — "This post describes X, surveys Y, and proposes Z" adds nothing when the TOC already exists.
6. **Em dashes** — do not use "—" in sentences. Use periods, commas, or restructure instead.

## Constraints

1. **No overclaiming** — state only what is precisely true. Prefer narrow, accurate statements over sweeping ones.
2. **Describe, don't critique** — in literature reviews and related work sections, state the design and its trade-offs. Do not editorialize on what is "broken" or "wrong."
3. **Balance parallel sections** — subsections covering comparable items (e.g., three engines, three algorithms) should have comparable depth and length. If one is trimmed, check the others.
4. **Prefer cutting to rewriting** — when a passage is verbose, the fix is usually deletion, not rephrasing.

## Public-facing responses (rebuttals, review replies, public comments)

Internal drafts and notes carry full detail; public posts carry only load-bearing detail. Detail is cheap to generate now, so volume no longer signals effort — to a reader it pattern-matches to generated padding. What signals a human is selection (the one right fact in the one right place) and disclosed calibration. For rebuttal *strategy* (what to argue), see the paper_rebuttal skill; this section is the prose register (how to write it).

1. **One checkable fact per claim** — the reader verifies one pointer and the claim stands. A second reference buries the first; nobody checks both. A full evidence list appears only where the pattern itself is the argument, and only once per document.
2. **Point, don't recite** — for results already in the paper, say what happens and point: "enforcing the invariants removes the corruption (Table 2)". Keep a number inline only when it is the punchline. Numbers sit in parentheses at the end of a claim, never as the subject of the sentence.
3. **Two-speed test** — a skimmer reading only first sentences gets the complete argument; a checker finds one pointer per claim that verifies in under thirty seconds.
4. **The claim must match the pointer exactly** — no qualifier the cited table does not show. Disclose exceptions instead of rounding over them: a disclosed 0.6-point exception reads as care, a discovered one reads as an overclaim. Do not understate your own source either. A claim about an aggregate must actually follow from it arithmetically.
5. **Match the register of the question** — a quantitative objection gets a quantitative answer; a conceptual objection gets a conceptual answer with one anchor. Vague answers to precise questions read as evasion (and vagueness is also an AI smell; the fix is precision in few places, not hedging everywhere).
6. **Correct a misread once, directly** — state what the work is, name the misread plainly, own what invited it, move on. Do not stack defenses where one suffices, and do not concede the misread to be polite.
7. **Cut hedges and status moves** — "we would respectfully argue", "we believe", "we hope", "in case it was easy to miss". State the point; keep courtesy in the frame, not inside the argument.
8. **Plain sentences over clever contrasts** — "The methods are contiguous-only; the findings are not" beats "The findings reach beyond that family even though the algorithms do not."
9. **Park trims in reserve** — move cut material to a not-for-posting notes section for round-2 follow-ups; do not delete it.
10. **Write for the cold reader** — assume the reviewer skimmed the paper and the AC never opened it. Gloss every paper-internal term in plain words once at first use, or replace it with a description ("the synchronization conditions a correct implementation must maintain", not "invariants I1/I2"). The argument must be followable without the paper open; if a sentence only lands after re-reading the paper, rewrite it. Pay the gloss cost once, in the block everyone reads first.

## Process

When asked to review or edit:

1. Read the full piece (or section) first.
2. List specific sentences or phrases that violate the rules above, with line references.
3. Wait for approval before making changes.
4. When editing, make all fixes in one pass.

For concrete examples, see [references/examples.md](references/examples.md).
