---
type: index
created: 2026-09-08
tags: []
---
# History

A chronicle of this vault's evolution. Each entry is **intellectual history, not a task
log**: flowing prose that clusters the day's notes thematically and explains what territory
they establish.

Entries are written by the `history-update` skill, usually offered at the end of a session
in which notes were created. Notes link back to the entry for the day they were made, so
you can always see a note among its siblings.

<!-- vault-health:callout:start -->
<!-- vault-health:callout:end -->

*The space above is where `/vault-health` writes its attention callout. It is script-owned
and regenerated on every run — fix the cause rather than deleting the callout.*

## Recent History (last 50 update days)

```dataview
LIST Summary
FROM "35-History"
WHERE type = "history"
SORT file.name DESC
LIMIT 50
```
