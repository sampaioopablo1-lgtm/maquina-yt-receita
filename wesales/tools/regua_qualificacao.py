"""Regua de qualificacao 0-100 (build-wesales.md, secao 9.1).

Fica num modulo proprio porque e usada em dois lugares: o
`Pós-agendamento v2` e o teste isolado que prova que ela soma certo.
Duplicar a tabela seria a maneira mais facil de as duas divergirem.

Rotulos sao os que `locations_get-custom-fields` devolve - nunca os que
pareceram razoaveis. Um If/Else contra rotulo inexistente nunca casa e a
regua pontuaria errado sem nenhum erro visivel.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghl_api as g

# (campo, [(valor exato na tela, pontos)])
REGUA = [
    ("Clientes novos por mês", [("10", 3), ("11-30", 6), ("31-100", 8),
                                ("+101", 10)]),
    ("Tem time comercial", [("Só dono", 3), ("1-5", 7), ("6-10", 9),
                            ("+10", 10)]),
    ("Quem atende os leads", [("Ninguém fixo", 10), ("Dono", 7),
                              ("Vendedor", 5), ("SDR", 3)]),
    ("Investe em anúncios", [("Sim", 13), ("Já investiu e parou", 9),
                             ("Nunca", 4)]),
    ("Investimento mensal em anúncios", [("Acima de 10k", 12),
                                         ("5k a 10k", 10), ("1k a 5k", 6),
                                         ("Até 1k", 2)]),
    ("Budget", [("Tem", 15), ("Precisa aprovar", 9), ("Não tem", 0)]),
    ("Decisor", [("Sim", 15), ("Influencia", 8), ("Não decide", 2)]),
    ("Prazo", [("Pra ontem", 15), ("Espera 30 dias", 11), ("Este ano", 6),
               ("Sem prazo", 2)]),
    # G-04 resolvido sem remapear formulario: o Meta Lead Ads grava a
    # resposta de prazo em `Urgência`, nao em `Prazo` (confirmado no lead
    # real Carlos Andrade, 21/09/2026: Urgência='Pra ontem', Prazo vazio).
    # Os rotulos sao os MESMOS, entao basta um bloco de reserva logo depois.
    # A estrutura ja garante que so um dos dois pontua: se `Prazo` casar, o
    # ramo salta por cima deste bloco. Maximo continua 100.
    ("Urgência", [("Pra ontem", 15), ("Espera 30 dias", 11), ("Este ano", 6),
                  ("Sem prazo", 2)]),
]


def _raiz(passos):
    p = passos[0]
    return p.id if isinstance(p, g.Branch) else p["id"]


def pontuar(rotulo, campo_id, opcoes, proximo, fim_id, nota_id):
    """Cadeia de If/Else de um campo: casou, soma e salta para o proximo.

    O proximo campo MORA no ramo 'nao' da ultima opcao. Encadear so por
    goto deixaria os campos seguintes fora do grafo.
    """
    destino = _raiz(proximo) if proximo else fim_id
    atual = list(proximo) if proximo else [g.goto_step(fim_id)]
    for valor, pts in reversed(opcoes):
        sim = []
        if pts:
            sim.append(g.math_step(nota_id, "add", pts))
        sim.append(g.goto_step(destino))
        atual = [g.Branch("%s = %s?" % (rotulo, valor),
                          [g.cond("contact_detail", campo_id, "==", valor)],
                          sim=sim, nao=atual)]
    return atual


def montar_regua(campos, nota_id, fim_id, fim_node=None):
    """Zera a nota e devolve a arvore inteira da regua.

    `fim_id` e para onde todo ramo que casou salta. Se `fim_node` vier, ele
    MORA no ramo mais interno (caso em que a regua e o grafo inteiro); se
    nao vier, o no final ja existe em outro lugar do grafo e o ramo mais
    interno so salta para la.
    """
    arvore = [fim_node] if fim_node else []
    for rotulo, opcoes in reversed(REGUA):
        arvore = pontuar(rotulo, campos[rotulo]["id"], opcoes, arvore,
                         fim_id, nota_id)
    zera = g.field_step(nota_id, "Nota de qualificação", 0, "numerical")
    return [zera] + arvore


def esperado(contato_campos, campos):
    """Calcula na mao a nota que a regua deveria dar, para conferir."""
    por_id = {v["id"]: k for k, v in campos.items()}
    valores = {por_id.get(c["id"]): c.get("value")
               for c in contato_campos if por_id.get(c["id"])}
    total, detalhe = 0, []
    for rotulo, opcoes in REGUA:
        v = valores.get(rotulo)
        pts = dict(opcoes).get(v)
        if pts is not None:
            total += pts
            detalhe.append("%s=%s (+%d)" % (rotulo, v, pts))
        else:
            detalhe.append("%s=%r (sem pontos)" % (rotulo, v))
    return total, detalhe
