"""A QUARTA pergunta do passo zero: de QUAL origem sai a peca desta rodada.

**Medido em 20/10 as 08:2x, escrevendo o `labtreinamento-s091`.** O
`passo_zero.py` responde tres perguntas numa chamada — inscritos, canal e cota —
e **a pauta ficou de fora**. Logo, a cada rodada, eu escrevia na linha de comando
um laco descartavel sobre `concentracao.contagem` + `segundo_angulo`, ordenava de
cabeca e aplicava o desempate no olho. **E a §10 da rotina diz, no item 3, que
todo numero que eu calculo a mao vira um erro meu** — ja medido em tres outras
dimensoes: a contagem de CANAL (19/10 as 11:2x, cinco rodadas seguidas a mao), a
de COTA (19/10 as 23:3x) e a de CENAS (20/10 as 02:2x).

**E o pior nao e o laco: e que eu NAO CHAMEI o `irmaos_da_origem`.** Ele existe
desde 15/10 (aprendizado 776), responde exatamente a pergunta que eu respondia
lendo cinco shorts no olho — *"quais familias esta origem ja rendeu"* — e
**modulo nenhum da fabrica o chamava**, so o teste dele. Rodado depois, sobre a
origem desta rodada, ele devolve as QUATRO familias anteriores em letra, porque
a geracao antiga as registrava na PROSA das copies dos irmaos. E a SEXTA vez da
mesma assinatura: nao chamar quem ja sabe.

**A REGRA NAO E NOVA e vai DELEGADA**, nao reimplementada: o `concentracao.py`
manda, em letra, *"pegue a origem de MENOR contagem com capitulos intocados"*, e
o desempate pela MAIOR reserva e o que eu venho aplicando a mao desde 19/10.
Aqui ela vira codigo com as quatro contas nos donos:

* a contagem de usos por origem -> `concentracao.contagem`
* a reserva de capitulos        -> `segundo_angulo.nao_mencionados`
* as familias dos irmaos        -> `irmaos_da_origem.relato`
* a origem de outro canal       -> `concentracao.origem_de_outro_canal`

**E ele NOMEIA em vez de filtrar.** Origem suspeita de ser de outro canal sai na
lista com a marca, e a decisao continua sendo leitura: esconder faria a rodada
seguinte perguntar por que a lista encurtou, que e a cegueira que o
`origens_sem_uso` nasceu para desfazer. Sem mapa de dono MEDIDO ele **diz que o
mapa falta** — ausencia de medicao nao e ausencia de problema.

**E O MAPA PASSOU A TER DONO EM 20/10 as 10:1x, porque ele nao existia como
DADO.** Nas duas primeiras rodadas deste modulo o relato saiu com *"mapa de dono
MEDIDO ausente"* — e a medicao existia, escrita em PROSA no `CLAUDE.md` e nos
docstrings deste modulo e do `concentracao`. O custo foi de ESCOLHA: nesta
rodada ele deu o `QiaGg03WSR0` como ESCOLHIDA no `kolejny-poziom`, e com o mapa
a vez passa ao `SZV9Vk5YFwI`. Agora o padrao e `dono_medido.mapa()`, e **quem
quiser medir o modulo SEM mapa passa `{}` explicitamente** — os dois ramos
continuam existindo e testaveis.

**NAO E PORTAO** e nao escolhe familia: capitulo livre NAO e familia livre (776),
e nenhum limiar de string distingue duas frases sobre o mesmo limiar. Codigo de
saida sempre zero.
"""
import sys

import concentracao as CO
import dono_medido as DM
import irmaos_da_origem as IO
import reservas_escritas as RE
import segundo_angulo as SA


def _resolve_mapa(dono_medido):
    """UM dono da regra: `None` = use o mapa MEDIDO, `{}` = sem mapa.

    A primeira versao deste conserto resolvia dentro do `quadro` e deixava a
    FLAG do relato ser calculada no `escolha` a partir do argumento nao
    resolvido — dois donos do mesmo fato, que e a assinatura que congelou a
    legenda, aparecendo DENTRO do conserto dela. O relato dizia "mapa ausente"
    com a suspeita ja NOMEADA na lista acima.
    """
    return DM.mapa() if dono_medido is None else dono_medido


def quadro(canal: str, dono_medido=None, exceto: str = "") -> list[dict]:
    """Uma linha por origem deste canal: usos, reserva e marca de suspeita.

    `exceto` vai as DUAS contas, e isso e o conserto de 20/10 as 14:3x: ate
    entao ele chegava so a CONTAGEM de usos, e nunca a RESERVA — que e o
    DESEMPATE. Com a peca da rodada no disco, a reserva da origem dela caia (76
    para 71 na medicao) e a escolha TROCAVA de origem mesmo com o `exceto`
    ligado. Conserto aplicado a UM de dois donos nao e conserto.

    `exceto` tira um pacote da contagem de irmaos — na hora de ESCOLHER, a spec
    desta rodada ja pode estar no disco, e ai "familia inedita" nunca podia ser
    verdade. E a mesma razao do `exceto` no `esqueleto_entre_canais`.
    """
    # O `exceto` vai ao DONO da contagem: filtrar aqui seria recontar o disco,
    # que e o segundo dono que congelou a legenda.
    usos = CO.contagem(canal, exceto=exceto)
    dono_medido = _resolve_mapa(dono_medido)
    fora = {}
    if dono_medido:
        fora = CO.origem_de_outro_canal(canal, dono_medido) or {}
    linhas = []
    for oid, n in usos.items():
        # O MESMO `exceto` da contagem, no dono da RESERVA. Sem ele a reserva
        # da origem da propria rodada vem deflacionada pelas mencoes da peca
        # que eu acabei de escrever, e e a reserva que desempata.
        nm = SA.nao_mencionados(oid, exceto=exceto or None)
        reserva = nm.get("nao_mencionados") or []
        linhas.append({
            "origem": oid,
            "usos": int(n),
            "pacote": nm.get("pacote"),
            "n_capitulos": int(nm.get("n_capitulos") or 0),
            "reserva": len(reserva),
            "suspeito_de_outro_canal": oid in fora,
            "dono_medido": fora.get(oid),
            "sem_spec_local": not nm.get("pacote"),
        })
    linhas.sort(key=lambda x: (x["usos"], -x["reserva"], x["origem"]))
    return linhas


def escolha(canal: str, dono_medido=None, exceto: str = "") -> dict:
    """A regra ESCRITA: menor contagem, desempate pela MAIOR reserva.

    Devolve `None` em `escolhida` quando nao sobra origem — e NAO inventa uma,
    do jeito que o `porta1` recusa janela curta.
    """
    dono_medido = _resolve_mapa(dono_medido)
    q = quadro(canal, dono_medido=dono_medido, exceto=exceto)
    # A suspeita de outro canal EXCLUI da escolha e NAO da lista: ela so entra
    # aqui porque foi MEDIDA (o mapa de dono), nunca por palpite.
    servem = [x for x in q
              if not x["suspeito_de_outro_canal"] and x["reserva"] > 0]
    esc = servem[0] if servem else None
    empatados = [x for x in servem if esc and x["usos"] == esc["usos"]]
    return {
        "canal": canal,
        "quadro": q,
        "escolhida": esc,
        "empatados_na_contagem": [x["origem"] for x in empatados],
        "nomeados_como_suspeitos": [x["origem"] for x in q
                                    if x["suspeito_de_outro_canal"]],
        "sem_mapa_de_dono": not dono_medido,
        "dominante": max(q, key=lambda x: x["usos"])["origem"] if q else None,
    }


def _linha_do_mapa(e: dict) -> str:
    """UM dono da frase do mapa, e ela sai nos DOIS ramos.

    A frase do teto nasceu duplicada em outro modulo e foi isso que a fez
    divergir (753).
    """
    if e["sem_mapa_de_dono"]:
        return ("  mapa de dono MEDIDO ausente: nenhuma origem foi marcada como "
                "de outro canal, e isso NAO prova que nao haja — o "
                "`QiaGg03WSR0` do kolejny e o caso medido (18/10 as 01:2x). "
                "Ausencia de medicao nao e ausencia de problema.")
    return ("  mapa de dono MEDIDO presente (%d entrada(s) no `dono_medido.py`): "
            "%d origem(ns) NOMEADA(s) como de outro canal, e elas saem da "
            "escolha sem sair da lista. O mapa NAO e exaustivo: origem fora "
            "dele e DESCONHECIDA, nunca do proprio canal."
            % (len(DM.MEDIDOS), len(e["nomeados_como_suspeitos"])))


def relato(canal: str, dono_medido=None, exceto: str = "") -> str:
    e = escolha(canal, dono_medido=_resolve_mapa(dono_medido), exceto=exceto)
    q = e["quadro"]
    L = ["PAUTA DO MOMENTO em %s: %d origens." % (canal, len(q))]
    for x in q[:6]:
        marca = ""
        if x["suspeito_de_outro_canal"]:
            marca += "  << SUSPEITA de ser do %s" % x["dono_medido"]
        if x["sem_spec_local"]:
            marca += "  << sem spec local (regra h)"
        if e["escolhida"] and x["origem"] == e["escolhida"]["origem"]:
            marca += "  << ESCOLHIDA"
        L.append("  %-12s usos %2d  reserva %3d de %3d  %s%s"
                 % (x["origem"], x["usos"], x["reserva"], x["n_capitulos"],
                    x["pacote"] or "-", marca))
    if e["escolhida"]:
        L.append("  regra ESCRITA (do `concentracao.py`): MENOR contagem com "
                 "capitulos intocados, desempate pela MAIOR reserva.")
        if len(e["empatados_na_contagem"]) > 1:
            L.append("  empate em %d usos entre %s — desempatado pela reserva."
                     % (e["escolhida"]["usos"],
                        ", ".join(e["empatados_na_contagem"])))
        L.append("  dominante do canal: %s (ela NAO foi escolhida; o alerta de "
                 "concentracao sai do `concentracao.py`)." % e["dominante"])
    else:
        L.append("  >> NENHUMA origem deste canal tem reserva de capitulo — "
                 "aqui nao se escolhe pauta local, e a rota e a regra (h) "
                 "(legenda do longo), do jeito que o `porta1` recusa janela "
                 "curta.")
    L.append(_linha_do_mapa(e))
    if e["escolhida"]:
        L.append("")
        L.append(IO.relato(e["escolhida"]["origem"],
                           excluir=(exceto,) if exceto else ()))
        # A RESERVA ESCRITA entra aqui porque e aqui que a pauta se escolhe:
        # ela existia em prosa em 24 pecas e nenhum instrumento a alcancava, e
        # a peca de 20/10 as 20:1x achou a dela por ACIDENTE (20:4x).
        L.append("")
        L.append(RE.relato(e["escolhida"]["origem"]))
        # E O TEXTO DOS LIVRES entra aqui pelo mesmo motivo que a reserva: ele
        # existia so como um laco que eu escrevia na hora, e em 22/10 as 10:3x
        # eu o cortei com uma fatia e escolhi a familia de 31 de 59 livres.
        # Instrumento que a rodada nao chama e a classe dos layouts mortos.
        L.append("")
        L.append(SA.relato_dos_livres(e["escolhida"]["origem"], exceto=exceto))
    L.append("")
    L.append("  isto NAO decide FAMILIA: capitulo livre nao e familia livre "
             "(776). As quatro contas sao dos donos — `concentracao`, "
             "`segundo_angulo`, `irmaos_da_origem`, `reservas_escritas` — "
             "e nenhuma e daqui.")
    return "\n".join(L)


def main() -> int:
    canal = sys.argv[1] if len(sys.argv) > 1 else "labtreinamento"
    exceto = sys.argv[2] if len(sys.argv) > 2 else ""
    print(relato(canal, exceto=exceto))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
