# 80-Fleeting — Inbox

Your inbox to Claude. Drop raw material here — articles, transcripts, drafts, PDFs, half
-thoughts — and it becomes available to work from. `/ingest-resource` looks here when given
a bare filename, and files are usually organised as `YYYY/Month/`.

**Inbound only.** Claude reads *from* this folder and never writes deliverables *to* it:
resource notes go to `40-Resources/`, analyses to `60-Analysis/<year>/`. Original sources
stay where you put them.

Source PDFs here are gitignored by default: they are never note content, and they are the
most likely place for material about other people to arrive.
