"""As 10 imagens dos anuncios, baixadas do Pexels.

Irmao do broll.py, com as mesmas cicatrizes: chave via broll.chave(), User-
Agent de navegador (o Pexels devolve 403 para o urllib padrao) e tentativa
tripla com timeout crescente (o runner do GitHub Actions estoura a primeira).
Muda o endpoint — /v1/search devolve foto, /videos/search devolve clipe — e o
criterio de escolha.

Roda no runner, nao na sessao do agente: a politica de egresso da sessao nega
CONNECT para pexels.com, entao o download so acontece aqui.

Busca em ingles de proposito: "business meeting" traz 10x mais que "reuniao
de negocios" no acervo do Pexels.
"""
import json
import os
import ssl
import urllib.parse
import urllib.request

from broll import chave

API = "https://api.pexels.com/v1/search"
DESTINO = "entregas/campanha/imagens"

# A ordem e a do SOURCING — 10 imagens Pexels.md. `alt` entra quando a busca
# principal volta vazia ou so com foto retrato.
PECAS = [
    ("01-crescimento", "hand holding smartphone message", "person texting phone"),
    ("02-analytics", "laptop analytics dashboard chart", "business data screen"),
    ("03-consultoria", "two people laptop meeting office", "business consulting meeting"),
    ("04-prova-social", "small business owner shop", "latin entrepreneur store"),
    ("05-urgencia", "calendar planner schedule", "agenda calendar desk"),
    ("06-antes-depois-vazio", "empty store interior", "empty shop counter"),
    ("06-antes-depois-cheio", "busy store customers", "crowded shop people"),
    ("07-dor", "worried businessman laptop", "frustrated person computer"),
    ("08-premium", "video call meeting laptop", "online meeting screen"),
    ("09-autoridade", "dark minimal background texture", "dark gradient backdrop"),
    ("10-cta", "hand pointing at phone screen", "finger touching smartphone"),
]


def buscar(q, api_key, tentativas=3):
    url = f"{API}?{urllib.parse.urlencode({'query': q, 'per_page': 12, 'orientation': 'landscape'})}"
    req = urllib.request.Request(
        url, headers={"Authorization": api_key,
                      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    ultimo = None
    for n in range(tentativas):
        try:
            with urllib.request.urlopen(
                    req, timeout=30 * (n + 1),
                    context=ssl.create_default_context()) as r:
                return json.load(r)
        except Exception as e:
            ultimo = e
    raise ultimo


def escolher(dados):
    """A foto e o credito, ou None.

    Paisagem com folga (>=1.4) porque o corte final e 1200x628, que e 1.91:1 —
    foto quase quadrada perde metade do enquadramento no crop. Minimo de
    1600px de largura pela mesma razao: o corte tira e nao devolve.
    """
    for f in dados.get("photos", []):
        larg, alt = f.get("width", 0), f.get("height", 0)
        if not alt or larg / alt < 1.4 or larg < 1600:
            continue
        link = f.get("src", {}).get("large2x") or f.get("src", {}).get("large")
        if not link:
            continue
        return link, {"pexels_id": f["id"], "autor": f.get("photographer", ""),
                      "url": f.get("url", "")}
    return None


def baixar(link, caminho):
    req = urllib.request.Request(
        link, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    with urllib.request.urlopen(req, timeout=60,
                                context=ssl.create_default_context()) as r:
        dados = r.read()
    # 10 kB separa JPEG de pagina de erro salva com extensao de imagem.
    if len(dados) < 10000:
        raise ValueError(f"resposta de {len(dados)} bytes")
    with open(caminho, "wb") as fp:
        fp.write(dados)


def main():
    api_key = chave()
    if not api_key:
        from broll import ORIGEM_DA_CHAVE
        raise SystemExit(f"sem chave do Pexels — {ORIGEM_DA_CHAVE}")

    os.makedirs(DESTINO, exist_ok=True)
    creditos, faltando = {}, []

    for nome, q, alt in PECAS:
        escolha = None
        for termo in (q, alt):
            try:
                escolha = escolher(buscar(termo, api_key))
            except Exception as e:
                print(f"{nome}: busca '{termo}' falhou — {type(e).__name__}: {e}")
                continue
            if escolha:
                break
            print(f"{nome}: '{termo}' sem foto no criterio")

        if not escolha:
            faltando.append(nome)
            continue

        link, credito = escolha
        caminho = os.path.join(DESTINO, f"{nome}.jpg")
        try:
            baixar(link, caminho)
        except Exception as e:
            print(f"{nome}: download falhou — {type(e).__name__}: {e}")
            faltando.append(nome)
            continue

        creditos[nome] = credito
        print(f"{nome}: ok — {credito['autor']} ({credito['url']})")

    with open(os.path.join(DESTINO, "creditos.json"), "w", encoding="utf-8") as fp:
        json.dump(creditos, fp, ensure_ascii=False, indent=2)

    print(f"\n{len(creditos)} de {len(PECAS)} baixadas em {DESTINO}")
    if faltando:
        # Sem codigo de erro: 9 de 11 ja da para subir no Meta, e o passo de
        # commit precisa rodar. A lista basta para reprocessar so o que faltou.
        print(f"faltando: {', '.join(faltando)}")


if __name__ == "__main__":
    main()
