"""O 000 tambem e "a resposta nao tinha onde ser gravada". 20/10/2026, 09:3x.

Em 19/10 as 23:4x eu acrescentei o modo `sem_egresso` com um discriminador: um
HOST NEUTRO na mesma chamada. Nesta rodada — a decima primeira seguida em que eu
escrevia `sem_egresso` — a sonda foi

    curl -s -o /tmp/o.html -w '%{http_code}' -m 25 <url>

num sandbox onde `/tmp/o.html` nao pode ser aberto. **Quando o `-o` falha o curl
sai em 23 e o `%{http_code}` imprime 000** — o MESMO 000 que o ramo le como "a
rede nao sai" —, e os TRES hosts, o neutro inclusive, voltaram 000. Logo
`neutro_respondeu=False` era ELE MESMO insuficiente: *"a rede nao sai"* e *"a
resposta nao tinha onde ser gravada"* nao se distinguem pelo 000 sozinho.

O discriminador novo e um CONTROLE DE ESCRITA na mesma chamada. Refeita a sonda
com destino gravavel, o `touch` passou e o arquivo da resposta continuou nao
existindo — ai `sem_egresso` esta medido.

O que isto RETRATA: o ROTULO das rodadas anteriores, afirmado sem esse controle.
A CONSEQUENCIA delas nao muda — nao havia leitura, logo nao havia ponto de
residuo e a peca foi parqueada. Cai a certeza sobre a CAUSA.
"""
import ast
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FABRICA, "vivacidade_publica.py")
sys.path.insert(0, FABRICA)

import vivacidade_publica as VP  # noqa: E402

PAREDE = ("x" * 1200) + "CONSENT" + ("y" * 1200)
SORRY = "https://www.google.com/sorry/index?continue=..."


def test_o_caso_MEDIDO_desta_rodada_sai_sem_egresso():
    """Neutro calado E a sonda podia gravar: foi o que de fato se mediu."""
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=False, sonda_pode_gravar=True) == "sem_egresso"


def test_a_PRIMEIRA_sonda_desta_rodada_nao_decide_nada():
    """O destino nao era gravavel, logo o 000 nao informa sobre a rede."""
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=False,
        sonda_pode_gravar=False) == "indeterminado"


def test_SEM_o_controle_de_escrita_ele_RECUSA_em_vez_de_escolher():
    """E a retratacao: era exatamente esta chamada que eu vinha fazendo."""
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=False) == "indeterminado"


def test_as_DUAS_sondas_tem_de_falar_e_nenhuma_basta():
    """Contraprova nos dois sentidos: cada controle sozinho nao conclui.

    Sem este par, bastaria devolver `indeterminado` sempre (ou `sem_egresso`
    sempre) para o arquivo passar.
    """
    so_escrita = VP.modo_de_fechamento("", "", sonda_pode_gravar=True)
    so_neutro = VP.modo_de_fechamento("", "", neutro_respondeu=False)
    assert so_escrita == "indeterminado", so_escrita
    assert so_neutro == "indeterminado", so_neutro
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=False, sonda_pode_gravar=True) == "sem_egresso"


def test_o_neutro_RESPONDENDO_nao_vira_sem_egresso_com_escrita_boa():
    """O caso que eu NAO medi (neutro responde, YouTube nao) segue sem nome."""
    assert VP.modo_de_fechamento(
        "", "", neutro_respondeu=True, sonda_pode_gravar=True) == "indeterminado"


def test_os_outros_modos_NAO_dependem_do_controle_novo():
    """Parede e limite vem de corpo/location, nao de sonda nenhuma."""
    for grava in (None, True, False):
        assert VP.modo_de_fechamento(
            PAREDE, "", neutro_respondeu=False,
            sonda_pode_gravar=grava) == "consentimento"
        assert VP.modo_de_fechamento(
            "", SORRY, neutro_respondeu=False,
            sonda_pode_gravar=grava) == "limite"
        assert VP.modo_de_fechamento(
            '"lengthSeconds":"44"', "", sonda_pode_gravar=grava) == "aberta"


def test_o_controle_de_escrita_esta_na_ASSINATURA():
    """Por AST: parametro removido faria os testes acima passar por default."""
    arvore = ast.parse(io.open(MODULO, encoding="utf-8").read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "modo_de_fechamento"]
    assert len(alvo) == 1
    nomes = [a.arg for a in alvo[0].args.args]
    assert "sonda_pode_gravar" in nomes, nomes
    assert "neutro_respondeu" in nomes, nomes


def test_nenhum_modo_novo_entrou_com_o_conserto():
    """O quarto modo que eu nao medi continua proibido (§10)."""
    arvore = ast.parse(io.open(MODULO, encoding="utf-8").read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "modo_de_fechamento"][0]
    devolvidos = set()
    for no in ast.walk(alvo):
        if isinstance(no, ast.Return) and no.value is not None:
            for dentro in ast.walk(no.value):
                if isinstance(dentro, ast.Constant) and isinstance(dentro.value,
                                                                   str):
                    devolvidos.add(dentro.value)
    assert devolvidos == {"limite", "consentimento", "aberta",
                          "sem_egresso", "indeterminado"}, devolvidos


def test_a_RETRATACAO_continua_escrita_no_modulo():
    """Sem ela a rodada seguinte rele `sem_egresso` como medido desde sempre."""
    fonte = io.open(MODULO, encoding="utf-8").read()
    for marca in ("sonda_pode_gravar", "RETRATA", "CONTROLE DE ESCRITA",
                  "23", "000"):
        assert marca in fonte, (
            "conserto sem o motivo escrito volta calado: falta %r" % marca)
    assert "CONSEQUENCIA" in fonte, (
        "a consequencia das rodadas anteriores NAO muda, e isso tem de ir dito")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
