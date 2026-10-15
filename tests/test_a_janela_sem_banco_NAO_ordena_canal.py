"""775, `alto`, medido em 15/10 as 11:1x — a PRIMEIRA rodada desta sessao sem
`execute_sql`, e o que a substituicao do contador ensinou.

O contador que escolhe o canal le `videos.publicado_em` (762/771), logo morre com
o banco. A fonte substituta existe e e datada — o `git log` do
`fabrica/corpus_publicados.json` — e ela trouxe TRES defeitos, cada um descoberto
ao conferir contra o numero que o banco dera uma hora antes (**24** pecas em 24 h):

1. **contar linhas `+` INFLA por ~2x** (46 contra 24): o corpus e regravado com
   `indent=2`, a lista se REORDENA, e 22 dos 24 titulos reaparecem como linha
   adicionada em commits posteriores;
2. **o commit ATRASA contra a publicacao**, e o atraso cai justamente no canal que
   acabou de produzir — o que mandaria produzir nele de novo, o oposto do 762;
3. **TITULO NAO E CHAVE DE PUBLICACAO**, e este e estrutural: o conserto do (1) —
   contar DISTINTOS — faz duas publicacoes de mesmo titulo curto colapsarem em
   uma. **E o 773:** `labtreinamento-s051` e `-s038` compartilham
   *"Conclusao nao e situacao"*, e a janela perde uma peca do labtreinamento.
   Os dois consertos se contradizem, e o corpus e **lista nua** — nao existe
   terceira forma de contar com esta fonte.

**Logo o modulo RECUSA ordenar canal**, sempre, e isso e medicao e nao zelo: o
erro e de DUAS pecas e uma parte dele nao esta limitada por nada que eu tenha
medido. Quem decide sem o banco e a **ULTIMA publicacao por canal**, lida dos
`created_at` dos runs do `retomar.yml` — o desempate MEDIDO do 771, que nao
depende de banco, nem de commit, nem de titulo.
"""
import datetime
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import janela_sem_banco as jsb  # noqa: E402

# Numeros REAIS de 15/10 as 11:1x.
BANCO_AS_10_07 = {"labtreinamento": 7, "epomeno-epipedo": 9, "kolejny-poziom": 8}
MODULO_AS_11_1x = {"labtreinamento": 5, "epomeno-epipedo": 9, "kolejny-poziom": 8}
COLISAO_DO_773 = "Conclusão não é situação"


def test_ordena_devolve_SEMPRE_None__a_recusa_e_o_comportamento():
    for jan in (MODULO_AS_11_1x, BANCO_AS_10_07,
                {"labtreinamento": 0, "epomeno-epipedo": 99, "kolejny-poziom": 98}):
        baixo, emp = jsb.ordena(jan)
        assert baixo is None, (
            "este modulo NAO ordena canal — nem com margem larga, porque o erro"
            " dele tem parte ESTRUTURAL (defeito 3)")
        assert len(emp) == 2


def test_os_dois_mais_baixos_saem_NOMEADOS_para_o_desempate():
    _b, emp = jsb.ordena(MODULO_AS_11_1x)
    assert emp == ["kolejny-poziom", "labtreinamento"], emp


def test_o_erro_contra_o_banco_esta_declarado_e_e_de_DUAS_pecas():
    erro = BANCO_AS_10_07["labtreinamento"] - MODULO_AS_11_1x["labtreinamento"]
    assert erro == jsb.ERRO_MEDIDO_EM_PECAS == 2, erro


def test_a_inflacao_de_contar_LINHAS_esta_travada_com_os_numeros_reais():
    i = jsb.INFLACAO_MEDIDA
    assert (i["linhas"], i["distintos"], i["repetidos"]) == (46, 24, 22)
    assert i["linhas"] > 1.8 * i["distintos"], (
        "se a inflacao encolher, a lista parou de se reordenar e isto deve ser"
        " relido em vez de reaproveitado")


def test_a_COLISAO_do_773_existe_de_verdade_nas_specs():
    """Sem esta colisao o defeito 3 seria hipotese, e nao medicao."""
    import collections
    import json
    import re
    por_titulo = collections.defaultdict(list)
    for f in sorted((RAIZ / "fabrica" / "specs").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        m = re.search(r"^##\s*TITULO SHORT\s*$\n+(.+)$", d.get("copy", "") or "", re.M)
        if m:
            por_titulo[m.group(1).strip()].append(f.name)
    colisoes = {t: v for t, v in por_titulo.items() if len(v) > 1}
    assert COLISAO_DO_773 in colisoes, (
        "a colisao do 773 saiu das specs — o defeito 3 perdeu a ancora e esta"
        " nota tem de ser relida (nao basta apagar o caso)")
    assert sorted(colisoes[COLISAO_DO_773]) == [
        "labtreinamento-s038.json", "labtreinamento-s051.json"]
    assert len(colisoes) == 1, (
        f"a frota tinha UMA colisao de titulo curto; agora tem {len(colisoes)}:"
        f" {sorted(colisoes)}")


def test_a_contagem_e_por_titulo_DISTINTO_e_pelo_commit_MAIS_VELHO():
    """Contraprova sem tocar o git: o mesmo titulo em dois commits conta UMA vez,
    e o instante que vale e o mais ANTIGO."""
    mapa = {"A": "labtreinamento", "B": "kolejny-poziom"}
    primeiro = {"A": "2026-10-15T09:00:00+00:00", "B": "2026-10-15T07:00:00+00:00"}
    agora = datetime.datetime(2026, 10, 15, 11, 10, tzinfo=datetime.timezone.utc)
    jan, ult = jsb.contagem(24, agora, mapa=mapa, primeiro=primeiro)
    assert jan == {"labtreinamento": 1, "kolejny-poziom": 1}
    assert ult["kolejny-poziom"].hour == 7


def test_titulo_FORA_da_janela_nao_entra():
    mapa = {"A": "labtreinamento"}
    primeiro = {"A": "2026-10-13T09:00:00+00:00"}
    agora = datetime.datetime(2026, 10, 15, 11, 10, tzinfo=datetime.timezone.utc)
    jan, _u = jsb.contagem(24, agora, mapa=mapa, primeiro=primeiro)
    assert jan == {}


def test_o_relato_DIZ_que_nao_ordena_e_PARA_ONDE_IR():
    mapa = {"A": "labtreinamento", "B": "kolejny-poziom"}
    primeiro = {"A": "2026-10-15T09:00:00+00:00", "B": "2026-10-15T07:00:00+00:00"}
    agora = datetime.datetime(2026, 10, 15, 11, 10, tzinfo=datetime.timezone.utc)
    t = jsb.relato(24, agora, mapa=mapa, primeiro=primeiro)
    assert "NAO ORDENA" in t
    assert "PISO" in t, "ele tem de se declarar piso, nao contador"
    assert "retomar.yml" in t, "tem de dizer PARA ONDE IR, nao so calar (761)"
    assert "773" in t, "a procedencia do defeito estrutural vai no relato"


def test_o_modulo_NAO_CHAMA_nada_de_banco():
    """Confere CODIGO, nao prosa — a primeira versao deste teste reprovou porque
    o docstring do modulo NOMEIA o `execute_sql` para explicar por que ele
    existe. Mencionar um bloqueio e o contrario de depender dele."""
    import ast
    fonte = (RAIZ / "fabrica" / "janela_sem_banco.py").read_text()
    arvore = ast.parse(fonte)
    # o docstring de cada no sai fora da conferencia; o resto do codigo entra
    for no in ast.walk(arvore):
        if isinstance(no, (ast.Module, ast.FunctionDef, ast.ClassDef)):
            no.body = [x for x in no.body
                       if not (isinstance(x, ast.Expr)
                               and isinstance(x.value, ast.Constant)
                               and isinstance(x.value.value, str))]
    codigo = ast.unparse(arvore).lower()
    for proibido in ("execute_sql", "supabase", "psycopg", "pg_net", "requests",
                     "httpx", "urllib"):
        assert proibido not in codigo, proibido
    # e o que ele de fato usa e git e o disco
    assert "subprocess" in codigo and "git" in codigo
