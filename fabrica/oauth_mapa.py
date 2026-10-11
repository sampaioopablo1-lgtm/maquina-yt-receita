#!/usr/bin/env python3
"""Normaliza o segredo `YT_OAUTH_JSON`, porque o copiar do SQL Editor EMBRULHA.

MEDIDO EM 11/10/2026, run `38175092152`. O dono colou o segredo e a sonda leu
`YT_OAUTH_JSON: presente (1116 chars)` seguido de **"tem 1 canal(is)"** — com os
tres canais dentro. O valor nao estava errado: estava EMBRULHADO pelo jeito que
o painel do Supabase copia uma linha de resultado,

    [ { "jsonb_pretty": "{\\n  \\"kolejny-poziom\\": { ... } }" } ]

que e um JSON valido com UMA chave cujo valor e o JSON de verdade em texto. O
`json.loads` aceita, o mapa fica com um unico canal chamado `jsonb_pretty`, e os
tres canais da frota saem como "FORA do YT_OAUTH_JSON". **O defeito nao era do
dono nem do segredo — era nosso, por exigir uma edicao manual de texto que a
maquina sabe fazer.** Instrucao de edicao a mao e instrucao que falha.

Esta funcao desembrulha as tres formas que o painel produz e devolve sempre o
mapa `{canal: {...}}`. Ela NAO valida credencial e NAO imprime nada.
"""

from __future__ import annotations

import json

# Mais que isto e sinal de embrulho aninhado de proposito, nao de copiar e colar.
MAX_CAMADAS = 4


def desembrulha(texto: str) -> dict:
    """Devolve o mapa `{canal: {...}}` a partir do que o dono colou.

    Aceita, alem do formato limpo:
      * `[{"jsonb_pretty": "<json>"}]` — linha de resultado copiada inteira;
      * `{"jsonb_pretty": "<json>"}`  — a mesma coisa sem o colchete;
      * qualquer chave de uma coluna so, porque o nome dela muda com o `select`.

    Levanta `ValueError` se nao sobrar um objeto JSON.
    """
    valor = json.loads(texto)
    for _ in range(MAX_CAMADAS):
        # Uma linha de resultado vem como lista de um elemento.
        if isinstance(valor, list) and len(valor) == 1:
            valor = valor[0]
            continue
        # Uma coluna so, cujo conteudo e o JSON em texto.
        if isinstance(valor, dict) and len(valor) == 1:
            unico = next(iter(valor.values()))
            if isinstance(unico, str):
                try:
                    valor = json.loads(unico)
                except ValueError:
                    break
                continue
        break
    if not isinstance(valor, dict):
        raise ValueError("YT_OAUTH_JSON nao reduz a um objeto JSON")
    return valor
