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


def modos() -> set:
    """O CONJUNTO de modos que o `modo_de_fechamento` devolve, DERIVADO dele.

    Existe porque o `leitura_de_inscritos` passou a dizer, ao lado do veredito
    de janela, qual e o modo MEDIDO da rota — e listar os nomes la seria o
    SEGUNDO dono deles. Derivar e a mesma disciplina do
    `layouts_do_short.desenham()`, que SONDA o render em vez de guardar lista:
    modo novo entra aqui sozinho no instante em que a funcao passa a devolve-lo,
    e modo inventado do lado de fora nao passa pela conferencia.

    A leitura e por AST sobre a propria funcao, e nao por regex na prosa: o
    docstring dela CITA os nomes para se explicar, e casar prosa pegaria a
    explicacao em vez do codigo — a razao pela qual os testes desta semana sao
    por AST.
    """
    import ast

    with open(__file__, encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "modo_de_fechamento"]
    if not alvo:
        raise RuntimeError("modo_de_fechamento nao encontrado: o dono mudou de nome")
    saida = set()
    # Todo literal de texto dentro de um `return` e um valor devolvido — num
    # ternario os DOIS ramos sao, e foi exatamente isso que a primeira versao
    # do teste do AST perdeu em 19/10 as 23:4x.
    for no in ast.walk(alvo[0]):
        if isinstance(no, ast.Return) and no.value is not None:
            for dentro in ast.walk(no.value):
                if isinstance(dentro, ast.Constant) and isinstance(dentro.value, str):
                    saida.add(dentro.value)
    return saida


def modo_de_fechamento(corpo: str, location: str = "",
                       neutro_respondeu: bool | None = None,
                       sonda_pode_gravar: bool | None = None,
                       politica_negou: bool | None = None) -> str:
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

    **E O `neutro_respondeu=False` ERA ELE MESMO INSUFICIENTE — medido em 20/10
    as 09:3x, na decima primeira rodada seguida em que eu escrevia
    `sem_egresso`.** A sonda e `curl -s -o ARQ -w '%{http_code}'`, e quando o
    `-o` nao consegue ABRIR o arquivo o curl sai em 23 e o `%{http_code}`
    imprime **000** — o MESMO 000 que este ramo le como "a rede nao sai". Na
    primeira sonda desta rodada o destino era `/tmp/o.html` num sandbox onde
    aquele caminho nao existe, e os TRES hosts (o neutro inclusive) voltaram
    000. Isto e: *"a rede nao sai"* e *"a resposta nao tinha onde ser gravada"*
    sao **indistinguiveis pelo 000 sozinho**.

    **O discriminador e um CONTROLE DE ESCRITA na mesma chamada** — um `touch`
    no mesmo diretorio —, e ele e tao barato quanto o host neutro. Refeita a
    sonda com destino gravavel, o `touch` passou e o arquivo da resposta
    **continuou nao existindo**: logo o curl nunca recebeu resposta, e ai sim
    `sem_egresso` esta medido. Sem esse controle este ramo devolve
    `indeterminado`, do jeito que o `porta1` recusa janela curta.

    **O que isto RETRATA, e vai dito:** o rotulo `sem_egresso` que eu escrevi
    nas rodadas anteriores foi afirmado sem esse controle. **A CONSEQUENCIA
    daquelas rodadas nao muda** — nao havia leitura, logo nao havia ponto de
    residuo e a peca foi parqueada —, o que cai e a certeza sobre a CAUSA.

    **E O `sem_egresso` ERA ELE MESMO DOIS MODOS — medido em 20/10 as 11:4x, no
    container desta sessao.** Com o controle de escrita passando (`escrita OK`),
    os TRES hosts — a peca, o controle e o NEUTRO `example.com` — voltaram 000
    sem arquivo, que por este ramo le `sem_egresso`, isto e *"a minha rede nao
    sai"*. **O proxy do proprio ambiente diz outra coisa**, e diz nomeando o
    host: o `__agentproxy/status` lista `www.youtube.com:443` **e**
    `example.com:443` em `recentRelayFailures` com
    `"gateway answered 403 to CONNECT (policy denial or upstream failure)"`.

    **Logo o 000 em TODOS os hosts, inclusive o neutro, nao estabelece ausencia
    de rede: ele e compativel com uma POLITICA que nega todo CONNECT — e esse e
    o quinto modo, `negado_por_politica`.** A
    consequencia pratica e a mesma — nao ha leitura, logo nao ha ponto de
    residuo e a peca vai parqueada —, e o REMEDIO e diferente, que e a mesma
    razao pela qual `limite` e `consentimento` vivem separados: negacao por
    politica e do dono (a tela de Network access, a mesma dos quatro hosts
    institucionais); rede ausente nao se conserta.

    **O discriminador e o STATUS DO PROPRIO PROXY na mesma rodada** — ele nomeia
    o host e o motivo —, e sem ele este ramo devolve `indeterminado` em vez de
    escolher, do jeito que o `porta1` recusa janela curta. **Isto RETRATA o
    rotulo `sem_egresso` que eu escrevi nas rodadas anteriores, inclusive a das
    09:3x**: o controle de escrita estabeleceu que a resposta tinha onde ser
    gravada, e NAO que a causa fosse ausencia de rede. **E a mesma classe do
    09:3x uma camada para fora** — o 000 segue ambiguo, agora entre rede ausente
    e politica que nega.

    **O que isto NAO muda:** o discriminador do 17/10 continua sendo a peca de
    CONTROLE. Saber o modo nao substitui reler o controle, porque nos modos de
    rota a leitura da peca nova vem vazia do mesmo jeito.
    """
    if SORRY in (location or "") or SORRY in (corpo or ""):
        return "limite"
    if not (corpo or "").strip():
        # NENHUMA pagina voltou. Isto nao e a parede do CONSENT, que vem com
        # 1,2 MB, e nao e recusa do YouTube: pode ser o sandbox sem egresso.
        if neutro_respondeu is None or neutro_respondeu:
            return "indeterminado"
        # O neutro calou. Isso SO vira `sem_egresso` com o controle de ESCRITA
        # da propria sonda: sem ele, 000 tambem e "a resposta nao tinha onde
        # ser gravada" (medido em 20/10 as 09:3x).
        if not sonda_pode_gravar:
            return "indeterminado"
        # O neutro calou E a resposta tinha onde ser gravada. Falta UMA coisa:
        # de QUEM e o silencio. O proxy do ambiente nega CONNECT por POLITICA
        # tambem para o host neutro (medido em 20/10 as 11:4x), logo sem essa
        # leitura os dois modos sao indistinguiveis.
        if politica_negou is None:
            return "indeterminado"
        if politica_negou:
            return "negado_por_politica"
        return "sem_egresso"
    if duracao_do_html(corpo) is None:
        return "consentimento"
    return "aberta"


def politica_negou_hosts(hosts, desde: str, status: dict | None = None) -> dict:
    """O `politica_negou` do `modo_de_fechamento` deixa de ser conta minha.

    POR QUE EXISTE (21/10, 19:2x): o quinto modo (`negado_por_politica`, medido
    em 20/10 as 11:4x) depende de o PROXY nomear o host, e esse argumento eu
    vinha passando A MAO — um `curl $HTTPS_PROXY/__agentproxy/status` com um
    `python3 -c` e uma FATIA escrita na hora. **Nesta rodada eu errei a fatia.**

    **A lista `recentRelayFailures` e OLDEST-FIRST e truncada nas 20 ultimas**
    (medido: 20 entradas, da mais velha as 18:43 a mais nova as 19:07). Logo
    `[:3]` le as MAIS VELHAS. As 18:20 isso acertou por sorte, porque o buffer
    estava curto e as tres primeiras eram da minha propria sonda; as 19:08
    devolveu tres `sb:443` de 18:43 — de outra rodada — e eu quase li isso como
    *"o proxy nao nomeou o YouTube nesta rodada"*, que daria `sem_egresso` onde
    o modo e `negado_por_politica`.

    **Sao DOIS erros numa fatia so, e o segundo e pior:** ela pega a ponta
    errada da lista, e ela nao tem INSTANTE — negacao de uma rodada anterior
    conta como medicao desta. Por isso `desde` e obrigatorio.

    AUSENCIA DE ENTRADA NAO E PERMISSAO: a lista e truncada, logo nao ter o
    host nela nao prova que a politica deixou passar. Nesse caso devolve
    `negou: None`, e o `modo_de_fechamento` ja trata None como `indeterminado`
    — do jeito que o `porta1` recusa janela curta. Isto e a licao de 17/10:
    instrumento que devolve vazio nao prova ausencia.

    `status` existe para o teste injetar o JSON; sem ele a funcao le o proxy.
    """
    if status is None:
        status = _status_do_proxy()
    if not isinstance(status, dict):
        return {"negou": None, "motivo": "status do proxy ilegivel",
                "hosts_nomeados": [], "mais_novo": None}
    falhas = status.get("recentRelayFailures") or []
    alvo = {str(h).split(":")[0] for h in (hosts or [])}
    # A lista e oldest-first: a ponta NOVA e o fim dela. Nao se fatia pelo
    # comeco, e e por isso que esta funcao existe.
    recentes = [f for f in falhas
                if str(f.get("ts") or "") >= str(desde)
                and str(f.get("host") or "").split(":")[0] in alvo]
    nomeados = sorted({str(f.get("host") or "").split(":")[0]
                       for f in recentes})
    mais_novo = max((str(f.get("ts") or "") for f in falhas), default=None)
    if not recentes:
        return {"negou": None,
                "motivo": ("nenhuma falha dos hosts %s depois de %s na lista do "
                           "proxy — e ela e TRUNCADA nas 20 ultimas, logo isto "
                           "NAO prova que a politica deixou passar"
                           % (sorted(alvo), desde)),
                "hosts_nomeados": [], "mais_novo": mais_novo}
    rejeitadas = [f for f in recentes
                  if "connect" in str(f.get("kind") or "").lower()
                  or "403" in str(f.get("detail") or "")]
    if not rejeitadas:
        return {"negou": None,
                "motivo": ("o proxy nomeou %s depois de %s, mas nenhuma entrada "
                           "e recusa de CONNECT — a causa e outra"
                           % (nomeados, desde)),
                "hosts_nomeados": nomeados, "mais_novo": mais_novo}
    return {"negou": True,
            "motivo": ("o proxy negou o CONNECT para %s depois de %s (%d "
                       "entrada(s))" % (nomeados, desde, len(rejeitadas))),
            "hosts_nomeados": nomeados, "mais_novo": mais_novo}


def _status_do_proxy() -> dict | None:
    """Le o `__agentproxy/status`. Falha de leitura devolve None, nao {}.

    Dicionario vazio passaria pela funcao acima como "nenhuma falha listada", e
    ai falha de LEITURA viraria ausencia de NEGACAO — a confusao que o
    `politica_negou_hosts` existe para desfazer.
    """
    import json as _json
    import os as _os
    import subprocess as _sub
    base = _os.environ.get("HTTPS_PROXY") or _os.environ.get("https_proxy")
    if not base:
        return None
    try:
        r = _sub.run(["curl", "-sS", "%s/__agentproxy/status" % base.rstrip("/")],
                     capture_output=True, text=True, timeout=20)
        if r.returncode != 0 or not (r.stdout or "").strip():
            return None
        return _json.loads(r.stdout)
    except Exception:
        return None


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


def main(argv=None) -> int:
    """`python3 fabrica/vivacidade_publica.py <desde> [host ...]`.

    Existe para a rodada nao reescrever a fatia na linha de comando: foi a fatia
    escrita a mao que leu a ponta VELHA da lista do proxy em 21/10 as 19:0x.
    Codigo de saida sempre ZERO: isto informa, nao reprova.
    """
    import sys as _sys
    argv = list(argv if argv is not None else _sys.argv[1:])
    if not argv:
        print("uso: vivacidade_publica.py <desde ISO-8601> [host ...]")
        print("  ex: vivacidade_publica.py 2026-10-21T19:18:00Z"
              " www.youtube.com example.com")
        return 0
    desde = argv[0]
    hosts = argv[1:] or ["www.youtube.com", "example.com"]
    r = politica_negou_hosts(hosts, desde)
    print("POLITICA NEGOU o CONNECT? %s" % r["negou"])
    print("  %s" % r["motivo"])
    print("  mais nova entrada na lista do proxy: %s" % r["mais_novo"])
    print("  a lista e OLDEST-FIRST e truncada nas 20 ultimas — ausencia de"
          " entrada NAO e permissao (17/10).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
