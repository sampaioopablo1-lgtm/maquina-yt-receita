"""O instrumento existia e eu refiz a conta a mao em CINCO rodadas seguidas.

O DEFEITO, medido em 19/10 as 11:2x. O `concentracao_frota.escolha_do_momento`
conta a janela movel de 24 h por canal, desempata pelo que esta ha mais tempo sem
publicar e devolve `escolhido` — e nas rodadas das 08:0x, 09:0x, 10:0x e 11:1x eu
escrevi, em vez de o chamar, um laco Python descartavel sobre
`docs/pendente/duracoes-a-medir.jsonl`.

**E o docstring do proprio modulo diz a razao de ele existir**, em letra: *"ele
existe porque eu vinha contando o DIA com um regex escrito a mao na linha de
comando, a cada rodada — e a §10 da rotina diz, no item 3, que todo numero que eu
calculo a mao vira um erro meu"*. Logo eu cometi, DENTRO do conserto do item 3,
exatamente o defeito que ele conserta. E a classe dos layouts mortos virada do
avesso: lah o codigo nao era chamado por ninguem; aqui ele nao era chamado pelo
proprio autor.

**E OS DOIS NUMEROS BATERAM, o que e SORTE e nao metodo** — eles vem de ARQUIVOS
DIFERENTES, cada um gravado por um passo meu diferente:

    docs/pendente/videos-a-inserir.sql     <- `registro_videos` (o instrumento le este)
    docs/pendente/duracoes-a-medir.jsonl   <- `duracao_a_medir` (a minha conta lia este)

**Dois donos do mesmo fato**, e e a assinatura que congelou a legenda, parou a
mira de conferir e poe job inventado na serie. Se eu esquecer UM dos dois passos
numa rodada, os arquivos divergem **em silencio** e a escolha de canal passa a
sair de um parque incompleto.

Este arquivo cruza os dois, como o `test_o_job_citado_na_serie_bate_com_o_PARQUE`
cruza a serie com o parque — e **reprova quando divergem**, em vez de deixar a
coincidencia passar por conferencia.
"""

import datetime
import json
import os
import re
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import concentracao_frota as CF  # noqa: E402

PARQUE = os.path.join(RAIZ, "docs", "pendente", "duracoes-a-medir.jsonl")
AGORA = datetime.datetime(2026, 10, 19, 11, 14, tzinfo=datetime.timezone.utc)


def _do_parque(janela_h=24.0, agora=AGORA):
    """A contagem pelo OUTRO dono: o parque das duracoes."""
    corte = agora - datetime.timedelta(hours=janela_h)
    fora = {c: 0 for c in CF.FROTA}
    vistos = set()
    for linha in open(PARQUE, encoding="utf-8"):
        linha = linha.strip()
        if not linha:
            continue
        d = json.loads(linha)
        yid, em = d.get("youtube_id"), d.get("em")
        if not yid or not em or yid in vistos:
            continue
        t = datetime.datetime.fromisoformat(em.replace("Z", "+00:00"))
        if t >= corte:
            vistos.add(yid)
            canal = str(d.get("pacote", "")).rsplit("-s", 1)[0]
            if canal in fora:
                fora[canal] += 1
    return fora


def test_o_instrumento_EXISTE_e_devolve_o_escolhido():
    """Se ele deixar de existir, a rodada volta ao laco descartavel."""
    e = CF.escolha_do_momento(24.0, agora=AGORA)
    for chave in ("contagem", "ultima", "escolhido", "empatados", "houve_empate"):
        assert chave in e, f"a chave {chave} saiu do veredito"
    assert set(e["contagem"]) == set(CF.FROTA)
    assert e["escolhido"] in CF.FROTA or e["escolhido"] is None


def test_os_DOIS_DONOS_do_mesmo_fato_concordam():
    """O cruzamento que a coincidencia de 19/10 escondia.

    Reprova quando os arquivos divergem: isso significa que um dos dois passos do
    registro ficou para tras numa rodada, e a escolha de canal passou a sair de um
    parque incompleto sem ninguem ver.
    """
    do_sql = CF.escolha_do_momento(24.0, agora=AGORA)["contagem"]
    do_parque = _do_parque()
    assert do_sql == do_parque, (
        f"os dois donos divergem: o .sql diz {do_sql} e o .jsonl diz {do_parque}. "
        "Um dos dois passos do registro (registro_videos / duracao_a_medir) nao "
        "rodou numa rodada — confira os dois antes de escolher canal."
    )
    assert sum(do_parque.values()) >= 3, (
        f"a janela de 24 h tem {sum(do_parque.values())} pecas — com tao poucas "
        "este teste passa por vacuidade, o defeito do 743 em forma de glob."
    )


def test_o_desempate_e_pelo_MAIS_TEMPO_sem_peca():
    """Com empate na contagem, decide quem publicou ha mais tempo.

    Era isso que eu fazia a mao, e e isso que o instrumento ja fazia. Ancorado no
    estado real de 19/10 as 11:1x, onde dois canais empatam em oito.
    """
    e = CF.escolha_do_momento(24.0, agora=AGORA)
    if not e["houve_empate"]:
        pytest.skip("nao ha empate neste estado do parque — nada a desempatar")
    assert len(e["empatados"]) >= 2
    ultimas = {c: e["ultima"].get(c) for c in e["empatados"]}
    assert all(ultimas.values()), f"empatado sem data de ultima peca: {ultimas}"
    mais_antigo = min(ultimas, key=lambda c: ultimas[c])
    assert e["escolhido"] == mais_antigo, (
        f"o desempate escolheu {e['escolhido']} e a mais antiga e de "
        f"{mais_antigo} ({ultimas})"
    )


def test_a_contagem_le_DATA_e_nao_o_arquivo_inteiro():
    """Janela de uma hora tem de devolver menos que a de 24 h.

    Sem isto o `desde` poderia estar sendo ignorado e a contagem seria do acervo
    — que e exatamente a cegueira do 762 que este modulo nasceu para consertar.
    """
    curta = CF.escolha_do_momento(1.0, agora=AGORA)["contagem"]
    longa = CF.escolha_do_momento(24.0, agora=AGORA)["contagem"]
    assert sum(curta.values()) < sum(longa.values()), (
        "a janela nao filtra por data: o contador voltou a medir acervo"
    )


def test_o_MOTIVO_de_ele_existir_continua_escrito():
    """Conserto sem motivo escrito volta calado — e este voltou de outra forma."""
    fonte = open(os.path.join(RAIZ, "fabrica", "concentracao_frota.py")).read()
    assert "regex escrito a mao" in fonte, (
        "o docstring perdeu a frase que explica por que o modulo existe — e e "
        "justamente ela que eu nao li em cinco rodadas"
    )
    assert "762" in fonte


def test_a_regra_de_CHAMAR_o_instrumento_esta_no_CLAUDE_md():
    """Se a nota sair do CLAUDE.md, a rodada seguinte volta ao laco a mao."""
    doc = open(os.path.join(RAIZ, "CLAUDE.md"), encoding="utf-8").read()
    assert "escolha_do_momento" in doc, (
        "o CLAUDE.md nao nomeia o instrumento que decide o canal — sem isso a "
        "rodada seguinte reescreve o laco descartavel, como eu fiz cinco vezes"
    )
