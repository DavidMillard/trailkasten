---
name: history-update
description: Update daily history after creating notes. Use at end of note creation (single or batch) to record additions in 35-History/YYYY-MM-DD.md with thematic clustering and narrative prose.
---

# History Update Skill

Update the daily history file after notes, hubs or MOCs have been created.

## When to Use

- After creating atomic note(s)
- After creating hub(s)
- After expanding MOC (if new notes created)
- At end of batch operations

## File Location

`35-History/YYYY-MM-DD.md` where YYYY-MM-DD is today's date.

## File Structure

```markdown
---
type: history
created: YYYY-MM-DD
tags: []
---
# YYYY-MM-DD

> [!tldr] What Happened Today
> **Summary**:: [One sentence naming the ideas that landed — see *The Summary Line* below]

> [!attention] Stats
> Nodes: X | Hubs: X | MOCs: X | Literature: X

---
## [Thematic Cluster Name]

[Narrative paragraph weaving note links into explanatory prose]

## [Another Cluster Name]

[Another narrative paragraph if needed]

---
← [[YYYY-MM-DD]] | [[YYYY-MM-DD]] →
```

## Core Principle: REWRITE, NEVER APPEND

When file exists, REWRITE entire file integrating all notes from today.

**Why**: Appending creates fragmented entries. Rewriting enables thematic synthesis.

## Core Principle: CONTENT, NEVER PROCESS

An entry describes **the ideas that landed**. It never describes the session that produced them.

The user reads the history list to recall *where a topic was worked on* — "oh yes, that is where all the material on agency went." A process account gives them nothing to recognise, because every entry's process is identical; only the ideas differ.

**Never write:**
- "We analysed many papers and brought three into the vault, then clarified one of them"
- "The afternoon turned to a large batch of papers, and the first pair taken from it…"
- "Two notes were created and four existing notes were amended"

**Write instead:** what was established, argued, complicated or conceded. Counts of papers read, notes created and amendments made belong in the Stats callout, never in prose.

Explaining how notes *relate* is content, not process, and remains required.

### The Summary Line

This applies most sharply to the `**Summary**::` line, which is the part scanned when looking back. It must name the day's ideas, not its activity.

- ❌ "Evaluated a large batch of papers and added several notes on AI ethics"
- ✅ "Attention got a mechanism it had been missing, and a second front opened on measurement — what a metric does to the thing it claims to observe once people know they are being counted"

### Cluster by Content, Not by Work Session

Batch boundaries, reading sessions and morning/afternoon splits are process artefacts and must be **invisible** in the entry.

- Papers from different batches converging on one theme are **one cluster**
- A single batch producing two unrelated ideas is **two clusters**
- If a cluster can only be described by when the work happened, it is not a cluster

## Restructuring: Fossilise, Never Re-link

When a note restructuring makes an existing history entry out of date,
**preserve the old entry as a fossil record with a provenance trail**. Never
silently re-link it to the new note names.

**Method:**
1. Add a superseded banner callout at the top of the old entry, linking forward
   to the entry that describes the restructuring.
2. **De-link every note reference in that entry's narrative to bold** — a frozen
   snapshot of what the notes were called at the time.
3. Leave the chronological `← prev | next →` navigation exactly as it was.
4. The new day's entry carries the live links, plus a cluster describing the
   restructuring itself.

**Why.** This gives a full provenance trail: the page as first written, plus a
pointer to what it became. Re-linking destroys the record of how the ideas were
originally named and connected, which is the only thing the old entry uniquely
holds.

Retired notes are deleted only after their salvageable content has been merged
into their replacements.

## Process

1. **Check if file exists**: Use `mcp__obsidian__view` action=file
2. **If exists**: Extract existing note links from cluster sections
3. **Combine**: Existing notes + new notes = complete set for today
4. **Cluster**: Group ALL notes by *idea*, into a small number of thematic clusters — typically 1–4, more only when the day genuinely covered distinct territory
5. **Write narrative**: One paragraph per cluster (max 1 para per 6 notes)
6. **Update stats**: Count by type (note, hub, moc, literature-note)
7. **Write file**: Complete rewrite with all sections
8. **Vault-health check-in**: once the file is written, check whether the health check is overdue and, if so, offer to run it (see *After Writing* below)
9. **Commit-and-push check-in**: after the health step resolves, offer to commit and push the session's work (see *After Writing: Commit and Push* below)

## After Writing: Vault-Health Check-In (side-effect trigger)

Writing history marks the end of a work session — notes, hubs, or MOCs have just landed, which is exactly the moment new orphans, broken references, or a shifted dormancy clock can appear. So this is the vault's chosen trigger for the self-surfacing health check: **no scheduled job — the check rides on activity that has already happened.** This is the side-effect-value principle, and it is why the vault runs no background timer.

**Overdue check (deterministic).** Look at the dated snapshots in `60-Analysis/health-snapshots/`. The most recent filename (`YYYY-MM-DD.json`) is the last run. If that date is more than **7 days** before today — or the directory is empty — the check is overdue. If it is within 7 days, **say nothing about health** and stop; the silence is the point, so this never fires on every history write.

**If overdue, offer once — never auto-run** (Value 1: the user decides):

> Having written today's history, your vault health check is N days out of date. Run a quick check now?

If the user declines, stop — no health run this session.

If the user agrees, run only the **light tier** — the callout refresh, no interpreted-page rewrite, no maturity reconcile:

```
python3 .claude/scripts/vault_health.py --write-callout
```

This archives today's snapshot and sets or clears the `00-Index/History.md` callout in seconds. Then report the outcome from `callout_markdown` in the JSON, in one line:

- **Callout clear** (`callout_markdown` is null): "Vault health checked — all clear, the History callout is clean."
- **Callout raised items**: name them in one line, then offer escalation — "Health check raised N item(s): [one-line summary]. Want to work through them now with `/vault-health`, or leave the callout for later?" Only run the full interactive `/vault-health` (maturity reconcile, interpreted-page rewrite, fix loop) if the user opts in.

The default side-effect stays cheap; the full audit happens only when there is something to act on **and** the user asks for it.

## After Writing: Commit and Push (side-effect trigger)

Writing history *is* the end-of-session marker, so it is the natural commit boundary — if
this vault is version-controlled at all. Many are not, and that is a perfectly good choice.

**Check first, in this order. Say nothing about git unless all three pass.**

1. **Is this a git repository?** `git rev-parse --git-dir`. If not, say nothing. Never
   propose initialising one — that is the user's decision to make unprompted.
2. **Are there changes?** `git status --porcelain`. If the tree is clean, say nothing. The
   silence is the point.
3. **Whose remote is it?** `git remote get-url origin`. See below — this one matters.

### The inherited-remote trap

A vault cloned from a template or a shared repository **carries the original author's
`origin`**. Pushing to it would send the user's private notes to someone else's repository,
and where they happen to have write access it would succeed.

**Never push to a remote the user has not confirmed is theirs.** If `origin` still points at
the repository this vault was cloned from, do not offer to push at all:

> `origin` still points at the repository this vault was cloned from, so pushing would send
> your notes there rather than somewhere of your own. I can commit locally, and you can set
> up your own remote when you want one — `/setup` can remove the inherited one.

Commit locally in that case if the user wants it. Just do not push.

### If all three checks pass

**Offer once — never auto-run** (Value 1: the intention/action boundary is the user's to
cross):

> Today's work isn't committed. Commit it now?

Offering rather than acting is deliberate. Publishing to a remote is outward-facing and
awkward to reverse, and a single confirmation costs one word whilst keeping the decision
human. If the user declines, stop — leave the tree dirty, and do not raise it again this
session.

**If the user agrees:**

1. **Stage selectively.** Exclude `.obsidian/` unless asked — those are application settings,
   often already dirty from ordinary use, and CLAUDE.md puts them off-limits by default.
   Check for anything else present but unrelated to the session's work.
2. **Commit to the current branch.** Do not create a branch for vault work: a knowledge
   vault's history is linear, and a branch strands the notes where the user's sync tooling
   will not see them.
3. **Split along natural seams** — new notes and their backlinks, enrichments, hygiene and
   repairs, the history entry itself — rather than one undifferentiated dump. The commit log
   is part of the vault's intellectual record, so messages say *what changed and why*, in the
   same register as a history entry.
4. **Push only if the remote is the user's**, and only if they asked for it.

**Verify, do not trust the exit code.** Capture stdout and stderr and read them. A piped
`git` command reports the exit status of the last element of the pipe, so `git push … | head`
can report success whilst the push failed. Report the actual ref update line, and confirm
afterwards with `git status -sb`.

**If a network operation fails inside a sandbox**, that means the sandbox setting is wrong,
not that authentication is broken. Retry outside it before concluding push is unavailable.

## Narrative Voice

- **Flowing prose**, not bullet lists
- **Past tense**: "introduced", "explored", "captured"
- **Inline wiki-links**: `[[Note Name]]` woven into sentences
- **Connection language**: Explain how notes relate
- **The vault's spelling convention**, consistently
- **Epistemological stance**: "captured ideas about", "explored frameworks for" (not "established" or "proved")

## Cluster Names

**Good**: "Spatial Hypertext Theory", "What Measurement Does to the Measured", "Where the Labour Actually Went"
**Bad**: "Cluster 1", "Notes Created Today", "Various Topics"
**Also bad — process names**: "Morning Session", "The Scholar Batch", "Papers Ingested Today", "Batch A". A cluster named for when or how the work happened has been grouped by process rather than by idea.

## Navigation Links

- Calculate previous/next dates
- Format: `← [[YYYY-MM-DD]] | [[YYYY-MM-DD]] →`
- First day: `[[YYYY-MM-DD]] →`
- Latest day: `← [[YYYY-MM-DD]]`

## Example Paragraph

```markdown
## Where Automation Should Cut

[[Tedious Friction and Cognitive Friction]] separates the clerical layer of a practice from the judgements inside it, which reframes the design question for an assistant: not how much work to remove, but where. [[Structural Scaffolds Make AI Output Correctable]] takes up what the remaining judgements need in order to be exercisable — a declared position for every generated unit, so one link can be disputed and one note dropped. [[The Human as Exit Condition]] then supplies what granularity alone cannot, since a generative system has no internal stopping point and the terminus is a fact about the person rather than the material.
```

## Brevity Guidelines

- **Max 1 paragraph per 6 notes** (round up)
- **3-5 sentences per paragraph**
- Chronicle what was added, don't teach each concept
- Mention each note once with key contribution

## Efficiency Note

This skill exists because the creating agent already has note content in context. Updating history inline avoids spawning a separate agent that re-reads all notes.
