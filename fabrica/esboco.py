#!/usr/bin/env python3
"""Emite o esqueleto de um `.build.py` ja dimensionado para o canal.

POR QUE, medido na noite de 25 para 26/08/2026.

Escrever uma spec a mao levou ~45 min, repartidos assim:

    pesquisa e duas fontes institucionais   ~15 min   irredutivel
    escrever a narracao                     ~15 min   irredutivel
    DIMENSIONAR (medir, acrescentar, remedir) ~10 min  <- `dimensiona.py`
    commit, render, conferir                 ~5 min   batchavel

Este arquivo ataca o que sobra do terceiro item: a ARITMETICA e a ESTRUTURA
que eu refazia do zero em cada spec — quantos capitulos cabem na faixa do
veredito, quantos segundos cada um precisa, e quantas cenas isso da NAQUELA
voz. Tudo isso e derivavel do `config/canais/<slug>.yaml` mais o veredito, e
derivar a mao foi exatamente o que fez as cinco specs da noite voltarem duas ou
tres vezes cada.

O que ele NAO faz: escrever texto. Ele emite os blocos vazios com o alvo de
cada capitulo anotado ao lado, e o texto continua sendo trabalho de quem
pesquisou. Um esqueleto que inventasse narracao seria pior que nenhum — a
pesquisa e a fonte dupla sao a parte que nao se automatiza aqui.

    python3 fabrica/esboco.py kolejny-poziom --veredito liberado > nova.build.py
"""

import argparse
import math
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import copy_md                                    # noqa: E402
from dimensiona import FAIXAS, FOLGA_CAP_S        # noqa: E402
from ensaio import MODELO_VOZ                     # noqa: E402


def config(slug):
    """Le o yaml do canal por regex, como o `publicar.idioma_do_canal` faz.

    Regex e nao PyYAML pelo mesmo motivo de la: isto tem de rodar em runner que
    nao instalou dependencia nenhuma.
    """
    caminho = os.path.join(RAIZ, "config", "canais", f"{slug}.yaml")
    if not os.path.exists(caminho):
        raise SystemExit(f"nao achei {caminho}")
    txt = open(caminho, encoding="utf-8").read()

    def campo(chave, padrao=""):
        m = re.search(rf'^\s*{chave}:\s*"?([^"\n#]+?)"?\s*(?:#.*)?$', txt, re.M)
        return m.group(1).strip() if m else padrao

    return {"nome": campo("nome"), "idioma": campo("idioma"),
            "voz": campo("voz_edge"), "trilha": campo("trilha", "Wholesome"),
            "estilo": campo("estilo_visual", "voxlite")}


def plano(voz, veredito, capitulos_desejados):
    """Quantos capitulos, de quantos segundos, e quantas cenas cada um."""
    r, p = MODELO_VOZ[voz]
    piso, _ = FAIXAS[veredito]
    alvo_cap = copy_md.MIN_CAP + FOLGA_CAP_S

    # O numero de capitulos e limitado pelo piso: nao cabe mais capitulo do que
    # (piso / alvo_cap), senao eles ficam curtos e o `copy_md` os engole.
    teto_caps = int(piso // alvo_cap)
    n_caps = min(capitulos_desejados, teto_caps) if capitulos_desejados else teto_caps
    seg_cap = piso / n_caps

    # Cena tipica desta frota: duas frases. Duracao = chars/r + 2p + 0,3 de
    # intervalo. Resolvendo para chars a partir de um alvo de ~9 s por cena.
    seg_cena = 9.0
    chars_cena = max(60, int((seg_cena - 2 * p - 0.3) * r))
    # ARREDONDA PARA CIMA, de proposito. Arredondar para baixo deixa o esboco
    # abaixo do piso — 11 capitulos de 7 cenas dao 693 s contra um piso de 720
    # — e devolve exatamente o laco de "medir, acrescentar, remedir" que este
    # arquivo existe para eliminar. Sobrar e barato: o `dimensiona.py` diz
    # quanto cortar numa passada.
    n_cenas_cap = max(4, math.ceil(seg_cap / seg_cena))
    return {"n_caps": n_caps, "seg_cap": seg_cap, "piso": piso,
            "n_cenas_cap": n_cenas_cap, "chars_cena": chars_cena,
            "seg_cena": seg_cena, "total_cenas": n_caps * n_cenas_cap}


CABECA = '''#!/usr/bin/env python3
"""Monta a spec {pacote}.

ALAVANCA ATACADA: {alavanca}

NUMERO DE PARTIDA (preencher com a consulta do canal, pacote a pacote):

    <pacote>   short   <views> views   <insc> insc   <pct>%

O QUE DEU CERTO:
O QUE NAO DEU:
O QUE MUDEI POR CAUSA DISSO:

As TRES condicoes do aprendizado 504, e as tres tem de valer juntas:
  1. o dinheiro E DO ESPECTADOR, em segunda pessoa
  2. e uma ESCOLHA que ele faz, nao um numero imposto de fora
  3. o video entrega a CONTA, nao so o fato

VEREDITO `{veredito}`: faixa a partir de {piso:.0f}s, e a alavanca B manda ir ao
PISO. Este esboco ja esta dimensionado para {n_caps} capitulos de ~{seg_cap:.0f}s.

OS NUMEROS, e as duas rotas institucionais
    rota 1
    rota 2

O QUE FICOU DE FORA, e o video diz isso em voz alta
    -
"""
import json

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {{"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def I(kicker, preco, nar):
    CENAS.append({{"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True}})


def L(kicker, itens, nar):
    CENAS.append({{"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True}})


def B(kicker, itens, alturas, nar):
    CENAS.append({{"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True}})


def C(kicker, sub, nar):
    CENAS.append({{"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True}})

'''

RODAPE = '''
# ---------------------------------------------------------------------------
# O SHORT: escolha, dinheiro do espectador, a conta — e aponta para o longo
# (aprendizado 493). Alvo de {short_min}-{short_teto:.0f}s previstos.
SHORT = [
    {{"layout": "titulo", "kicker": "", "sub": "",
     "nar": "", "sem_cap": True}},
    {{"layout": "cta", "kicker": "", "sub": "",
     "nar": "", "sem_cap": True}},
]

THUMB = {{"l1": "", "l2": ""}}

COPY = """# 

## TITULO


## DESCRICAO


## CAPITULOS
{{CAPITULOS}}

## COMENTARIO FIXADO


## HASHTAGS


## TAGS


## CONFIGURACAO DE STUDIO
- Idioma: {idioma} | Categoria: Educacao (27)
- Nao e conteudo para criancas
- Divulgacao de conteudo alterado ou sintetico: SIM (voz gerada por IA)
- Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ligado (duracao acima de oito minutos)

## MUSICA / LICENCA
{{TRILHA}}

## NOTA SOBRE FONTES


AVISO SOBRE OS NUMEROS — o que foi descartado e por que.
"""

SPEC = {{
    "slug": "{slug}",
    "pacote": "{pacote}",
    "idioma": "{idioma}",
    "voz": "{voz}",
    "trilha": "{trilha}",
    "paleta": {{"ink": "#1B3A5C", "c1": "#E4572E", "c2": "#F5B841", "bg": "#F4F1EA"}},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "{pacote}.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\\n")
    print(f"{{len(CENAS)}} cenas no longo, {{len(SHORT)}} no short -> {{destino}}")
'''


def proximo_numero(slug):
    import glob
    usados = []
    for p in glob.glob(os.path.join(RAIZ, "fabrica", "specs", f"{slug}-*.json")):
        m = re.search(r"-(\d{3})\.json$", p)
        if m:
            usados.append(int(m.group(1)))
    return max(usados, default=0) + 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--veredito", default="sem dado", choices=sorted(FAIXAS))
    ap.add_argument("--capitulos", type=int, default=0,
                    help="0 = o maximo que cabe no piso da faixa")
    ap.add_argument("--alavanca", default="A (conversao short -> inscrito)")
    a = ap.parse_args()

    cfg = config(a.slug)
    if cfg["voz"] not in MODELO_VOZ:
        raise SystemExit(f"voz {cfg['voz']!r} sem modelo medido em ensaio.MODELO_VOZ")
    pl = plano(cfg["voz"], a.veredito, a.capitulos)
    pacote = f"{a.slug}-{proximo_numero(a.slug):03d}"

    import prontidao
    teto_short = prontidao.SHORT_MAX_S / (1 + prontidao.MARGEM_SHORT)

    out = [CABECA.format(pacote=pacote, alavanca=a.alavanca, veredito=a.veredito,
                         piso=pl["piso"], n_caps=pl["n_caps"], seg_cap=pl["seg_cap"])]
    for i in range(1, pl["n_caps"] + 1):
        out.append(
            f'\n# {"-" * 60}\n'
            f'# CAPITULO {i} de {pl["n_caps"]} — alvo ~{pl["seg_cap"]:.0f}s, '
            f'~{pl["n_cenas_cap"]} cenas de ~{pl["chars_cena"]} caracteres\n'
            f'T("", "",\n'
            f'  "",\n'
            f'  cap="")\n'
            + "".join(f'T("", "",\n  "")\n' for _ in range(pl["n_cenas_cap"] - 1)))
    out.append(RODAPE.format(slug=a.slug, pacote=pacote, idioma=cfg["idioma"],
                             voz=cfg["voz"], trilha=cfg["trilha"],
                             short_min=int(prontidao.SHORT_MIN_S),
                             short_teto=teto_short))
    print("".join(out))

    print(f"\n# esboco de {pacote}: {pl['n_caps']} capitulos x ~{pl['seg_cap']:.0f}s "
          f"= {pl['piso']:.0f}s, ~{pl['total_cenas']} cenas de ~{pl['chars_cena']} "
          f"caracteres na voz {cfg['voz']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
