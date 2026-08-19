"""B-roll e enfeite, e enfeite nao pode derrubar render nem mudar cena antiga.

Experimento nº 10 (18/08/2026): cenas com layout "broll" poem footage do
Pexels atras de um lower-third. Os riscos que estes testes cercam:

  * REGRESSAO SILENCIOSA: o layout novo mexeu em svg_cena, elementos e
    clipe_cena — se um `if` vazar, toda cena antiga muda de desenho sem
    nenhum portao acusar. Por isso os testes de "nao mudou nada" vem antes
    dos testes do proprio broll.
  * FUNDO OPACO NO OVERLAY: se a cena broll pintar o rect de fundo, o
    footage fica 100% coberto e o video parece normal — defeito invisivel,
    como o da thumbnail verde-sobre-verde.
  * ESCOLHA DE ARQUIVO: retrato esticado e clipe mais curto que a fala sao
    os dois jeitos de o broll piorar o video em vez de melhorar.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import broll  # noqa: E402
import fabrica as F  # noqa: E402

PAL = {"ink": "#111111", "c1": "#AA2222", "c2": "#2266AA", "bg": "#FFF8EE"}


# --------------------------------------------- nada mudou para cena antiga

def test_cena_antiga_continua_pintando_fundo():
    s = F.svg_cena({"layout": "titulo", "kicker": "OI", "nar": "x"}, PAL, 1280, 720)
    assert f'fill="{PAL["bg"]}"' in s


def test_elementos_das_cenas_antigas_nao_mudou():
    assert F.elementos({"layout": "lista", "itens": ["a", "b", "c"]}) == 3
    assert F.elementos({"layout": "titulo", "kicker": "k", "sub": "s"}) == 2


# ------------------------------------------------------------ a cena broll

def test_broll_nao_pinta_fundo_e_tem_faixa():
    s = F.svg_cena({"layout": "broll", "kicker": "A conta", "sub": "x",
                    "broll_q": "money", "nar": "x"}, PAL, 1280, 720)
    assert f'fill="{PAL["bg"]}"' not in s, "fundo opaco cobriria o footage"
    assert 'opacity="0.45"' in s, "sem a faixa escura o texto nao le sobre footage claro"


def test_broll_e_uma_peca_so():
    assert F.elementos({"layout": "broll", "kicker": "k", "sub": "s"}) == 0


# ------------------------------------------------------- escolha de arquivo

def _video(vid, w, h, dur, files):
    return {"id": vid, "width": w, "height": h, "duration": dur,
            "url": "u", "user": {"name": "autor"},
            "video_files": [{"width": fw, "file_type": "video/mp4",
                             "link": f"l{fw}"} for fw in files]}


def test_escolher_recusa_retrato_e_clipe_curto():
    dados = {"videos": [
        _video(1, 720, 1280, 30, [1280]),      # retrato
        _video(2, 1920, 1080, 3, [1280]),      # curto para dd=8
        _video(3, 1920, 1080, 30, [3840, 1280, 1920]),
    ]}
    achado = broll.escolher(dados, 8)
    assert achado is not None
    link, credito = achado
    assert credito["pexels_id"] == 3
    assert link == "l1280", "o MENOR arquivo >=1280 poupa download sem perder o crop 720p"


def test_escolher_devolve_none_sem_candidato():
    assert broll.escolher({"videos": [_video(1, 720, 1280, 30, [1280])]}, 8) is None


# ----------------------------------------------------- falha nunca derruba

def test_garantir_sem_chave_e_fallback_silencioso(tmp_path):
    ok = broll.garantir(str(tmp_path), "l", 0,
                        {"layout": "broll", "broll_q": "money"},
                        8.0, 2560, 1440, api_key=None)
    assert ok is False


def test_garantir_sem_query_e_fallback_silencioso(tmp_path):
    ok = broll.garantir(str(tmp_path), "l", 0, {"layout": "broll"},
                        8.0, 2560, 1440, api_key="chave-qualquer")
    assert ok is False


# --------------------------------------------------- o motivo, sempre escrito

def test_sem_chave_diz_que_faltou_chave(tmp_path, monkeypatch):
    """O agla-level-004 gastou 20 min de render para produzir a duvida "por
    que nao teve footage?". Agora a resposta vem escrita."""
    monkeypatch.delenv("PEXELS_API_KEY", raising=False)
    monkeypatch.delenv("SB", raising=False)
    monkeypatch.delenv("KEY", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    ok = broll.garantir(str(tmp_path), "l", 0,
                        {"layout": "broll", "broll_q": "money"}, 8.0, 2560, 1440)
    assert ok is False
    assert "sem chave" in broll.ULTIMO_MOTIVO
    assert "AUSENTE" in broll.ORIGEM_DA_CHAVE


def test_sem_query_diz_que_faltou_query(tmp_path):
    ok = broll.garantir(str(tmp_path), "l", 0, {"layout": "broll"},
                        8.0, 2560, 1440, api_key="chave-qualquer")
    assert ok is False
    assert "broll_q" in broll.ULTIMO_MOTIVO


def test_a_etapa_15_loga_origem_e_motivo():
    """Se o log voltar a ser mudo, este teste cai — nao o proximo render."""
    fonte = (RAIZ / "fabrica" / "etapas.py").read_text(encoding="utf-8")
    assert "ORIGEM_DA_CHAVE" in fonte, "etapa 1.5 nao loga de onde veio a chave"
    assert "ULTIMO_MOTIVO" in fonte, "etapa 1.5 nao loga por que a cena desistiu"
