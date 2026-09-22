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

Requires a Zotero library and a Zotero MCP server. Without those, every
command in this tier fails on its first call — which is why they are not
installed by default.

> **Which Zotero MCP server?** Two are in circulation under confusingly close
> names. These commands are written against **`54yyyu/zotero-mcp`**, published
> to PyPI as **`zotero-mcp-server`** (`uv tool install zotero-mcp-server`).
> They call `zotero_get_item_metadata` and `zotero_semantic_search`, which the
> smaller, read-only **`kujenga/zotero-mcp`** — the package the bare name
> `zotero-mcp` resolves to — does not provide. Install the wrong one and
> `/create-literature-note` fails on its first call with an unknown tool.
> These commands are under revision to pin the server explicitly.
