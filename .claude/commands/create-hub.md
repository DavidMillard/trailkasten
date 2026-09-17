---
description: Create a new Hub page with intelligent connections and suggestions
skills: note-creation, vault-writing-style, zettelkasten-methods, obsidian-patterns, history-update
argument: hub subject
---

# Create Hub

Create a comprehensive Hub page that organises existing notes around a conceptual domain.

## Skills Required

- **note-creation** - For hub creation process and validation
- **vault-writing-style** - For the epistemological stance and spelling convention
- **zettelkasten-methods** - For template structure and conventions
- **obsidian-patterns** - For efficient MCP-based vault operations
- **history-update** - For recording creation in daily history

## What is a Hub?

Hubs are evergreen conceptual domains that organise related notes. Unlike MOCs (project-based, narrative), Hubs are stable landing pages for broad topics.

**Examples:** "Artificial Intelligence", "Learning", "Philosophy", "HCI"

## Workflow

### Step 1: Research and Validate

1. Read template: `90-Templates/Template - Hub.md`
2. Check hub doesn't already exist (same/similar name)
3. Validate scope against the thresholds in the `note-creation` skill (Hub Creation Process, Step 1) — too narrow, too broad, or overlapping an existing hub

**If issues found:** Present to user with recommendation before proceeding.

### Step 2: Create Hub File

Create `20-Hubs/<Subject>.md` following template exactly:

**Frontmatter:**
```yaml
---
type: hub
tags:
  - 🌱
used-by: 0
topics:
  - "[[Related Hub 1]]"
  - "[[Related Hub 2]]"
---
```

**Content structure:**
- **TLDR callout**: One-line domain description with `Key::` field
- **Introduction**: 2-3 paragraphs explaining the domain and its significance
- **Related Hubs**: 1-3 hubs with relationship explanations
- **DataView queries**: Keep exactly as in template (auto-populate)

**Hub naming:** 1-3 words maximum. Use clear, established terminology. No articles ("The", "A") or verbose descriptions.

### Step 3: Link Notes to Hub

Find 5-15 notes that belong to this domain:

1. Search vault using MCP tools:
   - `mcp__obsidian__vault` action `search` with domain keywords
   - `mcp__obsidian__dataview` for notes with related tags/topics
2. Select 2-3 of the most relevant notes found so far. Run `mcp__smart-connections__get_similar_notes` on each (threshold: 0.3, limit: 10) to discover notes in the hub's conceptual neighbourhood that keyword search missed. Deduplicate with existing results. Follow Smart Connections Failure Protocol from `obsidian-patterns` if unavailable.
3. Categorise: high relevance (include) vs medium relevance (include selectively)
4. For each note to link: Add hub to `topics` frontmatter field

**Note:** You link notes TO the hub via their topics field. The hub's DataView queries automatically show connected notes.

### Step 4: Update Related Hubs

For 1-3 related hubs:
1. Read hub file
2. Add bidirectional link in `topics` frontmatter if not present
3. Optionally add mention in Related Hubs section

### Step 5: Finalise

**Report to user:**
```markdown
## Hub Created: [[Subject]]

**Location**: `20-Hubs/Subject.md`

**Notes linked** (X total):
- [[Note 1]] - [brief relevance]
- [[Note 2]] - [brief relevance]
[Continue...]

**Related hubs connected**:
- [[Hub 1]] - [relationship]
- [[Hub 2]] - [relationship]

**Knowledge gaps identified**:
Notes that would strengthen this hub but don't exist:
- [[Suggested Note 1]] - [why needed]
- [[Suggested Note 2]] - [why needed]
[3-5 suggestions...]

Would you like me to create any of these notes to strengthen the hub?
```

**Update history:** Use `history-update` skill to offer recording in daily history.

## Guidelines

**Hub characteristics:**
- Organises 5-20 notes (ecosystem that's developed but manageable)
- Stable conceptual domain, not project-specific
- Scope thresholds, naming rules, and maturity (new hubs start 🌱 untested) are specified in the `note-creation` skill

**Tentative language with attribution** — follow the `vault-writing-style` skill (the Introduction is prose, so the epistemological stance matters here).

## Example Usage

```
/create-hub Machine Learning Ethics
/create-hub "Mixed Reality"
/create-hub Cognitive Science
```
