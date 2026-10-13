#!/usr/bin/env python3
"""A FONTE declara "esses cinco casos" e enumera SEIS: achar isso antes de copiar.

POR QUE ISTO EXISTE, e e defeito da FONTE e nao meu. Em 13/10/2026, as 05:0x,
escrevendo um short a partir do longo `labtreinamento-009` (`dsoEo103l1o`), eu
li no capitulo 35 *"depois de descartar esses CINCO casos"* — e os capitulos 28 a
33 enumeram **SEIS**. O proprio longo tambem diz "os seis casos" em outro ponto,
logo ele se contradiz sozinho.

**Por que isso importa mais do que parece:** o short carrega o que o longo diz, e
numero de contagem passa por todos os nossos portoes. O `narracao` conta
QUANTIDADES por frase, nao confere se a quantidade e verdadeira; a regra (g) tira
numero que MUDA (aliquota, data), e contagem de casos nao muda — logo nada barra
"os cinco casos" num short cujo longo tem seis. Seria numero errado no ar, com
portao verde: a assinatura do paragrafo 3.8.

**E O PRIMEIRO DETECTOR QUE EU ESCREVI SOBRECONTAVA.** Ele comparava a declaracao
com QUALQUER kicker ordinal do longo, e no `labtreinamento-009` havia um
"Primeiro passo" alem dos seis "<ordinal> caso" — sete ordinais, logo ele acusava
"cinco contra sete" e "seis contra sete", sendo que a enumeracao de CASOS e seis.
Reportar aquilo como achado seria inventar dois defeitos e errar o terceiro.
**O detector tem de casar o SUBSTANTIVO:** "cinco casos" compara com os kickers
`<ordinal> caso`, nao com `<ordinal> passo`.

O que ele NAO faz: nao corrige texto e nao reprova spec. Ele aponta, e quem
escreve decide — no `s031` a decisao foi **omitir a contagem**, porque eu nao sei
qual numero o autor quis e inventar um e pior que nao dizer.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

# O VOCABULARIO E POR IDIOMA, e isso e uma CORRECAO de 13/10/2026 as 12:1x.
#
# A primeira versao deste modulo era so PORTUGUES, e eu reportei "1 conflito em
# 207 specs" como se fosse medicao da frota. **Nao era**: as specs do epomeno
# sao gregas e as do kolejny polonesas, logo "0 conflitos" nelas era VACUO, nao
# limpo -- o detector nao entendia uma palavra do que lia. O mesmo erro de
# enquadramento do 679/698: tratar como da frota o que era de uma parte dela.
#
# Achado a MAO na mesma rodada, no `epomeno-epipedo-006`: o capitulo 73 declara
# `Τέσσερα λάθη` (QUATRO erros) e os capitulos enumeram CINCO -- o 79 chega a
# dizer "Υπάρχει και ένα πέμπτο" ("existe tambem um quinto"). O detector
# portugues passou isso em silencio.
NUMERAL = {
    # pt
    "dois": 2, "duas": 2, "tres": 3, "três": 3, "quatro": 4, "cinco": 5,
    "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10,
    # el — com as variantes de genero que as fontes usam de verdade
    "δύο": 2, "δυο": 2, "τρία": 3, "τρεις": 3, "τέσσερα": 4, "τέσσερις": 4,
    "πέντε": 5, "έξι": 6, "εφτά": 7, "επτά": 7, "οκτώ": 8, "οχτώ": 8,
    "εννέα": 9, "εννιά": 9, "δέκα": 10,
    # pl
    "dwa": 2, "dwie": 2, "trzy": 3, "cztery": 4, "pięć": 5, "piec": 5,
    "sześć": 6, "szesc": 6, "siedem": 7, "osiem": 8, "dziewięć": 9,
    "dziesięć": 10,
}
ORDINAL = [
    # pt
    "primeiro", "segundo", "terceiro", "quarto", "quinto", "sexto",
    "setimo", "sétimo", "oitavo", "nono", "decimo", "décimo",
    # el — neutro e masculino, que e como o kicker aparece
    "πρώτο", "πρώτος", "δεύτερο", "δεύτερος", "τρίτο", "τρίτος",
    "τέταρτο", "τέταρτος", "πέμπτο", "πέμπτος", "έκτο", "έκτος",
    "έβδομο", "έβδομος", "όγδοο", "όγδοος", "ένατο", "ένατος",
    "δέκατο", "δέκατος",
    # pl
    "pierwszy", "pierwsze", "drugi", "drugie", "trzeci", "trzecie",
    "czwarty", "czwarte", "piąty", "piąte", "szósty", "szóste",
    "siódmy", "siódme", "ósmy", "ósme", "dziewiąty", "dziesiąty",
]

# Plural -> singular dos substantivos que a fonte costuma enumerar. Fechado de
# proposito: lista curta e previsivel vale mais que stemmer que erra calado.
SINGULAR = {
    # pt
    "casos": "caso", "passos": "passo", "razoes": "razao",
    "razões": "razão", "pontos": "ponto", "itens": "item",
    "motivos": "motivo", "etapas": "etapa", "regras": "regra",
    "criterios": "critério", "critérios": "critério",
    # el
    "λάθη": "λάθος", "βήματα": "βήμα", "περιπτώσεις": "περίπτωση",
    "λόγοι": "λόγος", "λόγους": "λόγο", "κανόνες": "κανόνας",
    "σημεία": "σημείο", "στήλες": "στήλη", "χρώματα": "χρώμα",
    # pl
    "błędy": "błąd", "bledy": "blad", "kroki": "krok",
    "przypadki": "przypadek", "powody": "powód", "zasady": "zasada",
    "dźwignie": "dźwignia", "punkty": "punkt",
}

# O DETERMINANTE E OPCIONAL, e isso tambem e da correcao de 12:1x: em portugues
# a fonte escreve "esses cinco casos", mas em grego o kicker e so
# `Τέσσερα λάθη`, sem artigo. Exigir determinante deixava o caso grego passar.
# O que SEGURA o falso positivo nao e o artigo -- sao as duas travas que ja
# existiam e continuam: casar o SUBSTANTIVO e exigir PROXIMIDADE.
_DECL = re.compile(
    r"(?:(?:esses|estes|essas|estas|os|as|τα|τους|τις)\s+)?("
    + "|".join(NUMERAL) + r")\s+(" + "|".join(SINGULAR) + r")\b")


def _norm(s: str) -> str:
    return (s or "").strip().lower()


JANELA = 12          # capitulos de distancia que ainda contam como "a mesma lista"


# ORDINAL -> POSICAO na lista, com as variantes de genero colapsadas. Isto
# entrou em 13/10 as 12:2x e e a SEGUNDA correcao do mesmo modulo na mesma
# rodada: a primeira so trocou o vocabulario, e com ela a frota saltou de 1 para
# 13 "conflitos" -- DOZE deles FALSOS. Conferidos a mao: `cztery błędy` com tres
# kickers `<ordinal> błąd`, `quatro passos` com UM. A causa nao era o idioma: o
# PRIMEIRO item da lista mora na NARRACAO do capitulo que declara, nao num
# kicker proprio, entao contar kicker subconta sempre em um.
#
# O conserto nao e somar um -- e contar a POSICAO MAIS ALTA alcancada. Se a
# fonte chega a "quinto", a lista tem pelo menos cinco itens, e isso vale tanto
# no kicker quanto na narracao.
_RANK = {}
for _i in range(0, len(ORDINAL)):
    pass
_SEQ = [
    ("primeiro",), ("segundo",), ("terceiro",), ("quarto",), ("quinto",),
    ("sexto",), ("setimo", "sétimo"), ("oitavo",), ("nono",),
    ("decimo", "décimo"),
]
_SEQ_EL = [
    ("πρώτο", "πρώτος"), ("δεύτερο", "δεύτερος"), ("τρίτο", "τρίτος"),
    ("τέταρτο", "τέταρτος"), ("πέμπτο", "πέμπτος"), ("έκτο", "έκτος"),
    ("έβδομο", "έβδομος"), ("όγδοο", "όγδοος"), ("ένατο", "ένατος"),
    ("δέκατο", "δέκατος"),
]
_SEQ_PL = [
    ("pierwszy", "pierwsze"), ("drugi", "drugie"), ("trzeci", "trzecie"),
    ("czwarty", "czwarte"), ("piąty", "piąte"), ("szósty", "szóste"),
    ("siódmy", "siódme"), ("ósmy", "ósme"), ("dziewiąty",), ("dziesiąty",),
]
for _seq in (_SEQ, _SEQ_EL, _SEQ_PL):
    for _pos, _formas in enumerate(_seq, start=1):
        for _f in _formas:
            _RANK[_f] = _pos


def enumerados(longo: list[dict], singular: str, perto_de: int = None) -> int:
    """A POSICAO MAIS ALTA de `<ordinal> <singular>` perto da declaracao.

    Le kicker E narracao, porque o primeiro item costuma estar na narracao do
    proprio capitulo que declara a contagem (foi o que produziu doze falsos
    positivos em 13/10). O casamento do SUBSTANTIVO e a PROXIMIDADE continuam
    sendo as duas travas que impedem o detector de inventar achado.
    """
    ranks, nus = [], []
    for i, c in enumerate(longo):
        if perto_de is not None and abs(i - perto_de) > JANELA:
            continue
        k = re.sub(r"^(o|a|το|η)\s+", "", _norm(c.get("kicker")))
        texto = k + " || " + _norm(c.get("nar"))
        for m in re.finditer(r"\b(" + "|".join(_RANK) + r")\b(?:\s+|\s*)"
                             + re.escape(singular) + r"\b", texto):
            ranks.append(_RANK[m.group(1)])
        m = re.match(r"(" + "|".join(_RANK) + r")\s*$", k)
        if m:
            nus.append(_RANK[m.group(1)])
    if ranks:
        return max(ranks)
    # O ORDINAL NU NAO SUSTENTA ACUSACAO, e isto e a QUARTA correcao do mesmo
    # modulo na mesma rodada (13/10, 12:4x). O detector original o usava como
    # recurso quando nenhum kicker trazia o substantivo; com a regra da
    # assimetria ele virou fonte de falso positivo no outro sentido: no
    # `epomeno-epipedo-003` a declaracao "τις δύο στήλες" (duas colunas, e sao
    # duas) pareou com `πρώτο/δεύτερο/τρίτο` dos capitulos 71 a 73, que sao OUTRA
    # lista -- e saiu "2 contra 3". Mesmo acidente no `-011`.
    #
    # Um ordinal SEM o substantivo nao carrega evidencia de pertencer a lista
    # declarada, e proximidade nao supre isso: capitulo vizinho muda de assunto.
    # Entao ele nao conta. O custo e perder o estilo "Primeiro caso / Segundo /
    # Terceiro", e eu prefiro perder achado a inventar achado.
    return 0


def divergencias(spec: dict) -> list[dict]:
    """Declaracoes de contagem que NAO batem com a enumeracao do mesmo longo."""
    longo = spec.get("longo") or []
    if not longo:
        return []
    out, vistos = [], set()
    for idx, c in enumerate(longo):
        texto = _norm(c.get("nar")) + " " + _norm(c.get("kicker"))
        for m in _DECL.finditer(texto):
            declarado, plural = NUMERAL[m.group(1)], m.group(2)
            singular = SINGULAR[plural]
            n = enumerados(longo, singular, perto_de=idx)
            chave = (m.group(0), n)
            # SO REPORTA QUANDO A ENUMERACAO PASSA DA DECLARACAO, e a assimetria
            # e MEDIDA, nao estetica (13/10, 12:3x -- terceira correcao do mesmo
            # modulo na mesma rodada).
            #
            # Conferidos a mao os tres casos de `enumerados < declarado`
            # (`labtreinamento-004` 4 contra 1, `nivel-do-jogo-008` 3 contra 1,
            # `kolejny-poziom-012` 4 contra 1): os TRES estavam CERTOS na fonte.
            # Ela enumera com ordinal NU seguido de dois-pontos ("Primeiro:",
            # "Drugi:") ou com o numeral DEPOIS do substantivo ("Passo um"), e o
            # detector nao le nenhuma das duas formas. Logo subcontar e MEU
            # defeito, e acusar a fonte por isso seria inventar achado.
            #
            # O outro lado nao tem esse problema: se a fonte chega a "quinto
            # erro" tendo declarado quatro, o quinto EXISTE -- achar um item alem
            # da declaracao nao e artefato de contagem, e prova de que a lista
            # passou do numero. O detector perde o caso oposto (declarar mais do
            # que lista), e isso vai dito no relato em vez de ficar implicito.
            if n and n > declarado and chave not in vistos:
                vistos.add(chave)
                out.append({"declaracao": m.group(0), "declarado": declarado,
                            "enumerados": n, "substantivo": singular,
                            "capitulo": idx})
    return out


def relato(caminho: str) -> str:
    with open(caminho, encoding="utf-8") as f:
        spec = json.load(f)
    d = divergencias(spec)
    nome = os.path.basename(caminho)
    if not d:
        return f"{nome}: nenhuma contagem declarada em conflito."
    linhas = [f"{nome}: {len(d)} contagem(ns) declarada(s) em CONFLITO com a "
              "enumeracao do proprio longo."]
    for x in d:
        linhas.append(f"  \"{x['declaracao']}\" — mas o longo enumera "
                      f"{x['enumerados']} `{x['substantivo']}`.")
    linhas.append("  NAO copie a contagem para o short. Omitir e melhor que "
                  "inventar: o autor pode ter querido qualquer um dos dois.")
    return "\n".join(linhas)


def main() -> int:
    alvos = sys.argv[1:] or sorted(glob.glob(
        os.path.join(os.path.dirname(__file__), "specs", "*.json")))
    achou = 0
    for a in alvos:
        t = relato(a)
        if "CONFLITO" in t:
            print(t)
            achou += 1
    print(f"\n{achou} spec(s) com conflito, de {len(alvos)} conferida(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
