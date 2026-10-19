"""Eu contei os envios da janela de cabeca DUAS vezes e errei as duas.

MEDIDO: as 00:2x de 19/10 escrevi "ontem a frota fechou o dia em seis pecas"
(o dia tinha dezessete depois das 07:00 — eu contei as seis ULTIMAS), e as 04:1x
escrevi "doze envios, logo a cota e >= 19.200" quando a janela tinha vinte e
quatro. **Errado pela METADE**, e nas duas vezes a regra certa ja estava escrita
por mim no `CLAUDE.md`: *"conte as pecas da JANELA, nao do dia calendario"*.

`fabrica/janela_de_cota.py` tira o passo da minha mao: le o parque (toda peca
publicada entra nele desde 18/10 as 06:1x), corta na virada das 07:00 UTC e
conta por `youtube_id` DISTINTO.

Este arquivo cobra PROPRIEDADE (743/753/761): nada aqui crava "25" nem a data de
hoje — o que ele trava e a forma da conta, que e o que eu errei.
"""
import datetime
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import janela_de_cota as JC  # noqa: E402

UTC = datetime.timezone.utc


def test_a_virada_e_as_07_UTC_e_nao_a_meia_noite():
    """O erro de enquadramento do 771: dia calendario apaga as ultimas horas."""
    antes = datetime.datetime(2026, 10, 19, 6, 59, tzinfo=UTC)
    depois = datetime.datetime(2026, 10, 19, 7, 0, tzinfo=UTC)
    assert JC.abertura(antes) == datetime.datetime(2026, 10, 18, 7, 0, tzinfo=UTC)
    assert JC.abertura(depois) == datetime.datetime(2026, 10, 19, 7, 0, tzinfo=UTC)
    # meia-noite UTC ainda pertence a janela do dia ANTERIOR
    meia = datetime.datetime(2026, 10, 19, 0, 1, tzinfo=UTC)
    assert JC.abertura(meia).day == 18


def test_recusa_hora_SEM_fuso_em_vez_de_supor_UTC():
    with pytest.raises(ValueError):
        JC.abertura(datetime.datetime(2026, 10, 19, 6, 0))


def test_conta_por_id_DISTINTO_e_nao_por_LINHA(tmp_path):
    """Duas linhas do mesmo id sao reescrita, nao dois envios — foi contar
    linha que produziu o ponto fantasma da serie em 18/10."""
    arq = tmp_path / "p.jsonl"
    linhas = [
        {"em": "2026-10-18T08:00:00Z", "pacote": "a-s001", "youtube_id": "AAA"},
        {"em": "2026-10-18T08:00:00Z", "pacote": "a-s001", "youtube_id": "AAA"},
        {"em": "2026-10-18T09:00:00Z", "pacote": "a-s002", "youtube_id": "BBB"},
    ]
    arq.write_text("\n".join(json.dumps(d) for d in linhas), encoding="utf-8")
    agora = datetime.datetime(2026, 10, 18, 12, 0, tzinfo=UTC)
    assert JC.piso(agora, str(arq))["envios"] == 2


def test_a_peca_ANTES_da_virada_fica_de_FORA(tmp_path):
    """O caso exato que eu errei ao contar 'o dia' em vez da janela."""
    arq = tmp_path / "p.jsonl"
    linhas = [
        {"em": "2026-10-18T06:59:00Z", "pacote": "a-s000", "youtube_id": "ZZZ"},
        {"em": "2026-10-18T07:00:00Z", "pacote": "a-s001", "youtube_id": "AAA"},
        {"em": "2026-10-18T18:16:00Z", "pacote": "a-s002", "youtube_id": "BBB"},
    ]
    arq.write_text("\n".join(json.dumps(d) for d in linhas), encoding="utf-8")
    agora = datetime.datetime(2026, 10, 19, 6, 0, tzinfo=UTC)
    p = JC.piso(agora, str(arq))
    assert p["envios"] == 2 and p["primeiro"] == "a-s001"


def test_o_sub_intervalo_NAO_e_a_janela(tmp_path):
    """A forma literal do erro de 04:1x: contar so a cauda da janela.

    Com dezessete pecas, contar as seis ultimas da 6 e a janela da 17 — e a
    razao entre as duas contagens e o que eu reportei ao dono como cota."""
    arq = tmp_path / "p.jsonl"
    base = datetime.datetime(2026, 10, 18, 7, 15, tzinfo=UTC)
    linhas = [{"em": (base + datetime.timedelta(hours=i)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"), "pacote": f"a-s{i:03d}",
        "youtube_id": f"ID{i:03d}"} for i in range(17)]
    arq.write_text("\n".join(json.dumps(d) for d in linhas), encoding="utf-8")
    agora = datetime.datetime(2026, 10, 19, 6, 0, tzinfo=UTC)
    assert JC.piso(agora, str(arq))["envios"] == 17


def test_o_custo_e_o_MEDIDO_e_nao_um_numero_qualquer():
    assert JC.CUSTO_VIDEOS_INSERT == 1600
    agora = datetime.datetime(2026, 10, 19, 6, 0, tzinfo=UTC)
    p = JC.piso(agora)
    assert p["unidades"] == p["envios"] * 1600


def test_le_o_PARQUE_de_verdade_e_nao_fica_vazio():
    """Sem isto o modulo passaria verde lendo um arquivo que encolheu."""
    agora = datetime.datetime.now(UTC)
    e = JC.envios(agora)
    assert isinstance(e, list)
    # a janela corrente pode estar vazia logo depois da virada; o que NAO pode
    # e o arquivo inteiro nao ter envio nenhum.
    with open(JC.PARQUE, encoding="utf-8") as f:
        total = sum(1 for l in f if l.strip())
    assert total >= 30, f"o parque encolheu para {total} linhas — releia"


def test_o_relato_diz_que_e_PISO_e_nao_teto():
    """O 19/10 inteiro foi trocar um numero suposto por outro; o modulo nao
    pode voltar a dizer 'a cota e N'."""
    agora = datetime.datetime(2026, 10, 19, 6, 0, tzinfo=UTC)
    texto = JC.relato(agora)
    assert "PISO" in texto and "TETO segue desconhecido" in texto
    assert "403" in texto


def test_o_MOTIVO_dos_dois_erros_continua_escrito():
    with open(os.path.join(RAIZ, "fabrica", "janela_de_cota.py"),
              encoding="utf-8") as f:
        texto = " ".join(f.read().split())
    for frase in ("seis ULTIMAS", "METADE", "item 3 da §10"):
        assert frase in texto, f"o motivo perdeu {frase!r}"
