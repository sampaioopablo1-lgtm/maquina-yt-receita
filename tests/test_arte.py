"""Arte gerada e enfeite, e enfeite nao pode derrubar render nem mudar cena antiga.

Layout `arte` (fabrica/arte.py): imagem gerada na Muapi — o motor do Open
Higgsfield AI — atras do mesmo cartao flutuante do broll. Os riscos que
estes testes cercam sao os mesmos do broll, mais um:

  * REGRESSAO SILENCIOSA: `arte` mexeu em svg_cena e elementos — se um `if`
    vazar, cena antiga muda de desenho sem portao acusar;
  * FUNDO OPACO: se a cena arte pintar o rect de fundo, a imagem gerada fica
    100% coberta e o video parece normal — defeito invisivel;
  * SEM CHAVE, SEM REDE: garantir() devolve False com motivo, nunca levanta;
  * PROTOCOLO: submeter -> esperar -> baixar, com o endpoint certo para os
    ids cujo endpoint difere do id (flux-schnell -> flux-schnell-image).
"""
from __future__ import annotations

import io
import json
import sys
import types
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import arte  # noqa: E402
import fabrica as F  # noqa: E402
import muapi  # noqa: E402

PAL = {"ink": "#111111", "c1": "#AA2222", "c2": "#2266AA", "bg": "#FFF8EE"}
CENA = {"layout": "arte", "kicker": "A conta", "sub": "x",
        "arte_prompt": "bank statement on a desk", "nar": "x"}


# --------------------------------------------- nada mudou para cena antiga

def test_cena_antiga_continua_pintando_fundo():
    s = F.svg_cena({"layout": "titulo", "kicker": "OI", "nar": "x"}, PAL, 1280, 720)
    assert f'fill="{PAL["bg"]}"' in s


def test_elementos_das_cenas_antigas_nao_mudou():
    assert F.elementos({"layout": "lista", "itens": ["a", "b", "c"]}) == 3
    assert F.elementos({"layout": "broll", "kicker": "k"}) == 0


# ------------------------------------------------------------- a cena arte

def test_arte_nao_pinta_fundo_e_tem_cartao():
    s = F.svg_cena(CENA, PAL, 1280, 720)
    assert f'fill="{PAL["bg"]}"' not in s, "fundo opaco cobriria a imagem gerada"
    assert 'opacity="0.45"' in s
    assert F.elementos(CENA) == 0, "arte e uma peca so: Ken Burns sobre a composicao"


def test_estilo_lista_o_layout_arte():
    import estilo
    assert "arte" in estilo.LAYOUTS
    assert "arte_prompt" in estilo.LAYOUTS["arte"]


def test_capitulo_pode_abrir_em_arte():
    import copy_md
    sp = {"longo": [{"layout": "titulo", "kicker": "a", "cap": "A"},
                    {"layout": "arte", "kicker": "b", "cap": "B"}]}
    caps = copy_md.capitulos(sp, [copy_md.MAX_CAP + 1, 10])
    assert len(caps) == 2 and caps[1].endswith("B")


def test_prompt_da_cena_nunca_pede_texto():
    p = arte.prompt_da_cena(CENA, "paper collage")
    assert p.startswith("bank statement on a desk")
    assert "paper collage" in p and "no text" in p
    sem = arte.prompt_da_cena({"kicker": "Sem prompt", "sub": "cai no kicker"})
    assert sem.startswith("Sem prompt — cai no kicker")


# ------------------------------------------------- nunca derruba o render

def test_sem_chave_devolve_false_com_motivo(tmp_path, monkeypatch):
    for v in ("MUAPI_API_KEY", "SB", "KEY", "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        monkeypatch.delenv(v, raising=False)
    d = str(tmp_path)
    Image.new("RGBA", (64, 36)).save(f"{d}/l03.png")
    assert arte.garantir(d, "l", 3, CENA, 64, 36) is False
    assert "sem chave" in arte.ULTIMO_MOTIVO
    assert "MUAPI_API_KEY" in arte.ORIGEM_DA_CHAVE


def test_api_em_erro_devolve_false_e_nao_deixa_lixo(tmp_path, monkeypatch):
    def explode(*a, **k):
        raise muapi.ErroMuapi("HTTP 402 sem credito")
    monkeypatch.setattr(muapi, "gerar_imagem", explode)
    d = str(tmp_path)
    Image.new("RGBA", (64, 36)).save(f"{d}/l03.png")
    assert arte.garantir(d, "l", 3, CENA, 64, 36, api_key="k") is False
    assert "402" in arte.ULTIMO_MOTIVO
    assert not (tmp_path / "l03_arte.png").exists()


def test_sucesso_compoe_por_baixo_e_credita(tmp_path, monkeypatch):
    W, H = 64, 36

    def fake(chave, modelo, prompt, destino, **kw):
        assert modelo == "flux-schnell" and "no text" in prompt
        img = Image.new("RGB", (W, H), (200, 40, 40))
        img.save(destino)
        # PNG pequeno demais passaria o portao de 10 kB; engorda com ruido
        with open(destino, "ab") as f:
            f.write(b"\0" * 12000)
        return {"url": "x"}
    monkeypatch.setattr(muapi, "gerar_imagem", fake)
    d = str(tmp_path)
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    camada.putpixel((5, 5), (255, 255, 255, 255))
    camada.save(f"{d}/l07.png")

    assert arte.garantir(d, "l", 7, CENA, W, H, api_key="k") is True
    saida = Image.open(f"{d}/l07.png").convert("RGB")
    r, g, b = saida.getpixel((30, 20))
    assert r > 120 and g < 80, "a imagem gerada (vermelha, escurecida) tem de estar no fundo"
    assert saida.getpixel((5, 5)) == (255, 255, 255), "a camada de texto fica por cima"
    creds = json.load(open(f"{d}/arte_creditos.json"))
    assert creds[0]["cena"] == 7 and "muapi" in creds[0]["via"]
    # retomada: a segunda chamada nao gera de novo e nao empilha credito
    monkeypatch.setattr(muapi, "gerar_imagem", lambda *a, **k: (_ for _ in ()).throw(AssertionError("gerou de novo")))
    assert arte.garantir(d, "l", 7, CENA, W, H, api_key="k") is True
    assert len(json.load(open(f"{d}/arte_creditos.json"))) == 1


# ----------------------------------------------------- o protocolo da Muapi

def test_endpoint_dos_ids_que_diferem():
    assert muapi.endpoint_de("flux-schnell") == "flux-schnell-image"
    assert muapi.endpoint_de("nano-banana-2") == "nano-banana-2"


def test_payload_flux_em_pixels_e_outros_em_proporcao():
    p = muapi.payload_imagem("flux-schnell", "x", 1280, 720)
    assert p == {"prompt": "x", "width": 1280, "height": 704}
    q = muapi.payload_imagem("nano-banana-2", "x", 720, 1280)
    assert q == {"prompt": "x", "aspect_ratio": "9:16"}


def test_submeter_esperar_baixar(monkeypatch, tmp_path):
    chamadas = []

    class Resp(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

    def urlopen(req, timeout=0, context=None):
        url = req.full_url
        chamadas.append((req.get_method(), url, req.headers.get("X-api-key")))
        if url.endswith("/flux-schnell-image"):
            assert json.loads(req.data)["prompt"] == "p"
            return Resp(b'{"request_id": "abc"}')
        if url.endswith("/predictions/abc/result"):
            if len([c for c in chamadas if "result" in c[1]]) == 1:
                return Resp(b'{"status": "processing"}')
            return Resp(b'{"status": "completed", "outputs": ["https://cdn/x.png"]}')
        if url == "https://cdn/x.png":
            return Resp(b"PNGDATA")
        raise AssertionError(url)

    monkeypatch.setattr(muapi.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(muapi.time, "sleep", lambda s: None)
    destino = tmp_path / "x.png"
    r = muapi.gerar_imagem("chave", "flux-schnell", "p", str(destino), largura=1280, altura=720)
    assert r["url"] == "https://cdn/x.png"
    assert destino.read_bytes() == b"PNGDATA"
    assert chamadas[0][0] == "POST" and chamadas[0][2] == "chave"
    assert len([c for c in chamadas if "result" in c[1]]) == 2


def test_falha_da_api_vira_erro_muapi(monkeypatch):
    def urlopen(req, timeout=0, context=None):
        class R(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                pass
        if req.full_url.endswith("/result"):
            return R(b'{"status": "failed", "error": "nsfw"}')
        return R(b'{"request_id": "z"}')
    monkeypatch.setattr(muapi.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(muapi.time, "sleep", lambda s: None)
    try:
        muapi.gerar_imagem("k", "nano-banana", "p", "/dev/null")
    except muapi.ErroMuapi as e:
        assert "nsfw" in str(e)
    else:
        raise AssertionError("devia levantar ErroMuapi")


def test_catalogo_versionado_bate_com_o_app():
    cat = json.load(open(RAIZ / "config" / "muapi_modelos.json", encoding="utf-8"))
    ids = {m["id"]: m for m in cat["modelos"]}
    assert len(ids) >= 200
    assert ids["flux-schnell"]["endpoint"] == "flux-schnell-image"
    assert ids["nano-banana-2"]["categoria"] == "t2i"
    assert "infinitetalk-image-to-video" in ids
    # todo id cujo endpoint difere no app esta no mapa da fabrica
    for m in cat["modelos"]:
        if m["categoria"] == "t2i" and m["endpoint"] != m["id"]:
            assert muapi.ENDPOINTS.get(m["id"]) == m["endpoint"], m["id"]
