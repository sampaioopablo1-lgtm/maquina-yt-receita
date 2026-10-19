"""Passar a regra H NAO e resolver ritmo — e eu li de novo com 4 h.

O DEFEITO, medido na propria rodada das 10:0x de 19/10. Eu li os tres canais
porque a leitura anterior tinha **4 h**, e o quadro saiu com os tres em
`indeterminado` — como tinha de sair, porque numa janela de 4 h o piso de
resolucao e **6,00/dia** contra um ritmo suposto de ~1,8. **A leitura era
previsivelmente inutil**, e custou tres requisicoes na mesma madrugada em que a
rota da duracao fechou por LIMITE (19/10 as 06:1x).

**E o numero ja estava no modulo:** o docstring do `porta1.piso_de_resolucao`
diz em letra que as >= 4 h da regra H bastam para o DEGRAU da replica e **nao**
para medir ritmo. O que faltava era a DECISAO sair da minha cabeca — item 3 da
§10 — e as leituras morarem num arquivo em vez da minha memoria (a assinatura do
726: o passo sem instrumento e o passo que eu solto).

O que este arquivo guarda:

1. **As TRES portas sao distintas** e a primeira nao implica as outras.
2. **O caso real de 4 h** devolve `degrau: True` e `resolve: False`, com aviso.
3. **A janela de 49 h responde o que a de 4 h nao respondia** — ela e a
   contraprova no outro sentido: sem ela o teste passaria recusando tudo.
4. O parque **recusa** regravar o mesmo instante com valor diferente.
"""

import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import leitura_de_inscritos as LI  # noqa: E402
import porta1  # noqa: E402

CANAIS = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")


def _copia(tmp_path, ate=None):
    """Uma COPIA do parque, para nao tocar o arquivo real."""
    destino = tmp_path / "lidos.jsonl"
    with open(destino, "w", encoding="utf-8") as f:
        for r in LI.leituras():
            if ate is None or r["em"] < ate:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return str(destino)


def test_o_parque_tem_leitura_e_os_TRES_canais_em_cada_uma():
    todas = LI.leituras()
    assert len(todas) >= 4, (
        f"o parque tem {len(todas)} leituras — com poucas este arquivo passa "
        "por vacuidade, o defeito do 743 em forma de glob."
    )
    for r in todas:
        assert set(r["canais"]) == set(CANAIS), (
            f"a leitura {r['em']} nao cobre os tres canais da frota"
        )
        assert r.get("fonte"), f"a leitura {r['em']} esta sem procedencia"


def test_as_TRES_portas_sao_DISTINTAS():
    """4 h, 13,4 h e 26,8 h sao tres perguntas, nao uma."""
    uma = porta1.horas_para_resolver(LI.RITMO_SUPOSTO_DA_FROTA)
    duas = porta1.horas_para_resolver(LI.RITMO_SUPOSTO_DA_FROTA, 2)
    assert porta1.HORAS_MINIMAS < uma < duas, (
        "as portas deixaram de ser crescentes e distintas — juntar as duas "
        "primeiras foi o defeito que durou dias"
    )
    assert duas == pytest.approx(2 * uma)


def test_a_janela_de_4h_passa_o_DEGRAU_e_NAO_resolve(tmp_path):
    """O caso REAL: 06:08 -> 10:08 de 19/10."""
    caminho = _copia(tmp_path, ate="2026-10-19T10:00:00Z")
    v = LI.veredito("2026-10-19T10:08:00Z", caminho=caminho)
    assert v["horas"] == pytest.approx(4.0, abs=0.05)
    assert v["degrau"] is True, "a regra H nao foi reconhecida"
    assert v["resolve_ritmo"] is False
    assert v["resolve_duas_contagens"] is False
    assert v["piso_da_janela"] == pytest.approx(6.0, abs=0.05)
    texto = LI.relato("2026-10-19T10:08:00Z", caminho=caminho)
    assert "NAO e resolver ritmo" in texto, (
        "o relato deixou de avisar, e o aviso E o conserto"
    )


def test_a_janela_LONGA_resolve_o_que_a_curta_nao_resolvia(tmp_path):
    """Contraprova no outro sentido: sem ela, recusar tudo passaria.

    Entre 17/10 09:0x e 19/10 10:0x sao ~49 h, cujo piso e ~0,49/dia — abaixo do
    ritmo suposto. Logo essa janela RESOLVE a pergunta de uma contagem.
    """
    caminho = _copia(tmp_path, ate="2026-10-19T06:00:00Z")
    v = LI.veredito("2026-10-19T10:08:00Z", caminho=caminho)
    assert v["horas"] > 40, f"a ancora de 17/10 saiu do parque ({v['horas']} h)"
    assert v["degrau"] is True
    assert v["resolve_ritmo"] is True, (
        "nenhuma janela do parque resolve nada — o instrumento passou a recusar "
        "sempre, e teste que recusa sempre deixa de avisar"
    )
    assert v["piso_da_janela"] < LI.RITMO_SUPOSTO_DA_FROTA


def test_sem_leitura_nenhuma_ele_DIZ_em_vez_de_inventar(tmp_path):
    vazio = tmp_path / "vazio.jsonl"
    vazio.write_text("", encoding="utf-8")
    v = LI.veredito("2026-10-19T10:08:00Z", caminho=str(vazio))
    assert v["horas"] is None
    assert v["resolve_ritmo"] is False
    assert "ANCORA" in v["motivo"]


def test_regravar_o_mesmo_instante_DIFERENTE_levanta(tmp_path):
    caminho = _copia(tmp_path)
    ultima = LI.leituras(caminho)[-1]
    assert LI.grava(ultima["em"], ultima["canais"], "idem", caminho) is False, (
        "regravar valor IGUAL tem de ser no-op, nao erro"
    )
    outro = dict(ultima["canais"])
    outro[CANAIS[0]] = outro[CANAIS[0]] + 7
    with pytest.raises(ValueError, match="nao muda"):
        LI.grava(ultima["em"], outro, "conflito", caminho)


def test_a_conta_e_do_porta1_e_nao_daqui():
    """Delegacao: um dono para o piso de resolucao.

    Refazer `24/horas` aqui criaria o segundo dono — a assinatura que congelou a
    legenda e parou a mira de conferir por seis pecas.
    """
    import ast

    fonte = open(os.path.join(RAIZ, "fabrica", "leitura_de_inscritos.py")).read()
    arvore = ast.parse(fonte)
    for no in ast.walk(arvore):
        if isinstance(no, ast.Constant) and no.value in (24.0, 4.0):
            pytest.fail(f"a conta do piso/da regra H foi recopiada: {no.value}")
    assert "porta1.piso_de_resolucao" in fonte
    assert "porta1.HORAS_MINIMAS" in fonte


def test_o_MOTIVO_continua_escrito_no_modulo():
    fonte = open(os.path.join(RAIZ, "fabrica", "leitura_de_inscritos.py")).read()
    assert "726" in fonte, "a assinatura do passo sem instrumento saiu do modulo"
    assert "piso de resolucao" in fonte
    assert "RITMO_SUPOSTO_DA_FROTA" in fonte
    import leitura_de_inscritos as M
    assert "PREMISSA" in M.__doc__ or "premissa" in fonte, (
        "o ritmo de 1,79 tem de ir declarado como SUPOSICAO (755), nao como medida"
    )
