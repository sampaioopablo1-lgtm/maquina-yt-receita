# -*- coding: utf-8 -*-
"""O `comentario` da copy e um BALDE PEGA-TUDO, e o portao nao via a ausencia.

MEDIDO em 19/10 as 20:3x, na copy que eu mesmo acabei de escrever. Eu
entreguei a copy do `labtreinamento-s087` SEM a secao `## COMENTARIO FIXADO`
e SEM a `## HASHTAGS`. O portao `copy` reprovou com UM problema so:

    copy: 1 problema(s)
      - sem hashtags

e NAO disse nada sobre o comentario fixado, que tambem faltava. O motivo
esta no `publicar.ler_copy`: o ultimo ramo da classificacao de secoes e

    elif not comentario and not corpo.startswith("-"):
        comentario = corpo

isto e, a PRIMEIRA secao depois da DESCRICAO que nao casa com licenca, com
capitulos, com hashtags nem com tags cai no comentario. Sem a secao propria,
quem caiu ali foi a `## CONFIGURACOES DO STUDIO`. Reproduzido:

    comentario: '# NOTA: `categoryId` aqui e DECLARATIVO ... privacyStatus: public
                 defaultLanguage: pt-BR ...'

**Logo o bloco de configuracao do Studio iria ao ar como COMENTARIO FIXADO do
video, e a conferencia `if not cp.get("comentario")` do portao e INCAPAZ de
pegar isso** — ela pergunta se o balde esta cheio, e o pega-tudo sempre o
enche. Falha PERMISSIVA, que e o pior sentido, a mesma do corpus atrasado e a
mesma da mira que parou de conferir por seis pecas.

O BALDE PEGA-TUDO NAO SE TIRA, e o motivo e medido e anterior a mim: o
comentario do proprio `ler_copy` conta que em 25/08 a secao da licenca era
descartada em silencio por causa da ORDEM dos baldes, e que por isso a deteccao
dela passou a ser pelo CONTEUDO — "o titulo muda de spec para spec e de idioma
para idioma". Mexer na classificacao para exigir titulo arriscaria repetir
aquilo nas specs de outros idiomas.

O QUE SE FAZ E PERGUNTAR OUTRA COISA: nao "o balde esta cheio?", e sim "existe
secao DECLARANDO o comentario?". E essa pergunta tem procedencia medida, porque
o titulo desta secao especifica NAO varia: varridas as **322** specs com copy
no disco, **322 de 322** declaram uma secao que comeca por `COMENT` — e
**316** declaram `HASHTAG`, logo as seis que faltam ja levam o "sem hashtags"
do portao, que e falha RUIDOSA e correta.

E O BURACO E LATENTE: **zero** das 322 vaza hoje. Pelo argumento do `mira.py`
— aviso que reprova o acervo deixa de avisar — o lugar disto seria a suite; mas
aqui a conferencia reprova EXATAMENTE a copy quebrada e NENHUMA spec do disco,
que e a mesma conta que pos o cartao em branco no portao `layout` as 19:1x.
Entao vai no portao.

E A MINHA PRIMEIRA MEDICAO DISTO FOI VACUA, e essa e a licao mais barata do
dia: eu varri as 326 specs chamando `ler_copy(texto)` — assinatura errada, ela
recebe a SPEC e o workdir — dentro de um `except Exception: continue`. As 326
levantaram, o contador ficou em zero e eu quase relatei "zero vazamentos" como
medicao. Depois de corrigir a assinatura ela ainda levantava, agora no
placeholder `{TRILHA}`. **Varredura que volta vazia tem de REPROVAR**, e e por
isso que o teste deste arquivo tem piso de specs e exige que os dois lados
existam.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# O titulo e a chave aqui de PROPOSITO, e a procedencia esta no docstring:
# 322 de 322 specs do disco declaram uma secao que comeca por COMENT. Para a
# LICENCA isto seria errado (a medicao de 25/08 diz o contrario) e e por isso
# que a licenca NAO entra nesta lista.
SECOES_EXIGIDAS = ("COMENT", "HASHTAG")

# CORRECAO de 19/10 (rotina de continuidade): o "322 de 322 comecam por COMENT"
# valia so para o cabecalho em caractere latino do pt-BR/es. As specs antigas
# dos outros idiomas declaram o cabecalho LOCALIZADO — grego `SXOLIO`, polones
# `KOMENTARZ`, turco `YORUM`, indonesio `KOMENTAR`, ingles `PINNED COMMENT`, hindi `TIPPANI` — e 31 delas reprovavam em
# `test_toda_spec_com_copy_real_passa_no_portao_copy`. O portao tambem
# reprovaria copy nova do epomeno ou do kolejny escrita no cabecalho nativo.
# As alternativas abaixo saem da varredura dos cabecalhos `## ` do disco.
_ALTERNATIVAS = {
    "COMENT": r"(?:COMENT|COMMENT|PINNED[ ]COMMENT|टिप्पणी|KOMENT|\u03a3\u03a7\u039f\u039b|[^\n]*YORUM)",
}

_LICENCA_DE_SONDA = (
    "Inspired by Kevin MacLeod | incompetech.com\n"
    "Licensed under Creative Commons: By Attribution 4.0\n"
    "https://creativecommons.org/licenses/by/4.0/"
)


def declaradas(texto: str) -> dict:
    """Quais das secoes exigidas o texto da copy DECLARA por cabecalho."""
    return {
        s: bool(re.search(r"^##\s*" + _ALTERNATIVAS.get(s, s), texto or "", re.M | re.I))
        for s in SECOES_EXIGIDAS
    }


def _sem_placeholder(texto: str) -> str:
    """Enche os placeholders que o RENDER preencheria.

    O `ler_copy` LEVANTA com `{TRILHA}` ou `{CAPITULOS}` no texto, e com razao
    — publicar assim poria o placeholder na descricao. Fora do runner isso
    impede qualquer sonda, e foi o que tornou a minha primeira medicao vacua.
    """
    return (texto or "").replace("{TRILHA}", _LICENCA_DE_SONDA).replace(
        "{CAPITULOS}", "0:00 Inicio\n1:00 Meio"
    )


def comentario_vazado(spec: dict, workdir: str = ".") -> dict:
    """O comentario fixado veio da secao DECLARADA ou do balde pega-tudo?

    A leitura e DELEGADA ao `publicar.ler_copy`, que e o dono da regra. Refazer
    a classificacao de secoes aqui criaria o segundo dono dela — a assinatura
    que congelou a legenda e matou os layouts de longo.
    """
    if "fabrica" not in sys.path:
        sys.path.insert(0, os.path.join(RAIZ, "fabrica"))
    import publicar

    texto = spec.get("copy")
    if not isinstance(texto, str) or not texto.strip():
        return {"tem_secao": False, "comentario": "", "vazado": False,
                "motivo": "spec sem copy em texto"}

    q = dict(spec)
    q["copy"] = _sem_placeholder(texto)
    cp = publicar.ler_copy(q, workdir)
    com = (cp.get("comentario") or "").strip()
    tem = declaradas(texto)["COMENT"]
    return {
        "tem_secao": tem,
        "comentario": com,
        "vazado": bool(com) and not tem,
        "motivo": (
            "o comentario fixado saiu do balde PEGA-TUDO: nenhuma secao o "
            "declara, logo o que vai ao ar e a primeira secao que sobrou"
            if (com and not tem) else ""
        ),
    }


def avisos(spec: dict, workdir: str = ".") -> list:
    """Um problema por secao exigida que falta, mais o vazamento se houver."""
    texto = spec.get("copy")
    if not isinstance(texto, str) or not texto.strip():
        return []
    fora = []
    v = comentario_vazado(spec, workdir)
    if v["vazado"]:
        primeira = v["comentario"].split("\n")[0][:70]
        fora.append(
            "sem a secao do COMENTARIO FIXADO, e o balde pega-tudo do "
            "`ler_copy` encheu com outra secao — iria ao ar: "
            f"{primeira!r}"
        )
    elif not v["tem_secao"] and not v["comentario"]:
        fora.append("sem a secao do COMENTARIO FIXADO")
    return fora


def relato(caminho: str) -> str:
    import json

    with open(caminho, encoding="utf-8") as f:
        sp = json.load(f)
    d = declaradas(sp.get("copy") or "")
    linhas = ["SECOES DA COPY de %s:" % sp.get("slug", caminho)]
    for s, ok in d.items():
        linhas.append("  %-8s declarada: %s" % (s, "SIM" if ok else "NAO"))
    v = comentario_vazado(sp)
    if v["vazado"]:
        linhas.append("  >> VAZAMENTO: " + v["motivo"])
        linhas.append("     iria ao ar: " + repr(v["comentario"][:90]))
    else:
        linhas.append("  comentario fixado sai da secao declarada.")
    linhas.append(
        "  isto INFORMA aqui; quem reprova e o portao `copy` do prontidao."
    )
    return "\n".join(linhas)


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python3 fabrica/copy_secoes.py <spec.json>")
        return 2
    print(relato(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
