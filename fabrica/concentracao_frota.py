#!/usr/bin/env python3
"""Quanto a producao esta CONCENTRADA num canal so — um nivel acima do
`concentracao.py`, e ele existe porque eu reproduzi o habito que o outro
consertou.

POR QUE ISTO EXISTE, medido em 14/10/2026 as 16:1x (aprendizado 762). O
`concentracao.py` nasceu em 13/10 porque eu minerava UM longo por rodada dentro
de um canal. Ele conta origem DENTRO do canal — e e CEGO para o nivel de cima.
Medido no banco: das pecas publicadas em 14/10, **DEZESSEIS de dezesseis sairam
no `labtreinamento`**, todas `shorts`, de 00:12 a 15:12, e **zero** no
`epomeno-epipedo` e no `kolejny-poziom`. Eu construi o contador do meu habito e
repeti o mesmo habito uma camada acima, pela mesma razao: era o canal que estava
aberto na minha cabeca.

**E O QUE AGRAVA E A MEDICAO DO 713**, que e nossa e e por PECA (maximo por peca,
nao soma de linha de metrica):

    epomeno LONGO   0,33 inscrito/peca   <- o melhor par medido
    epomeno short   0,14
    kolejny short   0,09
    kolejny longo   0,08
    labtreinamento short  0,07           <- o pior par com numero
    labtreinamento longo  0,00

Logo as dezesseis pecas do dia sairam no par **penultimo da lista**, e nenhuma
no primeiro. **Isto NAO prova que produzir no epomeno renderia mais** — o 693
diz que views/peca e cego abaixo do dobro, e a amostra do 713 e de 161 pecas
para 19 inscritos. O que ele prova e que **a escolha de canal nao foi feita por
medicao nenhuma**: ela foi habito, e o instrumento que eu tinha nao podia
acusa-la.

**O QUE ESTE MODULO NAO AFIRMA, e a ressalva e grande:** que concentrar seja
errado. O `CLAUDE.md` tem a conta oposta escrita e ela segue valida — os 500
inscritos sao limite POR CANAL, logo **concentracao vence dispersao**, e o alvo
realista escrito la pede "ritmo de 5 a 7 pecas/dia CONCENTRADAS num canal".
Concentrar e o PLANO. O que o plano nao diz e **em QUAL canal**, e e exatamente
essa escolha que este contador torna visivel.

**E ELE TEVE UM BURACO NA PRIMEIRA EXECUCAO, achado por ela mesma.** A contagem
sai das SPECS, que nao tem data, logo ela mede o ACERVO: 50 / 25 / 22, que esta
DENTRO do dobro (50 nao e maior que 50) e portanto **nao alerta**. O DIA, lido de
`videos.publicado_em`, era 16 / 0 / 0. **Acervo dilui rodada**, e um contador que
so ve acervo nunca acusaria o dia — o mesmo tipo de cegueira que ele nasceu para
consertar, uma camada acima. Por isso o `relato` aceita `por_dia=` e aplica o
MESMO limiar aos dois niveis; sem esse argumento ele DIZ que esta lendo acervo em
vez de calar.

Ele conta e relata. NAO escolhe canal, NAO reprova, e NAO mexe em parametro.
"""
from __future__ import annotations

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import concentracao  # noqa: E402

# Os tres canais da frota, decisao do dono em 07/10/2026.
FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")

# Inscrito por PECA medido no 713, com `max` por peca sobre as 161 pecas que
# tem metrica. NAO e previsao: e o que foi observado, e o 693 diz que ele nao
# distingue efeito menor que o dobro. Fica aqui para o relato poder dizer em que
# par a producao do dia caiu, sem eu recalcular de cabeca.
POR_PECA_713 = {
    ("epomeno-epipedo", "longo"): 0.33,
    ("epomeno-epipedo", "shorts"): 0.14,
    ("kolejny-poziom", "shorts"): 0.09,
    ("kolejny-poziom", "longo"): 0.08,
    ("labtreinamento", "shorts"): 0.07,
    ("labtreinamento", "longo"): 0.00,
}


def contagem(raiz: str = None) -> dict[str, int]:
    """Shorts por canal da frota, lidos das specs (a mesma fonte do irmao)."""
    return {c: sum(concentracao.contagem(c, raiz).values()) for c in FROTA}


def analise(contagens: dict[str, int]) -> dict:
    """Quem domina, por quanto, e se passa do DOBRO do segundo.

    O limiar e o MESMO do `concentracao.py` — mais que o dobro do segundo — e ele
    e observado, nao derivado. Reusar o limiar e deliberado: se eu inventasse um
    numero novo aqui, seria criterio sem procedencia (a trava da §10).
    """
    vivos = {c: n for c, n in contagens.items() if n > 0}
    if not vivos:
        return {"dominante": None, "n_dominante": 0, "n_segunda": 0,
                "alerta": False, "zerados": list(contagens), "total": 0}
    ordem = sorted(vivos.items(), key=lambda kv: -kv[1])
    dom, n_dom = ordem[0]
    n_seg = ordem[1][1] if len(ordem) > 1 else 0
    return {
        "dominante": dom,
        "n_dominante": n_dom,
        "n_segunda": n_seg,
        "alerta": n_dom > 2 * n_seg,
        "zerados": [c for c, n in contagens.items() if n == 0],
        "total": sum(contagens.values()),
        "ordem": ordem,
    }


def par_do_dia(canal: str, formato: str) -> float | None:
    """O inscrito/peca MEDIDO do par (713), ou None se o par nao foi medido."""
    return POR_PECA_713.get((canal, formato))


def ranking_713() -> list[tuple[tuple[str, str], float]]:
    """Os pares do 713 do melhor para o pior."""
    return sorted(POR_PECA_713.items(), key=lambda kv: -kv[1])


def mais_baixo(contagem_: dict[str, int], ultima: dict = None):
    """O canal mais baixo da contagem, e a lista dos EMPATADOS com ele.

    MEDIDO em 15/10 as 04:0x, e e uma divergencia doc<->codigo do MEU proprio
    modulo: o comentario da regra dos dois niveis dizia, desde as 02:0x, que
    "empate na janela se desfaz pela peca mais ANTIGA" — e o codigo desfazia
    por `(contagem, c)`, isto e, pelo ALFABETO. A janela desta rodada veio
    6 / 6 empatada entre `epomeno-epipedo` e `kolejny-poziom`, e o modulo
    devolveu o epomeno por ele vir antes na ordem alfabetica, chamando isso de
    "o mais baixo". **Ordem alfabetica nao e critério medido**, e criterio sem
    procedencia e exatamente o que a §10 proibe.

    Agora o empate vai DITO, e so se desfaz com `ultima=` (o
    `max(publicado_em)` por canal), que e medido: vence o canal cuja ultima
    peca e a mais ANTIGA. Sem `ultima=` a funcao NAO escolhe — devolve os
    empatados para quem chama dizer que nao decidiu.
    """
    piso = min(contagem_.get(c, 0) for c in FROTA)
    empatados = sorted(c for c in FROTA if contagem_.get(c, 0) == piso)
    if len(empatados) == 1:
        return empatados[0], empatados
    if ultima:
        faltam = [c for c in empatados if ultima.get(c) is None]
        if not faltam:
            return min(empatados, key=lambda c: ultima[c]), empatados
    return None, empatados


def relato(raiz: str = None, por_dia: dict[str, int] = None,
           janela: dict[str, int] = None, janela_h: int = 24,
           ultima: dict = None) -> str:
    ct = contagem(raiz)
    a = analise(ct)
    linhas = [f"FROTA: {a['total']} shorts sobre {len(FROTA)} canais."]
    linhas.append("  " + ", ".join(f"{c} {n}" for c, n in a["ordem"]))
    if a["alerta"]:
        linhas.append(f"  ALERTA: {a['dominante']} com {a['n_dominante']} e MAIS "
                      f"que o dobro do segundo ({a['n_segunda']}).")
    else:
        linhas.append(f"  dentro do dobro: {a['dominante']} com "
                      f"{a['n_dominante']} contra {a['n_segunda']} do segundo.")
    if a["zerados"]:
        linhas.append("  canal da frota SEM nenhum short: " + ", ".join(a["zerados"]))
    melhor, pior = ranking_713()[0], ranking_713()[-1]
    linhas.append(f"  par medido no 713: melhor {melhor[0][0]}/{melhor[0][1]} "
                  f"({melhor[1]:.2f} inscrito/peca), pior {pior[0][0]}/{pior[0][1]} "
                  f"({pior[1]:.2f}).")
    if por_dia is None:
        linhas.append("  ACERVO NAO E O DIA: esta contagem le as specs, que nao tem "
                      "data. A do dia sai de `videos.publicado_em` e passa aqui em "
                      "`por_dia=` — sem ela o acervo DILUI a rodada.")
    elif sum(por_dia.get(c, 0) for c in FROTA) == 0:
        # 15/10 as 00:0x: o DIA CALENDARIO zera a meia-noite, e nas primeiras horas
        # ele devolve 0/0/0 — nao ordena NADA, justamente quando a rodada precisa
        # escolher. E a cegueira simetrica da que este contador nasceu para
        # consertar: acervo DILUI a rodada, e dia calendario recem-comecado APAGA
        # as ultimas horas. A saida e a JANELA MOVEL.
        linhas.append("  O DIA CALENDARIO ESTA EM ZERO nos tres canais: ele nao "
                      "ordena nada nas primeiras horas do dia. Passe `janela=` "
                      f"com as pecas das ultimas {janela_h} h.")
    else:
        b = analise({c: por_dia.get(c, 0) for c in FROTA})
        linhas.append(f"  NO DIA: {b['total']} pecas — "
                      + ", ".join(f"{c} {n}" for c, n in b["ordem"]))
        if b["alerta"] and b["total"] < len(FROTA):
            # 15/10 01:0x: com UMA peca no dia o relato gritou "ALERTA DO DIA:
            # epomeno 1 contra 0". Isso e artefato do TOTAL, nao concentracao:
            # com menos pecas que canais a distribuicao uniforme e IMPOSSIVEL, e
            # a peca tem de cair em algum canal. E aritmetica, nao limiar novo —
            # o limiar segue o do irmao.
            linhas.append(f"  o dia tem {b['total']} peca(s) para {len(FROTA)} "
                          "canais, logo distribuicao uniforme e IMPOSSIVEL e o "
                          "alerta seria artefato do total — nao alerto, e digo "
                          "por que. Use a janela movel.")
        elif b["alerta"]:
            linhas.append(f"  ALERTA DO DIA: {b['dominante']} com "
                          f"{b['n_dominante']} contra {b['n_segunda']} do segundo.")
        if b["zerados"]:
            linhas.append("  SEM NENHUMA PECA HOJE: " + ", ".join(b["zerados"]))
    if janela is not None:
        j = analise({c: janela.get(c, 0) for c in FROTA})
        linhas.append(f"  NAS ULTIMAS {janela_h} H: {j['total']} pecas — "
                      + ", ".join(f"{c} {n}" for c, n in j["ordem"]))
        if j["alerta"]:
            linhas.append(f"  ALERTA DA JANELA: {j['dominante']} com "
                          f"{j['n_dominante']} contra {j['n_segunda']} do segundo.")
        if j["zerados"]:
            linhas.append(f"  SEM NENHUMA PECA NAS ULTIMAS {janela_h} H: "
                          + ", ".join(j["zerados"]))
    if por_dia is not None and janela is not None:
        # 15/10 02:0x: os dois niveis apontaram canais DIFERENTES como o mais
        # baixo — a janela de 24 h acusava `labtreinamento` com 14 contra 5
        # (porque as 16 pecas de ontem ainda estao dentro dela) enquanto o DIA
        # tinha o mesmo canal em ZERO. Nenhum dos dois esta errado: eles
        # respondem perguntas diferentes, e eu estava desempatando isso a mao.
        #
        # A REGRA, com procedencia: quem governa a ESCOLHA e a JANELA, porque
        # este contador nasceu (762) pelo portao do conteudo INAUTENTICO, que e
        # sobre acumulo RECENTE no canal. O DIA entra no relato porque o alvo do
        # dono e 7/dia POR CANAL, logo ele diz quem esta ATRASADO — que e outra
        # pergunta. Empate na janela se desfaz pela peca mais ANTIGA.
        # CUIDADO MEDIDO AQUI: `analise()["ordem"]` OMITE canal com zero (eles
        # saem em `zerados`), logo ler o ultimo da `ordem` NAO da o mais baixo —
        # na primeira versao desta linha o canal em ZERO ficava invisivel e a
        # discordancia nao era detectada. O minimo tem de varrer a FROTA toda.
        dia_baixo, dia_emp = mais_baixo({c: por_dia.get(c, 0) for c in FROTA})
        jan_baixo, jan_emp = mais_baixo(
            {c: janela.get(c, 0) for c in FROTA}, ultima)
        if jan_baixo is None:
            linhas.append(
                "  A JANELA EMPATOU no mais baixo entre "
                + ", ".join(jan_emp)
                + ". ORDEM ALFABETICA NAO DESEMPATA — era o que este modulo "
                "fazia, e e criterio sem procedencia. Passe `ultima=` com o "
                "`max(publicado_em)` por canal: vence o de peca mais ANTIGA.")
        elif len(jan_emp) > 1:
            linhas.append(
                "  A JANELA EMPATOU entre " + ", ".join(jan_emp)
                + f", e o desempate foi MEDIDO: {jan_baixo} tem a peca mais "
                "ANTIGA (`max(publicado_em)`), nao a primeira do alfabeto.")
        if jan_baixo is not None and dia_baixo is not None \
                and dia_baixo != jan_baixo:
            linhas.append(
                f"  OS DOIS NIVEIS DISCORDAM: o mais baixo do dia e {dia_baixo} "
                f"e o da janela e {jan_baixo}. Quem governa a ESCOLHA e a "
                "JANELA (este contador existe pelo conteudo INAUTENTICO, que e "
                "acumulo RECENTE); o DIA diz quem esta ATRASADO nos 7/dia por "
                "canal, que e outra pergunta.")
    linhas.append("  (CONTA, nao reprova: concentrar e o PLANO, porque os 500 sao "
                  "limite POR CANAL. O que este contador mostra e EM QUAL canal, "
                  "e essa escolha tem de ser medida, nao habito.)")
    return "\n".join(linhas)


def main(argv: list[str]) -> int:
    print(relato())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


# ---------------------------------------------------------------------------
# A FONTE DO `ultima=` QUANDO O BANCO ESTA FORA — medido em 16/10 as 14:2x
# ---------------------------------------------------------------------------
#
# O `mais_baixo` aceita `ultima=` (o `max(publicado_em)` por canal) e sem ele
# RECUSA desempatar, de proposito. Mas enquanto o `execute_sql` esta negado —
# setima rodada seguida hoje — esse argumento **nao tinha fonte nenhuma**, e o
# resultado pratico foi que eu desempatei A MAO.
#
# E O QUE EU USEI NAO FOI O CRITERIO DESTE MODULO. Com o dia em 5/5/5 eu
# escolhi o canal pela tabela do 713 (par com melhor inscrito/peca), que vive em
# `POR_PECA_713` e em prosa no `CLAUDE.md`. O modulo tem essa tabela e
# **deliberadamente nao a usa para desempate** — ele usa a peca mais ANTIGA,
# que e medida e nao depende de uma amostra de 161 pecas para 19 inscritos.
#
# OS DOIS CRITERIOS CONCORDARAM nesta rodada (os dois devolvem
# `epomeno-epipedo`), e isso NAO e evidencia de que algum dos dois esteja certo:
# e uma coincidencia de uma rodada. O que fica errado e eu nao ter dito QUAL
# critério estava usando — escolher entre dois criterios sem declarar qual e o
# efeito (C) da rotina, comparador escolhido sem medir.
#
# A fonte que existe sem banco e o PENDENTE: cada linha parqueada em
# `docs/pendente/videos-a-inserir.sql` tem canal e `publicado_em`, porque o
# `registro_videos` os escreve. Logo o `ultima=` deixa de ser argumento sem
# origem.

PENDENTE = "docs/pendente/videos-a-inserir.sql"


def ultima_do_pendente(caminho: str = None) -> dict[str, str]:
    """`max(publicado_em)` por canal, lido das linhas PARQUEADAS.

    E um PISO, nao a verdade: ele so conhece as publicacoes que passaram pelo
    `registro_videos` desde que o parqueamento comecou. Peca publicada antes
    disso nao aparece, e por isso um canal AUSENTE do resultado nao vale como
    "nunca publicou" — vale como "nao sei", e o `mais_baixo` ja trata ausencia
    recusando o desempate em vez de inventar.
    """
    import os
    import re

    if caminho is None:
        caminho = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), PENDENTE)
    fora: dict[str, str] = {}
    if not os.path.exists(caminho):
        return fora
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            canal = next((c for c in FROTA if f"'{c}'" in linha), None)
            if not canal:
                continue
            datas = re.findall(r"'(20\d\d-\d\d-\d\dT[\d:]+Z)'", linha)
            if not datas:
                continue
            if canal not in fora or datas[-1] > fora[canal]:
                fora[canal] = datas[-1]
    return fora


def contagem_do_pendente(desde: str, caminho: str = None) -> dict[str, int]:
    """Quantas pecas por canal com `publicado_em >= desde`, nas linhas PARQUEADAS.

    Ele existe porque eu vinha contando o DIA com um regex escrito a mao na
    linha de comando, a cada rodada — e a §10 da rotina diz, no item 3, que todo
    numero que eu calculo a mao vira um erro meu mais cedo ou mais tarde. A
    contagem decide QUAL CANAL produz, logo e exatamente o tipo de numero que
    nao deve morar num `awk` descartavel.

    `desde` e um prefixo ou um instante ISO em UTC: `"2026-10-16"` conta o dia
    calendario, e `"2026-10-15T19:00:00Z"` conta a janela movel de 24 h do 771 —
    **a janela movel e a que ordena na virada da meia-noite**, e por isso o
    argumento aceita as duas formas em vez de so a data.

    Herda o aviso do irmao acima: e um PISO. Canal que nao aparece sai com
    ZERO, e zero aqui significa "nenhuma linha PARQUEADA", nao "nao publicou" —
    quem for desempatar com isso usa o `mais_baixo`, que recusa em vez de
    inventar. A comparacao e lexicografica, o que vale para ISO em UTC com o
    mesmo numero de digitos; nao passe data com fuso.
    """
    import os
    import re

    if not desde or not str(desde).startswith("20"):
        raise ValueError(
            f"`desde` tem de ser data ou instante ISO em UTC, veio {desde!r}")
    if caminho is None:
        caminho = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), PENDENTE)
    fora: dict[str, int] = {c: 0 for c in FROTA}
    if not os.path.exists(caminho):
        return fora
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            canal = next((c for c in FROTA if f"'{c}'" in linha), None)
            if not canal:
                continue
            datas = re.findall(r"'(20\d\d-\d\d-\d\dT[\d:]+Z)'", linha)
            if datas and datas[-1] >= desde:
                fora[canal] += 1
    return fora


def escolha_do_momento(janela_h: float = 24.0, caminho: str = None,
                       agora=None) -> dict:
    """A contagem da janela movel E a escolha, do MESMO instante.

    MEDIDO em 17/10 as 01:1x, e o defeito e de PROCESSO meu, nao do modulo.
    As 01:09 eu li a janela de 24 h em **8 / 8 / 9** e escolhi
    `labtreinamento` pelo desempate do `mais_baixo` (empate em 8, vence a
    peca mais ANTIGA — 22:13). As 01:13, quatro minutos depois, a MESMA
    janela deu **7 / 8 / 9**: a peca de 16/10 ~01:1x caiu fora do corte, e
    `labtreinamento` passou a ser minimo ABSOLUTO, sem empate nenhum.

    **A escolha nao mudou; a RAZAO mudou** — e eu relatei ao dono um
    desempate que, quatro minutos depois, nao existia. Com a frota
    publicando de hora em hora, a janela de 24 h perde ~1 peca por canal
    por hora, logo a contagem e funcao do MINUTO em que a pergunta e feita.
    Ler a contagem numa chamada e decidir noutra e a mesma assinatura do
    760 (a idade sai do `now()` da MESMA chamada), aqui na contagem.

    Esta funcao fixa `agora` UMA vez e devolve, juntos: o instante, o corte,
    a contagem, a ultima peca por canal, o escolhido e os empatados. Quem
    relata cita estes numeros, nao os de uma leitura anterior.

    `agora` existe para teste; em producao fica None e vale o `now()` real.
    """
    from datetime import datetime, timedelta, timezone
    if agora is None:
        agora = datetime.now(timezone.utc)
    corte = agora - timedelta(hours=janela_h)
    cont = contagem_do_pendente(corte.isoformat(), caminho)
    ult = ultima_do_pendente(caminho)
    escolhido, empatados = mais_baixo(cont, ult)
    return {
        "agora": agora.isoformat(),
        "corte": corte.isoformat(),
        "janela_h": janela_h,
        "contagem": cont,
        "ultima": ult,
        "escolhido": escolhido,
        "empatados": empatados,
        "houve_empate": len(empatados) > 1,
    }
