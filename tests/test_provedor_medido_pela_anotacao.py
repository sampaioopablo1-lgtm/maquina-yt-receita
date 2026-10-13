"""O PROVEDOR SE MEDE, NAO SE INFERE -- e isto RETRATA o 732, que e meu e de
uma hora antes.

**A medição que faltava, e ela era barata.** O `voz_piper.aviso_de_calibracao`
emite `::warning::NARRACAO PELO PIPER (fallback)...`, e `::warning::` SAI pelas
ANOTAÇÕES do job (`check-runs/<job>/annotations`). Logo o provedor de cada cena
e' observavel sem ler log nenhum. Eu passei tres rodadas INFERINDO o provedor
pela distancia entre previsao e real, quando bastava contar avisos.

Medido as 19:1x de 13/10, nos quatro renders:

    peca                  avisos_piper   provedor   prev    real   desvio
    kolejny-poziom-s023        10         PIPER     36,7     39    +6,4%
    epomeno-epipedo-s024        0         edge      43,1     44    +2,1%
    kolejny-poziom-s024         0         edge      42,9     44    +2,5%
    epomeno-epipedo-s025        0         edge      42,1     44    +4,5%

**AS QUATRO CASAM COM O PROVEDOR QUE DE FATO NARROU**, e o vies e' sempre
POSITIVO: +2,1 / +2,5 / +4,5 / +6,4%.

**O QUE CAI DO 732, e era a sua frase central:** "a previsao NAO prediz".
Ela vinha de eu comparar o real contra o mundo `edge` em TRES das quatro pecas
sem saber qual mundo havia narrado -- e numa delas (`s023`) o mundo era o outro.
Comparador escolhido sem medir, que e' o efeito (C) da rotina.

**E o "paradoxo" das tres previsoes diferentes com o mesmo real tambem cai, pelo
§3.8: o instrumento nao pode produzir aquele achado.** As tres previsoes caem
dentro de **1,0 s** uma da outra (42,1 / 42,9 / 43,1), e a duracao real tem
granularidade de **1 s com arredondamento PARA CIMA**. Tres valores num intervalo
de um segundo devolvendo o mesmo inteiro nao e' ausencia de relacao -- e' falta de
RESOLUCAO. Eu chamei de achado o que era o limite do instrumento.

**E a terceira afirmacao do 732 era um comparador escolhido:** eu disse que
"encurtar a previsao em 2,2 s nao encurtou a peca", comparando a versao publicada
do `s025` com OUTRAS pecas. A primeira versao (edge 44,3) **nunca foi
renderizada**, logo nao existe o real dela. Nao ha medida de antes-e-depois da
MESMA peca, e eu apresentei uma como se houvesse.

**O QUE SOBREVIVE E SAI FORTALECIDO:**
  - **730**: o provedor nao e' fixo. Agora com prova DIRETA e nao inferida --
    dez avisos num render e zero nos outros tres, no mesmo dia.
  - **731**: o vies e' para CIMA. Com n=3 no edge a mediana e' **+2,5%**, e o
    piper tem **+6,4%** com n=1. O portao de 18 a 45 nos DOIS mundos segue sendo
    a protecao certa.

**A REGRA QUE FICA, e e' de metodo:** antes de inferir qual provedor narrou,
CONTE OS AVISOS. Um `::warning::` por cena do Piper, zero se o edge venceu.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402

# Medido as 19:1x de 13/10 contando `::warning::NARRACAO PELO PIPER` nas
# anotacoes do job `produzir` de cada render.
MEDIDO = {
    "kolejny-poziom-s023": {"real": 39, "prov": "piper", "avisos": 10,
                            "render": "38420250327"},
    "epomeno-epipedo-s024": {"real": 44, "prov": "edge", "avisos": 0,
                             "render": "38428324742"},
    "kolejny-poziom-s024": {"real": 44, "prov": "edge", "avisos": 0,
                            "render": "38436428982"},
    "epomeno-epipedo-s025": {"real": 44, "prov": "edge", "avisos": 0,
                             "render": "38444637633"},
}


def _prev(pacote, provedor):
    s = json.loads((RAIZ / "fabrica" / "specs" / f"{pacote}.json").read_text())
    return ensaio.duracao_real_prevista(s["short"], s["voz"], provedor)


def test_cada_peca_casa_com_o_provedor_que_de_fato_narrou():
    """O fato que retrata o 732."""
    for pacote, d in MEDIDO.items():
        outro = "edge" if d["prov"] == "piper" else "piper"
        meu = abs(d["real"] - _prev(pacote, d["prov"]))
        alheio = abs(d["real"] - _prev(pacote, outro))
        assert meu < alheio, (pacote, meu, alheio)


def test_o_vies_e_sempre_POSITIVO_nos_quatro():
    """A previsao SUBESTIMA, qualquer que seja o provedor."""
    for pacote, d in MEDIDO.items():
        prev = _prev(pacote, d["prov"])
        assert d["real"] > prev, (pacote, d["real"], prev)


def test_o_vies_do_edge_fica_abaixo_de_5_porcento_com_n_tres():
    desvios = [(d["real"] - _prev(p, "edge")) / _prev(p, "edge")
               for p, d in MEDIDO.items() if d["prov"] == "edge"]
    assert len(desvios) == 3, desvios
    for x in desvios:
        assert 0 < x < 0.05, x


def test_o_piper_erra_MAIS_que_o_edge__n_um_declarado():
    pip = [(d["real"] - _prev(p, "piper")) / _prev(p, "piper")
           for p, d in MEDIDO.items() if d["prov"] == "piper"]
    edg = [(d["real"] - _prev(p, "edge")) / _prev(p, "edge")
           for p, d in MEDIDO.items() if d["prov"] == "edge"]
    assert len(pip) == 1, pip
    assert pip[0] > max(edg), (pip, edg)


def test_as_tres_do_edge_caem_dentro_de_UM_segundo__e_por_isso_nao_distinguem():
    """O §3.8 aplicado: o instrumento nao tem resolucao para separa-las, logo
    'tres previsoes diferentes, um real' nao era achado."""
    prev = sorted(_prev(p, "edge") for p, d in MEDIDO.items()
                  if d["prov"] == "edge")
    assert prev[-1] - prev[0] <= 1.0, prev
    reais = {d["real"] for d in MEDIDO.values() if d["prov"] == "edge"}
    assert reais == {44}, reais


def test_o_aviso_do_piper_e_WARNING_e_por_isso_sai_na_anotacao():
    """A propriedade que torna a medicao barata. Se alguem trocar por `print`,
    o provedor volta a ser inferido no olho e este teste quer falhar."""
    import voz_piper as VP
    msg = VP.aviso_de_calibracao("pl-PL-MarekNeural")
    assert msg.startswith("::warning::"), msg
    assert "NARRACAO PELO PIPER" in msg


def test_UM_aviso_por_CENA__e_a_contagem_bate_com_as_cenas_da_spec():
    """Dez avisos no s023 e ele tem dez cenas. E' assim que a contagem vira
    medida do provedor e nao so um sinal binario."""
    s = json.loads((RAIZ / "fabrica" / "specs" / "kolejny-poziom-s023.json")
                   .read_text())
    assert MEDIDO["kolejny-poziom-s023"]["avisos"] == len(s["short"]) == 10
