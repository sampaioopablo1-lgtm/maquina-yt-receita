"""O stdout do `registro_videos.py` e SQL PURO -- medido em 15/10 as 15:2x.

Eu rodei `... | tee -a docs/pendente/videos-a-inserir.sql` e o arquivo ficou com
TRES linhas de prosa portuguesa dentro de um .sql, porque o `main` imprimia o
relato em stdout junto do INSERT. E a assinatura e a do 729 do outro lado: la a
nota legivel grudou no base64 porque EU redirecionei stderr para dentro do
payload; aqui ela grudou no SQL porque o MODULO a punha em stdout.

O que estes testes NAO afirmam: que o arquivo parqueado ja tenha sido aplicado.
Sem `execute_sql` ele e so um arquivo, e o 726 continua em aberto.
"""
import ast
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULO = os.path.join(RAIZ, "fabrica", "registro_videos.py")
SQL = os.path.join(RAIZ, "docs", "pendente", "videos-a-inserir.sql")

NOTICE = ("PUBLICADO epomeno-epipedo-s036 shorts youtube_id=R4Ldmvcu9k8 "
          "titulo=Apothema em=2026-10-15T15:19:14Z")

PROSA_QUE_VAZOU = ["REGISTRO:", "rode o SQL por", "-> R4Ldmvcu9k8"]


def _roda(entrada):
    return subprocess.run([sys.executable, MODULO], input=entrada, text=True,
                          capture_output=True, cwd=RAIZ)


def test_stdout_e_so_insert():
    r = _roda(NOTICE)
    linhas = [l for l in r.stdout.splitlines() if l.strip()]
    assert linhas, "nenhum INSERT saiu -- o notice e real e tem youtube_id"
    for l in linhas:
        assert l.startswith("insert into videos"), l


def test_o_relato_continua_existindo_mas_em_stderr():
    r = _roda(NOTICE)
    assert "REGISTRO:" in r.stderr, "o relato nao pode simplesmente DESAPARECER"
    assert "REGISTRO:" not in r.stdout


def test_stdout_cola_num_sql_editor_sem_limpeza():
    """A propriedade de que eu dependi sem conferir."""
    r = _roda(NOTICE)
    for l in r.stdout.splitlines():
        if l.strip():
            assert l.rstrip().endswith("do nothing"), l


def test_o_arquivo_parqueado_nao_tem_prosa():
    bruto = open(SQL, encoding="utf-8").read()
    for marca in PROSA_QUE_VAZOU:
        assert marca not in bruto, f"a prosa {marca!r} voltou para o .sql"
    for l in bruto.splitlines():
        if l.strip():
            assert l.startswith("insert into videos"), l


def test_toda_linha_parqueada_tem_origem_id_e_on_conflict():
    """670: sem `origem_id` a estoque.sql nao sabe que a origem foi consumida."""
    linhas = [l for l in open(SQL, encoding="utf-8").read().splitlines() if l.strip()]
    assert len(linhas) >= 5, "o pendente so cresce enquanto o banco esta fora"
    for l in linhas:
        assert "origem_id" in l
        assert "on conflict (slug) do nothing" in l


def test_a_peca_desta_rodada_esta_parqueada():
    bruto = open(SQL, encoding="utf-8").read()
    assert "R4Ldmvcu9k8" in bruto
    assert "epomeno-epipedo-s036" in bruto


def test_o_main_NAO_imprime_relato_em_stdout_no_CODIGO():
    """Codigo, nao prosa: o docstring do modulo NOMEIA stdout para se explicar."""
    arvore = ast.parse(open(MODULO, encoding="utf-8").read())
    main = next(n for n in ast.walk(arvore)
                if isinstance(n, ast.FunctionDef) and n.name == "main")
    for no in ast.walk(main):
        if isinstance(no, ast.Call) and getattr(no.func, "id", "") == "print":
            alvo = [k.value for k in no.keywords if k.arg == "file"]
            arg0 = no.args[0] if no.args else None
            chama_relato = (isinstance(arg0, ast.Call)
                            and getattr(arg0.func, "id", "") == "relato")
            if chama_relato:
                assert alvo, "relato sem file= volta para stdout"
                assert ast.unparse(alvo[0]) == "sys.stderr"


def test_a_procedencia_do_729_continua_escrita():
    """Retratacao sem o motivo escrito volta -- e esta voltou uma vez."""
    fonte = open(MODULO, encoding="utf-8").read()
    assert "729" in fonte
    assert "726" in fonte
