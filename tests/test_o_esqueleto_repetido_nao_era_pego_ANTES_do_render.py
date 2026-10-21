"""Nada antes do render perguntava se a FORMA ja existia — 21/10 as 03:3x.

O primeiro rascunho da `labtreinamento-s097` usava
`titulo-lista-item-barras-item-cta`, que **JA EXISTE** na frota, e eu so peguei
porque listei as formas de seis cenas a mao antes de escrever. O
`antes_do_render` rodava cinco instrumentos e nenhum respondia isso; o portao
`variedade` avisa a partir de SEIS iguais **DENTRO** de um canal, e forma que
atravessa canal ele nao ve — 33 das 34.

E A PERGUNTA E FEITA EM TODA RODADA RECENTE: medido no disco, **35 das 252**
copies de short solto AFIRMAM novidade de esqueleto e **43** citam a forma. O
`esqueleto_entre_canais.relato` ja aceitava o caminho da spec e ja aplicava o
`exceto` da propria peca — ele so **nao era chamado**. SETIMA vez da assinatura
"nao chamar quem ja sabe" nesta familia.
"""
import ast
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import antes_do_render as ADR          # noqa: E402
import esqueleto_entre_canais as EC    # noqa: E402
import variedade as V                  # noqa: E402

FONTE = os.path.join(RAIZ, "fabrica", "antes_do_render.py")


def _shorts_soltos():
    saida = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") or not d.get("short"):
            continue
        saida.append((p, d))
    return saida


def test_a_varredura_nao_passa_por_VACUIDADE():
    assert len(_shorts_soltos()) >= 150, (
        "varredura curta: %d specs de short solto" % len(_shorts_soltos()))


def test_a_pergunta_e_FEITA_em_toda_rodada_e_isso_e_RECONFERIDO():
    """O numero que justifica a entrada: se quase nenhuma copy afirmasse
    novidade, o instrumento nao precisaria estar na passada."""
    com_copy = [d for _, d in _shorts_soltos() if (d.get("copy") or "")]
    afirma = [d for d in com_copy
              if re.search(r"inedit|inédit", d["copy"], re.I)
              and re.search(r"esqueleto|forma", d["copy"], re.I)]
    assert len(com_copy) >= 150, "poucas copies: %d" % len(com_copy)
    assert len(afirma) >= 20, (
        "so %d de %d copies afirmam novidade de esqueleto; abaixo disso a "
        "pergunta nao e de toda rodada e esta nota se rele"
        % (len(afirma), len(com_copy)))


def test_ele_ESTA_na_passada_e_e_CHAMADO_pelo_relato():
    assert "esqueleto_entre_canais" in ADR.INSTRUMENTOS, (
        "o instrumento do esqueleto saiu da passada: %r" % (ADR.INSTRUMENTOS,))
    # e todo nome da constante tem de ser alcancado pelo relato — propriedade,
    # nao identidade (o teste que cravava o CONJUNTO foi retratado em 20/10)
    alvo = _uma_spec()
    r = ADR.relato(alvo)
    assert "ESQUELETO ENTRE CANAIS" in r, (
        "o relato do `antes_do_render` nao carrega a saida do instrumento — "
        "import sem chamada e a classe dos layouts mortos")


def _uma_spec():
    """Uma spec de short solto DERIVADA do disco — nomear uma seria identidade
    onde ha propriedade (743/753/761)."""
    for p, d in _shorts_soltos():
        if d.get("copy"):
            return p
    raise AssertionError("perdi a ancora: nenhuma spec de short solto com copy")


def test_todo_INSTRUMENTO_da_constante_responde_para_uma_spec_real():
    """Propriedade sobre a constante, nao lista minha."""
    alvo = _uma_spec()
    for nome in ADR.INSTRUMENTOS:
        saida = ADR._relato_do_instrumento(nome, alvo)
        assert saida and "AMBIENTE, nao a spec" not in saida, (
            "o instrumento %r nao respondeu para uma spec real: %r"
            % (nome, saida[:120]))


def test_o_exceto_da_PROPRIA_peca_e_aplicado():
    """Sem ele "inedito" nunca pode ser verdade, porque a spec da rodada ja esta
    no disco quando eu pergunto — o defeito que o `exceto` conserta em cinco
    instrumentos da fabrica."""
    # uma peca cujo esqueleto tem UM exemplar no disco: ela mesma
    pecas = EC.varre()
    assert len(pecas) >= 150, "varredura curta no instrumento"
    por_forma = {}
    for x in pecas:
        por_forma.setdefault(x["esqueleto"], []).append(x)
    unicas = [v[0] for v in por_forma.values() if len(v) == 1]
    assert unicas, (
        "perdi a ancora: nenhuma forma do disco tem UM exemplar so")
    alvo = unicas[0]
    caminho = os.path.join(RAIZ, "fabrica", "specs", alvo["arquivo"])
    r = EC.relato(caminho)
    assert "INEDITO" in r.upper(), (
        "a peca que e o UNICO exemplar da propria forma saiu como JA EXISTENTE: "
        "o `exceto` nao foi aplicado. Saiu:\n%s" % r)


def test_o_portao_NAO_cobre_a_dimensao_e_isso_e_medido():
    """Se o `variedade` passasse a ver forma entre canais, a entrada aqui
    perderia a razao e esta nota se releria."""
    q = EC.cegas_para_o_portao()
    # AS CHAVES DO DONO SAO MISTAS, e eu errei isso DUAS vezes seguidas neste
    # mesmo teste: `cegas` e `vistas_por_acidente` sao LISTAS de forma,
    # `atravessam` e `pecas_cegas` sao CONTAGENS. Na primeira versao eu supus
    # uma chave `vistas` que nao existe; na segunda supus que as duas eram
    # inteiros. Nos dois casos era o TESTE errado e nao o modulo — e o
    # discriminador era ler os TIPOS em vez de os supor.
    assert len(q["cegas"]) > 0, (
        "nenhuma forma atravessa canal sem o portao ver — ele cobriu a "
        "dimensao e esta nota tem de ser RELIDA")
    assert len(q["cegas"]) > len(q["vistas_por_acidente"]), (
        "o portao passou a ver a MAIORIA das formas que atravessam canal "
        "(%d vistas por acidente contra %d cegas) — releia a nota"
        % (len(q["vistas_por_acidente"]), len(q["cegas"])))
    assert q["atravessam"] == len(q["cegas"]) + len(q["vistas_por_acidente"]), (
        "as duas listas nao fecham com o total que atravessa canal: "
        "atravessam=%d, cegas=%d, vistas=%d"
        % (q["atravessam"], len(q["cegas"]), len(q["vistas_por_acidente"])))
    assert q["limiar_do_portao"] == V.ESQUELETO_AVISA_EM, (
        "o limiar do relato divergiu do DONO (`variedade.ESQUELETO_AVISA_EM`)")
    # e o limiar sai do DONO, nunca copiado
    assert isinstance(V.ESQUELETO_AVISA_EM, int) and V.ESQUELETO_AVISA_EM >= 2


def test_a_entrada_NAO_virou_portao_e_a_saida_e_sempre_zero():
    """Portao aqui reprovaria o acervo: 271 das 392 pecas vivem em forma que
    atravessa canal."""
    import subprocess
    alvo = _uma_spec()
    r = subprocess.run(
        [sys.executable, os.path.join(RAIZ, "fabrica", "antes_do_render.py"),
         alvo],
        capture_output=True, text=True)
    assert r.returncode == 0, (
        "o `antes_do_render` passou a devolver codigo %d: ele INFORMA e nao "
        "reprova" % r.returncode)
    assert "NAO REPROVA" in r.stdout, (
        "a linha que diz que isto nao reprova saiu da saida")


def test_a_FORMA_que_colidiu_nesta_rodada_segue_existindo_no_disco():
    """O motivo da entrada e um caso REAL, e ele e cobrado por PROPRIEDADE: a
    forma do primeiro rascunho tem de continuar no acervo, senao o arquivo nao
    mede o defeito que o produziu."""
    q = EC.quadro()
    seis = q["formas_por_contagem_de_cena"].get(6, [])
    assert len(seis) >= 5, (
        "o tamanho de seis cenas caiu para %d formas; a colisao deste rascunho "
        "deixa de ser plausivel e a nota se rele" % len(seis))
    assert "titulo-lista-item-barras-item-cta" in seis, (
        "a forma do primeiro rascunho desta rodada saiu do disco — ela e a "
        "evidencia de que a colisao era real, nao hipotetica")


def test_o_motivo_e_a_medida_continuam_escritos():
    fonte = open(FONTE, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    assert "35 das 252" in fonte or "35" in fonte, (
        "a medida que justifica a entrada saiu do modulo")
    for marca in ("variedade", "atravessa canal"):
        assert marca in fonte, (
            "a razao %r saiu do modulo; sem ela a rodada seguinte tira o "
            "instrumento da passada por parecer redundante com o portao"
            % marca)
    # a constante e uma TUPLA de nomes de modulo, e todos importaveis
    for n in ast.walk(arvore):
        if isinstance(n, ast.Assign) and any(
                getattr(t, "id", "") == "INSTRUMENTOS" for t in n.targets):
            assert isinstance(n.value, ast.Tuple), (
                "INSTRUMENTOS deixou de ser tupla literal, e o teste por AST "
                "perde o alvo")
