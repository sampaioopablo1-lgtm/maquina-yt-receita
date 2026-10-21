# -*- coding: utf-8 -*-
"""A sonda lia UM segredo de credencial e existem DOIS, com concessoes opostas.

Medido em 21/10/2026, e o achado durou uma hora. O `confere_token` abortou o
render de um short solto dizendo que faltava `youtube.force-ssl`; a sonda, na
MESMA hora, respondeu `force-ssl=sim` nos tres canais (job 119073920894). As
duas estavam CERTAS — elas leem segredos diferentes:

  * `confere_token`/`publicar.py` caem no **`YT_TOKEN_JSON`** (os
    `YT_TOKEN_<CANAL>` estao ausentes, 0 chars): `youtube` + `youtube.upload` +
    **yt-analytics.readonly**, SEM force-ssl (job 119070898648);
  * o `retomar.yml`, que PUBLICA nas rodadas, usa o **`YT_OAUTH_JSON`**:
    `upload=sim, force-ssl=sim, analytics=NAO` nos tres.

Com um blob so a unica leitura disponivel era "o dono reautorizou e perdeu o
force-ssl" — falsa. E comparar os dois era conta MINHA, cruzando dois jobs a
mao, que e o item 3 da §10.

E a metade que vale para o dono: **o `yt-analytics.readonly` existe em um dos
dois**, e este repo o reporta como perdido desde o 689. Escopo concedido NAO e
prova de que o dado vem — quem prova e uma chamada a Analytics API.
"""
import ast
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
UP = "https://www.googleapis.com/auth/youtube.upload"
FS = "https://www.googleapis.com/auth/youtube.force-ssl"
AN = "https://www.googleapis.com/auth/yt-analytics.readonly"


def _mod():
    spec = importlib.util.spec_from_file_location(
        "sonda_oauth", RAIZ / "fabrica" / "sonda_oauth.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


SO = _mod()


def _quadro(a, b):
    return {"YT_OAUTH_JSON": {c: set(a) for c in SO.FROTA},
            "YT_TOKEN_JSON": {c: set(b) for c in SO.FROTA}}


def test_o_caso_MEDIDO_sai_como_divergencia_nos_dois_escopos():
    """O par exato de 21/10: um blob com force-ssl, o outro com analytics."""
    div = SO.divergencias(_quadro([UP, FS], [UP, AN]))
    rotulos = {(c, r) for c, r, _, _ in div}
    for canal in SO.FROTA:
        assert (canal, "force-ssl") in rotulos, div
        assert (canal, "analytics") in rotulos, div
    assert not any(r == "upload" for _, r, _, _ in div), (
        "upload esta nos dois e nao pode aparecer como divergencia")


def test_quem_TEM_e_quem_NAO_tem_sai_nomeado_e_nao_invertido():
    """Inverter os lados daria a conclusao oposta sobre qual passo quebra."""
    div = SO.divergencias(_quadro([UP, FS], [UP, AN]))
    fs = next(d for d in div if d[1] == "force-ssl")
    an = next(d for d in div if d[1] == "analytics")
    assert fs[2] == ["YT_OAUTH_JSON"] and fs[3] == ["YT_TOKEN_JSON"], fs
    assert an[2] == ["YT_TOKEN_JSON"] and an[3] == ["YT_OAUTH_JSON"], an


def test_blobs_que_CONCORDAM_nao_produzem_achado():
    """Contraprova no outro sentido: sem ela a funcao acusaria sempre."""
    assert SO.divergencias(_quadro([UP, FS, AN], [UP, FS, AN])) == []


def test_um_blob_SO_nao_e_ausencia_de_divergencia():
    """Com uma leitura so a pergunta nao foi feita, e isso tem de ir DITO.

    E a familia do 17/10: instrumento que devolve vazio nao prova ausencia.
    """
    assert SO.divergencias({"YT_OAUTH_JSON": {c: {UP, FS} for c in SO.FROTA}}) == []
    fonte = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")
    assert "NAO foi medida nesta passada" in fonte, (
        "o relato deixou de distinguir 'concordam' de 'nao foi medido', e os "
        "dois saem como silencio")


def test_refresh_MORTO_nao_vira_escopo_ausente():
    """Token que nao refresca e `None`, nao conjunto vazio.

    Tratar falha de leitura como 'nao tem o escopo' inventaria divergencia —
    detector que inventa achado e pior que nao ter detector (725).
    """
    q = {"YT_OAUTH_JSON": {c: {UP, FS} for c in SO.FROTA},
         "YT_TOKEN_JSON": {c: None for c in SO.FROTA}}
    assert SO.divergencias(q) == [], (
        "blob que nao refrescou entrou na comparacao como se tivesse "
        "respondido 'nao tenho'")


def test_a_sonda_LE_os_dois_segredos():
    """O defeito era de LEITURA: ela nem via o segundo blob."""
    fonte = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")
    for nome in ("YT_OAUTH_JSON", "YT_TOKEN_JSON"):
        assert ('os.environ.get("%s")' % nome) in fonte or (
            'os.environ["%s"]' % nome) in fonte, (
            "a sonda nao le %s — e com um blob so a divergencia nao e "
            "mensuravel" % nome)
    assert "_relata_divergencia" in fonte


def test_o_workflow_PASSA_o_segundo_segredo():
    """Defeito de CHAMADOR: o modulo pode ler e o yml nao entregar."""
    yml = (RAIZ / ".github" / "workflows" / "sonda-oauth.yml").read_text(
        encoding="utf-8")
    assert "secrets.YT_TOKEN_JSON" in yml, (
        "o sonda-oauth.yml voltou a nao passar o YT_TOKEN_JSON, e ai a sonda "
        "fica cega para a credencial que o frota.yml usa")


def test_a_sonda_NUNCA_imprime_credencial():
    """Trava da rotina, e ela vale para o codigo novo tambem.

    A PRIMEIRA versao deste teste estava ERRADA e o modulo estava certo: ela
    proibia a STRING `refresh_token` dentro de um `aviso`, e acusou a mensagem
    que apenas NOMEIA o formato esperado do segredo
    (`{"client_id", "client_secret", "refresh_token"}`) — documentacao da forma,
    nao vazamento. Casar texto pegou a explicacao em vez do codigo, que e a
    licao do `test_NAO_virou_portao` do acento.

    A propriedade certa e sobre INTERPOLACAO: nenhum valor de credencial pode
    entrar num `print`/`nota`/`aviso`. Mencao literal passa; valor formatado,
    nao.
    """
    arvore = ast.parse((RAIZ / "fabrica" / "sonda_oauth.py").read_text(
        encoding="utf-8"))
    proibidos = ("refresh_token", "client_secret", "access_token")
    vistos = 0
    for no in ast.walk(arvore):
        if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                and no.func.id in ("nota", "aviso", "print")):
            continue
        vistos += 1
        for sub in ast.walk(no):
            if not isinstance(sub, ast.FormattedValue):
                continue
            fonte = ast.unparse(sub.value)
            for chave in proibidos:
                assert chave not in fonte, (
                    "a sonda INTERPOLA %s numa mensagem: %s"
                    % (chave, fonte[:120]))
    assert vistos >= 10, (
        "menos de 10 chamadas de relato encontradas (%d) — a varredura por AST "
        "quebrou e este teste passaria por vacuidade" % vistos)


def test_o_canal_declarado_pelo_blob_generico_sai_no_relato():
    """`YT_TOKEN_JSON` e UM token e serve de reserva para QUALQUER canal.

    O `publicar.py` ja carrega o incidente de 14/08 (publicou no canal errado) e
    confere o campo `canal`/`slug` quando ele existe. Qual canal o blob declara
    nao e segredo, e e o que diz se a reserva publica no lugar certo.
    """
    fonte = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")
    assert "declara {dono}" in fonte or "declara " in fonte, (
        "o relato do blob generico deixou de dizer que canal ele declara")
    assert "publicar.py:139" in fonte, (
        "saiu a procedencia de que esse blob e a RESERVA de qualquer canal")


def test_o_motivo_e_a_medida_continuam_escritos():
    fonte = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")
    for marca in ("119073920894", "119070898648", "689", "yt-analytics"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo; sem os dois jobs a divergencia "
            "vira afirmacao minha" % marca)


def test_o_escopo_do_token_UNICO_nao_se_atribui_aos_TRES_canais():
    """RETRATACAO de 21/10, e e de algo que eu relatei ao dono.

    A primeira versao punha os escopos do `YT_TOKEN_JSON` em `{canal: escopos}`
    para os TRES canais e comparava POR CANAL, e eu reportei "o analytics existe
    nos tres canais". Falso: e um token UNICO de UM canal, MEDIDO como
    `UCf4-ZFoZQWKJotZNdi4Yl7w` (Setiap Level), FORA da frota — a familia
    "atribuir o numero ao orgao errado", onde a conta fecha e a origem esta
    errada.

    A comparacao certa e entre BLOBS, e os lados saem em nome de blob, nunca de
    canal.
    """
    div = SO.divergencia_entre_blobs({c: {UP, FS} for c in SO.FROTA}, {UP, AN})
    assert div, "a comparacao entre blobs parou de medir"
    for _, tem, nao in div:
        for lado in tem + nao:
            assert lado in ("YT_OAUTH_JSON", "YT_TOKEN_JSON"), (
                "lado em nome de CANAL: %r — e a atribuicao errada de volta"
                % lado)
    fonte = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")
    assert "UCf4-ZFoZQWKJotZNdi4Yl7w" in fonte and "fora da frota" in fonte, (
        "saiu a medida de QUE canal e o token unico; sem ela a atribuicao aos "
        "tres canais volta a parecer razoavel")
    assert "RETRATACAO" in fonte


def test_o_relato_DIZ_que_o_token_unico_e_de_um_canal_so():
    """Sem essa frase o leitor do log repete a minha conclusao errada."""
    fonte = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")
    assert "NAO se atribuem aos tres canais" in fonte, (
        "o relato deixou de avisar que os escopos do token unico nao valem "
        "para a frota")


def test_token_unico_NAO_lido_e_dito_e_nao_silencio():
    assert SO.divergencia_entre_blobs({c: {UP, FS} for c in SO.FROTA}, None) == []
    fonte = (RAIZ / "fabrica" / "sonda_oauth.py").read_text(encoding="utf-8")
    assert "NAO foi medida nesta passada" in fonte
