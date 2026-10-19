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


# A peca de CONTROLE que separa "rota fechada" de "peca nao indexada".
# Medido em 17/10 as 03:1x: o `O5o2SnovdEo`, publicado dois minutos antes,
# devolveu 200 com 1.219.721 bytes e ZERO `lengthSeconds`. Sozinha, essa leitura
# e indistinguivel de peca que ainda nao indexou — e eu ia relatar isso.
CONTROLE_17_10 = ("OhrGlJvnBoM", 44)


# O modo de fechamento da rota da duracao. MEDIDO em 19/10 as 06:1x, e e um
# estado NOVO: ate aqui a tabela do `CLAUDE.md` so conhecia o
# "200 com 1,2 MB e zero `lengthSeconds`", a parede de consentimento — e ela
# nao se resolve com cookie, User-Agent de navegador nem `&hl=en` (os tres
# testados em 16/10). Nesta rodada a rota devolveu **302 para
# `google.com/sorry/index`** com 402 bytes de corpo, no `kLsLXWCeI8Q` e no
# controle `OhrGlJvnBoM` na mesma chamada — logo ROTA, nao peca.
SORRY = "google.com/sorry"


def modo_de_fechamento(corpo: str, location: str = "",
                       neutro_respondeu: bool | None = None) -> str:
    """Por que a rota da duracao fechou — 'limite', 'consentimento' ou 'aberta'.

    Os dois modos pedem coisas DIFERENTES de quem lê, e e por isso que vale
    separa-los em vez de contar os dois como "fechada":

      * `limite` (302 para `/sorry/index`): e recusa por VOLUME de requisicao.
        **HIPOTESE DECLARADA, e vai como hipotese:** as seis requisicoes que eu
        mesmo fiz nos sete minutos anteriores (tres `/about`, duas `/watch` e um
        `yt-dlp`) sao o candidato obvio a causa, e eu NAO medi isso — uma
        rodada nao separa a minha carga da carga de todo o resto que sai deste
        IP. O que esta medido e a sequencia: a rota deu 200 com 1,2 MB as 05:3x
        e 302 as 06:14. A consequencia pratica e barata e vale mesmo se a
        hipotese estiver errada: **gaste menos requisicao por rodada, e leia
        inscritos e duracao na MESMA passagem** em vez de uma por vez;
      * `consentimento` (200, pagina grande, zero campo): e a parede do
        `CONSENT`/`captcha`, e nao ha o que economizar — ela nao responde a
        volume nenhum.

    **E HA UM TERCEIRO MODO, medido em 19/10 as 23:4x: `sem_egresso`.** A
    leitura da peca nova e a do CONTROLE voltaram as duas com **HTTP 000 e ZERO
    byte** — e o `example.com`, na mesma chamada, tambem. Logo nao foi a rota do
    YouTube: foi o **sandbox sem rede**. Sem esse ramo esta funcao devolvia
    `consentimento` para corpo VAZIO — isto e, uma afirmacao sobre a parede do
    `CONSENT` do YouTube a partir de uma falha em que o YouTube nunca foi
    alcancado. A parede vem com **1,2 MB**; zero byte nao e parede nenhuma.

    **O discriminador e um HOST NEUTRO na mesma chamada**, e e tao barato quanto
    o da peca de controle: ele separa *"a minha rede nao sai"* de *"o YouTube
    nao me responde"*. Sem ele os dois sao indistinguiveis, e o ramo devolve
    `indeterminado` em vez de escolher — do jeito que o `porta1` recusa janela
    curta. **Nao existe aqui um modo "recusa do YouTube"**, porque esse caso
    (neutro responde e o YouTube nao) eu ainda nao medi; inventa-lo seria
    limiar sem procedencia.

    **O que isto NAO muda:** o discriminador do 17/10 continua sendo a peca de
    CONTROLE. Saber o modo nao substitui reler o controle, porque nos modos de
    rota a leitura da peca nova vem vazia do mesmo jeito.
    """
    if SORRY in (location or "") or SORRY in (corpo or ""):
        return "limite"
    if not (corpo or "").strip():
        # NENHUMA pagina voltou. Isto nao e a parede do CONSENT, que vem com
        # 1,2 MB, e nao e recusa do YouTube: pode ser o sandbox sem egresso.
        if neutro_respondeu is None:
            return "indeterminado"
        return "sem_egresso" if not neutro_respondeu else "indeterminado"
    if duracao_do_html(corpo) is None:
        return "consentimento"
    return "aberta"


def veredito_da_rota(leitura_nova, leitura_controle, valor_conhecido: int):
    """Diz se a rota FECHOU ou se a peca nova e que nao respondeu.

    MEDIDO em 17/10 as 03:1x. Zero `lengthSeconds` numa peca de dois minutos
    tem duas explicacoes que a leitura sozinha NAO separa: a rota fechou (o
    200-com-1,2-MB-e-cinco-CONSENT da tabela do `CLAUDE.md`) ou a peca ainda
    nao indexou (o caminho normal do 672/758). Escolher uma seria comparador
    escolhido sem medir — o efeito (C) da rotina.

    **O discriminador e uma peca de CONTROLE cujo valor eu JA medi.** Naquela
    rodada o `OhrGlJvnBoM` havia lido **44** uma hora antes e voltou **zero** na
    mesma chamada: peca de uma hora de vida nao "desindexa", logo o que mudou
    foi a ROTA. Se o controle tivesse respondido 44, a leitura vazia seria da
    peca nova e o 672 se aplicaria.

    `leitura_nova` e `leitura_controle` sao o que `duracao_do_html` devolveu
    (int ou None). Devolve 'rota_fechada', 'peca_sem_leitura', 'ok' ou
    'controle_divergente' — este ultimo quando o controle responde um valor
    DIFERENTE do conhecido, que nao e caso previsto e nao se resolve calando.
    """
    if leitura_controle is None:
        return "rota_fechada"
    if leitura_controle != valor_conhecido:
        return "controle_divergente"
    if leitura_nova is None:
        return "peca_sem_leitura"
    return "ok"


def relato_da_rota(leitura_nova, leitura_controle, valor_conhecido: int,
                   id_novo: str = "<id>") -> str:
    v = veredito_da_rota(leitura_nova, leitura_controle, valor_conhecido)
    if v == "rota_fechada":
        return ("ROTA DA DURACAO FECHADA: o controle, cujo valor medido e"
                f" {valor_conhecido} s, voltou VAZIO. Logo a leitura vazia de"
                f" {id_novo} NAO diz nada sobre a peca — nao ha ponto de residuo"
                " nesta rodada, e isso vai dito em vez de virar acusacao.")
    if v == "controle_divergente":
        return (f"CONTROLE DIVERGENTE: esperava {valor_conhecido} s e veio"
                f" {leitura_controle}. Nao e caso previsto — releia antes de"
                " concluir qualquer coisa sobre a rota ou sobre a peca.")
    if v == "peca_sem_leitura":
        return (f"A ROTA RESPONDE (controle = {valor_conhecido} s) e"
                f" {id_novo} veio vazio: aqui o 672/758 se aplica — peca nova"
                " pode estar indexando. Releia, nao acuse.")
    return f"rota aberta e {id_novo} leu {leitura_nova} s."
