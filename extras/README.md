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
> names. These commands are written and tested against **`54yyyu/zotero-mcp`**
> version **0.15.1**, published to PyPI as **`zotero-mcp-server`**
> (`uv tool install zotero-mcp-server==0.15.1`). They call tools such as
> `zotero_get_item_metadata`, `zotero_search_by_tag` and
> `zotero_set_item_collections`, which the smaller, read-only
> **`kujenga/zotero-mcp`** — the package the bare name `zotero-mcp` resolves
> to — does not provide. Install the wrong one and the commands fail on their
> first call with an unknown tool. The server renames tools between releases,
> so upgrade deliberately.
>
> No semantic-search index is needed: the commands search by tag and keyword.
> `/create-literature-note` resolves citation keys through **Better BibTeX**,
> so Zotero desktop should be running with BBT installed. `/evaluate-papers`
> can take its queue from a Zotero collection, `Workflow/To Evaluate`, and
> files evaluated papers into dated `Workflow/Evaluated/…` collections —
> workflow state lives in collections you can see in Zotero, never in tags.
