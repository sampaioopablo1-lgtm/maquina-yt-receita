"""As pecas cuja duracao REAL a rota publica nao deixou medir — parqueadas.

MEDIDO em 17/10. A rota `watch?v=` -> `lengthSeconds` fechou as 03:1x e seguia
fechada as 04:1x (confirmado pela peca de CONTROLE do `vivacidade_publica`).
Nessas duas rodadas o `kolejny-poziom-s049` e o `labtreinamento-s066` foram ao ar
e **nao tiveram ponto de residuo** — a serie do 739 ficou sem crescer por falta
de instrumento, nao por falta de peca.

Isso ja aconteceu antes e em escala: em 16/10 as 03:3x **dezessete** duracoes
reais parqueadas sairam todas de uma vez quando a rota reabriu. A diferenca e que
aquelas foram parqueadas na minha cabeca e no relato; aqui ficam em ARQUIVO.

**E o campo que nao pode faltar e o PROVEDOR, porque ele se MEDE e nao se infere
(733).** O aviso `::warning::NARRACAO PELO PIPER` vive nas anotacoes do JOB, e
anotacao de job envelhece e pode sair do alcance. Se eu parquear sem o provedor,
a rodada que ler o real depois vai **inferir** qual mundo narrou pela distancia
entre previsao e real — que e exatamente o erro que o 733 nomeia, e que me custou
tres rodadas. Entao `provedor` e `job` sao obrigatorios na gravacao.

Formato: uma linha JSON por peca em `docs/pendente/duracoes-a-medir.jsonl`.
"""
from __future__ import annotations

import json
import os

CAMINHO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "pendente", "duracoes-a-medir.jsonl")

OBRIGATORIOS = ("pacote", "youtube_id", "prev_edge", "prev_piper",
                "provedor", "job", "em")


def valida(reg: dict) -> dict:
    """Levanta se faltar campo, em vez de parquear leitura que nao se pode usar."""
    faltam = [c for c in OBRIGATORIOS if not reg.get(c)]
    if faltam:
        raise ValueError(
            "PARQUEAMENTO INCOMPLETO: faltam " + ", ".join(faltam) +
            ". O `provedor` e o `job` sao obrigatorios pelo 733 — sem eles a"
            " rodada que ler o real depois INFERE o provedor pela distancia,"
            " que e o erro que aquele aprendizado nomeia.")
    if reg["provedor"] not in ("edge", "piper"):
        raise ValueError(f"provedor desconhecido: {reg['provedor']!r}")
    return reg


def carrega(caminho: str = None) -> list[dict]:
    caminho = caminho or CAMINHO
    if not os.path.exists(caminho):
        return []
    saida = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                saida.append(json.loads(linha))
    return saida


def parqueia(reg: dict, caminho: str = None) -> bool:
    """Acrescenta UMA peca. Devolve False se o `youtube_id` ja estava la.

    Idempotente de proposito: a rodada pode reexecutar o passo sem duplicar o
    ponto, que e o que inflaria a serie do 739 sem nenhuma medicao nova.
    """
    valida(reg)
    caminho = caminho or CAMINHO
    if any(r.get("youtube_id") == reg["youtube_id"] for r in carrega(caminho)):
        return False
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False, sort_keys=True) + "\n")
    return True


def residuos(reais: dict, caminho: str = None) -> list[dict]:
    """Os residuos das peças parqueadas, contra a previsao do provedor MEDIDO.

    `reais` mapeia `youtube_id -> duracao real em segundos`. Peca sem leitura
    sai com `real=None` e `residuo=None` — ausencia e silencio, nunca zero.

    `estabelecido` aplica o criterio aritmetico do 770: so quando
    `real - previsao > 1,0`, porque o YouTube arredonda PARA CIMA e abaixo disso
    a janela de arredondamento contem a previsao.
    """
    saida = []
    for r in carrega(caminho):
        prev = r["prev_edge"] if r["provedor"] == "edge" else r["prev_piper"]
        real = reais.get(r["youtube_id"])
        res = None if real is None else round(real - prev, 1)
        saida.append({
            "pacote": r["pacote"], "youtube_id": r["youtube_id"],
            "provedor": r["provedor"], "previsao": prev, "real": real,
            "residuo": res,
            "estabelecido": bool(real is not None and (real - prev) > 1.0),
        })
    return saida


def relato(reais: dict = None, caminho: str = None) -> str:
    reais = reais or {}
    linhas = residuos(reais, caminho)
    if not linhas:
        return "nenhuma peca parqueada a medir."
    sem = [l for l in linhas if l["real"] is None]
    com = [l for l in linhas if l["real"] is not None]
    out = [f"PARQUEADAS: {len(linhas)} peca(s) esperando duracao REAL."]
    for l in com:
        marca = "estabelecido" if l["estabelecido"] else "sinal NAO estabelecido (770)"
        out.append(f"  {l['pacote']} ({l['provedor']}): {l['previsao']} -> "
                   f"{l['real']}, residuo {l['residuo']:+} s — {marca}")
    if sem:
        out.append(f"  sem leitura ({len(sem)}): " +
                   ", ".join(l["pacote"] for l in sem))
        out.append("  ausencia de leitura NAO e residuo zero — a rota pode estar"
                   " fechada, e isso se confere com a peca de CONTROLE"
                   " (`vivacidade_publica.veredito_da_rota`).")
    return "\n".join(out)
