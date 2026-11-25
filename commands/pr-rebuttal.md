---
description: Investigate PR review comments and give a structured verdict per point. Read-only, no posting.
argument-hint: <pr-url>
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh api:*), Bash(git log:*), Bash(git show:*), Bash(git blame:*), Bash(git diff:*), Read, Grep, Glob, WebFetch, WebSearch
disable-model-invocation: true
---

Investigate the review on this PR and give a verdict on every substantive reviewer comment: $ARGUMENTS

Don't post anything to the PR, edit files, or change git state.

Read the PR, its diff, the reviews, the inline comments and the discussion thread. Use `--paginate` on the `gh api` comment endpoints: they return 30 per page and silently drop the rest. Follow links in the comments one hop.

Check each reviewer's claim against the actual code. A reviewer can be right about the problem and wrong about the fix; say so when that happens.

## Report

### PR summary
2-3 sentences: what the PR does, the reviewers, the review state, and the size.

### Review state
- **<reviewer>**: `APPROVED` / `CHANGES_REQUESTED` / `COMMENTED`, with a one-line take

### Verdict per comment
Number the comments. For each:

#### [N] <reviewer>: <one-line gist>
- **Where:** `path:line` or "general PR comment"
- **Quote:** a short direct quote
- **Verdict:** `AGREE` / `DISAGREE` / `PARTIAL` / `NEEDS-DISCUSSION`
- **Category:** bug / architecture / style / nit / question
- **Reasoning:** what you verified, in 1-3 sentences
- **Action (AGREE/PARTIAL):** what to change, in prose, not code

### Blocking vs non-blocking
- **Must-fix before merge:** [N, ...]
- **Should-fix, not blocking:** [N, ...]
- **Safe to dismiss:** [N: reason]

### Open questions
Judgment calls that need me.

Be direct. If a reviewer is wrong, say why. If the author was sloppy, say that too. This is a second opinion, not diplomacy.
