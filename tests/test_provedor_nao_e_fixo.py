"""O PROVEDOR DE VOZ NAO E FIXO -- medido em 13/10 as 16:2x, e retrata o 724.

O aprendizado 724 (desta mesma manha) concluiu, das dez pecas publicadas ate as
10:1x: *"as DEZ casaram com o Piper e NENHUMA com o edge. Sob a nula de meio a
meio, 1/1024. Em producao e o Piper que narra."*

**As duas pecas das 15:17 e 16:12 de hoje falsificam a segunda frase.** Duracao
REAL (`contentDetails.duration`, que o YouTube ARREDONDA PARA CIMA) contra as
duas previsoes de `ensaio.duracao_real_prevista`:

    peca                 real   edge    piper   casa com
    7qreIlqtUIU (s024)    44    43,1    38,2    EDGE  (+2,1% / +15,2%)
    xlQvH6JjrB4 (s023)    39    43,1    36,7    nenhum dos dois de perto

E o `s024` e o caso duro: **o real ficou ACIMA da previsao do edge** (44 > 43,1),
o que o teste `test_o_EDGE_erra_sistematicamente_para_CIMA_nestas_dez` do 724
declarava nao acontecer na frota -- aquele teste segue valendo para as dez pecas
em que foi ancorado, e **nao se generaliza para a frota**, que e exatamente o
erro de enquadramento do 679/698/725.

**O codigo sempre disse isso, e eu nao li:** `fabrica.py:598-620` tenta o
`edge_tts` TRES vezes e so cai no Piper na terceira falha. Entao o provedor e
decidido **por cena e por run**, pelo estado da rede do runner -- nao por
configuracao. As dez pecas do 724 mediram um runner em que o edge estava caindo;
elas nao mediram uma escolha.

**O que isto CONFIRMA, e e o conserto das 02:1x de hoje:** o portao `duracao`
exigir que a peca caiba em 18 a 45 s nos DOIS mundos era a decisao certa, e por
um motivo mais forte do que o que eu escrevi na epoca. Eu escrevi "o provedor se
decide no runner"; agora esta medido que ele se decide **de um run para o outro**.

**O que isto DERRUBA, e era proposta minha de hoje de manha:** o desenho
pre-registrado "mirar a faixa no mundo `piper`, ja que e ele quem narra".
**Nao se mira um mundo que nao se controla.** A mira tem de valer nos dois, que
e o que o `fabrica/mira.py` ja relata e o que o portao ja cobra.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402
from prontidao import SHORT_MAX_S, SHORT_MIN_S  # noqa: E402

# Medido as 16:2x de 13/10, `status_code` 200, uma chamada, part=contentDetails.
REAIS = {
    "epomeno-epipedo-s024": 44,   # 7qreIlqtUIU, publicada 16:12:50Z
    "kolejny-poziom-s023": 39,    # xlQvH6JjrB4, publicada 15:17:19Z
}


def _spec(pacote):
    return json.loads((RAIZ / "fabrica" / "specs" / f"{pacote}.json").read_text())


def _prev(pacote):
    s = _spec(pacote)
    cenas, voz = s["short"], s["voz"]
    return (ensaio.duracao_real_prevista(cenas, voz, "edge"),
            ensaio.duracao_real_prevista(cenas, voz, "piper"))


def test_as_duas_pecas_existem_e_tem_as_duas_previsoes():
    for pacote in REAIS:
        edge, piper = _prev(pacote)
        assert edge > piper > 0, (pacote, edge, piper)


def test_o_s024_casa_com_o_EDGE_e_nao_com_o_piper():
    """O caso que derruba 'em producao e o Piper que narra'."""
    edge, piper = _prev("epomeno-epipedo-s024")
    real = REAIS["epomeno-epipedo-s024"]
    assert abs(real - edge) < abs(real - piper), (real, edge, piper)
    assert abs(real - edge) / real < 0.05, (real, edge)
    assert abs(real - piper) / real > 0.10, (real, piper)


def test_o_real_do_s024_ficou_ACIMA_da_previsao_do_edge():
    """O teste do 724 exigia edge > real em 10 de 10. Aqui e o contrario, e
    por isso aquele teste e sobre AQUELAS DEZ e nao sobre a frota."""
    edge, _ = _prev("epomeno-epipedo-s024")
    assert REAIS["epomeno-epipedo-s024"] > edge


def test_as_duas_pecas_discordam_entre_si_sobre_qual_mundo_vale():
    """Uma casa com o edge, a outra nao casa com nenhum de perto. Se as duas
    passassem a casar com o mesmo mundo, este teste quer ser revisto."""
    casou_edge = []
    for pacote, real in REAIS.items():
        edge, piper = _prev(pacote)
        casou_edge.append(abs(real - edge) < abs(real - piper))
    assert len(set(casou_edge)) == 2, casou_edge


def test_as_duas_cabem_na_faixa_do_portao_nos_DOIS_mundos():
    """E o motivo pelo qual nenhuma das duas saiu fora da faixa apesar de o
    provedor ser imprevisivel: o portao cobra os dois mundos desde 13/10."""
    for pacote in REAIS:
        edge, piper = _prev(pacote)
        for d in (edge, piper):
            assert SHORT_MIN_S <= d <= SHORT_MAX_S, (pacote, d)


def test_o_fallback_do_piper_e_TERCEIRA_tentativa_e_nao_configuracao():
    """A causa do achado esta no codigo: o Piper e plano B por cena, nao a voz
    escolhida. Se isto virar configuracao, este teste quer falhar para que
    alguem releia o raciocinio acima."""
    fonte = (RAIZ / "fabrica" / "fabrica.py").read_text()
    assert "for tentativa in range(3)" in fonte
    assert "if tentativa == 2:" in fonte
    assert "import voz_piper as VP" in fonte
