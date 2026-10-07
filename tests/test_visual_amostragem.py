"""O portao visual tem de MEDIR o quadro que ele NOMEIA.

O que este arquivo trava, medido em 07/10/2026 no labtreinamento-011 (504,8 s,
12 quadros): `quadros()` extraia com `fps=n/d`, que emite o quadro i em
`i*d/n`, enquanto `conferir()` chamava esse mesmo quadro de `d*(i+0.5)/n`. Meio
passo — vinte e um segundos naquele video.

O preco foi um pacote bom reprovado: o rotulo 357,6 s cai na janela de footage
da cena 40, entao a regra do lower-third foi aplicada a um quadro de 336,6 s,
que e cena de cartao com o texto no centro e a faixa de baixo vazia POR
DESENHO. Medido depois no proprio arquivo entregue: 66,10% de tinta e contraste
246 em 357,6 s; 0,00% em 336,6 s. A cena estava perfeita.

E o lado que nao daria erro nenhum: a sonda do meio da janela e PULADA quando
um rotulo cai dentro dela. Com o desvio, a cena 40 ficou sem nenhuma sonda
dentro do footage e o portao se deu por conferido.

O teste nao renderiza video: ele troca `quadro_em` por um gravador e compara os
instantes PEDIDOS com os instantes NOMEADOS. E a forma mais barata de impedir
que os dois voltem a divergir.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import visual as V  # noqa: E402

D = 504.83
N = 12
QUADRO_FALSO = bytes(V.W * V.H * 3)


def _grava(monkey):
    pedidos = []

    def quadro_em(v, t):
        pedidos.append(t)
        return QUADRO_FALSO

    monkey.setattr(V, "duracao", lambda v: D)
    monkey.setattr(V, "quadro_em", quadro_em)
    return pedidos


def test_os_instantes_pedidos_sao_os_instantes_nomeados(monkeypatch):
    pedidos = _grava(monkeypatch)
    qs, d = V.quadros("x.mp4", N)
    assert d == D
    assert len(qs) == N, "a lista tem de ter um lugar por indice"
    nomeados = [D * (i + 0.5) / N for i in range(N)]
    for i, (pedido, nome) in enumerate(zip(pedidos, nomeados)):
        assert abs(pedido - nome) < 0.001, (
            f"quadro {i}: pedido em {pedido:.1f}s e nomeado {nome:.1f}s")


def test_o_desvio_de_meio_passo_nao_volta(monkeypatch):
    """O valor exato que o bug produzia, como numero, para nao voltar disfarcado."""
    pedidos = _grava(monkeypatch)
    V.quadros("x.mp4", N)
    passe_antigo = [D * i / N for i in range(N)]
    assert abs(pedidos[8] - 357.6) < 0.1, "o quadro 8 saiu do rotulo 357,6 s"
    assert abs(passe_antigo[8] - 336.6) < 0.1
    assert all(abs(p - a) > 20 for p, a in zip(pedidos, passe_antigo)
               if a > 0), "metade dos quadros voltou ao instante do passe antigo"


def test_o_ultimo_quadro_nao_passa_do_fim(monkeypatch):
    """Em video curto o rotulo do ultimo quadro pode cair depois do fim."""
    pedidos = _grava(monkeypatch)
    monkeypatch.setattr(V, "duracao", lambda v: 1.0)
    V.quadros("x.mp4", 4)
    assert all(p <= 0.9 + 1e-9 for p in pedidos), pedidos


def test_busca_que_falha_nao_renumera_os_seguintes(monkeypatch):
    """A posicao na lista e a identidade do instante: falha entra como None."""
    monkeypatch.setattr(V, "duracao", lambda v: D)
    monkeypatch.setattr(
        V, "quadro_em",
        lambda v, t: None if abs(t - D * 2.5 / N) < 0.001 else QUADRO_FALSO)
    qs, _ = V.quadros("x.mp4", N)
    assert len(qs) == N, "a lista encolheu e renumerou todos os seguintes"
    assert qs[2] is None
    assert qs[3] is not None


def test_conferir_sobrevive_a_um_quadro_ausente(monkeypatch):
    monkeypatch.setattr(V, "duracao", lambda v: D)
    monkeypatch.setattr(V, "quadros", lambda v, n=N: ([None] * N, D))
    erros, avisos = V.conferir("x.mp4")
    assert not erros, erros
    assert len(avisos) == N and "nao consegui buscar" in avisos[0]
