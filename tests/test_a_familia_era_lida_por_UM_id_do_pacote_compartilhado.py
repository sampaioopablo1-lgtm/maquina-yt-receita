"""O `segundo_angulo` ja unia os CAPITULOS; a FAMILIA seguia por UM id.

**Medido em 23/10 as 12:5x, escolhendo a pauta, e o custo foi desta rodada.**
O `segundo_angulo.texto_dos_livres` une as declaracoes de capitulo de todos os
ids que resolvem para o MESMO pacote desde 23/10 as 06:4x; o
`irmaos_da_origem.irmaos(origem)` seguia devolvendo os irmaos de UM id. Logo as
duas metades da MESMA pergunta discordavam, e a metade atrasada era justamente
a que sustenta a regra (f): a comparacao de FAMILIA.

**A minha primeira candidata de familia no `kolejny-poziom-004` era o warunek
dos cinco anos calendario, que e EXATAMENTE a familia do `kolejny-poziom-s034`
— irmao do OUTRO id.** Eu so a vi porque li o outro id A MAO.

**A forma dos testes:** a ancora e DERIVADA do disco (nomear um id seria
identidade onde ha propriedade — 743/753/761, e os ids mudam), os DOIS lados tem
de existir, a contraprova vai no outro sentido (pacote nao compartilhado le
IGUAL, senao unir sempre passaria), e a medida e reconferida como PROPRIEDADE e
nao como contagem absoluta, porque a populacao cresce uma spec por rodada
(22/10, 14:4x).
"""
import ast
import inspect
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO  # noqa: E402
import segundo_angulo as SA  # noqa: E402

PISO_DE_PACOTES = 20


def _mapa():
    m = SA._mapa_id_pacote()
    if len(m) < PISO_DE_PACOTES:
        pytest.fail(
            "o disco resolveu %d id(s) para pacote, abaixo do piso de %d:"
            " com tao pouco este arquivo passa por VACUIDADE em vez de medir"
            % (len(m), PISO_DE_PACOTES))
    return m


def _por_pacote(m):
    d = {}
    for yid, pac in m.items():
        d.setdefault(pac, []).append(yid)
    return d


def _compartilhados(m=None):
    return {p: v for p, v in _por_pacote(m or _mapa()).items() if len(v) > 1}


def _fonte(fn):
    import textwrap
    return textwrap.dedent(inspect.getsource(fn))


def _corpo_sem_docstring(fn):
    t = ast.parse(_fonte(fn))
    f = t.body[0]
    corpo = f.body
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return ast.Module(body=corpo, type_ignores=[])


def test_os_DOIS_lados_existem_no_disco():
    """Falha se TODOS ou se NENHUM pacote for compartilhado.

    Nos dois casos a nota tem de ser RELIDA em vez de o numero ser movido: sem
    compartilhado a uniao nao tem objeto, e sem pacote de id unico a
    contraprova do outro sentido nao mede nada.
    """
    m = _mapa()
    pp = _por_pacote(m)
    comp = _compartilhados(m)
    assert comp, (
        "NENHUM pacote do disco e compartilhado por dois ids — a uniao perde o"
        " objeto e esta nota tem de ser RELIDA, nao o numero movido")
    assert len(comp) < len(pp), (
        "TODOS os pacotes passaram a ser compartilhados — a contraprova do"
        " outro sentido deixou de existir e esta nota tem de ser RELIDA")


def test_o_compartilhado_e_MINORIA_reconferido_no_disco():
    """A medida vai como PROPORCAO, nao como contagem.

    Contagem absoluta sobre populacao que cresce uma spec por rodada e
    identidade disfarcada de medida (a licao de 22/10 as 14:4x).
    """
    m = _mapa()
    pp = _por_pacote(m)
    frac = len(_compartilhados(m)) / len(pp)
    assert frac < 0.5, (
        "pacote compartilhado deixou de ser minoria (%.2f): a nota diz que ele"
        " e a excecao, e com a maioria compartilhada a leitura por id passa a"
        " ser o caso raro — releia" % frac)


def _ancora_compartilhada():
    comp = _compartilhados()
    for pac, ids in sorted(comp.items()):
        for y in sorted(ids):
            u = IO.irmaos_do_pacote(y)
            if u["subconta"]:
                return y, u
    pytest.fail(
        "nenhum id do disco SUBCONTA irmaos — perdi a ancora: ou os pacotes"
        " compartilhados ficaram sem irmao, ou os irmaos se distribuiram"
        " igualmente. Em qualquer dos casos releia a nota")


def test_a_UNIAO_e_estritamente_maior_que_a_leitura_por_id():
    """Por PROPRIEDADE, nao pelo id: os ids do disco mudam a cada rodada."""
    yid, u = _ancora_compartilhada()
    assert u["compartilhado"] is True
    assert u["n"] > u["so_do_id"], (
        "a uniao de %s nao e maior que a leitura por id (%d contra %d) — o"
        " defeito que este arquivo mede deixou de ocorrer"
        % (yid, u["n"], u["so_do_id"]))
    crua = {i["pacote"] for i in IO.irmaos(yid)}
    unida = {i["pacote"] for i in u["irmaos"]}
    assert crua < unida, (
        "a leitura crua de %s nao e subconjunto ESTRITO da uniao" % yid)


def test_REPRODUZ_o_defeito_a_leitura_por_id_perde_irmao():
    """Sem isto, *"eu lia por um id so"* seria afirmacao minha e nao medida."""
    yid, u = _ancora_compartilhada()
    so_do_outro = [i["pacote"] for i in u["irmaos"]
                   if yid not in i["_de_ids"]]
    assert so_do_outro, (
        "nenhum irmao vem SO pelo outro id — o defeito nao se reproduz e esta"
        " nota tem de ser RELIDA")
    for i in u["irmaos"]:
        assert i["_de_ids"], "irmao sem `_de_ids`: a procedencia se perdeu"


def test_contraprova_pacote_NAO_compartilhado_le_IGUAL():
    """Senao unir sempre passaria, qualquer que fosse o conjunto."""
    m = _mapa()
    comp = _compartilhados(m)
    sozinhos = [v[0] for p, v in sorted(_por_pacote(m).items())
                if p not in comp]
    assert sozinhos, "nenhum pacote de id unico no disco: contraprova vazia"
    conferidos = 0
    for yid in sozinhos:
        u = IO.irmaos_do_pacote(yid)
        if not u["irmaos"]:
            continue
        conferidos += 1
        assert u["compartilhado"] is False
        assert u["subconta"] is False
        assert u["n"] == u["so_do_id"] == len(IO.irmaos(yid)), (
            "a uniao mudou a resposta em %s, que nao e compartilhado" % yid)
        if conferidos >= 5:
            break
    assert conferidos, (
        "nenhum pacote de id unico tem irmao: a contraprova nao mede nada")


def test_a_uniao_e_por_PACOTE_de_irmao_e_nao_repete():
    yid, u = _ancora_compartilhada()
    nomes = [i["pacote"] for i in u["irmaos"]]
    assert len(nomes) == len(set(nomes)), (
        "a uniao repetiu irmao: ela e por PACOTE, porque o mesmo short declara"
        " UM `longo_existente` so")
    assert nomes == sorted(nomes), "a uniao tem de sair ordenada e estavel"


def test_origem_IRRESOLVIVEL_nao_inventa_uniao(tmp_path):
    """Regra (h): origem sem spec local segue respondendo por si.

    Parque PROPRIO, porque ancorar numa origem viva seria identidade onde ha
    propriedade — e consumir pauta e o trabalho (18/10, 09:2x).
    """
    import json
    d = tmp_path / "specs"
    d.mkdir()
    (d / "canalz-s001.json").write_text(json.dumps({
        "pacote": "canalz-s001", "slug": "canalz-s001", "longo": [],
        "longo_existente": "IDSEMPACOTE", "short": [], "copy": "# x\n",
    }), encoding="utf-8")
    u = IO.irmaos_do_pacote("IDSEMPACOTE", dir_specs=str(d))
    assert u["pacote"] is None
    assert u["ids"] == ["IDSEMPACOTE"]
    assert u["compartilhado"] is False
    assert u["subconta"] is False
    assert [i["pacote"] for i in u["irmaos"]] == ["canalz-s001"]


def test_a_resolucao_e_DELEGADA_ao_segundo_angulo_por_AST():
    corpo = _corpo_sem_docstring(IO.irmaos_do_pacote)
    chamadas = {ast.unparse(n.func) for n in ast.walk(corpo)
                if isinstance(n, ast.Call)}
    assert "SA.pacote_do_id" in chamadas, (
        "a resolucao id -> pacote tem de ser DELEGADA: refaze-la aqui criaria o"
        " segundo dono da convencao de nome")
    assert "SA._ids_do_pacote" in chamadas, (
        "os ids do pacote tem de sair do dono do mapa, que tem MEMORIA desde"
        " 23/10 as 06:4x")
    proibidos = {"glob.glob", "os.listdir", "open", "json.load"}
    assert not (chamadas & proibidos), (
        "o corpo varre o disco por conta propria (%s): seria o segundo leitor"
        % sorted(chamadas & proibidos))


def test_a_frase_tem_UM_dono_e_o_relato_a_CHAMA():
    fonte = inspect.getsource(IO)
    marca = "PACOTE COMPARTILHADO por"
    donos = [fn for fn in ("_linha_do_pacote_compartilhado", "relato",
                           "irmaos_do_pacote")
             if marca in _fonte(getattr(IO, fn))]
    assert donos == ["_linha_do_pacote_compartilhado"], (
        "a frase do pacote compartilhado tem mais de um dono: %s" % donos)
    corpo = _corpo_sem_docstring(IO.relato)
    chamadas = {ast.unparse(n.func) for n in ast.walk(corpo)
                if isinstance(n, ast.Call)}
    assert "_linha_do_pacote_compartilhado" in chamadas, (
        "o `relato` nao chama a linha — import sem chamada e a classe dos"
        " layouts mortos")
    assert "irmaos_do_pacote" in chamadas, (
        "o `relato` voltou a ler por UM id")
    assert fonte.count(marca) == 1


def test_a_frase_sai_nos_DOIS_ramos_com_textos_DIVERGENTES():
    """Frase igual para estado diferente nao avisa nada."""
    yid, u = _ancora_compartilhada()
    sozinhos = [v[0] for p, v in sorted(_por_pacote(_mapa()).items())
                if len(v) == 1]
    outro = IO.irmaos_do_pacote(sozinhos[0])
    a = "\n".join(IO._linha_do_pacote_compartilhado(u))
    b = "\n".join(IO._linha_do_pacote_compartilhado(outro))
    assert a and b and a != b
    assert "COMPARTILHADO por" in a
    assert "NAO COMPARTILHADO" in b
    assert "UNIAO" in a
    assert "UNIAO" not in b, (
        "o ramo do nao-compartilhado nao pode falar de uniao: ali nao ha o que"
        " unir")


def test_o_relato_IMPRIME_a_linha_e_marca_o_irmao_do_outro_id():
    yid, u = _ancora_compartilhada()
    t = IO.relato(yid)
    assert "PACOTE COMPARTILHADO por" in t
    so_do_outro = [i["pacote"] for i in u["irmaos"]
                   if yid not in i["_de_ids"]]
    for pac in so_do_outro:
        assert pac in t, (
            "o irmao %s, que so vem pelo outro id, nao aparece no relato" % pac)
    assert "<< pelo id" in t, (
        "o relato nao MARCA de qual id vem o irmao: NOMEAR e o que distingue"
        " isto de filtrar")


def test_as_DUAS_metades_olham_o_MESMO_conjunto_de_ids():
    """A contagem de CAPITULOS e a lista de FAMILIAS tem de unir os mesmos ids.

    Era a divergencia entre as duas que produziu o defeito.
    """
    yid, u = _ancora_compartilhada()
    pac = SA.pacote_do_id(yid)
    do_sa = sorted(SA._ids_do_pacote(pac))
    assert sorted(u["ids"]) == do_sa, (
        "a uniao da FAMILIA (%s) nao olha os mesmos ids que a dos CAPITULOS"
        " (%s)" % (sorted(u["ids"]), do_sa))


def test_o_motivo_continua_escrito_no_modulo():
    fonte = inspect.getsource(IO.irmaos_do_pacote)
    for pedaco in ("06:4x", "s034", "item 3 da §10", "DELEGADA"):
        assert pedaco in fonte, (
            "o motivo saiu do modulo (%r): conserto sem motivo escrito volta"
            " calado" % pedaco)


def test_a_uniao_e_SIMETRICA_em_todo_id_do_pacote():
    """Ler por qualquer id do pacote tem de devolver a MESMA uniao.

    **Este teste nasceu de uma contraprova que NAO reprovou:** eu fatiei a
    lista de ids no primeiro (`[:1]`) e os treze testes passaram, porque a
    ancora DERIVADA achou o outro id, para o qual a uniao seguia completa. Uniao
    quebrada pela metade e indistinguivel de uniao certa quando se olha um lado
    — e e a familia da fatia do proxy (19/10, 19:2x) dentro do conserto da
    uniao.
    """
    comp = _compartilhados()
    assert comp, "nenhum pacote compartilhado: simetria sem objeto"
    conferidos = 0
    for pac, ids in sorted(comp.items()):
        vistos = {}
        for y in sorted(ids):
            u = IO.irmaos_do_pacote(y)
            assert u["pacote"] == pac
            assert sorted(u["ids"]) == sorted(ids), (
                "lido por %s, o pacote %s devolveu os ids %s em vez de %s"
                % (y, pac, sorted(u["ids"]), sorted(ids)))
            vistos[y] = tuple(i["pacote"] for i in u["irmaos"])
        assert len(set(vistos.values())) == 1, (
            "o pacote %s devolve unioes DIFERENTES conforme o id por que se le:"
            " %s" % (pac, vistos))
        conferidos += 1
    assert conferidos, "nenhum pacote compartilhado conferido"
