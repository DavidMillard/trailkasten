#!/usr/bin/env bash
# Pre-publication scrub. Checks a vault for material that should not leave your
# machine before you publish or share it.
#
#   ./tools/scrub-check.sh            # generic checks only
#   ./tools/scrub-check.sh --local    # also apply tools/scrub-patterns.local
#
# Exit 0 = clean, 1 = hits found.
#
# WHY THE PERSONAL PATTERNS LIVE ELSEWHERE
# A scrub list naming the things you are hiding discloses them to anyone who
# reads it. Keep your own terms — your domains, the services you use, project
# names, collaborators — in `tools/scrub-patterns.local`, which is gitignored.
# One extended-regex pattern per line; blank lines and # comments ignored.
#
# AND THE LIMIT WORTH KNOWING
# This catches shapes: addresses, paths, key-like strings. It cannot catch
# biography, a quoted unpublished draft, or a workflow that assumes your setup.
# Those need reading. A clean run here means "no obvious shapes", never "safe".

set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

EXCLUDES=(--exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.smart-env
          --exclude-dir=.obsidian
          # This script is excluded because its own pattern strings match
          # themselves. That is only safe because it holds no personal terms —
          # they live in the gitignored local file. Never put a name, a domain
          # or a service in here: it would be both published and unscanned.
          --exclude=scrub-check.sh)

# Files where your own name and affiliation BELONG — citation, credits, licence.
# They are still scanned for addresses, paths and keys.
ATTRIB=(--exclude=README.md --exclude=CITATION.cff --exclude=LICENSE
        --exclude=LICENSE-CONTENT --exclude=CONTRIBUTING.md)

fail=0
LOCAL=0
[ "${1:-}" = "--local" ] && LOCAL=1

report() {
  local label="$1" hits="$2"
  if [ -n "$hits" ]; then
    printf '\n\033[31m✗ %s\033[0m\n' "$label"
    printf '%s\n' "$hits" | sed 's/^/    /' | head -40
    fail=1
  else
    printf '\033[32m✓\033[0m %s\n' "$label"
  fi
}

# check <label> <pattern> [scope] [allow-pattern]
# Only POSIX extended regex is used: no lookahead, no -P. A pattern grep cannot
# compile must fail loudly rather than pass quietly, so compilation is verified
# before the scan and an unusable pattern is reported as an error, not a pass.
check() {
  local label="$1" pattern="$2" scope="${3:-all}" allow="${4:-}"
  local extra=() hits
  [ "$scope" = "not-attrib" ] && extra=("${ATTRIB[@]}")

  # grep exits 0 on match, 1 on no match, >1 on error. Only >1 means the
  # pattern could not be compiled, and that must be loud: a check that silently
  # does not run is worse than no check.
  printf 'scrub-compile-probe\n' | grep -E -- "$pattern" >/dev/null 2>&1
  if [ $? -gt 1 ]; then
    printf '\n\033[31m! %s — pattern failed to compile; CHECK DID NOT RUN\033[0m\n' "$label"
    fail=1; return
  fi

  hits=$(grep -rniE "${EXCLUDES[@]}" "${extra[@]+"${extra[@]}"}" -- "$pattern" . 2>/dev/null) || true
  [ -n "$allow" ] && hits=$(printf '%s\n' "$hits" | grep -vE -- "$allow" || true)
  hits=$(printf '%s' "$hits" | sed '/^$/d')
  report "$label" "$hits"
}

echo "Scrubbing $(pwd)"
echo

check "Email addresses"        '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' not-attrib 'example\.(com|org|net)'
check "Home directory paths"   '/(Users|home)/[a-z0-9_-]+/'
check "Cloud-sync paths"       'Mobile Documents|iCloud~|Dropbox/|OneDrive/'
check "API keys and tokens"    '(api[_-]?key|secret|token|bearer)"?\s*[:=]\s*"?[A-Za-z0-9_-]{16,}'
# localhost:3001 is the documented Obsidian plugin port and appears in the setup
# instructions; anything else local is likely someone's own machine.
check "Private network hosts"  'https?://(localhost|127\.0\.0\.1|192\.168\.|10\.[0-9])' all 'localhost:3001/mcp'
check "Committed MCP config"   '^\./\.mcp\.json$'

# Your own terms, kept out of this file on purpose.
if [ "$LOCAL" -eq 1 ]; then
  if [ -f tools/scrub-patterns.local ]; then
    while IFS= read -r pat; do
      [ -z "$pat" ] && continue
      case "$pat" in \#*) continue ;; esac
      hits=$(grep -rniE "${EXCLUDES[@]}" "${ATTRIB[@]}" -- "$pat" . 2>/dev/null) || true
      report "Local pattern: $(printf '%.28s' "$pat")" "$hits"
    done < tools/scrub-patterns.local
  else
    printf '\033[33m!\033[0m No tools/scrub-patterns.local — skipping personal checks\n'
  fi
fi

echo
if [ "$fail" -eq 0 ]; then
  printf '\033[32mNo obvious shapes found.\033[0m Now read the files — this cannot catch biography or quoted drafts.\n'
else
  printf '\033[31mHits found.\033[0m Clear every one before publishing.\n'
fi
exit "$fail"
