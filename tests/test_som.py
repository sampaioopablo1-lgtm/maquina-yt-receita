"""A conferência de volume da peça renderizada, validada com sinal CONTROLADO.

Estes testes geram o próprio sinal com o ffmpeg em vez de depender de um .mp4
no repo, por dois motivos: o render não acontece neste container, e sinal
sintético tem valor CONHECIDO — então o teste mede o instrumento, não a peça.

O que eles travam: que `loudness` lê o LUFS de verdade, que arquivo sem faixa de
áudio LEVANTA em vez de devolver None silencioso, e que o nosso próprio
`loudnorm=I=-14:TP=-1.5:LRA=11` leva um sinal de -52 LUFS para a vizinhança de
-14. Se alguém trocar o filtro da fábrica por um que não acerta o alvo, o
terceiro cai.
"""
import os
import shutil
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import som as S  # noqa: E402

pytestmark = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")),
    reason="sem ffmpeg/ffprobe neste ambiente")

# O mesmo filtro que `fabrica.py AUDIO_ARGS` aplica na peça de verdade. Se os
# dois sairem de sincronia, este teste deixa de medir o que a fabrica faz — por
# isso ele e conferido contra o arquivo no ultimo teste.
FILTRO_DA_FABRICA = "loudnorm=I=-14:TP=-1.5:LRA=11"


def _tom(destino, db=-30, dur=8):
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", f"sine=frequency=220:duration={dur}:sample_rate=48000",
         "-af", f"volume={db}dB", "-c:a", "aac", "-b:a", "192k", destino],
        check=True)
    return destino


def _normaliza(origem, destino):
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", origem,
         "-af", FILTRO_DA_FABRICA, "-ac", "2", "-ar", "48000",
         "-c:a", "aac", "-b:a", "192k", destino],
        check=True)
    return destino


def test_loudness_le_um_sinal_muito_abaixo_do_alvo(tmp_path):
    f = _tom(str(tmp_path / "baixo.m4a"), db=-30)
    lo = S.loudness(f)
    assert lo["lufs"] is not None
    # Nao prometo decimo: prometo que o instrumento ve que esta MUITO abaixo.
    assert lo["lufs"] < -40
    assert S.desvio_do_alvo(lo["lufs"]) < -20


def test_o_loudnorm_DA_FABRICA_leva_o_sinal_para_perto_do_alvo(tmp_path):
    # Medido em 12/10/2026: -52,0 LUFS antes, -13,9 depois. Este teste nao
    # repete o -13,9 (isso seria precisao fingida) — exige a vizinhanca de 1 LU,
    # que e a mesma tolerancia que o pipeline alheio usa como portao.
    bruto = _tom(str(tmp_path / "bruto.m4a"), db=-30)
    norm = _normaliza(bruto, str(tmp_path / "norm.m4a"))
    antes = S.loudness(bruto)["lufs"]
    depois = S.loudness(norm)["lufs"]
    assert antes < -40, antes
    assert abs(depois - S.ALVO_LUFS) <= S.TOLERANCIA_RELATO, depois


def test_arquivo_SEM_audio_levanta_em_vez_de_devolver_None(tmp_path):
    # Video sem faixa de audio e DEFEITO de render. Devolver None faria o relato
    # dizer "sem leitura" quando a peca esta muda — o mesmo principio do
    # `replica.piso`: ausencia e silencio, nunca zero.
    mudo = str(tmp_path / "mudo.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", "color=c=black:s=320x240:d=2", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", mudo], check=True)
    assert S.tem_audio(mudo) is False
    with pytest.raises(S.SemAudio):
        S.loudness(mudo)
    assert "DEFEITO" in S.relato(mudo)


def test_silencios_acha_o_trecho_mudo_e_o_piso_e_de_UM_segundo(tmp_path):
    # Piso de 1,0 s, nao de 2,0 s como no pipeline alheio, porque o nosso P de
    # fim de frase vai de 1,04 s (pt-BR) a 1,72 s (pl-PL): com 2,0 s o silencio
    # NORMAL do polones quase dispara e a medicao nao separa modelo de defeito.
    assert S.silencios.__defaults__[1] == 1.0
    mudo = str(tmp_path / "quieto.m4a")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", "anullsrc=r=48000:cl=mono:d=4",
         "-c:a", "aac", "-b:a", "128k", mudo], check=True)
    sil = S.silencios(mudo)
    assert sil, "silencio de 4 s tem de aparecer"
    assert sil[0][1] >= 3.0


def test_desvio_do_alvo_devolve_None_sem_leitura():
    assert S.desvio_do_alvo(None) is None
    assert S.desvio_do_alvo(-14.0) == 0.0
    assert S.desvio_do_alvo(-20.0) == -6.0


def test_o_alvo_declarado_aqui_E_O_MESMO_que_a_fabrica_aplica():
    # A razao do modulo existir e CONFERIR o filtro, entao o alvo nao pode ser
    # uma copia que envelhece: ele vem do mesmo numero que esta no comando.
    raiz = os.path.join(os.path.dirname(__file__), "..", "fabrica", "fabrica.py")
    with open(raiz, encoding="utf-8") as f:
        texto = f.read()
    assert f"loudnorm=I={int(S.ALVO_LUFS)}" in texto, (
        "o ALVO_LUFS de som.py saiu de sincronia com o loudnorm de fabrica.py")
    assert f"TP={S.TP_MAX_DBTP}" in texto
