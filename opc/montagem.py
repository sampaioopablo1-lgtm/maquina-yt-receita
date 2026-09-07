#!/usr/bin/env python3
"""Monta o Reel em PLANOS, e nao num layout so para o video inteiro.

POR QUE ESTE ARQUIVO SUBSTITUI O CAMINHO ANTIGO. O `opc/render.py` produzia um
unico grafo de filtros valido do primeiro ao ultimo quadro: uma faixa navy fixa,
o video encaixado num lugar fixo, o texto trocando por `enable=between(t,...)`.
Isso da uma peca cuja fracao de navy varia UM PONTO PERCENTUAL em 33 segundos —
medido, e reprovado duas vezes. As referencias variam de 1% a 37% (r_whats) e de
17% a 92% (r_aluguel), porque nelas o quadro inteiro troca, e nao so as letras.

Nenhum parametro conserta isso. O que faltava era poder ter planos diferentes.

OS QUATRO PLANOS, e a medida de onde cada um saiu:

* `pessoa_card`  — painel navy em cima com o card, a pessoa embaixo.
                   Da ~34% de navy, que e o pico do r_whats (37%) e do
                   r_indic (38%).
* `pessoa_cheia` — a pessoa ocupando o quadro todo, sem painel.
                   Da ~1-3% de navy, que e o vale das mesmas duas pecas.
* `broll`        — imagem de apoio do Pexels, sem ninguem na tela, escurecida
                   para a legenda continuar legivel. O r_aluguel passa 7
                   quadros amostrados assim, em dois trechos de ~6s.
* `cartela`      — navy cheio com a punchline. O r_aluguel fecha em 92% de navy;
                   sem isso a peca acaba no meio de uma frase.

A NARRACAO NAO E CORTADA. Os planos trocam o video; o audio corre inteiro por
baixo, extraido uma vez do bruto. E por isso que o b-roll funciona: quem fala
continua falando enquanto sai da tela.

POR QUE RENDERIZA UM PLANO POR VEZ, e nao tudo num `filter_complex` so: o
sandbox tem 1 GB de RAM e um grafo com quatro entradas concorrentes ja levou
SIGKILL do OOM killer duas vezes neste projeto. Um plano por vez faz uma
alocacao do tamanho de um quadro final e concatena no fim.

Uso:
    python3 opc/montagem.py BRUTO.mov SAIDA.mp4 --de 12.5 --ate 46.0 \\
        --cards cards.json --legenda legenda.ass --janela 380 \\
        --broll apoio1.mp4 apoio2.mp4
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import estilo  # noqa: E402
import legenda as legenda_mod  # noqa: E402  (o `recortar`, para a legenda por plano)
import render  # noqa: E402  (reaproveita resolver_fonte/_escapar/_cor)


# `ultrafast`, e nao `veryfast`. Nao e pressa: e memoria. O `veryfast` mantem
# lookahead e varios quadros de referencia, e num cgroup de 1 GB isso poe a
# maquina para paginar — medido, o mesmo plano caiu para 0,9 quadro por segundo
# (velocidade 0,03x, tres minutos para cinco segundos de video). O `ultrafast`
# usa uma referencia so e sem lookahead.
#
# O custo e tamanho de arquivo, nao qualidade: o CRF continua 18, e o Instagram
# reentrega tudo em 720x1280 a menos de 1 Mbps de qualquer jeito.
PRESET = os.environ.get("OPC_PRESET", "ultrafast")


def _dur(caminho: str) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", caminho],
        capture_output=True, text=True, check=True).stdout.strip())


def plano(dur: float, n_cards: int, n_broll: int) -> list[dict]:
    """A escaleta: que plano ocupa cada trecho da peca.

    A regra de alternancia sai da medicao. As referencias nao seguem um padrao
    fixo, mas as tres respeitam tres coisas: nenhum plano passa de ~6,5s, o
    b-roll aparece em pedacos inteiros de 4s ou mais (nunca em flashes), e a
    peca abre com a pessoa e o card — que e onde a promessa e feita.

    A alternancia comeca em `pessoa_card` porque abrir no b-roll esconde quem
    fala, e as tres referencias abrem com o rosto na tela.

    Primeiro divide o tempo em blocos IGUAIS que caibam na faixa, e so depois
    decide o tipo de cada um. A ordem inversa (ir consumindo o tempo e decidir
    na hora) foi a primeira versao e produzia tres defeitos de uma vez: dois
    b-rolls consecutivos viravam um trecho de 10,5s sem ninguem na tela, a
    sobra final era absorvida num plano de 10s (teto e 6,5s) e a fatia de apoio
    ia a 32% em vez dos 22% medidos.
    """
    k = estilo.chave()["montagem"]
    fim_util = max(0.0, dur - k["cartela_final_s"])
    if fim_util <= 0:
        return []

    # Quantos blocos cabem com duracao dentro de [min, max]. Arredonda pelo
    # meio da faixa e corrige para as bordas — assim nenhum bloco estoura.
    meio = (k["bloco_min_s"] + k["bloco_max_s"]) / 2
    n = max(1, round(fim_util / meio))
    while n > 1 and fim_util / n < k["bloco_min_s"]:
        n -= 1
    while fim_util / n > k["bloco_max_s"]:
        n += 1
    d = fim_util / n

    # Quantos blocos viram b-roll, pela fatia medida. Eles ocupam posicoes
    # alternadas a partir da terceira: nunca dois seguidos (isso esconderia
    # quem fala por mais de 6,5s) e nunca a abertura (as tres referencias
    # abrem com o rosto na tela).
    n_apoio = 0
    if n_broll and d >= k["broll_min_s"]:
        n_apoio = min(int(round(n * k["broll_fatia"])), max(0, (n - 2 + 1) // 2))
    posicoes, p = set(), 2
    while len(posicoes) < n_apoio and p < n:
        posicoes.add(p)
        p += 2

    blocos, i_card, i_broll = [], 0, 0
    for i in range(n):
        b = {"de": round(i * d, 3), "ate": round((i + 1) * d, 3)}
        if i in posicoes:
            b["tipo"] = "broll"
            b["broll"] = i_broll % n_broll
            i_broll += 1
        elif i % 2 == 0 and n_cards:
            b["tipo"] = "pessoa_card"
            b["card"] = i_card % n_cards
            i_card += 1
        else:
            b["tipo"] = "pessoa_cheia"
        blocos.append(b)
    if k["cartela_final_s"] > 0 and dur > k["cartela_final_s"]:
        blocos.append({"tipo": "cartela", "de": round(fim_util, 3), "ate": round(dur, 3)})
    return blocos


def _texto_card(card: dict, entrada: str, saida: str) -> list[str]:
    """As linhas do card sobre um rotulo de filtro. Sem `enable`: o plano
    inteiro E a janela do card, entao a condicao de tempo some daqui — era ela
    que fazia o card parecer que trocava enquanto o quadro ficava parado."""
    k = estilo.chave()
    t, g = k["tipografia"], k["geometria"]
    partes, rotulo = [], entrada
    for nivel, y in [("setup", g["y_setup"]), ("apoio", g["y_apoio"]),
                     ("chave", g["y_chave"]), ("punch", g["y_punch"])]:
        txt = card.get(nivel)
        if not txt:
            continue
        d = t[nivel]
        prox = f"{saida}_{nivel}"
        partes.append(render._linha(d["fonte"], txt, d["cor"], d["corpo"], y,
                                    rotulo, prox))
        rotulo = prox
    if card.get("punch"):
        prox = f"{saida}_regua"
        partes.append(
            f"[{rotulo}]drawbox=x=(iw-{g['regua_largura']})/2:y={g['y_regua']}:"
            f"w={g['regua_largura']}:h={g['regua_altura']}:"
            f"color={render._cor(k['paleta']['laranja'])}:t=fill[{prox}]")
        rotulo = prox
    partes.append(f"[{rotulo}]null[{saida}]")
    return partes


def _queimar(gr: list[str] | str, legenda: str | None) -> tuple[list[str], str]:
    """Pendura a legenda no fim do grafo do plano e devolve o rotulo final.

    A legenda e queimada AQUI, e nao sobre a peca montada. Queimar no fim levou
    SIGKILL do OOM killer (`total-vm:1133724kB` num cgroup de 1 GB), porque o
    libass com corpo 170 mais o x264 sobre 30s de 1080x1920 nao cabem juntos.
    Cada plano tem 5s e cabe com folga — e cada quadro passa a levar um encode
    so em vez de dois.
    """
    partes = list(gr) if isinstance(gr, list) else [gr]
    if not legenda:
        return partes, "out"
    cam = legenda.replace("\\", "/").replace(":", r"\:")
    dirf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes")
    partes.append(f"[out]subtitles='{cam}':fontsdir='{dirf}'[leg]")
    return partes, "leg"


def comando_plano(b: dict, bruto: str, brolls: list[str], cards: list[dict],
                  janela_fonte: int, saida: str, offset: float,
                  legenda: str | None = None) -> list[str]:
    """O argv do ffmpeg de UM plano, sem audio (o audio vem inteiro no fim)."""
    k = estilo.chave()
    p, f, g, m = k["paleta"], k["formato"], k["geometria"], k["montagem"]
    d = b["ate"] - b["de"]
    navy = render._cor(p["navy"])

    if b["tipo"] == "cartela":
        # Cartela: navy cheio, gerado por `color`. Aqui a fonte sintetica e
        # segura porque ela e a UNICA entrada — o OOM que matou a primeira
        # versao vinha de combinar `color` infinito com um video por `overlay`.
        card = cards[-1] if cards else {}
        gr = ["[0:v]null[b0]"] + _texto_card(
            {"punch": card.get("punch") or estilo.CTA.split(" que ")[0],
             "chave": card.get("chave")}, "b0", "out")
        gr, rot = _queimar(gr, legenda)
        return ["ffmpeg", "-y", "-f", "lavfi", "-i",
                f"color=c={navy}:s={f['largura']}x{f['altura']}:r={f['fps']}:d={d:.3f}",
                "-filter_complex", ";".join(gr), "-map", f"[{rot}]", "-an",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-preset", PRESET, "-threads", "1", saida]

    if b["tipo"] == "broll":
        clipe = brolls[b["broll"]]
        # `scale` cobrindo os dois lados e depois `crop`: o clipe do Pexels vem
        # em proporcoes variadas e um `scale` simples deixaria barra preta.
        # `setpts=N/FRAME_RATE/TB` no fim NAO e enfeite. Com `-stream_loop`, o
        # ffmpeg reinicia os carimbos de tempo do clipe a cada volta; o filtro
        # `fps` ve o tempo ANDAR PARA TRAS e fica esperando um instante que
        # nunca chega. O sintoma foi exatamente esse: o plano parava em
        # `frame=136` (4,46s de 5,16s) e ficava ali ate ser morto, com o fps
        # caindo de 15 para 2,2. Reconstruir o carimbo a partir do numero do
        # quadro tira o loop da conta.
        gr = (f"[0:v]scale={f['largura']}:{f['altura']}:force_original_aspect_ratio=increase,"
              f"crop={f['largura']}:{f['altura']},"
              f"eq=brightness=-{(1-m['broll_escurecer'])*0.5:.3f}:saturation=0.9,"
              f"fps={f['fps']},setpts=N/FRAME_RATE/TB[out]")
        gr, rot = _queimar(gr, legenda)
        return ["ffmpeg", "-y", "-stream_loop", "-1", "-t", f"{d:.3f}",
                "-i", clipe, "-filter_complex", ";".join(gr), "-map", f"[{rot}]", "-an",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-preset", PRESET, "-threads", "1", saida]

    # Planos com a pessoa. Os dois recortam a MESMA janela do bruto — o que
    # muda e se ha painel navy por cima. Manter a janela igual e o que faz o
    # corte entre eles ler como corte de montagem, e nao como salto de camera.
    if b["tipo"] == "pessoa_card":
        alto = f["altura"] - g["video_topo"]
        gr = [(f"[0:v]scale={f['largura']}:-2,"
               f"crop={f['largura']}:{alto}:0:{max(0, janela_fonte)},"
               f"pad={f['largura']}:{f['altura']}:0:{g['video_topo']}:color={navy}[b0]")]
        gr += _texto_card(cards[b["card"]] if cards else {}, "b0", "out")
    else:
        # Cheia: o quadro todo e a pessoa. A janela sobe metade do painel para
        # a cabeca nao encostar no topo quando o card sai.
        gr = [(f"[0:v]scale={f['largura']}:-2,"
               f"crop={f['largura']}:{f['altura']}:0:"
               f"{max(0, janela_fonte - g['video_topo'] // 2)}[out]")]
    gr, rot = _queimar(gr, legenda)
    return ["ffmpeg", "-y", "-ss", f"{offset + b['de']:.3f}", "-t", f"{d:.3f}",
            "-i", bruto, "-filter_complex", ";".join(gr), "-map", f"[{rot}]", "-an",
            "-r", str(f["fps"]),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            "-preset", PRESET, "-threads", "1", saida]


def montar(bruto: str, saida: str, de: float, ate: float, cards: list[dict],
           brolls: list[str], legenda: str | None, janela_fonte: int,
           trabalho: str) -> list[dict]:
    """Renderiza plano a plano, concatena, devolve a narracao e queima a legenda."""
    k = estilo.chave()
    f = k["formato"]
    os.makedirs(trabalho, exist_ok=True)
    dur = ate - de
    escaleta = plano(dur, len(cards), len(brolls))

    texto_ass = open(legenda, encoding="utf-8").read() if legenda else None
    pedacos = []
    for i, b in enumerate(escaleta):
        alvo = os.path.join(trabalho, f"p{i:02d}.mp4")
        leg_i = None
        if texto_ass:
            # Um .ass por plano, com os tempos recuados para a janela dele.
            # Sem o recuo, o evento de t=12s nao apareceria num plano que
            # comeca a contar do zero.
            leg_i = os.path.join(trabalho, f"leg{i:02d}.ass")
            with open(leg_i, "w", encoding="utf-8") as fh:
                fh.write(legenda_mod.recortar(texto_ass, b["de"], b["ate"]))
        cmd = comando_plano(b, bruto, brolls, cards, janela_fonte, alvo, de, leg_i)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"plano {i} ({b['tipo']}) falhou:\n{r.stderr[-1500:]}")
        pedacos.append(alvo)
        b["arquivo"] = alvo

    lista = os.path.join(trabalho, "planos.txt")
    with open(lista, "w", encoding="utf-8") as fh:
        for p in pedacos:
            fh.write(f"file '{os.path.abspath(p)}'\n")
    mudo = os.path.join(trabalho, "mudo.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lista,
                    "-c", "copy", mudo], check=True, capture_output=True)

    # A narracao, inteira, do bruto. `-vn` de proposito: e a unica coisa que se
    # quer daqui, e pedir video junto so gastaria tempo.
    narr = os.path.join(trabalho, "narr.m4a")
    subprocess.run(["ffmpeg", "-y", "-ss", f"{de:.3f}", "-to", f"{ate:.3f}",
                    "-i", bruto, "-vn", "-c:a", "aac", "-b:a", "128k", narr],
                   check=True, capture_output=True)
    if not os.path.exists(narr) or os.path.getsize(narr) < 1024:
        raise RuntimeError(
            f"a narracao saiu vazia ({narr}). O bruto tem faixa de audio no "
            f"trecho {de}-{ate}s? Entregar mudo ja aconteceu uma vez: o "
            f"`-map 0:a?` do ffmpeg engole isso e termina com codigo 0.")

    # `-map 1:a` sem interrogacao, de proposito: se a faixa nao existir, o
    # ffmpeg TEM de falhar aqui e nao entregar um mp4 mudo em silencio. Era a
    # interrogacao do `-map 0:a?` que deixava passar.
    #
    # O video sai por COPIA: a legenda ja foi queimada plano a plano, entao
    # aqui nao ha reencode nenhum — e o que tirou este passe do OOM killer.
    cmd = ["ffmpeg", "-y", "-i", mudo, "-i", narr, "-map", "0:v", "-map", "1:a",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
           "-movflags", "+faststart", saida]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"passe final falhou:\n{r.stderr[-1500:]}")
    return escaleta


def main() -> None:
    ap = argparse.ArgumentParser(description="Monta o Reel em planos")
    ap.add_argument("bruto")
    ap.add_argument("saida")
    ap.add_argument("--de", type=float, required=True)
    ap.add_argument("--ate", type=float, required=True)
    ap.add_argument("--cards", help="JSON com [{setup, apoio, chave, punch}, ...]")
    ap.add_argument("--legenda", help=".ass a queimar (opc/legenda.py gera)")
    ap.add_argument("--janela", type=int, default=0,
                    help="linha da fonte onde comeca a janela (opc/enquadrar.py calcula)")
    ap.add_argument("--broll", nargs="*", default=[], help="clipes de apoio (Pexels)")
    ap.add_argument("--trabalho", default="/tmp/opc_planos")
    a = ap.parse_args()

    cards = json.load(open(a.cards, encoding="utf-8")) if a.cards else []
    for c in cards:
        render.conferir_largura(c.get("setup", ""), c.get("apoio", ""),
                                c.get("chave", ""), c.get("punch", ""))
    esc = montar(a.bruto, a.saida, a.de, a.ate, cards, a.broll, a.legenda,
                 a.janela, a.trabalho)
    print(f"{a.saida}: {len(esc)} planos")
    for b in esc:
        print(f"  {b['de']:5.1f}-{b['ate']:5.1f}s  {b['tipo']}")


if __name__ == "__main__":
    main()
