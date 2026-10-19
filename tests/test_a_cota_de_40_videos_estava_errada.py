"""A cota de "40 videos por janela" estava errada por um fator de ~4.

Medido em 18/10/2026 as 23:3x, lendo o guia `06_YOUTUBE.md` do
`pipeline_canal_dark_v2.0.zip` que o dono trouxe. **Mas a conferencia NAO depende
da fonte dele**, e e por isso que este arquivo pode existir: a contradicao era
entre dois documentos NOSSOS.

  * `docs/ROTINA.md` §4: "Short solto ... ~1.600 de cota contra ~2.100 do pacote";
  * `fabrica/orquestra.py`, antes do conserto: "o `captions.insert` e ~400 das
    ~500 unidades de um pacote, e o teto medido e 40 videos por janela";
  * `docs/ROTINA.md` §8: "COTA ~40 videos/janela (619)".

Um pacote (longo + short + legenda) nao pode custar ~500 unidades se um short
SOLTO custa 1.600. A aritmetica publicada da API confirma a §4: `videos.insert`
custa 1.600, `captions.insert` custa 400, cota padrao 10.000/dia por projeto.
Logo o teto e 10.000/1.600 = SEIS envios de video por dia por projeto.

O que este arquivo trava NAO e o numero 6 — e a PROPRIEDADE que o sustenta, para
que ela nao seja movida por conveniencia numa rodada futura:

  1. o custo do short solto declarado na rotina bate com `videos.insert`;
  2. o pacote custa MAIS que o short solto (era isso que a frase antiga violava);
  3. o teto de envios por dia e consistente com a cota padrao e o custo do
     envio, em vez de ser um numero escrito a mao;
  4. a frase antiga NAO voltou para o codigo;
  5. e a consequencia que importa ao dono fica escrita: 7/dia/canal passa do
     teto de cota.

E um teste cobra que o que eu NAO sei continue declarado: se os tres canais
compartilham um projeto do Google Cloud. Sem isso, a proxima rodada pode ler
"6 por canal" onde o medido e "6 por projeto".
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ORQ = (RAIZ / "fabrica" / "orquestra.py").read_text(encoding="utf-8")
ROTINA = (RAIZ / "docs" / "ROTINA.md").read_text(encoding="utf-8")
DOC = RAIZ / "docs" / "pipeline-canal-dark-v2-o-que-entrou.md"

# Custos publicados da YouTube Data API v3, e a cota padrao de um projeto.
# Nao sao limiar nosso: sao preco de tabela da API, e e por isso que entram.
CUSTO_VIDEOS_INSERT = 1600
CUSTO_CAPTIONS_INSERT = 400
COTA_PADRAO_DIA = 10000


def test_o_teto_sai_da_ARITMETICA_e_nao_de_numero_escrito_a_mao():
    """6 = 10.000 / 1.600, derivado — nao um numero que alguem digitou."""
    teto = COTA_PADRAO_DIA // CUSTO_VIDEOS_INSERT
    assert teto == 6, teto
    # e os 40 da frase antiga pediriam mais de seis vezes a cota padrao
    assert 40 * CUSTO_VIDEOS_INSERT > 6 * COTA_PADRAO_DIA


def test_o_PACOTE_custa_mais_que_o_short_solto():
    """A propriedade que a frase antiga violava, e a razao de ela ser falsa."""
    short_solto = CUSTO_VIDEOS_INSERT
    pacote = CUSTO_VIDEOS_INSERT + CUSTO_CAPTIONS_INSERT
    assert pacote > short_solto, (short_solto, pacote)
    # E a §4 da rotina declara a mesma ordem. A primeira versao deste assert
    # comparava a POSICAO das strings "1.600" e "2.100" no documento inteiro, e
    # reprovou: "~2.100" aparece muito antes, falando de VIEWS/dia da frota.
    # Numero solto num documento de 65 KB nao identifica a afirmacao — a linha
    # que fala de COTA e que precisa ser lida.
    # A afirmacao da §4 QUEBRA EM DUAS LINHAS ("~1.600 de cota" / "contra
    # ~2.100 do pacote"), e a segunda versao deste assert leu uma linha so e
    # estourou. Lido como PARAGRAFO, que e a unidade da afirmacao.
    paragrafos = [p.replace("\n", " ") for p in ROTINA.split("\n\n")]
    alvo = [p for p in paragrafos if "de cota" in p and "1.600" in p and "2.100" in p]
    assert alvo, "o paragrafo da §4 que declara as duas cotas desapareceu"
    p = alvo[0]
    assert p.index("1.600") < p.index("2.100"), p
    assert "pacote" in p.split("2.100", 1)[1][:40], p


def test_o_custo_declarado_na_rotina_BATE_com_videos_insert():
    """1.600 nao e coincidencia: e o preco de tabela do `videos.insert`."""
    assert str(CUSTO_VIDEOS_INSERT) in ROTINA.replace(".", "")
    # o pacote declarado fica entre o envio puro e o envio + legenda + folga
    assert CUSTO_VIDEOS_INSERT < 2100 <= CUSTO_VIDEOS_INSERT + CUSTO_CAPTIONS_INSERT + 200


def test_a_frase_ERRADA_so_aparece_DENTRO_da_retratacao():
    """Retratacao sem teste volta — e esta volta CALADA, num comentario.

    A primeira versao deste assert era `morta not in ORQ`, e ela REPROVOU: as
    duas frases erradas aparecem no proprio texto da correcao, citadas para
    dizer o que estava errado. **Proibir a string proibiria a retratacao** — e
    e exatamente o defeito que eu cometi em 16/10 no
    `test_o_sinal_tambem_se_estabelece_para_BAIXO`, cuja primeira versao proibia
    a string "N de N acima" no modulo e com isso proibia a propria queda dela.
    Segunda vez da mesma assinatura.

    O que se cobra e a PROPRIEDADE: a frase morta pode existir como HISTORIA,
    citada dentro do bloco de correcao, e nao como afirmacao viva.
    """
    marca = "CORRECAO DE 18/10/2026"
    assert marca in ORQ
    inicio = ORQ.index(marca)
    for morta in ("~500 unidades de um pacote", "40 videos por janela"):
        assert morta in ORQ, f"a historia foi apagada em vez de retratada: {morta!r}"
        # toda ocorrencia tem de estar DEPOIS do inicio do bloco de correcao
        pos = -1
        while True:
            pos = ORQ.find(morta, pos + 1)
            if pos == -1:
                break
            assert pos > inicio, (
                f"{morta!r} aparece FORA do bloco de correcao, isto e, como "
                "afirmacao viva outra vez"
            )


def test_o_motivo_do_conserto_continua_ESCRITO_no_modulo():
    """Conserto sem motivo escrito volta, porque ninguem sabe por que mudou."""
    assert "CORRECAO DE 18/10/2026" in ORQ
    assert "6 envios de video por dia por projeto" in ORQ
    # e a procedencia da conferencia (contradicao interna, nao autoridade alheia)
    assert "entre dois" in ORQ and "NOSSOS" in ORQ


def test_a_CONSEQUENCIA_para_o_pedido_do_dono_vai_escrita():
    """O achado so vale se a consequencia dos 7/dia estiver nomeada."""
    assert "7 shorts/dia/canal" in ORQ
    assert "extensao de cota" in ORQ.lower() or "extensao de cota" in ORQ


def test_o_que_eu_NAO_sei_continua_declarado():
    """Se um projeto ou tres: isso decide 6/dia na frota contra 6/dia por canal.

    Falha se alguem apagar a ressalva — porque ai a rodada seguinte le "6 por
    canal" como medido, e nao esta.
    """
    assert "UM projeto do Google Cloud" in ORQ or "um projeto do Google Cloud" in ORQ
    assert "tokens.py:205-206" in ORQ, "a evidencia do modelo compartilhado saiu"


def test_o_documento_da_leitura_EXISTE_e_nao_e_so_citado():
    """O defeito do 743: citar caminho e afirmar que o caminho existe."""
    assert DOC.exists(), f"{DOC} citado e inexistente"
    texto = DOC.read_text(encoding="utf-8")
    assert len(texto) > 3000, len(texto)
    # e ele carrega as duas metades: o que entrou e o que foi FALSIFICADO
    assert "FALSIFICA" in texto
    assert "oembed" in texto, "a prova anonima de que as pecas sao publicas saiu"


def test_a_varredura_deste_arquivo_nao_ficou_VAZIA():
    """Um regex que deixa de casar faria todos os asserts passarem calados."""
    assert re.search(r"videos\.insert", ORQ) or "videos.insert" in ORQ
    assert len(ORQ) > 5000, len(ORQ)
    assert len(ROTINA) > 50000, len(ROTINA)
