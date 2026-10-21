# -*- coding: utf-8 -*-
"""O "NAO MEXA" podia estar a quase um segundo do alvo — 21/10 as 17:3x.

O `mira.quanto_cortar` comparava a MEDIA ARREDONDADA de caracteres com um alvo
inteiro. Logo uma peca com media 33,5 comparava igual a um alvo de 33 e o metodo
respondia *"ja esta la, NAO MEXA"* — com a previsao em 42,3 contra um piso de
41,5. Aconteceu na peca desta rodada.

**E o defeito tem uma forma pior que o tamanho: a DIRECAO.** O alvo em
caracteres supoe cenas UNIFORMES, e a peca real nao e (o `P` da voz e por
FRASE), logo a media nao resume a peca. Medido no disco: em **49 das 266** specs
o conselho em caracteres manda ACRESCENTAR enquanto a previsao JA ESTA acima do
alvo.

O conserto nao troca o conselho em caracteres — ele e inteiro porque o que se
escreve e texto. Ele acrescenta a distancia em SEGUNDOS (a grandeza que a mira e
o portao cobram), o passo de UM caractere medido pelo dono, e NOMEIA a
discordancia.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio   # noqa: E402
import mira     # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")


def _codigo(no):
    corpo = list(no.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return "\n".join(ast.unparse(x) for x in corpo)


def _respostas(rotulo="piso"):
    saida = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short"):
            continue
        q = mira.quanto_cortar(d, rotulo)
        if q:
            saida.append((os.path.basename(f)[:-5], d, q))
    return saida


def test_a_varredura_nao_e_vacua():
    r = _respostas()
    assert len(r) >= 150, (
        "so %d spec(s) com resposta: os testes abaixo passariam por vacuidade"
        % len(r))


def test_a_distancia_em_SEGUNDOS_sai_na_resposta():
    for nome, d, q in _respostas()[:40]:
        for chave in ("previsao_hoje", "delta_s", "direcao", "discorda",
                      "passo_de_um_char_s"):
            assert chave in q, (
                "%s: a resposta perdeu a chave %r — sem ela a distancia"
                " verdadeira volta a ficar invisivel" % (nome, chave))
        prev = ensaio.duracao_real_prevista(d["short"], d.get("voz", ""),
                                            "edge")
        assert abs(q["previsao_hoje"] - prev) < 0.02, (
            "%s: a previsao devolvida (%.2f) nao e a do dono (%.2f)"
            % (nome, q["previsao_hoje"], prev))
        assert abs(q["delta_s"] - (prev - q["alvo"])) < 0.02, (
            "%s: o delta em segundos nao e a distancia ate o alvo" % nome)


def test_a_DIRECAO_sai_dos_segundos_e_nao_dos_caracteres():
    for nome, _, q in _respostas():
        esperado = ("cortar" if q["delta_s"] > 0 else
                    "acrescentar" if q["delta_s"] < 0 else "esta no alvo")
        assert q["direcao"] == esperado, (
            "%s: direcao %r contra delta_s %+.2f" % (nome, q["direcao"],
                                                     q["delta_s"]))


def test_a_DISCORDANCIA_existe_e_e_MINORIA():
    """Os dois lados: se ninguem discordasse, o conserto nao mediria nada."""
    r = _respostas()
    disc = [x for x in r if x[2]["discorda"]]
    assert disc, (
        "PERDEU A ANCORA: nenhuma spec do disco tem o conselho em caracteres"
        " apontando para o lado oposto ao dos segundos — o defeito desapareceu"
        " e esta nota se rele")
    assert len(disc) < len(r) / 2.0, (
        "%d de %d specs discordam: a maioria mudou de comportamento e isto tem"
        " de ser relido" % (len(disc), len(r)))
    for nome, _, q in disc:
        assert q["delta_total"] and q["delta_s"], nome
        assert (q["delta_total"] > 0) == (q["delta_s"] > 0), (
            "%s marcado como discordante sem discordar" % nome)


def test_o_caso_do_NAO_MEXA_a_distancia_existe_e_sai_NOMEADO():
    r = [x for x in _respostas()
         if x[2]["delta_total"] == 0
         and abs(x[2]["delta_s"]) > x[2]["passo_de_um_char_s"] / 2.0]
    assert r, (
        "PERDEU A ANCORA: nenhuma spec recebe `delta 0` a mais de meio passo de"
        " caractere do alvo — era o caso que produziu o conserto")
    nome, d, q = r[0]
    linha = "\n".join(mira._linha_do_corte(d))
    assert "previsao" in linha and "do alvo" in linha, (
        "%s: a frase nao diz a distancia verdadeira: %r" % (nome, linha[:200]))


def test_o_passo_de_UM_caractere_e_MEDIDO_pelo_dono():
    for nome, d, q in _respostas()[:25]:
        n, hoje = q["cenas"], q["chars_hoje"]
        voz = d.get("voz", "")
        a = ensaio.duracao_real_prevista(
            [{"nar": "x" * hoje} for _ in range(n)], voz, "edge")
        b = ensaio.duracao_real_prevista(
            [{"nar": "x" * (hoje + 1)} for _ in range(n)], voz, "edge")
        assert abs(q["passo_de_um_char_s"] - abs(b - a)) < 0.02, (
            "%s: o passo devolvido (%.2f) nao e o do dono (%.2f)"
            % (nome, q["passo_de_um_char_s"], abs(b - a)))
        assert q["passo_de_um_char_s"] > 0


def test_o_conselho_em_CARACTERES_continua_inteiro():
    """Contraprova no outro sentido: o conserto NAO troca a unidade escrita."""
    for nome, _, q in _respostas()[:40]:
        assert isinstance(q["chars_alvo"], int), nome
        assert isinstance(q["delta_total"], int), nome


def test_a_conta_e_DELEGADA_e_nao_tem_constante_nova():
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py"),
                 encoding="utf-8").read()
    defs = {n.name: n for n in ast.walk(ast.parse(fonte))
            if isinstance(n, ast.FunctionDef)}
    corpo = _codigo(defs["quanto_cortar"])
    assert corpo.count("duracao_real_prevista") >= 2, (
        "a previsao e o passo tem de sair do dono: %r" % corpo[-400:])
    for proibido in ("0.56", "0.63", "0.7 *", "MODELO_VOZ"):
        assert proibido not in corpo, (
            "constante nova no corpo (%r): o passo e MEDIDO, nao escolhido"
            % proibido)


def test_as_duas_medidas_continuam_escritas():
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py"),
                 encoding="utf-8").read()
    assert "19 das 58" in fonte or "19 dessas" in fonte, (
        "a medida do `nao mexa` a distancia saiu do modulo")
    assert "49 das 266" in fonte, (
        "a medida da DISCORDANCIA de direcao saiu do modulo")
    assert "51 de 51" in fonte, (
        "a medida refinada do inversor saiu do modulo")
