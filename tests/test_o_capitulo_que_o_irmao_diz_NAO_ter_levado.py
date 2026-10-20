# -*- coding: utf-8 -*-
"""O `irmaos_da_origem` contava como DECLARADO o capitulo que o irmao NEGA.

**Medido em 20/10 as 17:4x.** O `_capitulos_declarados` casava `capitulos N a M`
em qualquer lugar da copy, e a geracao antiga escreve, em prosa, um bloco
*"O QUE EU NAO LEVEI, de proposito, e vai escrito para a proxima rodada achar:
as quatro dzwignie que FUNCIONAM (capitulos 52 a 61)"*. O relato saia dizendo
*"capitulos que ele declara: 52 a 61"* — o OPOSTO do que a frase diz.

**E o custo e de PAUTA e nao de relato:** capitulo que o irmao deixou de
proposito aparecia como consumido, e e justamente a reserva que ele escreveu
para a rodada seguinte achar.

A forma destes testes segue a disciplina da semana:
* a varredura sai do DISCO e **reprova por vacuidade**;
* os **DOIS** lados tem de existir, e o arquivo **falha se o acervo for
  uniformizado** nos dois sentidos — ai a nota se rele em vez de ficar;
* o caso do declarado VAZIO e derivado por **PROPRIEDADE**, nunca pelo nome da
  spec: 743/753/761, decima quinta vez;
* os **outros tres** marcadores de negacao continuam FORA, e um teste mede *por
  que* — ali o capitulo citado e a PROCEDENCIA da recusa de um NUMERO, isto e,
  capitulo que a peca LEU, e exclui-lo faria capitulo consumido parecer livre
  (725);
* a medida (15 de 242) e **RECONFERIDA** contra o disco, porque numero que
  ninguem reconfere envelhece calado (753).
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

PISO_DE_SPECS = 150     # vacuidade: glob que deixa de casar faria tudo passar
FONTE = open(os.path.join(RAIZ, "fabrica", "irmaos_da_origem.py"),
             encoding="utf-8").read()


def _shorts_soltos():
    """As specs de short SOLTO com copy — a populacao que o modulo serve.

    Nao e `*.json` inteiro de proposito: foi contar a populacao errada que
    produziu o numero retratado das "66 de 379" (eram PACOTES).
    """
    saida = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo"):
            continue
        copy = d.get("copy") or ""
        if "##" not in copy:
            continue
        saida.append((os.path.basename(f)[:-5], copy))
    assert len(saida) >= PISO_DE_SPECS, (
        "a varredura achou %d specs de short solto com copy, menos que o piso de"
        " %d: o glob deixou de casar e TODO assert deste arquivo passaria por"
        " vacuidade" % (len(saida), PISO_DE_SPECS))
    return saida


def test_o_caso_MEDIDO_sai_do_declarado_e_entra_no_negado():
    """A propriedade, derivada: existe spec cujo declarado FICOU vazio.

    Nomear a `kolejny-poziom-s022` seria identidade onde ha propriedade — o
    acervo muda e a spec pode ganhar outra citacao. O que nao muda e que o
    conserto tem de produzir ao menos um caso em que TODA citacao de capitulo
    mora dentro do bloco de negacao.
    """
    vazias = [(p, c) for p, c in _shorts_soltos()
              if IO.capitulos_negados(c) and not IO._capitulos_declarados(c)]
    assert vazias, (
        "nenhuma spec tem TODA citacao de capitulo dentro do bloco de negacao —"
        " perdi a ancora do defeito, e sem ela este arquivo nao mede o caso que"
        " o produziu (`kolejny-poziom-s022`, 10 de 10)")
    for p, c in vazias:
        negados = IO.capitulos_negados(c)
        assert negados, p
        # e o conjunto negado tem de ser exatamente o que a copy cita
        assert set(negados) == IO._citados(c), (
            "%s: o negado deixou de cobrir todas as citacoes da copy" % p)


def test_o_relato_DIZ_que_o_declarado_ficou_vazio_em_vez_de_calar():
    """Linha que desaparece se le como "ele nao declarou capitulo nenhum".

    Esse e o sentido PERMISSIVO: quem lesse concluiria que a origem esta livre.
    Cobrado no DONO da frase, nao reescrevendo a linha aqui.
    """
    i_vazio = {"capitulos_declarados": [], "capitulos_negados": [52, 61]}
    linha = IO._linha_dos_capitulos(i_vazio)
    assert "NENHUM" in linha, linha
    assert "NAO" in linha.upper(), (
        "a linha do declarado vazio nao diz que a citacao esta dentro do bloco"
        " do que ele NAO levou: %r" % linha)

    i_sem_nada = {"capitulos_declarados": [], "capitulos_negados": []}
    outra = IO._linha_dos_capitulos(i_sem_nada)
    assert outra.strip(), "copy sem citacao nenhuma ficou com linha vazia"
    assert outra != linha, (
        "os dois casos vazios saem com a MESMA frase, logo o relato nao"
        " distingue 'negou tudo' de 'nao citou nada'")

    i_cheio = {"capitulos_declarados": [7, 8, 9], "capitulos_negados": []}
    assert "7 a 9" in IO._linha_dos_capitulos(i_cheio)


def test_contraprova_nos_DOIS_sentidos():
    """Citacao FORA do bloco continua declarada; DENTRO, nao.

    Sem o primeiro ramo bastaria devolver sempre vazio para "consertar".
    """
    fora = ("## FONTES\nCapitulos desta peca: capitulos 12 a 14.\n")
    assert IO._capitulos_declarados(fora) == [12, 13, 14]
    assert IO.capitulos_negados(fora) == []

    dentro = (fora.rstrip("\n")
              + " O QUE EU NAO LEVEI, de proposito: a familia positiva"
                " (capitulos 30 a 32).\n")
    assert IO._capitulos_declarados(dentro) == [12, 13, 14], (
        "a citacao legitima foi perdida junto com a negada")
    assert IO.capitulos_negados(dentro) == [30, 31, 32]


def test_a_negacao_mora_uma_LINHA_acima_e_o_bloco_e_o_PARAGRAFO():
    """Por LINHA o detector achou UM caso; e por isso que o bloco e o paragrafo.

    E ele termina no paragrafo: citacao do paragrafo SEGUINTE volta a contar,
    senao um marcador contaminaria a copy inteira.
    """
    copy = ("## FONTES\nO QUE EU NAO LEVEI, de proposito, e vai escrito para a\n"
            "proxima rodada achar: as quatro alavancas que funcionam\n"
            "(capitulos 52 a 54).\n"
            "\n"
            "Capitulos desta peca: capitulos 70 a 72.\n")
    assert IO.capitulos_negados(copy) == [52, 53, 54], (
        "a citacao na linha ABAIXO do marcador nao foi atribuida ao bloco")
    assert IO._capitulos_declarados(copy) == [70, 71, 72], (
        "o bloco de negacao vazou para o paragrafo seguinte e engoliu a"
        " citacao legitima")


def test_os_OUTROS_marcadores_ficam_de_FORA_e_o_motivo_e_medido():
    """`ficaram FORA` cita o capitulo que a peca LEU — excluir faria o inverso.

    O `kolejny-poziom-s074` cita os capitulos 9 e 12 dentro de um
    *"ficaram FORA pela regra (g)"* para dizer por que o NUMERO deles nao
    entrou. Derivado por propriedade: existe spec com citacao dentro de um
    desses blocos, e ela continua DECLARADA.
    """
    marc = re.compile(r"(?i)\*{0,2}(?:ficaram?\s+fora|ficou\s+fora|DESCARTAD)")
    achou = []
    for p, c in _shorts_soltos():
        decl = set(IO._capitulos_declarados(c))
        if not decl:
            continue
        for m in marc.finditer(c):
            resto = c[m.end():]
            fim = re.search(r"\n\s*\n|\n##\s", resto)
            b = m.end() + (fim.start() if fim else len(resto))
            if IO._citados(c[m.start():b]) & decl:
                achou.append(p)
                break
    assert achou, (
        "nenhuma spec cita capitulo dentro de um bloco de numero DESCARTADO —"
        " perdi a ancora do motivo pelo qual esses marcadores ficam de fora")
    arv = ast.parse(FONTE)
    marcas = None
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and any(
                getattr(t, "id", "") == "MARCAS_DE_NEGACAO" for t in n.targets):
            marcas = ast.literal_eval(n.value)
    assert marcas == ("O QUE EU NAO LEVEI",), (
        "`MARCAS_DE_NEGACAO` mudou para %r. Marcador novo so entra com a medida"
        " ao lado: `ficaram FORA` e `DESCARTADO` citam capitulo que a peca LEU,"
        " e exclui-los faria capitulo CONSUMIDO parecer livre, cegando a regra"
        " (f)" % (marcas,))


def test_o_acervo_AINDA_tem_bloco_de_negacao():
    """Se o marcador sair do acervo, este arquivo passa por vacuidade.

    E ele falha nos DOIS sentidos: se NINGUEM negar, nao ha defeito a medir; se
    TODOS negarem, a nota se rele em vez de o numero ser movido.
    """
    pecas = _shorts_soltos()
    com = [p for p, c in pecas if IO.capitulos_negados(c)]
    assert com, (
        "nenhuma spec do disco tem capitulo negado: o marcador saiu do acervo e"
        " todo assert deste arquivo deixou de medir o defeito")
    assert len(com) < len(pecas) / 2, (
        "%d de %d specs negam capitulo — a negacao deixou de ser a minoria que"
        " a nota descreve, e ela tem de ser RELIDA" % (len(com), len(pecas)))


def test_a_MEDIDA_de_15_de_242_e_reconferida_contra_o_disco():
    """Numero que ninguem reconfere envelhece calado (753).

    A conta e a do defeito: quantas specs tinham capitulo negado contado como
    declarado ANTES do conserto — isto e, quantas tem negado nao-vazio.
    """
    pecas = _shorts_soltos()
    com = [p for p, c in pecas if IO.capitulos_negados(c)]
    assert abs(len(pecas) - 242) <= 25, (
        "a populacao foi de 242 para %d specs: a medida do modulo precisa ser"
        " reconferida" % len(pecas))
    assert abs(len(com) - 15) <= 5, (
        "as specs com capitulo negado foram de 15 para %d: a medida escrita no"
        " modulo envelheceu" % len(com))
    assert "15 de 242" in FONTE, (
        "a medida saiu do modulo — sem ela a rodada seguinte nao sabe o tamanho"
        " do defeito")


def test_o_scanner_de_citacao_tem_UM_dono():
    """A regex do capitulo mora em `_citados` e em lugar nenhum mais.

    Por AST: o modulo CITA `capitulos 52 a 61` na prosa que explica o defeito, e
    casar prosa pegaria a explicacao em vez do codigo. Dois donos da mesma regra
    com um atualizado e a assinatura que congelou a legenda.
    """
    arv = ast.parse(FONTE)
    donos = []
    for n in ast.walk(arv):
        if not isinstance(n, ast.FunctionDef):
            continue
        corpo = ast.unparse(n)
        if "capitulos?" in corpo or "[Cc]apitulo" in corpo:
            donos.append(n.name)
    assert donos == ["_citados"], (
        "a regex de capitulo aparece em %r: ela tem de ter UM dono" % (donos,))

    # e as duas portas publicas delegam a ele
    defs = {n.name: n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)}
    for nome in ("capitulos_negados", "_capitulos_declarados"):
        chamadas = [ast.unparse(c.func) for c in ast.walk(defs[nome])
                    if isinstance(c, ast.Call)]
        assert any("_citados" in c for c in chamadas), (
            "`%s` deixou de delegar a `_citados`: %r" % (nome, chamadas))


def test_a_linha_do_relato_tem_UM_dono_e_o_relato_a_CHAMA():
    """Instrumento consertado que o chamador nao alcanca e a classe dos mortos.

    Foi assim que o `relato` prometeu a prosa e nunca a imprimiu (15:3x) e que
    o `contagem_de_cenas` jogou fora o proprio quadro (03:2x).
    """
    arv = ast.parse(FONTE)
    defs = {n.name: n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)}
    assert "_linha_dos_capitulos" in defs, "o dono da frase desapareceu"
    chamadas = [ast.unparse(c.func) for c in ast.walk(defs["relato"])
                if isinstance(c, ast.Call)]
    assert any("_linha_dos_capitulos" in c for c in chamadas), (
        "o `relato` nao chama o dono da linha dos capitulos: %r" % (chamadas,))
    corpo_relato = ast.unparse(defs["relato"])
    assert "capitulos que ele declara" not in corpo_relato, (
        "a frase do declarado voltou a ser escrita DENTRO do relato: segundo"
        " dono")
    assert "capitulos_negados" in corpo_relato, (
        "o relato deixou de NOMEAR o negado — filtrar em silencio e a cegueira"
        " que o `origens_sem_uso` existe para desfazer")


def test_o_relato_NOMEIA_o_negado_numa_origem_de_VERDADE():
    """A prova sai do disco, nao de uma copy que eu escrevi para passar."""
    alvo = None
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if d.get("longo") or not d.get("longo_existente"):
            continue
        if IO.capitulos_negados(d.get("copy") or ""):
            alvo = d["longo_existente"]
            break
    assert alvo, "nenhuma origem do disco tem irmao com capitulo negado"
    r = IO.relato(alvo)
    assert "NAO ter levado" in r, (
        "o relato de uma origem com irmao que nega capitulo nao nomeia a"
        " reserva dele")
    assert "RESERVA" in r


def test_os_TRES_detectores_errados_continuam_escritos():
    """Sem eles a rodada seguinte reescreve um dos tres.

    E o terceiro e o 17/10: exigindo o marcador em NEGRITO eu achei ZERO e
    quase relatei que o defeito nao existia depois de o ter visto na peca.
    """
    for pedaco in ("por LINHA", "PARAGRAFO", "negrito", "ZERO", "37"):
        assert pedaco in FONTE, (
            "%r saiu do modulo: a historia dos detectores errados e o que"
            " impede a repeticao" % pedaco)
    assert "PONTO CEGO" in FONTE, (
        "o ponto cego da prosa saiu do modulo — sem ele a nota promete cobertura"
        " que o marcador nao tem")


def test_o_numero_RETRATADO_nao_volta_como_fato():
    """As "66 de 379" eram PACOTES, e a frase ficou no `_narracao` depois de
    retratada no docstring do modulo — o 753 em forma de docstring."""
    doc = IO._narracao.__doc__ or ""
    assert "66" not in doc or "RETRATA" in doc.upper(), (
        "o docstring do `_narracao` voltou a afirmar o numero retratado: %r"
        % doc)
    assert "242" in doc, (
        "o docstring do `_narracao` nao carrega a populacao CERTA")
