# -*- coding: utf-8 -*-
"""A familia desta rodada saiu de uma FATIA dos capitulos livres.

Medido em 22/10 as 10:3x, escrevendo o `epomeno-epipedo-s093`. O
`segundo_angulo.nao_mencionados` devolve KICKER, e kicker e TITULO — escrever a
partir de titulo e o que a regra (h) chama de inventar conteudo. Logo a rodada
tem de ler o TEXTO, e nao havia instrumento: eu escrevia um laco na hora e
cortava a saida com `sed -n '45,90p'`. Das 59 origens livres daquela leitura, o
texto de 28 (47%) caiu FORA da fatia.

E a assinatura da fatia do proxy (19/10 as 19:2x, ponta VELHA da lista) e do
`tail -10` das formas de treze cenas (21/10 as 23:2x, que me fez escolher um
esqueleto que ja existia): ler uma ponta de uma lista como se fosse a lista.

A forma destes testes e o que vale: a origem de prova e DERIVADA do disco (e
reprova dizendo que perdeu a ancora), a fatia e RECONFERIDA contra o disco em
vez de confiada a prosa (753), a delegacao e por AST nos dois sentidos, e a
contraprova vai nos dois lados — origem sem spec local segue no ramo legitimo da
regra (h), que nao e defeito.
"""
from __future__ import annotations

import ast
import glob
import inspect
import json
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
SPECS = os.path.join(FABRICA, "specs")
if FABRICA not in sys.path:
    sys.path.insert(0, FABRICA)

import segundo_angulo as SA   # noqa: E402

PISO_ORIGENS = 20
# MEDIDO em 22/10 as 10:3x: 59 livres, 28 fora da fatia (47%).
LIVRES_DA_RODADA = 59
FORA_DA_FATIA = 28


def _fonte(fn) -> ast.AST:
    """O corpo da funcao como AST.

    `textwrap.dedent` e nao `inspect.cleandoc`: o cleandoc desindenta a linha do
    `def` e deixa o corpo torto (IndentationError) — medido em 22/10 as 08:3x.
    """
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


def _chamadas(fn) -> set:
    nomes = set()
    for n in ast.walk(_fonte(fn)):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                nomes.add(f.id)
            elif isinstance(f, ast.Attribute):
                nomes.add(f.attr)
                if isinstance(f.value, ast.Name):
                    nomes.add("%s.%s" % (f.value.id, f.attr))
    return nomes


def _origens_com_spec_local() -> list:
    """Toda origem que algum short declara E que resolve para pacote no disco."""
    vistos = set()
    for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        le = sp.get("longo_existente")
        if le:
            vistos.add(le)
    fora = []
    for yid in sorted(vistos):
        if SA.pacote_do_id(yid, SPECS):
            fora.append(yid)
    return fora


def _origem_de_prova() -> str:
    for yid in _origens_com_spec_local():
        d = SA.texto_dos_livres(yid, SPECS)
        if d["n_capitulos"] >= 20 and len(d["livres"]) >= 10:
            return yid
    pytest.fail(
        "ANCORA PERDIDA: nenhuma origem do disco tem 20+ capitulos e 10+ "
        "livres com texto. Sem ela este arquivo nao mede nada — e passar por "
        "vacuidade e o defeito do 743 em forma de glob.")


def test_a_varredura_sai_do_DISCO_e_reprova_por_vacuidade():
    origens = _origens_com_spec_local()
    assert len(origens) >= PISO_ORIGENS, (
        "so %d origem(ns) com spec local; abaixo de %d a varredura nao mede "
        "nada" % (len(origens), PISO_ORIGENS))


def test_ele_devolve_o_TEXTO_e_nao_so_o_kicker():
    """O defeito era responder TITULO a quem precisa do texto (regra h)."""
    yid = _origem_de_prova()
    d = SA.texto_dos_livres(yid, SPECS)
    assert d["livres"], "nenhum livre devolvido em %s" % yid
    com_texto = [x for x in d["livres"] if x["nar"]]
    assert com_texto, (
        "todos os livres de %s voltaram sem narracao — ou a spec nao tem `nar`, "
        "ou o instrumento voltou a devolver so o kicker" % yid)
    for x in d["livres"]:
        assert set(x) >= {"indice", "kicker", "nar", "sem_narracao",
                          "cenas_do_kicker"}
        assert bool(x["nar"]) != bool(x["sem_narracao"]), (
            "cena %d: `nar` e `sem_narracao` tem de ser um ou o outro, senao "
            "vazio e ausencia ficam indistinguiveis (17/10)" % x["indice"])


def test_o_conjunto_livre_e_DELEGADO_ao_nao_mencionados_por_AST():
    ch = _chamadas(SA.texto_dos_livres)
    assert "nao_mencionados" in ch, (
        "o conjunto livre tem de sair do `nao_mencionados` — recomputa-lo aqui "
        "seria o SEGUNDO dono do indicio de capitulo livre, com o ponto cego do "
        "kicker repetido divergindo entre os dois")
    for proibido in ("shorts_da_origem", "_sem_reserva"):
        assert proibido not in ch, (
            "`%s` dentro do `texto_dos_livres` reimplementa a comparacao do "
            "dono" % proibido)


def test_a_leitura_do_longo_tem_UM_dono_por_AST():
    for fn in (SA.texto_dos_livres, SA.capitulos_do_pacote):
        ch = _chamadas(fn)
        assert "_cenas_do_longo" in ch, (
            "%s nao chama o dono da leitura do longo" % fn.__name__)
        for proibido in ("load", "open"):
            assert proibido not in ch, (
                "%s abre a spec por conta propria (`%s`): duas leituras do "
                "mesmo arquivo sao dois donos da forma dela"
                % (fn.__name__, proibido))


def test_ele_NAO_fatia_por_AST():
    """Fatia e o defeito que ele conserta — nao pode reaparecer dentro dele."""
    for fn in (SA.texto_dos_livres, SA.relato_dos_livres):
        for n in ast.walk(_fonte(fn)):
            if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice):
                pytest.fail(
                    "%s FATIA uma lista. Ler uma ponta como se fosse a lista e "
                    "exatamente o defeito de 19/10 as 19:2x, de 21/10 as 23:2x "
                    "e desta rodada." % fn.__name__)


def test_a_FATIA_de_fato_perdia_os_livres_RECONFERIDO_no_disco():
    """Sem esta medida, 'eu errei a fatia' seria afirmacao minha e nao medida."""
    origens = _origens_com_spec_local()
    perdem = 0
    medidas = 0
    for yid in origens:
        d = SA.texto_dos_livres(yid, SPECS)
        idx = [x["indice"] for x in d["livres"]]
        if len(idx) < 10:
            continue
        medidas += 1
        corte = d["n_capitulos"] // 2            # a fatia FINAL, como a minha
        fora = [i for i in idx if i < corte]
        if len(fora) >= 0.4 * len(idx):
            perdem += 1
    assert medidas >= 10, (
        "so %d origem(ns) com 10+ livres: a medida nao se sustenta" % medidas)
    assert perdem > medidas / 2, (
        "a fatia FINAL perde 40%% dos livres em so %d de %d origens. Se isso "
        "caiu, releia esta nota em vez de mover o numero: ela existe porque em "
        "22/10 a fatia deixou %d de %d livres sem leitura."
        % (perdem, medidas, FORA_DA_FATIA, LIVRES_DA_RODADA))


def test_o_kicker_REPETIDO_devolve_as_DUAS_cenas():
    """O ponto cego do `nao_mencionados` reaparece uma camada abaixo."""
    alvo = None
    for yid in _origens_com_spec_local():
        d = SA.texto_dos_livres(yid, SPECS)
        if d["kickers_repetidos"]:
            alvo = (yid, d)
            break
    if alvo is None:
        pytest.fail(
            "ANCORA PERDIDA: nenhuma origem do disco tem kicker repetido entre "
            "os livres. O docstring do `nao_mencionados` mede 71 de 134 specs "
            "de longo com kicker repetido — se isso zerou, o ponto cego mudou "
            "e esta nota se rele.")
    yid, d = alvo
    k = d["kickers_repetidos"][0]
    cenas = [x for x in d["livres"] if x["kicker"] == k]
    assert len(cenas) >= 2, (
        "o kicker %r e repetido em %s e voltou uma cena so: filtrar para uma "
        "esconde metade do texto justamente onde o `nao_mencionados` ja e cego"
        % (k, yid))
    assert len({x["indice"] for x in cenas}) == len(cenas)
    for x in cenas:
        assert x["cenas_do_kicker"] >= 2


def test_cena_livre_SEM_narracao_sai_NOMEADA(tmp_path):
    """Parque PROPRIO: o disco pode nao ter o caso, e ancorar no vivo seria
    identidade onde ha propriedade (743/753/761)."""
    # Raiz com a convencao `<raiz>/fabrica/specs`: desde 22/10 as 12:4x o
    # `texto_dos_livres` deriva a raiz via `raiz_do_dir_specs`, que LEVANTA em
    # diretorio fora dela — o parque PROPRIO tem de seguir a convencao.
    os.makedirs(os.path.join(str(tmp_path), "fabrica", "specs"))
    d = os.path.join(str(tmp_path), "fabrica", "specs")
    # O `slug` do longo e o CANAL e nao o pacote: o `nomes_de_spec` tira do
    # vocabulario todo nome que e slug de alguma spec (o falso positivo de
    # 12/10), logo `slug: "canalx-001"` tornaria a origem irresolvivel. A
    # primeira versao deste teste errava isso — era o TESTE, nao o modulo.
    longo = {
        "slug": "canalx", "pacote": "canalx-001", "idioma": "pt-BR",
        "longo": [{"layout": "titulo", "kicker": "Com texto",
                   "nar": "Uma frase."},
                  {"layout": "titulo", "kicker": "Sem texto", "nar": ""}],
        "short": [], "copy": "# canalx-001",
    }
    short = {
        "slug": "canalx-s001", "pacote": "canalx-s001", "idioma": "pt-BR",
        "longo_existente": "VID0000000X", "longo": [],
        "short": [{"layout": "titulo", "kicker": "a", "nar": "b"}],
        "copy": "# canalx-s001\n\n## FONTES\ncanalx-001\n",
    }
    json.dump(longo, open(os.path.join(d, "canalx-001.json"), "w",
                          encoding="utf-8"))
    json.dump(short, open(os.path.join(d, "canalx-s001.json"), "w",
                          encoding="utf-8"))
    r = SA.texto_dos_livres("VID0000000X", d)
    assert r["pacote"] == "canalx-001"
    kickers = {x["kicker"] for x in r["livres"]}
    assert "Sem texto" in kickers, (
        "a cena de narracao vazia DESAPARECEU da lista — vazio de instrumento "
        "nao prova ausencia (17/10)")
    assert r["sem_narracao"], "ela tem de sair NOMEADA, nao so vazia"
    assert "sem narracao" in SA.relato_dos_livres("VID0000000X", d)


def test_contraprova_origem_SEM_spec_local_segue_no_ramo_LEGITIMO():
    """Regra (h) nao e defeito: trocar uma cegueira por outra seria o avesso."""
    r = SA.texto_dos_livres("NAOEXISTE00", SPECS)
    assert r["pacote"] is None
    assert r["livres"] == []
    rel = SA.relato_dos_livres("NAOEXISTE00", SPECS)
    assert "regra h" in rel.lower()
    assert "nao e defeito" in rel.lower().replace("ã", "a")


def test_a_CONTAGEM_vem_na_primeira_linha_e_todas_as_linhas_saem():
    yid = _origem_de_prova()
    d = SA.texto_dos_livres(yid, SPECS)
    linhas = SA.relato_dos_livres(yid, SPECS).split("\n")
    assert str(len(d["livres"])) in linhas[0], (
        "a contagem tem de vir na PRIMEIRA linha: e ela que torna um corte na "
        "leitura visivel em vez de silencioso")
    impressas = [l for l in linhas if l.startswith("  ") and "|" in l]
    assert len(impressas) == len(d["livres"]), (
        "o relato imprimiu %d de %d capitulos livres"
        % (len(impressas), len(d["livres"])))


def test_o_exceto_chega_nos_DOIS_sentidos():
    yid = _origem_de_prova()
    base = SA.texto_dos_livres(yid, SPECS)
    shorts = base["shorts"]
    assert shorts, "a origem de prova tem de ter irmao, senao `exceto` nao mede"
    com = SA.texto_dos_livres(yid, SPECS, exceto=shorts[0])
    assert len(com["livres"]) >= len(base["livres"]), (
        "tirar um irmao da varredura so pode AUMENTAR o conjunto livre")
    vazio = SA.texto_dos_livres(yid, SPECS, exceto="nao-existe-999")
    assert len(vazio["livres"]) == len(base["livres"]), (
        "`exceto` de peca inexistente nao pode filtrar nada")


def test_NAO_virou_portao():
    import prontidao
    fonte = ast.parse(open(prontidao.__file__, encoding="utf-8").read())
    for n in ast.walk(fonte):
        if isinstance(n, ast.Call):
            f = n.func
            nome = getattr(f, "attr", None) or getattr(f, "id", None)
            assert nome not in ("texto_dos_livres", "relato_dos_livres"), (
                "o `prontidao` passou a chamar o instrumento: ele INFORMA e nao "
                "reprova, pelo argumento do `mira.py`")
    # por AST e nao por prosa: o modulo pode CITAR o nome para se explicar.


def test_o_motivo_e_a_medida_continuam_escritos():
    doc = SA.texto_dos_livres.__doc__ or ""
    assert str(FORA_DA_FATIA) in doc and str(LIVRES_DA_RODADA) in doc, (
        "a medida (%d de %d) saiu do docstring — sem ela a rodada seguinte "
        "reescreve o laco com fatia" % (FORA_DA_FATIA, LIVRES_DA_RODADA))
    assert "regra (h)" in doc or "regra h" in doc
    for marca in ("19/10", "21/10"):
        assert marca in doc, (
            "a familia da fatia (%s) saiu do docstring" % marca)


def test_a_PAUTA_chama_o_instrumento_por_AST():
    """Instrumento que a rodada nao chama e a classe dos layouts mortos.

    O `irmaos_da_origem` existiu cinco dias sem chamador nenhum fora do teste
    dele (20/10 as 08:2x), e foi por isso que eu lia cinco shorts no olho. Aqui
    o mesmo: a pauta tem de IMPRIMIR o texto dos livres, nao so poder.
    """
    import pauta_do_momento as PM
    ch = _chamadas(PM.relato)
    assert ("relato_dos_livres" in ch or "SA.relato_dos_livres" in ch), (
        "o `pauta_do_momento.relato` nao chama o `relato_dos_livres`: a rodada "
        "voltaria a escrever o laco com fatia na linha de comando")


def test_a_PAUTA_imprime_o_texto_dos_livres_de_verdade():
    import pauta_do_momento as PM
    yid = _origem_de_prova()
    canal = None
    for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        if sp.get("longo_existente") == yid:
            import canal as CN
            canal = CN.do_pacote(sp.get("pacote") or "")
            break
    assert canal, "ANCORA PERDIDA: nao achei o canal da origem de prova"
    rel = PM.relato(canal)
    assert "TEXTO DOS LIVRES" in rel, (
        "a pauta nao imprimiu o texto dos livres — chamada sem saida e o mesmo "
        "que nao chamar")
