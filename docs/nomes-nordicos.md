# The Norse crew: names, runes and typography

Status: **decided by the user on 17/11/2026, applied at the start of FoodBot 2.9.0.** Until then the agents keep the
Runeterra names (Swain, Galio, …). Nothing changes in the middle of 2.8.0.

## Decisions (user, 17/11/2026)

1. **Names by layer.** Gods lead and specialise; dwarf smiths execute and help; beasts do the mechanical work and eat
   the dead code; objects and creatures name the infrastructure.
2. **Runes: our own bind-runes (approved 17/11, draft 3).** One bind-rune per agent (the rune of the first letter +
   the rune of the role), with Mad Max cuts (chamfered ends, V notches) and the neon of the layer. They live in
   `assets/runes/`: `<name>.svg` (one colour, for the font), `<name>-neon.svg` (glow, for the README, the site and the
   slides), `preview.html`, and the `RuneChest Runes` font (U+100000 to U+10000C, mapped in Ghostty with
   `font-codepoint-map`). `runechest runas` shows them. Build: `.venv/bin/python assets/runes/build.py --install`.
   The Unicode Elder Futhark runes stay the fallback where the font is not installed (GitHub, Obsidian).
3. **Typography in the terminal: Monaspace.** Ghostty draws italic with Monaspace Radon. The scripts print the agent
   names in italic, so a name looks different from the code around it.
4. **Scope: everything, at the start of 2.9.0.** RuneChest, `.claude/agents`, the skills, `bin/agent`, the hooks, the
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
| **Ratatoskr** | The notifications (`runechest-notify.sh`) | The squirrel that carries the messages up and down the tree |
| **Huginn e Muninn** | The PAINEL tab | Odin's ravens, thought and memory, who fly out and report back |

## Rename checklist (start of 2.9.0)

The orchestrator (Odin, today Swain/Bird) turns this into tickets. Order: the identity table first, because the
scripts read it.

1. Vault: `11-Agentes/Identidade.md` (name, rune, colour, layer, role), `Arquitetura-Agentes.md`, one note per agent
   (rename the files, keep the history in the note), `Agentes.base`.
2. FoodBot: `.claude/agents/<name>.md` (the contracts), the skills (`/<agent>-<action>` and the ability names in the
   descriptions), `foodbot-ops/bin/agent`, `bin/agent-context`, `bin/agent-guard` (the allowed mergers), `CLAUDE.md`.
3. RuneChest: the `runechest` layout (tab names with the runes), `runechest-panel.sh` and `runechest-agents.sh` (italic
   names), the README crew table.
4. GitHub signatures: `OK (ᛉ Heimdall)` replaces `OK (🗿 Galio)`.
5. Tabs and scripts: print the rune of `assets/runes/codepoints.tsv` before each agent name.
