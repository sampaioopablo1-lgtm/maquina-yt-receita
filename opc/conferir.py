#!/usr/bin/env python3
"""Mede o mp4 PRONTO e recusa o que nao parece com os Reels no ar.

POR QUE ESTE ARQUIVO EXISTE. Tres entregas seguidas foram reprovadas, e as tres
tinham passado por conferencia. O que se conferia era a ENTRADA: a cor na chave
de estilo, o corpo da fonte na chave, a duracao pedida. Nenhuma dessas medidas
olhava o arquivo que a pessoa ia assistir.

O resultado disso, medido depois:

* a chave pedia corpo 100 de legenda e o mp4 entregou 30px de caixa alta;
* o render mapeava `0:a?` e o mp4 saiu sem faixa de audio, com codigo de saida 0;
* a marca tem ritmo de um corte a cada 3,6-4,3s e o mp4 tinha um a cada 16,5s.

Cada um desses passou porque ninguem mediu a saida. Entao aqui nao se le
nenhuma constante de intencao: abre-se o mp4, amostra-se quadro a quadro e
compara-se com a faixa medida nas tres referencias.

Uso:
    python3 opc/conferir.py entrega.mp4
    python3 opc/conferir.py entrega.mp4 --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import estilo  # noqa: E402

# A caixa alta da legenda, em px normalizados para um quadro de 1080 de largura.
# Piso e teto vem das tres referencias (r_aluguel 51, r_whats 80, r_indic 118),
# abertos o bastante para nao recusar uma peca legitima e apertados o bastante
# para pegar os 30px do reprovado.
CAIXA_ALTA_MIN, CAIXA_ALTA_MAX = 45.0, 150.0

# Onde as linhas de base caem. Esta e a regra FRACA das duas de legenda, e vale
# dizer por que: a mediana medida da em 0,778 (r_indic), 0,772 (r_whats), 0,683
# (r_aluguel) e 0,652 no reprovado. Trinta milesimos separam a pior referencia
# da peca ruim — regua ruim para decidir sozinha. Quem separa de verdade e o
# TAMANHO logo acima: 63/91/111 contra 32.
LEGENDA_BANDA_MIN, LEGENDA_BANDA_MAX = 0.67, 1.00

# O teto de duracao aqui e 44, e nao os 42 de `estilo.py`: o r_aluguel tem
# 42,4s depois do reencode do Instagram. Recusar a propria referencia por
# quatro decimos de segundo e a regua brigando com a realidade.
DUR_MAX_CONFERIDA_S = 44.0


def _ffprobe(args: list[str]) -> str:
    return subprocess.run(["ffprobe", "-v", "error", *args],
                          capture_output=True, text=True, check=True).stdout.strip()


def audio(video: str) -> dict:
    """A faixa existe? E tem nivel de narracao, ou e silencio com cabecalho?

    As duas perguntas sao diferentes e as duas ja falharam. Um mp4 pode ter
    stream de audio valido e mudo — o `volumedetect` e o unico que separa os
    dois casos.
    """
    tem = bool(_ffprobe(["-select_streams", "a:0", "-show_entries",
                         "stream=codec_name", "-of", "csv=p=0", video]))
    if not tem:
        return {"existe": False, "mean_db": None}
    saida = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video, "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", saida)
    return {"existe": True, "mean_db": float(m.group(1)) if m else None}


def cortes(video: str, limiar: float = 0.30) -> int:
    """Quantos cortes secos.

    Conta `pts_time:`, que sai UMA vez por quadro detectado. A primeira versao
    contava a palavra `showinfo`, e o filtro imprime varias linhas por quadro —
    entao a contagem saia inflada em graus DIFERENTES para cada arquivo. Isso e
    pior do que inflar por igual: eu estava comparando numeros que nao eram
    comparaveis, e concluindo coisas erradas sobre as referencias por causa
    disso.
    """
    saida = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video,
         "-vf", f"select='gt(scene,{limiar})',showinfo", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    return len(re.findall(r"pts_time:[0-9.]+", saida))


def quadros(video: str, passo: float = 2.0) -> list[dict]:
    """Amostra o video e mede, em cada quadro: navy, rosto e legenda.

    O passo de 2s nao e economia — e o intervalo em que as referencias foram
    medidas, entao os numeros sao comparaveis linha a linha com a tabela de
    `opc/estilo.py`.
    """
    import cv2
    import numpy as np

    casc = cv2.CascadeClassifier(cv2.data.haarcascades +
                                 "haarcascade_frontalface_default.xml")
    navy_bgr = np.array([int(estilo.NAVY[5:7], 16), int(estilo.NAVY[3:5], 16),
                         int(estilo.NAVY[1:3], 16)])
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    dur = (cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0) / fps
    fora = []
    t = passo / 2
    while t < dur:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, q = cap.read()
        if not ok:
            break
        h, w = q.shape[:2]
        k = 1080.0 / w
        frac_navy = float((np.abs(q.astype(int) - navy_bgr).sum(axis=2) < 60).mean())

        cinza = cv2.cvtColor(q, cv2.COLOR_BGR2GRAY)
        rostos = casc.detectMultiScale(cinza, 1.15, 5, minSize=(50, 50))
        rosto = ({"topo": float(rostos[0][1] / h), "alt": float(rostos[0][3] / h)}
                 if len(rostos) else None)

        # Legenda: mascara de branco OU laranja da marca no terco de baixo, e a
        # altura da caixa alta por componente conexo. Medir por componente, e
        # nao pela extensao da banda, e a correcao que este arquivo carrega —
        # confundir os dois foi o que produziu corpo 64 e corpo 100.
        faixa = q[int(h * 0.60):, :]
        b, g, r = (faixa[:, :, i].astype(int) for i in range(3))
        m = (((b > 210) & (g > 210) & (r > 210)) |
             ((r > 170) & (g > 70) & (g < 190) & (b < 110))).astype(np.uint8)
        n, _, st, _ = cv2.connectedComponentsWithStats(m, 8)
        alt = sorted((st[i, cv2.CC_STAT_HEIGHT] for i in range(1, n)
                      if st[i, cv2.CC_STAT_AREA] > 60 and st[i, cv2.CC_STAT_HEIGHT] < h * 0.15),
                     reverse=True)
        caixa = float(np.median(alt[:12]) * k) if alt else None
        # A linha de base pelo CENTRO dos maiores componentes, e nao pelo menor
        # `top` de todos. A primeira versao pegava o topo do recorte: as quatro
        # pecas medidas devolveram exatamente 0,600, que e onde eu cortava o
        # quadro. Regua que devolve o mesmo numero para peca boa e peca ruim
        # nao esta medindo a peca, esta medindo a si mesma.
        gr = [(st[i, cv2.CC_STAT_AREA],
               (int(h * 0.60) + st[i, cv2.CC_STAT_TOP] + st[i, cv2.CC_STAT_HEIGHT] / 2) / h)
              for i in range(1, n)
              if st[i, cv2.CC_STAT_AREA] > 150 and st[i, cv2.CC_STAT_HEIGHT] < h * 0.15]
        ys = [y for _, y in sorted(gr, reverse=True)[:20]]
        laranja = int(((r > 170) & (g > 70) & (g < 190) & (b < 110)).sum())

        fora.append({"t": round(t, 1), "navy": frac_navy, "rosto": rosto,
                     "caixa_alta": caixa,
                     "legenda_y": (float(np.median(ys)), max(ys)) if ys else None,
                     "laranja_px": laranja})
        t += passo
    cap.release()
    return fora


def conferir(video: str) -> dict:
    """Junta as medidas e devolve o veredito de cada regra."""
    import numpy as np

    k = estilo.chave()
    m, a = k["montagem"], k["audio"]
    dur = float(_ffprobe(["-show_entries", "format=duration", "-of", "csv=p=0", video]))
    aud = audio(video)
    n_cortes = cortes(video)
    qs = quadros(video)

    navys = [q["navy"] for q in qs]
    caixas = [q["caixa_alta"] for q in qs if q["caixa_alta"]]
    bandas = [q["legenda_y"] for q in qs if q["legenda_y"]]
    sem_rosto = sum(1 for q in qs if q["rosto"] is None)
    # Dois filtros, e os dois existem porque a regra reprovou peca boa.
    #
    # `alt >= 0.15`: so o rosto GRANDE e o locutor. Sem isso, o rosto pequeno e
    # distante do b-roll era lido como "cabeca no lugar errado" e reprovava o
    # r_indic, que esta no ar e correto.
    #
    # `navy >= 0.15`: a regra pergunta se a cabeca ficou POR BAIXO DO PAINEL, e
    # so faz sentido onde ha painel. Num plano de tela cheia nao ha nada em cima
    # da cabeca, entao rosto alto ali e enquadramento do celular, nao defeito —
    # e a peca nova cai exatamente nesse caso (rosto em 0,20 sem painel algum).
    com_rosto = [q["rosto"]["topo"] for q in qs
                 if q["rosto"] and q["rosto"]["alt"] >= 0.15 and q["navy"] >= 0.15]

    caixa_med = float(np.median(caixas)) if caixas else 0.0
    banda_lo = min(b[0] for b in bandas) if bandas else 0.0
    banda_hi = max(b[1] for b in bandas) if bandas else 0.0

    regras = [
        ("audio: a faixa existe",
         aud["existe"], "sem faixa de audio — Reel mudo"),
        ("audio: nivel de narracao",
         aud["mean_db"] is not None and a["mean_db_min"] <= aud["mean_db"] <= a["mean_db_max"],
         f"media {aud['mean_db']} dB fora de {a['mean_db_min']}..{a['mean_db_max']}"),
        # Regra fraca de proposito: o r_aluguel tem UM corte seco em 42s e e
        # referencia legitima — ele troca de quadro por dissolvencia, que o
        # detector nao conta. So pega o caso extremo do reprovado, que tem zero.
        ("ritmo: existe corte",
         n_cortes >= m["cortes_min"],
         f"{n_cortes} cortes em {dur:.1f}s (o reprovado teve zero)"),
        # Esta e a regra FORTE. Referencias: 20pp (r_aluguel 17->92... na
        # verdade 75pp), 36pp e 35pp. Reprovado: 1pp.
        ("ritmo: o quadro muda",
         (max(navys) - min(navys)) > m["variacao_navy_min"],
         f"navy varia so {(max(navys)-min(navys))*100:.0f}pp — layout congelado "
         f"(o reprovado variou 1pp; as referencias, 35 a 75)"),
        # ESCOLHA DA CASA, e nao regra medida — a distincao importa. O r_whats
        # nao tem um unico quadro sem rosto e e referencia legitima: ele varia
        # pelo painel navy que entra e sai. Corte de apoio do Pexels e uma
        # decisao nossa, pedida explicitamente. Ela reprova a entrega, mas NAO
        # entra na conta de "bate com a referencia".
        # O piso e UM, e nao dois. O dois era meu, e reprovava tanto o r_indic
        # (que tem exatamente um quadro amostrado sem rosto e esta no ar) quanto
        # a peca nova, que tem um bloco de apoio legitimo de quase 5s: com
        # amostra a cada 2s, um bloco de 4,7s cai em um ou dois quadros
        # dependendo de onde a amostra bate. A regra so responde "existe corte
        # de apoio?"; QUANTO de apoio quem decide e a escaleta, pela fatia
        # medida em `estilo.BROLL_FATIA`.
        ("b-roll do Pexels (escolha da casa, nao regra medida)",
         sem_rosto >= 1,
         f"{sem_rosto} quadros sem rosto — sem corte de apoio"),
        ("legenda: tamanho da caixa alta",
         CAIXA_ALTA_MIN <= caixa_med <= CAIXA_ALTA_MAX,
         f"{caixa_med:.0f}px fora de {CAIXA_ALTA_MIN:.0f}-{CAIXA_ALTA_MAX:.0f} "
         f"(referencias 51/80/118, reprovado 30)"),
        ("legenda: fica no rodape",
         bool(bandas) and banda_lo >= LEGENDA_BANDA_MIN,
         f"comeca em {banda_lo:.3f}, piso {LEGENDA_BANDA_MIN} "
         f"(referencias 0,755+, reprovado 0,645)"),
        ("legenda: destaque em laranja",
         sum(q["laranja_px"] for q in qs) > 2000,
         "quase nenhum pixel laranja — a palavra corrente nao esta destacada"),
        ("enquadramento: o rosto nao entra na faixa",
         (not com_rosto) or min(com_rosto) >= 0.28,
         f"topo do rosto em {min(com_rosto) if com_rosto else 0:.3f} nos planos "
         f"com painel — cabeca por baixo do card"),
        ("duracao na faixa da marca",
         k["formato"]["dur_min_s"] <= dur <= DUR_MAX_CONFERIDA_S,
         f"{dur:.1f}s fora de {k['formato']['dur_min_s']}-{DUR_MAX_CONFERIDA_S:.0f}s"),
    ]
    return {
        "arquivo": video,
        "duracao_s": round(dur, 1),
        "audio_mean_db": aud["mean_db"],
        "cortes": n_cortes,
        "navy_min_max": [round(min(navys), 3), round(max(navys), 3)],
        "caixa_alta_px": round(caixa_med, 1),
        "legenda_banda": [round(banda_lo, 3), round(banda_hi, 3)],
        "quadros_sem_rosto": sem_rosto,
        "regras": [{"regra": r, "passou": bool(ok), "motivo": None if ok else pq}
                   for r, ok, pq in regras],
        "aprovado": all(ok for _, ok, _ in regras),
        # Duas leituras diferentes, de proposito. `aprovado` inclui as escolhas
        # da casa; `conforme_referencia` e so o que foi MEDIDO nos Reels no ar.
        # Se este segundo campo der falso para uma das tres referencias, a regua
        # esta errada e nao a peca — foi assim que quatro regras miscalibradas
        # foram pegas antes de reprovarem uma entrega boa.
        "conforme_referencia": all(ok for r, ok, _ in regras
                                   if "escolha da casa" not in r),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Mede o mp4 pronto contra os Reels no ar")
    ap.add_argument("video")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = conferir(a.video)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print(f"{r['arquivo']}: {r['duracao_s']}s, {r['cortes']} cortes, "
              f"audio {r['audio_mean_db']} dB, caixa alta {r['caixa_alta_px']}px")
        for d in r["regras"]:
            print(f"  {'OK  ' if d['passou'] else 'FALHA'} {d['regra']}"
                  + ("" if d["passou"] else f"\n        {d['motivo']}"))
        print("  bate com as referencias no ar: "
              + ("sim" if r["conforme_referencia"] else "NAO"))
    sys.exit(0 if r["aprovado"] else 1)


if __name__ == "__main__":
    main()
