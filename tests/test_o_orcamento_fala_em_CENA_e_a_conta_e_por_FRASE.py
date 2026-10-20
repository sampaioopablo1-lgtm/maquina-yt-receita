# -*- coding: utf-8 -*-
"""O orcamento fala em caracteres POR CENA e a conta e por FRASE.

**Medido em 20/10 as 19:4x, escrevendo o `epomeno-epipedo-s078`.** A primeira
versao punha duas frases na cena do CTA e a previsao foi de 42,15 para **43,18**
— FORA do `ALVO_SHORT` — **com a MESMA media de caracteres por cena**. O termo
`P` do `MODELO_VOZ` e silencio por FRASE, nao por cena (11/10), e o
`ensaio.chars_por_cena` DIZ isso no docstring desde aquele dia. A ressalva
**nunca atravessava** para o relato, que e onde o numero e lido: o `_janela`, o
`chars_no_alvo` e a tabela do `contagem_de_cenas` montam cenas de UMA frase.

A forma dos testes segue a disciplina da semana: a varredura sai do DISCO e
reprova por vacuidade, os DOIS lados tem de existir (spec que cumpre a suposicao
e spec que nao cumpre) e o arquivo **falha se o acervo for uniformizado**, a
contagem e o custo sao cobrados como **DELEGADOS** por AST, a ressalva sai nos
**DOIS** ramos, a medida e **RECONFERIDA** contra o disco (753), e o caso que
produziu o achado e reproduzido **sem nomear a spec** — ele se constroi aqui.
"""
import ast
import glob
import json
import os
import statistics
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio  # noqa: E402
import mira    # noqa: E402

PISO_DE_SPECS = 150
FONTE = open(os.path.join(RAIZ, "fabrica", "mira.py"), encoding="utf-8").read()


def _specs():
    saida = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("short"):
            saida.append((os.path.basename(f)[:-5], d))
    assert len(saida) >= PISO_DE_SPECS, (
        "a varredura achou %d specs de short, menos que o piso de %d: o glob"
        " deixou de casar e TODO assert deste arquivo passaria por vacuidade"
        % (len(saida), PISO_DE_SPECS))
    return saida


def test_a_media_de_caracteres_NAO_determina_a_duracao():
    """O caso que produziu o achado, reproduzido sem nomear spec nenhuma.

    Duas cenas com o MESMO numero de caracteres, uma com uma frase e outra com
    duas, tem de dar duracoes DIFERENTES — e a diferenca tem de ser da ordem do
    `P` da voz, nao de arredondamento.
    """
    voz = "el-GR-NestorasNeural"
    assert voz in ensaio.MODELO_VOZ
    uma = [{"nar": "x" * 27 + "."} for _ in range(14)]
    duas = [{"nar": "x" * 13 + ". " + "y" * 12 + "."} for _ in range(14)]
    n_uma = sum(len(c["nar"]) for c in uma)
    n_duas = sum(len(c["nar"]) for c in duas)
    assert abs(n_uma - n_duas) <= 14, (
        "as duas amostras tem contagens de caractere muito diferentes (%d vs"
        " %d): o teste mediria tamanho em vez de frases" % (n_uma, n_duas))
    d_uma = ensaio.duracao_real_prevista(uma, voz, "edge")
    d_duas = ensaio.duracao_real_prevista(duas, voz, "edge")
    assert d_duas > d_uma + 10.0, (
        "catorze cenas com uma frase a mais cada custaram apenas %.2f s a mais:"
        " o termo P por FRASE desapareceu do modelo" % (d_duas - d_uma))


def test_o_custo_das_frases_extra_mede_FRASE_e_nao_TAMANHO():
    """A reconstrucao preserva os caracteres, senao mede as duas coisas.

    A primeira medicao desta rodada devolveu custo NEGATIVO (-0,12 s), que e
    impossivel, porque ela tirava os pontos do texto e mudava o tamanho.
    """
    for nome, d in _specs():
        c = mira.custo_das_frases_extra(d)
        if not c:
            continue
        assert c["custo_s"] >= 0.0, (
            "%s: custo NEGATIVO de %.2f s — frase a mais nao encurta peca, logo"
            " a reconstrucao voltou a mexer no numero de caracteres"
            % (nome, c["custo_s"]))
        if c["frases_extra"] == 0:
            assert c["custo_s"] < 0.5, (
                "%s nao tem frase extra e ainda assim paga %.2f s"
                % (nome, c["custo_s"]))
        else:
            assert c["custo_s"] > 0.2, (
                "%s tem %d frase(s) extra e paga %.2f s: o custo sumiu"
                % (nome, c["frases_extra"], c["custo_s"]))


def test_os_DOIS_lados_existem_e_o_acervo_nao_foi_uniformizado():
    pecas = _specs()
    com, sem = [], []
    for nome, d in pecas:
        c = mira.custo_das_frases_extra(d)
        if not c:
            continue
        (com if c["frases_extra"] else sem).append(nome)
    assert com, (
        "nenhuma spec do disco tem cena de duas frases: o defeito perdeu o"
        " objeto e esta nota tem de ser RELIDA, nao mantida")
    assert sem, (
        "TODA spec do disco tem frase extra: sem o outro lado nao existe o ramo"
        " em que o orcamento esta certo, e a ressalva nunca seria conferida")
    # maioria e o lado que paga, e e isso que torna a ressalva necessaria
    assert len(com) > len(pecas) / 4, (
        "so %d de %d specs pagam frase extra — se isso virar minoria pequena, a"
        " nota se rele" % (len(com), len(pecas)))


def test_a_MEDIDA_e_reconferida_contra_o_disco():
    """753: numero que ninguem reconfere envelhece calado."""
    custos, cenas, multi, n_com = [], 0, 0, 0
    for _, d in _specs():
        c = mira.custo_das_frases_extra(d)
        if not c:
            continue
        cenas += len(c["frases_por_cena"])
        multi += sum(1 for k in c["frases_por_cena"] if k > 1)
        if c["frases_extra"]:
            n_com += 1
            custos.append(c["custo_s"])
    assert custos, "nenhum custo medido"
    med = statistics.median(custos)
    assert abs(n_com - 216) <= 20, (
        "as specs com frase extra foram de 216 para %d: a medida escrita no"
        " modulo precisa ser reconferida" % n_com)
    assert abs(multi - 631) <= 60, (
        "as cenas com mais de uma frase foram de 631 para %d" % multi)
    assert abs(med - 3.53) <= 1.0, (
        "a mediana do custo foi de 3,53 s para %.2f s" % med)
    assert med > (ensaio.ALVO_SHORT[1] - ensaio.ALVO_SHORT[0]), (
        "a mediana do custo (%.2f s) caiu abaixo da largura do `ALVO_SHORT`"
        " (%.2f s): o erro de unidade deixou de valer uma faixa inteira e esta"
        " nota se rele"
        % (med, ensaio.ALVO_SHORT[1] - ensaio.ALVO_SHORT[0]))
    for pedaco in ("216", "631", "3,53", "8,91"):
        assert pedaco in FONTE, (
            "%r saiu do modulo: sem a medida a rodada seguinte nao sabe o"
            " tamanho do erro de unidade" % pedaco)


def test_a_contagem_de_frases_e_DELEGADA_a_quem_ja_sabe():
    """`narracao.frases` sabe que o fim de frase do grego nao e o do portugues.

    Por AST: um `re.split` escrito aqui seria o segundo dono, e foi exatamente
    o que fez a minha primeira medicao divergir da do instrumento em tres specs
    e dezessete cenas.
    """
    arv = ast.parse(FONTE)
    defs = {n.name: n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)}
    assert "frases_por_cena" in defs, "o contador de frases desapareceu"
    corpo = ast.unparse(defs["frases_por_cena"])
    assert "narracao.frases" in corpo or "frases(" in corpo, (
        "`frases_por_cena` deixou de delegar: %r" % corpo)
    for proibido in ("re.split", "split('.')", 'split(".")'):
        assert proibido not in corpo, (
            "%r dentro de `frases_por_cena`: segundo dono do fim de frase"
            % proibido)
    custo = ast.unparse(defs["custo_das_frases_extra"])
    assert "duracao_real_prevista" in custo, (
        "o custo deixou de sair do dono da duracao")
    for proibido in ("MODELO_VOZ[", "1.273", "0.737", "1.419"):
        assert proibido not in custo, (
            "%r dentro do custo: `P` tem UM dono, e e o `ensaio`" % proibido)


def test_a_ressalva_sai_nos_DOIS_ramos_e_tem_UM_dono():
    """Sair so quando ha frase extra faria ela CALAR na peca em que o orcamento
    esta certo — e quem lesse nao saberia que ele SUPOE uma frase por cena.
    E o ramo que cala quando importa, o defeito de 13:2x."""
    arv = ast.parse(FONTE)
    defs = {n.name: n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)}
    assert "_linha_das_frases" in defs, "o dono da ressalva desapareceu"
    chamadas = [ast.unparse(c.func) for c in ast.walk(defs["_linha_do_orcamento"])
                if isinstance(c, ast.Call)]
    assert any("_linha_das_frases" in c for c in chamadas), (
        "o `_linha_do_orcamento` nao chama o dono da ressalva: %r" % (chamadas,))
    for outro in defs:
        if outro == "_linha_das_frases":
            continue
        assert "SUPOE uma frase por cena" not in ast.unparse(defs[outro]), (
            "a ressalva ganhou um segundo dono em `%s`" % outro)

    com = sem = None
    for _, d in _specs():
        c = mira.custo_das_frases_extra(d)
        if not c:
            continue
        if c["frases_extra"] and com is None:
            com = d
        if not c["frases_extra"] and sem is None:
            sem = d
        if com is not None and sem is not None:
            break
    assert com is not None and sem is not None, "faltou um dos dois lados"
    l_com = "\n".join(mira._linha_das_frases(com))
    l_sem = "\n".join(mira._linha_das_frases(sem))
    assert "SUPOE uma frase por cena" in l_com and "SUPOE uma frase por cena" in l_sem
    # e a medida da FROTA nao se repete DENTRO da linha: ela e calculada, e
    # numero calculado reescrito em string e o 753 — a primeira versao desta
    # linha citava "213 de 384 ... 3,45 ... 9,23" e divergiu do docstring
    # corrigido em UMA HORA.
    corpo_linha = ast.unparse(defs["_linha_das_frases"])
    for proibido in ("216", "631", "3,53", "8,91", "213", "614", "3,45", "9,23"):
        assert proibido not in corpo_linha, (
            "%r dentro de `_linha_das_frases`: a medida da frota tem UM dono (o"
            " docstring do `custo_das_frases_extra`, reconferido pelo teste), e"
            " repeti-la aqui e o 753" % proibido)

    assert "ATENCAO" in l_com and "ATENCAO" not in l_sem, (
        "os dois ramos ficaram indistinguiveis: o que paga tem de ser o unico"
        " com ATENCAO")


def test_a_ressalva_CHEGA_ao_relato_e_ele_segue_INFORMANDO():
    """Instrumento que o chamador nao alcanca e a classe dos layouts mortos —
    e o codigo de saida sai do ESTADO, nunca do texto (19/10, 18:1x)."""
    import subprocess
    alvo = None
    for nome, d in _specs():
        c = mira.custo_das_frases_extra(d)
        if c and not c["frases_extra"] and not d.get("longo"):
            alvo = os.path.join(RAIZ, "fabrica", "specs", nome + ".json")
            break
    assert alvo, "nenhuma spec de short solto sem frase extra no disco"
    p = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "mira.py"),
                        alvo], capture_output=True, text=True)
    assert "SUPOE uma frase por cena" in p.stdout, (
        "a ressalva nao chega ao relato de uma spec de verdade")
    assert p.returncode == 0, (
        "a ressalva passou a reprovar: o codigo de saida tem de sair do"
        " veredito do `confere`, e ela so INFORMA")


def test_o_incidente_que_produziu_o_achado_continua_escrito():
    for pedaco in ("43,18", "19:4x", "chars_por_cena", "NAO CHAMAR QUEM JA SABE"):
        assert pedaco.lower() in FONTE.lower(), (
            "%r saiu do modulo: sem o incidente a ressalva parece zelo e nao"
            " medicao" % pedaco)
