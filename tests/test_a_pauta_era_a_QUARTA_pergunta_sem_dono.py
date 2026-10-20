"""A pauta era a QUARTA pergunta do passo zero, e nao tinha dono.

Medido em 20/10 as 08:2x, escrevendo o `labtreinamento-s091`. O `passo_zero`
responde tres perguntas — inscritos, canal e cota — e a escolha da ORIGEM ficava
num laco descartavel escrito na linha de comando a cada rodada, com o desempate
aplicado de cabeca. E o item 3 da §10 na QUARTA dimensao: canal (19/10 11:2x),
cota (19/10 23:3x), cenas (20/10 02:2x) e agora pauta.

E o achado maior: o `irmaos_da_origem` existe desde 15/10 (776), responde
exatamente a pergunta que eu respondia lendo cinco shorts no olho, e **modulo
nenhum da fabrica o chamava** — so o teste dele. SEXTA vez da assinatura "nao
chamar quem ja sabe".

E a primeira execucao do instrumento achou um defeito DELE: sem `exceto` na
CONTAGEM, a spec da rodada inflava a contagem da propria origem dela (4 -> 5) e a
escolha mudava. O `exceto` foi ao DONO (`concentracao.contagem`), nao reimplement-
ado aqui.
"""
import ast
import io
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import concentracao as CO  # noqa: E402
import pauta_do_momento as PM  # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "pauta_do_momento.py")
CANAL = "labtreinamento"
# A peca desta rodada e a origem dela. Vai como ANCORA do caso real, e os testes
# de REGRA abaixo nao dependem dela — eles cobram propriedade sobre o disco.
PECA = "labtreinamento-s091"
ORIGEM_DA_PECA = "POBNoY16wG8"


def test_a_varredura_nao_passa_por_VACUIDADE():
    q = PM.quadro(CANAL)
    assert len(q) >= 10, len(q)
    assert any(x["reserva"] > 0 for x in q)
    assert all(x["n_capitulos"] >= 0 for x in q)


def test_ele_REPRODUZ_a_escolha_feita_a_mao():
    """Sem isto a nota nao prova que o instrumento serve a decisao tomada."""
    if not os.path.exists(os.path.join(RAIZ, "fabrica", "specs",
                                       "%s.json" % PECA)):
        pytest.skip("a peca ancora saiu do disco; a regra segue cobrada abaixo")
    e = PM.escolha(CANAL, exceto=PECA)
    assert e["escolhida"] is not None
    assert e["escolhida"]["origem"] == ORIGEM_DA_PECA, e["escolhida"]


def test_o_exceto_vai_ao_DONO_e_muda_a_escolha():
    """Contraprova nos DOIS sentidos, e e o defeito medido na 1a execucao.

    Com a peca da rodada no disco, a origem dela sobe um uso; sem o `exceto` ela
    deixa de ser o minimo e a escolha vira outra.
    """
    if not os.path.exists(os.path.join(RAIZ, "fabrica", "specs",
                                       "%s.json" % PECA)):
        pytest.skip("a peca ancora saiu do disco")
    com = CO.contagem(CANAL, exceto=PECA)
    sem = CO.contagem(CANAL)
    assert sem[ORIGEM_DA_PECA] == com[ORIGEM_DA_PECA] + 1, (sem, com)
    e_com = PM.escolha(CANAL, exceto=PECA)
    e_sem = PM.escolha(CANAL)
    assert e_com["escolhida"]["origem"] != e_sem["escolhida"]["origem"], (
        "sem o `exceto` a escolha deveria mudar — se ela parou de mudar, o "
        "defeito medido desapareceu e esta nota tem de ser RELIDA"
    )


def test_a_REGRA_e_menor_contagem_e_depois_MAIOR_reserva():
    """Cobrada como propriedade sobre o disco, nao por id cravado."""
    e = PM.escolha(CANAL)
    esc = e["escolhida"]
    assert esc is not None
    servem = [x for x in e["quadro"]
              if not x["suspeito_de_outro_canal"] and x["reserva"] > 0]
    assert esc["usos"] == min(x["usos"] for x in servem)
    mesmos = [x for x in servem if x["usos"] == esc["usos"]]
    assert esc["reserva"] == max(x["reserva"] for x in mesmos)


def test_quando_nao_ha_origem_ele_RECUSA_e_aponta_a_regra_h():
    """O outro lado: sem canal no disco, ele nao inventa escolha."""
    e = PM.escolha("canal-que-nao-existe-no-disco")
    assert e["quadro"] == []
    assert e["escolhida"] is None
    r = PM.relato("canal-que-nao-existe-no-disco")
    assert "NENHUMA origem" in r
    assert "regra (h)" in r


def test_a_suspeita_e_NOMEADA_e_nao_filtrada():
    """Com mapa de dono MEDIDO, a origem sai da ESCOLHA sem sair da LISTA.

    O caso e o `QiaGg03WSR0`, medido em 18/10 as 01:2x como longo do
    LabTreinamento declarado por dois shorts do kolejny.
    """
    mapa = {"QiaGg03WSR0": "labtreinamento"}
    e = PM.escolha("kolejny-poziom", dono_medido=mapa)
    ids = [x["origem"] for x in e["quadro"]]
    if "QiaGg03WSR0" not in ids:
        pytest.skip("a origem do caso medido saiu do disco deste canal")
    assert "QiaGg03WSR0" in e["nomeados_como_suspeitos"]
    assert e["escolhida"]["origem"] != "QiaGg03WSR0"
    r = PM.relato("kolejny-poziom", dono_medido=mapa)
    assert "SUSPEITA" in r
    assert "QiaGg03WSR0" in r


def test_sem_mapa_ele_DIZ_que_o_mapa_falta():
    """Ausencia de medicao nao e ausencia de problema."""
    r = PM.relato(CANAL)
    assert "mapa de dono MEDIDO ausente" in r
    e = PM.escolha(CANAL)
    assert e["sem_mapa_de_dono"] is True
    assert e["nomeados_como_suspeitos"] == []


def test_a_frase_do_mapa_tem_UM_dono():
    """Por AST: a frase nasceu duplicada em outro modulo e divergiu (753)."""
    arvore = ast.parse(io.open(FONTE, encoding="utf-8").read())
    donos = set()
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef):
            continue
        for filho in ast.walk(no):
            if (isinstance(filho, ast.Constant)
                    and isinstance(filho.value, str)
                    and "mapa de dono MEDIDO" in filho.value):
                donos.add(no.name)
    assert donos == {"_linha_do_mapa"}, donos


def test_as_QUATRO_contas_sao_DELEGADAS():
    """Por AST. Ler o disco aqui seria o segundo dono — a assinatura que
    congelou a legenda."""
    fonte = io.open(FONTE, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    proibidos = {"glob", "listdir", "open", "walk"}
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call):
            nome = getattr(no.func, "attr", None) or getattr(no.func, "id", None)
            assert nome not in proibidos, nome
    chamados = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute):
            mod = getattr(no.func.value, "id", None)
            if mod:
                chamados.add("%s.%s" % (mod, no.func.attr))
    for esperado in ("CO.contagem", "SA.nao_mencionados", "IO.relato",
                     "CO.origem_de_outro_canal"):
        assert esperado in chamados, (esperado, sorted(chamados))


def test_ele_CHAMA_o_instrumento_que_ninguem_chamava():
    """O `irmaos_da_origem` existia e modulo nenhum o chamava (776).

    Cobrado no RELATO e nao so no import: import sem chamada e a classe dos
    layouts mortos.
    """
    r = PM.relato(CANAL)
    assert "IRMAOS de" in r
    assert "capitulo livre NAO e familia livre" in r


def test_o_codigo_de_saida_e_SEMPRE_zero():
    """Nao e portao: ele informa antes de escrever."""
    p = subprocess.run([sys.executable,
                        os.path.join(RAIZ, "fabrica", "pauta_do_momento.py"),
                        CANAL],
                       capture_output=True, text=True, cwd=RAIZ, timeout=900)
    assert p.returncode == 0, p.stderr[-800:]
    assert "PAUTA DO MOMENTO" in p.stdout


def test_o_MOTIVO_continua_escrito_nos_DOIS_modulos():
    """Conserto sem motivo escrito volta calado, e este e o SEXTO da familia."""
    fonte = io.open(FONTE, encoding="utf-8").read()
    assert "SEXTA vez" in fonte
    assert "776" in fonte
    assert "item 3" in fonte
    dono = io.open(os.path.join(RAIZ, "fabrica", "concentracao.py"),
                   encoding="utf-8").read()
    assert "exceto" in dono
    assert "infla a contagem da PROPRIA origem" in dono


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
