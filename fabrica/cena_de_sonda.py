# -*- coding: utf-8 -*-
"""A CENA DE SONDA ERA UM SEGUNDO DONO DO CONTRATO DO RENDER.

MEDIDO em 22/10 as 02:5x, escrevendo o `kolejny-poziom-021`. Para montar as
cenas de `formula`, `erro`, `divisor`, `numero` e `comparar` eu li os NOMES dos
campos de cada layout **a mao**, abrindo o `kolejny-poziom-020` — item 3 da §10.
Fui conferir se havia instrumento para isso e encontrei o defeito no instrumento
que existia.

O `layouts_do_short.desenham()` SONDA o render para saber que layouts desenham —
e a cena que ele entrega a sonda era um dicionario ESCRITO A MAO. Isto e, a
pergunta *"que campos cada layout consome"* tinha DOIS donos: o render, e aquele
dicionario. **E eles ja divergiam em dezenove lugares:**

| | |
|---|---|
| campos no disco que a cena de sonda NAO tinha | **12** |
| campos na cena de sonda que NAO existem em cena nenhuma do disco | **2** (`erro`, `partes`) |
| campos distintos que as cenas do disco carregam | **21** |

A primeira contagem que eu fiz dava **17** ausentes, e ela incluia os campos de
COMPORTAMENTO e os de REDE, que este modulo deixa FORA de proposito e com o
efeito medido. O numero que vale e o que o `divergencia()` devolve, e o teste o
RECONFERE contra o disco em vez de confiar nesta prosa (753).

**E a divergencia nao era cosmetica — ela LEVANTA.** Com a cena antiga, o render
16:9 de `comparar` morre em `AttributeError: 'str' object has no attribute
'get'`, porque ali `esq`/`dir` eram strings e o layout le dicionario. O
`desenham()` envolve a sonda em `except Exception: continue`, logo o layout
**seria reportado como NAO desenhando** — e o portao `layout` chamaria CARTAO EM
BRANCO uma cena que desenha onze `<text>`.

**E e a promessa do proprio modulo que o quebra.** O docstring dele diz que
*"quando alguem ensinar o retrato a desenhar `numero`, este modulo passa a
aceitar `numero` sem ninguem editar nada"*. No dia em que o retrato aprender
`comparar`, a sonda levanta e o portao reprova a peca certa.

**Medido no 16:9, que ja desenha os cinco:** com a cena antiga, `erro`, `formula`
e `numero` saem com **UM** `<text>` em vez de quatro, seis e quatro — isto e,
*"desenha o fundo e esquece a cena"*, que e o defeito de 19/10 as 04:2x,
acontecendo DENTRO do instrumento escrito para o pegar.

**O CONSERTO E UM DONO: a cena sai do DISCO.** Os valores vem de cenas reais, e a
uniao de campos tambem — campo inventado a mao nao sobrevive, porque nao existe
em cena nenhuma. Varredura vazia **LEVANTA** em vez de devolver cena pobre, do
jeito que o `porta1` recusa janela curta: cena pobre faria a sonda confundir *"o
layout nao desenha"* com *"faltou o campo"*, que e exatamente o que o docstring
do `layouts_do_short` manda evitar.

**O QUE A MEDICAO NAO ACHOU, e vai dito em vez de inflado:** eu fui procurar
cartao em branco no LONGO e nao existe. Varridas as **134** specs de longo do
disco, **9.538 cenas, ZERO** com layout que o `svg_cena` nao desenhe, e **ZERO**
sem um campo de conteudo que o render consuma — o unico campo ausente no acervo e
o `trilho`, em 9.346 cenas da geracao anterior a 19/10, e ele e a faixa do
mobiliario e nao o conteudo. Logo nao existe aqui o buraco que existia no short
(uma cena em 2.750), e por isso NAO nasceu portao novo nenhum.
"""
import glob
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Campos que MUDAM o comportamento do render em vez de fornecer conteudo. Eles
# saem da cena de sonda, e o motivo e medido: com `sem_cap` a cena `titulo`
# perde a legenda e a sonda passaria a medir a ausencia dela em vez do layout.
# A lista e curta de proposito — toda exclucao a mao aqui reconstroi o dono que
# este modulo acabou de tirar, logo so entra campo cujo efeito esta MEDIDO.
COMPORTAMENTO = ("sem_cap", "trilho_atual")

# O render referencia URL de b-roll dentro do SVG; a sonda nao deve sair para a
# rede nem depender de arquivo. Medido: sem estes campos o `broll` segue
# desenhando (tres `<text>` no 16:9).
SEM_REDE = ("broll_url", "broll_q", "broll_credito")

_CACHE: dict = {}


def campos_do_disco(raiz: str = None) -> dict:
    """`{layout: {campo: valor REAL}}`, lido das cenas que existem no disco.

    O valor e o primeiro nao vazio encontrado, para que a sonda entregue ao
    render a MESMA forma que a producao entrega — foi a forma errada (`esq` como
    string) que fez o `comparar` levantar.
    """
    raiz = raiz or RAIZ
    if raiz in _CACHE:
        return {k: dict(v) for k, v in _CACHE[raiz].items()}
    vis: dict = {}
    for caminho in glob.glob(os.path.join(raiz, "fabrica", "specs", "*.json")):
        try:
            with open(caminho, encoding="utf-8") as f:
                sp = json.load(f)
        except Exception:
            continue
        for campo in ("short", "longo"):
            for c in (sp.get(campo) or []):
                if not isinstance(c, dict):
                    continue
                lay = c.get("layout") or "titulo"
                alvo = vis.setdefault(lay, {})
                for k, v in c.items():
                    if k in ("layout", "nar") or k in COMPORTAMENTO or k in SEM_REDE:
                        continue
                    if k not in alvo and v not in (None, "", [], {}):
                        alvo[k] = v
    if not vis:
        raise SystemExit(
            "cena_de_sonda: nenhuma cena no disco em %s — a sonda NAO roda com "
            "cena pobre, porque ai ela confunde 'o layout nao desenha' com "
            "'faltou o campo', que e o defeito que ela existe para evitar"
            % os.path.join(raiz, "fabrica", "specs")
        )
    _CACHE[raiz] = vis
    return {k: dict(v) for k, v in vis.items()}


def cena(layout: str, raiz: str = None) -> dict:
    """A cena com que se sonda `layout`: a UNIAO do disco, e os valores DELE.

    A uniao entra porque o criterio da sonda e *"saiu `<text>`?"*, e layout que
    nao recebe o campo dele responderia nao por falta de campo. Os valores do
    PROPRIO layout vencem a uniao, porque e a forma dele que o render le.
    """
    vis = campos_do_disco(raiz)
    c = {}
    for lay in sorted(vis):
        for k, v in vis[lay].items():
            c.setdefault(k, v)
    c.update(vis.get(layout) or {})
    c["layout"] = layout
    c["nar"] = "Narracao de sonda."
    return c


def divergencia(mao: dict, raiz: str = None) -> dict:
    """O que uma cena escrita A MAO tem a mais e a menos que o disco.

    Existe para que a medida que derrubou a cena antiga seja RECONFERIVEL em vez
    de ficar so na prosa (753): `inventados` sao campos que nao existem em cena
    nenhuma do disco, `ausentes` sao campos do disco que ela nao tinha.
    """
    vis = campos_do_disco(raiz)
    doc = set()
    for lay in vis:
        doc |= set(vis[lay])
    tem = {k for k in (mao or {}) if k not in ("layout", "nar")}
    return {"inventados": sorted(tem - doc), "ausentes": sorted(doc - tem),
            "no_disco": len(doc)}


def relato(raiz: str = None) -> str:
    vis = campos_do_disco(raiz)
    linhas = ["CENA DE SONDA, derivada do DISCO (%d layout(s)):" % len(vis)]
    for lay in sorted(vis):
        linhas.append("  %-10s %d campo(s): %s"
                      % (lay, len(vis[lay]), ", ".join(sorted(vis[lay]))))
    linhas.append("  os valores sao de cenas REAIS, e campo inventado a mao nao")
    linhas.append("  sobrevive porque nao existe em cena nenhuma do disco.")
    return "\n".join(linhas)


if __name__ == "__main__":
    print(relato())
