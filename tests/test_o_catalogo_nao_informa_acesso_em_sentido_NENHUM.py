"""777, `alto`, medido em 15/10 as 14:1x — a QUARTA rodada seguida com o
`execute_sql` negado, e a celula que faltava na tabela do 709.

O **709** (`critico`, 12/10) dizia: *"catalogo nao e acesso"*. A evidencia dele
era UMA celula — o `list_projects` devolvia so `imobjazz-eng's Project`
**enquanto o `execute_sql` no `vevocauwtarctfwngrch` FUNCIONAVA**. Dali eu tirei a
regra certa (sondar a CAPACIDADE, nao o catalogo) com meia tabela.

**Hoje a outra celula apareceu, e ela e mais forte do que a primeira.** Medido com
tres chamadas nesta rodada:

| chamada | resultado |
|---|---|
| `execute_sql` em `vevocauwtarctfwngrch` | **negado** (`-32600`), 4 rodadas |
| `list_organizations` | **200** — uma org: `imobjazz-eng's Org` |
| `list_projects` | **200** — um projeto: `imobjazz-eng's Project` |

**O catalogo de hoje e INDISTINGUIVEL do catalogo de 12/10**, e o acesso e o
oposto. Logo:

1. **o catalogo nao informa acesso em sentido NENHUM** — nem "ha acesso" (o erro
   do 709) nem "nao ha acesso" (o erro que eu cometeria hoje se concluisse dele
   que o escopo mudou);
2. **o servidor MCP FUNCIONA** — ele responde duas chamadas com 200. Logo a
   negacao do `execute_sql` **nao e o servidor caido**, que era a hipotese barata;
3. **e eu NAO consigo atribuir a causa de dentro da sessao.** As duas leituras
   compativeis com o que eu vejo — o conector reapontado para outra org, ou uma
   permissao retirada do projeto — produzem o MESMO par de respostas. Dizer qual
   e seria comparador escolhido (efeito C).

**A consequencia pratica muda a FILA DO DONO, e e por isso que isto importa mais
que a diagnose.** A rotina diz, na pendencia 2: *"NAO peca a reconexao do conector
como primeira opcao: ela e a PIOR das tres"*. **Essa ordem pressupunha que o banco
FUNCIONAVA** e que so o REST estava em 402 — ali a reconexao devolvia o banco que
eu ja tinha e deixava o 402 de pe, logo era a pior. **Com o `execute_sql` negado a
premissa caiu:** sem ele nao ha `pg_net`, logo nao ha token, logo nao ha leitura de
duracao real, nao ha leitura de inscritos, nao ha rota da regra (h) e nao ha
registro em `videos`. A reconexao passa a ser a UNICA que devolve isso.

**O que NAO mudou:** a pendencia 3 (uma colagem de `YT_OAUTH_JSON`) segue sendo a
que liberta mais por menos trabalho dele — mas ela ja esta FEITA, e e por isso que
a publicacao continuou funcionando nestas quatro rodadas.
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]

# Medido nesta rodada, as 14:1x de 15/10.
EXECUTE_SQL_NEGADO = True
ORGS_VISTAS = ["imobjazz-eng's Org"]
PROJETOS_VISTOS = ["imobjazz-eng's Project"]
PROJETO_DA_MAQUINA = "vevocauwtarctfwngrch"
RODADAS_SEM_BANCO = 4


def test_o_projeto_da_maquina_NAO_esta_no_catalogo():
    assert PROJETO_DA_MAQUINA not in " ".join(PROJETOS_VISTOS)


def test_o_catalogo_de_hoje_e_o_MESMO_de_12_10_quando_o_acesso_FUNCIONAVA():
    """A celula que o 709 mediu: catalogo estreito E acesso OK.

    Se este fato cair, a tabela do 777 perde a perna que importa — porque e
    justamente a IGUALDADE dos dois catalogos que prova que ele nao informa nada.
    """
    catalogo_em_12_10 = ["imobjazz-eng's Project"]
    assert PROJETOS_VISTOS == catalogo_em_12_10, (
        "o catalogo mudou; releia o 777 em vez de reaproveitar a conclusao")


def test_as_DUAS_celulas_existem_e_isso_fecha_a_tabela():
    """709: catalogo estreito + acesso OK. 777: catalogo estreito + acesso NEGADO."""
    tabela = {("estreito", "ok"): "709 (12/10)",
              ("estreito", "negado"): "777 (15/10)"}
    assert len(tabela) == 2
    assert len({k[0] for k in tabela}) == 1, (
        "o catalogo e o MESMO nas duas linhas — e so por isso a conclusao vale")
    assert len({k[1] for k in tabela}) == 2


def test_o_SERVIDOR_responde__logo_a_negacao_nao_e_servidor_caido():
    assert ORGS_VISTAS and PROJETOS_VISTOS, (
        "as duas chamadas de catalogo voltaram 200 na mesma rodada em que o"
        " execute_sql foi negado")
    assert EXECUTE_SQL_NEGADO


def test_a_causa_fica_DECLARADA_como_indeterminada():
    """Duas leituras produzem o mesmo par de respostas; escolher uma e efeito C."""
    doc = pathlib.Path(__file__).read_text()
    assert "NAO consigo atribuir a causa" in doc
    assert "comparador escolhido" in doc


def test_a_FILA_do_dono_muda__e_a_premissa_da_ordem_antiga_vai_escrita():
    doc = pathlib.Path(__file__).read_text()
    assert "PIOR das tres" in doc, "a ordem antiga tem de ser citada"
    assert "pressupunha que o banco" in doc, (
        "e a PREMISSA dela tem de ir escrita, senao a mudanca parece capricho")


def test_o_que_NAO_mudou_vai_dito__a_pendencia_3_segue_feita():
    doc = pathlib.Path(__file__).read_text()
    assert "ja esta FEITA" in doc, (
        "a publicacao funcionou nas quatro rodadas; dizer que tudo caiu seria"
        " exagero e o dono tomaria decisao errada")


def test_o_pendente_de_videos_existe_e_e_a_consequencia_medida():
    """Sem `execute_sql` o segundo passo do registro (726) nao roda."""
    p = RAIZ / "docs" / "pendente" / "videos-a-inserir.sql"
    assert p.exists(), "o arquivo de pendencia sumiu — releia o 775"
    linhas = [l for l in p.read_text().splitlines() if l.strip().startswith("insert")]
    assert len(linhas) >= 3, (
        f"tres publicacoes sem linha em `videos`; achei {len(linhas)}")
    for l in linhas:
        assert "origem_id" in l, "sem origem_id a estoque.sql fica cega (670)"
        assert "on conflict (slug) do nothing" in l, "tem de poder rodar duas vezes"
