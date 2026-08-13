#!/usr/bin/env python3
"""Publica um pacote no YouTube pela ROTA PROPRIA e fecha os passos de Studio.

Existe porque o que publicou os pacotes de 2026-08-11 era codigo solto dentro de
uma sessao: a cada disparo eu reescrevia o mesmo `videos.insert` resumable, e o
que estava certo num pacote nao estava no seguinte. Regra 'o que vive so no
sandbox esta perdido' — entao mora aqui.

Faz, nesta ordem (a ordem importa e esta medida):

  1. SHORT primeiro. Em canal frio o feed de Shorts entrega e o de longos nao:
     4 shorts entre 1,7 e 17,9 views/hora contra 4 longos entre 0 e 0,2.
     O short leva o link do longo na descricao, nunca o contrario.
  2. LONGO, com a descricao ja apontando para o short publicado.
  3. thumbnails/set — 403 aqui NAO e defeito do codigo: e canal sem verificacao
     por telefone. O upload do video continua valendo, so a capa fica pendente.
  4. captions.insert (multipart) — 409 e SUCESSO: o video ja tem faixa naquele
     idioma. Foi o erro que fez a regra 'nenhum video tem legenda' parecer viva
     depois de resolvida.
  5. playlistItems.insert — playlist por canal levanta sessao, e uma chamada.

Credencial: config.yt_token_<slug> no Supabase (nunca so no sandbox, que
recicla). O access_token de 1h e descartavel; o refresh_token e o que importa.

Uso:
    python3 fabrica/publicar.py <spec.json> --canal <slug> [--playlist <id>]
"""
import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def idioma_do_canal(slug):
    """Le o idioma declarado em config/canais/<slug>.yaml.

    Esta e a fonte de verdade: os treze canais declaram idioma la desde sempre,
    um por arquivo, e e o mesmo valor que a rotina usa para escolher a voz. A
    matriz do frota.yml repetia esse valor a mao — e valor repetido a mao e
    valor que uma hora diverge, calado, num campo que ninguem confere depois de
    publicado.

    Le com regex de proposito: o passo de publicacao do frota.yml instala
    `edge-tts cairosvg pydantic pillow`, sem PyYAML. Um `import yaml` aqui
    derrubaria a publicacao com ModuleNotFoundError DEPOIS do render — o mesmo
    acoplamento que ja matou o reparar-copy com `import cairosvg`.
    """
    caminho = os.path.join(RAIZ, "config", "canais", f"{slug}.yaml")
    if not os.path.exists(caminho):
        return ""
    with open(caminho, encoding="utf-8") as f:
        m = re.search(r'^\s*idioma:\s*"?([\w-]+)"?', f.read(), re.M)
    return m.group(1) if m else ""


def _ctx():
    """Um proxy que re-termina TLS quebra o edge-tts e tambem estas chamadas se
    o CA nao estiver no contexto. SSL_CERT_FILE cobre o caso sem desligar
    verificacao — que nao se desliga em nenhuma hipotese."""
    ca = os.environ.get("SSL_CERT_FILE")
    return ssl.create_default_context(cafile=ca) if ca else None


def _req(url, data=None, method="GET", headers=None, timeout=60):
    r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    return urllib.request.urlopen(r, timeout=timeout, context=_ctx())


def token_do_canal(slug, sb_url, sb_key):
    """Le config.yt_token_<slug>. A tabela tem RLS para service_role, entao a
    chave anon nao serve aqui — e isso e proposital."""
    url = f"{sb_url}/rest/v1/config?chave=eq.yt_token_{slug}&select=valor"
    r = _req(url, headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    linhas = json.load(r)
    if not linhas:
        raise SystemExit(f"sem credencial para {slug}: grave config.yt_token_{slug}")
    return linhas[0]["valor"]


def access_token(tok):
    data = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
    }).encode()
    return json.load(_req(tok["token_uri"], data=data, method="POST"))["access_token"]


def subir(acc, caminho, meta):
    """videos.insert resumable. O corpo vai em JSON e o binario num PUT
    separado — mandar tudo junto estoura o limite de request simples."""
    corpo = json.dumps(meta).encode()
    tam = os.path.getsize(caminho)
    loc = _req(
        f"{UPLOAD}/videos?uploadType=resumable&part=snippet,status",
        data=corpo, method="POST",
        headers={"Authorization": "Bearer " + acc,
                 "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(tam),
                 "X-Upload-Content-Type": "video/mp4"},
    ).headers["Location"]
    with open(caminho, "rb") as f:
        binario = f.read()
    r = _req(loc, data=binario, method="PUT", timeout=900,
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": "video/mp4", "Content-Length": str(tam)})
    return json.load(r)["id"]


def thumbnail(acc, video_id, caminho):
    if not (caminho and os.path.exists(caminho)):
        return "sem arquivo"
    try:
        with open(caminho, "rb") as f:
            _req(f"{UPLOAD}/thumbnails/set?videoId={video_id}", data=f.read(),
                 method="POST", timeout=120,
                 headers={"Authorization": "Bearer " + acc, "Content-Type": "image/png"})
        return "ok"
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "403: canal sem verificacao por telefone (youtube.com/verify)"
        return f"{e.code}: {e.read().decode()[:120]}"


def legenda(acc, video_id, caminho, idioma):
    """409 significa que a faixa daquele idioma ja existe — sucesso, nao falha."""
    if not (caminho and os.path.exists(caminho)):
        return "sem arquivo"
    with open(caminho, "rb") as f:
        srt = f.read()
    meta = json.dumps({"snippet": {"videoId": video_id, "language": idioma,
                                   "name": "", "isDraft": False}}).encode()
    bnd = uuid.uuid4().hex.encode()
    corpo = (b"--" + bnd + b"\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" + meta +
             b"\r\n--" + bnd + b"\r\nContent-Type: application/octet-stream\r\n\r\n" + srt +
             b"\r\n--" + bnd + b"--\r\n")
    try:
        _req(f"{UPLOAD}/captions?part=snippet&uploadType=multipart", data=corpo,
             method="POST", timeout=180,
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": b"multipart/related; boundary=" + bnd})
        return "ok"
    except urllib.error.HTTPError as e:
        return "ja existia (409)" if e.code == 409 else f"{e.code}: {e.read().decode()[:120]}"


def na_playlist(acc, playlist_id, video_id):
    if not playlist_id:
        return "sem playlist"
    corpo = json.dumps({"snippet": {"playlistId": playlist_id,
                                    "resourceId": {"kind": "youtube#video",
                                                   "videoId": video_id}}}).encode()
    try:
        _req(f"{API}/playlistItems?part=snippet", data=corpo, method="POST",
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": "application/json; charset=UTF-8"})
        return "ok"
    except urllib.error.HTTPError as e:
        return f"{e.code}: {e.read().decode()[:120]}"


def orcamento_tags(tags, limite=480):
    """O limite de 500 do YouTube conta tag com espaco ENTRE ASPAS: custa
    len+2. Somar so os caracteres aprova lista que a API rejeita."""
    total, mantidas = 0, []
    for t in tags:
        custo = len(t) + (2 if " " in t else 0)
        if total + custo > limite:
            break
        total += custo
        mantidas.append(t)
    return mantidas, total


def _parece_lista_de_tags(corpo):
    """Distingue a secao de TAGS de um paragrafo que por acaso tem virgulas.

    Sem isso o parse pegava a SORUMLULUK REDDİ (o disclaimer de fontes) do
    seviye-seviye-002 como lista de tags: uma linha so, cinco virgulas, e o
    video subiria com "Verilerin kaynakları: asgari ücret için Çalışma ve
    Sosyal Güvenlik Bakanlığı" como tag de busca.

    Tag e termo de busca: curta e sem pontuacao de frase.
    """
    itens = [t.strip() for t in corpo.split(",") if t.strip()]
    return len(itens) >= 4 and all(
        len(t) <= 40 and ":" not in t and not t.endswith(".") for t in itens
    )


def apontar_para_longo(acc, short_id, longo_id):
    """Reescreve a descricao do short com o link do longo.

    videos.update exige o snippet INTEIRO — mandar so a descricao apaga titulo,
    tags e categoria. Por isso le primeiro.
    """
    try:
        atual = json.load(_req(
            f"{API}/videos?part=snippet&id={short_id}",
            headers={"Authorization": "Bearer " + acc}))
        snip = atual["items"][0]["snippet"]
        link = f"https://youtu.be/{longo_id}"
        if link in (snip.get("description") or ""):
            return "ja apontava"
        snip["description"] = ((snip.get("description") or "").strip()
                               + f"\n\n{link}").strip()
        _req(f"{API}/videos?part=snippet",
             data=json.dumps({"id": short_id, "snippet": snip}).encode(),
             method="PUT",
             headers={"Authorization": "Bearer " + acc,
                      "Content-Type": "application/json; charset=UTF-8"})
        return "ok"
    except Exception as e:  # nunca derruba a publicacao: os videos ja subiram
        return f"falhou: {str(e)[:120]}"


def tempos_do_srt(caminho):
    """Reconstroi a duracao de cada cena a partir da legenda.

    O `tempos.json` morre com o runner, mas o .srt vai para o Storage e carrega
    a mesma informacao: a etapa 3 escreve cada cena como um bloco unico, de
    t+0,15 a t+dur-0,15. Isso permite consertar capitulos de um pacote ja
    publicado sem repetir treze minutos de render.
    """
    def _seg(marca):
        h, m, resto = marca.split(":")
        s, ms = resto.replace(",", ".").split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    inicios, fins = [], []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if "-->" in linha:
                a, b = linha.split("-->")
                inicios.append(_seg(a.strip()) - 0.15)
                fins.append(_seg(b.strip()) + 0.15)
    if not inicios:
        raise SystemExit(f"{caminho} nao tem nenhum bloco de tempo")
    return [
        (inicios[i + 1] - inicios[i]) if i + 1 < len(inicios) else (fins[i] - inicios[i])
        for i in range(len(inicios))
    ]


def atualizar_descricao(acc, video_id, nova):
    """videos.update exige o snippet INTEIRO — mandar so a descricao apaga
    titulo, tags e categoria. Por isso le antes."""
    atual = json.load(_req(f"{API}/videos?part=snippet&id={video_id}",
                           headers={"Authorization": "Bearer " + acc}))
    itens = atual.get("items") or []
    if not itens:
        return f"{video_id} nao existe ou nao e deste canal"
    snip = itens[0]["snippet"]
    if snip.get("description") == nova:
        return "ja estava certa"
    snip["description"] = nova
    _req(f"{API}/videos?part=snippet",
         data=json.dumps({"id": video_id, "snippet": snip}).encode(), method="PUT",
         headers={"Authorization": "Bearer " + acc,
                  "Content-Type": "application/json; charset=UTF-8"})
    return "ok"


def _sem_placeholder(texto, esperado_em):
    """Placeholder na descricao de um video PUBLICO nao se desfaz sozinho.

    O aviso "copy.md ausente" existia e nao impediu nada: em 13/08/2026 o
    seviye-seviye-002 subiu com "{CAPITULOS}" literal para os assinantes. Um
    run que falha se refaz em treze minutos; uma descricao quebrada no ar so
    sai se alguem perceber.
    """
    achados = [p for p in ("{CAPITULOS}", "{TRILHA}", "PLACEHOLDER") if p in texto]
    if achados:
        raise SystemExit(
            f"copy ainda tem {', '.join(achados)} — o render nao preencheu. "
            f"Esperado em {esperado_em}. Publicar assim poe o placeholder na "
            f"descricao do video; rode o render de novo em vez de seguir."
        )


def ler_copy(spec, workdir):
    """Devolve {titulo, descricao, tags, hashtags, comentario} a partir do copy.

    Duas fontes, nesta ordem: o `copy.md` que o render escreveu no workdir, e o
    `copy` da spec. A ordem importa — o render substitui {CAPITULOS} pelos
    tempos medidos nos clipes RENDERIZADOS, e a spec so tem o placeholder.
    Publicar da spec poria "{CAPITULOS}" literal na descricao do YouTube.

    O `copy` e markdown em TODAS as 22 specs do repositorio, mas esta funcao
    aceitava apenas dict — `cp["titulo"]` num str e AttributeError, entao o
    passo de publicacao do frota.yml nunca completou com spec de verdade.

    O parse e por CONTEUDO, nao por cabecalho: os cabecalhos sao traduzidos
    (TITULO, TITLE, TÍTULO, ΤΙΤΛΟΣ, TYTUŁ, BAŞLIK) e a ordem varia entre as
    specs de 5 e as de 9 secoes. Posicao 1 e 2 sao estaveis (titulo, descricao);
    o resto se reconhece pelo formato do corpo.
    """
    if isinstance(spec.get("copy"), dict):
        return spec["copy"]

    bruto = ""
    md = os.path.join(workdir, "copy.md")
    if os.path.exists(md):
        with open(md, encoding="utf-8") as f:
            bruto = f.read()
    else:
        bruto = spec.get("copy") or ""
        print("aviso: copy.md ausente — usando a spec, capitulos podem vir sem tempo")
    _sem_placeholder(bruto, md)
    if not bruto.strip():
        raise SystemExit("spec sem copy: nao da para publicar sem titulo e descricao")

    secoes = []
    for bloco in re.split(r"^## +", bruto, flags=re.M)[1:]:
        linhas = bloco.split("\n")
        secoes.append((linhas[0].strip(), "\n".join(linhas[1:]).strip()))
    if len(secoes) < 2:
        # Cinco specs trazem `copy` so como bilhete ("gerado a partir dos
        # capitulos reais apos o render") — para elas o copy.md nao e preferido,
        # e obrigatorio. Melhor parar aqui do que publicar o bilhete como
        # descricao, que e exatamente o que o codigo antigo faria.
        raise SystemExit(
            f"copy sem secoes reconheciveis (achei {len(secoes)}). Esta spec depende "
            f"do copy.md que o render escreve em {workdir} — publique a partir do "
            f"workdir do render, nao da spec."
        )

    titulo = secoes[0][1].strip().split("\n")[0]
    descricao = secoes[1][1].strip()

    tags, hashtags, comentario, capitulos = [], "", "", ""
    for _, corpo in secoes[2:]:
        linhas = [x for x in corpo.split("\n") if x.strip()]
        if not linhas:
            continue
        if all(re.match(r"^\d{1,3}:\d{2}\b", x) for x in linhas):
            capitulos = corpo
        elif len(linhas) == 1 and linhas[0].startswith("#"):
            hashtags = linhas[0]
        elif len(linhas) == 1 and corpo.count(",") >= 3 and _parece_lista_de_tags(corpo):
            tags = [t.strip() for t in corpo.split(",") if t.strip()]
        elif not comentario and not corpo.startswith("-"):
            comentario = corpo

    # Capitulos entram na descricao so se o proprio texto ainda nao os tiver:
    # o placeholder {CAPITULOS} pode estar no meio da AÇIKLAMA em spec antiga.
    if capitulos and capitulos not in descricao:
        descricao = f"{descricao}\n\n{capitulos}"
    if hashtags:
        descricao = f"{descricao}\n\n{hashtags}"

    return {"titulo": titulo, "descricao": descricao, "tags": tags,
            "hashtags": hashtags, "comentario": comentario}


def meta_video(titulo, descricao, tags, idioma, publico=True):
    mantidas, _ = orcamento_tags(tags)
    return {
        "snippet": {"title": titulo[:100], "description": descricao, "tags": mantidas,
                    "categoryId": "27", "defaultLanguage": idioma,
                    "defaultAudioLanguage": idioma},
        # containsSyntheticMedia e obrigatorio e nao reduz alcance: a politica do
        # YouTube pune quem NAO divulga, nao quem divulga.
        "status": {"privacyStatus": "public" if publico else "private",
                   "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True},
    }


def reparar(args, sp, d, sb_url, sb_key):
    """Conserta a descricao de um pacote ja publicado, sem re-renderizar.

    Existe porque em 13/08/2026 o seviye-seviye-002 subiu com "{CAPITULOS}"
    literal na descricao: o `etapas.py` nunca escrevia copy.md e o publicar.py
    caiu no texto cru da spec com um aviso que nao impedia nada. Os dois
    defeitos estao consertados, mas os videos ja estavam no ar — e refazer
    treze minutos de render so para recalcular capitulos e desperdicio quando
    o .srt entregue no Storage carrega os mesmos tempos.
    """
    # copy_md, nao fabrica: formatar markdown nao pode exigir cairosvg.
    # O primeiro run deste reparo morreu exatamente nisso (run 31656308340).
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import copy_md

    alvos = json.loads(args.reparar)
    srt = os.path.join(d, "legendas.srt")
    if not os.path.exists(srt):
        raise SystemExit(f"preciso de {srt} para recalcular os capitulos")

    tempos = tempos_do_srt(srt)
    caps = copy_md.capitulos(sp, tempos)
    # A rotina registra `capitulos` em videos, e ate aqui esse numero so existia
    # dentro do markdown. Sem imprimir, o registro fica nulo ou chutado.
    print(f"capitulos: {len(caps)} em {sum(tempos):.1f}s ({caps[0]} ... {caps[-1]})")
    copy_md.escrever_copy(sp, tempos, d)
    cp = ler_copy(sp, d)

    acc = access_token(token_do_canal(args.canal, sb_url, sb_key))
    saida = {}
    if alvos.get("longo"):
        desc = cp["descricao"]
        if alvos.get("short"):
            desc += f"\n\nVersao curta: https://youtube.com/shorts/{alvos['short']}"
        saida["longo"] = atualizar_descricao(acc, alvos["longo"], desc)
        print("LONGO:", alvos["longo"], "->", saida["longo"])
    if alvos.get("short"):
        curta = cp["descricao"].split("\n\n")[0]
        if alvos.get("longo"):
            curta += f"\n\nhttps://youtu.be/{alvos['longo']}"
        saida["short"] = atualizar_descricao(acc, alvos["short"], curta)
        print("SHORT:", alvos["short"], "->", saida["short"])

    print(json.dumps(saida))
    return saida


def main():
    p = argparse.ArgumentParser()
    p.add_argument("spec")
    p.add_argument("--canal", required=True)
    p.add_argument("--playlist", default=None)
    p.add_argument("--dir", default=None, help="workdir (padrao: /tmp/f/<pacote>)")
    p.add_argument("--idioma", default="",
                   help="Idioma do canal (tr, hi, es-MX...). Vence o da spec.")
    p.add_argument("--reparar", default="",
                   help='JSON {"short":"id","longo":"id"} — so conserta a descricao '
                        'de video ja publicado, nao envia nada')
    args = p.parse_args()

    sb_url = os.environ["SUPABASE_URL"].rstrip("/")
    sb_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    sp = json.load(open(args.spec))
    d = args.dir or f"/tmp/f/{sp.get('pacote') or sp['slug']}"
    # O idioma decide defaultLanguage e defaultAudioLanguage do video, e a
    # linguagem da faixa de legenda. Tres fontes, da mais explicita para a mais
    # estavel: o argumento, a spec, e o config/canais/<slug>.yaml.
    #
    # O default "en" que estava aqui era o defeito: 21 das 24 specs nao
    # declaram `idioma`, entao qualquer disparo que esquecesse --idioma poria
    # o video no ar marcado como ingles — em grego, em hindi, em polones. Nao
    # ha default seguro para idioma, do mesmo jeito que nao ha para o pacote.
    idioma = args.idioma or sp.get("idioma") or idioma_do_canal(args.canal)
    if not idioma:
        raise SystemExit(
            f"idioma indefinido para o canal {args.canal}: nao veio em --idioma, "
            f"nem na spec, nem em config/canais/{args.canal}.yaml. Publicar assim "
            f"marcaria o video na lingua errada."
        )

    if args.reparar:
        return reparar(args, sp, d, sb_url, sb_key)

    cp = ler_copy(sp, d)

    acc = access_token(token_do_canal(args.canal, sb_url, sb_key))
    saida = {}

    # 1) SHORT primeiro — e ele que recebe distribuicao em canal frio.
    #    Medido: com 6 a 8 dias de vida o short entrega 130x o longo.
    curto = os.path.join(d, "short.mp4")
    if os.path.exists(curto):
        sid = subir(acc, curto, meta_video(
            cp.get("short_titulo") or cp["titulo"],
            cp.get("short_descricao") or cp["descricao"].split("\n\n")[0],
            (cp.get("short_tags") or cp.get("tags") or [])[:8], idioma))
        saida["short"] = sid
        print("SHORT:", sid, "| playlist:", na_playlist(acc, args.playlist, sid))

    # 2) LONGO, ja apontando para o short.
    longo = os.path.join(d, "video.mp4")
    if os.path.exists(longo):
        desc = cp["descricao"]
        if saida.get("short"):
            desc += f"\n\nVersao curta: https://youtube.com/shorts/{saida['short']}"
        vid = subir(acc, longo, meta_video(cp["titulo"], desc, cp.get("tags", []), idioma))
        saida["longo"] = vid
        print("LONGO:", vid)
        print("  thumbnail:", thumbnail(acc, vid, os.path.join(d, "thumbnail.png")))
        print("  legenda  :", legenda(acc, vid, os.path.join(d, "legendas.srt"), idioma))
        print("  playlist :", na_playlist(acc, args.playlist, vid))

        # O short sobe ANTES do longo existir, entao o CTA dele ("a conta
        # completa esta no canal") aponta para lugar nenhum ate aqui. Sem este
        # passo o short manda o publico procurar sozinho — e a razao de existir
        # do short e justamente levar ao longo.
        if saida.get("short"):
            print("  short->longo:", apontar_para_longo(acc, saida["short"], vid))

    print(json.dumps(saida))
    return saida


if __name__ == "__main__":
    main()
