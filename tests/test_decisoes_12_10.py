"""As decisoes de 12/10 ficam travadas, para nao voltarem por descuido.

O dono deu o controle em 12/10 com estas palavras: *"tome decisoes importantes
pra revertermos, mudando ate o formato, estilo do canal, tipo de conteudo, etc.
Assuma o controle"*. As decisoes estao em `docs/decisoes-12-10.md`.

Este arquivo nao julga se as decisoes estao CERTAS — ele garante que elas estao
APLICADAS e que a procedencia delas continua escrita. Parametro de producao que
muda sem procedencia e critério inventado, e foi para evitar isso que a trava
existia antes de o dono a levantar.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio as E  # noqa: E402
import prontidao as P  # noqa: E402


def test_a_mira_do_labtreinamento_e_curta():
    lo, hi = E.alvo_short("labtreinamento")
    assert (lo, hi) == (20.0, 26.0), (
        "DECISAO 3: 20 a 26 s REAIS. Se alguem devolveu isso para 33-37, leia "
        "docs/decisoes-12-10.md antes — aquela faixa media qual duracao era "
        "melhor DENTRO de um regime que nunca rompeu"
    )


def test_a_mira_da_FROTA_nao_mudou():
    """Mexer no global apagaria o braco do experimento 38 (698)."""
    assert E.alvo_short() == (41.5, 43.0)
    assert E.alvo_short("epomeno-epipedo") == (41.5, 43.0)
    assert E.alvo_short("kolejny-poziom") == (41.5, 43.0)


def test_o_piso_do_portao_deixa_a_mira_nova_passar():
    voz = "pt-BR-ThalitaMultilingualNeural"
    lo, hi = E.alvo_short("labtreinamento")
    est_lo = E.estimativa_para_real(lo, voz)
    assert P.SHORT_MIN_S < est_lo, (
        f"a mira pede estimativa de {est_lo:.1f} s e o piso do portao e "
        f"{P.SHORT_MIN_S} — a decisao 3 ficaria inaplicavel"
    )
    assert P.SHORT_MIN_S == 18


def test_o_TETO_do_portao_NAO_foi_afrouxado():
    """O 43,1 efetivo e elegibilidade de Short, nao habito nosso."""
    assert P.SHORT_MAX_S == 45
    assert P.SHORT_MAX_S / (1 + P.MARGEM_SHORT) <= 43.2


def test_a_mira_nova_cabe_INTEIRA_no_portao():
    voz = "pt-BR-ThalitaMultilingualNeural"
    lo, hi = E.alvo_short("labtreinamento")
    teto = P.SHORT_MAX_S / (1 + P.MARGEM_SHORT)
    for alvo in (lo, hi):
        est = E.estimativa_para_real(alvo, voz)
        assert P.SHORT_MIN_S < est < teto, (
            f"real {alvo} pede estimativa {est:.1f}, fora de "
            f"({P.SHORT_MIN_S}, {teto:.1f})"
        )


def test_a_PROCEDENCIA_das_decisoes_continua_escrita_no_codigo():
    """Limiar sem procedencia e critério inventado — inclusive o meu."""
    fonte = (RAIZ / "fabrica" / "ensaio.py").read_text(encoding="utf-8")
    for marca in ("mostPopular", "shorts-playbook", "713", "decisoes-12-10"):
        assert marca in fonte, (
            f"a procedencia {marca!r} saiu do ensaio.py: sem ela o 20-26 vira "
            "numero que eu inventei"
        )
    piso = (RAIZ / "fabrica" / "prontidao.py").read_text(encoding="utf-8")
    assert "HABITO NOSSO, SEM PROCEDENCIA" in piso, (
        "o motivo de o piso ter caido de 30 para 18 tem de ficar no arquivo"
    )


def test_o_documento_de_decisoes_existe_e_recusa_o_prazo():
    d = (RAIZ / "docs" / "decisoes-12-10.md").read_text(encoding="utf-8")
    assert "NAO aceito a meta de 31/10" in d, (
        "a decisao zero e recusar o prazo com numero. Se ela sair do documento, "
        "a proxima rodada promete 31/10 outra vez"
    )
    assert "5.000 views" in d, "a leitura que decide tem de estar declarada ANTES"
    assert "FURO QUE EU DECLARO" in d, (
        "o confundidor do 651 (os pacotes 006/007 sao adjacentes) tem de ir "
        "junto da decisao que se apoia nele"
    )
