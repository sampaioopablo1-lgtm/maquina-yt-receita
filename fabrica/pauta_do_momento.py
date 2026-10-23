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
        # A RESERVA SEM DECLARACAO, e ela e DELEGADA: quem casa capitulo livre
        # com a faixa que o irmao declara e o `texto_dos_livres`, dono dessa
        # juncao desde 22/10 as 12:3x. Refazer a juncao aqui seria o segundo
        # dono dela — a assinatura que congelou a legenda.
        sem_decl = None
        if nm.get("pacote"):
            tl = SA.texto_dos_livres(oid, exceto=exceto or None)
            sem_decl = len(reserva) - len(tl.get("declarados_por_irmao") or [])
        linhas.append({
            "origem": oid,
            "usos": int(n),
            "pacote": nm.get("pacote"),
            "n_capitulos": int(nm.get("n_capitulos") or 0),
            "reserva": len(reserva),
            "reserva_sem_declaracao": sem_decl,
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
    # As tres contas por PACOTE, para o caso em que ele nao e unico por origem
    # (23/10 as 03:3x). Elas vao NOMEADAS e NAO entram na escolha: ver o
    # docstring de `_compartilhados`.
    comp = _compartilhados(q)
    usos_pac, inter_pac = {}, {}
    for p, ids in comp.items():
        usos_pac[p] = sum(x["usos"] for x in q if x["origem"] in ids)
        livres = None
        ncap = 0
        for oid in ids:
            nm = SA.nao_mencionados(oid, exceto=exceto or None)
            s = set(nm.get("nao_mencionados") or [])
            ncap = max(ncap, int(nm.get("n_capitulos") or 0))
            livres = s if livres is None else (livres & s)
        inter_pac[p] = (len(livres or ()), ncap)
    # A suspeita de outro canal EXCLUI da escolha e NAO da lista: ela so entra
    # aqui porque foi MEDIDA (o mapa de dono), nunca por palpite.
    servem = [x for x in q
              if not x["suspeito_de_outro_canal"] and x["reserva"] > 0]
    esc = servem[0] if servem else None
    empatados = [x for x in servem if esc and x["usos"] == esc["usos"]]
    # O MESMO empate, desempatado pela reserva SEM DECLARACAO. Ela NAO troca a
    # `escolhida` — a regra escrita e do `concentracao.py` e nao e minha de
    # mudar —, ela vai NOMEADA ao lado, do jeito que o `origens_sem_uso` nomeia
    # origem inutilizavel em vez de a esconder. Medido em 22/10 as 17:3x: no
    # `labtreinamento` as duas DIVERGEM e a inversao e maxima (14 contra 37
    # capitulos sem declaracao), e nos outros dois canais elas concordam.
    por_sem = None
    cand = [x for x in empatados if x.get("reserva_sem_declaracao") is not None]
    if cand:
        por_sem = max(cand, key=lambda x: (x["reserva_sem_declaracao"],
                                           -x["usos"], x["origem"]))
    # O VAO da divergencia, em capitulos e em fracao do maior dos dois. Ele
    # existe porque a decisao de seguir a regra escrita ou a leitura nova
    # depende do TAMANHO do vao, e eu a tomei DE CABECA em duas rodadas:
    # em 22/10 as 17:3x o vao era 14 contra 37 (23 capitulos, 62%) e eu desviei;
    # as 18:0x era 59 contra 61 (2 capitulos, 3%) e eu segui a regra. Ele NOMEIA
    # o vao e NAO decide por ele: limiar aqui seria criterio inventado (§10),
    # e declaracao em prosa e INDICIO, nao veredito.
    vao = None
    if esc and por_sem and esc["origem"] != por_sem["origem"]:
        a_ = esc.get("reserva_sem_declaracao") or 0
        b_ = por_sem.get("reserva_sem_declaracao") or 0
        maior = max(a_, b_)
        vao = {"capitulos": b_ - a_,
               "fracao": (b_ - a_) / maior if maior else None,
               "da_regra": a_, "da_leitura_nova": b_}
    return {
        "compartilhados": comp,
        "usos_por_pacote": usos_pac,
        "reserva_na_interseccao": inter_pac,
        "desempate_vao": vao,
        "canal": canal,
        "quadro": q,
        "escolhida": esc,
        "escolhida_por_reserva_sem_declaracao": por_sem,
        "desempate_diverge": bool(esc and por_sem
                                  and esc["origem"] != por_sem["origem"]),
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


def _compartilhados(linhas: list) -> dict:
    """{pacote: [origens]} para todo pacote com MAIS DE UMA origem no quadro.

    **Medido em 23/10 as 03:3x, na rodada em que isto trocou a leitura da
    pauta.** Pacote nao e unico por origem: das 54 origens dos tres canais,
    QUATRO estao em pacote compartilhado. E o `nao_mencionados` le os capitulos
    de UMA spec para os dois ids, logo — para tudo o que este instrumento
    responde — os dois sao o MESMO texto, e as duas contas saem infladas:

    * **USOS**: o `kolejny-poziom-004` aparece como DUAS origens de 4 usos, e
      por texto ele tem **8** — o SEGUNDO mais usado do canal, enquanto por id
      ele empatava no MINIMO. No `labtreinamento` e pior: o
      `labtreinamento-002` tem **14** por texto e e o mais usado do canal,
      acima do `FtCtIJPsc_Q` (13) que o relato vinha chamando de dominante.
      Isto e o efeito (C-2) que a rotina nomeia desde o 658 — contar por id
      premia duplicata —, e o `origens_sem_uso` ganhou guarda contra ele em
      18/10 as 03:1x. A contagem de usos nao ganhou;
    * **RESERVA**: os livres de um id ignoram os shorts que declaram o IRMAO,
      que consomem capitulos do mesmo texto. No caso medido o pacote tem OITO
      shorts somando os dois ids, e o livre de verdade e a INTERSECCAO: **53 de
      74**, nao 64 nem 58.

    **Isto NOMEIA e NAO decide**, e o motivo e o mesmo da reserva sem
    declaracao: unir por pacote e unir por uma RESOLUCAO em prosa, e ela erra
    nos dois sentidos — o `QiaGg03WSR0` e um longo do labtreinamento declarado
    por engano em dois shorts do kolejny, isto e, resolucao de id e falivel.
    Trocar a `escolhida` por ela transformaria heuristica em regra.

    **E o que eu NAO consigo conferir vai declarado:** se os dois videos sao o
    mesmo conteudo de verdade. Isso se le na pagina de cada um, e a rota esta
    em `negado_por_politica`.
    """
    porpac = {}
    for x in linhas:
        p = x.get("pacote")
        if p:
            porpac.setdefault(p, []).append(x["origem"])
    return {p: sorted(v) for p, v in porpac.items() if len(v) > 1}


_PRE_COMP = "  PACOTE COMPARTILHADO: "


def _linha_dos_compartilhados(e: dict) -> str:
    """UM dono da frase, e ela sai nos DOIS ramos — ha e nao ha."""
    comp = e.get("compartilhados") or {}
    if not comp:
        return (_PRE_COMP + "nenhum pacote deste canal tem mais de uma origem, "
                "logo a contagem por id e a contagem por TEXTO coincidem aqui. "
                "Elas NAO coincidem sempre: em 23/10 as 03:3x o "
                "`kolejny-poziom-004` tinha 4 usos por id e 8 por texto.")
    partes = []
    for p, ids in sorted(comp.items()):
        u = e.get("usos_por_pacote", {}).get(p)
        inter = e.get("reserva_na_interseccao", {}).get(p)
        partes.append("%s <- %d origens %s: %s usos por TEXTO (cada id mostra "
                      "menos), e o livre de verdade e a INTERSECCAO dos livres "
                      "(%s)"
                      % (p, len(ids), ids,
                         "?" if u is None else u,
                         "?" if inter is None else "%d de %d" % inter))
    return (_PRE_COMP + "; ".join(partes) + ". **Isto NOMEIA e nao decide** — "
            "unir por pacote e unir por uma RESOLUCAO em prosa, que erra nos "
            "dois sentidos, e trocar a `escolhida` por ela viraria heuristica "
            "em regra. Conferir se os dois videos sao o mesmo conteudo pede a "
            "PAGINA de cada um, e a rota pode estar fechada.")


_PRE = "  DESEMPATE pela reserva SEM DECLARACAO: "


def _nome_da_origem(x: dict) -> str:
    """UM dono do nome de uma origem no relato: a ORIGEM, com o pacote ao lado.

    **Medido em 23/10 as 03:2x, na rodada em que a ambiguidade apareceu.** A
    frase do desempate escrevia `pacote or origem` em TRES lugares, isto e, o
    pacote vencia e o youtube_id era so o reserva. E pacote NAO e unico por
    origem: varridas as 54 origens dos tres canais, **QUATRO estao em pacote
    COMPARTILHADO**, em dois pacotes e em dois canais —
    `kolejny-poziom-004` <- {`iqV7m6tKb5A`, `ef_oZmfmdz4`} e
    `labtreinamento-002` <- {`StQNFMdpGdk`, `XgqPVJuAk3o`}.

    Logo quando as duas leituras do desempate escolhiam DUAS origens do mesmo
    pacote, a linha imprimia o MESMO nome nos dois lados e lia-se como
    CONCORDANCIA — enquanto o vao que ela mesma imprime na linha seguinte era
    de 17 capitulos. E a frase manda `LEIA as duas antes de escrever`: ler "as
    duas" quando as duas tem o mesmo nome e ler UMA.

    **A falha e de RELATO e nao de veredito** — a `escolhida` sempre saiu da
    regra escrita do `concentracao.py`, que trabalha com o youtube_id. O que
    ela custa e a leitura: foi so por desconfiar do nome repetido que eu fui
    conferir os ids desta rodada.

    A linha da TABELA do `relato` nao usa isto de proposito: ali a origem e o
    pacote ja tem COLUNA cada um, logo o nome nao e ambiguo.
    """
    o = x.get("origem") or "?"
    p = x.get("pacote")
    return "%s (%s)" % (o, p) if p else o


def _linha_do_desempate(e: dict) -> str:
    """UM dono da frase do desempate, e ela sai nos TRES ramos.

    Os tres compartilham o PREFIXO `DESEMPATE pela reserva SEM DECLARACAO`, e e
    ele que tem dono: marca mais curta casaria com a prosa que explica o defeito
    no `quadro`, e casar prosa pega a explicacao em vez do codigo — a licao do
    `test_NAO_virou_portao` do acento.

    Medido em 22/10 as 17:3x, escrevendo o `labtreinamento-s110`: o desempate
    escrito le a reserva CRUA, e desde 22/10 as 12:3x esta medido que capitulo
    que o irmao DECLARA sai como livre, porque o `nao_mencionados` casa o TEXTO
    do kicker e a copy declara FAIXA em digitos. Logo a reserva que DESEMPATA
    vem inflada. Nos cinco empatados em 6 usos daquele canal o raw escolhe a
    origem de **40** livres, dos quais so **14** estao sem declaracao, contra
    uma de **38** livres com **37** sem declaracao — a inversao e maxima. Nos
    outros dois canais as duas concordam, e e por isso que a divergencia vai
    NOMEADA em vez de a `escolhida` trocar: declaracao em prosa NAO e veredito
    nos dois sentidos (a faixa cobre capitulo que o irmao nao tocou, e a maior
    parte das specs de short solto nao declara nada).
    """
    if len(e.get("empatados_na_contagem") or []) < 2:
        return (_PRE + "nao houve empate de usos, logo a reserva nao "
                "desempatou nada nesta rodada — e a divergencia medida em "
                "22/10 as 17:3x nao tem objeto aqui.")
    s = e.get("escolhida_por_reserva_sem_declaracao")
    if not s:
        return (_PRE + "nao ha como medir — nenhum dos empatados tem spec "
                "local, logo a reserva nao se separa entre declarada e livre.")
    if not e.get("desempate_diverge"):
        return (_PRE + "a MESMA origem (%s, %d de %d livres sem declaracao "
                "de irmao). As duas leituras CONCORDAM aqui — e nao concordam "
                "sempre."
                % (_nome_da_origem(s), s["reserva_sem_declaracao"],
                   s["reserva"]))
    esc = e["escolhida"]
    v = e.get("desempate_vao") or {}
    frac = v.get("fracao")
    vao_txt = ("  O VAO e de %d capitulo(s), %s do maior dos dois — e a decisao "
               "de seguir a regra escrita ou a leitura nova depende DELE, nao "
               "do fato de divergirem: em 22/10 as 17:3x o vao foi de 23 (62%%) "
               "e a rodada desviou; as 18:0x foi de 2 (3%%) e ela seguiu a "
               "regra, porque declaracao em prosa e INDICIO e desviar por dois "
               "capitulos transformaria a heuristica em regra. **Isto NOMEIA o "
               "vao e nao decide por ele** — limiar aqui seria criterio "
               "inventado (§10)."
               % (v.get("capitulos", 0),
                  "%.0f%%" % (100 * frac) if frac is not None else "fracao "
                  "indefinida"))
    return (_PRE + "as duas DIVERGEM. A reserva CRUA escolhe %s (%d livres, "
            "mas so %s sem declaracao de irmao) e a reserva SEM DECLARACAO "
            "escolhe "
            "%s (%d livres, %d sem declaracao). A regra escrita e do "
            "`concentracao.py` e a `escolhida` segue dela; isto vai NOMEADO e "
            "nao filtra ninguem, porque declaracao em prosa nao e veredito nos "
            "dois sentidos. LEIA as duas antes de escrever."
            % (_nome_da_origem(esc), esc["reserva"],
               esc.get("reserva_sem_declaracao"),
               _nome_da_origem(s), s["reserva"],
               s["reserva_sem_declaracao"]) + "\n" + vao_txt)


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
        sd = x.get("reserva_sem_declaracao")
        L.append("  %-12s usos %2d  reserva %3d de %3d  (sem declaracao %s)  "
                 "%s%s"
                 % (x["origem"], x["usos"], x["reserva"], x["n_capitulos"],
                    "-" if sd is None else "%3d" % sd, x["pacote"] or "-",
                    marca))
    if e["escolhida"]:
        L.append("  regra ESCRITA (do `concentracao.py`): MENOR contagem com "
                 "capitulos intocados, desempate pela MAIOR reserva.")
        if len(e["empatados_na_contagem"]) > 1:
            L.append("  empate em %d usos entre %s — desempatado pela reserva."
                     % (e["escolhida"]["usos"],
                        ", ".join(e["empatados_na_contagem"])))
        L.append(_linha_do_desempate(e))
        L.append(_linha_dos_compartilhados(e))
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
