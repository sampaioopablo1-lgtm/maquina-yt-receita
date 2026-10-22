"""As formas JA USADAS num tamanho de cena sairam de um laco escrito na hora.

**Medido em 22/10 as 16:3x, escrevendo o `epomeno-epipedo-s095`.** O
`esqueleto_entre_canais.novidade` devolve um VEREDITO sobre uma forma e uma
CONTAGEM do tamanho (`formas_do_tamanho`), e o `formas_livres` devolve ordens
que ninguem usou. **Nenhum dos dois devolve a LISTA das usadas** — e e ela que
se le para escolher esqueleto quando a primeira forma colide. Logo, a cada
rodada, eu escrevia um laco sobre `varre()` na linha de comando. Terceira vez
nesta sessao, e e o item 3 da §10.

**E a falta JA PRODUZIU um defeito medido, com custo:** em 21/10 as 23:2x eu
precisei exatamente desta lista, escrevi o laco e cortei a saida com `tail -10`
sobre um tamanho que tinha DEZ formas — li as sete ultimas como se fossem o
conjunto e escolhi um esqueleto que JA EXISTIA. E a familia da fatia do proxy
(19/10 as 19:2x) e da fatia dos capitulos livres (22/10 as 10:3x): ler uma
ponta de lista como se fosse a lista.

**O tamanho do risco vai MEDIDO:** dos treze tamanhos de cena que a frota usa,
DEZ tem oito formas ou mais — um `tail -10` corta a lista em dez de treze. E o
pior deles e o mais usado: dez cenas tem 65 formas em 149 pecas.

O que este arquivo cobra e PROPRIEDADE e nao numero: que a lista saia inteira,
que a contagem venha na frente (e com ela um corte na leitura fique visivel),
que os DOIS lados existam (tamanho usado e tamanho inedito), e que a varredura
seja DELEGADA em vez de recopiada.
"""
import ast
import inspect
import os
import sys
import textwrap

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))

import esqueleto_entre_canais as EC            # noqa: E402
import nome_da_spec as NS                      # noqa: E402

PISO_PECAS = 200     # guarda de vacuidade: o disco tem centenas
PISO_FORMAS = 8      # a largura em que um `tail -10` ja corta
# MEDIDO em 22/10 as 16:3x: 13 tamanhos usados, 10 deles com 8+ formas,
# e dez cenas com 65 formas em 149 pecas. Vai como HISTORIA — os asserts
# cobram a propriedade, nao estes numeros (743/753/761).
MEDIDA_DE_16H = {"tamanhos": 13, "com_8_mais": 10, "pior": (10, 65, 149)}
# O defeito de 21/10 as 23:2x fica como HISTORIA, e nenhum assert depende dele.
FATIA_DE_23H = ("kolejny-poziom-s090", 13, 10)


def _fonte(fn) -> ast.AST:
    """`textwrap.dedent` e nao `inspect.cleandoc`: o cleandoc desindenta a
    linha do `def` e deixa o corpo torto (IndentationError) — 22/10 as 08:3x."""
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


def _chamadas(fn) -> set:
    nomes = set()
    for n in ast.walk(_fonte(fn)):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                nomes.add(f.id)
            elif isinstance(f, ast.Attribute):
                nomes.add(f.attr)
    return nomes


@pytest.fixture(scope="module")
def disco():
    p = EC.varre()
    assert len(p) >= PISO_PECAS, (
        "a varredura do disco voltou com %d peca(s), abaixo do piso de %d — "
        "sem populacao este arquivo passa por VACUIDADE, que e o defeito do "
        "743 em forma de glob" % (len(p), PISO_PECAS))
    return p


@pytest.fixture(scope="module")
def por_tamanho(disco):
    d = {}
    for x in disco:
        if x.get("esqueleto"):
            d.setdefault(x["cenas"], {}).setdefault(x["esqueleto"], []).append(
                x["arquivo"])
    return d


def test_a_lista_sai_INTEIRA_e_bate_com_a_varredura(disco, por_tamanho):
    """Nao basta a contagem: o instrumento existe porque eu precisava da LISTA."""
    for n, formas in por_tamanho.items():
        u = EC.formas_usadas_do_tamanho(n, pecas=disco)
        assert u["n_formas"] == len(formas), n
        assert len(u["formas"]) == u["n_formas"], (
            "o campo `formas` tem %d entrada(s) e `n_formas` diz %d — e o 753 "
            "dentro do proprio retorno" % (len(u["formas"]), u["n_formas"]))
        assert {f["esqueleto"] for f in u["formas"]} == set(formas), n
        assert u["n_pecas"] == sum(len(v) for v in formas.values()), n
        for f in u["formas"]:
            assert sorted(f["arquivos"]) == sorted(formas[f["esqueleto"]]), n


def test_a_FATIA_descartava_a_maioria_e_isso_e_RECONFERIDO(por_tamanho):
    """O defeito de 21/10 as 23:2x nao e afirmacao minha: ele se remede.

    E ele tem de continuar ocorrendo em ALGUM tamanho, senao a frase do
    instrumento perde o objeto e esta nota se rele.
    """
    largos = {n: len(f) for n, f in por_tamanho.items()
              if len(f) >= PISO_FORMAS}
    assert largos, (
        "nenhum tamanho tem %d formas ou mais — a fatia de dez linhas nao "
        "corta nada hoje, logo o motivo do instrumento caiu e esta nota tem "
        "de ser RELIDA em vez de o numero ser movido" % PISO_FORMAS)
    estreitos = {n for n, f in por_tamanho.items() if len(f) < PISO_FORMAS}
    assert estreitos, (
        "TODO tamanho tem %d formas ou mais — sem o lado contrario a medida "
        "nao distingue nada" % PISO_FORMAS)
    pior = max(largos, key=lambda n: largos[n])
    descartadas = largos[pior] - 7      # as sete ultimas que o `tail -10` deixa
    assert descartadas > largos[pior] // 2, (
        "no tamanho de %d cenas a fatia das sete ultimas descartaria %d de "
        "%d formas, que ja nao e a maioria" % (pior, descartadas, largos[pior]))


def test_os_DOIS_lados_existem_e_o_inedito_DIZ_em_vez_de_calar(disco,
                                                               por_tamanho):
    """Tamanho inedito devolve VAZIO e nao levanta — ali o vazio e o valor
    CERTO —, e a frase o diz em letra, para nao se confundir com varredura
    que falhou (17/10)."""
    usados = set(por_tamanho)
    ineditos = [n for n in range(2, 21) if n not in usados]
    assert usados, "nenhum tamanho usado: a varredura quebrou"
    assert ineditos, (
        "a frota usa TODOS os tamanhos de 2 a 20 — o ramo do inedito perde o "
        "objeto e esta nota se rele")
    n = sorted(ineditos)[0]
    u = EC.formas_usadas_do_tamanho(n, pecas=disco)
    assert u["usado"] is False and u["formas"] == [] and u["n_pecas"] == 0
    frase = EC._linha_das_formas_usadas(n, disco, "")
    assert "NENHUMA" in frase and "nunca usou" in frase, frase

    m = sorted(usados)[-1]
    u2 = EC.formas_usadas_do_tamanho(m, pecas=disco)
    assert u2["usado"] is True and u2["formas"]


def test_a_CONTAGEM_vem_antes_de_qualquer_esqueleto_na_frase(disco,
                                                             por_tamanho):
    """Com a contagem na frente, um corte na leitura fica visivel — e a
    disciplina do `segundo_angulo.relato_dos_livres`, de 22/10 as 10:3x."""
    n = max(por_tamanho, key=lambda k: len(por_tamanho[k]))
    frase = EC._linha_das_formas_usadas(n, disco, "")
    linhas = frase.splitlines()
    cab = linhas[0]
    assert "%d forma(s)" % len(por_tamanho[n]) in cab, cab
    assert "titulo" not in cab, (
        "o cabecalho ja traz esqueleto, logo a contagem deixou de vir "
        "primeiro: %r" % cab)
    assert len(linhas) == 1 + len(por_tamanho[n]), (
        "a frase tem %d linha(s) para %d forma(s) — ela esta TRUNCANDO, que e "
        "o defeito que ela existe para impedir"
        % (len(linhas) - 1, len(por_tamanho[n])))


def test_o_exceto_vai_nos_DOIS_sentidos_com_ancora_DERIVADA(disco,
                                                            por_tamanho):
    """Nomear um pacote seria identidade onde ha propriedade (743/753/761): a
    ancora e DERIVADA do disco, e o teste reprova dizendo que a perdeu."""
    alvo = None
    for n, formas in sorted(por_tamanho.items()):
        for e, arqs in sorted(formas.items()):
            if len(arqs) == 1:
                alvo = (n, e, arqs[0])
                break
        if alvo:
            break
    assert alvo, (
        "nenhuma forma do disco tem UM exemplar so — o teste perdeu a ancora; "
        "releia em vez de afrouxar")
    n, esq, arq = alvo

    com = EC.formas_usadas_do_tamanho(n, pecas=disco, exceto=arq)
    sem_ = EC.formas_usadas_do_tamanho(n, pecas=disco)
    assert esq in {f["esqueleto"] for f in sem_["formas"]}
    assert esq not in {f["esqueleto"] for f in com["formas"]}, (
        "com `exceto` a propria peca continua se contando")
    assert com["n_pecas"] == sem_["n_pecas"] - 1

    # contraprova no outro sentido: nome que nao casa nao filtra nada
    nada = EC.formas_usadas_do_tamanho(
        n, pecas=disco, exceto="nao-existe-mesmo-9999.json")
    assert nada["n_pecas"] == sem_["n_pecas"], (
        "`exceto` que nao casa filtrou peca — ausencia de nome nao e ausencia "
        "de peca (17/10)")


def test_a_varredura_e_o_filtro_sao_DELEGADOS_por_AST():
    """Recopiar o `glob` ou o casamento de nome aqui criaria o SEGUNDO dono —
    a assinatura que congelou a legenda."""
    ch = _chamadas(EC.formas_usadas_do_tamanho)
    assert "varre" in ch, "a varredura tem de ser DELEGADA ao `varre`"
    assert "sem" in ch, (
        "o filtro da propria peca tem de ser DELEGADO ao `sem`, que e o dono "
        "das duas convencoes de nome (20/10 as 11:3x)")
    for proibido in ("glob", "listdir", "open", "load", "casa", "arquivo"):
        assert proibido not in ch, (
            "`%s` no corpo do `formas_usadas_do_tamanho`: isso e o segundo "
            "dono da varredura ou do nome" % proibido)


def test_a_frase_tem_UM_dono_e_o_relato_a_CHAMA():
    """Import sem chamada e a classe dos layouts mortos (19/10 as 04:2x).

    **E o dono e a FUNCAO, nao a contagem de string — a primeira versao deste
    teste cobrava `fonte.count(marca) == 1` e REPROVOU o modulo certo**, porque
    a marca sai nos DOIS ramos da mesma funcao (tamanho usado e tamanho
    inedito), que e precisamente o que se quer. E a licao de 20/10 as 05:2x:
    cobrar a contagem proibiria justamente o ramo que impede a frase de ser
    dita sem dado. Por AST, entao: a marca so pode aparecer DENTRO do dono.
    """
    marca = "FORMAS USADAS em"
    dono = "_linha_das_formas_usadas"
    assert marca in inspect.getsource(getattr(EC, dono))
    for nome in dir(EC):
        fn = getattr(EC, nome)
        if not inspect.isfunction(fn) or nome == dono:
            continue
        if getattr(fn, "__module__", None) != EC.__name__:
            continue
        for n in ast.walk(_fonte(fn)):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                assert marca not in n.value, (
                    "a marca %r aparece em `%s`, fora do dono `%s` — e o "
                    "segundo dono da frase" % (marca, nome, dono))
    assert dono in _chamadas(EC.relato), (
        "o `relato` nao chama a linha: instrumento que ninguem chama PARECE "
        "pronto e nao esta no ar")


def test_o_relato_de_uma_peca_REAL_traz_a_lista(disco, por_tamanho):
    """O defeito era de CHAMADOR, logo o caminho inteiro e cobrado."""
    import json
    alvo = None
    for n in sorted(por_tamanho, reverse=True):
        if len(por_tamanho[n]) < PISO_FORMAS:
            continue
        for arqs in por_tamanho[n].values():
            alvo = (n, arqs[0])
            break
        if alvo:
            break
    assert alvo, "o teste perdeu a ancora: nenhum tamanho largo no disco"
    n, arq = alvo
    sp = json.load(open(os.path.join(EC.DIR_SPECS, arq)))
    r = EC.relato(os.path.join(EC.DIR_SPECS, arq), spec=sp)
    assert "FORMAS USADAS em %d cenas" % n in r, r[-900:]
    # a lista do relato ja vem SEM a propria peca, pelo `exceto`
    esperado = len(EC.formas_usadas_do_tamanho(n, pecas=disco, exceto=arq)
                   ["formas"])
    assert "%d forma(s)" % esperado in r


def test_os_CANAIS_de_cada_forma_batem_com_o_quadro(disco, por_tamanho):
    """A dimensao do pedido do dono (`em TODOS os canais`) tem de sobreviver
    aqui, senao a lista volta a nao responder a pergunta dele."""
    q = EC.quadro(disco)
    atravessa = False
    for n in por_tamanho:
        u = EC.formas_usadas_do_tamanho(n, pecas=disco)
        for f in u["formas"]:
            assert sorted(f["canais"]) == sorted(
                q["canais_da_forma"][f["esqueleto"]]), f["esqueleto"]
            if len(f["canais"]) > 1:
                atravessa = True
        assert set(u["canais"]) == {c for f in u["formas"] for c in f["canais"]}
    assert atravessa, (
        "nenhuma forma de nenhum tamanho atravessa canal — o `quadro` mede o "
        "contrario, logo a leitura dos canais aqui quebrou")


def test_a_medida_e_o_defeito_continuam_escritos():
    """Instrumento sem o motivo escrito volta calado."""
    fonte = inspect.getsource(EC.formas_usadas_do_tamanho)
    for marca in ("21/10", "tail -10", "10:3x", "13", "65"):
        assert marca in fonte, (
            "a procedencia %r saiu do docstring: sem ela a rodada seguinte "
            "reescreve o laco" % marca)
