---
description: First-run configuration — environment check, identity, tiers, and bootstrap
argument-hint: "[--recheck]"
skills: user-interaction-patterns, vault-writing-style
---

# Setup

The first thing a new user runs. It configures the vault for *this* person and *this*
machine, and it is the first demonstration of how everything else here behaves: it checks,
it reports, it proposes, and it asks before it writes.

**Never write anything in this command without showing it first and getting a yes.** The
Values Statement shipping alongside claims that the intention/action boundary is
inviolable; this is where a new user finds out whether that is true.

With `--recheck`, run Step 1 only and report. Useful after installing something.

---

Load `user-interaction-patterns` for the approval flows below, and `vault-writing-style`
for anything written into the vault during setup.

## Step 1: Environment check

**MCP tools cannot detect MCP servers that are not configured yet**, so this check works at
the filesystem and port level. Run these and report what you find. Do not fail, do not
block, do not ask for permission first — this is read-only inspection.

```bash
# Obsidian MCP — served by the Semantic Notes Vault MCP plugin from inside Obsidian
curl -s -o /dev/null -w "%{http_code}" --max-time 2 http://localhost:3001/mcp || echo "unreachable"

# Which community plugins are enabled
cat .obsidian/community-plugins.json 2>/dev/null || echo "no plugin config — is this open in Obsidian?"

# Has Smart Connections built its index? The MCP server will not start without this.
test -d .smart-env && echo "indexed" || echo "no .smart-env — Smart Connections has not indexed"

# Zotero MCP, for the academic tier
command -v zotero-mcp >/dev/null && echo "zotero-mcp found" || echo "zotero-mcp not installed"

# Existing config
test -f .mcp.json && echo ".mcp.json exists" || echo "no .mcp.json yet"
```

Report as a short table: what is present, what is missing, and what each missing thing
costs. Be concrete about consequences rather than listing absences.

| Missing | Consequence |
|---|---|
| Dataview | Hubs, MOCs and index pages render blank — this one genuinely breaks things |
| Semantic Notes Vault MCP | No `mcp__obsidian__*` tools; searching falls back to Grep and Read |
| Smart Connections | No semantic search; related notes sharing no vocabulary get missed |
| `.smart-env/` | The Smart Connections MCP server will refuse to start |
| Supercharged Links | `#human`-tagged content is not visually distinct |
| zotero-mcp | Academic tier unavailable |

If Dataview or the Obsidian MCP plugin are missing, say so plainly and point at the README's
install section. **Then carry on anyway** — a partially configured vault still works, and
stopping here would strand someone who just wants to look around.

---

## Step 2: Who are you, and what is this vault for?

Ask, in one message, conversationally:

1. **Who you are** — name, and roughly what you work on
2. **What this vault is for** — the research programme, the book, the teaching, the beat
3. **Anything the assistant should know about how you like to work**

Wait for the answer. If the user would rather skip, skip — everything below is optional and
the vault functions without it.

### Then propose a CLAUDE.md edit — do not make it

Draft a replacement for the **What This Is** section of `CLAUDE.md`, personalised from the
answers. **Show the diff and ask.** Something like:

```
Here is what I would change in CLAUDE.md. Shall I apply it?

  ## What This Is
- **Trailkasten** is a Zettelkasten built to be worked on with an AI assistant...
+ This vault belongs to <name>, <what they do>. It is a Zettelkasten for
+ <what it is for>, built to be worked on with an AI assistant...
```

Keep the rest of the file intact. Only the opening framing is personal; everything else is
method and applies to anyone.

### Seed memory

Offer to write two or three memory files capturing what was learned — who the user is, what
the vault is for, and any working preference they mentioned. Show the content before
writing. Explain in one line what memory is for, since most people will not know: notes to
the assistant that persist across sessions, kept as plain files the user can read and edit.

---

## Step 2.5: The inherited remote

A cloned vault carries the original repository's `origin`. Check it:

```bash
git remote get-url origin 2>/dev/null || echo "no remote"
```

If there is no remote, or it is clearly the user's own, say nothing and move on — someone
who used the template button or detached the history already has this right.

If it still points at the repository this vault was cloned from, say what that means and
offer to remove it:

> This vault still points at the repository it was cloned from, which means any push would
> send your notes there rather than somewhere of your own. Shall I remove that remote? Your
> history stays; you can add your own remote whenever you want one.

```bash
git remote remove origin
```

Removing it is the right default — it fails safe. If the user would rather keep the link to
pull future updates, leave it and say plainly that they should never push to it.

## Step 3: Which tiers?

Explain what is available and what it needs:

- **Core** — already installed. Nothing further required.
- **Academic** — `/create-literature-note`, `/find-papers`, `/find-citations`,
  `/evaluate-papers`. Needs a Zotero library and `zotero-mcp`. If Step 1 found no
  `zotero-mcp`, say so and offer to install the tier anyway for later.

If the academic tier is wanted:

```bash
cp extras/academic/commands/*.md .claude/commands/
cp -R extras/academic/skills/* .claude/skills/
rm -f .claude/commands/README.md .claude/skills/README.md
```

Then update the **Command Tiers** section of `CLAUDE.md` so the academic commands are listed
as installed rather than as inert. Show that edit too.

---

## Step 4: Write `.mcp.json`

Build the config **from what Step 1 actually found** — never from the full template. A
config that names a server the user does not have produces a startup error on every session
and no explanation.

Show the complete file and ask before writing.

```jsonc
{
  "mcpServers": {
    // Include only if the plugin responded on its port
    "obsidian": {
      "type": "http",
      "url": "http://localhost:3001/mcp"
    },
    // Include only if the user has cloned smart-connections-mcp AND .smart-env exists.
    // Ask for the path; do not guess it.
    "smart-connections": {
      "command": "node",
      "args": ["<absolute path>/dist/index.js"],
      "env": { "SMART_VAULT_PATH": "<absolute path to this vault>" }
    },
    // Academic tier only. Ask for the library ID and API key, and say plainly that
    // .mcp.json is gitignored so the key stays local.
    "zotero": {
      "command": "<path to zotero-mcp>",
      "args": [],
      "env": {
        "ZOTERO_LIBRARY_ID": "<id>",
        "ZOTERO_API_KEY": "<key>",
        "ZOTERO_LIBRARY_TYPE": "user",
        "ZOTERO_EMBEDDING_MODEL": "default"
      }
    }
  }
}
```

**Never invent a path.** If a path is needed and unknown, ask for it.

---

## Step 5: The bootstrap

This is the step that decides whether the vault ever becomes useful, so give it room.

Explain the position honestly: the vault is nearly empty, and almost everything interesting
here — connection proposals, duplicate detection, sibling nudges — is a function of having
material. Below roughly fifty notes it will feel thinner than it is.

Then make the offer:

> The fastest way to a vault that thinks the way you do is to fill it with what you have
> already written. If you have two or three years of blog posts, papers, talks or reports,
> drop them in `80-Fleeting/` — that is the inbox — and I will run `/ingest-resource` over
> them, which writes a tidied resource note for each into `40-Resources/` and proposes
> atomic notes from it.
>
> If you have not written much, key papers and authors in your area work too — the vault
> will just start out sounding like the field rather than like you.

If the user has material ready, offer to start on one now. One is enough to show the shape
of it; do not process a backlog in the setup session.

---

## Step 6: The examples

Ask whether to keep or clear the shipped example content:

- **Keep** — seven notes, a hub, a MOC and a history entry demonstrating the method. Useful
  reference while learning; harmless to leave.
- **Archive** — move to `99-Archive/`. Out of the way, still readable, excluded from
  maturity counts.
- **Delete** — remove entirely.

Recommend **keep for now, archive once you have fifty notes of your own**. There is no
hurry, and a worked example is worth more than it costs.

If archiving or deleting, run `python3 .claude/scripts/vault_maturity.py --write` afterwards
so the maturity cache reflects the change.

---

## Step 7: Finish

Two things, in this order.

**First, the restart.** Claude Code reads `.mcp.json` at startup, so nothing written in
Step 4 is live yet. Say so explicitly:

> I have written `.mcp.json`, but Claude Code only reads it at startup — restart for the
> MCP servers to connect. Run `/setup --recheck` afterwards and I will confirm they came up.

**Then a short summary**: what was configured, what is still missing and what that costs,
and one suggested next action. Point at [[Usage Guide]] for the method and [[Values
Statement]] for the position they have just inherited.

Keep it to a few lines. They have answered enough questions.
