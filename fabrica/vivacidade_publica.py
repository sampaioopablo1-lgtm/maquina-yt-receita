"""O PISO de vivacidade por rota PUBLICA — e por que ele NAO e `processed`.

A rotina manda contar **so peca `processed`** (666: eu afirmei "21 entregues" e
tive de retratar). Mas a condicao `processed` vive no `videos.list` com
`part=status`, que pede token OAuth, que pede `pg_net`, que pede o `execute_sql`
— negado em treze rodadas seguidas. Entao a pergunta "quantas pecas o dia
entregou de verdade" nao tem, hoje, a resposta que o alvo do dono exige.

O que EXISTE e um PISO, por duas rotas publicas que nao pedem credencial:

  1. `watch?v=<id>` -> `lengthSeconds`. **Duracao presente e maior que zero
     NEGA o `P0D`**, que e a forma de morte que o 665 descreve. A pagina pode
     trazer DOIS valores diferentes: vale o MAIOR (medido em 16/10, 41 e 42 na
     mesma peca).
  2. `oembed` -> HTTP 200. Peca privada, removida ou inexistente nao responde
     200 ali, logo 200 e evidencia de que ela esta PUBLICA e indexada.

**E o que este modulo NAO afirma, porque seria o §3.8:** que a peca esta
`processed`. As duas rotas juntas dizem "nao esta P0D e esta publica", e isso e
estritamente mais fraco. Uma peca pode estar indexada e ainda assim com
`uploadStatus` fora de `processed` — o 758 mediu exatamente isso, `uploaded` com
`duration: PT27S` aos dois minutos de vida. Por isso o nome e `piso` e o relato
diz, em letra, o que falta medir.

Medido em 16/10 as 20:2x nas 22 pecas publicadas no dia: **22 de 22** com duracao
maior que zero e oembed 200. Nenhuma `P0D`.
"""
from __future__ import annotations

ROTA_DURACAO = "https://www.youtube.com/watch?v={id}"
ROTA_PUBLICA = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={id}&format=json"

# O que o piso NAO cobre, nomeado para nao sumir do relato.
FALTA_MEDIR = "uploadStatus == 'processed' (pede token, logo pede o execute_sql)"


def duracao_do_html(html: str) -> int | None:
    """O MAIOR `lengthSeconds` da pagina, ou None se o CAMPO nao vier.

    Conta o CAMPO, nunca o codigo HTTP: a rota da duracao ja fechou com 200 e
    1,2 MB sem nenhum `lengthSeconds` (tabela de rotas do CLAUDE.md).
    """
    import re

    vals = [int(v) for v in re.findall(r'"lengthSeconds":"(\d+)"', html or "")]
    return max(vals) if vals else None


def veredito(duracao: int | None, http_oembed: int | None) -> str:
    """`viva` / `P0D` / `nao_publica` / `sem_leitura`, nesta ordem de forca.

    `sem_leitura` NAO e um defeito da peca — e a ausencia do campo, que o
    CLAUDE.md manda tratar como rota fechada e nao como canal vazio.
    """
    if duracao is None:
        return "sem_leitura"
    if duracao <= 0:
        return "P0D"
    if http_oembed != 200:
        return "nao_publica"
    return "viva"


def piso(leituras: dict) -> dict:
    """{id: (duracao, http)} -> contagem por veredito, mais a lista dos nao-vivos.

    Ele conta o que a rota publica sustenta, e nada alem. `sem_leitura` fica
    SEPARADO dos defeitos, porque somar os dois transformaria rota fechada em
    peca morta — que e o erro de enquadramento mais caro deste projeto.
    """
    if not leituras:
        raise ValueError(
            "AUSENCIA DE LEITURA: dicionario vazio nao e 'zero pecas vivas'. "
            "Sonde as rotas antes de concluir.")
    fora: dict[str, list] = {}
    for yid, (dur, http) in leituras.items():
        fora.setdefault(veredito(dur, http), []).append(yid)
    return {k: sorted(v) for k, v in fora.items()}


def relato(leituras: dict) -> str:
    por = piso(leituras)
    vivas = len(por.get("viva", []))
    linhas = [f"PISO DE VIVACIDADE: {vivas} de {len(leituras)} com duracao > 0 e "
              f"oembed 200."]
    for chave, titulo in (("P0D", "em P0D (defeito, 665)"),
                          ("nao_publica", "sem oembed 200"),
                          ("sem_leitura", "SEM o campo lengthSeconds (rota, nao peca)")):
        if por.get(chave):
            linhas.append(f"  {titulo}: {', '.join(por[chave])}")
    linhas.append(f"  e isto e um PISO: falta medir {FALTA_MEDIR}.")
    return "\n".join(linhas)
