---
type: resource
resource-type: conversation
created: 2026-09-09
source: Reconstructed interview between David Millard and Claude
tags: [🌱]
---
# Conversation - Why Build a Zettelkasten With an AI

> [!tldr] TLDR
> **Key**:: An interview with the vault's original author about why the system was built, what surprised him, and what he thinks it costs

> [!warning] Provenance
> This is a **reconstructed** conversation, not a transcript. It was assembled from the
> arguments in *Permanently Under Construction* (ACM Hypertext 2026) and edited for the
> released vault. The positions are the author's; the specific wording is not a verbatim
> record of anything said aloud. It ships as example material for `/ingest-resource` — try
> running the command on it and see what it proposes.

---

##  Comprehensive Summary

A conversation about the design and experience of an AI-augmented Zettelkasten, covering:
why earlier attempts at a Zettelkasten failed on clerical labour rather than on the idea;
why the friction that remains turned out to be enjoyable rather than costly; what is remembered and what
is forgotten, and why curation turns out to be a form of learning; what the daily history
entries are actually for, including the use they were not designed for; why a system built
by its own user may not transfer, and why that might be the point rather than the flaw; the
suggest-only interaction pattern and the problem it solves; and the honest costs —
tool-building as displacement activity, and the awkward seam between a knowledge network and
a finished paper.

---

## Key Concepts

- Tedious friction versus cognitive friction — clerical labour is not intellectual difficulty
- Hypertextual friction as intrinsically rewarding rather than a tax paid for later benefit
- Provenance fades while content is retained — curation as a mode of learning
- History entries as emergent maps of content, and as the route back into ingested material
- The builder's advantage, and its existentialist reading
- Suggest-only workflows and the human as exit condition
- Structural scaffolds making AI output legible and correctable
- The persistent artefact versus the ephemeral chat

---

## Full Content

**Claude:** Before we get to the system itself — what's your history with this way of
working?

**DM:** Long, and a story of mixed success. I've used hypertext tools for essentially my whole
professional life, but many of them didn't stick. The one that did is the personal wiki.
I've been keeping one for years, most recently in Obsidian, so my Obsidian use predates this system by a long way.

**Claude:** And Zettelkasten specifically?

**DM:** I'd tried to build one before. The idea always seemed obviously valuable to me —
genuinely interesting, with real value in it. The problem was that I couldn't sustain it.

**Claude:** What went wrong?

**DM:** The mechanics. Identifying the concepts and then linking them together — that's
where it fell down every time. Writing out the descriptions, going through the process of
connecting everything up, doing the reverse links, the whole curatorial stage. That's the
part that felt like *rote work*, and it was quite painful. It wasn't that I didn't want
the result. I couldn't face the labour of getting there.

**Claude:** So what changed?

**DM:** I started playing around with AI systems, and with frameworks like Claude Code in
particular, and the natural thing for me to do was point it at Markdown instead of at code.
Once you've done that the question asks itself — could I automate some of these processes?
That was the seed of the whole activity. It wasn't "let me build an AI knowledge system." It
was that the tedious part of a practice I already believed in had suddenly become tractable.

**Claude:** The tedious part isn't the same as the difficult part, though.

**DM:** No, and that distinction turns out to be the entire design. The judgement — is this
a real concept, does it belong here, is it distinct from what I've already got — that was
never what stopped me. That's the interesting bit. What I wanted rid of was the clerical
work around it: the typing up, the link maintenance, the housekeeping. They're completely
different kinds of effort, and most of what this system does is separate them, so the
machine takes one and I keep the other.

**Claude:** There are plenty of AI note-taking tools now, though. Why not just use one of
those?

**DM:** Because the good note-taking tools and the good AI assistants don't meet. That's the
whole thing, really. If I upload a stack of papers to a chat interface and ask it to reason
across them, I get something genuinely useful — a coherent narrative, an entry point into
material I don't know well. But when the
conversation ends, that synthesis is gone. The connections it found aren't anywhere I can
navigate. I can't annotate them, I can't build on them, I can't stumble across them again in
six months when they suddenly matter.

**Claude:** So the complaint is about persistence.

**DM:** It's about persistence, but it's more specific than that. It's that the AI mediates
all access. Everything has to go through it. Whereas if the output of that reasoning is a
hypertext — actual files, actual links — then I can just open Obsidian and wander. And I do,
constantly. I ask the assistant questions about the vault far less often than I just browse
it. The AI is the co-constructor. The hypertext is the thing that lasts.

**Claude:** Let's talk about the experience of using it. The paper makes a claim about
friction that I think surprises people.

**DM:** It surprised me. The friction literature mostly treats friction as a cost — you
endure a slower process now, you get better learning or safer decisions later. It's a trade.
And I went in expecting that: I assumed the review steps, the approving and rejecting of
proposed notes, would be a tax I paid for a tidier vault.

**Claude:** And it wasn't?

**DM:** It's the best part. Genuinely. When the system proposes eight notes from a paper,
going through them is the most engaging thing I do all day. Sometimes there's a moment of
rediscovery — you see how an idea you already had connects to what you're working on now, in
a way you'd never articulated. Sometimes there's an actual frisson, where it's surfaced
something you didn't know. And even when a proposal is obviously fine and you just approve
it, the pause isn't wasted. You're involved. You own the thing that results.

**Claude:** Why does that matter, if the outcome is the same?

**DM:** Because I think the curatorial decisions *are* the intellectual work. They're not
obstacles in front of the real work. Deciding whether this concept deserves to exist as a
separate idea, whether it's actually distinct from something I've already got, whether the
framing is right — that's thinking. It just doesn't look like thinking, because it's small
and it's repeated. Sennett has this line about craft knowledge living in the small repeated
judgements rather than the grand gestures. That's what this feels like.

**Claude:** There's a limitation you're honest about in the paper — that the decisions
themselves fade.

**DM:** The *provenance* fades. That's the honest version. For a note made back in March I
couldn't tell you now whether that was something the system proposed or something I asked
for. That distinction has genuinely gone. There's research on it — the AI Memory Gap —
which says roughly that when AI output is context-specific and immediately editable and
slides straight into your working environment, the cues you'd normally use to tell your own
thoughts from someone else's stop working.

**Claude:** You're drawing a distinction there, though.

**DM:** I am, because the *contents* haven't gone anywhere. I remember what's in the vault
remarkably well, considering how big it is. I'll be mid-session and stop and say, hang on,
that connects to something over here — or, isn't that just a restatement of a note we
already have? I do that constantly, and I'm usually right.

**Claude:** Which is a claim about learning rather than about storage.

**DM:** That's exactly it. I expected a filing system and I got something closer to a study
aid. Curating the thing is how I learn it, and then using it reinforces what I learned. What
I've lost is who suggested what. What I've kept is the actual knowledge, which is the part I
wanted.

**Claude:** So what are the history entries for?

**DM:** Two things, and the second is the one I didn't anticipate. The first is that they're
a hedge against exactly that forgetting — a persistent record of what was added and how it
connected, sitting there long after the experience of adding it has gone.

**Claude:** And the second?

**DM:** They're the way back in. If I've ingested something substantial — a conference's
worth of papers, a long transcript — I end up with a dozen notes that are related because
they arrived together, and the history entry is the thing that holds them together. It
clusters them thematically and narrates how they relate. It's effectively a small map of
content that got written for free, as a side effect of the ingestion.

**Claude:** Which changes how you use them.

**DM:** It's become a habit. Ingest the material, generate the history entry, then actually
go and read the entry — not as a record, but as the route into the notes. It's the fastest
way back into a body of material I brought in three weeks ago and have half forgotten. I'd
say it's the most underrated part of the system, and it's the part I built with the least
intention.

**Claude:** Let's talk about the interaction pattern. Everything here proposes rather than
acts.

**DM:** Suggest-only, yes. Partly that's a values position — I don't want the system making
decisions on my behalf, and there's a whole document in the vault arguing about where that
boundary sits. But there's also a structural reason that I think is less obvious and more
interesting.

**Claude:** Go on.

**DM:** Without human selection, the thing would generate forever. Every new note suggests
connections to notes that don't exist yet. Those could be created, and they'd suggest more.
It's recursive, and there's no natural stopping point inside the system. The human is the
exit condition. I'm the one who says: this is the boundary of what I currently care about,
further expansion is diminishing returns. Nothing in the machine can tell you that.

**Claude:** You've said elsewhere that the structure is what makes the AI output usable at
all.

**DM:** That's the bit I'd most want people to take away, actually. Without a scaffold, AI
writing arrives as undifferentiated prose. You accept it or you reject it, wholesale, and
mostly you accept it because reading it critically is more effort than writing it yourself
would have been. With a scaffold — atomic notes, hubs, maps of content — every generated
thing has a declared role and a position. You can argue with one link. You can reject one
note and keep seven. The scaffold doesn't limit what the AI can say. It shapes how what it
says enters your thinking, and that turns out to matter enormously.

**Claude:** Here's the awkward question. The system works well for you. Does it work for
anyone else?

**DM:** What I can tell you is that I find it transformatively useful. It has completely
changed how I engage with the literature, how I think about concepts, how I go about
learning a new area. That much I'm certain of.

**Claude:** And for other people?

**DM:** When I show it to colleagues they're interested, but it doesn't click for them the
way it does for me. And I think I know why. The core idea is transferable — absolutely it
is. But the moment you start actually using it, you stop having the core idea and start
having a bespoke system. It fits how you think, how you structure the world, how you talk
about the world.

**Claude:** Can you make that concrete?

**DM:** A lot of what's in my vault didn't come from papers I ingested at all. They're my
ideas — my own descriptions of things, that I've had the assistant write up properly. And
those become lynchpins. Lodestones, really: fixed points that I build the rest of the
knowledge around. When I show the vault to somebody else those notes don't mean anything to
them. They're just notes. To me they're load-bearing in the literal sense.

**Claude:** And the MOC workflow suits you specifically.

**DM:** It's just what I've always done when writing a paper — browse for ideas, assemble an
outline, annotate the relationships, then write. The vault scaffolds that rather than
replacing it. Which is exactly why it feels natural to me, and exactly why that naturalness
might not travel.

**Claude:** That still reads as a limitation.

**DM:** It reads as one, and I resisted it for a while, and then I came round to thinking
it's the finding rather than the confound. There's an argument that what unites hypertext
across all its forms isn't a technology, it's an ideology — a requirement for
non-regularity, rooted in post-structuralism, carrying existentialist values. Existence
precedes essence: meaning isn't given to you, you construct it through choices. That maps
almost exactly onto building a knowledge system. The value isn't in the architecture. The
architecture is trivially copyable — I'm literally about to publish it. The value is in
having built it.

**Claude:** Which is a slightly uncomfortable thing to say while releasing it publicly.

**DM:** It is. Though I don't think the conclusion is "everyone must start from nothing."
It's that a system has to leave genuine room for you to shape it — real consequential
decisions about structure and vocabulary and organisation, not a preferences panel. If
someone takes this and changes half the commands, that's the thing working. If they use it
exactly as shipped and it feels flat, that's the thing working too, in a sense. It's telling
them something.

**Claude:** What does it cost? You're candid in the paper about one thing in particular.

**DM:** Building the tool is more fun than using it. That's the danger. There's a
well-documented pattern of people who optimise their workflow until the optimising has
eaten the work, and I recognise myself in it. There have absolutely been afternoons where I
tuned a command instead of writing the paper the command exists to support.

**Claude:** Do you think that's straightforwardly bad?

**DM:** I go back and forth. The defence is that I'm not a machine — I get legitimate
professional value out of enjoying something, out of learning, out of poking at it. And if
building the tool is itself a way of thinking about the problems the tool addresses, then
the line between building and researching is blurrier than the productivity framing wants
it to be. But I'd be lying if I said it was always that. Sometimes it's just procrastination
with better branding.

**Claude:** Anything else you'd flag to someone picking this up?

**DM:** Two things. One, it's still not great at the last mile. It's excellent at pulling material
apart, finding connections, helping you assemble an argument. Turning that into a paper with
real citations rather than wiki-links is still clumsy, and I do a chunk of it by hand.

**Claude:** And the second?

**DM:** That this is absolutely not an automation system. I'd want that in bold. It requires
you to use it and to spend time with it, and if you won't do that you won't get anything out
of it — you'll get a large tidy structure that you didn't really oversee and don't actually
understand.

**Claude:** That sounds like a warning.

**DM:** It's meant as one. But I'd immediately add the other half, which is that the effort
*is* the enjoyable part. Keeping up with the literature used to be a slog. It genuinely
isn't any more — it's something I look forward to and benefit from enormously. It's work
that doesn't feel like work.

**Claude:** And you get that from the start, or do you have to wait for it?

**DM:** You get value from the beginning, which I think surprises people who expect a long
barren stretch. It's that the value *compounds* — the thing gets more useful the bigger and
denser it grows, and something you wrote eight months ago turning out to bear on what you're
doing today is a pleasure you can't have on day three. But go in understanding that none of
it comes for free.

---

## Processing Notes

Reconstructed for the released vault as example source material. Assembled from the
Discussion and Hypertextual Friction sections of the ACM Hypertext 2026 paper.

Deliberately dense in extractable concepts: it should yield five or six atomic notes with
clear boundaries, plus at least one idea (the builder's advantage) that argues against the
vault's own release. That tension is useful — a good ingestion should surface it rather than
smooth it over.

## References

- Millard, D. E. (2026). *Permanently Under Construction: Hypertextual Friction in an
  AI-Augmented Zettelkasten.* Proceedings of the 37th ACM Conference on Hypertext,
  pp. 383–393. https://doi.org/10.1145/3800935.3830837
