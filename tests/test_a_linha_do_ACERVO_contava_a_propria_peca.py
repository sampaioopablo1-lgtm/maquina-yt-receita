"""A linha do ACERVO e a da NOVIDADE, no MESMO relato, discordavam.

**Medido em 22/10 as 11:4x, no relato da peca daquela rodada.** Com a spec no
disco, o `esqueleto_entre_canais.relato` imprimia

    acervo: 424 pecas, 177 formas; 34 atravessam canal e levam 271 pecas (64%)
    ...
    esqueleto INEDITO nas 176 formas de short da frota

isto e, **dois numeros para o MESMO fato em linhas vizinhas do mesmo relato**,
porque so a frase da novidade filtrava a propria peca (`exceto`) e as outras
tres contas leiam `varre()` cru. E o **753 dentro de um relato** — a mesma
forma da banda cravada no texto do `mira` (15/10) e da linha do piso que nao
dizia de quantos mundos ela era (21/10 as 18:3x) — com o `exceto` chegando a
UMA das contas, que e a familia de 20/10 as 14:3x.

**E a divergencia aparece justamente quando a rodada ACERTA:** as duas linhas
so discordam na contagem de FORMAS quando a peca e o UNICO exemplar da propria
forma, que e o alvo declarado de toda rodada. A linha de PECAS discorda
SEMPRE, porque a peca perguntada esta sempre dentro do `varre()`.

O custo e de LEITURA e nao de veredito: o `forma_inedita` sempre saiu filtrado,
logo nenhuma peca foi publicada com a forma errada. O que o relato convidava a
fazer era citar o numero da linha do acervo na copy — e ai a peca se contaria
contra si mesma.
"""
import ast
import inspect
import os
import sys
import textwrap

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))

import esqueleto_entre_canais as EC            # noqa: E402
import contagem_de_cenas as CC                 # noqa: E402
import nome_da_spec as NS                      # noqa: E402

PISO_PECAS = 200          # guarda de vacuidade: o disco tem centenas
# MEDIDO em 22/10 as 11:4x, com 424 pecas no disco.
UNICOS_MEDIDOS = 137
PECAS_MEDIDAS = 424


def _fonte(fn) -> ast.AST:
    """`textwrap.dedent` e nao `inspect.cleandoc`: o cleandoc desindenta a
    linha do `def` e deixa o corpo torto (IndentationError) — 22/10 as 08:3x."""
    return ast.parse(textwrap.dedent(inspect.getsource(fn)))


@pytest.fixture(scope="module")
def pecas():
    p = EC.varre()
    assert len(p) >= PISO_PECAS, (
        "a varredura do disco voltou com %d peca(s): abaixo de %d este arquivo"
        " passa por VACUIDADE e nao mede nada" % (len(p), PISO_PECAS))
    return p


@pytest.fixture(scope="module")
def unico(pecas):
    """Uma peca que e o UNICO exemplar da propria forma, DERIVADA do disco.

    Nomear um pacote aqui seria identidade onde ha propriedade (743/753/761):
    os ids mudam a cada rodada e a forma de hoje e exemplar unico ate alguem
    repeti-la.
    """
    cf = EC.quadro(pecas)["contagem_da_forma"]
    cand = [p for p in pecas if cf.get(p["esqueleto"], 0) == 1]
    assert cand, (
        "nenhuma peca do disco e o UNICO exemplar da propria forma — este"
        " arquivo perdeu a ANCORA: a divergencia que ele mede so aparece"
        " nesse caso, e sem ela ele passaria sem medir nada")
    return sorted(cand, key=lambda p: p["arquivo"])[0]


def test_o_defeito_de_fato_OCORRIA(pecas, unico):
    """Com a populacao CRUA as duas contas discordam — e e isso que o conserto
    desfaz. Sem este teste, *'eu errei'* seria afirmacao minha e nao medida."""
    cru = EC.quadro(pecas)["formas"]
    filtrado = EC.novidade(unico["esqueleto"], unico["cenas"], pecas,
                           unico["arquivo"])["formas_na_frota"]
    assert cru == filtrado + 1, (
        "a divergencia que este arquivo mede desapareceu: cru %d, filtrado %d"
        % (cru, filtrado))


def test_a_linha_de_PECAS_discordava_SEMPRE(pecas):
    """A contagem de PECAS nao depende de a forma ser unica: a peca
    perguntada esta sempre dentro do `varre()`."""
    for p in pecas[:25]:
        assert len(EC.sem(pecas, p["arquivo"])) == len(pecas) - 1, (
            "a peca %s nao saiu da populacao" % p["arquivo"])


def test_o_relato_CONCORDA_consigo_mesmo(unico):
    """A linha do ACERVO e a da NOVIDADE citam o MESMO numero de formas."""
    # o caminho se DERIVA do `DIR_SPECS` do proprio modulo: cravar o diretorio
    # aqui seria o segundo dono de onde as specs moram.
    r = EC.relato(os.path.join(EC.DIR_SPECS, unico["arquivo"]))
    acervo = [l for l in r.split("\n") if l.strip().startswith("acervo:")]
    novid = [l for l in r.split("\n") if "formas de short da frota" in l]
    assert acervo and novid, r
    n_acervo = int(acervo[0].split("pecas,")[1].split("formas")[0].strip())
    n_novid = int(novid[0].split("nas")[1].split("formas")[0].strip())
    assert n_acervo == n_novid, (
        "o MESMO relato cita %d formas na linha do acervo e %d na da novidade"
        % (n_acervo, n_novid))


def test_SEM_peca_perguntada_o_relato_conta_a_frota_INTEIRA(pecas):
    """Contraprova no outro sentido: sem `exceto` nada se filtra.

    Sem ela bastaria filtrar sempre — e um relato que sempre tira uma peca
    descreveria uma frota que nao existe.
    """
    r = EC.relato()
    acervo = [l for l in r.split("\n") if l.strip().startswith("acervo:")]
    assert acervo, r
    n = int(acervo[0].split("acervo:")[1].split("pecas")[0].strip())
    assert n == len(pecas), (
        "sem peca perguntada o acervo devia ser a frota inteira (%d) e veio %d"
        % (len(pecas), n))


def test_sem_SEM_exceto_devolve_a_lista_como_VEIO(pecas):
    """Ausencia de nome nao e ausencia de peca — a licao de 17/10."""
    assert EC.sem(pecas, "") == pecas
    assert EC.sem(pecas, None) == pecas


def test_sem_delega_o_casamento_ao_nome_da_spec(pecas, unico):
    """As duas convencoes de nome tem UM dono (20/10 as 11:3x)."""
    pac = NS.pacote(unico["arquivo"])
    arq = NS.arquivo(unico["arquivo"])
    assert len(EC.sem(pecas, pac)) == len(pecas) - 1
    assert len(EC.sem(pecas, arq)) == len(pecas) - 1
    # e por AST: o `sem` nao compara nome por conta propria
    fonte = _fonte(EC.sem)
    nomes = {n.attr for n in ast.walk(fonte) if isinstance(n, ast.Attribute)}
    assert "casa" in nomes, (
        "o `sem` tem de CHAMAR o `nome_da_spec.casa`; comparar nome aqui"
        " seria o segundo dono das duas convencoes")


def test_o_filtro_tem_UM_dono_por_AST():
    """A compreensao do filtro so pode viver dentro do `sem`.

    Recopia-la em outra funcao e o segundo dono do mesmo fato — a assinatura
    que congelou a legenda, parou a mira por seis pecas e pos job inventado na
    serie.
    """
    for mod in (EC, CC):
        arv = ast.parse(open(mod.__file__, encoding="utf-8").read())
        for fn in ast.walk(arv):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if fn.name == "sem":
                continue
            for n in ast.walk(fn):
                if not isinstance(n, ast.Attribute) or n.attr != "casa":
                    continue
                raise AssertionError(
                    "%s.%s compara nome por conta propria: o filtro da peca"
                    " perguntada tem UM dono, o `esqueleto_entre_canais.sem`"
                    % (os.path.basename(mod.__file__), fn.name))


def test_o_relato_filtra_UMA_vez_e_as_contas_leem_a_MESMA_lista():
    """Por AST: o `relato` chama o `sem`, e nenhuma conta dele le `varre()`
    cru. Era exatamente isso que produzia os dois numeros."""
    fonte = _fonte(EC.relato)
    chamadas = [n for n in ast.walk(fonte) if isinstance(n, ast.Call)]
    nomes = [n.func.id for n in chamadas
             if isinstance(n.func, ast.Name)]
    assert "sem" in nomes, (
        "o `relato` tem de filtrar a populacao pelo `sem` — sem isso a linha"
        " do acervo volta a contar a propria peca")
    for n in chamadas:
        if isinstance(n.func, ast.Name) and n.func.id == "quadro":
            arg = n.args[0] if n.args else None
            assert isinstance(arg, ast.Name) and arg.id == "pecas", (
                "o `quadro` do relato tem de receber a lista JA filtrada")


def test_a_medida_e_RECONFERIDA_contra_o_disco(pecas):
    """O numero que torna o achado grave nao pode envelhecer calado (753).

    E ele tem de ter os DOIS lados: se NENHUMA peca for exemplar unico a nota
    perde o objeto, e se TODAS forem a divergencia deixa de ser o caso do
    acerto e passa a ser o estado normal do disco.
    """
    cf = EC.quadro(pecas)["contagem_da_forma"]
    unicos = [p for p in pecas if cf.get(p["esqueleto"], 0) == 1]
    assert 0 < len(unicos) < len(pecas), (
        "%d de %d: sem os dois lados esta nota nao se le" % (len(unicos),
                                                             len(pecas)))
    frac = 100.0 * len(unicos) / len(pecas)
    assert 15.0 <= frac <= 60.0, (
        "a fracao de pecas que sao exemplar unico da propria forma saiu de"
        " %.1f%% para fora da faixa medida — releia a nota em vez de mover o"
        " numero (medido: %d de %d)" % (frac, UNICOS_MEDIDOS, PECAS_MEDIDAS))


def test_contagens_da_frota_nao_conta_a_propria_peca(pecas, unico):
    """A conta irma, no `contagem_de_cenas`, delega ao MESMO dono."""
    fonte = _fonte(CC.contagens_da_frota)
    nomes = {n.attr for n in ast.walk(fonte) if isinstance(n, ast.Attribute)}
    assert "sem" in nomes, (
        "o `contagens_da_frota` tem de chamar o `EC.sem`")
    com = CC.contagens_da_frota(exceto=unico["arquivo"])
    s = unico["cenas"]
    sem_ = CC.contagens_da_frota()
    assert com.get(s, 0) == sem_.get(s, 0) - 1, (
        "a peca perguntada nao saiu da contagem do proprio tamanho")


def test_o_motivo_continua_escrito(pecas):
    """Conserto sem motivo escrito volta calado — e a rodada seguinte
    reescreve o filtro, como eu reescrevi o contador de canal cinco vezes."""
    doc = EC.sem.__doc__ or ""
    for marca in ("acervo", "NOVIDADE", "753", "nome_da_spec"):
        assert marca in doc, (
            "o motivo do `sem` perdeu a marca %r" % marca)
