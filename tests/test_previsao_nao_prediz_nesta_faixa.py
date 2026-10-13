"""A PREVISAO NAO PREDIZ a duracao real nesta faixa -- medido 13/10 as 18:2x.

E este arquivo RETRATA EM PARTE o 730 e o 731, que sao meus e sao de hoje.

As quatro pecas da tarde, `contentDetails.duration` contra
`ensaio.duracao_real_prevista` nos dois mundos, tudo em UMA chamada
(`status_code` 200):

    peca                             edge  piper  REAL
    epomeno-epipedo-s025 (G8v-...)   42,1  37,3    44
    kolejny-poziom-s024  (0ZIO...)   42,9  36,5    44
    epomeno-epipedo-s024 (7qre...)   43,1  38,2    44
    kolejny-poziom-s023  (xlQv...)   43,1  36,7    39

**TRES previsoes DIFERENTES devolveram o MESMO real de 44**, e a de previsao
MAIOR (43,1) devolveu o MENOR real (39). A ordem de previsto nao reproduz a
ordem de real em nenhum sentido.

**E ISTO FALSIFICA A DECISAO QUE EU TOMEI NESTA MESMA RODADA.** Pelo 731 eu
encurtei o `s025` de edge 44,3 para 42,1 -- 2,2 s a menos -- para ganhar folga
contra o teto de 45. **O real nao mudou: deu 44, igual as outras duas.** Encurtar
a narracao prevista em 2,2 s nao encurtou a peca em nada.

**O que CAI do 731:** o "vies de ~2,5% para cima no mundo edge". Com n=2 ele era
+2,1% e +2,6%; com o terceiro ponto virou **+4,5%**, e o vies cresce quando a
previsao diminui -- que e a assinatura de algo que NAO depende da previsao.

**O que CAI do 730:** a frase "casa com o EDGE". Ela descrevia a menor distancia
entre duas previsoes ruins. A leitura honesta e que **nenhum dos dois mundos
prediz** estas quatro.

**O que SOBREVIVE, e e o que importa:** o provedor nao e fixo (730 segue de pe
pelo codigo, `fabrica.py:598-620`), e **o portao exigir a faixa nos DOIS mundos
continua sendo a decisao certa** -- com mais razao agora, porque a previsao erra
mais do que eu pensava e a folga de 18 a 45 e o que esta segurando a peca.

**O QUE EU NAO AFIRMO, pelo §3.8:** nao digo que existe um teto de 44 s. A
`xlQvH6JjrB4` deu 39, logo nao ha teto duro. Tres pecas em 44 com n=4 pode ser
coincidencia; o que esta MEDIDO e a ausencia de relacao, nao a causa dela.
**Hipotese a testar com mais pecas** (declarada, nao concluida): a duracao de
cada cena e imposta pelo `-t` do clipe com folga fixa, e dez cenas acumulam essa
folga -- nesse caso o que manda e o NUMERO DE CENAS e nao os caracteres. As
tres de 44 tem DEZ cenas; a de 39 tambem. Entao a hipotese ainda nao explica a
de 39, e vai dita assim em vez de arredondada.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402
from prontidao import SHORT_MAX_S, SHORT_MIN_S  # noqa: E402

# Medido as 18:2x de 13/10, uma chamada, status_code 200, part=contentDetails.
REAIS = {
    "epomeno-epipedo-s025": 44,   # G8v-9R_9mFI, 18:13:10Z
    "kolejny-poziom-s024": 44,    # 0ZIOD-KOupY, 17:13:01Z
    "epomeno-epipedo-s024": 44,   # 7qreIlqtUIU, 16:12:50Z
    "kolejny-poziom-s023": 39,    # xlQvH6JjrB4, 15:17:19Z
}


def _prev(pacote):
    s = json.loads((RAIZ / "fabrica" / "specs" / f"{pacote}.json").read_text())
    cenas, voz = s["short"], s["voz"]
    return (ensaio.duracao_real_prevista(cenas, voz, "edge"),
            ensaio.duracao_real_prevista(cenas, voz, "piper"))


def test_tres_previsoes_diferentes_deram_o_mesmo_real():
    """O fato central. Se isto deixar de valer, o raciocinio quer ser relido."""
    em_44 = [p for p, r in REAIS.items() if r == 44]
    assert len(em_44) == 3, em_44
    edges = sorted({round(_prev(p)[0], 1) for p in em_44})
    assert len(edges) == 3, edges
    assert max(edges) - min(edges) >= 0.9, edges


def test_a_MAIOR_previsao_deu_o_MENOR_real():
    """A ordem de previsto nao reproduz a ordem de real."""
    por_edge = sorted(REAIS, key=lambda p: _prev(p)[0])
    maior_prev = por_edge[-1]
    assert REAIS[maior_prev] == min(REAIS.values()), (maior_prev, REAIS)


def test_encurtar_a_previsao_em_2_2_s_NAO_encurtou_a_peca():
    """A decisao que eu tomei nesta rodada, falsificada pela propria peca.
    A primeira versao do s025 dava edge 44,3; a publicada da 42,1; o real e 44,
    igual ao das duas pecas cuja previsao era MAIOR que 44,3 nao era."""
    edge, _ = _prev("epomeno-epipedo-s025")
    assert edge < 43.0, edge                      # foi encurtada de fato
    assert REAIS["epomeno-epipedo-s025"] == 44    # e o real nao mudou
    assert REAIS["kolejny-poziom-s024"] == 44
    assert REAIS["epomeno-epipedo-s024"] == 44


def test_o_vies_do_edge_CRESCE_quando_a_previsao_DIMINUI():
    """Retrata o '~2,5%' do 731, que era de n=2. Com o terceiro ponto o desvio
    da menor previsao e o maior de todos -- assinatura de algo que nao depende
    da previsao."""
    pontos = []
    for pacote, real in REAIS.items():
        if real != 44:
            continue
        edge, _ = _prev(pacote)
        pontos.append((edge, (real - edge) / edge))
    pontos.sort()
    assert pontos[0][1] > pontos[-1][1], pontos
    assert pontos[0][1] > 0.04, pontos[0]


def test_NAO_existe_teto_duro_de_44():
    """O que o §3.8 proibe afirmar: a peca de 39 s desmente o teto."""
    assert min(REAIS.values()) == 39


def test_as_quatro_cabem_na_faixa_do_portao_e_e_ela_que_segura():
    """O que sobrevive: a faixa larga nos dois mundos e a protecao real."""
    for pacote, real in REAIS.items():
        edge, piper = _prev(pacote)
        for d in (edge, piper):
            assert SHORT_MIN_S <= d <= SHORT_MAX_S, (pacote, d)
        assert real <= SHORT_MAX_S, (pacote, real)


def test_as_quatro_tem_DEZ_cenas__a_hipotese_ainda_nao_explica_a_de_39():
    """A hipotese do numero de cenas vai DECLARADA e incompleta: as tres de 44
    tem dez cenas, e a de 39 tambem. Logo cenas sozinhas nao explicam."""
    for pacote in REAIS:
        s = json.loads((RAIZ / "fabrica" / "specs" / f"{pacote}.json").read_text())
        assert len(s["short"]) == 10, (pacote, len(s["short"]))
