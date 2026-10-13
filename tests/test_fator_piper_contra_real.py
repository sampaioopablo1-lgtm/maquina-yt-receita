"""O FATOR_PIPER acertou DEZ peças reais -- e isto trava a validacao.

Medido em 13/10/2026 as 10:1x, lendo `contentDetails.duration` das dez peças
publicadas hoje (uma chamada, status_code 200). Esta e a PRIMEIRA validacao do
`duracao_real_prevista(..., 'piper')` contra duracao real desde que o fator
entrou, e e o contraponto do 711, onde o estimado do edge errava 10 a 20% nas
peças narradas pelo Piper.

    pacote                   real  piper  desvio
    labtreinamento-s026        25   24.5   +2.1%
    labtreinamento-s027        24   24.1   -0.6%
    labtreinamento-s028        25   25.1   -0.3%
    labtreinamento-s029        24   24.6   -2.4%
    labtreinamento-s030        25   25.8   -3.0%
    labtreinamento-s031        26   25.6   +1.5%
    labtreinamento-s032        21   20.7   +1.2%
    epomeno-epipedo-s020       37   37.8   -2.2%
    epomeno-epipedo-s021       39   37.4   +4.3%
    kolejny-poziom-s022        35   35.5   -1.5%

Mediana -0,5%, media -0,1%, faixa -3,0% a +4,3%, e NOVE das dez dentro de 1 s.
O YouTube arredonda a duracao PARA CIMA, entao 1 s e a propria granularidade.

E o achado que vem de graca: as DEZ casaram com o Piper e nenhuma com o edge
(que previa 25,3 a 42,7 contra os 21 a 39 reais). Sob a nula de meio a meio isso
e 1/1024 -- em producao e o Piper que narra.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))

import ensaio  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..", "fabrica", "specs")

# pacote -> (youtube_id, duracao REAL em segundos, lida em 13/10 10:1x)
REAIS = {
    "labtreinamento-s026": ("CdUiplaeP5g", 25),
    "labtreinamento-s027": ("uhhg3nZ1ZEY", 24),
    "labtreinamento-s028": ("UOLpIvPCl58", 25),
    "labtreinamento-s029": ("rWDgoEwwEWY", 24),
    "labtreinamento-s030": ("UEz0xdb3CL0", 25),
    "labtreinamento-s031": ("xwqCqRlE3jg", 26),
    "labtreinamento-s032": ("vHknlJnkUNA", 21),
    "epomeno-epipedo-s020": ("Q_1v7ZoBgiI", 37),
    "epomeno-epipedo-s021": ("6AZoMTvq6wc", 39),
    "kolejny-poziom-s022": ("PNWT8JndFWc", 35),
}


def _prev(pacote, provedor):
    d = json.load(open(os.path.join(RAIZ, pacote + ".json")))
    return ensaio.duracao_real_prevista(d["short"], d["voz"], provedor)


def test_as_dez_specs_ainda_existem_senao_o_teste_passa_por_vacuidade():
    for pacote in REAIS:
        assert os.path.exists(os.path.join(RAIZ, pacote + ".json")), pacote


def test_nove_das_dez_caem_dentro_de_um_segundo_do_piper():
    dentro = sum(1 for p, (_, r) in REAIS.items()
                 if abs(r - _prev(p, "piper")) <= 1.0)
    assert dentro >= 9, (
        f"so {dentro} de 10 dentro de 1 s do piper -- o FATOR_PIPER mudou e a "
        f"validacao de 13/10 nao vale mais")


def test_o_desvio_mediano_contra_o_piper_fica_abaixo_de_dois_por_cento():
    import statistics
    devs = [100.0 * (r - _prev(p, "piper")) / _prev(p, "piper")
            for p, (_, r) in REAIS.items()]
    assert abs(statistics.median(devs)) < 2.0


def test_nenhuma_das_dez_erra_mais_que_CINCO_por_cento_contra_o_piper():
    for p, (vid, r) in REAIS.items():
        dev = 100.0 * (r - _prev(p, "piper")) / _prev(p, "piper")
        assert abs(dev) < 5.0, f"{p} ({vid}) desviou {dev:+.1f}%"


def test_o_EDGE_erra_sistematicamente_para_CIMA_nestas_dez():
    # Contraponto do 711, e e o que diz que foi o Piper quem narrou: o mundo
    # `edge` preve MAIS tempo que o real em todas as dez.
    acima = sum(1 for p, (_, r) in REAIS.items() if _prev(p, "edge") > r)
    assert acima == 10, (
        f"so {acima} de 10 com edge acima do real -- se isto cair, o provedor "
        f"do runner mudou e a leitura de mira precisa ser refeita")


def test_as_dez_continuam_dentro_da_faixa_dura_do_portao():
    for p, (vid, r) in REAIS.items():
        assert 18 <= r <= 45, f"{p} ({vid}) foi ao ar com {r} s reais"
