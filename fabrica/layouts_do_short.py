# -*- coding: utf-8 -*-
"""O retrato do SHORT desenha QUATRO layouts, e os outros saem em branco.

MEDIDO em 19/10 as 19:1x, numa peca que eu publiquei QUARENTA MINUTOS antes.
O `epomeno-epipedo-s069` (`ZySLot-Cvo4`, no ar as 18:18:45Z) tem a cena 2 com
`layout: numero`, e o `fabrica.svg_cena_retrato` despacha so
`titulo`/`cta`, `item`, `lista` e `barras`. Tudo o mais **cai no ramo final e
volta como FUNDO VAZIO** — medido na propria spec:

| cena | layout | `<text>` no SVG | bytes |
|---|---|---|---|
| 0 | `titulo` | 2 | 615 |
| **1** | **`numero`** | **0** | **146** |
| 3 | `lista` | 5 | 1333 |
| 5 | `barras` | 5 | 1494 |

**E a classe do defeito esta escrita no `CLAUDE.md` desde 19/10 as 04:2x** — os
layouts de longo *"escritos e MORTOS"*, cena que *"caia no ramo final e saia como
fundo vazio. Sem erro, sem aviso: um cartao em branco no meio do video."* Lá o
render nao chamava o codigo; aqui eu chamei um layout que o render do SHORT nao
conhece. **A diferenca pratica e nenhuma: cartao em branco no ar, e nenhum portao
disse nada.**

**O TAMANHO VAI MEDIDO e ele e UM: de 2.750 cenas de short no disco, exatamente
UMA tem layout que o retrato nao desenha** — a que eu escrevi nesta hora. Logo
isto NAO e buraco do acervo, e e por isso que aqui o lugar certo e o PORTAO e nao
a suite: o argumento do `mira.py` (*"aviso que reprova 105 specs deixa de
avisar"*) nao se aplica a um aviso que reprova exatamente a peca quebrada.

**O CONJUNTO NAO E ESCRITO A MAO, e isso e deliberado:** `desenham()` SONDA o
proprio render — monta uma cena com todos os campos e pergunta se saiu `<text>`.
Lista de layouts cravada aqui seria um SEGUNDO dono do despacho, que e a
assinatura que congelou a legenda e matou os layouts de longo. Quando alguem
ensinar o retrato a desenhar `numero`, este modulo passa a aceitar `numero` **sem
ninguem editar nada**.
"""
import glob
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Uma cena com TODOS os campos que os layouts conhecidos consomem, para que a
# sonda nao confunda "o layout nao desenha" com "faltou o campo".
CENA_DE_SONDA = {
    "kicker": "Kicker", "sub": "Sub", "preco": "Preco",
    "nar": "Narracao de sonda.",
    "itens": ["Um", "Dois", "Tres"],
    "barras": [{"rotulo": "A", "valor": 3}, {"rotulo": "B", "valor": 7}],
    "valor": "42", "esq": "Esquerda", "dir": "Direita",
    "formula": "a = b / c", "erro": "#REF!", "partes": ["I", "II"],
}

PALETA_DE_SONDA = {
    "bg": "#101010", "ink": "#F0F0F0", "c1": "#CC3333", "c2": "#3333CC",
    "red": "#FF0000", "ok": "#00FF00", "panel": "#202020", "mut": "#808080",
    "acc": "#CC3333",
}


# A sonda varre as ~350 specs do disco e monta um SVG por candidato. Sem
# memoria isso roda a cada cena de cada spec, e o portao fica lento o bastante
# para ninguem o chamar — instrumento que nao se chama e a classe dos layouts
# mortos outra vez. A chave e a raiz, porque o teste aponta para copias.
_CACHE_CAND: dict = {}
_CACHE_DESENHAM: dict = {}


def candidatos(raiz: str = None) -> set:
    """Todo nome de layout que PODE aparecer: o disco mais os de longo.

    Sai do disco e do `layouts_longo.LAYOUTS` em vez de uma lista minha —
    layout novo entra na sonda sozinho, que e a forma do teste dos layouts de
    longo (a varredura sai de `LAYOUTS`, nao de uma lista escrita).
    """
    raiz = raiz or RAIZ
    if raiz in _CACHE_CAND:
        return set(_CACHE_CAND[raiz])
    nomes = set()
    for caminho in glob.glob(os.path.join(raiz, "fabrica", "specs", "*.json")):
        try:
            sp = json.load(open(caminho, encoding="utf-8"))
        except Exception:
            continue
        for campo in ("short", "longo"):
            for c in (sp.get(campo) or []):
                nomes.add(((c or {}).get("layout") or "titulo"))
    try:
        import layouts_longo as LL
        nomes |= set(LL.LAYOUTS)
    except Exception:
        pass
    _CACHE_CAND[raiz] = {n for n in nomes if n}
    return set(_CACHE_CAND[raiz])


def desenham(raiz: str = None) -> set:
    """Os layouts que o render do SHORT (9:16) de fato DESENHA.

    SONDA o render, nao uma lista: cena com todos os campos, e o layout conta
    como desenhado quando o SVG sai com ao menos um `<text>`. O criterio e o
    `<text>` porque o ramo final devolve so o retangulo do fundo — medido: 146
    bytes e zero `<text>`, contra 600 a 1.500 bytes e 2 a 5 nos que desenham.
    """
    import fabrica as F

    chave = raiz or RAIZ
    if chave in _CACHE_DESENHAM:
        return set(_CACHE_DESENHAM[chave])
    ok = set()
    for lay in candidatos(raiz):
        cena = dict(CENA_DE_SONDA)
        cena["layout"] = lay
        try:
            svg = F.svg_cena_retrato(cena, PALETA_DE_SONDA, 1080, 1920)
        except Exception:
            continue
        if "<text" in svg:
            ok.add(lay)
    _CACHE_DESENHAM[chave] = ok
    return set(ok)


def cenas_vazias(sp: dict, raiz: str = None) -> list:
    """As cenas de SHORT desta spec que sairiam como cartao em branco.

    Devolve `[(indice, layout), ...]`. Lista vazia quando toda cena desenha.
    """
    bons = desenham(raiz)
    fora = []
    for i, c in enumerate(sp.get("short") or []):
        lay = ((c or {}).get("layout") or "titulo")
        if lay not in bons:
            fora.append((i, lay))
    return fora


def avisos(sp: dict, raiz: str = None) -> list:
    """As mensagens para o portao `layout`, uma por cena em branco."""
    bons = sorted(desenham(raiz))
    return [
        f"cena {i} do SHORT tem layout {lay!r}, que o `svg_cena_retrato` NAO "
        f"desenha — ela sai como CARTAO EM BRANCO, sem erro e sem aviso "
        f"(medido no `epomeno-epipedo-s069`: 146 bytes e zero `<text>`). "
        f"O retrato desenha {bons}."
        for i, lay in cenas_vazias(sp, raiz)
    ]


def relato(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        sp = json.load(f)
    nome = sp.get("pacote") or os.path.basename(caminho)
    v = cenas_vazias(sp)
    if not v:
        return (f"LAYOUT DO SHORT de {nome}: todas as "
                f"{len(sp.get('short') or [])} cenas desenham.")
    return f"LAYOUT DO SHORT de {nome}:\n  >> " + "\n  >> ".join(avisos(sp))
