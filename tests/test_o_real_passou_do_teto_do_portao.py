"""O REAL passou do teto de 45 s do portao `duracao`, com a previsao DENTRO.

Aprendizado 772, `alto`, medido em 15/10 as 04:1x no `epomeno-epipedo-s032`
(`XmSOfi_rnic`). O portao `duracao` passou a exigir, em 13/10 as 02:1x, que a
peca caiba em 18 a 45 s nos DOIS mundos — `edge` e `piper` — e o motivo escrito
era que o provedor se decide no runner. Esta peca passou: edge **42,5** e piper
**37,7**, os dois dentro. O provedor MEDIDO pela anotacao foi o **edge** (zero
avisos `NARRACAO PELO PIPER` no job 116243667180), e o real deu **46 s**.

**Logo previsao dentro nos dois mundos NAO poe o real dentro do teto do portao.**
E a mesma estrutura do 740/748 — onde mira verde nao punha o real na mira do
`labtreinamento` — agora no teto da FROTA, que e o numero que o portao cobra.

A aritmetica e direta e ja estava escrita na banda: o residuo e sempre positivo e
vai ate **+3,7 s** observados, logo mirar o TOPO do `ALVO_SHORT` (43,0) admite
real de ate **~46,7 s**. O teto do portao e 45. **As duas coisas nao cabem
juntas**, e isso vale para a frota inteira, nao para um canal.

**E a copy declarou isso ANTES de publicar** — "o real deve cair entre 42,6 e
46,2 s, o topo PASSA do teto de 45" — logo este e um acerto out-of-sample da
banda, e nao uma descoberta depois do fato. O que nao vale e usar isso como
confianca: a faixa tem 3,6 s de largura contra 1 s de granularidade (770).

NADA de parametro mudou (trava da §10): `ALVO_SHORT` e o teto de 18 a 45 seguem
intocados, porque a saida — mirar o piso por padrao, ou descontar o residuo da
mira — e parametro de producao e decisao do dono. O que muda e a REDACAO: mire o
piso quando a voz nao exigir o topo.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import ensaio  # noqa: E402
import mira  # noqa: E402

PECA = "epomeno-epipedo-s032"
PREV_EDGE, PREV_PIPER, REAL = 42.5, 37.7, 46
TETO_DO_PORTAO = 45.0


def test_a_previsao_estava_DENTRO_nos_dois_mundos():
    assert 18.0 <= PREV_PIPER <= TETO_DO_PORTAO
    assert 18.0 <= PREV_EDGE <= TETO_DO_PORTAO


def test_e_o_real_ficou_FORA_do_teto_do_portao():
    assert REAL > TETO_DO_PORTAO


def test_o_residuo_esta_DENTRO_da_banda_e_com_o_sinal_ESTABELECIDO():
    r = REAL - PREV_EDGE
    lo, hi = mira.RESIDUO_OBSERVADO
    assert lo <= r <= hi, (r, mira.RESIDUO_OBSERVADO)
    # 770: o sinal so esta estabelecido quando a folga passa do passo de 1 s
    assert r > 1.0


def test_o_TOPO_do_alvo_da_frota_NAO_cabe_no_teto_do_portao():
    """A incompatibilidade e aritmetica, dados o alvo e a banda."""
    piso_alvo, topo_alvo = ensaio.ALVO_SHORT
    assert topo_alvo + mira.RESIDUO_OBSERVADO[1] > TETO_DO_PORTAO, (
        "se isto deixar de valer, o 772 tem de ser relido: ou a banda encolheu "
        "ou o alvo desceu")
    # e o PISO do alvo tambem nao salva, o que torna a nota mais forte
    assert piso_alvo + mira.RESIDUO_OBSERVADO[1] > TETO_DO_PORTAO


def test_o_piso_do_alvo_e_MENOS_exposto_que_o_topo():
    """O que a nota autoriza a fazer hoje, e e so redacao."""
    piso_alvo, topo_alvo = ensaio.ALVO_SHORT
    assert piso_alvo < topo_alvo
    exposicao_piso = piso_alvo + mira.RESIDUO_OBSERVADO[1] - TETO_DO_PORTAO
    exposicao_topo = topo_alvo + mira.RESIDUO_OBSERVADO[1] - TETO_DO_PORTAO
    assert exposicao_piso < exposicao_topo


def test_os_LIMITES_do_portao_seguem_INTOCADOS():
    """Trava da §10: este aprendizado NAO virou limiar novo."""
    fonte = (RAIZ / "fabrica" / "prontidao.py").read_text()
    assert "45" in fonte
    # O piso foi a ZERO em 16/10 as 21:2x (`kolejny-poziom-s045`, 41,0 -> 41).
    # 17/10 20:1x: o piso ficou NEGATIVO (-0,6) com o `epomeno-epipedo-s054`
    # (41,6 -> 41), o PRIMEIRO ponto abaixo da previsao em 78. O `==` fica, com o
    # valor novo, porque e ele que obriga a reler a cada movimento da banda.
    assert mira.RESIDUO_OBSERVADO == (-0.6, 4.0)
