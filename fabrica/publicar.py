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
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

from caminhos import dir_trabalho

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def trilha_do_canal_config(slug):
    """A assinatura sonora declarada em config/canais/<slug>.yaml.

    Existia so em `canais.trilha`, no banco — fora do alcance dos portoes, que
    rodam offline. O resultado: em 19/08/2026 o kolejny-poziom-005 foi ao ar
    com Deliberate_Thought num canal cuja identidade e Wholesome, e nenhum dos
    sete portoes viu. Quem viu foi um teste do repositorio, e so DEPOIS de
    existir uma segunda spec para divergir dela — tarde demais.

    Regex pelo mesmo motivo que `idioma_do_canal`: o passo de publicacao nao
    instala PyYAML, e um `import yaml` aqui derrubaria a publicacao depois do
    render.
    """
    caminho = os.path.join(RAIZ, "config", "canais", f"{slug}.yaml")
    if not os.path.exists(caminho):
        return ""
    with open(caminho, encoding="utf-8") as f:
        m = re.search(r'^\s*trilha:\s*"?([\w-]+)"?', f.read(), re.M)
    return m.group(1) if m else ""


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


def ja_publicado(pacote, sb_url, sb_key):
    """Devolve os youtube_id ja registrados para este pacote, por formato.

    Existe porque a spec no repositorio NAO diz se o pacote ja foi ao ar. Em
    13/08/2026 eu contei quinze specs como "prontas para disparar" olhando so os
    portoes — e dez delas ja estavam publicadas desde 05/08. Disparar a frota
    com aquela lista teria posto duplicata em dez canais.

    A checagem mora aqui, e nao numa contagem minha, porque aqui e o unico
    ponto por onde toda publicacao passa: nao importa quem disparou nem com que
    lista, o pacote ja publicado para antes de subir o primeiro byte.
    """
    # safe="" porque o padrao do quote NAO escapa a barra, e aqui o valor vai
    # dentro da query-string: uma barra crua mudaria o caminho da requisicao e
    # a resposta viria vazia — liberando exatamente a republicacao que esta
    # funcao existe para impedir.
    url = (f"{sb_url}/rest/v1/videos?pacote=eq.{urllib.parse.quote(pacote, safe='')}"
           f"&youtube_id=not.is.null&select=formato,youtube_id")
    r = _req(url, headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    return {linha["formato"]: linha["youtube_id"] for linha in json.load(r)}


def ja_no_ar_pelo_titulo(titulo, sb_url, sb_key):
    """O MESMO titulo ja esta publicado, sob qualquer nome de pacote?

    A trava por `pacote` acima nao basta, e isso foi medido em 17/08/2026. O
    mesmo render vive sob DOIS nomes: o da spec (kolejny-poziom-002) e o da
    rodada que o publicou (kp-plan-9233-20260811). `videos.pacote` guarda o
    segundo. Perguntando pelo primeiro, o banco responde "nunca publicado" —
    corretamente, e liberando a duplicata.

    Aconteceu de verdade: um disparo automatico da frota levava
    kolejny-poziom-002, seviye-seviye-002 e next-level-money-002, os tres com
    zero linhas na trava por pacote e os tres ja no ar como YLGwalTND7M,
    v2j35YekImM e UK-FswAW4QE. Foram tres duplicatas em tres canais, barradas
    porque alguem cruzou por titulo a mao.

    O titulo e o que o espectador ve, entao e ele que decide se e o mesmo
    video. A comparacao ignora caixa e espaco nas pontas; nao tenta ser
    esperta alem disso, porque um falso positivo aqui SEGURA publicacao boa e o
    operador precisa entender na hora por que segurou.
    """
    alvo = (titulo or "").strip().casefold()
    if not alvo:
        return []
    r = _req(f"{sb_url}/rest/v1/videos?youtube_id=not.is.null"
             f"&select=pacote,formato,youtube_id,titulo",
             headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    return [l for l in json.load(r)
            if (l.get("titulo") or "").strip().casefold() == alvo]


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


def _duracao(d, sp):
    """(duracao do longo, duracao do short) em segundos, ou None quando nao da.

    O longo sai de `tempos.json`, que a etapa 3 escreve com a duracao MEDIDA de
    cada clipe renderizado — a mesma lista que o `etapas.py` soma para imprimir
    "video.mp4 781.2s". O short nao tem tempos.json proprio; sobra o ffprobe,
    que existe no runner mas nao em toda maquina, entao a falta dele devolve
    None em vez de derrubar a publicacao.
    """
    longo = None
    try:
        longo = round(sum(json.load(open(os.path.join(d, "tempos.json")))), 1)
    except Exception:
        pass
    curto = None
    try:
        curto = round(float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", os.path.join(d, "short.mp4")],
            capture_output=True, text=True, timeout=30, check=True).stdout.strip()), 1)
    except Exception:
        pass
    return longo, curto


def registrar(saida, sp, cp, d, canal, sb_url, sb_key):
    """Escreve em `videos` o que acabou de subir.

    Este passo NAO EXISTIA, e a ausencia dele nao dava erro nenhum: o
    publicar.py imprimia os dois ids e saia com codigo 0. Medido em 17/08/2026
    no seja-mais-magra-002 — short 58oHNtVaAbg e longo 8ffwzHFW9ws publicos no
    canal certo as 16:33, e `videos` sem uma linha sequer do pacote.

    O estrago nao e so o registro faltando. As duas travas anti-duplicata la de
    cima consultam `videos`; se a frota publica sem registrar, elas ficam cegas
    justamente para o que a frota publicou. O disparo do cron das 17:01 pos o
    mesmo pacote na fila de novo e as duas travas o teriam deixado passar.

    Falhar aqui nao desfaz nada — os videos ja estao no ar —, entao o erro vira
    aviso com o SQL pronto para a mao, e nao uma excecao que mascara o sucesso.
    """
    longo_s, curto_s = _duracao(d, sp)
    pacote = sp.get("pacote") or sp["slug"]
    hoje = time.strftime("%Y-%m-%d", time.gmtime())
    base = f"{sb_url}/storage/v1/object/public/videos-maquina/{hoje}-{pacote}"

    def _existe(url: str) -> bool:
        """A URL do Storage e montada por CONVENCAO DE NOME, nao por resposta.

        Isso valia enquanto a entrega no Storage era pre-requisito da
        publicacao. Deixou de valer em 24/08/2026, quando o bucket estourou a
        cota do plano (HTTP 402) e o passo de entrega passou a poder falhar sem
        derrubar a publicacao — que e o certo, porque subir no YouTube nao
        depende do Storage.

        Sem esta conferencia, o registro gravaria uma URL que aponta para nada,
        e o aprendizado "presenca de artefato se prova por supabase_url, nao
        por nome de arquivo" viraria mentira: a coluna diria que o arquivo esta
        la justamente quando ele nao esta. Melhor NULL honesto que link morto.
        """
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=20) as r:
                return 200 <= r.status < 300
        except Exception as e:
            print(f"storage ausente para {url.rsplit('/', 1)[-1]}: {e}")
            return False

    linhas = []
    if saida.get("longo"):
        linhas.append({
            "slug": pacote, "status": "publicado", "formato": "longo",
            "titulo": cp["titulo"], "youtube_id": saida["longo"],
            "duracao_s": longo_s, "duracao_short_s": curto_s,
            "cenas": len(sp.get("longo") or []),
            "capitulos": len(re.findall(r"^\d{1,3}:\d{2}\b", cp["descricao"], re.M)),
            "supabase_url": (u if _existe(u := f"{base}-video.mp4") else None),
        })
    if saida.get("short"):
        linhas.append({
            "slug": f"{pacote}-short", "status": "publicado", "formato": "shorts",
            "titulo": cp.get("short_titulo") or cp["titulo"],
            "youtube_id": saida["short"],
            "duracao_s": curto_s, "duracao_short_s": curto_s,
            "cenas": len(sp.get("short") or []), "capitulos": 0,
            "supabase_url": (u if _existe(u := f"{base}-short.mp4") else None),
        })
    for l in linhas:
        l.update({"canal": canal, "pacote": pacote,
                  "fonte_pauta": sp.get("fonte_pauta"),
                  "publicado_em": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    if not linhas:
        return []
    try:
        try:
            _req(f"{sb_url}/rest/v1/videos",
                 data=json.dumps(linhas).encode(), method="POST",
                 headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key,
                          "Content-Type": "application/json",
                          "Prefer": "return=minimal"})
        except urllib.error.HTTPError as e:
            if e.code != 409:
                raise
            # 409 = slug ja usado. Aconteceu em 18/08/2026 com o
            # epomeno-epipedo-003: uma rodada de 11/08, cuja spec nunca entrou
            # no repositorio, ja tinha gravado esse slug para OUTRO video. O
            # video novo estava no ar e ficou fora do banco — cego para as
            # travas anti-duplicata. O slug e so identidade da linha; quem
            # deduplica e (pacote, titulo). Sufixar e registrar vale mais que
            # abortar com o video ja publico.
            for l in linhas:
                l["slug"] = f"{l['slug']}-r2"
            _req(f"{sb_url}/rest/v1/videos",
                 data=json.dumps(linhas).encode(), method="POST",
                 headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key,
                          "Content-Type": "application/json",
                          "Prefer": "return=minimal"})
            print("  registro : slug ja existia; gravado com sufixo -r2",
                  file=sys.stderr)
        _req(f"{sb_url}/rest/v1/canais?slug=eq.{urllib.parse.quote(canal, safe='')}",
             data=json.dumps({"ultimo_pacote_em": "now()"}).encode(), method="PATCH",
             headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key,
                      "Content-Type": "application/json",
                      "Prefer": "return=minimal"})
        print(f"  registro : {len(linhas)} linha(s) em videos")
    except Exception as e:
        # stderr para nao sujar o JSON que o passo seguinte le em stdout.
        print(f"aviso: registro em videos falhou ({e}). Rode a mao:\n"
              f"  insert into videos {json.dumps(linhas, ensure_ascii=False)}",
              file=sys.stderr)
    return linhas


def atualizar_descricao(acc, video_id, nova, idioma):
    """videos.update exige o snippet INTEIRO — mandar so a descricao apaga
    titulo, tags e categoria. Por isso le antes.

    O `idioma` nao e enfeite: reler-e-reenviar PRESERVA o que estiver la, e o
    que estiver la pode estar errado. Em 24/08/2026 uma correcao de descricao
    feita pelo wrapper YOUTUBE_UPDATE_VIDEO do Composio trocou o
    defaultAudioLanguage do kolejny-poziom-010 de `pl` para `en-US` sem pedir
    nada: aquele wrapper so aceita title/description/tags/category/privacy e
    preenche o resto por conta propria. Um video polones marcado como ingles
    entra na recomendacao errada e vira candidato a dublagem automatica.

    Por isso o reparo REAFIRMA o idioma em vez de herdar: o caminho de
    publicacao ja grava os dois campos a partir de `idioma`, e o caminho de
    reparo passa a garantir o mesmo invariante. Vale o mesmo aprendizado do
    default "en": nao existe idioma seguro por omissao.
    """
    atual = json.load(_req(f"{API}/videos?part=snippet&id={video_id}",
                           headers={"Authorization": "Bearer " + acc}))
    itens = atual.get("items") or []
    if not itens:
        return f"{video_id} nao existe ou nao e deste canal"
    snip = itens[0]["snippet"]
    torto = (snip.get("defaultLanguage") != idioma
             or snip.get("defaultAudioLanguage") != idioma)
    if snip.get("description") == nova and not torto:
        return "ja estava certa"
    snip["description"] = nova
    snip["defaultLanguage"] = idioma
    snip["defaultAudioLanguage"] = idioma
    _req(f"{API}/videos?part=snippet",
         data=json.dumps({"id": video_id, "snippet": snip}).encode(), method="PUT",
         headers={"Authorization": "Bearer " + acc,
                  "Content-Type": "application/json; charset=UTF-8"})
    return "ok (idioma reafirmado)" if torto else "ok"


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
        # stderr, nao stdout: o `maquina.py proximo` imprime a matriz JSON em
        # stdout e o diario.yml alimenta o disparo com ela. Um aviso no meio
        # corrompe o JSON e o disparo morre — ou pior, dispara errado.
        print("aviso: copy.md ausente — usando a spec, capitulos podem vir sem tempo",
              file=sys.stderr)
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


def reparar(args, sp, d, sb_url, sb_key, idioma):
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
        saida["longo"] = atualizar_descricao(acc, alvos["longo"], desc, idioma)
        print("LONGO:", alvos["longo"], "->", saida["longo"])
    if alvos.get("short"):
        curta = cp["descricao"].split("\n\n")[0]
        if alvos.get("longo"):
            curta += f"\n\nhttps://youtu.be/{alvos['longo']}"
        saida["short"] = atualizar_descricao(acc, alvos["short"], curta, idioma)
        print("SHORT:", alvos["short"], "->", saida["short"])

    print(json.dumps(saida))
    return saida


def main():
    p = argparse.ArgumentParser()
    p.add_argument("spec")
    p.add_argument("--canal", required=True)
    p.add_argument("--playlist", default=None)
    p.add_argument("--dir", default=None,
                   help="workdir (padrao: $FABRICA_WORKDIR/<pacote>, ou /tmp/f/<pacote>)")
    p.add_argument("--idioma", default="",
                   help="Idioma do canal (tr, hi, es-MX...). Vence o da spec.")
    p.add_argument("--reparar", default="",
                   help='JSON {"short":"id","longo":"id"} — so conserta a descricao '
                        'de video ja publicado, nao envia nada')
    p.add_argument("--repetir", action="store_true",
                   help="publica mesmo que o pacote ja tenha youtube_id em videos. "
                        "So para republicacao deliberada — o padrao e recusar.")
    p.add_argument("--so-conferir-nome", action="store_true",
                   help="roda SO a trava por nome de pacote e sai. Serve para "
                        "rodar ANTES do render, que e onde a colisao custa "
                        "barato.")
    args = p.parse_args()

    sb_url = os.environ["SUPABASE_URL"].rstrip("/")
    sb_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    sp = json.load(open(args.spec))
    # `caminhos.dir_trabalho` e nao a string a mao: este literal ignorava
    # FABRICA_WORKDIR, entao render em disco real + publicar caiam em raizes
    # diferentes — e o modo de falha ruim nao e "nao achei", e achar o resto de
    # uma tentativa velha em /tmp/f e publicar o video errado com o nome certo.
    d = args.dir or dir_trabalho(sp)
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
        return reparar(args, sp, d, sb_url, sb_key, idioma)

    # Conferencia ANTECIPADA do nome do pacote.
    #
    # A trava logo abaixo sempre existiu e sempre funcionou — mas so roda
    # DEPOIS do render, porque publicar e o ultimo passo. Em 19/08/2026 o
    # kolejny-poziom-007 renderizou 89 cenas, 17 minutos de runner, e so entao
    # descobriu que o nome ja pertencia a um video de 11/08. A numeracao deste
    # canal nunca foi sequencial (007 e de 11/08, 003 e de 18/08), e eu escolhi
    # o numero contando longos distintos em vez de olhar os nomes existentes.
    #
    # A pergunta e a mesma; o que muda e a HORA de faze-la. Uma chamada HTTP
    # antes do render custa um segundo e devolve os dezessete minutos.
    #
    # So a trava por PACOTE cabe aqui. A trava por TITULO precisa do copy.md,
    # que so existe depois do render — essa continua no lugar dela.
    if args.so_conferir_nome:
        vivos = ja_publicado(sp.get("pacote") or sp["slug"], sb_url, sb_key)
        if vivos and not args.repetir:
            onde = ", ".join(f"{f}={i}" for f, i in sorted(vivos.items()))
            raise SystemExit(
                f"{sp.get('pacote') or sp['slug']} JA ESTA no ar ({onde}) — "
                f"escolha outro nome de pacote ANTES de renderizar. Confira os "
                f"nomes ja usados no canal, nao a contagem de videos: a "
                f"numeracao nao e sequencial."
            )
        print(f"nome do pacote livre: {sp.get('pacote') or sp['slug']}")
        return

    # Republicar e pior que nao publicar: o canal fica com dois videos iguais,
    # o algoritmo divide a entrega entre eles, e a limpeza e manual em treze
    # canais. Como a spec no repositorio nao carrega o youtube_id, so o banco
    # sabe — entao pergunta-se ao banco, aqui, antes de subir o primeiro byte.
    pacote = sp.get("pacote") or sp["slug"]
    if not args.repetir:
        vivos = ja_publicado(pacote, sb_url, sb_key)
        if vivos:
            onde = ", ".join(f"{f}={i}" for f, i in sorted(vivos.items()))
            raise SystemExit(
                f"{pacote} JA ESTA no ar ({onde}). Para trocar a descricao use "
                f"--reparar; para republicar de proposito use --repetir."
            )

    cp = ler_copy(sp, d)

    # Segunda trava, pelo TITULO. A de cima pergunta pelo nome do pacote, e o
    # mesmo render vive sob dois nomes — o da spec e o da rodada que publicou.
    # So da para conferir aqui embaixo porque o titulo sai do copy.md, que so
    # existe depois do render.
    if not args.repetir:
        iguais = ja_no_ar_pelo_titulo(cp.get("titulo"), sb_url, sb_key)
        if iguais:
            onde = ", ".join(f"{l['formato']}={l['youtube_id']} (pacote {l['pacote']})"
                             for l in iguais)
            raise SystemExit(
                f"titulo JA ESTA no ar: {cp.get('titulo')!r} -> {onde}. O pacote "
                f"{pacote} nao consta publicado porque o banco guarda o nome da "
                f"RODADA, nao o da spec. Para republicar de proposito use "
                f"--repetir."
            )

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
    r_leg = "sem arquivo"
    if os.path.exists(longo):
        desc = cp["descricao"]
        if saida.get("short"):
            desc += f"\n\nVersao curta: https://youtube.com/shorts/{saida['short']}"
        vid = subir(acc, longo, meta_video(cp["titulo"], desc, cp.get("tags", []), idioma))
        saida["longo"] = vid
        print("LONGO:", vid)
        # Mesma historia da legenda, um degrau abaixo. O 403 de thumbnail nao e
        # defeito do codigo — e canal sem verificacao por telefone — mas ate
        # 20/08/2026 ele so era IMPRESSO, e o efeito e permanente: todo longo
        # daquele canal sobe com um quadro qualquer do video no lugar da capa
        # desenhada, o que corta clique. Vira ::warning:: e nao ::error:: porque
        # o video em si esta certo e a correcao e do lado do Pablo, nao daqui.
        r_thumb = thumbnail(acc, vid, os.path.join(d, "thumbnail.png"))
        print("  thumbnail:", r_thumb)
        if r_thumb != "ok":
            print(f"::warning title=Longo com thumbnail automatica::{vid} subiu "
                  f"sem a capa desenhada ({r_thumb}). O PNG existe e esta no "
                  f"Storage; o que falta e permissao no canal.")
        # A legenda do LONGO nao e cosmetica e nao e opcional: alimenta a busca,
        # habilita a traducao automatica e sustenta retencao no mudo. Em canal
        # de idioma nao-ingles isso e metade do alcance (aprendizado 93).
        #
        # Ate 20/08/2026 o resultado desta chamada era so IMPRESSO. O
        # epomeno-epipedo-008 subiu com "legenda: 403 permissions ... not
        # sufficient" e o job ficou VERDE — mesmo defeito do dia: o passo
        # confere que o que ele fez esta certo, e nao reclama do que nao fez.
        # Agora a falha vira ::error:: e derruba o codigo de saida no fim.
        r_leg = legenda(acc, vid, os.path.join(d, "legendas.srt"), idioma)
        print("  legenda  :", r_leg)
        if not r_leg.startswith(("ok", "ja existia", "sem arquivo")):
            print(f"::error title=Longo sem legenda::{vid} foi publicado sem "
                  f"faixa de legenda ({r_leg}). O video ESTA no ar; o que "
                  f"falta e a legenda, que pode ser enviada depois.")
        print("  playlist :", na_playlist(acc, args.playlist, vid))

        # O short sobe ANTES do longo existir, entao o CTA dele ("a conta
        # completa esta no canal") aponta para lugar nenhum ate aqui. Sem este
        # passo o short manda o publico procurar sozinho — e a razao de existir
        # do short e justamente levar ao longo.
        if saida.get("short"):
            print("  short->longo:", apontar_para_longo(acc, saida["short"], vid))

    # Publicar sem registrar deixa as duas travas la de cima cegas para o que a
    # propria frota acabou de subir. Por isso o registro fica aqui, no mesmo
    # processo que publicou, e nao numa etapa separada que alguem pode esquecer.
    registrar(saida, sp, cp, d, args.canal, sb_url, sb_key)

    print(json.dumps(saida))
    # Sai diferente de zero DEPOIS de publicar e registrar. A ordem importa: o
    # video ja esta no ar e o registro ja esta no banco, entao derrubar aqui nao
    # perde nada — so acende a luz. Job verde com longo sem legenda e pior que
    # job vermelho, porque ninguem vai olhar de novo.
    if saida.get("longo") and not r_leg.startswith(
            ("ok", "ja existia", "sem arquivo")):
        raise SystemExit(4)
    return saida


if __name__ == "__main__":
    main()
