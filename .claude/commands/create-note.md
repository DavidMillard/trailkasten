---
description: Create a new Zettelkasten note with intelligent connections and suggestions
skills: note-creation, vault-writing-style, zettelkasten-methods, obsidian-patterns, history-update
argument: note subject
---

# Create Note

Create a comprehensive atomic note with intelligent bidirectional connections.

## Skills Required

- **note-creation** - For connection strength tiers, backlink rules, and note creation process
- **vault-writing-style** - For the epistemological stance and spelling convention
- **zettelkasten-methods** - For template structure and conventions
- **obsidian-patterns** - For efficient MCP-based vault operations
- **history-update** - For recording creation in daily history

## Workflow

### Step 1: Clarification Phase (Only if Needed)

Skip for clearly unambiguous subjects with context provided.

**Check for ambiguity:**
- Term has multiple meanings across domains
- Broad term that should be multiple atomic notes
- Unfamiliar technical term

**If ambiguous:** Use AskUserQuestion to present 2-4 interpretations.

**Verify understanding:** For technical/academic terms, briefly confirm your interpretation before proceeding.

**Check for issues:**
- Similar existing note (>60% overlap) - offer to show it first
- Broad scope - suggest narrowing
- Related notes already overloaded (10+ connections) - note backlinks will be skipped

Present concerns as informational flags (max 1-2). User can say "proceed" to continue.

### Step 2: Research Vault

1. Read template: `90-Templates/Template - Zettel Note.md`
2. Search for related content using MCP tools:
   - Use `mcp__obsidian__vault` action `search` with relevant keywords
   - Use `mcp__obsidian__graph` action `neighbors` to explore connections
   - If a closely related note exists, call `mcp__smart-connections__get_similar_notes` on the most relevant existing note (threshold: 0.3, limit: 10) to discover additional semantic neighbours. Follow Smart Connections Failure Protocol from `obsidian-patterns` if unavailable.
3. Read 2-3 exemplar notes from `30-Notes/` to understand style

### Step 3: Create Note File

Create `30-Notes/<Subject>.md` following template exactly:

**Frontmatter:**
```yaml
---
type: note
created: YYYY-MM-DD
tags:
  - 🌱
topics:
  - "[[Hub Name]]"
aliases:
  - [if applicable]
---
```

**Content structure:**
- **TLDR callout**: `> [!tldr] TLDR` with `Key::` one-line description (<100 chars)
- **Details**: 4-6 bullets explaining ONLY what the concept IS (not connections)
- **Connections**: 2-6 related notes with inline descriptions
- **References**: Source information

Follow the `vault-writing-style` skill for tentative language and attribution.

### Step 4: Identify Connections

**Semantic enrichment:** After creating the note file, call `mcp__smart-connections__get_similar_notes` on the new note (threshold: 0.3, limit: 10) to validate and enrich connections. Merge with existing candidates from Step 2, then filter. Follow Smart Connections Failure Protocol from `obsidian-patterns` if unavailable.

Apply **Connection Strength Tiers**, the **quality tests**, and the **2-6 hard limit** from the `note-creation` skill — it is the single source for these criteria.

### Step 5: Add Bidirectional Links

**For each related note (2-6):**
1. Read note, count existing connections
2. Apply the **backlink rules** from `note-creation` (the table keyed on the existing note's connection count)
3. If approved: Add backlink with one-sentence description

**Track:** Backlinks added, backlinks skipped (with reason).

### Step 6: Finalise

**Check if new hub needed:** If concept is broad enough for 5-15 notes and no existing hub covers it, suggest to user.

**Suggest related notes:** 3-5 topics that would strengthen the network but don't exist.

**Report to user:**
```markdown
## Note Created: [[Subject]]

**Location**: `30-Notes/Subject.md`
**Maturity**: 🌱 untested (all new notes — graduates when a MOC, draft, or analysis draws on it)

**Connections established** (X total):
- [[Note 1]] - [relationship]
- [[Note 2]] - [relationship]
[Continue...]

**Backlinks added** (Y notes updated):
- [[Note A]] - now has Z connections
- [[Note B]] - now has Z connections
[Continue...]

**Backlinks skipped** (Z notes at capacity):
- [[Note C]] - 10+ connections, skipped
[If any...]

**Suggestions for network growth**:
- [[Suggested Note 1]] - would connect to X, Y, Z
- [[Suggested Note 2]] - would connect to A, B
[3-5 suggestions...]

Would you like me to create any of these suggested notes?
```

**Update history:** Use `history-update` skill to offer recording in daily history.

## Guidelines

- **Atomic principle, alias criteria, connection limits, backlink rules, maturity** — all specified in the `note-creation` skill; do not restate them here
- **Topics:** link to 1-3 relevant hubs in frontmatter
- **Tentative language with attribution** — follow the `vault-writing-style` skill

## Example Usage

```
/create-note Flow State Psychology
/create-note "Reinforcement Learning from Human Feedback"
/create-note Constitutional AI
```
