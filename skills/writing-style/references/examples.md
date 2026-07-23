# Before/After Examples

## Restating evidence

Before:
> **$62.47 per GB** ... **$18.55 per GB**, more than 3x cheaper. Apple Silicon offers a surprisingly economical option.

After:
> **$62.47 per GB** ... **$18.55 per GB**, more than 3x cheaper.

The numbers already said it.

## Throat-clearing

Before:
> A quick cost-of-memory comparison helps explain the motivation. An NVIDIA RTX 5090 ships with...

After:
> An NVIDIA RTX 5090 ships with...

## Roadmap narration

Before:
> We first review vLLM's memory allocation on CUDA as the baseline design — it is the upstream that vllm-metal adapts from. We then examine how mistral.rs and llama.cpp, both with native Metal support, approach the same problem on Apple Silicon. To compare them clearly, we use a common vocabulary:

After:
> To compare the three engines below, we use a common vocabulary:

The subsection headers (### vLLM, ### mistral.rs, ### llama.cpp) already tell the reader what's coming.

## Boilerplate sign-off

Before:
> This post describes the problem in detail, surveys related work, and proposes a redesigned memory allocation path for vllm-metal that is honest about its memory model and adapts to Apple Silicon's shared-memory reality.

After: deleted. The TOC communicates structure; "honest about its memory model" is editorializing.

## Cliche emphasis

Before:
> **llama.cpp** sidesteps dynamic budget computation entirely. It uses the memory hint as its ceiling...

After:
> **llama.cpp** uses the memory hint as its ceiling...

## Overclaiming

Before:
> none of them target the shared-memory desktop case that vllm-metal needs to handle.

After:
> vLLM assumes exclusive ownership of a discrete memory pool. mistral.rs introduces Apple Silicon-specific caps for desktop coexistence. llama.cpp pre-commits a user-specified amount with no system-wide awareness.

mistral.rs does target the shared-memory desktop case. State what each does precisely.

## Describe, don't critique

Before:
> The intent is reasonable, but the cap is applied inconsistently between the two phases.

After: rewritten to describe the mechanism neutrally — what each phase does, how the values relate — without judging it as a bug.

---

# Public-facing responses (from an EMNLP rebuttal)

## Point, don't recite

Before:
> Enforcing the invariants restores equivalence: 90.8 to 97.3% exact match versus 0 to 3.5% for BSP/DSD (Table 2), and removing raggedness removes the cost: alignment overhead 27.7% to 14.6%, one-third fewer verification calls, 64% higher throughput (Table 4).

After:
> Enforcing the invariants removes the corruption (Table 2), and removing raggedness removes the cost (Table 4).

The tables carry the magnitudes; the sentence carries the logic. Keep a number inline only when it is the punchline (a 0-3.5% exact-match collapse).

## Stacked references

Before:
> HuggingFace Transformers still has no batched speculation: a WIP PR from Oct 2023 was closed unmerged (huggingface/transformers#26875), and the feature request has been open since Jul 2024 (#32165).

After:
> HuggingFace Transformers still has no batched speculation (the feature request, huggingface/transformers#32165, has been open since Jul 2024).

One reference the reader might actually open beats two they skim. The duration claim also shrank to match the surviving pointer.

## Claim must match the pointer

Before:
> our methods sit at or above that floor on every model family.

After:
> our methods match or exceed that floor in all but one case, which is within 0.6 points.

One cell sat 0.6 points below the floor; a reviewer comparing the cited table would find it. Same rule for qualifiers: "27.7% to 14.6% at batch 8 (Table 4)" fails if Table 4 nowhere says batch 8. Drop the qualifier.

## Aggregates must support the sentence

Before:
> on average the first divergent token appears only in the final few percent of the sequence.

After:
> when divergence occurs, it occurs late in generation (partial match 95.7-98.6%, Table 2).

The average includes exact-match sequences at 100%, so "final few percent" does not follow from it.

## Hedges and status moves

Before:
> We would respectfully argue the audited population is broader and more current than it may appear.

After:
> The audited population is broader and more current than it may appear.

Before:
> Finally, in case it was easy to miss: the complete implementation is included in the Supplementary Material.

After:
> One note on the software subscore: the complete implementation is included in the Supplementary Material (Appendix I).

The first hedges; the second sneers. Both bury the point.

## Clever contrast

Before:
> The findings reach beyond that family even though the algorithms do not.

After:
> The methods are contiguous-only; the findings are not.

## Cold reader

Before:
> We write down the two requirements a correct implementation must keep, rectangular alignment and position-ID contiguity. And we prove that keeping them under contiguous layouts has a superlinear cost (Theorem 3.1).

After:
> We trace the root cause to the ragged tensor problem: sequences in a batch accept different numbers of tokens each step, so their positions and caches drift out of sync. The paper writes down the synchronization conditions an implementation must maintain to stay correct, and proves that maintaining them is disproportionately expensive in the standard memory layout, where the whole batch lives in one rectangular tensor (Theorem 3.1).

The before is correct but only readable with the paper fresh in mind: it assumes the reader knows the invariant names, "contiguous", and "superlinear". The after glosses each term in-line, so a reader who never opened the paper can follow the argument. Reviewers skim; the AC may not have read the paper at all.
