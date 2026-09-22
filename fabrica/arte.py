"""Arte gerada por IA atras do lower-third — layout `arte` (Open Higgsfield AI).

Irma do broll.py: la a cena recebe footage do Pexels; aqui recebe uma imagem
gerada na Muapi (o motor do Open Higgsfield AI, ferramentas/open-higgsfield-ai)
a partir de `arte_prompt`. O desenho e o mesmo, de proposito:

  * so cenas com layout "arte" mudam; todo o resto da fabrica fica identico;
  * a cena declara o prompt em `arte_prompt` (ingles rende mais nos modelos);
    sem prompt, o `kicker` e o `sub` viram prompt, com o estilo do canal;
  * sem chave, sem rede ou com a API em erro, a cena cai no fallback (texto
    sobre preto, como o broll) e o render NUNCA para por causa de enfeite;
  * cada imagem usada gera credito em arte_creditos.json e o copy.md leva a
    divulgacao de conteudo sintetico, que a publicacao ja exige.

A composicao e feita AQUI, em cima do PNG transparente que `montar` ja
rasterizou (svg_cena nao pinta fundo no layout arte). O clipe_cena nao muda:
`elementos()` devolve zero para `arte`, entao o clipe segue o ramo simples de
Ken Burns sobre a imagem pronta.

A chave NAO mora no git: vem do env MUAPI_API_KEY quando o runner exporta,
senao de config.muapi_api_key no Supabase via SB/KEY.

Uso avulso (gera as artes de uma spec, sem renderizar):
    python3 fabrica/arte.py spec.json <pasta_do_pacote>
"""
from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import muapi  # noqa: E402

# Barato e rapido: ~1-2s por imagem e o menor custo por unidade do catalogo.
# Troque por `nano-banana-2` ou `seedream-5.0` (aspect_ratio, texto legivel)
# quando o canal justificar; `arte_modelo` na spec sobrepoe por pacote.
MODELO_PADRAO = os.environ.get("MUAPI_MODELO_IMAGEM", "flux-schnell")

# Vai em TODO prompt: cena de b-roll, sem letras (o TTS e a legenda ja
# carregam o texto; letras geradas saem erradas no idioma do canal).
SUFIXO = (", cinematic editorial illustration, soft depth of field, "
          "no text, no letters, no watermark, no logos")

ORIGEM_DA_CHAVE = "nao consultada"
ULTIMO_MOTIVO = ""


def _ctx():
    return ssl.create_default_context()


def chave():
    """MUAPI_API_KEY do ambiente, senao config.muapi_api_key no banco."""
    global ORIGEM_DA_CHAVE
    k = os.environ.get("MUAPI_API_KEY")
    if k:
        ORIGEM_DA_CHAVE = "env MUAPI_API_KEY"
        return k.strip()
    sb = os.environ.get("SB") or os.environ.get("SUPABASE_URL")
    sk = os.environ.get("KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not (sb and sk):
        ORIGEM_DA_CHAVE = ("AUSENTE: sem MUAPI_API_KEY e sem SB/KEY no "
                           "ambiente")
        return None
    url = f"{sb.rstrip('/')}/rest/v1/config?chave=eq.muapi_api_key&select=valor"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sk}", "apikey": sk})
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ctx()) as r:
            linhas = json.load(r)
        valor = linhas[0]["valor"] if linhas else None
        if not isinstance(valor, str) or not valor.strip():
            ORIGEM_DA_CHAVE = "AUSENTE: config.muapi_api_key nao existe no banco"
            return None
        ORIGEM_DA_CHAVE = "banco (config.muapi_api_key)"
        return valor.strip()
    except Exception as e:
        ORIGEM_DA_CHAVE = f"AUSENTE: erro ao ler config.muapi_api_key — {type(e).__name__}: {e}"
        return None


def cenas_com_arte(sp: dict) -> list[int]:
    return [i for i, c in enumerate(sp.get("longo", []))
            if c.get("layout") == "arte"]


def prompt_da_cena(c: dict, estilo: str = "") -> str:
    base = (c.get("arte_prompt") or "").strip()
    if not base:
        base = " — ".join(t for t in (c.get("kicker"), c.get("sub")) if t)
    partes = [base]
    if estilo:
        partes.append(estilo.strip())
    return ", ".join(p for p in partes if p) + SUFIXO


def compor(fundo_png: str, camada_png: str, saida: str, W: int, H: int) -> None:
    """Imagem gerada (escurecida) por baixo, cartao/texto transparente por cima."""
    from PIL import Image, ImageEnhance, ImageOps

    fundo = ImageOps.fit(Image.open(fundo_png).convert("RGB"), (W, H),
                         Image.LANCZOS)
    # brightness 0.82 e o equivalente do eq=brightness=-0.12 do broll: escurece
    # o bastante para o branco do lower-third ler sobre qualquer imagem.
    fundo = ImageEnhance.Brightness(fundo).enhance(0.82)
    fundo = ImageEnhance.Color(fundo).enhance(0.9).convert("RGBA")
    camada = Image.open(camada_png).convert("RGBA")
    if camada.size != (W, H):
        camada = camada.resize((W, H), Image.LANCZOS)
    Image.alpha_composite(fundo, camada).convert("RGB").save(saida)


def garantir(d, pref, i, c, W, H, api_key=None, estilo="", modelo=None):
    """Deixa {d}/{pref}{i:02d}.png com a arte composta. Devolve True se
    conseguiu; False (com ULTIMO_MOTIVO) se a cena fica no fallback.

    Nunca levanta: arte e enfeite, e enfeite nao derruba render.
    """
    global ULTIMO_MOTIVO
    ULTIMO_MOTIVO = ""
    alvo = f"{d}/{pref}{i:02d}.png"
    bruto = f"{d}/{pref}{i:02d}_arte.png"
    if os.path.exists(bruto) and os.path.getsize(bruto) > 10000:
        pass  # retomada: a imagem ja veio, so recompoe
    else:
        api_key = api_key or chave()
        if not api_key:
            ULTIMO_MOTIVO = f"sem chave da Muapi ({ORIGEM_DA_CHAVE})"
            return False
        if not os.path.exists(alvo):
            ULTIMO_MOTIVO = f"{alvo} nao existe — rode montar() antes"
            return False
        try:
            muapi.gerar_imagem(api_key, modelo or c.get("arte_modelo") or MODELO_PADRAO,
                               prompt_da_cena(c, estilo), bruto,
                               largura=W, altura=H)
        except Exception as e:
            ULTIMO_MOTIVO = f"{type(e).__name__}: {e}"
            try:
                os.remove(bruto)
            except OSError:
                pass
            return False
        if not (os.path.exists(bruto) and os.path.getsize(bruto) > 10000):
            ULTIMO_MOTIVO = "imagem baixada vazia ou pequena demais"
            return False
    try:
        # A camada transparente e o PNG que montar() deixou em `alvo`; guarda
        # uma copia para a retomada nao compor sobre a composicao anterior.
        camada = f"{d}/{pref}{i:02d}_camada.png"
        if not os.path.exists(camada):
            os.replace(alvo, camada)
        compor(bruto, camada, alvo, W, H)
    except Exception as e:
        ULTIMO_MOTIVO = f"composicao: {type(e).__name__}: {e}"
        return False
    cred_path = f"{d}/arte_creditos.json"
    todos = []
    if os.path.exists(cred_path):
        todos = json.load(open(cred_path, encoding="utf-8"))
    todos = [t for t in todos if t.get("cena") != i]
    todos.append({"cena": i, "modelo": modelo or c.get("arte_modelo") or MODELO_PADRAO,
                  "via": "muapi.ai (Open Higgsfield AI)"})
    json.dump(todos, open(cred_path, "w", encoding="utf-8"), ensure_ascii=False)
    return True


if __name__ == "__main__":
    import fabrica as F
    spec = sys.argv[1] if len(sys.argv) > 1 else "spec.json"
    sp = json.load(open(spec, encoding="utf-8"))
    import caminhos
    d = sys.argv[2] if len(sys.argv) > 2 else caminhos.dir_trabalho(sp)
    k = chave()
    print(f"chave da Muapi — {ORIGEM_DA_CHAVE}")
    pal = sp["paleta"]
    ok = 0
    pedem = cenas_com_arte(sp)
    for i in pedem:
        c = sp["longo"][i]
        alvo = f"{d}/l{i:02d}.png"
        if not os.path.exists(alvo):
            import cairosvg
            cairosvg.svg2png(bytestring=F.svg_cena(c, pal, 1280, 720).encode(),
                             write_to=alvo)
        if garantir(d, "l", i, c, 1280, 720, api_key=k, estilo=sp.get("arte_estilo", "")):
            ok += 1
        else:
            print(f"  cena {i} SEM ARTE: {ULTIMO_MOTIVO}")
    print(f"arte em {ok}/{len(pedem)} cenas")
    sys.exit(0 if ok == len(pedem) else 1)
