#!/usr/bin/env bash
# runechest-lib — shared helpers for the RuneChest scripts. Source it; do not run it.
# shellcheck disable=SC2034  # the variables are used by the scripts that source this file
# Agent identity (rune, colour, name) comes from ONE place: the vault note 11-Agentes/Identidade.md. In the terminal
# the rune is the RuneChest Runes bind-rune of assets/runes/codepoints.tsv (the Unicode rune is the fallback).

FOODBOT_ROOT=${FOODBOT_ROOT:-$HOME/Foodbot}
DD_VAULT=$FOODBOT_ROOT/obsidian-vault/knowledge
DD_IDENTITY=${DD_IDENTITY:-$DD_VAULT/11-Agentes/Identidade.md}
DD_CODEPOINTS=${DD_CODEPOINTS:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/assets/runes/codepoints.tsv}

# ${#name} must count letters, not bytes ("Völundr"): a UTF-8 locale.
case "${LC_ALL:-${LC_CTYPE:-${LANG:-}}}" in *UTF-8*|*utf8*) ;; *) export LC_ALL=en_US.UTF-8 ;; esac

# Palette
DD_M=$'\e[38;2;232;69;122m'; DD_C=$'\e[38;2;76;201;214m'; DD_Y=$'\e[38;2;230;200;76m'; DD_G=$'\e[38;2;95;215;160m'
DD_W=$'\e[38;2;216;218;229m'; DD_D=$'\e[38;2;135;140;166m'; DD_B=$'\e[1m'; DD_R=$'\e[0m'
DD_I=$'\e[3m'   # italic: Ghostty draws it with Monaspace Radon, so an agent name stands out

# "#rrggbb" -> ANSI truecolor foreground
dd_fg() {
    local h=${1#\#}
    [ ${#h} -eq 6 ] || { printf '%s' "$DD_W"; return; }
    printf '\e[38;2;%d;%d;%dm' "0x${h:0:2}" "0x${h:2:2}" "0x${h:4:2}"
}

# Prints "key<TAB>rune<TAB>#hex<TAB>name" for each agent of the identity table
# (| agente | runa | cor | camada | papel | nome |; an old table without "nome" gives the key as the name).
dd_identity() {
    [ -f "$DD_IDENTITY" ] || return 0
    awk -F'|' '/^\| *[a-z]+ *\| / && $2 !~ /agente/ {
        k=$2; e=$3; c=$4; n=$7; gsub(/^ +| +$/, "", k); gsub(/^ +| +$/, "", e); gsub(/^ +| +$/, "", c)
        gsub(/^ +| +$/, "", n); if (n == "") n = k
        if (c ~ /^#[0-9a-fA-F]{6}$/) print k "\t" e "\t" c "\t" n }' "$DD_IDENTITY"
}

# The bind-rune of a display name (codepoints.tsv: "Völundr<TAB>U+100004…"), empty when the table has no row.
dd_bindrune() {
    local cp
    [ -f "$DD_CODEPOINTS" ] || return 0
    cp=$(awk -F'\t' -v n="$1" '$1 == n { sub(/^U\+/, "", $2); print $2; exit }' "$DD_CODEPOINTS")
    [ -n "$cp" ] && printf '%b' "\\U$(printf '%08X' "0x$cp")"
}

# dd_who <name or key> -> sets DD_EMOJI (the rune), DD_NAME (the display name) and DD_COLOR (ANSI).
# Unknown name: a dot, the name as given, and white.
dd_who() {
    local key line bind
    key=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
    line=$(dd_identity | awk -F'\t' -v k="$key" '$1==k {print; exit}')
    if [ -n "$line" ]; then
        DD_NAME=$(cut -f4 <<<"$line")
        bind=$(dd_bindrune "$DD_NAME")
        DD_EMOJI=${bind:-$(cut -f2 <<<"$line")}
        DD_COLOR=$(dd_fg "$(cut -f3 <<<"$line")")
    else
        DD_EMOJI="·"
        DD_NAME=$1
        DD_COLOR=$DD_W
    fi
}
