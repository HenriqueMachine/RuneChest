<p align="center"><img src="assets/runes/banner.svg" alt="RuneChest: the thirteen neon runes of the crew" width="100%"></p>

# RuneChest

**One developer, a team of agents.** RuneChest is the personal development environment of a solo founder: the
terminal, the editor and a crew of Claude Code agents in one calm screen. You decide what to build and you review
what comes back. The agents plan, write, test and keep the paperwork, each one with its own role.

It started as the work environment of FoodBot (a SaaS for iFood restaurants, built by one person and a dozen
agents), and it is the "at home" version of the talk *Card #2187 · Pare de conversar. Delegue.*

## The idea

Three limits drive every decision here:

1. **Context is finite.** The more an agent reads, the worse it answers (the "smart zone" and the "dumb zone").
   So each agent gets a small, focused job and a fresh session.
2. **An agent wakes up with no memory** (like Leonard in *Memento*). So the state lives in files that the agent
   reads when it starts: the rules, the agent note, the ticket, git.
3. **A promise is not evidence.** "The tests passed" does not count. Hooks, a heavy-command queue and one full
   check per pull request give the real output.

From these limits come the four rules of the crew:

- **One decides, many execute** (orchestrator-workers). The orchestrator plans and delegates; it does not edit code.
- **One owner per area.** Backend and app have separate executors and separate integrators, so two agents never
  edit the same file.
- **The author never merges.** An integrator reviews and merges to `develop`. Only the human merges to `main`,
  deploys and touches secrets.
- **The human spends attention at the start and the end.** At the start: what to build (the interview, the
  ticket). At the end: the review by risk. The middle belongs to the harness.

## Architecture

```mermaid
flowchart TB
    subgraph Screen["RuneChest screen"]
        G[Ghostty<br/>font, palette, GPU]
        Z[Zellij<br/>tabs per role, key bar]
        N[Neovim + GUIA<br/>LazyVim, command guide]
        P[PAINEL · Huginn and Muninn<br/>agents, heavy lanes, PRs, tokens]
    end
    subgraph Crew["The crew (Claude Code sessions)"]
        S[Odin · orchestrator]
        I[Heimdall · Forseti<br/>integrators]
        E[Eitri · Völundr · Mímir<br/>executors]
        H[Brokkr · Egill · Grisnir · Gnjóstr<br/>helpers as subagents]
    end
    subgraph Memory["State in files (the Memento tattoos)"]
        V[(Yggdrasil · Obsidian vault<br/>one note per agent,<br/>Agentes.base)]
        C[CLAUDE.md + skills<br/>+ agent contracts]
        Git[(git + PRs<br/>changelog)]
    end
    subgraph Harness["Harness (what a prompt cannot promise)"]
        K[hooks: Gleipnir agent-guard,<br/>agent-context, Ratatoskr notify]
        Q[heavy queue<br/>heavy and quick lanes]
    end
    U([You]) --> G --> Z
    Z --> N & P & Crew
    S --> E --> H
    E -- PR --> I -- develop --> U
    Crew <--> Memory
    Crew --> Harness
    P -. reads .-> V & Q & Git
```

| Layer | Tool | Job |
|---|---|---|
| Terminal | Ghostty | Native and light on the GPU; JetBrains Mono 16, soft palette, Option as Alt |
| Multiplexer | Zellij | One tab per role, agent panes that start suspended (ENTER starts the agent), the key bar |
| Editor | Neovim (LazyVim) | The code, with the GUIA pane next to it while you learn the keys |
| Panel | `scripts/runechest-panel.sh` | Agents and their status, the diary, the heavy lanes, open PRs, tokens of the day |
| Agents | Claude Code | One session per role, started with `runechest agent <name>` or the AGENTES menu |
| Memory | Obsidian vault, git | One note per agent (status, task, PR, block, next step); the source of truth |
| Harness | hooks, `heavy` | Hard limits (no merge to main, no secrets), one verification per PR, notifications |

## The crew

Every agent takes a Norse name by layer: gods lead and specialise, dwarf smiths execute and help, beasts do the
mechanical work and eat the dead code. Each one has a **bind-rune** (the rune of the first letter + the rune of the
role, cut Mad Max style, in the neon of its layer) and an **avatar** (a Norse object or creature, made with
[open-bot-avatar](https://github.com/DominikScholz/open-bot-avatar), MIT). The full story of each name is in
[docs/nomes-nordicos.md](docs/nomes-nordicos.md). The FoodBot sessions switch to these names at the start of 2.9.0;
the last column is the name they use until then.

| Rune | Avatar | Agent | Role | Model | Session | Until 2.9.0 |
|:---:|:---:|---|---|---|---|---|
| <img src="assets/runes/odin-neon.svg" width="44" alt="rune of Odin"> | <img src="assets/avatars/still/odin.svg" width="56" alt="Odin avatar"> | **Odin** | Orchestrator: plans the version, writes the tickets, decides with you, runs the release. Never edits code | Opus | fixed | Swain |
| <img src="assets/runes/heimdall-neon.svg" width="44" alt="rune of Heimdall"> | <img src="assets/avatars/still/heimdall.svg" width="56" alt="Heimdall avatar"> | **Heimdall** | Backend integrator: reviews and merges service PRs, owns the migration queue | Opus | fixed | Galio |
| <img src="assets/runes/forseti-neon.svg" width="44" alt="rune of Forseti"> | <img src="assets/avatars/still/forseti.svg" width="56" alt="Forseti avatar"> | **Forseti** | App integrator: design fidelity, reviews and merges app PRs | Opus | fixed | Taric |
| <img src="assets/runes/eitri-neon.svg" width="44" alt="rune of Eitri"> | <img src="assets/avatars/still/eitri.svg" width="56" alt="Eitri avatar"> | **Eitri** | Backend executor: plans and writes the service features | Opus | fixed | Viktor |
| <img src="assets/runes/volundr-neon.svg" width="44" alt="rune of Völundr"> | <img src="assets/avatars/still/volundr.svg" width="56" alt="Völundr avatar"> | **Völundr** | App executor: plans and writes the Flutter screens | Opus | fixed | Heimerdinger |
| <img src="assets/runes/mimir-neon.svg" width="44" alt="rune of Mímir"> | <img src="assets/avatars/still/mimir.svg" width="56" alt="Mímir avatar"> | **Mímir** | Full-stack AI: the assistant, calibration, pricing, the lab | Opus | fixed | Zilean |
| <img src="assets/runes/bifrost-neon.svg" width="44" alt="rune of Bifröst"> | <img src="assets/avatars/still/bifrost.svg" width="56" alt="Bifröst avatar"> | **Bifröst** | Full-stack integrations: iFood, the WhatsApp bot, the landing, the alerts | Opus | on demand | Thresh |
| <img src="assets/runes/bragi-neon.svg" width="44" alt="rune of Bragi"> | <img src="assets/avatars/still/bragi.svg" width="56" alt="Bragi avatar"> | **Bragi** | Marketing, design, PDFs and product copy | Sonnet | on demand | Lupin |
| <img src="assets/runes/nidhoggr-neon.svg" width="44" alt="rune of Níðhöggr"> | <img src="assets/avatars/still/nidhoggr.svg" width="56" alt="Níðhöggr avatar"> | **Níðhöggr** | Dead code and refactor | Sonnet | on demand | Pyke |
| <img src="assets/runes/brokkr-neon.svg" width="44" alt="rune of Brokkr"> | <img src="assets/avatars/still/brokkr.svg" width="56" alt="Brokkr avatar"> | **Brokkr** | Code helper of Eitri | Sonnet | subagent | Xayah |
| <img src="assets/runes/egill-neon.svg" width="44" alt="rune of Egill"> | <img src="assets/avatars/still/egill.svg" width="56" alt="Egill avatar"> | **Egill** | Code helper of Völundr | Sonnet | subagent | Rakan |
| <img src="assets/runes/grisnir-neon.svg" width="44" alt="rune of Grisnir"> | <img src="assets/avatars/still/grisnir.svg" width="56" alt="Grisnir avatar"> | **Grisnir** | Mechanical helper of Eitri: tests, regressivo, search, vault | Haiku | subagent | Ziggs |
| <img src="assets/runes/gnjostr-neon.svg" width="44" alt="rune of Gnjóstr"> | <img src="assets/avatars/still/gnjostr.svg" width="56" alt="Gnjóstr avatar"> | **Gnjóstr** | Mechanical helper of Völundr: analyze, format, tests | Haiku | subagent | Rumble |

The infrastructure has Norse names too: **Yggdrasil** is the vault (the tree that holds the worlds together),
**Gleipnir** is the `agent-guard` hook (the thin chain that holds Fenrir), **Ratatoskr** carries the notifications
(the squirrel that runs messages up and down the tree), and **Huginn and Muninn** are the PAINEL (Odin's ravens,
thought and memory). See the crew alive: [the crew page](https://henriquemachine.github.io/RuneChest/). Each agent has a personality
(a base mood, a way to look, moods it drifts into); hover an agent and it looks at you. On your own machine,
`runechest tripulacao` shows the **real** mood of each agent, read from the `status` of its vault note (working =
thinking, merged = happy, waiting = idle). That file stays local and is never published.

A ticket passes six gates, and a failure goes back one gate: **Ready** (Odin) → **Build**, tests first
(executor) → **Candidate** → **Review** (Heimdall or Forseti; Bragi for text) → **Train** (merge in batches, one
verification) → **Regressivo** (Grisnir, Gnjóstr) → release, with your OK.

## Tabs

The agent tabs keep the current names until the 2.9.0 switch; then they show the runes and the Norse names.

| Key | Tab | What is in it |
|---|---|---|
| Option+1 | NVIM | Neovim (70 %) and the GUIA (30 %) |
| Option+2 | PAINEL | Left: agents and diary. Right: machine, PRs, tokens |
| Option+3 | 🗿⚙️ BACKEND | Galio and Viktor |
| Option+4 | 💎🔧 APP | Taric and Heimerdinger |
| Option+5 | 🐦‍⬛⏳ SWAIN | Swain and Zilean |
| Option+6 | EXTRA | Thresh, Lupin, Pyke on demand |
| Option+7 | AGENTES | fzf menu: Enter starts a session, Ctrl-R resumes one |

Other keys, in every Zellij mode (also inside Neovim): **Option+arrows** go to the next pane, **Option+g** shows
the focused pane on the full screen (it hides the guide) and back. The key bar at the bottom shows the rest.

## Palette (RuneChest soft)

| Role | Colour |
|---|---|
| Background | `#0e0e14` |
| Text | `#d8dae5` |
| Active (magenta) | `#e8457a` |
| Details (cyan) | `#4cc9d6` |
| Alerts (yellow) | `#e6c84c` |
| Dim and comments | `#878ca6` (5.8:1 on the background, WCAG AA) |

## Contents

| Path | What it is |
|---|---|
| `stow/ghostty`, `stow/zellij`, `stow/nvim` | The screen: terminal, multiplexer (theme, keys, layouts), editor |
| `stow/zsh`, `stow/git`, `stow/starship` | The shell: the `runechest` command, aliases, prompt, git |
| `scripts/runechest-*.sh` | Panel, agent menu, guide, macOS notification |
| `scripts/00-*.sh` … `40-*.sh`, `install.sh`, `update.sh` | Install and update (Homebrew, stow, Zellij plugins) |
| `docs/guia-nvim.txt` | The Neovim guide. Format: `## SECTION` and `key \| what it does` |
| `library/` | Cheat sheets, notes and snippets |
| `Brewfile` | Homebrew packages and fonts |

## Install and use

```sh
./install.sh          # Homebrew, the Brewfile, stow, the Zellij plugins
runechest              # open or go back to the runechest session
runechest agents       # the agent menu
runechest agent viktor # one agent in this pane
runechest reset        # delete the session (a new layout applies on the next open)
runechest help         # all commands
```

The agent launcher (`foodbot-ops/bin/agent`) and the agent files (`.claude/agents/*.md`) live in the project
repository, not here: RuneChest is the screen and the habits; the project brings its own crew.

## History

The first commit comes from the environment of 17/11/2026 (the old repository HenriqueMachine/AntaresOS, now
archived), without its history.
