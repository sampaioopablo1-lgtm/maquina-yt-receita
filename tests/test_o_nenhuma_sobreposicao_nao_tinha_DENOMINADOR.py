""""Nenhuma sobreposicao" nao valia a mesma coisa em dois irmaos — 21/10, 01:3x.

O `cobertura_dos_capitulos` nasceu UMA rodada antes e dizia *"nenhuma
sobreposicao entre os declarados e os seus"* **sem o denominador**. Medido nos
103 irmaos que declaram capitulo em origem de 20+ capitulos, a fracao do longo
que um irmao reivindica vai de **1% a 62%**, logo a chance de colidir com uma
familia de cinco capitulos — sob SORTEIO — vai de **0,05 a 0,99**, mediana 0,41.

Irmao que declara 1 de 100: "nao colidiu" era quase certo por construcao e prova
quase nada. Irmao que declara 40 de 64: "nao colidiu" e sinal forte. O
instrumento devolvia o BINARIO e nunca o denominador — a primeira linha da
disciplina da rotina aplicada ao meu proprio instrumento de um dia.

E A NULA VAI DECLARADA E E FALSA DE PROPOSITO: capitulo de familia nao e
sorteado, vem em bloco contiguo. O numero e ordem de grandeza da FORCA, nunca
probabilidade do mundo — e ha teste cobrando que essa ressalva continue na saida.
"""
import ast
import inspect
import math
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO  # noqa: E402
import segundo_angulo as SA    # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "irmaos_da_origem.py")


def _declarantes():
    """Todo irmao do disco que declara capitulo, com o tamanho do longo dele.

    DERIVADO — nomear pacotes seria identidade onde ha propriedade
    (743/753/761), e o disco muda a cada rodada.
    """
    import glob
    import json
    saida = []
    vistas = set()
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short"):
            continue
        o = d.get("longo_existente")
        if not o or o in vistas:
            continue
        vistas.add(o)
        n = (SA.nao_mencionados(o) or {}).get("n_capitulos") or 0
        if n < 20:
            continue
        for i in IO.irmaos(o):
            caps = i["capitulos_declarados"]
            if caps:
                saida.append((i["pacote"], len(caps), n))
    return saida


def test_a_varredura_nao_passa_por_VACUIDADE():
    d = _declarantes()
    assert len(d) >= 50, (
        "so %d irmaos declarantes no disco; abaixo de 50 este arquivo passa "
        "por vacuidade" % len(d))


def test_os_DOIS_regimes_de_forca_EXISTEM_no_disco():
    """Se todos os irmaos reivindicassem a mesma fracao, o denominador nao
    mudaria nada e esta nota se releria."""
    ps = [IO.forca_da_ausencia(k, n) for _, k, n in _declarantes()]
    ps = [x for x in ps if x is not None]
    assert min(ps) < 0.25, (
        "nenhum irmao do disco esta no regime FRACO (P < 0,25) — sem ele o "
        "aviso de 'prova pouco' nunca dispara e a nota perde o objeto")
    assert max(ps) >= 0.75, (
        "nenhum irmao do disco esta no regime FORTE (P >= 0,75) — sem ele "
        "'nenhuma sobreposicao' nunca vale como sinal, e isso tambem se rele")
    assert max(ps) / max(min(ps), 1e-9) >= 4.0, (
        "a razao entre o mais forte e o mais fraco caiu para %.1f; abaixo de "
        "4x o denominador deixa de trocar a leitura" % (max(ps) / min(ps)))


def test_a_conta_bate_com_a_hipergeometrica_feita_a_mao():
    """A conta e verificavel e vai verificada — nao delegada a ninguem, porque
    aqui ESTE modulo e o dono dela."""
    for k, n, m in ((3, 69, 5), (1, 100, 5), (40, 64, 5), (18, 56, 5)):
        esperado = 1.0 - math.comb(n - k, m) / float(math.comb(n, m))
        assert abs(IO.forca_da_ausencia(k, n, m) - esperado) < 1e-12, (k, n, m)


def test_os_casos_degenerados_devolvem_None_e_nao_ZERO():
    """Zero leria como 'colisao impossivel', que e o oposto de 'nao sei'."""
    assert IO.forca_da_ausencia(0, 50) is None
    assert IO.forca_da_ausencia(3, 0) is None
    assert IO.forca_da_ausencia(-1, 50) is None
    # e quando o irmao reivindica quase tudo, a colisao e CERTA
    assert IO.forca_da_ausencia(60, 62, 5) == 1.0


def test_a_cobertura_carrega_a_forca_POR_IRMAO():
    d = _declarantes()
    pac = d[0][0]
    # a origem do primeiro declarante, derivada pelo proprio modulo
    import glob
    import json
    origem = None
    for p in glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")):
        try:
            x = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if x.get("pacote") == pac:
            origem = x.get("longo_existente")
    assert origem, "perdi a ancora: o declarante derivado nao tem origem"
    c = IO.cobertura_dos_capitulos(origem, meus=[1, 2, 3])
    assert "forca" in c, "a cobertura deixou de carregar a forca"
    for p2 in c["conhecidos"]:
        assert p2 in c["forca"], (
            "%s esta em `conhecidos` e nao tem forca — irmao conferido sem "
            "denominador e o defeito que este arquivo mede" % p2)
        v = c["forca"][p2]
        assert v["n_capitulos"] > 0, (
            "o tamanho do longo saiu ZERO para %s: foi assim que a primeira "
            "versao disto calou, com um `except Exception` engolindo a guarda "
            "`_dir_valido` de 20/10 as 12:3x" % p2)


def test_a_LINHA_avisa_no_regime_fraco_e_credita_no_FORTE():
    """Os dois ramos, cobrados no DONO da frase com dicionario construido —
    ancorar no disco vivo seria identidade onde ha propriedade."""
    fraco = {"forca": {"irmao-a": {"declarados": 1, "n_capitulos": 100,
                                   "p_colidiria": 0.05}}}
    L = "\n".join(IO._linha_da_forca(fraco))
    assert "QUASE CERTO" in L and "prova" in L.lower(), (
        "no regime fraco a linha tem de dizer que prova pouco; saiu: %r" % L)
    assert "LEITURA" in L, (
        "no regime fraco ela tem de apontar para onde ir — a leitura")

    forte = {"forca": {"irmao-b": {"declarados": 40, "n_capitulos": 64,
                                   "p_colidiria": 0.99}}}
    M = "\n".join(IO._linha_da_forca(forte))
    assert "FORTE" in M, (
        "no regime forte a linha tem de creditar o sinal; saiu: %r" % M)
    assert "QUASE CERTO" not in M, (
        "o aviso do regime fraco saiu no regime forte")

    # e o pior caso governa: um irmao fraco ao lado de um forte nao apaga o forte
    misto = {"forca": {
        "a": {"declarados": 1, "n_capitulos": 100, "p_colidiria": 0.05},
        "b": {"declarados": 40, "n_capitulos": 64, "p_colidiria": 0.99}}}
    X = "\n".join(IO._linha_da_forca(misto))
    assert "FORTE" in X and "QUASE CERTO" not in X, (
        "com um irmao forte presente a ausencia JA e informativa; saiu: %r" % X)


def test_sem_denominador_ela_DIZ_que_nao_calculou():
    """Ausencia de denominador nao e denominador grande — e foi exatamente isso
    que a primeira versao fez calada."""
    L = "\n".join(IO._linha_da_forca({"forca": {}}))
    assert "NAO calculada" in L, (
        "sem forca nenhuma a linha tem de DIZER isso em vez de calar; "
        "saiu: %r" % L)
    assert "nao e denominador grande" in L, (
        "a razao tem de ir escrita onde ela e lida")


def test_a_NULA_vai_declarada_como_nula_na_SAIDA():
    """Tratar isto como probabilidade do mundo seria o erro INVERSO do que o
    instrumento conserta, e a ressalva tem de viver na saida, nao so no
    docstring — e a saida que a rodada seguinte le."""
    forte = {"forca": {"b": {"declarados": 40, "n_capitulos": 64,
                             "p_colidiria": 0.99}}}
    M = "\n".join(IO._linha_da_forca(forte))
    assert "SORTEIO" in M, "a nula nao vai nomeada na saida"
    assert "contiguo" in M.lower(), (
        "a saida tem de dizer POR QUE a nula e falsa — capitulo de familia vem "
        "em bloco contiguo")
    assert "nunca probabilidade" in M.lower(), (
        "a saida tem de proibir a leitura como probabilidade do mundo")


def test_o_tamanho_do_longo_e_DELEGADO_e_o_caminho_tem_UM_dono():
    """Recontar capitulo aqui criaria o segundo dono, e errar a POSICAO do
    argumento foi o que calou a primeira versao."""
    arvore = ast.parse(open(FONTE, encoding="utf-8").read())
    fn = [n for n in ast.walk(arvore)
          if isinstance(n, ast.FunctionDef)
          and n.name == "cobertura_dos_capitulos"][0]
    txt = ast.unparse(fn)
    assert "SA.nao_mencionados" in txt, (
        "a contagem de capitulo deixou de ser delegada ao dono")
    assert "_dir_specs" in txt, (
        "o caminho das specs tem de sair do helper de UM dono — foi passar a "
        "raiz na posicao de `dir_specs` que calou a primeira versao")
    assert "except Exception" not in txt, (
        "voltou um `except Exception` em volta da chamada: ele ENGOLE a guarda "
        "`_dir_valido` de 20/10 as 12:3x, que nasceu para LEVANTAR. Guarda "
        "engolida por chamador e guarda que nao existe")


def test_o_motivo_e_a_medida_continuam_escritos():
    doc = inspect.getdoc(IO.forca_da_ausencia) or ""
    assert "103" in doc, "a medida dos 103 declarantes saiu do docstring"
    assert "0,05" in doc and "0,99" in doc, (
        "a faixa de P que torna o achado grave saiu do docstring")
    assert "FALSA de proposito" in doc or "falso de proposito" in doc.lower(), (
        "a declaracao de que a nula e falsa de proposito saiu do docstring")


def test_o_RELATO_alcanca_a_forca_e_nao_a_descarta():
    """ESTE TESTE NASCEU DA PROPRIA CONTRAPROVA FALHANDO EM FALHAR.

    Desligada a chamada em `_linha_da_cobertura`, os dez testes acima passaram
    TODOS — porque todos chamam `_linha_da_forca` direto. Isto e exatamente a
    classe que o instrumento conserta: calculado e descartado pelo chamador,
    como a nota da rota em 13:2x e o `quadro` do `contagem_de_cenas` em 03:2x.
    O arquivo escrito para pegar esse defeito o tinha dentro.
    """
    # (a) por AST: a linha da cobertura tem de CHAMAR a da forca
    arvore = ast.parse(open(FONTE, encoding="utf-8").read())
    fn = [n for n in ast.walk(arvore)
          if isinstance(n, ast.FunctionDef)
          and n.name == "_linha_da_cobertura"][0]
    chamadas = [c.func.id for c in ast.walk(fn)
                if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)]
    assert "_linha_da_forca" in chamadas, (
        "`_linha_da_cobertura` nao chama `_linha_da_forca`: a forca e "
        "calculada e descartada, que e o defeito de 13:2x")

    # (b) de ponta a ponta, numa origem REAL de ausencia — derivada, nao nomeada
    alvo = None
    for pac, k, n in _declarantes():
        import glob
        import json
        for p in glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")):
            try:
                x = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            if x.get("pacote") != pac:
                continue
            o = x.get("longo_existente")
            c = IO.cobertura_dos_capitulos(o, meus=[n + 10, n + 11])
            if c["conhecidos"] and not c["colidem"]:
                alvo = o
            break
        if alvo:
            break
    assert alvo, (
        "perdi a ancora: nenhuma origem do disco produz o caso 'ha irmao "
        "declarante E nenhuma sobreposicao', que e onde a forca importa")
    L = "\n".join(IO._linha_da_cobertura(alvo, meus=[999, 1000]))
    assert "nenhuma sobreposicao" in L, "o caso derivado nao e o de ausencia"
    assert "SORTEIO" in L, (
        "o relato da cobertura NAO carrega a forca da ausencia: ela ficou "
        "calculada e jogada fora. Saiu:\n%s" % L)
