# Contributing

Thanks for looking. A few honest expectations first.

## What this repository is

Trailkasten is a **research artefact**, released so people can try the approach described in
the [paper](https://doi.org/10.1145/3800935.3830837) rather than only read about it. It is
not a product, and it is maintained in whatever time is left over from the research it came
out of.

**Issues and discussions are welcome. Replies are not promised.** If you need something
fixed on a schedule, fork it — that is a legitimate outcome, not a failure.

## The most useful thing you can do

**Tell us where a new user gets stuck.** The install sequence has an ordering dependency
that is invisible until it bites, the vault is deliberately near-empty on arrival, and the
first `/vault-health` run says almost nothing. Those are all known. What is not known is
which *other* moment made you close the terminal. That report is worth more than a patch.

## Good contributions

- **Documentation fixes.** Wrong link, stale instruction, a step that assumes knowledge the
  reader does not have. Always welcome, always merged quickly.
- **Portability fixes.** Anything that assumes macOS, a particular path, or a tool that is
  not in the requirements list.
- **Command and skill improvements**, if they generalise. The test is whether the change
  helps someone whose research has nothing to do with hypertext.

## Less good contributions

- **New commands encoding your own workflow.** These are genuinely valuable — to you. The
  expected use of this repository is that you change the commands to suit how you think, and
  most of those changes should stay in your copy. If you build something you believe is
  general, open a discussion before writing it.
- **Adding dependencies.** The requirement list is four plugins and it is deliberately
  short. Anything that grows it needs to earn its place.
- **Vendoring third-party code.** Plugins and MCP servers are installed by the user, never
  bundled here. This is a licensing position as well as a size one.

## If you change the tooling

Record it in `00-Index/Vault Rationale.md`, in the format that page describes: what changed,
why, which values it engages, which files. This applies to contributions as much as to your
own edits — a change to a command without a rationale entry is a change whose reasoning
will be lost.

## Style

- **Match the existing spelling convention**, which is British English. Not a principle — just consistency.
- **Tentative register** in vault content: the vault captures perspectives rather than
  establishing truths. See `.claude/skills/vault-writing-style/`.
- Commands and skills are written as instructions to a model. Be specific, say why a rule
  exists, and prefer a worked example over an abstract principle.

## Licence

Contributions to `.claude/` and `tools/` are accepted under MIT; contributions to vault
content and documentation under CC BY 4.0. By opening a pull request you agree to license
your contribution on those terms.
