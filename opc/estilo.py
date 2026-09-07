#!/usr/bin/env python3
"""A chave de estilo do O Proximo Cliente: uma verdade so, executavel.

O guia de estilo desta marca nasceu como documento escrito a mao, com as cores
digitadas no texto E digitadas de novo no comando de render. Duas verdades. O
`fabrica/estilo.py` deste mesmo repositorio ja tinha diagnosticado esse defeito
para o canal de YouTube, na frase que vale para ca tambem:

    "Um prompt com numero copiado envelhece calado — e envelhecer calado e o
     defeito que mais custou tempo neste repositorio."

Entao aqui a ordem se inverte: as constantes sao a fonte, e o guia em markdown e
GERADO a partir delas. Trocar o laranja da marca e mudar uma linha; o card, o
render e o guia mudam juntos ou nao mudam nenhum.

DE ONDE VEM CADA NUMERO. Nada aqui foi escolhido por gosto. Tudo saiu de medicao
pixel a pixel sobre os posts que ja estao no ar em @oproximocliente, em
07/09/2026:

* as cores, por filtro de matiz/saturacao sobre o card 1080x1350 do feed
  (o Reel reentregue em 720x1280 tem a cor deslocada pela compressao, entao a
  amostra veio do estatico, que e o arquivo limpo);
* a geometria, medindo onde a faixa navy deixa de dominar a linha no frame;
* a duracao, dos tres Reels baixados: 28,6s / 34,5s / 42,4s.

Uso:
    python3 opc/estilo.py            # imprime o guia em markdown
    python3 opc/estilo.py --json     # imprime a chave em JSON
"""
from __future__ import annotations

import argparse
import json

# ---------------------------------------------------------------------------
# PALETA — medida nos arquivos publicados, nao escolhida.
# ---------------------------------------------------------------------------
NAVY = "#0B1320"      # fundo; 314.568 px amostrados no card do feed
BRANCO = "#FFFFFF"    # setup: a premissa que a pessoa ja aceita
LARANJA = "#FF7A1B"   # o soco e a assinatura; nunca decorativo
CREME = "#FDF6E0"     # a palavra-chave, sempre em serifada italica
CINZA = "#ACB4C1"     # linha de apoio, cinza-azulado

# ---------------------------------------------------------------------------
# TIPOGRAFIA — a hierarquia e semantica, e essa e a regra que segura a marca.
#
# Branco = premissa aceita. Creme italico = o conceito. Laranja = o soco.
# Trocar a cor de um nivel troca o SIGNIFICADO da linha, nao a decoracao dela.
# ---------------------------------------------------------------------------
SANS_PESADA = "Montserrat-Black"          # setup e punchline, caixa alta
SANS_MEDIA = "Montserrat-Bold"            # linha de apoio, caixa alta
SERIF_ITALICA = "PlayfairDisplay-BoldItalic"  # a palavra-chave

CORPO_SETUP = 76
CORPO_APOIO = 54
CORPO_CHAVE = 96
CORPO_PUNCH = 72

# ---------------------------------------------------------------------------
# FORMATO — 9:16 na entrega. O Instagram reentrega em 720x1280 a ~0,9 Mbps,
# e e por isso que o corpo minimo e 54: abaixo disso o texto embola na
# recompressao, que e o arquivo que o espectador realmente ve.
# ---------------------------------------------------------------------------
LARGURA = 1080
ALTURA = 1920
FPS = 30

# Faixa de duracao medida nos tres Reels no ar. Os roteiros A1-A10 miram 25-40s,
# o que cai dentro dela — os dois numeros concordam, entao nenhum foi ajustado.
DUR_MIN_S = 28
DUR_MAX_S = 42

# Geometria do card. O video entra ENCAIXADO, nunca full-bleed: e o encaixe que
# cria a faixa navy onde o texto vive.
VIDEO_LARGURA = 880
VIDEO_TOPO = 660
Y_SETUP = 170
Y_APOIO = 270
Y_CHAVE = 380
Y_PUNCH = 510
Y_REGUA = 610
REGUA_LARGURA = 200
REGUA_ALTURA = 8

# ---------------------------------------------------------------------------
# LEGENDA QUEIMADA — o que faltava, e o motivo da primeira entrega ser reprovada.
#
# Os Reels da marca trocam de card ao longo do video (medido: cards distintos em
# t=0,5s / 9s / 13s / 21s / 25s / 30s / 34s) e levam legenda acompanhando a fala.
# Um card congelado por meio minuto tem a cor certa e o ritmo errado.
#
# O padrao que performa em Reels NAO e o karaoke classico do ASS (tag \k, que
# varre a linha inteira e serve para musica). E um grupo curto de palavras na
# tela com a palavra corrente destacada — por isso aqui e um evento por palavra,
# redesenhando o grupo, e nao \k.
# ---------------------------------------------------------------------------
LEGENDA_FONTE = "Montserrat-Black"
# O nome da FAMILIA, que e diferente do nome do arquivo — e essa diferenca ja
# custou um render. O `drawtext` carrega o .ttf direto e acerta o peso; o libass
# (que queima a legenda) casa por NOME DE FAMILIA no fontconfig. Sem
# `--update-name-table` no instancer, as duas instancias de Montserrat herdam o
# nome do default da variavel ("Montserrat Thin") e a legenda sai fina, com o
# arquivo certo no disco. Passa no terminal, nao passa no feed.
LEGENDA_FAMILIA = "Montserrat Black"
# 170. Os dois numeros anteriores (64 e 100) foram medidos errado: eu media a
# EXTENSAO DA BANDA de texto e chamava de tamanho da letra. Banda inclui varias
# linhas, entao o numero saia grande e o corpo derivado dele saia pequeno.
#
# A medida certa e a altura da CAIXA ALTA, por componentes conexos sobre a
# mascara de branco+laranja. Nos tres Reels no ar, normalizada para 1080 de
# largura (mediana por peca):
#
#     r_indic   118px      r_whats   80px      r_aluguel   51px
#
# e no meu Reel reprovado: 30px. Um terco do menor deles.
#
# A razao caixa-alta/corpo medida na propria peca reprovada e 30/64 = 0,47
# (nao os ~0,70 da metrica da fonte: a entrega passa por reencode do Instagram
# a 720 de largura e o contorno come parte). Mirando a mediana das tres
# referencias, 80px, o corpo e 80/0,47 = 170.
#
# Este numero NAO e para ser confiado. `opc/conferir.py` remede a caixa alta no
# mp4 pronto e recusa fora de 45-150px — foi exatamente por nao medir a saida
# que 64 e 100 passaram.
LEGENDA_CORPO = 170
LEGENDA_COR = BRANCO       # as palavras do grupo
LEGENDA_COR_ATIVA = LARANJA  # a palavra sendo dita agora
LEGENDA_CONTORNO = 6       # grosso: o Reel e reentregue comprimido, contorno fino some
LEGENDA_SOMBRA = 2
LEGENDA_PALAVRAS_POR_GRUPO = 3
# Onde termina a legenda, em fracao da altura. As linhas de base medidas nas
# tres referencias caem em 0,755-0,981 — legenda colada no rodape, que e onde
# ela nao briga com o rosto. O Reel reprovado tem as dela em 0,645-0,735: acima
# da faixa inteira da referencia, no meio do peito de quem fala.
LEGENDA_Y = 0.96

# ---------------------------------------------------------------------------
# MONTAGEM — o ritmo, que e o que separa um Reel de um cartaz com narracao.
#
# Este bloco existe porque a peca reprovada tinha cor certa, fonte certa,
# duracao certa e MESMO ASSIM foi reprovada duas vezes. O que faltava nao
# estava em nenhuma constante: o quadro nunca mudava. Medido, quadro a quadro,
# a cada 2 segundos:
#
#   | medida                    | r_indic | r_whats | r_aluguel | reprovado |
#   |---------------------------|---------|---------|-----------|-----------|
#   | cortes de cena            | 8/28,6s | 8/34,5s | 4/42,4s   | 2/33,1s   |
#   | um corte a cada           | 3,6s    | 4,3s    | 10,6s     | 16,5s     |
#   | fracao navy (min -> max)  | 3%->38% | 1%->37% | 17%->92%  | 35%->36%  |
#   | trechos sem rosto (b-roll)| 1 (~6s) | 0       | 2 (~6s)   | nenhum    |
#
# A coluna do reprovado e uma linha reta: 35-36% de navy do primeiro ao ultimo
# quadro, blocos navy sempre em 0,00-0,09 e 0,91-1,00, legenda sempre na mesma
# faixa. Trinta e tres segundos de um unico layout congelado.
#
# Dai as tres regras abaixo. Elas nao sao gosto: sao a media das referencias.
# ---------------------------------------------------------------------------
BLOCO_MIN_S = 4.0    # nenhum plano dura menos: pisca e cansa
BLOCO_MAX_S = 6.5    # nenhum plano dura mais: e onde o reprovado morreu
BROLL_MIN_S = 4.0    # o corte de apoio precisa respirar para nao virar flash
BROLL_FATIA = 0.22   # ~1/5 da peca sem rosto, como em r_indic e r_aluguel
CARTELA_FINAL_S = 2.0  # r_aluguel fecha em 92% de navy; a peca precisa de ponto final
# Piso de ritmo: 5, e nao 10. O 10 foi o meu primeiro chute e ele REPROVAVA o
# r_aluguel — que e a referencia de ouro, o Reel que o proprio COMO_PUBLICAR.txt
# manda publicar. Ele da 5,7 cortes/min. Quando a regua reprova a peca que
# funciona, o defeito esta na regua. O 5 ainda pega o reprovado, que deu 3,6.
CORTES_MIN_POR_MIN = 5

# O b-roll escurece para a legenda continuar legivel por cima dele. Medido no
# r_aluguel: o trecho sem rosto tem media de luminancia 18% menor que o trecho
# com a pessoa.
BROLL_ESCURECER = 0.82

# ---------------------------------------------------------------------------
# AUDIO — a narracao e o produto. Um Reel mudo nao e um Reel com defeito, e um
# arquivo errado.
#
# Isto virou constante porque uma entrega saiu sem som e nada no caminho
# reclamou: o `-map 0:a?` do ffmpeg tem uma interrogacao, que quer dizer "se
# existir". Quando a faixa se perde num passo intermediario, o `?` engole o
# problema e o render termina com codigo 0. A faixa medida nas tres referencias
# e no proprio reprovado e -17,1 a -16,7 dB de media; a janela abaixo e essa
# com folga dos dois lados.
# ---------------------------------------------------------------------------
AUDIO_MEAN_DB_MIN = -30.0
AUDIO_MEAN_DB_MAX = -8.0

# ---------------------------------------------------------------------------
# ENQUADRAMENTO — onde o rosto tem de cair.
#
# Isto existe porque a primeira entrega saiu com a cabeca cortada e nenhuma
# verificacao pegou. A faixa navy comeca em y=0 e vai ate `video_topo`; se o
# rosto do bruto comecar acima disso, a faixa passa por cima dele. No bruto do
# celular o rosto comeca em 0.201 da altura e a faixa vai ate 0.344 — cobria os
# 274px de cima da cabeca.
#
# O alvo saiu do r1, o mais apertado dos tres Reels no ar: rosto comecando em
# 0.364 da altura, logo abaixo da faixa. Os outros dois sao mais folgados
# (0.475 e 0.512); usar o mais apertado mantem o rosto o maior possivel sem
# encostar na faixa.
#
# A medida que pega o defeito e o detector de rosto: no v3 ele achou rosto em
# 1 de 12 quadros; no bruto, em 12 de 12. Cor, duracao e OCR do card passavam.
# ---------------------------------------------------------------------------
ROSTO_TOPO_ALVO = 0.365

# ---------------------------------------------------------------------------
# COPY — a estrutura de legenda dos posts atuais, em cinco blocos.
# ---------------------------------------------------------------------------
CTA = "Siga @oproximocliente que eu te ajudo a encontrar o seu."

HASHTAGS = [
    "#trafegopago", "#metaads", "#anuncios", "#pequenosnegocios",
    "#empreendedorismo", "#marketingdigital", "#clientes", "#whatsappbusiness",
]

BLOCOS_LEGENDA = [
    "Frase-choque curta, com numero concreto.",
    "A virada, comecando com 'Mas'.",
    "Explicacao em 2-3 frases, tom direto, com travessao.",
    "Consequencia dura, sem suavizar.",
    "CTA fixo + bloco de hashtags.",
]

# O perfil tem DUAS geracoes de legenda. A antiga (posts de 06/09 03h) usa emoji
# e "Clique no link da bio". Ela nao e um estilo alternativo — foi substituida.
# Fica registrada aqui para que ninguem a reintroduza achando que e variacao.
LEGENDA_PROIBIDA = ["emoji no corpo", "Clique no link da bio", "Clique no video"]

# ---------------------------------------------------------------------------
# PUBLICACAO
# ---------------------------------------------------------------------------
JANELA = "segunda-feira, 12h30 (almoco do dono de comercio)"
MAX_REELS_DIA = 1
VOLUME_AUDIO_EM_ALTA = "5-10%"  # so para entrar na distribuicao; a narracao manda


def chave() -> dict:
    """A chave inteira, para quem precisa dela como dado."""
    return {
        "paleta": {"navy": NAVY, "branco": BRANCO, "laranja": LARANJA,
                   "creme": CREME, "cinza": CINZA},
        "tipografia": {
            "setup": {"fonte": SANS_PESADA, "corpo": CORPO_SETUP, "cor": BRANCO},
            "apoio": {"fonte": SANS_MEDIA, "corpo": CORPO_APOIO, "cor": CINZA},
            "chave": {"fonte": SERIF_ITALICA, "corpo": CORPO_CHAVE, "cor": CREME},
            "punch": {"fonte": SANS_PESADA, "corpo": CORPO_PUNCH, "cor": LARANJA},
        },
        "formato": {"largura": LARGURA, "altura": ALTURA, "fps": FPS,
                    "dur_min_s": DUR_MIN_S, "dur_max_s": DUR_MAX_S},
        "geometria": {"video_largura": VIDEO_LARGURA, "video_topo": VIDEO_TOPO,
                      "rosto_topo_alvo": ROSTO_TOPO_ALVO,
                      "y_setup": Y_SETUP, "y_apoio": Y_APOIO, "y_chave": Y_CHAVE,
                      "y_punch": Y_PUNCH, "y_regua": Y_REGUA,
                      "regua_largura": REGUA_LARGURA, "regua_altura": REGUA_ALTURA},
        "legenda": {"fonte": LEGENDA_FONTE, "familia": LEGENDA_FAMILIA,
                    "corpo": LEGENDA_CORPO,
                    "cor": LEGENDA_COR, "cor_ativa": LEGENDA_COR_ATIVA,
                    "contorno": LEGENDA_CONTORNO, "sombra": LEGENDA_SOMBRA,
                    "palavras_por_grupo": LEGENDA_PALAVRAS_POR_GRUPO,
                    "y": LEGENDA_Y},
        "montagem": {"bloco_min_s": BLOCO_MIN_S, "bloco_max_s": BLOCO_MAX_S,
                     "broll_min_s": BROLL_MIN_S, "broll_fatia": BROLL_FATIA,
                     "cartela_final_s": CARTELA_FINAL_S,
                     "cortes_min_por_min": CORTES_MIN_POR_MIN,
                     "broll_escurecer": BROLL_ESCURECER},
        "audio": {"mean_db_min": AUDIO_MEAN_DB_MIN, "mean_db_max": AUDIO_MEAN_DB_MAX},
        "copy": {"cta": CTA, "hashtags": HASHTAGS, "blocos": BLOCOS_LEGENDA,
                 "proibido": LEGENDA_PROIBIDA},
        "publicacao": {"janela": JANELA, "max_reels_dia": MAX_REELS_DIA,
                       "volume_audio_em_alta": VOLUME_AUDIO_EM_ALTA},
    }


def guia() -> str:
    """O guia em markdown, GERADO da chave. Nao edite o .md: edite este arquivo."""
    k = chave()
    p, t, f, g, c, pb = (k["paleta"], k["tipografia"], k["formato"],
                         k["geometria"], k["copy"], k["publicacao"])
    linhas = [
        "# Guia de estilo — O Proximo Cliente",
        "",
        "> GERADO por `opc/estilo.py`. Nao edite este arquivo a mao: ele e",
        "> reescrito a cada geracao e a sua edicao se perde. Edite o modulo.",
        "",
        "Extraido por medicao dos posts publicados em @oproximocliente (07/09/2026).",
        "",
        "## Paleta",
        "",
        "| Uso | Hex |",
        "|---|---|",
        f"| Fundo (navy) | `{p['navy']}` |",
        f"| Setup (branco) | `{p['branco']}` |",
        f"| Soco / assinatura (laranja) | `{p['laranja']}` |",
        f"| Palavra-chave (creme) | `{p['creme']}` |",
        f"| Linha de apoio (cinza-azul) | `{p['cinza']}` |",
        "",
        "## Tipografia — hierarquia semantica",
        "",
        "Branco = a premissa que a pessoa ja aceita. Creme italico = o conceito.",
        "Laranja = o soco. A cor carrega o papel da linha, nao a decoracao.",
        "",
        "| Nivel | Fonte | Corpo | Cor |",
        "|---|---|---|---|",
    ]
    for nome, campo in [("Setup (CAIXA ALTA)", "setup"), ("Apoio (CAIXA ALTA)", "apoio"),
                        ("Palavra-chave (italica)", "chave"), ("Punchline (CAIXA ALTA)", "punch")]:
        d = t[campo]
        linhas.append(f"| {nome} | {d['fonte']} | {d['corpo']}px | `{d['cor']}` |")
    linhas += [
        "",
        "## Formato",
        "",
        f"- Entrega: {f['largura']}x{f['altura']}, {f['fps']} fps, H.264 + AAC",
        f"- Duracao: {f['dur_min_s']}-{f['dur_max_s']}s (medida nos Reels no ar)",
        f"- Video encaixado: {g['video_largura']}px de largura, topo em y={g['video_topo']}",
        "- O video NUNCA e full-bleed: o encaixe e o que cria a faixa navy do texto",
        "",
        "## Legenda — cinco blocos",
        "",
    ]
    linhas += [f"{i}. {b}" for i, b in enumerate(c["blocos"], 1)]
    linhas += [
        "",
        f"CTA fixo: \"{c['cta']}\"",
        "",
        "Hashtags: " + " ".join(c["hashtags"]),
        "",
        "NAO usar (geracao antiga, substituida): " + ", ".join(c["proibido"]),
        "",
        "## Publicacao",
        "",
        f"- Janela: {pb['janela']}",
        f"- Maximo de {pb['max_reels_dia']} Reel por dia",
        f"- Audio em alta a {pb['volume_audio_em_alta']}; a narracao continua sendo o que se ouve",
        "- Compartilhar no feed: sim, com o local da cidade marcado",
        "",
    ]
    return "\n".join(linhas)


def main() -> None:
    ap = argparse.ArgumentParser(description="Chave de estilo do O Proximo Cliente")
    ap.add_argument("--json", action="store_true", help="imprime a chave em JSON")
    args = ap.parse_args()
    print(json.dumps(chave(), indent=2, ensure_ascii=False) if args.json else guia())


if __name__ == "__main__":
    main()
