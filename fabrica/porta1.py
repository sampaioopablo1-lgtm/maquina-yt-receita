#!/usr/bin/env python3
"""Quanto falta para a Porta 1 do YPP, e QUANDO — com a conta fora da minha cabeca.

POR QUE ISTO EXISTE. Pedido do dono em 12/10/2026, com estas palavras:
*"informe quadro dos resultados atuais projecao e tendencia, de quando o canal
ira monetizar, e o que e preciso para isso acontecer ate fim de outubro,
mudancas que precisam ser feitas para ter mais resultados. Em cada rodada da
rotina este questionamento precisa ser feito, e ajustado o processo."*

Eu vinha respondendo isso de cabeca, e todo numero que eu calculo de cabeca vira
um erro meu mais cedo ou mais tarde — foi assim com os 652/655, 658, 682, 685,
com os "~1,9 s por cena" e com os "3,7 GB de Storage". Entao a conta mora aqui,
recebe leitura medida e devolve o quadro. Se o quadro doer, o remedio e mudar o
mundo, nao a conta.

O QUE ESTE MODULO NAO FAZ: nao estima view, nao inventa taxa de conversao e nao
projeta crescimento exponencial. Ele faz aritmetica linear sobre DUAS leituras
de inscritos separadas por >= 4 h (regra H, aprendizado 686) e diz, sem adoçar,
quantos dias faltam no ritmo observado. Ritmo linear e otimista para um canal
que acelera e pessimista para um que satura; os dois casos vao DITOS no relato.
"""
from __future__ import annotations

import datetime as dt
import json
import sys

# PORTA 1, e a barra SOBE em 1/FEV/2027 (1.000 inscritos). Quem projeta para
# depois dessa data tem de projetar contra a barra nova, nao contra esta.
PORTA1_INSCRITOS = 500
PORTA2_INSCRITOS = 1000
BARRA_SOBE_EM = dt.date(2027, 2, 1)
INSCRITOS_APOS_A_BARRA_SUBIR = 1000

# Minimo entre leituras de contador DE CANAL. Abaixo disso o degrau do 686/703
# devolve o mesmo byte e o delta e ruido, nao crescimento.
HORAS_MINIMAS = 4.0


class LeituraCurta(Exception):
    """Duas leituras perto demais nao medem crescimento de canal (686)."""


def piso_de_resolucao(horas: float) -> float:
    """O MENOR ritmo/dia que um contador INTEIRO consegue expressar nesta janela.

    MEDIDO em 12/10/2026 as 18:1x, e e um defeito meu que quase foi ao relato.
    As >= 4 h da regra H (686) bastam para pular o DEGRAU da replica, e eu tratei
    isso como se bastasse para medir RITMO. Nao basta, e a conta e de uma linha:
    o contador anda de um em um, entao numa janela de `horas` o menor ritmo
    diferente de zero que ele consegue mostrar e `24/horas` por dia.

    Numa janela de 4 h isso da SEIS inscritos por dia. O ritmo medido da frota
    inteira e ~1,8/dia. Logo uma janela de 4 h nao distingue "1,8/dia" de
    "zero" — ela devolve delta zero nos dois casos, e `dias_para` transforma
    esse zero em "nunca". **"Nunca" lido de janela curta nao e resultado, e
    falsa precisao**, do mesmo tipo do portao verde do paragrafo 3.8.

    Por isso a leitura de 40,3 h funcionou e esta de 3,7 h nao funcionaria: a
    40,3 h o piso e 0,6/dia, abaixo do ritmo real; a 4 h ele esta tres vezes
    ACIMA dele.
    """
    if horas <= 0:
        raise LeituraCurta("janela de zero hora nao resolve ritmo nenhum")
    return 24.0 / horas


def horas_para_resolver(por_dia: float, contagens: int = 1) -> float | None:
    """Janela necessaria para o contador inteiro mostrar `contagens` mudancas.

    A inversa do piso. Com o ritmo medido de 0,60/dia do labtreinamento, UMA
    contagem pede 40 h — que e exatamente a janela em que o quadro de 12/10 foi
    medido, e nao por sorte.
    """
    if por_dia <= 0:
        return None
    return contagens * 24.0 / por_dia


def dias_para(alvo: int, agora: int, por_dia: float) -> float | None:
    """Dias no ritmo observado. None quando o ritmo nao leva a lugar nenhum."""
    falta = alvo - agora
    if falta <= 0:
        return 0.0
    if por_dia <= 0:
        return None
    return falta / por_dia


def ritmo(antes: int, agora: int, horas: float) -> float:
    """Inscritos por dia entre duas leituras. Levanta se a janela e curta."""
    if horas < HORAS_MINIMAS:
        raise LeituraCurta(
            f"{horas:.1f} h entre leituras, e o minimo e {HORAS_MINIMAS}. "
            "O contador de canal anda em DEGRAU (686/703): duas leituras "
            "proximas devolvem o mesmo byte e o delta nao e crescimento."
        )
    return (agora - antes) * 24.0 / horas


def alvo_na_data(data: dt.date) -> int:
    """A barra que vale NAQUELA data, nao a de hoje."""
    return INSCRITOS_APOS_A_BARRA_SUBIR if data >= BARRA_SOBE_EM else PORTA1_INSCRITOS


def quadro(canais: dict, horas: float, hoje: dt.date | None = None) -> dict:
    """`canais` = {nome: {'antes': int, 'agora': int}}. Devolve o quadro inteiro.

    `faltam_ate_fim_do_mes` responde literalmente a pergunta do dono: quantos
    inscritos o canal TERA no fim do mes no ritmo observado, e qual fracao da
    Porta 1 isso representa. A resposta pode ser humilhante; e para ser.
    """
    hoje = hoje or dt.date.today()
    fim_do_mes = dt.date(hoje.year + (hoje.month == 12),
                         1 if hoje.month == 12 else hoje.month + 1, 1) - dt.timedelta(days=1)
    dias_ate_fim = (fim_do_mes - hoje).days

    linhas = []
    for nome, v in canais.items():
        r = ritmo(v["antes"], v["agora"], horas)
        # Delta zero nao e ritmo zero, e UMA contagem nao e ritmo medido.
        #
        # CORRIGIDO EM 13/10/2026 as 09:1x, por uma leitura de producao, e e a
        # MESMA assimetria que eu ja havia corrigido para o kolejny em 12/10 --
        # so que do outro lado do sinal. O critério antigo era
        # `agora != antes`, isto é: delta ZERO nao resolve, mas delta de UMA
        # contagem resolve. Nao resolve: o piso da janela E uma contagem, logo
        # |ritmo| == piso e a incerteza e da ordem do proprio valor. Com isso o
        # labtreinamento lendo 68 -> 67 em 13,6 h saiu como "-1,76/dia, chega
        # NUNCA", quando o que a janela permite dizer e so "|ritmo| <= o piso".
        #
        # Eu ja tinha escrito exatamente este argumento no CLAUDE.md para o
        # +0,60/dia ("e UMA contagem, a incerteza e da ordem do valor") e nao o
        # apliquei ao codigo. Duas contagens sao o minimo para o ritmo sair do
        # piso, e vale nos dois sentidos.
        resolvido = abs(v["agora"] - v["antes"]) >= 2
        d = dias_para(PORTA1_INSCRITOS, v["agora"], r)
        no_fim = v["agora"] + r * dias_ate_fim
        data = (hoje + dt.timedelta(days=round(d))) if d is not None else None
        linhas.append({
            "canal": nome,
            "inscritos": v["agora"],
            "delta": v["agora"] - v["antes"],
            "por_dia": round(r, 2),
            "ritmo_resolvido": resolvido,
            "falta": PORTA1_INSCRITOS - v["agora"],
            "pct_da_porta1": round(100.0 * v["agora"] / PORTA1_INSCRITOS, 1),
            "dias_para_porta1": None if d is None else round(d),
            "data_porta1": None if data is None else data.isoformat(),
            # A barra que valera NA DATA da chegada — nao a de hoje.
            "alvo_que_vale_na_chegada": None if data is None else alvo_na_data(data),
            "chega_antes_da_barra_subir": None if data is None else data < BARRA_SOBE_EM,
            "inscritos_no_fim_do_mes": round(no_fim),
            "pct_no_fim_do_mes": round(100.0 * no_fim / PORTA1_INSCRITOS, 1),
        })
    linhas.sort(key=lambda x: -x["inscritos"])

    # Views necessarias para fechar no prazo, pela conversao MEDIDA. Isto e o
    # que transforma "faltam 432 inscritos" em "faltam N views por dia", que e
    # a forma em que a frase pode ser confrontada com a producao real.
    for l in linhas:
        if dias_ate_fim > 0 and l["falta"] > 0:
            for nome_taxa, taxa in (("a_1_2_por_mil", 1.2), ("a_5_por_mil", 5.0),
                                    ("a_20_por_mil", 20.0)):
                l[f"views_por_dia_para_fechar_no_mes_{nome_taxa}"] = round(
                    l["falta"] / taxa * 1000.0 / dias_ate_fim)

    return {
        "hoje": hoje.isoformat(),
        "fim_do_mes": fim_do_mes.isoformat(),
        "dias_ate_fim_do_mes": dias_ate_fim,
        "horas_entre_leituras": round(horas, 1),
        "piso_de_resolucao_por_dia": round(piso_de_resolucao(horas), 2),
        "barra_sobe_em": BARRA_SOBE_EM.isoformat(),
        "canais": linhas,
        "frota_por_dia": round(sum(l["por_dia"] for l in linhas), 2),
        "melhor_canal": linhas[0]["canal"] if linhas else None,
    }


def relato(q: dict) -> str:
    """O quadro em texto, e ele NAO adoça."""
    out = [f"PORTA 1 — 500 inscritos POR CANAL. Quadro de {q['hoje']}, "
           f"leituras separadas por {q['horas_entre_leituras']} h.",
           f"Faltam {q['dias_ate_fim_do_mes']} dias para {q['fim_do_mes']}.",
           ""]
    out.append(f"{'canal':18} {'insc':>5} {'delta':>6} {'/dia':>6} {'%P1':>6} "
               f"{'dias':>6} {'chega em':>12} {'no fim do mes':>14}")
    for l in q["canais"]:
        if not l["ritmo_resolvido"]:
            # Nao escreva "nunca" a partir de delta zero: a janela nao resolve.
            dias = "indet."
        elif l["dias_para_porta1"] is None:
            dias = "nunca"
        else:
            dias = str(l["dias_para_porta1"])
        data = ("—" if not l["ritmo_resolvido"] else (l["data_porta1"] or "—"))
        out.append(f"{l['canal']:18} {l['inscritos']:5d} {l['delta']:+6d} "
                   f"{l['por_dia']:6.2f} {l['pct_da_porta1']:5.1f}% {dias:>6} "
                   f"{data:>12} {l['inscritos_no_fim_do_mes']:6d} "
                   f"({l['pct_no_fim_do_mes']:.1f}%)")
    out.append("")
    out.append(f"frota inteira: {q['frota_por_dia']:+.2f} inscritos/dia")

    # A parte que responde "o que e preciso para acontecer ate fim do mes".
    nao_resolvidos = [l["canal"] for l in q["canais"] if not l["ritmo_resolvido"]]
    if nao_resolvidos:
        out.append("")
        out.append(f"RITMO NAO RESOLVIDO em {len(nao_resolvidos)} canal(is): "
                   + ", ".join(nao_resolvidos) + ".")
        out.append(f"  A janela de {q['horas_entre_leituras']} h tem piso de "
                   f"resolucao de {q['piso_de_resolucao_por_dia']:.2f} "
                   "inscritos/dia —")
        out.append("  o contador anda de um em um. Delta zero aqui significa "
                   "'ritmo abaixo")
        out.append("  desse piso', e NAO 'ritmo zero'. Esses canais saem como "
                   "indet., nao")
        out.append("  como 'nunca'.")

    out.append("")
    out.append("PARA FECHAR A PORTA 1 AINDA NESTE MES, por canal, em VIEWS/DIA:")
    for l in q["canais"]:
        k = "views_por_dia_para_fechar_no_mes_"
        if k + "a_1_2_por_mil" in l:
            out.append(f"  {l['canal']:18} "
                       f"na conversao MEDIDA (1,2/mil): {l[k+'a_1_2_por_mil']:,} views/dia | "
                       f"a 5/mil: {l[k+'a_5_por_mil']:,} | "
                       f"a 20/mil: {l[k+'a_20_por_mil']:,}")
    out.append("")
    out.append("COMO LER ISTO, e vai junto de proposito:")
    out.append("  * o ritmo e LINEAR sobre duas leituras — otimista para canal")
    out.append("    que acelera, pessimista para canal que satura;")
    out.append("  * a barra SOBE para 1.000 inscritos em "
               f"{q['barra_sobe_em']}: projecao que passa dessa data nao fecha")
    out.append("    a Porta 1, fecha outra coisa;")
    out.append("  * canal com acervo anterior a maquina tem inscrito que a")
    out.append("    maquina nao trouxe (668) — o PORTAO conta o absoluto, mas a")
    out.append("    CONVERSAO desse canal nao e atribuivel.")
    return "\n".join(out)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print("uso: porta1.py '<json>'")
        print('  {"horas": 40.3, "canais": {"labtreinamento": '
              '{"antes": 67, "agora": 68}}}')
        return 2
    d = json.loads(sys.argv[1])
    print(relato(quadro(d["canais"], d["horas"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
