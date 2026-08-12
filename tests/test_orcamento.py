"""Teto de tempo das etapas que falam com provider externo.

Em 12/08/2026 um job ficou DUAS HORAS no passo de producao sem terminar e sem
nada que o interrompesse. As retentativas de TTS e de Pollinations sao por
chamada e nao tem teto agregado, entao um provider degradado consome os 300 min
de timeout do job e o unico sinal e o silencio. Cancelei na mao.
"""

from __future__ import annotations

import time

import pytest

from maquina.models import Cena, Formato, Roteiro
from maquina.stages import producao


def _roteiro(n: int) -> Roteiro:
    return Roteiro(
        titulo="T", gancho="G",
        cenas=[Cena(indice=i, narracao=f"cena {i}", prompt_visual="doodle")
               for i in range(n)],
    )


class TTSLento:
    """Sintetiza, mas devagar — como um provider em retentativa."""

    def __init__(self, atraso_s: float):
        self.atraso_s = atraso_s
        self.chamadas = 0

    def sintetizar(self, texto, saida, voice_id=""):
        self.chamadas += 1
        time.sleep(self.atraso_s)
        saida.write_bytes(b"\x00" * 64)


class ImagemLenta:
    def __init__(self, atraso_s: float):
        self.atraso_s = atraso_s
        self.chamadas = 0

    def gerar(self, prompt, saida, largura=1920, altura=1080):
        self.chamadas += 1
        time.sleep(self.atraso_s)
        saida.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)


def test_narracao_lenta_demais_desiste_em_vez_de_travar(tmp_path, monkeypatch):
    monkeypatch.setattr(producao, "ORCAMENTO_TTS_S", 0.05)
    monkeypatch.setattr(producao.media, "duracao", lambda _: 3.0)
    tts = TTSLento(atraso_s=0.08)

    with pytest.raises(producao.OrcamentoEstourado, match="narracao"):
        producao.narrar(tts, _roteiro(20), tmp_path)

    # Desistiu cedo, nao no fim: o teto existe para nao gastar o job inteiro.
    assert tts.chamadas < 20


def test_o_que_ja_ficou_pronto_sobrevive_ao_estouro(tmp_path, monkeypatch):
    """`maquina retomar` conta com os arquivos em disco."""
    monkeypatch.setattr(producao, "ORCAMENTO_TTS_S", 0.05)
    monkeypatch.setattr(producao.media, "duracao", lambda _: 3.0)

    with pytest.raises(producao.OrcamentoEstourado):
        producao.narrar(TTSLento(atraso_s=0.08), _roteiro(20), tmp_path)

    prontos = list((tmp_path / "audio").glob("*.mp3"))
    assert prontos, "os mp3 ja gerados nao podem sumir com o erro"


def test_ilustracao_tambem_tem_teto(tmp_path, monkeypatch):
    monkeypatch.setattr(producao, "ORCAMENTO_IMAGEM_S", 0.05)
    imagem = ImagemLenta(atraso_s=0.08)

    with pytest.raises(producao.OrcamentoEstourado, match="ilustracao"):
        producao.ilustrar(imagem, _roteiro(20), tmp_path, Formato.LONGO)

    assert imagem.chamadas < 20


def test_ritmo_normal_nao_e_interrompido(tmp_path, monkeypatch):
    """O teto e generoso de proposito: 60 s/cena contra ~5 s medidos."""
    monkeypatch.setattr(producao.media, "duracao", lambda _: 3.0)
    tts = TTSLento(atraso_s=0.001)

    producao.narrar(tts, _roteiro(30), tmp_path)

    assert tts.chamadas == 30


def test_mensagem_diz_onde_parou(tmp_path, monkeypatch):
    """Erro sem numero nao ajuda ninguem as duas da manha."""
    monkeypatch.setattr(producao, "ORCAMENTO_TTS_S", 0.05)
    monkeypatch.setattr(producao.media, "duracao", lambda _: 3.0)

    with pytest.raises(producao.OrcamentoEstourado) as e:
        producao.narrar(TTSLento(atraso_s=0.08), _roteiro(20), tmp_path)

    texto = str(e.value)
    assert "de 20 cenas" in texto
    assert "retomar" in texto
