#!/usr/bin/env python3
"""O esqueleto repete ENTRE canais, e o portao compara DENTRO de um.

Por que este modulo existe, e sao duas razoes, nao uma.

A PRIMEIRA e o item 3 da §10: toda conta que eu faco a mao vira um erro meu.
Eu venho escrevendo, no relato de cada rodada e no `CLAUDE.md`, frases como
"esqueleto inedito nas 116 formas da frota" e "a frota nao tinha nenhuma peca
de doze cenas" — e cada uma dessas frases saiu de um laco Python descartavel
escrito na hora, sobre o `glob` das specs. Conferido depois, os numeros que eu
escrevi estavam CERTOS (113 em 20:1x de 19/10 mais tres pecas da e 116 em
23:1x, mais tres = 119 hoje), logo o defeito nao e numero errado. O defeito e
que a pergunta era escrita a mao junto com o laco, e por isso eu so respondia
a pergunta que me ocorria digitar.

A SEGUNDA e a que apareceu na PRIMEIRA execucao deste modulo, e e dela que
sai o valor: a pergunta que nunca me ocorreu digitar e a do DONO. Palavras
dele em 19/10: "os videos publicados me parecem todos a mesma dinamica,
imagens, formas, estilo. EM TODOS OS CANAIS." O "em todos os canais" e uma
dimensao que o portao `variedade` NAO PODE ver: o `_especs_do_canal` dele
filtra `slug == slug`, logo ele conta esqueleto repetido DENTRO do canal e e
cego para forma que atravessa canal. Medido no disco:

    | | |
    |---|---|
    | specs com short | 366 |
    | formas DISTINTAS | 119 |
    | formas presentes em MAIS DE UM canal | 34 |
    | pecas nessas formas | 271 = 74% |
    | a mais repetida, `titulo-titulo-titulo-titulo-cta` | 82 pecas, ONZE canais |

Nos tres canais VIVOS o quadro nao se dissolve: 276 pecas, 106 formas, 26
atravessando canal e 186 pecas (67%) nelas, com a mesma forma no topo (58
pecas, os tres canais). Isto e o 762 numa dimensao nova — la eu concentrei
producao num canal sem ver; aqui a FORMA atravessa os canais sem ninguem
contar.

O que isto NAO afirma: que forma compartilhada seja defeito por si. Peca de
cinco cenas tem poucas sequencias possiveis, e `titulo-...-cta` e a moldura de
todas elas. O que esta medido e a NEGACAO da leitura confortavel: nao se pode
dizer "o esqueleto esta variado" olhando o aviso do portao, porque ele mede
outra coisa.

NAO E PORTAO, pelo argumento do `mira.py`: ele reprovaria 271 specs, que sao
acervo e nao producao. Aviso que reprova 271 vezes deixa de avisar. O codigo
de saida e SEMPRE zero.

E a ASSINATURA sai de `variedade.esqueleto`, que e o dono dela desde que o
portao existe. Reescrever o `"-".join(...)` aqui criaria o segundo dono da
mesma regra — a assinatura que congelou a legenda, parou a mira de conferir
por seis pecas e pos job inventado na serie. Ha teste por AST cobrando isso.
"""
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import variedade as V  # noqa: E402  — DONO da assinatura do esqueleto

DIR_SPECS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specs")

# Os tres canais da frota. Lista DECLARADA e nao derivada, porque "vivo" e
# estado do negocio e nao propriedade do disco: canal parado continua tendo
# spec. Ela existe para separar ACERVO de PRODUCAO, que e a licao do 762 —
# acervo dilui rodada.
CANAIS_VIVOS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")


def _canal_da_spec(d: dict) -> str:
    """O canal de uma spec, delegado ao dono UNICO (`canal.da_spec`)."""
    import canal
    return canal.da_spec(d)


def varre(dir_specs: str = None) -> list[dict]:
    """Toda spec do disco que tem short, com canal, contagem e esqueleto.

    Levanta se nao achar nenhuma: varredura vazia que devolve lista vazia faz
    todo teste passar por vacuidade, que e o defeito do 743 em forma de glob.
    """
    dir_specs = dir_specs or DIR_SPECS
    saida = []
    for f in sorted(glob.glob(os.path.join(dir_specs, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        short = d.get("short") or []
        if not short:
            continue
        saida.append({
            "arquivo": os.path.basename(f),
            "canal": _canal_da_spec(d),
            "cenas": len(short),
            "esqueleto": V.esqueleto(short),
        })
    if not saida:
        raise RuntimeError(
            f"AUSENCIA DE LEITURA: nenhuma spec com short em {dir_specs}. "
            "Varredura vazia nao e 'frota sem esqueleto' — e instrumento sem "
            "dado, e devolver zero aqui faria todo teste passar por vacuidade."
        )
    return saida


def quadro(pecas: list[dict] = None, so_vivos: bool = False) -> dict:
    """As contagens que eu vinha escrevendo a mao, todas de uma vez."""
    pecas = pecas if pecas is not None else varre()
    if so_vivos:
        pecas = [p for p in pecas if p["canal"] in CANAIS_VIVOS]
    canais = collections.defaultdict(set)
    formas = collections.Counter()
    por_n = collections.Counter()
    for p in pecas:
        formas[p["esqueleto"]] += 1
        canais[p["esqueleto"]].add(p["canal"])
        por_n[p["cenas"]] += 1
    atravessam = {e for e, s in canais.items() if len(s) > 1}
    n_atravessadas = sum(formas[e] for e in atravessam)
    return {
        "pecas": len(pecas),
        "formas": len(formas),
        "formas_que_atravessam": len(atravessam),
        "pecas_em_forma_que_atravessa": n_atravessadas,
        "fracao_atravessada": (n_atravessadas / len(pecas)) if pecas else 0.0,
        "por_contagem_de_cena": dict(sorted(por_n.items())),
        "canais_da_forma": {e: sorted(s) for e, s in canais.items()},
        "contagem_da_forma": dict(formas),
    }


def cegas_para_o_portao(pecas: list[dict] = None) -> dict:
    """As formas que atravessam canal e que o portao `variedade` NAO PODE ver.

    E este o numero que importa, e ele e mais agudo que a fracao: o portao
    avisa a partir de `variedade.ESQUELETO_AVISA_EM` pecas iguais DENTRO de um
    canal, logo forma que aparece uma vez em cada de oito canais nunca o faz
    disparar. Medido no disco: das 34 formas que atravessam canal, **33 sao
    invisiveis** ao portao, e elas levam 189 pecas.

    O limiar e LIDO de `variedade.ESQUELETO_AVISA_EM` e nao copiado — seria o
    segundo dono do mesmo numero, que e a assinatura da semana. Se alguem
    baixar o limiar do portao, este instrumento acompanha sozinho.
    """
    pecas = pecas if pecas is not None else varre()
    q = quadro(pecas)
    cegas, vistas = [], []
    for esq, canais in q["canais_da_forma"].items():
        if len(canais) < 2:
            continue
        por = collections.Counter(
            p["canal"] for p in pecas if p["esqueleto"] == esq)
        (cegas if max(por.values()) < V.ESQUELETO_AVISA_EM
         else vistas).append(esq)
    return {
        "limiar_do_portao": V.ESQUELETO_AVISA_EM,
        "atravessam": len(cegas) + len(vistas),
        "cegas": sorted(cegas),
        "vistas_por_acidente": sorted(vistas),
        "pecas_cegas": sum(q["contagem_da_forma"][e] for e in cegas),
    }


def novidade(esq: str, cenas: int, pecas: list[dict] = None,
             exceto: str = "") -> dict:
    """Esta forma e nova? E este TAMANHO? — a frase do relato, derivada.

    Responde as duas perguntas que eu escrevia a mao em cada rodada, e a
    TERCEIRA que eu nunca escrevia: em quantos CANAIS esta forma ja vive.

    `exceto` e o nome do arquivo da propria peca, e ele NAO e conveniencia: a
    spec desta rodada ja esta no disco quando eu pergunto, logo sem ele
    "inedito" nunca pode ser verdade e o relato diz "JA EXISTE: 1 exemplar"
    de uma peca que e o proprio unico exemplar. O `variedade._especs_do_canal`
    carrega o mesmo parametro pela mesma razao, e foi dele que eu copiei a
    forma depois de a primeira execucao daqui mostrar o defeito.
    """
    pecas = pecas if pecas is not None else varre()
    if exceto:
        pecas = [p for p in pecas if p["arquivo"] != exceto]
    q = quadro(pecas)
    iguais = q["contagem_da_forma"].get(esq, 0)
    canais = q["canais_da_forma"].get(esq, [])
    return {
        "esqueleto": esq,
        "cenas": cenas,
        "formas_na_frota": q["formas"],
        "forma_inedita": iguais == 0,
        "exemplares_da_forma": iguais,
        "canais_da_forma": canais,
        "exemplares_do_tamanho": q["por_contagem_de_cena"].get(cenas, 0),
        "tamanho_inedito": q["por_contagem_de_cena"].get(cenas, 0) == 0,
        "contagens_existentes": sorted(q["por_contagem_de_cena"]),
    }


def _frase_da_novidade(n: dict) -> str:
    if n["forma_inedita"]:
        p = (f"esqueleto INEDITO nas {n['formas_na_frota']} formas de short "
             f"da frota")
    else:
        p = (f"esqueleto JA EXISTE: {n['exemplares_da_forma']} exemplar(es), "
             f"em {len(n['canais_da_forma'])} canal(is) "
             f"({', '.join(n['canais_da_forma'])})")
    if n["tamanho_inedito"]:
        t = (f"e o TAMANHO de {n['cenas']} cenas e inedito — as contagens "
             f"existentes sao {n['contagens_existentes']}")
    else:
        t = (f"e o tamanho de {n['cenas']} cenas tem "
             f"{n['exemplares_do_tamanho']} exemplar(es)")
    return f"  {p},\n  {t}."


def relato(spec_ou_caminho=None) -> str:
    pecas = varre()
    q = quadro(pecas)
    qv = quadro(pecas, so_vivos=True)
    L = ["ESQUELETO ENTRE CANAIS — o que o portao `variedade` nao ve"]
    for rot, x in (("acervo", q), ("canais VIVOS", qv)):
        L.append(
            f"  {rot}: {x['pecas']} pecas, {x['formas']} formas; "
            f"{x['formas_que_atravessam']} atravessam canal e levam "
            f"{x['pecas_em_forma_que_atravessa']} pecas "
            f"({100 * x['fracao_atravessada']:.0f}%)"
        )
    topo = sorted(q["contagem_da_forma"].items(),
                  key=lambda kv: -kv[1])[:3]
    for e, n in topo:
        c = q["canais_da_forma"][e]
        L.append(f"   {n:3d}x em {len(c):2d} canal(is)  {e}")
    if spec_ou_caminho is not None:
        d = spec_ou_caminho
        if isinstance(d, str):
            d = json.load(open(d, encoding="utf-8"))
        short = d.get("short") or []
        if short:
            L.append("")
            L.append(f"desta peca ({d.get('pacote', '?')}):")
            exceto = (os.path.basename(spec_ou_caminho)
                      if isinstance(spec_ou_caminho, str) else "")
            L.append(_frase_da_novidade(
                novidade(V.esqueleto(short), len(short), pecas, exceto)))
    c = cegas_para_o_portao(pecas)
    L.append("")
    L.append(
        f"  das {c['atravessam']} formas que atravessam canal, "
        f"{len(c['cegas'])} sao INVISIVEIS ao portao (ele avisa a partir de "
        f"{c['limiar_do_portao']} iguais DENTRO de um canal) e levam "
        f"{c['pecas_cegas']} pecas"
    )
    L.append("")
    L.append("  o portao `variedade` compara contra o MESMO canal (o")
    L.append("  `_especs_do_canal` filtra pelo slug), logo forma que")
    L.append("  atravessa canal e invisivel para ele. Isto NOMEIA e NAO")
    L.append("  reprova: portao aqui reprovaria o acervo inteiro.")
    return "\n".join(L)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    print(relato(arg))
    sys.exit(0)   # SEMPRE zero: isto informa, nao reprova.
