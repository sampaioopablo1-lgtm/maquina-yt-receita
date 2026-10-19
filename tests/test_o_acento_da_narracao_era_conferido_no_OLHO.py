# -*- coding: utf-8 -*-
"""O acento da NARRACAO nao tinha instrumento, e falhou DUAS rodadas seguidas.

Em 19/10 as 15:3x a descricao grega do `epomeno-epipedo-s068` subiu **sem
tonos**; as 17:2x a primeira versao do `labtreinamento-s086` trazia *"O mesmo
treino da tres"*. Nas duas vezes quem pegou fui eu RELENDO, e nas duas o
`CLAUDE.md` registrou a mesma frase — *"o acento e passo de REDACAO e nao tem
instrumento"*. Duas vezes com a mesma assinatura e o item 3 da §10.

O QUE ESTE ARQUIVO GUARDA, e e a parte que importa: o criterio sai da
DISTRIBUICAO MEDIDA do proprio idioma, lida do disco — nao de uma lista de
idiomas escrita a mao, que e o limiar sem procedencia que a §10 proibe. Em `en`,
`id` e `hi` TODAS as specs estao em zero, logo ali o zero e o valor certo e o
instrumento tem de RECUSAR; em `el` sao 86 de 86 com acento, logo ali o zero
seria inedito.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import acento  # noqa: E402


def _specs():
    out = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if sp.get("short"):
            out.append((os.path.basename(p), sp))
    return out


def test_a_varredura_sai_do_DISCO_e_nao_pode_ficar_vazia():
    todas = _specs()
    assert len(todas) >= 50, (
        f"menos de 50 specs com short ({len(todas)}): a varredura deixou de "
        "medir o parque e todo teste deste arquivo passaria por vacuidade")


def test_os_DOIS_lados_existem__idioma_que_discrimina_e_idioma_que_nao():
    """Sem os dois lados, recusar sempre (ou nunca) passaria."""
    idiomas = sorted({(sp.get("idioma") or "?") for _, sp in _specs()})
    discriminam = [i for i in idiomas if acento.distribuicao(i)["discrimina"]]
    nao = [i for i in idiomas if not acento.distribuicao(i)["discrimina"]]
    assert discriminam, ("nenhum idioma discrimina: o instrumento nao mede nada")
    assert nao, ("nenhum idioma deixou de discriminar: sem esse lado a RECUSA "
                 "nunca e exercitada e o teste passa por vacuidade")


def test_o_grego_carrega_acento_em_TODAS_as_specs_do_disco():
    """E a base da conclusao: em `el` o zero seria inedito.

    Falha se aparecer spec grega sem tonos — e ai esta nota tem de ser RELIDA,
    porque o discriminador do idioma mudou.
    """
    d = acento.distribuicao("el")
    assert d["n"] >= 50, f"amostra grega encolheu para {d['n']}"
    assert d["zeros"] == [], (
        f"spec grega SEM tonos no disco: {d['zeros']} — ou e defeito novo, ou o "
        "discriminador deste idioma caiu e a nota se rele")
    assert d["discrimina"], "o grego deixou de discriminar"


def test_o_idioma_SEM_diacritico_RECUSA_em_vez_de_alarmar():
    """Alarmar ali seria detector que inventa achado (725)."""
    achou = False
    for nome, sp in _specs():
        v = acento.veredito(sp)
        if v["discrimina"]:
            continue
        achou = True
        assert v["suspeita"] is None, (
            f"{nome}: idioma que nao discrimina devolveu veredito {v['suspeita']!r} "
            "em vez de RECUSAR")
        assert v["motivo"] and "NAO" in v["motivo"], (
            f"{nome}: a recusa saiu sem motivo escrito")
    assert achou, "nenhuma spec de idioma sem diacritico: nada foi medido aqui"


def test_CONTRAPROVA_tirar_o_acento_da_peca_de_HOJE_a_torna_SUSPEITA():
    """Sem o caso negativo, o instrumento poderia nunca acusar."""
    alvo = os.path.join(RAIZ, "fabrica", "specs", "epomeno-epipedo-s069.json")
    assert os.path.exists(alvo), (
        "a spec grega desta rodada saiu do disco — e ela e o caso em que a "
        "contraprova se mede")
    sp = json.load(open(alvo, encoding="utf-8"))
    assert acento.veredito(sp)["suspeita"] is False, (
        "a peca COM tonos foi acusada: o instrumento esta alarmando errado")
    nu = json.loads(json.dumps(sp))
    for c in nu["short"]:
        c["nar"] = acento.sem_acento(c["nar"])
    v = acento.veredito(nu)
    assert v["suspeita"] is True, (
        "retirados os tonos, o instrumento NAO acusou: ele nao mede o defeito "
        "que o produziu")
    assert "PRONUNCIA" in (v["motivo"] or ""), (
        "o motivo da suspeita deixou de dizer o custo (o TTS le o texto como "
        "esta escrito)")


def test_o_ACERVO_tem_zeros_e_eles_sao_MINORIA_no_idioma_que_discrimina():
    """A varredura achou sete; o que o teste cobra e a FORMA, nao a lista.

    Nomear as sete seria identidade onde ha propriedade (743/753/761, SETIMA
    vez). O que vale e: existem, sao minoria, e o instrumento as acusa.
    """
    acusadas = []
    for nome, sp in _specs():
        v = acento.veredito(sp)
        if v["suspeita"]:
            acusadas.append(nome)
    assert acusadas, (
        "nenhuma spec do acervo e acusada: ou o acervo foi corrigido — e ai "
        "esta nota se rele — ou o instrumento parou de acusar")
    total = len(_specs())
    assert len(acusadas) * 4 < total, (
        f"{len(acusadas)} de {total} specs acusadas: isso e alarme de massa, e "
        "pelo argumento do `mira.py` um aviso que dispara sempre deixa de avisar")


def test_ausencia_de_narracao_NAO_e_zero():
    """Ausencia e silencio, nao leitura de zero — a regra do `duracao_a_medir`."""
    assert acento.proporcao([]) is None
    assert acento.proporcao([{"nar": ""}]) is None
    assert acento.proporcao([{"nar": "123 456"}]) is None
    v = acento.veredito({"idioma": "el", "short": [{"nar": ""}]})
    assert v["suspeita"] is None and "ausencia" in (v["motivo"] or "")


def test_o_criterio_e_DERIVADO_e_nao_uma_lista_de_idiomas():
    """Lista de idiomas cravada e limiar sem procedencia (§10).

    Por AST, porque o docstring do modulo CITA os idiomas numa tabela para se
    explicar, e casar prosa pegaria a explicacao em vez do codigo.
    """
    fonte = open(os.path.join(RAIZ, "fabrica", "acento.py"),
                 encoding="utf-8").read()
    arv = ast.parse(fonte)
    alvo = [n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)
            and n.name == "distribuicao"]
    assert alvo, "`distribuicao` desapareceu do modulo"
    corpo = ast.unparse(alvo[0])
    for proibido in ("'el'", '"el"', "'id'", '"id"', "'pt-BR'", '"pt-BR"'):
        assert proibido not in corpo, (
            f"{proibido} cravado dentro de `distribuicao`: o criterio voltou a "
            "ser uma lista de idiomas em vez da distribuicao medida")
    assert "glob" in corpo, "a distribuicao deixou de ler o DISCO"


def test_NAO_virou_portao():
    """Ele reprovaria as sete do acervo — o argumento do `mira.py`.

    POR AST, e isto foi pego pelo proprio teste na primeira execucao: a versao
    anterior cobrava `"acento." not in pront`, e o `prontidao.py` CITA a palavra
    na prosa (*"sem acento. So peguei relendo o texto na mao"*). Casar prosa
    pegou a explicacao em vez do codigo — o defeito que o docstring do modulo
    `acento` descreve, cometido no teste que o guarda.
    """
    import subprocess
    arv = ast.parse(open(os.path.join(RAIZ, "fabrica", "prontidao.py"),
                         encoding="utf-8").read())
    for n in ast.walk(arv):
        if isinstance(n, ast.Import):
            assert all(a.name != "acento" for a in n.names), (
                "o `prontidao` passou a IMPORTAR o `acento`")
        if isinstance(n, ast.ImportFrom):
            assert n.module != "acento", (
                "o `prontidao` passou a importar DE `acento`")
        if isinstance(n, ast.Call):
            assert not ast.unparse(n.func).startswith("acento."), (
                "o `prontidao` passou a CHAMAR o `acento`: ele reprovaria as "
                "specs de acervo em zero, e aviso que reprova acervo deixa de "
                "avisar")
    r = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "acento.py"),
                        os.path.join(RAIZ, "fabrica", "specs",
                                     "labtreinamento-002.json")],
                       capture_output=True, text=True)
    assert r.returncode == 0, (
        "o `acento.py` devolveu nao-zero numa spec SUSPEITA: ele virou portao")


def test_o_MOTIVO_continua_escrito_no_modulo():
    fonte = open(os.path.join(RAIZ, "fabrica", "acento.py"),
                 encoding="utf-8").read()
    for marca in ("epomeno-epipedo-s068", "labtreinamento-s086", "725",
                  "mira.py"):
        assert marca in fonte, (
            f"{marca!r} saiu do modulo: conserto sem motivo escrito volta calado")
