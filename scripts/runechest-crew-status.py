#!/usr/bin/env python3
"""runechest-crew-status — the real emotion of each agent, every 30 s, for the local crew page.

Sources (user decision, 17/11: vault + GitHub + machine):
  vault   11-Agentes/<note>.md: `bloqueio` filled -> worried; `status` "em revisão" -> suspicious,
          "em andamento"/"ativo" -> focused; anything else -> idle.
  GitHub  the PRs named in the note's `pr` field (service#N, app#N, ops#N, #N = service):
          merged in the last 2 min -> celebrating; open with a last comment "CHANGES REQUESTED" -> worried.
  machine `foodbot-ops/bin/heavy --status`: a heavy or quick run in the worktree of the agent's PR branch -> focused.
Priority: celebrating > worried > focused (machine) > the vault state.
Writes docs/crew/status.json (git-ignored, never published): {"odin": {"state": "focused", "why": "..."}}.
Run: python3 -I scripts/runechest-crew-status.py <vault 11-Agentes dir> <out json> [--once]
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

NOTES, OUT = Path(sys.argv[1]), Path(sys.argv[2])
ONCE = "--once" in sys.argv
HEAVY = Path.home() / "Foodbot" / "foodbot-ops" / "bin" / "heavy"
REPOS = {"service": "HenriqueMachine/foodbot-service", "app": "HenriqueMachine/foodbot-app",
         "ops": "HenriqueMachine/foodbot-ops"}
# Norse id -> the notes (the 2.9.0 Norse note first, then the 2.8.0 notes).
MAP = {
    "odin": ["Odin", "Bird"], "heimdall": ["Heimdall", "Tirr"], "forseti": ["Forseti", "Maestro"],
    "eitri": ["Eitri", "Hecarim"], "volundr": ["Völundr", "Picasso"], "brokkr": ["Brokkr", "Dormanu", "Octopus"],
    "egill": ["Egill"], "grisnir": ["Grisnir"], "gnjostr": ["Gnjóstr"], "mimir": ["Mímir", "Antares"],
    "bifrost": ["Bifröst", "Antagon"], "bragi": ["Bragi", "Lupin"], "nidhoggr": ["Níðhöggr", "Nyx"],
}
RANK = {"celebrating": 4, "worried": 3, "focused": 2, "suspicious": 1, "idle": 0}
merged_cache: dict = {}


def front(note: Path) -> dict:
    if not note.exists():
        return {}
    parts = note.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        return {}
    out = {}
    for line in parts[1].splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip()
    return out


def vault_state(fm: dict) -> tuple[str, str]:
    block, status = fm.get("bloqueio", ""), fm.get("status", "").lower()
    if block:
        return "worried", "bloqueio: " + block[:60]
    if "revis" in status:
        return "suspicious", status
    if any(w in status for w in ("andamento", "ativo", "trabalhando")):
        return "focused", status
    return "idle", status


def pr_refs(text: str) -> list:
    refs = []
    for repo, num in re.findall(r"\b(service|app|ops)?#(\d{2,5})\b", text):
        refs.append((REPOS[repo or "service"], int(num), (repo or "service") + "#" + num))
    return refs[:3]


def gh_pr(repo: str, num: int):
    key = (repo, num)
    if key in merged_cache:
        return merged_cache[key]
    try:
        out = subprocess.run(
            ["gh", "pr", "view", str(num), "-R", repo, "--json", "state,mergedAt,headRefName,comments",
             "--jq", "{state, mergedAt, headRefName, last: (.comments[-1].body // \"\")}"],
            capture_output=True, text=True, timeout=15)
        data = json.loads(out.stdout) if out.returncode == 0 else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        data = None
    if data and data.get("state") == "MERGED":
        merged_cache[key] = data
    return data


def heavy_branches() -> set:
    try:
        out = subprocess.run([str(HEAVY), "--status"], capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.TimeoutExpired):
        return set()
    branches = set()
    for path in re.findall(r"\((/[^)]+)\)", out):
        try:
            b = subprocess.run(["git", "-C", path, "branch", "--show-current"], capture_output=True, text=True,
                               timeout=5).stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            b = ""
        if b:
            branches.add(b)
    return branches


def one_pass() -> dict:
    running, now, result = heavy_branches(), datetime.now(timezone.utc), {}
    for nid, names in MAP.items():
        best = None
        for name in names:
            fm = front(NOTES / f"{name}.md")
            if not fm:
                continue
            state, why = vault_state(fm)
            for repo, num, label in pr_refs(fm.get("pr", "")):
                pr = gh_pr(repo, num)
                if not pr:
                    continue
                if pr.get("mergedAt"):
                    age = (now - datetime.fromisoformat(pr["mergedAt"].replace("Z", "+00:00"))).total_seconds()
                    if age <= 120:
                        state, why = "celebrating", f"{label} mesclado"
                elif pr.get("state") == "OPEN" and pr.get("last", "").startswith("CHANGES REQUESTED"):
                    if RANK[state] < RANK["worried"]:
                        state, why = "worried", f"{label}: mudança pedida no PR"
                if pr.get("headRefName") in running and RANK[state] < RANK["focused"]:
                    state, why = "focused", f"{label}: verificação rodando"
            if best is None or RANK[state] > RANK[best[0]]:
                best = (state, why)
        if best:
            result[nid] = {"state": best[0], "why": best[1]}
    return result


while True:
    status = one_pass()
    OUT.write_text(json.dumps(status, ensure_ascii=False) + "\n", encoding="utf-8")
    if ONCE:
        print("  " + "  ".join(f"{k}:{v['state']}" for k, v in status.items()))
        break
    time.sleep(30)
