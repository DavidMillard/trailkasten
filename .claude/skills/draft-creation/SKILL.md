---
name: draft-creation
description: Shared logic for creating draft files in 50-Drafts/ with proper structure, frontmatter, and source linking. Use when creating any draft for an external destination — a blog post, a paper section, a talk, a report. Covers file structure, metadata, source material reading strategy, and how formatting follows the destination.
---

# Draft Creation

Shared procedures for creating drafts in `50-Drafts/`.

## Draft File Structure

All drafts follow the template at `90-Templates/Template - Draft.md`.

### Frontmatter

```yaml
---
type: draft
created: YYYY-MM-DD
status: in-progress
project: [[Source Note/MOC/Literature Note Title]]
word-count: [actual word count]
---
```

**Fields:**
- `type`: Always `draft`
- `created`: Today's date
- `status`: `in-progress` for new drafts, `complete` when finished
- `project`: Wiki-link to primary source (preserves provenance)
- `word-count`: Actual word count of draft text

### Sections

**1. Metadata**
```markdown
## Metadata

**Purpose**: [Publication venue or intent]
**Target Audience**: [Who will read this]
**Target Length**: [Approved word count] words
**Source Notes**: Primary and contextual notes
- [[Primary Source]]
- [[Linked Note 1]] (if read during research)
- [[Linked Note 2]]
```

**2. Draft Text**
```markdown
## Draft Text

[Complete draft content]
```

**3. Notes and Revisions**
```markdown
## Notes and Revisions

**Initial Draft**: [Date] - [Word count] words
- [Notes about stylistic choices, assumptions, areas needing attention]
```

---

## Source Material Reading Strategy

**Principle:** Only read linked notes when explanation or evidence is needed.

### Decision Matrix

| READ when | DON'T READ when |
|-----------|-----------------|
| Concept is CENTRAL to argument | Supporting reference only |
| Need EXPLANATION with evidence | Note name is self-explanatory |
| Contains empirical data to incorporate | Brief mention sufficient |
| Theoretical framework requires detail | Tangential to main argument |
| Note name isn't self-explanatory | Source already has sufficient explanation |

### Process

1. Parse all `[[Note Name]]` wiki-links from source
2. Assess centrality: central / supporting / tangential
3. Read 2-5 most relevant notes maximum
4. Extract key concepts, evidence, frameworks
5. Note which concepts need systematic development

### Literature Notes as Sources

When primary source is a Literature Note (`45-Literature/`):
- ALWAYS read full Literature Note (metadata, abstract, AI analysis, related work)
- Selectively read linked atomic notes referenced within
- Consider reading related papers if central to argument

---

## File Location and Naming

**Location:** `50-Drafts/YYYY/Month/[Approved Title].md`
- Drafts are filed by creation date into year/month subfolders (e.g. `50-Drafts/2026/July/`), mirroring the `80-Fleeting/` convention so the "go to the current month" navigation habit transfers.
- Derive `YYYY/Month` from the draft's `created:` date, using the full month name (e.g. `July`).
- Create the `YYYY/Month/` folder if it does not yet exist.
- Applies to both blog posts and academic drafts.

**Naming:**
- Use the title approved by the user in the workflow.
- Preserve capitalisation and punctuation.

---

## Formatting Follows the Destination

There is no fixed set of draft types. Ask where the piece is going, and let the destination
decide the formatting. Two questions settle almost every case:

**Will this be pasted into something else?** If it lands in a publishing platform, an email,
or a CMS, the Draft Text must survive copy-and-paste:

- **No wiki-links in Draft Text** — they paste literally as `[[Note Name]]`. Use italics for
  titles, plain text for names, and full external URLs for sources
- **Minimal markdown** — paragraphs, occasional bold or italic
- **No bullets, lists or block quotes** in prose
- **Subheadings** only past roughly 2,000 words

**Is it a working document that stays in your hands?** A paper section, a chapter draft, a
report you will keep editing can carry more scaffolding:

- **Wiki-links allowed as citation placeholders** — `[[AuthorYear]]`, resolved later
- **Structured headings** for sections
- **Placeholders welcome** — `[TABLE 1: Comparison here]`, `[FIGURE: Process diagram]`
- **Lists** where the content genuinely is a list

Whatever the destination, the Metadata and Notes and Revisions sections around the draft may
use wiki-links freely. Only the Draft Text has to travel.

---

## Scaffold Before Voice (pieces built from vault material)

Build the **MOC scaffold first**, then write the piece from it. Do not massage
an existing draft whose structure is drifting.

**Why.** A tone problem in a weak draft is usually structural rather than
surface, and fixing the argument's spine in a neutral MOC is cleaner than
un-polishing prose. Building the scaffold also exposes missing atomic notes —
gaps the essay would otherwise gesture at without vault support.

**How to apply:**
- **MOC voice ≠ draft voice.** The MOC stays deliberately objective:
  argument-first, no hooks, no rousing conclusion. The piece's voice and
  emotional beats come afterwards.
- **Logic from the notes; voice from the source.** Draw the argument from the
  vault notes, but take the voice from the originating transcript or fleeting
  note and the user's own phrasings. Do not voice an essay off the tentative,
  hedged prose of note text.
- **An over-weighted single example in a section signals a missing-notes gap.**
  Fill it before writing.

## Whitespace Rules

- No empty line above headings
- One empty line after headings
- One empty line between sections
- No trailing empty lines
