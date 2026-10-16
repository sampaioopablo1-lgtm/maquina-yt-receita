"""As quatro rotas do sandbox sondadas no MESMO MINUTO — e elas divergem.

O `CLAUDE.md` carrega uma tabela de rotas com duas colunas de HORA (03:3x e
07:1x), e a regra que ela ensina e a certa: rota medida como aberta e ESTADO,
nao propriedade. Mas a FORMA como eu media sustentava, sem dizer, uma segunda
hipotese que nunca foi testada: que o estado era do SANDBOX — uma mare que sobe
e desce com todas as rotas juntas. Eu sondava uma rota por rodada, pela rota de
que precisava, e atribuia o resultado ao ambiente.

Medido em 16/10 as 17:2x, as quatro na MESMA chamada de bash, mesma sandbox
(sufixo `ui0p`), dentro do mesmo minuto:

| rota | 03:3x | 07:1x | **17:2x** | como se mede |
|---|---|---|---|---|
| `/channel/<UC>/about` | abre | abre | **ABRE** | campo "N inscritos" |
| `/watch?v=` | abre | FECHA | **ABRE** | campo `lengthSeconds` |
| `yt-dlp` legenda | abre | FECHA | **ABRE** | o .vtt baixa |
| `/channel/<UC>/videos` | — | FECHA | **FECHA** | contagem de `videoRenderer` |

**A listagem FECHOU enquanto as outras tres ABRIAM, no mesmo minuto.** Logo o
estado e por ROTA, e nao do sandbox: nao existe "a mare do ambiente" para
consultar, e sondar uma rota NAO informa sobre as outras. As duas que haviam
fechado as 07:1x voltaram juntas, e a que fechou as 12:2x continua fechada
quatro horas e meia depois — o que tambem diz que o estado de uma rota tem
duracao propria.

E a listagem fecha do jeito mais caro que existe: **HTTP 200 com 1.132.822
bytes**, zero `videoRenderer`, um marcador `CONSENT` e um `captcha`. Quem conta
o codigo HTTP le "funcionou" e recebe um canal vazio. Quem conta o CAMPO ve o
bloqueio. E por isso que a `recencia.ordem_viva` LEVANTA em saida vazia.

O que este arquivo NAO afirma: que as rotas sejam independentes. Tres pontos no
tempo e uma sonda simultanea nao medem correlacao — duas rotas voltaram JUNTAS
as 17:2x, e isso e compativel com dependencia parcial. O que esta medido e a
negacao: elas nao sobem e descem TODAS juntas, porque uma estava do outro lado
no mesmo minuto.
"""
import re
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# As quatro rotas na sonda simultanea de 16/10 17:2x. True = abre.
SONDA_17_2X = {
    "about": True,
    "watch": True,
    "legenda": True,
    "listagem": False,
}

# O que a listagem devolveu quando FECHADA, para que ninguem leia o 200 como
# sucesso: (codigo, bytes, videoRenderer, CONSENT, captcha).
LISTAGEM_FECHADA = (200, 1132822, 0, 1, 1)

# As colunas anteriores da tabela do CLAUDE.md, para a comparacao no tempo.
SONDAS_ANTERIORES = {
    "03:3x": {"about": True, "watch": True, "legenda": True},
    "07:1x": {"about": True, "watch": False, "legenda": False, "listagem": False},
}


def test_a_sonda_simultanea_tem_rotas_dos_DOIS_lados():
    """Se todas tivessem o mesmo estado, a hipotese da mare sobreviveria."""
    estados = set(SONDA_17_2X.values())
    assert estados == {True, False}, (
        "a sonda simultanea tem de ter rota aberta E rota fechada — e ela que "
        f"derruba a mare do sandbox; veio {SONDA_17_2X}"
    )


def test_a_rota_fechada_devolveu_200_e_pagina_GRANDE():
    """O bloqueio nao se ve no codigo HTTP, e e por isso que se conta o campo."""
    codigo, tamanho, renderers, consent, captcha = LISTAGEM_FECHADA
    assert codigo == 200, "o caso caro e justamente o 200"
    assert tamanho > 1_000_000, "pagina grande, logo 'veio conteudo' engana"
    assert renderers == 0, "zero do CAMPO que importa — e isso que acusa"
    assert consent >= 1 and captcha >= 1


def test_duas_rotas_que_haviam_FECHADO_voltaram():
    """Estado, nao propriedade — e nos dois sentidos, que e o ponto do 11/10."""
    antes = SONDAS_ANTERIORES["07:1x"]
    voltaram = [k for k in ("watch", "legenda") if antes[k] is False and SONDA_17_2X[k]]
    assert voltaram == ["watch", "legenda"], (
        "as duas que fecharam as 07:1x estao abertas as 17:2x; se isso mudar, "
        "a nota tem de ser RELIDA em vez de reaproveitada"
    )


def test_a_rota_que_fechou_as_12_2x_continua_fechada():
    """O estado de uma rota tem duracao propria, e esta passou de 4 h."""
    assert SONDA_17_2X["listagem"] is False
    assert SONDAS_ANTERIORES["07:1x"]["listagem"] is False


def test_a_sonda_de_UMA_rota_nao_informa_as_outras():
    """A consequencia operacional, escrita como propriedade e nao como frase."""
    abertas = {k for k, v in SONDA_17_2X.items() if v}
    fechadas = {k for k, v in SONDA_17_2X.items() if not v}
    assert abertas and fechadas
    # Para qualquer rota que eu sonde, existe outra rota cujo estado DIFERE —
    # logo nenhuma sonda isolada autoriza concluir sobre a rota de que preciso.
    # (Escrito assim de proposito: a primeira versao deste assert terminava em
    # `or True`, isto e, passava com qualquer tabela. Portao verde fabricado,
    # §3.8, num arquivo escrito para guardar justamente essa licao.)
    for rota, estado in SONDA_17_2X.items():
        outras = {v for k, v in SONDA_17_2X.items() if k != rota}
        assert (not estado) in outras, (
            f"a rota {rota!r} esta {estado} e nenhuma outra esta do lado oposto "
            "— sem isso a sonda isolada seria informativa"
        )
    assert len(abertas) == 3 and len(fechadas) == 1


def test_a_ordem_viva_LEVANTA_em_saida_vazia():
    """A defesa contra o 200-sem-campo mora no codigo, e este teste a ABRE."""
    import sys

    sys.path.insert(0, str(RAIZ / "fabrica"))
    import recencia

    try:
        recencia.ordem_viva("")
    except ValueError as e:
        assert "AUSENCIA DE LEITURA" in str(e)
    else:
        raise AssertionError(
            "saida vazia tem de LEVANTAR: e ai que o 200-sem-campo reaparece "
            "disfarcado de canal vazio"
        )


def test_o_docstring_nao_promete_independencia():
    """A ressalva vai no arquivo, nao so na minha cabeca (743/753/761)."""
    texto = " ".join(__doc__.split())
    assert "nao medem correlacao" in texto
    assert "compativel com dependencia parcial" in texto
