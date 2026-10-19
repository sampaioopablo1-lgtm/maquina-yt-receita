"""A regra 600 bloqueia uma CLASSE de longo, e eu a apliquei a todas.

RETRATACAO DE 19/10/2026, provocada por uma captura de tela do dono (a aba
*Videos* do `labtreinamento` no Studio). Eu respondi a ele que "nao consigo fazer
longo novo hoje" porque longo carrega numero sobre o mundo e numero exige duas
fontes institucionais, que estao em 403 no proxy. **A frase vale para longo que
carrega numero que MUDA — nao para longo de PROCEDIMENTO.**

Este arquivo trava as tres propriedades que sustentam a retratacao, para que ela
nao volte a virar "a maquina nao faz longo":

  1. a maquina JA publicou longo de ~8 min: o `labtreinamento-013` e o
     "Vale-Transporte: 6% de Qual Salario?" que esta no ar desde 7/out;
  2. o longo da REFERENCIA (`FtCtIJPsc_Q`, o PROCV de 14/out) **nao e nosso** —
     ele nao e spec de longo nenhuma do disco, e aparece so como ORIGEM de
     shorts. Era a peca do dono o tempo todo, e eu media a distancia ate ela sem
     dizer de quem ela era;
  3. e existe longo nosso SEM numero do mundo, logo a trava de fonte nao se
     aplica a ele.
"""
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SPECS = RAIZ / "fabrica" / "specs"
CLAUDE = (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")
REFERENCIA = "FtCtIJPsc_Q"


def _longos():
    """Specs com cenas de longo — a definicao de 'a maquina faz longo'."""
    fora = {}
    for f in sorted(SPECS.glob("labtreinamento-0*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("longo"):
            fora[f.stem] = d
    return fora


def test_a_maquina_JA_publicou_longo_de_oito_minutos():
    longos = _longos()
    assert len(longos) >= 10, f"a varredura achou so {len(longos)} longos"
    d = longos["labtreinamento-013"]
    assert "Vale-Transporte" in d["copy"], d["copy"][:80]
    # ~8 min nao se mede por cena solta, mas o porte sim: dezenas de cenas
    assert len(d["longo"]) >= 50, len(d["longo"])


def test_a_REFERENCIA_de_oito_minutos_NAO_e_uma_spec_nossa():
    """Se ela fosse nossa, a distancia medida em 16/10 seria contra nos mesmos."""
    for nome, d in _longos().items():
        assert REFERENCIA not in json.dumps(d), (
            f"{nome} declara a referencia como peca de longo — a nota de 19/10 "
            "dizia que ela e do dono"
        )


def test_a_referencia_aparece_so_como_ORIGEM_de_short():
    """E e isso que a torna referencia: ela entra na pauta, nao na producao."""
    usam = [f.stem for f in SPECS.glob("labtreinamento-s*.json")
            if REFERENCIA in f.read_text(encoding="utf-8")]
    assert len(usam) >= 5, usam
    assert all(s.startswith("labtreinamento-s") for s in usam), usam


def test_existe_longo_nosso_SEM_numero_do_mundo():
    """A contraprova: se todo longo nosso carregasse aliquota, a trava valeria.

    Falha se a varredura ficar vazia — regex que deixa de casar faria o assert
    passar calado.
    """
    MUNDO = ("por cento", "%", "alíquota", "aliquota", "salário mínimo",
             "salario minimo", "R$")
    sem = [n for n, d in _longos().items()
           if not any(m in d["copy"] for m in MUNDO)]
    com = [n for n, d in _longos().items()
           if any(m in d["copy"] for m in MUNDO)]
    assert com, "nenhum longo carrega numero do mundo — a varredura nao mede nada"
    assert sem, (
        "TODO longo nosso carrega numero do mundo; se isso for verdade, a "
        "retratacao de 19/10 cai e a regra 600 volta a valer para o formato"
    )


def test_a_RETRATACAO_continua_escrita_e_com_os_dois_lados():
    """Retratacao sem o motivo escrito volta calada."""
    assert "a trava de fonte é por **TIPO DE CONTEÚDO**, não por formato" in CLAUDE
    # e os dois lados vao nomeados, senao ela vira licenca para inventar numero
    assert "número do mundo que MUDA" in CLAUDE
    assert "não autoriza" in CLAUDE.lower() or "NÃO autoriza" in CLAUDE
    assert "regra (g)" in CLAUDE


def test_o_video_POLONES_no_canal_pt_BR_fica_registrado():
    """Achado da tela do dono, e ele confirma por fora o que a medicao dizia."""
    assert "QiaGg03WSR0" in CLAUDE
    assert "79 views" in CLAUDE
    assert "exige o dono" in CLAUDE, "a trava de nao mexer em peca publicada saiu"
