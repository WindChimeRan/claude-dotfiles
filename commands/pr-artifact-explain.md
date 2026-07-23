---
description: Explain a PR from scratch — no repo, domain, or review-thread knowledge assumed — and publish the explanation as an Artifact.
argument-hint: <pr-url | pr-number | empty for current branch's PR>
allowed-tools: Bash(gh:*), Bash(git log:*), Bash(git show:*), Bash(git diff:*), Bash(git blame:*), Bash(git status:*), Bash(git rev-parse:*), Bash(git ls-files:*), Read, Grep, Glob, WebFetch, WebSearch, Skill, Write, Artifact
---

Explain a GitHub pull request to someone brand new to this repository. Assume the reader knows nothing about the codebase, the domain, or why the change exists, and has not read a single review comment. Deliver the explanation as a self-contained Artifact.

**Target PR:** $ARGUMENTS

## What this command is for

A newcomer opened this PR cold. They don't know the subsystem, the jargon, or the problem it solves. Bring them from zero to "I understand what this changes, why, and how", grounded in the actual code rather than the discussion around it.

## Hard constraints

- **Read-only.** Do not edit, stage, commit, push, or post anything. No `gh pr review/comment/merge/close`, no `gh api` writes (GET only), no git mutations. `Write` is ONLY for the artifact HTML in the scratchpad, never a repository file.
- **No assumed background.** Explain the subsystem the PR touches from scratch. Define every repo-specific term, acronym, and abbreviation the first time it appears. If a newcomer would need to already know it, explain it instead.
- **Ignore the review back-and-forth.** Do NOT fetch or summarize PR reviews, inline review comments, or issue comment threads. Explain the change on its own merits. A linked issue's title and body are allowed as problem context; its comment thread is not.
- **Explain from source, label inference.** Read the actual changed files and enough of their surroundings to explain them, and cite `file:line` for concrete claims. When you infer intent the code does not state outright, mark it as inference. Never present a guess as fact.

## Steps

### 1. Resolve the PR
- URL: parse owner/repo/number. Bare number: current repo. Empty `$ARGUMENTS`: the PR for the current branch (`gh pr view` with no target).
- If it does not resolve to a real PR, stop and say so.

### 2. Fetch (read-only)
Run in parallel:
- `gh pr view <target> --json number,title,body,state,isDraft,author,baseRefName,headRefName,additions,deletions,changedFiles,files,commits,url,labels`
- `gh pr diff <target>`
- If the body links an issue ("Fixes/Closes #N"), fetch only that issue's title and body: `gh issue view N --json number,title,body`. Do not fetch its comments.

Do NOT call the reviews or comments endpoints.

### 3. Understand it from zero
- Identify the subsystem(s) the diff touches. For each meaningful file, Read the file and enough around it (module `__init__`, nearby `README`/docs, docstrings, the definitions the diff calls into) to explain what that area does and how the change fits.
- Trace the key code path the change adds or alters. Establish before-vs-after behavior.
- Collect every repo-specific term you had to learn; those become the glossary.
- Separate load-bearing changes from mechanical ones (renames, formatting, generated files). Do not drown the reader in trivia.

### 4. Build the artifact
1. Invoke the `artifact-design` skill first (required before authoring any artifact).
2. Write a self-contained, theme-aware, responsive HTML file to the scratchpad, then publish it with the `Artifact` tool. Set a `<title>` like `PR #<n>: <short title> — Explained`, a one-sentence `description`, and favicon `📖` (keep it stable across re-runs of the same PR).

Artifact sections, in order:
- **Header** — PR number, title, repo, author, state, +additions/−deletions, link. Metadata as small chips.
- **TL;DR** — one plain-language paragraph: what it does and why it matters.
- **Background you need** — the subsystem from zero: what this part of the codebase is responsible for, and how the moving parts worked before this PR.
- **The problem** — what was missing or wrong (from the linked issue if any, otherwise inferred from the diff and labeled as inference).
- **What changed** — a table of the load-bearing files (`path` · what changed · why); mechanical changes summarized in one line.
- **How it works** — the mechanism, walking the key code path with short snippets from the diff. Add a `mermaid` diagram (flow, or before/after) when it clarifies.
- **Impact & risk** — who is affected, and behavior/compatibility/performance changes and edge cases.
- **How to verify** — tests added or changed and the command to run them; what a reviewer should eyeball.
- **Glossary** — every repo or domain term, one line each.

### 5. Report back
In chat, give a 2-3 sentence summary and the artifact link. The artifact is the deliverable.
