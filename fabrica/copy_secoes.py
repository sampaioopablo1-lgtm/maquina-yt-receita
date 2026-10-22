# -*- coding: utf-8 -*-
"""O `comentario` da copy e um BALDE PEGA-TUDO — e eu NAO achei o discriminador.

O ACHADO, que e real e esta REPRODUZIDO (19/10 as 20:3x). Eu entreguei a copy
do `labtreinamento-s087` sem a secao `## COMENTARIO FIXADO` e sem a
`## HASHTAGS`. O portao `copy` reprovou UM problema — "sem hashtags" — e deu
VERDE no comentario, que tambem faltava. O motivo esta no `publicar.ler_copy`:
o ultimo ramo da classificacao de secoes e

    elif not comentario and not corpo.startswith("-"):
        comentario = corpo

isto e, a PRIMEIRA secao depois da descricao que nao casa com licenca,
capitulos, hashtags nem tags cai no comentario. Sem a secao propria, quem caiu
ali foi o bloco `## CONFIGURACOES DO STUDIO`:

    comentario: '# NOTA: `categoryId` aqui e DECLARATIVO ... privacyStatus:
                 public  defaultLanguage: pt-BR ...'

**Logo o bloco de configuracao do Studio iria ao ar como COMENTARIO FIXADO do
video, e a conferencia `if not cp.get("comentario")` do portao e INCAPAZ de
pegar isso** — ela pergunta se o balde esta cheio, e o pega-tudo sempre o
enche. Falha PERMISSIVA. Isso esta reproduzido por `vazamento_simulado` abaixo.

O BALDE NAO SE TIRA, e o motivo e anterior a mim: o comentario do proprio
`ler_copy` conta que em 25/08 a secao da LICENCA era descartada em silencio
pela ORDEM dos baldes, e que por isso ela passou a ser detectada pelo CONTEUDO
— "o titulo muda de spec para spec e de idioma para idioma".

=============================================================================
E AS TRES TENTATIVAS DE DISCRIMINADOR FALHARAM. Os numeros ficam aqui para que
a rodada seguinte NAO as repita.
=============================================================================

**(1) POR CABECALHO — e a medicao que a autorizou era CIRCULAR.** Eu varri as
specs do disco filtrando por `'## DESCRICAO' in copy`, contei "322 de 322
declaram cabecalho que comeca por COMENT" e liguei a conferencia no portao. A
suite reprovou **47 testes**. O filtro era o cabecalho em PORTUGUES, logo a
amostra NAO PODIA conter contraexemplo. Varrido sem filtro: **360** specs com
copy seccionada, **32** nao usam o cabecalho portugues, e o cabecalho do
comentario aparece como `KOMENTARZ`, `KOMENTARZ PRZYPIETY`, `KOMENTAR
DISEMATKAN`, `SXOLIO` (grego), `SABITLENEN YORUM`, `PINNED COMMENT` e em
devanagari. **E o 725 com vocabulario de um idioma reportado como medicao da
frota**, e o comentario do `ler_copy` ja dizia isso em letra.

**(2) PELAS CHAVES DO BLOCO DO STUDIO** (`privacyStatus`, `categoryId`,
`madeForKids`, `defaultLanguage`), que sao nomes de campo da API e nao
traduzem. Elas nao sao universais entre GERACOES: **183 das 360** specs nao tem
as quatro. Discriminador que depende delas acusa por geracao, nao por defeito.

**(3) PELA FORMA DAS LINHAS** — fracao de linhas do balde que casam
`^(#|palavra:)`, porque o bloco do Studio e `chave: valor` e um comentario
fixado e PROSA. Deu **SEIS falsos positivos** no acervo, e os seis sao
comentarios legitimos: prosa em polones e indonesio comeca com "Rachunek:",
"Sedno:", "Szczerze:", "Jujur:". **Detector que inventa achado e pior que nao
ter detector** (725) — pego antes de relatar, desta vez.

**LOGO NAO HA PORTAO, e isso vai dito em vez de disfarcado.** Uma conferencia
confiavel exige que a copy DECLARE qual secao e o comentario de um jeito que
nao dependa de idioma — mudanca de FORMATO de copy, que e decisao do dono
(§10), nao coisa para inventar numa rodada. Este modulo e INSTRUMENTO: ele
reproduz o vazamento e nao acusa ninguem. Codigo de saida sempre zero.

**E A MINHA PRIMEIRA MEDICAO DE TUDO ISSO FOI VACUA**, que fecha a conta de
tres erros de medicao na mesma hora: eu varri 326 specs chamando
`ler_copy(texto)` — assinatura errada, ela recebe a SPEC e o workdir — dentro
de um `except Exception: continue`. As 326 levantaram, o contador ficou em zero
e eu quase relatei "zero vazamentos" como medicao. Corrigida a assinatura ela
ainda levantava, no placeholder `{TRILHA}`. Varredura que volta vazia tem de
REPROVAR.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Os cabecalhos de comentario fixado MEDIDOS no disco, nos sete idiomas. Esta
# lista NAO e um discriminador — ela existe para a REPRODUCAO do vazamento e
# para o teste provar que o cabecalho traduz. Usa-la para acusar seria repetir
# a tentativa (1).
CABECALHOS_MEDIDOS = (
    "COMENT", "KOMENTAR", "KOMENTARZ", "ΣΧΟΛΙΟ",
    "YORUM", "PINNED COMMENT", "टिप्पणी",
)

_LICENCA_DE_SONDA = (
    "Inspired by Kevin MacLeod | incompetech.com\n"
    "Licensed under Creative Commons: By Attribution 4.0\n"
    "https://creativecommons.org/licenses/by/4.0/"
)


def cabecalhos(texto: str) -> list:
    """Todos os `## ...` da copy, na ordem."""
    return [h.strip() for h in re.findall(r"^##\s*(.+)$", texto or "", re.M)]


def cabecalho_do_comentario(texto: str):
    """O cabecalho que DECLARA o comentario fixado, em qualquer dos idiomas.

    Devolve None quando nenhum casa — e isso NAO significa que a secao falta:
    significa que esta lista nao conhece aquele idioma, que e exatamente por
    que ela nao serve para acusar.
    """
    for h in cabecalhos(texto):
        for c in CABECALHOS_MEDIDOS:
            if h.upper().startswith(c.upper()):
                return h
    return None


# Os UNICOS sufixos com que um cabecalho legitimo estende outro cabecalho da
# MESMA copy. MEDIDOS no disco em 21/10 as 04:3x, varrendo as 392 copies: dos
# **325** pares (base, extensao) existentes, ha **TRES** formas e **DOIS**
# sufixos — `SHORT` (287 vezes, `TITULO`/`TITULO SHORT` e o `JUDUL` indonesio) e
# `SOBRE OS NUMEROS` (38, `AVISO`/`AVISO SOBRE OS NUMEROS`). Os dois sao secoes
# que o `publicar.ler_copy` conhece.
SUFIXOS_LEGITIMOS = ("SHORT", "SOBRE OS NUMEROS")


def prefixo_colidido(texto: str) -> list:
    """Cabecalho que ESTENDE outro da mesma copy com sufixo nao observado.

    **POR QUE EXISTE (21/10 as 04:3x).** Escrevendo a `epomeno-epipedo-s082` eu
    deixei um `## COMENTARIO FIXADO FIM` solto na copy. Para o
    `publicar.ler_copy` isso e uma SECAO, e o comentario fixado e um balde
    PEGA-TUDO (medido em 20/10 as 20:3x): o bloco errado podia ir ao ar como
    comentario do video. **Peguei relendo, nao por instrumento.**

    **E ESTE E O UNICO DISCRIMINADOR QUE SOBREVIVEU, de CINCO tentados** — as
    tres de 20/10 (cabecalho `COMENT*`, que TRADUZ em sete idiomas; chaves do
    Studio, ausentes por geracao em 183 de 360; forma das linhas, com seis
    falsos positivos) e as DUAS desta rodada:

      * **prefixo CRU**: 325 acusacoes, e as 325 sao os pares legitimos
        `TITULO`/`TITULO SHORT` e `AVISO`/`AVISO SOBRE OS NUMEROS`. Detector que
        inventa achado e pior que nao ter detector (725);
      * **frequencia** (cabecalho que aparece numa copy so): acusa traducao
        legitima (`KOMENTARZ PRZYPIETY`, `JUDUL SHORT`) e secao ad-hoc
        (`MIRA — ...`). Nao serve.

    **O que faz este funcionar e ele comparar a copy COM ELA MESMA**, logo nao
    depende de idioma nenhum: o par (base, extensao) e interno. E o conjunto de
    sufixos e **OBSERVADO** no disco, nao escolhido — acusa **ZERO** das 392
    copies do acervo e pegaria o meu `FIM`.

    **LIMITE DECLARADO:** uma copy que legitimamente tenha `## FONTES` **e**
    `## FONTES E RESSALVAS` seria acusada. Hoje nao existe nenhuma (as duas
    nunca aparecem juntas), e e por isso que isto INFORMA e **nao e portao** —
    quem decide e quem le, e o sufixo novo entra em `SUFIXOS_LEGITIMOS` com a
    medida ao lado, nunca por conveniencia de uma rodada.
    """
    hs = cabecalhos(texto)
    saida = []
    for base in hs:
        for ext in hs:
            if ext == base or not ext.startswith(base + " "):
                continue
            sufixo = ext[len(base) + 1:].strip()
            if sufixo.upper() in SUFIXOS_LEGITIMOS:
                continue
            saida.append({"base": base, "extensao": ext, "sufixo": sufixo})
    return saida


def _sem_placeholder(texto: str) -> str:
    """Enche o que o RENDER preencheria.

    O `ler_copy` LEVANTA com `{TRILHA}` ou `{CAPITULOS}` no texto, e com razao.
    Fora do runner isso impede qualquer sonda, e foi o que tornou a minha
    primeira medicao vacua.
    """
    return (texto or "").replace("{TRILHA}", _LICENCA_DE_SONDA).replace(
        "{CAPITULOS}", "0:00 Inicio\n1:00 Meio"
    )


def _ler(spec: dict, texto: str, workdir: str = "."):
    """Delega ao `publicar.ler_copy`, que e o DONO da classificacao.

    Refazer a classificacao de secoes aqui criaria o segundo dono dela — a
    assinatura que congelou a legenda e matou os layouts de longo.
    """
    if os.path.join(RAIZ, "fabrica") not in sys.path:
        sys.path.insert(0, os.path.join(RAIZ, "fabrica"))
    import publicar

    q = dict(spec)
    q["copy"] = _sem_placeholder(texto)
    return publicar.ler_copy(q, workdir)


def comentario_de(spec: dict, workdir: str = ".") -> str:
    """O que ESTA copy poria como comentario fixado do video."""
    texto = spec.get("copy")
    if not isinstance(texto, str) or not texto.strip():
        return ""
    return (_ler(spec, texto, workdir).get("comentario") or "").strip()


def secao_do_balde(spec: dict, workdir: str = ".") -> dict:
    """QUAL secao da copy o balde PEGA-TUDO de fato pegou — nomeada.

    **Medido em 22/10 as 21:5x, e e a conferencia que faltava a este modulo.**
    Em 20/10 as 20:3x eu reproduzi o vazamento e tentei TRES conferencias, as
    tres caidas: o cabecalho TRADUZ (32 de 360 copies), as chaves do Studio
    faltam por GERACAO (183 de 360) e a forma das linhas da SEIS falsos
    positivos. A conclusao daquela rodada foi *"nao ha portao"*, e ela
    continua valendo.

    **O que faltava era mais barato que um portao: NOMEAR.** O balde pega a
    PRIMEIRA secao que nao casou com licenca, capitulos, hashtags nem tags, e
    isso e DETERMINISTICO — logo da para dizer qual secao venceu, sem precisar
    saber qual delas o autor QUERIA. Quem le a passada ve `FONTES` no lugar de
    `COMENTARIO FIXADO` e corrige a ORDEM, que e redacao e nao formato.

    **E A REGRA QUE EU ESCREVI AS 21:5x ESTAVA INCOMPLETA — corrigida as 22:5x,
    e quem me pegou foi o PORTAO.** Ela dizia *"ponha a secao do comentario
    como a PRIMEIRA que nao casa com as quatro"*, e seguir isso ao pe da letra
    poe a secao antes da descricao. **O `titulo` e a `descricao` do
    `publicar.ler_copy` saem da POSICAO — `secoes[0]` e `secoes[1]` —, nao do
    cabecalho**, logo a secao do comentario virou a DESCRICAO e o portao `copy`
    reprovou com *"descricao com 42 palavras (minimo 200)"*. A regra certa:
    **DEPOIS da descricao e ANTES de qualquer outra nao casada.**

    **O TAMANHO VAI MEDIDO:** das 417 copies com secao de comentario fixado,
    o `ler_copy` consegue ler 90 (as outras tem placeholder de render), e
    nessas o balde pegou a secao ERRADA em **DEZESSETE**.

    **E O DEFEITO E LATENTE, nao de fora:** o `comentario` e PARSEADO e NUNCA
    POSTADO — o `confere_token` diz isso em letra, e o `commentThreads.insert`
    nao e chamado em lugar nenhum. Logo nenhum texto errado chegou ao YouTube.
    O que ele custa e a conferencia do portao `copy`, que pergunta
    `if not cp.get("comentario")` e e sempre satisfeita pelo pega-tudo. Dizer
    que isto vazou para fora seria inflar o achado.
    """
    texto = spec.get("copy")
    if not isinstance(texto, str) or not texto.strip():
        return {"possivel": False, "motivo": "spec sem copy em texto"}
    try:
        com = comentario_de(spec, workdir)
    except BaseException as e:      # `ler_copy` levanta SystemExit no placeholder
        return {"possivel": False, "motivo": "a copy nao e legivel aqui (%s)" % e}
    if not com:
        return {"possivel": False, "motivo": "o balde ficou vazio"}
    venceu = None
    for cab in cabecalhos(texto):
        corpo = _secao_bruta(texto, cab)
        if corpo and corpo[:50] == com[:50]:
            venceu = cab
            break
    declarado = cabecalho_do_comentario(texto)
    return {
        "possivel": True,
        "balde": venceu,
        "declarado": declarado,
        "bate": bool(venceu) and bool(declarado) and venceu == declarado,
        "motivo": None if (venceu and declarado and venceu == declarado) else (
            "o balde PEGA-TUDO pegou %r e a secao do comentario declarada e "
            "%r — ele enche com a PRIMEIRA secao que nao casou com licenca, "
            "capitulos, hashtags nem tags, logo a ORDEM decide. **Ponha a "
            "secao do comentario DEPOIS da descricao e ANTES de qualquer outra "
            "nao casada** — nao como a primeira secao da copy: o `titulo` e a "
            "`descricao` saem da POSICAO (`secoes[0]` e `secoes[1]`), nao do "
            "cabecalho, logo secao posta antes da descricao VIRA a descricao. "
            "Isto NAO vazou para fora: o comentario e parseado e nunca postado"
            % (venceu, declarado)),
    }


def _secao_bruta(texto: str, cab: str) -> str:
    m = re.search(r"^##\s*" + re.escape(cab) + r"\s*$\n(.*?)(?=^##\s|\Z)",
                  texto, re.M | re.S)
    return (m.group(1).strip() if m else "")


def vazamento_simulado(spec: dict, workdir: str = ".") -> dict:
    """REPRODUZ o defeito: tira a secao do comentario e ve o que sobe no lugar.

    Isto e a prova, nao a conferencia. Ele nao julga spec nenhuma do disco —
    ele mostra, numa spec qualquer, o que acontece com quem escrever a copy sem
    a secao, que foi o que eu fiz nesta hora.
    """
    texto = spec.get("copy")
    if not isinstance(texto, str) or not texto.strip():
        return {"possivel": False, "motivo": "spec sem copy em texto"}
    cab = cabecalho_do_comentario(texto)
    if not cab:
        return {"possivel": False,
                "motivo": "nenhum cabecalho conhecido declara o comentario"}
    i = texto.index("## " + cab)
    j = texto.find("\n## ", i + 1)
    if j < 0:
        return {"possivel": False, "motivo": "a secao do comentario e a ultima"}
    antes = comentario_de(spec, workdir)
    q = dict(spec)
    q["copy"] = texto[:i] + texto[j + 1:]
    depois = (_ler(q, q["copy"], workdir).get("comentario") or "").strip()
    return {
        "possivel": True,
        "cabecalho": cab,
        "antes": antes,
        "depois": depois,
        "vazou": bool(depois) and depois != antes,
        "motivo": (
            "retirada a secao, o balde PEGA-TUDO encheu com outra e o portao "
            "segue verde no comentario" if (depois and depois != antes) else ""
        ),
    }


def _linha_do_balde(spec: dict, workdir: str = ".") -> str:
    """UM dono da frase, e ela sai nos DOIS ramos — bate e nao bate."""
    q = secao_do_balde(spec, workdir)
    if not q.get("possivel"):
        return ("  SECAO DO BALDE: nao deu para medir — %s"
                % q.get("motivo"))
    if q.get("bate"):
        return ("  SECAO DO BALDE: %r, que e a declarada — a ORDEM esta certa "
                "nesta copy." % q.get("balde"))
    return "  SECAO DO BALDE: %s" % q.get("motivo")


def relato(caminho: str) -> str:
    import json

    with open(caminho, encoding="utf-8") as f:
        sp = json.load(f)
    linhas = ["SECOES DA COPY de %s:" % sp.get("slug", caminho)]
    texto = sp.get("copy") or ""
    linhas.append("  cabecalhos: " + ", ".join(cabecalhos(texto)))
    cab = cabecalho_do_comentario(texto)
    linhas.append("  cabecalho do comentario: %s" % (cab or "NENHUM conhecido"))
    v = vazamento_simulado(sp)
    if v["possivel"]:
        linhas.append("  SIMULACAO (tirando a secao):")
        linhas.append("    vazou: %s" % ("SIM" if v["vazou"] else "nao"))
        if v["vazou"]:
            linhas.append("    iria ao ar: " + repr(v["depois"][:90]))
    else:
        linhas.append("  sem simulacao: " + v["motivo"])
    # QUAL secao o balde pegou — NOMEADA, nao gated (21:5x). Instrumento
    # calculado e descartado pelo chamador e a classe dos layouts mortos.
    linhas.append(_linha_do_balde(sp))
    linhas.append(
        "  DA SECAO DO COMENTARIO isto NAO acusa ninguem: CINCO "
        "discriminadores foram tentados e QUATRO falharam — os numeros estao "
        "nos docstrings deste modulo e do `prefixo_colidido`. Sem procedencia "
        "nao ha portao, e o unico que sobreviveu e a colisao de PREFIXO, logo "
        "e a UNICA coisa que este relato acusa."
    )
    # A COLISAO DE PREFIXO, que o relato TEM de carregar: instrumento calculado
    # e descartado pelo chamador e a classe dos layouts mortos (13:2x).
    col = prefixo_colidido(texto)
    if col:
        for x in col:
            linhas.append(
                "  >> CABECALHO COLIDIDO: %r ESTENDE %r com o sufixo %r, que"
                " nao esta entre os OBSERVADOS %s. Para o `ler_copy` isso e uma"
                " SECAO, e o comentario fixado e um balde PEGA-TUDO (20/10 as"
                " 20:3x): o bloco errado pode ir ao ar como comentario."
                % (x["extensao"], x["base"], x["sufixo"],
                   list(SUFIXOS_LEGITIMOS)))
    else:
        linhas.append(
            "  nenhum cabecalho ESTENDE outro com sufixo nao observado"
            " (os legitimos sao %s, MEDIDOS no disco)."
            % list(SUFIXOS_LEGITIMOS))

    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python3 fabrica/copy_secoes.py <spec.json>")
        return 0
    print(relato(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
