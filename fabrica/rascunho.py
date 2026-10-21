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


def spec_de(caminho: str, spec: dict | None = None) -> dict:
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
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def e_rascunho(caminho: str, spec: dict | None = None) -> bool:
    """O arquivo ainda nao esta no disco, logo a varredura do acervo nao o ve."""
    import os
    return spec is not None and not os.path.exists(caminho)


def aviso_do_rascunho(caminho: str, spec: dict | None = None) -> str:
    """A frase que NOMEIA o que o rascunho nao alcanca. Vazia quando nao e um.

    Ela tem UM dono porque os cinco relatos a imprimem, e cinco copias dela
    seria a assinatura que congelou a legenda.
    """
    if not e_rascunho(caminho, spec):
        return ""
    return ("  RASCUNHO: o arquivo ainda NAO esta no disco. O `similaridade` e o"
            " `variedade` varrem o acervo e nao veem esta peca, e o"
            " `identidade` confere o `pacote` contra um nome que ainda nao"
            " existe — as tres respostas sao validas e INCOMPLETAS. Grave a"
            " spec e rode o `prontidao` inteiro antes do render.")
