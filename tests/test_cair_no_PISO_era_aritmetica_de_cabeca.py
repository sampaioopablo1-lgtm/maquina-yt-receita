# -*- coding: utf-8 -*-
"""Duas regras do repo apontam para pontos diferentes da faixa.

Medido em 21/10/2026. O `mira.orcamento` da o numero de caracteres por cena
para o **MEIO** da faixa, com a razao escrita (mirar a borda e o que o 752/774
mostra que nao sobrevive ao residuo). A **regra de redacao do 772** manda outra
coisa: *"mire o PISO do `ALVO_SHORT` quando a voz nao exigir o topo"*. Logo
cair no piso era aritmetica MINHA.

E ela custou passadas medidas: o `epomeno-epipedo-s083` levou TRES builds
(42,0 -> 41,4 -> 41,6) e o `kolejny-poziom-s086` TRES (42,5 -> 42,3 -> 41,5),
cada um com um corte adivinhado no olho.

**O instrumento NAO escolhe o alvo** — diz os dois, com a procedencia de cada
um. E a medida que eu NAO tenho vai dita: 98 das 208 specs na faixa estao mais
perto do piso e 110 do meio, e com piso e meio a 0,75 s num campo onde um
caractere vale ~0,7 s **isso nao discrimina as duas regras** (§3.8).
"""
import ast
import importlib.util
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]


def _mod(nome):
    spec = importlib.util.spec_from_file_location(
        nome, RAIZ / "fabrica" / ("%s.py" % nome))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = _mod("mira")


def _spec_viva():
    """Uma spec do disco com voz modelada e short — DERIVADA, nao nomeada.

    Nomear uma peca seria identidade onde ha propriedade (743/753/761), e peca
    sai do disco quando a pauta anda.
    """
    import glob
    ensaio = _mod("ensaio")
    for p in sorted(glob.glob(str(RAIZ / "fabrica" / "specs" / "*.json"))):
        try:
            sp = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:
            continue
        if (isinstance(sp, dict) and sp.get("short") and not sp.get("longo")
                and sp.get("voz") in ensaio.MODELO_VOZ
                and M.quanto_cortar(sp, "piso")):
            return sp
    pytest.skip("nenhuma spec do disco serve de ancora — perdi a ancora")


def test_os_TRES_alvos_nomeados_e_o_default_segue_o_MEIO():
    """Mudar o default seria trocar a decisao documentada do `orcamento`."""
    sp = _spec_viva()
    piso = M.quanto_cortar(sp, "piso")
    meio = M.quanto_cortar(sp, "meio")
    topo = M.quanto_cortar(sp, "topo")
    assert piso["alvo"] < meio["alvo"] < topo["alvo"]
    assert M.quanto_cortar(sp)["rotulo"] == "meio", (
        "o default deixou de ser o MEIO — isso reescreveria a decisao do "
        "`orcamento`, que tem razao escrita (752/774)")


def test_alvo_em_SEGUNDOS_tambem_vale_e_alvo_torto_LEVANTA():
    sp = _spec_viva()
    q = M.quanto_cortar(sp, 42.0)
    assert abs(q["alvo"] - 42.0) < 1e-9
    with pytest.raises(ValueError):
        M.quanto_cortar(sp, "meio-do-meio")


def test_o_delta_e_COERENTE_com_o_orcamento_e_nao_recalculado():
    """O alvo do meio tem de dar o MESMO numero que o `orcamento` ja da.

    Dois caminhos para a mesma conta tem de concordar — e quando nao concordam,
    e a assinatura de dois donos.
    """
    sp = _spec_viva()
    orc = M.orcamento(sp)
    meio = M.quanto_cortar(sp, "meio")
    assert meio["chars_alvo"] == orc["chars"], (orc["chars"], meio)
    assert meio["chars_hoje"] == orc["hoje"]
    assert meio["delta_por_cena"] == orc["chars"] - orc["hoje"]
    assert meio["delta_total"] == meio["delta_por_cena"] * meio["cenas"]


def test_o_alvo_MAIS_BAIXO_pede_MENOS_caractere():
    """Monotonia: piso <= meio <= topo em caracteres. Se inverter, a inversao
    numerica do `_chars_para_o_real` quebrou."""
    sp = _spec_viva()
    a, b, c = (M.quanto_cortar(sp, k)["chars_alvo"]
               for k in ("piso", "meio", "topo"))
    assert a <= b <= c, (a, b, c)


def test_a_conta_e_DELEGADA_ao_inversor_e_nao_refeita():
    """Por AST: refazer `P + 0,300` aqui criaria o segundo dono da sobrecarga.

    O docstring CITA a formula em prosa, logo casar texto pegaria a explicacao.
    """
    arvore = ast.parse((RAIZ / "fabrica" / "mira.py").read_text(
        encoding="utf-8"))
    fn = next(n for n in ast.walk(arvore)
              if isinstance(n, ast.FunctionDef) and n.name == "quanto_cortar")
    corpo = ast.unparse(fn)
    assert "_chars_para_o_real" in corpo, "a inversao deixou de ser delegada"
    assert "0.300" not in corpo and "0.3" not in corpo, (
        "a sobrecarga por cena foi recopiada aqui")


def test_o_relato_DIZ_os_dois_alvos_e_que_as_regras_DIVERGEM():
    """Dizer so um esconderia a divergencia que produziu a conta de cabeca."""
    sp = _spec_viva()
    linhas = "\n".join(M._linha_do_corte(sp))
    assert "PISO" in linhas and "MEIO" in linhas
    assert "DIVERGEM" in linhas and "772" in linhas
    assert "752/774" in linhas, (
        "a procedencia do alvo do MEIO saiu da frase; sem ela alguem troca o "
        "default por preferencia")


def test_a_frase_tem_UM_dono():
    """Duas copias da frase divergem — foi o 753 em procedencia."""
    fonte = (RAIZ / "fabrica" / "mira.py").read_text(encoding="utf-8")
    assert fonte.count("para cair no %s da faixa") == 1, (
        "a frase do corte foi duplicada")
    arvore = ast.parse(fonte)
    chamadas = [n for n in ast.walk(arvore)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "_linha_do_corte"]
    assert len(chamadas) == 1, (
        "a linha do corte e montada em mais de um lugar (%d)" % len(chamadas))


def test_ele_ENTRA_no_relato_e_o_codigo_de_saida_segue_ZERO():
    """Instrumento que o relato nao alcanca e a classe dos layouts mortos.

    E o `mira.py` informa e nao reprova — o codigo de saida sai do veredito do
    `confere`, nunca do texto (a licao de 19/10).
    """
    import subprocess
    import glob
    ensaio = _mod("ensaio")
    alvo = None
    for p in sorted(glob.glob(str(RAIZ / "fabrica" / "specs" / "*.json"))):
        try:
            sp = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:
            continue
        if (isinstance(sp, dict) and sp.get("short") and not sp.get("longo")
                and sp.get("voz") in ensaio.MODELO_VOZ
                and not M.confere(sp).get("fora")):
            alvo = p
            break
    if alvo is None:
        pytest.skip("nenhuma spec DENTRO da mira no disco")
    r = subprocess.run(["python3", str(RAIZ / "fabrica" / "mira.py"), alvo],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-400:]
    assert "para cair no PISO" in r.stdout


def test_a_medida_que_NAO_discrimina_continua_escrita():
    """98 contra 110, com piso e meio a 0,75 s: isso nao escolhe regra nenhuma.

    Sem essa frase a rodada seguinte le o 98/110 como se fosse evidencia.
    """
    fonte = (RAIZ / "fabrica" / "mira.py").read_text(encoding="utf-8")
    for marca in ("98", "110", "nao discrimina", "0,75 s"):
        assert marca in fonte, (
            "a medida que NAO discrimina perdeu %r — e ela existe para impedir "
            "que alguem afirme qual regra a producao segue" % marca)
    assert "TRES builds" in fonte, (
        "saiu o custo medido (as passadas das pecas s083 e s086)")
