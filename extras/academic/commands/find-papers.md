---
description: Find relevant Zotero papers for vault notes and concepts using intelligent tag-based search
skills: obsidian-patterns, vault-writing-style, zettelkasten-methods, zotero-tag-vocabulary
argument: note name or concept
---

# Find Papers for Vault Concepts

Discovers relevant papers in the Zotero library for vault concepts using intelligent tag-based search with progressive query expansion.

## Skills Required

- **zotero-tag-vocabulary** - Tag vocabulary and concept-to-tag mappings
- **obsidian-patterns** - Efficient vault reading with MCP tools
- **zettelkasten-methods** - Understanding note structure and connections
- **vault-writing-style** - conventions for reporting results

## Critical Rules

1. **Use progressive query strategy** - Start specific, broaden if needed (0 results = valuable signal)
2. **Explain query expansion** - Show user why papers matched (transparency)
3. **Deduplicate results** - Remove duplicates across query levels
4. **Respect user agency** - Offer integration options, don't automatically modify notes
5. **Flag concerns** - Identify query issues (too broad/narrow, gaps) before presenting results

## Workflow

### Step 1: Accept Input and Read Note

**Input handling**:

The command accepts either a vault note name or a bare concept:
- `[[Note Name]]` or `Note Name` → Search vault and read note
- Bare concept (e.g., "intentional friction") → Use concept directly
- Ambiguous input → Ask for clarification

**Reading strategy** (following `obsidian-patterns`):

If input is a note name:
1. Use `mcp__obsidian__vault` with `action: search` to locate the note:
   ```
   action: search
   query: file:"Note Name"
   searchStrategy: filename
   ```

2. Use `mcp__obsidian__vault` with `action: fragments` to extract relevant content:
   ```
   action: fragments
   path: [path from search]
   strategy: adaptive
   maxFragments: 3
   ```

   This retrieves TLDR and first few Detail bullets (~500 tokens) without reading full file.

**If note doesn't exist**:
```
Note [[Note Name]] not found in vault.

Would you like me to:
1. **Search for similar notes** - Find related concepts
2. **Use as bare concept** - Search Zotero for "Note Name" directly
3. **Cancel** - Check the note name
```

### Step 2: Extract Concepts and Map to Tags

**From note content** (or bare concept):

1. Extract key terms from:
   - Note title
   - TLDR `Key::` field (if note)
   - First 3-4 Detail bullets (if note)
   - Connection descriptions (if note)
   - Bare concept text (if no note)

2. Use `zotero-tag-vocabulary` skill to:
   - Map concepts to known Zotero tags (concept-to-tag mappings)
   - Apply hierarchical expansion (e.g., `intentional friction` → also search `friction`)
   - Identify related tags (e.g., `friction` → also consider `disfluency`)
   - Determine relevant category tags (e.g., `HCI`, `game-design`)

3. Prepare three-level query strategy:
   - **Primary**: Specific tags + category constraint
   - **Broadened**: Related tags without category constraint
   - **Category-level**: Category + keyword search

**Example extraction**:
```
Input: [[Intentional Friction]]
→ Key terms: "intentional friction", "friction", "user experience", "HCI"
→ Specific tags: `intentional-friction`, `friction`
→ Related tags: `disfluency`, `designed-friction`
→ Categories: `HCI`, `game-design`
→ Query strategy:
   - Primary: "(intentional-friction OR friction) AND HCI"
   - Broadened: "friction OR disfluency OR designed-friction OR intentional-friction"
   - Category: tag="HCI" query="friction"
```

### Step 3: Execute Progressive Zotero Queries

**Three-level progressive strategy**:

#### Level 1: Primary Query (Most Specific)

Execute most specific query first:
```
mcp__zotero__zotero_search_items:
  tag: "(specific-tag OR related-specific-tag) AND category-tag"
  limit: 10
```

**Example**:
```
mcp__zotero__zotero_search_items:
  tag: "(intentional-friction OR friction) AND HCI"
  limit: 10
```

#### Level 2: Broadened Query (If <3 Results)

If primary query returns fewer than 3 results, broaden:
```
mcp__zotero__zotero_search_items:
  tag: "specific-tag OR related-tag-1 OR related-tag-2"
  limit: 10
```

**Example**:
```
mcp__zotero__zotero_search_items:
  tag: "friction OR disfluency OR designed-friction OR intentional-friction"
  limit: 10
```

#### Level 3: Category + Keyword (If Still <3 Results)

If still fewer than 3 results, use category with keyword:
```
mcp__zotero__zotero_search_items:
  tag: "category-tag"
  query: "concept-keyword"
  qmode: "titleCreatorYear"
  limit: 10
```

**Example**:
```
mcp__zotero__zotero_search_items:
  tag: "HCI"
  query: "friction"
  qmode: "titleCreatorYear"
  limit: 10
```

**Deduplication**:

After executing queries, deduplicate results across all levels by item key before presenting to user.

### Step 4: Rank and Present Results

**Relevance scoring** (for deduped results):

Score each paper based on tag specificity:
- **High relevance** (3 pts): Has specific tag (`intentional-friction`) that directly matches concept
- **Medium relevance** (2 pts): Has general tag (`friction`) + category tag (`HCI`)
- **Low relevance** (1 pt): Category only OR keyword match only (no tags)

**Fetch metadata for top results**:

For each unique item key (deduplicated), use `mcp__zotero__zotero_item_metadata` to get:
- Title
- Authors
- Year
- Citation key
- Tags (to explain relevance)

**Check vault for existing literature notes**:

For each result, search vault for literature note:
```
mcp__obsidian__vault:
  action: search
  query: file:"citation-key"
  searchStrategy: filename
```

**Presentation format**:

```markdown
## Papers Found for [[Concept Name]]

**Search strategy**: Expanded `[concept]` to tags: `tag-1`, `tag-2`, `tag-3` + category `category-tag`

**Results**: X papers found across Y query levels

### High Relevance (N papers)

1. **[Author Year]**: "[Paper Title]"
   - **Citation key**: `authorYearKeyword`
   - **Tags**: `specific-tag`, `category-tag`, `related-tag`
   - **Why relevant**: Directly discusses [specific aspect] in [context]
   - **Vault status**: ✓ Literature note exists: [[authorYearKeyword]]

2. [Continue for all high relevance papers...]

### Medium Relevance (N papers)

1. **[Author Year]**: "[Paper Title]"
   - **Citation key**: `authorYearKeyword`
   - **Tags**: `general-tag`, `category-tag`
   - **Why relevant**: Addresses [related aspect] in [category] context
   - **Vault status**: ✗ No literature note yet

[Continue for all medium relevance papers...]

### Low Relevance (N papers)

[Similar format, if any...]

---

**Query levels executed**:
- Level 1 (specific): X results
- Level 2 (broadened): Y additional results
- Level 3 (category): Z additional results
```

**If 0 results across all levels**:

```markdown
## No Papers Found for [[Concept Name]]

**Search strategy**: Tried tags `tag-1`, `tag-2`, `tag-3` across 3 query levels

### Research Gap Identified

No papers found in your Zotero library with these tags.

**This may indicate**:
1. **Research opportunity** - Concept not yet researched in this combination
2. **Tag vocabulary gap** - Papers exist but aren't tagged with these terms yet
3. **Terminology mismatch** - Papers use different terminology for this concept

**Suggestions**:
1. **Manual Zotero search** - Search abstracts for "[concept keywords]"
2. **Tag existing papers** - Run `/process-zotero-tags` to tag untagged papers
3. **Note the gap** - This could be a contribution opportunity for your research

Would you like me to:
- Search Zotero by keyword in abstracts? (may find untagged papers)
- Show papers from broader category `[category]` for context?
- Just note this as a research gap?
```

### Step 5: Critical Review (Value 6: Reciprocal Challenge)

**Before presenting results, check for concerns** (flag max 1-2):

| Concern | Detection Signal | Alternative Suggested |
|---------|-----------------|----------------------|
| **Query too narrow** | 0 results across all 3 levels | Suggest related concepts to search |
| **Query too broad** | 20+ results with many low-relevance | Suggest additional constraints (time period, sub-domain) |
| **Tag vocabulary gap** | Level 3 keyword search finds papers, but tag searches don't | Suggest running tagging workflow |
| **Note underdeveloped** | Note has <3 Details bullets or unclear Key | Suggest developing note first to clarify concept |
| **Generic category query** | Input is just "AI" or "HCI" | Ask user to narrow to specific sub-area |
| **All papers already processed** | Every result has literature note | Note that library already covers this well |

**If concern detected, add to presentation**:

```markdown
---

### Search Consideration

**Concern**: [Brief description of issue]

**Implication**: [What this means for results]

**Suggestion**: [Alternative approach]

Would you like me to:
1. [Option 1 - addressing concern]
2. [Option 2 - alternative strategy]
3. [Option 3 - proceed anyway]
```

**Examples**:

*Query too broad*:
```markdown
### Search Consideration

**Concern**: Query returned 25+ papers with many loosely related results.

**Implication**: May include papers where concept is mentioned but not central focus.

**Suggestion**: Narrow search to specific sub-area.

Would you like me to:
1. **Filter by sub-domain** - e.g., friction in game design specifically
2. **Show top 10 only** - Most relevant subset
3. **Refine concept** - What specific aspect of friction interests you?
```

*Tag vocabulary gap*:
```markdown
### Search Consideration

**Concern**: Found 0 papers with tag `intentional-friction` but keyword search for "intentional friction" finds 8 papers.

**Implication**: Papers exist but aren't tagged yet.

**Suggestion**: Run tagging workflow to tag these papers.

Would you like me to:
1. **Show keyword results** - Papers that mention "intentional friction"
2. **Run tagging workflow** - Use `/process-zotero-tags` on these papers
3. **Note for later** - Continue with current results
```

### Step 6: Optional Integration

**After presenting results, offer integration options**:

```markdown
---

## Next Steps

Would you like me to:

**A. Add to note** - Update [[Concept Name]] with findings
  - **Format option 1**: Static list with relevance annotations
  - **Format option 2**: DataView query (auto-updates as library grows)

**B. Create literature notes** - For papers without vault notes (X papers)

**C. Just reference results** - Use manually, no vault changes

**D. Refine search** - Adjust query strategy and search again
```

**If user chooses A (Add to note)**:

1. Ask which format:
   - **Static list**: Bulleted links with relevance notes (snapshot)
   - **DataView query**: Dynamic query that updates as library changes

2. Check note for `#human` tags in any section that would be modified

3. If no `#human` conflicts, proceed with chosen format:

**Static list format**:
```markdown
## Related Papers

High relevance:
- [[citationKey1]] - [Author Year]: Directly discusses [specific aspect]
- [[citationKey2]] - [Author Year]: Explores [related aspect]

Medium relevance:
- [[citationKey3]] - [Author Year]: Addresses [general topic] in [context]
```

**DataView format**:
```markdown
## Related Papers

```dataview
TABLE author, year, file.link as "Title"
FROM "45-Literature"
WHERE contains(tags, "friction") OR contains(tags, "intentional-friction")
SORT year DESC
```
```

**If user chooses B (Create literature notes)**:

For each paper without literature note:
1. Offer batch creation: "Create literature notes for X papers?"
2. If approved, use `/create-literature-note [citation-key]` for each
3. Report results

**If user chooses C or D**: Acknowledge and exit.

## Token Efficiency

**Estimated token usage** (~5000-6000 tokens total):
- Command overhead: ~400 tokens
- Skills loading (4 skills): ~2000 tokens
- Note reading (fragments): ~500 tokens
- Zotero queries (3 levels): ~1000-1500 tokens
- Metadata fetching (5-10 papers): ~1000 tokens
- Result presentation: ~1000 tokens

**Efficiency patterns used**:
- Use `fragments` not full file reads (60% savings on note reading)
- Progressive query execution (stop when enough results)
- Limit results to 10 per query level
- Deduplicate before fetching metadata (avoid redundant calls)
- Batch metadata fetches where possible

## Values Alignment

**Value 1 (Human Agency)**: User initiates search, reviews results, decides integration approach

**Value 2 (Transparency)**: Query expansion logic explained, relevance scoring visible, tag mappings shown

**Value 3 (Beneficial Friction)**: Approval point for integration creates steering opportunity

**Value 4 (Augmentation)**: Command discovers connections, doesn't make decisions

**Value 6 (Reciprocal Challenge)**: Flags query issues (too broad/narrow, gaps), suggests alternatives

**Value 8 (Provenance)**: Links papers to citation keys, maintains vault-to-Zotero traceability

## Edge Cases

### No Note Found
If note name doesn't exist, offer to search for similar notes or use as bare concept.

### Generic Category Input
If input is just a category (e.g., "AI"), warn about breadth and ask for sub-area:
```
"AI" is a broad category (50+ papers). Which aspect interests you?
- AI safety and alignment
- AI-assisted writing
- AI in education
- AI ethics
- General AI capabilities
```

### Multi-Domain Concept
If concept spans multiple domains (e.g., "AI writing education"), include all relevant categories:
```
Concept spans multiple domains:
- AI: AI-assisted writing, LLMs
- e-learning: Pedagogy, learning theory
- HCI: User interfaces, writing tools

Searching across AI + e-learning + HCI categories...
```

### All Results Have Literature Notes
If every result already has a literature note, flag this positively:
```
Good news: Your vault already has literature notes for all matching papers!

This suggests:
- You've thoroughly processed papers in this area
- Your library is well-covered for this concept
- May be time to synthesise into MOC or draft
```

### No Literature Notes Exist
If no results have literature notes, suggest batch creation:
```
None of these papers have literature notes yet.

Would you like me to create literature notes for high-relevance papers (X papers)?
This will extract key concepts and integrate into vault structure.
```

## Example Usage

```
/find-papers "Intentional Friction"
/find-papers [[Hypertext as Method]]
/find-papers "AI alignment"
/find-papers [[Emergent Narrative]]
```

## Follow-Up Commands

After `/find-papers`, user might want to:
- `/create-literature-note [citation-key]` - Process specific paper
- `/create-note` - Extract concept from paper
- `/create-hub` - Create thematic organization for paper cluster
- `/ingest-resource` - Process paper PDF or transcript

## Future Extensions

**Potential enhancements** (not implemented yet):
- `/suggest-papers-for-hub` - Hub-level discovery (aggregate tags from hub notes)
- `/validate-tags` - Check tag vocabulary consistency across library
- `/tag-recommendations` - Suggest tags for untagged papers based on abstracts
- `/find-gaps` - Identify under-researched intersections in library
