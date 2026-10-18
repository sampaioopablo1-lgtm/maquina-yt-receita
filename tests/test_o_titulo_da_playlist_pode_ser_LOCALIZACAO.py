# -*- coding: utf-8 -*-
"""O TITULO QUE A PLAYLIST DEVOLVE PODE SER UMA LOCALIZACAO — 18/10 as 06:1x.

A regra que eu escrevi as 04:1x diz: "origem devolvida nao e origem
utilizavel — confira o IDIOMA do titulo antes de escrever". Duas horas
depois ela quase me fez FABRICAR um achado.

O `yt-dlp --flat-playlist` na playlist de uploads do `kolejny-poziom`
devolveu os quatro longos mais recentes com titulo em INGLES ("Renting or
a Mortgage?", "Child Tax Credit", "Real Estate Tax", "PPK: What Your
Contribution Really Costs"). Pela regra de 04:1x isso se le como "o topo
do canal polones esta em idioma errado", e era o que eu ia relatar.

**Era o INSTRUMENTO.** A chamada nao levava locale, e o YouTube serve o
titulo LOCALIZADO. Lidos na pagina com `Accept-Language: pl-PL`, os dois
primeiros sao poloneses:
  GUiq15usizw -> "Wynajem czy Kredyt? Porownaj Czynsz z Odsetkami..."
  kWZW-qV4tQc -> "Ulga na Dziecko: Limit Dochodu Istnieje Tylko przy Jednym..."

E a nota de 04:1x SOBREVIVEU a conferencia, o que e sorte e nao metodo: o
`QiaGg03WSR0` devolve o MESMO titulo polones com `Accept-Language` pt-BR,
pl-PL e en-US, e o `yt-dlp -J` declara `language: pl`. Logo a conclusao
daquela rodada esta certa; o caminho que a produziu nao garantia nada.

A regra que fica: **titulo de playlist nao estabelece idioma.** O
discriminador e o campo `language` do proprio video, ou o
`<meta name="title">` lido em mais de um `Accept-Language` — se ele nao
muda, e o original.
"""
import os, re

AQUI = os.path.dirname(__file__)
CLAUDE = os.path.join(AQUI, '..', 'CLAUDE.md')
MOD = os.path.join(AQUI, '..', 'fabrica', 'concentracao.py')

# Medido em 18/10 as 06:1x. Tres leituras da pagina com locales diferentes.
TITULO_PT = "Twoja Pierwsza Rata Jest Niższa, a Oddajesz Bankowi Więcej"
TITULO_PL = "Twoja Pierwsza Rata Jest Niższa, a Oddajesz Bankowi Więcej"
TITULO_EN = "Twoja Pierwsza Rata Jest Niższa, a Oddajesz Bankowi Więcej"
LANGUAGE_DECLARADO = "pl"

# E o par que mostrou a localizacao, no kolejny-poziom.
FLAT_PLAYLIST = {           # yt-dlp --flat-playlist, SEM locale
    "GUiq15usizw": "Renting or a Mortgage? Compare Rent to Interest",
    "kWZW-qV4tQc": "Child Tax Credit: Income Limit Applies Only to One Child",
}
PAGINA_PL = {               # a mesma peca, Accept-Language: pl-PL
    "GUiq15usizw": "Wynajem czy Kredyt? Porównaj Czynsz z Odsetkami",
    "kWZW-qV4tQc": "Ulga na Dziecko: Limit Dochodu Istnieje Tylko przy Jednym",
}


def test_a_playlist_e_a_pagina_DISCORDAM_na_mesma_peca():
    """Sem isto o resto do arquivo nao retrata nada."""
    for vid in FLAT_PLAYLIST:
        assert FLAT_PLAYLIST[vid] != PAGINA_PL[vid], (
            f"{vid}: a playlist e a pagina devolveram o MESMO titulo. Se a "
            "localizacao deixou de acontecer, esta nota precisa ser RELIDA, "
            "nao apagada — o risco era de metodo, nao daquele dia.")


def test_a_leitura_da_playlist_produziria_a_conclusao_ERRADA():
    """A regra de 04:1x, aplicada ao titulo da playlist, acusa idioma errado
    num canal cujo conteudo esta no idioma certo."""
    palavras_en = ("Renting", "Child", "Real Estate", "Contribution")
    acusadas = [v for v, t in FLAT_PLAYLIST.items()
                if any(p in t for p in palavras_en)]
    assert len(acusadas) == len(FLAT_PLAYLIST), (
        "o teste perdeu o caso: era justamente por parecerem inglesas que "
        "essas origens seriam acusadas.")
    # e a pagina desmente cada uma
    for v in acusadas:
        assert not any(p in PAGINA_PL[v] for p in palavras_en), (
            f"{v}: a pagina tambem veio em ingles, logo a acusacao nao era "
            "falsa e esta nota esta errada.")


def test_o_discriminador_e_o_titulo_NAO_MUDAR_entre_locales():
    """Tres locales, um titulo: e o original. Esta e a propriedade que
    sustenta a conclusao de 04:1x."""
    assert TITULO_PT == TITULO_PL == TITULO_EN, (
        "o titulo do QiaGg03WSR0 mudou com o locale, logo ele TEM "
        "localizacao e a leitura de 04:1x nao estabelecia o idioma dele. "
        "A nota daquela rodada teria de ser retratada.")


def test_e_o_campo_language_concorda_com_o_titulo():
    """Segundo discriminador, independente do primeiro."""
    assert LANGUAGE_DECLARADO == "pl", (
        "o `language` do proprio video deixou de ser pl. Reler a nota de "
        "04:1x antes de usar aquela origem.")


def test_a_nota_de_04_1x_continua_escrita_e_NAO_foi_apagada_por_esta():
    """Esta rodada CONFIRMA aquela nota; nao a substitui. Apagar a de 04:1x
    perderia o achado (origem devolvida nao e origem utilizavel) e deixaria
    so o detalhe de metodo."""
    t = open(CLAUDE, encoding='utf-8').read()
    assert 'QiaGg03WSR0' in t, (
        "a nota da origem de outro idioma saiu do CLAUDE.md. Ela e o achado; "
        "esta rodada so corrigiu o METODO de a verificar.")
    # o documento quebra linha onde quiser: normaliza o espaco antes de casar,
    # senao o teste trava FORMATACAO em vez da propriedade (743/753).
    liso = re.sub(r'\s+', ' ', t)
    assert re.search(r'IDIOMA do t[íi]tulo', liso, re.I), (
        "a regra 'confira o IDIOMA do titulo antes de escrever' saiu do "
        "CLAUDE.md.")


def test_e_a_regra_passou_a_dizer_ONDE_ler_o_idioma():
    """A regra de 04:1x mandava conferir o idioma e NAO dizia onde. Sem o
    'onde', ela manda ler o campo que mente."""
    t = open(CLAUDE, encoding='utf-8').read()
    assert re.search(r'localiza[cç][aã]o', t, re.I), (
        "o CLAUDE.md nao fala de LOCALIZACAO de titulo. Sem essa palavra, a "
        "regra de 04:1x segue mandando conferir idioma no campo que o "
        "YouTube localiza, e o falso positivo de 06:1x volta.")


def test_o_modulo_nao_passou_a_filtrar_idioma_por_causa_disto():
    """A decisao de 04:1x — NAO filtrar idioma dentro do instrumento — fica
    de pe, e com mais razao: o dado de idioma que ele teria a mao e
    justamente o que pode ser localizacao."""
    import ast
    fonte = open(MOD, encoding='utf-8').read()
    arvore = ast.parse(fonte)
    for no in ast.walk(arvore):
        if isinstance(no, ast.FunctionDef) and no.name == 'origens_sem_uso':
            args = [a.arg for a in no.args.args]
            assert not any('idioma' in a for a in args), (
                "`origens_sem_uso` ganhou parametro de idioma. Pelo 762/771 "
                "filtrar ESCONDE a origem em vez de a nomear, e pelo achado "
                "de 06:1x o idioma do titulo pode ser localizacao — logo o "
                "filtro esconderia pelo campo errado.")
            return
    raise AssertionError("`origens_sem_uso` nao existe mais no modulo.")
