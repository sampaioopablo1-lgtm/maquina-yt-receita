"""B-roll do Pexels intercalado no render — experimento nº 10 do banco.

Motivacao (18/08/2026): o dono reportou mesmice visual entre os videos, e
video generativo classe Veo 3 nao tem rota gratis. O que existe gratis e
efetivamente ilimitado e banco de footage com API: o Pexels responde 3.401
resultados so para "counting money", com arquivos 1080p-4K, licenca livre
para uso comercial e 200 requisicoes/hora sem custo.

O desenho e deliberadamente NAO invasivo:
  * so cenas com layout "broll" usam footage; todo o resto da fabrica fica
    identico, entao nenhum pacote existente muda de comportamento;
  * a cena declara a busca em `broll_q` (ingles rende mais resultados);
  * se a chave faltar, a busca falhar ou o download vier corrompido, o clipe
    cai no caminho antigo (texto sobre fundo escuro) e o render NUNCA para
    por causa de enfeite;
  * cada clipe usado gera credito em broll_creditos.json — a licenca do
    Pexels nao exige, mas a copy credita mesmo assim.

A chave NAO mora no git: vem do env PEXELS_API_KEY quando o runner exporta,
senao de config.pexels_api_key no Supabase via SB/KEY (os mesmos secrets que
o passo de render ja tem).
"""
import json
import os
import ssl
import subprocess
import urllib.parse
import urllib.request

API = "https://api.pexels.com/videos/search"


def _ctx():
    return ssl.create_default_context()


def chave():
    k = os.environ.get("PEXELS_API_KEY")
    if k:
        return k.strip()
    sb = os.environ.get("SB") or os.environ.get("SUPABASE_URL")
    sk = os.environ.get("KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not (sb and sk):
        return None
    url = f"{sb.rstrip('/')}/rest/v1/config?chave=eq.pexels_api_key&select=valor"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sk}", "apikey": sk})
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ctx()) as r:
            linhas = json.load(r)
        return linhas[0]["valor"] if linhas else None
    except Exception:
        return None


def escolher(dados, dd):
    """O video e o arquivo dentro dele, ou None.

    Regras, na ordem em que ja doeram em teste manual:
      * paisagem (width > height) — retrato esticado sobre 16:9 fica obvio;
      * duracao >= dd + 1: cortar clipe mais curto que a fala congela o
        ultimo frame, que e exatamente a estatica que o broll veio matar;
      * arquivo com width >= 1280, o MENOR acima disso — o de 4K existe e
        custa 100 MB de download para virar 720p no crop.
    """
    for v in dados.get("videos", []):
        if v.get("width", 0) <= v.get("height", 0):
            continue
        if v.get("duration", 0) < dd + 1:
            continue
        arquivos = [f for f in v.get("video_files", [])
                    if f.get("width") and f["width"] >= 1280 and
                    (f.get("file_type") or "").endswith("mp4")]
        if not arquivos:
            continue
        arq = min(arquivos, key=lambda f: f["width"])
        credito = {"pexels_id": v["id"], "autor": v.get("user", {}).get("name", ""),
                   "url": v.get("url", "")}
        return arq["link"], credito
    return None


def _valido(caminho, dd):
    if not (os.path.exists(caminho) and os.path.getsize(caminho) > 10000):
        return False
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", caminho], capture_output=True, text=True, timeout=30)
        return abs(float(out.stdout.strip()) - dd) < 1.0
    except Exception:
        return False


def garantir(d, pref, i, c, dd, RW, RH, api_key=None):
    """Deixa {d}/{pref}{i:02d}_broll.mp4 pronto (dd segundos, RWxRH, sem
    audio, escurecido para o lower-third ler). Devolve True se conseguiu.

    Nunca levanta: broll e enfeite, e enfeite nao derruba render.
    """
    saida = f"{d}/{pref}{i:02d}_broll.mp4"
    if _valido(saida, dd):
        return True
    api_key = api_key or chave()
    q = (c.get("broll_q") or "").strip()
    if not (api_key and q):
        return False
    try:
        url = f"{API}?{urllib.parse.urlencode({'query': q, 'per_page': 8, 'orientation': 'landscape'})}"
        req = urllib.request.Request(url, headers={"Authorization": api_key})
        with urllib.request.urlopen(req, timeout=30, context=_ctx()) as r:
            achado = escolher(json.load(r), dd)
        if not achado:
            return False
        link, credito = achado
        bruto = f"{d}/{pref}{i:02d}_broll_bruto.mp4"
        req = urllib.request.Request(link, headers={"User-Agent": "curl/8"})
        with urllib.request.urlopen(req, timeout=120, context=_ctx()) as r, \
                open(bruto, "wb") as f:
            while True:
                peda = r.read(1 << 20)
                if not peda:
                    break
                f.write(peda)
        # brightness -0.12 + saturation 0.9: escurece o bastante para o texto
        # branco do lower-third ler sobre qualquer footage, sem parecer filtro.
        subprocess.run(
            ["ffmpeg", "-nostdin", "-y", "-ss", "0.3", "-t", f"{dd:.2f}",
             "-i", bruto, "-vf",
             f"scale={RW}:{RH}:force_original_aspect_ratio=increase,"
             f"crop={RW}:{RH},eq=brightness=-0.12:saturation=0.9,fps=30",
             "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
             "-pix_fmt", "yuv420p", saida],
            check=True, capture_output=True, timeout=300)
        os.remove(bruto)
        if not _valido(saida, dd):
            return False
        cred_path = f"{d}/broll_creditos.json"
        todos = []
        if os.path.exists(cred_path):
            todos = json.load(open(cred_path, encoding="utf-8"))
        todos.append({"cena": i, **credito})
        json.dump(todos, open(cred_path, "w", encoding="utf-8"), ensure_ascii=False)
        return True
    except Exception:
        for lixo in (f"{d}/{pref}{i:02d}_broll_bruto.mp4",):
            try:
                os.remove(lixo)
            except OSError:
                pass
        return False
