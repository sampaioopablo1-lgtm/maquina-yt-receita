# -*- coding: utf-8 -*-
"""O `query_de_retencao` existia desde 16/10 e nenhum caminho o chamava.

E a classe dos layouts mortos: codigo escrito que ninguem chama PARECE pronto e
nao esta no ar. A razao escrita para nao o chamar estava no proprio modulo —
*"Escopo: `yt-analytics.readonly` ... Falta so o clique de consentimento"* — e
ela foi **FALSIFICADA por medicao em 21/10**: o escopo esta CONCEDIDO no segredo
`YT_TOKEN_JSON`, nos TRES canais (run 39556791145, pelo `sonda_oauth` lendo os
dois blobs). O que faltava nao era o clique, era a chamada.

E a retencao nao e um instrumento qualquer: pelo 693, views/peca e cego para
efeito menor que o DOBRO, e o `relativeRetentionPerformance` ja vem normalizado
contra videos de duracao semelhante — e esse comparador que dispensa construir
linha de base com 109 pecas por braco.

O que este arquivo NAO permite: que "sem linhas" seja lido como "retencao zero".
"""
import ast
import importlib.util
import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def _mod(nome):
    spec = importlib.util.spec_from_file_location(
        nome, RAIZ / "fabrica" / ("%s.py" % nome))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R = _mod("retencao")
CR = _mod("chama_retencao")
COLS = [{"name": "elapsedVideoTimeRatio"}, {"name": "audienceWatchRatio"},
        {"name": "relativeRetentionPerformance"}]


def test_a_forma_da_query_e_DELEGADA_e_nao_remontada():
    """Por AST: remontar a query criaria o SEGUNDO dono de uma forma lida na
    fonte primaria, e o docstring deste modulo CITA os nomes das metricas em
    prosa — casar texto pegaria a explicacao.
    """
    arvore = ast.parse((RAIZ / "fabrica" / "chama_retencao.py").read_text(
        encoding="utf-8"))
    fn = next(n for n in ast.walk(arvore)
              if isinstance(n, ast.FunctionDef) and n.name == "url_do_relatorio")
    corpo = ast.unparse(fn)
    assert "query_de_retencao" in corpo, (
        "a URL deixou de sair do DONO da forma")
    for cravado in ("audienceWatchRatio", "relativeRetentionPerformance",
                    "elapsedVideoTimeRatio", "channel==MINE"):
        assert cravado not in corpo, (
            "a query foi REMONTADA aqui (%r cravado) — segundo dono da forma"
            % cravado)


def test_a_URL_carrega_os_campos_que_a_fonte_primaria_exige():
    url = CR.url_do_relatorio("abc123", "2026-07-23", "2026-10-21")
    assert url.startswith("https://youtubeanalytics.googleapis.com/v2/reports?")
    for pedaco in ("ids=channel%3D%3DMINE", "audienceWatchRatio",
                   "relativeRetentionPerformance",
                   "dimensions=elapsedVideoTimeRatio",
                   "filters=video%3D%3Dabc123",
                   "startDate=2026-07-23", "endDate=2026-10-21"):
        assert pedaco in url, (pedaco, url)


def test_UM_video_por_chamada_continua_sendo_exigencia():
    """O dono da forma LEVANTA com mais de um video; o chamador nao afrouxa."""
    import pytest
    with pytest.raises(ValueError):
        CR.url_do_relatorio("a,b", "2026-07-23", "2026-10-21")


def test_as_linhas_sao_lidas_pelo_NOME_da_coluna():
    """Posicao e o que matou tres runs (718/729/738).

    A contraprova e trocar a ORDEM das colunas: o resumo tem de sair igual.
    """
    direto = CR.resumo({"columnHeaders": COLS,
                        "rows": [[0.0, 1.0, 0.5], [0.5, 0.6, 0.7]]})
    trocado = CR.resumo({
        "columnHeaders": [COLS[0], COLS[2], COLS[1]],
        "rows": [[0.0, 0.5, 1.0], [0.5, 0.7, 0.6]]})
    assert direto["retencao_media"] == trocado["retencao_media"] == 0.8
    assert (direto["desempenho_relativo_medio"]
            == trocado["desempenho_relativo_medio"] == 0.6)


def test_SEM_LINHAS_nao_e_retencao_zero():
    """A familia de 17/10, e e a leitura que mais custaria caro aqui.

    Ler "zero linhas" como "retencao zero" mandaria a rodada seguinte concluir
    que a peca nao retem ninguem.
    """
    r = CR.resumo({"columnHeaders": [], "rows": []})
    assert r["vazio"] is True and r["linhas"] == 0
    assert r["retencao_media"] is None, (
        "vazio virou numero — zero aqui seria retencao fabricada")
    texto = CR.relato({"resumo": r})
    assert "NAO e retencao zero" in texto and "ausencia de LEITURA" in texto


def test_o_ERRO_de_leitura_tambem_vai_DITO_como_leitura_e_nao_como_dado():
    texto = CR.relato({"erro": "HTTP 403 — insufficient permissions"})
    assert "403" in texto and "NAO" in texto and "LEITURA" in texto


def test_o_resumo_com_linhas_diz_os_TRES_numeros():
    r = CR.resumo({"columnHeaders": COLS, "rows": [[0.0, 1.0, 0.5]]})
    texto = CR.relato({"resumo": r})
    assert "RETENCAO MEDIDA" in texto
    for n in ("1 pontos", "1.0", "0.5"):
        assert str(n) in texto, texto
    assert "693" in texto, (
        "o relato deixou de dizer POR QUE o desempenho relativo importa — sem "
        "isso ele volta a ser um numero solto")


def test_a_janela_nunca_pede_FIM_no_futuro():
    i, f = CR.janela(90, datetime.date(2026, 10, 21))
    assert f == "2026-10-21" and i == "2026-07-23"
    assert i < f


def test_o_video_sai_do_PARQUE_e_nao_da_minha_memoria():
    """Contar/escolher de cabeca foi o erro de 19/10 as 05:4x."""
    arvore = ast.parse((RAIZ / "fabrica" / "chama_retencao.py").read_text(
        encoding="utf-8"))
    fn = next(n for n in ast.walk(arvore)
              if isinstance(n, ast.FunctionDef) and n.name == "_video_do_parque")
    corpo = ast.unparse(fn)
    assert "duracao_a_medir" in corpo and "carrega" in corpo
    assert "open(" not in corpo, (
        "o chamador abriu o parque por conta propria — segundo leitor dele")


def test_NUNCA_imprime_credencial():
    """Trava da rotina, por AST sobre INTERPOLACAO.

    Mencao literal em mensagem passa (o modulo NOMEIA os campos para dizer o
    que nao sai dele); valor formatado, nao.
    """
    arvore = ast.parse((RAIZ / "fabrica" / "chama_retencao.py").read_text(
        encoding="utf-8"))
    vistos = 0
    for no in ast.walk(arvore):
        if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                and no.func.id in ("nota", "aviso", "print")):
            continue
        vistos += 1
        for sub in ast.walk(no):
            if isinstance(sub, ast.FormattedValue):
                fonte = ast.unparse(sub.value)
                for chave in ("refresh_token", "client_secret", "access_token",
                              "acc"):
                    assert chave not in fonte, (
                        "o chamador INTERPOLA %s numa mensagem: %s"
                        % (chave, fonte[:120]))
    assert vistos >= 5, (
        "menos de 5 chamadas de relato (%d) — a varredura por AST quebrou e "
        "este teste passaria por vacuidade" % vistos)


def test_a_RETRATACAO_do_motivo_continua_escrita():
    """O modulo antigo dizia "falta so o clique". Medido: falta a CHAMADA.

    Sem a retratacao escrita, a rodada seguinte le o `retencao.py` e volta a
    reportar ao dono que a rota depende de um clique dele.
    """
    cr = (RAIZ / "fabrica" / "chama_retencao.py").read_text(encoding="utf-8")
    assert "FALSIFICADO" in cr and "39556791145" in cr, (
        "saiu a medicao que derrubou o 'falta o clique'")
    ret = (RAIZ / "fabrica" / "retencao.py").read_text(encoding="utf-8")
    assert "chama_retencao" in ret, (
        "o `retencao.py` nao aponta para quem CHAMA a query dele — e foi "
        "justamente por nao haver chamador que ela ficou tres rodadas no ar "
        "como promessa")


def test_o_workflow_PASSA_o_blob_que_TEM_o_escopo():
    """Defeito de CHAMADOR: o modulo pode ler e o yml nao entregar."""
    yml = (RAIZ / ".github" / "workflows" / "sonda-retencao.yml").read_text(
        encoding="utf-8")
    assert "secrets.YT_TOKEN_JSON" in yml, (
        "o workflow nao passa o segredo que tem o yt-analytics.readonly")
    assert "chama_retencao.py" in yml
    assert "workflow_dispatch" in yml
