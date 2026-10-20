# -*- coding: utf-8 -*-
"""O `contagem_de_cenas` nao sabia o que o canal ACABOU de publicar.

Medido em 20/10 as 05:2x, escrevendo o `labtreinamento-s090`. Ele deu **SETE**
cenas como melhor cadencia, e as DUAS pecas anteriores daquele canal — a `s088` e
a `s089` — tem sete cada. Eu recusei o sete **a mao**, como tinha recusado o treze
a mao uma hora antes no `kolejny`. Duas recusas a mao em duas rodadas e o item 3
da §10, **dentro do instrumento que existe para tirar essa conta da minha
cabeca**.

O que este arquivo cobra:

* a recencia sai do PARQUE (a spec no disco nao tem data) e o canal sai do
  `canal.do_pacote`, nao do campo `canal` do registro — que falta na MAIORIA das
  linhas antigas;
* ela NOMEIA e nao FILTRA: a melhor cadencia continua saindo, com a colisao ao
  lado;
* os DOIS lados existem — canal que repete e canal que nao —, e isso e cobrado
  com PARQUE PROPRIO. **RETRATADO NO LUGAR em 20/10 as 09:5x:** a primeira
  versao destes dois testes lia o parque VIVO e exigia que ALGUM canal
  colidisse hoje. Com tres rodadas seguidas escolhendo pela
  `por_cadencia_sem_repetir`, os tamanhos espalharam e **nenhum dos tres canais
  colide mais** — isto e, o teste passou a reprovar porque o instrumento
  FUNCIONOU. E a licao de 18/10 as 09:2x: *"teste que ancora em id de origem
  LIVRE reprova quando a pauta for consumida — e consumir pauta e o trabalho"*,
  aqui com a colisao no lugar da origem. O que ficou cobrado e que a FUNCAO
  discrimina, e que **se o vivo voltar a colidir o relato NOMEIA** — propriedade
  condicional, que nao pune o acerto;
* a janela do `K` e cobrada na FRONTEIRA, com parque proprio: ancorar no vivo
  seria identidade onde ha propriedade (743/753/761).
"""
import ast
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
sys.path.insert(0, FABRICA)

import contagem_de_cenas as CC            # noqa: E402
import duracao_a_medir as DM              # noqa: E402
import canal as CA                        # noqa: E402

MODULO = os.path.join(FABRICA, "contagem_de_cenas.py")

VOZES = {
    "labtreinamento": "pt-BR-ThalitaMultilingualNeural",
    "epomeno-epipedo": "el-GR-NestorasNeural",
    "kolejny-poziom": "pl-PL-MarekNeural",
}


def _fonte():
    with open(MODULO, encoding="utf-8") as f:
        return f.read()


def _func(nome):
    arvore = ast.parse(_fonte())
    for no in ast.walk(arvore):
        if isinstance(no, ast.FunctionDef) and no.name == nome:
            return no
    raise AssertionError("funcao %r nao existe no modulo" % nome)


def _chamadas(no):
    fora = set()
    for n in ast.walk(no):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute):
                base = f.value
                if isinstance(base, ast.Name):
                    fora.add("%s.%s" % (base.id, f.attr))
            elif isinstance(f, ast.Name):
                fora.add(f.id)
    return fora


def test_a_varredura_do_parque_nao_esta_VAZIA():
    """Sem pecas publicadas no parque o arquivo passaria por vacuidade."""
    regs = DM.carrega()
    assert len(regs) >= 20, "parque pequeno demais: %d linhas" % len(regs)
    por_canal = {}
    for r in regs:
        c = CA.do_pacote(r.get("pacote", ""))
        por_canal[c] = por_canal.get(c, 0) + 1
    for c in VOZES:
        assert por_canal.get(c, 0) >= 3, (
            "o canal %s tem %d pecas no parque — com menos de tres a janela de "
            "recencia nao mede nada" % (c, por_canal.get(c, 0))
        )


def test_as_tres_contas_sao_DELEGADAS_e_nenhuma_le_o_arquivo():
    """Por AST: o docstring CITA os nomes dos donos, e casar prosa pegaria a
    explicacao em vez do codigo. E `open()` aqui seria o segundo leitor do
    parque — a assinatura que congelou a legenda."""
    no = _func("recentes_do_canal")
    chamadas = _chamadas(no)
    assert "DM.carrega" in chamadas, (
        "o instante tem de vir do dono do parque: %s" % sorted(chamadas))
    assert "CA.do_pacote" in chamadas, (
        "o canal tem de vir do dono UNICO da derivacao: %s" % sorted(chamadas))
    assert "EC.varre" in chamadas, (
        "as cenas tem de vir do dono da varredura: %s" % sorted(chamadas))
    assert "open" not in chamadas, (
        "`open()` dentro de `recentes_do_canal` e um SEGUNDO leitor do parque")


def test_o_canal_sai_do_DONO_e_nao_do_campo_do_registro():
    """A maioria das linhas do parque NAO tem o campo `canal`.

    Logo ler o campo perderia essas pecas em silencio — e a janela de recencia
    andaria para tras sem ninguem ver. Cobrado como PROPRIEDADE: um registro sem
    o campo continua sendo atribuido ao canal certo.
    """
    regs = DM.carrega()
    sem_campo = [r for r in regs if "canal" not in r]
    assert len(sem_campo) > len(regs) / 2, (
        "so %d de %d linhas do parque estao sem o campo `canal` — se a maioria "
        "passar a ter, esta nota se rele" % (len(sem_campo), len(regs)))
    fake = [{"pacote": "labtreinamento-s901", "em": "2026-10-20T06:00:00Z"}]
    r = CC.recentes_do_canal("labtreinamento", k=1, registros=fake,
                             cenas_por_pacote={})
    assert len(r) == 1 and r[0]["pacote"] == "labtreinamento-s901", (
        "registro SEM o campo `canal` foi perdido: %r" % (r,))


def _parque_que_COLIDE(canal, n):
    """Parque PROPRIO em que as duas ultimas do canal tem `n` cenas."""
    regs = [{"pacote": "%s-s801" % canal, "em": "2026-10-20T01:00:00Z"},
            {"pacote": "%s-s802" % canal, "em": "2026-10-20T02:00:00Z"}]
    cen = {"%s-s801" % canal: n, "%s-s802" % canal: n}
    return CC.recentes_do_canal(canal, k=2, registros=regs,
                                cenas_por_pacote=cen)


def test_os_DOIS_lados_existem_sobre_o_MESMO_canal():
    """A recencia discrimina: com o parque que colide ela acusa, sem ele nao.

    **RETRATADO NO LUGAR:** a versao antiga lia o parque VIVO e exigia que
    algum canal colidisse HOJE. Isso e estado, nao propriedade — e o estado
    mudou justamente porque eu passei a seguir o instrumento. Com parque
    proprio os dois lados existem sempre, e e a FUNCAO que esta sob teste.
    """
    for c, v in VOZES.items():
        melhor = CC.escolha(c, v).get("por_cadencia_geral")
        assert melhor, c
        n = melhor["cenas"]
        q_colide = CC.quadro(c, v, recentes=_parque_que_COLIDE(c, n))
        q_livre = CC.quadro(c, v, recentes=[])
        rep_colide = {x["cenas"] for x in q_colide if x["repete_recente"]}
        rep_livre = {x["cenas"] for x in q_livre if x["repete_recente"]}
        assert n in rep_colide, (c, n, sorted(rep_colide))
        assert rep_livre == set(), (c, sorted(rep_livre))


def test_o_VIVO_recebe_veredito_para_TODO_canal():
    """O outro lado, sobre o parque vivo: ele pode legitimamente nao colidir,
    e o que nao pode e ficar SEM resposta — campo ausente seria cegueira."""
    for c, v in VOZES.items():
        e = CC.escolha(c, v)
        x = e.get("por_cadencia_geral")
        assert x is not None, c
        assert isinstance(x.get("repete_recente"), bool), (c, x)
        # o DONO da frase, porque o `relato` le o parque vivo por conta propria
        r = CC._linha_da_recencia(e)
        assert "RECENCIA no canal" in r, c
        if x["repete_recente"]:
            assert "NAO repete" in r, (
                "o vivo voltou a colidir em %s e o relato nao ofereceu a "
                "alternativa" % c)


def test_ele_NOMEIA_a_colisao_e_NAO_filtra_a_contagem():
    """Filtrar esconderia a contagem que a cadencia escolhe — a cegueira que o
    `origens_sem_uso` nasceu para desfazer.

    **Com PARQUE PROPRIO**, pela mesma razao do teste acima: a colisao no vivo
    e estado, e a rodada que segue o instrumento a desfaz.
    """
    for c, v in VOZES.items():
        n = CC.escolha(c, v)["por_cadencia_geral"]["cenas"]
        rec = _parque_que_COLIDE(c, n)
        e = CC.escolha(c, v, recentes=rec)
        assert e["por_cadencia_geral"]["cenas"] == n
        assert e["por_cadencia_geral"]["repete_recente"] is True
        quadro = CC.quadro(c, v, recentes=rec)
        assert any(x["cenas"] == n for x in quadro), (
            "a contagem que repete DESAPARECEU do quadro — isto e filtrar")
        # O `relato` le o parque VIVO, logo aqui se chama o DONO da frase
        # (`_linha_da_recencia`) em vez de reimplementa-la — reescrever a linha
        # no teste criaria o segundo dono dela.
        r = CC._linha_da_recencia(e)
        assert "RECENCIA no canal" in r, "o relato nao nomeia a recencia"
        assert str(n) in r, "o relato esconde a contagem que repete"
        nova = e.get("por_cadencia_sem_repetir")
        assert nova and nova["cenas"] != n, (
            "sem a alternativa que nao repete, nomear a colisao nao ajuda a "
            "escrever a peca: %r" % (nova,))
        assert "NAO repete" in r, "o relato nao oferece a alternativa"


def test_a_janela_do_K_e_cobrada_na_FRONTEIRA():
    """Parque PROPRIO, porque ancorar no vivo seria identidade onde ha
    propriedade — e o vivo anda a cada rodada."""
    regs = [
        {"pacote": "labtreinamento-s801", "em": "2026-10-20T01:00:00Z"},
        {"pacote": "labtreinamento-s802", "em": "2026-10-20T02:00:00Z"},
        {"pacote": "labtreinamento-s803", "em": "2026-10-20T03:00:00Z"},
    ]
    cen = {"labtreinamento-s801": 5, "labtreinamento-s802": 9,
           "labtreinamento-s803": 7}
    um = CC.recentes_do_canal("labtreinamento", k=1, registros=regs,
                              cenas_por_pacote=cen)
    assert [x["cenas"] for x in um] == [7], (
        "k=1 tem de devolver SO a mais nova: %r" % (um,))
    dois = CC.recentes_do_canal("labtreinamento", k=2, registros=regs,
                                cenas_por_pacote=cen)
    assert [x["cenas"] for x in dois] == [7, 9], (
        "k=2 tem de devolver as duas mais novas, da mais nova para a mais "
        "velha: %r" % (dois,))
    q1 = CC.quadro("labtreinamento", VOZES["labtreinamento"], recentes=um)
    q2 = CC.quadro("labtreinamento", VOZES["labtreinamento"], recentes=dois)
    rep1 = {x["cenas"] for x in q1 if x["repete_recente"]}
    rep2 = {x["cenas"] for x in q2 if x["repete_recente"]}
    assert rep1 == {7}, "com k=1 so o 7 repete: %r" % (rep1,)
    assert rep2 == {7, 9}, "com k=2 o 9 entra: %r" % (rep2,)


def test_ele_REPRODUZ_a_escolha_de_OITO_que_eu_fiz_a_mao():
    """Sem isto a nota nao prova que o instrumento serve a decisao que de fato
    foi tomada. O parque e o do INSTANTE da escolha — a `s090` ja esta no vivo,
    logo usa-lo mediria a rodada seguinte, nao esta."""
    regs = [
        {"pacote": "labtreinamento-s088", "em": "2026-10-19T23:18:02Z"},
        {"pacote": "labtreinamento-s089", "em": "2026-10-20T02:13:52Z"},
    ]
    cen = {"labtreinamento-s088": 7, "labtreinamento-s089": 7}
    rec = CC.recentes_do_canal("labtreinamento", registros=regs,
                               cenas_por_pacote=cen)
    e = CC.escolha("labtreinamento", VOZES["labtreinamento"], recentes=rec,
                   exceto="labtreinamento-s090.json")
    assert e["por_cadencia_geral"]["cenas"] == 7, (
        "a melhor cadencia daquele instante era SETE: %r"
        % (e["por_cadencia_geral"]["cenas"],))
    assert e["por_cadencia_geral"]["repete_recente"], (
        "o sete repetia a `s088` e a `s089` e o instrumento nao viu")
    assert e["por_cadencia_sem_repetir"]["cenas"] == 8, (
        "a escolha que eu fiz a mao foi OITO e o instrumento devolve %r"
        % (e["por_cadencia_sem_repetir"]["cenas"],))


def test_peca_sem_spec_no_disco_NAO_desaparece_da_janela():
    """Ausencia de spec nao e ausencia de publicacao: descartar faria a janela
    de recencia andar para tras em silencio."""
    regs = [{"pacote": "labtreinamento-s999", "em": "2026-10-20T04:00:00Z"},
            {"pacote": "labtreinamento-s998", "em": "2026-10-20T03:00:00Z"}]
    rec = CC.recentes_do_canal("labtreinamento", registros=regs,
                               cenas_por_pacote={"labtreinamento-s998": 6})
    assert len(rec) == 2, "a peca sem spec sumiu: %r" % (rec,)
    assert rec[0]["cenas"] is None, "cenas desconhecidas tem de sair None"
    q = CC.quadro("labtreinamento", VOZES["labtreinamento"], recentes=rec)
    rep = {x["cenas"] for x in q if x["repete_recente"]}
    assert rep == {6}, (
        "cenas None nao pode virar repeticao de nada: %r" % (rep,))


def test_a_frase_da_recencia_tem_UM_dono_e_sai_nos_DOIS_ramos():
    """A frase do teto nasceu duplicada e foi isso que a fez divergir (753).

    **A PRIMEIRA VERSAO DESTE TESTE ESTAVA ERRADA e o modulo estava certo:** eu
    contei a string no arquivo e exigi UMA, e ela aparece DUAS vezes — a frase
    normal e o ramo em que o parque nao tem peca do canal. Os dois moram dentro
    do MESMO dono. O dono e a FUNCAO, nao a contagem de string, e cobrar a
    contagem proibiria o ramo da ausencia, que e justamente o que impede
    "nao repete" de ser dito sem dado.

    E ela tem de sair tanto no canal de mira larga (janela aberta) quanto nos
    dois da pinca (nenhuma janela) — calar na pinca foi o defeito das 03:2x.
    """
    arvore = ast.parse(_fonte())
    donos = []
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef):
            continue
        for n in ast.walk(no):
            if isinstance(n, ast.Constant) and isinstance(n.value, str) \
                    and "RECENCIA no canal" in n.value:
                donos.append(no.name)
    assert donos, "a frase da recencia nao existe no modulo"
    assert set(donos) == {"_linha_da_recencia"}, (
        "a frase da recencia tem mais de um dono: %r" % sorted(set(donos)))
    for c, v in VOZES.items():
        r = CC.relato(c, v)
        assert "RECENCIA no canal" in r, (
            "o relato de %s nao traz a linha da recencia" % c)


def test_a_medida_e_o_pedido_do_dono_continuam_ESCRITOS():
    """Sem o motivo escrito, a rodada seguinte apaga a coluna por ser 'ruido'."""
    fonte = _fonte()
    for marca in ("RECENTES_K", "05:2x", "s088", "s089",
                  "mesma dinamica", "variedade"):
        assert marca in fonte, "a nota perdeu %r" % marca
    assert "REDACAO DECLARADA" in fonte, (
        "o K tem de ir declarado como redacao, nao como medida")


def test_o_codigo_de_saida_continua_ZERO():
    """Isto informa; quem reprova e o portao."""
    for c in VOZES:
        p = subprocess.run([sys.executable, MODULO, c], capture_output=True,
                           text=True, timeout=600)
        assert p.returncode == 0, (
            "%s devolveu %d — isto virou portao" % (c, p.returncode))
        assert "RECENCIA no canal" in p.stdout, (
            "a linha da recencia nao chegou ao stdout de %s" % c)
