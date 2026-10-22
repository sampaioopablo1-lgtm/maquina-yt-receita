# -*- coding: utf-8 -*-
"""O RASCUNHO nao tinha como perguntar — todo relato exigia ARQUIVO.

MEDIDO em 21/10 as 20:3x, escrevendo o `kolejny-poziom-s089`. A peca se escreve
num construtor que vive FORA do repo, e o comprimento da narracao se acerta por
iteracao: escreve, mede a previsao, move caracteres, mede outra vez. Nessa
iteracao a spec existe **so na memoria** — e, varrido o conjunto da passada de
pre-render, de SEIS relatos apenas UM aceitava dicionario:

| relato | aceitava |
|---|---|
| `paleta_da_spec.relato` | **dicionario** |
| `mira.relato` | caminho |
| `acento.relato` | caminho |
| `gancho.relato` | caminho |
| `layouts_do_short.relato` | caminho |
| `antes_do_render.relato` | caminho |

**E a capacidade existia uma camada abaixo:** `mira.quanto_cortar` e
`mira.orcamento` recebem dicionario, e **DEZ dos DOZE portoes** do `prontidao`
nao abrem o arquivo — eles recebem `sp` do despachante, e o caminho so serve de
NOME (o `identidade` compara `pacote` com o nome do arquivo, o `similaridade` e
o `variedade` varrem o disco). Logo o rascunho sempre pudera ser conferido, e o
que impedia era a CAMADA do relato.

**O CUSTO ESTA MEDIDO e foi desta rodada:** eu movi o comprimento da narracao em
QUATRO builds, calculando *"~0,57 s por caractere"* de cabeca a partir de duas
medicoes — e **passei do ponto**, com a previsao em 41,19 s contra um piso de
41,5. O `mira.quanto_cortar` devolve esse passo e o total a mover, pronto, e eu
nao o chamei porque chama-lo exigia gravar a spec no disco primeiro. **Item 3 da
§10: numero que eu calculo a mao vira um erro meu.**

Este modulo tem UM dono da normalizacao e nada mais: `spec_de(caminho, spec)`.
Os cinco relatos passaram a aceitar `spec=`, e o `prontidao.avalia` tambem — o
rascunho entrega o caminho PRETENDIDO (que e nome, nao arquivo) com o
dicionario.

**O QUE O RASCUNHO NAO ALCANCA, e vai NOMEADO em vez de escondido:** com o
arquivo ainda fora do disco, o `similaridade` e o `variedade` nao enxergam esta
peca na varredura deles, e o `identidade` confere o `pacote` contra um nome que
ainda nao existe. Os tres respondem sobre o ACERVO, logo a resposta e valida e
INCOMPLETA — e o relato diz isso, do jeito que o `porta1` recusa janela curta.
"""
from __future__ import annotations

import json


def spec_de(caminho: str | None = None, spec: dict | None = None) -> dict:
    """O dicionario da spec: o passado por `spec`, ou o lido do arquivo.

    `spec` vence o arquivo de proposito — e para isso que o rascunho existe. E
    um dicionario VAZIO nao e "nenhum dicionario": `{}` levanta, porque spec
    vazia no lugar da lida do disco seria o 17/10 outra vez (vazio nao prova
    ausencia) e faria toda conferencia passar por vacuidade.
    """
    if spec is not None:
        if not isinstance(spec, dict):
            raise TypeError("spec tem de ser dicionario, e veio %r"
                            % type(spec).__name__)
        if not spec:
            raise ValueError(
                "spec VAZIA no lugar da do disco: toda conferencia passaria por "
                "vacuidade, e vazio nao prova ausencia (17/10)")
        return spec
    if caminho is None:
        raise ValueError(
            "sem `caminho` e sem `spec` nao ha spec nenhuma: sem esta guarda o "
            "`open(None)` levanta `TypeError: stat`, que e erro de TIPO onde a "
            "pergunta e de DADO (22/10, 04:4x)")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def e_rascunho(caminho: str | None = None, spec: dict | None = None) -> bool:
    """O arquivo ainda nao esta no disco, logo a varredura do acervo nao o ve.

    **`caminho=None` E A FORMA CANONICA DA PERGUNTA, e ate 22/10 as 04:4x ela
    LEVANTAVA aqui** — `os.path.exists(None)` da `TypeError: stat`. Tres dos
    relatos normalizados em 21/10 as 23:2x declaram `caminho=None` na
    assinatura, logo o repo carregava DUAS convencoes para a mesma chamada: o
    mesmo nome de parametro com dois significados em modulos irmaos, que e a
    assinatura do `exceto` de 20/10 as 11:3x — criada pelo meu proprio conserto
    uma rodada depois dele.

    E o CUSTO foi pago: chamado `mira.relato(None, spec=sp)` para pedir o passo
    em caracteres, a resposta foi um `TypeError` — e `mira` levanta justamente
    porque e o UNICO sub-relato que PERGUNTA a este dono. Os que respondiam,
    respondiam por nao perguntar.

    Sem `spec` ele devolve False em qualquer forma de caminho, e isso NAO e
    descuido: sem dicionario nao ha nada a conferir fora do disco.
    """
    import os
    if spec is None:
        return False
    return caminho is None or not os.path.exists(caminho)


def aviso_do_rascunho(caminho: str | None = None,
                      spec: dict | None = None) -> str:
    """A frase que NOMEIA o que o rascunho nao alcanca. Vazia quando nao e um.

    Ela tem UM dono porque copia-la seria a assinatura que congelou a legenda.
    **A primeira versao desta frase dizia que "os cinco relatos a imprimem", e
    isso era FALSO:** medidos em 22/10 as 04:4x, os chamadores sao DOIS — o
    `mira` e o `antes_do_render`. Dois e o numero CERTO, porque a passada ja
    imprime o aviso uma vez no topo e cinco copias nela seriam ruido. O que
    estava errado era so o numero escrito em prosa, que ninguem reconferia
    (753) — e por isso ele saiu daqui: quem o reconta contra o codigo e o teste.

    E `caminho=None` ganha UMA FRASE A MAIS, porque ali nao falta so o arquivo:
    falta o NOME. O `identidade` compara o `pacote` com o nome do arquivo, logo
    sem caminho ele nao tem contra o que comparar.
    """
    if not e_rascunho(caminho, spec):
        return ""
    base = ("  RASCUNHO: o arquivo ainda NAO esta no disco. O `similaridade` e o"
            " `variedade` varrem o acervo e nao veem esta peca, e o"
            " `identidade` confere o `pacote` contra um nome que ainda nao"
            " existe — as tres respostas sao validas e INCOMPLETAS. Grave a"
            " spec e rode o `prontidao` inteiro antes do render.")
    if caminho is None:
        base += ("\n  E SEM CAMINHO falta tambem o NOME: o `identidade` compara"
                 " o `pacote` com o nome do ARQUIVO, logo aqui ele nao tem"
                 " contra o que comparar. Passe o caminho PRETENDIDO quando"
                 " quiser essa conferencia — ele e nome, nao arquivo.")
    return base
