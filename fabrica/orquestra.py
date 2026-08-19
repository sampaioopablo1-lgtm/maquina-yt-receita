#!/usr/bin/env python3
"""Decide o que produzir e conta como a maquina esta. Sem palpite meu.

Chama-se orquestra e nao maquina porque `src/maquina/` JA e um pacote:
com os dois no caminho, `import maquina` traz um ou outro conforme a
ordem de importacao, e a suite inteira quebrou assim antes deste commit.
Modulo que some sem avisar e o defeito mais caro deste repositorio.

POR QUE ISTO EXISTE, com os erros que o motivaram (13/08/2026):

  - Contei quinze pacotes como "prontos para disparar". Dez ja estavam no ar
    desde 05/08. A lista teria posto duplicata em dez canais.
  - Produzi copy para o resep-naik-level acreditando que o canal estava em
    zero. Estava em zero porque duas linhas dele tinham `canal` errado no banco.
  - Reportei "estoque 31/50" varias vezes sem que ninguem pudesse conferir de
    onde saia o numero.

Os tres erros tem a mesma forma: eu li o estado, guardei na cabeca, e agi. A
correcao nao e prestar mais atencao — e nao guardar na cabeca. Aqui o estado
sai do banco toda vez, a selecao e deterministica, e o relatorio mostra a conta.

    orquestra.py estado                # onde cada canal esta em relacao a meta
    orquestra.py proximo --n 10        # a matriz do frota.yml, escolhida sozinha
    orquestra.py relatorio             # o texto do informe diario

Sem rede? Passe --dados <arquivo.json> com o retorno de /rest/v1/videos. E
assim que este modulo e testado, e e assim que se reproduz uma decisao antiga.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS = os.path.join(RAIZ, "fabrica", "specs")
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

META_POR_CANAL = 10       # longos publicados por canal
MAX_POR_DIA_POR_CANAL = 3  # trava da rotina contra spam


# --------------------------------------------------------------------- estado

def busca_videos(sb_url: str, sb_key: str) -> list[dict]:
    # `titulo` entra porque a trava por pacote sozinha nao basta: o banco
    # guarda o nome da RODADA e a spec tem outro. Sem esta coluna a conferencia
    # por titulo devolve conjunto vazio e nao barra nada.
    url = (f"{sb_url}/rest/v1/videos"
           f"?select=canal,pacote,formato,youtube_id,publicado_em,erro,titulo")
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def carrega_videos(args) -> list[dict]:
    if args.dados:
        return json.load(open(args.dados, encoding="utf-8"))
    return busca_videos(os.environ["SUPABASE_URL"].rstrip("/"),
                        os.environ["SUPABASE_SERVICE_ROLE_KEY"])


def busca_canais_com_destino(sb_url: str, sb_key: str) -> set[str]:
    """Slugs cujo canal EXISTE no YouTube.

    `canais.youtube_channel_id` e a mesma coluna que a `v_maquina_fila` usa
    para o campo `no_youtube`. O handle do config/canais/*.yaml nao serve: em
    onze dos treze arquivos ele ainda e o comentario "preencher quando o canal
    for criado".
    """
    url = f"{sb_url}/rest/v1/canais?select=slug,youtube_channel_id"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    with urllib.request.urlopen(req, timeout=60) as r:
        return {c["slug"] for c in json.load(r) if c.get("youtube_channel_id")}


def canais_do_repo() -> list[str]:
    d = os.path.join(RAIZ, "config", "canais")
    return sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{d}/*.yaml"))


def specs_do_repo() -> dict[str, dict]:
    fora = {}
    for p in sorted(glob.glob(f"{SPECS}/*.json")):
        sp = json.load(open(p, encoding="utf-8"))
        if sp.get("longo"):
            fora[os.path.basename(p)[:-5]] = sp
    return fora


def publicados_por_pacote(videos: list[dict]) -> set[str]:
    """Pacotes com pelo menos um formato no ar.

    A ligacao e pelo `pacote`, nao pelo titulo: titulo muda entre a spec e o
    que foi publicado. Onde `pacote` e nulo o vinculo se perde — por isso o
    relatorio conta essas linhas em separado em vez de ignora-las.
    """
    return {v["pacote"] for v in videos if v.get("pacote") and v.get("youtube_id")}


def titulos_no_ar(videos: list[dict]) -> set[str]:
    """Titulos ja publicados, normalizados para comparacao."""
    return {v["titulo"].strip().casefold()
            for v in videos if v.get("titulo") and v.get("youtube_id")}


def titulo_da_spec(sp: dict) -> str:
    """O titulo que a spec vai publicar, lido do `copy` ANTES do render.

    NAO usa `publicar.ler_copy` de proposito. Ele recusa qualquer copy que
    ainda tenha `{CAPITULOS}` — e ter esse placeholder e o estado normal de uma
    spec que nao renderizou, que e exatamente quando esta pergunta e feita.
    Tentei por ali primeiro e a funcao devolvia string vazia para TODAS as
    specs, o que fazia a trava por titulo nao barrar nada.

    O titulo e a primeira secao `## ` do markdown, mesma convencao que o
    `ler_copy` usa para a posicao 1.
    """
    copy = sp.get("copy")
    if isinstance(copy, dict):
        return copy.get("titulo", "") or ""
    if not isinstance(copy, str) or not copy.strip():
        return ""
    import re
    secoes = re.split(r"^## +", copy, flags=re.M)[1:]
    if not secoes:
        return ""
    corpo = secoes[0].split("\n")[1:]
    for linha in corpo:
        if linha.strip():
            return linha.strip()
    return ""


def ja_no_ar(nome: str, sp: dict, por_pacote: set[str], por_titulo: set[str]) -> str:
    """Por que esta spec NAO deve entrar na matriz, ou string vazia.

    Duas perguntas, porque uma so nao basta. `videos.pacote` guarda o nome da
    RODADA que publicou (nivel-do-jogo-cron-2026-08-13), nao o da spec
    (nivel-do-jogo-002): perguntar so pelo pacote devolve "nunca publicado",
    que e verdade sobre o nome e mentira sobre o video.

    Medido em 17/08/2026: cinco dos seis pacotes de cada disparo do cron ja
    estavam no ar e mesmo assim renderizavam doze minutos cada para abortar na
    trava do publicar.py — que pergunta pelo titulo e por isso acertava.
    """
    if nome in por_pacote:
        return "ja publicado (pelo nome do pacote)"
    t = titulo_da_spec(sp).strip().casefold()
    if t and t in por_titulo:
        return "ja publicado (pelo titulo, sob outro nome de pacote)"
    return ""


def estado(videos: list[dict]) -> dict:
    specs = specs_do_repo()
    ja = publicados_por_pacote(videos)
    titulos = titulos_no_ar(videos)

    por_canal = {}
    for c in canais_do_repo():
        # DISTINTOS por titulo, nao linhas. A meta e "dez videos diferentes
        # no canal", e o cron republicou o MESMO pacote todo dia: em
        # 19/08/2026 havia 26 duplicatas em seis canais, e as duas piores
        # eram justamente as que o placar dava por prontas — o kolejny-poziom
        # marcava 10 de 10 com CINCO videos distintos, seis linhas do mesmo
        # "Emerytura z ZUS" publicadas de 11 a 17/08.
        #
        # Contar linha nao so inflava o placar: punha o canal em faltam=0, no
        # fim da ordem de `proximo`, onde ele nunca mais seria escolhido.
        # Um canal pela metade ficava invisivel para a propria maquina.
        # Chave: o TITULO quando existe, senao o proprio youtube_id. Assim uma
        # republicacao (mesmo titulo, id novo) colapsa, e uma linha sem titulo
        # continua valendo um — porque o modo de falha oposto e pior: sumir com
        # um video que existe faz a maquina reproduzir o que ja tem.
        longos = {(v.get("titulo") or "").strip().casefold() or v["youtube_id"]
                  for v in videos
                  if v.get("canal") == c and v.get("formato") == "longo"
                  and v.get("youtube_id")}
        # Spec de producao e a que tem sufixo -00N; as sem sufixo sao pilotos v1.
        minhas = {n: sp for n, sp in specs.items()
                  if sp.get("slug") == c and n[-4:-3] == "-" and n[-3:].isdigit()}
        por_canal[c] = {
            "publicados": len(longos),
            "faltam": max(0, META_POR_CANAL - len(longos)),
            "specs": sorted(minhas),
            "specs_no_ar": sorted(n for n in minhas
                                  if ja_no_ar(n, minhas[n], ja, titulos)),
            "specs_pendentes": sorted(n for n in minhas
                                      if not ja_no_ar(n, minhas[n], ja, titulos)),
        }

    orfas = [v for v in videos if v.get("youtube_id") and not v.get("pacote")]
    return {
        "meta_por_canal": META_POR_CANAL,
        "canais": por_canal,
        "publicados_total": sum(c["publicados"] for c in por_canal.values()),
        "meta_total": META_POR_CANAL * len(por_canal),
        "linhas_sem_pacote": len(orfas),
    }


# -------------------------------------------------------------------- selecao

def _falhas_baratas(nome: str, sp: dict) -> list[str]:
    """Portoes que rodam em milissegundos.

    O layout fica de fora de proposito: ele rasteriza cada cena e leva minutos
    por spec. Ele roda como passo do frota.yml, onde reprovar ainda custa
    segundos e nao um pacote.
    """
    import prontidao as P

    caminho = os.path.join(SPECS, f"{nome}.json")
    faltas = []
    for fn in (lambda: P._gate_identidade(caminho, sp),
               lambda: P._gate_copy(sp),
               lambda: P._gate_narracao(caminho),
               lambda: P._gate_duracao(sp)):
        faltas += fn()
    return faltas


def proximo(videos: list[dict], n: int,
            com_destino: set[str] | None = None) -> tuple[list[dict], list[dict]]:
    """A matriz do frota.yml, e o motivo de cada spec descartada.

    Ordem: canal mais LONGE da meta primeiro. Um canal em zero vale mais que o
    decimo video de um canal que ja tem nove — a meta e por canal, entao o
    ganho marginal e maior onde falta mais.
    """
    import prontidao as P  # noqa: F401  (garante que os portoes importam)

    est = estado(videos)
    specs = specs_do_repo()
    ja = publicados_por_pacote(videos)
    titulos = titulos_no_ar(videos)

    escolhidas, descartadas = [], []
    por_canal_hoje: dict[str, int] = {}

    ordem = sorted(est["canais"].items(),
                   key=lambda kv: (-kv[1]["faltam"], kv[0]))
    for canal, info in ordem:
        for nome in info["specs_pendentes"]:
            if len(escolhidas) >= n:
                break
            repetido = ja_no_ar(nome, specs[nome], ja, titulos)
            if repetido:
                descartadas.append({"spec": nome, "motivo": repetido})
                continue
            # Canal que nao existe no YouTube renderiza doze minutos e nao tem
            # onde publicar. O cocina-por-niveles esta assim desde 05/08 e
            # entrava em toda matriz. `None` desliga a conferencia, que e o que
            # os testes sem rede querem.
            if com_destino is not None and canal not in com_destino:
                descartadas.append({"spec": nome,
                                    "motivo": "canal ainda nao existe no YouTube"})
                continue
            if por_canal_hoje.get(canal, 0) >= MAX_POR_DIA_POR_CANAL:
                descartadas.append({"spec": nome,
                                    "motivo": f"teto de {MAX_POR_DIA_POR_CANAL}/dia no canal"})
                continue
            faltas = _falhas_baratas(nome, specs[nome])
            if faltas:
                descartadas.append({"spec": nome, "motivo": "; ".join(faltas)})
                continue
            # O idioma vai RESOLVIDO na matriz, nunca vazio. O frota.yml
            # aceitaria vazio (o publicar.py cai no config do canal), mas ai a
            # matriz deixa de dizer em que lingua o video vai ao ar — e foi
            # exatamente um campo silencioso desses que quase publicou hindi
            # marcado como ingles.
            from publicar import idioma_do_canal

            idioma = specs[nome].get("idioma") or idioma_do_canal(canal)
            if not idioma:
                descartadas.append({"spec": nome,
                                    "motivo": f"idioma indefinido: nem na spec nem "
                                              f"em config/canais/{canal}.yaml"})
                continue
            escolhidas.append({"canal": canal, "pacote": nome, "idioma": idioma})
            por_canal_hoje[canal] = por_canal_hoje.get(canal, 0) + 1
    return escolhidas, descartadas


# ------------------------------------------------------------------ relatorio

def relatorio(videos: list[dict]) -> str:
    est = estado(videos)
    escolhidas, descartadas = proximo(videos, 10)

    L = []
    pub, meta = est["publicados_total"], est["meta_total"]
    L.append(f"MAQUINA — {pub}/{meta} longos publicados "
             f"({META_POR_CANAL} por canal em {len(est['canais'])} canais)")
    L.append("")
    L.append(f"{'canal':22} {'no ar':>6} {'faltam':>7}  specs pendentes")
    for c, i in sorted(est["canais"].items(), key=lambda kv: (-kv[1]["faltam"], kv[0])):
        pend = ", ".join(i["specs_pendentes"]) or "—"
        L.append(f"{c:22} {i['publicados']:6} {i['faltam']:7}  {pend}")

    L.append("")
    L.append(f"PROXIMO DISPARO ({len(escolhidas)} pacotes):")
    for e in escolhidas:
        L.append(f"    {e['canal']:22} {e['pacote']}")
    if not escolhidas:
        L.append("    nenhum — veja os motivos abaixo")

    if descartadas:
        L.append("")
        L.append("DESCARTADAS:")
        for d in descartadas:
            L.append(f"    {d['spec']:24} {d['motivo'][:110]}")

    faltam_specs = sum(i["faltam"] for i in est["canais"].values()) - len(
        [s for i in est["canais"].values() for s in i["specs_pendentes"]])
    L.append("")
    L.append(f"Para fechar a meta faltam {sum(i['faltam'] for i in est['canais'].values())} "
             f"longos, e {max(0, faltam_specs)} deles ainda nao tem spec escrita.")
    if est["linhas_sem_pacote"]:
        L.append(f"AVISO: {est['linhas_sem_pacote']} linhas publicadas sem `pacote` — "
                 f"a trava contra republicacao nao enxerga essas.")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("acao", choices=["estado", "proximo", "relatorio"])
    p.add_argument("--n", type=int, default=10, help="maximo de pacotes no disparo")
    p.add_argument("--dados", default=None,
                   help="JSON com as linhas de videos (para rodar sem rede)")
    args = p.parse_args()

    videos = carrega_videos(args)
    if args.acao == "estado":
        print(json.dumps(estado(videos), ensure_ascii=False, indent=1))
    elif args.acao == "proximo":
        com_destino = None
        if not args.dados:
            com_destino = busca_canais_com_destino(
                os.environ["SUPABASE_URL"].rstrip("/"),
                os.environ["SUPABASE_SERVICE_ROLE_KEY"])
        escolhidas, _ = proximo(videos, args.n, com_destino)
        print(json.dumps(escolhidas, ensure_ascii=False))
    else:
        print(relatorio(videos))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
