---
description: Evaluate papers for vault contribution value. Provide a list of papers, a file path, or pull from Zotero queue.
skills: research-paper-evaluation, obsidian-patterns, zotero-tag-vocabulary
argument: (optional) number of Zotero papers to evaluate, or a file path (.txt/.md) containing a paper list
---

# /evaluate-papers

Evaluate a set of papers against the vault's knowledge needs and recommend which are worth adding. Reports recommendations with reasoning — does not modify the vault or library.

## Usage

```
/evaluate-papers
/evaluate-papers 15
/evaluate-papers 40-Resources/my-reading-list.md
/evaluate-papers /path/to/papers.txt
```

Then either:
- Paste a list of papers (titles, abstracts, URLs from any source)
- Provide a file path argument — the command reads the file and parses its contents as the paper list
- Or provide nothing — the command pulls from Zotero's `_to-evaluate` queue

## Skills Required

- **research-paper-evaluation** — Value tiers, evaluation criteria, vault scope, report format
- **obsidian-patterns** — Efficient vault scanning for connection candidates
- **zotero-tag-vocabulary** — Tag vocabulary for Zotero duplicate checking

## Three Modes of Operation

### Mode 1: External List

User provides a list of papers from any source (Google Scholar alerts, reading lists, conference proceedings, colleague recommendations). Papers may include any combination of title, authors, year, abstract, and URL.

**Trigger**: User pastes paper information after invoking the command.

### Mode 2: File Input

User provides a path to a `.txt` or `.md` file containing a list of papers. The file is read and its contents treated identically to a pasted list (Mode 1).

**Trigger**: Argument is a file path (contains `/` or ends in `.txt` or `.md`).

**Path resolution**:
- Absolute paths (`/Users/...`) → use as-is with the `Read` tool
- Relative paths or vault-relative paths (`40-Resources/list.md`, `papers.txt`) → resolve relative to the vault root

**Trigger**: User provides a file path argument.

### Mode 3: Zotero Queue

No list provided. Pull papers from Zotero that have been tagged `_to-evaluate`.

**Trigger**: User invokes command without pasting papers or a file path, or provides only a number.

**Parameters**:
- No argument → pull 10 papers from `_to-evaluate` queue
- Number argument → pull that many papers

## Workflow

### Phase 1: Determine Mode and Gather Papers

**If argument is a file path (Mode 2 — File Input)**:
1. Determine the full path:
   - If the argument starts with `/`, use it as an absolute path
   - Otherwise, treat it as relative to the vault root (the directory Claude Code was started in)
2. Read the file using the `Read` tool
3. If the file cannot be read, inform the user:
   ```
   Could not read file: <path>
   Please check the path and try again, or paste the paper list directly.
   ```
4. Treat the file contents as if the user had pasted them — proceed as Mode 1 below

**If user provides a list (Mode 1 — External List)**:
1. Parse the provided papers — be flexible about format (structured lists, pasted alerts, BibTeX, plain text)
2. Extract: title, authors, year, abstract, URL for each paper
3. Proceed to Phase 1.5 to classify each paper's abstract quality

**If no list provided (Mode 3 — Zotero queue)**:
1. Search for papers with `_to-evaluate` tag:
   ```
   mcp__zotero__zotero_search_items(query: "", tag: "_to-evaluate", limit: batch-size)
   ```
2. If no papers found, inform user:
   ```
   No papers in the evaluation queue. Add `_to-evaluate` tag in Zotero to queue papers,
   or paste a list of papers directly.
   ```
3. Fetch metadata for each paper using `zotero_item_metadata`
4. For papers without abstracts: fetch using `zotero_item_fulltext` via Haiku subagent (same pattern as process-zotero-tags)

### Phase 1.5: Detect Snippet-Only Papers (Modes 1 and 2 only)

For each paper parsed in Mode 1, classify its Abstract field using this logic:

```python
def is_snippet(abstract: str) -> bool:
    if not abstract:
        return True
    s = abstract.strip()
    if len(s) < 250:
        return True
    if s.endswith(('...', '…')):
        return True
    return False
```

Mark each paper internally as `snippet_only = True` or `snippet_only = False`.

Papers from Zotero (Mode 3) skip this step — they always have full abstracts; treat all as `has_abstract`.

### Phase 2: Prepare Vault Context

Before evaluating, gather vault context to ground the assessment:

1. **Scan vault for current concept coverage**:
   Use `mcp__obsidian__vault` search to get a snapshot of existing notes, hubs, and MOCs:
   ```
   action: list
   directory: 30-Notes
   ```
   ```
   action: list
   directory: 20-Hubs
   ```
   ```
   action: list
   directory: 10-MOCs
   ```

   This provides the concept landscape for assessing connection potential. Keep the file listing in context — do not read individual files unless needed to resolve a specific connection question.

2. **Check Zotero for duplicates** (both modes):
   For each paper being evaluated, search Zotero by title or DOI:
   ```
   mcp__zotero__zotero_search_items(query: "<paper title or key terms>", qmode: "titleCreatorYear", limit: 3)
   ```
   Flag any papers already in the library.

### Phase 3a: Preliminary Triage

For each paper, apply the evaluation criteria (vault scope, key test, value tier) using whatever information is currently available:

- `has_abstract` papers → use title + full abstract
- `snippet_only` papers → use title + short snippet

Produce a **preliminary tier** (Add / Consider / Skip) per paper. Do not present this to the user — it is an internal staging step only.

### Phase 3b: Enrich Snippet-Only Survivors via OpenAlex (Modes 1 and 2 only)

For every paper where `preliminary_tier ∈ {Add, Consider}` AND `snippet_only = True`, fetch the full abstract via OpenAlex.

Run the following script inline via a Bash heredoc. Process papers **sequentially** with a 0.3s delay — do **not** fan out to parallel subagents (free API rate limits).

```python
import urllib.request
import urllib.parse
import json
import time
import sys

# OpenAlex asks API users to identify themselves; in return you get the faster
# "polite pool". Put your own address here — it is sent with every request.
POLITE_EMAIL = "your.email@example.com"
DELAY = 0.3

def reconstruct_abstract(inverted_index):
    """OpenAlex returns abstracts as {word: [positions]}; reconstruct linearly."""
    if not inverted_index:
        return None
    positions = []
    for word, indices in inverted_index.items():
        for pos in indices:
            positions.append((pos, word))
    positions.sort()
    return " ".join(word for _, word in positions)

def fetch_abstract(title, year=None):
    """Returns dict with 'abstract' key (str or None), plus doi, openalex_url, source."""
    params = {
        "search": title,
        "per-page": "3",
        "select": "title,abstract_inverted_index,doi,id,publication_year",
        "mailto": POLITE_EMAIL,
    }
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"evaluate-papers ({POLITE_EMAIL})"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as e:
        return {"abstract": None, "error": str(e)}

    results = data.get("results", [])
    norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
    for r in results:
        if norm(r.get("title", ""))[:80] == norm(title)[:80]:
            abstract = reconstruct_abstract(r.get("abstract_inverted_index"))
            if abstract:
                return {
                    "abstract": abstract,
                    "doi": r.get("doi"),
                    "openalex_url": r.get("id"),
                    "source": "openalex",
                }
    return {"abstract": None, "error": "no_match"}

# stdin: JSON list of {title, year} for snippet_only Add/Consider papers
papers = json.load(sys.stdin)
results = {}
for i, p in enumerate(papers):
    if i > 0:
        time.sleep(DELAY)
    print(f"[{i+1}/{len(papers)}] {p['title'][:60]}", file=sys.stderr)
    results[p["title"]] = fetch_abstract(p["title"], p.get("year"))

print(json.dumps(results, indent=2))
```

**After enrichment**, for each paper:

- If `abstract` is non-null: replace the snippet in the working data with the full abstract; update URL if `doi` or `openalex_url` was returned.
- If `abstract` is null: keep the snippet; mark paper with `enrichment_failed = True` so Phase 3c knows the abstract is still a snippet.

### Phase 3c: Final Evaluation

Re-evaluate any paper whose abstract was just enriched in Phase 3b — the tier may change (e.g. Consider → Add, or even Skip → Consider) once the full text is available.

For all other papers (has_abstract from the start, or enrichment_failed), carry their preliminary tier forward.

Then apply the full evaluation criteria from the `research-paper-evaluation` skill:

1. **Check vault scope** — Does it connect to at least one of the 9 research domains?
2. **Apply the key test** — Can I point to a vault concept this would enrich, or a new concept it would justify?
3. **Determine value tier** — Add / Consider / Skip
4. **Identify value type** — Foundational, Framework, Empirical, Bridge, Novel concept, Background, etc.
5. **Check connection potential** — Which existing vault notes/hubs/MOCs does it connect to? Verify these exist using the vault listing from Phase 2.
6. **For Consider papers** — Add actionable guidance: what would tip it to Add?

**Publication status checks**:

- **arXiv preprints**: Flag with `⚠️ arXiv preprint — not peer-reviewed`. Default recommendation is Skip unless the paper is genuinely exceptional (widely cited, no peer-reviewed equivalent for an important concept). Apply this conservatively.
- **Working papers** (government, think tank, institutional reports): Flag similarly with `⚠️ Working paper — not peer-reviewed`. Same conservative default.
- **Suspicious papers**: Flag any paper that appears to be promotional material, has implausible authorship claims, or is not genuine academic work.

**Zotero library status**:

- If a paper is already in the Zotero library, note this: `Already in Zotero library`
- If a paper already has `_tagged` marker, note: `Already in Zotero, tagged`
- This information is relevant but does not determine the recommendation — a paper can be in Zotero for library purposes without being worth bringing into the vault.

### Phase 4: Present Detailed Evaluation

Present the full evaluation organised by recommendation tier, following the report format from `research-paper-evaluation` skill:

```markdown
## Recommended: Add

**[Title]** — Author(s), Year
📖 enriched via OpenAlex          ← only when abstract was fetched in Phase 3b
Value type: Foundational | Framework | Empirical | Bridge | Novel concept
Reasoning: <1-2 sentences on why this paper earns its place>
Connects to: <verified vault concepts or notes>

## Recommended: Consider

**[Title]** — Author(s), Year
📖 enriched via OpenAlex          ← only when abstract was fetched in Phase 3b
⚠️ [any flags: arXiv, working paper, already in Zotero]
Value type: Background | Secondary source | Narrow empirical | Methodological
Reasoning: <why borderline — what it offers and what it lacks>  (snippet only — could not retrieve abstract)  ← append when enrichment_failed=True
Connects to: <relevant vault concepts, if any>
Tip: <what would move this to Add>

## Recommended: Skip

**[Title]** — Author(s), Year
Reason: Out of scope | Redundant | Too narrow | Insufficient information | arXiv default
```

For arXiv papers that are all Skip, group them concisely (as in the example session) rather than giving each a full entry.

### Phase 5: Summary Table

After the detailed evaluation, present a summary table of ALL papers:

```markdown
## Summary

| # | Paper | Recommendation | Flags | URL |
|---|-------|---------------|-------|-----|
| 1 | Title (Author, Year) | Add | | [link](url) |
| 2 | Title (Author, Year) | Consider | ⚠️ arXiv | [link](url) |
| 3 | Title (Author, Year) | Skip | | [link](url) |
```

**Flags column**: `⚠️ arXiv`, `⚠️ Working paper`, `📚 Already in Zotero`, `⚠️ Suspicious`

### Phase 6: Actionable Import List

At the very end, present a focused list of **Add papers only** — this is the user's working list for import:

```markdown
## Papers to Add

1. **[Title]** — Author(s), Year
   URL: <url>
   Connects to: <key vault concepts>

2. **[Title]** — Author(s), Year
   URL: <url>
   Connects to: <key vault concepts>
```

If no papers are recommended as Add:
```markdown
## Papers to Add

None from this batch. [N] papers flagged as Consider if you'd like to review borderline cases.
```

### Phase 7: Tracking Tags (Zotero Mode Only)

**Only applies when papers came from the Zotero `_to-evaluate` queue.**

After presenting the evaluation report, ask:

```
Shall I update the evaluation tracking tags in Zotero?

This will:
- Add `_evaluated` (permanent) and `_evaluated-YYYY-MM-DD` (verification) to all evaluated papers
- Remove `_to-evaluate` from all evaluated papers

This only updates tracking tags — it does not add, remove, or modify any other tags or metadata.
```

If approved, for each evaluated paper:
```bash
zotero-tag-by-key <item-key> _evaluated _evaluated-YYYY-MM-DD
zotero-remove-tags <item-key> _to-evaluate
```

Then remind:
```
Verify in Zotero using `_evaluated-YYYY-MM-DD` tag, then remove it (keep `_evaluated` permanently).
```

If user declines, do not apply tracking tags.

## Error Handling

**No abstract available (external list)**: Papers without any abstract go directly to Skip — "Insufficient information — cannot evaluate reliably from title alone". Papers with snippet-only abstracts proceed through the two-pass flow; if OpenAlex enrichment fails, keep the preliminary tier and append `(snippet only — could not retrieve abstract)` to the Reasoning line in the report.

**No abstract available (Zotero mode)**: Attempt to retrieve via Haiku subagent from fulltext. If no fulltext either, evaluate from title and existing tags only if there is high confidence; otherwise recommend Skip with note.

**Empty Zotero queue**: Inform user and suggest adding `_to-evaluate` tags or pasting a list directly.

**Very large list (20+ papers)**: Process all papers but note at the start: "Evaluating N papers — this will be a substantial report."

## Values Alignment

**Value 1 (Human Agency)**: User reviews all recommendations; command never modifies vault or library (except optional tracking tags in Zotero mode)

**Value 2 (Transparency)**: Reasoning visible for every recommendation; flags for publication status; duplicate detection explained

**Value 3 (Beneficial Friction)**: The evaluation itself is friction — a deliberate pause between "finding a paper" and "adding it to the vault"

**Value 4 (Augmentation)**: Command assesses and recommends; user decides

**Value 6 (Reciprocal Challenge)**: Consider tier with actionable tips challenges user to think about borderline cases rather than binary add/skip

**Value 8 (Provenance)**: URLs, publication status, and Zotero library status all tracked and reported
