# motion_web — o motion da fabrica renderizado por navegador

Prova de conceito de 05/10/2026, feita para responder a pergunta do dono sobre
Remotion. E a MESMA arquitetura do Remotion, sem a dependencia: o navegador
desenha cada quadro, o ffmpeg costura.

    NODE_PATH=/opt/node22/lib/node_modules node render.js      # 120 quadros .jpg
    cat frames/*.jpg | ffmpeg -f image2pipe -vcodec mjpeg -framerate 30 \
        -i pipe:0 -c:v libvpx -b:v 0 -crf 6 -qmin 0 -qmax 14 -auto-alt-ref 0 \
        -pix_fmt yuv420p -an -y file:cena-21.webm

`quadro.html` traz as contas de `fabrica.tempos_entrada`, `fabrica.ken_burns` e
`fabrica.filtro_camadas` reescritas em JavaScript, e o SVG das camadas sai de
`fabrica.svg_cena(cena, paleta, 1280, 720, camada=k)` sem uma letra de
diferenca. Com `DejaVu Sans` instalada, o quadro e o mesmo que o render produz.

## Tres coisas que custaram tentativa e ficam escritas

1. **O ffmpeg desta sessao e o do Playwright** (`/opt/pw-browsers/ffmpeg-1011/`),
   compilado com `--disable-everything`. Nao ha libx264, nem aac, nem muxer mp4,
   nem os filtros `overlay`/`zoompan`/`fade`. Da para VP8 em .webm, sem audio.
   Dizer "nao ha ffmpeg aqui" estava errado; dizer "ha ffmpeg" sem o resto
   tambem engana.
2. **Os quadros tem de ser JPEG, nao PNG.** O decoder de png nao foi compilado
   (`--enable-decoder=mjpeg` e so). PNG entra como "unknown codec".
3. **`-i -` nao resolve**: so os protocolos `pipe` e `file` existem. Use
   `-i pipe:0` e `-y file:saida.webm`.

## O que isto NAO e

Nao substitui `fabrica.render`. Um quadro por screenshot custa ~0,15 s; um longo
de 600 s a 30 fps sao 18.000 quadros, ~45 min de navegador contra 11 min de
ffmpeg para o pacote inteiro. Serve para o SHORT (30-45 s = ~1.350 quadros) e
para vitrine, nao para a esteira de 26 pacotes por dia.
