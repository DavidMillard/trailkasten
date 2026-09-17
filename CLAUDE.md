# CLAUDE.md

Guidance for Claude Code when working in this vault.

## What This Is

**Trailkasten** is a Zettelkasten built to be worked on with an AI assistant. It is an
Obsidian vault — markdown files linked with wiki-link syntax (`[[note name]]`) — plus a
vocabulary of commands and skills that encode how notes get made, connected, matured and
turned into writing.

The structure is the point. Atomic notes, hubs and Maps of Content give AI operations a
grammar to work within, which makes what the assistant produces legible, correctable and
navigable in a way free-form generation is not. Changes happen at the level of individual
notes rather than wholesale rewriting, and explicit links keep the scope of any revision
visible.

This is a starting structure, not a finished vault. It ships with a handful of example
notes so the machinery has something to act on; the intent is that you replace them.

### Writing Style

The vault **captures perspectives rather than establishing truths** — it embraces
epistemological pluralism. Which frameworks matter is decided by the vault's owner through
curation, not asserted by the vault itself. That stance, and the tentative language and
attribution it implies, is the convention that matters.

Spelling follows **British English**, which is simply what the shipped content uses. Change
it in the `vault-writing-style` skill if you prefer otherwise; consistency is the point, not
the variety.

The conventions that follow from this — tentative language and attribution, when definitive
language is nonetheless appropriate, and the spelling patterns — are owned by the
**vault-writing-style skill**, which loads automatically whenever content is created or
edited. Do not restate its rules here.

## Values Statement

The vault includes a [[Values Statement]] (`00-Index/Values Statement.md`) articulating
principles for AI-assisted knowledge work. These are a position, not a neutral description
— they were written by the vault's original author and are open to disagreement. They guide
how the tooling here was built:

- Preserving human agency and the intention/action boundary
- Maintaining transparency over opacity
- Designing for augmentation rather than automation
- Supporting spatial and associative thinking
- Enabling reciprocal challenge rather than sycophancy

**When building new commands or skills, refer to the Values Statement** to check alignment.
It serves as both a design guide and an evaluation framework.

**When modifying commands or skills on values grounds, record it in [[Vault Rationale]]**
(`00-Index/Vault Rationale.md`). This creates an audit trail showing how abstract values
translate into concrete implementation decisions: which gaps were identified, what changed,
which values are now better served, which files were touched.

## Repository Structure

This vault follows a Zettelkasten methodology with numbered folders:

- `00-Index/` - Entry points and navigation (Home, Usage Guide, History index, Values)
- `10-MOCs/` - Maps of Content (narrative trails through the notes)
- `20-Hubs/` - Concept hubs (evergreen thematic organisation)
- `30-Notes/` - Atomic Zettelkasten notes (individual ideas and insights)
- `35-History/` - Daily chronicle of vault evolution
- `40-Resources/` - Resource notes written by `/ingest-resource`: summary, extracted concepts, source preserved
- `41-Attachments/` - Images, PDFs and other binaries embedded in notes (excluded from analysis)
- `45-Literature/` - Literature notes for academic papers (academic tier)
- `50-Drafts/` - Writing drafts synthesised from notes
- `60-Analysis/` - Strategic analyses, organised by year
- `80-Fleeting/` - Inbox: raw material dropped in for Claude to find and ingest from
- `90-Templates/` - Note templates
- `99-Archive/` - Completed projects and deprecated content
- `.obsidian/` - Obsidian configuration
- `extras/` - Optional tiers, inert until installed by `/setup`

**`80-Fleeting/` is inbound only.** It is the user's inbox *to Claude* — where source
material is dropped to be found and worked from. Read source material *from* fleeting;
never write deliverables *to* it. Analysis documents Claude generates — critiques, edit
lists, strategic assessments, gap analyses — go to `60-Analysis/<year>/`, filed by year
with no month subdivision. Leave original sources where the user put them.

## Command Tiers

**Core** — installed and active. Needs nothing beyond Obsidian and Claude Code:

- `/setup` - First-run configuration: environment check, identity, tiers, bootstrap
- `/create-note <subject>` - Create an atomic note with intelligent connections
- `/create-hub <concept>` - Create a hub page organising related notes
- `/ingest-resource [path]` - Extract atomic notes from raw materials
- `/create-moc <name>` - Build a Map of Content from a stated argument shape, or expand an existing skeleton
- `/create-draft <note-or-moc>` - Turn curated material into an external-facing draft
- `/vault-health` - Audit vault structure and health

**Academic** — inert in `extras/academic/` until installed. Requires a Zotero library and
the `zotero-mcp` server:

- `/create-literature-note <citation-key>` - Literature note from Zotero with analysis
- `/find-papers <note-or-concept>` - Find relevant Zotero papers for vault concepts
- `/find-citations <text with \cite{...}>` - Recommend citations for placeholders
- `/evaluate-papers` - Assess papers for vault contribution value

Commands are full-workflow specifications that load relevant skills and execute directly.
See the files in `.claude/commands/` for detail.

## Vault Search: Prefer MCP, Degrade Gracefully

Search quality depends on what is installed. **Use the best tool available, and say what
you are working without.**

### If the MCP servers are configured

Use them, in this order:

1. **Semantic similarity** — `mcp__smart-connections__get_similar_notes` finds
   conceptually related notes without reading any files
2. **Keyword/content search** — `mcp__obsidian__vault` (search with snippets → fragments
   → selective read)
3. **Structural navigation** — `mcp__obsidian__graph` for traversing wiki-links
4. **Metadata queries** — `mcp__obsidian__dataview` for type, tag and frontmatter filters

Reading vault files in full is appropriate only *after* triage has identified which files
are worth it. See the `obsidian-patterns` skill for token-efficiency guidance.

### If they are not

**Grep, Glob and Read are the correct tools, not a policy violation.** A vault with no MCP
servers works — it is simply less efficient, and semantic search is unavailable, so
conceptually related notes that share no vocabulary will be missed.

Say so once, early, rather than silently doing worse work:

> No semantic search configured, so I am matching on keywords — I may miss related notes
> that use different vocabulary. `/setup` can help you configure it.

Do not ask for approval before every search. Do not stop and negotiate. Work.

**This applies to searching and reading only.** It is not a general licence to act without
asking — content creation is governed by the rule directly below, which it does not
override.

### If a configured server fails

This is different: something that should work does not.

1. Do **not** silently fall back
2. Tell the user what failed
3. Ask: (a) retry, (b) continue with direct file tools, (c) stop

### Obsidian MCP warm-up

`mcp__obsidian__vault` can fail on its first call in a session with "Server not
initialized" — a race between the HTTP connection and the MCP handshake. **Make one
sequential vault call first** (reading a template, say) before batching parallel vault
operations. Smart Connections has the same race but returns empty results rather than
errors, which is harder to spot; warm it with `get_stats`.

## Review Happens at Creation

**Non-negotiable. This is the rule the vault's whole design rests on.**

Notes are proposed before they are written, and the user accepts, redirects or rejects them
one at a time. This is not politeness, and it is not a safety catch to be traded away for
throughput. It is where the intellectual work happens: deciding whether a concept is real,
whether it belongs here, and whether it merely restates something already held *is* the
thinking. The vault is worth having only because someone did that work.

**Deferred review is not review.** "I'll build, you review afterwards" sounds efficient and
is not. Notes that arrive unreviewed are never revisited — they can be altered later in
principle, and in practice they never are. Creation is the only moment when the judgement
actually gets made, so that is where the interaction belongs. A vault filled by a process
that skipped it looks identical to one that did not, which is precisely what makes the
shortcut dangerous.

Therefore:

- **Never propose batching creation ahead of review**, or any arrangement where content
  lands first and is inspected afterwards.
- **Never save such an arrangement to memory.** A relaxation persisted across sessions stops
  being a choice and silently becomes the default.
- **If the user asks for it directly**, say plainly what it costs before complying, and do
  not persist it beyond the current session.

Batching *operations* is fine and encouraged — writing ten already-approved notes in one
pass is efficient and changes nothing. What must never be batched is the approval.

## Working with Notes

Notes are markdown with Obsidian extensions. Always use wiki-links (`[[Note Title]]`,
`[[Note Title|Display Text]]`, `![[Embed]]`) rather than standard markdown links, and give
notes clear, descriptive names. Formatting, frontmatter and naming conventions are owned by
the **zettelkasten-methods skill**; note *creation* procedure is owned by the
**note-creation skill**.

### Human-Written Content Protection (`#human` Tag)

**CRITICAL — never modify human-written content without explicit permission.**

Any paragraph or bullet containing the `#human` tag is human-written, in a vault where most
prose is machine-generated. These segments get special care:

1. **Never modify** a paragraph or bullet containing `#human` without explicit permission
2. **Preserve exactly** when updating surrounding content — incorporate unchanged
3. **Give higher weight** to `#human` content in analysis and conceptual understanding
4. **Ask first** if a change seems necessary — flag it rather than making it

The tag preserves the user's authentic voice and original insights, keeping the knowledge
base grounded in human thinking while benefiting from AI assistance in organisation and
expansion.

## Zettelkasten Methodology

Content types, linking principles, navigation flow, formatting conventions and the maturity
system are owned by the **zettelkasten-methods skill**, which loads automatically when
working with notes, hubs, MOCs or literature notes. Folder layout is above.

Three standing constraints, because getting them wrong damages the vault rather than merely
producing poor output:

- **Tags mean maturity, nothing else.** Concepts are expressed through hub links, never tags.
- **Maturity is a computed cache, not a judgement.** The 🌱🌿🌲 tags and `used-by:` field are
  owned by `.claude/scripts/vault_maturity.py` and record *use* — how many MOCs, drafts or
  analyses draw on a note. Never hand-set them beyond the 🌱 birth state, and never retag by
  connection count. Commands that create or edit MOCs, drafts or analyses run the reconcile
  script as their final step.
- **No per-note research-question metadata.** Persistent questions live on one curated page,
  `00-Index/Research Programme.md`. A per-note `problems:` field was tried and retired: it
  depended on maintenance nobody performed, because tagging a note with a question has no
  value at the moment of tagging.

## History Chronicle System

The vault keeps a daily chronicle in `35-History/YYYY-MM-DD.md`, entered from
`00-Index/History.md`. Entries are **intellectual history, not task logs**: flowing prose
that clusters the day's notes thematically and explains what territory they establish.

File structure, narrative voice, clustering rules, brevity limits and the
rewrite-don't-append methodology are owned by the **history-update skill**.

### When to offer an entry

After completing any operation that creates or substantially modifies vault content,
proactively ask whether to update today's entry:

```
Would you like me to update today's history entry (35-History/YYYY-MM-DD.md)
to chronicle these additions?

Created:
- [[Note Name 1]]
- [[Note Name 2]]
```

**Warrants an offer:** new notes, hubs, MOCs or literature notes; substantial expansion of
an existing MOC or hub; resource ingestion; any batch operation.

**Does not:** reading files; pure research or exploration; when the user has said to skip
history; when they are clearly experimenting or prototyping.

The user may batch several sessions before updating, or skip history for experimental work.
Respect the preference and remember it for the session.

## Configuration

- `.claude/commands/` - Slash command definitions with full workflow logic
- `.claude/skills/` - Reusable skill modules loaded by commands
- `.claude/scripts/` - Deterministic vault analysis (`vault_health.py`, `vault_maturity.py`)
- `extras/` - Optional tiers, inert until installed
- `.mcp.json` - MCP server configuration. Not in the repo; `/setup` writes it.

**Skill architecture:** commands load skills to provide domain knowledge and standardised
procedure. Skills are modular and shared across commands to avoid repetition.

**Key skills:** `vault-writing-style` (epistemological stance, spelling convention),
`zettelkasten-methods` (structure and content types), `note-creation` (connection tiers,
backlinks, atomicity), `user-interaction-patterns` (approval flows, critical review),
`draft-creation` (draft structure), `obsidian-patterns` (efficient MCP operations),
`history-update` (daily chronicle), `summarise-large-document` (subagent preprocessing).

Do not modify files in `.obsidian/` unless asked — they control the Obsidian application.
