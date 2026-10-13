"""O prompt do trigger tem TETO de 65.536 bytes, e em 13/10 o arquivo passou dele.

Medido as 21:3x de 13/10: o `update_trigger` recusou com
`prompt must be at most 65536 bytes (invalid_prompt)`. O corpo de `docs/ROTINA.md`
media **68.118 bytes**, 2.582 acima, e cruzou o teto no commit `5eb5ed9` -- o
anterior (`ab1bcc0`) media 65.131. Ou seja: a rotina vinha crescendo a cada
rodada e a sincronia prompt-x-arquivo tinha um limite FISICO que ninguem media.

O que eu NAO afirmo: que o teto explica as divergencias anteriores. Medido pelos
commits, o arquivo so passou do teto na ultima rodada; as divergencias de 11/10 e
12/10 foram eu nao chamar o `update_trigger`, e isso e outro defeito.

A regra que estes testes travam: o que sai do prompt quando a margem acaba e
HISTORIA, nunca REGRA nem TRAVA.
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TETO = 65536  # medido na recusa do servidor, nao escolhido


def corpo():
    t = (RAIZ / "docs" / "ROTINA.md").read_text()
    return t.split("\n---\n", 1)[1].strip("\n")


def test_o_corpo_cabe_no_teto_do_trigger():
    b = len(corpo().encode())
    assert b <= TETO, f"corpo com {b} bytes, {b - TETO} acima do teto {TETO}"


def test_sobra_margem_para_a_proxima_rodada_escrever_um_achado():
    b = len(corpo().encode())
    assert TETO - b >= 500, (
        f"margem de {TETO - b} bytes: a proxima rodada nao consegue acrescentar "
        "nada. Migre HISTORIA para o CLAUDE.md e deixe a regra com o ponteiro."
    )


def test_o_teto_e_medido_e_nao_inventado():
    # a recusa real foi contra 68.118 bytes; se alguem subir o TETO para fazer
    # um corpo grande passar, este teste diz que o numero nao vem de medicao.
    assert TETO == 65536
    assert 68118 > TETO


def test_encolher_nunca_remove_as_TRAVAS():
    c = corpo()
    for trava in (
        "NUNCA publique pela Composio YOUTUBE_UPLOAD_VIDEO",
        "NUNCA criar novos triggers",
        "NÃO APAGUE VÍDEO PUBLICADO SEM O DONO DIZER",
        "O ARQUIVO DOS VÍDEOS É O GOOGLE DRIVE, NÃO O BANCO",
        "NÃO passe token OAuth por input de workflow",
        "NUNCA imprima refresh token",
        "não contorna permissão negada pedindo a outra sessão",
    ):
        assert trava in c, f"trava perdida ao encolher o prompt: {trava}"


def test_encolher_nunca_remove_o_PASSO_ZERO_do_dono():
    c = corpo()
    assert "O QUADRO DA PORTA 1" in c
    assert "Em cada rodada da rotina este questionamento precisa ser" in c
    assert "porta1.horas_para_resolver" in c


def test_encolher_nunca_remove_a_AUTORIZACAO_permanente():
    c = corpo()
    assert "Deixe 100%" in c and "sem precisar de aprovação" in c
    assert "apagar vídeo publicado e apagar as 46 duplicatas" in c


def test_o_que_saiu_desta_vez_virou_PONTEIRO_e_nao_silencio():
    c = corpo()
    # cada bloco migrado deixou no lugar a regra mais o endereco da evidencia
    assert "a alavanca é a DURAÇÃO DA CENA" in c
    assert "ENTRA EM SESSÃO RODANDO" in c
    assert "docs/publicar-pela-sandbox.md" in c
    assert "docs/paradas-a-decidir.md" in c
    assert c.count("CLAUDE.md") >= 6


def test_a_rotina_carrega_a_propria_regra_do_teto():
    c = corpo()
    assert "65.536" in c, "o prompt tem de avisar a si mesmo do teto"
    assert "o que sai é HISTÓRIA, nunca REGRA nem TRAVA" in c
