"""A capa tinha `#FFFFFF` cravado, e isso ASSUMIA tinta escura.

MEDIDO EM 19/10/2026. O dono olhou a peca de 5 s publicada e disse que ela "nao
tem nada a ver com o estilo do video de 8 min". Conferido, ele esta certo, e o
numero e MEU: o `video_referencia.py` grava que a referencia tem YAVG mediana
37,3 e ZERO quadros com Y > 180 — e o fundo que a frota usava no
`labtreinamento` tem Y = 244, isto e, ele E um quadro claro pelo limiar que eu
mesmo escrevi.

Ao derivar a paleta nova a `ink` virou CLARA, e a capa saiu **texto quase branco
sobre cartao branco** — ilegivel. Nenhum portao via: o `layout.analisa_thumb`
mede COLISAO e TRANSBORDO e o `visual` amostra o VIDEO; **nenhum mede
CONTRASTE**.

O que este arquivo trava:

  1. a contradicao que originou tudo (o nosso fundo e "quadro claro" pela
     nossa propria regua);
  2. que a paleta nova e DERIVADA da medicao, nao escolhida;
  3. que a capa segue a POLARIDADE da tinta;
  4. e a contraprova de regressao ZERO: toda spec da frota continua com cartao
     branco, byte a byte.
"""
import glob
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "fabrica"))

import fabrica  # noqa: E402
import paleta_referencia as pr  # noqa: E402


def test_o_fundo_ANTIGO_era_quadro_claro_pela_NOSSA_propria_regua():
    """A contradicao que o dono viu, em numero, e com o limiar do nosso modulo."""
    import video_referencia as vr
    assert vr.LUMINANCIA["yavg_max"] < pr.LIMIAR_QUADRO_CLARO, vr.LUMINANCIA
    assert abs(vr.LUMINANCIA["yavg_mediana"] - pr.ALVO_LUMA_FUNDO) < 0.1
    assert pr.e_quadro_claro(pr.PALETA_ANTIGA["bg"]), pr.luma(pr.PALETA_ANTIGA["bg"])
    # e por um fator grande, nao por pouco
    assert pr.luma(pr.PALETA_ANTIGA["bg"]) / pr.ALVO_LUMA_FUNDO > 5


def test_a_paleta_e_a_DO_DONO_e_nao_a_minha_reconstrucao():
    """A fonte e o `motor/config.py` do pipeline dele, tema `noite`.

    Eu havia DERIVADO a paleta da capa comprimida; o dono apontou que o video
    foi produzido no PC dele, e o pacote que ele mesmo mandou traz o tema. Usar
    o arquivo dele e melhor que usar a minha leitura dele.
    """
    assert pr.PALETA["bg"] == pr.CORES_DO_TEMA["bg"] == "#0E1117"
    assert pr.PALETA["ink"] == pr.CORES_DO_TEMA["txt"] == "#EEF1F5"
    assert pr.PALETA["c1"] == pr.CORES_DO_TEMA["acc"] == "#3DDBD9"
    assert pr.TEMA_DO_DONO == "noite"
    # e o fundo dele e MAIS escuro ainda que a mediana dos quadros, porque a
    # mediana inclui painel e texto. As duas medidas sao coerentes.
    assert pr.luma(pr.PALETA["bg"]) < pr.ALVO_LUMA_FUNDO
    assert not pr.e_quadro_claro(pr.PALETA["bg"])


def test_a_MINHA_leitura_da_capa_bateu_com_o_valor_REAL():
    """O que torna a medicao confiavel: ela recuperou o acento sozinha.

    Lendo a capa quantizada eu obtive `#3CE4E4`; o tema declara `#3DDBD9`. A
    diferenca e de quantizacao de JPEG. Falha se a distancia crescer, porque ai
    a minha rota de medicao deixou de valer.
    """
    medido, real = "#3CE4E4", pr.CORES_DO_TEMA["acc"]
    assert medido in pr.CAPA_DOMINANTES
    d = max(abs(int(medido[i:i+2], 16) - int(real.lstrip("#")[i-1:i+1], 16))
            for i in (1, 3, 5))
    assert d <= 12, (medido, real, d)


def test_a_tinta_NOVA_contrasta_com_o_fundo_NOVO():
    """Trocar a polaridade sem conferir contraste reconstroi o defeito."""
    assert pr.luma(pr.PALETA["ink"]) - pr.luma(pr.PALETA["bg"]) > 150


def test_a_caixa_da_capa_segue_a_POLARIDADE_da_tinta():
    assert fabrica._caixa_da_capa(pr.PALETA_ANTIGA) == "#FFFFFF"
    assert fabrica._caixa_da_capa(pr.PALETA) == pr.PALETA["bg"]


def test_REGRESSAO_ZERO_para_as_specs_de_tinta_ESCURA():
    """Sem esta contraprova o conserto mudaria a aparencia de centenas de capas.

    Falha se a varredura ficar vazia — glob que deixa de casar faria o assert
    passar calado, que e o defeito do 743 em forma de glob.
    """
    vistas = 0
    for f in glob.glob(str(RAIZ / "fabrica" / "specs" / "*.json")):
        pal = json.loads(pathlib.Path(f).read_text(encoding="utf-8")).get("paleta") or {}
        if "ink" not in pal or pr.luma(pal["ink"]) >= 128:
            continue
        vistas += 1
        assert fabrica._caixa_da_capa(pal) == "#FFFFFF", (f, pal)
    assert vistas > 300, f"a varredura achou so {vistas} specs de tinta escura"


def test_O_DEFEITO_JA_ESTAVA_NO_AR_em_tres_specs_do_nivel_do_jogo():
    """Achado da contraprova, e ele nao e meu: tres capas ja saiam ilegiveis.

    O `nivel-do-jogo` usa `ink #F2F2F7` sobre `bg #0F1020` — tinta CLARA — e o
    cartao era `#FFFFFF` cravado. Logo a capa daquelas pecas era texto quase
    branco sobre branco, e nenhum portao dizia nada, pelo mesmo motivo: eles
    medem colisao e transbordo, nunca CONTRASTE.

    Isto NAO foi introduzido pela paleta nova — ela so revelou. Varrido antes
    do conserto: 337 specs de tinta escura e TRES de tinta clara, todas desse
    canal.
    """
    claras = []
    for f in sorted(glob.glob(str(RAIZ / "fabrica" / "specs" / "*.json"))):
        pal = json.loads(pathlib.Path(f).read_text(encoding="utf-8")).get("paleta") or {}
        # `pal != pr.PALETA` era IDENTIDADE e caiu no mesmo dia: a PALETA ganhou
        # `red`, `ok`, `panel`, `mut` e `acc` para os layouts de LONGO, e a spec
        # do `s082` guarda so as quatro historicas. A propriedade e "esta spec
        # usa o tema novo", e isso se decide pelas QUATRO chaves que o render do
        # short le. 743/753/761 outra vez.
        historicas = {k: pal.get(k) for k in ("bg", "ink", "c1", "c2")}
        do_tema = {k: pr.PALETA[k] for k in ("bg", "ink", "c1", "c2")}
        if "ink" in pal and pr.luma(pal["ink"]) >= 128 and historicas != do_tema:
            claras.append(pathlib.Path(f).stem)
    assert claras, "a varredura ficou vazia — este teste deixaria de medir"
    # As TRES do `nivel-do-jogo` sao o caso historico e tem de continuar na
    # varredura; cravar que SO elas aparecem era IDENTIDADE, e caiu no dia em
    # que o `kolejny-poziom` recebeu o tema `misterio` (tinta clara tambem).
    # 743/753/761 pela QUINTA vez. A propriedade e: toda spec de tinta clara
    # tem de ser atendida pelo conserto, seja de que canal for.
    historicas = [n for n in claras if n.startswith("nivel-do-jogo")]
    assert len(historicas) >= 3, (
        f"as specs do caso historico sumiram da varredura: {claras}")
    # e o conserto as atende tambem: cartao escuro, contraste alto
    for n in claras:
        pal = json.loads((RAIZ / "fabrica" / "specs" / f"{n}.json").read_text(
            encoding="utf-8"))["paleta"]
        caixa = fabrica._caixa_da_capa(pal)
        assert caixa == pal["bg"]
        assert abs(pr.luma(caixa) - pr.luma(pal["ink"])) > 150


def test_a_capa_NOVA_nao_sai_com_tinta_sobre_cartao_da_MESMA_cor():
    """O defeito literal: texto quase branco sobre branco."""
    svg = fabrica.svg_thumb({"l1": "Nunca viu", "l2": "seu FAP?"}, pr.PALETA)
    caixa = fabrica._caixa_da_capa(pr.PALETA)
    assert caixa in svg and pr.PALETA["ink"] in svg
    assert abs(pr.luma(caixa) - pr.luma(pr.PALETA["ink"])) > 150


def test_a_nota_de_que_isto_NAO_fecha_a_distancia_continua_escrita():
    """Cor nao era nenhuma das tres partes que eu medi em 16/10."""
    fonte = (RAIZ / "fabrica" / "paleta_referencia.py").read_text(encoding="utf-8")
    assert "trilho de capitulos" in fonte
    assert "18,9 s por plano" in fonte
    assert "cinco layouts" in fonte
    assert "NAO conserta" in fonte or "NAO fecha" in fonte


def test_o_MOTIVO_do_conserto_continua_no_codigo():
    """Conserto sem motivo escrito volta calado."""
    fonte = (RAIZ / "fabrica" / "fabrica.py").read_text(encoding="utf-8")
    assert "_caixa_da_capa" in fonte
    assert "CRAVADO" in fonte
    assert "CONTRASTE" in fonte
