#!/usr/bin/env python3
"""O que o PROPRIO acervo ja provou — e que a producao nunca consultou.

## O buraco que este arquivo fecha

A maquina tinha memoria da PESQUISA e nao tinha memoria do RESULTADO.

`v_maquina_formatos` guarda o que os concorrentes fazem: views/dia por familia
de formato, coletado por YOUTUBE_SEARCH ao longo de semanas. Ela decide pauta
desde o primeiro disparo, e funciona.

O espelho disso sobre o proprio acervo nao existia. Em 20/08/2026 havia 152
videos no ar e 1.932 linhas em `metricas`, e NENHUMA linha do caminho de
decisao lia qualquer uma delas. A maquina publicava havia duas semanas sem
nunca perguntar o que tinha funcionado — e a pergunta era barata, o dado ja
estava no banco.

## O que entra na conta, e o que nao entra

`views` decide. `retencao` entra quando existe, e quase nunca existe.

Este paragrafo ja afirmou o contrario e a afirmacao era falsa, entao ela fica
registrada: eu escrevi aqui que nenhum dos treze refresh_token carregava
`yt-analytics.readonly` e que retencao e CTR eram portanto incolhiveis sem um
novo consentimento nos doze canais. Baseei isso em `config.yt_token_*.scopes`,
que registra o que foi PEDIDO e nao o que foi concedido. O banco desmente:
a coleta diaria escreve 629 linhas e a query de Analytics RESPONDE — se
faltasse escopo ela daria 403 e o video nao teria linha nenhuma. Doze videos
tem retencao real hoje, e ela MUDA entre coletas.

Retencao aparece em 12 de 629 porque 617 quase nao sao assistidos, nao porque
falte permissao. Isso muda a conclusao inteira: nao ha decisao do dono
pendente, ha audiencia faltando.

Entao a regra e: `views` continua sendo quem decide, porque e o unico numero
que existe para todos. `retencao` viaja junto com `ret_n`, quantos videos do
grupo a tem — mediana sobre um video nao pode parecer mediana sobre trinta —
e entra no prompt so quando ha pelo menos um. Ela e o que diz POR QUE um video
funcionou, e nao apenas QUE funcionou: 0,11 v/d com 28% de retencao e um
problema de distribuicao, 0,11 v/d com 3% e um problema de roteiro. Views
sozinho nunca separou os dois.

O que continua fora: `ctr` e `impressoes` (as linhas existem mas vem zeradas),
`inscritos_ganhos` e `receita_estimada_usd` (canal nenhum esta no YPP).
Decidir com coluna que ninguem mediu seria repetir o defeito que o `models.py`
registrou em 13/08: "o painel inteiro parecia dado e era default".

## Por que isto muda producao e nao e so relatorio

`v_maquina_licoes.veredito_longo` nao descreve, decide:

    suspenso    o short entrega e o longo nao paga o proprio render. Um longo
                custa ~20x um short (80 cenas contra 6), entao cada longo aqui
                queima a vaga de vinte shorts que funcionariam.
    canal frio  NENHUM dos dois entrega e o canal nunca teve pico. O problema
                nao e formato, e gancho ou nicho — trocar de formato responde a
                pergunta errada.
    liberado    o longo entrega o bastante para se pagar.
    sem dado    menos de 3 videos com 48h+ no formato.

O veredito entra no prompt do `autor.py`, entao ele muda o roteiro seguinte.
E o `painel` entra na rotina horaria, para a decisao humana ver o mesmo numero.

Uso:
    python3 fabrica/aprendizado.py painel            # a frota inteira
    python3 fabrica/aprendizado.py memoria <slug>    # o bloco que vai ao prompt
    python3 fabrica/aprendizado.py fechar            # fecha experimentos maduros
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

# Idade minima para um video contar. E a mesma regra que a rotina aplica para
# nao concluir desempenho cedo demais, e ela existe porque o contador do
# YouTube atualiza em lote — medir antes disso mede o lote, nao o video
# (aprendizado 360).
IDADE_MINIMA_H = 48


def _sb(caminho: str, sb_url: str, sb_key: str):
    import publicar as P

    r = P._req(f"{sb_url}/rest/v1/{caminho}",
               headers={"Authorization": f"Bearer {sb_key}", "apikey": sb_key})
    return json.load(r)


def licoes(sb_url: str, sb_key: str, slug: str = "") -> list[dict]:
    q = {"select": "*", "order": "views_total.desc"}
    if slug:
        q["canal"] = f"eq.{slug}"
    return _sb(f"v_maquina_licoes?{urllib.parse.urlencode(q)}", sb_url, sb_key)


def desempenho(sb_url: str, sb_key: str, slug: str = "") -> list[dict]:
    q = {"select": "*"}
    if slug:
        q["canal"] = f"eq.{slug}"
    return _sb(f"v_maquina_desempenho?{urllib.parse.urlencode(q)}", sb_url, sb_key)


def melhores(sb_url: str, sb_key: str, slug: str, n: int = 5) -> list[dict]:
    """Os videos do canal com mais views, com idade — a materia-prima do "o que
    funcionou aqui". Titulo e formato, que e o que o gerador consegue imitar."""
    q = {"select": "titulo,formato,youtube_id,publicado_em",
         "canal": f"eq.{slug}", "youtube_id": "not.is.null",
         "order": "publicado_em.desc", "limit": "40"}
    vids = _sb(f"videos?{urllib.parse.urlencode(q)}", sb_url, sb_key)
    if not vids:
        return []
    ids = ",".join(v["youtube_id"] for v in vids)
    m = _sb("v_ultima_metrica?" + urllib.parse.urlencode(
        {"select": "youtube_id,views", "youtube_id": f"in.({ids})"}), sb_url, sb_key)
    views = {x["youtube_id"]: x["views"] for x in m}

    import datetime as dt

    agora = dt.datetime.now(dt.timezone.utc)
    saida = []
    for v in vids:
        pub = v.get("publicado_em")
        if not pub:
            continue
        quando = dt.datetime.fromisoformat(pub.replace("Z", "+00:00"))
        idade_h = (agora - quando).total_seconds() / 3600
        if idade_h < IDADE_MINIMA_H:
            continue
        vw = views.get(v["youtube_id"], 0) or 0
        saida.append({**v, "views": vw, "idade_d": idade_h / 24,
                      "vd": vw / max(idade_h / 24, 1)})
    saida.sort(key=lambda x: -x["vd"])
    return saida[:n]


ACAO = {
    "suspenso": ("O LONGO DESTE CANAL NAO SE PAGA. O short entrega e o longo "
                 "nao. Escreva o longo no PISO da faixa (mais perto de 8 min "
                 "que de 15) e ponha o seu melhor material no SHORT — e ele "
                 "que este canal ja provou que entrega."),
    "canal frio": ("NENHUM DOS DOIS FORMATOS ENTREGOU AINDA, e o canal nunca "
                   "teve um pico. O problema nao e o formato: e o gancho, o "
                   "titulo ou o nicho. Nao repita o angulo do que ja foi ao "
                   "ar aqui — ele foi medido e nao pegou. Arrisque um eixo "
                   "novo."),
    "liberado": ("O longo deste canal se paga. Pode usar a faixa inteira de "
                 "12 a 15 minutos."),
    "sem dado": ("Ainda nao ha video suficiente com 48h de vida para este "
                 "canal provar nada. Siga a memoria do NICHO."),
}


def memoria(sb_url: str, sb_key: str, slug: str) -> str:
    """O bloco de texto que entra no prompt do gerador.

    Ele diz tres coisas, nessa ordem: o veredito (que muda o que escrever), os
    numeros que o sustentam, e os titulos que de fato performaram no canal.
    Titulo real do proprio canal vale mais que qualquer descricao de formato —
    e o unico exemplo que ja passou pelo publico deste canal especifico.
    """
    ls = licoes(sb_url, sb_key, slug)
    if not ls:
        return ""
    lc = ls[0]
    v = lc.get("veredito_longo") or "sem dado"

    linhas = [f"MEMORIA DO PROPRIO CANAL — o que os videos ja publicados aqui "
              f"provaram (views/dia, so videos com {IDADE_MINIMA_H}h+ de vida):",
              ""]
    if lc.get("short_vd_mediana") is not None:
        linhas.append(f"  short: mediana {lc['short_vd_mediana']} v/d, topo "
                      f"{lc['short_vd_topo']} v/d, em {lc['shorts_medidos']} medidos")
    if lc.get("longo_vd_mediana") is not None:
        linhas.append(f"  longo: mediana {lc['longo_vd_mediana']} v/d, em "
                      f"{lc['longos_medidos']} medidos")

    # Retencao so aparece quando foi medida, e sempre acompanhada de quantos
    # videos a sustentam. Numero sem n vira certeza falsa no prompt: uma
    # mediana de um video unico le-se igual a uma de trinta.
    # Retencao e o acessorio, o veredito e o principal. Se a consulta de
    # desempenho cair, a memoria segue sem ela — perder o bloco inteiro porque
    # uma query secundaria falhou seria trocar o essencial pelo ornamento.
    try:
        com_ret = [d for d in desempenho(sb_url, sb_key, slug) if d.get("ret_n")]
    except Exception:
        com_ret = []
    for d in com_ret:
        linhas.append(
            f"  {d['formato']}: retencao mediana {d['ret_mediana_pct']}% "
            f"({d['ret_dur_mediana_s']} s assistidos), em {d['ret_n']} "
            f"medido(s) — poucos, trate como indicio e nao como lei")
    linhas += ["", f"VEREDITO: {v.upper()}. {ACAO.get(v, '')}", ""]
    if com_ret:
        linhas += ["COMO LER A RETENCAO: ela separa dois problemas que views "
                   "sozinho confunde. Views baixo COM retencao alta e "
                   "distribuicao — o titulo e a thumb nao fazem clicar, o "
                   "roteiro esta bom. Views baixo COM retencao baixa e "
                   "roteiro — quem entrou saiu. Acima de 100% o video foi "
                   "reassistido, que e o sinal mais forte que existe em "
                   "short.", ""]

    tops = melhores(sb_url, sb_key, slug, 5)
    if tops:
        linhas.append("O QUE MAIS ENTREGOU NESTE CANAL, em views/dia:")
        for t in tops:
            linhas.append(f"  {t['vd']:7.1f} v/d  [{t['formato']}] {t['titulo']}")
        linhas.append("")
        linhas.append("Estes titulos ja passaram pelo publico DESTE canal. Eles "
                      "valem mais que qualquer descricao de formato — leia o que "
                      "eles tem em comum antes de escrever o proximo.")
    return "\n".join(linhas)


def painel(sb_url: str, sb_key: str) -> str:
    ls = licoes(sb_url, sb_key)
    ordem = {"suspenso": 0, "canal frio": 1, "liberado": 2, "sem dado": 3}
    ls.sort(key=lambda x: (ordem.get(x.get("veredito_longo"), 9),
                           -(x.get("views_total") or 0)))
    larg = max((len(x["canal"]) for x in ls), default=10)
    out = [f"{'canal':<{larg}}  {'short v/d':>10}  {'longo v/d':>10}  "
           f"{'views':>7}  veredito",
           "-" * (larg + 46)]
    for x in ls:
        s = x.get("short_vd_mediana")
        l = x.get("longo_vd_mediana")
        out.append(f"{x['canal']:<{larg}}  {(s if s is not None else '-'):>10}  "
                   f"{(l if l is not None else '-'):>10}  "
                   f"{x.get('views_total') or 0:>7}  {x.get('veredito_longo')}")
    susp = [x["canal"] for x in ls if x.get("veredito_longo") == "suspenso"]
    frio = [x["canal"] for x in ls if x.get("veredito_longo") == "canal frio"]
    out.append("")
    if susp:
        out.append(f"LONGO SUSPENSO em {len(susp)}: {', '.join(susp)} — o short "
                   f"entrega e o longo nao paga o render.")
    if frio:
        out.append(f"CANAL FRIO em {len(frio)}: {', '.join(frio)} — nenhum dos "
                   f"dois formatos pegou; o que falta e gancho, nao formato.")
    return "\n".join(out)


def fechar_experimentos(sb_url: str, sb_key: str) -> list[str]:
    """Experimento que nunca fecha e um palpite que virou habito.

    A rotina grava hipotese em `experimentos` a cada disparo e nada nunca as
    fecha. Isto nao DECIDE o resultado — decidir pede leitura — mas marca as
    que ja tem dado maduro, para que a decisao aconteca em vez de a lista
    crescer para sempre.
    """
    import datetime as dt

    abertos = _sb("experimentos?" + urllib.parse.urlencode(
        {"select": "id,slug,canal,variavel,criado_em", "status": "eq.aberto"}),
        sb_url, sb_key)
    agora = dt.datetime.now(dt.timezone.utc)
    maduros = []
    for e in abertos:
        criado = dt.datetime.fromisoformat(e["criado_em"].replace("Z", "+00:00"))
        if (agora - criado).total_seconds() / 3600 >= IDADE_MINIMA_H:
            maduros.append(f"#{e['id']} {e['canal']}/{e['slug']}: {e['variavel']}")
    return maduros


def main() -> int:
    sb_url = os.getenv("SUPABASE_URL", "")
    sb_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not (sb_url and sb_key):
        print("exporte SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY")
        return 2
    cmd = sys.argv[1] if len(sys.argv) > 1 else "painel"

    if cmd == "painel":
        print(painel(sb_url, sb_key))
        maduros = fechar_experimentos(sb_url, sb_key)
        if maduros:
            print(f"\n{len(maduros)} experimento(s) com dado maduro esperando "
                  f"leitura:")
            for m in maduros:
                print(f"  {m}")
        return 0

    if cmd == "memoria":
        if len(sys.argv) < 3:
            print("uso: aprendizado.py memoria <slug>")
            return 2
        txt = memoria(sb_url, sb_key, sys.argv[2])
        print(txt or f"(sem licao para {sys.argv[2]})")
        return 0

    if cmd == "fechar":
        for m in fechar_experimentos(sb_url, sb_key):
            print(m)
        return 0

    print(f"comando desconhecido: {cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
