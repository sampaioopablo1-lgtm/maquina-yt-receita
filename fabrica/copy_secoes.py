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
    linhas.append(
        "  ISTO NAO ACUSA NINGUEM: as tres tentativas de discriminador "
        "falharam, e os numeros estao no docstring deste modulo. Sem "
        "procedencia nao ha portao."
    )
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python3 fabrica/copy_secoes.py <spec.json>")
        return 0
    print(relato(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
