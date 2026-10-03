#!/usr/bin/env bash
# Baixa Montserrat e Playfair Display para fontes/ (que o .gitignore nao versiona).
#
# Dois caminhos porque os ambientes diferem: no runner do GitHub Actions o
# raw.githubusercontent responde; na sessao do agente ele devolve 403 e so o
# protocolo git passa pelo proxy. Tenta o barato, cai para o que sempre funciona.
set -euo pipefail
destino="${1:-fontes}"
mkdir -p "$destino"

raw_mont="https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
raw_play="https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf"

baixou=1
curl -sSLf --max-time 90 -o "$destino/Montserrat.ttf" "$raw_mont" 2>/dev/null &&
curl -sSLf --max-time 90 -o "$destino/Playfair-Italic.ttf" "$raw_play" 2>/dev/null || baixou=0

# `curl -f` nao protege contra um 403 que devolve corpo JSON com 200 no proxy,
# entao confere o que chegou de verdade antes de dar por feito.
if [ "$baixou" = 1 ] && file "$destino/Montserrat.ttf" | grep -qi "truetype\|font"; then
  echo "fontes: via raw"
else
  echo "fontes: raw indisponivel, usando sparse checkout"
  tmp=$(mktemp -d)
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/google/fonts "$tmp/gf" >/dev/null 2>&1
  git -C "$tmp/gf" sparse-checkout set ofl/montserrat ofl/playfairdisplay >/dev/null
  cp "$tmp/gf/ofl/montserrat/Montserrat[wght].ttf" "$destino/Montserrat.ttf"
  cp "$tmp/gf/ofl/playfairdisplay/PlayfairDisplay-Italic[wght].ttf" "$destino/Playfair-Italic.ttf"
  rm -rf "$tmp"
fi

python3 - "$destino" <<'PY'
import sys
from PIL import ImageFont
d = sys.argv[1]
for nome in ("Montserrat.ttf", "Playfair-Italic.ttf"):
    f = ImageFont.truetype(f"{d}/{nome}", 40)
    print(f"  {nome}: ok ({len(f.get_variation_names())} pesos)")
PY
