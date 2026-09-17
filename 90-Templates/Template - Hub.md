---
type: hub
created: {{date}}
tags: [🌱]  # maturity is computed from use — script-owned, never hand-set
used-by: 0
topics:
  - "[[Related Hub]]"
---
# 🗂️ {{title}}

> [!tldr] TLDR
> **Key**:: Brief one-line description of this concept or domain

Brief description of this concept or domain area. Frame hubs as domains of inquiry that organize multiple perspectives, rather than establishing definitive truth about the domain. Hubs collect ideas and frameworks, they don't declare orthodoxy.

---
## Notes in this Hub

```dataview
TABLE Key as "Description"
FROM "30-Notes"
WHERE contains(topics, this.file.link)
SORT file.name ASC
```

---
## Related MOCs
```dataview
LIST "(" + status + ") : " + Key
FROM "10-MOCs"
WHERE contains(file.outlinks, this.file.link) AND type = "moc"
SORT file.name ASC
```