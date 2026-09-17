#!/usr/bin/env python3
"""Usage-maturity reconciler: stamps the 🌱🌿🌲 cache from how notes are used.

Maturity records USE, not structure: how many distinct higher-level artefacts
(MOCs, drafts in 50-Drafts, analyses in 60-Analysis) draw on a knowledge note.
    🌱 untested (0 consumers) · 🌿 drawn on (1-2) · 🌲 load-bearing (3+)

The wiki-links in consumer files are the ground truth; the 🌱/🌿/🌲 tag and
`used-by:` count stamped in each note's frontmatter are a regenerable cache.
This script recomputes the truth and rewrites stale frontmatter. It is safe to
run at any time and is invoked as the final step of any command that creates
or modifies consumer files (/create-moc, /create-draft,
/ingest-resource), plus /vault-health as backstop.

Usage:
    python3 .claude/scripts/vault_maturity.py             # dry run: report changes
    python3 .claude/scripts/vault_maturity.py --write     # apply changes
    python3 .claude/scripts/vault_maturity.py --hubs      # hub-territory usage table
    python3 .claude/scripts/vault_maturity.py --json      # machine-readable report
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (  # noqa: E402
    VaultIndex, VAULT_ROOT, MATURITY_TAGS, FRONTMATTER_RE, _norm,
    usage_maturity, USAGE_FERN_MIN, USAGE_TREE_MIN,
)

EMOJI_RE = re.compile("|".join(MATURITY_TAGS))
USED_BY_RE = re.compile(r"^used-by:\s*\S.*$", re.MULTILINE)
TAGS_LINE_RE = re.compile(r"^tags:.*$", re.MULTILINE)
TYPE_LINE_RE = re.compile(r"^type:.*$", re.MULTILINE)


def plan_changes(index: VaultIndex):
    """Yield per-note reconciliation plans: (note, want_tag, count, consumers)."""
    usage = index.usage()
    for note in index.knowledge_notes():
        consumers = usage.get(note.rel, set())
        count = len(consumers)
        want = usage_maturity(count)
        yield note, want, count, sorted(consumers)


def restamp(note, want_tag: str, count: int) -> tuple[bool, str]:
    """Rewrite the note's frontmatter cache. Returns (changed, detail)."""
    text = note.path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return False, "no frontmatter — skipped"
    fm, rest = m.group(0), text[m.end():]
    orig = fm

    emojis = EMOJI_RE.findall(fm)
    if len(set(emojis)) > 1:
        # Collapse duplicates: replace the first, delete the rest.
        first_done = [False]

        def _sub(mm):
            if first_done[0]:
                return ""
            first_done[0] = True
            return want_tag
        fm = EMOJI_RE.sub(_sub, fm)
        fm = re.sub(r",\s*([\]\)])", r"\1", fm)  # tidy dangling commas in lists
        fm = re.sub(r"\[\s*,", "[", fm)
    elif emojis:
        fm = EMOJI_RE.sub(want_tag, fm)
    else:
        tags_m = TAGS_LINE_RE.search(fm)
        if tags_m:
            line = tags_m.group(0)
            if "[" in line:
                new_line = line.replace("[", f"[{want_tag}, ", 1) if line.rstrip() != "tags: []" \
                    else line.replace("[]", f"[{want_tag}]")
                new_line = new_line.replace(f"[{want_tag}, ]", f"[{want_tag}]")
                fm = fm.replace(line, new_line, 1)
            else:  # block-style list: insert first item after the tags: line
                fm = fm.replace(line, f"{line}\n  - {want_tag}", 1)
        else:
            anchor = TYPE_LINE_RE.search(fm)
            if anchor:
                fm = fm.replace(anchor.group(0), f"{anchor.group(0)}\ntags: [{want_tag}]", 1)
            else:
                fm = fm.replace("---\n", f"---\ntags: [{want_tag}]\n", 1)

    used_line = f"used-by: {count}"
    if USED_BY_RE.search(fm):
        fm = USED_BY_RE.sub(used_line, fm)
    else:
        tags_m = TAGS_LINE_RE.search(fm)
        if tags_m and "[" in tags_m.group(0):
            fm = fm.replace(tags_m.group(0), f"{tags_m.group(0)}\n{used_line}", 1)
        else:
            fm = re.sub(r"\n---\s*\n$", f"\n{used_line}\n---\n", fm)

    if fm == orig:
        return False, "already current"
    note.path.write_text(fm + rest, encoding="utf-8")
    return True, "restamped"


def hub_table(index: VaultIndex) -> list[dict]:
    """Per-hub territory usage: how tested is each hub's region of the vault?"""
    usage = index.usage()
    hubs = [n for n in index.knowledge_notes() if n.folder == "20-Hubs"]
    hub_by_name = {_norm(h.name): h for h in hubs}
    for h in hubs:
        for alias in h.aliases:
            hub_by_name.setdefault(_norm(alias), h)
    territory = {h.rel: [] for h in hubs}
    for n in index.knowledge_notes():
        if n.folder != "30-Notes":
            continue
        for t in n.topics:
            h = hub_by_name.get(_norm(t))
            if h:
                territory[h.rel].append(n)
    rows = []
    for h in hubs:
        terr = territory[h.rel]
        used = [n for n in terr if usage.get(n.rel)]
        consumers = set()
        for n in used:
            consumers |= usage[n.rel]
        rows.append({
            "hub": h.name,
            "notes": len(terr),
            "used": len(used),
            "pct_used": round(100 * len(used) / len(terr)) if terr else None,
            "distinct_consumers": len(consumers),
        })
    rows.sort(key=lambda r: (-(r["pct_used"] or 0), -r["notes"]))
    return rows


def main():
    ap = argparse.ArgumentParser(description="Reconcile usage-maturity tags with ground truth.")
    ap.add_argument("--write", action="store_true", help="apply changes (default: dry run)")
    ap.add_argument("--hubs", action="store_true", help="print hub-territory usage table")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    index = VaultIndex()

    if args.hubs:
        rows = hub_table(index)
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            print(f"{'hub':<40}{'notes':>6}{'used':>6}{'%':>5}{'consumers':>11}")
            for r in rows:
                pct = f"{r['pct_used']}" if r["pct_used"] is not None else "-"
                print(f"{r['hub']:<40}{r['notes']:>6}{r['used']:>6}{pct:>5}"
                      f"{r['distinct_consumers']:>11}")
        return

    dist = {"🌱": 0, "🌿": 0, "🌲": 0}
    changes, errors = [], []
    for note, want, count, consumers in plan_changes(index):
        dist[want] += 1
        stale = note.maturity != want
        # used-by staleness check needs the raw frontmatter; cheap re-read only if tag is clean
        if not stale:
            fm_text = note.path.read_text(encoding="utf-8", errors="replace")
            m = USED_BY_RE.search(FRONTMATTER_RE.match(fm_text).group(0)
                                  if FRONTMATTER_RE.match(fm_text) else "")
            stale = not m or m.group(0) != f"used-by: {count}"
        if not stale:
            continue
        entry = {"note": note.rel, "from": note.maturity, "to": want, "used_by": count,
                 "consumers": consumers}
        if args.write:
            changed, detail = restamp(note, want, count)
            entry["result"] = detail
            if detail == "no frontmatter — skipped":
                errors.append(entry)
                continue
        changes.append(entry)

    total = sum(dist.values())
    if args.json:
        print(json.dumps({"distribution": dist, "total": total,
                          "changes": changes, "errors": errors},
                         ensure_ascii=False, indent=2))
    else:
        mode = "applied" if args.write else "dry run — would change"
        print(f"knowledge notes: {total} | 🌱 {dist['🌱']} · 🌿 {dist['🌿']} · 🌲 {dist['🌲']}"
              f"  (🌿 at {USAGE_FERN_MIN}+, 🌲 at {USAGE_TREE_MIN}+ distinct consumers)")
        print(f"{mode}: {len(changes)} notes")
        for e in changes:
            frm = e["from"] or "untagged"
            print(f"  {frm} -> {e['to']}  used-by {e['used_by']:>2}  {e['note']}")
        for e in errors:
            print(f"  ERROR {e['note']}: {e['result']}")


if __name__ == "__main__":
    main()
