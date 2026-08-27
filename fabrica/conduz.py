#!/usr/bin/env python3
"""Publica uma fila de pacotes ja renderizados pela rota ponte, de fora do runner.

QUANDO USAR: quando o Supabase estiver em 402 (PostgREST fechado) e o segredo
YT_OAUTH_JSON nao existir — ou seja, quando nem o caminho normal nem o
`retomar.yml` servirem. A ordem completa esta em
`docs/publicar-pela-sandbox.md`; este script e o passo 6.

O CORPUS CRESCE DENTRO DA RODADA, e essa e a decisao que importa aqui. Cada
pacote recebe o estado anti-duplicata com tudo o que subiu antes dele,
INCLUSIVE o que subiu ha trinta segundos nesta mesma fila. Congelar o estado no
comeco seria deixar a trava cega a partir do segundo pacote, e trava cega tem
exatamente a mesma cara de trava que passou.

Manter o corpus aqui so e valido porque durante a janela ninguem mais escreve
em `videos` — e por isso ele TEM de ser conferido contra o banco no fim:

    select count(distinct lower(btrim(titulo))) from videos
    where youtube_id is not null and titulo is not null;

Em 27/08/2026 a sandbox fechou em 111 e o banco deu 111.

UM PACOTE QUE FALHA NAO DERRUBA A FILA. Ele vai para `falhas` e os outros
seguem: dez canais parados por causa de um seria trocar um problema por dez.

Entradas:
    RAIZ/manifesto.tsv   pacote<TAB>canal<TAB>idioma<TAB>access_token
    RAIZ/corpus.json     {"titulos": [...]}   — o estado de partida
Saidas:
    RAIZ/reg/<pacote>.json   registro de cada pacote, para entrar em `videos`
    RAIZ/corpus.json         reescrito a cada publicacao

Uso:
    RAIZ=/home/user/pub MAQ=/home/user/maq python3 fabrica/conduz.py

Rode com `nohup`: a sandbox mata comando em 180 s e dez uploads passam disso.
"""
import json
import os
import subprocess
import sys
import unicodedata

RAIZ = os.environ.get("RAIZ", "/home/user/pub")
MAQ = os.environ.get("MAQ", "/home/user/maq")


def chave(t: str) -> str:
    """Mesma normalizacao que a consulta do banco: NFC, sem borda, minuscula."""
    return unicodedata.normalize("NFC", t).strip().lower()


def main() -> int:
    corpus = json.load(open(f"{RAIZ}/corpus.json", encoding="utf-8"))["titulos"]
    vistos = {chave(t) for t in corpus}
    falhas, ok = [], []

    for linha in open(f"{RAIZ}/manifesto.tsv", encoding="utf-8"):
        if not linha.strip():
            continue
        pacote, canal, idioma, tok = linha.rstrip("\n").split("\t")

        # `titulos_no_ar_n` acompanha a lista de proposito: quem recebe o estado
        # recusa lista truncada. Em 26/08/2026 uma transcricao cortou a lista no
        # decimo terceiro titulo e nada avisou.
        est = {"ja_publicado": {},
               "titulos_no_ar": [{"titulo": t} for t in corpus],
               "titulos_no_ar_n": len(corpus)}
        assert len(est["titulos_no_ar"]) == est["titulos_no_ar_n"]
        with open(f"{RAIZ}/estado_corrente.json", "w", encoding="utf-8") as f:
            json.dump(est, f, ensure_ascii=False)

        print(f"\n=== {pacote} ({canal}, {idioma}) | corpus {len(corpus)} titulos ===",
              flush=True)
        r = subprocess.run(
            [sys.executable, "fabrica/publicar.py", f"fabrica/specs/{pacote}.json",
             "--canal", canal, "--idioma", idioma, "--access-token", tok,
             "--estado-json", f"{RAIZ}/estado_corrente.json",
             "--registro-json", f"{RAIZ}/reg/{pacote}.json",
             "--dir", f"{RAIZ}/f/{pacote}"],
            cwd=MAQ, env={**os.environ, "FABRICA_WORKDIR": f"{RAIZ}/f"},
            capture_output=True, text=True)

        # O token nao vai para o log NEM no caminho de erro: o publicar.py pode
        # repetir o comando inteiro dentro de uma mensagem, e o caminho de erro
        # e justamente o que ninguem exercita.
        saida = ((r.stdout or "") + (r.stderr or "")).replace(tok, "<TOKEN>")
        print(saida.strip(), flush=True)

        if r.returncode != 0:
            falhas.append(pacote)
            print(f"!!! {pacote} FALHOU (codigo {r.returncode}) — a fila continua",
                  flush=True)
            continue

        reg = json.load(open(f"{RAIZ}/reg/{pacote}.json", encoding="utf-8"))
        for l in reg["linhas"]:
            t = l.get("titulo")
            if t and chave(t) not in vistos:
                vistos.add(chave(t))
                corpus.append(t)
        with open(f"{RAIZ}/corpus.json", "w", encoding="utf-8") as f:
            json.dump({"titulos": corpus}, f, ensure_ascii=False)
        ok.append(pacote)

    print(f"\n===== FIM: {len(ok)} publicados, {len(falhas)} falharam =====")
    print("ok:", ", ".join(ok) or "-")
    print("falhas:", ", ".join(falhas) or "-")
    print("corpus final:", len(corpus), "— confira contra o banco antes de confiar")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
