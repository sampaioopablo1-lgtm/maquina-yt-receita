"""A meta e dez videos DIFERENTES por canal, nao dez linhas na tabela.

Em 19/08/2026 o placar dizia que kolejny-poziom e setiap-level estavam em
10 de 10 e portanto prontos. O kolejny tinha CINCO longos distintos: seis
das dez linhas eram o mesmo "Emerytura z ZUS", republicado todo dia de 11 a
17/08 pelo cron. Vinte e seis duplicatas em seis canais no total.

O dano nao era so cosmetico. `faltam` ia a zero, o canal caia para o fim da
ordem de `proximo`, e um canal pela metade ficava invisivel para a propria
maquina — para sempre, porque nada o traria de volta.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import orquestra as O  # noqa: E402


def _long(canal, titulo, i):
    return {"canal": canal, "formato": "longo", "pacote": None,
            "titulo": titulo, "youtube_id": f"yt-{canal}-{i}"}


def _canal_qualquer():
    """Um slug que existe em config/canais/, para estado() enxergar."""
    canais = O.canais_do_repo()
    assert canais, "sem canais no repo — o teste nao tem onde medir"
    return sorted(canais)[0]


def test_seis_linhas_do_mesmo_video_contam_uma():
    c = _canal_qualquer()
    videos = [_long(c, "Emerytura z ZUS: 34,4% pensji w 2050 roku", i)
              for i in range(6)]
    est = O.estado(videos)
    assert est["canais"][c]["publicados"] == 1, "contou linha em vez de video"
    assert est["canais"][c]["faltam"] == O.META_POR_CANAL - 1


def test_titulos_diferentes_contam_todos():
    c = _canal_qualquer()
    videos = [_long(c, f"Video numero {i}", i) for i in range(4)]
    assert O.estado(videos)["canais"][c]["publicados"] == 4


def test_o_caso_real_do_kolejny():
    """Dez linhas, cinco videos: o canal NAO esta pronto."""
    c = _canal_qualquer()
    distintos = ["Emerytura z ZUS: 34,4% pensji w 2050 roku",
                 "Jak ulozyc finanse przy sredniej pensji 9233 zl",
                 "Nadplacac Kredyt czy Inwestowac w 2026",
                 "Oplaty i podatek Belki",
                 "IKE czy IKZE w 2026"]
    videos = [_long(c, distintos[0], i) for i in range(6)]           # 6 iguais
    videos += [_long(c, t, 100 + i) for i, t in enumerate(distintos[1:])]
    assert len(videos) == 10, "o caso real tinha dez linhas"
    est = O.estado(videos)["canais"][c]
    assert est["publicados"] == 5
    assert est["faltam"] == 5, "canal pela metade tem de continuar na fila"


def test_maiuscula_e_espaco_nao_criam_video_novo():
    c = _canal_qualquer()
    videos = [_long(c, "  Emerytura z ZUS  ", 1),
              _long(c, "emerytura z zus", 2),
              _long(c, "EMERYTURA Z ZUS", 3)]
    assert O.estado(videos)["canais"][c]["publicados"] == 1


def test_linha_sem_titulo_cai_no_youtube_id_e_continua_contando():
    """A primeira versao deste conserto DESCARTAVA linha sem titulo, e a
    fixture de tests/dados_videos.json (que nao tem coluna titulo) zerou o
    placar inteiro. O modo de falha certo e o contrario: sumir com um video
    que existe faria a maquina reproduzir o que ja esta no ar. Sem titulo, a
    chave e o proprio youtube_id."""
    c = _canal_qualquer()
    videos = [_long(c, "", 1), _long(c, None, 2), _long(c, "Um video", 3)]
    assert O.estado(videos)["canais"][c]["publicados"] == 3


def test_canal_pela_metade_volta_a_ser_escolhido():
    """O efeito que importa: faltam>0 traz o canal de volta para `proximo`."""
    c = _canal_qualquer()
    videos = [_long(c, "O mesmo video de sempre", i) for i in range(10)]
    est = O.estado(videos)["canais"][c]
    assert est["faltam"] > 0, "canal com dez copias seguiria dado por pronto"
