#!/usr/bin/env python3
"""A leitura de SOM da peça publicada não morava em lugar nenhum.

POR QUE ISTO EXISTE, e é o §11-bis de 21/10 às 22:3x.

Toda rodada eu leio o `::notice:: SOM` da anotação do job — LUFS, pico real,
LRA, desvio do alvo, silêncios —, escrevo os números no relato e no commit, e
**eles acabam ali**. O parque de duração (`duracao_a_medir`) grava provedor,
job e duração de toda peça publicada; o som, não. Logo *"quantas peças já
saíram com o pico acima do nosso próprio teto?"* era pergunta para mim, e eu a
respondia à mão: a medida de **NOVE dos 38 renders recentes** escrita no
docstring do `som.py` foi contada na API numa rodada, e o próprio comentário
dela diz, em letra, que *"nenhum teste a reconfere, porque ela não está no
disco"*.

É a assinatura do **726**: o passo que não tem instrumento é o passo que eu
solto. E é o item 3 da §10 numa dimensão nova — canal (19/10 11:2x), cota
(19/10 23:3x), cenas (20/10 02:2x), pauta (20/10 08:2x), dono da origem (20/10
10:1x) e agora **SOM**.

**O VEREDITO NÃO É PARQUEADO, e esta é a decisão que mais importa aqui.** A
anotação já traz o campo `pico_vs_teto` calculado no runner, e gravá-lo seria
congelar um veredito feito com um teto que pode mudar — o segundo dono da
mesma regra, a assinatura que congelou a legenda. O parque guarda a **MEDIDA**
(`pico_dbtp`) e quem julga é sempre `som.pico_acima_do_teto`, logo mexer no
`som.TP_MAX_DBTP` relê o parque inteiro em vez de deixar atrás uma classificação
velha.

**E isso não é precaução teórica: 51 das 60 linhas semeadas NÃO TÊM o campo**,
porque ele nasceu em 21/10 às 13:4x. Parque que dependesse dele perderia 85% da
própria base.

A SEMENTE é medição com procedência e vai declarada: os 60 `::notice:: SOM` dos
60 runs mais recentes do `frota.yml`, lidos da API do GitHub em 21/10 às 22:4x,
cada linha com o `run` e o `job` que a emitiram. Não é memória minha — e por
isso o `distribuicao` pode ser reconferido.

**Isto NÃO é portão** e o código de saída é sempre zero, pelo argumento do
`mira.py`: `acima_do_teto` é LEITURA e não defeito (só `clipa` é defeito, e o
`som.pico_acima_do_teto` é quem diz isso), e um portão aqui reprovaria dez peças
de acervo que já estão no ar.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import canal  # noqa: E402
import som  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARQUE = os.path.join(RAIZ, "docs", "pendente", "som-medido.jsonl")

# O que uma linha do parque tem de trazer. `pacote` e `job` são a PROCEDÊNCIA, e
# são obrigatórios pela mesma razão que o provedor é obrigatório no parque de
# duração (733): leitura sem procedência convida a conferir no lugar errado, e
# em 20/10 às 14:3x eu gravei um job INVENTADO porque nada o cobrava.
OBRIGATORIOS = ("pacote", "arquivo", "job", "pico_dbtp")

# Abaixo disto o `distribuicao` RECUSA afirmar, do jeito que o `porta1` recusa
# janela curta. Não é limiar de qualidade: é o tamanho abaixo do qual a contagem
# dos três estados não diz nada — com duas linhas "nenhuma clipa" é vacuidade.
MINIMO_PARA_AFIRMAR = 20

_NOTICE = re.compile(r"^(?:::notice::\s*)?SOM\s+(\S+)\s+(\S+)\s+(\{.*\})\s*$")


class SemProcedencia(Exception):
    """Falta `pacote`, `job` ou a medida — e isso levanta em vez de parquear."""


def do_notice(linha: str, job: str, run: str | None = None) -> dict:
    """A linha `::notice:: SOM <arquivo> <pacote> {json}` virada em registro.

    O `job` vem de FORA e não tem padrão, porque ele é medição da rodada — quem
    o tem à mão é quem leu a anotação, e dar-lhe padrão faria a rodada futura
    inventar procedência.
    """
    if not job:
        raise SemProcedencia(
            "job vazio: a anotacao e a procedencia desta leitura, e leitura sem"
            " ela convida a conferir no lugar errado (733, e o job inventado de"
            " 20/10 as 14:3x)")
    m = _NOTICE.match((linha or "").strip())
    if not m:
        raise SemProcedencia(
            "a linha nao tem a forma do `::notice:: SOM <arquivo> <pacote>"
            " {json}` — recusar e melhor que gravar leitura de origem incerta")
    arquivo, pacote, bruto = m.group(1), m.group(2), m.group(3)
    try:
        d = json.loads(bruto)
    except ValueError as e:
        raise SemProcedencia("o JSON da anotacao nao abriu: %s" % e)
    reg = {
        "pacote": pacote,
        "arquivo": arquivo,
        "job": str(job),
        "lufs": d.get("lufs"),
        "lra": d.get("lra"),
        "pico_dbtp": d.get("pico_dbtp"),
        "desvio_do_alvo": d.get("desvio_do_alvo"),
        "silencios": d.get("silencios"),
        # O FATO de a anotação ter trazido o veredito, não o veredito. Guardar o
        # valor seria o segundo dono do teto; guardar o fato é o que mede quanto
        # da base dependeria dele.
        "tinha_veredito": "pico_vs_teto" in d,
    }
    if run:
        reg["run"] = str(run)
    valida(reg)
    return reg


def valida(reg: dict) -> dict:
    faltam = [k for k in OBRIGATORIOS if reg.get(k) in (None, "")]
    if faltam:
        raise SemProcedencia(
            "faltam %s — `pacote` e `job` sao PROCEDENCIA e `pico_dbtp` e a"
            " medida; parquear sem eles seria numero sem dono (733)"
            % ", ".join(faltam))
    return reg


def carrega(caminho: str = PARQUE) -> list:
    if not os.path.exists(caminho):
        return []
    saida = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                saida.append(json.loads(linha))
    return saida


def chave(reg: dict) -> tuple:
    """A identidade de uma leitura: (pacote, ARQUIVO) — e o arquivo é metade.

    Pego na PRIMEIRA execução, semeando o parque: o `labtreinamento-014` é um
    PACOTE e emite DUAS anotações, `longo.mp4` em -3,2 e `short.mp4` em -2,3.
    Chave por pacote sozinho leu isso como leitura discordante da mesma peça e
    levantou — a guarda estava certa e a CHAVE estava errada.

    É a mesma forma do defeito do `registro_videos` de 19/10 às 13:0x, onde o
    `slug` cravado fazia a linha do longo e a do short colidirem e o
    `on conflict do nothing` descartava uma **em silêncio**. Aqui ela levantou,
    o que é o sentido ruidoso e portanto o barato.
    """
    return (reg.get("pacote"), reg.get("arquivo"))


def parqueia(reg: dict, caminho: str = PARQUE) -> dict:
    """Grava, e LEVANTA se a mesma peça já estiver lá com medida DIFERENTE.

    Som de peça publicada não muda: duas leituras discordantes são do
    instrumento, não da peça — é a regra do parque de duração.
    """
    valida(reg)
    for antigo in carrega(caminho):
        if chave(antigo) == chave(reg):
            if antigo.get("pico_dbtp") != reg.get("pico_dbtp"):
                raise SemProcedencia(
                    "%s/%s ja esta no parque com pico %r e esta leitura diz"
                    " %r — som de peca publicada nao muda, logo a divergencia e"
                    " do INSTRUMENTO e nao da peca"
                    % (reg["pacote"], reg.get("arquivo"),
                       antigo.get("pico_dbtp"), reg.get("pico_dbtp")))
            return antigo
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False, sort_keys=True) + "\n")
    return reg


def veredito(reg: dict) -> dict:
    """O estado do pico desta linha, DELEGADO ao dono do teto.

    O teto não aparece neste módulo: ele vive em `som.TP_MAX_DBTP`, e copiá-lo
    aqui criaria o segundo dono — a assinatura que congelou a legenda.
    """
    return som.pico_acima_do_teto(reg.get("pico_dbtp"))


def distribuicao(registros: list | None = None) -> dict:
    regs = carrega() if registros is None else list(registros)
    contagem = {"dentro": 0, "acima_do_teto": 0, "clipa": 0, "sem_leitura": 0}
    acusadas = {"acima_do_teto": [], "clipa": []}
    for r in regs:
        est = veredito(r)["estado"]
        contagem[est] = contagem.get(est, 0) + 1
        if est in acusadas:
            acusadas[est].append("%s/%s" % (r.get("pacote"),
                                            r.get("arquivo")))
    picos = [r.get("pico_dbtp") for r in regs
             if isinstance(r.get("pico_dbtp"), (int, float))]
    # POR CANAL, e com o DENOMINADOR ao lado — oito das onze acusadas são de um
    # canal só, e dizer isso sem o denominador é o erro de enquadramento do
    # 679/698/725. Medido, os denominadores saem IGUAIS (vinte por canal), o que
    # desmentiu a ressalva que eu havia escrito aqui ANTES de olhar. A derivação
    # do canal é DELEGADA ao `canal.do_pacote`, dono único desde 19/10 às 05:2x.
    por_canal = {}
    for r in regs:
        c = canal.do_pacote(r.get("pacote") or "")
        d = por_canal.setdefault(c, {"n": 0, "fora": 0})
        d["n"] += 1
        if veredito(r)["estado"] in ("acima_do_teto", "clipa"):
            d["fora"] += 1
    for d in por_canal.values():
        d["fracao"] = round(d["fora"] / d["n"], 3) if d["n"] else None
    basta = len(regs) >= MINIMO_PARA_AFIRMAR
    return {
        "n": len(regs),
        "contagem": contagem,
        "acusadas": acusadas,
        "faixa_de_pico": (min(picos), max(picos)) if picos else None,
        "por_canal": por_canal,
        "afirma": basta,
        "minimo": MINIMO_PARA_AFIRMAR,
        # Quantas ANOTACOES nao trouxeram o `pico_vs_teto` pronto. Le o campo
        # `tinha_veredito`, que e o FATO gravado — a primeira versao desta linha
        # procurava `pico_vs_teto` DENTRO do registro, que nunca esta la porque
        # o veredito nao e parqueado, e por isso ela dizia "60 de 60" onde a
        # medida e 51. Era o relato medindo outra coisa, pego na semeadura.
        "sem_o_campo_na_anotacao": sum(
            1 for r in regs if not r.get("tinha_veredito")),
    }


def _linha_dos_denominadores(d: dict) -> str:
    """A frase dos denominadores, DERIVADA — ela nunca escreve o numero à mão.

    A primeira versão dizia que eles "diferem", escrita antes de eu olhar; o
    parque a desmentiu (saíam vinte por canal). A **segunda** dizia que eles são
    IGUAIS, e com ela eu travei num teste um acidente da rotação 8/8/8: a
    primeira peça parqueada depois disso levou um canal a 21 e derrubou o teste
    — identidade onde havia propriedade (743/753/761).

    O que de fato sustenta ler o contraste direto não é a igualdade, é a
    COMPARABILIDADE: nenhum denominador abaixo da metade do maior. Acima dessa
    folga a contagem bruta deixa de se comparar e a frase tem de ser relida, e é
    isso que esta linha diz em vez de um número.
    """
    pc = d["por_canal"]
    if not pc:
        return ("  por CANAL: o parque nao tem canal nenhum derivado — sem isso"
                " a comparacao nao existe.")
    ns = {c: v["n"] for c, v in pc.items()}
    maior, menor = max(ns.values()), min(ns.values())
    corpo = ", ".join("%s %d" % (c, n) for c, n in sorted(ns.items()))
    if maior == menor:
        como = ("os denominadores saem IGUAIS (%d por canal), logo o contraste"
                " se le direto" % maior)
    elif menor * 2 >= maior:
        como = ("os denominadores DIFEREM e seguem COMPARAVEIS (%s; o menor e"
                " %.0f%% do maior), logo o contraste ainda se le direto"
                % (corpo, 100.0 * menor / maior))
    else:
        como = ("os denominadores estao DESEQUILIBRADOS (%s; o menor e %.0f%% do"
                " maior) — a contagem bruta deixa de se comparar e esta linha"
                " tem de ser RELIDA" % (corpo, 100.0 * menor / maior))
    return ("  e %s. **A primeira versao desta linha dizia que eles diferem**,"
            " escrita antes de eu olhar, e a segunda cravou a IGUALDADE num"
            " teste — a peca seguinte, num canal so, a derrubou." % como)


def _linha_da_recusa(d: dict) -> str:
    """A frase da recusa, com UM dono — ela sai no ramo em que o parque é curto.

    Sem ela um parque de duas linhas imprimiria "zero clipa" e isso leria como
    medição; vazio de instrumento não prova ausência (17/10).
    """
    return ("  >> NAO AFIRMA: o parque tem %d linha(s) e o minimo e %d. Contar"
            " os tres estados com menos que isso e vacuidade — 'nenhuma clipa'"
            " em duas linhas nao mede nada." % (d["n"], d["minimo"]))


def relato(registros: list | None = None) -> str:
    d = distribuicao(registros)
    c = d["contagem"]
    ls = ["SOM PARQUEADO: %d peca(s) com leitura de som, teto do filtro"
          " %s dBTP (lido do `som.py`)" % (d["n"], som.TP_MAX_DBTP)]
    if not d["afirma"]:
        ls.append(_linha_da_recusa(d))
        return "\n".join(ls)
    ls.append("  dentro do teto: %d | ACIMA do teto: %d | CLIPA (acima de"
              " zero): %d | sem leitura: %d"
              % (c["dentro"], c["acima_do_teto"], c["clipa"],
                 c["sem_leitura"]))
    if d["faixa_de_pico"]:
        ls.append("  faixa de pico medida: %s a %s dBTP"
                  % d["faixa_de_pico"])
    if d["acusadas"]["clipa"]:
        ls.append("  >> CLIPA, e isto e DEFEITO e nao margem: %s"
                  % ", ".join(sorted(d["acusadas"]["clipa"])))
    if d["acusadas"]["acima_do_teto"]:
        ls.append("  acima do teto, e isto e LEITURA e nao defeito (quem diz e"
                  " o `som.pico_acima_do_teto`): %s"
                  % ", ".join(sorted(d["acusadas"]["acima_do_teto"])))
    ls.append("  por CANAL, com o denominador ao lado (sem ele seria o"
              " enquadramento do 679/698/725): %s"
              % " | ".join("%s %d de %d" % (c, v["fora"], v["n"])
                           for c, v in sorted(d["por_canal"].items())))
    ls.append(_linha_dos_denominadores(d))
    ls.append("  o que isto NAO afirma: que a voz de um canal produza pico mais"
              " alto. Voz e CONTEUDO andam juntos nos tres canais e ninguem"
              " aleatorizou nada — o que esta medido e a contagem.")
    ls.append("  o VEREDITO nao e parqueado: o parque guarda `pico_dbtp` e"
              " quem julga e o `som.pico_acima_do_teto`, logo mexer no teto rele"
              " o parque inteiro em vez de deixar atras classificacao velha.")
    ls.append("  e isso nao e precaucao teorica: a anotacao TRAZ um"
              " `pico_vs_teto` pronto, e ele nasceu em 21/10 as 13:4x — %d das"
              " %d linhas do parque NAO o tinham."
              % (d["sem_o_campo_na_anotacao"], d["n"]))
    ls.append("  isto NAO reprova e o codigo de saida e sempre zero: um portao"
              " aqui reprovaria peca de acervo que ja esta no ar.")
    return "\n".join(ls)


def main(argv: list | None = None) -> int:
    print(relato())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
