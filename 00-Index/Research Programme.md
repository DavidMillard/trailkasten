---
type: index
created: 2026-09-08
updated: 2026-09-08
tags: [🌱]
---
# Research Programme

> [!tldr] TLDR
> **Key**:: The persistent questions this vault organises around — roughly a dozen, curated by hand, each pointing to the MOCs and hubs that operationalise it

This page is empty until you fill it. That is deliberate: the questions have to be *yours*,
and they are discovered rather than declared. Do not try to write them on day one.

## Why this is a page and not a metadata field

An earlier version of this system attached a `problems:` field to every note, so a note
could declare which research question it served. It failed — not as an idea, but as a
mechanism. Only a small fraction of notes ever carried the field, because tagging a note
with a question has no value *at the moment of tagging*. The payoff comes later, when you
want to see everything bearing on a question, and by then the data is too patchy to trust.

One curated page has the opposite property: it costs something to maintain, but what it
holds is always true.

## How to build it

Wait until you have enough notes to mine — fifty or so, at minimum. Then look for what the
vault keeps circling back to. The questions are usually already there, implied by which
MOCs you built and which hubs grew; you are naming a pattern, not inventing one.

**Cap the list at about twelve.** The constraint is the point: admitting a new programme
should force the question "which existing one does this displace?" at the moment you care
most. A list of thirty questions is a list of no questions.

## How it stays current

Nothing here is per-note metadata, and nothing accretes on a schedule. Entries change as a
side-effect of MOC work: when a MOC is created or substantially expanded, the reflection
step asks whether it fits an existing programme, extends one, or implies a new one.

`/vault-health` reports any programme whose MOCs and hubs have gone untouched for twelve
months and asks once whether it is still live. *"Still live, it's slow-burning"* is a
legitimate answer, and gets recorded as a `**Reviewed**:` line so the question is not asked
again next year.

Retired programmes move to **Emeritus** at the foot of the page rather than being deleted,
because dormant questions revive.

---

## Entry format

Each programme is a numbered `###` heading under **Active Programmes** below, followed by a
paragraph and its links. `/vault-health` parses that shape, so keep to it:

```markdown
### 1. <The question, phrased as a question>

A paragraph saying what the question actually asks — sharp enough that you could tell
whether a given note bears on it. Say what makes it live for you now.

- **MOCs**: [[A MOC that operationalises it]]
- **Hubs**: [[A Hub]] · [[Another Hub]]
- **Anchors**: [[The three to five notes that carry the question]]
```

Dormancy is computed from the `created:` dates of notes hanging off the linked MOCs and
hubs, not from file modification times — so a bulk retag cannot silently reset the clock.

---

## Active Programmes

*None yet.* Add your first when the vault is large enough to show you what it is.

---

## Emeritus

*None yet.* Retired programmes land here with a line saying what displaced them and when.
