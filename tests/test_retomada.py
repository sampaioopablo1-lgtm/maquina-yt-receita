"""Retomada: o status diz ate onde chegou, o disco diz o que ainda existe.

Quando os dois discordam manda o disco — e eles discordam no caso NORMAL, nao
no excepcional: todo job do Actions e um runner novo, e o `maquina sincronizar`
traz do Supabase linhas em `narrado` e `ilustrado` cujos mp3 e png morreram com
a maquina que os gerou.

Medido em 12/08/2026: skill-stacking-2-8af772 ficou em `ilustrado` quando
cancelei o job. Retomar pularia direto para renderizar, montando video a partir
de caminhos que nao existem mais.
"""

from __future__ import annotations

import pytest

from maquina.models import Cena, Formato, Roteiro, Status, Video
from maquina.pipeline import _ultimo_estado_valido


def _video(status: Status, tmp_path=None, com_audio=False, com_imagem=False,
           com_mp4=False) -> Video:
    cenas = []
    for i in range(3):
        c = Cena(indice=i, narracao="n", prompt_visual="p")
        if tmp_path:
            if com_audio:
                a = tmp_path / f"a{i}.mp3"
                a.write_bytes(b"x")
                c.audio_path = str(a)
            else:
                c.audio_path = str(tmp_path / f"sumiu{i}.mp3")
            if com_imagem:
                im = tmp_path / f"i{i}.png"
                im.write_bytes(b"x")
                c.imagem_path = str(im)
            else:
                c.imagem_path = str(tmp_path / f"sumiu{i}.png")
        cenas.append(c)

    v = Video(slug="s", formato=Formato.LONGO, status=status,
              roteiro=Roteiro(titulo="t", gancho="g", cenas=cenas))
    if tmp_path and com_mp4:
        mp4 = tmp_path / "final.mp4"
        mp4.write_bytes(b"x")
        v.video_path = str(mp4)
    return v


def test_ilustrado_sem_arquivo_volta_para_roteirizado(tmp_path):
    """O caso real: job cancelado, disco do runner morto, status intacto."""
    v = _video(Status.ILUSTRADO, tmp_path, com_audio=False, com_imagem=False)
    assert _ultimo_estado_valido(v) is Status.ROTEIRIZADO


def test_audio_em_disco_e_imagem_nao_volta_para_narrado(tmp_path):
    v = _video(Status.ILUSTRADO, tmp_path, com_audio=True, com_imagem=False)
    assert _ultimo_estado_valido(v) is Status.NARRADO


def test_tudo_em_disco_confirma_ilustrado(tmp_path):
    v = _video(Status.ILUSTRADO, tmp_path, com_audio=True, com_imagem=True)
    assert _ultimo_estado_valido(v) is Status.ILUSTRADO


def test_com_mp4_em_disco_nao_re_renderiza(tmp_path):
    """Render e o passo mais caro da pipeline — refazer o que existe e desperdicio."""
    v = _video(Status.RENDERIZADO, tmp_path, com_audio=True, com_imagem=True, com_mp4=True)
    assert _ultimo_estado_valido(v) is Status.RENDERIZADO


@pytest.mark.parametrize("status", [
    Status.PUBLICADO, Status.REJEITADO, Status.CANCELADO,
    Status.LISTADO_PARA_PUBLICACAO,
])
def test_video_fora_da_esteira_nunca_e_rebobinado(status, tmp_path):
    """Rebobinar um publicado re-produziria um video que ja esta no YouTube."""
    v = _video(status, tmp_path, com_audio=False, com_imagem=False)
    assert _ultimo_estado_valido(v) is status


def test_sem_roteiro_volta_para_ideia():
    v = Video(slug="s", formato=Formato.LONGO, status=Status.NARRADO)
    assert _ultimo_estado_valido(v) is Status.IDEIA


def test_a_funcao_so_anda_para_tras(tmp_path):
    """Aplicar em toda retomada so e seguro porque ela nunca promove status."""
    ordem = [Status.IDEIA, Status.ROTEIRIZADO, Status.NARRADO, Status.ILUSTRADO]
    for i, status in enumerate(ordem):
        v = _video(status, tmp_path, com_audio=False, com_imagem=False)
        resultado = _ultimo_estado_valido(v)
        assert ordem.index(resultado) <= i, f"{status} foi promovido para {resultado}"
