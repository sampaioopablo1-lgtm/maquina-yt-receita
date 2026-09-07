#!/usr/bin/env bash
# As fontes da marca, reconstruidas do zero em qualquer maquina.
#
# O Google Fonts so publica Montserrat e Playfair como fontes VARIAVEIS. O
# drawtext do ffmpeg desenha a instancia padrao delas — Regular 400 — e nao o
# peso que a marca usa. O card sai parecido e errado, que e o pior modo de
# falha: ninguem repara no terminal, todo mundo repara no feed.
#
# Por isso aqui os pesos sao FIXADOS com o instancer do fonttools. Os nomes de
# saida sao exatamente os que `opc/estilo.py` declara — se voce mudar um nome
# la, mude aqui, senao o `resolver_fonte` levanta.
#
# Uso: bash opc/fontes.sh [destino]   (padrao: opc/fontes/)
set -euo pipefail

DEST="${1:-$(dirname "$0")/fontes}"
mkdir -p "$DEST"
cd "$DEST"

GF="https://raw.githubusercontent.com/google/fonts/main/ofl"

curl -fsSL -o _montserrat-var.ttf   "$GF/montserrat/Montserrat%5Bwght%5D.ttf"
curl -fsSL -o _playfair-italic.ttf  "$GF/playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf"

# `--update-name-table` NAO e opcional. Sem ele a instancia herda o nome do
# default da fonte variavel ("Montserrat Thin"), e ai o drawtext acerta (carrega
# o arquivo) enquanto o libass erra (casa por nome de familia no fontconfig): a
# legenda queimada sai fina com o arquivo certo no disco.
python3 -m fontTools.varLib.instancer _montserrat-var.ttf  wght=900 --update-name-table -o Montserrat-Black.ttf
python3 -m fontTools.varLib.instancer _montserrat-var.ttf  wght=700 --update-name-table -o Montserrat-Bold.ttf
python3 -m fontTools.varLib.instancer _playfair-italic.ttf wght=700 --update-name-table -o PlayfairDisplay-BoldItalic.ttf

# Confere o nome de familia resultante contra o que `opc/estilo.py` declara.
fc-query -f '%{family}\n' Montserrat-Black.ttf | grep -q "Montserrat Black" \
  || { echo "ERRO: Montserrat-Black.ttf nao expoe a familia 'Montserrat Black'"; exit 1; }

rm -f _montserrat-var.ttf _playfair-italic.ttf
ls -la ./*.ttf
