# -*- coding: utf-8 -*-
"""Tres guardas copiadas a mao em todo builder, e a quarta que eu nunca escrevi.

Medido em 21/10/2026. Cada peca nasce de um builder descartavel, e eu copiava
para dentro dele dois `assert` — uma frase por cena e layout dentro do conjunto
SONDADO. **As palavras da thumbnail eu nunca assertei, e elas falharam CINCO
vezes nesta sessao**: `kolejny-poziom-s071`, a primeira versao da `s089`, a
`s075`, a primeira versao da `s098` e a primeira versao da `s099`. Nas cinco
quem pegou foi o portao ou o `antes_do_render`, DEPOIS de a peca estar escrita —
e cinco vezes a mesma assinatura e o item 3 da §10.

A quarta guarda e a que **nenhum portao tem**: a chave `longo` ausente, que em
18/10 matou o run 39110638169 com `KeyError` depois de o render comecar.

Este arquivo cobra que as quatro moram num dono so, que os limites sao LIDOS e
que isto NAO virou portao — porque 216 das 398 specs do acervo reprovariam a
regra de uma frase por cena.
"""
import ast
import glob
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


SM = _mod("spec_minima")
V = _mod("variedade")
LS = _mod("layouts_do_short")


def _boa():
    """Uma spec que passa nas quatro guardas, montada aqui.

    Nao e lida do disco de proposito: ancorar numa peca viva seria identidade
    onde ha propriedade (743/753/761), e peca sai do disco quando a pauta anda.
    """
    layout = sorted(LS.desenham())[0]
    return {"idioma": "pt-BR", "longo": [],
            "thumb": {"l1": "Duas", "l2": "palavras"},
            "short": [{"layout": layout, "nar": "Uma frase so, com ponto."}]}


def test_a_spec_boa_passa_nas_QUATRO():
    assert SM.confere(_boa()) == []
    SM.exige(_boa())              # nao levanta


def test_a_thumbnail_de_CINCO_palavras_e_acusada():
    """O defeito que falhou cinco vezes nesta sessao."""
    sp = _boa()
    sp["thumb"] = {"l1": "O de baixo", "l2": "se move"}
    assert SM.palavras_da_thumb(sp["thumb"]) == 5
    problemas = SM.confere(sp)
    assert any("thumbnail" in p for p in problemas), problemas


def test_a_FRONTEIRA_da_thumbnail_e_cobrada_dos_dois_lados():
    sp = _boa()
    sp["thumb"] = {"l1": "uma duas", "l2": "tres quatro"}
    assert SM.confere(sp) == [], "o limite EXATO tem de passar"
    sp["thumb"] = {"l1": "uma duas", "l2": "tres quatro cinco"}
    assert SM.confere(sp), "um acima do limite tem de reprovar"


def test_a_chave_longo_AUSENTE_e_acusada_e_lista_vazia_NAO_e():
    """Ausencia de chave nao e valor vazio — o run 39110638169.

    E o outro lado tem de passar: `longo: []` e a forma CERTA do short solto, e
    acusa-la quebraria toda peca da frota.
    """
    sp = _boa()
    sp.pop("longo")
    assert any("longo" in p for p in SM.confere(sp))
    sp["longo"] = []
    assert SM.confere(sp) == []


def test_duas_frases_numa_cena_e_acusado():
    sp = _boa()
    sp["short"][0]["nar"] = "Primeira frase. E a segunda tambem."
    assert any("frases" in p for p in SM.confere(sp))


def test_layout_fora_do_conjunto_SONDADO_e_acusado():
    sp = _boa()
    sp["short"][0]["layout"] = "numero"
    problemas = SM.confere(sp)
    assert any("NAO desenha" in p for p in problemas), problemas
    assert any("s069" in p for p in problemas), (
        "a acusacao perdeu o incidente que a justifica — a peca que foi ao ar "
        "com cartao em branco")


def test_o_exige_levanta_com_TODOS_os_problemas_de_uma_vez():
    """Levantar no primeiro esconde os outros e faz a escrita ir de erro em erro.

    Foi assim que a `s099` levou duas passadas.
    """
    sp = {"idioma": "pt-BR", "thumb": {"l1": "uma duas tres", "l2": "quatro cinco"},
          "short": [{"layout": "numero", "nar": "Uma. Duas."}]}
    with pytest.raises(AssertionError) as e:
        SM.exige(sp)
    texto = str(e.value)
    for marca in ("longo", "thumbnail", "frases", "NAO desenha"):
        assert marca in texto, (marca, texto[:400])


def test_os_limites_sao_LIDOS_dos_donos_e_nao_copiados():
    """Por AST: o modulo CITA "4 palavras" na prosa que explica a medida, logo
    casar texto pegaria a explicacao. O que se proibe e numero em CODIGO.
    """
    fonte = (RAIZ / "fabrica" / "spec_minima.py").read_text(encoding="utf-8")
    arvore = ast.parse(fonte)
    corpo = [n for n in arvore.body if not isinstance(n, ast.Expr)]
    for no in corpo:
        for sub in ast.walk(no):
            if isinstance(sub, ast.Assign):
                for alvo in sub.targets:
                    if (isinstance(alvo, ast.Name) and alvo.id.isupper()
                            and isinstance(sub.value, ast.Constant)
                            and isinstance(sub.value.value, int)):
                        raise AssertionError(
                            "limite cravado no modulo: %s = %r"
                            % (alvo.id, sub.value.value))
    assert "V.THUMB_MAX_PALAVRAS" in fonte, "o limite deixou de vir do dono"
    assert "NR.frases" in fonte and "LS.desenham()" in fonte


def test_NAO_virou_portao_e_o_numero_do_acervo_e_RECONFERIDO():
    """216 das 398 specs reprovariam a regra de uma frase por cena.

    Isto e o que torna a guarda de ESCRITA e nao portao — e o numero tem de ser
    reconferido contra o disco, senao envelhece calado (753).
    """
    arvore = ast.parse((RAIZ / "fabrica" / "prontidao.py").read_text(
        encoding="utf-8"))
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            assert all(a.name != "spec_minima" for a in no.names), (
                "o `prontidao` passou a importar a guarda de escrita; ela "
                "reprovaria mais da metade do acervo")
        if isinstance(no, ast.ImportFrom):
            assert no.module != "spec_minima"

    NR = _mod("narracao")
    com_short = multi = thumb_ruim = 0
    for p in sorted(glob.glob(str(RAIZ / "fabrica" / "specs" / "*.json"))):
        try:
            sp = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(sp, dict) or not sp.get("short"):
            continue
        com_short += 1
        idi = (sp.get("idioma") or "pt")[:2]
        if any(len(NR.frases(c.get("nar") or "", idi)) != 1
               for c in sp["short"]):
            multi += 1
        if SM.palavras_da_thumb(sp.get("thumb")) > V.THUMB_MAX_PALAVRAS:
            thumb_ruim += 1
    assert com_short >= 200, (
        "menos de 200 specs com short (%d) — a varredura quebrou" % com_short)
    assert multi > com_short * 0.3, (
        "a regra de uma frase por cena deixou de reprovar boa parte do acervo "
        "(%d de %d) — se o acervo convergiu, esta nota se rele e a guarda pode "
        "virar portao" % (multi, com_short))
    fonte = (RAIZ / "fabrica" / "spec_minima.py").read_text(encoding="utf-8")
    assert "**216**" in fonte and "**87**" in fonte, (
        "as medidas do acervo sairam do modulo; sem elas a decisao de nao ser "
        "portao fica sem procedencia")
    assert abs(multi - 216) <= 15 and abs(thumb_ruim - 87) <= 15, (
        "a medida mudou (%d com multi-frase e %d com thumb larga, contra 216 e "
        "87 escritos) — releia em vez de mover o numero" % (multi, thumb_ruim))


def test_as_CINCO_falhas_e_o_run_continuam_escritos():
    fonte = (RAIZ / "fabrica" / "spec_minima.py").read_text(encoding="utf-8")
    for marca in ("CINCO", "s071", "s089", "s075", "s098", "39110638169"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo; sem ela a guarda parece zelo e "
            "nao conserto de defeito medido" % marca)
