---
name: zotero-tag-vocabulary
description: Tag vocabulary and query expansion for Zotero library searches. Use when working with Zotero searches, finding papers for concepts, or mapping vault concepts to Zotero tags.
---

# Zotero Tag Vocabulary

Provides tag vocabulary knowledge and query expansion strategies for discovering papers in the Zotero library using concept-to-tag mappings.

## Category Tags (9 High-Level)

Each paper typically has 1-3 category tags. Category tags provide high-level classification:

1. **`hypertext`** - Non-linear, linked text structures, hypertext theory, spatial hypertext
   - Often co-occurs with: `IDN` (narrative hypertext)

2. **`IDN`** - Interactive Digital Narrative (audience/player agency in stories)
   - Often co-occurs with: `hypertext`, `game-design`, `XR`

3. **`XR`** - Extended Reality (AR, VR, MR, spatial computing, immersive experiences)
   - Often co-occurs with: `game-design`, `IDN`

4. **`e-learning`** - Educational technology, learning theory, pedagogy
   - Often co-occurs with: `AI`

5. **`HCI`** - Human-Computer Interaction (UI, interaction design, usability, UX)
   - Often co-occurs with: Most other categories (cross-cutting domain)

6. **`methodology`** - Research methods, frameworks, evaluation techniques
   - Often co-occurs with: Any category (methodological papers)

7. **`ethics`** - Moral and ethical implications, normative questions, values
   - Often co-occurs with: `AI`, `XR`
   - **Used sparingly**: Only when paper explicitly addresses normative questions

8. **`game-design`** - Game mechanics, game theory, play, game studies
   - Often co-occurs with: `XR`, `IDN`

9. **`AI`** - Artificial Intelligence (ML, LLMs, generative AI, algorithmic systems)
   - Often co-occurs with: `ethics`, `e-learning`, `HCI`

## Hierarchical Tag Relationships

The tagging system uses hierarchical tagging: specific terms include their base term.

**General pattern**: When paper discusses `[specific concept]`, it gets both `[base]` AND `[specific]` tags.

**Examples**:
- `intentional friction` → tagged with both `friction` AND `intentional friction`
- `spatial hypertext` → tagged with both `hypertext` AND `spatial hypertext`
- `AI literacy` → tagged with both `literacy` AND `AI literacy`
- `VR` → tagged with both `XR` AND `VR`
- `RLHF` → tagged with both `reinforcement learning` AND `RLHF`

**Query implication**: When searching for specific concepts, also search the base term to capture related papers.

## Common Concept-to-Tag Mappings

When user requests papers about a vault concept, map to relevant Zotero tags.

### Friction and User Experience
- **"friction"** → `intentional-friction`, `friction`, `disfluency`, `designed-friction`
- **"intentional friction"** → `intentional-friction`, `friction` + category `HCI` or `game-design`
- **"disfluency"** → `disfluency`, `friction` + category `HCI` or `e-learning`
- **"usability"** → `usability`, `HCI`

### Hypertext and Non-linearity
- **"hypertext"** → `hypertext`, `spatial-hypertext`, `non-linearity`, `linked-data`
- **"spatial hypertext"** → `spatial-hypertext`, `hypertext`
- **"linking"** → `hypertext`, `linked-data`, `semantic-web`

### Interactive Narrative and Games
- **"interactive narrative"** → `IDN`, `interactive-narrative`, `emergent-narrative`, `storylet`, `IDN` category
- **"game learning"** → `game-based-learning`, `serious-game`, `e-learning` + `game-design` categories
- **"game design"** → `game-design` category, `game-mechanics`, `ludonarrative`

### AI and Writing
- **"AI writing"** → `AI-assisted-writing`, `generative-AI`, `LLM`, `AI` category
- **"LLMs"** → `LLM`, `transformer`, `GPT`, `language-model`
- **"prompt engineering"** → `prompt-engineering`, `LLM`, `AI` category
- **"AI literacy"** → `AI-literacy`, `literacy`, `AI` + `e-learning` categories

### AI Safety and Ethics
- **"AI alignment"** → `AI-alignment`, `alignment-problem`, `value-learning`, `AI` + `ethics`
- **"AI safety"** → `AI-safety`, `alignment-problem`, `RLHF`, `AI` + `ethics`
- **"sycophancy"** → `sycophancy`, `AI-alignment`, `truthfulness`

### Extended Reality
- **"VR"** → `VR`, `XR` category, `immersion`, `presence`
- **"AR"** → `AR`, `XR` category, `locative-media`, `spatial-computing`
- **"immersion"** → `immersion`, `presence`, `XR` category

### Learning and Education
- **"spaced repetition"** → `spaced-repetition`, `memory`, `e-learning` category
- **"zone of proximal development"** → `ZPD`, `scaffolding`, `Vygotsky`, `e-learning`
- **"cognitive load"** → `cognitive-load`, `working-memory`, `e-learning` or `HCI`

### Philosophy and Theory
- **"existentialism"** → `existentialism`, `phenomenology`, `Heidegger`, `Sartre`
- **"post-structuralism"** → `post-structuralism`, `Derrida`, `Foucault`
- **"virtue ethics"** → `virtue-ethics`, `Aristotle`, `phronesis`, `ethics` category

### Cognition and Attention
- **"cognitive offloading"** → `cognitive-offloading`, `extended-mind`, `distributed-cognition`
- **"attention"** → `attention`, `attention-economy`, `distraction`, `flow`
- **"metacognition"** → `metacognition`, `metacognitive-monitoring`, `self-regulation`

## Query Expansion Strategy

When searching for papers related to a vault concept, use a three-level progressive strategy:

### Level 1: Primary Query (Most Specific)
Combine specific tags with category constraint:
```
tag: "(specific-tag OR related-specific-tag) AND category-tag"
limit: 10
```

**Example** (for "intentional friction"):
```
tag: "(intentional-friction OR friction) AND HCI"
```

### Level 2: Broadened Query (If <3 Results)
Remove category constraint, keep related specific tags:
```
tag: "specific-tag OR related-tag-1 OR related-tag-2"
limit: 10
```

**Example**:
```
tag: "friction OR disfluency OR designed-friction OR intentional-friction"
```

### Level 3: Category + Keyword (If Still <3 Results)
Search category with concept as keyword:
```
tag: "category-tag"
query: "concept keyword"
qmode: "titleCreatorYear"
limit: 10
```

**Example**:
```
tag: "HCI"
query: "friction"
qmode: "titleCreatorYear"
```

**Rationale**: Progressive broadening surfaces research gaps (0 results = valuable signal) while avoiding overwhelming user with loosely-related papers.

## Related Tag Discovery Patterns

When mapping a concept, consider multiple dimensions:

1. **Direct synonyms**: Terms meaning the same thing
   - "disfluency" ↔ "friction"

2. **Hierarchical relationships**: Base and specific terms
   - "friction" ← "intentional friction"

3. **Contextual co-occurrence**: Terms that appear together
   - "hypertext" + "non-linearity"
   - "AI" + "alignment-problem"

4. **Cross-category connections**: Same concept in different domains
   - "friction" in `HCI` vs `game-design` vs `e-learning`

5. **Methodological terms**: How concept is studied
   - "cognitive-offloading" + "extended-mind" + "distributed-cognition"

## Tag Normalization Rules

When generating search queries, ensure tags follow normalization conventions:

1. **Singular form** - `algorithm` not `algorithms`
2. **Lowercase** - except proper nouns/acronyms (`ChatGPT`, `Storyspace`)
3. **Prefer acronyms** - `AR` not `augmented reality`, `LLM` not `large language model`
4. **Hyphenate compounds** - `mixed-reality`, `AI-assisted`, `human-computer interaction`
5. **No category duplication** - Don't combine `HCI` category with `human-computer interaction` atomic tag

## Special Cases

### Generic Category Concepts
When concept is just a category (e.g., "AI", "hypertext"), flag as potentially too broad:
- May return 50+ papers
- Suggest narrowing to specific aspect
- Ask user which sub-area they're interested in

### Research Gaps
When 0 results across all levels:
- **Potential contribution area** - Concept not yet researched in this combination
- **Tag vocabulary gap** - Papers exist but aren't tagged yet
- **Terminology mismatch** - Papers use different terminology

Distinguish by checking:
1. Does keyword search find anything? (terminology issue)
2. Are there untagged papers in library? (tagging gap)
3. Truly no papers? (research gap)

### Multi-Dimensional Concepts
Some vault concepts span multiple domains. Include all relevant category tags:
- "AI writing education" → `AI`, `e-learning`, tags: `AI-assisted-writing`, `pedagogy`
- "VR narrative games" → `XR`, `IDN`, `game-design`, tags: `VR`, `narrative-design`

## Usage Pattern

**When user requests papers for `[[Vault Concept]]`**:

1. Extract key terms from concept name and note content (TLDR, first few bullets)
2. Map terms to Zotero tag candidates using concept-to-tag mappings
3. Apply hierarchical expansion (include base terms)
4. Identify relevant category tags
5. Execute three-level query strategy
6. Deduplicate results
7. Explain query expansion logic to user

**Example flow**:
```
Input: [[Intentional Friction]]
→ Key terms: "intentional friction", "friction", "user experience"
→ Tag candidates: `intentional-friction`, `friction`, `disfluency`
→ Category: `HCI`, possibly `game-design`
→ Primary query: "(intentional-friction OR friction) AND HCI"
→ Broadened query: "friction OR disfluency OR intentional-friction"
→ Category query: tag="HCI" query="friction"
```

## Auto-Load Triggers

This skill auto-loads when:
- Command name includes "zotero", "papers", or "citations"
- User message includes "working with Zotero"
- User message includes "searching papers" or "finding papers"
- User message includes "tag vocabulary" or "tag mapping"
