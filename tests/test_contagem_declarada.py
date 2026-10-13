"""A fonte que declara "cinco casos" e enumera SEIS — e os DOIS falsos positivos
que o meu proprio detector produziu antes de ficar de pe.

O caso real: `labtreinamento-009` (`dsoEo103l1o`) diz no capitulo 35 "depois de
descartar esses CINCO casos" e enumera SEIS nos capitulos 28 a 33 — e em outro
ponto diz "os seis casos", contradizendo-se sozinho. Isso importa porque nenhum
portao nosso barraria "os cinco casos" num short: o `narracao` conta QUANTIDADES
por frase sem conferir se sao verdadeiras, e a regra (g) so tira numero que MUDA.

OS DOIS FALSOS POSITIVOS, os dois meus, os dois na mesma rodada de 13/10:
  1. a primeira versao comparava a declaracao com QUALQUER kicker ordinal, e o
     "Primeiro passo" do 009 fazia a conta dar sete;
  2. a segunda ainda pareava a declaracao "os dois casos" do capitulo 20 do
     `labtreinamento-010` com quatro ordinais NUS dos capitulos 59 a 62 — outra
     lista, outro assunto, cinquenta capitulos de distancia.
Cada teste abaixo trava um deles.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))
import contagem_declarada as CD  # noqa: E402

SPECS = os.path.join(os.path.dirname(__file__), "..", "fabrica", "specs")


def _spec(nome):
    with open(os.path.join(SPECS, nome), encoding="utf-8") as f:
        return json.load(f)


def test_o_conflito_REAL_do_009_e_cinco_contra_SEIS():
    d = CD.divergencias(_spec("labtreinamento-009.json"))
    assert d, "o conflito de 'cinco casos' contra seis tem de aparecer"
    assert all(x["declarado"] == 5 and x["enumerados"] == 6 for x in d), d
    assert all(x["substantivo"] == "caso" for x in d)


def test_o_mesmo_longo_diz_SEIS_em_outro_ponto_e_isso_NAO_e_conflito():
    # "os seis casos" bate com a enumeracao, logo nao pode entrar na lista —
    # a primeira versao do detector acusava este tambem, contra "sete".
    d = CD.divergencias(_spec("labtreinamento-009.json"))
    assert not any(x["declarado"] == 6 for x in d), d


def test_PRIMEIRO_falso_positivo_o_ordinal_de_OUTRO_substantivo_nao_conta():
    # "Primeiro passo" nao entra na contagem de `caso`.
    longo = [{"kicker": "Primeiro passo", "nar": ""},
             {"kicker": "Primeiro caso", "nar": ""},
             {"kicker": "Segundo caso", "nar": ""},
             {"kicker": "Fecha", "nar": "descarte esses dois casos"}]
    assert CD.enumerados(longo, "caso") == 2
    assert CD.divergencias({"longo": longo}) == []


def test_SEGUNDO_falso_positivo_ordinal_nu_LONGE_da_declaracao_nao_conta():
    # O caso do `labtreinamento-010`: declaracao no comeco, checklist no fim.
    longo = [{"kicker": "Confundir custa", "nar": "quem trata os dois casos igual"}]
    longo += [{"kicker": f"Enche {i}", "nar": ""} for i in range(1, 40)]
    longo += [{"kicker": o, "nar": ""} for o in
              ("Primeiro", "Segundo", "Terceiro", "Quarto")]
    assert CD.divergencias({"longo": longo}) == [], (
        "ordinal nu a quarenta capitulos de distancia e OUTRA lista")


def test_ordinal_nu_NAO_CONTA_MAIS__retratado_em_13_10_as_12_4x():
    """ESTE TESTE AFIRMAVA O CONTRARIO, e o contrario estava errado.

    Ele travava o recurso do ordinal NU perto da declaracao. Medido na frota as
    12:4x, esse recurso produziu DOIS falsos positivos no sentido da
    superenumeracao: no `epomeno-epipedo-003` a declaracao "τις δύο στήλες"
    (sao duas, de fato) pareou com `πρώτο/δεύτερο/τρίτο` de OUTRA lista doze
    capitulos adiante, e saiu "2 contra 3". Mesmo acidente no `-011`.

    Um ordinal sem o substantivo nao carrega evidencia de pertencer a lista
    declarada, e proximidade nao supre isso. O custo e perder o estilo
    "Primeiro caso / Segundo / Terceiro"; eu prefiro perder achado a inventar
    achado, e e a mesma regra que justificou os dois consertos de 05:0x.
    """
    longo = [{"kicker": o, "nar": ""} for o in
             ("Primeiro", "Segundo", "Terceiro")]
    longo.append({"kicker": "Fecha", "nar": "descarte esses dois casos"})
    assert CD.divergencias({"longo": longo}) == []


def test_o_10_real_NAO_aparece_mais():
    assert CD.divergencias(_spec("labtreinamento-010.json")) == []


def test_o_UM_conflito_era_SO_PORTUGUES__retratado_em_13_10_as_12_1x():
    """O "1 conflito em 207 specs" que eu reportei as 05:2x era VACUO.

    O vocabulario deste modulo era inteiro em portugues, e as specs do epomeno
    sao gregas e as do kolejny polonesas -- logo "0 conflitos" nelas nao era
    limpo, era ANALFABETO. Achado a mao as 12:1x no `epomeno-epipedo-006`:
    declara `Τέσσερα λάθη` e enumera CINCO.

    Com os tres idiomas sao QUATRO, e a contagem viva esta em
    `tests/test_contagem_declarada_multilingue.py`, que tambem guarda os tres
    falsos positivos que o conserto produziu antes de ficar de pe. Este teste
    fica aqui so para que ninguem releia o 1 como medicao da frota.
    """
    import glob
    culpados = []
    for f in sorted(glob.glob(os.path.join(SPECS, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            if CD.divergencias(json.load(fh)):
                culpados.append(os.path.basename(f))
    assert len(culpados) > 1, (
        "se voltou a UM, o vocabulario de grego e polones saiu do modulo")
    assert "labtreinamento-009.json" in culpados


def test_spec_sem_longo_devolve_vazio_em_vez_de_levantar():
    assert CD.divergencias({"longo": []}) == []
    assert CD.divergencias({}) == []


def test_o_relato_MANDA_omitir_em_vez_de_escolher():
    t = CD.relato(os.path.join(SPECS, "labtreinamento-009.json"))
    assert "CONFLITO" in t
    assert "Omitir e melhor que inventar" in t
