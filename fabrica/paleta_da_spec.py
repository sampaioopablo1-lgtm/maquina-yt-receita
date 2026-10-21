"""A paleta da spec contra a do DONO do canal — conferida, nao lembrada.

POR QUE ESTE MODULO EXISTE (20/10/2026, 00:3x). Eu escrevi a paleta do
`epomeno-epipedo-s071` **a mao**, de cabeca, e as NOVE chaves contradiziam a do
canal. O `CLAUDE.md` diz, em letra, desde 19/10: a identidade visual sai de
`fabrica/paleta_referencia.PALETA` / `temas_do_dono.paleta_do_canal`, **"nunca
escrita a mao"**. E os DEZ portoes baratos passaram LIMPOS com a paleta errada —
medido, nao suposto: o `identidade` confere outras coisas (trilha, faixa do
canal) e nao compara a paleta com a do dono.

**E o custo nao e estetico.** O pedido do dono em 19/10 foi exatamente este:
*"os videos publicados me parecem todos a mesma dinamica, imagens, formas,
estilo. Em todos os canais. Ajuste."* Peca com paleta inventada por mim e a
falha que ele reclamou, publicada com portao verde.

**POR QUE NAO E PORTAO, e o numero vem antes da decisao:** varridas as specs dos
tres canais vivos as 00:3x de 20/10, **252 CONTRADIZEM** a paleta do dono e
**23** sao compativeis (251 e 24 depois de eu consertar a `s071`, que era uma
delas). A maioria e a geracao anterior a 19/10, quando a paleta trocou — portao
aqui reprovaria o parque inteiro, que e o argumento pelo qual o `mira.py` tambem
nao e portao (ele dispararia 44 avisos e deixaria de avisar). **Quem reconfere o
numero e o `distribuicao()`, nao esta prosa** (753): o que o teste cobra e a
PROPRIEDADE — os que contradizem sao MAIORIA —, nao o inteiro. Logo isto
**informa** antes do render, com codigo de saida SEMPRE zero.

**E A PRIMEIRA CONTAGEM QUE EU FIZ ESTAVA INFLADA, do jeito que o 725 descreve:**
comparei os dicionarios com `==` e contei **255**. Tres delas so tinham MENOS
chaves, com todos os valores iguais — subconjunto nao e contradicao. A
propriedade certa e mais estreita: **chave presente na spec cujo valor
CONTRADIZ o dono**. Pego antes de relatar, porque detector que inventa achado e
pior que nao ter detector.

**A paleta NAO e recalculada aqui.** Ela vem de `temas_do_dono.paleta_do_canal`,
e o canal vem de `canal.da_spec` — os dois donos unicos. Copiar hex para dentro
deste arquivo criaria o terceiro dono da identidade visual, que e a assinatura
que congelou a legenda do short e parou a mira de conferir por seis pecas.
"""
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_SPECS = os.path.join(RAIZ, "fabrica", "specs")


def _dono(canal: str) -> dict:
    """A paleta do canal, pedida a quem e dono dela."""
    import temas_do_dono
    return temas_do_dono.paleta_do_canal(canal)


def _canal(spec: dict) -> str:
    import canal as mod_canal
    return mod_canal.da_spec(spec)


def conflitos(spec: dict) -> dict:
    """Chaves da paleta da spec cujo valor CONTRADIZ a do dono.

    Chave que a spec nao traz NAO entra: subconjunto nao e contradicao, e foi
    contar assim que inflou a minha primeira medicao de 252 para 255.
    """
    c = _canal(spec)
    try:
        d = _dono(c)
    except Exception:
        return {"canal": c, "tem_dono": False, "conflitos": {}}
    pal = spec.get("paleta") or {}
    fora = {k: {"dono": d[k], "spec": pal[k]}
            for k in pal if k in d and pal[k] != d[k]}
    return {"canal": c, "tem_dono": True, "conflitos": fora,
            "sem_paleta": not pal}


def distribuicao(dir_specs: str | None = None) -> dict:
    """Quantas specs dos canais VIVOS contradizem a paleta do dono.

    E esta contagem que diz que o lugar disto e o relato e nao o portao.
    """
    import temas_do_dono
    canais = tuple(temas_do_dono.TEMA_DO_CANAL)
    contradizem, compativeis, sem = [], [], []
    for p in sorted(glob.glob(os.path.join(dir_specs or DIR_SPECS, "*.json"))):
        nome = os.path.basename(p)[:-5]
        if not any(nome.startswith(c) for c in canais):
            continue
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        v = conflitos(sp)
        if v.get("sem_paleta"):
            sem.append(nome)
        elif v["conflitos"]:
            contradizem.append(nome)
        else:
            compativeis.append(nome)
    return {"contradizem": contradizem, "compativeis": compativeis,
            "sem_paleta": sem}


def relato(caminho=None, spec=None) -> str:
    """A MESMA convencao dos outros relatos: `(caminho, spec=None)`.

    Ela nasceu como `relato(spec)` aceitando "a spec OU o caminho dela", e isso
    criou DUAS convencoes para o mesmo nome dentro da mesma passada — o defeito
    do `exceto` de 20/10 as 11:3x, agora na assinatura do `relato`. Em 21/10 as
    20:4x isso cobrou: o despachante do rascunho decidia pelo NOME do parametro
    e chamava `relato(caminho, spec)` aqui, que levantava `takes 1 positional
    argument`. Nome de parametro nao e convencao; a ASSINATURA e.

    O primeiro posicional segue aceitando a spec inteira, para nao quebrar quem
    chamava `relato(sp)` — e isso vai dito em vez de suposto.
    """
    if isinstance(caminho, dict) and spec is None:
        spec = caminho
    elif spec is None:
        import rascunho
        spec = rascunho.spec_de(caminho, None)
    if isinstance(spec, str):
        spec = json.load(open(spec, encoding="utf-8"))
    v = conflitos(spec)
    nome = spec.get("pacote") or spec.get("slug") or "?"
    if not v["tem_dono"]:
        return ("PALETA de %s: canal %r nao tem tema do dono — nada a conferir."
                % (nome, v["canal"]))
    if v.get("sem_paleta"):
        return ("PALETA de %s: a spec nao declara paleta, logo o render usa o "
                "padrao. Isto NAO e conflito." % nome)
    if not v["conflitos"]:
        return ("PALETA de %s (%s): compativel com a do dono "
                "(`temas_do_dono.paleta_do_canal`)." % (nome, v["canal"]))
    linhas = ["PALETA de %s (%s): **%d chave(s) CONTRADIZEM a do dono**."
              % (nome, v["canal"], len(v["conflitos"]))]
    for k, par in sorted(v["conflitos"].items()):
        linhas.append("  %-6s dono %s | spec %s" % (k, par["dono"], par["spec"]))
    linhas.append("  a identidade visual sai de `temas_do_dono.paleta_do_canal` "
                  "e NUNCA se escreve a mao (CLAUDE.md, 19/10). Isto INFORMA — "
                  "os dez portoes baratos passam LIMPOS com paleta errada.")
    return "\n".join(linhas)


if __name__ == "__main__":
    for caminho in sys.argv[1:]:
        print(relato(json.load(open(caminho, encoding="utf-8"))))
    if not sys.argv[1:]:
        d = distribuicao()
        print("PALETA no acervo dos canais vivos: %d contradizem, %d compativeis,"
              " %d sem paleta." % (len(d["contradizem"]), len(d["compativeis"]),
                                   len(d["sem_paleta"])))
    sys.exit(0)
