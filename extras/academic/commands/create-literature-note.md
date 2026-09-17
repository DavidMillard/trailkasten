---
description: Create a new Literature Note from a Zotero citation key with automated metadata and AI analysis
skills: summarise-large-document, note-creation, vault-writing-style, zettelkasten-methods, obsidian-patterns, user-interaction-patterns, history-update
argument: citation key
---

# Create Literature Note from Zotero

Create a comprehensive Literature Note from an academic paper in the user's Zotero library, with automated metadata extraction, AI analysis, reading strategy, and atomic note extraction.

## Skills Required

- **summarise-large-document** - For token-efficient full text summarisation
- **note-creation** - For batch atomic note creation with connections
- **vault-writing-style** - For the epistemological stance and spelling convention
- **zettelkasten-methods** - For template structure and conventions
- **obsidian-patterns** - For efficient MCP-based vault operations
- **user-interaction-patterns** - For approval flows and critical review
- **history-update** - For recording creation in daily history

## Critical Rules

1. **Never pull full text into Claude's context directly** - extract the attached PDF and summarise it locally via the `summarise-large-document` skill
2. **Always batch atomic notes** - Create all approved notes in one pass (batch mode pattern from note-creation skill)
3. **Wait for user approval** - Never create notes without explicit approval
4. **If the summariser fails** - Ask user how to proceed, don't fall back automatically
5. **Never create a duplicate** - Step 2.5 checks `45-Literature/` for an existing note (by DOI and title, not just citation key) before any summarisation or writing; if one exists, stop and point to it

## Workflow

### Step 1: Search Zotero

Use `mcp__zotero__search` with the citation key (from $ARGUMENTS).

If not found, try title/author keywords as fallback.

### Step 2: Fetch Metadata

Use `mcp__zotero__zotero_get_item_metadata` with:
- `include_abstract: true`
- `format: markdown`

Extract: title, authors, year, venue, DOI, URL, abstract, Zotero item key.

### Step 2.5: Check for an existing literature note

Before any summarisation or note creation, confirm no literature note already exists for this paper. This prevents a duplicate when the paper has been processed before — possibly under a **different citation key** (BBT can assign a disambiguating suffix, so a citekey match alone is not enough).

1. Is there a note at `45-Literature/<citekey>.md`? → it exists.
2. Otherwise search `45-Literature/` by the paper's **DOI** (from Step 2), then by normalised **title**:
   `mcp__obsidian__vault(action: "search", query: "<DOI>", directory: "45-Literature")`, and if no hit, the title.

If an existing note is found, **stop** — do not summarise or create anything — and report:

```
A literature note for this paper already exists: [[<existing-citekey>]]
(45-Literature/<existing-citekey>.md). Nothing created.
Open it, or tell me to update it / add a second note deliberately.
```

Proceed to Step 3 only when no existing note is found.

### Step 3: Fetch and Summarise Full Text

Follow the `summarise-large-document` skill: resolve the paper's attached PDF
from the Zotero item (the attachment key comes from the item's `children`), then
dispatch a Haiku subagent to read it and return the eight-section summary.

```bash
# Resolve the attached PDF path from the Zotero item, then pass it to the subagent.
ls ~/Zotero/storage/[ATTACHMENT_KEY]/*.pdf | head -1
```

Give the subagent the PDF path and `Context: "[TITLE] by [AUTHORS] ([YEAR]), [VENUE]"`.

If the item has no PDF, write the Zotero MCP `zotero_item_fulltext` output to a
temporary file and give the subagent that path instead.

**If the summariser fails or the item has no full text:**

First, assess training knowledge confidence: *high* = can reliably reconstruct key arguments, structure, and concepts; *low* = limited familiarity.

**If high confidence:**
```
No full text was available. I have substantial prior knowledge of this work.

1. **Use training knowledge** — flagged in note; Engagement Guide uses Engagement Map + Intellectual Stakes
2. **Abstract only** — Intellectual Stakes only
3. **Retry the summariser**
4. **Stop here**
```

**If low confidence:** omit option 1 and note limited familiarity.

**Wait for user response before proceeding.**

### Step 4: Find Related Papers

Use `mcp__zotero__zotero_semantic_search` for papers related to main topics (limit 5).

### Step 5: Generate AI Analysis

Using the local summary:
- Identify 3-5 key contributions (novel insights, methods, findings)
- List related papers from user's Zotero library
- Write in clear, concise academic language

### Step 6: Create Literature Note

1. Read template: `90-Templates/Template - Literature Note.md`
2. Create filename: Citation key (e.g., `authorYearKeyword.md`) in `45-Literature/`
3. Populate frontmatter:
```yaml
---
type: literature-note
created: YYYY-MM-DD
tags:
  - 🌱
topics:
  - "[[Relevant Hub]]"
---
```

4. Replace all template placeholders:
   - Date, title, authors, year, venue, DOI, URL
   - Zotero link: `zotero://select/library/items/ITEMKEY`
   - Abstract (from metadata)

5. Fill AI Analysis with Key Contributions and Related Papers

6. Generate one-line TLDR for Key field (<100 chars)

7. Leave Engagement Guide section for next step

### Step 6.5: Generate Engagement Guide

Adapts to available knowledge. Search vault for related concepts before generating.

**Full text available (local summary):**
Categorise sections using SECTION STRUCTURE:
- 🔥 **DEEP READ** — Contradicts/challenges vault notes, provides empirical evidence, offers novel alternatives. Explain why; link specific notes.
- 📖 **READ** — Examples, case studies, or extensions of existing concepts.
- (Others can be skimmed)

**Training knowledge, structured text (book/thesis):**
Three components:
- **Engagement Map** — Map each extracted concept to the chapter(s) where it's principally developed, so the user can navigate purposefully.
- **Intellectual Stakes** — 2–3 open questions this text may help answer, framed relative to existing vault problems or MOCs.
- **Epistemic Provenance** — Note which extracted concepts are high-confidence from training vs. which need verification from the text directly.

**Training knowledge, less structured (article/chapter I know partially):**
- **Intellectual Stakes** only.

**Abstract only:**
- **Intellectual Stakes** derived from abstract and vault connections.

Update the literature note's Engagement Guide section with this analysis.

### Step 7: Suggest Atomic Notes

**Two categories of notes to consider — check both:**

#### 7a: Foundational Concept Gap Check

Before suggesting novel contributions, identify foundational concepts the paper defines or builds upon that the vault lacks:

1. Take the summary's KEY CONCEPTS list
2. For each concept, search vault (`30-Notes/`) for an existing atomic note
3. Flag concepts that meet ANY of these criteria:
   - Referenced by 2+ existing vault notes but no dedicated atomic note exists
   - Core disciplinary term that the paper formally defines
   - Concept that multiple Zotero items are tagged with (check tags)
4. These are **foundational gaps** — concepts the vault implicitly uses but hasn't formally defined

#### 7b: Novel Contributions

Using the summary's POTENTIAL ATOMIC NOTES and KEY CONCEPTS:
- Refine to 2-5 concepts worth extracting as novel contributions
- For each concept:
  - Concept name
  - Brief explanation
  - Why it's atomic (single idea)
  - Suggested hub/note connections

#### Present Both Categories

Present suggestions using approval flow from `user-interaction-patterns` skill, clearly distinguishing the two categories:

```markdown
## Suggested Atomic Notes from [[citationKey]]

### Foundational Concepts (vault gaps)

These concepts are referenced across existing notes but lack dedicated atomic definitions:

1. **[[Concept Name]]**
   - **What**: [Brief description]
   - **Why needed**: Referenced by [[Note A]], [[Note B]]; no dedicated note exists
   - **Connects to**: [[Hub]], [[Note 1]], [[Note 2]]

### Novel Contributions

Insights specific to this paper worth extracting:

1. **[[Concept Name]]**
   - **What**: [Brief description with tentative language]
   - **Why atomic**: [Reasoning]
   - **Connects to**: [[Hub]], [[Note 1]], [[Note 2]]

[Continue for all suggestions]

Which would you like me to create?
```

**Wait for user approval.**

### Step 7.5: Critical Review (Value 6: Reciprocal Challenge)

Follow `user-interaction-patterns` skill's critical review pattern.

Check for concerns (flag max 1-2):
- **Redundancy**: Suggestion overlaps significantly with existing note
- **Over-atomisation**: Multiple suggestions share conceptual core
- **Weak connections**: Suggestion would have ≤1 connection
- **Over-extraction**: 4-5 notes from single paper may be excessive
- **Confirmatory vs novel**: Most suggestions confirm rather than extend existing knowledge

Present concerns as questions with alternatives. **Wait for user response.**

### Step 8: Create Atomic Notes (Batch Mode)

Follow `note-creation` skill's batch mode pattern.

**Setup (once):**
1. Read template: `90-Templates/Template - Zettel Note.md`
2. List vault structure
3. Validate all suggested connections exist
4. Read 2-3 exemplar notes

**Create notes (sequential):**
For each approved concept:
1. Create note file with:
   - Frontmatter: type, created date, 🌱 tag, topics
   - TLDR with Key field
   - Details: 4-6 bullets explaining concept
   - Connections: 2-6 related notes (from suggestions + validated)
   - References: Link to [[citationKey]]
2. Track for backlink phase

**Do NOT add backlinks yet.**

**Batch backlinks:**
After all notes created:
1. Collect all related notes across new notes (deduplicate)
2. For each unique target: Read once, apply backlink rules, add ALL applicable backlinks
3. Update maturity tags where appropriate
4. Track decisions

### Step 9: Enrich Literature Note

Edit AI Analysis section to add inline links to newly created and existing related atomic notes:

```markdown
1. **Key Contribution**: This connects to [[The Thief of Reason]] - when AI
   erases the thinking process... Related to [[Cognitive Offloading]].
```

### Step 9.5: Territory Feedback

Run `python3 .claude/scripts/vault_maturity.py --hubs` and, for each hub the new notes link to via `topics:`, note its territory heat for the report — flag when the paper's material lands in one of the vault's least-tested territories (see `note-creation` skill, Territory Feedback).

### Step 10: Report to User

```markdown
## Literature Note Created: [[citationKey]]

**Location**: `45-Literature/citationKey.md`
**Title**: "[Paper Title]" by [Authors] ([Year])

### Atomic Notes Created (X total)

| Note | Connections |
|------|-------------|
| [[Concept 1]] | 4 |
| [[Concept 2]] | 3 |
[Continue...]

### Backlinks Established

- **Added** (Y notes updated): [[Note A]], [[Note B]]...
- **Skipped** (Z notes at capacity): [[Note C]]...

### Territory

- This paper extends [[Hub A]] (62% tested) and [[Hub B]] (29% tested — one of the vault's least-tested territories)

### Literature Note Enriched

AI Analysis now includes inline links to:
- [[New Note 1]], [[New Note 2]]
- [[Existing Note 1]], [[Existing Note 2]]

### Engagement Guide Generated

- [Mode: Full text / Training knowledge / Abstract only]
- [Key elements produced: e.g. Section priorities / Engagement Map / Intellectual Stakes / Epistemic Provenance]

Would you like me to update today's history entry?
```

**Update history:** Use `history-update` skill.

## Conventions

- Inline metadata: `**Author(s)**:: Value` for DataView compatibility
- Wiki-links for related papers: `[[citationKey]]`
- Zotero link format: `zotero://select/library/items/ITEMKEY`
- TLDR under 100 characters
- The vault's spelling convention

## Example Usage

```
/create-literature-note atzenbeckUnwindingAIsMoral2024
/create-literature-note bushAsWeMayThink1945
```
