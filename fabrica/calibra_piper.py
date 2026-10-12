#!/usr/bin/env python3
"""Mede R e P das vozes do PIPER com o texto REAL das specs da frota.

POR QUE ISTO EXISTE (12/10/2026). O `voz_piper` entrou em producao no mesmo dia
em que o edge-tts passou a dar 403 no runner, e a peca `labtreinamento-s013`
(`byriXB1gSg8`) foi ao ar narrada por ele. Ela saiu com o aviso certo — o `R` e o
`P` de `MODELO_VOZ` sao do edge-tts e NAO valem para o Piper — mas aviso nao e
calibracao: enquanto os numeros antigos ficam no lugar, o portao `duracao` e a
mira estao decidindo com a constante de OUTRA voz, que e o erro do 679/698.

**O QUE ESTE MODULO NAO E: nao e `calibra_voz.py`.** Aquele mede no material que
FOI AO AR, lendo o `.srt` do bucket, e existe justamente porque medir em
laboratorio com duas amostras sinteticas produziu vies de +6,6% a +18,0% em nove
vozes de nove (17/08). Aqui nao ha material no ar: ha UMA peca do Piper, com onze
cenas, e o Storage esta em 402.

Entao este modulo faz a unica coisa honesta disponivel: sintetiza em laboratorio,
mas com o **texto de producao** — as cenas das specs reais daquela voz, centenas
delas, com a distribuicao de tamanho de frase que o roteiro tem de verdade. O que
envenenou a medicao de 17/08 foi a AMOSTRA (duas frases), nao o laboratorio.

**OS CONFUNDIDORES, e eles nao saem do relato:**
  1. isto mede o SINTETIZADOR, nao a esteira. A duracao de cena no `.srt` sai do
     clipe montado; aqui sai do mp3. O intervalo de montagem (`GAP_CENA_S`) nao
     entra nem deve entrar, e segue medido em 0,300 s;
  2. o `length_scale` esta fixo em `voz_piper.LENGTH_SCALE`. Se alguem mexer
     nele, esta medicao vence por nada;
  3. a voz grega so existe em qualidade `low`. O ajuste dela vale, mas a
     comparacao de retencao entre canais carrega essa diferenca.

Uso:
    python3 fabrica/calibra_piper.py [--max-cenas 120] [--specs fabrica/specs]

Nao escreve em `ensaio.py`. Imprime o bloco pronto para colar, como o
`calibra_voz.py` faz — trocar constante de producao a partir de uma medicao de
laboratorio e decisao, nao efeito colateral de rodar um script.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import voz_piper as VP                                  # noqa: E402
from calibra_voz import ajusta                          # noqa: E402
from ensaio import MODELO_VOZ                           # noqa: E402
from narracao import frases                             # noqa: E402


def duracao_mp3(caminho: str) -> float | None:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", caminho],
                       capture_output=True, text=True, timeout=60)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def cenas_por_voz(dir_specs: str, max_cenas: int) -> dict:
    """Cenas de SHORT e de LONGO das specs reais, agrupadas pela voz do edge.

    Pega as duas listas porque o que se quer e a distribuicao de tamanho de
    frase, e o longo e onde vivem as frases compridas. Amostra deterministica
    (passo fixo sobre a lista ordenada), nunca aleatoria: medicao que muda de
    resultado a cada execucao nao serve para comparar com a proxima.
    """
    bruto: dict[str, list[tuple[str, str]]] = {}
    for caminho in sorted(glob.glob(os.path.join(dir_specs, "*.json"))):
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except Exception:                                # noqa: BLE001
            continue
        voz = sp.get("voz")
        if voz not in VP.VOZES:
            continue
        idioma = sp.get("idioma") or voz.split("-")[0]
        for c in list(sp.get("longo") or []) + list(sp.get("short") or []):
            nar = (c or {}).get("nar")
            if nar and len(nar) > 10:
                bruto.setdefault(voz, []).append((nar, idioma))
    fora = {}
    for voz, itens in bruto.items():
        if len(itens) > max_cenas:
            passo = len(itens) / max_cenas
            itens = [itens[int(i * passo)] for i in range(max_cenas)]
        fora[voz] = itens
    return fora


def mede(voz: str, itens: list, saida: str) -> tuple[list, list, list, int]:
    """(C, F, D, falhas) sintetizando cada cena e medindo o mp3."""
    C, F, D, falhas = [], [], [], 0
    for i, (nar, idioma) in enumerate(itens):
        alvo = os.path.join(saida, f"{i:04d}.mp3")
        if not VP.sintetiza(nar, voz, alvo):
            falhas += 1
            continue
        d = duracao_mp3(alvo)
        os.remove(alvo)
        # Silencio nao e leitura de zero: cena que nao sintetizou ou que
        # devolveu duracao absurda sai da amostra e vai contada em `falhas`.
        if not d or d <= 0.2:
            falhas += 1
            continue
        C.append(len(nar))
        F.append(len(frases(nar, idioma)))
        D.append(d)
    return C, F, D, falhas


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--specs", default=os.path.join(RAIZ, "fabrica", "specs"))
    p.add_argument("--max-cenas", type=int, default=120)
    p.add_argument("--tmp", default="/tmp/calibra-piper")
    args = p.parse_args()

    if not VP.disponivel():
        print("::error::piper-tts nao esta instalado — nada a medir", flush=True)
        return 2

    os.makedirs(args.tmp, exist_ok=True)
    amostra = cenas_por_voz(args.specs, args.max_cenas)
    if not amostra:
        print("::error::nenhuma spec com voz da frota", flush=True)
        return 2

    linhas = []
    for voz in sorted(amostra):
        itens = amostra[voz]
        C, F, D, falhas = mede(voz, itens, args.tmp)
        n = len(C)
        if n < 20:
            print(f"::warning::{voz}: so {n} cenas mediram ({falhas} falhas) — "
                  f"amostra pequena demais, NAO calibre com isto", flush=True)
            continue
        r = ajusta(C, F, D)
        if r is None:
            print(f"::warning::{voz}: ajuste degenerado em n={n}", flush=True)
            continue
        R, P = r
        R0, P0 = MODELO_VOZ.get(voz, (float("nan"), float("nan")))
        previsto = sum(c / R0 + f * P0 for c, f in zip(C, F))
        erro = (sum(D) / previsto - 1) * 100 if previsto else float("nan")
        modelo = VP.VOZES[voz][1]
        print(f"::notice::{voz} -> {modelo} | n={n} falhas={falhas} | "
              f"R edge {R0:.2f} -> piper {R:.2f} | P edge {P0:.3f} -> "
              f"piper {P:.3f} | a estimativa do edge erra {erro:+.1f}% "
              f"nesta voz", flush=True)
        linhas.append(f'    "{voz}": ({R:.2f}, {P:.3f}),   '
                      f'# PIPER {modelo}, n={n}')

    if linhas:
        print("\nR e P do PIPER, medidos. NAO colei em ensaio.MODELO_VOZ: a "
              "tabela e chaveada pela voz do EDGE e as duas convivem na frota "
              "(o Piper e fallback). Trocar exige decidir ANTES o que fazer "
              "quando o edge volta.\n")
        print("\n".join(linhas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
