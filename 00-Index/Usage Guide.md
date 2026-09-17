---
type: index
created: 2026-09-08
tags: [🌲]
---
# Usage Guide

> [!tldr] TLDR
> **Key**:: How this vault is shaped, which command to reach for, and what to do in your first week

Read this once before you start. It is about twelve minutes, and it will save you from the
two mistakes almost everyone makes: writing notes by hand into an empty vault, and setting
the maturity tags yourself.

---

## The shape of the thing

Three layers, and the difference between them is the whole method.

**Atomic notes** (`30-Notes/`) hold one idea each — 200 to 400 words, opening with a
one-line summary. The discipline is the atomicity: a note about two ideas connects to
everything and therefore says nothing. When you find yourself writing "and also", you have
found a second note.

**Hubs** (`20-Hubs/`) gather notes around a persistent concept — *Hypertext*, *Learning*,
*AI Writing*. Hubs organise; they do not argue. A note declares its hub membership in its
`topics:` frontmatter, and the hub's Dataview query collects it automatically. You do not
maintain a list by hand.

**Maps of Content** (`10-MOCs/`) sequence notes into an argument. This is where writing
starts. A MOC is not a table of contents — it is a trail through the material that makes a
case, and the order carries meaning.

The layers are load-bearing rather than decorative. Because every piece of content has a
declared role, the assistant has a grammar to work within: it proposes a note rather than
producing prose, and you can accept, redirect or reject it at the level of a single idea.
That is the difference between reviewable and unreviewable AI output.

---

## What goes where

| Folder | Holds | Filled by |
|---|---|---|
| `00-Index/` | Navigation and foundations | Hand |
| `10-MOCs/` | Narrative trails through the notes | You, curating |
| `20-Hubs/` | Evergreen concept pages | `/create-hub` |
| `30-Notes/` | Atomic notes — the core | `/create-note`, `/ingest-resource` |
| `35-History/` | Daily chronicle | `history-update`, at session end |
| `40-Resources/` | Tidied resource notes: summary, concepts, source preserved | `/ingest-resource` |
| `41-Attachments/` | Images and PDFs embedded in notes | Obsidian |
| `45-Literature/` | One note per academic paper | `/create-literature-note` *(academic tier)* |
| `50-Drafts/` | Blog posts, paper sections, outputs | `/create-draft` |
| `60-Analysis/` | Assessments that draw on the vault | Claude, when asked |
| `80-Fleeting/` | Your inbox to Claude — raw material awaiting ingestion | You, dropping things in |
| `90-Templates/` | Templates for each content type | Hand, rarely |
| `99-Archive/` | Finished and deprecated | You |

Two of these are easy to confuse, and the direction of travel is the thing to hold on to.
**`80-Fleeting/`** is the inbox: raw material you drop in for Claude to work from — an
article, a transcript, a draft to critique. **`40-Resources/`** is downstream of it, holding
the tidied resource note that `/ingest-resource` writes: a summary, the extracted concepts,
and the source preserved underneath.

So you put things *into* fleeting and the vault produces things *into* resources. Claude
reads from fleeting and never writes to it.

---

## The commands

Grouped by what you are actually trying to do.

You rarely need to type them. Claude invokes a command from conversation, so *"I want a note
on X"* runs the same workflow as `/create-note`. The slash form is for when you want to name
the workflow explicitly — and either way the command still proposes, shows its working, and
waits for you.

More to the point: **most of the useful work here is not a command at all**, and the thing
worth learning is not this list but the vocabulary above it — atomic notes, hubs, MOCs.
Those three words are what make the conversation precise. *"That wants to be its own atomic
note"*, *"is this a hub or a MOC?"*, *"what would a MOC on this draw on?"* — each is
specific enough to act on, and none is a command. The commands are the recurring moves worth
doing consistently. They are not the interface.

### Getting material in

**`/ingest-resource [path]`** — the workhorse, and the one to start with. Point it at
something you have dropped in `80-Fleeting/`: a transcript, an article, a conversation, a
talk. It reads the source (delegating to a subagent if it is long), writes a tidied resource
note into `40-Resources/`, proposes a cluster of atomic notes, shows you what it found and
what already overlaps, and creates only what you approve.

**`/create-note <subject>`** — for an idea that arrived without a source. Less used than you
would expect: most notes come out of ingestion, because most ideas come from reading.

**`/create-hub <concept>`** — when you notice a cluster of notes wanting a home. Usually
after the notes exist, not before.

### Working with the literature *(academic tier)*

**`/create-literature-note <citation-key>`** pulls a paper from Zotero, summarises it,
writes a structured literature note, and spawns atomic notes for its concepts.
**`/find-papers`** searches your library for work relevant to a vault concept.
**`/find-citations`** matches Zotero entries to `\cite{...}` placeholders in a draft.
**`/evaluate-papers`** triages incoming papers for whether they earn a note at all.

These need Zotero. Install them with `/setup` if you want them.

### Getting writing out

**`/create-moc <name>`** builds a Map of Content. You say roughly how the argument runs —
"start with X, then why that bears on Y, then the consequences for Z" — and it finds the
notes that fill that shape, writes a skeleton you can read and rearrange in Obsidian, and
expands it into narrative when you are happy. Run it again on an existing MOC to expand it.
The sequence stays yours throughout; that is the whole point of the command.

**`/create-draft <note-or-moc>`** turns curated material into a draft in `50-Drafts/`,
with the register following the destination you name. It will not work from a bare topic —
if there is no curated argument, it says so and sends you to `/create-moc` first.

There is a sequencing rule worth knowing: **build the MOC first, then write from it.** A
tone problem in a draft is usually a structure problem wearing a disguise, and it is far
easier to fix the argument in a neutral MOC than to un-polish bad prose.

### Keeping it honest

**`/vault-health`** audits structure: orphans, broken links, thin notes, missing metadata,
hub balance, and how much of each territory has actually been drawn on. It offers fixes and
waits — it does not edit on its own initiative.

---

## Maturity: 🌱 🌿 🌲

Every note carries one of three tags. They mean something specific, and it is **not** how
good or how finished the note is.

| | | |
|---|---|---|
| 🌱 | **Untested** | Never drawn on by a MOC, draft or analysis |
| 🌿 | **Drawn on** | Used by one or two |
| 🌲 | **Load-bearing** | Used by three or more |

Maturity records **use**, not quality or connectedness. A beautifully written note that no
piece of work has ever leaned on is 🌱, and that is correct — it is untested, in the sense
that nothing has yet depended on it being right.

**Never set these by hand.** They are a cache, computed from the link graph by
`.claude/scripts/vault_maturity.py`, and any value you type will be overwritten on the next
reconcile. The only exception is 🌱 at birth.

The practical use is diagnostic. A hub with thirty notes and two ever used is a territory
you are collecting rather than thinking with — which might mean it is a reserve awaiting the
right project, or might mean you are hoarding. The heat map on [[Vault Health]] shows you
which.

---

## Conventions you will bump into

**Notes are reviewed as they are created, not afterwards.** Every command proposes and
waits. That will occasionally feel slow, and it is deliberate: deciding whether a concept is
real and whether it belongs is the thinking, and it is the reason the vault is worth having.
If an assistant ever offers to build first and let you review later, decline — notes that
arrive unreviewed are never revisited, and a vault filled that way looks exactly like one
that was not.

**Wiki-links, always.** `[[Note Name]]`, `[[Note Name|display text]]`, `![[Embed]]` — never
markdown links for internal navigation. Obsidian tracks them bidirectionally and the whole
graph depends on it.

**Tags mean maturity and nothing else.** Concepts are expressed through hub membership, not
tags. If you start tagging notes with topics you will end up with two competing
organisational schemes and no idea which is authoritative.

**The `#human` tag protects your words.** Any paragraph or bullet containing `#human` is
treated as untouchable: Claude will not modify it without asking, preserves it verbatim when
editing around it, and weights it more heavily when reasoning. Use it for anything you wrote
yourself that matters — your own insight in a note the assistant otherwise drafted.

**A tentative epistemological register.** The vault captures perspectives rather than
establishing truths. "Offers a lens", "proposes that", "can be understood as" — not "is".
Definitive language is reserved for empirical findings, and for accurately reporting what a
source claims. This is the one writing convention that is doing real work: it keeps ideas
held as provisional, which is what makes a knowledge base a space for thinking rather than a
store of conclusions.

---

## Your first week

**Day one: feed it.** Find two or three years of your own writing — blog posts, papers,
talks, reports, long emails you were pleased with. Drop them in `80-Fleeting/` and run
`/ingest-resource` on each. Approve the notes that look right; reject the ones that do not.
Expect to reject a lot at first, and expect that to improve as the vault fills.

**Do not start by writing notes by hand.** An empty Zettelkasten has nothing to connect to.
Every interesting behaviour here — connection proposals, duplicate detection, sibling
nudges — is a function of having material, and below about fifty notes the system will seem
less useful than it is.

**Day three or four: make a hub.** Once you can see clusters, run `/create-hub` on two or
three of them and let the notes attach.

**End of the first week: build a MOC.** Pick something you actually want to write about,
curate the notes that bear on it, and put them in an order that makes a case. This is the
step that is explicitly yours — the MOC is your synthesis, not the assistant's. Then run
`/create-moc` and see whether the argument holds up as prose.

By then the vault will have started to feel like yours rather than like someone's template,
and the maturity tags will have begun to move.

---

## Where to go deeper

- [[Values Statement]] — the position this tooling was built on
- [[Vault Rationale]] — why the tools are the way they are; add to it when you change them
- [[Research Programme]] — the persistent questions, once you can see what yours are
- [[Vault Health]] — structural audit and the territory heat map
- [[History]] — the daily chronicle

The method itself lives in `.claude/skills/zettelkasten-methods/`, which is worth reading if
you intend to modify the commands. Everything the assistant knows about this vault is in
`CLAUDE.md` and those skill files — there is no hidden configuration.
