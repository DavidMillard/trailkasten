---
type: moc
created: {{date}}
status: active
tags: [🌱]  # maturity is computed from use — script-owned, never hand-set
topics:
  - "[[Topic Hub]]"
---
# 🗺️ -  {{title}}

> [!tldr] TLDR
> **Key**:: Brief one-line description of this map of content

## Current Status
```dataviewjs
const status = dv.current().status || "Not set";
const createdRaw = dv.current().created;
const created = createdRaw && typeof createdRaw.toFormat === 'function' ? createdRaw.toFormat("dd-MM-yyyy") : (createdRaw || "Not set");
const modified = dv.current().file.mtime.toFormat("dd-MM-yyyy") || "Not set";

dv.list([
  `**Status**: ${status}`,
  `**Started**: ${created}`,
  `**Last Updated**: ${modified}`
]);
```

## Current Focus

A brief statement about what you're currently working on or exploring within this MOC. This is the minimal project tracking space - just enough to orient yourself when you return to this work.

---
## Narrative Overview

Write a narrative that synthesizes the ideas and concepts in this map of content. This should:

- **Tell a story** about how the linked notes relate to each other conceptually
- **Explain connections** between ideas rather than just listing them
- **Build a coherent thesis** or understanding of this knowledge domain
- **Weave insights together** from different notes to create a unified perspective
- **Guide the reader** through the intellectual landscape you're exploring

Think of this as the "why" and "how" these notes belong together, not just "what" they are. This narrative should make sense to someone encountering these ideas for the first time.

### Notes in This Narrative

As you reference notes in the narrative above, list them here with brief contextual descriptions:

- [[Note 1]] - How this note fits into the narrative
- [[Note 2]] - How this note contributes to the story
- [[Note 3]] - The role this note plays in the synthesis

---
## Suggestions for Expanding This MOC

Ideas for developing this map of content further:

**Specific Note Topics:**
- **[[Potential Note Title 1]]** - Why this would deepen the narrative (e.g., "Would bridge the gap between X and Y concepts")
- **[[Potential Note Title 2]]** - How this extends the current understanding

**Thematic Areas to Explore:**
- **Broader theme 1** - What this would add to the overall story (e.g., "Exploring practical applications would ground the theoretical framework")
- **Broader theme 2** - Why this direction is worth pursuing

