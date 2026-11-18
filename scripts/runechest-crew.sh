#!/usr/bin/env bash
# runechest-crew — the crew page with the REAL emotion of each agent, on this machine only.
# scripts/runechest-crew-status.py writes docs/crew/status.json (git-ignored, never published) from the vault, GitHub
# and the heavy queue, every 30 s; this script serves docs/ on 127.0.0.1 and opens the browser. Ctrl-C stops both.
set -u
DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=runechest-lib.sh
. "$DIR/scripts/runechest-lib.sh"
NOTES=$DD_VAULT/11-Agentes
OUT=$DIR/docs/crew/status.json
PORT=${RUNECHEST_CREW_PORT:-8765}

# The emotions (vault + GitHub + the heavy queue), once now and then every 30 s while the page runs.
python3 -I "$DIR/scripts/runechest-crew-status.py" "$NOTES" "$OUT" --once
python3 -I "$DIR/scripts/runechest-crew-status.py" "$NOTES" "$OUT" &
COLLECTOR=$!
trap 'kill "$COLLECTOR" 2>/dev/null' EXIT INT TERM

# Never fight for a port: when PORT is busy (another session's server), take a free one.
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    PORT=$(python3 -I -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')
fi
printf '\n  %sA tripulação com o humor real%s: http://127.0.0.1:%s/  %s(Ctrl-C para parar)%s\n\n' \
    "$DD_M$DD_B" "$DD_R" "$PORT" "$DD_D" "$DD_R"
[ -n "${RUNECHEST_NO_OPEN:-}" ] || ( sleep 1; open "http://127.0.0.1:$PORT/" ) &
cd "$DIR/docs" && python3 -m http.server "$PORT" --bind 127.0.0.1
