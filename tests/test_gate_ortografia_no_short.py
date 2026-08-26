"""O portao de acentuacao lia so o longo, e o short e o que vai ao ar.

MEDIDO EM 25/08/2026, escrevendo a `seja-mais-magra-006`. Escrevi as duas
partes sem acento nenhum. O portao acusou, eu reescrevi o LONGO com acento, e
na segunda passada o portao ficou MUDO — com o short ainda inteiro em ASCII.
Peguei relendo o texto na mao, que e exatamente o trabalho que um portao
existe para dispensar.

O defeito importa mais no short do que no longo: o short e o unico formato
desta frota que recebe distribuicao, e o TTS le "voce" como outra palavra que
nao "voce". Passa no portao de idioma (continua parecendo portugues), passa no
de glifos (ASCII sempre tem fonte) e chega ao ar mal pronunciado.

Somar os dois blocos numa densidade so NAO conserta, e o primeiro teste aqui
mede por que: o longo tem cerca de dezesseis vezes o texto do short, entao ele
dilui o short ate dentro da folga do portao.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import prontidao as PR  # noqa: E402


COM_ACENTO = ("Não é o preço que muda, é a alíquota. Três porcentagens "
              "diferentes saem da mesma máquina, e você paga a que estiver "
              "impressa na última linha. ")
SEM_ACENTO = ("Nao e o preco que muda, e a aliquota. Tres porcentagens "
              "diferentes saem da mesma maquina, e voce paga a que estiver "
              "impressa na ultima linha. ")


def _cenas(texto, vezes):
    return [{"nar": texto} for _ in range(vezes)]


def _spec(longo, short):
    return {"slug": "seja-mais-magra", "idioma": "pt-BR",
            "longo": longo, "short": short}


def _referencia(monkeypatch, valor=0.041):
    """Fixa a referencia do idioma: o alvo aqui e o portao, nao o corpus."""
    monkeypatch.setattr(PR, "_referencia_do_idioma", lambda *a, **k: valor)


# ------------------------------------- por que nao basta somar os dois blocos

def test_o_longo_dilui_o_short_se_medidos_juntos():
    """A conta que justifica medir separado, com o tamanho real dos blocos."""
    tabela = PR.DIACRITICOS["pt"]
    longo, short = _cenas(COM_ACENTO, 60), _cenas(SEM_ACENTO, 4)

    so_longo = PR._densidade_diacritica(longo, tabela)
    juntos = PR._densidade_diacritica(longo + short, tabela)

    assert PR._letras(longo) > 10 * PR._letras(short), "os blocos sao desiguais"
    # O short zerado derruba a densidade muito menos que a folga de metade.
    assert juntos > so_longo / 2, "juntos, um short em ASCII puro nem aparece"


# ------------------------------------------------- o defeito medido, prendido

def test_short_sem_acento_com_longo_certo_e_acusado(monkeypatch):
    """O caso exato da seja-mais-magra-006 na segunda passada."""
    _referencia(monkeypatch)
    notas = PR._gate_ortografia("/nao/existe.json",
                                _spec(_cenas(COM_ACENTO, 60),
                                      _cenas(SEM_ACENTO, 4)))
    assert len(notas) == 1
    assert "no short" in notas[0]


def test_longo_sem_acento_continua_acusado(monkeypatch):
    """O comportamento antigo nao pode ter sido trocado pelo novo."""
    _referencia(monkeypatch)
    notas = PR._gate_ortografia("/nao/existe.json",
                                _spec(_cenas(SEM_ACENTO, 60),
                                      _cenas(COM_ACENTO, 4)))
    assert len(notas) == 1
    assert "no longo" in notas[0]


def test_os_dois_errados_dao_duas_notas(monkeypatch):
    """Uma nota por bloco: consertar um nao pode calar o outro."""
    _referencia(monkeypatch)
    notas = PR._gate_ortografia("/nao/existe.json",
                                _spec(_cenas(SEM_ACENTO, 60),
                                      _cenas(SEM_ACENTO, 4)))
    assert len(notas) == 2
    assert {"no longo" in n for n in notas} == {True, False}


def test_os_dois_certos_passam(monkeypatch):
    _referencia(monkeypatch)
    assert PR._gate_ortografia("/nao/existe.json",
                               _spec(_cenas(COM_ACENTO, 60),
                                     _cenas(COM_ACENTO, 4))) == []


# ------------------------------------------------- o piso que evita alarme fal

def test_texto_curto_demais_nao_e_julgado(monkeypatch):
    """Uma frase pode nao ter acento sem que nada esteja errado."""
    _referencia(monkeypatch)
    curto = [{"nar": "Comeca amanha."}]
    assert PR._letras(curto) < PR.MINIMO_LETRAS_MEDIDAS
    assert PR._gate_ortografia("/nao/existe.json",
                               _spec(_cenas(COM_ACENTO, 60), curto)) == []


def test_o_piso_fica_abaixo_de_um_short_real():
    """Se o piso subir acima do texto de um short, o portao volta a ser cego.

    Um short desta frota tem 30 a 43 segundos de fala. Medido na spec que esta
    no repositorio, para nao depender de estimativa.
    """
    caminho = os.path.join(RAIZ, "fabrica/specs/epomeno-epipedo-011.json")
    sp = json.load(open(caminho, encoding="utf-8"))
    assert PR._letras(sp["short"]) > PR.MINIMO_LETRAS_MEDIDAS * 1.5


# ------------------------------------------ o portao continua mudo sem referen

def test_sem_referencia_nao_inventa_regra(monkeypatch):
    """Canal sem vizinha e idioma sem corpus: o portao se cala nos DOIS blocos.

    Slug inventado de proposito — com `seja-mais-magra` o portao acha as specs
    irmas no repositorio e usa a mediana delas, que e o caminho do teste acima.
    """
    _referencia(monkeypatch, valor=0.0)
    sem_vizinha = _spec(_cenas(SEM_ACENTO, 60), _cenas(SEM_ACENTO, 4))
    sem_vizinha["slug"] = "canal-que-nao-existe"
    assert PR._gate_ortografia("/nao/existe.json", sem_vizinha) == []


# ------------------------------- a referencia do canal so conta quem acentua

# Um short em que uma cena de tres acentua. Densidade a um terco da
# referencia: acima da metade da mediana rebaixada e abaixo da metade da
# referencia de quem acentua — a faixa exata em que as duas leituras
# discordam.
MEIO_ACENTO = _cenas(COM_ACENTO, 1) + _cenas(SEM_ACENTO, 2)


def _canal_falso(tmp_path, monkeypatch, densidades):
    """Monta um canal de mentira no disco e aponta o portao para ele.

    Cada valor de `densidades` vira uma spec irma com aquela acentuacao no
    LONGO — que e o bloco de onde a referencia do canal sai.
    """
    specs = tmp_path / "fabrica" / "specs"
    specs.mkdir(parents=True)
    for i, acentua in enumerate(densidades):
        texto = COM_ACENTO if acentua else SEM_ACENTO
        (specs / f"canal-de-teste-{i:03d}.json").write_text(
            json.dumps({"slug": "canal-de-teste", "idioma": "pt-BR",
                        "longo": _cenas(texto, 60), "short": _cenas(texto, 4)}),
            encoding="utf-8")
    monkeypatch.setattr(PR, "RAIZ", str(tmp_path))
    return str(specs / "canal-de-teste-999.json")


def test_uma_vizinha_zerada_nao_rebaixa_a_referencia_do_canal(tmp_path, monkeypatch):
    """O defeito de 26/08/2026: escrever uma spec CERTA afrouxou o portao.

    A labtreinamento tinha tres vizinhas — duas da fase ASCII a 0,00% e uma a
    4,57%. Mediana 0,00%, abaixo do piso, entao o portao caia na referencia do
    idioma (4,10%) e acusava o short da 004 a 1,57%. Escrevi a 006, tambem
    acentuada, e a mediana de quatro virou a media do meio: (0,00 + 4,49) / 2 =
    2,25%. Acima do piso, entao o portao passou a usar o CANAL, cujo limite e
    metade disso — 1,12% — e o mesmo short passou a ser aprovado.

    A regra ja estava escrita para a populacao do idioma e faltava aqui: uma
    vizinha com o defeito nao e referencia de nada.
    """
    _referencia(monkeypatch, valor=0.041)
    caminho = _canal_falso(tmp_path, monkeypatch, [False, True])
    sp = _spec(_cenas(COM_ACENTO, 60), MEIO_ACENTO)

    minha = PR._densidade_diacritica(sp["short"], PR.DIACRITICOS["pt"])
    acentuada = PR._densidade_diacritica(_cenas(COM_ACENTO, 60),
                                         PR.DIACRITICOS["pt"])
    # O short cai justamente na faixa que separa as duas leituras: passa pela
    # mediana rebaixada e reprova pela referencia de quem acentua.
    assert acentuada / 4 < minha < acentuada / 2

    sp["slug"] = "canal-de-teste"
    notas = PR._gate_ortografia(caminho, sp)
    assert notas and "short" in notas[0], notas
    assert "que acentuam" in notas[0], notas


def test_canal_inteiro_zerado_ainda_cai_na_referencia_do_idioma(tmp_path, monkeypatch):
    """Filtrar as zeradas nao pode deixar o portao sem populacao nenhuma.

    Com todas as vizinhas em ASCII nao sobra ninguem na mediana do canal, e o
    caminho certo continua sendo o do idioma — que e como o sx-educacao, com
    duas specs zeradas, deixou de ser um ponto cego em 20/08/2026.
    """
    _referencia(monkeypatch, valor=0.041)
    caminho = _canal_falso(tmp_path, monkeypatch, [False, False])
    sp = _spec(_cenas(SEM_ACENTO, 60), _cenas(SEM_ACENTO, 4))
    sp["slug"] = "canal-de-teste"

    notas = PR._gate_ortografia(caminho, sp)
    assert len(notas) == 2, notas
    assert all("nas specs de pt que acentuam" in n for n in notas), notas
