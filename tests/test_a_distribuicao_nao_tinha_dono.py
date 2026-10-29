#!/usr/bin/env python3
"""A distribuicao para as outras redes nao tinha dono — e a skill do
Upload-Post estava no repo sem ninguem a chamar.

PEDIDO DO DONO EM 29/10/2026: o mesmo video publicado no YouTube indo
automaticamente para Instagram, TikTok e as outras redes, para levar gente ao
perfil e ao link da bio. MEDIDO antes de escrever (docs/distribuicao-multi-
rede.md): a unica rota automatica e a API do Upload-Post, cuja skill ja
estava em `.claude/skills/upload-post/` — codigo escrito que ninguem chama e a
classe dos layouts mortos, agora numa skill.

O que este arquivo cobra e PROPRIEDADE e nao identidade (743/753/761): a spec
de prova e DERIVADA do disco, os tetos sao cobrados na FRONTEIRA nos dois
lados, a recusa vai com contraprova no outro sentido, e a chave e cobrada
como AUSENTE de argv e de stdout — nunca por um valor cravado.
"""
import ast
import glob
import inspect
import json
import os
import re
import stat
import subprocess
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as ADR        # noqa: E402
import concentracao_frota as CF      # noqa: E402
import distribuicao as D             # noqa: E402
import publicar as PB                # noqa: E402

WORKFLOW = os.path.join(RAIZ, ".github", "workflows", "distribuir.yml")
SKILL = os.path.join(RAIZ, ".claude", "skills", "produzir-e-distribuir", "SKILL.md")
SENTINELA = "CHAVE-DE-PROVA-QUE-NAO-PODE-APARECER-7f3a"


# ------------------------------------------------------------ fixtures
def _spec_com_titulo_curto():
    """Uma spec de short solto DERIVADA do disco, com `## TITULO SHORT` e
    hashtags — nomear um pacote seria identidade onde ha propriedade."""
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")),
                    reverse=True):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        copy = d.get("copy") or ""
        if d.get("longo") or not d.get("short") or not isinstance(copy, str):
            continue
        if "## TITULO SHORT" in copy and "## HASHTAGS" in copy:
            return p, d
    pytest.fail("perdi a ancora: nenhuma spec de short solto com TITULO SHORT e HASHTAGS")


def _workdir_com_copy(tmp_path, spec):
    """O render escreve o copy.md com os placeholders preenchidos; aqui e a
    copy da spec com eles tirados, que e o que o dono da copy aceita."""
    md = (spec["copy"].replace("{TRILHA}", "Wholesome").replace("{CAPITULOS}", "")
          .replace("PLACEHOLDER", ""))
    (tmp_path / "copy.md").write_text(md, encoding="utf-8")
    return str(tmp_path)


def _mapa_preenchido(canal):
    m = D.perfis()
    m["canais"][canal]["perfil"] = "perfil-de-prova"
    m["canais"][canal]["link_da_bio"] = "https://exemplo.invalid/curso"
    return m


def _fonte(fn):
    return textwrap.dedent(inspect.getsource(fn))


# ------------------------------------------------------------ perfis
def test_todo_canal_da_frota_tem_entrada_e_a_varredura_nao_e_vazia():
    m = D.perfis()
    canais = m.get("canais") or {}
    assert len(canais) >= 3, "mapa de perfis curto demais para medir a frota"
    for c in CF.FROTA:
        assert c in canais, "canal da frota sem entrada em perfis_sociais.json: %r" % c
        assert canais[c].get("cta"), "canal %r sem CTA de link na bio" % c
        assert canais[c].get("plataformas"), "canal %r sem redes" % c
    assert all("youtube" not in e["plataformas"] for e in canais.values()), (
        "youtube no mapa de redes: o dono dele e o retomar.yml")


def test_canal_sem_perfil_RECUSA_com_o_motivo_e_nao_inventa_nome():
    m = D.perfis()
    alvo = next(c for c in CF.FROTA)
    m["canais"][alvo]["perfil"] = None
    with pytest.raises(ValueError) as e:
        D.perfil_do_canal(alvo, m)
    assert "perfil" in str(e.value) and "dono" in str(e.value)
    # Contraprova no outro sentido: preenchido, devolve o perfil.
    m["canais"][alvo]["perfil"] = "x"
    assert D.perfil_do_canal(alvo, m)["perfil"] == "x"
    with pytest.raises(ValueError):
        D.perfil_do_canal("canal-que-nao-existe", m)


# ------------------------------------------------------------ limites
def test_youtube_e_RECUSADO_porque_tem_dono():
    with pytest.raises(ValueError) as e:
        D.cabem(["instagram", "youtube"], 43.0)
    assert "retomar" in str(e.value)


def test_a_FRONTEIRA_dos_tetos_vai_nos_dois_lados_em_toda_rede():
    assert len(D.TETO_S) >= 6, "tabela de tetos curta demais"
    for p, teto in D.TETO_S.items():
        perfil = {v: "id-de-prova" for v in D.EXIGE_ID.values()}
        assert p in D.cabem([p], teto, perfil)["cabem"], "%s: o teto exato nao cabe" % p
        r = D.cabem([p], teto + 0.1, perfil)
        assert p in r["nao_cabem"] and "teto" in r["nao_cabem"][p], (
            "%s: um decimo acima do teto passou" % p)
    for p, piso in D.PISO_S.items():
        perfil = {v: "id-de-prova" for v in D.EXIGE_ID.values()}
        assert p in D.cabem([p], piso, perfil)["cabem"]
        assert p in D.cabem([p], piso - 0.1, perfil)["nao_cabem"]


def test_plataforma_desconhecida_e_duracao_nao_medida_LEVANTAM():
    with pytest.raises(ValueError):
        D.cabem(["orkut"], 43.0)
    for ruim in (None, 0, -1.0):
        with pytest.raises(ValueError) as e:
            D.cabem(["instagram"], ruim)
        assert "MEDIDA" in str(e.value)


def test_rede_que_exige_id_sai_NOMEADA_sem_o_id_e_entra_com_ele():
    for p, campo in D.EXIGE_ID.items():
        r = D.cabem([p], 43.0, {})
        assert p in r["nao_cabem"] and campo in r["nao_cabem"][p]
        assert p in D.cabem([p], 43.0, {campo: "id"})["cabem"]


def test_o_short_da_frota_cabe_em_toda_rede_e_o_longo_NAO_cabe_no_reels():
    """Os dois lados existem: sem o lado que NAO cabe, nomear seria vacuo."""
    perfil = {v: "id" for v in D.EXIGE_ID.values()}
    todas = sorted(D.TETO_S)
    r = D.cabem(todas, 43.0, perfil)          # short da frota: 41 a 45 s reais
    assert sorted(r["cabem"]) == todas, r["nao_cabem"]
    r = D.cabem(todas, 540.0, perfil)         # longo: 8 a 10 min
    assert "instagram" in r["nao_cabem"] and "x" in r["nao_cabem"]
    assert "tiktok" in r["cabem"] and "facebook" in r["cabem"]


# ------------------------------------------------------------ texto
def test_o_texto_vem_do_DONO_da_copy_e_nao_de_um_segundo_parser():
    """Por AST: `texto` chama `ler_copy` e o modulo nao abre `## ` por conta
    propria — reparsear a copy foi o que pos o bloco do Studio no comentario."""
    fonte = open(D.__file__, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    chamadas = {n.func.attr for n in ast.walk(arvore)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    assert "ler_copy" in chamadas
    corpo = fonte.split('"""', 2)[2]          # fora do docstring do modulo
    assert "## " not in corpo and "re.split" not in corpo, (
        "o modulo esta parseando a copy sozinho")


def test_o_titulo_e_o_CURTO_e_a_legenda_leva_CTA_e_hashtags(tmp_path):
    caminho, sp = _spec_com_titulo_curto()
    wd = _workdir_com_copy(tmp_path, sp)
    canal = D.CA.da_spec(sp)
    m = _mapa_preenchido(canal)
    pl = D.payload(sp, 43.0, wd, None, m)
    cp = PB.ler_copy(sp, wd)
    assert pl["campos"]["title"] == cp["short_titulo"], "o titulo nao e o CURTO"
    assert pl["campos"]["title"] != cp["titulo"]
    desc = pl["campos"]["description"]
    assert m["canais"][canal]["cta"] in desc, "a legenda nao leva o CTA de link na bio"
    assert cp["hashtags"] in desc
    assert len(desc) <= D.LEGENDA_MAX
    assert m["canais"][canal]["link_da_bio"] in pl["campos"]["first_comment"], (
        "o link da bio nao foi ao primeiro comentario")
    assert pl["campos"]["user"] == "perfil-de-prova"
    assert "youtube" not in pl["plataformas"]


def test_copy_com_placeholder_e_RECUSA_de_dado_e_nao_saida_do_processo(tmp_path):
    caminho, sp = _spec_com_titulo_curto()
    m = _mapa_preenchido(D.CA.da_spec(sp))
    sp2 = dict(sp)
    sp2["copy"] = sp["copy"] + "\n{CAPITULOS}\n"
    with pytest.raises(ValueError) as e:
        D.payload(sp2, 43.0, str(tmp_path), None, m)   # sem copy.md -> le a spec
    assert "copy" in str(e.value)


# ------------------------------------------------------------ chave
def test_a_chave_nunca_vai_em_argv_e_o_arquivo_dela_e_0600(tmp_path):
    caminho, sp = _spec_com_titulo_curto()
    wd = _workdir_com_copy(tmp_path, sp)
    m = _mapa_preenchido(D.CA.da_spec(sp))
    pl = D.payload(sp, 43.0, wd, None, m)
    cfg = D._config_da_chave(SENTINELA, str(tmp_path))
    args = D.curl_args(pl, "/x/short.mp4", cfg)
    assert SENTINELA not in " ".join(args), "a chave foi para argv"
    assert "-K" in args and cfg in args
    assert stat.S_IMODE(os.stat(cfg).st_mode) == 0o600
    assert SENTINELA in open(cfg, encoding="utf-8").read()
    assert "platform[]=instagram" in args or "platform[]=tiktok" in args


def test_a_chave_do_ambiente_nao_aparece_no_relato(tmp_path, monkeypatch):
    caminho, sp = _spec_com_titulo_curto()
    wd = _workdir_com_copy(tmp_path, sp)
    m = _mapa_preenchido(D.CA.da_spec(sp))
    monkeypatch.setenv(D.VAR_DA_CHAVE, SENTINELA)
    saida = D.relato(sp, video=os.path.join(wd, "short.mp4"), duracao_s=43.0, mapa=m)
    assert SENTINELA not in saida
    assert "vai para" in saida and "bio" in saida


def test_publica_RECUSA_sem_chave_e_nao_toca_a_rede(tmp_path, monkeypatch):
    caminho, sp = _spec_com_titulo_curto()
    wd = _workdir_com_copy(tmp_path, sp)
    m = _mapa_preenchido(D.CA.da_spec(sp))
    pl = D.payload(sp, 43.0, wd, None, m)
    monkeypatch.delenv(D.VAR_DA_CHAVE, raising=False)

    def _nunca(*a, **k):
        raise AssertionError("curl foi chamado sem chave")
    monkeypatch.setattr(D.subprocess, "run", _nunca)
    with pytest.raises(ValueError) as e:
        D.publica(pl, os.path.join(wd, "copy.md"))
    assert D.VAR_DA_CHAVE in str(e.value)


def test_o_relato_nao_pode_ser_consultado_sem_o_video_e_esta_FORA_da_passada():
    caminho, _ = _spec_com_titulo_curto()
    with pytest.raises(ValueError):
        D.relato(caminho)
    assert "distribuicao" in ADR.FORA_DA_PASSADA
    assert "distribuicao" not in ADR.INSTRUMENTOS


# ------------------------------------------------------------ parque
def test_o_parque_RECUSA_repetir_a_mesma_peca_na_mesma_rede(tmp_path):
    parque = str(tmp_path / "d.jsonl")
    pl = {"pacote": "x-s001", "canal": "x", "plataformas": ["instagram", "tiktok"],
          "recusadas": {}}
    reg = D.registro(pl, "VID1", {"success": True, "request_id": "r1"},
                     run="1", job="2", em="2026-10-29T00:00:00Z")
    assert D.parqueia(reg, parque)
    assert D.ja_distribuida("VID1", parque) == ["instagram", "tiktok"]
    with pytest.raises(ValueError) as e:
        D.parqueia(dict(reg, em="2026-10-29T01:00:00Z"), parque)
    assert "instagram" in str(e.value) and "dono" in str(e.value)
    # Contraprova no outro sentido: rede NOVA para a mesma peca entra.
    reg2 = dict(reg, plataformas=["threads"], em="2026-10-29T01:00:00Z")
    assert D.parqueia(reg2, parque)
    assert D.ja_distribuida("VID1", parque) == ["instagram", "threads", "tiktok"]
    assert len(D.carrega(parque)) == 2
    with pytest.raises(ValueError):
        D.parqueia({"pacote": "x"}, parque)


# ------------------------------------------------------------ workflow e skill
def test_o_workflow_le_o_segredo_e_nunca_o_recebe_por_input():
    yml = open(WORKFLOW, encoding="utf-8").read()
    assert "secrets.UPLOAD_POST_API_KEY" in yml
    inputs = yml.split("inputs:", 1)[1].split("permissions:", 1)[0]
    assert not re.search(r"(?i)(chave|api_key|apikey|token)\s*:", inputs), (
        "o workflow aceita segredo por input")
    assert "fabrica/distribuicao.py" in yml and "--publicar" in yml
    assert "pacote-${{ inputs.pacote }}" in yml, "o artefato nao e procurado pelo NOME"
    assert "timeout-minutes" in yml
    assert "ffprobe" in yml, "a duracao tem de ser MEDIDA no runner"
    assert "publicar=true" not in yml


def test_a_skill_aponta_para_os_donos_e_nao_copia_numero():
    md = open(SKILL, encoding="utf-8").read()
    for dono in ("distribuicao.py", "retomar.yml", "despacho_da_rodada",
                 "passo_zero", "pauta_do_momento", "prontidao", "espera_do_run",
                 "perfis_sociais.json", "docs/ROTINA.md"):
        assert dono in md, "a skill nao aponta para %r" % dono
    assert not re.search(r"\b\d{2},\d\b", md), (
        "a skill carrega numero decimal de producao — numero em skill envelhece")
    assert "Composio" in md and "publicar=true" in md


def test_todo_caminho_que_a_skill_e_o_doc_citam_EXISTE():
    cit = re.compile(r"`([A-Za-z0-9_./-]+/[A-Za-z0-9_.-]+\.(?:py|md|json|jsonl|yml))`")
    for arq in (SKILL, os.path.join(RAIZ, "docs", "distribuicao-multi-rede.md")):
        txt = open(arq, encoding="utf-8").read()
        faltam = [c for c in set(cit.findall(txt))
                  if not c.startswith(("http", "/tmp/"))
                  and not os.path.exists(os.path.join(RAIZ, c))]
        assert not faltam, "%s cita caminho que nao existe: %r" % (arq, faltam)
