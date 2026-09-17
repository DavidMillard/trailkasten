---
name: zettelkasten-methods
description: Zettelkasten methodology for Obsidian-based personal knowledge management. Use when working with notes, MOCs, hubs, literature notes, or any Zettelkasten structure task including (1) Creating notes, hubs, MOCs, or literature notes, (2) Understanding linking strategies and navigation flow, (3) Applying file naming, frontmatter, or formatting conventions, (4) Determining when to create specific content types, (5) Understanding maturity tagging or content organization.
---

# Zettelkasten Methods

This skill provides the methodology for working with an Obsidian-based Zettelkasten personal knowledge management system.

## Quick Reference: When to Create What

**Reading an academic paper?**
→ Create Literature Note in `45-Literature/` → Extract atomic concepts as Notes in `30-Notes/`

**New idea from reading?**
→ Create Note in `30-Notes/` → Link to source Literature Note in References

**Starting a project?**
→ Create MOC in `10-MOCs/` → Link to relevant Hubs and Notes

**Notice cluster of notes?**
→ Create Hub in `20-Hubs/` → Link all related Notes

**Identify persistent question?**
→ Consider it against [[Research Programme]] (`00-Index/`) — see Research Programme below

**Hub getting too large?**
→ Split into sub-Hubs or create specific MOCs

**Ready to write?**
→ Create Draft in `50-Drafts/` → Link to source Notes and related MOC

## Core Content Types

### Research Programme (`00-Index/Research Programme.md`)

The vault's persistent research questions — roughly twelve, curated by the user — live on **one page**, not in a folder. It replaced an earlier per-note approach, where each note declared which research question it served through a `problems:` frontmatter field. That failed as a mechanism: hardly any notes ever carried the field, because tagging a note with a question has no value at the moment of tagging — the payoff comes later, by which time the data is too patchy to trust.

**There is no per-note problem metadata. Do not reintroduce any.** A note's relationship to a programme is readable from the MOCs and hubs the programme links to.

**The reflection step (this is how the page stays current).** Whenever you create or substantially expand a MOC, ask the user — do not decide alone:

> Does this MOC fit an existing programme on [[Research Programme]], extend one, or imply a new one?

- *Fits*: offer to add the MOC to that programme's **MOCs** line.
- *Extends*: offer to revise the programme's sentence so it covers the new ground.
- *Implies a new one*: the page is capped at ~12 (Feynman's constraint). Ask which existing programme it displaces — the cap is the retirement mechanism, and displacement is the only routine route to Emeritus.

Retired programmes move to the **Emeritus** section; they are never deleted, because dormant questions revive. `/vault-health` reports any programme whose territory has gained no new content in twelve months and asks once whether it is still live — "still live, it's slow-burning" is a legitimate answer.

### MOCs - Maps of Content (`10-MOCs/`)
Narrative synthesis documents that tell a story connecting related notes.

**Characteristics:**
- Focus on conceptual synthesis and coherent understanding
- Tied to projects or learning journeys (dynamic and temporal)
- 15-25 links maximum, woven into narrative
- Include minimal project tracking

### Hubs (`20-Hubs/`)
Evergreen conceptual anchors organizing notes by theme or domain.

**Characteristics:**
- Stable and permanent
- Link primarily to Notes, can reference other Hubs
- Domain-focused (e.g., "Personal Knowledge Management", "Artificial Intelligence")

### Literature Notes (`45-Literature/`)
Comprehensive representations of academic papers and research.

**Characteristics:**
- Full metadata, abstract, AI-generated analysis
- Bibliographic references for atomic notes
- Named using citation keys (e.g., `atzenbeckUnwindingAIsMoral2024.md`)
- AI Analysis section MUST include inline links to existing atomic notes

### Notes (`30-Notes/`)
Atomic ideas following Zettelkasten principles.

**Characteristics:**
- One idea per note, self-contained but richly linked
- Spawn from Literature Notes or Resources, synthesized in your own words
- Link back to source in References section
- Should link to 1-3 relevant hubs

### Resources (`40-Resources/`)
Raw materials for note extraction (conversations, transcripts, articles).

**Characteristics:**
- Processing artifacts serving as sources for atomic notes
- Include metadata (source, date, format) and content summary
- Tagged with `resource-type` for subcategorization

### Drafts (`50-Drafts/`)
Writing projects synthesized from Zettelkasten notes.

**Characteristics:**
- Blog posts, articles, papers synthesized from multiple notes
- Minimal markdown formatting for easy export
- Track source notes, revisions, publishing status
- Status field: in-progress, completed, or published

## Maturity System (Usage Model)

All notes use emoji tags to represent maturity, NOT concepts. Since 2026-07-13 maturity records **use, not structure**: how many distinct higher-level artefacts (MOCs, drafts, analyses — "consumers") draw on the note.

- **🌱 Untested** - Never drawn on by higher-level work (0 consumers)
- **🌿 Drawn on** - Has fed at least one narrative (1–2 distinct consumers)
- **🌲 Load-bearing** - Supports multiple narratives (3+ distinct consumers)

**CRITICAL:** Maturity tags and the `used-by:` frontmatter field are a **computed cache**, owned by `.claude/scripts/vault_maturity.py`. Never hand-set or hand-update them beyond the birth state (`tags: [🌱]`, `used-by: 0`). Commands that create or edit MOCs, drafts, or analyses run `python3 .claude/scripts/vault_maturity.py --write` as their final step; `/vault-health` reconciles as backstop. Backlinks, hub membership, and content edits do NOT change maturity — only being drawn on does.

## Essential Conventions

### Frontmatter

```yaml
---
type: [moc|hub|note|literature-note|resource|draft]
created: YYYY-MM-DD
tags: [🌱]  # Maturity (script-owned) + optional _-prefixed maintenance tags (see conventions.md)
used-by: 0  # Consumer count — script-owned cache, never hand-set
status: [active|on-hold|completed]  # for MOCs only
---
```

**Type field convention:**
- `type: note` - ALL files in `30-Notes/`
- `type: literature-note` - ONLY files in `45-Literature/`
- `type: hub` - ONLY files in `20-Hubs/`
- `type: moc` - ONLY files in `10-MOCs/`
- `type: resource` - ONLY files in `40-Resources/`
- `type: draft` - ONLY files in `50-Drafts/`

### TLDR Callout

Every MOC, Hub, and Note MUST start with:

```markdown
> [!tldr] TLDR
> **Key**:: Brief one-line description of the page
```

This enables DataView queries and enforces clarity.

### File Naming

- **MOCs**: "Project Name" (no prefix)
- **Hubs**: "Concept Name" (no prefix)
- **Literature Notes**: Citation key format (`authorYearKeyword.md`)
- **Notes**: "Descriptive Title" (no prefix)
- **Templates**: "Template - Type"

Use descriptive names, not numeric IDs.

## Detailed Information

For comprehensive details, see:
- **[methodology.md](methodology.md)** - Complete content type definitions, navigation flow, linking principles, and hybrid literature workflow
- **[conventions.md](conventions.md)** - Markdown formatting rules, DataView integration patterns, and detailed tagging philosophy

## Core Principles

1. **Atomic notes** - One idea per note
2. **Bidirectional linking** - Use wiki-links `[[Note Name]]` everywhere
3. **Hub-based organization** - Concepts via links, not tags
4. **Emergent structure** - Let organization emerge from connections
5. **Maturity from use** - Notes graduate 🌱 → 🌿 → 🌲 as MOCs, drafts, and analyses draw on them
6. **Progressive disclosure** - Start simple, add detail as needed
