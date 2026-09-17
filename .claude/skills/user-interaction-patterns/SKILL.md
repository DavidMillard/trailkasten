---
name: user-interaction-patterns
description: Patterns for gathering user context, presenting structural previews, and providing critical review before major generation tasks. Use when creating blog posts, academic drafts, literature notes, ingesting resources, or expanding MOCs. Covers context gathering, approval flows, and reciprocal challenge (Value 6).
---

# User Interaction Patterns

Standardised patterns for user interaction checkpoints in complex workflows.

## Context Gathering Pattern

**When:** Before any major content generation (drafts, literature notes, expanded MOCs).

**Purpose:** Gather information that affects structure, tone, or content decisions BEFORE writing.

**Format:**
```
I'm preparing to [action] based on [[Source]].

[Domain-specific questions - 3-5 max]

Please provide as much or as little detail as you'd like - I can make reasonable decisions where you don't have specific requirements.
```

**Handle responses:**
- **Comprehensive:** Use all guidance
- **Partial:** Make reasonable assumptions, note them in report
- **Minimal:** Default to conventions based on source analysis

**Wait for response before proceeding.**

---

## Structural Preview Pattern

**When:** Before generating long content (>1000 words) or complex structures.

**Purpose:** Allow user to steer structure before committing to large generation task.

**Format:**
```
Before writing the full [word-count]-word [content type], here's the proposed structure:

**Structure Type**: [type and rationale]

**Outline**:
1. [Section] ([%], ~[words]): [2-3 sentence description]
2. [Section] ([%], ~[words]): [description]
[Continue for all sections...]

[Readiness concerns if any - max 2]

Would you like me to proceed with this structure, adjust the approach, or address the concern(s) first?
```

**User options:**
- **Proceed:** Write full content
- **Adjust:** Revise outline and re-present
- **Read more:** Return to research phase for more context
- **Address concerns:** Handle flagged issues first

**Wait for explicit approval before writing.**

---

## Approval Flow Pattern

**When:** Presenting suggestions for user selection (note concepts, titles, connections).

**Purpose:** Never create content without explicit user approval.

**Format:**
```
## [Analysis/Suggestion Type]: [Source/Context]

### [Category 1]:

1. **[[Item Title]]**
   - **What**: [Brief description]
   - **Why**: [Value/rationale]
   - [Additional context as needed]

[Continue for all items]

Which would you like me to [create/proceed with]?
```

**Rules:**
- Present all options clearly
- Include rationale for each
- Wait for explicit selection
- Confirm understanding before proceeding

---

## Source-First Proposal Pattern

When proposing atomic notes extracted from a source — a paper, transcript, or
article — never present the candidate concepts in isolation. Lead with the
source. One source at a time, summary then proposals:

1. **Full title.**
2. **A paragraph on what the source actually is and does** — its argument,
   method, the case it makes, and its main weakness. Weaknesses belong here
   (unevaluated prototype, no user study, single-site autoethnography); they
   bear directly on whether a note should exist.
3. **Only then**, the notes proposed from it.

**Why this order.** A proposal cannot be judged without the source in view. The
summary is what makes the overlap check possible: reading it, the user
recognises that a "new" concept is something the vault already holds under
another name, or spots that the proposal has ignored the source's most
distinctive feature. Expect the summary to trigger objections, and treat that as
the mechanism working rather than as a setback.

Never consolidate several sources into one merged list of candidate concepts —
that removes exactly the context the judgement needs.

## Critical Review Pattern (Value 6: Reciprocal Challenge)

**When:** Before finalising suggestions or proceeding to creation phase.

**Purpose:** Surface genuine concerns to help user make informed decisions. Addresses Value 6 (Reciprocal Challenge) - questioning rather than validating.

**Concerns to check:**

| Concern | Signal | Alternative to Offer |
|---------|--------|---------------------|
| **Source maturity** | Source rests mainly on 🌱 untested notes (never drawn on by higher-level work) | Verify claims while writing, or expand source first |
| **Redundancy** | >70% overlap with existing content | Show existing, merge or differentiate |
| **Over-atomisation** | Multiple suggestions share conceptual core | Combine into single item |
| **Weak connections** | Item would have ≤1 connection | Rethink scope or skip |
| **Scope mismatch** | Ambition exceeds target length | Narrow scope or increase length |
| **Conceptual gaps** | Argument relies on concepts without notes | Create atomic notes first |
| **Hub redundancy** | Suggested hub overlaps existing | Clarify distinction or skip |

**Format:**
```
**Readiness consideration**: [Specific concern description]
**Alternative**: [Actionable suggestion]

[If second concern:]
**Additional consideration**: [Second concern]
**Alternative**: [Actionable suggestion]
```

**Rules:**
- Flag maximum 1-2 concerns per interaction (avoid annoyance)
- Present as questions with alternatives, not blocking objections
- Frame as "consideration" not "problem"
- Always offer path forward
- Wait for user response before proceeding

**Rationale:**
- Creates strategic pause at critical decision points
- Better to fix issues in outline form than during post-generation editing
- Encourages vault development where gaps exist
- Maintains user agency while providing honest assessment
