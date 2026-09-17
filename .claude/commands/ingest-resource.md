---
description: Process raw resources (conversations, transcripts, articles) and extract atomic notes
skills: summarise-large-document, note-creation, vault-writing-style, zettelkasten-methods, obsidian-patterns, user-interaction-patterns, history-update
argument: file path or pasted content
---

# Ingest Resource

Process raw resources (AI conversations, transcripts, articles) and extract valuable atomic notes with user approval.

## Skills Required

- **summarise-large-document** - For token-efficient processing of large documents
- **note-creation** - For batch atomic note creation with connections
- **vault-writing-style** - For the epistemological stance and spelling convention
- **zettelkasten-methods** - For template structure and conventions
- **obsidian-patterns** - For efficient MCP-based vault operations
- **user-interaction-patterns** - For approval flows and critical review
- **history-update** - For recording creation in daily history

## Critical Rules

1. **Never read large resources directly** - For files >25,000 chars, check size first then summarise locally
2. **Always batch atomic notes** - Create all approved notes in one pass (batch mode pattern)
3. **Wait for user approval** - Never create notes without explicit approval
4. **If the summariser fails** - Ask user how to proceed, don't fall back automatically

## Workflow

### Step 1: Accept Resource (Do NOT Read Yet)

**Input options:**
- File path → Check size first (Step 2) before reading
- Filename only (no path) → Assume file is in `80-Fleeting/YYYY/Month/` using the current date (e.g., `80-Fleeting/2026/March/`)
- Pasted content → Use directly (skip size check)

**Formats supported:** .txt, .md, .docx, .pdf

**IMPORTANT:** Do NOT use Read tool on the file yet. Proceed to Step 2 to check size first.

### Step 2: Check Size and Preprocess

**Check file size FIRST:**
```bash
wc -c "path/to/file.md"
```

Report size:
```
Resource received: [X] characters (~[Y] words)
```

**If >25,000 chars → delegate the summary (MANDATORY):**

Follow the `summarise-large-document` skill: dispatch a Haiku subagent with the
file path, a one-line description of the resource, and the eight-section output
format. The full text stays in the subagent's context and never enters this one.

**After it returns:** use ONLY the summary for Steps 3-4. Do NOT read the
original file.

**If ≤25,000 chars:** Use the Read tool on the file, then proceed.

**If the summary comes back empty or generic** — usually failed text extraction
— follow the skill's fallback protocol: name what happened and offer (1) retry
via `pdftotext`, (2) direct reading at higher context cost, (3) stop.

**Wait for user response.** Never fall back automatically.

### Step 3: Create Resource File

1. Read template: `90-Templates/Template - Resource.md`
2. Create file in `40-Resources/` with format: `[Source Type] - [Topic].md`
   - Examples: `Conversation - Vibe Writing.md`, `Transcript - AI Ethics Podcast.md`
3. Populate frontmatter:
```yaml
---
type: resource
created: YYYY-MM-DD
status: unprocessed
topics:
  - "[[Relevant Hub]]"
---
```

4. Replace template placeholders:
   - Type, date, source, title, format, length, link

5. Populate Comprehensive Summary with key points

6. **Full Content section:**
   - If the summariser was used: Link to original file (e.g., `See original: [[filename]]`)
   - If read directly: Append complete original content

7. Leave Key Concepts and Processing Notes for later steps

### Step 4: Analyse and Suggest

**Two categories of notes to consider — check both:**

#### 4a: Foundational Concept Gap Check

Before suggesting novel extractions, identify foundational concepts the resource discusses that the vault lacks:

1. Take the key concepts/terms from the local summary or your own analysis
2. For each concept, search vault (`30-Notes/`) for an existing atomic note
3. Flag concepts that meet ANY of these criteria:
   - Referenced by 2+ existing vault notes but no dedicated atomic note exists
   - Core disciplinary term that the resource formally defines or relies upon
   - Concept that would serve as a high-connectivity node linking existing notes
4. These are **foundational gaps** — concepts the vault implicitly uses but hasn't formally defined

#### 4b: Novel Contributions

**Identify 2-5 concepts** worth developing as atomic notes. For each:
- What the concept is
- Why it's valuable for the vault
- Which existing notes it connects to

#### 4c: Search Vault for Connections

**Search vault for connections** using MCP tools:
- Search with concept keywords to find related notes
- Explore existing connections to identify linking opportunities
- For each suggested concept, search for an existing note with the closest title match. If found, run `mcp__smart-connections__get_similar_notes` on it (threshold: 0.3, limit: 10) to discover the concept's semantic neighbourhood. This enriches connection suggestions and helps the critical review step (4.75) catch redundancy more effectively — a semantic match > 0.8 with an existing note is stronger evidence of overlap than keyword matching alone. Follow Smart Connections Failure Protocol from `obsidian-patterns` if unavailable.

**Identify potential hubs** (0-2) if:
- Concept is broad enough for 5-15 notes
- No existing hub covers the domain
- You find orphaned note clusters sharing a conceptual domain

### Step 4.5: Present Suggestions

Follow `user-interaction-patterns` skill's approval flow:

```markdown
## Analysis Complete: [Resource Title]

Resource file: `40-Resources/[filename].md`

### Foundational Concepts (vault gaps)

These concepts are referenced across existing notes but lack dedicated atomic definitions:

1. **[[Concept Name]]**
   - **What**: [Brief description]
   - **Why needed**: Referenced by [[Note A]], [[Note B]]; no dedicated note exists
   - **Connects to**: [[Hub]], [[Note 1]], [[Note 2]]

### Novel Contributions

Insights from this resource worth extracting:

1. **[[Note Title]]**
   - **What**: [Brief description with tentative language]
   - **Why**: [Value for vault]
   - **Connects to**: [[Note 1]], [[Note 2]], [[Hub]]

[Continue for all suggestions]

### Suggested Hubs (if any):
- **[[Hub Name]]**: [Why this domain deserves a hub]

Which would you like me to create?
```

**Wait for explicit user approval.**

### Step 4.75: Critical Review (Value 6: Reciprocal Challenge)

Follow `user-interaction-patterns` skill's critical review pattern.

Check for concerns (flag max 1-2):
- **Redundancy**: Suggestion overlaps significantly (>70%) with existing note
- **Over-atomisation**: Multiple suggestions share a conceptual core
- **Weak connections**: Suggestion would have ≤1 connection (isolated)
- **Hub redundancy**: Suggested hub overlaps with existing hubs

Present concerns as questions with alternatives. **Wait for user response.**

### Step 5: Create Approved Notes (Batch Mode)

Follow `note-creation` skill's batch mode pattern.

**Setup (once):**
1. Read template: `90-Templates/Template - Zettel Note.md`
2. List vault structure
3. Validate all suggested connections exist
4. Read 2-3 exemplar notes

**Create notes (sequential):**
For each approved concept:
1. Create note file with:
   - Frontmatter: type, created date, 🌱 tag with `used-by: 0`, topics
   - TLDR with Key field
   - Details: 4-6 bullets explaining concept
   - Connections: 2-6 related notes
   - References: Link to resource file
2. Track for backlink phase

**Do NOT add backlinks yet.**

**Batch backlinks:**
After all notes created:
1. Collect all related notes across new notes (deduplicate)
2. For each unique target: Read once, apply backlink rules, add ALL applicable backlinks
3. Track decisions (backlinks do not change maturity — see `note-creation` skill)

**If hubs approved:**
Create hub using hub creation process from `note-creation` skill.

### Step 6: Update Resource File

Edit resource file to add:
- **Key Concepts**: Concepts that were created
- **Processing Notes**: Date processed, notes created, hubs created, backlinks established, status → `processed`

### Step 6.5: Territory Feedback

Run `python3 .claude/scripts/vault_maturity.py --hubs` and, for each hub the new notes link to via `topics:`, note its territory heat for the report — flag when material lands in one of the vault's least-tested territories (see `note-creation` skill, Territory Feedback).

### Step 7: Report to User

```markdown
## Resource Processed: [Resource Title]

**Resource file**: `40-Resources/[filename].md`

### Notes Created (X total)

| Note | Connections |
|------|-------------|
| [[Note 1]] | 4 |
| [[Note 2]] | 3 |
[Continue...]

### Hubs Created (if any)

- [[Hub Name]] - [X notes linked]

### Backlinks Established

- **Added** (Y notes updated): [[Note A]], [[Note B]]...
- **Skipped** (Z notes at capacity): [[Note C]]...

### Territory

- New material extends [[Hub A]] (62% tested) and [[Hub B]] (29% tested — one of the vault's least-tested territories)

### Knowledge Network Impact

- [Brief description of how new content integrates]

Would you like me to update today's history entry?
```

**Update history:** Use `history-update` skill.

## Guidelines

- Follow the `vault-writing-style` skill for tentative language and attribution
- Follow `zettelkasten-methods` skill for type fields and conventions
- Use `obsidian-patterns` skill for efficient vault searches
- All extracted notes must link back to resource in References section

## Example Usage

**From file:**
```
/ingest-resource ./conversations/claude-chat.txt
/ingest-resource ~/Downloads/transcript.md
```

**From pasted content:**
```
/ingest-resource
I had a conversation about AI and thinking...
[paste full content here]
```
