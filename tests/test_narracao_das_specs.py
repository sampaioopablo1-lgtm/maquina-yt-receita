"""Erro duro de narracao nao reprova: some da matriz e ninguem ve.

Medido em 18/08/2026. A spec sx-educacao-002 passou nos 698 testes da suite e
mesmo assim o cron NAO a escolheria: `orquestra.proximo` roda os portoes de
`prontidao` por spec e descarta em silencio quem tem falta. Duas cenas tinham
quatro quantidades numa frase — a regra `MAX_NUM_FRASE`, "planilha falada".

O estrago tem a forma que este repositorio ja conhece de outros lugares: nada
fica vermelho. O disparo produz um pacote a menos, e a spec fica no diretorio
parecendo pronta. Se eu nao tivesse rodado `proximo` a mao antes de empurrar,
teria esperado o video de um pacote que nunca entraria na fila.

O teste roda os MESMOS quatro portoes que `orquestra._falhas_baratas` roda, e pela
mesma porta — nao uma reimplementacao deles. Duas armadilhas dessa porta,
porque as duas me custaram tempo hoje:

  * `narracao.analisa` devolve TRES coisas (erros, avisos, todas). Desempacotar
    duas levanta ValueError, e desempacotar so `erros` esconde os avisos.
  * o idioma que ela espera e a BASE ("pt"), nao a tag da spec ("pt-BR").
    `NUMEROS.get("pt-BR")` nao existe, a funcao cai no ramo que so conta
    digito, e um roteiro inteiro por extenso passa com zero numeros contados.
    Uma auditoria minha da suite inteira deu "0 specs com erro" por isso —
    estava certa por acidente, o que e pior do que errada.
"""

from __future__ import annotations

import json
import re
import sys
import types
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, str(RAIZ / "fabrica"))

import narracao  # noqa: E402
import orquestra as O  # noqa: E402

SPECS = [p for p in sorted((RAIZ / "fabrica" / "specs").glob("*.json"))
         if re.search(r"-\d{3}$", p.stem)
         and json.loads(p.read_text(encoding="utf-8")).get("longo")]


# As specs que HOJE nao entram na matriz, e o motivo de cada uma. Ficar de
# fora nao e sempre defeito: setiap-level-003 e -004 sao os 26 e 28 min que eu
# mesmo tirei do escalonamento em 17/08/2026, porque longos de 25 a 28 min
# rendiam 0,30 view/dia contra 91,25 da mediana do nicho. O que nao pode e
# alguem descobrir isso esperando um video que nunca vem.
#
# O inventario tem DOIS tipos de parada, e confundi-los foi um defeito real
# deste teste ate 19/08/2026. "portao" e spec que reprova num portao barato —
# se voltar a passar, tem de sair daqui, e e isso que o assert protege.
# "sem portao" e spec que passa em tudo e mesmo assim nao deve ser disparada,
# por um motivo que portao nenhum enxerga. Exigir falha de portao das duas
# obrigava a inventar defeito para justificar parada legitima.
PARADAS = {
    # Passa nos portoes e continua parada: o canal NAO EXISTE no YouTube
    # (canais.no_youtube = false e config.yt_token_cocina-por-niveles com
    # refresh_token nulo, conferidos em 19/08/2026). Renderizar quinze minutos
    # aqui e renderizar para o vazio. Encurtar o roteiro nao resolveria nada.
    #
    # Ela entrou aqui por outro motivo — "15,0 min, acima do teto" — que a
    # recalibracao de 19/08/2026 dissolveu: com o Dalia medido cena-a-cena
    # (17,20 -> 17,48 chars/s) a spec passou a prever 14,95 min. So que 14,95
    # contra teto de 15,00 e margem de 3 s, menor que o erro tipico do proprio
    # modelo (0,75% de 897 s = 6,7 s). Passar no portao por menos que a barra
    # de erro nao e passar.
    # Virou "portao" em 20/08/2026, sem que a spec mudasse uma linha: a quarta
    # medida de short (resep-naik-level-005, +6,6%) levou MARGEM_SHORT de 3%
    # para 5%, o teto previsto caiu de 43,6 para 42,8 s, e o short desta spec
    # mede 43,0. O motivo PRINCIPAL de ela estar parada continua sendo outro e
    # continua valendo — ver abaixo. O tipo mudou porque agora existe portao
    # que a segura, e o teste cobra que os dois batam.
    "cocina-por-niveles-002": ("portao",
                               "canal nao existe no YouTube (motivo principal, "
                               "que portao nenhum enxerga); alem disso short de "
                               "43,0 s contra teto de 41,8, e longo de 14,95 min "
                               "contra teto de 15,00 — margem menor que o erro "
                               "do proprio modelo"),
    # kolejny-poziom-003 saiu daqui em 18/08/2026: 88 cenas viraram 79
    # (16,6 -> 13,0 min no Marek) e a copy-bilhete virou markdown completo.
    # Os limites de 2026 do roteiro foram reconferidos antes (28.260 /
    # 11.304 / 16.956 zl — Analizy.pl, BDO e PZU batem).
    # labtreinamento-002 saiu daqui em 18/08/2026: encurtada de 92 para 87
    # cenas (15,33 -> 14,49 min) e devolvida a matriz.
    # resep-naik-level-003 saiu em 18/08/2026: encurtada de 86 para 76 cenas
    # (16,20 -> 14,32 min) e devolvida a matriz.
    # As tres abaixo entraram juntas em 20/08/2026, pelo MESMO motivo e sem que
    # nenhuma delas mudasse uma linha: a quarta medida de short
    # (resep-naik-level-005, previsto 37,8 s e real 40,3 s, +6,6%) levou a
    # mediana do erro para +4,8% e MARGEM_SHORT de 3% para 5%. O teto previsto
    # caiu de 43,6 para 42,8 s e elas ficaram do lado de fora por dois decimos.
    #
    # Nenhuma perdeu nada com isso: as TRES ja estao no ar, publicadas antes da
    # margem subir, e o orquestrador descarta pacote com youtube_id de qualquer
    # forma. Elas entram aqui porque o inventario mede spec contra portao, nao
    # contra o banco — e uma spec que sai da matriz sem registro e exatamente o
    # defeito que este teste existe para pegar. Se um dia forem reaproveitadas,
    # o corte e de uma frase no short.
    #
    # Em 20/08/2026, mais tarde no mesmo dia, a QUINTA medida de short
    # (seja-mais-magra-004: previsto 35,8 s, real 38,2 s, +6,7%) levou a
    # MARGEM_SHORT de 5% para 7%, e o teto previsto de 42,8 para 41,8 s. Isso
    # trouxe SEIS specs a mais para ca, nenhuma delas alterada em uma linha.
    #
    # O custo disso e zero e foi conferido no banco, nao suposto: das dez specs
    # que 7% segura, OITO ja estao publicadas — e o orquestrador descarta
    # pacote com youtube_id, entao elas nunca mais entram em matriz nenhuma.
    # Das duas restantes, a do cocina nao tem canal no YouTube e a
    # seviye-seviye-002 tem o titulo ja no ar sob outro pacote (aprendizado 378).
    #
    # Elas ficam listadas aqui, e nao apagadas, porque o inventario mede spec
    # contra PORTAO e nao contra o banco: uma spec que sai da matriz sem
    # registro e exatamente o defeito que este teste existe para pegar. Se
    # alguma for reaproveitada um dia, o corte e de uma frase no short.
    "labtreinamento-003":     ("portao", "short 43,4 s contra teto de 41,8 (MARGEM_SHORT 7%); ja no ar"),
    "seviye-seviye-003":      ("portao", "short 43,4 s contra teto de 41,8 (MARGEM_SHORT 7%); ja no ar"),
    "sx-educacao-002":        ("portao", "short 43,6 s contra teto de 41,8 (MARGEM_SHORT 7%); ja no ar"),
    "labtreinamento-002":     ("portao", "short 42,7 s contra teto de 41,8 (MARGEM_SHORT 7%); ja no ar"),
    "seviye-seviye-002":      ("portao", "short 42,5 s contra teto de 41,8 (MARGEM_SHORT 7%); titulo ja no ar sob outro pacote"),
    "agla-level-004":         ("portao", "short 42,3 s contra teto de 41,8 (MARGEM_SHORT 7%); ja no ar"),
    # (kolejny-poziom-003 tambem estoura o teto de short — 42,0 s — mas o
    # motivo esta escrito junto com o do acento, mais abaixo. Ela chegou a ter
    # DUAS entradas aqui, e como isto e um dicionario a segunda apagava a
    # primeira em silencio: o inventario perdia um motivo registrado, que e
    # exatamente o defeito que ele existe para impedir. Uma spec, uma linha.)
    # As tres abaixo entraram em 20/08/2026 pelo portao NOVO de ortografia, e
    # as tres ja estao no ar. Elas tem narracao sem os acentos que as OUTRAS
    # specs do proprio canal usam — turco e polones sem acento continuam
    # parecendo turco e polones, entao passaram no portao de idioma, no de
    # glifos (ASCII sempre tem fonte) e chegaram ao TTS.
    #
    # O defeito foi descoberto quando EU o cometi na seviye-seviye-004: 72
    # cenas em ASCII num canal cujas outras specs acentuam 12,7% das letras.
    # Corrigi antes de publicar; estas tres nao deu tempo.
    #
    # Nao ha o que consertar nelas — video no ar nao se reescreve — e o
    # orquestrador ja as descarta por terem youtube_id. Ficam listadas porque
    # spec que sai da matriz sem registro e o defeito que este teste pega.
    "kolejny-poziom-003":     ("portao", "narracao sem acento polones (0,0% contra 6,9% do canal) E short de 42,0 s contra o teto; ja no ar"),
    "kolejny-poziom-004":     ("portao", "narracao sem acento polones (0,0% contra 6,9% do canal); ja no ar"),
    "seja-mais-magra-004":    ("portao", "narracao sem acento portugues (0,0% contra 4,0% do canal); ja no ar"),
    # As seis abaixo entraram em 20/08/2026 pelo portao NOVO de capitulos, e as
    # seis ja estao no ar. Elas desenham um capitulo que abre em layout `item`,
    # e `copy_md.capitulos` so trata `titulo` e `broll` como abertura de secao —
    # entao o capitulo some da descricao e ninguem ve. E a mesma classe do
    # aprendizado 311, que era sobre `broll`.
    #
    # Video no ar nao se reescreve, e o orquestrador ja as descarta por terem
    # youtube_id. Ficam listadas porque spec que sai da matriz sem registro e o
    # defeito que este teste existe para pegar.
    "epomeno-epipedo-002":    ("portao", "8 capitulos desenhados, 6 produzidos; ja no ar"),
    "next-level-money-003":   ("portao", "8 capitulos desenhados, 6 produzidos; ja no ar"),
    "seja-mais-magra-002":    ("portao", "8 capitulos desenhados, 7 produzidos; ja no ar"),
    "setiap-level-005":       ("portao", "7 capitulos desenhados, 6 produzidos; ja no ar"),
    "setiap-level-007":       ("portao", "8 capitulos desenhados, 7 produzidos; ja no ar"),
    "seviye-seviye-004":      ("portao", "7 capitulos desenhados, 6 produzidos; ja no ar"),
    # resep-naik-level-004 e a spec que mais entrou e saiu deste inventario, e
    # o vaivem e sobre o teto, nunca sobre ela: nao mudou uma linha desde
    # 18/08/2026, quando foi ao ar (w2XxXYku3wo e TZCrcXzOdQU).
    #
    #   entrou  — teto 43,6 s (MARGEM_SHORT 3%), previsao 41,8
    #   saiu    — recalibracao da Gadis (14,26 chars/s) baixou a previsao
    #   voltou  — teto 41,6 s (MARGEM_SHORT 7,5%), previsao 41,8
    #
    # Sao dois decimos de segundo. Ela volta porque o inventario mede spec
    # contra portao e nao contra o meu bom senso — e uma spec que sai da matriz
    # sem registro e o defeito que este teste pega. Nada produzivel para aqui:
    # os dois videos ja estao no ar e o orquestrador descarta pacote com
    # youtube_id.
    "resep-naik-level-004":   ("portao", "short 41,8 s previstos contra teto de 41,6 (MARGEM_SHORT 7,5%); ja no ar"),
    "setiap-level-003":       ("portao", "26,0 min — desescalonado por medicao em 17/08"),
    "setiap-level-004":       ("portao", "28,1 min — desescalonado por medicao em 17/08"),
    "setiap-level-006":       ("portao", "copy ainda em bilhete"),
}


@pytest.mark.parametrize("spec", SPECS, ids=lambda p: p.stem)
def test_spec_de_producao_ou_entra_na_matriz_ou_esta_no_inventario(spec):
    """O defeito nao e ter spec parada — e ter spec parada que ninguem sabe.

    Uma spec nova que comeca a reprovar cai aqui em vez de sumir calada; uma
    spec parada de proposito fica no inventario acima, com o motivo escrito.
    """
    sp = json.loads(spec.read_text(encoding="utf-8"))
    faltas = O._falhas_baratas(spec.stem, sp)
    if spec.stem in PARADAS:
        tipo, motivo = PARADAS[spec.stem]
        if tipo == "portao":
            assert faltas, (f"{spec.stem} voltou a passar nos portoes — tire do "
                            f"inventario PARADAS, o motivo registrado era: "
                            f"{motivo}")
        else:
            assert not faltas, (
                f"{spec.stem} esta no inventario como parada SEM portao, mas "
                f"reprova em portao barato. Ou o motivo mudou, ou o tipo esta "
                f"errado:\n  " + "\n  ".join(faltas))
        return
    assert not faltas, (f"{spec.stem} sairia da matriz calada:\n  "
                        + "\n  ".join(faltas))


# --- a regra que pegou, explicita ------------------------------------------

def _erros(nar: str, idi: str = "pt") -> list[str]:
    return narracao.analisa({"longo": [{"nar": nar}]}, idi)[0]


def test_quatro_quantidades_numa_frase_e_erro_duro():
    """O caso real: salario nominal e adicional na mesma frase, cada um com
    reais E centavos, dao quatro grupos de numero."""
    erros = _erros("Sao nove mil quatrocentos e vinte e tres reais e trinta "
                   "centavos de salario nominal, mais mil duzentos e sessenta "
                   "e dois reais e catorze centavos de adicional.")
    assert any("planilha falada" in e for e in erros)


def test_a_mesma_conta_quebrada_em_duas_frases_passa():
    """A correcao nao e cortar o numero, e distribuir: um por frase."""
    assert not _erros("O salario nominal e nove mil quatrocentos e vinte e "
                      "tres reais. Em cima dele vem um adicional de atividade "
                      "de mil duzentos e sessenta e dois.")


def test_o_conector_nao_parte_a_quantidade():
    """"quarenta e dois" e UM numero, nao dois — senao qualquer frase com dois
    valores por extenso reprovaria e a regra viraria ruido."""
    assert narracao.conta_numeros("Sao quarenta e dois reais.", "pt") == 1


def test_a_tag_da_spec_nao_serve_como_idioma():
    """O motivo de este arquivo existir com esta forma. Passar "pt-BR" nao
    levanta erro: devolve zero e a regra fica desligada em silencio."""
    frase = ("Sao nove mil reais, mais mil duzentos reais, mais sete mil "
             "reais, mais dez mil reais.")
    assert narracao.conta_numeros(frase, "pt") >= 4
    assert narracao.conta_numeros(frase, "pt-BR") == 0
    assert narracao.idioma_de({"voz": "pt-BR-AntonioNeural"}, None) == "pt"


# --- o elo que faltava ------------------------------------------------------

def test_analisa_devolve_tres_coisas():
    """Desempacotar em duas levanta ValueError na hora de checar uma spec, que
    e exatamente quando ninguem quer descobrir a assinatura."""
    assert len(narracao.analisa({"longo": [{"nar": "Oi."}]}, "pt")) == 3


def test_a_matriz_consulta_os_portoes_mesmo():
    """Se um dia `proximo` parar de chamar `_falhas_baratas`, este arquivo deixa de
    proteger alguma coisa sem que nenhum teste caia."""
    fonte = (RAIZ / "fabrica" / "orquestra.py").read_text(encoding="utf-8")
    corpo = fonte.split("def proximo")[1].split("\ndef ")[0]
    assert "_falhas_baratas(" in corpo, "proximo nao roda mais os portoes por spec"
