---
description: Audit vault structure, maintain the health page, and surface attention-worthy state on the History index
argument-hint: "[--report-only]"
skills: zettelkasten-methods, obsidian-patterns
---

# Vault Health Check

Audit the vault, maintain `00-Index/Vault Health.md` (the canonical record), and set or clear an attention **callout** on `00-Index/History.md` (the signal that comes to the user). **The scripts count and compute the signal; Claude interprets the page.** All arithmetic — maturity distribution, orphans, thin notes, metadata gaps, hub balance, broken references, regressions since the last run, and which callout to raise — comes from the deterministic scripts. The model's job is judgement on the *page*: what the numbers mean, what matters most, what the user should (or needn't) do.

**Two modes** (Phase 3.2):
- **Interactive (default)** — regenerate the page and callout, then *offer* to work through any callout-worthy items and re-run to clear them.
- **`--report-only`** — regenerate the page and callout and stop. No prompting. The unattended seam, for a future scheduled full-page refresh.

**The settled trigger is not a scheduled job.** The `history-update` skill offers the *light* callout refresh (`vault_health.py --write-callout`, no interpreted-page rewrite) whenever a history entry is written and the last run is over a week old — so the signal stays fresh as a side-effect of work already happening. `--report-only` remains available if a full-page unattended refresh is ever wanted.

## Skills Required

- **zettelkasten-methods** - Vault conventions, type mappings, and the usage-maturity model
- **obsidian-patterns** - Only if follow-up exploration of specific flagged notes is needed

## The callout — what it is and what fires it

`00-Index/History.md` is the one maintenance-adjacent surface the user passes through voluntarily (after a session they land there to link to their latest daily entry). The callout sits just above the Recent History section, **computed and script-owned with the same discipline as the maturity cache**: `vault_health.py --write-callout` regenerates it from current state on every run, between fixed markers. The user never deletes it — they fix the cause and the next run regenerates a callout-free page.

It fires on **only two things**, both computed by the script:
1. **Questions the vault cannot answer itself** — a Research Programme that is *dormant* (no new work in its territory for 12+ months **and** not reviewed within 12 months).
2. **Regressions since the last snapshot** — a new orphan, a newly-broken reference, or a programme now pointing at a deleted MOC/hub. Diffed against the previous snapshot in `60-Analysis/health-snapshots/`, so the semantics are "since your last run", independent of cadence.

Everything else — standing orphan/broken-reference lists, thin notes, missing metadata, type mismatches, hub balance, a hub crossing the split line — stays **on the health page, never in the callout**. Self-healing findings (stale maturity cache) and the user's own maintenance tags (`_needs-zotero`) are never surfaced in the callout at all.

## Workflow

### Step 1: Reconcile Maturity (Backstop)

Run the maturity reconciler first, so the audit reads current tags and any drift from manual Obsidian edits is healed:

```
python3 .claude/scripts/vault_maturity.py --write
```

Note any graduations it prints — they belong in the report ("since the last audit, N notes graduated through use").

### Step 2: Run the Health Script (and sync the callout)

```
python3 .claude/scripts/vault_health.py --pretty --write-callout
```

This emits the JSON report, archives a dated snapshot to `60-Analysis/health-snapshots/YYYY-MM-DD.json`, computes regressions against the previous snapshot, and **writes or clears the History.md callout in place**. The callout is fully rendered by the script (`callout_markdown` in the JSON) so it is identical whichever model runs the command — do not hand-edit it.

**Key fields:**
- `summary.maturity_distribution` — 🌱 untested / 🌿 drawn on / 🌲 load-bearing counts (usage model: consumers are MOCs, drafts, analyses)
- `summary.untested_age_buckets` — how long untested notes have been waiting (context, not a to-do list: the untested half of a Zettelkasten is its option value)
- `hub_usage` — the territory heat map: per-hub % of notes ever drawn on. This is the "where is the vault strong/lacking" orientation table
- `regressions` — the deltas since the previous snapshot (`baseline: true` on a first run — nothing to compare against, so no regressions raised)
- `callout_markdown` — the exact callout the script wrote (or `null` when the page is callout-free); the interactive offer below works from the same underlying state
- `research_programme.active[].dormant` / `.reviewed` — dormancy (respecting the `reviewed:` marker) and when each programme was last reviewed
- `stale_maturity_cache` — should be empty after Step 1; anything here is a note the reconciler could not stamp (e.g. missing frontmatter) — investigate
- `orphans`, `thin_notes`, `type_folder_mismatches`, `missing_metadata`, `broken_references` — genuine outliers worth listing on the page
- `maintenance_tags`, `hub_balance` — page-only inventories

### Step 3: Interpret and Rewrite the Report Page

Rewrite `00-Index/Vault Health.md`. **The file has a fixed two-part structure — preserve it exactly:**

1. **Header + Live Snapshot (do not regenerate — carry over verbatim):** the frontmatter (update `last-run:` to today), the `[!warning] How this page updates` callout (update its "Last run:" date), and the **Live Snapshot** section containing two `dataviewjs` blocks (live maturity distribution; live territory heat map from `used-by` frontmatter). These blocks self-update in Obsidian — copy them through unchanged unless the maturity model itself has changed.

2. **Report section (regenerate from this run's data):**

```markdown
## Report (as of last run: YYYY-MM-DD)

### Summary

- **Knowledge notes at last run**: {n} — {🌱 n} untested ({pct}%), {🌿 n} drawn on, {🌲 n} load-bearing
- **Graduations since last run**: {n or "none"}
- **Genuine outliers**: {orphans + thin + broken counts}
- **Regressions since last snapshot**: {from `regressions` — new orphans/broken refs/programme links, or "none"}

### Reading the Map

[Interpretation of the hub_usage table: which territories are load-bearing (cite
tested % AND distinct-consumer counts — the live block cannot show consumers),
which are untested reserves, anything that shifted since the previous snapshot.
Untested is not bad — it is unexercised option value. Flag only genuine surprises.
Include the untested-age buckets as one line of context.]

### Outliers Worth Attention

[Orphans, thin/empty notes, broken references, type mismatches, missing TLDR/Key/topics
— as short lists with a suggested action each. Frame as opportunities, not errors.]

### Maintenance Tags

[Inventory of _-prefixed tags with counts]

### Research Programme

[From `research_programme` in the JSON. One line per active programme ONLY if
something is worth saying; otherwise a single line: "All {n} programmes have gained
new content within the last {x} months." Report `unresolved_links` if any — a
programme pointing at a MOC or hub that no longer exists is a real defect (and one
that also fires the callout as a regression).

**Dormancy is now surfaced by the callout, not just the console.** For each programme
in `dormant`, the script has already raised the "still live, or emeritus?" question in
the History.md callout. On the page, simply note which programmes are dormant and
awaiting an answer. Never move a programme to Emeritus yourself, and never propose
retiring one just because it is quiet.]

### Observations

[Max 3 interpretive observations, prioritised. Optionally ONE serendipitous
observation — a forgotten note or an unusually load-bearing cluster — per the
serendipity-as-garnish constraint. Page-only, never homework.]
```

Compare against the previous snapshot in `60-Analysis/health-snapshots/` where useful — the interesting story is usually the delta, not the totals.

### Step 4: Branch on Mode

**If invoked with `--report-only`:** stop here. Give the short console summary (Step 6) and do not prompt. The page and callout already reflect current state.

**Otherwise (interactive default):** proceed to Step 5.

### Step 5 (interactive only): Offer to Work Through the Callout

If `callout_markdown` is non-null, *offer* — do not assume:

> The health check raised {N} item(s) on the History callout. Shall we work through them now, or leave the report for later?

The user can decline and keep just the report. For approved fixes, use ordinary editing:

- **A new orphan** — re-link it into its territory (add a `topics:` hub link or a body link).
- **A broken reference** — mend the `topics:` link, or add the intended alias to the target hub.
- **A programme pointing at a deleted MOC/hub** — correct or remove the link on `00-Index/Research Programme.md`.
- **A dormancy question** — put it to the user and act on their answer:
  - *"Still live / slow-burning"* → stamp the programme entry on `Research Programme.md` with a review marker so it does not re-fire for a year. Add, under that programme's `### N.` entry, a line in the page's house style:
    `- **Reviewed**: YYYY-MM-DD — <the user's words, e.g. "still live, slow-burning">`
    (The parser reads any `**Reviewed**: YYYY-MM-DD` line; the note after the em dash is for the human.)
  - *"Emeritus"* → with the user's confirmation, move the entry to the **Emeritus** section at the foot of the page (never delete it — dormant questions revive), following the existing Emeritus entry's format.

Then, *mention* the health page's Tier-2 backlog as an optional batchable pass — never the default grind:

> There are also {N} notes missing metadata / {N} thin hub intros on the page — a hygiene sweep if you fancy it, or leave it?

**After any fixes, re-run Steps 1–2** (`vault_maturity.py --write` then `vault_health.py --pretty --write-callout`) so the page and callout reflect the fixed state and the callout clears itself. Then rewrite the page (Step 3) and give the summary. The loop closes itself.

### Step 6: Return Summary

Console summary: 3-5 lines — maturity distribution, graduations, outlier count, whether the callout is set or clear, and at most 3 priority actions. If nothing needs attention, say so plainly.

## Guidelines

Follow the vault's spelling convention throughout.

**Epistemological stance:** frame issues as opportunities, suggest rather than mandate, acknowledge the user's authority over what counts as a problem. The 🌱 pile is not a backlog — never present untested notes as work owed. The callout helps with the user's work; it does not create new work — the vault never turns a quiet programme or a large hub into homework.

**Values alignment:** explain why a flagged item matters (Value 2: Transparency); give the specific command or edit that would address it (Value 4: Augmentation); prefer expansion or linking over deletion (Value 7: Cognitive Preservation). The signal-comes-to-the-user design preserves agency (Value 1): the callout informs, the user decides.

**The `reviewed:` marker is legitimate stored state** — a human decision not derivable from links, the same category as `#human`. It is the *only* thing this command writes to `Research Programme.md` without an explicit content change, and only ever in answer to a dormancy question the user has actually answered.

**Error handling:** if a script fails, report the error and stop — do not fall back to counting by hand or via MCP queries; that is the failure mode this design replaced.

## Example Usage

```
/vault-health                # interactive: report + callout, then offer to fix
/vault-health --report-only  # unattended: report + callout only, no prompting
```

Results written to `00-Index/Vault Health.md`; the attention callout set or cleared on `00-Index/History.md`.
