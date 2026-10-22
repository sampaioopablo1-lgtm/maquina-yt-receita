# -*- coding: utf-8 -*-
"""A copy declarava os numerais falados, e eu os conferia relendo.

Medido em 21/10/2026. Toda copy desta geracao traz, no
`## AVISO SOBRE OS NUMEROS`, uma frase do tipo *"o unico numeral falado e X"* —
e **na PRIMEIRA vez que ela foi conferida mecanicamente estava INCOMPLETA**, na
peca de duas horas antes: o `epomeno-epipedo-s083` declara `τρεις` e `δύο` e a
narracao fala tambem **τρία**.

O CONTEUDO estava certo e a DECLARACAO errada — `τρία πράγματα` conta a lista da
propria peca, igual aos dois declarados, e nao viola a regra (g). O que estava
falso era a palavra *"unicos"*. **Declaracao que lista dois de tres e pior que
declaracao ausente**, porque convida a rodada seguinte a confiar nela.

O instrumento LISTA e NAO julga, e NAO alarma: 144 das 259 specs de short solto
falam algum numeral por extenso.
"""
import ast
import glob
import json
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def _mod(nome):
    spec = importlib.util.spec_from_file_location(
        nome, RAIZ / "fabrica" / ("%s.py" % nome))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


NF = _mod("numerais_falados")


def test_o_caso_MEDIDO_da_s083_e_reproduzido():
    """A peca ancora: declaracao com dois, narracao com tres.

    Se ela sair do disco o teste SKIPA dizendo que perdeu a ancora, em vez de
    passar por vacuidade — e a propriedade segue cobrada nos testes abaixo.
    """
    p = RAIZ / "fabrica" / "specs" / "epomeno-epipedo-s083.json"
    if not p.exists():
        import pytest
        pytest.skip("a peca ancora saiu do disco")
    sp = json.loads(p.read_text(encoding="utf-8"))
    d = NF.da_spec(sp)
    assert "τρία" in d["total"] and "τρεις" in d["total"] and "δύο" in d["total"]
    assert NF.declaracao_incompleta(sp) == ["τρία"], (
        "a incompletude medida mudou — releia em vez de apagar o caso")


def test_a_peca_LIMPA_sai_limpa():
    """Contraprova no outro sentido: sem ela bastaria acusar sempre."""
    sp = {"idioma": "el", "copy": "o unico numeral falado e δύο",
          "short": [{"nar": "Δύο δρόμοι φτάνουν στη γραμμή."}]}
    assert NF.declaracao_incompleta(sp) == []


def test_idioma_DESCONHECIDO_diz_que_nao_sabe_e_nao_devolve_vazio():
    """Vazio de instrumento nao prova ausencia (17/10).

    Lista vazia leria como "nenhum numeral"; `None` diz que o modulo nao sabe.
    """
    assert NF.encontra("dua tiga empat", "id") is None
    sp = {"idioma": "id", "copy": "", "short": [{"nar": "dua tiga"}]}
    assert NF.da_spec(sp)["total"] is None
    assert NF.declaracao_incompleta(sp) == [], (
        "idioma desconhecido produziu acusacao — seria achado inventado")
    texto = NF.relato(sp)
    assert "NAO SABE" in texto


def test_o_ARTIGO_fica_de_fora_e_isso_vai_DITO():
    """`um`/`uma` e equivalentes acusariam quase toda frase (725)."""
    assert NF.encontra("Escreva a regra uma vez, e cumpra.", "pt") == []
    fonte = (RAIZ / "fabrica" / "numerais_falados.py").read_text(
        encoding="utf-8")
    assert "FORA_POR_SER_ARTIGO" in fonte
    assert "artigo" in fonte.lower() and "725" in fonte, (
        "saiu a razao de excluir o artigo; sem ela alguem o inclui de volta")
    for proibido in ("um", "uma"):
        assert proibido not in NF.VOCABULARIO["pt"], (
            "%r entrou no vocabulario e ele e artigo na maioria das "
            "ocorrencias" % proibido)


def test_a_FRONTEIRA_de_palavra_e_respeitada():
    """`dois` dentro de outra palavra nao conta, e o acento nao quebra a busca."""
    assert NF.encontra("adoisado", "pt") == []
    assert NF.encontra("Sao tres coisas.", "pt") == ["tres"]
    assert NF.encontra("São três coisas.", "pt") == ["três"]
    assert NF.encontra("Τρία πράγματα μένουν έξω.", "el") == ["τρία"]


def test_os_TRES_idiomas_vivos_tem_vocabulario():
    assert set(("pt", "el", "pl")).issubset(set(NF.idiomas()))
    for idi in ("pt", "el", "pl"):
        assert len(NF.VOCABULARIO[idi]) >= 10, idi


def test_NAO_alarma_e_a_medida_do_acervo_e_RECONFERIDA():
    """144 de 259 falam numeral — e por isso isto NAO e portao nem alarme.

    O numero e reconferido contra o disco, senao envelhece calado (753).
    """
    com = tot = 0
    for p in sorted(glob.glob(str(RAIZ / "fabrica" / "specs" / "*.json"))):
        try:
            sp = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:
            continue
        if (not isinstance(sp, dict) or not sp.get("short")
                or sp.get("longo")):
            continue
        tot += 1
        achados = NF.da_spec(sp)["total"]
        if achados:
            com += 1
    assert tot >= 200, "menos de 200 specs de short solto (%d)" % tot
    assert com > tot * 0.3, (
        "o numeral por extenso deixou de ser comum (%d de %d) — se o acervo "
        "mudou, esta nota se rele e o instrumento pode virar aviso" % (com, tot))
    fonte = (RAIZ / "fabrica" / "numerais_falados.py").read_text(
        encoding="utf-8")
    assert "144 das 259" in fonte or "144/259" in fonte, (
        "o snapshot original saiu do modulo — ele fica como HISTORIA, porque e "
        "dele que a retratacao de 22/10 as 14:4x fala")
    # RETRATADO em 22/10 as 14:4x: a versao anterior cobrava a CONTAGEM
    # (`abs(com - 144) <= 15`) e o acervo cresce uma spec por rodada, logo ela
    # saia da tolerancia a cada ~16 rodadas por CRESCIMENTO e nao por mudanca.
    # Deu 160 de 285 e o teste reprovou mandando reler; relido, a PROPORCAO foi
    # de 0,556 para 0,561 — a propriedade que sustenta "e comum" nao se mexeu.
    # Identidade onde havia propriedade (743/753/761).
    prop = com / float(tot)
    assert 0.45 <= prop <= 0.70, (
        "a PROPORCAO saiu da faixa observada (%.3f contra 0,556 do snapshot) — "
        "aqui sim o acervo mudou de carater, e esta nota se rele em vez de a "
        "faixa ser movida" % prop)
    assert "a MEDIDA E A PROPORCAO" in fonte or "A MEDIDA E A PROPORCAO" in fonte, (
        "a retratacao saiu do modulo: sem ela a rodada seguinte volta a cobrar "
        "a contagem absoluta")


def test_ele_LISTA_e_NAO_julga_nem_reprova():
    """Decidir se o numeral e do mundo e LEITURA, e o codigo de saida e zero."""
    fonte = (RAIZ / "fabrica" / "numerais_falados.py").read_text(
        encoding="utf-8")
    arvore = ast.parse(fonte)
    main = next(n for n in ast.walk(arvore)
                if isinstance(n, ast.FunctionDef) and n.name == "main")
    retornos = [ast.unparse(n.value) for n in ast.walk(main)
                if isinstance(n, ast.Return) and n.value is not None]
    assert retornos and all(r == "0" for r in retornos), retornos
    assert "LISTA e NAO julga" in fonte
    assert "regra (g)" in fonte


def test_ele_ENTRA_na_passada_do_antes_do_render():
    """Instrumento que o chamador nao alcanca e a classe dos layouts mortos."""
    fonte = (RAIZ / "fabrica" / "antes_do_render.py").read_text(
        encoding="utf-8")
    assert "numerais_falados" in fonte
    ADR = _mod("antes_do_render")
    assert "numerais_falados" in ADR.INSTRUMENTOS


def test_o_incidente_continua_escrito():
    fonte = (RAIZ / "fabrica" / "numerais_falados.py").read_text(
        encoding="utf-8")
    for marca in ("s083", "Xp4jcAkYaPM", "INCOMPLETA", "dois de tres"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo; sem ela o instrumento parece "
            "zelo e nao conserto de defeito medido" % marca)
