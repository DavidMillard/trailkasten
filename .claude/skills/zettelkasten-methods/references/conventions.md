# Conventions and Formatting

Detailed conventions for markdown formatting, frontmatter structure, DataView integration, and maturity tagging.

## Markdown Formatting Conventions

### Whitespace and Spacing Rules

**CRITICAL - Strict spacing requirements:**

- **No empty line above any heading** (including the main title after frontmatter)
- **Exactly one empty line after headings** before content begins
- **Exactly one empty line between sections** (before the next heading)
- **No trailing empty lines** at the end of files

### Example of Correct Spacing

```markdown
---
type: note
created: 2025-11-20
tags: [🌱]
---
# Note Title

> [!tldr] TLDR
> **Key**:: Brief description

Main content paragraph starts here.

## Section Heading

Content under this section.

### Subsection

More content.

---

## Another Section

Final content.
```

### Common Mistakes to Avoid

- ❌ Empty line before main title
- ❌ Empty line before section headings
- ❌ Multiple empty lines between sections
- ❌ No empty line after headings

## TLDR Callout Convention

**Every MOC, Hub, and Note must start with a TLDR callout immediately after the frontmatter.**

### Format

```markdown
> [!tldr] TLDR
> **Key**:: Brief one-line description of the page
```

### Purpose

- Quick overview when browsing
- Dataview can query the inline `Key::` field to build dynamic indexes
- Enforces clarity - if you can't summarize it in one line, the note may not be atomic enough

### Examples

**For a MOC:**
```markdown
> [!tldr] TLDR
> **Key**:: Research on AI/LLM applications for knowledge work and creative tasks
```

**For a Hub:**
```markdown
> [!tldr] TLDR
> **Key**:: Methods, tools, and practices for capturing and organizing information
```

**For a Note:**
```markdown
> [!tldr] TLDR
> **Key**:: One idea per note maximizes flexibility in connecting notes
```

### Guidelines

- Keep it to one line (under 100 characters ideal)
- Focus on the essence, not implementation details
- Use active, descriptive language
- The `Key::` inline field enables queries like: `TABLE Key FROM "30-Notes"`

## Frontmatter Structure

All notes include YAML frontmatter for metadata.

### Standard Structure

```yaml
---
type: [moc|hub|note|literature-note|resource|draft]
created: YYYY-MM-DD
tags: [🌱]  # Maturity status only (see Tagging Philosophy)
status: [active|on-hold|completed]  # for MOCs only
---
```

### Type Field Convention (CRITICAL)

- **`type: note`** - ALL files in `30-Notes/` (atomic Zettelkasten notes)
- **`type: literature-note`** - ONLY files in `45-Literature/` (papers from Zotero)
- **`type: hub`** - ONLY files in `20-Hubs/` (concept hubs)
- **`type: moc`** - ONLY files in `10-MOCs/` (maps of content)
- **`type: resource`** - ONLY files in `40-Resources/` (raw materials for note extraction)
  - Use additional `resource-type` field for subcategorization (conversation, transcript, article, podcast, video)
- **`type: draft`** - ONLY files in `50-Drafts/` (writing projects)
  - Use additional `status` field: in-progress, completed, or published

**NEVER use `type: literature-note` for notes in `30-Notes/` - these are always `type: note`**

### Additional Fields

**Source and author information:**
- Belong in the References section with proper web links
- Do NOT put in frontmatter

**Keep frontmatter minimal:**
- Use it for metadata that enables queries and organization
- Don't duplicate information that belongs in the note body

### No `problems:` Field — Retired 2026-07-13

The `problems:` field was removed from every note and from both templates when the `05-Problems/` folder was replaced by [[Research Programme]] (`00-Index/`). **Never add it back, to any note.** A note's relation to a research question is expressed through the MOCs and hubs it already links to, not through metadata it has to carry.

## DataView Integration

The vault uses the DataView plugin to create dynamic, automatically-updating content.

### Home Page Queries

The home page (`00-Index/Home.md`) uses DataView queries instead of hardcoded lists.

**Active Projects (MOCs):**
```dataview
TABLE Key as "Description"
FROM "10-MOCs"
WHERE type = "moc"
SORT file.name ASC
```
- Lists all MOC pages
- Displays the `Key::` inline field from each MOC's TLDR callout
- Automatically updates when MOCs are added/removed

**Key Concept Hubs:**
```dataview
TABLE Key as "Description"
FROM "20-Hubs"
WHERE type = "hub"
SORT file.name ASC
```
- Lists all Hub pages
- Displays the `Key::` inline field from each Hub's TLDR callout
- Automatically updates when Hubs are added/removed

**Vault Statistics:**
```dataviewjs
const activeMocs = dv.pages('"10-MOCs"').where(p => p.type === "moc" && p.status === "active").length;
const hubs = dv.pages('"20-Hubs"').where(p => p.type === "hub").length;
const saplings = dv.pages('').where(p => p.tags && p.tags.includes("🌱")).length;
const ferns = dv.pages('').where(p => p.tags && p.tags.includes("🌿")).length;
const trees = dv.pages('').where(p => p.tags && p.tags.includes("🌲")).length;
```
- Counts active MOCs (status = "active")
- Counts all Hubs
- Counts notes by maturity (🌱 untested, 🌿 drawn on, 🌲 load-bearing)
- Updates automatically as the vault grows

### Key Benefits

- No manual updates needed when adding/removing/editing pages
- TLDR callouts serve as both human-readable summaries and queryable metadata
- Statistics always reflect current vault state
- Enforces consistency (missing TLDR callouts will be obvious in queries)

### Other Useful Queries

**List all notes by maturity:**
```dataview
TABLE type, tags
WHERE contains(tags, "🌱")
```

**Find untested notes in a hub's territory (e.g. before a writing project):**
```dataview
LIST used-by
WHERE contains(tags, "🌱") AND contains(topics, [[Hub Name]])
SORT file.name
```

**Show all literature notes with their sources:**
```dataview
TABLE source, Key
WHERE type = "literature-note"
SORT file.name
```

## Tagging Philosophy

**Tags represent note maturity, NOT concepts.**

This vault uses a three-level maturity system with emoji tags. Since 2026-07-13, maturity records **use, not structure** — the earlier growth-based definitions (bullet counts and connection counts) saturated once AI-assisted creation began birthing notes fully formed, and were retired. See [[Vault Rationale]] for the redesign record.

### Maturity Levels

A note's maturity is the number of **distinct consumers** that draw on it, where consumers are files in `10-MOCs/`, `50-Drafts/`, and `60-Analysis/`. Hubs are not consumers — hub membership is shelving, not use.

**🌱 Untested** - Never drawn on by higher-level work (0 consumers)
- Structurally complete but epistemically unproven: nothing has yet exercised its claims against real work
- The natural birth state of every note; not a backlog — the untested half of a Zettelkasten is its option value

**🌿 Drawn on** - Has fed at least one narrative (1–2 distinct consumers)
- Has been read critically and deployed at least once

**🌲 Load-bearing** - Supports multiple narratives (3+ distinct consumers)
- Repeatedly tested material the vault's higher-level work rests on

### Maturity Tag Update Policy (CRITICAL)

The emoji tag and the `used-by:` frontmatter field are a **computed cache**. Ground truth is the wiki-links in consumer files; `.claude/scripts/vault_maturity.py --write` recomputes and rewrites the cache deterministically.

- New notes are created as `tags: [🌱]`, `used-by: 0` — nothing else is ever hand-set
- Never hand-compute, upgrade, or downgrade a maturity tag; the reconcile script will overwrite manual changes
- Commands that create or edit MOCs, drafts, or analyses run the reconcile as their final step; `/vault-health` reconciles as backstop
- Backlinks, hub membership, and content edits do NOT change maturity — only being drawn on does
- Because usage is a historical fact recorded in links, maturity effectively never regresses in normal operation

Applies uniformly to notes, literature notes, hubs, and MOCs — there are no per-type criteria and no "hubs are always 🌲" rule.

### Maintenance Tags

Maintenance state lives in frontmatter `tags:` alongside the maturity emoji, disambiguated by an underscore prefix (the same shape as the tag conventions many people keep in a reference manager). Applied by the user's judgement or at their direction — never automatically. The health script inventories them each run.

**Vocabulary:**
- `_needs-zotero` — literature note created from an open-web source; import to Zotero when the canonical version is available
- `_needs-citations` — draft or note contains unsupported claims requiring literature
- `_stale` — long-untested note (🌱 under the usage model) flagged for review or removal
- `_superseded` — content replaced but kept for provenance

## File Naming Conventions

Use descriptive names, not numeric IDs (Obsidian's search makes IDs unnecessary).

### By Content Type

- **MOCs**: "Project Name" (no prefix - Obsidian highlighting distinguishes them)
- **Hubs**: "Concept Name" (no prefix - Obsidian highlighting distinguishes them)
- **Literature Notes**: Citation key format (e.g., `authorYearKeyword.md`)
- **Notes**: "Descriptive Title" (no prefix)
- **Templates**: "Template - Type" (prefix kept since they're not referenced in notes)

### Guidelines

- Use clear, descriptive names that indicate content
- Capitalize main words in titles
- No special characters except hyphens and question marks
- Obsidian's visual styling (via Supercharged Links plugin) distinguishes content types, not prefixes

## Obsidian-Specific Features

### Wiki-Links

Use wiki-links `[[Note Name]]` for all internal references, not standard markdown links.

**Basic link:**
```markdown
[[Note Title]]
```

**Link with display text:**
```markdown
[[Note Title|Display Text]]
```

**Embed note content:**
```markdown
![[Note Title]]
```

**Embed image:**
```markdown
![[Image.png]]
```

### Bidirectional Linking

All wiki-links automatically create bidirectional connections:
- Forward links appear in the note body
- Backlinks appear in Obsidian's backlinks pane
- Both are visible in the graph view

This enables emergent structure and serendipitous discovery.

### Graph View

The graph view visualizes the knowledge network:
- Nodes represent notes
- Edges represent links
- Clusters reveal conceptual areas
- Orphans (isolated nodes) indicate notes needing integration

Use graph view to:
- Identify clusters that need Hubs
- Find orphaned notes
- Visualize project boundaries (MOCs)
- Discover unexpected connections
