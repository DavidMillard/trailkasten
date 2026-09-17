# Trailkasten

A Zettelkasten built to be worked on with an AI assistant.

Trailkasten is an [Obsidian](https://obsidian.md) vault plus a vocabulary of commands and
skills for [Claude Code](https://claude.com/claude-code). Clone it, open Claude Code in the
directory, run `/setup`, and start feeding it things you have read.

The name welds Vannevar Bush's *trails* to Niklas Luhmann's *Zettelkasten* — a slip box you
navigate by the paths you build through it.

---

## Why this exists

Most AI writing tools generate prose. This one builds structure, and the structure is the
point.

Notes are atomic: one idea each, 200–400 words, connected by explicit links. Hubs gather
notes around persistent concepts. Maps of Content sequence them into arguments. That
three-layer grammar gives AI operations something to work *within*, which makes what the
assistant produces legible, correctable and navigable in a way free-form generation is not.
Revisions happen note by note rather than wholesale, and the links make the scope of any
change visible.

### Learn the vocabulary, not the commands

A list of slash commands makes this look like a tool you operate. It is not, and learning
the list is not the skill.

**The skill is the vocabulary: atomic notes, hubs, Maps of Content.** Those three words are
what make the conversation work. *"That feels like it wants to be its own atomic note"* is
precise enough to act on. So is *"is this a hub, or have I actually got a MOC here?"*, or
*"which notes would a MOC on this draw on, and where would it be thin?"* You are not issuing
instructions — you are thinking out loud in a shared language, and the structure is that
language as much as it is a filing system.

Most of the useful work never touches a command. Asking what a new idea connects to, whether
the vault already says this somewhere, what a cluster is actually claiming, where an argument
has a hole in it — none of that is on the command list, and it is where the vault earns its
keep. The commands exist because a few moves recur often enough to be worth doing
consistently, and Claude runs them from ordinary conversation anyway: *"I'd like a note
about X"* is the same thing as `/create-note`.

So a Zettelkasten is a space for thinking in rather than a pipeline for producing notes. The
three layers are what let you say precisely where in that space you are.

The system is described in:

> Millard, D. E. (2026). *Permanently Under Construction: Hypertextual Friction in an
> AI-Augmented Zettelkasten.* In Proceedings of the 37th ACM Conference on Hypertext
> (HT '26), pp. 383–393. ACM. https://doi.org/10.1145/3800935.3830837
> *(open access, CC BY 4.0)*

This repository is the structure from that paper, stripped of one researcher's notes.

---

## What you get

**Thirteen folders**, each with a README explaining what it holds.

**Seven core commands** — `/setup`, `/create-note`, `/create-hub`, `/ingest-resource`,
`/create-moc`, `/create-draft`, `/vault-health`.

**Eight skills** encoding the method: writing style, Zettelkasten conventions, note
creation and linking, interaction patterns, draft structure, efficient vault search, the
history chronicle, and large-document preprocessing.

**Two Python scripts** that count deterministically so the model only has to interpret:
`vault_health.py` audits structure, `vault_maturity.py` maintains the maturity cache.

**An optional academic tier** in `extras/`, for people working with a Zotero library.

**A handful of example notes**, so the machinery has something to act on. Replace them.

---

## Requirements

| | |
|---|---|
| **Obsidian** | The vault itself |
| **Claude Code** | The assistant |
| **Dataview** (plugin, required) | Hubs, MOCs and index pages are built on Dataview queries; without it the navigation layer is blank |
| **Semantic Notes Vault MCP** (plugin, required) | Serves the `obsidian` MCP server from inside Obsidian — how Claude searches and edits the vault |
| **Smart Connections** (plugin, recommended) | Semantic search: finds related notes that share no vocabulary |
| **Supercharged Links** (plugin, recommended) | Makes `#human`-tagged content visually distinct |

Nothing third-party is bundled here. Install the plugins through Obsidian's community
browser; `/setup` will tell you which are missing.

## Install

**Order matters** — step 3 fails if you skip step 2.

1. **Get your own copy** — one of two ways, and neither leaves you connected to this
   repository.

   **With a GitHub account**, press **Use this template** at the top of this page. You get a
   repository of your own, with no fork relationship and `origin` already pointing at it, so
   you can push from the first day.

   **Without one**, take the files and start a fresh history:
   ```bash
   git clone --depth 1 https://github.com/DavidMillard/trailkasten.git my-vault
   cd my-vault
   rm -rf .git && git init
   ```
   The `rm -rf .git` matters. A plain clone leaves `origin` pointing here and the commit log
   full of this project's development — neither of which belongs in your vault. Starting a
   fresh history means the log records *your* thinking from its first entry.

   Then open the folder as a vault in Obsidian.
2. **Install the plugins** above and enable them. **Let Smart Connections finish its first
   index** — it creates `.smart-env/`, and the MCP server below will not start without it.
3. **Install the Smart Connections MCP server** (optional, but do it before `/setup` if you
   want semantic search):
   ```bash
   git clone https://github.com/msdanyg/smart-connections-mcp
   cd smart-connections-mcp && npm install
   ```
   That is the whole install: the project ships its compiled output, so there is
   nothing to build.
4. **Open Claude Code** in the vault directory and run `/setup`. It checks what is present,
   writes your `.mcp.json`, asks who you are and what the vault is for, and offers to
   install the academic tier.
5. **Restart Claude Code** so it picks up the new MCP configuration.

If you cloned without detaching the history, your copy still points at this repository and
pushing would send your notes here. `/setup` detects that and offers to remove the remote —
let it.

### The MCP configuration

`/setup` writes `.mcp.json` for you, and it is gitignored because it holds absolute paths
and — if you install the academic tier — an API key. For reference, or if you need to
hand-edit later:

```jsonc
{
  "mcpServers": {
    "obsidian": {
      "type": "http",
      "url": "http://localhost:3001/mcp"
      // Served by the Semantic Notes Vault MCP plugin. Obsidian must be running
      // with this vault open. Check the port in the plugin's settings.
    },
    "smart-connections": {
      "command": "node",
      "args": ["/path/to/smart-connections-mcp/dist/index.js"],
      "env": { "SMART_VAULT_PATH": "/path/to/this/vault" }
      // Reads <vault>/.smart-env/ — will not start until Smart Connections has indexed.
    }
  }
}
```

---

## Your first fortnight

**Do not start by writing notes by hand.** An empty Zettelkasten has nothing to connect to,
and the system's interesting behaviour — connection proposals, duplicate detection,
semantic linking — is a function of having material. Below about fifty notes, links will
feel thin and the assistant will seem less useful than it is.

**Start by ingesting your own back catalogue.** If you have published anything — blog
posts, papers, talks, long emails you were proud of — drop two or three years of it into
`80-Fleeting/` and run `/ingest-resource` on each. That folder is the inbox: raw material
you are handing over. The command reads from there, writes a tidied resource note into
`40-Resources/`, and proposes atomic notes from it. This is the fastest route to a vault
that thinks the way you do, because it already contains what you think.

If you have not written much, pick the key papers and authors in the area you want to work
in and ingest those instead. It works, but the vault will start out sounding like the field
rather than like you.

**Talk to it rather than operating it**, as above — and note that this changes nothing about
how carefully anything happens. Asked conversationally, a command still proposes before it
writes, still shows you what it found, and still waits. The approval steps are the workflow,
not a formality attached to the slash. If anything arrives already created, something has
gone wrong.

Either way, expect the first fortnight to be feeding rather than harvesting.

---

## What this is not

This is a **research artefact**, not a product. It is released so people can try the
approach described in the paper and take it somewhere else.

- **Unsupported.** Issues and discussions are welcome; replies are not promised.
- **Opinionated.** The `00-Index/Values Statement.md` sets out a position on AI-assisted
  knowledge work. You inherit it by cloning, so read it — and disagree with it in your own
  copy if you want to.
- **A starting structure.** The commands encode one person's working method. Changing them
  is the expected use, not a fork.

---

## Licence

Dual-licensed, split at the directory:

- **`.claude/` and `tools/`** — [MIT](LICENSE). Commands, skills and scripts, so anyone can
  lift them into their own tooling without a compatibility question.
- **Everything else** — [CC BY 4.0](LICENSE-CONTENT). Vault content, templates, index pages
  and documentation. Use it however you like, including commercially; credit the source.

## Credits

Built by David Millard ([DAIS Group](https://www.southampton.ac.uk/dais/), University of
Southampton) in collaboration with Claude.

The tools it leans on are other people's work:

- [Obsidian](https://obsidian.md)
- [Dataview](https://community.obsidian.md/plugins/dataview) — Michael Brenan
- [Semantic Notes Vault MCP](https://community.obsidian.md/plugins/semantic-vault-mcp) — Aaron Bockelie
- [Smart Connections](https://community.obsidian.md/plugins/smart-connections) — Brian Petro
- [Supercharged Links](https://community.obsidian.md/plugins/supercharged-links-obsidian) — mdelobelle & Emile
- [smart-connections-mcp](https://github.com/msdanyg/smart-connections-mcp) — Daniel Glickman (MIT)
