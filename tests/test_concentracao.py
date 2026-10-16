"""A concentracao de pauta por origem, ancorada no numero REAL de 13/10 04:0x.

Este arquivo existe porque eu minerei o MESMO longo (`ntrMxq89I4o`) dez vezes
seguidas no labtreinamento enquanto NOVE das treze origens do canal tinham sido
usadas uma vez so. Nao foi escassez de pauta: foi habito meu, e eu so vi ao
CONTAR. O risco e o portao `similaridade`, que e de MONETIZACAO (conteudo
inautentico do YPP) e nao de estetica.

O limiar de alerta e OBSERVADO e declarado no modulo: mais que o DOBRO da
segunda origem. Um teste abaixo trava o caso de fronteira — 10 contra 5 e
exatamente o dobro e NAO alerta — porque essa foi a leitura real da rodada e eu
relatei assim em vez de arredondar para "alertou".
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import concentracao as C  # noqa: E402


def test_o_caso_REAL_de_13_10_dez_contra_cinco_NAO_alerta_e_isso_e_honesto():
    # Medido: ntrMxq89I4o com 10, 4OYBkCHFTV8 com 5. 10 nao e MAIOR que 2x5,
    # e 10 > 2*5 e falso. O relato da rodada disse exatamente isso.
    r = C.analise({"ntrMxq89I4o": 10, "4OYBkCHFTV8": 5, "6BeNHqT2okA": 4,
                   "bQoujWaY7Hw": 2, "a": 1, "b": 1, "c": 1, "d": 1, "e": 1,
                   "f": 1, "g": 1, "h": 1, "i": 1})
    assert r["dominante"] == "ntrMxq89I4o"
    assert r["n_dominante"] == 10 and r["n_segunda"] == 5
    assert r["alerta"] is False, (
        "10 contra 5 e exatamente o dobro; o limiar e MAIS que o dobro")
    assert len(r["usadas_uma_vez"]) == 9


def test_UM_a_mais_na_dominante_JA_alerta():
    r = C.analise({"x": 11, "y": 5})
    assert r["alerta"] is True
    assert "MONETIZACAO" in r["motivo"]


def test_origem_unica_alerta_porque_o_canal_depende_de_um_texto_so():
    r = C.analise({"x": 3})
    assert r["n_segunda"] == 0
    assert r["alerta"] is True


def test_canal_equilibrado_nao_alerta():
    r = C.analise({"a": 3, "b": 3, "c": 2})
    assert r["alerta"] is False
    assert "dentro do dobro" in r["motivo"]


def test_sem_origem_declarada_e_SILENCIO_e_nao_zero():
    r = C.analise({})
    assert r["total_shorts"] == 0
    assert r["alerta"] is False
    assert "nenhum short" in r["motivo"]


def test_contagem_le_as_specs_de_verdade_e_acha_o_dominante_do_labtreinamento():
    c = C.contagem("labtreinamento")
    assert c, "o canal tem shorts com origem declarada"
    r = C.analise(c)
    # Nao travo o VALOR (ele cresce a cada peca); travo que o instrumento
    # enxerga concentracao e nomeia as pouco usadas, que e o que decide pauta.
    assert r["dominante"] in c
    assert r["n_dominante"] >= r["n_segunda"]
    assert isinstance(r["usadas_uma_vez"], list)


def test_o_relato_NOMEIA_as_origens_pouco_usadas():
    """14/10: o texto mudou porque o relato passou a SEPARAR escrevivel de
    sem-fonte. A intencao do teste e a mesma — as pouco usadas vao NOMEADAS —
    e por isso ele passou a cobrar a intencao em vez da frase antiga."""
    texto = C.relato("labtreinamento")
    assert "nao reprova" in texto
    a = C.analise(C.contagem("labtreinamento"), "labtreinamento")
    poucas = a["recomendadas"] + a["sem_fonte_local"]
    # 761: este teste CRAVAVA a frase "usadas UMA vez", que so existe nos dois
    # ramos de LISTA do relato. Em 14/10 as 15:2x o canal deixou de ter origem de
    # um uso so (o s049 e o s050 consumiram as duas ultimas) e o relato passou ao
    # ramo "nenhuma origem usada UMA vez" — o teste reprovou por uma frase, nao
    # por uma propriedade. E a propriedade que importa e esta: SE houver pouco
    # usadas, elas vao NOMEADAS; se nao houver, o relato tem de DIZER isso em vez
    # de calar. Mesma classe do 743 e do 753: guardar o TEXTO em vez do fato.
    if poucas:
        assert "UMA vez" in texto
        for o in poucas:
            assert o in texto, f"origem pouco usada {o} ficou fora do relato"
    else:
        assert "nenhuma origem usada UMA vez" in texto
        assert "MENOR contagem" in texto, (
            "sem origem de um uso so o relato tem de dizer para onde ir")


def test_origem_SEM_SPEC_LOCAL_nao_entra_nas_recomendadas(tmp_path):
    """O defeito de 14/10: duas origens recomendadas nao tinham fonte nenhuma.

    `KRUERlNPzDw` e `StQNFMdpGdk` tem SETE capitulos de titulo e nenhuma faixa de
    legenda (runs 38504585378 e 38504726301) — e a regra (h) proibe escrever a
    partir de titulo. O modulo apontava as duas como a proxima peca.
    """
    (tmp_path / "ch-s001.json").write_text(
        json.dumps({"longo_existente": "COM_SPEC"}), encoding="utf-8")
    (tmp_path / "ch-s002.json").write_text(
        json.dumps({"longo_existente": "SEM_SPEC"}), encoding="utf-8")
    # so a primeira tem spec de longo com capitulos
    (tmp_path / "ch-001.json").write_text(
        json.dumps({"longo_existente": "COM_SPEC",
                    "longo": [{"nar": "x"}]}), encoding="utf-8")
    a = C.analise(C.contagem("ch", str(tmp_path)), "ch", str(tmp_path))
    assert a["recomendadas"] == ["COM_SPEC"]
    assert a["sem_fonte_local"] == ["SEM_SPEC"]


def test_spec_de_longo_VAZIA_nao_conta_como_fonte(tmp_path):
    """Spec homonima sem `longo` nao da texto nenhum — foi o falso positivo do
    `segundo_angulo` em 12/10, do outro lado."""
    (tmp_path / "ch-s001.json").write_text(
        json.dumps({"longo_existente": "AAA"}), encoding="utf-8")
    (tmp_path / "ch-001.json").write_text(
        json.dumps({"longo_existente": "AAA", "longo": []}), encoding="utf-8")
    assert C.escrevivel("AAA", "ch", str(tmp_path)) is False


def test_o_relato_DIZ_que_sem_spec_local_nao_e_inviavel(tmp_path):
    """Ele nao pode afirmar inviabilidade: a legenda pode existir."""
    (tmp_path / "ch-s001.json").write_text(
        json.dumps({"longo_existente": "SEM_SPEC"}), encoding="utf-8")
    texto = C.relato("ch", str(tmp_path))
    assert "LEGENDA" in texto and "capitulos.yml" in texto
    assert "nao escreva a partir de titulo" in texto


def test_as_duas_origens_de_14_10_TINHAM_spec_local__RETRATACAO():
    """RETRATADO em 16/10 as 11:4x, e o teste e que me obrigou a conferir.

    A versao anterior exigia `escrevivel(...) is False` para `KRUERlNPzDw` e
    `StQNFMdpGdk`, ancorada na minha afirmacao de 14/10 (aprendizados 759/761)
    de que as duas nao tinham spec local. **A afirmacao era falsa:** elas sao o
    `labtreinamento-002` e o `-003`, com **87 e 84** capitulos no disco.

    O que produzia o falso negativo era o resolvedor, nao o dado: o
    `segundo_angulo.pacote_do_id` le o vinculo `origem -> pacote` da COPY de um
    short que nomeie o pacote, logo e cego para origem que ainda nao gerou um
    short com esse texto. O mapa `youtube_id -> pacote` estava no retrato da
    ponte desde sempre, e agora o `escrevivel` o consulta como ultimo recurso.

    O custo foi real e vai dito: por tres rodadas eu fui pela rota da LEGENDA
    (regra h) para origens cujo texto estava no disco. A rota funcionou e era
    legitima — ela so nao era necessaria.
    """
    for o in ("KRUERlNPzDw", "StQNFMdpGdk"):
        assert C.escrevivel(o, "labtreinamento") is True, (
            f"{o} voltou a NAO ser escrevivel: ou o retrato da ponte saiu do"
            " caminho, ou a spec de longo perdeu os capitulos — releia o"
            " aprendizado 759/761 antes de mandar a rodada pela legenda")


def test_o_conserto_NAO_devolve_True_para_tudo():
    """Contraprova: origem sem spec de longo no disco continua False.

    Sem este teste o conserto acima passaria por vacuidade — bastaria
    `escrevivel` devolver True sempre. O `FtCtIJPsc_Q` e o longo que o dono
    apontou: ele NAO tem pacote no retrato nem spec de longo local, e a rota
    dele e de fato a legenda.
    """
    assert C.escrevivel("FtCtIJPsc_Q", "labtreinamento") is False
    assert C.escrevivel("id-que-nao-existe", "labtreinamento") is False


def test_contagem_ignora_short_sem_longo_existente(tmp_path):
    (tmp_path / "ch-s001.json").write_text(
        json.dumps({"longo_existente": "AAA"}), encoding="utf-8")
    (tmp_path / "ch-s002.json").write_text(json.dumps({}), encoding="utf-8")
    assert C.contagem("ch", str(tmp_path)) == {"AAA": 1}
