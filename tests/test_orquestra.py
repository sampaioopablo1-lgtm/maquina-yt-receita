"""A selecao e a contagem nao podem depender de mim.

Cada teste aqui corresponde a um erro que eu cometi em 13/08/2026 lendo o
estado a mao. Se algum deles cair, o erro voltou.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import orquestra as M  # noqa: E402

DADOS = json.loads((RAIZ / "tests" / "dados_videos.json").read_text(encoding="utf-8"))


def test_pacote_no_ar_nunca_entra_no_disparo():
    """O erro caro: contei quinze specs como prontas e dez ja estavam no ar.

    Disparar aquela lista teria posto duplicata em dez canais.
    """
    escolhidas, _ = M.proximo(DADOS, n=50)
    nomes = {e["pacote"] for e in escolhidas}
    ja = M.publicados_por_pacote(DADOS)
    assert not (nomes & ja), f"escolheu pacote publicado: {nomes & ja}"
    # e as que EU chamei de prontas e estavam no ar continuam fora
    for p in ("setiap-level-004", "agla-level-003", "epomeno-epipedo-002",
              "game-money-lab-002", "resep-naik-level-002", "setiap-level-006"):
        assert p not in nomes


def test_contagem_so_conta_longo_com_youtube_id():
    """Eu vinha reportando "estoque 31/50". Os dois numeros estavam errados: 31
    contava linha sem youtube_id, e 50 nao era a meta de 10 por canal."""
    est = M.estado(DADOS)
    assert est["meta_total"] == 10 * len(M.canais_do_repo())
    esperado = len({(v["canal"], v["youtube_id"]) for v in DADOS
                    if v["formato"] == "longo" and v["youtube_id"]})
    assert est["publicados_total"] == esperado


def test_canal_mais_longe_da_meta_vem_primeiro():
    """A meta e POR CANAL: o primeiro video de um canal em zero vale mais que
    o decimo de um canal com nove."""
    escolhidas, _ = M.proximo(DADOS, n=50)
    est = M.estado(DADOS)
    faltas = [est["canais"][e["canal"]]["faltam"] for e in escolhidas]
    assert faltas == sorted(faltas, reverse=True), faltas


def test_teto_de_tres_por_dia_por_canal():
    muitos = DADOS + []
    escolhidas, descartadas = M.proximo(muitos, n=50)
    por_canal: dict[str, int] = {}
    for e in escolhidas:
        por_canal[e["canal"]] = por_canal.get(e["canal"], 0) + 1
    assert all(v <= M.MAX_POR_DIA_POR_CANAL for v in por_canal.values()), por_canal


def test_spec_travada_e_descartada_com_o_motivo():
    """Descartar em silencio e como nao descartar: ninguem sabe o que consertar."""
    _, descartadas = M.proximo(DADOS, n=50)
    assert descartadas, "nenhuma descartada — o corpus tem specs travadas"
    for d in descartadas:
        assert d["motivo"].strip(), d


def test_toda_escolhida_declara_canal_pacote_e_idioma():
    """A matriz alimenta o frota.yml direto. Faltando idioma, o video sobe
    marcado na lingua errada; faltando pacote, o render escreve num diretorio
    e a entrega procura noutro."""
    escolhidas, _ = M.proximo(DADOS, n=50)
    assert escolhidas
    for e in escolhidas:
        assert e["canal"] and e["pacote"] and e["idioma"], e
        assert e["pacote"].startswith(e["canal"]), e


def test_linhas_sem_pacote_sao_contadas_e_nao_escondidas():
    """Onde falta `pacote`, a trava contra republicacao e cega. O relatorio tem
    que dizer quantas sao, senao o buraco fica invisivel."""
    est = M.estado(DADOS)
    assert est["linhas_sem_pacote"] > 0
    assert "sem `pacote`" in M.relatorio(DADOS)


def test_relatorio_mostra_quantos_longos_ainda_nao_tem_spec():
    """A meta de 10 por canal nao esbarra em render, esbarra em roteiro. O
    informe precisa dizer isso, senao a conversa fica sobre a infraestrutura."""
    texto = M.relatorio(DADOS)
    assert "ainda nao tem spec escrita" in texto


@pytest.mark.parametrize("n", [0, 1, 3, 10])
def test_n_limita_o_disparo(n):
    escolhidas, _ = M.proximo(DADOS, n=n)
    assert len(escolhidas) <= n


def test_proximo_imprime_json_limpo_em_stdout(capsys, monkeypatch):
    """O diario.yml alimenta o disparo com o stdout de `proximo`.

    Um aviso impresso no meio corrompe o JSON e o disparo morre — ou dispara
    errado. Aconteceu: o `ler_copy` avisava "copy.md ausente" em stdout, e as
    specs de producao passam por ele em todo `proximo`.
    """
    monkeypatch.setattr(sys, "argv", ["orquestra.py", "proximo", "--n", "3",
                                      "--dados", str(RAIZ / "tests" / "dados_videos.json")])
    M.main()
    saida = capsys.readouterr()
    dados = json.loads(saida.out)          # levanta se houver qualquer sujeira
    assert isinstance(dados, list) and dados
    assert "aviso" not in saida.out


def test_orquestra_nao_colide_com_o_pacote_maquina():
    """`src/maquina/` ja e um pacote instalado.

    Enquanto este modulo se chamava fabrica/maquina.py, `import maquina` trazia
    um ou outro conforme a ordem de importacao: os testes passavam sozinhos e
    treze quebravam na suite inteira. Modulo que troca de identidade sem avisar
    e o defeito mais caro deste repositorio — foi assim que uma copia velha da
    fabrica produziu o pacote errado sem levantar erro.
    """
    import importlib

    pacote = importlib.import_module("maquina")
    assert not hasattr(pacote, "proximo"), (
        "o pacote src/maquina expoe `proximo` — o nome voltou a colidir"
    )
    assert Path(M.__file__).name == "orquestra.py"
    assert Path(M.__file__).parent.name == "fabrica"
