---
description: Build a Map of Content from a stated argument shape, or expand an existing skeleton into narrative
argument-hint: "<MOC name or topic>"
skills: note-creation, vault-writing-style, zettelkasten-methods, obsidian-patterns, user-interaction-patterns, history-update
---

# Create MOC

Build a Map of Content: a narrative trail that sequences notes into an argument.

This command covers the whole arc — from a topic and a rough shape, through a skeleton you
can read and rearrange in Obsidian, to a full narrative. Run it once to build the skeleton
and again to expand it; it detects which it is looking at.

## Critical Rules

1. **The argument is the user's.** Ask for the shape; do not invent one and present it as
   theirs. Claude finds and arranges the material *inside* a spine the user supplies.
2. **Name shape drift out loud.** Reorganisations that *fill* the user's movements need no
   ceremony. A reorganisation that **replaces** them — merges two movements, re-sequences
   them, or proposes a different organising principle — must be flagged as what it is
   before it is adopted:

   > This changes your shape rather than filling it. You said state → organisational →
   > individual; this reorganises around two mirrored challenges instead. That may well be
   > better, but it would make the spine mine rather than yours. Do you want it?

   Consent gathered one small step at a time is not the same as owning the argument. Drift
   is gradual by nature, so the checkpoint has to be explicit.
3. **Always re-read the file from disk** before acting on an existing MOC. The user edits
   and reorders skeletons in Obsidian between sessions — the version on disk is
   authoritative, never Claude's memory of what it wrote.
4. **Wait for approval** before writing anything, at every stage.
5. **Preserve `#human` content unchanged.**

## Step 0: Determine the state

Look for `10-MOCs/<name>.md`.

| State | What to do |
|---|---|
| No file | **Path A** — build a skeleton (Steps 1–5) |
| Exists, `status: draft` | **Path B** — re-read it, then iterate or expand (Steps 6–7) |
| Exists, `status: active` and already has narrative | Ask: expand further, restructure, or leave alone |

Say which path you are on before proceeding, so the user can redirect.

---

# Path A — Building the skeleton

## Step 1: Understand the topic

Load `user-interaction-patterns` before this step — it owns the approval flows and the
reciprocal-challenge pattern this command leans on throughout.

A short conversation, not an interrogation. Establish:

- **What the MOC is about** — the territory it covers
- **What it is for** — a paper, a talk, a blog post, or working something out
- **What is already known about its shape** — see Step 2

If the user opened with a full brief, do not re-ask. Move on.

### Offer a round of reaction first

Some topics need a beat before they need a shape — particularly territory the user is still
finding their footing in, where the point of building a MOC is to work out what they think
rather than to record what they already do.

Before asking for the shape, offer that explicitly:

> Do you want to talk around this first? I can pull up what the vault already holds and we
> can react to it — no structure yet — or if you already know roughly how the argument runs,
> tell me and I will go and find the notes.

If the user takes it, stay unstructured: surface what the territory contains, say what
surprises you about it, and let them think aloud. **Do not quietly start proposing a shape
during this round** — the point is that no shape is being committed to yet. When something
firms up, say so and move to Step 2.

If the user already knows what they want to argue, skip straight to Step 2. Do not impose
a discussion round on someone who arrived with a thesis.

## Step 2: Ask for the argument's shape

**This is the step that makes the MOC theirs.** Ask how they want the argument to run, in
their own words — something like:

> How do you want the argument to go? A rough sequence is enough — "start with X, then why
> that bears on Y, then the consequences for Z". I will find the notes and fit them to it.

Accept whatever granularity comes back. Three clauses is plenty.

**If the user has no shape yet**, offer to propose one — but mark it plainly as a proposal
to be corrected, not a recommendation:

> I can suggest a shape from what is in the vault, but treat it as a first guess to argue
> with rather than a plan. The sequence is the part worth owning.

## Step 3: Find candidate notes

Follow `obsidian-patterns` for efficient search. Work outward from the shape the user gave:

1. `mcp__smart-connections__get_similar_notes` on the topic and on each movement of the
   stated shape (threshold 0.4, limit 15)
2. `mcp__obsidian__vault` search for terms the user used
3. `mcp__obsidian__graph` neighbours on any notes the user named directly
4. Check existing hubs for territory that matches

Do not read candidate notes in full. Triage on snippets and fragments; read only what you
must to judge fit.

## Step 4: Map candidates onto the shape

Present the candidates **grouped under the user's own movements**, using their words as the
section headings. For each note, one line on **how it bears on this argument** — not what
the note is about in general.

```
You said: start with what tools make thinkable → why that makes interface design
epistemological → consequences for AI writing tools.

**Start: what tools make thinkable**
- [[Note A]] — supplies the mechanism; the strongest opening
- [[Note B]] — the counter-case, useful if you want the tension early

**Why that makes interface design epistemological**
- [[Note C]] — does the actual work of this move
- [[Note D]] — adjacent; may be one step sideways

**Consequences for AI writing tools**
- [[Note E]] — the applied case
- (thin here — see gaps below)

**Doesn't fit your shape, but sits close:** [[Note F]], [[Note G]]
**Gaps:** the second movement leans on "epistemic framing", which has no note
```

### Cap what you present

**No more than five or six notes per movement.** Pruning is Claude's job at this stage, not
the user's — a movement with seventeen candidates under it is not a shortlist, it is the
search results, and handing that over transfers the work rather than doing it.

Where a movement has more, choose the strongest and hold the rest back as a named overflow:

> Movement 3 has a deeper pool — 11 more notes I have not listed, mostly on platform
> governance and data rights. Say the word and I will show them.

Say plainly where the argument is **thin**, too. A movement with one supporting note is
worth flagging before it becomes a paragraph with nothing under it.

Ask the user to select, drop, add and rearrange. Iterate here until they are content.

## Step 5: Write the skeleton

**Size gate — check before writing.** If the selection runs past roughly fifteen notes,
**make the cut yourself and present it**. Do not report the overage and ask where to cut:
capping each movement and then handing over an over-budget total transfers exactly the work
the cap exists to absorb.

> That came to 26 notes, which reads as a catalogue rather than an argument. Here is my cut
> to 15 — argue with it.
>
> **Movement 1** — keeping [[A]], [[B]]; dropping **C** (restates B) and **D** (belongs in
> Movement 3 if anywhere)
> **Movement 2** — keeping [[E]], [[F]], [[G]]; dropping **H** (the weakest link in a
> movement that is already the strongest)
> …

Say what you dropped and why, in one clause each. A cut you can argue with is a decision;
a list you have to prune is homework. A skeleton written too large gets rejected on sight,
and rewriting it costs more than pruning it did.

Write `10-MOCs/<Name>.md` from `90-Templates/Template - MOC.md` with `status: draft`.

**The skeleton exists so the user can re-familiarise themselves by following the links.**
Its annotations are therefore load-bearing, and must say how each note bears on *this*
argument. A summary of the note is useless here — they can read the note.

Include:
- Frontmatter: `type: moc`, `status: draft`, `created`, `tags: [🌱]`, `used-by: 0`, `topics`
- **Current Focus** — one or two lines on what this MOC is for
- **Narrative Overview** — the user's stated shape as `###` subsections, each holding its
  selected notes as a list with the one-line "how it bears on this" annotation
- **Suggestions for Expanding** — the gaps and near-misses from Step 4

**Do not wiki-link notes that were set aside.** `vault_maturity.py` counts wiki-links
anywhere in a consumer file, so a set-aside note named as `[[Note]]` in the Suggestions
section graduates 🌱→🌿 as though the MOC drew on it. Name them in **bold** instead, the same
convention used for fossilised history entries. Only notes the argument actually uses get
links.

Then hand back explicitly:

> Skeleton written to `10-MOCs/<Name>.md` with `status: draft`.
>
> Worth reading it in Obsidian and following the links — that is what the skeleton is for.
> Reorder or rewrite it there if you want; I will read whatever is on disk next time.
>
> When you are happy with the shape, run `/create-moc <Name>` again and I will expand it
> into narrative. Or tell me what to change and we can iterate here.

**Stop. Do not expand in the same breath.**

**Do not offer a history entry here.** A skeleton is a work in progress, not a completed
operation; CLAUDE.md's history prompt applies at the end of Step 10, on the expansion path
only. Offering it at every stage trains the user to ignore it.

---

# Path B — Iterating and expanding

## Step 6: Re-read and offer

**Re-read the file from disk first.** The user may have reordered sections, rewritten
annotations, added or removed notes, or added `#human` passages. Report what changed since
the skeleton was written, briefly — it confirms you are working from their version.

Then resolve every wiki-link in the file:

- **Resolved** — the note exists
- **Unresolved** — a placeholder for a note that does not exist yet (see Step 6.5)

Offer:

> The skeleton has N notes across M movements. I can expand it into full narrative now, or
> we can keep working on the shape. Which?

## Step 6.5: Missing notes

If the argument leans on concepts with no note, name them and offer to write them **now**,
before expanding:

> Two movements lean on concepts the vault has no note for: "epistemic framing" and
> "representational commitment". Shall I draft those as atomic notes first? The MOC will
> draw on them, so they are worth having as notes rather than as paragraphs.

If accepted, follow the `note-creation` skill (batch mode, connection tiers, backlinks) and
then return to the MOC and link them in. Keep this a detour, not a takeover: create what the
argument needs and come back.

## Step 7: Expand into narrative

**Lead with provenance.** Before writing, report what the argument stands on:

> Building on N notes: X 🌲 load-bearing, Y 🌿 drawn on, Z 🌱 untested — [[Note A]],
> [[Note B]]. Untested notes have never been exercised by higher-level work; worth
> verifying their claims as I draw on them.

Then write the narrative, following `vault-writing-style`:

- Prose that **explains how the notes relate**, not a list with sentences around it
- The user's stated movements remain the structure; do not silently re-sequence them
- Wiki-links woven inline, not collected at the end
- Tentative register with attribution — this captures a perspective, it does not settle a question
- **`#human` passages preserved exactly**
- Keep the **Notes in This Narrative** list in step with the prose

Set `status: active`.

## Step 8: Reconcile maturity

```bash
python3 .claude/scripts/vault_maturity.py --write
```

A MOC is a consumer: notes it draws on may graduate 🌱→🌿 or 🌿→🌲. Report any that did.

## Step 9: Research Programme reflection

Ask the user — never decide alone — whether this MOC fits an existing programme on
`00-Index/Research Programme.md`, extends one, or implies a new one. The page is capped at
roughly twelve, so a new programme forces the question of what it displaces. Apply only what
they choose.

**If the question goes unanswered, keep it open.** A user who moves straight on to another
command has not declined — they have been distracted. Carry it into the Step 10 report as an
outstanding item, and raise it once more at the end of the session rather than letting it
evaporate. Asking and then silently dropping the question is worse than not asking.

## Step 10: Report

```
## MOC Expanded: [Name]

**Location**: `10-MOCs/[Name].md` — status: draft → active
**Structure**: [N] movements, [M] notes — count the wiki-links in the written file rather
than estimating; this report is often the user's only summary of what went to disk
**Provenance**: X 🌲 · Y 🌿 · Z 🌱

### Notes Created (if any)
| Note | Connections |
|------|-------------|

### Maturity Graduations
- [[Note]] — 🌱→🌿 (this MOC now draws on it)

### Gaps Still Open
- [Anything the argument leans on that has no note]

### Research Programme
- [What the user chose, or "no change"]
```

Then offer the history entry (`history-update` skill) if notes were created.

---

## Guidelines

- `vault-writing-style` — tentative language with attribution, and the spelling convention
- `zettelkasten-methods` — template structure and conventions
- `note-creation` — connection limits, backlink rules, maturity model
- Argumentative MOCs are **curated snapshots**: selective by design. A new related note does
  not oblige an update.

## Example Usage

```
/create-moc Intentional Friction in Experience Design
/create-moc "The Author Function"
/create-moc Representational Geometry of Knowledge Tools   # existing skeleton → expands
```
