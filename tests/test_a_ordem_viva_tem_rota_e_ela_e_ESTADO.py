"""A ordem VIVA de uploads tem rota, e a rota obvia FECHOU na mesma rodada.

O `recencia.py` de 16/10 as 09:xx exigia a ordem viva por argumento e NAO dizia
de onde tira-la — logo a regra que ele criou dependia de eu lembrar de uma
chamada de API que nesta sessao nao existe (`execute_sql` negado pela quinta
rodada seguida, portanto sem `pg_net` e sem token).

Medido as 12:2x: `youtube.com/channel/<id>/videos` devolveu HTTP 200 com
1.196.398 bytes e ZERO `videoRenderer`, com marcador CONSENT. O
`yt-dlp --flat-playlist` na playlist `UU...` respondeu com 84 itens.

Estes testes travam o PARSER (a chamada vive no sandbox) e, acima de tudo, a
distincao entre AUSENCIA DE LEITURA e canal vazio — que e a forma em que o
"200 com campo zero" me pegaria de novo.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import recencia as r  # noqa: E402

# As quatro primeiras linhas reais da leitura de 16/10 as 12:2x, mais os dois
# primeiros longos — o `GUiq15usizw` virou o `kolejny-poziom-s042`.
REAL = """WxlzxXVcMXI|42|A proposal is not a law
7KZjro4H8ls|43|It's the terms that matter, not the amount
RT_qRi_S1Mw|44|Sure beats possible
GUiq15usizw|538|Renting or a Mortgage? Compare Rent to Interest
kWZW-qV4tQc|489|Child Tax Credit: Income Limit Applies Only to One Child"""


def test_a_playlist_de_uploads_e_UC_virando_UU():
    assert r.playlist_de_uploads("UCGe6sYpjzKyCC_K22ae1anw") == \
        "UUGe6sYpjzKyCC_K22ae1anw"
    with pytest.raises(ValueError):
        r.playlist_de_uploads("UUGe6sYpjzKyCC_K22ae1anw")


def test_saida_VAZIA_levanta_porque_ausencia_de_leitura_NAO_e_canal_vazio():
    """O coracao do teste: o modo de falha de hoje devolve pagina SEM campo."""
    for vazio in ("", "\n\n", "WARNING: nothing here", "[youtube] aviso"):
        with pytest.raises(ValueError) as e:
            r.ordem_viva(vazio)
        assert "AUSENCIA DE LEITURA" in str(e.value)


def test_linha_de_aviso_NAO_aborta_a_ordem_inteira():
    com_aviso = "[youtube:tab] Downloading page\n" + REAL
    assert r.ordem_viva(com_aviso) == r.ordem_viva(REAL)


def test_o_rank_do_longo_conta_os_SHORTS_tambem():
    """A pergunta do dono e sobre o ULTIMO VIDEO PUBLICADO, nao o ultimo longo."""
    longos = r.longos_na_ordem(REAL)
    assert longos[0] == (4, "GUiq15usizw"), (
        "o rank 4 inclui os tres shorts acima dele; rank entre longos daria 1 "
        "e esconderia exatamente a distancia que o dono apontou"
    )
    assert r.topo_de_pauta(REAL) == "GUiq15usizw"


def test_short_NUNCA_vira_origem():
    so_shorts = "\n".join(REAL.splitlines()[:3])
    assert r.longos_na_ordem(so_shorts) == []
    assert r.topo_de_pauta(so_shorts) is None, (
        "sem longo a resposta e None, para o relato DIZER isso em vez de "
        "devolver um short de 42 s como se tivesse capitulos"
    )


def test_duracao_ausente_nao_e_tratada_como_longo():
    """Live e privado vem sem duracao; supor longo inventaria pauta."""
    assert r.longos_na_ordem("aaaaaaaaaaa|NA|live agora") == []


def test_o_limiar_de_short_e_o_DOS_180_s_e_nao_um_numero_novo():
    """180 s e o teto do Short que o CLAUDE.md ja carrega — nao limiar inventado."""
    assert r.LIMITE_DE_SHORT_S == 180
    assert r.longos_na_ordem("aaaaaaaaaaa|180|exatamente no teto") == []
    assert r.longos_na_ordem("aaaaaaaaaaa|181|um acima") == [(1, "aaaaaaaaaaa")]


def test_a_rota_fechada_vai_NOMEADA_no_modulo():
    """Para que a rodada seguinte nao volte a raspar /videos e ler o 200."""
    fonte = open(r.__file__).read()
    assert "videoRenderer" in fonte and "CONSENT" in fonte
    assert "Conte o CAMPO" in fonte
