# -*- coding: utf-8 -*-
"""Eu conciliei os dois limites do gancho a mao, em quatro iteracoes.

MEDIDO em 19/10 as 21:1x, escrevendo o `epomeno-epipedo-s070`. O
`mira.orcamento` deu 59 caracteres por cena; a cena 0 escrita nesse orcamento
levou 13 palavras e o portao `variedade` reprovou (limite 12). Encurtar o
gancho derrubou a previsao abaixo do piso da faixa, e eu recuperei o
comprimento somando de cabeca: 57,9 -> 62,3 -> 58,8 -> 59,3.

Sao DOIS limites sobre a MESMA cena — o orcamento fala em CARACTERES e o portao
em PALAVRAS — e nenhum instrumento os mostrava juntos.
"""
import ast
import glob
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import gancho as G  # noqa: E402
import variedade as V  # noqa: E402

PISO_DE_SPECS = 150
PISO_DE_IDIOMAS = 4


def _specs_com_short():
    fora = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            with open(p, encoding="utf-8") as f:
                sp = json.load(f)
        except Exception:
            continue
        if sp.get("short") and sp.get("voz"):
            fora.append((os.path.basename(p), sp))
    return fora


def test_a_varredura_sai_do_DISCO_e_reprova_se_encolher():
    specs = _specs_com_short()
    assert len(specs) >= PISO_DE_SPECS, (
        f"so {len(specs)} specs com short e voz — abaixo do piso de "
        f"{PISO_DE_SPECS} este arquivo passa por VACUIDADE"
    )


def test_o_limite_e_LIDO_do_portao__cobrado_por_AST():
    """Copiar o 12 aqui seria o quinto caso de dois donos da semana."""
    assert G.limite() == V.GANCHO_MAX_PALAVRAS
    with open(os.path.join(RAIZ, "fabrica", "gancho.py"), encoding="utf-8") as f:
        fonte = f.read()
    arvore = ast.parse(fonte)
    # ninguem atribui o limite a mao
    for n in ast.walk(arvore):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and "LIMITE" in t.id.upper():
                    raise AssertionError(
                        f"ha um limite cravado em {t.id} — ele tem de sair do "
                        "`variedade`, que e o portao que o cobra"
                    )
    # e a leitura do portao esta no codigo, nao so na prosa
    nomes = [
        ast.unparse(n) for n in ast.walk(arvore) if isinstance(n, ast.Attribute)
    ]
    assert any("GANCHO_MAX_PALAVRAS" in x for x in nomes), (
        "o modulo nao LE `variedade.GANCHO_MAX_PALAVRAS`"
    )


def test_a_contagem_usa_a_MESMA_funcao_do_portao__por_AST():
    """Partir frase por conta propria daria contagem diferente da do portao."""
    with open(os.path.join(RAIZ, "fabrica", "gancho.py"), encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    chamadas = [
        ast.unparse(n.func) for n in ast.walk(arvore) if isinstance(n, ast.Call)
    ]
    assert any("primeira_frase" in c for c in chamadas), (
        "o modulo nao chama `variedade.primeira_frase` — a contagem tem de "
        "sair da mesma funcao que o portao usa"
    )
    assert any("duracao_real_prevista" in c for c in chamadas), (
        "a previsao tem de ser DELEGADA ao `ensaio`; refazer R e P aqui "
        "criaria o segundo dono da sobrecarga por voz"
    )


def test_CONTRAPROVA_gancho_acima_do_limite_e_ACUSADO():
    """Com a frase que o portao de fato reprovou nesta rodada."""
    sp = None
    for _, s in _specs_com_short():
        if s.get("slug") == "epomeno-epipedo-s070":
            sp = json.loads(json.dumps(s))
            break
    assert sp is not None, (
        "a spec desta rodada saiu do disco — sem ela este teste nao mede o "
        "caso real que o produziu"
    )
    sp["short"][0]["nar"] = (
        "Ο ένας μήνας "
        "κρύβει ό,τι "
        "πληρώνεις "
        "μία φορά στο "
        "τρίμηνο ή τον "
        "χρόνο."
    )
    d = G.custo_do_encurtamento(sp)
    assert d["passa"] and d["palavras"] == 13 and d["limite"] == 12
    assert d["chars_perdidos"] > 0
    assert d["queda_s"] > 0, "cortar palavra tem de derrubar a previsao"
    assert d["recolocar_por_cena"] > 0, (
        "sem o quanto RECOLOCAR o instrumento nao substitui a conta que eu "
        "fiz de cabeca"
    )


def test_CONTRAPROVA_no_outro_sentido_gancho_que_cabe_NAO_e_acusado():
    """Sem este, um instrumento que acusa sempre passaria."""
    sp = next(s for _, s in _specs_com_short()
              if s.get("slug") == "epomeno-epipedo-s070")
    d = G.custo_do_encurtamento(sp)
    assert not d["passa"], d
    assert "chars_perdidos" not in d, (
        "nao ha corte a medir quando o gancho cabe"
    )


def test_o_TETO_ESTATISTICO_nao_teria_pegado_o_meu_caso():
    """E a honestidade do instrumento: a mediana orienta, nao decide.

    A frase reprovada tinha 68 caracteres, ABAIXO dos ~69 que a mediana do
    grego da para doze palavras — e ainda assim 13 palavras, porque usou
    palavras curtas. Se este teste parar de valer, a nota tem de ser relida.
    """
    teto = G.teto_de_caracteres("el")
    assert teto is not None and 68 <= teto, (
        f"o teto do grego ({teto}) deixou de ser >= 68 — a nota de que a "
        "mediana nao pegaria o caso real precisa ser refeita"
    )


def test_a_tabela_de_chars_por_palavra_cobre_MAIS_DE_UM_IDIOMA():
    """A guarda do 725, que e justamente a que faltou na rodada anterior."""
    assert len(G.CHARS_POR_PALAVRA) >= PISO_DE_IDIOMAS, G.CHARS_POR_PALAVRA
    for k in ("el", "pl", "pt-BR"):
        assert k in G.CHARS_POR_PALAVRA, k
    # e idioma sem medida devolve None em vez de um numero inventado
    assert G.teto_de_caracteres("zz-ZZ") is None


def test_a_tabela_BATE_com_o_disco__e_reprova_se_divergir():
    """Numero medido que ninguem reconfere envelhece calado (753)."""
    import statistics

    por = {}
    for _, sp in _specs_com_short():
        idi = sp.get("idioma")
        for c in sp["short"]:
            fr = V.primeira_frase(c.get("nar") or "")
            pal = fr.split()
            if len(pal) >= 3:
                por.setdefault(idi, []).append(len(fr) / len(pal))
    for idi, valor in G.CHARS_POR_PALAVRA.items():
        amostra = por.get(idi)
        if not amostra or len(amostra) < 20:
            continue
        medido = statistics.median(amostra)
        assert abs(medido - valor) < 0.35, (
            f"{idi}: a tabela diz {valor} e o disco mede {medido:.2f} — "
            "reconfira em vez de deixar o numero envelhecer"
        )


def test_NAO_e_portao__o_codigo_de_saida_continua_zero():
    """Quem reprova o gancho e o `variedade`; isto informa ANTES do render.

    E o acervo confirma que um portao novo aqui nao caberia: o docstring do
    `variedade` mede 14 de 39 shorts soltos passando do limite.
    """
    alvo = os.path.join(RAIZ, "fabrica", "specs", "epomeno-epipedo-s070.json")
    r = subprocess.run(
        [sys.executable, os.path.join(RAIZ, "fabrica", "gancho.py"), alvo],
        capture_output=True, text=True, cwd=RAIZ, timeout=600,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "INFORMA" in r.stdout


def test_a_licao_das_QUATRO_iteracoes_continua_escrita():
    with open(os.path.join(RAIZ, "fabrica", "gancho.py"), encoding="utf-8") as f:
        t = f.read()
    for marca in ("41,0", "43,0", "41,4", "41,6"):
        assert marca in t, (
            f"a serie das quatro iteracoes perdeu {marca} — e ela a medida do "
            "que o instrumento substitui"
        )
    assert re.search(r"mediana\s+N[AÃ]O teria", t, re.I), (
        "saiu do modulo a nota de que o teto estatistico nao pegaria o caso"
    )
