"""O `youtube_id` da publicacao tem de chegar a uma ANOTACAO. Medido duas vezes.

Historia curta e inteira do defeito, em 12/10/2026:

  1. o registro da publicacao era so impresso no LOG. Log de job nao se le por
     API quando o MCP do GitHub esta fora, entao o `kolejny-poziom-s018`
     publicou com sucesso (run 38217420591) e eu nao tinha como saber o id;
  2. consertei pondo um heredoc `python3 - <<'PYFIM'` INLINE no `retomar.yml`;
  3. **o conserto saiu errado**: ele iterava o TOPO do registro em vez de
     `linhas`. O run 38223514079 publicou o `epomeno-epipedo-s017` e a anotacao
     saiu `youtube_id=? titulo=` — pior que nao existir, porque tem cara de
     dado;
  4. o parsing saiu do YAML e virou `fabrica/registro_anota.py`, que tem teste.

**A licao travada aqui nao e sobre dicionario: e que logica dentro do YAML nao
tem suite.** O caso real de (3) e a ancora do primeiro teste.
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import registro_anota as R  # noqa: E402

# A FORMA REAL, copiada do log do run 38223514079 (epomeno-epipedo-s017).
REAL = {
    "canal": "epomeno-epipedo",
    "pacote": "epomeno-epipedo-s017",
    "linhas": [{
        "slug": "epomeno-epipedo-s017-short",
        "status": "publicado",
        "formato": "shorts",
        "titulo": "Δες ποια μείωση λείπει",
        "youtube_id": "rusVeiFco9Q",
        "duracao_s": None,
        "cenas": 11,
        "capitulos": 0,
        "supabase_url": None,
        "canal": "epomeno-epipedo",
        "pacote": "epomeno-epipedo-s017",
        "publicado_em": "2026-10-12T08:26:02Z",
    }],
}


def test_a_forma_REAL_do_registro_produz_o_id():
    """A ancora: e exatamente o caso em que a versao inline falhou."""
    saida = R.anotacoes(REAL)
    assert len(saida) == 1, saida
    linha = saida[0]
    assert linha.startswith("::notice::PUBLICADO")
    assert "youtube_id=rusVeiFco9Q" in linha
    assert "Δες ποια μείωση λείπει" in linha
    assert "youtube_id=?" not in linha


def test_o_que_a_versao_inline_fazia_NAO_passa_mais():
    """Iterar o topo dava zero linha util; hoje isso e aviso, nao `?`."""
    # o topo de REAL tem chaves que nao sao dict; a versao antiga as varria
    topo = [v for v in REAL.values() if not isinstance(v, dict)]
    assert topo, "a ancora mudou de forma"
    assert all("youtube_id=?" not in s for s in R.anotacoes(REAL))


def test_linha_sem_id_vira_AVISO_e_nao_notice_com_interrogacao():
    d = {"pacote": "x-001", "linhas": [{"titulo": "t", "formato": "shorts"}]}
    saida = R.anotacoes(d)
    assert len(saida) == 1 and saida[0].startswith("::warning::")
    assert "SEM youtube_id" in saida[0]
    assert "x-001" in saida[0], "o aviso tem de dizer QUAL pacote"


def test_forma_desconhecida_grita_em_vez_de_calar():
    for d in ({}, {"canal": "c"}, {"linhas": []}, 42, "texto"):
        saida = R.anotacoes(d) if not isinstance(d, (int, str)) else R.anotacoes({})
        assert saida and saida[0].startswith("::warning::"), d
        assert "a FORMA do arquivo mudou" in saida[0]


def test_aceita_lista_solta_e_linha_solta():
    """Formas que o arquivo ja teve; tolerante na leitura, nunca silenciosa."""
    uma = dict(REAL["linhas"][0])
    assert "youtube_id=rusVeiFco9Q" in R.anotacoes([uma])[0]
    assert "youtube_id=rusVeiFco9Q" in R.anotacoes(uma)[0]


def test_o_pacote_do_envelope_serve_de_reserva():
    sem = {"pacote": "epomeno-epipedo-s017",
           "linhas": [{"youtube_id": "abc12345678", "formato": "shorts"}]}
    assert "epomeno-epipedo-s017" in R.anotacoes(sem)[0]


def test_nao_imprime_nada_que_pareca_segredo():
    """O registro nao tem segredo, e o modulo nao pode inventar um campo."""
    fonte = (RAIZ / "fabrica/registro_anota.py").read_text()
    for proibido in ("token", "secret", "refresh", "client_s", "Bearer"):
        assert proibido not in fonte.lower().replace("segredo", ""), proibido


def test_o_retomar_yml_CHAMA_o_modulo_e_nao_tem_mais_heredoc_inline():
    yml = (RAIZ / ".github/workflows/retomar.yml").read_text()
    assert "fabrica/registro_anota.py" in yml
    assert "PYFIM" not in yml, (
        "voltou a haver logica inline no YAML — e ali que ela nao tem teste")


def test_json_ilegivel_nao_derruba_o_passo(tmp_path, capsys):
    ruim = tmp_path / "r.json"
    ruim.write_text("{nao e json")
    sys.argv = ["x", str(ruim)]
    assert R.main() == 0, "ler registro corrompido nao pode falhar o job DEPOIS de publicar"
    assert "::warning::" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# `capitulos_do_longo`: a legenda tem de ser lida TAMBEM quando nao ha capitulo
# ---------------------------------------------------------------------------
def test_a_legenda_e_lida_mesmo_sem_capitulo_na_descricao():
    """Defeito meu, 12/10, uma rodada depois de eu escrever o modulo.

    O ramo "nenhum capitulo marcado" tinha um `return 0`, e a leitura da
    legenda vinha DEPOIS dele — entao o `--legenda` era ignorado exatamente no
    caso em que a legenda e a UNICA fonte de texto. Medido no `GwNkPfM9pSY`:
    descricao com 600 chars de resumo, zero capitulo, pedido de legenda
    silenciosamente nao atendido. O instrumento falhava no caso que ele existe
    para resolver.
    """
    fonte = (RAIZ / "fabrica/capitulos_do_longo.py").read_text()
    i_sem_cap = fonte.index("NENHUM capitulo marcado")
    i_legenda = fonte.index('os.environ.get("LEGENDA"')
    assert i_sem_cap < i_legenda, "a ordem mudou; refaca este teste"
    # entre o aviso de "sem capitulo" e o bloco da legenda NAO pode haver return
    trecho = fonte[i_sem_cap:i_legenda]
    assert "return 0" not in trecho, (
        "voltou a existir um `return` antes da leitura da legenda — o "
        "--legenda sera ignorado em longo sem capitulo")
    assert "roda nos DOIS casos" in fonte
