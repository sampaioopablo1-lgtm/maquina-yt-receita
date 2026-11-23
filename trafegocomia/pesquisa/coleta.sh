#!/bin/bash
# Roda no runner: busca anuncios ATIVOS por termo na Biblioteca de Anuncios
# e grava um JSON por termo. Nao publica nada.
set -uo pipefail
OUT=trafegocomia/pesquisa/bruto; mkdir -p "$OUT"
PAIS=$(jq -r .pais trafegocomia/pesquisa/buscas.json)
jq -r '.termos[]' trafegocomia/pesquisa/buscas.json | while read -r T; do
  F="$OUT/$(echo "$T" | iconv -f utf8 -t ascii//TRANSLIT | tr ' A-Z' '-a-z' | tr -cd 'a-z0-9-').json"
  echo "busca: $T -> $F"
  timeout 240 facebook-ad-library-cli search-ads \
     --query "$T" --country "$PAIS" --json > "$F" 2> "$F.err" || echo "::warning::falhou: $T"
  jq -r '"  anuncios: \(.count // 0)"' "$F" 2>/dev/null || true
  sleep 8
done
