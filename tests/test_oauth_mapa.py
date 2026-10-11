"""O segredo colado do SQL Editor vem EMBRULHADO, e isso ja quebrou em producao.

Run `38175092152`, 11/10/2026: `YT_OAUTH_JSON: presente (1116 chars)` e logo
abaixo `tem 1 canal(is)`, com os tres canais da frota dentro do valor. O copiar
do painel do Supabase entrega a LINHA do resultado, nao a celula, e a linha e
`[{"<coluna>": "<json em texto>"}]`.

Eu tinha "resolvido" isso mandando o dono editar o texto a mao — apagar o
comeco, o fim e as sequencias `\\n`. Instrucao de edicao manual e instrucao que
falha, e falhou. Estes testes travam o desembrulho no codigo.
"""

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

from oauth_mapa import desembrulha  # noqa: E402

FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")

LIMPO = {
    c: {"client_id": f"id-{c}", "client_secret": f"seg-{c}",
        "refresh_token": f"ref-{c}",
        "token_uri": "https://oauth2.googleapis.com/token"}
    for c in FROTA
}


def test_o_formato_limpo_passa_intacto():
    assert desembrulha(json.dumps(LIMPO)) == LIMPO


def test_a_linha_copiada_do_sql_editor_desembrulha():
    """A forma exata que chegou em producao: lista, coluna, JSON em texto."""
    linha = [{"jsonb_pretty": json.dumps(LIMPO, indent=4)}]
    assert desembrulha(json.dumps(linha)) == LIMPO


def test_a_mesma_coisa_sem_o_colchete():
    assert desembrulha(json.dumps({"jsonb_pretty": json.dumps(LIMPO)})) == LIMPO


def test_o_nome_da_coluna_nao_importa():
    """O `select` pode nomear a coluna de qualquer jeito — nao ancore no nome."""
    for coluna in ("jsonb_pretty", "jsonb_object_agg", "?column?", "text"):
        assert desembrulha(json.dumps({coluna: json.dumps(LIMPO)})) == LIMPO


def test_mapa_de_UM_canal_so_NAO_e_confundido_com_embrulho():
    """Um canal so e legitimo, e o valor dele e objeto — nao string."""
    um = {"labtreinamento": LIMPO["labtreinamento"]}
    assert desembrulha(json.dumps(um)) == um


def test_texto_que_nao_e_json_levanta():
    with pytest.raises(ValueError):
        desembrulha("isto nao e json")


def test_json_que_nao_reduz_a_objeto_levanta():
    for ruim in ("[1, 2, 3]", '"so uma string"', "42"):
        with pytest.raises(ValueError):
            desembrulha(ruim)


def test_a_sonda_usa_o_desembrulho_e_nao_json_loads_cru():
    """Ligar no modulo e esquecer de ligar na sonda reconstroi o defeito."""
    import inspect

    import sonda_oauth

    fonte = inspect.getsource(sonda_oauth.main)
    assert "desembrulha(" in fonte
    assert 'json.loads(os.environ["YT_OAUTH_JSON"])' not in fonte


def test_o_retomar_tambem_desembrulha():
    """`retomar.yml` roda ANTES do checkout, entao leva a copia inline.

    Se ela sair, a publicacao sem banco volta a morrer com o mesmo segredo que
    a sonda aprova — e o sintoma seria `KeyError` no nome do canal.
    """
    yml = Path(__file__).resolve().parents[1] / ".github/workflows/retomar.yml"
    texto = yml.read_text()
    assert "mapa = json.load(sys.stdin)" in texto
    assert "cfg = mapa['$CANAL']" in texto


def test_o_retomar_NAO_escapa_o_cifrao_do_ACC():
    """`\\$ACC` e literal em shell, e isso deixou o token VAZIO em producao.

    Run 38175625236, 11/10/2026: a sonda aprovava os tres canais, o refresh
    rodava, e mesmo assim o publicar.py falhava — porque o output do passo saia
    com o TEXTO "$ACC". O sintoma foi "Can't add secret mask for empty string".
    O defeito sobreviveu desde que a rota nasceu porque o segredo estava vazio:
    nunca se chegou a exercitar esta linha.
    """
    from pathlib import Path

    yml = (Path(__file__).resolve().parents[1]
           / ".github/workflows/retomar.yml").read_text()
    corpo = "\n".join(l for l in yml.splitlines() if not l.strip().startswith("#"))
    assert 'echo "acc=$ACC" >> "$GITHUB_OUTPUT"' in corpo
    assert "\\$ACC" not in corpo
    assert "\\$GITHUB_OUTPUT" not in corpo
