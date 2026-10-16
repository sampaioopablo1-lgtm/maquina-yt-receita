"""Eu previ que o aviso do esqueleto dispararia com DUAS pecas iguais. Nao.

Medido em 16/10 as 15:2x, escrevendo o `kolejny-poziom-s043`. Eu mantive o
esqueleto IGUAL ao do `s042` **de proposito**, esperando que o portao
`variedade` avisasse para eu trocar a ordem — e os onze portoes passaram em
silencio.

E A MINHA PRIMEIRA EXPLICACAO ESTAVA ERRADA, o que fica registrado porque e do
mesmo tipo que o 743: eu escrevi no relato que "o aviso e menos sensivel do que
eu supunha", como se o limiar fosse desconhecido. **Ele e SEIS pecas iguais
seguidas no canal, documentado no proprio modulo com procedencia.** Eu nao tinha
lido o numero; tinha suposto que qualquer repeticao avisava.

E A MEDICAO DEU DE GRACA UM FATO QUE IMPORTA MAIS: existe no `kolejny-poziom` um
esqueleto com **14** ocorrencias — o `titulo-titulo-titulo-titulo-cta` da forma
antiga de cinco cenas. Esse esta MUITO acima do limiar, logo qualquer peca nova
naquela forma AVISA, e e o aviso funcionando. O meu, com duas, esta longe.

NADA de limiar mudou (trava da §10): o 6 tem procedencia e eu nao a tenho para
trocar por outro numero.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import variedade as v  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..")
LIMIAR_DOCUMENTADO = 6


def _contagem(canal: str) -> dict[str, int]:
    fora: dict[str, int] = {}
    for caminho in sorted(glob.glob(
            os.path.join(RAIZ, "fabrica", "specs", f"{canal}-s*.json"))):
        with open(caminho, encoding="utf-8") as fh:
            d = json.load(fh)
        if d.get("short"):
            e = v.esqueleto(d["short"])
            fora[e] = fora.get(e, 0) + 1
    return fora


def test_o_limiar_e_SEIS_e_esta_ESCRITO_no_modulo():
    """Pela licao do 743: o teste ABRE o arquivo em vez de confiar na frase."""
    fonte = open(v.__file__, encoding="utf-8").read()
    assert "aviso a partir de 6 pecas iguais" in fonte, (
        "o limiar saiu do modulo ou mudou de texto; se mudou de VALOR, esta "
        "nota tem de ser relida, nao o teste ajustado"
    )


def test_duas_pecas_iguais_ficam_LONGE_do_limiar():
    """O caso real: o `s043` repetiu o `s042` e passou calado, com razao."""
    cont = _contagem("kolejny-poziom")
    with open(os.path.join(RAIZ, "fabrica", "specs",
                           "kolejny-poziom-s043.json"), encoding="utf-8") as fh:
        meu = v.esqueleto(json.load(fh)["short"])
    assert cont.get(meu, 0) < LIMIAR_DOCUMENTADO, (
        "se este esqueleto chegar a seis, o aviso passa a disparar e a peca "
        "seguinte tem de trocar a ORDEM dos layouts, que e conteudo"
    )


def test_existe_um_esqueleto_LEGADO_muito_acima_do_limiar():
    """E e por isso que o aviso serve: a forma antiga de cinco cenas tem 14."""
    cont = _contagem("kolejny-poziom")
    acima = {e: n for e, n in cont.items() if n >= LIMIAR_DOCUMENTADO}
    assert acima, (
        "sem nenhum esqueleto acima do limiar o aviso nunca dispararia, e a "
        "medicao de 15/10 dizia o contrario"
    )
    assert max(acima.values()) >= 14


def test_a_nota_do_ERRO_de_previsao_continua_escrita():
    """Retratacao sem teste volta (§10, item 2)."""
    doc = __doc__ or ""
    assert "minha primeira explicacao estava errada" in doc.lower()
    assert "SEIS" in doc
