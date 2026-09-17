---
type: index
created: 2026-09-08
tags: [🌲]
---
# Values Statement

> [!tldr] TLDR
> **Key**:: The principles this vault's tools were built on — a position, offered for you to adopt, adapt or argue with

## Purpose

This document sets out the values that shaped how the commands, skills and workflows in
this vault were built. They derive from the argument developed in *Permanently Under
Construction: Hypertextual Friction in an AI-Augmented Zettelkasten*
([doi:10.1145/3800935.3830837](https://doi.org/10.1145/3800935.3830837)).

**These are a position, not a neutral description of good practice.** You inherited them by
cloning this vault. They reflect one researcher's commitments about the relationship
between people, machines and knowledge work, and reasonable people disagree with several
of them. Read them, keep what you want, and rewrite the rest — this is your copy.

They serve two purposes. As a **design guide**, they inform decisions when building new
commands or skills. As an **evaluation framework**, they give criteria for asking whether a
tool actually serves its intended purpose.

---

## Core Principles

### 1. Human Agency as Non-Negotiable

Human agency must remain central and inviolable. The intention/action boundary — where
humans determine *what* and *why* whilst machines execute *how* — must be preserved.
Systems should never appear autonomous or make decisions on behalf of users. Tools must
enable and empower user control over structure, connections and content rather than
replacing human decision-making.

### 2. Transparency Over Opacity

All AI reasoning, connections and processes must be visible and traceable. Systems should
expose relationships, provenance and alternatives explicitly rather than hiding synthesis
behind black-box operations. Users must be able to see *how* things connect and relate, not
merely *that* they do. Transparency enables verification, learning and informed
decision-making.

### 3. Beneficial Friction

Design for active engagement rather than passive consumption. Whilst tedious friction
should be eliminated, cognitive friction that enables learning and understanding must be
preserved. Tools should require explicit user decisions at critical junctures, maintaining
effort where effort produces capability development. Seamlessness should serve user goals
without undermining user growth.

### 4. Augmentation Over Automation

Tools must extend and enhance human capabilities rather than replace them. Support thinking
processes rather than outsource them. Scaffold learning and development rather than
shortcut it. The measure of success is whether tools make users *more* capable over time or
increasingly dependent.

### 5. Spatial and Associative Thinking

Privilege hypertext, network structures and spatial organisation over linear sequences.
Support non-linear exploration, multiple simultaneous threads, and explicit representation
of conceptual relationships. Externalise mental models as visible, manipulable structures.
Resist flattening knowledge into linear outputs when complexity requires network
representation.

### 6. Reciprocal Challenge and Genuine Collaboration

AI assistance should question assumptions, suggest alternatives and present conflicting
perspectives rather than merely mirroring user expectations. Avoid sycophancy. Enable
productive disagreement and refinement. True collaboration requires the capacity to push
back meaningfully, not just acquiesce smoothly.

### 7. Cognitive Preservation

Actively resist deskilling and cognitive offloading. Design for long-term capability
development rather than short-term convenience. Tools should strengthen thinking
capacities, not atrophy them. Monitor for patterns that erode rather than enhance human
cognitive abilities.

### 8. Provenance and Attribution

Maintain clear chains from sources to synthesis. Distinguish human-generated content from
AI-generated content. Track where ideas originate and how they transform. Support proper
citation, acknowledgement and intellectual honesty. Preserve the author function even as
authorship becomes distributed.

### 9. Emergent Structure Over Imposed Taxonomy

Let organisation emerge from use, connection-making and navigation rather than imposing
rigid taxonomies. Prefer bottom-up linking over top-down categorisation. Support multiple
simultaneous organisational schemes that coexist and complement each other. Allow meaning
to evolve through exploration and association.

### 10. Humanism as Foundation

Centre human meaning-making, intentionality and agency in all design decisions. Resist
technocratic centralism, where algorithms make hidden decisions, and algorithmic
paternalism, where systems guide behaviour through opaque optimisations. Design for radical
free play — user-directed exploration without predetermined paths. Treat users as thinking
agents engaged in meaning-making, not consumers of content.

---

## Where these show up in the tooling

The values are not decorative. Some concrete places they bite:

- **Value 1** — `/vault-health` offers fixes and waits; it never edits on its own initiative.
  The `#human` protection rule exists for the same reason.
- **Value 2** — `vault_health.py` and `vault_maturity.py` compute deterministically and the
  model interprets, so the numbers can be checked independently of what is said about them.
- **Value 3** — note creation proposes and asks rather than generating silently, and
  duplicate checks flag rather than resolve. The gate sits at creation rather than after it,
  because deferred review does not happen: unreviewed notes are never revisited, and the
  resulting vault is indistinguishable from one that was curated.
- **Value 6** — the `user-interaction-patterns` skill has an explicit critical-review
  pattern, because an assistant that agrees with everything is not collaborating.
- **Value 8** — the history chronicle and the `used-by` maturity model both exist to keep
  provenance visible.

## Application

These should inform the design of new commands and skills; the interaction patterns of the
assistant; the structure of the vault itself; decisions about what to automate and what to
keep as human practice; and the criteria for judging whether a tool works.

When you change the tooling on values grounds, record it in [[Vault Rationale]].
