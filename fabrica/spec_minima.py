# -*- coding: utf-8 -*-
"""As guardas que eu reescrevia em TODO builder — e a que eu nunca escrevi.

POR QUE ISTO EXISTE (21/10/2026). Cada peca nasce de um builder descartavel no
rascunho, e eu copiava para dentro dele, a mao, dois `assert`: uma frase por
cena e layout dentro do conjunto SONDADO. **O terceiro limite — as palavras da
thumbnail — eu nunca assertei, e ele falhou CINCO vezes nesta sessao**:
`kolejny-poziom-s071` (19/10 as 22:1x), a primeira versao da `s089`, a `s075`,
a primeira versao da `s098` e a primeira versao da `s099`. Nas cinco quem pegou
foi o portao ou o `antes_do_render`, DEPOIS de a peca estar escrita.

Cinco vezes a mesma assinatura e o item 3 da §10: todo numero que eu confiro de
cabeca vira um erro meu. E a quarta guarda e a que **nenhum portao tem**: a
chave `longo` ausente, que em 18/10 matou o run 39110638169 com `KeyError` DEPOIS
de instalar o ffmpeg e baixar as tres trilhas — ausencia de chave nao e valor
vazio.

**TODOS OS LIMITES SAO LIDOS DOS DONOS** — `variedade.THUMB_MAX_PALAVRAS`,
`narracao.frases`, `layouts_do_short.desenham()`. Copiar qualquer um aqui
criaria o segundo dono, que e a assinatura que congelou a legenda.

**ISTO NAO E PORTAO E NAO VALE PARA O ACERVO, e o numero vem antes da decisao.**
Medido no disco em 21/10, sobre as 398 specs com short:

| guarda | quantas specs do acervo REPROVARIAM |
|---|---|
| thumbnail acima de 4 palavras | **87** |
| alguma cena com != 1 frase | **216** |
| layout que o retrato nao desenha | **1** |
| sem a chave `longo` | **0** |

As 216 dizem o essencial: **uma frase por cena e regra da geracao ATUAL**, nao
do parque. Logo isto e uma guarda de ESCRITA — para a spec que esta nascendo —,
e transformar em portao reprovaria mais da metade do acervo, que e o argumento
pelo qual o `mira.py` tambem nao e portao. Quem reprova thumbnail e layout
continua sendo o `prontidao`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import layouts_do_short as LS      # noqa: E402  — DONO do conjunto que DESENHA
import narracao as NR              # noqa: E402  — DONO da contagem de frases
import variedade as V              # noqa: E402  — DONO do limite da thumbnail


def palavras_da_thumb(thumb) -> int:
    """As duas linhas somadas, do jeito que o portao conta."""
    t = thumb or {}
    return len(("%s %s" % (t.get("l1") or "", t.get("l2") or "")).split())


def confere(spec) -> list:
    """Devolve a LISTA de problemas da spec que esta sendo ESCRITA.

    Lista vazia quer dizer que as quatro guardas passaram. Ela NAO levanta: quem
    levanta e o `exige`, para que um chamador possa relatar em vez de morrer.
    """
    sp = spec or {}
    problemas = []

    if "longo" not in sp:
        problemas.append(
            "sem a chave `longo` — ausencia de chave NAO e valor vazio, e foi "
            "isto que matou o run 39110638169 com KeyError depois do render "
            "comecar. Short solto leva `longo: []`.")

    n = palavras_da_thumb(sp.get("thumb"))
    if n > V.THUMB_MAX_PALAVRAS:
        problemas.append(
            "thumbnail com %d palavras somando as duas linhas e o limite e %d "
            "(lido de `variedade.THUMB_MAX_PALAVRAS`) — o portao `variedade` "
            "REPROVA isto, e nesta sessao ele reprovou CINCO vezes"
            % (n, V.THUMB_MAX_PALAVRAS))

    idioma = (sp.get("idioma") or "pt")[:2]
    desenha = LS.desenham()
    for i, c in enumerate(sp.get("short") or []):
        frases = len(NR.frases(c.get("nar") or "", idioma))
        if frases != 1:
            problemas.append(
                "cena %d tem %d frases: `P` e por FRASE (11/10), e duas frases "
                "numa cena tiram a peca da faixa com a MESMA media de "
                "caracteres" % (i, frases))
        if c.get("layout") not in desenha:
            problemas.append(
                "cena %d usa layout %r que o retrato do SHORT NAO desenha "
                "(sondado: %s) — cena em branco no ar foi o que a `s069` "
                "publicou em 19/10" % (i, c.get("layout"), sorted(desenha)))
    return problemas


def exige(spec) -> None:
    """Levanta com TODOS os problemas de uma vez.

    De uma vez de proposito: levantar no primeiro esconde os outros e faz a
    escrita ir de erro em erro — foi assim que a `s099` levou duas passadas.
    """
    problemas = confere(spec)
    if problemas:
        raise AssertionError(
            "a spec nao passa nas guardas de ESCRITA (%d):\n  - %s"
            % (len(problemas), "\n  - ".join(problemas)))
