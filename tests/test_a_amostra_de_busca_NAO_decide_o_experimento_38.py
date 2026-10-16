"""Eu colhi dados publicos para o experimento 38 e a nossa regua disse NAO.

Pedido do dono de 16/10 ("quero bater recordes, destravar"). O experimento 38
(duracao do short) esta aberto e sem veredito desde 09/10, e a rota publica que
eu achei na pesquisa permite colher duracao e views de peca alheia de graca.
Colhi: 18 shorts do nicho `excel/planilha`, por oito buscas distintas.

A MEDIANA PARECIA FALAR: 15.492 views na faixa de 20-35 s contra 4.032 na de
45-70 s — fator 3,8, e na direcao que eu ja acreditava (os nossos 41-43 s sao
longos demais). **Era exatamente a hora de aplicar o 693 em vez de relatar.**

E A REGUA REPROVOU POR DOIS MOTIVOS INDEPENDENTES:

1. **As faixas se sobrepoem quase inteiras** — 4.416 a 899.277 contra 11 a
   413.816. O 693 e explicito: "se a peca cai DENTRO da faixa antiga, nao ha
   leitura, qualquer que seja a mediana". Com CV ~0,66 e n de 7 e 11, um fator
   3,8 de mediana nao e sinal.
2. **ZERO das 18 pecas cai na faixa de 35 a 45 s, que e onde as NOSSAS vivem.**
   A amostra nao cobre o nosso tratamento, logo nao pode falar dele nem a favor
   nem contra.

E HA UM CONFUNDIDOR QUE SOZINHO JA MATARIA A LEITURA: a amostra vem de BUSCA, e
busca ordena por relevancia e engajamento. Logo ela e enviesada PARA o que foi
bem — nao e amostra do nicho, e a selecao correlaciona com a propria variavel de
resposta.

O QUE ISTO NAO E: argumento a favor dos 41-43 s. O 38 continua sem veredito, e
duas fontes independentes seguem apontando para curto (o nosso `mostPopular`:
10-35 s; o `shorts-playbook`: 15-60 s com picos em 13 e 60).

O QUE ISTO E: o registro de que eu colhi, medi e NAO movi parametro — que a §10
chama de decisao legitima quando o braco precisa de n.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import ensaio  # noqa: E402

# A amostra real de 16/10, 18 shorts do nicho, oito buscas (duracao_s, views).
AMOSTRA_20_35 = [4416, 5749, 10101, 15492, 133906, 819085, 899277]
AMOSTRA_45_70 = [11, 351, 401, 2082, 2555, 4032, 4582, 8902, 50980, 82824, 413816]
FAIXA_NOSSA_S = (35, 45)


def test_as_faixas_se_SOBREPOEM_logo_nao_ha_leitura():
    """A regra do 693: faixa manda mais que mediana."""
    a, b = AMOSTRA_20_35, AMOSTRA_45_70
    sobrepoe = not (min(a) > max(b) or max(a) < min(b))
    assert sobrepoe, (
        "se as faixas se separarem com n maior, ISTO passa a ser leitura e o "
        "experimento 38 tem de ser relido — nao ajuste o teste, releia a nota"
    )


def test_a_mediana_parecia_falar_e_isso_fica_REGISTRADO():
    """Para a rodada seguinte nao reaproveitar o 3,8x como se fosse achado."""
    import statistics as st
    razao = st.median(AMOSTRA_20_35) / st.median(AMOSTRA_45_70)
    assert razao > 3, "o fator de mediana era grande, e mesmo assim nao decide"
    assert "fator 3,8" in __doc__


def test_a_amostra_NAO_cobre_a_faixa_das_NOSSAS_pecas():
    """O motivo mais simples de nao concluir: ela nem mede o nosso tratamento."""
    lo, hi = FAIXA_NOSSA_S
    alvo = ensaio.ALVO_SHORT  # a mira da frota, em segundos estimados
    assert lo <= alvo[0] <= hi and lo <= alvo[1] <= hi, (
        f"a mira da frota {alvo} saiu da faixa {FAIXA_NOSSA_S}; se ela mudou, "
        f"esta nota precisa ser refeita com a faixa nova"
    )


def test_o_confundidor_da_BUSCA_vai_declarado():
    """Amostra de busca correlaciona com a variavel de resposta."""
    # Normaliza antes de casar: a frase quebra em duas linhas no docstring, e
    # casar a string crua reprova por FORMATACAO em vez de por propriedade —
    # a mesma classe do 743/753/761.
    doc = " ".join((__doc__ or "").split())
    assert "busca ordena por relevancia e engajamento" in doc
    assert "enviesada PARA o que foi bem" in doc


def test_nenhum_parametro_de_producao_foi_tocado():
    """A trava da §10: o 38 segue sem veredito e ALVO_SHORT nao muda."""
    assert ensaio.ALVO_SHORT == (41.5, 43.0), (
        "ALVO_SHORT mudou. Se foi por decisao do dono, otimo — mas esta nota "
        "dizia que a amostra de busca NAO autoriza a mudanca"
    )
