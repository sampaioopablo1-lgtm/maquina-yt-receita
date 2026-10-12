"""Contar pauta por ID em vez de por TITULO infla o estoque. Medido duas vezes.

`fabrica/pauta_local.py` existe porque eu errei a conta da pauta DUAS vezes em
12/10, e a segunda foi dentro da correcao da primeira:

  * as 07:0x eu reportei "cinco origens livres", contando ids;
  * as 08:2x eu corrigi para "tres", depois de ver que dez dos doze ids livres
    eram o MESMO titulo (`Emerytura z ZUS`), publicado onze vezes por um cron
    entre 13 e 17/08;
  * e as 08:4x o proprio modulo mostrou que eram **dois**: o
    `W_iFAIQWvi8` e uma SEGUNDA copia de `Próg Podatkowy 120 000 zł` cuja irma
    `SP7Vz8qHdRY` ja esta consumida por uma spec. O titulo ja esta servido.

Esses dois casos reais sao as ancoras destes testes. Se alguem voltar a contar
por id, ou parar de excluir grupo parcialmente usado, eles falham.

**E a defesa nao pode ser `docs/duplicatas-a-apagar.md`:** as dez copias do ZUS
nao estao nele. Ha um teste exigindo que isso continue verdade — se um dia
estiverem, o teste avisa, e a ancora precisa ser revista em vez de passar por
vacuidade.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import pauta_local as PL  # noqa: E402

ZUS = "Emerytura z ZUS"
PROG = "Próg Podatkowy 120 000"


def test_o_grupo_ZUS_tem_muitas_copias_no_ar():
    """A ancora. Sem isto, os testes abaixo passariam por vacuidade."""
    todos = PL.longos_publicados()
    ids = [y for y, (_, tit, _) in todos.items() if tit.startswith(ZUS)]
    assert len(ids) >= 5, (
        f"so {len(ids)} copias do grupo ZUS no retrato — a ancora destes testes "
        f"mudou, revise-os em vez de afrouxa-los")


def test_dez_copias_de_um_titulo_valem_UMA_origem():
    L = PL.livres()
    grupos = [(t, ids) for t, _, ids in L if t.startswith(ZUS)]
    assert len(grupos) <= 1, "o mesmo titulo saiu como varias origens"
    if grupos:
        _, ids = grupos[0]
        assert len(ids) > 1, (
            "o grupo ZUS tem copias no ar; se so uma aparece, a contagem "
            "voltou a ser por id")


def test_ids_livres_e_origens_livres_sao_numeros_DIFERENTES():
    """Era exatamente a confusao que produziu o "cinco"."""
    L = PL.livres()
    ids = sum(len(i) for _, _, i in L)
    assert ids >= len(L)
    # no retrato de hoje ha grupo com copia, entao tem de haver diferenca
    assert ids > len(L), (
        "sem nenhum grupo com copia, este teste nao esta medindo nada — "
        "confira a ancora do ZUS")


def test_grupo_PARCIALMENTE_usado_sai_inteiro():
    """`W_iFAIQWvi8` esta livre, mas a irma `SP7Vz8qHdRY` ja foi consumida."""
    todos = PL.longos_publicados()
    usadas = PL.origens_usadas()
    irmas = [y for y, (_, tit, _) in todos.items() if PROG in tit]
    assert len(irmas) >= 2, f"ancora mudou: {irmas}"
    assert any(y in usadas for y in irmas), (
        "nenhuma copia do grupo Prog esta usada — ancora mudou")
    livres_ids = {y for _, _, ids in PL.livres() for y in ids}
    assert not (set(irmas) & livres_ids), (
        "o grupo Prog voltou a ser oferecido como pauta livre, mas o titulo "
        "dele ja esta no ar por outra copia — seria a MESMA pauta de novo")


def test_origem_consumida_nesta_rodada_nao_e_mais_oferecida():
    """O `uWs-k_Wrn_w` foi para o `epomeno-epipedo-s017` em 12/10."""
    livres_ids = {y for _, _, ids in PL.livres() for y in ids}
    assert "uWs-k_Wrn_w" not in livres_ids
    assert "uWs-k_Wrn_w" in PL.origens_usadas()


def test_short_e_longo_sem_id_ficam_FORA():
    """Short nao e origem, e longo sem id nao pode ser apontado."""
    for _, (pacote, _, _) in PL.longos_publicados().items():
        assert pacote
    linhas = PL._linhas()
    com_id = {v.get("youtube_id") for v in linhas if v.get("youtube_id")}
    assert set(PL.longos_publicados()) <= com_id


def test_as_dez_copias_do_ZUS_NAO_estao_no_documento_de_duplicatas():
    """Era por isso que subtrair o documento nao salvava a conta."""
    doc = RAIZ / "docs/duplicatas-a-apagar.md"
    if not doc.exists():
        return
    texto = doc.read_text()
    todos = PL.longos_publicados()
    zus = [y for y, (_, tit, _) in todos.items() if tit.startswith(ZUS)]
    dentro = [y for y in zus if y in texto]
    assert len(dentro) < len(zus), (
        "agora TODAS as copias do ZUS estao no documento de duplicatas — a "
        "premissa deste modulo mudou e o relato precisa ser revisto")


def test_o_relato_carrega_as_TRES_ressalvas():
    r = PL.relato()
    assert "06/10" in r and "SUBESTIMA" in r
    assert "por TITULO" in r
    assert "estoque.sql" in r, (
        "o relato tem de dizer que NAO substitui a consulta")
