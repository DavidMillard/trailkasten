---
name: summarise-large-document
description: Summarise long documents in a subagent before analysis, keeping the full text out of the main context window. Trigger when (1) ingesting resources longer than ~5000 words, (2) processing PDFs or transcripts, (3) summarising an academic paper, (4) bulk relevance assessment. A Haiku subagent does the mechanical extraction; the main model does the nuanced reasoning.
---

# Summarise Large Document

Long sources — papers, theses, transcripts, book chapters — are expensive to
read directly. Reading a 20,000-word thesis into the main context to write four
atomic notes from it spends most of a session's budget on text that will never
be referred to again.

The fix is to read it **somewhere else**. Delegate the extraction to a Haiku
subagent: the subagent reads the full document into its own context and returns
only a structured summary, so the main context receives roughly 1,200 words
instead of 20,000.

Division of labour: **the subagent extracts; the main model reasons.**

## When to Use

**Delegate to a subagent for:**
- Documents over ~5,000 words, before ingestion or literature-note creation
- PDFs, theses, transcripts, and lengthy conversations
- Initial relevance filtering ("is this worth reading properly?")
- Any first pass where only the gist is needed

**Keep in the main context:**
- Atomic-note framing and the epistemological stance
- Connection-quality assessment — this needs vault context the subagent lacks
- Nuanced or critical analysis, tentative language, attribution

Short documents need no subagent. Below ~5,000 words, reading directly is
simpler and the summary would cost more than it saves.

## Invocation

Use the Agent tool with `model: "haiku"`. Give the subagent the file path, a
one-line description of what the document is, and the output format.

```
Agent(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Summarise <short name>",
  prompt: """
    Read the document at <ABSOLUTE PATH> and produce a structured summary.

    Context: <what this document is — e.g. "a 2026 CHI paper on intentional
    friction in AI interfaces">

    Return ONLY the summary, in these eight sections:

    OVERVIEW — what the document is and does, in one paragraph
    KEY ARGUMENTS — the central claims, as bullets
    METHODOLOGY — how the work was done (or "n/a" for non-empirical work)
    MAIN FINDINGS / CONTRIBUTIONS — what it establishes
    SECTION STRUCTURE — the document's own shape, with approximate lengths
    KEY CONCEPTS — named concepts, frameworks and distinctions it introduces
    NOTABLE QUOTES — up to six, verbatim, with page or section references
    POTENTIAL ATOMIC NOTES — candidate standalone concepts, one line each

    Also state the document's main weakness plainly in OVERVIEW — an
    unevaluated prototype, absent user study, single-site autoethnography.
    That bears directly on how the material should be used.

    Do not editorialise, and do not omit a section. Aim for ~1,200 words.
  """
)
```

**PDFs**: the Read tool handles PDFs directly, so pass the path unchanged. If a
PDF is scanned or extraction returns nothing useful, fall back to
`pdftotext -enc UTF-8 file.pdf -` and pass the text.

**Very long documents** (a full thesis or book): one subagent may not hold it.
Split the source into parts, run one subagent per part with the same output
format, then reconcile the summaries in the main context.

**A different output than the eight-part summary** — a relevance check, say —
just change the format block:

```
Rate this document's relevance to <TOPIC> from 1 to 5.
Reply only: SCORE: [N] | REASON: [one sentence].
```

## Why the eight-part format matters

The `ingest-resource` and `create-literature-note` workflows both expect it.
POTENTIAL ATOMIC NOTES feeds note proposals; KEY CONCEPTS feeds the vault
overlap check; NOTABLE QUOTES supplies the evidence that ends up in a
literature note. Changing the format for a one-off task is fine; changing it in
this skill will break both commands.

## The summary is a first pass

Treat it as triage, not as ground truth. A subagent working without vault
context will miss overlaps that matter and will occasionally flatten a
distinction the source was careful about.

- **Verify specifics against the source** before they enter a note. Quotes,
  numbers and attributions get checked; framing does not survive on the
  subagent's authority alone.
- **Preserve provenance.** When analysis rests on a delegated summary rather
  than a direct reading, say so.
- **A thin summary is a signal.** If it reads as generic, the document may be
  scanned, badly extracted, or genuinely thin. Check the source before
  concluding the last of those.

## Fallback Protocol

**Do not silently fall back.** If delegation fails, say what happened and ask:

- **Subagent returned nothing useful** → "The summary came back empty or
  generic, which usually means text extraction failed. Shall I try
  `pdftotext`, or read the document directly (more context, always works)?"
- **File unreadable** → name the path and the error, and ask whether to
  continue without it.
- **Document too large for one subagent** → offer the split-and-reconcile
  approach, or direct reading of the sections that matter.

Options to present: (1) retry after fixing the cause, (2) direct reading —
costs context, always works, (3) skip this source, (4) stop. Wait for the
user's choice.

## Substituting a local model

Nothing here depends on Haiku specifically; the skill needs only *something
that reads the document elsewhere and returns the eight sections*. A local
model served over an OpenAI-compatible API (LM Studio, Ollama, llama.cpp) works
equally well and keeps the document on your own machine, which matters for
confidential material. Replace the Agent call with a script that chunks the
text, summarises each chunk, and synthesises one structured summary from the
parts — the map-reduce shape a small local model needs.

Two things to know if you go that way: a local run is bounded by free RAM
rather than by tokens, and small models under-summarise when chunks are too
large. Keep chunks well inside the loaded context window.
