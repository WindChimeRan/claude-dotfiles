---
description: Investigate PR review comments and give a structured verdict per point. Investigation only — no edits, no posting.
argument-hint: <pr-url>
allowed-tools: Bash(gh:*), Bash(git log:*), Bash(git show:*), Bash(git blame:*), Bash(git diff:*), Bash(git status:*), Bash(git rev-parse:*), Read, Grep, Glob, WebFetch, WebSearch
---

Investigate a GitHub pull request review and produce a structured verdict on each reviewer comment. Investigation-only — no edits, no posting back to the PR.

**PR URL:** $ARGUMENTS

## Hard constraints

- **No file edits.** You cannot Write, Edit, or create files. Enforced by `allowed-tools`.
- **No posting.** Never run `gh pr review`, `gh pr comment`, `gh pr merge`, `gh pr close`, or `gh api ... -X POST/PUT/PATCH/DELETE`. GET only.
- **No git mutations.** Only read-only git inspection (log, show, blame, diff, status, rev-parse). No checkout, commit, push, stash, branch, or merge.
- **Auto mode.** Investigate every substantive comment proactively. Do not ask which ones to dig into — `/discuss` is the follow-up tool for interactive deep-dives.

## Steps

### 1. Fetch everything

Parse `owner`, `repo`, and `number` from the PR URL. If the URL is malformed or not a PR URL, stop and say so.

Run these in parallel:
- `gh pr view <url> --json number,title,body,state,author,baseRefName,headRefName,additions,deletions,files,reviewDecision`
- `gh pr diff <url>`
- `gh api repos/{owner}/{repo}/pulls/{number}/reviews` — review-level feedback with state (APPROVED / CHANGES_REQUESTED / COMMENTED)
- `gh api repos/{owner}/{repo}/pulls/{number}/comments` — **inline line-level comments** (substantive feedback usually lives here)
- `gh api repos/{owner}/{repo}/issues/{number}/comments` — issue-level discussion thread

If any call fails, report the error and stop. Don't guess from partial data.

### 2. Follow references (one hop deep)

Scan all fetched comments for:
- Links to other PRs/issues in the same repo → `gh api` or `gh pr view` them
- Links to external docs, RFCs, specs, library docs → `WebFetch` them
- "As we discussed in X" / "per the thread in Y" → follow X/Y
- References to files or functions not in the diff → Read them
- Mentions of standards ("RFC 7519", "PEP 8", "React docs say...") → `WebFetch` or `WebSearch` to verify

Do not recurse beyond one hop. If a linked thread itself references more threads, summarize them but do not fetch.

### 3. Investigate each comment

For every substantive comment (skip pure reactions like "thanks" or emoji), work out:

1. **Is the reviewer factually right?** Verify claims against the actual code. Grep for "this is used elsewhere" claims. Read the surrounding file for "this breaks Y" claims.
2. **Category**: bug, architectural concern, style preference, nit, or question?
3. **External context**: if the reviewer cites an RFC, standard, or library behavior, verify it.
4. **Alternative fixes**: a reviewer may be right about the problem but wrong about the solution. Note that.

### 4. Produce the report

Output in this exact structure:

---

### PR summary
<2-3 sentences: what the PR does, reviewer(s), overall review state, size (+/- lines)>

### Review state
- **<Reviewer>**: `APPROVED` / `CHANGES_REQUESTED` / `COMMENTED` — <one-line take>

### Verdict per comment

Number comments sequentially. For each:

#### [N] <reviewer>: <one-line gist>
- **Where:** `path/to/file.py:123` or "general PR comment"
- **Quote:** "<short direct quote, ≤25 words>"
- **Verdict:** `AGREE` / `DISAGREE` / `PARTIAL` / `NEEDS-DISCUSSION`
- **Category:** bug / architecture / style / nit / question
- **Reasoning:** <1-3 sentences grounded in what you actually verified>
- **Action (if AGREE/PARTIAL):** <prose description of what to change — NOT code>

### Blocking vs non-blocking
- **Must-fix before merge:** [N, N, N]
- **Should-fix but not blocking:** [N, N]
- **Safe to dismiss:** [N — reason], [N — reason]

### Open questions
<Anything you couldn't decide — judgment calls, missing context, or places where my weigh-in is needed>

### Next step
End with: "Run `/discuss` to dig into any of these points interactively, or address them manually. I will not edit files or post to the PR from this command."

---

## Tone

Be direct. If a reviewer is wrong, say so and explain why. If a reviewer is right and the author was sloppy, say that too. Do not hedge to be polite — this is a second opinion, not diplomacy.
