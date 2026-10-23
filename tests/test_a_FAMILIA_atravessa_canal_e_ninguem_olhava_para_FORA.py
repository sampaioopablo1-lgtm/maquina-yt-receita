"""A FAMILIA atravessa canal, e a conferencia era a minha MEMORIA.

Medido em 23/10 as 17:0x, escolhendo a familia do `epomeno-epipedo-s102`: eu
descartei a candidata da ATRIBUICAO porque ela e o eixo do
`kolejny-poziom-s099`, publicado HOJE em OUTRO canal — e eu sabia isso de
cabeca. As tres comparacoes que existiam param antes desta: o
`irmaos_da_origem` olha DENTRO da origem, o portao `similaridade` compara
titulo contra o MESMO canal, e o `esqueleto_entre_canais` atravessa canal mas
compara a FORMA.

E A QUINTA FORMA DE SLUG saiu deste instrumento, na primeira execucao: o parque
grava `<pacote>-longo` para a peca de pacote, e o `canal.do_pacote` nao a
conhecia — as TRES linhas de longo de 19/10 resolviam para si mesmas e viravam
canal FANTASMA.
"""
import ast
import glob
import inspect
import io
import json
import os
import subprocess
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import canal as CA                      # noqa: E402
import duracao_a_medir as DM            # noqa: E402
import familia_entre_canais as FC       # noqa: E402
import irmaos_da_origem as IO           # noqa: E402
import pauta_do_momento as PM           # noqa: E402

SPECS = os.path.join(RAIZ, "fabrica", "specs")
FROTA = ("labtreinamento", "epomeno-epipedo", "kolejny-poziom")

# HISTORIA, e nenhum assert depende dela: a medida de 23/10 as 17:0x foi 138 de
# 311 specs de short solto COM o campo (0,444) e TRES de 163 linhas do parque
# com o sufixo `-longo`. Contagem absoluta sobre populacao que cresce uma spec
# por rodada e identidade disfarcada de medida (22/10, 14:4x), logo o que os
# testes cobram e a PROPORCAO e a presenca dos dois lados.
MEDIDA_DE_17H = {"com_campo": 138, "sem_campo": 311 - 138, "longo_no_parque": 3}


def _corpo(f) -> str:
    return textwrap.dedent(inspect.getsource(f))


def _arvore_sem_docstring(f):
    a = ast.parse(_corpo(f)).body[0]
    corpo = list(a.body)
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return corpo


def _chamadas(f) -> set:
    nomes = set()
    for no in corpo_nos(f):
        for n in ast.walk(no):
            if isinstance(n, ast.Call):
                nomes.add(ast.unparse(n.func))
    return nomes


def corpo_nos(f):
    return _arvore_sem_docstring(f)


def _nomes_do_disco() -> list:
    return [os.path.basename(p)[:-5]
            for p in sorted(glob.glob(os.path.join(SPECS, "*.json")))]


def _shorts_soltos_com_copy() -> list:
    fora = []
    for p in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        try:
            sp = json.load(io.open(p, encoding="utf-8"))
        except Exception:
            continue
        if sp.get("longo") or not sp.get("short"):
            continue
        if not (sp.get("copy") or ""):
            continue
        fora.append((os.path.basename(p)[:-5], sp))
    return fora


def _parque_proprio(linhas) -> list:
    """Parque PROPRIO: ancorar no vivo seria identidade onde ha propriedade."""
    return [dict(x) for x in linhas]


# --------------------------------------------------------------- vacuidade

def test_o_parque_tem_peca_de_mais_de_um_canal_da_frota():
    regs = DM.carrega()
    canais = {CA.do_pacote(r.get("pacote") or "") for r in regs}
    vivos = canais & set(FROTA)
    assert len(regs) >= 20, (
        "parque com %d linha(s): abaixo disso este arquivo nao mede nada"
        % len(regs))
    assert len(vivos) >= 2, (
        "o parque tem peca de %s so — sem dois canais nao existe 'entre "
        "canais', e este arquivo passaria por vacuidade" % sorted(vivos))


def test_os_DOIS_lados_do_campo_da_familia_existem_no_disco():
    pares = _shorts_soltos_com_copy()
    assert len(pares) >= 150, (
        "so %d spec(s) de short solto com copy: piso de vacuidade" % len(pares))
    com = [n for n, sp in pares
           if IO._secao(sp.get("copy") or "", IO.CAMPO_FAMILIA).strip()]
    sem = [n for n, sp in pares if n not in set(com)]
    frac = len(com) / float(len(pares))
    assert com and sem, (
        "o acervo tem um lado so (com=%d, sem=%d): sem os dois, um dos ramos "
        "do instrumento nunca e exercitado e a nota tem de ser RELIDA em vez "
        "de o numero ser movido" % (len(com), len(sem)))
    assert 0.15 <= frac <= 0.85, (
        "fracao com o campo = %.3f, fora da faixa 0,15 a 0,85 medida em 23/10 "
        "(era %.3f): se o acervo foi uniformizado, a leitura por PROSA perde o "
        "objeto e esta nota se rele" % (frac, 138 / 311.0))


# ------------------------------------------------- o que o instrumento faz

def test_ele_devolve_as_ultimas_de_cada_OUTRO_canal_e_NUNCA_do_proprio():
    for c in FROTA:
        d = FC.recentes_de_outros(c)
        assert c not in d["outros"], (
            "o canal %s apareceu na propria leitura: o instrumento existe para "
            "olhar para FORA" % c)
        for outro, pecas in d["outros"].items():
            assert outro != c
            assert len(pecas) <= FC.RECENTES_K
            for f in pecas:
                assert CA.do_pacote(f["pacote"]) == outro


def test_o_K_e_respeitado_na_FRONTEIRA():
    k = 2
    linhas = []
    for i in range(k + 3):
        linhas.append({"pacote": "kolejny-poziom-s%03d" % (90 + i),
                       "em": "2026-10-20T%02d:00:00Z" % (10 + i)})
    d = FC.recentes_de_outros("labtreinamento", k=k,
                              parque=_parque_proprio(linhas))
    assert len(d["outros"]["kolejny-poziom"]) == k
    pacs = [f["pacote"] for f in d["outros"]["kolejny-poziom"]]
    assert pacs == ["kolejny-poziom-s%03d" % (90 + k + 2),
                    "kolejny-poziom-s%03d" % (90 + k + 1)], (
        "as %d devolvidas tem de ser as MAIS NOVAS, e sairam %s — ler a ponta "
        "velha de uma lista e a familia da fatia do proxy (19/10, 19:2x)"
        % (k, pacs))


def test_o_canal_sai_do_do_pacote_e_NAO_do_campo_canal():
    """PROPRIEDADE e nao identidade: 57 das 163 linhas do parque nao tem o
    campo `canal`, logo ler o campo perderia essas pecas em silencio."""
    linhas = _parque_proprio([
        {"pacote": "kolejny-poziom-s090", "em": "2026-10-20T10:00:00Z"},
    ])
    assert "canal" not in linhas[0]
    d = FC.recentes_de_outros("labtreinamento", parque=linhas)
    assert [f["pacote"] for f in d["outros"].get("kolejny-poziom", [])] == \
        ["kolejny-poziom-s090"], (
        "registro SEM o campo `canal` desapareceu: o canal tem de sair do "
        "`canal.do_pacote`")


def test_a_RECUSA_vem_com_motivo_quando_nenhum_outro_canal_tem_peca():
    linhas = _parque_proprio([
        {"pacote": "labtreinamento-s117", "em": "2026-10-23T14:30:27Z"},
    ])
    d = FC.recentes_de_outros("labtreinamento", parque=linhas)
    assert d["recusa"], "parque com so o proprio canal tinha de RECUSAR"
    assert "ESTADO" in d["recusa"], "a recusa vai com o MOTIVO escrito"
    t = FC.relato("labtreinamento", parque=linhas)
    assert d["recusa"].split("—")[0].strip()[:20] in t


def test_contraproba_com_outro_canal_no_parque_ele_NAO_recusa():
    """Sem este par, recusar sempre passaria."""
    linhas = _parque_proprio([
        {"pacote": "labtreinamento-s117", "em": "2026-10-23T14:30:27Z"},
        {"pacote": "kolejny-poziom-s102", "em": "2026-10-23T15:43:45Z"},
    ])
    d = FC.recentes_de_outros("labtreinamento", parque=linhas)
    assert not d["recusa"]
    assert d["outros"]["kolejny-poziom"]


def test_spec_ausente_sai_NOMEADA_e_nao_desaparece():
    linhas = _parque_proprio([
        {"pacote": "kolejny-poziom-s999", "em": "2026-10-20T10:00:00Z"},
    ])
    d = FC.recentes_de_outros("labtreinamento", parque=linhas)
    f = d["outros"]["kolejny-poziom"][0]
    assert f["sem_spec"] is True and f["tem_campo"] is None, (
        "spec ausente tem de sair com `tem_campo` None e nao False: ausencia "
        "de leitura nao e ausencia de familia (17/10)")
    t = FC.relato("labtreinamento", parque=linhas)
    assert "spec NAO esta no disco" in t and "kolejny-poziom-s999" in t


def test_peca_SEM_campo_entrega_PROSA_e_NARRACAO_inteiras():
    pares = _shorts_soltos_com_copy()
    alvo = None
    for n, sp in pares:
        if IO._secao(sp.get("copy") or "", IO.CAMPO_FAMILIA).strip():
            continue
        if IO._narracao(sp):
            alvo = (n, sp)
            break
    if alvo is None:
        pytest.fail("perdi a ancora: nenhuma spec de short solto SEM o campo "
                    "da familia e COM narracao no disco")
    n, sp = alvo
    f = FC.familia_da_peca(n)
    assert f["tem_campo"] is False
    assert f["narracao"] == IO._narracao(sp), (
        "a narracao tem de vir do DONO e INTEIRA — truncar por tamanho foi o "
        "que quase cortou a frase que salvou o `labtreinamento-s035`")
    linhas = _parque_proprio([{"pacote": n, "em": "2026-10-20T10:00:00Z"}])
    outro = "labtreinamento" if CA.do_pacote(n) != "labtreinamento" \
        else "kolejny-poziom"
    t = FC.relato(outro, parque=linhas)
    for fala in IO._narracao(sp):
        assert fala in t, "narracao truncada no relato: %r" % fala[:40]


def test_peca_COM_campo_NAO_recebe_prosa_nem_narracao():
    """O campo e o dono quando existe; imprimir os dois criaria o segundo."""
    pares = _shorts_soltos_com_copy()
    alvo = next((p for p in pares
                 if IO._secao(p[1].get("copy") or "",
                              IO.CAMPO_FAMILIA).strip()), None)
    if alvo is None:
        pytest.fail("perdi a ancora: nenhuma spec COM o campo no disco")
    f = FC.familia_da_peca(alvo[0])
    assert f["tem_campo"] is True and f["campo"]
    assert f["prosa"] == [] and f["narracao"] == [], (
        "peca COM o campo recebeu prosa/narracao: o campo deixaria de ser dono "
        "unico da familia")


def test_o_exceto_tira_a_peca_da_rodada_e_so_ela():
    linhas = _parque_proprio([
        {"pacote": "kolejny-poziom-s101", "em": "2026-10-23T12:33:45Z"},
        {"pacote": "kolejny-poziom-s102", "em": "2026-10-23T15:43:45Z"},
    ])
    sem = FC.recentes_de_outros("labtreinamento", parque=linhas)
    com = FC.recentes_de_outros("labtreinamento", parque=linhas,
                                exceto="kolejny-poziom-s102")
    assert len(sem["outros"]["kolejny-poziom"]) == 2
    assert [f["pacote"] for f in com["outros"]["kolejny-poziom"]] == \
        ["kolejny-poziom-s101"]
    nada = FC.recentes_de_outros("labtreinamento", parque=linhas,
                                 exceto="kolejny-poziom-s999")
    assert len(nada["outros"]["kolejny-poziom"]) == 2, (
        "`exceto` que nao casa nao filtra nada (20/10, 11:3x)")


# --------------------------------------------------- a QUINTA forma de slug

def test_a_QUINTA_forma_de_slug_resolve_para_o_canal():
    for pac, esperado in (("epomeno-epipedo-068-longo", "epomeno-epipedo"),
                          ("epomeno-epipedo-068-short", "epomeno-epipedo"),
                          ("labtreinamento-014-longo", "labtreinamento"),
                          ("kolejny-poziom-020-longo", "kolejny-poziom")):
        assert CA.do_pacote(pac) == esperado, (
            "%r -> %r: a forma do parque virava canal FANTASMA"
            % (pac, CA.do_pacote(pac)))


def test_as_formas_ANTIGAS_nao_mudaram():
    """Contraproba: o conserto quase virou regressao — a primeira versao
    iterava os dois cortes e mudava `kp-plan-9233-20260811`."""
    for pac, esperado in (("labtreinamento-s083", "labtreinamento"),
                          ("epomeno-epipedo-068", "epomeno-epipedo"),
                          ("epomeno-epipedo", "epomeno-epipedo"),
                          ("kp-plan-9233", "kp-plan"),
                          ("kp-plan-9233-20260811", "kp-plan-9233"),
                          ("", "")):
        assert CA.do_pacote(pac) == esperado, (
            "%r mudou para %r e a forma antiga esperava %r"
            % (pac, CA.do_pacote(pac), esperado))


def test_NENHUM_nome_do_disco_termina_nos_dois_sufixos():
    """A medida que AUTORIZOU o corte, reconferida contra o disco (753)."""
    nomes = _nomes_do_disco()
    assert len(nomes) >= 200, "piso de vacuidade: %d nome(s)" % len(nomes)
    maus = [n for n in nomes
            if n.endswith("-longo") or n.endswith("-short")]
    assert not maus, (
        "o corte de `-longo`/`-short` foi autorizado por NENHUM nome do disco "
        "terminar assim, e agora %d termina(m): %s — releia a nota em vez de "
        "mover o numero" % (len(maus), maus[:5]))
    prefixos = {CA.do_pacote(n) for n in nomes}
    maus = [p for p in prefixos
            if p.endswith("-longo") or p.endswith("-short")]
    assert not maus, "prefixo de canal terminando no sufixo: %s" % maus


def test_o_parque_tinha_a_forma_que_o_disco_nao_tem():
    """Sem este lado, o conserto nao tem objeto e esta nota se rele."""
    pacs = {r.get("pacote") or "" for r in DM.carrega()}
    com = [p for p in pacs if p.endswith("-longo") or p.endswith("-short")]
    assert com, (
        "nenhuma linha do parque tem mais a forma `<pacote>-longo`: o defeito "
        "do canal FANTASMA perdeu o objeto e esta nota tem de ser RELIDA")
    for p in com:
        assert CA.do_pacote(p) in FROTA, (
            "%r resolve para %r, que nao e canal da frota" % (p, CA.do_pacote(p)))


# ------------------------------------------------------------- delegacoes

def test_a_RECENCIA_e_a_FAMILIA_saem_dos_DONOS_por_AST():
    for f in (FC.recentes_de_outros, FC.familia_da_peca, FC._spec,
              FC._linha_das_familias):
        fonte = "\n".join(ast.unparse(n) for n in corpo_nos(f))
        for proibido in ("open(", "json.load", "glob.", "listdir",
                         "re.compile", "re.search", "re.findall"):
            assert proibido not in fonte, (
                "%s usa %r: a leitura do parque e do `duracao_a_medir`, a da "
                "spec e do `rascunho` e a da copy e do `irmaos_da_origem` — "
                "reparsear aqui criaria o segundo dono"
                % (f.__name__, proibido))
    chamadas = _chamadas(FC.recentes_de_outros)
    assert "DM.carrega" in chamadas, "a recencia sai do parque, pelo dono"
    assert "CA.do_pacote" in chamadas, "o canal sai do `canal.do_pacote`"
    chamadas = _chamadas(FC.familia_da_peca)
    assert "IO._secao" in chamadas, "o campo e a prosa saem do `_secao`"
    assert "IO._narracao" in chamadas, "a narracao sai do `_narracao`"


def test_o_nome_da_secao_NAO_e_cravado_aqui():
    fonte = inspect.getsource(FC)
    assert "FAMILIA DE ENTRADA ERRADA" not in fonte.replace(
        "`## FAMILIA DE ENTRADA ERRADA`", ""), (
        "o nome da secao esta cravado no modulo: ele e `IO.CAMPO_FAMILIA`")
    assert "IO.CAMPO_FAMILIA" in fonte
    assert "IO.BLOCOS_DE_PROSA" in fonte


def test_ele_NAO_decide_semelhanca():
    fonte = inspect.getsource(FC)
    for proibido in ("difflib", "SequenceMatcher", "import similaridade",
                     "ratio("):
        assert proibido not in fonte, (
            "o modulo usa %r: decidir semelhanca de texto seria detector que "
            "inventa achado (725), e o caso de 23/10 as 17:0x nao compartilha "
            "uma palavra com o irmao de outro canal" % proibido)
    d = FC.recentes_de_outros("epomeno-epipedo")
    for pecas in d["outros"].values():
        for f in pecas:
            assert "repetida" not in f and "igual" not in f, (
                "o instrumento nao tem veredito de semelhanca, e nao deve ter")
    assert "NAO decide se duas familias sao a MESMA" in FC.relato(
        "epomeno-epipedo")


def test_a_frase_tem_UM_dono_e_sai_nos_DOIS_ramos():
    fonte = inspect.getsource(FC)
    marca = "FAMILIA ENTRE CANAIS"
    donos = [n.name for n in ast.walk(ast.parse(fonte))
             if isinstance(n, ast.FunctionDef)
             and marca in ast.unparse(n)]
    assert donos == ["_linha_das_familias"], (
        "a marca %r aparece em %s: a frase tem UM dono" % (marca, donos))
    linhas = _parque_proprio([
        {"pacote": "labtreinamento-s117", "em": "2026-10-23T14:30:27Z"},
    ])
    assert marca in FC.relato("labtreinamento", parque=linhas), \
        "a frase tem de sair tambem no ramo da RECUSA"
    linhas.append({"pacote": "kolejny-poziom-s102",
                   "em": "2026-10-23T15:43:45Z"})
    assert marca in FC.relato("labtreinamento", parque=linhas)


def test_a_PAUTA_chama_este_instrumento_FORA_de_ramo_condicional():
    """Instrumento que a rodada nao chama e a classe dos layouts mortos — e
    dentro de um `if` ele calaria justamente quando nao ha origem escolhida."""
    fonte = inspect.getsource(PM.relato)
    assert "FC." in fonte, "o `pauta_do_momento.relato` nao chama o modulo"
    corpo = _arvore_sem_docstring(PM.relato)
    # A PROPRIEDADE e que o `FC.` nao mora DENTRO de controle de fluxo. A
    # primeira versao deste assert apenas pedia um statement de nivel de cima
    # que CONTIVESSE "FC." — e um `if` de nivel de cima contem o corpo dele,
    # logo ele passava com o defeito religado. Assert que aprova qualquer coisa
    # e a familia do `or True` de 16/10, e a contraproba o pegou.
    fluxo = (ast.If, ast.For, ast.While, ast.Try, ast.With)
    dentro = [ast.unparse(n).splitlines()[0]
              for n in corpo if isinstance(n, fluxo) and "FC." in ast.unparse(n)]
    assert not dentro, (
        "a chamada do `FC.` esta dentro de um ramo condicional (%s): sem "
        "origem escolhida ela calaria, que e o defeito da nota da rota "
        "(20/10, 13:2x)" % dentro)
    solto = [n for n in corpo
             if not isinstance(n, fluxo) and "FC." in ast.unparse(n)]
    assert solto, "nenhum statement de nivel de cima chama o `FC.`"


def test_codigo_de_saida_sempre_zero():
    r = subprocess.run([sys.executable,
                        os.path.join(RAIZ, "fabrica",
                                     "familia_entre_canais.py"),
                        "epomeno-epipedo"],
                       capture_output=True, text=True, cwd=RAIZ, timeout=300)
    assert r.returncode == 0, r.stderr[-400:]
    assert "FAMILIA ENTRE CANAIS" in r.stdout


def test_o_MOTIVO_e_a_medida_continuam_escritos_no_modulo():
    fonte = inspect.getsource(FC)
    for marca in ("similaridade", "esqueleto_entre_canais", "memoria",
                  "Em\ntodos os canais", "776", "725", "RECENTES_K"):
        assert marca in fonte, (
            "o motivo saiu do modulo (%r): sem ele a rodada seguinte volta a "
            "conferir de cabeca" % marca)
    assert "57 das 163" in fonte, (
        "a medida que FORCA a delegacao do canal saiu do modulo")
