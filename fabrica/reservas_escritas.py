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
import segundo_angulo as SA

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


# A convencao do indice de capitulo citado na prosa e MEDIDA, nao suposta:
# `capitulos 33 a 36` do `labtreinamento-s033` casa com a posicao 33 da lista de
# cenas do longo contada de ZERO (`Fontes que valem`, e a prosa diz "as FONTES
# que valem"), e o mesmo vale para o `kolejny-poziom-s022` (52 -> `Cztery
# dzwignie`, e a prosa diz "as quatro dzwignie") e para o `epomeno-epipedo-s021`
# (40 -> `Protoi plevra`, e a prosa diz "as DUAS pessoas"). Tres amostras, e o
# teste RECONFERE isto contra o disco em vez de confiar nesta linha (753).
BASE_DO_INDICE = 0


def estado(origem: str = None, dir_specs: str = None) -> list:
    """Cada reserva ESCRITA com um veredito: ela segue livre ou foi consumida?

    **POR QUE ISTO SO FOI POSSIVEL AGORA (21/10 as 13:1x).** O docstring deste
    modulo diz, desde que ele nasceu, que decidir se a reserva segue livre e do
    `concentracao` e do `segundo_angulo` — e o `segundo_angulo` **nao podia
    responder**, porque o proprio bloco de reserva fazia o capitulo contar como
    MENCIONADO (medido em 20/10 as 12:4x). **A remissao era circular, e o
    conserto daquela rodada e o que destrava esta pergunta.**

    E ela custava uma rodada: nesta, para saber que a reserva do
    `epomeno-epipedo-s020` ja havia sido consumida pelo `-s036`, eu li os quatro
    irmaos da origem um por um.

    **O veredito e sobre os capitulos que o DONO extraiu**, e os quatro valores
    sao:

      * `livre` — nenhum capitulo da reserva aparece na copy de irmao nenhum;
      * `consumida` — todos aparecem;
      * `parcial` — alguns. **E `parcial` NAO quer dizer "metade consumida":**
        o bloco pode nomear capitulo em mais de um papel na mesma frase (o
        `labtreinamento-s033` cita o que deixou *e* o que um irmao ja levou), e
        este modulo nao le papel de frase. `parcial` quer dizer **leia a
        prosa**;
      * `indeterminada` — a reserva nao nomeia capitulo por indice, ou a origem
        nao resolve para pacote local (a regra h). **Isto RECUSA em vez de
        chutar**, do jeito que o `porta1` recusa janela curta — e e o caso da
        reserva que esta rodada teve de resolver lendo: **9 das 24 do acervo**
        descrevem o capitulo em prosa, sem indice.

    As duas contas sao **DELEGADAS**: a lista de capitulos do longo e a mencao
    saem do `segundo_angulo`, que e quem sabe resolver origem para pacote e quem
    (desde 20/10 as 12:4x) tira o bloco de reserva antes de testar mencao.
    Reimplementar qualquer uma aqui criaria o segundo dono.

    **E a mencao segue sendo INDICIO e nao prova**, com os dois limites do dono:
    um short pode usar o capitulo sem citar o kicker, e kicker repetido no longo
    e uma entrada so.
    """
    saida = []
    for r in (da_origem(origem, dir_specs) if origem
              else varre(dir_specs)):
        reg = dict(r)
        pacote = SA.pacote_do_id(r["origem"], **({"dir_specs": dir_specs}
                                                 if dir_specs else {}))
        caps = (SA.capitulos_do_pacote(pacote, **({"dir_specs": dir_specs}
                                                  if dir_specs else {}))
                if pacote else [])
        indices = [i for i in (r["capitulos"] or [])
                   if BASE_DO_INDICE <= i < len(caps) + BASE_DO_INDICE]
        kickers = [caps[i - BASE_DO_INDICE] for i in indices]
        kickers = [k for k in kickers if k]
        if not kickers:
            reg.update({"pacote_da_origem": pacote, "kickers": [],
                        "livres": [], "mencionados": [],
                        "veredito": "indeterminada"})
            saida.append(reg)
            continue
        d = SA.nao_mencionados(r["origem"], **({"dir_specs": dir_specs}
                                               if dir_specs else {}))
        nao = set(d["nao_mencionados"])
        livres = [k for k in kickers if k in nao]
        men = [k for k in kickers if k not in nao]
        reg.update({"pacote_da_origem": pacote, "kickers": kickers,
                    "livres": livres, "mencionados": men,
                    "veredito": ("livre" if not men else
                                 "consumida" if not livres else "parcial")})
        saida.append(reg)
    return saida


def da_origem(origem: str, dir_specs: str = None) -> list:
    return [r for r in varre(dir_specs) if r["origem"] == origem]


def _linha_do_veredito(e: dict) -> str:
    """A frase do veredito, com UM dono — ela sai nos DOIS ramos do relato.

    Ela nasceu duplicada em outros modulos desta semana e a segunda copia ficou
    citando conta velha (753). Aqui ela e uma funcao desde o primeiro minuto.
    """
    if not e:
        return ("veredito: INDETERMINADO — o `estado` nao devolveu esta"
                " reserva.")
    v = e["veredito"]
    if v == "indeterminada":
        return ("veredito: INDETERMINADA — a reserva descreve o capitulo em"
                " PROSA, sem indice, ou a origem nao tem spec local (regra h)."
                " Isto RECUSA em vez de chutar: 9 das 24 do acervo sao assim, e"
                " a desta classe se resolve LENDO os irmaos.")
    if v == "livre":
        return ("veredito: LIVRE — nenhum dos %d capitulo(s) dela aparece na"
                " copy de irmao nenhum." % len(e["kickers"]))
    if v == "consumida":
        return ("veredito: CONSUMIDA — os %d capitulo(s) dela ja aparecem em"
                " irmao. Foi assim que a reserva do `epomeno-epipedo-s020`"
                " acabou: o `-s036` a levou." % len(e["kickers"]))
    return ("veredito: PARCIAL — %d livre(s) e %d mencionado(s). Isto NAO quer"
            " dizer metade consumida: o bloco pode nomear capitulo em mais de"
            " um papel na mesma frase, e este modulo nao le papel de frase."
            " PARCIAL quer dizer LEIA A PROSA."
            % (len(e["livres"]), len(e["mencionados"])))


def relato(origem: str = None, dir_specs: str = None) -> str:
    todas = varre(dir_specs)
    if origem is not None:
        delas = [r for r in todas if r["origem"] == origem]
        if not delas:
            return (f"RESERVA ESCRITA para {origem}: NENHUMA. Nenhum irmao desta"
                    " origem deixou indicacao em prosa — a pauta sai do"
                    " `segundo_angulo` e da leitura, como sempre.")
        L = [f"RESERVA ESCRITA para {origem}: {len(delas)}."]
        por_pacote = {e["pacote"]: e for e in estado(origem, dir_specs)}
        for r in delas:
            L.append(f"  deixada por {r['pacote']}"
                     + (f", capitulos {r['capitulos'][0]} a"
                        f" {r['capitulos'][-1]}" if r["capitulos"] else ""))
            L.append(f"    {r['texto'][:600]}")
            L.append("    " + _linha_do_veredito(por_pacote.get(r["pacote"])))
        L.append("  o veredito acima e sobre os capitulos que o dono EXTRAIU, e"
                 " ele so foi possivel depois de 20/10 as 12:4x, quando o bloco"
                 " de reserva parou de fazer o proprio capitulo contar como"
                 " MENCIONADO. Mencao e INDICIO, nao prova: um short pode usar"
                 " o capitulo sem citar o kicker.")
        return "\n".join(L)
    L = [f"RESERVAS ESCRITAS no acervo: {len(todas)}, em"
         f" {len({r['origem'] for r in todas})} origem(ns)."]
    for r in todas:
        L.append(f"  {r['pacote']:<24} {r['origem'] or '-'}"
                 + (f"  cap {r['capitulos'][0]}-{r['capitulos'][-1]}"
                    if r["capitulos"] else ""))
    conta = {}
    for e in estado(None, dir_specs):
        conta[e["veredito"]] = conta.get(e["veredito"], 0) + 1
    L.append("  por veredito: "
             + ", ".join(f"{k} {v}" for k, v in sorted(conta.items())))
    L.append("  " + _linha_do_veredito({"veredito": "indeterminada",
                                        "kickers": [], "livres": [],
                                        "mencionados": []}))
    L.append("  o marcador tem UM dono (`irmaos_da_origem.MARCAS_DE_NEGACAO`) e"
             " tem de ABRIR paragrafo: das 25 ocorrencias do disco, 24 abrem e"
             " UMA e citacao de uma reserva ja consumida.")
    return "\n".join(L)


if __name__ == "__main__":
    import sys
    print(relato(sys.argv[1] if len(sys.argv) > 1 else None))
