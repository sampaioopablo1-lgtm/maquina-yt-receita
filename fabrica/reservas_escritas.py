# -*- coding: utf-8 -*-
"""As reservas de pauta que as rodadas anteriores deixaram ESCRITAS em prosa.

**POR QUE EXISTE (20/10 as 20:4x).** A peca desta rodada
(`kolejny-poziom-s078`) saiu de uma indicacao que o `kolejny-poziom-s019`
escreveu em prosa, em letra: *"O QUE EU NAO LEVEI, escrito para a proxima rodada
achar: 'Rata ma dwie czesci' / 'Na poczatku' ... Outra familia (A PARTE QUE
DOMINA NO COMECO) e um TERCEIRO angulo"*. **Eu a achei por ACIDENTE** — o
`irmaos_da_origem` passou a imprimir o bloco de prosa dos irmaos sem campo as
15:3x de hoje, e ela estava la dentro.

**MEDIDO: o acervo carrega VINTE E QUATRO reservas dessas, uma por peca que
escreveu uma**, e nenhuma delas era alcancavel por instrumento nenhum — so
lendo um irmao por vez, e so quando a origem do irmao e a que a rodada escolheu.
E a classe dos layouts mortos virada do avesso: nao e codigo que ninguem chama,
e **DADO que ninguem pode consultar**.

**E ELAS SAO A PAUTA MAIS BARATA QUE EXISTE AQUI**, porque vem com tres coisas
que a escolha de pauta normalmente custa uma rodada para produzir: a origem, os
capitulos, e o MOTIVO pelo qual a rodada anterior nao a levou. Varias dizem, em
letra, que o que falta e *"um TERCEIRO angulo"*.

**O MARCADOR TEM UM DONO, e e o `irmaos_da_origem.MARCAS_DE_NEGACAO`**, criado
as 17:4x de hoje para o conserto do capitulo negado contado como declarado.
Repetir a string aqui criaria o segundo dono — a assinatura que congelou a
legenda.

**E O DISCRIMINADOR DO FALSO POSITIVO E MEDIDO, nao suposto:** o marcador tem de
ABRIR um paragrafo. Das 25 ocorrencias do disco, **24 abrem** (precedidas de
linha em branco) e **UMA** e uma CITACAO — a propria copy desta rodada, que
reproduz a indicacao do `s019` dentro de uma frase, precedida de `*"` e seguida
de `"*`. Sem essa guarda o instrumento contaria como reserva NOVA a mencao de
uma reserva JA CONSUMIDA, que e detector inventando achado (725) no lugar mais
caro: ele mandaria a rodada seguinte reescrever a peca de hoje.

**O que ele NAO faz:** decidir se a reserva ainda esta livre. Isso e do
`concentracao` (contagem) e do `segundo_angulo` (capitulos), e uma reserva
escrita em 13/10 pode ter sido consumida depois sem ninguem riscar a prosa. Ele
poe a lista na mesa COM a origem, para que as outras duas contas respondam.
"""
import glob
import json
import os
import re

import irmaos_da_origem as IO

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _blocos(copy: str) -> list:
    """Os blocos de reserva que ABREM paragrafo — a guarda do falso positivo."""
    saida = []
    for marca in IO.MARCAS_DE_NEGACAO:
        for m in re.finditer(r"\*{0,2}" + re.escape(marca), copy, re.I):
            antes = copy[:m.start()].rstrip(" *\"'`")
            if antes and not antes.endswith("\n"):
                continue          # marcador no meio de frase: e CITACAO
            resto = copy[m.end():]
            fim = re.search(r"\n\s*\n|\n##\s", resto)
            saida.append(copy[m.start(): m.end() +
                              (fim.start() if fim else len(resto))])
    return saida


def blocos_de_reserva(copy: str) -> list:
    """A porta PUBLICA do `_blocos` — e ela existe por um defeito medido.

    **20/10 as 12:4x: o bloco de reserva do irmao fazia o `segundo_angulo`
    contar o capitulo como MENCIONADO.** Aquele instrumento procura o kicker na
    copy INTEIRA do irmao, e o bloco de reserva NOMEIA, em letra, os capitulos
    que a rodada anterior deliberadamente NAO levou. Logo a promessa virava uso,
    e a direcao e perversa: **quanto melhor a rodada anterior documentou o que
    deixou, mais invisivel o capitulo fica.**

    O docstring deste modulo manda, desde que ele nasceu, perguntar ao
    `segundo_angulo` se a reserva segue livre — e o `segundo_angulo` nao podia
    responder, porque a propria reserva o cegava. **A remissao era CIRCULAR.**

    Esta funcao e so o nome publico: o dono da extracao continua sendo o
    `_blocos` deste modulo, e o dono do marcador continua sendo o
    `irmaos_da_origem.MARCAS_DE_NEGACAO`. Reimplementar a leitura do bloco no
    `segundo_angulo` criaria o SEGUNDO dono dela, que e a assinatura que
    congelou a legenda.
    """
    return _blocos(copy)


def varre(dir_specs: str = None) -> list:
    """Uma entrada por reserva ESCRITA, com a origem e os capitulos dela."""
    dir_specs = dir_specs or os.path.join(RAIZ, "fabrica", "specs")
    if not os.path.isdir(dir_specs):
        raise ValueError(
            "dir_specs nao e um diretorio: %r. Varredura em caminho"
            " inexistente devolveria lista VAZIA e bem formada, indistinguivel"
            " de acervo sem reserva nenhuma — medido em 20/10 as 12:3x no"
            " `segundo_angulo`." % dir_specs)
    saida = []
    for f in sorted(glob.glob(os.path.join(dir_specs, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo"):
            continue
        copy = d.get("copy") or ""
        pacote = os.path.basename(f)[:-5]
        for bloco in _blocos(copy):
            saida.append({
                "pacote": pacote,
                "origem": d.get("longo_existente"),
                "texto": " ".join(bloco.split()),
                # capitulos DELEGADOS ao dono, que e quem sabe ler a faixa
                "capitulos": IO.capitulos_negados(bloco),
            })
    return saida


def da_origem(origem: str, dir_specs: str = None) -> list:
    return [r for r in varre(dir_specs) if r["origem"] == origem]


def relato(origem: str = None, dir_specs: str = None) -> str:
    todas = varre(dir_specs)
    if origem is not None:
        delas = [r for r in todas if r["origem"] == origem]
        if not delas:
            return (f"RESERVA ESCRITA para {origem}: NENHUMA. Nenhum irmao desta"
                    " origem deixou indicacao em prosa — a pauta sai do"
                    " `segundo_angulo` e da leitura, como sempre.")
        L = [f"RESERVA ESCRITA para {origem}: {len(delas)}."]
        for r in delas:
            L.append(f"  deixada por {r['pacote']}"
                     + (f", capitulos {r['capitulos'][0]} a"
                        f" {r['capitulos'][-1]}" if r["capitulos"] else ""))
            L.append(f"    {r['texto'][:600]}")
        L.append("  isto NAO diz que a reserva segue livre: quem conta uso e o"
                 " `concentracao`, e quem conta capitulo e o `segundo_angulo`."
                 " Reserva escrita em 13/10 pode ter sido consumida sem ninguem"
                 " riscar a prosa.")
        return "\n".join(L)
    L = [f"RESERVAS ESCRITAS no acervo: {len(todas)}, em"
         f" {len({r['origem'] for r in todas})} origem(ns)."]
    for r in todas:
        L.append(f"  {r['pacote']:<24} {r['origem'] or '-'}"
                 + (f"  cap {r['capitulos'][0]}-{r['capitulos'][-1]}"
                    if r["capitulos"] else ""))
    L.append("  o marcador tem UM dono (`irmaos_da_origem.MARCAS_DE_NEGACAO`) e"
             " tem de ABRIR paragrafo: das 25 ocorrencias do disco, 24 abrem e"
             " UMA e citacao de uma reserva ja consumida.")
    return "\n".join(L)


if __name__ == "__main__":
    import sys
    print(relato(sys.argv[1] if len(sys.argv) > 1 else None))
