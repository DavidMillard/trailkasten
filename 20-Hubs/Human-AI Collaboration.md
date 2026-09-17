---
type: hub
created: 2026-09-09
tags: [🌿]
used-by: 1
topics: []
---
# 🗂️ Human-AI Collaboration

> [!tldr] TLDR
> **Key**:: How work is divided between a person and an assistant, and what that division does to the person

A domain concerned with the division of labour in AI-assisted work: which parts of a practice can be delegated, which cannot, and what the delegation does to the delegator over time.

The notes gathered here approach that from a particular angle — the construction of knowledge structures rather than the generation of prose — and they tend to converge on a distinction between the clerical layer of a practice and its judgements. That is one framing among several. Accounts grounded in automation research, in distributed cognition, or in labour studies would carve the territory differently, and a hub is a place to collect those rather than to adjudicate between them.

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
