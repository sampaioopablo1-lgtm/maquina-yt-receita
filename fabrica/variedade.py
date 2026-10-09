#!/usr/bin/env python3
"""O portao que faltava: o que o YouTube chama de conteudo INAUTENTICO.

POR QUE ESTE ARQUIVO EXISTE (09/10/2026). O dono trouxe o "Mapa do Canal Dark
com IA" (ianofacil.com.br) e pediu para aplicar. Das oito etapas do mapa a
maquina ja faz as oito, e com mais portao do que o mapa pede — mas tres itens
dele apontam para coisas que a maquina NAO olhava, e um deles e o portao mais
caro de todos, porque o que ele arrisca nao e view, e a propria monetizacao.

=============================================================================
O QUE EU VERIFIQUEI, porque o mapa erra a data e a natureza da regra
=============================================================================
O mapa diz: "o YouTube desmonetiza conteudo feito em serie em cima de molde
(politica de conteudo inautentico, julho de 2025)". Conferi, e corrijo em dois
pontos:

  (1) NAO e proibicao nova. Em 15/07/2025 o YouTube RENOMEOU a regra que ja
      existia, de "repetitious content" para "inauthentic content". Conteudo
      repetitivo e feito em massa JA era ineligivel antes disso; o proprio
      liaison do YouTube chamou de atualizacao menor, de rotulo.
  (2) NAO e regra de remocao, e de ELEGIBILIDADE DO YPP. Para quem ja monetiza
      e risco de desmonetizar; para nos, que estamos tentando ENTRAR pela Porta
      1, e o portao em si. Ou seja: importa MAIS para esta maquina, nao menos.

A frase que opera, do texto oficial do YPP, e esta:
  "The substance of each video should be materially varied and deliver
   creative, educational, or other value."
O YouTube NAO define "mass produced" nem publicou lista exaustiva, e quase toda
a cobertura e secundaria. Entao o que este modulo faz NAO e prever enforcement
— e MEDIR o quanto a nossa saida e igual a si mesma, e dizer o numero.

=============================================================================
O NUMERO QUE ME FEZ ESCREVER ISTO
=============================================================================
Medido em 09/10/2026 nas specs da frota:

    39 de 39 shorts soltos tem a MESMA sequencia de layouts:
        titulo - titulo - titulo - titulo - cta

Trinta e nove de trinta e nove. Nao e tendencia, e identidade. A SUBSTANCIA
varia de verdade (origem diferente, aritmetica diferente, entrada errada
diferente) e o kicker do CTA tem TRINTA valores distintos nas 39 — a maquina ja
fazia metade do que o mapa pede, sem saber. O ESQUELETO e que nao varia nunca.

NAO AFIRMO que o esqueleto aciona a politica. Nao tenho esse dado, e inventar
causa aqui seria a decima nona vez que eu fabrico um achado com a assinatura do
item 8 da rotina. O que afirmo e mais modesto e suficiente: o risco e de nivel
CANAL e irreversivel, os testes que ele disputa sao de nivel VIEW, e eu estava
medindo zero sobre ele.

=============================================================================
POR QUE (a) AVISA E (b)/(c) REPROVAM
=============================================================================
O `esqueleto` AVISA e nao reprova, por uma razao de experimento e nao de
conveniencia: mudar o numero de cenas mexe no GANCHO VISUAL, e o experimento 33
(motion) esta com trava de intocado por 10 dias ou 15 shorts/canal justamente
para medir esse gancho. Reprovar hoje me obrigaria a quebrar a trava do 33 na
proxima peca. Entao fica medido, nomeado e PRE-REGISTRADO: variar o esqueleto e
o PRIMEIRO teste da fila quando o 33 fechar, passando na frente dos tres que
estao na espera (short de 22-26 s, broll na cena 1, matar os fades), porque
aqueles sao de view e este e do portao.

O `gancho` e a `thumb` reprovam, porque o conserto e reescrever uma linha antes
do render e custa zero ciclo.

=============================================================================
DE ONDE VEM CADA LIMIAR — e nenhum deles e meu
=============================================================================
  gancho  <= 12 palavras na PRIMEIRA FRASE da cena 1   (mapa, prompt 25)
  thumb   <= 4 palavras somando l1 e l2                (mapa, prompt 23)
  esqueleto: aviso a partir de 6 pecas iguais seguidas no canal

As duas primeiras sao do mapa, LITERALMENTE, e vao aqui com a fonte escrita
porque limiar sem procedencia e criterio que eu inventei. O 6 do esqueleto e
meu e por isso ele so AVISA: nao reprovo ninguem com numero que eu chutei.

Estado medido em 09/10/2026, para que o conserto nao pareca regressao:
  gancho: 14 de 39 shorts soltos passam de 12 palavras (mediana 9, max 21)
  thumb:  40 de 86 specs da frota passam de 4 palavras

Os portoes rodam em spec NOVA, entao nada disso reprova peca publicada.
"""
import glob
import json
import os
import re

# Fim de frase nas tres linguas da frota. O grego usa `;` como interrogacao e
# `;` (EROTIMATIKO) existe em texto antigo — ja me enganei uma vez com um
# `endswith("?")` que recusou titulo grego que ERA pergunta.
_FIM = re.compile(r"(?<=[.!?;;])\s")

GANCHO_MAX_PALAVRAS = 12   # mapa, prompt 25
THUMB_MAX_PALAVRAS = 4     # mapa, prompt 23
ESQUELETO_AVISA_EM = 6     # meu, e por isso so avisa


def esqueleto(cenas: list[dict]) -> str:
    """A assinatura estrutural de uma peca: a sequencia de layouts."""
    return "-".join(c.get("layout", "?") for c in cenas)


def primeira_frase(nar: str) -> str:
    return _FIM.split((nar or "").strip())[0] if nar else ""


# Cache do diretorio. Sem ele, uma varredura de N specs liga N leituras do
# diretorio inteiro — o portao ficaria O(N^2) e a varredura, que ja e lenta por
# causa da rasterizacao do `layout` e do `ortografia`, ficaria pior por minha
# causa. A chave guarda o arquivo a excluir fora: o filtro e por nome, depois.
_CACHE: dict[str, list[tuple[str, dict]]] = {}


def _todas(raiz: str) -> list[tuple[str, dict]]:
    if raiz not in _CACHE:
        saida = []
        for f in sorted(glob.glob(os.path.join(raiz, "fabrica", "specs", "*.json"))):
            try:
                saida.append((os.path.basename(f), json.load(open(f, encoding="utf-8"))))
            except Exception:
                continue
        _CACHE[raiz] = saida
    return _CACHE[raiz]


def _especs_do_canal(raiz: str, slug: str, exceto: str) -> list[dict]:
    return [d for nome, d in _todas(raiz)
            if nome != exceto and d.get("slug") == slug
            and d.get("short") and not d.get("longo")]


def analisa(spec: dict, raiz: str = ".", arquivo: str = "") -> tuple[list[str], list[str]]:
    """Devolve (erros, avisos).

    `erros` reprovam a spec. `avisos` vao no relatorio e nao reprovam.
    """
    erros: list[str] = []
    avisos: list[str] = []
    short = spec.get("short") or []

    # ---- (b) GANCHO, reprova. Mapa, prompt 25: prender em 1 segundo. -------
    if short:
        pri = primeira_frase(short[0].get("nar", ""))
        n = len(pri.split())
        if n > GANCHO_MAX_PALAVRAS:
            erros.append(
                f"gancho: a primeira frase da cena 1 tem {n} palavras e o limite "
                f"e {GANCHO_MAX_PALAVRAS} (mapa, prompt 25 — o gancho precisa "
                f"fechar no primeiro segundo). Frase: {pri!r}"
            )

    # ---- (c) THUMB, reprova. Mapa, prompt 23: 2 linhas, 4 palavras. --------
    th = spec.get("thumb") or {}
    palavras = (f"{th.get('l1', '')} {th.get('l2', '')}").split()
    if len(palavras) > THUMB_MAX_PALAVRAS:
        erros.append(
            f"thumbnail: {len(palavras)} palavras somando as duas linhas e o "
            f"limite e {THUMB_MAX_PALAVRAS} (mapa, prompt 23 — a linha 2 e a "
            f"palavra de impacto, e o teste e legibilidade a 20% do tamanho). "
            f"l1={th.get('l1')!r} l2={th.get('l2')!r}"
        )

    # ---- (a) ESQUELETO, so avisa. Politica de conteudo inautentico. --------
    if short and not spec.get("longo"):
        meu = esqueleto(short)
        irmas = _especs_do_canal(raiz, spec.get("slug", ""), arquivo)
        iguais = sum(1 for d in irmas if esqueleto(d["short"]) == meu)
        total = len(irmas)
        if total and iguais + 1 >= ESQUELETO_AVISA_EM:
            avisos.append(
                f"esqueleto: esta peca seria a {iguais + 1}a de "
                f"{total + 1} no canal com a MESMA sequencia de layouts "
                f"({meu}). O texto do YPP cobra que 'a substancia de cada video "
                f"seja materialmente variada'; a substancia aqui varia, o "
                f"esqueleto nao. Variar o esqueleto e o primeiro teste da fila "
                f"quando o experimento 33 fechar — ver o docstring deste modulo."
            )
    return erros, avisos
