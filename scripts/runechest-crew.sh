#!/usr/bin/env bash
# runechest-crew — the crew page with the REAL mood of each agent, on this machine only.
# It reads the `status` property of each agent note in the vault (11-Agentes), writes docs/crew/status.json
# (git-ignored, never published), serves docs/ on 127.0.0.1 and opens the browser. Ctrl-C stops it.
#   em andamento, ativo, em revisão     -> thinking (trabalhando)
#   concluído, mesclado, pronto         -> happy
#   em espera, aguardando, idle, ...    -> idle
# Until 2.9.0 the notes keep the 2.8.0 names; MAP links them to the Norse names.
set -u
DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=runechest-lib.sh
. "$DIR/scripts/runechest-lib.sh"
NOTES=$DD_VAULT/11-Agentes
OUT=$DIR/docs/crew/status.json
PORT=${RUNECHEST_CREW_PORT:-8765}

python3 -I - "$NOTES" "$OUT" <<'PY'
import json, re, sys
from pathlib import Path

notes, out = Path(sys.argv[1]), Path(sys.argv[2])
# Norse id -> the 2.8.0 notes (the first busy one wins). The 2.9.0 notes use the Norse name itself.
MAP = {
    "odin": ["Odin", "Bird"], "heimdall": ["Heimdall", "Tirr"], "forseti": ["Forseti", "Maestro"],
    "eitri": ["Eitri", "Hecarim"], "volundr": ["Völundr", "Volundr", "Picasso"],
    "brokkr": ["Brokkr", "Dormanu", "Octopus"], "egill": ["Egill"], "grisnir": ["Grisnir"],
    "gnjostr": ["Gnjóstr", "Gnjostr"], "mimir": ["Mímir", "Mimir", "Antares"], "bifrost": ["Bifröst", "Bifrost", "Antagon"],
    "bragi": ["Bragi", "Lupin"], "nidhoggr": ["Níðhöggr", "Nidhoggr", "Nyx"],
}
BUSY = ("andamento", "ativo", "revisão", "revisao", "trabalhando")
DONE = ("concluído", "concluido", "mesclado", "pronto", "done")
RANK = {"thinking": 2, "happy": 1, "idle": 0}


def mood(note: Path) -> str | None:
    if not note.exists():
        return None
    head = note.read_text(encoding="utf-8").split("---", 2)
    m = re.search(r'^status:\s*"?([^"\n]*)', head[1] if len(head) > 2 else "", re.M)
    if not m:
        return None
    s = m.group(1).strip().lower()
    return "thinking" if any(w in s for w in BUSY) else "happy" if any(w in s for w in DONE) else "idle"


result = {}
for nid, names in MAP.items():
    found = [x for x in (mood(notes / f"{n}.md") for n in names) if x]
    if found:
        result[nid] = max(found, key=RANK.get)
out.write_text(json.dumps(result, ensure_ascii=False) + "\n", encoding="utf-8")
print("  " + "  ".join(f"{k}:{v}" for k, v in result.items()))
PY

# Never fight for a port: when PORT is busy (another session's server), take a free one.
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    PORT=$(python3 -I -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')
fi
printf '\n  %sA tripulação com o humor real%s: http://127.0.0.1:%s/  %s(Ctrl-C para parar)%s\n\n' \
    "$DD_M$DD_B" "$DD_R" "$PORT" "$DD_D" "$DD_R"
[ -n "${RUNECHEST_NO_OPEN:-}" ] || ( sleep 1; open "http://127.0.0.1:$PORT/" ) &
cd "$DIR/docs" && exec python3 -m http.server "$PORT" --bind 127.0.0.1
