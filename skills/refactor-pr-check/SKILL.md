---
name: refactor-pr-check
description: "Checklist for preparing or reviewing a refactoring PR — a change that moves, extracts, renames, or reorganizes code with behavior preserved. Use when you have written or are about to open a refactor/cleanup/extract/move PR, or are reviewing one, and want it faithful (behavior unchanged), minimal (no needless new files or config), reviewable (git renders moves as renames), verified (actually run), and described by risk. Triggers on 'refactor', 'extract', 'move X to Y', 'rename', 'split this file', 'pure move', 'reorganize', 'pull out shared', or preparing a PR that is mostly relocation. Covers isolating the one real change, keeping moved code byte-identical, earning the git rename badge, choosing the right home (library vs tooling), reverting needless config, running one real end-to-end path, and a risk-first description."
---

# Refactor PR Check

A refactoring PR moves, extracts, renames, or reorganizes code with behavior preserved. Its whole value is being *obviously* faithful and small. These checks make it so. Run them before requesting review, and when reviewing someone else's.

Commands assume git plus a `make quality`-style gate; adapt to the repo. Set `BASE` to the merge target (`main`, `upstream/main`).

## 1. Isolate the one real change

A refactor is "everything is a move **except** ___." Name that one change, or "none." Then read the whole diff and confirm every other hunk is a move, an import update, or a lint-forced edit.

```
git diff $BASE...HEAD
```

A hunk that changes behavior and is not the named change is scope creep — split it out. Lint-forced edits that ride along (`assert`→`raise` outside test dirs, magic-value constants) get named in the PR body, never left silent.

## 2. Keep moved code byte-identical

Do not let your own prose leak into relocated code. Bodies and docstrings of moved functions must match the base exactly. Write new docstrings only for new or changed code, and be able to prove which is which.

```
python3 - <<'PY'
import ast, subprocess
def ds(src):
    t = ast.parse(src); out = {}
    if ast.get_docstring(t): out["<module>"] = ast.get_docstring(t)
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(n):
            out[n.name] = ast.get_docstring(n)
    return out
base = ds(subprocess.check_output(["git", "show", "BASE:path/old.py"], text=True))
head = ds(open("path/new.py").read())
for k, v in head.items():
    print(k, "identical" if base.get(k) == v else "I WROTE / CHANGED")
PY
```

## 3. Put moved code in the right home

Before choosing a destination for shared code, ask:

- Does this location auto-publish as public API — a docs autonav over the package, an exported top-level name? A dev/CI helper does not belong there.
- Can it run from an installed package? Code that shells out to repo-relative paths cannot live in the shipped library.
- Match the repo's own split: importable library for installed users, versus CLI and dev tooling.

Smell: a module docstring that *apologizes* for its location ("requires a source checkout, not a wheel") means it is in the wrong place.

## 4. Make git render the move as a rename

A reviewer skims a rename and re-reads an add. So a move must render as a rename.

git detects a rename only when the source path is **deleted** and a **>50%-similar** file is added. A *partial* extraction from a file that survives can never render as a rename — the survivor is "modified," not "deleted." To earn the badge, delete the source entirely and relocate its smaller remainder elsewhere.

Measure before pushing, then confirm on GitHub:

```
git diff -M --summary $BASE HEAD    # want: rename old => new (NN%)
gh api repos/OWNER/REPO/pulls/N/files \
  --jq '.[]|select(.status=="renamed")|"\(.previous_filename) -> \(.filename)"'
```

One source renames to only one target (the closest match). The relocated remainder still shows as additions — unavoidable; note in the PR that it is mostly moved.

## 5. Cut needless new files and config

Every new file or config line is friction and must earn its place. For each one you added to "make it work," revert it and run the gate:

```
git checkout $BASE -- pyproject.toml   # or delete the new __init__.py, etc.
make quality                           # still green? it was never needed
```

Before adding config to make an import resolve, check whether the base already does the same thing without it. Aim for zero config changes in a move.

## 6. Actually run it

Collect-only proves imports resolve. It does not prove the moved code runs. Execute one real end-to-end path that exercises the moved *and* changed code, and confirm from the logs it ran from the new location.

Do not write "can't run, needs hardware" when the environment has it. If you genuinely can't, state exactly what you ran and what you didn't — do not imply more.

## 7. Describe the PR by risk, not by file

- Lead with the one real change from §1 — the reason for the PR. Everything else "is a move."
- Organize by what could break, not file by file. Short sentences, plain words.
- Put code names in the section that routes review ("What changed"); keep them out of orienting prose. Drop file:line and similarity percentages from the text.
- For a redundancy or follow-up, show one short before/after example, not an enumeration.
- A "separate PR" note must prove nothing is broken (it still collects), never hide breakage. Distinguish "redundant but working" from "broken."

## 8. Hygiene

- Gate green: format, lint, types.
- Stage named paths — never `git add -A` with untracked scratch files in the tree.
- Sign off if the repo requires DCO (`git commit -s`).
- Keep a pure move to one clean commit; amend rather than pile fixups while it is an unreviewed draft.
