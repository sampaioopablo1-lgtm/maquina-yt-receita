"""A frase "conferido short por short" nao e conferencia uniforme — 20/10, 23:4x.

Eu escrevo em TODA copy uma frase da forma *"nenhum dos tres toca os capitulos
38 a 45 — conferido short por short"*. Ela soa como verificacao mecanica, e a
rota mecanica — o capitulo que o irmao DECLARA na prosa da copy dele — esta
em branco para **146 das 248** specs de short solto do disco. Na origem desta
rodada eram **ZERO de tres**, isto e, a frase era inteiramente LEITURA minha.

A forma destes testes segue a disciplina da sessao: a varredura sai do DISCO
com piso contra vacuidade, as ancoras sao DERIVADAS por propriedade (nomear um
pacote seria identidade onde ha propriedade — 743/753/761), os DOIS lados tem
de existir, o `excluir` e cobrado nos dois sentidos, a frase tem UM dono
cobrado por AST, e a trava do 776 tem de continuar escrita.
"""
import ast
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import irmaos_da_origem as IO  # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "irmaos_da_origem.py")
PISO_SPECS = 150


def _shorts_soltos():
    saida = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short"):
            continue
        if not (d.get("copy") or ""):
            continue
        saida.append(d)
    return saida


def _origens_por_lado():
    """Separa as origens em TRES baldes, derivados do disco.

    Nenhum pacote vai nomeado: o que importa e existir origem em que a rota
    mecanica alcanca TODOS, origem em que alcanca NENHUM, e origem MISTA.
    """
    por_origem = {}
    for d in _shorts_soltos():
        o = d.get("longo_existente")
        if o:
            por_origem.setdefault(o, 0)
            por_origem[o] += 1
    mistas, todas_sem, todas_com = [], [], []
    for o, n in por_origem.items():
        if n < 3:
            continue
        irs = IO.irmaos(o)
        com = [i for i in irs if i["capitulos_declarados"]]
        sem = [i for i in irs if not i["capitulos_declarados"]]
        if com and sem:
            mistas.append(o)
        elif sem:
            todas_sem.append(o)
        elif com:
            todas_com.append(o)
    return mistas, todas_sem, todas_com


def test_a_varredura_nao_passa_por_VACUIDADE():
    """Glob que deixa de casar faria todo teste daqui passar sem medir nada."""
    specs = _shorts_soltos()
    assert len(specs) >= PISO_SPECS, (
        "a varredura caiu para %d specs de short solto; abaixo de %d este "
        "arquivo passa por vacuidade, que e o defeito do 743 em forma de glob"
        % (len(specs), PISO_SPECS))


def test_a_rota_mecanica_DEIXOU_de_estar_em_branco_para_a_maioria():
    """RETRATADO em 22/10 as 21:4x, e a propria mensagem antiga mandava reler.

    Este teste cobrava `frac > 0.5` — *"a rota mecanica esta em BRANCO para a
    maioria"* — e dizia, em letra: *"se a maioria passou a declarar, esta nota
    tem de ser RELIDA, nao o numero movido"*. **Ela passou.** O `_citados` so
    lia FAIXA e capitulo UNICO, e so em portugues; com a ENUMERACAO e as outras
    linguas a cobertura foi de **136 para 181 de 181** das copies que citam
    capitulo, e a fracao sem declaracao caiu de mais de metade para **38%**
    (112 de 293).

    **E a causa da brancura era o PARSER, nao os autores** — e e isso que a nota
    antiga atribuia errado. A propriedade que fica e mais forte: **spec sem
    capitulo declarado e spec que nao CITA capitulo nenhum**, e o resto da
    conferencia (a leitura da narracao) segue necessario porque 38% nao citam.
    """
    specs = _shorts_soltos()
    sem = [d for d in specs if not IO._capitulos_declarados(d.get("copy") or "")]
    assert sem, ("TODA spec declara capitulo: ai a rota mecanica alcanca tudo e "
                 "esta nota se rele outra vez")
    frac = len(sem) / float(len(specs))
    assert 0.15 <= frac <= 0.60, (
        "%d de %d specs (%.0f%%) sem capitulo declarado, fora da faixa "
        "OBSERVADA depois do conserto de 21:4x — RELEIA em vez de mover o "
        "numero" % (len(sem), len(specs), 100 * frac))
    # E O QUE DE FATO SUSTENTA A NOTA: quem fica sem declaracao nao CITA.
    citam_sem_declarar = [
        d for d in sem
        if re.search(IO.PALAVRA_CAPITULO + r"\s+\d{1,3}",
                     IO._sem_reserva(d.get("copy") or ""), re.I)]
    assert not citam_sem_declarar, (
        "%d spec(s) CITAM capitulo e seguem sem declaracao: alguma FORMA de "
        "citacao voltou a ficar invisivel, e capitulo declarado saindo como "
        "LIVRE e o defeito de 12/10 as 12:3x"
        % len(citam_sem_declarar))


def test_os_DOIS_lados_existem_no_disco():
    """Sem os dois lados o instrumento nao mede nada: se todo irmao declarasse,
    a frase da copy seria conferencia de fato; se nenhum declarasse, nao haveria
    o que chamar de cobertura parcial."""
    mistas, todas_sem, todas_com = _origens_por_lado()
    assert todas_com, (
        "nenhuma origem do disco tem TODOS os irmaos declarando capitulo — sem "
        "esse lado o ramo 'pode dizer conferido sem ressalva' nunca e exercido")
    assert todas_sem or mistas, (
        "nenhuma origem do disco tem irmao SEM capitulo declarado — o defeito "
        "que este arquivo mede desapareceu, e a nota se rele")


def test_o_irmao_sem_capitulo_NAO_entra_como_sem_sobreposicao():
    """Ausencia de dado nao e ausencia de colisao — e o erro que custou o 761."""
    mistas, todas_sem, _ = _origens_por_lado()
    alvo = (todas_sem or mistas)
    assert alvo, "perdi a ancora: nenhuma origem com irmao de capitulo desconhecido"
    o = alvo[0]
    c = IO.cobertura_dos_capitulos(o, meus=[1, 2, 3])
    assert c["desconhecidos"], "a origem derivada deixou de ter irmao desconhecido"
    for p in c["desconhecidos"]:
        assert p not in c["conhecidos"], (
            "%s esta nos dois baldes: desconhecido contado como conferido" % p)
    assert not any(x["pacote"] in c["desconhecidos"] for x in c["colidem"]), (
        "irmao de capitulo desconhecido apareceu em `colidem` — isso afirmaria "
        "sobreposicao sem dado")


def test_a_fracao_mecanica_bate_com_os_baldes():
    """Duas contas da mesma coisa tem de concordar."""
    mistas, todas_sem, todas_com = _origens_por_lado()
    for o in (mistas[:3] + todas_sem[:2] + todas_com[:2]):
        c = IO.cobertura_dos_capitulos(o)
        assert c["irmaos"] == len(c["conhecidos"]) + len(c["desconhecidos"]), o
        esperado = len(c["conhecidos"]) / float(c["irmaos"])
        assert abs(c["fracao_mecanica"] - esperado) < 1e-9, o
    c = IO.cobertura_dos_capitulos("ORIGEM-QUE-NAO-EXISTE-NO-DISCO")
    assert c["irmaos"] == 0 and c["fracao_mecanica"] == 0.0, (
        "origem sem irmao tem de devolver zero, nunca levantar ZeroDivisionError")


def test_a_SOBREPOSICAO_sai_quando_existe_e_e_cobrada_nos_dois_sentidos():
    """Contraprova nos dois sentidos: funcao que nunca acusa nao mede nada."""
    _, _, todas_com = _origens_por_lado()
    assert todas_com, "perdi a ancora: nenhuma origem com todos declarando"
    o = todas_com[0]
    irs = [i for i in IO.irmaos(o) if i["capitulos_declarados"]]
    caps = irs[0]["capitulos_declarados"]
    com = IO.cobertura_dos_capitulos(o, meus=caps)
    assert any(x["pacote"] == irs[0]["pacote"] for x in com["colidem"]), (
        "pedi os PROPRIOS capitulos de um irmao e a sobreposicao nao saiu")
    # o outro sentido: capitulo que nenhum irmao declara nao pode colidir
    todos = set()
    for i in irs:
        todos |= set(i["capitulos_declarados"])
    livre = max(todos) + 500
    sem = IO.cobertura_dos_capitulos(o, meus=[livre])
    assert not sem["colidem"], (
        "capitulo %d nao e declarado por irmao nenhum e ainda assim colidiu"
        % livre)


def test_o_excluir_e_cobrado_nos_DOIS_sentidos():
    """A spec da rodada ja esta no disco quando eu pergunto, logo sem `excluir`
    ela aparece como irma de si mesma e colide com os PROPRIOS capitulos. E a
    QUINTA vez desta assinatura na fabrica."""
    _, _, todas_com = _origens_por_lado()
    assert todas_com, "perdi a ancora"
    o = todas_com[0]
    irs = [i for i in IO.irmaos(o) if i["capitulos_declarados"]]
    eu = irs[0]
    com_ela = IO.cobertura_dos_capitulos(o, meus=eu["capitulos_declarados"])
    sem_ela = IO.cobertura_dos_capitulos(
        o, meus=eu["capitulos_declarados"], excluir=(eu["pacote"],))
    assert any(x["pacote"] == eu["pacote"] for x in com_ela["colidem"]), (
        "sem `excluir` a peca tinha de aparecer colidindo consigo mesma — e "
        "esse e o defeito que o parametro conserta")
    assert not any(x["pacote"] == eu["pacote"] for x in sem_ela["colidem"]), (
        "`excluir` nao retirou a propria peca de `colidem`")
    assert sem_ela["irmaos"] == com_ela["irmaos"] - 1, (
        "`excluir` tem de tirar UM irmao da contagem, nem zero nem dois")
    # outro sentido: `excluir` que nao casa nao pode filtrar nada
    igual = IO.cobertura_dos_capitulos(
        o, meus=eu["capitulos_declarados"], excluir=("pacote-que-nao-existe",))
    assert igual["irmaos"] == com_ela["irmaos"], (
        "`excluir` de pacote inexistente filtrou alguem")


def test_com_MEUS_vazio_ele_RECUSA_em_vez_de_dizer_nenhuma():
    """Dizer 'nenhuma sobreposicao' com `meus` vazio e afirmar sobre conjunto
    vazio — o verde fabricado do §3.8 na forma mais barata."""
    _, _, todas_com = _origens_por_lado()
    assert todas_com, "perdi a ancora"
    o = todas_com[0]
    L = "\n".join(IO._linha_da_cobertura(o))
    assert "NAO conferida" in L, (
        "com `meus` vazio a linha tem de RECUSAR, do jeito que o `porta1` "
        "recusa janela curta; saiu: %r" % L)
    assert "nenhuma sobreposicao" not in L, (
        "com `meus` vazio ele afirmou 'nenhuma sobreposicao'")
    irs = [i for i in IO.irmaos(o) if i["capitulos_declarados"]]
    todos = set()
    for i in irs:
        todos |= set(i["capitulos_declarados"])
    L2 = "\n".join(IO._linha_da_cobertura(o, meus=[max(todos) + 500]))
    assert "nenhuma sobreposicao" in L2, (
        "com `meus` preenchido e sem colisao ele tem de DIZER que nao ha, "
        "senao recusar sempre passaria por este teste; saiu: %r" % L2)


def _corpo(nome):
    arvore = ast.parse(open(FONTE, encoding="utf-8").read())
    for n in ast.walk(arvore):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return n
    raise AssertionError("funcao %s nao existe no %s" % (nome, FONTE))


def test_a_FRASE_tem_UM_dono_e_o_relato_a_CHAMA():
    """A nota da rota de 13:2x era calculada e descartada pelo relato; aqui a
    linha tem de ter um dono e o chamador tem de alcanca-lo."""
    chamadas = []
    for n in ast.walk(_corpo("relato")):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            chamadas.append(n.func.id)
    assert "_linha_da_cobertura" in chamadas, (
        "o `relato` nao chama `_linha_da_cobertura` — instrumento calculado e "
        "descartado e a classe dos layouts mortos")
    # UM dono: a conta mora so dentro da linha e da propria cobertura
    arvore = ast.parse(open(FONTE, encoding="utf-8").read())
    donos = []
    for n in ast.walk(arvore):
        if not isinstance(n, ast.FunctionDef):
            continue
        for c in ast.walk(n):
            if (isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                    and c.func.id == "cobertura_dos_capitulos"):
                donos.append(n.name)
    assert donos == ["_linha_da_cobertura"], (
        "a cobertura e calculada em %r; ela tem de ter UM dono, senao as duas "
        "contas divergem como divergiram a legenda e a mira" % (donos,))


def test_a_trava_do_776_continua_ESCRITA():
    """Sobreposicao de capitulo e MOTIVO PARA LER, nunca veredito de familia."""
    fonte = open(FONTE, encoding="utf-8").read()
    assert "776" in fonte, "a trava do 776 saiu do modulo"
    doc = ast.get_docstring(_corpo("cobertura_dos_capitulos")) or ""
    assert "776" in doc and "veredito" in doc.lower(), (
        "o docstring da cobertura tem de dizer, em letra, que ela NAO decide "
        "familia — sem isso a rodada seguinte a le como veredito")
    _, _, todas_com = _origens_por_lado()
    o = todas_com[0]
    irs = [i for i in IO.irmaos(o) if i["capitulos_declarados"]]
    L = "\n".join(IO._linha_da_cobertura(o, meus=irs[0]["capitulos_declarados"]))
    assert "MOTIVO PARA LER" in L, (
        "a linha da sobreposicao tem de carregar a trava onde ela e lida, nao "
        "so no docstring; saiu: %r" % L)


def test_a_medida_do_defeito_continua_escrita_no_modulo():
    """Numero medido que ninguem reconfere envelhece calado (753) — e este e o
    numero que torna o achado grave."""
    doc = ast.get_docstring(_corpo("cobertura_dos_capitulos")) or ""
    assert "146" in doc and "248" in doc, (
        "a medida (146 de 248) saiu do docstring; sem ela o modulo nao diz o "
        "tamanho do que ele mede")
