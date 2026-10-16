"""O ramo sem spec local do `segundo_angulo` calava sobre os usos anteriores.

Medido em 16/10 as 19:2x, e o custo foi um short inteiro reescrito. A pauta
servia o topo do `labtreinamento` (`FtCtIJPsc_Q`, o longo da referencia), que NAO
tem spec local. O `segundo_angulo` respondeu, corretamente, que nao resolve para
pacote nenhum e que a rota e o `capitulos.yml` com `legenda=true` — e **parou
ali**. Eu escrevi o short sobre o terceiro limite do longo, e o portao
`similaridade` reprovou com 0,69 e depois 0,73: nao era titulo parecido, era a
FAMILIA que o `labtreinamento-s059` ja tinha usado, saindo da MESMA origem.
Troquei o titulo duas vezes antes de entender que o portao falava de CONTEUDO.

**O modulo TINHA a informacao.** `shorts_da_origem(yid)` lista as specs que
declaram aquele `longo_existente`, e o `continue` do ramo sem pacote a jogava
fora junto com o resto do relato. Quando ha spec local, a mesma lista sai
impressa — logo a cegueira era EXATAMENTE do caso em que a origem e nova para o
disco, que e o caso da regra (h) e por isso o mais provavel de repetir familia.

O que o conserto NAO faz, e vai dito: ele nomeia as PECAS, nao os capitulos
usados. Sem spec local nao ha kicker para cruzar, logo `nao_mencionados` continua
sem resposta e a leitura das copies anteriores continua sendo trabalho de quem
escreve. O modulo passou a dizer onde olhar em vez de calar.
"""
import json
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import segundo_angulo as sa  # noqa: E402

ORIGEM_REAL = "FtCtIJPsc_Q"
# As pecas que saiam dela quando o defeito foi medido. Outras podem entrar.
NA_EPOCA = {
    "labtreinamento-s058", "labtreinamento-s059",
    "labtreinamento-s061", "labtreinamento-s062", "labtreinamento-s063",
}
# A colisao real: as duas usaram a familia da POSICAO como endereco.
COLIDIRAM = ("labtreinamento-s059", "labtreinamento-s063")


def _relato(*args):
    r = subprocess.run(
        [sys.executable, str(RAIZ / "fabrica" / "segundo_angulo.py"), *args],
        capture_output=True, text=True, timeout=180)
    return r.stdout


def test_a_origem_real_NAO_resolve_para_pacote():
    """A premissa do achado: sem isso o teste passaria por vacuidade."""
    assert sa.pacote_do_id(ORIGEM_REAL) is None, (
        "se esta origem passar a ter spec local, este arquivo descreve um caso "
        "que deixou de existir e tem de ser RELIDO, nao ajustado"
    )


def test_o_relato_NOMEIA_os_shorts_anteriores_mesmo_sem_pacote():
    saida = _relato(ORIGEM_REAL)
    assert "legenda=true" in saida, "a rota da regra (h) continua indicada"
    for nome in sorted(NA_EPOCA):
        assert nome in saida, (
            f"{nome} sai desta origem e tem de ir NOMEADO — foi calar sobre "
            "isso que me fez repetir familia"
        )


def test_as_DUAS_pecas_que_colidiram_saem_da_mesma_origem():
    """A evidencia do custo, lida do disco e nao da minha memoria."""
    for nome in COLIDIRAM:
        sp = json.loads((RAIZ / "fabrica" / "specs" / f"{nome}.json").read_text())
        assert sp.get("longo_existente") == ORIGEM_REAL


def test_o_relato_DIZ_quando_e_primeiro_angulo():
    """Nao havendo peca anterior, ele afirma isso em vez de calar (761)."""
    saida = _relato("ZZnaoExisteZZ")
    assert "primeiro" in saida and "familia anterior" in saida


def test_o_relato_declara_o_PONTO_CEGO_que_sobra():
    """Nomear pecas nao e nomear capitulos, e o modulo nao finge que e."""
    saida = _relato(ORIGEM_REAL)
    assert "nao sabe quais capitulos" in saida, (
        "o limite tem de sair IMPRESSO: quem le precisa saber que ainda tem de "
        "abrir a copy de cada peca"
    )


def test_quando_HA_spec_local_a_lista_continua_saindo():
    """Contraprova do outro lado: o conserto nao mexeu no ramo que funcionava."""
    com_spec = "nttW9fR8wyY"
    if sa.pacote_do_id(com_spec) is None:
        import pytest
        pytest.skip("a origem de controle perdeu a spec local")
    saida = _relato(com_spec)
    assert "shorts:" in saida and "epomeno-epipedo-s" in saida


def test_o_docstring_registra_que_a_informacao_JA_EXISTIA():
    texto = " ".join(__doc__.split())
    assert "TINHA a informacao" in texto
    assert "shorts_da_origem" in texto
