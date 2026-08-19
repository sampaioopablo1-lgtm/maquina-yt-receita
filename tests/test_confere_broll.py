"""Spec que pede footage sem chave no banco nao deve chegar ao render.

O agla-level-004 pagou 20 minutos de render para entregar 7 cenas de desenho
onde a spec pedia 7 de footage. A causa nao foi rede nem busca vazia: a linha
`config.pexels_api_key` nunca existiu (aprendizado 309). Estes testes cercam
as tres maneiras de o portao voltar a ser inutil:

  * conferir a spec ERRADA: um pacote sem cenas broll nao pode falhar por
    falta de uma chave que ele nem usa;
  * passar CALADO: se a saida nao disser onde a chave foi procurada nem como
    grava-la, o portao apenas troca vinte minutos de render por vinte
    minutos de investigacao;
  * sumir do workflow: o portao so vale se rodar ANTES de "Renderizar".
"""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import confere_broll as CB  # noqa: E402

SEM = {"pacote": "x-001", "longo": [{"layout": "titulo", "kicker": "k"}]}
COM = {"pacote": "x-002", "longo": [{"layout": "titulo", "kicker": "k"},
                                    {"layout": "broll", "broll_q": "money"},
                                    {"layout": "broll", "broll_q": "bills"}]}


def _spec(tmp_path, sp):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(sp), encoding="utf-8")
    return str(p)


def _sem_ambiente(monkeypatch):
    for v in ("PEXELS_API_KEY", "SB", "KEY", "SUPABASE_URL",
              "SUPABASE_SERVICE_ROLE_KEY"):
        monkeypatch.delenv(v, raising=False)


def test_conta_so_as_cenas_broll():
    assert CB.cenas_com_broll(SEM) == []
    assert CB.cenas_com_broll(COM) == [1, 2]


def test_spec_sem_broll_passa_mesmo_sem_chave(tmp_path, monkeypatch):
    _sem_ambiente(monkeypatch)
    assert CB.main(_spec(tmp_path, SEM)) == 0


def test_spec_com_broll_falha_sem_chave(tmp_path, monkeypatch):
    _sem_ambiente(monkeypatch)
    assert CB.main(_spec(tmp_path, COM)) == 1


def test_a_falha_diz_onde_procurou_e_como_gravar(tmp_path, monkeypatch, capsys):
    _sem_ambiente(monkeypatch)
    CB.main(_spec(tmp_path, COM))
    saida = capsys.readouterr().out
    assert "AUSENTE" in saida, "nao diz onde a chave foi procurada"
    assert "pexels_api_key" in saida, "nao diz que linha gravar"
    assert "insert into config" in saida, "nao da o conserto"
    assert "2 cenas" in saida or "declara 2" in saida


def test_com_chave_no_ambiente_passa(tmp_path, monkeypatch):
    _sem_ambiente(monkeypatch)
    monkeypatch.setenv("PEXELS_API_KEY", "chave-de-teste")
    assert CB.main(_spec(tmp_path, COM)) == 0


def test_o_portao_roda_antes_do_render():
    """Depois do render ele nao economiza nada — economizar e o ponto."""
    y = (RAIZ / ".github" / "workflows" / "frota.yml").read_text(encoding="utf-8")
    assert "confere_broll.py" in y, "portao nao esta no workflow"
    assert y.index("confere_broll.py") < y.index("- name: Renderizar"), \
        "o portao do broll ficou DEPOIS do render"
