#!/usr/bin/env python3
"""Deterministic vault-health audit.

Counts things a model shouldn't: stale maturity caches (usage model — see
vault_maturity.py), orphans, thin/empty notes, type/folder mismatches, missing
metadata, maintenance-tag inventory, hub balance and territory usage, broken
topic references, and Research Programme dormancy.

Emits a JSON report to stdout and archives a dated copy to
60-Analysis/health-snapshots/YYYY-MM-DD.json. The /vault-health command reads the
JSON and writes the interpreted report; this script does not interpret.

Usage:  python3 .claude/scripts/vault_health.py [--pretty] [--no-archive]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (  # noqa: E402
    VaultIndex, VAULT_ROOT, FOLDER_TYPE, KNOWLEDGE_FOLDERS,
    usage_maturity, USAGE_FERN_MIN, USAGE_TREE_MIN,
    parse_research_programme, PROGRAMME_DORMANT_DAYS,
)
from vault_maturity import hub_table  # noqa: E402

# --- thresholds (documented so future runs can notice drift) ---
# Maturity model: usage-based since 2026-07-13 (vault_maturity.py) —
# 🌱 untested (0 consumers), 🌿 drawn on (1-2), 🌲 load-bearing (3+).
NEW_NOTE_GRACE_DAYS = 7    # notes newer than this are exempt from orphan flags
THIN_NOTE_MAX_WORDS = 100  # body below this is flagged as thin/empty
HUB_SPARSE_MAX = 10        # < this = sparse hub
HUB_CROWDED_MIN = 20       # > this = crowded hub
# Programme dormancy threshold lives in vault_lib (PROGRAMME_DORMANT_DAYS).

# --- self-surfacing signal (Phase 3.2) ---
# The callout on the History index is a computed cache, script-owned with the
# same discipline as the maturity tags: regenerated from current state on every
# run, present only when attention-worthy, never hand-managed. It fires on
# exactly two things — questions the vault cannot answer itself (programme
# dormancy) and regressions since the last snapshot. Everything else stays on
# the health page. Written into History.md between these markers, in place, only
# when --write-callout is passed (mutation is opt-in, like vault_maturity --write).
HISTORY_PAGE = "00-Index/History.md"
CALLOUT_START = "<!-- vault-health:callout:start -->"
CALLOUT_END = "<!-- vault-health:callout:end -->"
CALLOUT_ANCHOR = "## Recent History"  # callout sits just above this


def age_days(d, today: date):
    return (today - d).days if d else None


def build_report(index: VaultIndex, today: date) -> dict:
    knowledge = index.knowledge_notes()

    # --- counts ---
    per_folder = {}
    for n in index.notes:
        per_folder[n.folder] = per_folder.get(n.folder, 0) + 1

    conn_of = {n.rel: index.connections(n) for n in knowledge}
    note_like = [n for n in knowledge if n.folder in ("30-Notes", "45-Literature")]

    # --- usage maturity (ground truth) and stale caches ---
    usage = index.usage()
    per_maturity = {"🌱": 0, "🌿": 0, "🌲": 0}
    stale_maturity_cache = []
    untested_age_buckets = {"<90d": 0, "90-365d": 0, ">365d": 0, "unknown": 0}
    for n in knowledge:
        count = len(usage.get(n.rel, ()))
        want = usage_maturity(count)
        per_maturity[want] += 1
        if n.maturity != want:
            stale_maturity_cache.append(
                {"note": n.rel, "tagged": n.maturity, "computed": want, "used_by": count})
        if count == 0:
            a = age_days(n.created, today)
            if a is None:
                untested_age_buckets["unknown"] += 1
            elif a < 90:
                untested_age_buckets["<90d"] += 1
            elif a <= 365:
                untested_age_buckets["90-365d"] += 1
            else:
                untested_age_buckets[">365d"] += 1

    # --- thin or empty notes ---
    thin_notes = [{"note": n.rel, "words": n.word_count}
                  for n in knowledge if n.word_count < THIN_NOTE_MAX_WORDS]
    thin_notes.sort(key=lambda x: x["words"])

    # --- orphans (0 connections, past grace) ---
    orphans = []
    for n in knowledge:
        if conn_of[n.rel] == 0:
            a = age_days(n.created, today)
            if a is not None and a < NEW_NOTE_GRACE_DAYS:
                continue
            orphans.append({"note": n.rel, "created": n.created.isoformat() if n.created else None})

    # --- type / folder mismatches ---
    type_mismatches = []
    for n in index.notes:
        expected = FOLDER_TYPE.get(n.folder)
        if expected and n.type and n.type != expected:
            type_mismatches.append({"note": n.rel, "type": n.type, "expected": expected})

    # --- missing metadata ---
    missing_tldr, missing_key, missing_topics = [], [], []
    for n in knowledge:
        if not n.has_tldr:
            missing_tldr.append(n.rel)
        elif not n.has_key:
            missing_key.append(n.rel)
    for n in note_like:
        if not n.topics:
            missing_topics.append(n.rel)

    # --- maintenance-tag inventory ---
    maintenance_tags = [{"note": n.rel, "tags": n.maint_tags}
                        for n in index.notes if n.maint_tags]

    # --- hub balance ---
    hubs = []
    for n in knowledge:
        if n.folder != "20-Hubs":
            continue
        members = index.backlink_count_from_knowledge(n.rel)
        status = ("sparse" if members < HUB_SPARSE_MAX
                  else "crowded" if members > HUB_CROWDED_MIN else "balanced")
        hubs.append({"hub": n.name, "members": members, "status": status})
    hubs.sort(key=lambda x: -x["members"])

    # --- broken topic references ---
    broken_references = []
    for n in index.notes:
        for target in n.topics:
            if not index.resolves(target):
                broken_references.append({"note": n.rel, "field": "topics", "target": target})

    # --- programme dormancy ---
    # Computed from the mtimes of each programme's MOCs and hubs; nothing stored.
    programme = parse_research_programme(index, today)

    total_conn = sum(conn_of.values())
    n_notes = len(knowledge)
    return {
        "generated": today.isoformat(),
        "thresholds": {
            "usage_fern_min": USAGE_FERN_MIN, "usage_tree_min": USAGE_TREE_MIN,
            "new_note_grace_days": NEW_NOTE_GRACE_DAYS,
            "thin_note_max_words": THIN_NOTE_MAX_WORDS,
            "hub_sparse_max": HUB_SPARSE_MAX, "hub_crowded_min": HUB_CROWDED_MIN,
            "programme_dormant_days": PROGRAMME_DORMANT_DAYS,
        },
        "connection_model": "knowledge-subgraph in+out, hubs included, admin folders excluded",
        "maturity_model": ("usage-based: 🌱 untested (0 consumers), 🌿 drawn on (1-2), "
                           "🌲 load-bearing (3+); consumers = MOCs, drafts, analyses; "
                           "reconcile with vault_maturity.py --write"),
        "summary": {
            "content_files": len(index.notes),
            "knowledge_notes": n_notes,
            "per_folder": dict(sorted(per_folder.items())),
            "maturity_distribution": per_maturity,
            "untested_age_buckets": untested_age_buckets,
            "avg_connections": round(total_conn / n_notes, 2) if n_notes else 0,
            "counts": {
                "stale_maturity_cache": len(stale_maturity_cache),
                "orphans": len(orphans),
                "thin_notes": len(thin_notes),
                "type_folder_mismatches": len(type_mismatches),
                "missing_tldr": len(missing_tldr),
                "missing_key": len(missing_key),
                "missing_topics": len(missing_topics),
                "maintenance_tagged": len(maintenance_tags),
                "sparse_hubs": sum(1 for h in hubs if h["status"] == "sparse"),
                "crowded_hubs": sum(1 for h in hubs if h["status"] == "crowded"),
                "broken_references": len(broken_references),
                "dormant_programmes": len(programme.get("dormant", [])),
            },
        },
        "stale_maturity_cache": stale_maturity_cache,
        "orphans": orphans,
        "thin_notes": thin_notes,
        "hub_usage": hub_table(index),
        "type_folder_mismatches": type_mismatches,
        "missing_metadata": {
            "missing_tldr": missing_tldr,
            "missing_key": missing_key,
            "missing_topics": missing_topics,
        },
        "maintenance_tags": maintenance_tags,
        "hub_balance": hubs,
        "broken_references": broken_references,
        "research_programme": programme,
    }


def load_prev_snapshot(snap_dir: Path, today: date) -> dict | None:
    """Most-recent archived snapshot strictly before today (baseline if none).

    Filenames are ISO dates, so lexical order is chronological. Re-running on the
    same day still diffs against the previous day, not the snapshot we are about
    to overwrite.
    """
    if not snap_dir.is_dir():
        return None
    today_name = f"{today.isoformat()}.json"
    prior = sorted(p for p in snap_dir.glob("????-??-??.json") if p.name < today_name)
    if not prior:
        return None
    try:
        return json.loads(prior[-1].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _programme_unresolved(report: dict):
    """Yield (n, question, target) for every unresolved programme link."""
    rp = report.get("research_programme", {})
    for e in rp.get("active", []) + rp.get("emeritus", []):
        for target in e.get("unresolved_links", []):
            yield e.get("n"), e.get("question"), target


def compute_regressions(prev: dict | None, curr: dict) -> dict:
    """What got worse since the previous snapshot — the only deltas worth a callout.

    New orphans, newly-broken topic references, and Research Programme entries now
    pointing at a MOC/hub that no longer resolves. First run (no prior) is a
    baseline and raises nothing.
    """
    if not prev:
        return {"baseline": True, "prev_date": None, "new_orphans": [],
                "new_broken_references": [], "new_unresolved_programme_links": []}

    prev_orphans = {o["note"] for o in prev.get("orphans", [])}
    new_orphans = [o for o in curr["orphans"] if o["note"] not in prev_orphans]

    prev_broken = {(b["note"], b["target"]) for b in prev.get("broken_references", [])}
    new_broken = [b for b in curr["broken_references"]
                  if (b["note"], b["target"]) not in prev_broken]

    prev_pu = {(n, t) for (n, _q, t) in _programme_unresolved(prev)}
    new_pu = [{"n": n, "question": q, "target": t}
              for (n, q, t) in _programme_unresolved(curr) if (n, t) not in prev_pu]

    return {"baseline": False, "prev_date": prev.get("generated"),
            "new_orphans": new_orphans, "new_broken_references": new_broken,
            "new_unresolved_programme_links": new_pu}


def render_callout(report: dict, regressions: dict) -> str | None:
    """The computed callout markdown, or None when nothing is attention-worthy.

    Fires only on dormancy questions and regressions; everything else lives on
    the health page. British English throughout.
    """
    dormant = [e for e in report["research_programme"].get("active", []) if e.get("dormant")]

    reg_lines = []
    for o in regressions["new_orphans"]:
        reg_lines.append(f"> - New orphan: [[{Path(o['note']).stem}]] — no links in or out.")
    for b in regressions["new_broken_references"]:
        reg_lines.append(f"> - Broken reference in [[{Path(b['note']).stem}]]: "
                         f"`{b['target']}` no longer resolves.")
    for p in regressions["new_unresolved_programme_links"]:
        reg_lines.append(f"> - Research Programme #{p['n']} points at `{p['target']}`, "
                         f"which no longer exists.")

    q_lines = []
    for e in dormant:
        since = e.get("newest_content") or "an unknown date"
        q_lines.append(f"> - [[Research Programme]] #{e.get('n')} — “{e.get('question')}” "
                       f"has had no new work since {since}. Still live, or emeritus?")

    if not reg_lines and not q_lines:
        return None

    parts = ["> [!warning] Vault health check-in"]
    if reg_lines:
        prev = regressions.get("prev_date")
        parts.append(f"> **Since your last check ({prev}):**" if prev
                     else "> **Since your last check:**")
        parts.extend(reg_lines)
    if q_lines:
        if reg_lines:
            parts.append(">")
        parts.append("> **A question only you can answer:**")
        parts.extend(q_lines)
    parts.append(">")
    parts.append("> _Regenerated on every `/vault-health` run — fix the cause "
                 "and it clears itself._")
    return "\n".join(parts)


def sync_callout(callout: str | None) -> str:
    """Write (or clear) the callout on the History index, between fixed markers.

    Idempotent: replaces whatever is between the markers, inserting the marker
    block just above the Recent History heading on first run. When there is no
    callout the markers remain with nothing between them, so placement is stable
    and the next callout lands in the same spot. Returns a short status word.
    """
    path = VAULT_ROOT / HISTORY_PAGE
    text = path.read_text(encoding="utf-8")
    inner = f"\n{callout}\n" if callout else "\n"
    block = f"{CALLOUT_START}{inner}{CALLOUT_END}"

    if CALLOUT_START in text and CALLOUT_END in text:
        pre = text[:text.index(CALLOUT_START)]
        post = text[text.index(CALLOUT_END) + len(CALLOUT_END):]
        new_text = pre + block + post
        status = "set" if callout else "cleared"
    elif CALLOUT_ANCHOR in text:
        idx = text.index(CALLOUT_ANCHOR)
        new_text = text[:idx] + block + "\n\n" + text[idx:]
        status = "inserted" if callout else "inserted-empty"
    else:
        return "no-anchor"

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return status


def main():
    ap = argparse.ArgumentParser(description="Deterministic vault health audit.")
    ap.add_argument("--pretty", action="store_true", help="indent JSON output")
    ap.add_argument("--no-archive", action="store_true", help="skip writing the dated snapshot")
    ap.add_argument("--write-callout", action="store_true",
                    help="sync the computed callout into 00-Index/History.md (mutates the vault)")
    args = ap.parse_args()

    today = date.today()
    index = VaultIndex()
    report = build_report(index, today)

    snap_dir = VAULT_ROOT / "60-Analysis" / "health-snapshots"
    prev = load_prev_snapshot(snap_dir, today)
    report["regressions"] = compute_regressions(prev, report)
    report["callout_markdown"] = render_callout(report, report["regressions"])

    if not args.no_archive:
        snap_dir.mkdir(parents=True, exist_ok=True)
        snap_path = snap_dir / f"{today.isoformat()}.json"
        snap_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"snapshot: {snap_path.relative_to(VAULT_ROOT)}", file=sys.stderr)

    if args.write_callout:
        status = sync_callout(report["callout_markdown"])
        print(f"callout: {status} ({HISTORY_PAGE})", file=sys.stderr)

    print(json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
