# -*- coding: utf-8 -*-
"""O `publicar.py` prometia perguntar a API de quem e o token. Nunca perguntou.

Medido em 21/10/2026 (run 39560816227). O comentario da linha 150 do
`publicar.py` dizia, em letra: *"se nao nomeia, siga — o `publicar.py` ainda
pergunta a API de quem e o token antes de subir"*. **Nao havia nenhuma chamada a
`channels?mine=true` naquele arquivo.** O unico confronto era com o campo
`canal`/`slug` DECLARADO dentro do segredo.

E o `YT_TOKEN_JSON` desta conta nao declara canal — e pertence a
`UCf4-ZFoZQWKJotZNdi4Yl7w`, o **Setiap Level**, um dos dez PARADOS. Logo, com
`publicar=true` no `frota.yml`, uma peca da frota subiria em OUTRO canal, em
silencio; o proprio `publicar.py` registra que isso "ja aconteceu uma vez
(14/08)".

Nas rodadas nao ocorreu porque elas publicam pelo `retomar.yml`, que le o
`YT_OAUTH_JSON` (mapa POR CANAL). E no meu disparo das 06:1x o que separou um
short da frota de uma subida no canal errado foram DUAS falhas sem relacao — o
escopo da legenda e o 402 do nome. **Sorte, nao metodo.**

Quem confere agora e o `confere_token.canal_do_access_token`, ANTES do render.
"""
import ast
import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ALHEIO = "UCf4-ZFoZQWKJotZNdi4Yl7w"          # Setiap Level, fora da frota


def _mod(nome):
    spec = importlib.util.spec_from_file_location(
        nome, RAIZ / "fabrica" / ("%s.py" % nome))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CT = _mod("confere_token")
FS = "https://www.googleapis.com/auth/youtube.force-ssl"
UP = "https://www.googleapis.com/auth/youtube.upload"


def _roda(monkeypatch, capsys, canal, canal_real, escopo=f"{UP} {FS}"):
    """Roda o `main()` com o refresh e o `channels?mine=true` trocados."""
    monkeypatch.setenv("SUPABASE_URL", "https://exemplo.invalid")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "chave")
    monkeypatch.setattr(sys, "argv", ["confere_token.py", canal])
    monkeypatch.setattr(CT, "token_do_canal", lambda *a: {
        "client_id": "x", "client_secret": "y", "refresh_token": "z",
        "token_uri": "https://oauth2.googleapis.com/token"})
    monkeypatch.setattr(CT.urllib.request, "urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError(
                            "nenhuma chamada real deve sair do teste")))
    monkeypatch.setattr(CT.json, "load",
                        lambda r: {"access_token": "a", "scope": escopo})
    monkeypatch.setattr(CT, "canal_do_access_token", lambda acc: canal_real)

    class _R:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False
    monkeypatch.setattr(CT.urllib.request, "urlopen", lambda *a, **k: _R())
    try:
        CT.main()
        return 0, capsys.readouterr().out
    except SystemExit as e:
        return e.code, capsys.readouterr().out


def test_canal_ERRADO_aborta_o_render(monkeypatch, capsys):
    """O caso MEDIDO: a credencial e do Setiap Level e o pacote e da frota.

    Abortar custa trinta segundos; publicar no canal errado nao se desfaz, e a
    autorizacao de 09/10 nao cobre mover nem apagar video publicado.
    """
    codigo, _ = _roda(monkeypatch, capsys, "labtreinamento", ALHEIO)
    assert codigo not in (0, None), "a credencial de outro canal foi aprovada"
    assert "CANAL ERRADO" in str(codigo)
    assert ALHEIO in str(codigo) and "UCtv_ewwSmwdi1ZRALW4_azg" in str(codigo)


def test_canal_CERTO_passa_e_diz_qual(monkeypatch, capsys):
    """Contraprova no outro sentido: sem ela bastaria abortar sempre."""
    codigo, saida = _roda(monkeypatch, capsys, "labtreinamento",
                          "UCtv_ewwSmwdi1ZRALW4_azg")
    assert codigo == 0, codigo
    assert "canal conferido na API" in saida and "UCtv_" in saida


def test_canal_NAO_LIDO_avisa_e_NAO_aborta(monkeypatch, capsys):
    """Ausencia de leitura nao e prova de que o canal esta certo.

    Abortar aqui faria uma falha de rede parar a producao, e e a familia de
    17/10 na direcao oposta: vazio nao prova nem ausencia nem presenca.
    """
    codigo, saida = _roda(monkeypatch, capsys, "labtreinamento", None)
    assert codigo == 0, codigo
    assert "ausencia de leitura" in saida.lower()
    assert "::warning" in saida


def test_canal_fora_do_mapa_nao_inventa_veredito(monkeypatch, capsys):
    """Canal desconhecido NAO aborta e NAO diz que conferiu.

    Inventar faixa/veredito para canal desconhecido e o defeito que o
    `temas_do_dono` ja proibe: padrao silencioso foi como os tres fundos
    convergiram.
    """
    codigo, saida = _roda(monkeypatch, capsys, "canal-que-nao-existe", ALHEIO)
    assert codigo == 0, codigo
    assert "canal conferido na API" not in saida


def test_o_mapa_de_canal_e_DELEGADO_e_nao_recopiado():
    """Por AST: id de canal cravado aqui seria o segundo dono do mapa."""
    fonte = (RAIZ / "fabrica" / "confere_token.py").read_text(encoding="utf-8")
    arvore = ast.parse(fonte)
    importa = any(
        (isinstance(n, ast.ImportFrom) and n.module == "medir"
         and any(a.name == "CANAIS" for a in n.names))
        for n in ast.walk(arvore))
    assert importa, "o mapa deixou de vir do `medir.CANAIS`"
    # O docstring CITA o id do canal alheio para contar o incidente; o que o
    # teste proibe e id da FROTA cravado em codigo.
    corpo = fonte.split('"""', 2)[-1]
    for no in ast.walk(ast.parse(fonte)):
        if isinstance(no, ast.Constant) and isinstance(no.value, str):
            if no.value.startswith("UCtv_") or no.value.startswith("UC1hk4"):
                raise AssertionError(
                    "id de canal da frota cravado no codigo: %r" % no.value)
    assert "medir" in corpo


def test_NUNCA_imprime_o_access_token():
    """Trava da rotina, por AST sobre INTERPOLACAO."""
    arvore = ast.parse((RAIZ / "fabrica" / "confere_token.py").read_text(
        encoding="utf-8"))
    for no in ast.walk(arvore):
        if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                and no.func.id == "print"):
            continue
        for sub in ast.walk(no):
            if isinstance(sub, ast.FormattedValue):
                f = ast.unparse(sub.value)
                for chave in ("access_token", "refresh_token", "client_secret",
                              "acc"):
                    assert chave not in f, (
                        "o portao INTERPOLA %s numa mensagem: %s" % (chave, f))


def test_o_comentario_FALSO_do_publicar_foi_RETRATADO_no_lugar():
    """Retratacao vai onde a afirmacao morava, e travada com teste."""
    pub = (RAIZ / "fabrica" / "publicar.py").read_text(encoding="utf-8")
    assert "ESTE COMENTARIO MENTIA" in pub, (
        "a retratacao saiu do `publicar.py`; sem ela a rodada seguinte le a "
        "promessa e conclui que a conferencia existe")
    assert "39560816227" in pub, "saiu a procedencia da medicao"
    assert "confere_token.canal_do_access_token" in pub, (
        "a retratacao deixou de apontar QUEM confere de verdade")


def test_o_incidente_continua_escrito_no_portao():
    ct = (RAIZ / "fabrica" / "confere_token.py").read_text(encoding="utf-8")
    for marca in (ALHEIO, "Setiap Level", "retomar.yml", "sorte, nao metodo"):
        assert marca.lower() in ct.lower(), (
            "a medida %r saiu do portao — sem ela a severidade maxima deste "
            "ramo parece exagero" % marca)
