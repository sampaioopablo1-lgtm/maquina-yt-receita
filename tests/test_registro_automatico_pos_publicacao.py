"""O registro depois de publicar e do RUNNER, nao meu — 18/10/2026.

Tres passos manuais pos-publicacao foram esquecidos de forma medida (corpus
sete rodadas, `videos` doze publicacoes, dezessete duracoes na cabeca). O dono
pediu 100% automatico. O `retomar.yml` passa a chamar os tres instrumentos e a
comitar; `pos_publicacao.py` parqueia a duracao com o provedor MEDIDO pela
contagem de avisos do run do render (`avisos_do_run.py`).
"""
import json
import pathlib
import sys

sys.path.insert(0, "fabrica")
import avisos_do_run as AR  # noqa: E402
import duracao_a_medir as DM  # noqa: E402
import pos_publicacao as PP  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SPEC = json.loads((RAIZ / "fabrica/specs/labtreinamento-s079.json").read_text())
REG = {"pacote": "labtreinamento-s079", "linhas": [
    {"slug": "labtreinamento-s079-short", "formato": "shorts",
     "youtube_id": "skQt0Js1t-k", "publicado_em": "2026-10-18T19:00:00Z"}]}


def test_a_previsao_e_a_do_portao_nos_dois_mundos():
    """O ponto parqueado pelo runner tem de ser o MESMO que eu parqueava a mao:
    o s079 real esta na serie com prev_edge 25,8."""
    pe, pp = PP.previsoes(SPEC)
    assert pe == 25.8, pe
    assert 0 < pp < pe, (pe, pp)


def test_zero_avisos_parqueia_como_edge_e_N_avisos_como_piper():
    regs, _ = PP.registros(REG, SPEC, 0, "117")
    assert len(regs) == 1 and regs[0]["provedor"] == "edge"
    regs, _ = PP.registros(REG, SPEC, len(SPEC["short"]), "117")
    assert regs[0]["provedor"] == "piper" and regs[0]["job"] == "117"
    assert regs[0]["youtube_id"] == "skQt0Js1t-k" and regs[0]["pacote"] == "labtreinamento-s079"


def test_run_MISTO_nao_parqueia_e_diz_por_que():
    regs, motivo = PP.registros(REG, SPEC, 2, "117")
    assert regs == [] and "MISTO" in motivo


def test_sem_contagem_nao_parqueia__provedor_se_mede_e_nao_se_infere():
    regs, motivo = PP.registros(REG, SPEC, None, None)
    assert regs == [] and "733" in motivo
    regs, motivo = PP.registros(REG, SPEC, 0, None)
    assert regs == []


def test_so_a_linha_de_SHORT_entra_na_serie():
    reg = {"pacote": "x", "linhas": [
        {"slug": "x", "formato": "longo", "youtube_id": "L1", "publicado_em": "t"},
        {"slug": "x-short", "formato": "shorts", "youtube_id": "S1", "publicado_em": "t"}]}
    regs, _ = PP.registros(reg, SPEC, 0, "1")
    assert [r["youtube_id"] for r in regs] == ["S1"]


def test_o_registro_que_sai_e_aceito_pelo_parque_e_e_idempotente(tmp_path):
    caminho = str(tmp_path / "d.jsonl")
    regs, _ = PP.registros(REG, SPEC, 0, "117")
    assert DM.parqueia(regs[0], caminho) is True
    assert DM.parqueia(regs[0], caminho) is False
    assert len(DM.carrega(caminho)) == 1


def _get_falso(jobs, anots):
    def get(url):
        if "/actions/runs/" in url:
            return {"jobs": jobs}
        jid = int(url.split("/check-runs/")[1].split("/")[0])
        return anots.get(jid, [])
    return get


def test_conta_os_avisos_do_job_do_pacote_pelo_NOME():
    jobs = [{"id": 1, "name": "preparar"},
            {"id": 2, "name": "produzir (labtreinamento, labtreinamento-s079, pt-BR)"},
            {"id": 3, "name": "produzir (kolejny-poziom, kolejny-poziom-s063, pl)"}]
    anots = {2: [{"message": AR.MARCA + " na voz x"}] * 2 + [{"message": "SOM ..."}],
             3: [{"message": AR.MARCA}] * 10}
    r = AR.contar("o/r", "39", "labtreinamento-s079", _get_falso(jobs, anots))
    assert r == {"avisos_piper": 2, "job": "2", "jobs": 3, "motivo": ""}


def test_matriz_de_um_so_cai_no_unico_job_com_anotacao():
    jobs = [{"id": 1, "name": "preparar"}, {"id": 2, "name": "produzir (x)"}]
    anots = {2: [{"message": "SOM: LUFS -14"}]}
    r = AR.contar("o/r", "39", "nome-que-nao-casa", _get_falso(jobs, anots))
    assert r["avisos_piper"] == 0 and r["job"] == "2"


def test_ambiguo_devolve_None_em_vez_de_adivinhar():
    jobs = [{"id": 2, "name": "produzir (a)"}, {"id": 3, "name": "produzir (b)"}]
    anots = {2: [{"message": "x"}], 3: [{"message": "y"}]}
    r = AR.contar("o/r", "39", "zzz", _get_falso(jobs, anots))
    assert r["avisos_piper"] is None and r["job"] is None and r["motivo"]


def test_o_retomar_chama_os_tres_instrumentos_e_comita():
    """Sem o commit, o registro morre com o runner — e o passo volta a ser meu."""
    y = (RAIZ / ".github/workflows/retomar.yml").read_text()
    for peca in ("corpus_atrasado.py --aplicar", "registro_videos.py",
                 "pos_publicacao.py", "avisos_do_run.py", "git commit", "git push"):
        assert peca in y, peca
    assert "contents: write" in y and "checks: read" in y
    # a falha do registro nao pode desfazer a publicacao: e aviso, nao erro
    i = y.index("Registrar o publicado")
    trecho = y[i:y.index("Guardar o registro")]
    assert "::warning::" in trecho and "set -e" not in trecho.replace("set -uo", "")
