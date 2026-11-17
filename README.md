# Deepdeck

The FoodBot work environment for a solo developer: Ghostty, Zellij and Neovim with one calm palette, the
Runeterra agents in Zellij tabs, a metrics panel and a Neovim guide.

## Contents

| Path | What it is |
|---|---|
| `stow/ghostty` | Ghostty: JetBrains Mono Nerd Font 16 pt, 10 % more line height, the Deepdeck soft palette |
| `stow/zellij` | Zellij: the `deepdeck` theme, the keys (Option+arrows, Option+1..7, Option+g in every mode) and the `deepdeck` layout |
| `stow/nvim` | Neovim (LazyVim): base16 with the Deepdeck palette, cursor line, bar cursor in insert mode |
| `scripts/deepdeck-panel.sh` | The PAINEL tab: agents, diary, heavy lanes, open PRs, tokens of the day |
| `scripts/deepdeck-agents.sh` | The AGENTES tab: an fzf menu to open or resume an agent session |
| `scripts/deepdeck-guide.sh` | The GUIA pane next to nvim; it shows `docs/guia-nvim.txt` |
| `scripts/deepdeck-notify.sh` | The macOS notification of the Claude Code Notification hook |
| `docs/guia-nvim.txt` | The Neovim guide (Nvim basics + LazyVim). Format: `## SECTION` and `key \| what it does` |
| `Brewfile` | The Homebrew packages and fonts |

## Palette (Deepdeck soft)

| Role | Colour |
|---|---|
| Background | `#0e0e14` |
| Text | `#d8dae5` |
| Active (magenta) | `#e8457a` |
| Details (cyan) | `#4cc9d6` |
| Alerts (yellow) | `#e6c84c` |
| Dim and comments | `#878ca6` (5.8:1 on the background, WCAG AA) |

## Install

```sh
brew bundle --file Brewfile
stow -d stow -t ~ ghostty zellij nvim
```

The Zellij plugins (`zellij-autolock`, `zellij-attention`) are in `~/.config/zellij/plugins`.

## Keys

- Option+arrows: go to the next pane (also from nvim to the guide).
- Option+1..7: go to a tab.
- Option+g: show the focused pane on the full screen (it hides the guide), and back.

The first commit comes from the work environment of 17/11 (the old repository HenriqueMachine/AntaresOS, now
archived), without its history.
