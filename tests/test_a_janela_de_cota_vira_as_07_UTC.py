"""A janela de cota da API vira as 07:00 UTC, e nao a meia-noite.

MEDIDO EM 19/10/2026 as 00:2x, e foi isto que impediu um `403 quota`.

A `sonda_oauth` leu o numero do projeto do Google Cloud dos tres canais e eles
**compartilham um so**: `777159180424` (job `117829119323`). Logo o teto de
`10.000 / 1.600` = 6 envios de video por dia vale para a FROTA INTEIRA.

E a cota da YouTube Data API zera a **meia-noite do Pacifico**, nao em UTC. Em
outubro de 2026 vigora o PDT (UTC-7), logo a janela corre de 07:00 UTC a 07:00
UTC. As seis pecas de 18/10 sairam entre 18:16 e 23:13 UTC — **todas dentro da
janela que fecha as 07:00 de 19/10** —, somando 9.600 de 10.000 e deixando 400.
Um envio custa 1.600: **nao cabe.**

Este arquivo trava DUAS coisas, e a segunda e a que me pegaria de novo:

  1. a aritmetica do teto (derivada, nunca cravada a mao);
  2. **que a contagem e por JANELA e nao por dia calendario.** Contar o dia
     calendario diria "zero pecas hoje, pode publicar" as 00:1x — e isso e a
     mesma classe do 771, onde o dia recem-comecado apagava as ultimas horas e
     o contador nao ordenava nada na virada da meia-noite.
"""
import datetime as dt

CUSTO_ENVIO = 1600
COTA_PADRAO = 10000
# Deslocamento do Pacifico em outubro de 2026: o horario de verao dos EUA so
# termina em 1/nov/2026, logo PDT = UTC-7 e a janela vira as 07:00 UTC.
PACIFICO_OUT_2026 = dt.timezone(dt.timedelta(hours=-7))

# As seis peças de 18/10 que a sessao publicou, em UTC.
PUBLICADAS_18 = (
    "2026-10-18T18:16:07", "2026-10-18T19:12:33", "2026-10-18T20:12:56",
    "2026-10-18T21:12:03", "2026-10-18T22:13:23", "2026-10-18T23:13:05",
)


def inicio_da_janela(agora: dt.datetime) -> dt.datetime:
    """Comeco da janela de cota que contem `agora`, em UTC."""
    local = agora.astimezone(PACIFICO_OUT_2026)
    virada = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return virada.astimezone(dt.timezone.utc)


def _usado(agora: dt.datetime) -> int:
    ini = inicio_da_janela(agora)
    n = sum(1 for p in PUBLICADAS_18
            if dt.datetime.fromisoformat(p).replace(tzinfo=dt.timezone.utc) >= ini)
    return n * CUSTO_ENVIO


def test_o_teto_e_DERIVADO_e_nao_cravado():
    assert COTA_PADRAO // CUSTO_ENVIO == 6


def test_a_janela_vira_as_07_UTC_e_nao_a_meia_noite():
    meia_noite_utc = dt.datetime(2026, 10, 19, 0, 20, tzinfo=dt.timezone.utc)
    ini = inicio_da_janela(meia_noite_utc)
    assert ini.hour == 7, ini
    assert ini.date() == dt.date(2026, 10, 18), ini
    assert ini != meia_noite_utc.replace(hour=0, minute=0)


def test_as_SEIS_pecas_de_18_10_caem_TODAS_na_mesma_janela():
    agora = dt.datetime(2026, 10, 19, 0, 20, tzinfo=dt.timezone.utc)
    assert _usado(agora) == 6 * CUSTO_ENVIO == 9600


def test_as_00_2x_de_19_10_NAO_cabia_mais_um_envio():
    """O assert que impediu o 403: a sobra era 400 e o envio custa 1.600."""
    agora = dt.datetime(2026, 10, 19, 0, 20, tzinfo=dt.timezone.utc)
    sobra = COTA_PADRAO - _usado(agora)
    assert sobra == 400, sobra
    assert sobra < CUSTO_ENVIO, "a conta que proibiu publicar mudou"


def test_DEPOIS_das_07_UTC_a_janela_zera_e_cabe():
    """A producao volta as 07:0x, e isso tambem e aritmetica."""
    agora = dt.datetime(2026, 10, 19, 7, 10, tzinfo=dt.timezone.utc)
    assert _usado(agora) == 0, "a janela nova herdou peca da anterior"
    assert COTA_PADRAO - _usado(agora) >= CUSTO_ENVIO


def test_contar_o_DIA_CALENDARIO_daria_a_resposta_ERRADA():
    """A contraprova que justifica este arquivo existir — classe do 771.

    Pelo dia calendario UTC, as 00:2x de 19/10 havia ZERO pecas publicadas
    "hoje", logo a leitura ingenua liberaria o envio. Pela JANELA, havia seis.
    """
    agora = dt.datetime(2026, 10, 19, 0, 20, tzinfo=dt.timezone.utc)
    por_dia = [p for p in PUBLICADAS_18
               if dt.datetime.fromisoformat(p).date() == agora.date()]
    assert len(por_dia) == 0, "o dia calendario deixou de ser enganoso aqui"
    por_janela = _usado(agora) // CUSTO_ENVIO
    assert por_janela == 6
    assert por_janela != len(por_dia), "as duas contagens coincidiram"


def test_os_7_por_dia_por_canal_ficam_acima_do_teto_COMPARTILHADO():
    """Com um projeto para os tres, 21 envios/dia pedem 3,4x a cota."""
    pedido = 7 * 3
    assert pedido * CUSTO_ENVIO == 33600
    assert pedido * CUSTO_ENVIO > 3 * COTA_PADRAO
    # e mesmo o ritmo ATUAL (2/dia/canal) ja bate no teto
    atual = 2 * 3
    assert atual * CUSTO_ENVIO == 9600
    assert COTA_PADRAO - atual * CUSTO_ENVIO < CUSTO_ENVIO


def test_o_projeto_COMPARTILHADO_fica_registrado_com_a_evidencia():
    """Sem o id e o job, a proxima rodada nao sabe se isso foi medido ou suposto."""
    import pathlib
    claude = (pathlib.Path(__file__).resolve().parent.parent
              / "CLAUDE.md").read_text(encoding="utf-8")
    assert "777159180424" in claude, "o id do projeto medido saiu do CLAUDE.md"
    assert "117829119323" in claude, "o job que mediu saiu — virou suposicao"
    assert "07:00 UTC" in claude
