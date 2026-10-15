"""A trava de titulo IDENTICO comparava a forma ERRADA contra o corpus.

MEDIDO em 15/10 as 08:2x, depois de publicar `labtreinamento-s051`
(`iRSJ6w03lj0`). Ele foi ao ar com o MESMO `## TITULO SHORT` do
`labtreinamento-s038` (`EgcUqRhx9IY`) — "Conclusao nao e situacao" — e com a
MESMA familia de entrada errada (conclusao no lugar de situacao). Os doze
portoes passaram.

A causa e de UMA linha: o `corpus_publicados.json` guarda o `## TITULO SHORT`,
que e o que o YouTube recebe (nota de 13/10 no `CLAUDE.md`), e o
`_titulo_do_copy` devolvia o `## TITULO` LONGO. **A trava comparava uma forma
contra um corpus da outra, logo nao podia casar nunca em short solto.**

E e a MESMA CLASSE de erro que o docstring do proprio `_titulo_do_copy` ja
descrevia, uma camada adiante: a primeira versao dele comparava a DESCRICAO
porque lia a linha `# `. Consertaram a leitura da spec e nao a correspondencia
com o corpus.

A mesma causa cegava um SEGUNDO portao. O `_titulos_do_canal` decide de qual
canal um titulo publicado e cruzando as specs do disco com o corpus — tambem
pelo titulo longo. Medido: ZERO specs do `labtreinamento` tinham o titulo longo
no corpus, logo a similaridade "contra o MESMO canal" comparava apenas titulos
de geracao antiga (os que moram na linha `# `), nunca os cinquenta shorts que
estao de fato no ar.

TAMANHO MEDIDO DO BURACO, e ele e pequeno: varridas todas as specs, existe
**UMA** colisao de `## TITULO SHORT` na frota inteira, e e esta. Nao e uma
enchente silenciosa — e um caso, e ele foi ao ar.

O QUE NAO FOI FEITO: a peca publicada NAO foi apagada. Apagar video publicado
exige o dono (trava da §8), e a autorizacao de 09/10 nao cobre isso.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import prontidao as P  # noqa: E402

CURTO = "Conclusão não é situação"


def _spec(nome):
    return json.load(open(RAIZ / "fabrica" / "specs" / f"{nome}.json",
                          encoding="utf-8"))


def test_o_corpus_guarda_o_titulo_CURTO_e_nao_o_longo():
    corpus = set(P._titulos_do_corpus(str(RAIZ)))
    sp = _spec("labtreinamento-s051")
    longo = [t for t in P._titulos_do_copy(sp) if t.startswith("Estresse")]
    assert longo, "a spec tem de ter o titulo longo"
    assert longo[0] not in corpus, (
        "se o titulo LONGO passar a entrar no corpus, esta nota tem de ser "
        "relida: a premissa do conserto muda")
    assert CURTO in corpus


def test_o_portao_le_TODOS_os_titulos_que_vao_ao_ar__o_curto_primeiro():
    ts = P._titulos_do_copy(_spec("labtreinamento-s051"))
    assert ts[0] == CURTO, ts
    assert any(t.startswith("Estresse") for t in ts)


def test_as_DUAS_specs_carregam_o_mesmo_titulo_curto():
    a = P._titulos_do_copy(_spec("labtreinamento-s038"))
    b = P._titulos_do_copy(_spec("labtreinamento-s051"))
    assert CURTO in a and CURTO in b
    # e os titulos LONGOS sao diferentes — e por isso que a trava antiga passou
    la = [t for t in a if t != CURTO and not t.startswith("labtreinamento")]
    lb = [t for t in b if t != CURTO and not t.startswith("labtreinamento")]
    assert la and lb and la[0] != lb[0]


def test_o_portao_AGORA_reprova_a_peca_duplicada():
    falhas = P._gate_similaridade(
        str(RAIZ / "fabrica/specs/labtreinamento-s051.json"),
        _spec("labtreinamento-s051"))
    assert falhas, "a colisao real tem de reprovar"
    assert "JA PUBLICADO" in falhas[0]
    assert "labtreinamento-s038" in falhas[0], falhas[0]


def test_e_NAO_reprova_peca_publicada_contra_a_propria_publicacao():
    """Portao que reprova sempre deixa de avisar — o argumento do `mira.py`."""
    for nome in ("kolejny-poziom-s032", "epomeno-epipedo-s033",
                 "labtreinamento-s050"):
        sp = _spec(nome)
        falhas = P._gate_similaridade(
            str(RAIZ / "fabrica/specs" / f"{nome}.json"), sp)
        assert not falhas, (nome, falhas)


def test_a_colisao_da_frota_e_UMA__o_tamanho_do_buraco_vai_medido():
    import collections
    import glob
    cnt = collections.Counter()
    for f in glob.glob(str(RAIZ / "fabrica/specs/*.json")):
        try:
            sp = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        ts = P._titulos_do_copy(sp)
        if ts:
            cnt[ts[0]] += 1
    dup = {t: n for t, n in cnt.items() if n > 1}
    assert list(dup) == [CURTO], dup
    assert dup[CURTO] == 2


def test_o_PONTO_CEGO_declarado_continua_declarado():
    """Spec nova que copie titulo de peca ANTIGA sem spec no disco passa.

    Isso vai DITO no codigo em vez de resolvido com criterio inventado: o corpus
    e uma lista nua e nao diz de quem e o titulo.
    """
    fonte = (RAIZ / "fabrica" / "prontidao.py").read_text(encoding="utf-8")
    assert "PONTO CEGO DECLARADO" in fonte
    assert "_outra_spec_com_o_titulo" in fonte
