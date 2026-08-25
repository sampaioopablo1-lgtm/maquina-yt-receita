"""Sem os mp3 na maquina, `escrever_copy` tem de RECUSAR, nao escrever "—".

MEDIDO EM 25/08/2026, e no mesmo dia em que o credito CC-BY foi corrigido em
`ler_copy`. Regerei o copy.md da kolejny-poziom-011 numa maquina que tinha a
spec mas nao tinha as trilhas. `credito_trilha` nao achou mp3 nenhum, devolveu
"—", `escrever_copy` gravou isso no lugar de {TRILHA}, e o longo SP7Vz8qHdRY
subiu SEM atribuicao. O copy.md original do render — feito onde os mp3 existem
— trazia o credito certo; eu o sobrescrevi.

Nada falhou em lugar nenhum. E o mesmo modo de falha do aprendizado 481: a
licenca desaparece calada e o video vai ao ar assim mesmo.

A regra tem de ser assimetrica, e e de proposito:

  spec DECLARA trilha  + mp3 ausente  -> RECUSA (o uso ficaria sem licenca)
  spec SEM trilha                     -> segue (video sem musica nao credita)

Na esteira de verdade isto nunca dispara: o frota.yml baixa as faixas antes de
renderizar. Ele dispara exatamente onde me pegou — fora da esteira.
"""

import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import copy_md  # noqa: E402


def _spec(trilha="Wholesome"):
    sp = {
        "slug": "kolejny-poziom",
        "copy": "# t\n\n## TITULO\nT\n\n## DESCRICAO\nD\n\n## MUSICA / LICENCA\n{TRILHA}\n",
        "longo": [{"layout": "titulo", "kicker": "k", "sub": "s",
                   "nar": "Otwarcie.", "cap": "Cap"}],
    }
    if trilha:
        sp["trilha"] = trilha
    return sp


def test_recusa_quando_a_spec_declara_trilha_e_o_mp3_nao_esta(tmp_path, monkeypatch):
    monkeypatch.setattr(copy_md, "TRILHA_DIR", str(tmp_path / "vazio"))
    (tmp_path / "vazio").mkdir()
    with pytest.raises(RuntimeError) as e:
        copy_md.escrever_copy(_spec(), [10.0], str(tmp_path))
    assert "Wholesome" in str(e.value)
    assert "CC-BY" in str(e.value)


def test_a_recusa_acontece_antes_de_gravar_o_arquivo(tmp_path, monkeypatch):
    """Gravar e depois estourar deixaria o copy.md ruim no disco."""
    monkeypatch.setattr(copy_md, "TRILHA_DIR", str(tmp_path / "vazio"))
    (tmp_path / "vazio").mkdir()
    with pytest.raises(RuntimeError):
        copy_md.escrever_copy(_spec(), [10.0], str(tmp_path))
    assert not (tmp_path / "copy.md").exists()


def test_com_o_mp3_presente_escreve_o_credito(tmp_path, monkeypatch):
    d = tmp_path / "trilhas"
    d.mkdir()
    (d / "Wholesome.mp3").write_bytes(b"\xff\xfb\x00")
    monkeypatch.setattr(copy_md, "TRILHA_DIR", str(d))
    monkeypatch.setattr(copy_md, "TRILHAS_VALIDAS", {"Wholesome"})
    txt = copy_md.escrever_copy(_spec(), [10.0], str(tmp_path))
    assert "creativecommons.org/licenses" in txt
    assert "Wholesome by Kevin MacLeod" in txt
    # o travessao aparece DENTRO do proprio credito ("incompetech.com) —
    # Licensed under"), entao o que se prende e a secao nao ser SO ele
    assert txt.split("## MUSICA / LICENCA")[1].strip() != "—"


def test_spec_sem_trilha_segue_em_frente(tmp_path, monkeypatch):
    """Video sem musica nao tem o que creditar — recusar aqui pararia a frota."""
    monkeypatch.setattr(copy_md, "TRILHA_DIR", str(tmp_path / "vazio"))
    (tmp_path / "vazio").mkdir()
    txt = copy_md.escrever_copy(_spec(trilha=None), [10.0], str(tmp_path))
    assert (tmp_path / "copy.md").exists()
    assert "—" in txt
