#!/usr/bin/env bash
# deepdeck-runes — shows the Norse crew: the rune (Deepdeck Runes font), the name in italic (Monaspace Radon) and the
# neon of the layer. It reads assets/runes/codepoints.tsv (written by assets/runes/build.py).
set -u
DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=deepdeck-lib.sh
. "$DIR/scripts/deepdeck-lib.sh"
TABLE=$DIR/assets/runes/codepoints.tsv
[ -f "$TABLE" ] || { echo "sem $TABLE: rode .venv/bin/python assets/runes/build.py"; exit 1; }

printf '\n  %s%sA tripulação nórdica%s %s(nomes valem a partir da 2.9.0)%s\n\n' "$DD_M" "$DD_B" "$DD_R" "$DD_D" "$DD_R"
tail -n +2 "$TABLE" | while IFS=$'\t' read -r name cp neon role today; do
    hex=${cp#U+}
    rune=$(printf "\\U$(printf '%08X' "0x$hex")")
    printf '  %s%s%s  %s\e[3m%-10s\e[23m%s %s%-28s%s %shoje %s%s\n' \
        "$(dd_fg "$neon")" "$rune" "$DD_R" "$(dd_fg "$neon")" "$name" "$DD_R" \
        "$DD_W" "$role" "$DD_R" "$DD_D" "$today" "$DD_R"
done
printf '\n'
