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
