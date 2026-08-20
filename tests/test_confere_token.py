"""O portao de token: vivo NAO e a mesma pergunta que PODE PUBLICAR COMPLETO.

Este arquivo existe por causa de 20/08/2026. O epomeno-epipedo-008 passou no
`confere_token`, renderizou, publicou — e a legenda do longo levou 403
"permissions not sufficient". O token estava vivo; o que faltava era escopo.

Pior: `config.yt_token_epomeno-epipedo.scopes` LISTAVA `youtube.force-ssl`.
Esse campo guarda o que foi PEDIDO no fluxo de autorizacao, nao o que foi
CONCEDIDO, e eu o usei como prova numa auditoria dos treze canais. A resposta
do refresh traz o campo `scope`, que e a lista efetiva — e e nela que o portao
manda agora.
"""
import importlib.util
import sys
import types
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]


def _modulo():
    spec = importlib.util.spec_from_file_location(
        "confere_token", RAIZ / "fabrica" / "confere_token.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CT = _modulo()
FORCE_SSL = "https://www.googleapis.com/auth/youtube.force-ssl"
UPLOAD = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE = "https://www.googleapis.com/auth/youtube"


def _roda(monkeypatch, resposta, capsys):
    """Executa o main() com o refresh do Google trocado por `resposta`."""
    monkeypatch.setenv("SUPABASE_URL", "https://exemplo.invalid")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "chave")
    monkeypatch.setattr(sys, "argv", ["confere_token.py", "canal-teste"])
    monkeypatch.setattr(CT, "token_do_canal", lambda *a: {
        "client_id": "x", "client_secret": "y", "refresh_token": "z",
        "token_uri": "https://oauth2.googleapis.com/token"})

    class _R:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            import json
            return json.dumps(resposta).encode()

    monkeypatch.setattr(CT.urllib.request, "urlopen", lambda *a, **k: _R())
    monkeypatch.setattr(CT.json, "load", lambda r: resposta)
    try:
        CT.main()
        return 0, capsys.readouterr().out
    except SystemExit as e:
        return e.code, capsys.readouterr().out


def test_token_vivo_sem_force_ssl_e_reprovado(monkeypatch, capsys):
    """O caso real do epomeno-epipedo: vive, publica, e nao leva legenda.

    Reprovar aqui custa trinta segundos. Deixar passar custa um longo publico e
    mudo para a busca — e publicacao nao se desfaz.
    """
    codigo, saida = _roda(monkeypatch, {
        "access_token": "a", "scope": f"{YOUTUBE} {UPLOAD}"}, capsys)
    assert codigo not in (0, None), (
        "token sem force-ssl foi aprovado; o longo subiria sem legenda")
    assert "ESCOPO FALTANDO" in str(codigo)
    assert "legenda" in str(codigo)


def test_token_com_os_dois_escopos_passa(monkeypatch, capsys):
    codigo, saida = _roda(monkeypatch, {
        "access_token": "a", "scope": f"{YOUTUBE} {UPLOAD} {FORCE_SSL}"}, capsys)
    assert codigo == 0, f"token completo foi reprovado: {codigo}"
    assert "escopos necessarios concedidos" in saida


def test_sem_o_campo_scope_nao_inventa_aprovacao(monkeypatch, capsys):
    """Algumas respostas de refresh omitem `scope`.

    Nesse caso o portao NAO pode dizer "esta tudo certo" nem barrar o canal por
    uma ausencia que nao e evidencia de nada. Ele deixa passar e diz, no log,
    que ficou por conferir — que e a verdade.
    """
    codigo, saida = _roda(monkeypatch, {"access_token": "a"}, capsys)
    assert codigo == 0
    assert "por conferir" in saida


def test_o_escopo_de_legenda_e_exigido_pelo_nome():
    """Se alguem tirar force-ssl da lista, este teste cai junto.

    A lista e a regra; o resto do arquivo so a aplica.
    """
    assert FORCE_SSL in CT.ESCOPOS_NECESSARIOS
    assert UPLOAD in CT.ESCOPOS_NECESSARIOS


def test_nao_escreve_em_config():
    """`config.valor` e um jsonb unico e dentro dele mora o refresh_token.

    Um PATCH nessa coluna substitui o objeto inteiro. Cheguei a escrever um
    passo que gravava os escopos concedidos de volta e o desfiz antes de rodar:
    consertar um campo descritivo nao vale o risco de apagar a credencial dos
    treze canais. Este teste existe para que ninguem o reintroduza distraido.
    """
    fonte = (RAIZ / "fabrica" / "confere_token.py").read_text(encoding="utf-8")
    # A palavra PATCH aparece de proposito na docstring, explicando por que ela
    # nao deve virar codigo. O que o teste proibe e a CHAMADA.
    corpo = fonte.split('"""', 2)[-1]      # fora a docstring do modulo
    for escrita in ("PATCH", "PUT", "DELETE"):
        assert f'method="{escrita}"' not in corpo, (
            f"confere_token voltou a escrever em config ({escrita}); `valor` e "
            f"jsonb unico e a escrita levaria o refresh_token junto")
    # POST e legitimo: e o refresh no endpoint do Google, nao no banco.
    assert corpo.count("rest/v1/config") == 1, (
        "config e tocado em mais de um lugar; este arquivo so deve LER o token")
