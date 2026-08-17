"""A duracao prevista tem que bater com a que foi ao ar.

O defeito prendido aqui (17/08/2026): o MODELO_VOZ era calibrado com duas
amostras sinteticas por voz e as NOVE vozes com dados de producao subestimavam,
de +6,6% a +18,0%. Nove de nove para o mesmo lado. O resep-naik-level-003 foi
dimensionado para 14,2 min, passou no portao de duracao (teto 15,0) e foi
publicado com 16:14.

O teste que importa nao e o do ajuste — e o de PROCEDENCIA: garantir que ninguem
volte a por numero de laboratorio na tabela sem medir.
"""

import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

from calibra_voz import ajusta, coleta, tempos  # noqa: E402
from ensaio import GAP_CENA_S, MODELO_VOZ, duracao_estimada  # noqa: E402

# As nove medidas contra .srt de producao em 17/08/2026. Mexer numa destas sem
# rodar o calibra_voz.py de novo e voltar ao defeito.
MEDIDAS_EM_PRODUCAO = {
    "pt-BR-AntonioNeural", "pt-BR-ThalitaMultilingualNeural",
    "id-ID-GadisNeural", "id-ID-ArdiNeural", "es-MX-DaliaNeural",
    "en-GB-RyanNeural", "en-US-AndrewNeural", "tr-TR-AhmetNeural",
    "hi-IN-MadhurNeural", "pt-BR-FranciscaNeural",
}


def _srt(blocos):
    """blocos = [(inicio_s, fim_s, texto)] -> texto de um .srt."""
    def hms(s):
        return (f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:"
                f"{int(s % 60):02d},{int(round(s % 1 * 1000)):03d}")
    return "\n\n".join(
        f"{i}\n{hms(a)} --> {hms(z)}\n{t}"
        for i, (a, z, t) in enumerate(blocos, 1)
    ) + "\n"


def test_ajuste_recupera_os_parametros_que_geraram_os_dados():
    """Dados sinteticos com R e P conhecidos: o ajuste tem que devolve-los."""
    R, P = 15.0, 1.2
    C = [80, 120, 160, 200, 100, 140]
    F = [1, 3, 2, 5, 4, 2]
    D = [c / R + f * P for c, f in zip(C, F)]
    r = ajusta(C, F, D)
    assert r is not None
    assert r[0] == pytest.approx(R, rel=1e-6)
    assert r[1] == pytest.approx(P, abs=1e-6)


def test_ajuste_degenerado_devolve_none():
    """Se chars/frases e constante, os dois termos sao indistinguiveis.

    Devolver um par qualquer da reta seria pior que nao devolver nada: entraria
    na tabela parecendo medido.
    """
    C = [100, 200, 300]
    F = [1, 2, 3]                       # razao chars/frases identica
    D = [c / 15.0 + f * 1.2 for c, f in zip(C, F)]
    assert ajusta(C, F, D) is None


def test_tempos_le_o_srt(tmp_path):
    p = tmp_path / "x.srt"
    p.write_text(_srt([(0.15, 12.817, "a"), (13.117, 23.45, "b")]), encoding="utf-8")
    t = tempos(str(p))
    assert t == [(0.15, 12.817), (13.117, 23.45)]


def test_coleta_pula_pacote_com_contagem_diferente(tmp_path):
    """No bucket ha .srt gravado sob o nome de outro pacote.

    Casar o texto de uma spec com o tempo de outra envenena o ajuste sem
    levantar erro nenhum — por isso o par tem que ser recusado inteiro.
    """
    specs = tmp_path / "specs"
    srts = tmp_path / "srt"
    specs.mkdir()
    srts.mkdir()
    import json
    (specs / "p.json").write_text(json.dumps({
        "voz": "id-ID-GadisNeural",
        "longo": [{"nar": "Satu dua tiga."}, {"nar": "Empat lima enam."}],
    }), encoding="utf-8")
    # tres legendas para uma spec de duas cenas
    (srts / "p.srt").write_text(
        _srt([(0, 5, "a"), (5.3, 10, "b"), (10.3, 15, "c")]), encoding="utf-8")

    por_voz, _, pulados = coleta(str(srts), str(specs))
    assert por_voz == {}
    assert pulados and pulados[0][0] == "p"
    assert "srt=3" in pulados[0][1] and "spec=2" in pulados[0][1]


def test_gap_e_intervalo_entre_cenas_nao_por_cena():
    """n cenas tem n-1 intervalos. Multiplicar por n soma uma cena fantasma."""
    cena = {"nar": "Satu dua tiga empat."}
    voz = "id-ID-GadisNeural"
    uma = duracao_estimada([cena], voz)
    duas = duracao_estimada([cena, cena], voz)
    assert duas - uma == pytest.approx(uma + GAP_CENA_S)
    # uma cena sozinha nao tem intervalo nenhum
    from ensaio import duracao_cena
    assert uma == pytest.approx(duracao_cena(cena["nar"], voz))


def test_lista_vazia_nao_estoura():
    assert duracao_estimada([], "id-ID-GadisNeural") == 0


def test_gap_e_o_valor_unico_medido():
    """1.056 intervalos medidos em 13 pacotes, todos exatamente 0,300 s."""
    assert GAP_CENA_S == 0.300


def test_as_nove_medidas_continuam_na_tabela():
    faltando = MEDIDAS_EM_PRODUCAO - set(MODELO_VOZ)
    assert not faltando, f"vozes medidas sumiram do MODELO_VOZ: {faltando}"


def test_nenhuma_voz_medida_voltou_ao_valor_de_laboratorio():
    """Os valores de laboratorio, para conferencia de regressao.

    Se alguem restaurar um destes, o portao volta a aprovar roteiro que estoura
    o teto — foi assim que o resep-naik-level-003 saiu com 16:14.
    """
    laboratorio = {
        "pt-BR-AntonioNeural": 18.56, "pt-BR-ThalitaMultilingualNeural": 19.09,
        "id-ID-GadisNeural": 17.42, "id-ID-ArdiNeural": 23.76,
        "es-MX-DaliaNeural": 21.14, "en-GB-RyanNeural": 21.90,
        "en-US-AndrewNeural": 18.45, "tr-TR-AhmetNeural": 16.96,
        "hi-IN-MadhurNeural": 13.10,
    }
    for voz, R_velho in laboratorio.items():
        assert MODELO_VOZ[voz][0] != R_velho, f"{voz} voltou ao valor de laboratorio"
        # todas as nove mediram MAIS LENTO que o laboratorio dizia
        assert MODELO_VOZ[voz][0] < R_velho, f"{voz} ficou mais rapido que o medido"


def test_francisca_errava_na_pausa_e_nao_na_taxa():
    """A decima voz medida (17/08/2026) erra num eixo diferente das nove.

    R praticamente nao mudou (16,97 -> 16,92) e P triplicou (0,310 -> 1,036),
    e mesmo assim o total subestimava 15,6%. Conferir so chars/s deixaria essa
    voz passar — por isso o modelo tem que ter os dois termos MEDIDOS, nao um
    medido e outro herdado.
    """
    R, P = MODELO_VOZ["pt-BR-FranciscaNeural"]
    assert R == pytest.approx(16.92, abs=0.01)
    assert P == pytest.approx(1.036, abs=0.001)
    assert P > 3 * 0.310, "P voltou ao valor de laboratorio"
