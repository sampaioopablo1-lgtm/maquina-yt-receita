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
    contava linha sem youtube_id, e 50 nao era a meta de 10 por canal.

    Em 19/08/2026 a chave ficou mais forte: conta video DISTINTO, nao linha —
    o cron republicava o mesmo pacote e o placar somava cada copia. Onde nao
    ha titulo, a chave cai no youtube_id e o comportamento antigo continua,
    que e o caso desta fixture.
    """
    est = M.estado(DADOS)
    assert est["meta_total"] == 10 * len(M.canais_do_repo())
    esperado = len({(v["canal"], v["youtube_id"]) for v in DADOS
                    if v["formato"] == "longo" and v["youtube_id"]})
    assert est["publicados_total"] == esperado


def test_republicacao_nao_infla_o_placar():
    """Seis linhas do mesmo titulo sao UM video, mesmo com seis ids."""
    c = sorted(M.canais_do_repo())[0]
    videos = [{"canal": c, "formato": "longo", "pacote": None,
               "titulo": "Emerytura z ZUS: 34,4% pensji", "youtube_id": f"id{i}"}
              for i in range(6)]
    assert M.estado(videos)["canais"][c]["publicados"] == 1


def test_linha_sem_titulo_nao_some_da_contagem():
    """O modo de falha oposto e pior: sumir com video que existe faria a
    maquina reproduzir o que ja esta no ar."""
    c = sorted(M.canais_do_repo())[0]
    videos = [{"canal": c, "formato": "longo", "pacote": None,
               "titulo": None, "youtube_id": f"id{i}"} for i in range(3)]
    assert M.estado(videos)["canais"][c]["publicados"] == 3


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


# ------------------------------------------------ o teto que valia por disparo

def _agora():
    import datetime as dt
    return dt.datetime(2026, 8, 19, 18, 0, tzinfo=dt.timezone.utc)


def _ha(horas: float) -> str:
    import datetime as dt
    return (_agora() - dt.timedelta(hours=horas)).isoformat()


def test_a_consulta_traz_as_colunas_da_janela(monkeypatch):
    """Some `criado_em` do select e a janela zera em silencio — o teto volta a
    valer por disparo sem que nada falhe. Este teste e o que segura a coluna."""
    vistas = {}

    class Falsa:
        def __init__(self, url, headers=None):
            vistas["url"] = url

        def __enter__(self):
            import io
            return io.BytesIO(b"[]")

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(M.urllib.request, "Request", Falsa)
    monkeypatch.setattr(M.urllib.request, "urlopen", lambda req, timeout=0: req)
    M.busca_videos("https://x", "k")
    for col in ("criado_em", "status", "slug", "pacote", "canal"):
        assert col in vistas["url"], f"{col} sumiu do select: {vistas['url']}"


def test_janela_conta_pacote_distinto_como_a_v_maquina_fila():
    """Mesma chave, mesmo filtro, mesma janela movel. Duas contagens do mesmo
    teto que discordam sao piores que uma so."""
    videos = [
        # um pacote, duas linhas (longo + short) — vale UM
        {"canal": "epomeno-epipedo", "pacote": "epomeno-epipedo-007",
         "slug": "epomeno-epipedo-007", "status": "publicado",
         "criado_em": _ha(2)},
        {"canal": "epomeno-epipedo", "pacote": "epomeno-epipedo-007",
         "slug": "epomeno-epipedo-007-short", "status": "publicado",
         "criado_em": _ha(2)},
        # sem `pacote`: a chave cai no slug sem o sufixo -short
        {"canal": "epomeno-epipedo", "pacote": None,
         "slug": "epomeno-epipedo-006-short", "status": "publicado",
         "criado_em": _ha(6)},
        {"canal": "epomeno-epipedo", "pacote": None,
         "slug": "epomeno-epipedo-006", "status": "publicado",
         "criado_em": _ha(6)},
        # fora da janela
        {"canal": "epomeno-epipedo", "pacote": "epomeno-epipedo-005",
         "slug": "epomeno-epipedo-005", "status": "publicado",
         "criado_em": _ha(30)},
        # status descartado pela view
        {"canal": "epomeno-epipedo", "pacote": "epomeno-epipedo-009",
         "slug": "epomeno-epipedo-009", "status": "erro",
         "criado_em": _ha(1)},
        {"canal": "epomeno-epipedo", "pacote": "epomeno-epipedo-010",
         "slug": "epomeno-epipedo-010", "status": "cancelado",
         "criado_em": _ha(1)},
    ]
    assert M.pacotes_na_janela(videos, agora=_agora()) == {"epomeno-epipedo": 2}


def test_janela_e_movel_e_nao_o_relogio_do_dia():
    """A `v_maquina_fila` usa `now() - 24h`, nao meia-noite. Se a matriz usasse
    o dia civil, um disparo as 23h e outro a 00h dariam seis pacotes em duas
    horas com as duas contagens dizendo tres."""
    videos = [{"canal": "c", "pacote": f"c-00{i}", "slug": f"c-00{i}",
               "status": "publicado", "criado_em": _ha(h)}
              for i, h in enumerate((23.9, 24.1))]
    assert M.pacotes_na_janela(videos, agora=_agora()) == {"c": 1}


def test_teto_conta_o_que_ja_esta_no_banco_e_nao_so_o_disparo(monkeypatch):
    """O defeito de 19/08/2026: `por_canal_hoje` nascia VAZIO, entao contava so
    o que a propria matriz escolhia. Com o diario.yml disparando de meia em
    meia hora, "tres por dia" era na verdade "tres por disparo" — o
    epomeno-epipedo recebeu o quarto pacote do dia com a trava intacta.

    O teste antigo (`test_teto_de_tres_por_dia_por_canal`) passava o tempo
    todo: ele so olhava as escolhidas de UMA chamada.
    """
    canal = sorted(M.canais_do_repo())[0]
    livre, _ = M.proximo(DADOS, n=50)
    disponiveis = [e for e in livre if e["canal"] == canal]
    if not disponiveis:
        pytest.skip(f"{canal} nao tem spec pendente aprovada no corpus")

    # o canal ja registrou o teto inteiro nas ultimas 24h, em outro disparo
    cheio = DADOS + [{"canal": canal, "pacote": f"{canal}-j{i}",
                      "slug": f"{canal}-j{i}", "status": "publicado",
                      "formato": "longo", "youtube_id": None, "titulo": None,
                      "criado_em": _ha(i + 1)}
                     for i in range(M.MAX_POR_DIA_POR_CANAL)]
    escolhidas, descartadas = M.proximo(cheio, n=50)
    assert not [e for e in escolhidas if e["canal"] == canal], \
        f"{canal} ja tinha {M.MAX_POR_DIA_POR_CANAL} na janela e entrou de novo"
    motivos = [d["motivo"] for d in descartadas
               if d["spec"].startswith(canal) and "teto" in d["motivo"]]
    assert motivos, "descartou sem dizer que foi o teto"
    assert str(M.MAX_POR_DIA_POR_CANAL) in motivos[0], motivos[0]


def test_janela_ignora_linha_sem_criado_em():
    """Corpus antigo nao tem a coluna. Contar essas linhas como recentes
    travaria a frota inteira num teto que ninguem pediu."""
    assert M.pacotes_na_janela(DADOS, agora=_agora()) == {}


def test_relatorio_mostra_a_janela_de_24h():
    """Teto invisivel e teto que ninguem entende: o relatorio dizia que a spec
    estava pendente sem dizer que o canal ja tinha esgotado o dia."""
    txt = M.relatorio(DADOS)
    assert "24h" in txt
