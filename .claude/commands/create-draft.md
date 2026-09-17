---
description: Turn a note or MOC into an external-facing draft, with provenance reported first
argument-hint: "<note or MOC name>"
skills: draft-creation, vault-writing-style
---

# Create Draft

Turn curated vault material into a piece of writing for somewhere else — a blog post, a
paper section, a talk, a report.

This is the command with the most obvious failure mode in the vault. Every other command
produces something reviewable one idea at a time; this one produces continuous prose, which
can only be accepted or rejected wholesale. The guardrails below are what keep it from
becoming a slop generator, and they are not optional.

## Critical Rules

1. **Refuse a bare topic.** This command takes a note or a MOC. If there is no curated
   source, there is no argument yet — say so and stop.
2. **Report provenance before writing.** The user sees what the argument stands on.
3. **Ask, never invent.** Biography, anecdotes, settings, numbers, named people — if a
   concrete detail would strengthen the piece and you do not have it, ask.
4. **Say what this is.** The output is a first draft expecting substantial editing, and the
   report says so.
5. **No wiki-links in the Draft Text.** It must paste cleanly into an external platform.

---

## Step 1: Resolve the source

Find the named note or MOC. Then check what kind of thing it is.

| Source | Response |
|---|---|
| A MOC | The best case. The argument is already curated and sequenced. |
| An atomic note | Workable for a short piece. Say that a MOC would give a stronger spine if the piece is long. |
| A bare topic, or nothing found | **Stop.** See below. |

**If given a topic rather than a source:**

> I write from curated material rather than from a topic — otherwise the argument would be
> mine rather than yours, which is the thing this vault exists to avoid.
>
> Options: point me at an existing note or MOC, or run `/create-moc <topic>` first to build
> the argument, and then come back. If you have material in `80-Fleeting/`, ingesting it
> first would give us something to draw on.

Do not negotiate past this. It is the rule that makes the rest defensible.

## Step 2: Read the source and its notes

**Load both skills now**, explicitly: `draft-creation` for file structure and the reading
strategy, `vault-writing-style` for language. A skill named in frontmatter but never invoked
contributes nothing, so only two are declared — a draft is not a note, so the Zettelkasten
conventions do not govern it, and this command spells out its own approval gates rather than
leaning on the interaction-patterns skill for them.

Follow `draft-creation`'s reading strategy. Read the source in full; read the notes it
draws on selectively — enough to represent them accurately, not the whole territory.

## Step 3: Provenance and readiness

**Always report provenance:**

> Building on 9 notes: 2 🌲 load-bearing, 3 🌿 drawn on, 4 🌱 untested — [[Note A]],
> [[Note B]], [[Note C]], [[Note D]]. Untested notes have never been exercised by
> higher-level work, so I will verify their claims rather than assume them.

**Discount recent graduations.** Maturity records use, and a MOC written an hour ago counts
as use — so a source built from a fresh MOC will report a flattering mix. Check the
graduation dates and say so when it applies:

> That flatters it: six of those nine are 🌿 only because this MOC drew on them today. In
> practice the argument rests on 3 notes with independent use behind them.

Maturity is a record of use, never of endorsement. A 🌲 note is one that other work has
leaned on, which is evidence it is useful — not evidence it is right.

**Then flag readiness, maximum two concerns**, from:

- **Thin foundations** — the argument rests mainly on 🌱 untested notes
- **Conceptual gaps** — a load-bearing step has no note behind it
- **Single-source dependence** — most of the argument traces to one paper or conversation

Each concern gets an actionable alternative, not just a warning.

Two further concerns — **scope mismatch against the target length** and **no voice
material** — cannot be judged until Step 4 has been answered. Raise those there, not here.

## Step 4: Ask about destination and register

One message, then wait:

1. **Where is this going?** A blog, a journal, a talk, a newsletter, an internal report.
   Register follows destination.
2. **Who reads it?** Specialists, a mixed audience, students, a funder.
3. **How long?**
4. **What prompted it?** A conversation, an argument you want to make, a deadline. This
   often supplies the opening better than the notes do.
5. **Is there source material with your voice in it** — a transcript, a fleeting note, an
   email where you already said this? Voice should come from there, not from note-prose.

The last two matter most. Notes are written in a hedged, tentative register appropriate to
a knowledge base and wrong for almost any external piece. Drafting from note-prose alone is
the single most reliable route to something that reads as machine-written.

**Once answered, complete the readiness check** with the two concerns that needed these
answers: does the material actually fill the stated length (or badly overflow it), and is
there any source in the user's own voice to draw on? If there is none, say so plainly —
the draft will read as machine-written and no amount of craft in Step 6 will fix it.

## Step 5: Structural preview

Present the shape before writing a word:

```
**Destination**: [where] · **Register**: [what] · **Length**: ~[N] words

**Opening**: [how it starts, and why — from the prompt, not from the notes]

1. [Section] (~[N] words) — [what it establishes] — drawing on [[Note]], [[Note]]
2. [Section] (~[N] words) — [what it establishes] — drawing on [[Note]]
...

**Not included**: [material in the source deliberately left out, and why]

[IF CONCERNS] **Readiness**: [concern] → [alternative]

Proceed, adjust, or address the concern first?
```

**Wait for explicit approval.**

## Step 6: Write

Follow `draft-creation` for file structure and `vault-writing-style` for language. Then:

### Voice

- **Logic from the notes; voice from the source material** — the transcript, the fleeting
  note, the user's own phrasings. Never voice an essay off hedged note-prose.
- **Ask rather than invent.** Never manufacture a setting, an audience, an anecdote or a
  credential. If the argument leans on lived authority, ask for the real detail or leave an
  obvious hook for the user to fill. An invented specific is the most expensive kind of
  error here: it is confident, plausible, and wrong.
- **No unverifiable specifics.** Named people, dates, mechanisms and technique names only
  where the user can vouch for them. When in doubt, generalise or cut.
- **Name concepts and their tradition** where the source notes theorise them. Keep the named
  concept and its attribution; drop the notes' hedging.

### Craft

- **Cut throat-clearing.** Delete sentences whose only job is to announce the next move.
  Make the move.
- **Concrete over abstract.** Prefer an image or a number to a metaphysical formulation.
- **Suspect the clever sentence.** Sweeping sign-offs and aphorisms read as performed.
- **Dissolve metaphors imported from the notes.** A structuring metaphor lifted from
  analytical prose reads as seminar language inside an essay.
- **Do not over-explain the takeaway.** Trust the reader.
- **Gloss jargon** briefly for a mixed audience.

### Avoiding the obvious tells

- Do not open successive paragraphs with "This [noun] represents/proves/matters"
- Vary sentence structure; break perfect parallelism in lists
- Cut hedging ("increasingly", "perhaps we need", "one might say")
- Vary transitions beyond "Yet", "However", "Moreover"
- Allow rough edges — asides, abrupt shifts, an unresolved tension

### Format

**No wiki-links in the Draft Text section.** Italicise titles, use plain text for names, and
full external URLs for online sources. The surrounding Metadata and Notes sections may use
wiki-links freely.

## Step 7: Write the file

`50-Drafts/<year>/<Month>/<Title>.md`, following `draft-creation` structure: frontmatter,
Metadata (purpose, audience, length, source notes as wiki-links), Draft Text, Notes and
Revisions.

## Step 8: Reconcile maturity

```bash
python3 .claude/scripts/vault_maturity.py --write
```

A draft is a consumer. Report any notes that graduated.

## Step 9: Report

```
## Draft Created: [Title]

**Location**: `50-Drafts/[year]/[Month]/[Title].md`
**Destination**: [where] · **Length**: [N] words
**Provenance**: X 🌲 · Y 🌿 · Z 🌱

### Drawn on
[[Note]], [[Note]], [[Note]]

### Left out
- [What was in the source but not used, and why]

### Needs you
- [Any place a real detail was asked for and not supplied]
- [Any claim resting on an untested note worth checking]

### Maturity graduations
- [[Note]] — 🌱→🌿

---
**This is a first draft.** It expects substantial editing — the voice especially. Prose is
the one thing this vault cannot hand you finished.
```

## Guidelines

- The MOC is where the argument gets made; this command only renders it. If the draft feels
  structurally wrong, fix the MOC rather than editing the prose — a tone problem is usually
  a structure problem wearing a disguise.
- Offer a history entry only if notes were created.

## Example Usage

```
/create-draft The Argument for Hypertextual AI Interfaces
/create-draft "Intentional Friction in Experience Design"
```
