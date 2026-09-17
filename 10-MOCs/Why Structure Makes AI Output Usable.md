---
type: moc
created: 2026-09-09
status: active
tags: [🌱]
used-by: 0
topics:
  - "[[Human-AI Collaboration]]"
---
# 🗺️ -  Why Structure Makes AI Output Usable

> [!tldr] TLDR
> **Key**:: An argument that the reviewability of AI output is a property of structure rather than of prose quality

## Current Status
```dataviewjs
const status = dv.current().status || "Not set";
const createdRaw = dv.current().created;
const created = createdRaw && typeof createdRaw.toFormat === 'function' ? createdRaw.toFormat("dd-MM-yyyy") : (createdRaw || "Not set");
const modified = dv.current().file.mtime.toFormat("dd-MM-yyyy") || "Not set";

dv.list([
  `**Status**: ${status}`,
  `**Started**: ${created}`,
  `**Last Updated**: ${modified}`
]);
```

## Current Focus

An example MOC, shipped with this vault to demonstrate what a Map of Content is and how one
is assembled. Replace it with your own once you have material to work with.

---
## Narrative Overview

The complaint about AI writing is usually made about its quality: it is bland, it hedges, it
produces competent prose with nothing at stake. This trail argues that quality is the wrong
place to look, and that the more consequential problem is one of *granularity*.

The starting point is a distinction drawn from practice rather than from theory.
[[Tedious Friction and Cognitive Friction]] separates two kinds of effort that a knowledge
practice demands: the clerical layer of writing descriptions and maintaining links, and the
judgements about whether a concept is real and whether it belongs. These are routinely
conflated because both feel like work. The distinction matters because attempts at keeping a
Zettelkasten by hand appear to fail on the first while the second remains attractive — which
suggests that the design question for an assistant is not how much work to remove, but where
to cut.

Cutting in the right place leaves the judgements intact, and this is where structure enters.
[[Structural Scaffolds Make AI Output Correctable]] argues that ungrounded AI prose can only
be accepted or rejected wholesale, because nothing in it is individually addressable — and
that people mostly accept, since reading critically enough to reject part of a passage costs
more than writing it would have. A three-layer scaffold changes the granularity: each
generated unit has a declared role and a position, so one link can be disputed and one note
rejected while others are kept. On this account reviewability is a property of the
surrounding structure, not of the text.

Granularity makes selection possible but does not say when to stop.
[[The Human as Exit Condition]] supplies that: a generative knowledge system has no internal
terminus, because each note implies connections to notes that do not yet exist, recursively.
The stopping point is not a property of the material but of what the person currently cares
about — which makes human selection load-bearing rather than merely reassuring. Remove it and
the structure does not become autonomous; it becomes unbounded.

The trail closes on the experiential claim that makes the rest sustainable.
[[Hypertextual Friction as Intrinsic Reward]] reports that the selection work, once the
clerical layer has been removed, is not experienced as a tax at all but as the most engaging
part of the practice — because the curatorial decisions are the intellectual work rather than
an obstacle in front of it. If that generalises, it undercuts the usual cost-benefit framing
of beneficial friction, in which effort now is justified by payoff later.

Taken together the four notes make a single argument: structure is what converts AI output
from something you must accept or discard into something you can think with.

### Notes in This Narrative

- [[Tedious Friction and Cognitive Friction]] - Establishes which effort is worth keeping, and so where automation should cut
- [[Structural Scaffolds Make AI Output Correctable]] - The granularity argument, and the trail's central claim
- [[The Human as Exit Condition]] - Why selection cannot be delegated even once structure is in place
- [[Hypertextual Friction as Intrinsic Reward]] - Why the remaining work is sustainable rather than merely necessary

---
## Suggestions for Expanding This MOC

**Specific Note Topics:**
- **Reviewability and fluency** - Whether better prose makes wholesale acceptance more likely, which would strengthen the granularity argument
- **Failure modes of scaffolds** - What happens when the structure itself is wrong for the material

**Thematic Areas to Explore:**
- **Comparison with code review** - Diffs solved the granularity problem for software decades ago; the parallel is close and largely unexamined here
- **The limits of the argument** - the vault's note on the builder's advantage suggests structure alone may not transfer, which this trail does not address. Linking it here would be premature: the trail does not yet engage with it.
