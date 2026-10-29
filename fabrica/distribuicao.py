#!/usr/bin/env python3
"""Distribuir o short ja publicado no YouTube para as OUTRAS redes — UM dono.

PEDIDO DO DONO EM 29/10/2026, nas palavras dele: *"esse mesmo video ele possa
ser publicado automaticamente no Instagram, no TikTok, no YouTube, em outras
redes sociais disponiveis [...] para que gere trafego e assim as pessoas elas
acessem o perfil e o link da bio para comprar o meu curso ou o meu aplicativo."*

MEDIDO ANTES DE ESCREVER, em `docs/distribuicao-multi-rede.md`: das tres rotas
que existem nesta maquina, so UMA e automatica — a API do Upload-Post, cuja
skill ja estava no repo (`.claude/skills/upload-post/`) e que publica em
Instagram, TikTok, Threads, X, LinkedIn, Facebook, Pinterest e Bluesky numa
chamada so. A rota do TikTok pela Higgsfield (`docs/tiktok-sondado.md`) exige
o dono num widget a cada peca, e a Composio NUNCA publica (6/6 apagados). O
YouTube continua saindo pelo `retomar.yml`, que e o dono dele: pedir YouTube
aqui e RECUSADO, porque seria o segundo caminho de publicacao para o mesmo
canal — a assinatura de dois donos que congelou a legenda.

O QUE ESTE MODULO FAZ: monta o PAYLOAD da chamada a partir dos donos que ja
existem (`publicar.ler_copy` para titulo e hashtags, `canal.da_spec` para o
canal, `perfis_sociais.json` para perfil, link da bio e redes), confere se a
DURACAO do arquivo cabe em cada rede — os tetos vem da referencia da skill,
com a procedencia escrita ao lado —, NOMEIA as redes em que nao cabe em vez
de filtra-las em silencio, chama a API sem nunca por a chave em argv nem em
stdout, e PARQUEIA o resultado em `docs/pendente/distribuicoes.jsonl`.

O QUE ELE RECUSA, do jeito que o `porta1` recusa janela curta:
  * canal sem `perfil` no `perfis_sociais.json` — inventar nome de perfil
    mandaria a peca para o perfil de outra pessoa ou para lugar nenhum;
  * `youtube` na lista de plataformas — o dono dele e o `retomar.yml`;
  * plataforma que a API nao conhece, e plataforma que exige id de pagina ou
    de board sem o id no perfil (Facebook, Pinterest, LinkedIn);
  * peca sem duracao MEDIDA — sem ela nao da para dizer se cabe no Reels;
  * chave ausente no ambiente quando se pede para PUBLICAR.

O QUE ELE NAO E: nao e portao (nao reprova spec nenhuma) e nao conecta conta
nenhuma — abrir presenca numa rede nova e decisao do DONO, e a autorizacao de
09/10 cobre os TRES canais do YouTube, nao redes novas. A chave vem do
ambiente (`UPLOAD_POST_API_KEY`), e o segredo e colagem do dono no GitHub,
porque o proxy desta sessao bloqueia a API de secrets.

LINK NA BIO, e por que o CTA e assim: Instagram e TikTok nao deixam link
clicavel na legenda. O que leva ao link e o PERFIL, logo a legenda diz "o link
esta na bio" na lingua do canal, e o link em si vai no PRIMEIRO COMENTARIO
onde a rede aceita (`first_comment`). Esse e o caminho que o dono descreveu.
"""
import datetime as _dt
import json
import os
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import canal as CA        # noqa: E402
import publicar as PB     # noqa: E402

PERFIS = os.path.join(RAIZ, "fabrica", "perfis_sociais.json")
PARQUE = os.path.join(RAIZ, "docs", "pendente", "distribuicoes.jsonl")
API = "https://api.upload-post.com/api/upload"
VAR_DA_CHAVE = "UPLOAD_POST_API_KEY"

# TETO de duracao em segundos por rede, para VIDEO. Procedencia: a referencia
# da skill, `.claude/skills/upload-post/references/requirements.md` (Instagram
# Reels 0-90 s; X 140 s; Bluesky 60 s; TikTok e LinkedIn 3 s a 10 min; Threads
# 5 min; Pinterest 4 s a 15 min; Facebook 240 min). O short da frota mede 41 a
# 45 s e cabe em TODAS; o longo (8 a 10 min) NAO cabe no Instagram, no X, no
# Threads nem no Bluesky — e o instrumento diz isso em vez de calar.
TETO_S = {
    "instagram": 90.0,
    "tiktok": 600.0,
    "threads": 300.0,
    "x": 140.0,
    "bluesky": 60.0,
    "linkedin": 600.0,
    "pinterest": 900.0,
    "facebook": 14400.0,
}
PISO_S = {"tiktok": 3.0, "linkedin": 3.0, "pinterest": 4.0}

# Redes que a API aceita mas que exigem um ID do dono no perfil. Sem ele a
# chamada falha do outro lado, e o nome do campo e o da API.
EXIGE_ID = {
    "facebook": "facebook_page_id",
    "pinterest": "pinterest_board_id",
    "linkedin": "target_linkedin_page_id",
}

# O YouTube tem dono, e nao e este modulo.
RESERVADAS = {
    "youtube": "o YouTube sai pelo retomar.yml, que refresca o token no runner "
               "e grava o registro; mandar daqui seria um SEGUNDO caminho de "
               "publicacao para o mesmo canal",
}

# Limite de legenda das duas redes que o dono nomeou (Instagram e TikTok
# aceitam ate 2.200 caracteres). Acima disso a API corta ou recusa; cortar
# aqui, com as hashtags preservadas, e melhor que descobrir do outro lado.
LEGENDA_MAX = 2200


# ---------------------------------------------------------------- perfis
def perfis(caminho: str = None) -> dict:
    with open(caminho or PERFIS, encoding="utf-8") as f:
        return json.load(f)


def perfil_do_canal(canal: str, mapa: dict = None) -> dict:
    """O perfil do Upload-Post daquele canal — ou RECUSA dizendo o que falta."""
    mapa = mapa if mapa is not None else perfis()
    ent = (mapa.get("canais") or {}).get(canal)
    if not ent:
        raise ValueError(
            "canal %r nao esta em perfis_sociais.json; distribuir sem perfil "
            "mandaria a peca para lugar nenhum — o dono preenche" % (canal,))
    faltam = [k for k in ("perfil", "plataformas") if not ent.get(k)]
    if faltam:
        raise ValueError(
            "canal %r sem %s em perfis_sociais.json: o perfil e o NOME criado "
            "no painel do Upload-Post com as contas do canal conectadas, e so "
            "o dono o conhece. Inventar um mandaria a peca para o perfil de "
            "outra pessoa ou para lugar nenhum" % (canal, " e ".join(faltam)))
    return dict(ent)


# ---------------------------------------------------------------- limites
def cabem(plataformas, duracao_s: float, perfil: dict = None) -> dict:
    """Em que redes a peca CABE, e em quais nao — NOMEADAS com o motivo.

    Plataforma desconhecida ou reservada LEVANTA: isso e erro de chamada e nao
    estado da peca. Rede sem o id obrigatorio no perfil sai como `nao_cabem`,
    porque e o perfil que esta incompleto, nao a peca.
    """
    if duracao_s is None or not (float(duracao_s) > 0):
        raise ValueError(
            "duracao nao MEDIDA: sem ela nao da para dizer se a peca cabe no "
            "Reels (teto de 90 s) — meca com ffprobe antes de distribuir")
    d = float(duracao_s)
    ok, nao = [], {}
    for p in plataformas:
        p = str(p).strip().lower()
        if p in RESERVADAS:
            raise ValueError("plataforma %r RECUSADA: %s" % (p, RESERVADAS[p]))
        if p not in TETO_S:
            raise ValueError(
                "plataforma %r desconhecida; as que a API aceita para video "
                "sao %s" % (p, ", ".join(sorted(TETO_S))))
        if d > TETO_S[p]:
            nao[p] = "%.1f s passa do teto de %.0f s" % (d, TETO_S[p])
            continue
        if d < PISO_S.get(p, 0.0):
            nao[p] = "%.1f s fica abaixo do piso de %.0f s" % (d, PISO_S[p])
            continue
        if p in EXIGE_ID and not (perfil or {}).get(EXIGE_ID[p]):
            nao[p] = "exige %s no perfil, e ele nao esta preenchido" % EXIGE_ID[p]
            continue
        ok.append(p)
    return {"cabem": ok, "nao_cabem": nao, "duracao_s": d}


# ---------------------------------------------------------------- texto
def texto(spec: dict, workdir: str, perfil: dict) -> dict:
    """Titulo, legenda e primeiro comentario — a copy e lida pelo DONO dela.

    Reparsear a copy aqui criaria o segundo dono da regra de secoes, e foi um
    balde pega-tudo dessa regra que quase pos o bloco do Studio como
    comentario fixado (20/10). `publicar.ler_copy` ja devolve o titulo curto
    do short, a descricao e as hashtags.
    """
    try:
        cp = PB.ler_copy(spec, workdir)
    except SystemExit as e:
        # O dono da copy RECUSA copy com placeholder ou sem secoes — e certo.
        # Aqui isso vira recusa de DADO, nao saida do processo.
        raise ValueError("a copy nao esta pronta para publicar: %s"
                         % str(e).split(" Esperado em")[0][:200])
    titulo = (cp.get("short_titulo") or cp.get("titulo") or "").strip()
    if not titulo:
        raise ValueError("copy sem titulo — nao ha legenda a montar")
    cta = (perfil.get("cta") or "").strip()
    hashtags = (cp.get("hashtags") or "").strip()
    legenda = "\n\n".join(x for x in (titulo, cta, hashtags) if x)
    if len(legenda) > LEGENDA_MAX:
        sobra = len(legenda) - LEGENDA_MAX
        legenda = "\n\n".join(x for x in (titulo[:max(1, len(titulo) - sobra)],
                                          cta, hashtags) if x)
    desc = (cp.get("descricao") or "").strip()
    primeiro = desc.split("\n\n")[0].strip() if desc else ""
    link = (perfil.get("link_da_bio") or "").strip()
    comentario = "\n\n".join(x for x in (primeiro, cta, link) if x)
    return {"titulo": titulo, "legenda": legenda[:LEGENDA_MAX],
            "primeiro_comentario": comentario[:LEGENDA_MAX]}


# ---------------------------------------------------------------- payload
def payload(spec: dict, duracao_s: float, workdir: str, plataformas=None,
            mapa: dict = None) -> dict:
    """Os campos da chamada, SEM a chave. Recusa o que nao pode distribuir."""
    canal = CA.da_spec(spec)
    perfil = perfil_do_canal(canal, mapa)
    pedidas = [str(p).lower() for p in (plataformas or perfil["plataformas"])]
    c = cabem(pedidas, duracao_s, perfil)
    if not c["cabem"]:
        raise ValueError(
            "nenhuma das redes pedidas recebe esta peca: %s"
            % "; ".join("%s (%s)" % kv for kv in c["nao_cabem"].items()))
    t = texto(spec, workdir, perfil)
    campos = {
        "user": perfil["perfil"],
        "title": t["titulo"],
        "description": t["legenda"],
        "first_comment": t["primeiro_comentario"],
        "async_upload": "true",
    }
    # Parametros por rede, com os nomes da API (platforms.md da skill).
    if "tiktok" in c["cabem"]:
        campos["privacy_level"] = "PUBLIC_TO_EVERYONE"
        campos["post_mode"] = "DIRECT_POST"
    if "instagram" in c["cabem"]:
        campos["media_type"] = "REELS"
    for p in c["cabem"]:
        if p in EXIGE_ID:
            campos[EXIGE_ID[p]] = perfil[EXIGE_ID[p]]
    return {
        "canal": canal,
        "pacote": spec.get("pacote") or spec.get("slug"),
        "plataformas": c["cabem"],
        "recusadas": c["nao_cabem"],
        "duracao_s": c["duracao_s"],
        "campos": campos,
    }


# ---------------------------------------------------------------- chamada
def _config_da_chave(chave: str, pasta: str) -> str:
    """O cabecalho vai num arquivo 0600 lido com `curl -K`: nunca em argv, que
    qualquer `ps` le, e nunca em stdout."""
    p = os.path.join(pasta, "curl.cfg")
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write('header = "Authorization: Apikey %s"\n' % chave.replace('"', ""))
    return p


def curl_args(pl: dict, video: str, config: str) -> list:
    """A linha do curl. NAO contem a chave: ela esta no arquivo `config`."""
    args = ["curl", "-sS", "-K", config, "-X", "POST", API,
            "-F", "video=@%s" % video]
    for p in pl["plataformas"]:
        args += ["-F", "platform[]=%s" % p]
    for k, v in pl["campos"].items():
        args += ["-F", "%s=%s" % (k, v)]
    return args


def publica(pl: dict, video: str, chave: str = None) -> dict:
    """Chama a API. A chave vem do ambiente quando nao e passada; ausente,
    RECUSA — e o segredo e colagem do dono no GitHub."""
    chave = chave if chave is not None else os.environ.get(VAR_DA_CHAVE, "")
    if not chave.strip():
        raise ValueError(
            "sem %s no ambiente: a chave do Upload-Post e segredo do GitHub, e "
            "o proxy desta sessao bloqueia a API de secrets — colagem do dono"
            % VAR_DA_CHAVE)
    if not os.path.exists(video):
        raise ValueError("video nao existe: %s" % video)
    with tempfile.TemporaryDirectory() as d:
        cfg = _config_da_chave(chave, d)
        r = subprocess.run(curl_args(pl, video, cfg), capture_output=True,
                           text=True, timeout=1800)
    if r.returncode != 0:
        raise RuntimeError("curl saiu com %d: %s" % (r.returncode, r.stderr[-400:]))
    try:
        resp = json.loads(r.stdout)
    except ValueError:
        raise RuntimeError("resposta nao e JSON: %s" % r.stdout[:400])
    if resp.get("success") is False:
        raise RuntimeError("a API recusou: %s" % json.dumps(resp)[:400])
    return resp


# ---------------------------------------------------------------- parque
def registro(pl: dict, youtube_id: str, resposta: dict, run: str = None,
             job: str = None, em: str = None) -> dict:
    return {
        "em": em or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pacote": pl["pacote"],
        "canal": pl["canal"],
        "youtube_id": youtube_id,
        "plataformas": list(pl["plataformas"]),
        "recusadas": dict(pl.get("recusadas") or {}),
        "request_id": (resposta or {}).get("request_id"),
        "resultado": {k: v for k, v in (resposta or {}).items()
                      if k in ("success", "request_id", "results", "message")},
        "run": run,
        "job": job,
    }


def carrega(caminho: str = None) -> list:
    caminho = caminho or PARQUE
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def parqueia(reg: dict, caminho: str = None) -> bool:
    """Grava UMA linha. RECUSA repetir a mesma peca na mesma rede: distribuir
    duas vezes poe o mesmo video duas vezes no perfil, e tirar e irreversivel
    sem o dono."""
    for k in ("pacote", "canal", "youtube_id", "plataformas", "em"):
        if not reg.get(k):
            raise ValueError("registro sem %r" % k)
    caminho = caminho or PARQUE
    for antigo in carrega(caminho):
        if antigo["youtube_id"] != reg["youtube_id"]:
            continue
        rep = sorted(set(antigo["plataformas"]) & set(reg["plataformas"]))
        if rep:
            raise ValueError(
                "a peca %s ja foi distribuida em %s (parqueada em %s); repetir "
                "duplicaria o post, e apagar post e do dono"
                % (reg["youtube_id"], ", ".join(rep), antigo["em"]))
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False, sort_keys=True) + "\n")
    return True


def ja_distribuida(youtube_id: str, caminho: str = None) -> list:
    return sorted({p for r in carrega(caminho) if r["youtube_id"] == youtube_id
                   for p in r["plataformas"]})


# ---------------------------------------------------------------- relato
def _carrega_spec(caminho_ou_spec):
    if isinstance(caminho_ou_spec, dict):
        return caminho_ou_spec
    with open(caminho_ou_spec, encoding="utf-8") as f:
        return json.load(f)


def duracao_medida(video: str) -> float:
    """A duracao REAL do arquivo, pelo ffprobe. Levanta se nao der para medir:
    duracao inferida da previsao nao serve para decidir se cabe no Reels."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", video],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        raise ValueError("ffprobe nao mediu %s: %s" % (video, r.stderr[-200:]))
    return float(r.stdout.strip())


def relato(caminho, video: str = None, duracao_s: float = None,
           plataformas=None, mapa: dict = None) -> str:
    """O que seria distribuido, rede por rede. EXIGE o mp4 renderizado (ou a
    duracao medida dele): sem isso nao ha o que distribuir nem como saber se
    cabe, e responder com a previsao seria inventar medida."""
    if video is None and duracao_s is None:
        raise ValueError(
            "sem o mp4 renderizado (ou a duracao MEDIDA dele) nao ha o que "
            "distribuir: este relato vem DEPOIS do render e da publicacao no "
            "YouTube, nao antes")
    sp = _carrega_spec(caminho)
    if video:
        workdir = os.path.dirname(os.path.abspath(video))
    elif isinstance(caminho, str):
        workdir = os.path.dirname(os.path.abspath(caminho))
    else:
        # spec em memoria e sem video: nao ha copy.md em lugar nenhum, e o
        # dono da copy le a spec quando o workdir nao tem o arquivo.
        workdir = tempfile.mkdtemp(prefix="distribuicao-")
    if duracao_s is None:
        duracao_s = duracao_medida(video)
    try:
        pl = payload(sp, duracao_s, workdir, plataformas, mapa)
    except ValueError as e:
        return "DISTRIBUICAO: RECUSADA — %s" % e
    linhas = ["DISTRIBUICAO: %s (%s), %.1f s, perfil %r"
              % (pl["pacote"], pl["canal"], pl["duracao_s"], pl["campos"]["user"]),
              "  vai para: %s" % ", ".join(pl["plataformas"])]
    for p, m in pl["recusadas"].items():
        linhas.append("  NAO vai para %s: %s" % (p, m))
    linhas.append("  titulo: %s" % pl["campos"]["title"])
    linhas.append("  legenda (%d chars): %s" % (len(pl["campos"]["description"]),
                                                pl["campos"]["description"].replace("\n", " | ")[:160]))
    linhas.append("  CTA: o link NAO e clicavel na legenda do Instagram nem do "
                  "TikTok — ele vai na bio e no primeiro comentario")
    return "\n".join(linhas)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("video")
    ap.add_argument("--plataformas", default=None,
                    help="lista separada por virgula; padrao: as do perfil")
    ap.add_argument("--duracao", type=float, default=None,
                    help="duracao medida; sem ela o ffprobe mede")
    ap.add_argument("--youtube-id", default=None)
    ap.add_argument("--publicar", action="store_true")
    ap.add_argument("--parque", default=None)
    ap.add_argument("--run", default=None)
    ap.add_argument("--job", default=None)
    a = ap.parse_args(argv)
    plats = [x.strip() for x in a.plataformas.split(",")] if a.plataformas else None
    print(relato(a.spec, a.video, a.duracao, plats))
    if not a.publicar:
        return 0
    if not a.youtube_id:
        print("RECUSADO: --publicar exige --youtube-id, que e a chave do parque")
        return 2
    sp = _carrega_spec(a.spec)
    dur = a.duracao if a.duracao is not None else duracao_medida(a.video)
    pl = payload(sp, dur, os.path.dirname(a.video), plats)
    ja = ja_distribuida(a.youtube_id, a.parque)
    if set(pl["plataformas"]) & set(ja):
        print("RECUSADO: %s ja distribuida em %s" % (a.youtube_id, ", ".join(ja)))
        return 2
    resp = publica(pl, a.video)
    reg = registro(pl, a.youtube_id, resp, a.run, a.job)
    parqueia(reg, a.parque)
    print("DISTRIBUIDO: request_id=%s redes=%s"
          % (reg["request_id"], ",".join(reg["plataformas"])))
    print(json.dumps(reg, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
