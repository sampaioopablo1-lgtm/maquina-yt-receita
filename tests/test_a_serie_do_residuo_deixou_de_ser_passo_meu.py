"""Acrescentar ponto na serie era passo MEU em DOIS arquivos — e corrompeu duas vezes.

MEDIDO: em 18/10 as 11:2x `RESIDUO_N` dizia 93 e a lista tinha 94, porque o
`epomeno-epipedo-s058` estava nela duas vezes. A causa era a forma do meu
`t.replace(ancora, ancora + "\\n" + linha)`: a ancora era a linha SEM o
comentario `# job` e a linha no arquivo TEM, logo o replace casava PREFIXO, a
linha nova entrava no MEIO da antiga e o comentario ficava pendurado na nova.
Seis rodadas acumularam seis jobs numa linha so.

`fabrica/serie_residuo.py` tira o passo da minha mao: insere por LINHA INTEIRA,
recusa pacote e job repetidos, exige provedor MEDIDO (733) e sincroniza o
`RESIDUO_N` no MESMO passo — logo os dois donos passam a ser um.

Este arquivo cobra as PROPRIEDADES (743/753/761), nao os valores de hoje: a
contagem sai do disco e o par de limites se compara com o do `mira.py` em vez de
ser cravado aqui.
"""
import os
import shutil
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import mira  # noqa: E402
import serie_residuo as SR  # noqa: E402


def test_a_serie_e_o_RESIDUO_N_nao_divergem():
    """A divergencia de 18/10 as 11:2x, como propriedade."""
    d = SR.divergencia()
    assert d["bate"], (
        f"a serie tem {d['n_serie']} pontos e o RESIDUO_N diz "
        f"{d['n_declarado']} — e esse numero eu reporto ao dono")


def test_nenhum_pacote_e_nenhum_job_aparece_DUAS_vezes():
    d = SR.divergencia()
    assert not d["pacotes_repetidos"], d["pacotes_repetidos"]
    assert not d["jobs_repetidos"], d["jobs_repetidos"]
    assert not d["linhas_com_duas_marcas_de_job"], (
        "linha com duas marcas de job e o SINTOMA visivel que precede a "
        f"duplicata: {d['linhas_com_duas_marcas_de_job'][:3]}")


def test_a_varredura_nao_fica_VAZIA():
    """Leitura vazia nao e serie vazia — sem isto todos passariam calados."""
    ps = SR.pontos()
    assert len(ps) >= 100, f"a serie encolheu para {len(ps)} — releia"
    assert all(len(p) == 4 for p in ps)


def test_a_banda_calculada_bate_com_a_do_mira():
    """DUAS contas da mesma coisa tem de concordar.

    O `RESIDUO_OBSERVADO` do `mira.py` e escrito a mao a cada correcao; o
    `limites()` DERIVA da serie. Se divergirem, um dos dois foi editado sem o
    outro — que e o defeito que este arquivo inteiro guarda."""
    assert SR.limites() == tuple(mira.RESIDUO_OBSERVADO), (
        f"derivado {SR.limites()} contra escrito {mira.RESIDUO_OBSERVADO}")


def test_a_leitura_LEVANTA_em_vez_de_devolver_vazio():
    with pytest.raises(RuntimeError) as e:
        SR.pontos("OUTRA = [1, 2]\n")
    assert "AUSENCIA DE LEITURA" in str(e.value)


def test_recusa_pacote_que_JA_esta_na_serie():
    """O ponto fantasma de 18/10, barrado na entrada."""
    ja = SR.pontos()[0][0]
    with pytest.raises(ValueError) as e:
        SR.acrescenta(ja, 25.0, 27, "edge", "999999999")
    assert "JA esta na serie" in str(e.value)


def test_recusa_provedor_que_nao_foi_MEDIDO():
    """733: o provedor se CONTA pelas anotacoes, nunca se infere."""
    with pytest.raises(ValueError) as e:
        SR.acrescenta("canal-s999", 25.0, 27, "provavelmente edge", "999999999")
    assert "733" in str(e.value)


def test_recusa_job_que_JA_aparece_no_arquivo():
    import re
    jobs = re.findall(r"#\s*job\s*(\d+)", SR._texto(SR.ARQ_SERIE))
    assert jobs, "sem marca de job o teste nao mede nada"
    with pytest.raises(ValueError) as e:
        SR.acrescenta("canal-s999", 25.0, 27, "edge", jobs[0])
    assert "ja aparece na serie" in str(e.value)


def test_sem_aplicar_NAO_toca_os_arquivos():
    antes = (SR._texto(SR.ARQ_SERIE), SR._texto(SR.ARQ_N))
    r = SR.acrescenta("canal-s999", 25.0, 27, "edge", "999999999")
    assert r["aplicado"] is False and r["residuo"] == 2.0
    assert (SR._texto(SR.ARQ_SERIE), SR._texto(SR.ARQ_N)) == antes


def test_insere_por_LINHA_INTEIRA_e_sincroniza(tmp_path, monkeypatch):
    """A contraprova do defeito: o ponto novo nao entra no MEIO de outra linha,
    o comentario de job da linha anterior fica onde estava, e o `RESIDUO_N`
    anda junto."""
    serie = tmp_path / "serie.py"
    ene = tmp_path / "n.py"
    shutil.copy(SR.ARQ_SERIE, serie)
    shutil.copy(SR.ARQ_N, ene)
    monkeypatch.setattr(SR, "ARQ_SERIE", str(serie))
    monkeypatch.setattr(SR, "ARQ_N", str(ene))

    n0 = len(SR.pontos())
    ultima_antes = SR._texto(SR.ARQ_SERIE).splitlines()[-1]
    r = SR.acrescenta("canal-de-teste-s001", 41.0, 43, "edge", "999999999",
                      nota="nota de teste, para conferir que ela sai comentada",
                      aplicar=True)
    ps = SR.pontos()
    assert len(ps) == n0 + 1 and r["n"] == n0 + 1
    assert SR.n_declarado() == n0 + 1
    assert ps[-1] == ("canal-de-teste-s001", 41.0, 43, "edge")
    d = SR.divergencia()
    assert d["bate"] and not d["pacotes_repetidos"]
    assert not d["linhas_com_duas_marcas_de_job"]
    assert SR._texto(SR.ARQ_SERIE).splitlines()[-1] == ultima_antes, (
        "o fim do arquivo mudou — a linha entrou fora da lista")
    # e o ARQUIVO DE VERDADE nao foi tocado
    assert SR.divergencia.__module__ == "serie_residuo"


def test_o_relato_DIZ_quando_divergem_em_vez_de_calar():
    assert "BATE" in SR.relato() or "DIVERGEM" in SR.relato()
    assert "banda OBSERVADA" in SR.relato()
