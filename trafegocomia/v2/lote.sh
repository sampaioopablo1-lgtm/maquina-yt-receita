#!/bin/bash
# uso: lote.sh semana.json pasta_saida
set -e
J="$1"; OUT="$2"; mkdir -p "$OUT"; T=$(mktemp -d)
N=$(python3 -c "import json;print(len(json.load(open('$J'))['videos']))")
for i in $(seq 0 $((N-1))); do
  python3 -c "import json;v=json.load(open('$J'))['videos'][$i];json.dump(v,open('$T/r.json','w'),ensure_ascii=False);print(v['slug'])" > $T/slug
  S=$(cat $T/slug); NN=$(printf %02d $((i+1)))
  python3 "$(dirname "$0")/produz.py" $T/r.json "$OUT/$NN-$S.mp4" "$OUT/$NN-$S-capa.png" | tail -1
  rm -rf "$OUT/$NN-$S"_trab "$OUT/_cena.html"
done
