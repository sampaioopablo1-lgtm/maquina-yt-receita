# -*- coding: utf-8 -*-
"""O `contagem_de_cenas` recusava a janela e CALAVA a cadencia.

Medido em 20/10 as 03:2x, na PRIMEIRA rodada depois de ele existir. O `relato`
devolvia UMA linha quando nenhuma contagem abre janela nos dois mundos, e jogava
fora o `quadro` que ele acabara de calcular — inclusive a cadencia, que **nao
depende da janela**. Sao **38 dos 57 pares (canal, contagem)** sem uma palavra,
isto e DOIS dos tres canais.

E a dimensao que faltava e a do pedido do dono de 19/10 (*"a mesma dinamica...
em todos os canais"*): qual contagem de cena a FROTA nunca usou. Ela morava no
`esqueleto_entre_canais`, que este modulo nao chamava.
"""
import ast
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
sys.path.insert(0, FABRICA)

import contagem_de_cenas as CC            # noqa: E402
import esqueleto_entre_canais as EC       # noqa: E402

MODULO = os.path.join(FABRICA, "contagem_de_cenas.py")

VOZES = {
    "labtreinamento": "pt-BR-ThalitaMultilingualNeural",
    "epomeno-epipedo": "el-GR-NestorasNeural",
    "kolejny-poziom": "pl-PL-MarekNeural",
}
PECA_DA_RODADA = "epomeno-epipedo-s072.json"


def test_a_varredura_da_frota_sai_do_DISCO_e_nao_e_vazia():
    """Sem spec no disco todo teste daqui passa por vacuidade (743)."""
    pc = CC.contagens_da_frota()
    assert sum(pc.values()) >= 200, (
        "menos de 200 pecas com short na varredura: a frota tem 366 — "
        "varredura encolhida faz 'inedita' virar sempre verdade"
    )
    assert len(pc) >= 8, f"so {len(pc)} tamanhos distintos: {sorted(pc)}"


def test_a_contagem_da_frota_e_DELEGADA_e_nao_recontada():
    """Recontar aqui criaria o segundo dono da varredura do disco."""
    assert CC.contagens_da_frota() == EC.quadro()["por_contagem_de_cena"]

    arv = ast.parse(open(MODULO, encoding="utf-8").read())
    proibidos = {"glob", "listdir", "walk", "iglob"}
    achados = []
    for no in ast.walk(arv):
        if isinstance(no, ast.Call):
            f = no.func
            nome = getattr(f, "attr", None) or getattr(f, "id", None)
            if nome in proibidos:
                achados.append(nome)
    assert not achados, (
        f"o modulo varre o disco por conta propria ({achados}): a varredura tem "
        "UM dono, o `esqueleto_entre_canais`"
    )


def test_os_DOIS_lados_existem_e_a_pinca_segue_FECHADA_em_dois_canais():
    """Se a pinca abrir nos tres, esta nota se rele em vez de ficar."""
    abertas = {}
    for canal, voz in VOZES.items():
        abertas[canal] = CC.escolha(canal, voz)["abertas"]
    com = [c for c, n in abertas.items() if n]
    sem = [c for c, n in abertas.items() if not n]
    assert com, f"nenhum canal abre janela: {abertas} — sem o lado aberto o arquivo nao mede o contraste"
    assert sem, (
        f"TODOS os canais abrem janela agora ({abertas}): a pinca do 740/748 "
        "abriu e o defeito do silencio perdeu o objeto — releia a nota"
    )
    assert len(sem) == 2, f"esperava DOIS canais na pinca, achei {sem}"


def test_com_a_pinca_FECHADA_o_relato_ORDENA_em_vez_de_calar():
    """Era este o defeito: uma linha e nada mais."""
    r = CC.relato("epomeno-epipedo", VOZES["epomeno-epipedo"])
    linhas = [x for x in r.splitlines() if "cadencia" in x and "cenas" in x]
    assert len(linhas) >= 3, (
        "o relato da pinca voltou a calar: ele tem de ordenar por cadencia, "
        f"que NAO depende da janela.\n{r}"
    )
    assert "pinca" in r, "o relato parou de nomear a pinca do 740/748"
    assert "EXPOSICAO" in r, "o relato parou de mandar declarar a exposicao"
    assert "INEDITA" in r, "o relato nao nomeia o tamanho que a frota nunca usou"


def test_a_cadencia_e_a_novidade_saem_nos_DOIS_ramos():
    """Elas nao dependem da janela, logo nao podem sumir com ela."""
    for canal, voz in VOZES.items():
        e = CC.escolha(canal, voz)
        assert e["por_cadencia_geral"] is not None, canal
        assert "ineditas" in e, canal
        assert "por_novidade" in e, canal
    fechado = CC.escolha("epomeno-epipedo", VOZES["epomeno-epipedo"])
    assert fechado["por_cadencia"] is None, (
        "escolha POR JANELA com a pinca fechada tem de seguir None: inventar "
        "uma esconderia a pinca em vez de a nomear"
    )


def test_o_exceto_vale_nos_DOIS_sentidos():
    """Na hora de escolher, a spec da rodada pode ja estar no disco."""
    voz = VOZES["epomeno-epipedo"]
    com = CC.escolha("epomeno-epipedo", voz)
    sem = CC.escolha("epomeno-epipedo", voz, exceto=PECA_DA_RODADA)
    alvo = os.path.join(FABRICA, "specs", PECA_DA_RODADA)
    if not os.path.exists(alvo):
        pytest.skip(f"{PECA_DA_RODADA} saiu do disco")
    assert set(sem["ineditas"]) > set(com["ineditas"]), (
        "excluir a peca da rodada tem de DEVOLVER o tamanho dela a lista de "
        f"ineditas: com={com['ineditas']} sem={sem['ineditas']}"
    )
    assert 14 in sem["ineditas"] and 14 not in com["ineditas"]


def test_ele_REPRODUZ_a_escolha_de_CATORZE_que_eu_fiz_a_mao():
    """Sem isto a nota nao prova que ele serve a decisao que foi tomada."""
    alvo = os.path.join(FABRICA, "specs", PECA_DA_RODADA)
    if not os.path.exists(alvo):
        pytest.skip(f"{PECA_DA_RODADA} saiu do disco")
    e = CC.escolha("epomeno-epipedo", VOZES["epomeno-epipedo"],
                   exceto=PECA_DA_RODADA)
    assert e["por_novidade"]["cenas"] == 14, (
        "a melhor cadencia entre os tamanhos nunca usados deixou de ser 14: "
        f"deu {e['por_novidade']['cenas']}. Era 14 a escolha de 20/10 as 03:0x, "
        "feita a mao antes deste conserto"
    )
    assert e["por_cadencia_geral"]["cenas"] == 14


def test_ineditas_e_PROPRIEDADE_e_nao_lista_cravada():
    """Se a frota usar todos os tamanhos, o modulo diz isso em vez de calar."""
    pc = CC.contagens_da_frota()
    faixa = range(CC.MIN_CENAS, CC.MAX_CENAS + 1)
    usados = [n for n in faixa if pc.get(n)]
    nunca = [n for n in faixa if not pc.get(n)]
    assert usados, "a frota nao usa tamanho nenhum entre 2 e 20"
    assert nunca, (
        "a frota JA usou todos os tamanhos de 2 a 20: a novidade de TAMANHO "
        "acabou e esta nota tem de ser relida — a de FORMA fica com o "
        "`esqueleto_entre_canais`"
    )
    r = CC.relato("epomeno-epipedo", VOZES["epomeno-epipedo"])
    assert str(nunca[0]) in r


def test_o_codigo_de_saida_e_SEMPRE_zero():
    """Isto informa; quem reprova e o `prontidao`."""
    for canal in VOZES:
        p = subprocess.run([sys.executable, MODULO, canal],
                           capture_output=True, text=True, cwd=RAIZ)
        assert p.returncode == 0, (canal, p.returncode, p.stderr[-400:])
        assert "cadencia" in p.stdout, (canal, p.stdout[:300])


def test_a_MEDIDA_do_silencio_continua_escrita_no_modulo():
    """Conserto sem o numero que o motivou volta calado."""
    t = open(MODULO, encoding="utf-8").read()
    assert "38 dos 57" in t, (
        "a medida do silencio (38 de 57 pares (canal, contagem)) saiu do "
        "modulo — sem ela a rodada seguinte nao sabe por que o ramo existe"
    )
    assert "esqueleto_entre_canais" in t
    assert "em todos os canais" in t.lower(), (
        "o pedido do dono que nomeia a dimensao da novidade saiu do modulo"
    )
