# Zettelkasten Methodology

Comprehensive guide to content organization, linking strategies, and workflows.

## Navigation Flow

The vault structure creates multiple entry points and navigation paths:

```
Home (00-Index/Home.md)
    ↓
    ├─→ Research Programme (00-Index/) - The persistent questions, one page
    │       ↓
    │       └─→ MOCs (10-MOCs/) and Hubs (20-Hubs/) that operationalise each question
    │
    ├─→ MOCs (10-MOCs/) - Project entry points
    │       ↓
    │       ├─→ Notes (30-Notes/)
    │       └─→ Drafts (50-Drafts/) - Synthesised writing projects
    │
    ├─→ Hubs (20-Hubs/) - Conceptual entry points
    │       ↓
    │       └─→ Notes (30-Notes/)
    │
    ├─→ Resources (40-Resources/) - Raw materials
    │       ↓
    │       └─→ Notes (30-Notes/) - Atomic concepts extracted from resources
    │
    ├─→ Literature (45-Literature/) - Academic papers
    │       ↓
    │       └─→ Notes (30-Notes/) - Atomic concepts spawned from papers
    │
    └─→ Notes (30-Notes/) - Atomic concepts
            ↓
            └─→ Drafts (50-Drafts/) - Synthesised writing projects
```

The programme layer points *downward only*: notes and MOCs carry no metadata pointing back up at it (see Research Programme, below).

## Linking Principles

Links form the connective tissue of the knowledge graph. Follow these principles:

1. **Notes → Notes**: Direct links for related ideas (most important for discovery)
2. **Notes → Hubs**: Every note should link to 1-3 relevant hubs
3. **Notes → Literature**: Atomic notes link to source papers in References section
4. **Literature → Literature**: Papers link to related papers they cite or are cited by
5. **Hubs → Notes**: Hubs list relevant notes under their domain
6. **MOCs → Notes**: MOCs link to notes relevant to the project
7. **MOCs → Hubs**: MOCs reference hubs for broader context
8. **Hubs ↔ Hubs**: Related hubs link to each other
9. **Drafts → Notes**: Drafts link to source notes they synthesise
10. **Drafts → MOCs**: Drafts often relate to specific projects or MOCs
11. **Research Programme → MOCs and Hubs**: the programme page links *down* to the artefacts operationalising each question. Nothing links back up: there is no per-note problem metadata (see below).

### No `problems:` Field

An earlier design gave every note a `problems:` frontmatter field naming the research question it served, with a `05-Problems/` folder behind it. Both were removed. Persistent questions live on a single curated page instead, [[Research Programme]] (`00-Index/`).

**Do not reintroduce per-note problem metadata**, and do not propose it as an improvement. The mechanism failed on the side-effect-value principle: tagging a note with a problem has no value at the moment of tagging, so hardly any notes ever carried the field, and the Dataview queries that depended on it returned almost nothing. What a programme covers is instead readable from the MOCs and hubs it links to, which the MOC workflow already maintains.

**The reflection step**: when creating or substantially expanding a MOC, ask the user whether it fits an existing programme, extends one, or implies a new one (which forces a displacement, since the page is capped at ~12). See SKILL.md, Research Programme.

## Hybrid Literature → Atomic Note Workflow

The vault combines comprehensive literature notes with atomic concept notes.

> **Academic tier.** `45-Literature/` and the `/create-literature-note`,
> `/find-papers`, `/find-citations` and `/evaluate-papers` commands belong to the
> optional academic tier and require a Zotero library plus the `zotero-mcp`
> server. Install them with `/setup`, or copy them from `extras/academic/`. The
> literature-note *content type* below is worth understanding either way —
> nothing stops you writing one by hand — but the commands will not exist until
> the tier is installed.

### Step 1: Create Literature Note

Located in `45-Literature/`, use `/create-literature-note <citation-key>` command to:
- Auto-populate from Zotero library
- Include metadata, abstract, AI analysis
- Serve as bibliographic reference and entry point
- **CRITICAL**: AI Analysis section MUST include inline links to existing atomic notes

### Step 2: Extract Atomic Concepts

Create separate atomic notes in `30-Notes/`:
- Identify 2-5 key concepts from the Literature Note worth developing
- Write each concept in your own words
- Link back to Literature Note in References section
- Literature Note automatically tracks these via DataView backlinks

### Step 3: Enrich Literature Note with Inline Links

**CRITICAL STEP** - Return to the Literature Note's AI Analysis section:
- Add inline links `[[Note Name]]` or `[[Note Name|display text]]` to connect key contributions to existing notes
- Explain how each contribution relates to your existing knowledge
- Creates a richly interconnected knowledge graph

**Example inline linking:**
- "This connects to [[The Thief of Reason]] - when AI erases the thinking process..."
- "[[Cognitive Offloading Mediates AI Impact on Critical Thinking|cognitive offloading]]"
- "This aligns with [[System 1 vs System 2 Task Division]]"

### Step 4: Connect to Knowledge Network

- Link atomic notes to relevant Hubs
- Link to related atomic notes from other papers
- Build citation network by linking Literature Notes to each other

### Example Workflow

1. Read Atzenbeck (2024) on AI ethics
2. Create `45-Literature/atzenbeckUnwindingAIsMoral2024.md` via `/create-literature-note`
3. Extract concepts: `System 1 vs System 2 Tasks`, `Hypertext as Ethical Framework`, `AI Moral Agency`
4. Each becomes atomic note in `30-Notes/` linking back to Atzenbeck paper
5. **Return to literature note and add inline links in AI Analysis section**
6. Link to existing notes on AI ethics, link to `[[Artificial Intelligence]]` hub

## Content Type Details

### Research Programme - Expanded

The persistent intellectual questions — roughly twelve, curated by the user — live on one page: `00-Index/Research Programme.md`. There is no problem folder, no problem template, and no per-note problem metadata; all three were retired on 2026-07-13 (see "No `problems:` Field" above).

**Structure** (the health script parses this shape — keep it):
- `## Active Programmes`, then one `### N. The question?` heading per programme
- Under each: a sentence or two, then **MOCs**, **Hubs** and **Anchors** lines of wiki-links
- `## Emeritus` at the foot, same shape, for retired questions

**Liveness is computed, never stored.** `/vault-health` reports the newest content in each programme's territory (its MOCs, its anchor notes, and what they draw on) and flags any that has gained nothing in twelve months, asking once whether it is still live.

**Maintenance is a side-effect of MOC work** — the reflection step, not a scheduled review. See SKILL.md, Research Programme.

### MOCs - Expanded

Located in `10-MOCs/`, MOCs are narrative synthesis documents:

**Purpose:**
- Tell a narrative story connecting related notes
- Synthesize insights across a topic or project area
- Focus on conceptual synthesis: explaining how notes relate and building coherent understanding

**Characteristics:**
- More dynamic and temporal than Hubs (tied to projects or learning journeys)
- Examples: "Building a Second Brain", "AI Research Project"
- Typically contain 15-25 links maximum, woven into a narrative rather than listed
- Include minimal project tracking (current focus) but avoid excessive checklists or resource lists

**Status field:**
- `active` - Currently working on
- `on-hold` - Paused temporarily
- `completed` - Finished project

**Template**: `[[Template - MOC]]`

### Framework Notes vs MOCs

A small, **claim-bearing** cluster is an atomic *framework note* in `30-Notes/`
(`type: note`) — not a MOC, and not a new type. The discriminant is
**navigation-load**, not size alone: a 4–5 note cluster expressing a single
structural claim is a note; a 20-note territory a reader needs guiding through
is a MOC.

**Linking rule.** Link a framework note only when you mean *the structural
distinction it draws*. Never route links through it to reach its members — that
creates a hub-and-spoke bottleneck and loses the specificity that made the
member notes worth writing. Prefer precise note-to-note links.

**Two genres of staleness**, which must be treated differently:
- **Argumentative MOCs are curated snapshots.** Selective by design. A new
  related note does *not* oblige an update.
- **Framework and structure notes claim local completeness.** A missing sibling
  is a genuine defect.

### Hubs - Expanded

Located in `20-Hubs/`, Hubs are evergreen conceptual anchors:

**Purpose:**
- Organize notes by theme or domain
- Provide stable, permanent entry points to conceptual areas

**Characteristics:**
- More stable and permanent than MOCs
- Examples: "Personal Knowledge Management", "Artificial Intelligence"
- Link primarily to Notes, can reference other Hubs
- Domain-focused rather than project-focused

**When to create:**
- Notice cluster of related notes forming around a concept
- A Hub is getting too large and needs sub-Hubs
- A distinct conceptual domain emerges

**Template**: `[[Template - Hub]]`

### Literature Notes - Expanded

Located in `45-Literature/`, Literature Notes are comprehensive paper records:

**Purpose:**
- Comprehensive representations of academic papers, books, and research articles
- Serve as bibliographic references and sources for atomic notes
- Entry points for exploring research

**Structure:**
- Full metadata (authors, title, venue, DOI, abstract, URL)
- AI-generated analysis identifying key contributions
- Links to related papers in your library
- Named using citation keys (e.g., `atzenbeckUnwindingAIsMoral2024.md`)

**Critical requirement:**
- AI Analysis section MUST include inline links `[[Note Name]]` to connect key contributions to existing atomic notes in your vault
- This creates the richly interconnected knowledge graph

**Creation:**
- Created via `/create-literature-note <citation-key>` command
- Pulls metadata and full text from Zotero library
- Automatically generates AI analysis

**Template**: `[[Template - Literature Note]]`

### Notes - Expanded

Located in `30-Notes/`, Notes are atomic Zettelkasten notes:

**Purpose:**
- Individual atomic ideas following Zettelkasten principles
- Building blocks of knowledge synthesis

**Characteristics:**
- One idea per note, self-contained but richly linked
- Often spawn from Literature Notes or Resources but synthesize concepts in your own words
- Link back to source Literature Notes or Resources in References section
- Should link to 1-3 relevant hubs

**Maturity criteria (usage model, 2026-07-13):**
- 🌱 Untested: never drawn on by a MOC, draft, or analysis (0 consumers)
- 🌿 Drawn on: has fed at least one narrative (1–2 distinct consumers)
- 🌲 Load-bearing: supports multiple narratives (3+ distinct consumers)
- Tags are a computed cache owned by `vault_maturity.py` — never hand-set (see conventions.md)

**Template**: `[[Template - Zettel Note]]`

### Resources - Expanded

Located in `40-Resources/`, Resources are raw materials:

**Purpose:**
- Raw materials like AI conversations, transcripts, articles, podcasts
- Processing artifacts that serve as sources for atomic notes

**Characteristics:**
- Include metadata (source, date, format) and content summary
- Processed via `/ingest-resource` command to extract atomic notes
- Tagged with `resource-type` for subcategorization (conversation, transcript, article, podcast, video)

**Workflow:**
1. Resource created in `40-Resources/` with metadata
2. Agent analyzes and presents suggestions for atomic notes
3. You review and approve specific suggestions
4. Approved notes created with connections
5. Resource file updated with processing notes

**Template**: `[[Template - Resource]]`

### Drafts - Expanded

Located in `50-Drafts/`, Drafts are writing projects:

**Purpose:**
- Writing drafts for various projects (blog posts, articles, papers, etc.)
- Synthesise ideas from multiple Zettelkasten notes into coherent texts

**Characteristics:**
- Minimal markdown formatting for easy export to other platforms
- Track source notes, revisions, and publishing status
- Status field: in-progress, completed, or published

**Creation:**
- `/create-draft <note-or-moc-name>` - Register follows the destination you name

**Template**: `[[Template - Draft]]`

## Why Links Over Tags for Concepts

The vault uses links for concepts, NOT tags. Tags represent maturity only.

**Benefits of links over tags:**

1. **Bidirectional connections** - Obsidian's backlinks show all notes mentioning a concept
2. **Flexible organization** - Same note can relate to multiple hubs without forced categorization
3. **Emergent structure** - Links can be created before hub pages exist
4. **Context preservation** - Links show how concepts relate in context, not just that they exist
5. **Graph visualization** - Concept relationships visible in graph view

**Old approach (avoid):**
```yaml
tags: [ai, machine-learning, pkm]  # Concept tags
```

**New approach:**
```yaml
tags: [🌲]  # Maturity status only
```
```markdown
Concepts indicated by hub links in the note body:
- [[Artificial Intelligence]]
- [[Personal Knowledge Management]]
```
