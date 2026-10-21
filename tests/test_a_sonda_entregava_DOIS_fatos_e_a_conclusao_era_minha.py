# -*- coding: utf-8 -*-
"""A sonda de retencao entregou dois fatos soltos e a conclusao foi minha.

Medido na PRIMEIRA leitura em producao (run 39560816227). Ela imprimiu
`canal do token: UCf4-ZFoZQWKJotZNdi4Yl7w` e `ZERO linhas` como dois avisos
separados — **e fui eu que liguei os dois**.

Separados, o segundo le como *"a peca e nova demais ou tem poucas views"*, que e
uma hipotese que eu NAO medi. O primeiro explica o segundo INTEIRO:
`ids=channel==MINE` resolve para o canal da credencial, logo pedir um video de
OUTRO canal devolve relatorio vazio **por construcao**.

Esta e a terceira camada da mesma familia nesta sessao: 403, 200-com-linhas e
200-sem-linhas ja eram distinguidos; o que faltava era distinguir **por que** o
vazio veio.
"""
import ast
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ALHEIO = "UCf4-ZFoZQWKJotZNdi4Yl7w"
LAB = "UCtv_ewwSmwdi1ZRALW4_azg"


def _mod(nome):
    spec = importlib.util.spec_from_file_location(
        nome, RAIZ / "fabrica" / ("%s.py" % nome))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CR = _mod("chama_retencao")
VAZIO = {"columnHeaders": [], "rows": []}


def _res(canal, token, confere):
    return {"canal": canal, "canal_do_token": token, "canal_confere": confere,
            "resumo": CR.resumo(VAZIO)}


def test_o_caso_MEDIDO_sai_como_ESPERADO_e_nao_como_ausencia_de_dado():
    texto = CR.relato(_res("labtreinamento", ALHEIO, False))
    assert "ESPERADO" in texto, texto
    assert ALHEIO in texto and LAB in texto, (
        "o relato deixou de NOMEAR os dois canais; sem eles quem le nao sabe "
        "de qual lado esta o erro")
    assert "nao diz NADA sobre a peca" in texto
    assert "nova demais" in texto, (
        "o relato tem de NEGAR explicitamente a hipotese que o vazio sugere — "
        "calar sobre ela a deixa de pe")


def test_canal_CERTO_mantem_a_leitura_antiga(tmp_path):
    """Contraprova no outro sentido: sem ela bastaria dizer 'ESPERADO' sempre.

    Com a credencial do canal certo, o vazio volta a ser ausencia de leitura —
    e ai a hipotese de peca nova ou com poucas views e legitima.
    """
    texto = CR.relato(_res("labtreinamento", LAB, True))
    assert "ESPERADO" not in texto
    assert "ausencia de LEITURA" in texto and "nova demais" in texto


def test_canal_NAO_CONFERIDO_nao_estabelece_nem_a_ausencia():
    """Terceiro estado, e ele nao pode colapsar nos outros dois."""
    texto = CR.relato(_res("labtreinamento", None, None))
    assert "NAO foi conferido" in texto, texto
    assert "nem 'a peca nao tem dado' esta estabelecido" in texto


def test_os_TRES_estados_do_veredito_do_canal():
    assert CR.canal_confere("labtreinamento", ALHEIO) is False
    assert CR.canal_confere("labtreinamento", LAB) is True
    assert CR.canal_confere("labtreinamento", None) is None
    assert CR.canal_confere("canal-fora-do-mapa", LAB) is None, (
        "canal desconhecido virou veredito — inventar aqui e pior que calar")
    assert CR.canal_confere("labtreinamento", "(nao lido: HTTP 403)") is None, (
        "a mensagem de erro do campo foi comparada como se fosse um id")


def test_o_mapa_de_canal_e_DELEGADO_e_nenhum_id_e_cravado_no_codigo():
    """Por AST, e com os dois lados: delega e nao recopia.

    O docstring do modulo CITA o id alheio para contar o incidente; o que o
    teste proibe e id em CODIGO.
    """
    fonte = (RAIZ / "fabrica" / "chama_retencao.py").read_text(encoding="utf-8")
    arvore = ast.parse(fonte)
    assert any(isinstance(n, ast.ImportFrom) and n.module == "medir"
               and any(a.name == "CANAIS" for a in n.names)
               for n in ast.walk(arvore)), "o mapa nao vem do `medir.CANAIS`"
    for no in ast.walk(arvore):
        if isinstance(no, ast.Assign):
            for alvo in no.targets:
                if isinstance(alvo, ast.Name) and alvo.id == "CANAIS":
                    raise AssertionError(
                        "`CANAIS` foi reatribuido no modulo — foi exatamente "
                        "essa COLISAO DE NOME que fez o mapa virar uma str e o "
                        "`.get` levantar na primeira execucao")
        if isinstance(no, ast.Constant) and isinstance(no.value, str):
            if no.value.startswith("UCtv_") or no.value.startswith("UC1hk4"):
                raise AssertionError("id da frota cravado: %r" % no.value)


def test_o_main_AVISA_antes_de_mostrar_metrica():
    """O aviso tem de sair no fluxo, nao so na funcao.

    Instrumento consertado que o chamador nao alcanca e a classe dos layouts
    mortos — ela apareceu tres vezes nesta sessao.
    """
    arvore = ast.parse((RAIZ / "fabrica" / "chama_retencao.py").read_text(
        encoding="utf-8"))
    main = next(n for n in ast.walk(arvore)
                if isinstance(n, ast.FunctionDef) and n.name == "main")
    corpo = ast.unparse(main)
    assert "canal_confere" in corpo, (
        "o `main` nao usa o veredito do canal; ele voltaria a imprimir dois "
        "fatos soltos")
    assert corpo.count("aviso(") >= 2


def test_o_incidente_e_o_motivo_continuam_escritos():
    fonte = (RAIZ / "fabrica" / "chama_retencao.py").read_text(encoding="utf-8")
    # As marcas sao palavras, nao FRASES: o docstring quebra linha e "por
    # construcao" nasce partido. Casar frase longa em fonte com wrap e teste
    # que reprova por formatacao — e a primeira versao desta lista reprovou
    # exatamente assim, com o modulo certo.
    for marca in ("39560816227", "channel==MINE", "construcao", "colidiram"):
        assert marca in fonte, (
            "a procedencia %r saiu do modulo; sem ela a rodada seguinte volta a "
            "ler o vazio como 'sem dado ainda'" % marca)
