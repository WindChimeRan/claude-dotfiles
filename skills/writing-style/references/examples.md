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
