"""O segundo angulo precisa achar os capitulos SEM prosa e SEM API.

Historia, 12/10/2026. O achado da rodada das 10:07 foi que a unidade de pauta e
(longo, familia de capitulo). Para escrever o primeiro segundo angulo eu precisei
achar qual spec LOCAL carrega os capitulos do longo `6BeNHqT2okA`, e descobri
isso lendo a PROSA do aviso do short.

**A minha primeira tentativa de mecanizar estava errada, e o teste real pegou:**
eu resolvi `youtube_id -> pacote` pelo retrato `fabrica/ponte/videos.json`. O
retrato NAO tem nem o id nem o pacote `labtreinamento-010` — nenhum dos dois, em
nenhuma linha. Nao existe mapeamento estruturado local; o par existe so na prosa.

O conserto casa contra um VOCABULARIO FECHADO: os nomes de spec que existem em
`fabrica/specs/`. Qualquer acerto e verificavel abrindo o arquivo.

E a saida diz "mencionado", nao "usado" — porque a copy de um short pode citar um
capitulo justamente para dizer que NAO o levou, e foi o que a minha propria copy
do `s014` fez com "Copia fiel".
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import segundo_angulo as SA  # noqa: E402

ORIGEM = "6BeNHqT2okA"
PACOTE = "labtreinamento-010"


def test_o_retrato_NAO_resolve_esta_origem_e_e_por_isso_que_o_modulo_mudou():
    """A ancora do defeito: se o retrato passasse a ter o id, revise o modulo."""
    d = json.load(open(RAIZ / "fabrica/ponte/videos.json", encoding="utf-8"))
    if isinstance(d, dict):
        d = d.get("videos") or next(iter(d.values()))
    ids = {v.get("youtube_id") for v in d if isinstance(v, dict)}
    pacotes = {str(v.get("pacote") or "") for v in d if isinstance(v, dict)}
    assert ORIGEM not in ids, (
        "o retrato passou a conter esta origem — a premissa do conserto mudou")
    assert PACOTE not in pacotes


def test_resolve_pelo_VOCABULARIO_de_specs_e_nao_por_padrao_de_texto():
    assert SA.pacote_do_id(ORIGEM) == PACOTE
    # o vocabulario e fechado: so nomes que existem como arquivo
    vocab = SA.nomes_de_spec()
    assert PACOTE in vocab
    for n in vocab:
        assert (RAIZ / "fabrica/specs" / f"{n}.json").exists()


def test_o_mais_longo_casa_primeiro():
    """Senao `labtreinamento-01` roubaria o lugar de `labtreinamento-010`."""
    v = SA.nomes_de_spec()
    assert len(v) == len(set(v))
    assert all(len(v[i]) >= len(v[i + 1]) for i in range(len(v) - 1))


def test_nao_devolve_o_PROPRIO_short_como_pacote_de_origem():
    """O short tambem e uma spec; ele nao carrega as cenas do longo."""
    p = SA.pacote_do_id(ORIGEM)
    assert p not in [n for n, _ in SA.shorts_da_origem(ORIGEM)]


def test_exige_que_o_pacote_TENHA_cenas_de_longo():
    assert SA.capitulos_do_pacote(PACOTE), "a ancora perdeu as cenas"
    assert SA.capitulos_do_pacote("nao-existe-esta-spec") == []


def test_os_DOIS_shorts_desta_origem_aparecem():
    """s007 (primeiro angulo) e s014 (segundo). Se cair, a ancora mudou."""
    nomes = [n for n, _ in SA.shorts_da_origem(ORIGEM)]
    assert "labtreinamento-s007" in nomes
    assert "labtreinamento-s014" in nomes


def test_mencionado_nao_quer_dizer_usado():
    """A copy do s014 cita "Copia fiel" para dizer que NAO a levou.

    Se a saida dissesse "usado", a proxima rodada descartaria um capitulo que
    esta livre — e seria um erro causado pelo meu proprio texto.
    """
    d = SA.nao_mencionados(ORIGEM)
    assert "Cópia fiel" in d["mencionados"]
    s014 = dict(SA.shorts_da_origem(ORIGEM))["labtreinamento-s014"]
    assert "NAO LEVEI" in s014 and "COPIA\nFIEL" in s014.replace(" FIEL", "\nFIEL")
    fonte = (RAIZ / "fabrica/segundo_angulo.py").read_text()
    assert "indicio, nao prova" in fonte or "indicio e nao prova" in fonte


def test_convencao_nao_seguida_vira_None_e_manda_usar_a_regra_h():
    assert SA.pacote_do_id("idInexistente") is None
    fonte = (RAIZ / "fabrica/segundo_angulo.py").read_text()
    assert "capitulos.yml" in fonte
    assert "legenda=true" in fonte


def test_o_modulo_NAO_escolhe_capitulo_nem_nomeia_familia():
    """Capitulo e conteudo que vai ao ar; familia e julgamento."""
    fonte = (RAIZ / "fabrica/segundo_angulo.py").read_text()
    assert "nao escolhe capitulo" in fonte and "nao nomeia familia" in fonte
    assert "similaridade" in fonte
