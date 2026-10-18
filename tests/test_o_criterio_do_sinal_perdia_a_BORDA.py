"""O criterio de sinal do 770 escrevia `> 1,0` e perdia a BORDA do intervalo.

Medido em 18/10 as 15:2x, no PRIMEIRO ponto que caiu exatamente nela: o
`kolejny-poziom-s061` previa 42,0 no edge (provedor MEDIDO, zero avisos no job
117710246704) e saiu com 43 s reais — residuo nominal +1,0.

A aritmetica, que e toda a razao: o YouTube arredonda PARA CIMA, logo real `R`
significa duracao verdadeira em `(R-1, R]`, e o residuo verdadeiro vive em
`(d-1, d]` com `d = R - prev`. Esse intervalo e ABERTO embaixo, logo ele e todo
estritamente positivo exatamente quando `d - 1 >= 0`, isto e `d >= 1,0` — e NAO
`d > 1,0`. Com `d == 1,0` o intervalo e `(0; 1]`: cada valor dele e positivo.

**Logo o criterio que eu escrevi no 770 era SUFICIENTE e nao necessario**, e
chamava de "nao estabelecido" um ponto cujo sinal esta provado. Nao e limiar
novo nem afrouxamento: e a mesma aritmetica do 770 com a desigualdade certa na
borda do intervalo que ela propria descreve.

**Dois pontos da serie moram nessa borda**, e os dois sao `42,0 -> 43`: o
`kolejny-poziom-s043` (que estava contado como nao estabelecido desde o 770) e o
`-s061` desta rodada. O ramo NEGATIVO nao muda: `(d-1, d]` e todo negativo so
quando `d < 0`, porque com `d == 0` o intervalo e `(-1; 0]` e contem o zero.

E a lição e a mesma classe do 771 — criterio de sinal escrito olhando para um
lado — agora na forma mais fina: **criterio sobre INTERVALO tem de respeitar de
que lado ele esta ABERTO.**
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import duracao_a_medir as dm  # noqa: E402

SERIE = os.path.join(
    os.path.dirname(__file__), "test_residuo_quebra_o_limite_de_dois_segundos.py"
)
LINHA = re.compile(r'^\s*\("([a-z-]+-s\d+)",\s*([\d.]+),\s*(\d+),\s*"(\w+)"\),')


def _pontos():
    saida = []
    for linha in open(SERIE, encoding="utf-8"):
        m = LINHA.match(linha)
        if m:
            saida.append((m.group(1), float(m.group(2)), int(m.group(3))))
    return saida


def test_a_borda_exata_estabelece_o_sinal():
    # 42,0 -> 43: residuo verdadeiro em (0; 1], todo positivo.
    assert dm._sinal(43, 42.0) == 1


def test_logo_abaixo_da_borda_NAO_estabelece():
    # 41,1 -> 42: residuo verdadeiro em (-0,1; +0,9], contem zero.
    assert dm._sinal(42, 41.1) == 0
    assert dm._sinal(42, 41.9) == 0


def test_o_ramo_negativo_NAO_mudou():
    # (d-1, d] e todo negativo so com d < 0; com d == 0 ele contem o zero.
    assert dm._sinal(41, 41.5) == -1
    assert dm._sinal(42, 42.0) == 0


def test_o_criterio_e_exatamente_d_maior_ou_igual_a_um():
    # Contraprova nos dois sentidos, varrendo a vizinhanca da borda.
    for d in (0.98, 0.99, 1.0, 1.01, 1.02):
        esperado = 1 if d >= 1.0 else 0
        assert dm._sinal(round(42.0 + d, 2), 42.0) == esperado, d


def test_os_DOIS_pontos_da_borda_estao_na_serie():
    """Falha se a ancora desaparecer — sem eles este arquivo nao mede nada."""
    borda = [
        (p, pv, r) for p, pv, r in _pontos() if abs((r - pv) - 1.0) < 1e-9
    ]
    assert len(borda) >= 2, (
        f"a serie tem {len(borda)} ponto(s) na borda exata; este arquivo foi "
        "escrito com DOIS (kolejny-poziom-s043 e -s061, os dois 42,0 -> 43) e "
        "perde a ancora sem eles — releia a nota acima em vez de apagar o teste"
    )
    for _, prev, real in borda:
        assert dm._sinal(real, prev) == 1


def test_a_licao_continua_escrita_no_modulo():
    """O conserto sem o MOTIVO escrito volta — e este voltaria calado."""
    fonte = open(dm.__file__, encoding="utf-8").read()
    assert "d >= 1.0" in fonte
    assert "d > 1.0" not in fonte.replace("d >= 1.0", "")
    baixo = fonte.lower()
    assert "aberto" in baixo, "o motivo (o intervalo e ABERTO embaixo) saiu do modulo"
