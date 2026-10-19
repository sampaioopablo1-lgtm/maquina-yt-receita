"""O teto de "6 envios/dia" caiu: a setima peca da janela passou sem 403.

MEDIDO EM 19/10/2026 as 00:49:51 UTC. A secao de cota do CLAUDE.md declarou o
discriminador em letra — "se um envio passar com a janela nesta conta, e prova
de que o projeto tem extensao" — e a producao o executou sozinha, sem
experimento inventado: o dono pediu uma peca de teste e mandou postar agora.

A aritmetica de 10.000/1.600 = 6 nunca esteve errada. O que estava errado era a
PREMISSA de que a cota deste projeto e a padrao de 10.000 — premissa que eu
declarei como nao verificada e apresentei ao dono como conta.

O que este arquivo trava:

  1. a conta que derruba o teto (7 pecas na janela x 1.600 > 10.000);
  2. que o resultado e um PISO e nao um teto novo — trocar 6 por outro numero
     suposto seria repetir o erro com outro digito;
  3. que a regra da JANELA (07:00 UTC) sobrevive, porque ela e sobre quando
     contar e nao sobre quanto cabe;
  4. e que a retratacao continua escrita onde a afirmacao foi feita.
"""
import datetime as dt
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CLAUDE = (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")

CUSTO_ENVIO = 1600
COTA_PADRAO = 10000
PACIFICO_OUT_2026 = dt.timezone(dt.timedelta(hours=-7))

# As SETE da janela que abriu as 07:00 UTC de 18/10, em UTC.
NA_JANELA = (
    "2026-10-18T18:16:07", "2026-10-18T19:12:33", "2026-10-18T20:12:56",
    "2026-10-18T21:12:03", "2026-10-18T22:13:23", "2026-10-18T23:13:05",
    "2026-10-19T00:49:51",          # labtreinamento-s081 = a5BV9xEQKvw
)


def _inicio_da_janela(agora):
    local = agora.astimezone(PACIFICO_OUT_2026)
    return local.replace(hour=0, minute=0, second=0,
                         microsecond=0).astimezone(dt.timezone.utc)


def test_as_SETE_caem_na_MESMA_janela():
    """Sem isto a conta nao vale: duas janelas de seis nao provam nada."""
    agora = dt.datetime(2026, 10, 19, 0, 50, tzinfo=dt.timezone.utc)
    ini = _inicio_da_janela(agora)
    dentro = [p for p in NA_JANELA
              if dt.datetime.fromisoformat(p).replace(tzinfo=dt.timezone.utc) >= ini]
    assert len(dentro) == 7, dentro
    assert ini.hour == 7 and ini.date() == dt.date(2026, 10, 18), ini


def test_a_SETIMA_nao_cabia_na_cota_PADRAO():
    """A conta que derruba a premissa, e ela e aritmetica."""
    usado = 7 * CUSTO_ENVIO
    assert usado == 11200
    assert usado > COTA_PADRAO, (usado, COTA_PADRAO)
    # e a sexta ja deixava sobra menor que um envio
    assert COTA_PADRAO - 6 * CUSTO_ENVIO < CUSTO_ENVIO


def test_o_resultado_e_um_PISO_e_nao_um_teto_novo():
    """Trocar 6 por outro numero suposto repetiria o erro com outro digito."""
    assert "PISO, não um teto" in CLAUDE
    assert "teto verdadeiro segue desconhecido" in CLAUDE.lower() or \
           "O teto verdadeiro segue desconhecido" in CLAUDE
    # e o caminho de descobrir vai escrito, senao a nota nao aciona nada
    assert "403 quota" in CLAUDE


def test_a_regra_da_JANELA_sobrevive_a_queda_do_numero():
    """Ela e sobre QUANDO contar; so o numero 6 caiu."""
    assert "07:00 UTC" in CLAUDE
    assert "continua valendo" in CLAUDE


def test_a_retratacao_fica_ONDE_a_afirmacao_foi_feita():
    """Retratar so no fim do arquivo deixa o meio contradizendo o fim."""
    i_afirm = CLAUDE.index("~6 ENVIOS DE VÍDEO POR DIA POR PROJETO")
    i_queda = CLAUDE.index("O TETO DE 6/DIA CAIU")
    assert i_queda > i_afirm, "a queda tem de vir DEPOIS da afirmacao que ela derruba"
    # e perto o bastante para quem le a afirmacao alcancar a queda
    assert i_queda - i_afirm < 6000, i_queda - i_afirm


def test_a_peca_de_5s_NAO_entrou_na_serie_do_mira():
    """Somar um ponto de 4,4 s a uma banda de 23 a 44 s e o erro de 679/698/725."""
    serie = (RAIZ / "tests"
             / "test_residuo_quebra_o_limite_de_dois_segundos.py").read_text(
                 encoding="utf-8")
    assert serie.count('", ') > 50, "a serie encolheu — este teste deixaria de medir"
    assert "labtreinamento-s081" not in serie, (
        "a peca de 5 s entrou na banda de 23 a 44 s"
    )
    import sys
    sys.path.insert(0, str(RAIZ / "fabrica"))
    import mira
    assert mira.RESIDUO_N == 105, mira.RESIDUO_N
    assert "UM ponto, e ele é este" in CLAUDE


def test_o_PROVEDOR_e_o_CONTROLE_ficam_registrados():
    """Sem eles o real de 5 s vira numero sem procedencia."""
    assert "a5BV9xEQKvw" in CLAUDE
    assert "117837682861" in CLAUDE, "o job que mede o provedor saiu"
    assert "OhrGlJvnBoM" in CLAUDE, "a peca de controle saiu — o veredito fica cego"
