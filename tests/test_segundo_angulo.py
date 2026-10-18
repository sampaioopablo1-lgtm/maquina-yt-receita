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


# ---------------------------------------------------------------------------
# O falso positivo do SLUG DO CANAL — medido na primeira vez que eu usei o
# modulo para escolher, uma rodada depois de escreve-lo
# ---------------------------------------------------------------------------
FALSOS = ("Xgt32iH8Ft8", "SP7Vz8qHdRY", "MjI4ZGJAhIo")


def test_o_slug_do_canal_NAO_e_candidato_a_pacote():
    """Era a causa de tres falsos positivos de uma vez (12/10 12:1x).

    As tres origens resolviam para a spec `kolejny-poziom`, que e o SLUG do canal
    e tem dez cenas de longo. O vocabulario passou a excluir slug de canal.
    """
    vocab = SA.nomes_de_spec()
    slugs = SA.slugs_de_canal()
    assert slugs, "nenhuma spec declara slug — a ancora deste teste mudou"
    assert "kolejny-poziom" in slugs
    assert not (set(vocab) & slugs), "slug de canal voltou ao vocabulario"


def test_nenhuma_das_TRES_resolve_para_o_SLUG_nem_para_pacote_sem_capitulo():
    """RETRATACAO DE 18/10 as 03:2x, e ela e de um teste MEU.

    A versao anterior cobrava `pacote_do_id(yid) is None` nas tres, e reprovou
    nesta rodada porque o `SP7Vz8qHdRY` passou a resolver para
    `kolejny-poziom-011`. **Conferido: a resolucao esta CERTA** — aquele pacote
    tem 77 cenas de longo, e foi dele que saiu o `kolejny-poziom-s057`.

    O que mudou foi a CONVENCAO ter sido seguida: o `pacote_do_id` resolve pela
    copy do short que declara a origem, e a copy do `s057` NOMEIA o pacote na
    secao FONTES. O docstring da propria funcao sempre disse isso — *"devolve
    None quando a convencao nao foi seguida"* — logo `None` era um retrato do
    estado, nao uma propriedade.

    A propriedade do falso positivo de 12/10 e OUTRA, e esta e cobrada aqui: o
    que estava errado era resolver para o SLUG DO CANAL (`kolejny-poziom`, dez
    cenas). Mesma classe do 743/753/761: eu travei identidade onde havia
    propriedade.
    """
    slugs = SA.slugs_de_canal()
    for yid in FALSOS:
        r = SA.pacote_do_id(yid)
        if r is None:
            continue
        assert r not in slugs, f"{yid} resolveu para o SLUG do canal: {r}"
        caps = SA.capitulos_do_pacote(r)
        assert len(caps) >= 20, (
            f"{yid} resolveu para {r}, que tem {len(caps)} cenas de longo — "
            "o limiar observado do 12/10 e 20, e dez era o falso positivo")


def test_e_o_SP7Vz8qHdRY_resolve_porque_a_convencao_foi_SEGUIDA():
    """Ancora a queda: sem isto a retratacao acima nao tem evidencia."""
    r = SA.pacote_do_id("SP7Vz8qHdRY")
    assert r == "kolejny-poziom-011"
    assert len(SA.capitulos_do_pacote(r)) == 77
    copy = (RAIZ / "fabrica/specs/kolejny-poziom-s057.json").read_text()
    assert "kolejny-poziom-011" in copy, (
        "a copy do s057 e que nomeia o pacote — e o que faz a convencao valer")


def test_as_outras_DUAS_seguem_sem_convencao():
    """Contraprova no outro sentido: a funcao nao passou a resolver tudo."""
    assert SA.pacote_do_id("Xgt32iH8Ft8") is None
    assert SA.pacote_do_id("MjI4ZGJAhIo") is None


def test_a_VERDADE_CONHECIDA_do_Xgt32iH8Ft8_e_que_nao_ha_spec_local():
    """Escrito por mim em 11/10 no docstring do `kolejny-poziom-s017`.

    Nao e opiniao: o proprio builder diz que o pacote e `kp-plan-9233-20260811`,
    anterior a convencao de nome, e que NAO tem spec em `fabrica/specs/`.
    """
    b = (RAIZ / "fabrica/specs/kolejny-poziom-s017.build.py").read_text()
    assert "Xgt32iH8Ft8" in b
    assert "kp-plan-9233-20260811" in b
    assert "NAO tem spec" in b
    assert not (RAIZ / "fabrica/specs/kp-plan-9233-20260811.json").exists()


def test_nome_NAO_casa_como_prefixo_de_identificador_maior():
    """Sem fronteira, `kolejny-poziom` casava dentro de `kolejny-poziom-s017`."""
    assert SA._casa_inteiro("abc-01", "veja abc-01, pronto")
    assert SA._casa_inteiro("abc-01", "(abc-01)")
    assert not SA._casa_inteiro("abc-01", "veja abc-010 aqui")
    assert not SA._casa_inteiro("abc-01", "xabc-01")


def test_pacote_com_poucas_cenas_vira_SUSPEITO_em_vez_de_passar_calado():
    """O limiar e OBSERVADO: os longos da frota medem 56 a 90 capitulos."""
    assert SA.MIN_CAPITULOS_PLAUSIVEL == 20
    fonte = (RAIZ / "fabrica/segundo_angulo.py").read_text()
    assert "56 a 90" in fonte, "a procedencia do limiar tem de ficar escrita"
    assert "OBSERVADO" in fonte
    d = SA.nao_mencionados(ORIGEM)
    assert d["suspeito"] is False and d["n_capitulos"] >= 56


def test_as_origens_boas_continuam_resolvendo_depois_do_conserto():
    """Conserto que derruba os acertos nao e conserto."""
    assert SA.pacote_do_id("6BeNHqT2okA") == "labtreinamento-010"
    assert SA.pacote_do_id("kDkagIf2isA") == "kolejny-poziom-010"
