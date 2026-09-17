"""Reusable vault parsing and wiki-link graph indexing for the maintenance scripts.

Shared core for vault_health.py and vault_maturity.py.
Principle: scripts count deterministically; Claude interprets.

Connection model: a note's "connections" are its distinct
neighbours in the KNOWLEDGE SUBGRAPH only — files in 30-Notes, 20-Hubs, 10-MOCs,
45-Literature — counting both directions (out-links and back-links) and
including hub (topics) links. Edges to/from administrative files (35-History,
99-Archive, 00-Index, 50-Drafts, 40-Resources, 41-Attachments, 80-Fleeting,
90-Templates) are excluded so the auto-accruing history/report backlinks don't
inflate the metric.
"""
from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# Vault root = three levels up from .claude/scripts/vault_lib.py
VAULT_ROOT = Path(__file__).resolve().parents[2]

MATURITY_TAGS = ("🌱", "🌿", "🌲")
MATURITY_ORDER = {"🌱": 1, "🌿": 2, "🌲": 3}

# Usage-maturity model (it replaced an earlier connection-count model):
# a knowledge note's maturity records how often it has been DRAWN ON by
# higher-level artefacts ("consumers"), not how connected or long it is.
#   🌱 untested      — 0 distinct consumers
#   🌿 drawn on      — 1-2 distinct consumers
#   🌲 load-bearing  — 3+ distinct consumers
# Consumers are files in 10-MOCs, 50-Drafts, 60-Analysis. Hubs are NOT
# consumers (hub membership is shelving, not use). 99-Archive is excluded
# because it holds deprecated tooling, not completed intellectual work — if
# finished projects ever move there, add it. Ground truth is the wiki-links
# in consumer files; frontmatter tags are a regenerable cache stamped by
# vault_maturity.py.
CONSUMER_FOLDERS = ("10-MOCs", "50-Drafts", "60-Analysis")
USAGE_FERN_MIN = 1   # >=1 distinct consumer  -> 🌿
USAGE_TREE_MIN = 3   # >=3 distinct consumers -> 🌲


def usage_maturity(consumer_count: int) -> str:
    if consumer_count >= USAGE_TREE_MIN:
        return "🌲"
    if consumer_count >= USAGE_FERN_MIN:
        return "🌿"
    return "🌱"

# Files in these folders participate in connection counting.
KNOWLEDGE_FOLDERS = ("30-Notes", "20-Hubs", "10-MOCs", "45-Literature")

# Content folders we parse for counts/metadata (superset of knowledge folders).
CONTENT_FOLDERS = KNOWLEDGE_FOLDERS + ("40-Resources", "50-Drafts", "00-Index")

# Expected `type:` per folder (for type-folder mismatch checks).
FOLDER_TYPE = {
    "30-Notes": "note",
    "20-Hubs": "hub",
    "10-MOCs": "moc",
    "45-Literature": "literature-note",
    "40-Resources": "resource",
    "50-Drafts": "draft",
    "00-Index": "index",
}

# Never walked into.
IGNORE_DIR_NAMES = {".git", ".obsidian", ".claude", ".smart-env", ".trash",
                    "node_modules", "41-Attachments"}

# Repo scaffolding, not vault content: a folder README explains what the folder
# holds and must never be counted as a note or flagged for a missing type.
IGNORE_FILE_NAMES = {"README.md"}

# Capture [[target]], [[target|alias]], [[target#heading]] and ![[embeds]].
# Group 1 is the link target (before any # or |).
WIKILINK_RE = re.compile(r"\[\[([^\]\|#\n]+)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TLDR_RE = re.compile(r">\s*\[!tldr\]", re.IGNORECASE)
KEY_RE = re.compile(r"\*\*Key\*\*\s*::")


def _norm(name: str) -> str:
    """Normalise a link target or filename to a resolution key (basename, lowercased)."""
    name = name.strip()
    if "/" in name:
        name = name.rsplit("/", 1)[-1]
    if name.lower().endswith(".md"):
        name = name[:-3]
    return name.lower()


def _as_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return datetime.strptime(value[:10], "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def _tag_list(raw) -> list:
    """Frontmatter tags may be a list, a single scalar, or absent. Return list of strings."""
    if raw is None:
        return []
    if isinstance(raw, (list, tuple)):
        items = raw
    else:
        items = [raw]
    out = []
    for t in items:
        if t is None:
            continue
        s = str(t).strip().lstrip("#")
        if s:
            out.append(s)
    return out


class Note:
    __slots__ = ("path", "rel", "folder", "name", "type", "created", "mtime",
                 "tags", "maturity", "maint_tags", "topics", "aliases",
                 "has_tldr", "has_key", "links_out", "is_knowledge", "word_count")

    def __init__(self, path: Path):
        self.path = path
        self.rel = str(path.relative_to(VAULT_ROOT))
        self.folder = self.rel.split("/", 1)[0]
        self.name = path.stem
        self.is_knowledge = self.folder in KNOWLEDGE_FOLDERS

        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = self._split_frontmatter(text)

        self.type = fm.get("type")
        self.created = _as_date(fm.get("created"))
        try:
            self.mtime = datetime.fromtimestamp(path.stat().st_mtime).date()
        except OSError:
            self.mtime = None
        self.tags = _tag_list(fm.get("tags"))
        self.maturity = next((t for t in self.tags if t in MATURITY_TAGS), None)
        self.maint_tags = sorted(t for t in self.tags if t.startswith("_"))
        self.topics = self._link_targets(fm.get("topics"))
        self.aliases = [str(a).strip() for a in _tag_list(fm.get("aliases"))]

        self.has_tldr = bool(TLDR_RE.search(body))
        self.has_key = bool(KEY_RE.search(body))
        self.word_count = len(body.split())
        # All wiki-link targets across the WHOLE file (frontmatter topics + body).
        self.links_out = {t.strip() for t in WIKILINK_RE.findall(text) if t.strip()}

    @staticmethod
    def _split_frontmatter(text: str):
        m = FRONTMATTER_RE.match(text)
        if not m:
            return {}, text
        raw = m.group(1)
        data = {}
        if yaml is not None:
            try:
                loaded = yaml.safe_load(raw)
                if isinstance(loaded, dict):
                    data = loaded
            except yaml.YAMLError:
                data = {}
        return data, text[m.end():]

    @staticmethod
    def _link_targets(raw) -> list:
        """Extract wiki-link targets from a frontmatter field (e.g. topics/problems)."""
        if raw is None:
            return []
        items = raw if isinstance(raw, (list, tuple)) else [raw]
        out = []
        for item in items:
            for t in WIKILINK_RE.findall(str(item)):
                t = t.strip()
                if t:
                    out.append(t)
        return out


class VaultIndex:
    def __init__(self, root: Path = VAULT_ROOT):
        self.root = root
        self.notes: list[Note] = []          # parsed content-folder notes
        self.by_rel: dict[str, Note] = {}
        self._resolve_all: dict[str, Path] = {}       # any .md in vault: key -> path
        self._resolve_knowledge: dict[str, str] = {}  # key -> knowledge note rel path
        self._neighbours: dict[str, set] = {}         # rel -> set(rel) in knowledge subgraph
        self._build()

    def _build(self):
        # 1. Inventory EVERY markdown file (for broken-link resolution across the vault).
        for path in self._walk_md(self.root):
            self._resolve_all.setdefault(_norm(path.stem), path)

        # 2. Parse content-folder notes.
        for folder in CONTENT_FOLDERS:
            base = self.root / folder
            if not base.is_dir():
                continue
            for path in self._walk_md(base):
                note = Note(path)
                self.notes.append(note)
                self.by_rel[note.rel] = note

        # 3. Resolution map for the knowledge subgraph (basenames + aliases).
        for note in self.notes:
            if not note.is_knowledge:
                continue
            self._resolve_knowledge.setdefault(_norm(note.name), note.rel)
            for alias in note.aliases:
                self._resolve_knowledge.setdefault(_norm(alias), note.rel)

        # 4. Build the undirected knowledge subgraph.
        for note in self.notes:
            self._neighbours.setdefault(note.rel, set())
        for note in self.notes:
            if not note.is_knowledge:
                continue
            for target in note.links_out:
                tgt_rel = self._resolve_knowledge.get(_norm(target))
                if tgt_rel and tgt_rel != note.rel:
                    self._neighbours[note.rel].add(tgt_rel)
                    self._neighbours[tgt_rel].add(note.rel)

    def _walk_md(self, base: Path):
        for path in base.rglob("*.md"):
            if path.name in IGNORE_FILE_NAMES:
                continue
            if any(part in IGNORE_DIR_NAMES for part in path.relative_to(self.root).parts):
                continue
            yield path

    # --- public API used by health/digest scripts ---
    def knowledge_notes(self):
        return [n for n in self.notes if n.is_knowledge]

    def connections(self, note: Note) -> int:
        return len(self._neighbours.get(note.rel, ()))

    def neighbours(self, note: Note) -> set:
        return self._neighbours.get(note.rel, set())

    def backlink_count_from_knowledge(self, target_rel: str) -> int:
        """How many knowledge notes link TO target_rel (for hub balance)."""
        return sum(1 for n in self.notes
                   if n.is_knowledge and target_rel in self._neighbours.get(n.rel, ()))

    def resolves(self, target: str) -> bool:
        """Does a wiki-link target resolve to any file in the vault?"""
        return _norm(target) in self._resolve_all

    def knowledge_note(self, target: str):
        """Resolve a wiki-link target to its knowledge Note, or None."""
        rel = self._resolve_knowledge.get(_norm(target))
        return self.by_rel.get(rel) if rel else None

    def usage(self) -> dict:
        """Map each knowledge note rel -> set of consumer rel paths that link to it.

        Consumers are every .md file under CONSUMER_FOLDERS (10-MOCs and
        50-Drafts are already parsed; 60-Analysis is walked raw). Self-links
        are ignored, so a MOC's own maturity counts only OTHER artefacts
        drawing on it.
        """
        if not hasattr(self, "_usage"):
            consumer_links = {}  # consumer rel -> set of raw link targets
            for note in self.notes:
                if note.folder in CONSUMER_FOLDERS:
                    consumer_links[note.rel] = note.links_out
            for folder in CONSUMER_FOLDERS:
                base = self.root / folder
                if not base.is_dir():
                    continue
                for path in self._walk_md(base):
                    rel = str(path.relative_to(self.root))
                    if rel in consumer_links:
                        continue
                    text = path.read_text(encoding="utf-8", errors="replace")
                    consumer_links[rel] = {t.strip() for t in WIKILINK_RE.findall(text)
                                           if t.strip()}
            usage = {n.rel: set() for n in self.notes if n.is_knowledge}
            for crel, targets in consumer_links.items():
                for target in targets:
                    tgt_rel = self._resolve_knowledge.get(_norm(target))
                    if tgt_rel and tgt_rel != crel:
                        usage[tgt_rel].add(crel)
            self._usage = usage
        return self._usage


# --- Research Programme page ---------------------------------------------
#
# The programme page replaced the 05-Problems/ layer, which failed because it
# depended on per-note `problems:` metadata nobody maintained. Its successor
# stores nothing per note: the page lists the questions, and everything about
# their liveness is COMPUTED from the files they link to.
#
# Structure contract — the page is written for humans, and this parser depends
# on that shape holding:
#     ## Active Programmes | ## Emeritus     section headings
#     ### N. The question?                   one heading per programme
#     ...body wiki-links...                  its MOCs, hubs and anchor notes
#
# Dormancy is measured by CONTENT, not file churn. The obvious signal — the
# newest mtime among a programme's MOCs and hubs — is forgeable: any bulk edit
# (a retag pass, a frontmatter migration) touches every file and silently resets
# the clock for a year. So dormancy uses the newest `created:` date among the
# knowledge notes hanging off those MOCs and hubs: when did new thinking last
# land in this territory? That date is stable frontmatter, and no mechanical
# pass can fake it. mtime is still reported, as context.
#
# The check asks a question once a year; it never retires anything by itself
# (retirement is displacement, and the user's call).

RESEARCH_PROGRAMME_PAGE = "00-Index/Research Programme.md"
PROGRAMME_DORMANT_DAYS = 365

H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(?:(\d+)\.\s*)?(.+?)\s*$")
# A programme entry the user has reviewed carries a "Reviewed" marker line, e.g.
#     - **Reviewed**: 2026-07-16 — still live (slow-burning)
# This is legitimate stored state: a human decision not derivable from links,
# the same category as #human. The dormancy check reads it so an answered
# question does not re-fire for another year (Phase 3.2, wrinkle b).
REVIEWED_RE = re.compile(r"\*\*Reviewed\*\*\s*:{1,2}\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)


def parse_research_programme(index: VaultIndex, today: date | None = None) -> dict:
    """Parse the Research Programme page into structured entries with computed dormancy.

    Returns {"status": "pending-2.3"|"ok", ...}. Shared by vault_health.py and
    any future tooling that needs the same entries for orientation.
    """
    today = today or date.today()
    path = index.root / RESEARCH_PROGRAMME_PAGE
    if not path.exists():
        return {"status": "pending-2.3", "page": RESEARCH_PROGRAMME_PAGE,
                "note": f"{RESEARCH_PROGRAMME_PAGE} not found; programme check inactive."}

    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text

    entries, section, current = [], None, None
    in_fence = False
    for line in body.split("\n"):
        # A fenced block on this page is documentation (the entry format is shown
        # as an example). Without this, a sample "### 1. ..." inside a fence is
        # parsed as a live programme and fires a spurious dormancy question.
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        h2 = H2_RE.match(line)
        if h2:
            heading = h2.group(1).lower()
            section = ("active" if "active" in heading
                       else "emeritus" if "emeritus" in heading else None)
            current = None
            continue
        h3 = H3_RE.match(line)
        if h3 and section:
            current = {"n": int(h3.group(1)) if h3.group(1) else None,
                       "question": h3.group(2), "section": section,
                       "_links": [], "_reviewed": None}
            entries.append(current)
            continue
        if current is not None:
            current["_links"].extend(t.strip() for t in WIKILINK_RE.findall(line))
            rev = REVIEWED_RE.search(line)
            if rev:
                current["_reviewed"] = rev.group(1)

    active, emeritus = [], []
    for e in entries:
        mocs, hubs, unresolved = [], [], []
        moc_notes, hub_notes, anchor_notes = [], [], []
        newest_mtime = None
        for target in e.pop("_links"):
            note = index.knowledge_note(target)
            if note is None:
                if not index.resolves(target):
                    unresolved.append(target)
                continue
            if note.folder == "10-MOCs":
                mocs.append(note.name)
                moc_notes.append(note)
            elif note.folder == "20-Hubs":
                hubs.append(note.name)
                hub_notes.append(note)
            else:
                anchor_notes.append(note)   # the named exemplar notes
            if note.mtime and (newest_mtime is None or note.mtime > newest_mtime):
                newest_mtime = note.mtime

        # Dormancy territory: a programme's MOCs and named anchor notes, plus
        # everything those draw on. Hubs are the fallback only for a programme with
        # no MOC and no anchors — several hubs ([[AI]], [[Philosophy]]) are broad
        # enough that anything linking them would look permanently alive, which
        # would stop the check ever firing.
        territory = (moc_notes + anchor_notes) or hub_notes
        newest, newest_src = None, None
        for anchor in territory:
            candidates = [anchor] + [index.by_rel[r] for r in index.neighbours(anchor)
                                     if r in index.by_rel]
            for note in candidates:
                if note.created and (newest is None or note.created > newest):
                    newest, newest_src = note.created, note.name

        days = (today - newest).days if newest else None

        # A programme is dormant only when BOTH its newest content and the user's
        # last review are >12 months old. A recent "still live" answer suppresses
        # the question for another year; an entry never reviewed is judged on
        # content alone (Phase 3.2, wrinkle b).
        reviewed = _as_date(e.pop("_reviewed", None))
        days_reviewed = (today - reviewed).days if reviewed else None
        content_stale = (days is None or days > PROGRAMME_DORMANT_DAYS)
        reviewed_stale = (days_reviewed is None or days_reviewed > PROGRAMME_DORMANT_DAYS)
        e.update({
            "mocs": sorted(set(mocs)), "hubs": sorted(set(hubs)),
            "unresolved_links": sorted(set(unresolved)),
            "dormancy_basis": ("mocs+anchors" if (moc_notes or anchor_notes)
                               else "hubs" if hub_notes else "none"),
            "newest_content": newest.isoformat() if newest else None,
            "newest_content_source": newest_src,
            "days_since_new_content": days,
            "newest_mtime": newest_mtime.isoformat() if newest_mtime else None,
            "reviewed": reviewed.isoformat() if reviewed else None,
            "days_since_reviewed": days_reviewed,
            "dormant": bool(e["section"] == "active" and content_stale and reviewed_stale),
        })
        (active if e["section"] == "active" else emeritus).append(e)

    return {
        "status": "ok",
        "page": RESEARCH_PROGRAMME_PAGE,
        "dormant_threshold_days": PROGRAMME_DORMANT_DAYS,
        "active_count": len(active),
        "emeritus_count": len(emeritus),
        "dormant": [e["question"] for e in active if e["dormant"]],
        "active": active,
        "emeritus": emeritus,
    }
