# -*- coding: utf-8 -*-
"""O dono da pergunta "esta peca tem longo?" PARA QUEM DECIDE O QUE PUBLICAR.

Ela decide coisas diferentes em lugares diferentes — o `etapas.py` pula as
etapas 1.5 a 7 por causa dela, e o `confere_token.py` exige um escopo do Google
por causa dela — e ate 21/10/2026 cada lugar a respondia por conta propria com
a mesma expressao escrita de novo. Dois donos da mesma regra e a assinatura que
congelou a legenda do short (09/10 no `fabrica.py`, 19/10 no `etapas.py`),
parou a mira de conferir por seis pecas (19/10 as 05:2x) e pos job inventado na
serie. O pretexto de nao haver dono era o tamanho: `not sp.get("longo")` cabe
numa linha, e por isso ninguem a chamou de regra.

MEDIDO no disco em 21/10: **256** specs sao short solto e **140** tem longo, de
396. Logo a distincao nao e um caso de borda — e a maioria do parque.

**E O ALCANCE DESTE DONO VAI MEDIDO em vez de prometido, porque "UM dono" seria
falso na escala da frota:** a chave `longo` e lida como RAMO em **20** lugares de
**12** modulos, e como default (`or []`) em outros **23**. Este arquivo e o dono
dos DOIS que decidem o que a peca PUBLICA — o `etapas.py` (que caminho de render
tomar) e o `confere_token.py` (que escopo do Google exigir) —, porque sao esses
dois que, discordando, produzem peca publicada errada. Os outros dezoito ramos
seguem respondendo sozinhos, e isso fica DECLARADO como divida em vez de
anunciado como consertado; o teste reconfere a contagem contra o disco para ela
nao envelhecer calada (753).
"""


def tem_longo(sp):
    """True quando a spec declara cenas de longo.

    `longo: []` e `longo` ausente sao a MESMA coisa aqui, de proposito: as duas
    formas existem no disco e as duas significam short solto.
    """
    return bool((sp or {}).get("longo"))


def so_short(sp):
    """True para short solto — o inverso de `tem_longo`, com o nome do render.

    Existe porque o `etapas.py` fala em `SO_SHORT` e o `confere_token.py` fala
    em "tem longo": sao a mesma pergunta, e ter os dois nomes apontando para a
    MESMA funcao e o que impede que amanha um deles responda diferente.
    """
    return not tem_longo(sp)
