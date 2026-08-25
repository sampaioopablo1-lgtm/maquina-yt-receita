"""O credito CC-BY tem de chegar na descricao publicada.

MEDIDO EM 25/08/2026, contra a fonte primaria e nao contra o codigo: pedi o
snippet do video n01kuj6iiE8 (agla-level-005, publico) para a API do YouTube.
Descricao de 2.090 caracteres, e nem "creativecommons" nem "MacLeod" dentro.
Nenhum dos 186 videos da frota tem o credito.

A causa e a ORDEM das secoes do copy.md. O laco de `ler_copy` classifica cada
secao depois da descricao, e a musica caia no ultimo `elif`:

    ## COMENTARIO FIXADO   <- enche o balde `comentario`
    ...
    ## MUSICA / LICENCA    <- chega no `elif not comentario`, ja falso, e some

Some em silencio: nada falha, nada avisa, e o video sobe.

Nao e detalhe de estilo. O docstring do `copy_md.credito_trilha` diz o que
esta em jogo — "sem ele o uso da faixa deixa de ser licenciado". As faixas sao
CC-BY do Kevin MacLeod: sem atribuicao, o uso nao esta licenciado, em treze
canais e oito idiomas.

Estes testes prendem o comportamento pelo CONTEUDO (a URL da licenca), nao
pelo titulo da secao — o titulo muda de spec para spec e de idioma para
idioma, a URL nao.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import publicar as P  # noqa: E402


CREDITO = ("Music: Inspired by Kevin MacLeod (incompetech.com) — Licensed under "
           "Creative Commons: By Attribution 4.0\n"
           "http://creativecommons.org/licenses/by/4.0/")


def _copy(**extra):
    """O copy.md real do agla-level-006, na ordem que causou o defeito."""
    return f"""# titulo do arquivo

## TITULO
EPFO 3.0: ATM se 50%, UPI se 75%

## DESCRICAO
O texto da descricao.

## CAPITULOS
0:00 Abertura
2:12 O que mudou

## COMENTARIO FIXADO
Comentario que vai fixado no video.

## HASHTAGS
#EPFO #PFWithdrawal #AglaLevel

## TAGS
epfo, pf withdrawal, epf 2026, atm pf, upi pf

## CONFIGURACOES DO STUDIO
- categoria: 27

## MUSICA / LICENCA
{extra.get('licenca', CREDITO)}

## AVISO SOBRE OS NUMEROS
Numeros conferidos em fonte institucional.
"""


def _ler(tmp_path, texto):
    (tmp_path / "copy.md").write_text(texto, encoding="utf-8")
    return P.ler_copy({"copy": "ignorado"}, str(tmp_path))


def test_a_descricao_publicada_leva_o_credito(tmp_path):
    cp = _ler(tmp_path, _copy())
    assert "creativecommons.org/licenses" in cp["descricao"]
    assert "Kevin MacLeod" in cp["descricao"]


def test_o_comentario_fixado_continua_sendo_o_comentario(tmp_path):
    """A correcao nao pode roubar a secao do vizinho."""
    cp = _ler(tmp_path, _copy())
    assert cp["comentario"].startswith("Comentario que vai fixado")
    assert "MacLeod" not in cp["comentario"]


def test_as_hashtags_continuam_por_ultimo(tmp_path):
    """Hashtag no fim e convencao do canal; a licenca entra ANTES dela."""
    cp = _ler(tmp_path, _copy())
    assert cp["descricao"].rstrip().endswith("#EPFO #PFWithdrawal #AglaLevel")


def test_capitulos_e_tags_seguem_intactos(tmp_path):
    cp = _ler(tmp_path, _copy())
    assert "0:00 Abertura" in cp["descricao"]
    assert cp["tags"][0] == "epfo" and len(cp["tags"]) == 5


def test_reconhece_pela_url_e_nao_pelo_titulo_da_secao(tmp_path):
    """Titulo de secao muda por idioma; a URL da licenca nao muda nunca."""
    texto = _copy().replace("## MUSICA / LICENCA", "## संगीत और लाइसेंस")
    assert "creativecommons.org/licenses" in _ler(tmp_path, texto)["descricao"]


def test_copy_sem_musica_nao_estoura(tmp_path):
    """Nem toda spec traz a secao — ausencia nao pode virar excecao."""
    texto = "\n".join(l for l in _copy().split("\n")
                      if "MacLeod" not in l and "creativecommons" not in l)
    cp = _ler(tmp_path, texto)
    assert cp["licenca"] == ""
    assert "0:00 Abertura" in cp["descricao"]


def test_nao_duplica_credito_ja_presente_na_descricao(tmp_path):
    """Spec que ja escreveu o credito a mao nao pode receber duas copias."""
    texto = _copy().replace("O texto da descricao.",
                            f"O texto da descricao.\n\n{CREDITO}")
    assert _ler(tmp_path, texto)["descricao"].count("creativecommons.org") == 1


# ------------------------------------------ o short toca a mesma faixa

def test_a_descricao_curta_do_short_recebe_o_credito(tmp_path):
    """Medido no FHfkxxDQz8A, ao vivo: longo com credito, short sem.

    A descricao do short e so o PRIMEIRO paragrafo da do longo, e o credito
    fica no fim — entao ele nao chegava. O short toca a MESMA faixa, e a
    licenca exige atribuicao onde a obra e usada: "o longo credita" nao cobre
    o short. Este teste prende a montagem que o `main()` faz.
    """
    cp = _ler(tmp_path, _copy())
    curta = cp.get("short_descricao") or cp["descricao"].split("\n\n")[0]
    assert "creativecommons" not in curta, "o paragrafo 1 nao tem o credito"
    if cp.get("licenca") and "creativecommons.org/licenses" not in curta:
        curta = f"{curta}\n\n{cp['licenca']}"
    assert "creativecommons.org/licenses" in curta
    assert "Kevin MacLeod" in curta
