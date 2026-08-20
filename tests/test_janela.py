"""A hora de publicar deixou de ser sobra de escalonamento de runner.

Ate 20/08/2026 nada decidia isso: o pacote subia quando o render terminava. O
custo foi medido — o seviye-seviye, dono do melhor short da frota (mediana de
81,5 views/dia), publicou dois tercos dos seus as 03h e 04h de Istambul.

Estes testes cercam o que quebra em silencio numa regra de horario: fuso
faltando virando penalidade, horario de verao ignorado, e preferencia virando
portao — que pararia a frota.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import janela as J  # noqa: E402
import orquestra as O  # noqa: E402

UTC = dt.timezone.utc


def _em(h, dia=15, mes=8):
    return dt.datetime(2026, mes, dia, h, 0, tzinfo=UTC)


# ------------------------------------------------------------------- o fuso

def test_todo_canal_do_repo_tem_fuso():
    """Canal sem fuso publica em hora aleatoria e ninguem ve — o defeito volta
    calado para aquele canal so."""
    for yaml in sorted((RAIZ / "config" / "canais").glob("*.yaml")):
        assert yaml.stem in J.FUSO, yaml.stem


def test_o_fuso_acompanha_horario_de_verao():
    """Offset fixo acerta metade do ano e erra a outra metade, calado. Varsovia
    fica em UTC+2 no verao e UTC+1 no inverno."""
    verao = J.hora_local("kolejny-poziom", _em(12, dia=15, mes=7))
    inverno = J.hora_local("kolejny-poziom", _em(12, dia=15, mes=1))
    assert verao == 14 and inverno == 13


def test_istambul_nao_tem_horario_de_verao():
    """A Turquia fixou UTC+3 em 2016. Se este teste cair, a tabela do zoneinfo
    mudou e a janela do melhor canal da frota mudou junto."""
    assert J.hora_local("seviye-seviye", _em(12, mes=7)) == 15
    assert J.hora_local("seviye-seviye", _em(12, mes=1)) == 15


# ------------------------------------------------------------------ a janela

def test_madrugada_esta_fora_da_janela():
    # 01h UTC = 04h em Istambul, dentro da faixa morta
    assert not J.na_janela("seviye-seviye", _em(1))


def test_o_caso_que_motivou_a_regra():
    """seviye-seviye publicou as 00h e 01h UTC, que sao 03h e 04h de Istambul."""
    for h_utc in (0, 1):
        assert not J.na_janela("seviye-seviye", _em(h_utc))


def test_tarde_esta_dentro():
    # 14h UTC = 17h em Istambul
    assert J.na_janela("seviye-seviye", _em(14))


def test_canal_sem_fuso_nao_e_penalizado():
    """Desconhecido nao pode virar penalidade: um canal novo ficaria no fim da
    fila para sempre por um dado que ninguem preencheu."""
    assert J.na_janela("canal-que-nao-existe", _em(3))
    assert J.hora_local("canal-que-nao-existe", _em(3)) is None


def test_horas_ate_abrir_e_zero_quando_ja_esta_aberto():
    assert J.horas_ate_a_janela("seviye-seviye", _em(14)) == 0


def test_horas_ate_abrir_conta_certo_na_madrugada():
    # 01h UTC = 04h Istambul; a faixa morta vai ate 08h -> faltam 4h
    assert J.horas_ate_a_janela("seviye-seviye", _em(1)) == 4


# ------------------------------------------------- preferencia, nunca portao

def test_a_janela_e_preferencia_e_nao_portao():
    """Se ela bloqueasse, a frota pararia toda madrugada. O `proximo` so
    REORDENA — nao ha caminho em que a janela descarte uma spec."""
    import inspect

    fonte = inspect.getsource(O.proximo)
    assert "na_janela" in fonte
    # a janela aparece na CHAVE DE ORDENACAO, nunca num `descartadas.append`
    depois = fonte.split("na_janela")[1]
    assert "descartadas.append" not in depois.split("for canal")[0]


def test_canal_na_janela_vem_antes_do_fora(monkeypatch):
    """Dois canais com a MESMA distancia da meta: quem esta acordado passa na
    frente."""
    monkeypatch.setattr(J, "na_janela",
                        lambda slug, agora=None: slug != "dormindo")
    est = {"canais": {"dormindo": {"faltam": 9, "specs_pendentes": []},
                      "acordado": {"faltam": 9, "specs_pendentes": []}}}
    ordem = sorted(est["canais"].items(),
                   key=lambda kv: (0 if J.na_janela(kv[0]) else 1,
                                   -kv[1]["faltam"], kv[0]))
    assert [k for k, _ in ordem] == ["acordado", "dormindo"]


def test_a_meta_ainda_desempata_dentro_da_janela(monkeypatch):
    """A janela nao pode apagar a regra antiga: entre dois canais acordados,
    quem esta mais longe da meta continua vindo primeiro."""
    monkeypatch.setattr(J, "na_janela", lambda slug, agora=None: True)
    est = {"canais": {"perto": {"faltam": 1}, "longe": {"faltam": 9}}}
    ordem = sorted(est["canais"].items(),
                   key=lambda kv: (0 if J.na_janela(kv[0]) else 1,
                                   -kv[1]["faltam"], kv[0]))
    assert [k for k, _ in ordem] == ["longe", "perto"]


def test_a_faixa_morta_e_conservadora():
    """Ela afirma so o que nao precisa de medicao: madrugada e pior. Uma faixa
    larga seria uma escolha de melhor horario, e isso a frota ainda nao mediu."""
    assert (J.MORTA_ATE - J.MORTA_DE) <= 8
    assert J.MORTA_DE >= 0 and J.MORTA_ATE <= 9
