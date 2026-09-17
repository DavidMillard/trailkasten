---
type: index
created: 2026-09-08
tags: [🌲]
---
# 🏡 Trailkasten

A Zettelkasten built to be worked on with an AI assistant. This page is the front door;
everything else is reachable from here.

**New here?** Start with the [[Usage Guide]] — what goes where, and which command to reach
for. Then read [[Values Statement]], because you have inherited a position on AI-assisted
knowledge work and you should know what it is.

## Vault Foundations

- [[Usage Guide]] - What goes where, and how the commands fit together
- [[Values Statement]] - Principles guiding the tools and workflows
- [[Vault Rationale]] - Why the tooling is the way it is, and what you have changed
- [[Research Programme]] - The persistent questions this vault organises around
- [[History]] - The daily chronicle of how the vault grew
- [[Vault Health]] - Structural audit, refreshed by `/vault-health`

## Quick Navigation

### Active MOCs

```dataview
TABLE Key as "Description"
FROM "10-MOCs"
WHERE type = "moc" AND status = "active"
SORT file.name ASC
```

### Concept Hubs

```dataview
TABLE Key as "Description"
FROM "20-Hubs"
WHERE type = "hub"
SORT file.name ASC
```

### Recent Additions

Notes, hubs, MOCs and literature notes added in the last 30 days.

```dataview
TABLE created as Created, Key as "Description"
FROM "10-MOCs" OR "20-Hubs" OR "30-Notes" OR "45-Literature"
WHERE file.ctime >= date(today) - dur(30 days)
SORT created DESC
LIMIT 20
```

### Recently Modified

```dataview
TABLE file.mtime as Modified, Key as "Description"
FROM "10-MOCs" OR "20-Hubs" OR "30-Notes" OR "45-Literature"
WHERE file.mtime >= date(today) - dur(30 days)
SORT file.mtime DESC
LIMIT 20
```

---
## Vault Statistics

```dataviewjs
const activeMocs = dv.pages('"10-MOCs"').where(p => p.type === "moc" && p.status === "active").length;
const hubs = dv.pages('"20-Hubs"').where(p => p.type === "hub").length;
const notes = dv.pages('"30-Notes"').where(p => p.type === "note").length;
const literature = dv.pages('"45-Literature"').where(p => p.type === "literature-note").length;
const has = (p, e) => p.tags && p.tags.includes(e);
const k = dv.pages('"30-Notes" or "20-Hubs" or "10-MOCs" or "45-Literature"');
dv.list([
  `**Atomic notes**: ${notes}`,
  `**Concept hubs**: ${hubs}`,
  `**Active MOCs**: ${activeMocs}`,
  `**Literature notes**: ${literature}`,
  `**🌱 Untested**: ${k.where(p => has(p, "🌱")).length} (never drawn on by a MOC, draft or analysis)`,
  `**🌿 Drawn on**: ${k.where(p => has(p, "🌿")).length} (used by 1–2 artefacts)`,
  `**🌲 Load-bearing**: ${k.where(p => has(p, "🌲")).length} (used by 3+ artefacts)`
]);
```

*Statistics update automatically via Dataview. Maturity is computed from use by
`.claude/scripts/vault_maturity.py` — never set it by hand.*
