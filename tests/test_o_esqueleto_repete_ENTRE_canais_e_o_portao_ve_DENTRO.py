"""O esqueleto atravessa canal, e o portao `variedade` compara DENTRO de um.

Guarda o achado de 20/10 as 01:3x e o instrumento que o produziu. A forma
destes testes e a da semana: a varredura sai do DISCO e reprova vazia, a
delegacao e cobrada por AST, os DOIS lados do achado tem de existir, e ha
teste que reprova quando o achado SUMIR — para que a nota seja relida em vez
de o numero ser movido.
"""
import ast
import collections
import json
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import esqueleto_entre_canais as EC   # noqa: E402
import variedade as V                 # noqa: E402

MOD = os.path.join(RAIZ, "fabrica", "esqueleto_entre_canais.py")

# Pisos OBSERVADOS em 20/10, nao escolhidos. Eles guardam contra vacuidade: um
# glob que deixa de casar faria todo teste aqui passar sem medir nada, que e o
# defeito do 743 em forma de glob.
MIN_SPECS = 200
MIN_FORMAS = 60


@pytest.fixture(scope="module")
def pecas():
    return EC.varre()


def test_a_varredura_sai_do_DISCO_e_nao_fica_vazia(pecas):
    assert len(pecas) >= MIN_SPECS, (
        f"so {len(pecas)} specs com short — a varredura encolheu e os outros "
        "testes deste arquivo passariam por vacuidade"
    )
    for p in pecas[:5]:
        assert p["cenas"] > 0 and p["esqueleto"] and p["canal"]


def test_varredura_de_diretorio_vazio_LEVANTA(tmp_path):
    """Ausencia de leitura nao e 'frota sem esqueleto'."""
    with pytest.raises(RuntimeError, match="AUSENCIA DE LEITURA"):
        EC.varre(str(tmp_path))


def test_a_assinatura_e_DELEGADA_ao_variedade_por_AST():
    """O docstring CITA o `"-".join(...)` em prosa para se explicar, logo
    casar prosa pegaria a explicacao em vez do codigo."""
    arv = ast.parse(open(MOD, encoding="utf-8").read())
    chama_o_dono = False
    for n in ast.walk(arv):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "esqueleto"
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "V"):
            chama_o_dono = True
        # nenhum `"-".join(...)` proprio: isso seria o SEGUNDO dono
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "join"
                and isinstance(n.func.value, ast.Constant)
                and n.func.value.value == "-"):
            pytest.fail(
                "o modulo remonta a assinatura do esqueleto com '-'.join — "
                "isso cria o segundo dono da regra, que e a assinatura que "
                "congelou a legenda e parou a mira de conferir"
            )
    assert chama_o_dono, "a assinatura tem de sair de `variedade.esqueleto`"


def test_o_limiar_do_portao_e_LIDO_e_nao_copiado():
    arv = ast.parse(open(MOD, encoding="utf-8").read())
    for n in ast.walk(arv):
        if (isinstance(n, ast.Attribute) and n.attr == "ESQUELETO_AVISA_EM"):
            break
    else:
        pytest.fail("o limiar tem de sair de `variedade.ESQUELETO_AVISA_EM`")
    c = EC.cegas_para_o_portao()
    assert c["limiar_do_portao"] == V.ESQUELETO_AVISA_EM


def test_os_DOIS_lados_do_achado_existem(pecas):
    """Sem forma que atravessa E forma de um canal so, nada esta medido."""
    q = EC.quadro(pecas)
    assert q["formas"] >= MIN_FORMAS
    atrav = [e for e, c in q["canais_da_forma"].items() if len(c) > 1]
    unica = [e for e, c in q["canais_da_forma"].items() if len(c) == 1]
    assert atrav, "nenhuma forma atravessa canal — o achado se desfez"
    assert unica, (
        "TODA forma atravessa canal — se isto acontecer, a fracao deixa de "
        "discriminar e esta nota tem de ser relida"
    )


def test_a_fracao_que_ATRAVESSA_nao_desabou(pecas):
    """Reprova se o achado encolher, para a nota ser RELIDA.

    O piso e o valor OBSERVADO menos folga (74% no acervo, 67% nos vivos).
    Ele reprova nos dois sentidos: se despencar, a producao variou e isto se
    rele; se for a 100%, a medida perdeu o contraste.
    """
    for so_vivos, piso in ((False, 0.50), (True, 0.45)):
        q = EC.quadro(pecas, so_vivos=so_vivos)
        f = q["fracao_atravessada"]
        assert piso <= f < 1.0, (
            f"fracao atravessada {f:.2f} fora de [{piso}, 1.0) "
            f"(so_vivos={so_vivos}) — releia a nota de 20/10 as 01:3x"
        )


def test_o_portao_e_CEGO_para_a_maioria_delas(pecas):
    """O numero agudo: 33 de 34 formas que atravessam nao disparam o portao."""
    c = EC.cegas_para_o_portao(pecas)
    assert len(c["cegas"]) > len(c["vistas_por_acidente"]), (
        "a maioria das formas que atravessam canal deixou de ser invisivel "
        "ao portao — se isso acontecer o portao passou a cobrir a dimensao e "
        "este modulo perde a razao de existir"
    )
    assert c["pecas_cegas"] > 0


def test_a_cegueira_do_portao_e_REAL_nao_deduzida(pecas):
    """Contraprova chamando o DONO: o `variedade.analisa` de uma peca cuja
    forma vive em varios canais com UM exemplar em cada nao avisa nada sobre
    esqueleto; e a mesma funcao AVISA quando a forma repete no canal."""
    q = EC.quadro(pecas)
    alvo = None
    for esq, canais in q["canais_da_forma"].items():
        if len(canais) < 3:
            continue
        por = collections.Counter(
            p["canal"] for p in pecas if p["esqueleto"] == esq)
        if max(por.values()) == 1:
            alvo = (esq, por)
            break
    assert alvo, (
        "nenhuma forma com 3+ canais e UM exemplar em cada — sem este caso o "
        "arquivo nao mede a cegueira e passa por vacuidade"
    )
    esq, _ = alvo
    arq = next(p["arquivo"] for p in pecas if p["esqueleto"] == esq)
    sp = json.load(open(os.path.join(RAIZ, "fabrica", "specs", arq),
                       encoding="utf-8"))
    _erros, avisos = V.analisa(sp, raiz=RAIZ, arquivo=arq)
    assert not [a for a in avisos if "esqueleto" in a], (
        f"o portao avisou sobre o esqueleto de {arq}, que vive em 3+ canais "
        "com um exemplar em cada — se ele passou a ver isso, releia a nota"
    )
    # ... e o outro sentido: a forma mais repetida DENTRO de um canal avisa.
    maior = max(q["contagem_da_forma"], key=lambda e: q["contagem_da_forma"][e])
    por = collections.Counter(
        p["canal"] for p in pecas if p["esqueleto"] == maior)
    assert max(por.values()) >= V.ESQUELETO_AVISA_EM, (
        "a forma mais repetida da frota nao chega ao limiar do portao dentro "
        "de nenhum canal — sem esse lado, 'o portao e cego' nao diz nada, "
        "porque ele nao veria coisa alguma"
    )


def test_a_novidade_EXCLUI_a_propria_peca(pecas):
    """O defeito da primeira execucao, cobrado nos DOIS sentidos."""
    alvo = next(p for p in pecas
                if sum(1 for q in pecas if q["esqueleto"] == p["esqueleto"]) == 1)
    com = EC.novidade(alvo["esqueleto"], alvo["cenas"], pecas,
                      exceto=alvo["arquivo"])
    sem = EC.novidade(alvo["esqueleto"], alvo["cenas"], pecas)
    assert com["forma_inedita"] is True, (
        "com `exceto`, forma de um unico exemplar tem de sair INEDITA"
    )
    assert sem["forma_inedita"] is False and sem["exemplares_da_forma"] == 1, (
        "sem `exceto` a peca se conta a si mesma — e esse era o defeito"
    )


def test_a_novidade_responde_as_TRES_perguntas(pecas):
    n = EC.novidade("titulo-cta-NAO-EXISTE-EM-LUGAR-NENHUM", 99, pecas)
    assert n["forma_inedita"] and n["tamanho_inedito"]
    assert n["canais_da_forma"] == []
    assert n["formas_na_frota"] >= MIN_FORMAS
    assert 5 in n["contagens_existentes"] and 10 in n["contagens_existentes"]


def test_os_VIVOS_sao_subconjunto_e_o_acervo_DILUI(pecas):
    """A licao do 762: acervo dilui rodada, logo os dois quadros tem de sair."""
    assert set(EC.CANAIS_VIVOS) <= {p["canal"] for p in pecas}
    q = EC.quadro(pecas)
    qv = EC.quadro(pecas, so_vivos=True)
    assert 0 < qv["pecas"] < q["pecas"], (
        "o quadro dos vivos deixou de ser menor que o do acervo — ou o filtro "
        "parou de filtrar, ou a frota passou a ser o acervo inteiro"
    )


def test_NAO_e_portao_e_o_prontidao_NAO_o_importa():
    """Pelo argumento do `mira.py`: ele reprovaria o acervo inteiro.

    Por AST, porque o `prontidao.py` pode citar o nome do modulo na prosa que
    explica por que ele ficou de fora — casar prosa pegaria a explicacao.
    """
    r = subprocess.run(
        [sys.executable, MOD,
         os.path.join(RAIZ, "fabrica", "specs", "kolejny-poziom-s072.json")],
        capture_output=True, text=True, cwd=RAIZ, timeout=300)
    assert r.returncode == 0, "isto INFORMA: o codigo de saida e sempre zero"
    assert "INVISIVEIS ao portao" in r.stdout

    arv = ast.parse(open(os.path.join(RAIZ, "fabrica", "prontidao.py"),
                         encoding="utf-8").read())
    for n in ast.walk(arv):
        nomes = []
        if isinstance(n, ast.Import):
            nomes = [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            nomes = [n.module or ""]
        assert "esqueleto_entre_canais" not in nomes, (
            "o `prontidao` passou a importar o instrumento — isto nao e "
            "portao, e como portao reprovaria 271 specs de acervo"
        )


def test_o_relato_NOMEIA_a_dimensao_que_o_portao_nao_ve():
    t = EC.relato()
    assert "MESMO canal" in t and "_especs_do_canal" in t, (
        "o relato tem de dizer POR QUE o portao nao ve, senao a proxima "
        "rodada lê o aviso verde dele como 'o esqueleto esta variado'"
    )
