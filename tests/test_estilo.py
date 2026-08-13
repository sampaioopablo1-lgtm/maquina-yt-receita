"""A chave de estilo nao pode envelhecer calada.

Ela existe para ir dentro do prompt que rascunha roteiro. Um prompt com numero
copiado a mao continua repetindo o numero antigo depois que o portao mudou — e
ai o modelo escreve para uma regra que nao existe mais, o portao reprova, e
ninguem entende por que. Envelhecer calado e o defeito que mais custou tempo
neste repositorio.

Estes testes trancam a unica propriedade que impede isso: TUDO que a chave
afirma vem importado de quem aplica.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import estilo as E  # noqa: E402
import narracao as N  # noqa: E402
import prontidao as P  # noqa: E402
from copy_md import MAX_CAP, MIN_CAP  # noqa: E402
from ensaio import MODELO_VOZ  # noqa: E402

CANAIS = sorted(p.stem for p in (RAIZ / "config" / "canais").glob("*.yaml"))


@pytest.mark.parametrize("canal", CANAIS)
def test_chave_sai_para_todo_canal(canal):
    texto = E.chave(canal)
    assert texto.startswith(f"CHAVE DE ESTILO — {canal}")
    assert len(texto) > 800, "chave curta demais para guiar um roteiro"


def test_limites_da_narracao_vem_do_narracao_e_nao_de_copia():
    """Se MAX_VIRGULAS mudar, a chave muda junto."""
    texto = E.chave("sx-educacao")
    assert f"no maximo {N.MAX_NUM_FRASE - 1} quantidades" in texto
    assert f"no maximo {N.MAX_PALAVRAS} palavras" in texto
    assert f"no maximo {N.MAX_VIRGULAS - 1} virgulas" in texto


def test_limites_de_duracao_vem_do_prontidao():
    texto = E.chave("sx-educacao")
    assert f"abaixo de {P.PISO_LONGO_S // 60} min" in texto
    assert f"{P.SHORT_MIN_S}-{P.SHORT_MAX_S} s" in texto


def test_limites_de_capitulo_vem_do_copy_md():
    texto = E.chave("sx-educacao")
    assert f"{MIN_CAP} s" in texto and f"{MAX_CAP} s" in texto


def test_slop_e_vago_saem_da_lista_viva():
    """Termos proibidos sao lidos do narracao, entao acrescentar um la basta."""
    texto = E.chave("nivel-do-jogo")
    for termo in N.SLOP["pt"]:
        assert termo in texto
    for termo in N.VAGO["pt"]:
        assert termo in texto


def test_config_do_canal_entra_verbatim():
    """O conhecimento medido de cada canal mora nos comentarios do config.

    Resumir aqui seria criar uma segunda verdade que ninguem atualiza — o
    sx-educacao tem quarenta e cinco linhas de medicao ali dentro.
    """
    cfg = (RAIZ / "config" / "canais" / "sx-educacao.yaml").read_text(encoding="utf-8")
    texto = E.chave("sx-educacao")
    for linha in cfg.strip().splitlines():
        if linha.strip():
            assert linha in texto, f"config perdeu a linha: {linha[:60]}"


@pytest.mark.parametrize("canal", CANAIS)
def test_orcamento_usa_taxa_medida_ou_avisa(canal):
    """Nenhum canal pode receber orcamento de caracteres com modelo chutado.

    Foi assumindo taxa errada que um roteiro de 11,1 min apareceu como 8:30 e
    eu quase reescrevi um texto que estava certo.
    """
    texto = E.chave(canal)
    cfg = (RAIZ / "config" / "canais" / f"{canal}.yaml").read_text(encoding="utf-8")
    voz = E._voz_do_config(cfg)
    if voz in MODELO_VOZ:
        R, P_ = MODELO_VOZ[voz]
        assert f"{R} chars/s de fala + {P_} s por frase" in texto
        assert "SEM MODELO MEDIDO" not in texto
    else:
        assert "SEM MODELO MEDIDO" in texto


def test_orcamento_bate_com_a_spec_que_escrevi_a_mao():
    """A sx-educacao-001 foi escrita a mao e passa nos portoes. O orcamento da
    chave tem que descrever ELA, senao esta descrevendo outro produto."""
    sp = json.loads((RAIZ / "fabrica" / "specs" / "sx-educacao-001.json")
                    .read_text(encoding="utf-8"))
    orc = E.orcamento(sp["voz"])
    real = sum(len(c["nar"]) for c in sp["longo"]) / len(sp["longo"])
    assert abs(real - orc["chars_por_cena"]) < 20, (
        f"chave pede {orc['chars_por_cena']} chars/cena, a spec boa tem {real:.0f}"
    )
    assert E.CENAS_MIN <= len(sp["longo"]) <= E.CENAS_MAX


def test_titulos_anteriores_entram_para_a_regra_de_similaridade():
    texto = E.chave("nivel-do-jogo", ["Lei Felca nos Games", "Inflacao nos Games"])
    assert "Lei Felca nos Games" in texto and "0,65" in texto


def test_canal_inexistente_para_em_vez_de_inventar():
    with pytest.raises(SystemExit):
        E.chave("canal-que-nao-existe")


def test_toda_voz_do_portfolio_tem_taxa_medida():
    """Nenhum canal pode ficar com orcamento de caracteres chutado.

    R vai de 13,10 (hindi) a 25,37 (grego) e P de 0,243 (en-US-Andrew) a 1,376
    (id-ID-Gadis). Voz nova entra com as DUAS amostras medidas — uma de frases
    longas e outra de frases curtas — porque uma amostra so nao separa os
    termos, ela devolve a media dos dois no roteiro que voce usou para medir.
    """
    faltando = []
    for canal in CANAIS:
        cfg = (RAIZ / "config" / "canais" / f"{canal}.yaml").read_text(encoding="utf-8")
        voz = E._voz_do_config(cfg)
        if voz not in MODELO_VOZ:
            faltando.append((canal, voz))
    assert not faltando, f"vozes sem medicao: {faltando}"


def test_a_chave_carrega_o_arco_emocional():
    """Seis portoes conferem se o roteiro esta CERTO. Nenhum pergunta se alguem
    se importa.

    Sem esta secao a chave descreve um produto correto e morto — e um roteiro
    correto e morto passa em tudo. O arco nao vira portao de proposito: emocao
    nao se afere por expressao regular, e um portao burro sobre ela produziria
    reprovacao arbitraria em texto bom.
    """
    texto = E.chave("nivel-do-jogo")
    assert "7. O ARCO" in texto
    for marca in ("A ABERTURA", "MOVIMENTO CENTRAL", "FALE COM ALGUEM",
                  "NOMEIE O CUSTO NA VIDA", "O RITMO", "FECHE DEVOLVENDO CONTROLE"):
        assert marca in texto, f"o arco perdeu: {marca}"


def test_o_arco_ensina_com_frase_do_proprio_acervo():
    """Os exemplos saem das specs deste repositorio, nao de manual de copywriting.

    "Dia vinte e cinco, saldo zero" e a abertura real da setiap-level-004, e a
    frase sobre construir contra sobreviver e da epomeno-epipedo-002. Exemplo
    inventado ensina um estilo que a maquina nao tem.
    """
    texto = E.chave("setiap-level")
    assert "Dia vinte e cinco, saldo zero" in texto
    assert "construir alguma coisa e sobreviver" in texto
    assert "Nao e porque voce e gastador" in texto


@pytest.mark.parametrize("canal", CANAIS)
def test_o_arco_vale_para_todo_canal(canal):
    """O arco nao e de financas: e de como se fala com quem assiste. Vale para
    receita barata e para planilha de Excel igual."""
    assert "7. O ARCO" in E.chave(canal)
