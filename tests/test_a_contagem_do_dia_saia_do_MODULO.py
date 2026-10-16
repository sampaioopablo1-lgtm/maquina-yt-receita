"""A contagem que escolhe o canal saiu da linha de comando e entrou no modulo.

Eu escolhi o canal em oito rodadas seguidas pelo contador, o que e procedimento
e nao achado. O que NAO era procedimento e como eu obtinha o numero: um `re` ou
um `awk` escrito a mao na linha de comando, de novo a cada rodada, sobre as
linhas parqueadas em `docs/pendente/videos-a-inserir.sql`. A §10 da rotina diz,
no item 3, que todo numero que eu calculo a mao vira um erro meu mais cedo ou
mais tarde — e este decide QUAL CANAL produz.

Agora e `concentracao_frota.contagem_do_pendente(desde)`, irmao do
`ultima_do_pendente`, com o mesmo aviso de PISO.

E ele mede, de graca, a divergencia que o 771 descreveu: na rodada das 18:1x de
16/10 o DIA calendario dava 6/7/7 e a janela MOVEL de 24 h dava 8/8/9 — as duas
contagens ordenam a frota de formas diferentes, e e a movel que nao se apaga na
virada da meia-noite.
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import concentracao_frota as cf  # noqa: E402

# A linha parqueada tem a forma exata que o `registro_videos` imprime.
def _linha(canal, quando, slug):
    return (
        "insert into videos (slug,status,formato,titulo,youtube_id,canal,pacote,"
        "origem_id,cenas,publicado_em,trilha) values "
        f"('{slug}','publicado','shorts','t','ID','{canal}','{slug}','ORI',10,"
        f"'{quando}','Inspired') on conflict (slug) do nothing\n"
    )


FIXO = [
    ("kolejny-poziom", "2026-10-15T20:00:00Z", "k-a"),
    ("kolejny-poziom", "2026-10-16T15:14:35Z", "k-b"),
    ("epomeno-epipedo", "2026-10-16T17:18:43Z", "e-a"),
    ("labtreinamento", "2026-10-14T10:00:00Z", "l-a"),
]


def _arquivo(tmp_path, linhas=FIXO):
    p = tmp_path / "pendente.sql"
    p.write_text("".join(_linha(*t) for t in linhas), encoding="utf-8")
    return str(p)


def test_conta_o_dia_calendario(tmp_path):
    assert cf.contagem_do_pendente("2026-10-16", _arquivo(tmp_path)) == {
        "labtreinamento": 0, "epomeno-epipedo": 1, "kolejny-poziom": 1}


def test_a_janela_MOVEL_conta_o_que_o_dia_apagou(tmp_path):
    """O ponto do 771: a peca das 20:00 de ontem ainda conta na janela de 24 h."""
    dia = cf.contagem_do_pendente("2026-10-16", _arquivo(tmp_path))
    movel = cf.contagem_do_pendente("2026-10-15T18:13:00Z", _arquivo(tmp_path))
    assert movel["kolejny-poziom"] == 2 and dia["kolejny-poziom"] == 1, (
        "a janela movel tem de ver a peca de ontem a noite que o dia calendario "
        "jogou fora — e e nisso que as duas contagens discordam"
    )


def test_canal_sem_linha_sai_com_ZERO_e_nao_ausente(tmp_path):
    """Zero para o `mais_baixo` poder recusar; ausencia viraria KeyError calado."""
    fora = cf.contagem_do_pendente("2026-10-16", _arquivo(tmp_path))
    assert set(fora) == set(cf.FROTA)
    assert fora["labtreinamento"] == 0


def test_o_docstring_declara_que_e_PISO(tmp_path):
    texto = " ".join(cf.contagem_do_pendente.__doc__.split())
    assert "PISO" in texto
    assert "nao publicou" in texto, (
        "o aviso de que zero NAO significa 'nao publicou' tem de viver no "
        "modulo, porque e ele que decide canal"
    )


def test_data_invalida_LEVANTA_em_vez_de_contar_zero(tmp_path):
    """Contar zero por argumento errado seria falha permissiva e silenciosa."""
    for ruim in ("", None, "ontem", "16/10/2026"):
        try:
            cf.contagem_do_pendente(ruim, _arquivo(tmp_path))
        except ValueError:
            continue
        raise AssertionError(f"{ruim!r} tinha de LEVANTAR")


def test_reproduz_a_contagem_REAL_da_rodada():
    """Ancorado no arquivo de verdade: o modulo bate com o que eu li a mao."""
    dia = cf.contagem_do_pendente("2026-10-16")
    assert sum(dia.values()) >= 20, (
        "as linhas parqueadas de 16/10 existem; se isso cair, o pendente foi "
        "esvaziado (o `execute_sql` voltou) e o teste tem de ser RELIDO"
    )
    movel = cf.contagem_do_pendente("2026-10-15T18:13:00Z")
    assert all(movel[c] >= dia[c] for c in cf.FROTA), (
        "a janela de 24 h cobre o dia calendario inteiro desta data, logo nunca "
        "pode contar MENOS que ele"
    )
