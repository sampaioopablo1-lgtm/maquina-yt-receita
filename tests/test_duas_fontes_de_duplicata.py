"""A segunda fonte de duplicata, travada com o defeito que a produziu.

O defeito, medido em 10 e 11/10/2026: o orquestrador lia duplicata so da lista
`videos`, que com a porta do Supabase fechada e o RETRATO
`fabrica/ponte/videos.json` de 06/10 — cego para tudo que foi publicado a
partir de 07/10. O `prontidao` lia do `corpus_publicados.json`, reescrito a
cada publicacao. **Duas fontes discordantes:** o portao pegava, o orquestrador
nao, e a Frota morria todo ciclo redisparando os MESMOS tres pacotes —
`kolejny-poziom-016`, `labtreinamento-010` e `epomeno-epipedo-015`, as 19:27,
22:49 e 01:27.

Estes testes existem porque o conserto tem duas partes que podem se separar
sem que nada quebre em silencio: a fonte (`titulos_do_corpus`) e a LIGACAO
dela nas tres acoes do `main`. Ligar duas e esquecer a terceira devolve
exatamente o estado de duas fontes discordantes que causou o defeito.
"""

from __future__ import annotations

import builtins
import inspect
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import orquestra as M  # noqa: E402

DADOS = json.loads((RAIZ / "tests" / "dados_videos.json").read_text(encoding="utf-8"))

# Os tres que morreram em producao, por nome. Nao sao exemplo: sao o defeito.
AS_TRES_QUE_MORRERAM = ("kolejny-poziom-016", "labtreinamento-010",
                        "epomeno-epipedo-015")


def test_as_tres_que_morreram_estao_no_corpus_real():
    """Se um dia sairem do corpus, o teste abaixo passaria por vacuidade."""
    corpus = M.titulos_do_corpus()
    assert corpus, "corpus_publicados.json vazio ou ilegivel"
    specs = M.specs_do_repo()
    for nome in AS_TRES_QUE_MORRERAM:
        assert nome in specs, f"{nome} sumiu do repo"
        t = M.titulo_da_spec(specs[nome]).strip().casefold()
        assert t in corpus, (
            f"{nome} nao esta mais no corpus — este arquivo perdeu o ancoradouro")


def test_titulo_que_so_o_corpus_conhece_derruba_a_spec():
    """O coracao do conserto: duplicata que a lista `videos` NAO ve.

    A spec e escolhida com a lista crua e descartada com a segunda fonte, no
    mesmo acervo — logo foi o corpus que decidiu, nao o retrato.
    """
    escolhidas, _ = M.proximo(DADOS, n=50)
    assert escolhidas, "nada escolhido com a lista crua — acervo de teste mudou"
    alvo = escolhidas[0]["pacote"]
    titulo = M.titulo_da_spec(M.specs_do_repo()[alvo]).strip().casefold()

    depois, descartadas = M.proximo(DADOS, n=50, titulos_extra={titulo})
    assert alvo not in {e["pacote"] for e in depois}
    motivo = next(d["motivo"] for d in descartadas if d["spec"] == alvo)
    assert "titulo" in motivo, motivo


def test_estado_e_relatorio_leem_a_mesma_segunda_fonte():
    """O informe e o disparo discordarem foi a forma do defeito.

    Se `estado` recebesse a segunda fonte e `relatorio` nao (ou o contrario),
    o relato diria uma coisa e a matriz faria outra — que e exatamente o que
    aconteceu entre o `prontidao` e o orquestrador.
    """
    escolhidas, _ = M.proximo(DADOS, n=50)
    alvo = escolhidas[0]["pacote"]
    titulo = M.titulo_da_spec(M.specs_do_repo()[alvo]).strip().casefold()

    canal = escolhidas[0]["canal"]
    antes = M.estado(DADOS)["canais"][canal]
    depois = M.estado(DADOS, {titulo})["canais"][canal]
    assert alvo in antes["specs_pendentes"]
    assert alvo in depois["specs_no_ar"], (
        f"{canal}: a segunda fonte nao mexeu na contagem de `estado`")
    assert alvo not in depois["specs_pendentes"]

    # No informe o alvo passa de escolhido a descartado COM o motivo escrito —
    # descartar em silencio e como nao descartar.
    motivo = "ja publicado (pelo titulo, sob outro nome de pacote)"
    linha_antes = [l for l in M.relatorio(DADOS).splitlines() if alvo in l]
    linha_depois = [l for l in M.relatorio(DADOS, {titulo}).splitlines()
                    if alvo in l]
    assert not any(motivo in l for l in linha_antes), linha_antes
    assert any(motivo in l for l in linha_depois), linha_depois


def test_titulos_no_ar_continua_pura():
    """Ela e chamada com acervo SINTETICO. Lendo arquivo por baixo, o teste de
    unidade passa a medir o acervo real — e em 11/10 isso quebrou quatro
    testes, inclusive fazendo o do token morto nunca alcancar o motivo do
    token, porque tudo era descartado antes, por titulo."""
    assert M.titulos_no_ar([]) == set(), (
        "`titulos_no_ar([])` devolveu titulo — a leitura do corpus voltou para "
        "dentro dela")
    assert M.titulos_do_corpus(), "e a segunda fonte existe, so que FORA dela"


def test_corpus_ilegivel_nao_derruba_o_ciclo(monkeypatch):
    """Falha em silencio DE PROPOSITO: e uma fonte A MAIS. Sem o arquivo o
    comportamento volta ao de antes, em vez de parar a producao."""
    real = builtins.open

    def recusa(caminho, *a, **k):
        if "corpus_publicados.json" in str(caminho):
            raise OSError("sem arquivo")
        return real(caminho, *a, **k)

    monkeypatch.setattr(builtins, "open", recusa)
    assert M.titulos_do_corpus() == set()


def test_o_main_liga_a_segunda_fonte_NAS_TRES_acoes():
    """Ligar em duas e esquecer a terceira reconstroi o defeito.

    Conferencia pela fonte do `main` de proposito: o caminho de producao
    depende de `argparse` e de rede, e o que precisa ser travado aqui e a
    LIGACAO, nao a execucao.
    """
    fonte = inspect.getsource(M.main)
    assert "titulos_do_corpus()" in fonte
    # O `main` passa `do_corpus` posicional em duas acoes e por nome na
    # terceira, entao o que se conta e a VARIAVEL e nao o nome do parametro.
    assert fonte.count("do_corpus") >= 4, (
        "o `main` passa a segunda fonte em menos de tres acoes — `estado`, "
        "`proximo` e `relatorio` tem de ler a MESMA coisa\n" + fonte)
    for fn in (M.estado, M.proximo, M.relatorio):
        assert "titulos_extra" in inspect.signature(fn).parameters, fn.__name__
