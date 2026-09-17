---
type: index
created: 2026-09-08
tags: [🌱]
---
# Vault Rationale

> [!tldr] TLDR
> **Key**:: An audit trail of changes to the vault's own tooling, and the reasoning behind them

## Purpose

[[History]] chronicles how the *knowledge* grew. This page chronicles how the *tools* did.

When you change a command, a skill or a convention — particularly on [[Values Statement]]
grounds — record it here. The point is not bureaucracy. It is that six months later you
will want to know why `/create-note` asks a question it did not used to ask, and the commit
message will not tell you.

This is also the vault being honest about itself. A system that claims transparency as a
value and keeps no record of its own modification is not practising what it states.

## Why keep this at all

Three arguments, in rough order of how often they pay off:

1. **Decisions decay into folklore.** Without a record, a rule survives as "we do it this
   way" long after the reason has stopped applying. Written reasoning can be re-examined;
   folklore can only be obeyed or broken.
2. **It makes reversal cheap.** Knowing what a change was *for* tells you whether undoing it
   costs anything.
3. **It surfaces drift.** Reading a year of entries shows you what you actually value, as
   opposed to what the Values Statement says you do. Where those diverge, one of them needs
   editing.

## Entry format

```markdown
### YYYY-MM-DD — <Short title of the change>

**What changed:** The concrete edit. Name the files.

**Why:** What prompted it — a failure, a repeated correction, a value gap you noticed.
Be specific about the trigger; "it seemed better" is not a reason you can re-evaluate.

**Values engaged:** Which principles from [[Values Statement]] this serves, or trades off
against. Trade-offs are worth recording precisely because they are the interesting ones.

**Files:** `.claude/commands/...`, `.claude/skills/...`
```

Keep entries short. A paragraph each is plenty; this is a log, not an essay.

---

## Changes

### 2026-09-08 — Vault released as a starting structure

**What changed:** This vault was stripped from a working research Zettelkasten of ~900
notes down to a foundational structure: folders, commands, skills, scripts, templates and a
handful of example notes. Personal content, one researcher's notes, and infrastructure tied
to a specific machine were removed. Zotero-dependent commands were moved to an optional
tier in `extras/`, and the large-document summariser was rewritten to delegate to a
subagent rather than a local model server.

**Why:** The system was described in a conference paper, and describing a method without
releasing it leaves readers with an argument they cannot try. The stripping was necessary
because the original vault contains private material, and because notes tailored to one
researcher's thinking are noise to everyone else.

**Values engaged:** Value 2 (Transparency) — the tooling is now inspectable by anyone, not
just described. Value 8 (Provenance) — the paper and the artefact now point at each other.
A trade-off against Value 9 (Emergent Structure): shipping a fixed folder layout imposes a
taxonomy that a vault grown from nothing would have discovered for itself. The judgement
was that the cost of a blank start outweighs the cost of an inherited structure you are
free to change.

**Files:** everything.

---

*This is your log now. Add to it.*
