# -*- coding: utf-8 -*-
"""A ORIGEM DE ZERO USOS DO LABTREINAMENTO E DE OUTRO IDIOMA — 18/10 as 04:1x.

O `origens_sem_uso` ganhou o mapa de titulos as 03:1x (o conserto do
"contava ID e nao TITULO"). Na PRIMEIRA vez que ele escolheu pauta depois
disso, no `labtreinamento`, ele devolveu UMA origem: `QiaGg03WSR0`, rank 4
da ordem viva — e o titulo dela, medido na propria playlist de uploads do
canal, e POLONES.

Logo o instrumento esta CERTO e a origem NAO SERVE a este canal: short
pt-BR dela reprovaria a identidade (601) e o conteudo e sobre credito
polones. Sao duas coisas diferentes, e sem a distincao a rodada seguinte
escreve peca de idioma errado por SEGUIR o instrumento — que e o modo de
falha mais caro, porque o instrumento esta verde.

O que este arquivo cobra e a PROPRIEDADE, nao a identidade da peca
(743/753/761): que `origens_sem_uso` NAO filtra idioma, e que isso vai
dito em vez de corrigido em silencio — filtrar idioma dentro dele
esconderia a origem em vez de a nomear, e origem de zero usos escondida
e exatamente a cegueira do 762/771 que ele nasceu para desfazer.
"""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'fabrica'))
import concentracao as C

AQUI = os.path.dirname(__file__)
MOD = os.path.join(AQUI, '..', 'fabrica', 'concentracao.py')

# A ordem VIVA de longos do labtreinamento, medida em 18/10 as 04:1x por
# `yt-dlp --flat-playlist` na playlist UUtv_ewwSmwdi1ZRALW4_azg.
ORDEM = ["FtCtIJPsc_Q", "NNgAQLlpEzg", "Sr6VhvD_aPE", "QiaGg03WSR0",
         "lau1nnOUm1U", "6BeNHqT2okA", "dsoEo103l1o", "bQoujWaY7Hw",
         "ntrMxq89I4o", "4OYBkCHFTV8", "3KtwRYxl7_U", "yrWVyqQtw00",
         "KRUERlNPzDw"]

# Titulos MEDIDOS na mesma leitura. O do rank 4 e polones.
POLONES = "Twoja Pierwsza Rata Jest Nizsza, a Oddajesz Bankowi Wiecej"
TITULOS = {
    "FtCtIJPsc_Q": "PROCV ou PROCX: qual usar no Excel (e quando)",
    "NNgAQLlpEzg": "Vale-Transporte: 6% de Qual Salario?",
    "Sr6VhvD_aPE": "Treinamento Cotado por Turma",
    "QiaGg03WSR0": POLONES,
    "lau1nnOUm1U": "Quantos da Sua Equipe Estao com Treinamento Vencendo",
    "6BeNHqT2okA": "CAT em Doenca Ocupacional",
    "dsoEo103l1o": "FGTS: os 8% do Mes Passado e o Dia 20",
    "bQoujWaY7Hw": "Desconto para Pagar a Vista",
    "ntrMxq89I4o": "Por Hora ou por Projeto?",
    "4OYBkCHFTV8": "INSS do Autonomo: 11% ou 20%?",
    "3KtwRYxl7_U": "FAP 2027",
    "yrWVyqQtw00": "NR-10 Atualizada",
    "KRUERlNPzDw": "[EXCEL] ISO 9001:2026 — Planilha de Transicao",
}


def test_o_instrumento_devolve_a_origem_de_zero_usos():
    """Sem isto o resto do arquivo passaria por vacuidade."""
    livres = C.origens_sem_uso('labtreinamento', ORDEM, None, TITULOS)
    assert livres, (
        "o `origens_sem_uso` nao devolveu origem nenhuma no labtreinamento. "
        "Se o canal passou a usar todas, este arquivo perdeu o caso que "
        "retrata e precisa ser RELIDO, nao ajustado.")


def test_o_instrumento_NAO_filtra_idioma_e_isso_e_a_propriedade():
    """A origem de zero usos pode ser de outro idioma, e ele a devolve."""
    livres = C.origens_sem_uso('labtreinamento', ORDEM, None, TITULOS)
    de_outro_idioma = [o for o in livres
                       if TITULOS.get(o, '').startswith('Twoja')]
    assert de_outro_idioma, (
        "nenhuma origem de titulo polones saiu de `origens_sem_uso`. Se "
        "alguem passou a FILTRAR idioma dentro dele, leia o docstring: "
        "filtrar esconde a origem em vez de a nomear, e origem de zero "
        "usos escondida e a cegueira do 762/771.")


def test_e_ele_NAO_e_cego_para_origem_do_IDIOMA_do_canal():
    """Contraprova no outro sentido: sem ela o teste acima passaria com um
    instrumento que devolvesse QUALQUER COISA, ou so o que e estranho."""
    ordem = ORDEM + ["ZZnovaPTBR1"]
    titulos = dict(TITULOS)
    titulos["ZZnovaPTBR1"] = "Ferias Proporcionais: a Conta do Mes Quebrado"
    livres = C.origens_sem_uso('labtreinamento', ordem, None, titulos)
    assert "ZZnovaPTBR1" in livres, (
        "origem nova de titulo pt-BR e zero usos NAO foi devolvida — o "
        "instrumento deixou de achar justamente o caso que serve ao canal.")


def test_a_origem_de_outro_idioma_nao_e_acusada_de_ser_de_outro_CANAL():
    """Ela E do labtreinamento: aparece na playlist de uploads DELE. Idioma
    errado e canal errado sao coisas distintas, e confundi-las reconstruiria
    o falso positivo de 01:2x."""
    dono = {o: 'labtreinamento' for o in ORDEM}
    fora = C.origem_de_outro_canal('labtreinamento', dono)
    assert 'QiaGg03WSR0' not in fora, (
        "a origem polonesa foi acusada de ser de outro canal. Ela esta na "
        "playlist de uploads do labtreinamento e o dono MEDIDO e ele — o "
        "que esta errado nela e o IDIOMA, nao o dono (725).")


def test_a_nota_do_idioma_fica_escrita_no_modulo():
    """Retratacao sem teste volta. E esta nota e o unico aviso de que
    seguir o instrumento, verde, pode produzir peca de idioma errado."""
    t = open(MOD, encoding='utf-8').read()
    assert re.search(r'idioma', t, re.I), (
        "o `concentracao.py` deixou de falar de IDIOMA. Sem essa nota o "
        "relato de origem de zero usos nao avisa que a origem pode ser de "
        "outro idioma, e a rodada seguinte escreve a peca errada por "
        "seguir um instrumento VERDE.")


def test_o_relato_de_zero_usos_segue_avisando_que_lista_vazia_nao_prova():
    """A playlist UU... OMITE longo publico (medido em 01:2x), logo lista
    vazia nao prova ausencia de origem livre. O aviso e de outra nota e
    tem de sobreviver a esta."""
    t = open(MOD, encoding='utf-8').read()
    assert 'OMITE' in t or 'omite' in t, (
        "o aviso de que a playlist OMITE longo publico saiu do modulo. Sem "
        "ele, `origens_sem_uso` devolvendo [] passa a ser lido como 'nao ha "
        "origem livre', que e a conclusao errada de 01:2x.")
