# O que mexe no resultado, em ordem de impacto por esforco

Levantado em 07/09/2026, depois do primeiro Reel produzido inteiro pelo pipeline
em nuvem. Cada item tem a fonte que o sustenta; onde a fonte primaria estava
bloqueada pelo proxy, isso esta dito.

## O primeiro Reel foi reprovado, e por que

O veredito do Pablo sobre a entrega de 07/09 foi curto: **"ficou pior dos videos
feito no Drift"**. Ele estava certo, e o motivo importa mais que o resultado.

O que eu acertei foi o que dava para medir: cor (medida pixel a pixel), fonte,
corpo, proporcao, duracao, estrutura de legenda. O que eu errei foi o que so
aparece assistindo:

| Nos Reels que ja estavam no ar | O que eu entreguei |
|---|---|
| O texto MUDA ao longo do video — o OCR achou cards distintos em t=0,5s / 9s / 13s / 21s / 25s / 30s / 34s | **um card estatico** pelos 33 segundos inteiros |
| Legenda queimada acompanhando a fala | nenhuma |
| Mockups de WhatsApp, cards de comparacao, cortes internos | nada disso |
| O video ocupa bem o quadro | encaixe pequeno, muito navy vazio |

A licao, que vale alem deste caso: **medir um frame nao e entender uma edicao.**
Eu reconstrui com precisao um instante da identidade e tratei isso como se fosse
a identidade inteira. Um card congelado por meio minuto e exatamente o que faz a
peca parecer amadora ao lado da referencia — e nenhuma das metricas que eu tinha
(cor certa, fonte certa, duracao na faixa) pega isso.

Por isso o item 1 desta lista nao e cosmetico. Ele e o conserto.

## 1. Legenda karaoke queimada em ASS — impacto altissimo, esforco baixo

O `faster-whisper` que ja roda no sandbox devolve `word_timestamps=True`. Falta
so gerar o `.ass` e queimar com o filtro que o ffmpeg ja tem:

    ffmpeg -i entrada.mp4 -vf "subtitles=legenda.ass" saida.mp4

Nao adote biblioteca: um gerador de ASS tem ~150 linhas e assim o estilo da
legenda fica sob a chave da marca, junto com o resto. O
[ai-video-captions](https://github.com/nicolaigaina/ai-video-captions) serve de
referencia de estilo (mesmo stack: faster-whisper + ffmpeg).

Duas armadilhas documentadas:

* O que performa em Reels **nao** e karaoke classico com `\k`. E **um evento ASS
  por palavra** (ou por grupo de 2-3), com `\t(...)` de escala/cor e `\bord`
  grosso. O `\k` varre a linha inteira e serve para musica.
* `\k` conta em centesimos de segundo e `\t` em milissegundos. `\k100` = 1s
  equivale a `\t(0,1000,...)`, nao a `\t(0,100,...)`. E `\k0` pode fazer o
  render falhar sem dizer por que.

Se os timestamps do faster-whisper derraparem, o WhisperX faz alinhamento
forcado por fonema e entrega precisao abaixo de 100 ms.

## 2. Agendador proprio, e o container do Instagram criado na hora — impacto alto, esforco baixo

Confirmado: a Content Publishing API do Instagram **nao agenda e nao salva
rascunho**. So existe container + publish. E o container **expira em 24 h**.

Entao o desenho correto nao e "criar o container antes e publicar depois". E:

    job no Supabase -> cron dispara 3-5 min antes do horario
    -> cria o container -> aguarda FINISHED -> publica

O limite diario tem que ser lido em `GET /<IG_ID>/content_publishing_limit`: a
documentacao da Meta e internamente inconsistente (aparecem 50/24h e 100/24h no
mesmo arquivo) e o numero "25" que circula em blogs nao esta na doc atual.

No **Facebook e diferente**: `scheduled_publish_time` existe desde a Graph API
2.3 e agenda de verdade — `published=false` + timestamp Unix, minimo ~10 min no
futuro. Duas limitacoes conhecidas do Reels de Pagina por API: capa customizada
nao e suportada, e musica/efeitos nativos nao entram por ferramenta de terceiro.

## 3. Trilha propria mixada no MP4 — impacto medio-alto, esforco baixo

Como nenhuma das duas plataformas aceita audio nativo via API, a trilha tem de
estar **dentro** do arquivo. Isso e uma escolha, nao um defeito: abre mao do
audio em alta em troca de publicar sem ninguem no celular.

Sobre as fontes: o Pixabay **nao tem API de musica** (a API cobre imagem e
video), mas a licenca e livre para uso comercial sem atribuicao. O Free Music
Archive desligou a API e proibe hotlink. O Uppbeat so da API no plano
Enterprise. O Jamendo tem API real e gratuita, mas boa parte do catalogo aberto
e Creative Commons **NC** — uso comercial exige filtrar licenca ou pagar.

Conclusao: curar 20-40 faixas do Pixabay uma vez, guardar no Drive com BPM e
mood no Supabase, e mixar com `amix` + `sidechaincompress` (a trilha cede sob a
voz). Sai mais barato e mais previsivel que integrar qualquer API.

## 4. Cortar silencio e cortar na batida — impacto medio, esforco baixo-medio

`silencedetect` do proprio ffmpeg tira as pausas mortas. Depois da legenda, e o
melhor ganho de ritmo por hora de trabalho.

## 5. Drift headless como camada de motion graphics — impacto alto, esforco alto

Aqui a correcao importante: **o Drift roda sem interface grafica.** O
`docs/MCP.md` do repo documenta `drift --headless`, que serve MCP por stdio ou
por HTTP (`--mcp-port`), sem editor aberto e sem token de sessao. Sao 17
toolboxes — inclusive `subtitles.generate_subtitles` (Whisper embutido),
deteccao de batida, deteccao de cena e `project.export_video`.

O que segura: o `docs/BUILDING.md` diz que **editar nao precisa de display, mas
renderizar e exportar ainda querem um contexto OpenGL 3.3**. Em servidor:

    QT_QPA_PLATFORM=xcb xvfb-run -a drift --headless --mcp-port 4731

`QT_QPA_PLATFORM=offscreen` **nao** resolve: sem `/dev/dri` o plugin nao cria o
contexto GL. Num sandbox so de CPU da para usar Mesa llvmpipe, com o custo de
velocidade que isso implica.

Dois riscos em aberto, e o segundo e o maior: a licenca e **GPLv3** (usar como
processo externo esta ok, linkar em codigo proprietario nao), e as fontes, os
emojis e os modelos de fala sao **addons baixados pelo Addon Manager, que e
GUI** — nao esta confirmado se da para instala-los headless. Sem addon nao ha
`generate_subtitles` nem texto estilizado, que sao justamente os motivos para
querer o Drift.

Provar numa branch isolada antes de por no caminho critico.

## O que foi descartado, e por que

| Opcao | Motivo |
|---|---|
| Remotion | minimo de US$ 100/mes no plano de automacao inviabiliza volume baixo |
| editly | projeto parado desde ~2022, instalacao quebrada |
| MoviePy como motor de legenda | `TextClip` e lento, com regressao de performance aberta |
| Shotstack / Creatomate | funcionam, mas sao pagos por minuto para fazer o que o ffmpeg ja faz aqui |
| Uppbeat / Free Music Archive | sem API utilizavel |
