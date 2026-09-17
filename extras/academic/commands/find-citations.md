---
description: Find appropriate Zotero citations for text with \cite{PLACEHOLDER} markers
skills: obsidian-patterns, zotero-tag-vocabulary, vault-writing-style
argument: inline text block with \cite{PLACEHOLDER} markers
---

# Find Citations for Placeholders

Analyses text with `\cite{PLACEHOLDER}` markers, maps each to vault concepts and Zotero papers, and recommends citations with confidence ratings.

## Skills Required

- **obsidian-patterns** - Efficient vault reading with MCP tools
- **zotero-tag-vocabulary** - Tag vocabulary and concept-to-tag mappings
- **vault-writing-style** - the vault's writing conventions

## Critical Rules

1. **Claim-level precision** — each placeholder supports a specific claim in the sentence; match the citation to the claim, not just the topic
2. **Vault first, Zotero second, training knowledge third** — this ordering minimises token cost and maximises relevance
3. **Use MCP fragments where possible** — fall back to direct reads only if MCP is unavailable
4. **Never auto-substitute** — produce the recommendation table; user copies citation keys manually
5. **Distinguish three statuses clearly** — In Zotero + vault, In Zotero only, Not in Zotero

## Workflow

### Step 1: Parse Placeholders

Extract all `\cite{PLACEHOLDER}` markers from the input text. For each, record:
- The placeholder name
- The surrounding sentence/clause (the specific claim it supports)

Present a brief summary: "Found N placeholders: PLACEHOLDER_1, PLACEHOLDER_2, ..."

### Step 2: Map Placeholders to Vault Notes

For each placeholder, attempt to find a matching vault note:

1. **Direct name match** — search `30-Notes/` for the placeholder name (e.g., `COGNITIVE_OFFLOADING` → `Cognitive Offloading.md`)
2. **Fuzzy match** — if no direct match, try variants (spaces, hyphens, title case)
3. **No match** — flag as "no vault note" and proceed to Step 3 with the placeholder name as a bare concept

Read matched notes using MCP fragments (TLDR + first details + references section). The references section is critical — it often names the exact papers needed.

### Step 3: Search for Citations

For each placeholder, follow this priority order:

**3a. Check references in vault note**
If the note's References section names specific papers (e.g., `[[citationKey]]` or author/title), search Zotero for those first. These are the highest-confidence candidates — the vault has already identified them as relevant.

**3b. Search Zotero by concept tags**
Use `zotero-tag-vocabulary` to map the placeholder concept to Zotero tags. Execute progressive query strategy (specific → broadened → category+keyword). Limit to 5 results per level.

**3c. Assess training knowledge for gaps**
If Steps 3a–3b produce no candidate with good or high confidence for a placeholder, assess whether training knowledge can identify a well-known paper that fits the specific claim. If so, include it as a "Not in Zotero" recommendation.

### Step 4: Evaluate Candidates

For each candidate paper, assess:

- **Claim fit** — does this paper actually argue/evidence the specific claim in the sentence? (not just discuss the topic)
- **Status** — check whether it exists in Zotero (found via search) and whether a vault literature note exists (search `45-Literature/` for citation key)
- **Confidence** — rate as High / Good / Moderate / Low based on claim fit:
  - **High** — paper directly argues or evidences the claim
  - **Good** — paper substantially addresses the claim as part of a broader argument
  - **Moderate** — paper is topically relevant but doesn't directly make this point
  - **Low** — best available but weak fit; gap identified

### Step 5: Compile Output

Output is grouped by effort level, with quick wins last (most visible in terminal). Each section uses the same three-column table format.

#### Citation key conventions

- **Citation key known** (paper has a vault literature note in `45-Literature/`): use the citation key directly, e.g. `nelsonComplexInformation1965`. The presence of a bare citation key signals "already in Zotero, ready to use."
- **Citation key unknown** (paper is in Zotero but has no vault literature note): use `item ITEMKEY` after the short reference, e.g. `item PVKBBAER`. This signals "in Zotero, but user needs to look up the citation key."
- **Not in Zotero**: no key at all — provide author, year, title, venue so user can find and import it.

IMPORTANT: The Zotero MCP does not expose BetterBibTeX citation keys. Only use a citation key if you have confirmed it from a vault literature note filename in `45-Literature/`. Never fabricate plausible citation keys.

#### Vault column values

- `Already in vault` — literature note exists in `45-Literature/`
- `No — worth creating` — paper is substantive enough to warrant a vault literature note
- `Not needed — citation only` — paper serves as a citation source but doesn't need vault integration
- `Yes — if you adopt it` — for Add to Zotero papers where a vault entry would follow

#### Output sections

Present sections in this order (user sees bottom first in terminal):

**1. "Add to Zotero"** (most effort — shown first/top)

Only present if there are papers not in Zotero. Table format:

| Placeholder | Paper | Vault |
|---|---|---|
| `PLACEHOLDER_NAME` | Author (Year). "Title." *Venue*. | Vault status |

**2. "Ready to cite"** (least effort — shown last/bottom)

Papers already in Zotero. Table format:

| Placeholder | Paper | Vault |
|---|---|---|
| `PLACEHOLDER_NAME` | Author (Year). "Title." *Venue*. `citationKey` or `item ITEMKEY` | Vault status |

**3. "Notes"** (after the tables)

Brief notes covering:
- Rationale for recommendations where choice is non-obvious
- Which paper is the stronger fit when multiple candidates exist
- Gap issues or authorial contribution flags (see Step 6)

Keep to one line per paper. Do not repeat information already visible in the tables.

Multiple citations per placeholder are appropriate when the text warrants it.

### Step 6: Gap Summary and Authorial Contribution Check

For any placeholder where no candidate reaches Good confidence, include in the Notes section:

**Authorial contribution signals** — check the claim language for:
- Definitional or coining language ("a new kind of", "we propose", "what we term")
- Italicisation or capitalisation of novel terminology
- Framing that positions the concept as this work's contribution

**Two outcomes:**

- **Novel framing + no strong candidate**: Flag as likely authorial contribution. Recommend removing the citation marker or replacing with self-citation if the concept is published elsewhere.
- **Novel framing + strong candidate found at earlier steps**: Flag the tension. "You've framed this as novel, but [Author (Year)] substantially defines this concept. Consider citing them or differentiating your framing." This is a genuine reciprocal challenge — prior art the author may have missed.

If neither applies (weak results but no novelty signals), provide standard gap analysis:
- What kind of source would strengthen the citation
- Specific recommendations from training knowledge (with full bibliographic detail)
- Whether the gap suggests a research contribution opportunity

## Token Efficiency

- MCP fragments for vault reads (~500 tokens per note vs ~2000 for full read)
- Vault note references checked before any Zotero search (often resolves immediately)
- Progressive Zotero queries — stop when strong candidate found
- Batch metadata fetches in parallel
- No full text reads — metadata and abstracts suffice for citation fitness

## Example Usage

```
/find-citations Personal note-taking and scholarly writing are cognitively demanding
practices in which composing text is inseparable from thinking, yet contemporary
large language models increasingly invite us to delegate this labour to machines.
\cite{COGNITIVE_OFFLOADING}\cite{DESKILLING}
```
