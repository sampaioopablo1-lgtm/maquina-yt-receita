"""A legenda queimada do short SOLTO era a fala inteira — e e o caminho de TODA peca.

Medido em 19/10/2026 no `ANxWQYgtUAY` (epomeno-epipedo-s064), baixando o proprio
arquivo publicado e lendo o quadro: a faixa escura da legenda vai de y=471 a
y=562 num quadro de 360x640 -- **91 px, 14% da altura, TRES linhas de texto** --
e o perfil de pixels escuros por linha e **IDENTICO em t=1,0 s e em t=2,8 s**.
Legenda que nao muda em 1,8 s dentro da mesma cena nao esta em pedacos: e a fala
inteira congelada.

A CAUSA, e ela e a assinatura que este mesmo arquivo ja carrega: **dois donos da
mesma regra, um atualizado.** O `legenda.py` foi escrito em 09/10 justamente
porque ~18 palavras paradas por oito segundos deixavam 91% dos quadros
congelados; o conserto entrou no `fabrica.py:862` (`LG.srt(...) if pref == "s"`)
e **NAO entrou no `etapas.py`**, que escrevia

    srt.write(f"1\\n{F.st(0.2)} --> {F.st(dd - 0.15)}\\n{c['nar']}\\n")

E o `etapas.py` e o caminho do SHORT SOLTO, isto e, de praticamente toda peca da
frota. E a mesma forma do `assert 20 <= ds <= 60` cravado neste arquivo, que em
16/10 matou o run 38847013520 depois de o mp4 ja existir.

O que estes testes travam e a PROPRIEDADE, nao o texto: as duas bocas que
escrevem o `.srt` do short tem de sair da MESMA funcao, e frase de mais de
`MAX_PALAVRAS` palavras tem de virar mais de um bloco com tempos diferentes.
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))
import legenda as LG  # noqa: E402

ETAPAS = (RAIZ / "fabrica" / "etapas.py").read_text()
FABRICA = (RAIZ / "fabrica" / "fabrica.py").read_text()

FRASE = "Ο ίδιος άνθρωπος παίρνει δύο εντελώς διαφορετικές τιμές"


def test_o_short_solto_escreve_a_legenda_pela_mesma_funcao():
    assert "F.LG.srt(" in ETAPAS, (
        "o caminho do short SOLTO voltou a montar o .srt a mao; ele tem de usar "
        "a mesma funcao do fabrica.clipe_cena"
    )


def test_o_short_solto_NAO_escreve_mais_um_bloco_unico():
    # o bloco unico se reconhece pela forma: um "1\n" com o tempo da cena INTEIRA
    assert 'srt.write(f"1\\n' not in ETAPAS, (
        "bloco unico de legenda de volta no short solto: a fala congela pela "
        "cena inteira, que e o defeito de 09/10"
    )


def test_as_DUAS_bocas_do_srt_do_short_usam_LG():
    # fabrica.py (caminho do pacote) e etapas.py (short solto)
    assert re.search(r"LG\.srt\(c\[.nar.\], dd\)", FABRICA), "o fabrica.py perdeu o LG.srt"
    assert re.search(r"F\.LG\.srt\(c\[.nar.\], dd\)", ETAPAS), "o etapas.py perdeu o LG.srt"


def test_frase_longa_vira_MAIS_DE_UM_bloco_com_tempos_diferentes():
    s = LG.srt(FRASE, 4.6)
    blocos = [b for b in s.strip().split("\n\n") if b.strip()]
    assert len(blocos) >= 2, f"frase de 8 palavras saiu em {len(blocos)} bloco(s)"
    tempos = re.findall(r"(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)", s)
    assert len(tempos) == len(blocos)
    assert len(set(tempos)) == len(tempos), "dois blocos com o MESMO tempo nao animam nada"


def test_nenhum_pedaco_passa_do_limite_de_forma():
    for p in LG.pedacos(FRASE):
        assert len(p.split()) <= LG.MAX_PALAVRAS, p


def test_a_contraprova_no_outro_sentido_frase_curta_fica_em_UM_bloco():
    # sem isto, um "sempre quebre" passaria tambem — e quebrar 2 palavras em
    # duas piscaria a tela sem motivo.
    s = LG.srt("Δύο τιμές", 2.0)
    assert len([b for b in s.strip().split("\n\n") if b.strip()]) == 1


def test_a_MEDIDA_que_pegou_o_defeito_continua_escrita():
    # medicao sem procedencia escrita volta a ser opiniao na rodada seguinte
    doc = pathlib.Path(__file__).read_text()
    assert "ANxWQYgtUAY" in doc
    assert "y=471" in doc and "t=2,8" in doc
