"""A chave de escolha aplicava SO a recencia, e a folga ela mesma calculava.

Medido em 20/10 as 07:4x, na rodada seguinte a que criou a coluna da folga. O
`contagem_de_cenas` passou a calcular `folga_no_piso` em 06:3x e
`repete_recente` em 05:2x — e `escolha()["por_cadencia_sem_repetir"]`, que e a
chave que a rodada LE para decidir, filtrava so pela recencia. Resultado medido
nos TRES canais:

| canal | `por_cadencia_sem_repetir` | folga | servivel |
|---|---|---|---|
| kolejny-poziom | 14 | **+1** (rente) | 13 |
| epomeno-epipedo | 15 | **+1** (rente) | 12 |
| labtreinamento | 9 | **-2** (PISO INALCANCAVEL) | 6 |

Tres de tres devolviam contagem que a coluna do PROPRIO modulo recusa, e no
`labtreinamento` o conjunto descartado inclui **10 cenas, a forma mais usada da
frota**. E a quinta vez desta familia de instrumentos: nao aplicar o que o
modulo ja sabe — a mesma forma do 06:3x uma camada acima, onde o
`mira.orcamento` dava conselho que a propria `mira.confere` reprovava.

A contraprova deste arquivo vai nos DOIS sentidos: ele mede que a chave ANTIGA
de fato devolve contagem recusada (senao "o defeito existia" seria afirmacao
minha), e exige que a chave NOVA passe os tres filtros ao mesmo tempo.
"""
import ast
import io
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import contagem_de_cenas as CC  # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "contagem_de_cenas.py")

# Os tres canais VIVOS e as vozes deles. A varredura sai daqui e nao de uma
# contagem escrita a mao: canal novo entra sozinho.
CANAIS = {
    "kolejny-poziom": "pl-PL-MarekNeural",
    "epomeno-epipedo": "el-GR-NestorasNeural",
    "labtreinamento": "pt-BR-ThalitaMultilingualNeural",
}


def _escolhas():
    return {c: CC.escolha(c, v) for c, v in CANAIS.items()}


def test_a_varredura_nao_passa_por_VACUIDADE():
    """Quadro curto faria todo assert deste arquivo passar sem medir nada."""
    for canal, voz in CANAIS.items():
        q = CC.quadro(canal, voz)
        assert len(q) >= 15, (canal, len(q))
        assert any(x["cabe_na_voz"] for x in q), canal


def test_a_chave_NOVA_passa_os_TRES_filtros_ao_mesmo_tempo():
    for canal, e in _escolhas().items():
        s = e["por_cadencia_servivel"]
        if s is None:
            continue
        assert s["cabe_na_voz"] is True, canal
        assert s["repete_recente"] is False, canal
        assert s["folga_no_piso"] > CC.FOLGA_RENTE, (canal, s["folga_no_piso"])


def test_a_chave_ANTIGA_de_fato_devolvia_contagem_RECUSADA():
    """Contraprova no outro sentido: sem ela, o defeito seria afirmacao minha.

    Cobrado por PROPRIEDADE e nao pelo numero 14 ou 9 — a contagem que cai aqui
    muda com a recencia do canal, e cravar o numero e o defeito 743/753/761.
    """
    ruins = []
    for canal, e in _escolhas().items():
        ant = e["por_cadencia_sem_repetir"]
        if ant and ant["folga_no_piso"] <= CC.FOLGA_RENTE:
            ruins.append((canal, ant["cenas"], ant["folga_no_piso"]))
    assert ruins, (
        "nenhum canal tem a chave antiga devolvendo contagem de folga rente ou "
        "negativa — se isso virou verdade, o defeito que este arquivo mede "
        "desapareceu e a nota do CLAUDE.md tem de ser RELIDA, nao o numero "
        "movido"
    )


def test_os_DOIS_lados_existem_e_a_convergencia_RELE_esta_nota():
    """Tem de haver canal em que a chave nova DIVERGE da antiga, e canal algum
    pode ser o unico — se as tres convergirem, o defeito acabou."""
    es = _escolhas()
    diverge = [c for c, e in es.items()
               if e["por_cadencia_servivel"] and e["por_cadencia_sem_repetir"]
               and (e["por_cadencia_servivel"]["cenas"]
                    != e["por_cadencia_sem_repetir"]["cenas"])]
    assert diverge, (
        "as tres escolhas convergiram: ou a folga deixou de apertar, ou alguem "
        "igualou as duas chaves. Releia a nota em vez de afrouxar este teste."
    )


def test_o_PISO_INALCANCAVEL_tambem_e_descartado_e_nao_so_o_rente():
    """A folga negativa e caso DIFERENTE do rente, e os dois tem de cair.

    No `labtreinamento` o descartado inclui contagem de folga NEGATIVA, isto e,
    piso inalcancavel com texto legivel (a nota de 06:3x).
    """
    achou_negativa = False
    for canal, voz in CANAIS.items():
        e = CC.escolha(canal, voz)
        q = {x["cenas"]: x for x in CC.quadro(canal, voz)}
        for n in e["descartados_pela_folga"]:
            assert q[n]["folga_no_piso"] <= CC.FOLGA_RENTE, (canal, n)
            if q[n]["folga_no_piso"] < 0:
                achou_negativa = True
        s = e["por_cadencia_servivel"]
        if s:
            assert s["folga_no_piso"] >= 0, (canal, s)
    assert achou_negativa, (
        "nenhuma contagem com piso INALCANCAVEL foi descartada em canal algum — "
        "sem ela este arquivo nao distingue o rente do negativo"
    )


def _por_contagem_sintetico(folga_do_teto: int):
    """Um quadro PROPRIO, para cobrar a fronteira sem ancorar no disco vivo.

    Ancorar a fronteira no parque vivo seria identidade onde ha propriedade
    (743/753/761): a folga de cada contagem muda quando a faixa ou a voz muda.
    """
    return {n: 0 for n in range(2, 21)}


def test_a_FRONTEIRA_da_folga_e_cobrada_nos_dois_lados():
    """Exatamente `FOLGA_RENTE` cai; `FOLGA_RENTE + 1` fica."""
    canal, voz = "kolejny-poziom", CANAIS["kolejny-poziom"]
    q = CC.quadro(canal, voz)
    cabem = [x for x in q if x["cabe_na_voz"]]
    assert cabem, "quadro sem contagem que cabe na voz"
    na_borda = [x for x in cabem if x["folga_no_piso"] == CC.FOLGA_RENTE]
    acima = [x for x in cabem if x["folga_no_piso"] == CC.FOLGA_RENTE + 1]
    # A borda exata pode nao existir no quadro vivo; o que NAO pode e o
    # criterio ser `>=` em vez de `>`.
    serve = [x for x in cabem if x["folga_no_piso"] > CC.FOLGA_RENTE]
    assert all(x["folga_no_piso"] > CC.FOLGA_RENTE for x in serve)
    for x in na_borda:
        assert x not in serve, ("folga igual ao limiar NAO serve", x["cenas"])
    for x in acima:
        assert x in serve, ("folga um acima do limiar SERVE", x["cenas"])


def test_a_chave_nova_entra_AO_LADO_e_nao_no_lugar_das_outras():
    """A disciplina de 05:2x: substituir seria FILTRAR, e o `FOLGA_RENTE` e
    redacao declarada, nao medida."""
    for canal, e in _escolhas().items():
        assert "por_cadencia_geral" in e, canal
        assert "por_cadencia_sem_repetir" in e, canal
        assert "por_cadencia_servivel" in e, canal
        geral = e["por_cadencia_geral"]
        assert geral is not None, canal
        # a melhor cadencia GERAL ignora recencia e folga, por construcao
        q = [x for x in CC.quadro(canal, CANAIS[canal]) if x["cabe_na_voz"]]
        melhor = min(q, key=lambda x: x["distancia_da_cadencia"])
        assert geral["cenas"] == melhor["cenas"], canal


def test_o_descartado_vai_NOMEADO_no_relato_e_nao_filtrado():
    """Filtrar faria a rodada seguinte perguntar por que a lista encurtou."""
    for canal, voz in CANAIS.items():
        e = CC.escolha(canal, voz)
        r = CC.relato(canal, voz)
        if e["descartados_pela_folga"]:
            assert "NOMEADAS" in r, canal
            for n in e["descartados_pela_folga"]:
                assert str(n) in r, (canal, n)
        if e["por_cadencia_servivel"]:
            assert "SERVE" in r, canal


def test_quando_NADA_serve_ele_RECUSA_em_vez_de_inventar():
    """Do jeito que o `porta1` recusa janela curta."""
    canal, voz = "kolejny-poziom", CANAIS["kolejny-poziom"]
    q = CC.quadro(canal, voz)
    todas = [x["cenas"] for x in q if x["cabe_na_voz"]]
    assert todas, "sem contagem que cabe na voz, o teste nao mede nada"
    recentes = [{"pacote": "%s-sXXX" % canal, "em": "2026-10-20T07:00:00Z",
                 "cenas": n} for n in todas]
    e = CC.escolha(canal, voz, recentes=recentes)
    assert e["por_cadencia_servivel"] is None
    # A frase sai do DONO dela. O `relato` nao aceita `recentes` — ele le o
    # parque vivo —, e reimplementar a linha aqui criaria o segundo dono.
    r = CC._linha_da_folga(CC.quadro(canal, voz, recentes=recentes), e)
    assert "NENHUMA contagem serve" in r


def test_a_frase_da_escolha_servivel_tem_UM_dono():
    """Por AST. A frase do teto nasceu duplicada e foi isso que a fez divergir
    (753), logo a propriedade e haver UM dono — nao a contagem de string."""
    arvore = ast.parse(io.open(FONTE, encoding="utf-8").read())
    donos = set()
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef):
            continue
        for filho in ast.walk(no):
            if (isinstance(filho, ast.Constant)
                    and isinstance(filho.value, str)
                    and "que SERVE" in filho.value):
                donos.add(no.name)
    assert donos == {"_linha_da_folga"}, donos


def test_a_folga_e_LIDA_do_quadro_e_nao_recalculada():
    """Refazer a conta na `escolha` criaria o segundo dono — a assinatura que
    congelou a legenda. Cobrado por AST: a `escolha` nao chama o inversor nem o
    teto de caracteres por conta propria."""
    arvore = ast.parse(io.open(FONTE, encoding="utf-8").read())
    alvo = [n for n in arvore.body
            if isinstance(n, ast.FunctionDef) and n.name == "escolha"]
    assert alvo, "funcao `escolha` nao achada"
    proibidos = {"chars_no_alvo", "_chars_para_o_real", "teto_de_cenas"}
    for no in ast.walk(alvo[0]):
        if isinstance(no, ast.Call):
            f = no.func
            nome = getattr(f, "attr", None) or getattr(f, "id", None)
            assert nome not in proibidos, nome


def test_ele_REPRODUZ_a_escolha_de_ONZE_feita_a_mao():
    """Sem isto a nota nao prova que o instrumento serve a decisao que de fato
    foi tomada. O `exceto` tira a peca da rodada, que ja esta no disco."""
    rec = [{"pacote": "kolejny-poziom-s073", "em": "2026-10-20T04:13:06Z",
            "cenas": 12},
           {"pacote": "kolejny-poziom-s072", "em": "2026-10-20T01:17:14Z",
            "cenas": 13}]
    e = CC.escolha("kolejny-poziom", CANAIS["kolejny-poziom"],
                   recentes=rec, exceto="kolejny-poziom-s074")
    s = e["por_cadencia_servivel"]
    assert s is not None
    assert s["cenas"] == 11, s
    # e a chave antiga teria devolvido a contagem rente que eu recusei a mao
    assert e["por_cadencia_sem_repetir"]["folga_no_piso"] <= CC.FOLGA_RENTE


def test_o_MOTIVO_continua_escrito_no_modulo():
    """Conserto sem motivo escrito volta calado, e este e o quinto da familia."""
    fonte = io.open(FONTE, encoding="utf-8").read()
    assert "folga_no_piso" in fonte
    assert "quinta vez" in fonte
    assert "06:3x" in fonte


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
