---
description: Fast-forward local main to the project's main and push it to my fork
disable-model-invocation: true
---
Sync this repo's main with the project, then push it to my fork.

- `upstream` is the project and `origin` is my fork. If the remotes don't look like that, stop and show me `git remote -v`.
- Fast-forward only. If local main has its own commits or the tree is dirty, stop and tell me.
- Push main to my fork only, never to the project.
- Then list the incoming commits, one line each.
