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


def _sinal(real, prev) -> int:
    """O sinal ESTABELECIDO do residuo, ou 0 quando ele nao esta — ver o
    docstring de `residuos` para a aritmetica do arredondamento."""
    if real is None:
        return 0
    d = real - prev
    # `>=` e nao `>`, e a diferenca e a BORDA do intervalo: o residuo verdadeiro
    # vive em `(d-1, d]`, ABERTO embaixo, logo ele e todo positivo exatamente
    # quando `d-1 >= 0`. Com `d == 1,0` o intervalo e `(0, 1]` — estritamente
    # positivo, e o sinal ESTA estabelecido. A primeira versao deste criterio
    # (770) escrevia `> 1.0` e perdia justamente a borda; dois pontos da serie
    # moram nela (`kolejny-poziom-s043` e `-s061`, os dois 42,0 -> 43).
    if d >= 1.0:
        return 1
    if d < 0:
        return -1
    return 0


def residuos(reais: dict, caminho: str = None) -> list[dict]:
    """Os residuos das peças parqueadas, contra a previsao do provedor MEDIDO.

    `reais` mapeia `youtube_id -> duracao real em segundos`. Peca sem leitura
    sai com `real=None` e `residuo=None` — ausencia e silencio, nunca zero.

    `estabelecido` aplica o criterio aritmetico do 770, **agora pelos DOIS
    lados** — e a primeira versao dele era de um lado so, o que me fez chamar de
    "nao estabelecido" um ponto cujo sinal NEGATIVO estava provado.

    A aritmetica, e ela e toda a razao: o YouTube arredonda PARA CIMA, logo real
    `R` significa duracao verdadeira em `(R-1, R]`, e o residuo verdadeiro vive
    em `(R-1-prev, R-prev]`. Dai:

      * sinal POSITIVO estabelecido  <=>  `R - prev > 1,0`
        (o piso do intervalo fica acima de zero);
      * sinal NEGATIVO estabelecido  <=>  `R - prev < 0`
        (o TETO do intervalo, que e atingido, fica abaixo de zero);
      * entre os dois o intervalo contem zero, e o sinal NAO esta estabelecido.

    MEDIDO em 17/10 as 20:1x no `epomeno-epipedo-s054` (`A4M3SLs8FEk`): previsao
    edge 41,6, real **41**, residuo nominal **-0,6**. O criterio antigo
    (`> 1,0`) devolvia "nao estabelecido" — mas 41,6 esta ACIMA de todo o
    intervalo `(40; 41]`, logo o residuo verdadeiro esta em `(-1,6; -0,6]` e e
    **estritamente negativo**. E o PRIMEIRO ponto negativo estabelecido da serie,
    em 78 pontos, e ele derruba a frase "N de N acima" que eu venho escrevendo
    desde o 734.

    `sinal` devolve `+1`, `-1` ou `0` (nao estabelecido), para que quem le nao
    tenha de refazer a conta.
    """
    saida = []
    for r in carrega(caminho):
        prev = r["prev_edge"] if r["provedor"] == "edge" else r["prev_piper"]
        real = _real_gravado(r, reais)
        res = None if real is None else round(real - prev, 1)
        saida.append({
            "pacote": r["pacote"], "youtube_id": r["youtube_id"],
            "provedor": r["provedor"], "previsao": prev, "real": real,
            "residuo": res,
            "estabelecido": _sinal(real, prev) != 0,
            "sinal": _sinal(real, prev),
        })
    return saida


def relato(reais: dict = None, caminho: str = None) -> str:
    reais = reais or {}
    linhas = residuos(reais, caminho)
    if not linhas:
        return "nenhuma peca parqueada a medir."
    sem = [l for l in linhas if l["real"] is None]
    com = [l for l in linhas if l["real"] is not None]
    # O cabecalho conta os DOIS baldes: dizer "esperando" com tudo resolvido era
    # um relato falso, e foi pego na primeira execucao depois do `resolve`.
    out = [f"PARQUE: {len(linhas)} peca(s) — {len(sem)} sem leitura,"
           f" {len(com)} com duracao REAL."]
    for l in com:
        if l["sinal"] > 0:
            marca = "estabelecido"
        elif l["sinal"] < 0:
            marca = "estabelecido, e NEGATIVO"
        else:
            marca = "sinal NAO estabelecido (770)"
        out.append(f"  {l['pacote']} ({l['provedor']}): {l['previsao']} -> "
                   f"{l['real']}, residuo {l['residuo']:+} s — {marca}")
    if sem:
        out.append(f"  sem leitura ({len(sem)}): " +
                   ", ".join(l["pacote"] for l in sem))
        out.append("  ausencia de leitura NAO e residuo zero — a rota pode estar"
                   " fechada, e isso se confere com a peca de CONTROLE"
                   " (`vivacidade_publica.veredito_da_rota`).")
    return "\n".join(out)


def pendentes(caminho: str = None) -> list[dict]:
    """So as pecas que ainda NAO tem duracao real gravada."""
    return [r for r in carrega(caminho) if r.get("real") is None]


def resolve(youtube_id: str, real: int, caminho: str = None) -> bool:
    """Grava a duracao REAL na linha da peca. Devolve False se ela nao esta la.

    MEDIDO como PROCESSO em 17/10 as 06:1x, e e a assinatura do 726: o passo de
    PARQUEAR dependia de eu notar que a rota estava fechada. Quando ela esta
    aberta eu meco na hora e nao parqueio nada — logo o parque so recebe peca nas
    rodadas em que eu LEMBRO de olhar o estado da rota, que e exatamente a
    condicao em que eu esqueco passo (o corpus parou sete rodadas assim).

    O conserto e tornar o parqueamento INCONDICIONAL: toda peca publicada entra,
    e a medicao vem depois por aqui. Assim o arquivo e o LOG dos pontos, e o
    pendente e o que ele ainda nao resolveu — nao o que eu me lembrei de anotar.

    **Reescrever com valor DIFERENTE levanta**, em vez de sobrescrever calado: a
    duracao de uma peca publicada nao muda, logo duas leituras discordantes sao
    um problema da ROTA (o 200-sem-campo, o arredondamento) e pedem releitura,
    nao a ultima resposta. E a mesma disciplina do `controle_divergente`.
    """
    caminho = caminho or CAMINHO
    regs = carrega(caminho)
    achou = False
    for r in regs:
        if r.get("youtube_id") != youtube_id:
            continue
        achou = True
        ja = r.get("real")
        if ja is not None and ja != real:
            raise ValueError(
                f"LEITURA DIVERGENTE em {youtube_id}: gravado {ja}, agora {real}."
                " Duracao de peca publicada nao muda — releia antes de decidir,"
                " e confira a rota com a peca de CONTROLE.")
        r["real"] = real
    if not achou:
        return False
    with open(caminho, "w", encoding="utf-8") as f:
        for r in regs:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return True


def _real_gravado(reg: dict, reais: dict):
    """O real do ARQUIVO tem precedencia; `reais` cobre o que ainda nao resolveu."""
    if reg.get("real") is not None:
        return reg["real"]
    return reais.get(reg["youtube_id"])
