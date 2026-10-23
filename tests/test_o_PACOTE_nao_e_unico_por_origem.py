# -*- coding: utf-8 -*-
"""A frase do desempate nomeava o PACOTE, e pacote nao e unico por origem.

Medido em 23/10 as 03:2x, na rodada em que a ambiguidade apareceu. A frase
escrevia `pacote or origem` em TRES lugares — o pacote vencia e o youtube_id
era so o reserva. Varridas as 54 origens dos tres canais, **QUATRO estao em
pacote COMPARTILHADO**, em dois pacotes e dois canais.

Logo quando as duas leituras do desempate escolhem DUAS origens do mesmo
pacote, a linha imprimia o MESMO nome nos dois lados e lia-se como
CONCORDANCIA — com o vao da linha seguinte em 17 capitulos. E a frase manda
`LEIA as duas antes de escrever`.

**A falha e de RELATO e nao de veredito:** a `escolhida` sempre saiu da regra
escrita do `concentracao.py`, que trabalha com o youtube_id.

A forma dos testes: o par de prova e DERIVADO do disco (nomear
`kolejny-poziom-004` seria identidade onde ha propriedade — 743/753/761), a
medida e RECONFERIDA e reprova se o acervo deixar de ter o caso, a contraprova
vai nos DOIS sentidos, e o dono e cobrado por AST.
"""
import ast
import collections
import inspect
import io
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import concentracao as CC      # noqa: E402
import pauta_do_momento as PM  # noqa: E402
import segundo_angulo as SA    # noqa: E402

CANAIS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")

# HISTORIA: o par que produziu o achado. NENHUM assert depende dele — os
# pacotes compartilhados mudam quando a pauta anda, e consumir pauta e o
# trabalho (18/10 as 09:2x).
PAR_DE_03H = ("kolejny-poziom-004", ("iqV7m6tKb5A", "ef_oZmfmdz4"))


def _fonte(fn):
    return textwrap.dedent(inspect.getsource(fn))


def _compartilhados():
    """{pacote: [origens]} para todo pacote com MAIS DE UMA origem, do disco."""
    fora = {}
    for canal in CANAIS:
        pac = collections.defaultdict(list)
        for yid in CC.contagem(canal):
            p = SA.pacote_do_id(yid)
            if p:
                pac[p].append(yid)
        for p, ids in pac.items():
            if len(ids) > 1:
                fora[p] = sorted(ids)
    return fora


# --------------------------------------------------------------- a medida

def test_a_varredura_nao_passa_por_VACUIDADE():
    n = sum(len(CC.contagem(c)) for c in CANAIS)
    assert n >= 30, (
        "so %d origens nos tres canais: a varredura ficou curta e os testes "
        "abaixo passariam sem medir nada" % n)


def test_existe_pacote_COMPARTILHADO_no_disco_e_a_medida_e_RECONFERIDA():
    """Sem o caso no acervo, a ambiguidade nao tem objeto e isto se rele."""
    comp = _compartilhados()
    assert comp, (
        "nenhum pacote do disco tem mais de uma origem: o arquivo PERDEU A "
        "ANCORA. Se a pauta andou e o caso desapareceu, esta nota tem de ser "
        "RELIDA, nao o teste afrouxado.")
    origens = sum(len(v) for v in comp.values())
    assert 2 <= origens <= 20, (
        "origens em pacote compartilhado: %d (eram 4 em 54). Fora dessa ordem "
        "de grandeza a medida envelheceu e tem de ser relida (753)" % origens)


# ------------------------------------------- o dono, e ele nomeia a ORIGEM

def test_o_nome_SEMPRE_carrega_a_origem():
    """Com pacote ou sem ele, o youtube_id tem de aparecer."""
    assert PM._nome_da_origem({"origem": "abc123", "pacote": "canal-004"}) \
        .startswith("abc123")
    assert PM._nome_da_origem({"origem": "abc123", "pacote": None}) == "abc123"
    assert "canal-004" in PM._nome_da_origem(
        {"origem": "abc123", "pacote": "canal-004"}), "o pacote some do nome"


def test_DUAS_origens_do_mesmo_pacote_dao_nomes_DIFERENTES():
    """Era exatamente isto que falhava, e o par sai do DISCO."""
    comp = _compartilhados()
    pacote, ids = sorted(comp.items())[0]
    a = PM._nome_da_origem({"origem": ids[0], "pacote": pacote})
    b = PM._nome_da_origem({"origem": ids[1], "pacote": pacote})
    assert a != b, (a, b)
    # e a leitura ANTIGA de fato as confundia — sem isto, "eu errei" seria
    # afirmacao minha e nao medida
    antigo_a = pacote or ids[0]
    antigo_b = pacote or ids[1]
    assert antigo_a == antigo_b, (
        "a leitura antiga nao confundia este par: o arquivo nao mede o defeito")


def test_a_frase_do_desempate_CHAMA_o_dono_por_AST():
    """Import sem chamada e a classe dos layouts mortos."""
    arv = ast.parse(_fonte(PM._linha_do_desempate))
    chamadas = {n.func.id for n in ast.walk(arv)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "_nome_da_origem" in chamadas, (
        "a frase do desempate nao chama o dono do nome")


def test_a_frase_do_desempate_NAO_remonta_o_nome_por_AST():
    """`pacote or origem` dentro dela seria o segundo dono."""
    arv = ast.parse(_fonte(PM._linha_do_desempate))
    for n in ast.walk(arv):
        if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or):
            chaves = [v.slice.value for v in n.values
                      if isinstance(v, ast.Subscript)
                      and isinstance(getattr(v, "slice", None), ast.Constant)]
            assert not ("pacote" in chaves and "origem" in chaves), (
                "a frase voltou a escolher entre pacote e origem por conta "
                "propria: esse e o defeito de 23/10 as 03:2x")


def test_a_TABELA_segue_com_coluna_propria_para_cada_um():
    """Contraprova no outro sentido: la o nome NAO e ambiguo, e nao se mexe.

    Se a tabela passasse a usar o dono, ela imprimiria o pacote duas vezes na
    mesma linha — o nome dela ja tem uma coluna para a origem e outra para o
    pacote.
    """
    arv = ast.parse(_fonte(PM.relato))
    chamadas = [n for n in ast.walk(arv)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "_nome_da_origem"]
    assert not chamadas, (
        "o `relato` passou a montar o nome da TABELA com o dono do desempate")


# --------------------------------------------- a frase inteira, nos ramos

def test_na_DIVERGENCIA_os_dois_lados_vao_NOMEADOS_com_id():
    """Montado o estado da divergencia, as duas origens tem de aparecer."""
    e = {
        "empatados_na_contagem": ["aaa", "bbb"],
        "escolhida": {"origem": "aaa", "pacote": "canal-004",
                      "reserva": 64, "reserva_sem_declaracao": 35},
        "escolhida_por_reserva_sem_declaracao": {
            "origem": "bbb", "pacote": "canal-004",
            "reserva": 58, "reserva_sem_declaracao": 52},
        "desempate_diverge": True,
        "desempate_vao": {"capitulos": 17, "fracao": 0.327},
    }
    linha = PM._linha_do_desempate(e)
    assert "aaa" in linha and "bbb" in linha, linha
    assert "DIVERGEM" in linha and "17 capitulo" in linha


def test_na_CONCORDANCIA_o_id_tambem_aparece():
    """Contraprova no outro sentido: o ramo que concorda nao perde o id."""
    e = {
        "empatados_na_contagem": ["aaa", "bbb"],
        "escolhida": {"origem": "aaa", "pacote": "canal-004",
                      "reserva": 64, "reserva_sem_declaracao": 35},
        "escolhida_por_reserva_sem_declaracao": {
            "origem": "aaa", "pacote": "canal-004",
            "reserva": 64, "reserva_sem_declaracao": 35},
        "desempate_diverge": False,
    }
    linha = PM._linha_do_desempate(e)
    assert "aaa" in linha and "CONCORDAM" in linha, linha


def test_sem_EMPATE_a_frase_diz_que_nao_ha_objeto():
    linha = PM._linha_do_desempate({"empatados_na_contagem": ["aaa"]})
    assert linha.startswith(PM._PRE) and "nao houve empate" in linha


def test_o_motivo_e_a_medida_continuam_escritos():
    doc = PM._nome_da_origem.__doc__ or ""
    assert "COMPARTILHADO" in doc
    assert "QUATRO" in doc and "54 origens" in doc
    assert "RELATO e nao de veredito" in doc, (
        "o escopo do defeito saiu do docstring: sem ele a rodada seguinte "
        "pode ler isto como erro de escolha de pauta")
    assert "TABELA" in doc, "a razao de a tabela ficar de fora saiu do dono"


# ============================================================ as TRES contas
# A mesma raiz com tres faces: o NOME (acima), os USOS e a RESERVA. As duas
# ultimas entraram em 23/10 as 03:3x, na rodada em que a escolha da pauta caiu
# sobre a origem que, contada por TEXTO, e a SEGUNDA mais usada do canal.

def _canal_com_compartilhado():
    comp = _compartilhados()
    for canal in CANAIS:
        e = PM.escolha(canal)
        if e.get("compartilhados"):
            return canal, e
    pytest.fail("nenhum canal do disco tem pacote compartilhado: o arquivo "
                "PERDEU A ANCORA e os testes abaixo passariam por vacuidade")


def test_os_USOS_por_pacote_SOMAM_as_origens():
    canal, e = _canal_com_compartilhado()
    q = {x["origem"]: x["usos"] for x in e["quadro"]}
    for p, ids in e["compartilhados"].items():
        assert e["usos_por_pacote"][p] == sum(q[i] for i in ids)
        assert e["usos_por_pacote"][p] > max(q[i] for i in ids), (
            "a contagem por TEXTO nao ficou acima da de cada id: o arquivo "
            "nao mede a inflacao")


def test_a_RESERVA_do_pacote_e_a_INTERSECCAO_e_nao_a_maior():
    """A uniao dos shorts dos dois ids consome capitulos do MESMO texto."""
    canal, e = _canal_com_compartilhado()
    for p, ids in e["compartilhados"].items():
        inter, ncap = e["reserva_na_interseccao"][p]
        maiores = [x["reserva"] for x in e["quadro"] if x["origem"] in ids]
        assert inter <= min(maiores), (
            "a interseccao (%d) nao e menor ou igual ao menor dos livres (%r)"
            % (inter, maiores))
        assert inter < max(maiores), (
            "a interseccao igualou o maior: nenhum capitulo e consumido so "
            "pelo irmao, logo o arquivo nao mede a inflacao da reserva")
        assert 0 < ncap, ncap


def test_os_dois_ids_do_pacote_leem_os_MESMOS_capitulos():
    """E a razao de unir: o `nao_mencionados` le UMA spec para os dois ids."""
    canal, e = _canal_com_compartilhado()
    for p, ids in e["compartilhados"].items():
        ns = {SA.nao_mencionados(i)["n_capitulos"] for i in ids}
        assert len(ns) == 1, (
            "os ids de %s leem contagens de capitulo diferentes (%r): a uniao "
            "por pacote perde a razao de ser" % (p, ns))


def test_a_frase_dos_compartilhados_sai_nos_DOIS_ramos():
    com = PM._linha_dos_compartilhados({
        "compartilhados": {"canal-004": ["aaa", "bbb"]},
        "usos_por_pacote": {"canal-004": 8},
        "reserva_na_interseccao": {"canal-004": (53, 74)},
    })
    assert com.startswith(PM._PRE_COMP)
    assert "aaa" in com and "bbb" in com and "8 usos por TEXTO" in com
    assert "53 de 74" in com and "NOMEIA e nao decide" in com
    sem = PM._linha_dos_compartilhados({"compartilhados": {}})
    assert sem.startswith(PM._PRE_COMP) and "nenhum pacote" in sem
    assert "NAO coincidem sempre" in sem, (
        "o ramo sem compartilhado perdeu o aviso de que as contas divergem "
        "em outros canais — sem ele a rodada le a ausencia como garantia")
    assert com != sem


def test_a_frase_tem_UM_dono_e_o_relato_a_CHAMA():
    import ast as _a
    arv = _a.parse(_fonte(PM.relato))
    chamadas = {n.func.id for n in _a.walk(arv)
                if isinstance(n, _a.Call) and isinstance(n.func, _a.Name)}
    assert "_linha_dos_compartilhados" in chamadas
    corpo = io.open(PM.__file__, encoding="utf-8").read()
    assert corpo.count(PM._PRE_COMP) == 1, (
        "o prefixo da frase aparece %d vezes: ele tem de ter UM dono"
        % corpo.count(PM._PRE_COMP))


def test_a_escolhida_NAO_troca_pela_leitura_por_pacote():
    """Contraprova no outro sentido: NOMEAR nao e FILTRAR.

    Se a uniao por pacote mudasse a `escolhida`, uma resolucao em prosa — que
    erra nos dois sentidos, e o `QiaGg03WSR0` e o caso medido — viraria regra.
    """
    canal, e = _canal_com_compartilhado()
    servem = [x for x in e["quadro"]
              if not x["suspeito_de_outro_canal"] and x["reserva"] > 0]
    assert e["escolhida"]["origem"] == servem[0]["origem"], (
        "a escolhida deixou de seguir a regra escrita do `concentracao.py`")


def test_o_limite_que_eu_NAO_consigo_conferir_vai_declarado():
    doc = PM._compartilhados.__doc__ or ""
    assert "negado_por_politica" in doc or "rota" in doc, (
        "saiu do dono a declaracao de que eu nao consigo conferir se os dois "
        "videos sao o mesmo conteudo")
    assert "658" in doc and "(C-2)" in doc, (
        "a procedencia do efeito (contar por id premia duplicata) saiu do dono")
