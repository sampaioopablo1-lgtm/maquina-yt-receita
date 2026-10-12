#!/usr/bin/env python3
"""Origem livre pelo RETRATO de 06/10. **PREFIRA `pauta_viva.py`.**

SUPERADO EM 12/10, no mesmo dia em que nasceu, e a nota fica no topo porque
deixar dois modulos de pauta com respostas diferentes e exatamente o defeito das
"duas fontes discordantes" que matou tres pacotes em 11/10.

`fabrica/pauta_viva.py` le a PLAYLIST DE UPLOADS pela API — a lista viva, sem
banco e sem retrato — e por isso ve o que este modulo nao pode ver: longo
publicado depois de 06/10. Medido: este modulo dizia UMA origem livre; o vivo
achou TRES, duas delas no epomeno.

**Quando este ainda serve:** quando nao ha token (fora do runner) ou a API nao
responde. Ele e o piso, nao a fonte. E o numero dele SUBESTIMA por construcao.

Origem livre SEM o banco, contada por TITULO DISTINTO. Nao por id.

POR QUE ISTO EXISTE (12/10/2026, e nasce de um erro meu de uma rodada antes).

Com o gateway do Supabase em 402 a `consultas/estoque.sql` nao roda, e ela e a
unica fonte que exclui origem usada e grupo duplicado **por construcao** (670).
A reconstrucao local que eu fiz no lugar dela vivia em prosa no
`docs/rotina-ponta-a-ponta.md`, e eu a reexecutava a mao a cada rodada.

**Em 12/10 ela me deu o numero errado.** Eu reportei "cinco origens livres"
contando IDS. Medido depois: dos doze ids livres, **dez carregavam o MESMO
TITULO** — `Emerytura z ZUS: 34,4% pensji w 2050 roku`, publicado onze vezes por
um cron entre 13 e 17/08. Sao DEZ COPIAS de UMA origem, e contar id por id
inflou o estoque em dez. A pauta real era TRES.

**E o detalhe que fez isso passar calado:** essas dez copias **nao estao** em
`docs/duplicatas-a-apagar.md`. Uma reconstrucao que exclui duplicata subtraindo
aquele documento nao as pega — logo o documento nao serve de filtro, e a unica
defesa que funciona e agrupar por titulo.

Somar duplicata como estoque e a forma mais crua do efeito (C-2) da rotina:
*"ordenar pelo alcance do short original PREMIA DUPLICATA"*. Aqui nao era a
ordem, era a CONTAGEM.

**O QUE ESTE MODULO NAO E:** nao substitui a consulta. Ele erra para o lado
seguro e carrega as ressalvas no proprio relato:
  1. o retrato `fabrica/ponte/videos.json` e de 06/10 — longo publicado depois
     nao aparece, entao o numero SUBESTIMA;
  2. a exclusao de duplicata aqui e por TITULO, nao pela construcao da consulta.
     Titulos diferentes para o mesmo conteudo passariam;
  3. ele so considera longo com `youtube_id` e `status=publicado`: short precisa
     apontar para longo que existe.
Quando a porta reabrir, **use a consulta** e jogue este modulo fora da decisao.
"""
from __future__ import annotations

import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")

RETRATO = os.path.join(RAIZ, "fabrica", "ponte", "videos.json")
SPECS = os.path.join(RAIZ, "fabrica", "specs")


def _linhas(caminho: str = RETRATO) -> list:
    d = json.load(open(caminho, encoding="utf-8"))
    if isinstance(d, dict):
        d = d.get("videos") or next(iter(d.values()))
    return [v for v in d if isinstance(v, dict)]


def origens_usadas(dir_specs: str = SPECS) -> set:
    """Os `longo_existente` que as specs ja consomem."""
    fora = set()
    for p in glob.glob(os.path.join(dir_specs, "*.json")):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        if sp.get("longo_existente"):
            fora.add(sp["longo_existente"])
    return fora


def longos_publicados(caminho: str = RETRATO) -> dict:
    """{youtube_id: (pacote, titulo, canal)} dos LONGOS da frota no ar."""
    fora = {}
    for v in _linhas(caminho):
        slug = str(v.get("slug") or "")
        pacote = str(v.get("pacote") or "")
        canal = next((c for c in FROTA if pacote.startswith(c)), None)
        if not canal or slug.endswith("-short"):
            continue
        if v.get("status") != "publicado" or not v.get("youtube_id"):
            continue
        fora[v["youtube_id"]] = (pacote, (v.get("titulo") or "").strip(), canal)
    return fora


def livres(caminho: str = RETRATO, dir_specs: str = SPECS) -> list:
    """Uma entrada POR TITULO DISTINTO livre, nao por id.

    Devolve `[(titulo, canal, [ids...])]`, com a lista de ids inteira para que o
    relato possa dizer QUANTAS copias aquele titulo tem no ar. Dez copias de um
    titulo valem UMA origem — e ver as dez e o que impede a proxima contagem
    errada.
    """
    usadas = origens_usadas(dir_specs)
    grupos: dict[tuple, list] = {}
    for yid, (pacote, titulo, canal) in longos_publicados(caminho).items():
        if yid in usadas:
            continue
        # A chave inclui o canal: titulo igual em canais diferentes seria outra
        # peca e outro publico, nao duplicata.
        grupos.setdefault((titulo, canal), []).append(yid)
    # Grupo em que QUALQUER copia ja foi usada sai inteiro: o titulo ja esta
    # servido, e um short apontando para a copia irma seria a mesma pauta.
    por_titulo = {}
    for yid, (pacote, titulo, canal) in longos_publicados(caminho).items():
        por_titulo.setdefault((titulo, canal), []).append(yid)
    fora = []
    for chave, ids in sorted(grupos.items()):
        if any(y in usadas for y in por_titulo[chave]):
            continue
        fora.append((chave[0], chave[1], sorted(ids)))
    return fora


def relato(caminho: str = RETRATO, dir_specs: str = SPECS) -> str:
    L = livres(caminho, dir_specs)
    todos = longos_publicados(caminho)
    usadas = origens_usadas(dir_specs) & set(todos)
    ids_livres = sum(len(ids) for _, _, ids in L)
    linhas = [
        f"longos da frota publicados com id: {len(todos)}",
        f"origens ja usadas por spec:        {len(usadas)}",
        f"ids livres:                        {ids_livres}",
        f"ORIGENS LIVRES (titulo distinto):  {len(L)}",
        "",
    ]
    for titulo, canal, ids in L:
        extra = f"  [{len(ids)} COPIAS no ar — valem UMA]" if len(ids) > 1 else ""
        linhas.append(f"  {canal:16} {ids[0]}  {titulo[:58]}{extra}")
    linhas += [
        "",
        "ESTE MODULO E O PISO, NAO A FONTE: prefira `fabrica/pauta_viva.py`,",
        "que le a playlist de uploads ao vivo e ve longo publicado depois de",
        "06/10. Em 12/10 este disse UMA origem e o vivo achou TRES.",
        "",
        "RESSALVAS, e elas nao saem do relato:",
        "  (1) o retrato e de 06/10 — longo publicado depois nao aparece, entao",
        "      este numero SUBESTIMA (erra para o lado seguro);",
        "  (2) a exclusao de duplicata aqui e por TITULO, nao pela construcao da",
        "      consulta: titulos diferentes para o mesmo conteudo passariam;",
        "  (3) isto NAO substitui `consultas/estoque.sql`. Quando a porta do",
        "      Supabase reabrir, rode a consulta e ignore este modulo.",
    ]
    return "\n".join(linhas)


def main() -> int:
    print(relato())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
