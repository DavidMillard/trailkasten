# extras

Optional tiers. Nothing in here is active: Claude Code only loads commands from
`.claude/commands/` and skills from `.claude/skills/`, so these files sit inert
until you install them.

Run `/setup` to install a tier, or copy the files across by hand.

## academic/

Zotero-backed commands for working with the research literature: creating
literature notes from citation keys, finding papers relevant to a vault
concept, matching citations to placeholders in a draft, and triaging incoming
papers for whether they earn a note.

Requires a Zotero library and the `zotero-mcp` server. Without those, every
command in this tier fails on its first call — which is why they are not
installed by default.
