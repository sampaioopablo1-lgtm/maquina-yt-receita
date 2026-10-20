# -*- coding: utf-8 -*-
"""Duas rodadas seguidas pedindo conserto por um limite de 0,05 s.

MEDIDO em 19/10 as 22:1x. Em 21:1x a peca reprovou pelo gancho (13 palavras,
limite 12) e em 22:1x pela thumbnail (5 palavras, limite 4) — as duas no portao
`variedade`, que custa **0,05 s**. Nas duas eu rodei `mira` e `acento` no
rascunho e NAO rodei o portao.

E o custo nao sustenta a escolha: os DEZ portoes baratos somam **0,65 s** e o
`layout`, que RENDERIZA, custa **8,0 s** sozinho. A causa e procedural.
"""
import ast
import json
import os
import subprocess
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as AR  # noqa: E402
import prontidao as P  # noqa: E402

TETO_BARATO_S = 3.0
PISO_CARO_S = 2.0


def _uma_spec_de_short():
    import glob

    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")),
                    reverse=True):
        with open(p, encoding="utf-8") as f:
            sp = json.load(f)
        if sp.get("short") and not sp.get("longo") and sp.get("voz"):
            return p, sp
    raise AssertionError("nenhuma spec de short solto no disco")


def test_os_portoes_baratos_saem_do_prontidao__nao_de_uma_lista_minha():
    """Lista aqui seria o segundo dono do registro de portoes."""
    nomes = [n for n, _ in AR.portoes_baratos()]
    todos = [n for n, _ in P.PORTOES]
    assert set(nomes) == set(todos) - set(AR.PORTOES_CAROS), (nomes, todos)
    assert len(nomes) == len(todos) - len(AR.PORTOES_CAROS)
    with open(os.path.join(RAIZ, "fabrica", "antes_do_render.py"),
              encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    nomes_attr = [ast.unparse(n) for n in ast.walk(arvore)
                  if isinstance(n, ast.Attribute)]
    assert any("PORTOES" in x for x in nomes_attr), (
        "o modulo nao LE `prontidao.PORTOES` — se ele lista os portoes a mao, "
        "portao novo nasce fora da passada rapida"
    )


def test_a_CRONOMETRAGEM_e_reconferida__e_reprova_se_o_conjunto_mudar():
    """Numero medido que ninguem reconfere envelhece calado (753)."""
    caminho, sp = _uma_spec_de_short()
    t0 = time.time()
    AR.portoes(caminho)
    barato = time.time() - t0
    assert barato < TETO_BARATO_S, (
        f"os portoes baratos levaram {barato:.2f} s — acima do teto de "
        f"{TETO_BARATO_S}. Algum deles passou a renderizar e o conjunto "
        "PORTOES_CAROS tem de ser relido"
    )
    caros = dict(P.PORTOES)
    for nome in AR.PORTOES_CAROS:
        t0 = time.time()
        try:
            caros[nome](caminho, sp)
        except Exception:
            pass
        dt = time.time() - t0
        assert dt > PISO_CARO_S, (
            f"o portao `{nome}` levou {dt:.2f} s — abaixo do piso de "
            f"{PISO_CARO_S}. Se ele deixou de renderizar, ele volta para a "
            "passada rapida e esta nota se rele"
        )


def test_CONTRAPROVA_ele_pega_os_DOIS_defeitos_das_duas_rodadas():
    """Gancho de 13 palavras e thumbnail de 5 — os dois no `variedade`."""
    caminho, sp = _uma_spec_de_short()
    destino = os.path.join(RAIZ, "fabrica", "specs", "zz-teste-antes.json")

    def roda(mut):
        q = json.loads(json.dumps(sp))
        q["slug"] = q["pacote"] = "zz-teste-antes"
        mut(q)
        with open(destino, "w", encoding="utf-8") as f:
            json.dump(q, f, ensure_ascii=False)
        try:
            return {k: v for k, v in AR.portoes(destino).items() if v}
        finally:
            os.remove(destino)

    def thumb_de_cinco(q):
        q["thumb"] = {"l1": "Uma duas tres", "l2": "quatro cinco"}

    def gancho_longo(q):
        q["short"][0]["nar"] = (
            "Uma duas tres quatro cinco seis sete oito nove dez onze doze treze."
        )

    r1 = roda(thumb_de_cinco)
    assert "variedade" in r1 and any("thumbnail" in str(x)
                                     for x in r1["variedade"]), r1
    r2 = roda(gancho_longo)
    assert "variedade" in r2 and any("gancho" in str(x)
                                     for x in r2["variedade"]), r2


def test_CONTRAPROVA_no_outro_sentido_a_peca_REAL_sai_limpa():
    """Sem este, um agregador que acusa sempre passaria."""
    caminho, _ = _uma_spec_de_short()
    ruins = {k: v for k, v in AR.portoes(caminho).items() if v}
    assert not ruins, ruins


def test_ele_chama_CADA_instrumento_pelo_relato_dele():
    """RETRATADO em 20/10: a primeira versao cravava o CONJUNTO de tres nomes.

    Quando o `paleta_da_spec` entrou como quarto instrumento, ela reprovou um
    comportamento CORRETO — identidade onde a afirmacao era propriedade, a
    classe 743/753/761, num teste que eu escrevi na vespera. A propriedade e
    outra e e esta: **todo nome de `INSTRUMENTOS` e chamado pelo `relato` DELE**,
    e a marca de cada um aparece no relato — derivada da constante, nunca
    listada a mao. Reimplementar a conta aqui criaria o segundo dono de cada uma.
    """
    assert len(AR.INSTRUMENTOS) >= 3, AR.INSTRUMENTOS
    caminho, _ = _uma_spec_de_short()
    t = AR.relato(caminho)
    for nome in AR.INSTRUMENTOS:
        mod = __import__(nome)
        assert callable(getattr(mod, "relato", None)), (
            f"{nome} nao tem `relato`: o agregador chamaria o que nao existe")
        # a marca do relato e a PRIMEIRA palavra dele, em maiuscula
        marca = mod.relato(caminho).split()[0]
        assert marca in t, f"o relato perdeu {nome!r} (marca {marca!r})"


def test_NAO_e_portao_e_DIZ_que_nao_substitui_o_prontidao():
    caminho, _ = _uma_spec_de_short()
    r = subprocess.run(
        [sys.executable, os.path.join(RAIZ, "fabrica", "antes_do_render.py"),
         caminho],
        capture_output=True, text=True, cwd=RAIZ, timeout=900,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "NAO REPROVA" in r.stdout and "prontidao" in r.stdout, (
        "o relato tem de dizer que o `layout` fica de fora e que o portao "
        "inteiro ainda roda — senao ele convida a pular a conferencia que "
        "pega cartao em branco"
    )
