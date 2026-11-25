---
name: refactor-pr-check
description: Checklist for preparing or reviewing a refactor PR, a move, extraction, rename or reorganization that must preserve behavior.
disable-model-invocation: true
---

# Refactor PR check

A refactor PR is worth its review cost only when it is obviously faithful and small.

1. **Isolate the one real change.** A refactor is "everything is a move except ___". Name that change, or "none", and lead the PR description with it. Every other hunk must be a move, an import update or a lint-forced edit. Name lint-forced edits in the PR body; split out anything else.
2. **Keep moved code byte-identical.** Bodies and docstrings of moved functions match the base exactly. New prose goes only on new or changed code.
3. **Put it in the right home.** Dev and CI helpers don't belong where a docs autonav or a top-level export publishes them as API. Code that shells out to repo-relative paths can't live in the shipped library. A module docstring that apologizes for its location means it is in the wrong place.
4. **Earn the rename badge.** git detects a rename only when the source path is deleted and the new file is more than 50% similar. A partial extraction from a file that survives never renders as a rename: to get the badge, delete the source and relocate its smaller remainder. One source renames to only one target. Check with `git diff -M --summary $BASE HEAD`.
5. **Cut needless new files and config.** Revert each one you added to make it work and rerun the checks. If they still pass, it was never needed. Aim for zero config changes in a move.
6. **Run one real path.** Collect-only proves imports resolve, not that moved code runs. Exercise the moved and changed code end to end and confirm it ran from the new location.
