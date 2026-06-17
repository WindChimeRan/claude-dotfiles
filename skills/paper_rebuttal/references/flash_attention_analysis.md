# FlashAttention NeurIPS 2022 Rebuttal — Deep Analysis

This is a sentence-level reading of Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré's rebuttal to the NeurIPS 2022 reviews of *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. Source: `flash_attention_rebuttal.pdf` in this folder, downloaded from OpenReview.

The rebuttal succeeded — paper was accepted. The Area Chair's metareview specifically noted that "during the rebuttal phase the authors have included additional experiments that further strengthen the contributions and value of the paper."

This document captures both the macro structure and the sentence-level rhetorical maneuvers, so future rebuttals can reuse them.

---

## The reviewer field

Five reviewers. Understanding their ratings, confidences, and stances is essential, because the authors handle each differently:

| Reviewer | Rating | Confidence | Stance |
|----------|--------|------------|--------|
| jjqW     | 8 (Strong Accept) | 3 | Supportive, has technical clarifying Qs |
| UuW7     | 6 (Weak Accept)   | **5** | Adversarial, deeply technical, raises 8 Qs including "you're optimizing the wrong thing" |
| uahY     | 8 (Strong Accept) | 4 | Supportive, asks about end-to-end metrics and inference |
| ucdo     | 7 (Accept)        | 4 | Positive, asks about resource-constrained devices |
| 5Whx     | 7 (Accept)        | 4 | Positive, asks about ViT, roofline plot |

UuW7 is the only score below 7. Confidence 5 means "absolutely certain... checked math/other details carefully." Authors clearly knew this score was unlikely to flip — and optimized the engagement accordingly.

Final outcome: jjqW unchanged at 8, UuW7 unchanged at 6, uahY raised score, ucdo raised to "clear accept," 5Whx satisfied. Three explicit "rebuttal acknowledged" posts.

---

## Macro structure

The rebuttal is organized as:

```
Common Response [1/2]   <-- shared themes, opens to all reviewers
Common Response [2/2]
  Response to jjqW
    Reviewer reply
  Response to UuW7 (part 1)
  Response to UuW7 (part 2)
    Reviewer follow-up
    Authors' follow-up response
  Response to uahY
    Reviewer score raise
  Response to ucdo
    Reviewer score raise
  Response to 5Whx
    Reviewer acknowledgment
```

The Common Response is split across two posts due to OpenReview's character limit. The first post handles **Updates + Contribution + Techniques**. The second handles **Baselines + Outlook**. This ordering matters: the AC reads top-down, so the most positive framing (impact updates) lands first.

---

## Sentence-level analysis of the Common Response

### Opening (the AC anchor)

> "We thank the reviewers for insightful comments and constructive feedback. We are happy that all reviews were positive, and that reviewers thought that our work addresses an important problem with well-designed experiments, and that our paper was clear and well-written."

Two sentences. Three implicit messages to the AC:
1. **All reviews are positive.** This is true (lowest is Weak Accept) and is the headline before any debate.
2. **The reviewers agreed on three things**: important problem, well-designed experiments, clear writing. Naming these establishes them as not-up-for-debate.
3. **The authors are gracious**, not adversarial. Sets the tone the AC will use to read the rest.

### Structural announcement

> "We first report some updates, address a few common questions, and then respond to specific questions from the reviewers."

A table of contents. Lets the AC skim. This kind of meta-narration is normally bad in papers but is right in rebuttals because the AC's reading mode is triage.

### Updates section (the impact anchor)

Before any defense, the authors list four updates since submission:

1. **PyTorch integration in progress** — i.e., framework adoption
2. **Triton & Jax reimplementations exist** — i.e., other researchers found it valuable enough to port
3. **MLPerf submission officially verified by MLCommons** — i.e., external authority confirmed
4. **Major companies adopting for 8K-context LLMs** — i.e., industry pull

This isn't "future work." Every claim is a present-tense external action by people other than the authors. The AC's read: *the field has already decided this paper matters; we are being asked to ratify a verdict.*

The phrasing "We are happy to see that FlashAttention has already begun making an impact in a short time" frames updates as *impact*, not progress.

### The Contribution paragraph (where the existential critique is handled)

This paragraph addresses "techniques are well-known," which UuW7 and 5Whx and (gently) jjqW raised. The construction is worth quoting in full:

> "Several reviewers point out that the high-level techniques we used are known (as we made clear in the paper, lines 49 and 145). If this were a new problem, a simple answer using well-known techniques might suggest that the problem is not interesting or that the solution is obvious. However, speeding up attention is arguably one of the most studied and economically valuable problems in machine learning in the past 5 years, with huge teams of researchers and engineers working on it (from major deep learning frameworks, many large companies, and academia, cf. paragraph below on baselines). Yet FlashAttention can still speed it up substantially with no approximation (2-4x speedup, 10-20x memory saving for the attention layer). That we showed a classic viewpoint was even competitive, and in fact missing from the state of the art, is to our mind elegant and important."

Four moves in sequence:

1. **Pre-emptive concession with citation** — "as we made clear in the paper, lines 49 and 145." Forecloses any "you tried to hide this" reading.
2. **Hypothetical strawman construction** — "If this were a new problem, a simple answer might suggest obviousness." The authors build the reviewer's argument *for* them, in maximally charitable form.
3. **Denial of premise, not of conclusion** — "However, this problem has been studied for 5 years by huge teams." The strawman's "if" clause is denied; the logic is preserved.
4. **Reframe novelty as taste** — "showing a classic viewpoint was even competitive... is *elegant* and important." The word "elegant" is the key — taste claims are unanswerable by reviewers, while novelty claims invite counterclaims.

Then comes the analogy:

> "Moreover, this 'simple technique' of being IO-aware was at the core of large scale data processing (e.g., relational databases), and its implications played out over several generations. Being IO-aware required massive redesign to databases and data management systems, so it's a big idea and viewpoint that we look forward to applying to more areas."

Database IO-awareness was foundational despite (or because of) its simplicity. The implicit argument: *the simpler an insight looks once stated, the more foundational it may be.* This turns "obvious in hindsight" — usually a slur — into the point of the paper.

### The Techniques paragraph (the gap thesis)

> "It was surprising to us that even though all the high-level techniques (tiling & recomputation) are available, there was still so much headroom (2-4x) in speeding up exact attention."

The word **"surprising"** does heavy lifting. It positions the authors as readers of the field, not actors — they're discovering with the reviewer, not defending.

> "(1) The technique of softmax decomposition with scaling (line 151) is known to many ML algorithm researchers but might not have been obvious to many systems researchers, while operation fusion / memory IOs reduction is the bread-and-butter of the systems / compilers community but is not as familiar to algorithm researchers. In our case of FlashAttention, one needs both the softmax decomposition and the operation fusion to achieve speedup and memory saving."

This is the **culture-gap explanation**: ML algorithms and systems are separate research cultures with separate vocabularies. The novelty is in bridging them, not in inventing either primitive. This is a rare and powerful kind of contribution claim — it can't be falsified by pointing to either community's prior work, because the whole point is that neither community combined them.

### The Baselines paragraph (status play disguised as evidence)

> "For BERT, it's the MLPerf implementation from Nvidia that set the fastest training record at the time of submission, which also fuses all attention steps. This implementation is written specifically for BERT-large in the MLPerf benchmark (seqlen at most 512, head dim 64 only, A100 only), and is 2.8x faster than Huggingface BERT (Appendix E.1). MLPerf implementations from vendors are often the result of teams of hardware and software engineers working for 6 months (duration between MLPerf rounds)."

Three credibility moves stacked:

1. **Provenance**: not "a strong baseline" but "the MLPerf implementation from Nvidia that set the fastest training record at submission time."
2. **Calibration**: this baseline is itself 2.8× faster than the common reference (HuggingFace). So beating it by another 2-3× is meaningful, not incremental.
3. **Effort framing**: "teams of engineers working for 6 months." The authors aren't beating a quick baseline; they're beating organized industrial effort. The implicit argument: *if simple ideas can beat 6 engineer-months, simple ideas are valuable.*

For GPT-2, the same move with Megatron-LM, framed via **celebrity models**:

> "the Megatron-LM implementation of Transformers has been used to train some of the largest language models (Megatron-Turing NLG, OPT, and BLOOM)."

The reader doesn't have to know Megatron-LM's benchmarks — they know OPT and BLOOM. Authority by association.

### Outlook closing

> "Outlook: FlashAttention is an example where exciting opportunities open up at the intersection of hardware & algorithms. We hope that our work inspires future research in this intersection."

One sentence, plus one wish. No score plea. The sentence positions the paper as the opening of a research program. This is the line you want the AC to internalize.

---

## Per-reviewer playbook

### jjqW (Strong Accept, Confidence 3)
**Stance**: supportive, technical clarifying questions.
**Strategy**: precise direct answers; cite a third-party counterexample (Rabe & Staats with 40% slowdown) to settle the tiling-vs-HBM-access question. Concede the writing-clarity suggestion with grace: "We will clarify this in the text. Thank you for this suggestion." Result: no change in score, supportive post-rebuttal comment.

### UuW7 (Weak Accept, Confidence 5) — the adversarial reviewer
**Stance**: skeptical; raises 8 questions including the most dangerous one (Q8: "you're optimizing the wrong thing — FFN dominates").
**Strategy**: never get defensive; answer every single question; add new appendix B.5 specifically for this reviewer's Rabe & Staats comparison; reframe Q8 causally (see below); in the discussion-phase follow-up, add **two new tables** (Table 8 multi-GPU, Table 11 batch-size sensitivity); own the figure-batch-size inconsistency UuW7 catches; sign off with "thank you for the productive discussion."

Q8 is worth quoting in full because the reframe is masterful:

UuW7 said: *"For reasonably large sequence lengths, FF layers are still the main contributor to the end-to-end runtime. I am wondering if we are targeting the right problem to reduce the runtime of transformer models."*

Authors:
> "For the large language models currently in use (e.g., >1B) the FFN layers take more time than attention, as the hidden dimension is often much larger than the context length, but future models could have much longer context length. We speculate that one of the reasons these models are scaled by increasing hidden dimension (and not context length) is that the existing attention implementation is slow and memory-hungry on long sequences. One would then have to use larger hidden dimensions so that the FFN layers take more time proportionally (compared to attention), in order to make efficient use of hardware. Our work is a step toward changing this calculus..."

Four moves:
1. **Concede the fact** (FFN does dominate for >1B).
2. **Pivot to hypothesis** (future models with longer context).
3. **Causal reframe** (FFN dominates *because* attention was inefficient; the design space was constrained by what the paper fixes).
4. **Conclusion** ("Our work is a step toward changing this calculus.") plus evidence ("several companies are looking to use FlashAttention with 8k context").

The reviewer's objection becomes evidence of the paper's importance.

Result: UuW7's score stayed at 6, but the discussion thread reads as engaged and constructive. The AC's metareview overrides the lone 6.

### uahY (Strong Accept, Confidence 4)
**Stance**: supportive; wants end-to-end memory and inference data; concerned about pretrained models.
**Strategy**: precise numbers ("10-20x for attention layer; 1.8x for BERT-large, 4x for GPT2-small for full model"), appeal to authority for inference ("PyTorch developers report FlashAttention matches FasterTransformer + Tensor RT"), point to in-paper example for pretrained ("Sec 4.2 directly replaced attention in pretrained RoBERTa without modifying weights"). Result: **score raised**.

### ucdo (Accept, Confidence 4)
**Stance**: positive; raises resource-constrained-device concern.
**Strategy**: show empirical data (T4 GPU experiment, 2-4.5x speedup), pivot to trend ("other accelerators have *more* SRAM, not less — TPUv4 has 128MB, Graphcore 1GB vs A100's 19MB"), generalize ("alternative is register files"). Result: **score raised to clear accept**.

### 5Whx (Accept, Confidence 4)
**Stance**: positive; asks about ViT, roofline plot.
**Strategy**: run the requested experiments during the rebuttal — add Appendix E.4 (ViT on ImageNet, 1.5x speedup at seqlen 196, 3.4x at seqlen 3136) and Appendix E.7 (roofline). Concede techniques-known concern by referring to Common Response. Result: satisfied acknowledgment.

---

## The "13% / 9.1× / 5.7×" sentence

> "FlashAttention incurs more FLOPs (13% more) due to recomputation but reduces IOs by 9.1X, leading to 5.7X speedup."

This sentence appears in the reply to UuW7's Q5. It's the entire paper compressed into 18 words:

- **Trade**: 13% more compute
- **Win**: 9.1× less memory I/O
- **Result**: 5.7× wallclock speedup

This is the IO-awareness thesis as one quotable line. The AC's metareview echoed this exact framing: "Even though the proposed approach has higher FLOP count w.r.t. the standard attention implementation, it leads to reduced wall clock time due to the smaller number of HBM accesses."

The lesson: **build at least one such triplet for your own paper**. Three numbers in one sentence that prove the design philosophy.

---

## Counted appendix additions during the rebuttal

The authors added the following during the rebuttal window (all referenced by name in replies):

- **Appendix B.5** — comparison with Rabe & Staats (for UuW7's Q2)
- **Appendix E.1** — end-to-end memory reduction for BERT-large and GPT2-small (for uahY)
- **Appendix E.4** — ViT-base on ImageNet, ViT-large with patch 4x4 (for 5Whx)
- **Appendix E.5** — comparison with NVfuser, AOT compiler, TVM (for the common-baselines critique)
- **Appendix E.7** — roofline plot (for 5Whx)
- **Table 8** — speedup with 1–8 GPUs (for UuW7 follow-up)
- **Table 11** — batch-size sensitivity (for UuW7 follow-up)
- **Figure 2 update** — to fix the dropout / masking inconsistency UuW7 caught

That is the surface area the AC's "additional experiments" line is rewarding.

---

## What to extract for our own rebuttals

When working on a new rebuttal, ask:

1. What is the **single existential critique** that, if accepted by the AC, would sink the paper? Reframe it causally or via taste, not via denial.
2. What is the **3-number thesis sentence** for our paper?
3. What **external evidence** can we cite as updates since submission (industry use, integrations, citations, follow-up work, verifications)?
4. What **published counterexamples** can we point at when reviewers ask "why didn't you just do X?"
5. Which reviewer is the Confidence-5 adversary? Optimize their engagement for AC-readability, not score flip.
6. What **specific appendices and tables** will we add during the rebuttal? Each one is a deliverable.
7. What is our **viewpoint-closing sentence** — the line that positions the paper as a research program?
