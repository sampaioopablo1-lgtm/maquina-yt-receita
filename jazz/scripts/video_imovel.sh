#!/usr/bin/env bash
# Vídeo de apresentação de UM imóvel, montado só com as fotos reais dele.
#
# O que isto é: cada quadro do vídeo é uma foto verdadeira do imóvel, com
# movimento lento de aproximação (Ken Burns) e fundido entre ambientes.
# O que isto NÃO é: tour virtual 360. Foto comum não vira esfera — quem
# "converte" inventa ~83% do que o comprador veria. Este vídeo preenche o
# campo de VÍDEO do anúncio; o campo de tour continua exigindo panorama
# capturado no imóvel.
#
# Por que roda no runner do GitHub e não numa Edge Function: precisa de
# ffmpeg de verdade (a mesma máquina que já produz os vídeos do YouTube), e
# o runner tem rede aberta para o CDN do Vista.
#
# Uso: SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... ./video_imovel.sh 40346
set -euo pipefail

CODIGO="${1:?uso: video_imovel.sh CODIGO}"
: "${SUPABASE_URL:?}" "${SUPABASE_SERVICE_ROLE_KEY:?}"

DIR="$(mktemp -d)"
trap 'rm -rf "$DIR"' EXIT

# 1) Fotos do imóvel, na ordem do Vista (a mesma que o XML emite).
curl -fsS "$SUPABASE_URL/rest/v1/feed_properties?codigo_original=eq.$CODIGO&select=dados_normalizados" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  | jq -r '.[0].dados_normalizados.fotos[]?' > "$DIR/urls.txt"

TOTAL=$(wc -l < "$DIR/urls.txt")
if [ "$TOTAL" -lt 5 ]; then
  echo "imóvel $CODIGO tem só $TOTAL fotos — mínimo 5 para um vídeo que preste" >&2
  exit 1
fi

# Teto de 30 fotos ≈ 90s de vídeo. Acima disso o vídeo cansa.
head -30 "$DIR/urls.txt" > "$DIR/sel.txt"

echo "baixando $(wc -l < "$DIR/sel.txt") fotos do imóvel $CODIGO..."
n=0
while read -r u; do
  n=$((n+1))
  curl -fsS --retry 3 -o "$DIR/$(printf 'f%03d.jpg' "$n")" "$u" &
done < "$DIR/sel.txt"
wait

# 2) Um segmento de 3s por foto: zoom lento alternado (par aproxima, ímpar
#    afasta), fundido de 0,3s nas pontas. 1280x720 — nenhuma foto do acervo
#    passa de 1280 de largura, então subir a resolução só inflaria bytes.
i=0
for f in "$DIR"/f*.jpg; do
  i=$((i+1))
  if [ $((i % 2)) -eq 0 ]; then
    Z="1+0.10*on/89"           # aproxima
  else
    Z="1.10-0.10*on/89"        # afasta
  fi
  ffmpeg -hide_banner -loglevel error -y -i "$f" -filter_complex \
    "scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,\
zoompan=z='$Z':d=90:x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':s=1280x720:fps=30,\
fade=t=in:st=0:d=0.3,fade=t=out:st=2.7:d=0.3,format=yuv420p" \
    -c:v libx264 -preset veryfast -crf 23 -t 3 "$DIR/seg$(printf '%03d' "$i").mp4"
done

for s in "$DIR"/seg*.mp4; do echo "file '$s'"; done > "$DIR/lista.txt"
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$DIR/lista.txt" \
  -c copy -movflags +faststart "$DIR/video.mp4"

TAM=$(stat -c%s "$DIR/video.mp4")
echo "vídeo pronto: $((TAM/1024/1024))MB"

# 3) Sobe para o bucket público. x-upsert: regenerar substitui, nunca duplica.
curl -fsS -X POST "$SUPABASE_URL/storage/v1/object/videos-imoveis/$CODIGO.mp4" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: video/mp4" -H "x-upsert: true" \
  --data-binary @"$DIR/video.mp4" > /dev/null

echo "publicado: $SUPABASE_URL/storage/v1/object/public/videos-imoveis/$CODIGO.mp4"
