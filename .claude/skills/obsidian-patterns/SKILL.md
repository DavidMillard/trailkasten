---
name: obsidian-patterns
description: Efficient patterns for working with Obsidian vault using MCP tools. Use when searching the vault, finding connections between notes, exploring vault structure, identifying related content, or any task requiring vault exploration. Provides token-efficient alternatives to traditional Glob+Grep+Read patterns, reducing token usage by 60-75%.
---

# Obsidian Patterns

## Overview

When working with the Obsidian vault, use MCP tools (`mcp__obsidian__vault`, `mcp__obsidian__graph`, `mcp__obsidian__dataview`, `mcp__smart-connections`) instead of traditional file search patterns. These tools provide 60-75% token savings through progressive disclosure: search with ranked snippets → extract focused fragments → read full files only when necessary.

For **note-to-note similarity**, prefer `mcp__smart-connections__get_similar_notes` over keyword search — it returns ranked results with similarity scores without reading any files, enabling semantic triage in a single call.

**Context window principle**: Treat the context window as a public good. Load only what you need, when you need it.

## The Efficient Search Pattern

Follow this four-step pattern when searching the vault for connections or related content:

### 1. Search with Ranked Results

Use `mcp__obsidian__vault` with `action: search` to get an overview:

```
mcp__obsidian__vault:
  action: search
  query: content:"AI systems" OR content:"knowledge work"
  ranked: true
  includeSnippets: true
  searchStrategy: combined
  head_limit: 5
```

**Key parameters**:
- `ranked: true` - Enables TF-IDF relevance scoring
- `includeSnippets: true` - Returns contextual extracts (~500-1000 tokens)
- `searchStrategy: combined` - Searches both filenames and content
- `head_limit: 5` - Limits initial results to top 5 matches

**Output**: Ranked list with snippet previews showing context around matches

### 2. Review Snippets to Assess Relevance

Examine the returned snippets to identify which files are actually relevant. Snippets provide enough context to judge relevance without reading full files.

Identify the 3-5 most promising matches based on snippet content.

### 3. Extract Detailed Excerpts with Fragments

Use `mcp__obsidian__vault` with `action: fragments` on the top matches:

```
mcp__obsidian__vault:
  action: fragments
  path: 30-Notes/Relevant Note.md
  strategy: proximity
  maxFragments: 3
```

**Key parameters**:
- `strategy: proximity` - Gets context around relevant terms
- `maxFragments: 3` - Extracts 3 most relevant sections per file

**Output**: Focused excerpts (~1500-2000 tokens for 3-5 files) with surrounding context

### 4. Read Full Files Only When Necessary

After reviewing fragments, read 1-2 full files ONLY if you need:
- Complete context for decision-making
- Full structure understanding
- Detailed implementation specifics

Most connections and relationships can be identified from fragments alone.

## Token Savings Comparison

| Pattern | Operations | Approximate Tokens |
|---------|-----------|-------------------|
| **Traditional** | Glob (list 300+ files) + Grep (search all) + Read 5-10 full files | 15,000-30,000 |
| **MCP Efficient** | Search with snippets + fragments (3-5 files) + read 1-2 full files | 4,000-8,000 |
| **Savings** | Progressive disclosure pattern | **60-75%** |

## Tool Reference

### mcp__obsidian__vault

Primary tool for file operations and content search.

**Key actions**:

- `search` - Find files with ranked results and snippets
  - Use operators: `content:`, `file:`, `path:`, `tag:`
  - Combine with OR/AND, use "quoted phrases", /regex/
  - Set `ranked: true` for relevance scoring

- `fragments` - Extract relevant excerpts from files
  - `strategy: proximity` - Context around search terms
  - `strategy: semantic` - Thematically related content
  - `maxFragments` - Limit number of excerpts per file

- `list` - List files in directories
  - Use for getting file inventories without reading content

- `read` - Read complete files
  - **Requires `returnFullFile: true`** to get actual content — default now returns a summary view with no body
  - `raw: true` returns metadata only (not file content) — do not use for reading notes
  - The "Formatter error, showing raw data" label in output is a display artefact; the content field contains the full file text
  - Fallback after reviewing snippets and fragments

### mcp__obsidian__graph

Graph navigation for exploring connections.

**Key actions**:

- `neighbors` - Find directly connected notes (one hop away)
  - Efficient for understanding immediate relationships

- `backlinks` - Find notes linking TO a target note
  - Understand what references this concept

- `forwardlinks` - Find notes that the target links TO
  - Understand what this concept depends on

- `path` - Find shortest path between two notes
  - Discover connection chains

- `traverse` - Explore multi-hop connections
  - `maxDepth` - Control traversal depth
  - Use for broader network exploration

### mcp__obsidian__dataview

Query vault metadata and frontmatter.

**Key actions**:

- `query` - Execute DQL (Dataview Query Language) queries
  - List files by type: `LIST FROM "20-Hubs" WHERE type = "hub"`
  - Filter by metadata: `LIST FROM #tag WHERE status = "active"`
  - Extract fields: `TABLE author, year FROM "45-Literature"`
  - Efficient for metadata-based searches

### mcp__smart-connections

Embedding-based semantic similarity — finds conceptually related notes regardless of explicit links or shared vocabulary. Best for the **discovery/triage phase** when you have a source note and want to surface related content.

**Key actions**:

- `get_similar_notes` - Find notes semantically similar to a given note
  - `note_path` - Path to the source note (required)
  - `threshold` - Similarity cutoff (default 0.5; use 0.3 for broader results)
  - `limit` - Max results (default 10)
  - Returns paths + similarity scores without reading any files
  - **Best for**: "What's related to this specific note?"

- `get_connection_graph` - Build multi-level semantic connection graph from a note
  - `note_path` - Starting note (required)
  - `depth` - Levels to traverse (default 2)
  - `max_per_level` - Connections per level (default 5)
  - `threshold` - Similarity cutoff (default 0.6)
  - **Best for**: Exploring a conceptual neighbourhood beyond direct similarity — surfaces notes connected to notes connected to the source

**When to use which**:
- `get_similar_notes` — Single-hop discovery: "What's related to X?"
- `get_connection_graph` — Multi-hop exploration: "What's the broader conceptual neighbourhood around X?"

**`search_notes` usage rules** (free-text semantic search):
- **Requires warm-up**: Like the Obsidian MCP, smart connections may return empty results on the first call(s) in a session. Always make one warm-up call (e.g., `get_stats`) before relying on search results. If results are empty, retry once before concluding nothing matches.
- **Short queries only**: The small embedding model (`bge-micro-v2`, 384d) degrades sharply on multi-term queries. Use 2–3 focused terms, not kitchen-sink lists. Run multiple short queries rather than one long compound query.
  - ✅ `"information seeking"` → returns results
  - ❌ `"information seeking virtual reality immersion presence cognitive load"` → returns nothing
- **Prefer `get_similar_notes` when you have a source note** — it's more reliable than `search_notes` because it compares embeddings directly rather than embedding a free-text query.

**When to prefer over vault search**: When finding "what's conceptually related to this note?" — especially for notes with implicit connections not yet reflected in wiki-links.

## Smart Connections Failure Protocol

Smart Connections depends on a local embeddings model that may not always be running. When any `mcp__smart-connections__*` call fails or returns an error:

1. **Do NOT silently skip or fall back** — the user must decide
2. **Present the error and options:**
   ```
   Smart Connections returned an error — the local embeddings model may not be running.

   Would you like to:
   (a) Start it and retry
   (b) Continue without semantic search
   (c) Stop
   ```
3. **Only proceed based on user's choice**
4. **If user chooses (b)**: Note in any reports or output that semantic connections were unavailable (e.g., "Note: Semantic search was unavailable for this operation — connections are based on keyword and graph search only")

## Common Anti-Patterns

### ❌ DON'T: Glob + Grep + Read Multiple Files

```
1. Glob to list all files in 30-Notes/ (300+ files)
2. Grep to search all files for keywords
3. Read 5-10 full files
Token cost: 15,000-30,000 tokens
```

**Problem**: Loads entire file lists and reads many complete files unnecessarily.

### ✅ DO: Search + Fragments + Selective Read

```
1. Search with snippets (top 5 results)
2. Extract fragments from 3-5 relevant matches
3. Read 1-2 files if needed
Token cost: 4,000-8,000 tokens
```

**Benefit**: Progressive disclosure - only load what's needed at each step.

### ❌ DON'T: Read All Files to Find Connections

Reading 10-15 full files hoping to find relevant connections.

### ✅ DO: Use Graph Tools or Smart-Connections

- **Structural connections** (explicit links): `mcp__obsidian__graph` with `neighbors` or `backlinks`
- **Semantic connections** (conceptual similarity, regardless of links): `mcp__smart-connections__get_similar_notes`

Neither requires reading file content.

### ❌ DON'T: Search Then Immediately Read Everything

Getting search results and immediately reading all matching files.

### ✅ DO: Review Snippets First

Let snippets guide which files deserve full reads. Most decisions can be made from snippet context.

## Fallback Protocol (Traditional Tools Require User Approval)

Glob, Grep, and Read are **last-resort only**. Do not fall back silently.

**If any MCP tool fails:**

1. Identify which tool failed and note the error
2. Ask the user before proceeding:

   > `[Tool name]` returned an error — [brief reason if known].
   >
   > Would you like me to:
   > (a) Retry
   > (b) Continue with direct file tools (Grep/Read) — less token-efficient, may miss semantic connections
   > (c) Stop

3. Only use Grep/Glob/Read with explicit user approval
4. If user approves (b), note in any output that semantic search was unavailable

**Legitimate uses of traditional tools (no approval needed):**
- Reading a specific file at a known path (after triage has identified it)
- Writing or editing vault files (Write/Edit tools — not search tools)
- Working with files outside the vault structure (e.g. config files, templates being created)

## Integration with Agents

When spawning sub-agents via the Task tool, include efficient patterns in prompts:

```
**Suggested connections:**
- [[Hub 1]] - hub (from vault analysis)
- [[Related Note 1]] - related note: <relationship>

This eliminates redundant vault searches in the sub-agent.
```

Pass connection context discovered during your vault search to downstream agents to avoid duplicate work.

## Best Practices

1. **Start broad, narrow progressively**: Search → snippets → fragments → full read
2. **Stop when you have enough**: Don't read more files than necessary
3. **Use ranked search**: TF-IDF scoring surfaces most relevant matches first
4. **Leverage graph tools**: Direct connection discovery beats content search for relationships
5. **Query metadata**: Use dataview for type, tag, and frontmatter-based searches
6. **Pass context forward**: Share discovered connections with sub-agents to avoid duplicate searches
7. **Semantic triage with smart-connections**: For "what's related to this note?" tasks, call `get_similar_notes` first — similarity scores guide reading decisions before any file is opened. Complements graph tools (structural) with semantic discovery (conceptual).
