# The Norse crew: names, runes and typography

Status: **decided by the user on 17/11/2026, applied at the start of FoodBot 2.9.0.** Until then the agents keep the
Runeterra names (Swain, Galio, …). Nothing changes in the middle of 2.8.0.

## Decisions (user, 17/11/2026)

1. **Names by layer.** Gods lead and specialise; dwarf smiths execute and help; beasts do the mechanical work and eat
   the dead code; objects and creatures name the infrastructure.
2. **Runes: Unicode now, SVG later.** The tabs, the panel and the agent menu use the real Elder Futhark runes of
   Unicode (U+16A0–16FF; macOS draws them with Apple Symbols). Later we draw our own SVG runes (one bind-rune per
   agent), build the `Deepdeck Runes` font and map it in Ghostty with `font-codepoint-map`.
3. **Typography in the terminal: Monaspace.** Ghostty draws italic with Monaspace Radon. The scripts print the agent
   names in italic, so a name looks different from the code around it.
4. **Scope: everything, at the start of 2.9.0.** Deepdeck, `.claude/agents`, the skills, `bin/agent`, the hooks, the
   vault (`11-Agentes`, `Identidade`, `Arquitetura-Agentes`) and the README change together, when the sessions restart.

## The crew

| Rune | Name | Role | Today (Runeterra) | Why this name |
|---|---|---|---|---|
| ᚨ Ansuz | **Odin** | Orchestrator: plans the version, writes the tickets, never edits code | Swain | The All-Father sees everything from his throne and decides; Ansuz is the rune of the god and of the word |
| ᛉ Algiz | **Heimdall** | Backend integrator: reviews and merges service PRs, owns the migrations | Galio | The guard of the bridge: nothing passes without him |
| ᛏ Tiwaz | **Forseti** | App integrator: design fidelity, reviews and merges app PRs | Taric | The judge who settles every dispute |
| ᚲ Kenaz | **Eitri** | Backend executor | Viktor | The dwarf smith who forged Mjölnir; Kenaz is the torch of the forge |
| ᚷ Gebo | **Völundr** | App executor | Heimerdinger | The master craftsman of fine pieces: the interface |
| ᚠ Fehu | **Brokkr** | Code helper of Eitri | Xayah | Eitri's brother, who kept the bellows going |
| ᛇ Eihwaz | **Egill** | Code helper of Völundr | Rakan | Völundr's brother, the archer: precise work |
| ᚢ Uruz | **Grisnir** | Mechanical helper of Eitri (tests, regressivo, search) | Ziggs | Tanngrisnir, Thor's goat: works all day, comes back new each morning (a fresh session) |
| ᚢ Uruz | **Gnjóstr** | Mechanical helper of Völundr (analyze, format, tests) | Rumble | Tanngnjóstr, the other goat |
| ᛚ Laguz | **Mímir** | AI full-stack: the assistant, calibration, pricing, the lab | Zilean | The wise one of the well of memory, who counsels Odin; Laguz is the water of the well |
| ᚱ Raidho | **Bifröst** | Integrations full-stack: iFood, the WhatsApp bot, the landing, the alerts | Thresh | The bridge between the worlds; Raidho is the journey |
| ᚹ Wunjo | **Bragi** | Marketing, design, PDFs, product copy | Lupin | The god of poetry and eloquence |
| ᚺ Hagalaz | **Níðhöggr** | Dead code and refactor | Pyke | The dragon that gnaws the dead roots of the tree; Hagalaz is the hail that clears |

## The infrastructure

| Name | What it is | Why |
|---|---|---|
| **Yggdrasil** | The Obsidian vault (one note per agent) | The tree that holds the nine worlds together |
| **Gleipnir** | The `agent-guard` hook (no merge to main, no secrets, no production writes) | The thin chain that holds Fenrir: the hard limits |
| **Ratatoskr** | The notifications (`deepdeck-notify.sh`) | The squirrel that carries the messages up and down the tree |
| **Huginn e Muninn** | The PAINEL tab | Odin's ravens, thought and memory, who fly out and report back |

## Rename checklist (start of 2.9.0)

The orchestrator (Odin, today Swain/Bird) turns this into tickets. Order: the identity table first, because the
scripts read it.

1. Vault: `11-Agentes/Identidade.md` (name, rune, colour, layer, role), `Arquitetura-Agentes.md`, one note per agent
   (rename the files, keep the history in the note), `Agentes.base`.
2. FoodBot: `.claude/agents/<name>.md` (the contracts), the skills (`/<agent>-<action>` and the ability names in the
   descriptions), `foodbot-ops/bin/agent`, `bin/agent-context`, `bin/agent-guard` (the allowed mergers), `CLAUDE.md`.
3. Deepdeck: the `deepdeck` layout (tab names with the runes), `deepdeck-panel.sh` and `deepdeck-agents.sh` (italic
   names), the README crew table.
4. GitHub signatures: `OK (ᛉ Heimdall)` replaces `OK (🗿 Galio)`.
5. Later: the SVG runes, the `Deepdeck Runes` font, `font-codepoint-map` in Ghostty.
