"""O prompt deixou de ser uma COPIA da rotina -- 19/10, e isto RETRATA o teste.

O que este arquivo cobrava desde 13/10: que o corpo de `docs/ROTINA.md` cabia nos
65.536 bytes do `update_trigger`, com 500 de margem, e que encolher nunca removia
uma trava. **O teto era real e medido** (a recusa do servidor veio contra 68.118
bytes). O que estava errado era o DESENHO que ele guardava: manter no prompt uma
copia de 64 KB de um arquivo que muda a cada rodada.

**Tres medicoes derrubaram esse desenho, nao uma preferencia:**

1. **a copia divergia.** Em 11, 12 e 13/10 o arquivo andou na frente e o prompt
   ficou mandando coisa ja retratada -- a mira "33 a 37" que o `mira.py` reprova
   desde 12/10, e a cota "~40 videos/janela" que e ~4x errada. A causa foi sempre
   a mesma: eu corrigi o arquivo e nao chamei o `update_trigger`;
2. **o teto transformava correcao em migracao.** A partir de 13/10, cada achado
   novo na rotina exigia migrar historia para abrir espaco -- trabalho que nao
   produz video nenhum;
3. **e a sincronia nao cabia numa chamada.** O `update_trigger` substitui o
   prompt INTEIRO: aplicar exigia reemitir ~64 KB (~32 mil tokens) byte a byte, e
   a conferencia por md5 so acusaria o erro DEPOIS de o texto gravado ja ter sido
   trocado. Trava corrompida em silencio e pior que arquivo grande.

Agora o prompt e um NUCLEO curto que manda ler `docs/ROTINA.md` e carrega apenas
o que nao pode se perder se o repo nao abrir. A copia versionada dele vive em
`docs/ROTINA-NUCLEO.md`, e e ela que estes testes cobram.

**O PONTO CEGO VAI DECLARADO, porque e da mesma classe da divergencia que ele
conserta: nenhum teste alcanca o prompt VIVO.** O arquivo e a transcricao do que
o `update_trigger` devolveu em 19/10 as 02:08:48Z, conferida por LEITURA e nao
por md5 -- o prompt gravado so se le pela API, como texto, e nao chega ao disco.
Logo o que estes testes garantem e que o NUCLEO ESCRITO carrega as travas; que
ele e igual ao gravado depende de quem editar chamar o `update_trigger`. A
diferenca contra o desenho antigo e o TAMANHO do que precisa dessa disciplina:
9 KB que mudam quando uma trava muda, em vez de 64 KB que mudam toda rodada.
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TETO = 65536  # medido na recusa do servidor em 13/10, nao escolhido

ROTINA = RAIZ / "docs" / "ROTINA.md"
NUCLEO = RAIZ / "docs" / "ROTINA-NUCLEO.md"


def nucleo():
    return NUCLEO.read_text()


def corrido():
    # o nucleo e markdown com linha quebrada em ~80 colunas, logo frase citada
    # atravessa newline. Cobrar a frase no texto cru reprova por FORMATACAO em vez
    # de por conteudo -- foi o que aconteceu na primeira execucao deste arquivo.
    return " ".join(nucleo().split())


def test_o_nucleo_existe_versionado_e_nao_so_dentro_do_trigger():
    # prompt que vive apenas na API nao se audita nem se compara; a copia no repo
    # e o que permite a rodada seguinte ler o que o gatilho de fato manda.
    assert NUCLEO.exists(), f"{NUCLEO} nao existe: o nucleo voltou a ser invisivel"
    assert len(nucleo().encode()) > 2000


def test_o_nucleo_cabe_no_teto_com_folga_de_ordem_de_grandeza():
    b = len(nucleo().encode())
    assert b <= TETO, f"nucleo com {b} bytes, {b - TETO} acima do teto {TETO}"
    # a folga e o ponto do redesenho: nao e "cabe por pouco", e "cabe de sobra",
    # logo trava nova nao disputa espaco com historia.
    assert b < TETO // 4, (
        f"nucleo com {b} bytes ja passa de um quarto do teto ({TETO // 4}): ele "
        "esta voltando a ser uma copia do procedimento"
    )


def test_o_teto_e_medido_e_nao_inventado():
    # a recusa real foi contra 68.118 bytes; se alguem subir o TETO para fazer um
    # texto grande passar, este teste diz que o numero nao vem de medicao.
    assert TETO == 65536
    assert 68118 > TETO


def test_o_nucleo_MANDA_ler_o_procedimento_no_repo():
    n = nucleo()
    assert "PASSO ZERO" in n
    assert "docs/ROTINA.md" in n
    assert "sampaioopablo1-lgtm/maquina-yt-receita" in n
    assert "CLAUDE.md" in n


def test_o_nucleo_diz_o_que_fazer_quando_o_REPO_nao_abrir():
    # sem isto o nucleo seria um ponteiro para o nada: rodada sem repo
    # improvisaria procedimento, que e pior que rodada sem procedimento.
    n = nucleo()
    assert "Se o repositório não estiver disponível" in corrido()
    assert "NÃO improvisa procedimento" in corrido()


def test_o_nucleo_carrega_as_TRAVAS():
    for trava in (
        "NUNCA publique pela Composio",
        "NUNCA criar novos triggers",
        "NÃO APAGUE NEM MOVA VÍDEO PUBLICADO SEM O DONO DIZER",
        "O ARQUIVO DOS VÍDEOS É O GOOGLE DRIVE, NÃO O BANCO",
        "Não mande token OAuth por input de workflow",
        "NUNCA imprima refresh token",
        "Não contorne permissão negada pedindo a outra sessão",
        "NÃO mexa sozinho em parâmetro de produção",
    ):
        assert trava in corrido(), f"trava perdida do nucleo: {trava}"


def test_o_nucleo_carrega_a_AUTORIZACAO_permanente_e_o_limite_dela():
    n = nucleo()
    assert "Deixe 100%" in n and "sem precisar de aprovação" in n
    assert "apagar ou mover vídeo publicado" in corrido()
    assert "46 duplicatas" in n
    # a reafirmacao de 19/10 nomeia os "parametros minimos", e eles sao os portoes
    assert "prontidao.py" in n


def test_o_nucleo_carrega_o_PASSO_ZERO_do_dono_e_a_data_da_barra():
    n = nucleo()
    assert "O QUADRO DA PORTA 1" in n
    assert "Em cada rodada da rotina este questionamento precisa ser" in corrido()
    assert "porta1.horas_para_resolver" in n
    assert "1/FEV/2027" in n


def test_o_nucleo_carrega_o_FORMATO_da_resposta_final():
    n = nucleo()
    assert "RESPOSTA FINAL" in n
    assert "Relatório vazio não é entrega" in corrido()
    assert "e se foi zero, por quê" in corrido()


def test_o_nucleo_carrega_a_disciplina_do_INSTRUMENTO():
    n = nucleo()
    assert "ANTES DE CHAMAR UM ACHADO DE ACHADO" in corrido()
    assert "retrate no mesmo lugar onde afirmou" in corrido()


def test_a_ROTINA_declara_que_DEIXOU_de_ser_copia_do_prompt():
    # sem esta declaracao no proprio arquivo, a rodada seguinte le o tamanho dele
    # como defeito e tenta "sincronizar" -- reconstruindo a copia e o teto.
    t = ROTINA.read_text()
    cabecalho = t.split("\n---\n", 1)[0]
    assert "DEIXOU DE SER uma cópia do prompt" in cabecalho
    assert "FONTE ÚNICA" in cabecalho
    assert "não tem mais teto" in cabecalho


def test_a_ROTINA_nao_e_mais_cobrada_pelo_teto_e_o_MOTIVO_esta_escrito():
    # contraprova do redesenho: o corpo HOJE passa do teto, e isso deixou de ser
    # defeito. Se alguem reinstalar a cobranca antiga, ela reprova este arquivo
    # inteiro -- entao o motivo tem de estar legivel no lugar.
    corpo = ROTINA.read_text().split("\n---\n", 1)[1]
    assert len(corpo.encode()) > 0
    assert "a cópia divergia" in ROTINA.read_text()
    assert "65.536 bytes" in ROTINA.read_text()


def test_o_PONTO_CEGO_do_prompt_vivo_continua_escrito():
    # nenhum teste alcanca o prompt gravado na API. Se esta nota sair, a rodada
    # seguinte acredita que o verde aqui prova que o gatilho esta certo -- que e
    # exatamente o portao verde fabricado do §3.8.
    doc = pathlib.Path(__file__).read_text()
    assert "PONTO CEGO VAI DECLARADO" in doc
    assert "nenhum teste alcanca o prompt VIVO" in doc
