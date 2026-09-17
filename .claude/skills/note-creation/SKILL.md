---
name: note-creation
description: Shared logic for creating atomic notes and hubs with intelligent bidirectional linking. Use when creating notes, hubs, or batch processing from literature notes or resource ingestion. Covers connection strength tiers, backlink rules, maturity tagging, and the atomic principle.
---

# Note Creation

Shared procedures for creating atomic notes and hubs with intelligent connections.

> **This skill is the single source for the rules below** — connection limits and strength tiers, backlink rules, maturity, alias criteria, the atomic principle, hub scope thresholds, and the batch mode pattern. Commands own their *workflow sequence* and their own reporting formats; they must reference these rules rather than restate them, so the two cannot drift apart.

## Connection Limits (Soft Target)

**Aim for 2–6 Related Notes per note.** This is a target that describes a typical healthy note, **not a gate**. An important note may legitimately carry more as it matures, and a genuine bridge between two lineages will.

- **Fewer than 2**: search harder, or the note may not be sufficiently atomic
- **More than 6**: not a fault in itself. Ask whether the extra connections are still Tier 1 or Tier 2 (below). If they are, keep them and read the density as a structural signal
- **Never delete a valuable connection merely to satisfy the count.** Refusing connections is not curation — it degrades the network silently, because the links refused entry to mature notes are systematically the high-value ones

## Connection Strength Tiers

Tiers classify by **function** — what the connection does for the reader — not by relation type. The same kind of relation can be strong or weak depending on the notes involved.

### Tier 1 — Constitutive

Remove it and this note becomes harder to understand. The foundational or parent concept, the direct counterpoint, the alternative it defines itself against, the thing it is a component of.

*Test*: a Tier 1 subnetwork is really **one proper subject** viewed from several angles.

### Tier 2 — Illuminating

Changes how you read the other note — surfaces a tension, names a problem, supplies a concrete instance, shifts an interpretation — but neither note depends on it. More than an explained adjacency, less than essential.

### Tier 3 — Adjacent

The two ideas have something genuinely in common and you can always write the sentence, but the sentence makes no point beyond locating them in the same space.

Tier 3 is **developmental scaffolding**: expected and useful on new notes, where it makes them findable, and expected to decay as the note accumulates stronger connections. Trigger that decay on the note's connection richness and age — **not** on its 🌱🌿🌲 tag, which records use by MOCs and drafts and is a separate system.

### Tiers are directional

A connection has two strengths, one per direction, and they are frequently different. `[[Fiduciary Relationship]] → [[Accountability Sinks in AI Systems]]` is Tier 1 (the framework exists to prevent that failure mode); the reverse is Tier 2 (accountability sinks are a broader phenomenon that does not depend on fiduciary theory).

**Record the tier from the perspective of the note the bullet sits in.** Each note ranks its own connections. Do not apply a reciprocity test — it assumes a symmetry that does not hold.

### Marking Tier 1

Bold **the wiki-link itself** in the Related Notes list:

```markdown
- **[[Foundational Concept]]** — one sentence on why this is constitutive
- [[Illuminating Note]] — one sentence on what it changes
```

- Bold the link only, never a lead-in phrase. `- **Provides empirical support for**: [[Note]]` is emphasis, not a tier marker; the convention is that a bolded *link* means Tier 1
- Only Tier 1 is marked. Tier 2 and 3 are inferred, because only Tier 1 carries a protective rule and misreading a 3 as a 2 costs nothing
- **Unmarked means unassessed, not Tier 3.** Most existing notes predate this convention. Treat unmarked connections as Tier 2 for permission purposes until they have actually been assessed. Mark opportunistically when a note is touched for other reasons — never as a migration sweep

## Connection Maintenance

Curating an existing network is part of the work, not a separate cleanup phase. Removing a stale connection to make room for a stronger one is normal maintenance.

| Tier | May add | May remove |
|------|---------|-----------|
| **Tier 1** | Always | **Never without asking the user** — even when it looks stale |
| **Tier 2** | Always | Your judgement; report what you removed and why |
| **Tier 3** | On new notes; **not** to already richly-connected notes | Freely, to make room for a Tier 1 or Tier 2 |

Applied to backlinks: when a target note is already dense, do **not** default to skipping. Read its connections and ask whether any are Tier 3 and displaceable. Skipping is only correct when everything there is genuinely stronger than what you are holding.

### Density as a structural signal

Density is a signal to **look**, never an automatic trigger to act. Resist numeric thresholds.

- **Many Tier 1 on one note** — the note is unfactored, not well-connected. Propose a split, or a framework note (see the framework-notes guidance in `zettelkasten-methods`)
- **Many Tier 2 on one note** — a candidate MOC or spin-off note is forming. This is the expected growth path; do not prune it away
- **Many Tier 3 on a mature, well-connected note** — scaffolding that has outlived its purpose; prune

### Escalating connection decisions

Never present replacements mechanically as "A and B were connected, I would rather connect A to C" — the user cannot adjudicate those one at a time, and a list of them is unanswerable.

**Cluster proposed changes into the editorial question underneath them.** Several mechanical changes usually reduce to two or three real decisions about what a note is *for*. Ask that question; let the connection changes follow from the answer.

> **[[Accountability Sinks in AI Systems]]** — is this note primarily about responsibility diffusing through organisational structure, or about how responsibility gets assigned in the first place? The answer decides three connections at once.

Classification is yours; permission is the user's. Decide which tier a connection is by judgement, every time. Do not exceed the permissions in the table above without asking.

## Maturity Tags (Usage Model)

Maturity records **use, not structure**: how many distinct higher-level artefacts — MOCs, drafts in `50-Drafts/`, analyses in `60-Analysis/` (the "consumers") — draw on a note. The wiki-links in consumer files are the ground truth; the emoji tag and `used-by:` field in a note's frontmatter are a regenerable cache owned by `.claude/scripts/vault_maturity.py`.

| Tag | Meaning | Definition |
|-----|---------|-----------|
| 🌱 Untested | Never drawn on by higher-level work | 0 consumers |
| 🌿 Drawn on | Has fed at least one narrative | 1–2 distinct consumers |
| 🌲 Load-bearing | Supports multiple narratives | 3+ distinct consumers |

**Rules:**
- New notes start as `tags: [🌱]`, `used-by: 0` — true by definition at birth
- **Never hand-compute or hand-edit maturity tags** — the reconcile script owns them and will overwrite manual changes
- Hubs are not consumers (hub membership is shelving, not use), and hubs themselves carry computed tags like any note
- Reconcile after any operation that creates or edits MOCs, drafts, or analyses:
  `python3 .claude/scripts/vault_maturity.py --write` (prints graduations)

### Provenance Reporting (commands that draw on notes)

Commands that build on vault notes (`/create-draft`, `/create-moc`):

1. **Before writing** — after gathering source notes, report their maturity mix: "Building on N notes: X 🌲 load-bearing, Y 🌿 drawn on, Z 🌱 untested", listing the untested ones. Untested notes deserve extra critical scrutiny at this moment — nothing has yet exercised their claims.
2. **After the artefact is written** — run the reconcile (`--write`) and report the graduations it prints (e.g. "This draft moved 3 notes 🌱→🌿").

### Territory Feedback (commands that add material)

Commands that add new notes (`/ingest-resource`, `/create-literature-note`):

1. Run `python3 .claude/scripts/vault_maturity.py --hubs`
2. For each hub the new notes link to via `topics:`, mention its territory heat in the report: "extends [[Hypertext]] (50% tested)" — and flag when material lands in one of the vault's least-tested territories
3. Run the reconcile (`--write`) as the final step if any MOC, draft, or analysis was touched

## Alias Criteria

**Consider for:** Acronyms (PKM, RLHF), well-known phrases, alternative terminology.

**Skip for:** Minor variations, overly generic terms.

## Atomic Principle

- One idea per note
- Details section: 4-6 bullets explaining ONLY what the concept IS
- Connections belong in Connections section, not Details
- TLDR: One-line Key:: description (<100 chars)

### Concepts, Not Findings

The vault holds **concepts** — ideas reusable across unrelated pieces of work.
**Findings** are evidence supporting a concept; they attach to an existing note
and are not notes in their own right. A finding is sometimes genuinely a concept
— a typology, a named distinction, a measurable dimension — but that is the
exception, not the default.

**Diagnostic:** could this idea be carried into a project that has nothing to do
with the study it came from? If not, it is a finding.

**How to apply.** When proposing notes from a source, state for each candidate
whether it is a *concept* (new note) or a *finding* (naming which existing note
it amends). "No new notes, three notes enriched" is a valid and common outcome —
say so rather than manufacturing a note to show for the work.

---

## Single Note Creation Process

### Step 1: Clarification (Only if Needed)

Skip for clearly unambiguous subjects with context provided.

**Check for:**
- Term has multiple meanings across domains
- Broad term that should be multiple atomic notes
- Unfamiliar technical term

**If ambiguous:** Ask user to select interpretation.

**Check for issues:**
- Similar existing note (>60% overlap) - offer to show first
- Broad scope - suggest narrowing
- Related notes densely connected — backlinks may require displacing a Tier 3 connection rather than being added outright

Present concerns as informational flags (max 1-2). User can say "proceed" to continue.

### Step 2: Research Vault

**If suggested_connections provided:** Validate they exist, skip broad searches.

**Otherwise:**
1. Read template: `90-Templates/Template - Zettel Note.md`
2. Search for related content (search with snippets → fragments → selective reads)
3. Read 2-3 exemplar notes to understand style

### Sibling and Duplicate Checks (flag, never resolve)

These belong here, at create time — not in `/vault-health`, which runs too late
to prevent anything. They **flag for the user and never auto-resolve**: merging
or redirecting is a decision, and decisions stay with the human.

During vault research, watch for two things:
- **A near-duplicate** — an existing note already covering this concept. Show it
  and ask whether to enrich rather than create a second.
- **A sibling** — the candidate looks like a member of an existing framework
  note's or MOC's cluster: "this looks like a sibling of [[X]]'s members — does
  it belong there?"

The sibling check is fuzzy and will produce false positives; raise it as a
question, never as a correction. Do not implement either check as a new
frontmatter field — the raw material is already in `used-by` and the backlinks.

### Step 3: Create Note File

Create `30-Notes/<Subject>.md` following template exactly:

- **Frontmatter**: `type: note`, `created: YYYY-MM-DD`, `tags: [🌱]`
- **topics**: 1-3 hub links in wiki-link format: `"[[Hub Name]]"`
- **aliases**: Add if applicable (acronyms, well-known phrases)
- **TLDR**: One-line Key:: description (<100 chars)
- **Details**: 4-6 bullets explaining ONLY the concept itself
- **Connections**: 2–6 related notes with inline descriptions (Tier 1 links bolded)
- **References**: Source information

### Step 4: Identify Connections

**If suggested_connections provided:** Validate and use these. Add 1-2 more only if obvious ones missed AND total stays ≤6.

**Otherwise:** Search vault for Tier 1 and Tier 2 connections. Aim for 2–6; keep a seventh or eighth only where it is genuinely Tier 1 or Tier 2, and say why in the report.

**Semantic enrichment (after note file is created):** Call `mcp__smart-connections__get_similar_notes` on the new note (threshold: 0.3, limit: 10) to surface semantically related notes not found by keyword search. Merge semantic results with keyword/graph results before applying Tier 1/2/3 filtering. Follow Smart Connections Failure Protocol from `obsidian-patterns` if unavailable.

**Validation:** At least 2. Beyond 6, confirm each additional connection is Tier 1 or Tier 2 rather than trimming to fit.

### Step 5: Add Bidirectional Links

**For each related note:**
1. Read note, count existing connections
2. Apply the Connection Maintenance permissions above — displace a Tier 3 where warranted rather than defaulting to a skip
3. If approved: Add backlink with one-sentence description

Backlinks do not change maturity — maturity records use by MOCs/drafts/analyses, not peer connections.

**Track:** Backlinks added, backlinks skipped (with reason).

### Step 6: Finalise

**Check if new hub needed:** If concept is broad enough for 5-15 notes and no existing hub covers it, suggest to user.

**Suggest related notes:** 3-5 topics that would strengthen the network but don't exist.

**Report:** Note path, connections established, backlinks added/skipped, suggestions.

---

## Hub Creation Process

Hubs organise existing notes around a conceptual domain.

### Step 1: Research and Validate

1. Read template: `90-Templates/Template - Hub.md`
2. Check hub doesn't already exist (same/similar name)
3. Validate scope:
   - Too narrow (<5 potential notes): Suggest creating a note instead
   - Too broad (20+ notes, multiple domains): Suggest splitting
   - >50% overlap with existing hub: Clarify distinction

### Step 2: Create Hub File

Create `20-Hubs/<Subject>.md` following template:

- **Frontmatter**: `type: hub`, `tags: [🌱]`, `used-by: 0` (maturity is computed from use, for hubs like any note)
- **TLDR**: One-line domain description
- **Introduction**: 2-3 paragraphs explaining the domain
- **Related Hubs**: 1-3 hubs with relationship explanations
- **DataView queries**: Keep exactly as in template (auto-populate)

**Hub naming:** 1-3 words maximum. Use clear, established terminology. No articles or verbose descriptions.

### Step 3: Link Notes to Hub

Find 5-15 notes that belong to this domain:
1. Search vault for relevant notes using keyword search
2. Select 2-3 of the most relevant notes found so far. Run `mcp__smart-connections__get_similar_notes` on each (threshold: 0.3, limit: 10) to discover notes in the hub's conceptual neighbourhood that keyword search missed. Deduplicate with existing results. Follow Smart Connections Failure Protocol from `obsidian-patterns` if unavailable.
3. Categorise: high relevance (include) vs medium relevance (include selectively)
4. For each note: Add hub to `topics` frontmatter field

### Step 4: Finalise

**Update related hubs:** Add bidirectional hub-to-hub links in `topics` fields.

**Report:** Hub path, notes linked (count), related hubs, knowledge gaps identified.

---

## Batch Mode Pattern

Use when creating 2+ notes in a single invocation (from literature notes or resource ingestion).

### Setup (Once)

1. Read template once
2. List vault structure once
3. Validate all suggested connections exist
4. Read 2-3 exemplar notes once

### Create Notes (Sequential)

For each concept:
1. Skip clarification (coordinator already confirmed)
2. Consider aliases
3. Create note file using suggested connections
4. Apply connection strength criteria; trim only genuine Tier 3 padding, never a Tier 1 or Tier 2 connection to satisfy a count
5. Track for backlink phase

**Do NOT add backlinks yet.**

### Semantic Enrichment Pass

After all notes are created and before batch backlinks:
1. For each new note, call `mcp__smart-connections__get_similar_notes` (threshold: 0.3, limit: 10)
2. Merge semantic results into the backlink candidate pool (deduplicate with existing connections)
3. Apply Tier 1/2/3 filtering to any new candidates surfaced
4. Follow Smart Connections Failure Protocol from `obsidian-patterns` if unavailable

### Batch Backlinks

After all notes created (and semantic enrichment):
1. Collect all related notes across new notes (deduplicate)
2. For each unique target: read once, apply the Connection Maintenance permissions, add ALL applicable backlinks in one edit
3. Track decisions

### Report

Consolidated summary: All notes created, backlinks added/skipped, territory feedback (see Maturity Tags section).

---

## Quality Checklist

Before reporting, verify:

- [ ] New note has at least 2 Related Notes; any beyond 6 justified as Tier 1 or Tier 2
- [ ] All connections are Tier 1 or Tier 2
- [ ] Pre-flight check done for all backlinks
- [ ] Dense targets examined for displaceable Tier 3 connections, not skipped by default
- [ ] Tier 1 connections bolded on the link; no Tier 1 removed without user approval
- [ ] Connection changes escalated as clustered editorial questions, not as individual swaps
- [ ] Details has 4-6 bullets explaining concept only
- [ ] Type field matches folder (note/hub)
- [ ] New notes tagged 🌱 with `used-by: 0` (maturity is otherwise script-owned — never hand-set)
- [ ] Spelling convention consistent
- [ ] Template structure followed exactly
