Sync local main with upstream main, then push to origin.

## Steps

1. **Pre-check**: Confirm the current branch is `main`. If not, stop and tell me.
2. **Pre-check**: Confirm the working tree is clean (no uncommitted changes). If not, stop and tell me to commit or stash first.
3. **Fetch**: Run `git fetch upstream main`.
4. **Preview**: Show incoming commits with `git log --oneline main..upstream/main`. If there are no new commits, say so and stop.
5. **Merge**: Run `git merge upstream/main`.
   - **If the merge succeeds**: Run `git push origin main`. Then give a brief summary of what was merged (number of commits, one-line descriptions).
   - **If the merge fails (conflict)**: Immediately run `git merge --abort`. Show which files had conflicts. Do NOT attempt to resolve conflicts automatically — discuss with me first and wait for my instructions.
