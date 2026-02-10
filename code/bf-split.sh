#!/usr/bin/env sh
set -eu

# bf-split.sh
# Split a Brewfile into:
#  - Brewfile.current : lines WITHOUT the marker
#  - Brewfile.next    : lines WITH the marker (marker removed)
#
# Usage:
#   ./bf-split.sh [--file Brewfile] [--marker '#next'] [--install current|next]
#
# Notes:
#   - Marker is matched only at end of line (with optional trailing spaces).
#   - Existing Brewfile.current / Brewfile.next will be overwritten.
#   - Safe: creates a timestamped backup of original Brewfile alongside it.
#
# chmod +x bf-split.sh
# 
# Minimal usage
# Tag future lines with:  brew "jq"  #next
# ./bf-split.sh                       # reads ./Brewfile, marker '#next'
# brew bundle install --file=Brewfile.current
# …later:
# brew bundle install --file=Brewfile.next
#
# Customizations
# Different source file and marker:
# ./bf-split.sh --file ./infra/Brewfile --marker '#later'
#
# Do the split and immediately install the current set:
# ./bf-split.sh --install current


BREWFILE="Brewfile"
MARKER="#next"
DO_INSTALL=""

while [ $# -gt 0 ]; do
  case "$1" in
    --file)   BREWFILE="${2:-}"; shift 2 ;;
    --marker) MARKER="${2:-}";   shift 2 ;;
    --install)
      case "${2:-}" in
        current|next) DO_INSTALL="$2"; shift 2 ;;
        *) echo "ERROR: --install expects 'current' or 'next'." >&2; exit 2 ;;
      esac
      ;;
    -h|--help)
      grep -E '^# ' "$0" | sed 's/^# //'
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

[ -f "$BREWFILE" ] || { echo "ERROR: File not found: $BREWFILE" >&2; exit 1; }

CURRENT="Brewfile.current"
NEXT="Brewfile.next"

# Backup original Brewfile
TS="$(date +%Y%m%d-%H%M%S)"
cp -f "$BREWFILE" "${BREWFILE}.bak.${TS}"

# Empty output files
: > "$CURRENT"
: > "$NEXT"

# Build a basic AWK program with the chosen marker.
# Match: marker at end of line, optionally preceded by spaces.
# Example regex when MARKER='#next' -> /[[:space:]]*#next[[:space:]]*$/
awk -v marker="$MARKER" -v nextf="$NEXT" -v curf="$CURRENT" '
  BEGIN {
    # Escape marker for regex: we only need to escape literal slashes
    gsub("/", "\\/", marker)
    pattern = "[[:space:]]*" marker "[[:space:]]*$"
  }
  {
    line = $0
    if ($0 ~ pattern) {
      sub(pattern, "", line)     # strip marker
      print line >> nextf
    } else {
      print $0 >> curf
    }
  }
' "$BREWFILE"

# Optional install step
if [ -n "$DO_INSTALL" ]; then
  case "$DO_INSTALL" in
    current)
      echo "Installing current set from $CURRENT…"
      brew bundle install --file="$CURRENT"
      ;;
    next)
      echo "Installing next set from $NEXT…"
      brew bundle install --file="$NEXT"
      ;;
  esac
fi

echo "Done."
echo "  -> $CURRENT (now) "
echo "  -> $NEXT    (future)"
echo "Backup of original: ${BREWFILE}.bak.${TS}"

