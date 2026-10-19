"""O trilho estava ligado ao render e NADA o alimentava.

As 08:1x de 19/10 o `svg_cena` passou a desenhar `trilho.faixa`. No mesmo passo
ficou visivel que **nenhuma spec de longo do disco declara o campo `trilho`** —
logo o conserto era alcancavel e sem dado. **E a mesma classe do defeito que ele
conserta, uma camada acima:** as 04:2x o codigo nao era chamado; aqui ele e
chamado e nunca recebe nada.

O que este arquivo guarda:

1. **A DERIVACAO, com a regra do separador MEDIDA** — kicker repetido nao e
   capitulo. Medido no `labtreinamento-002`, cujas treze cenas `titulo` sao sete
   capitulos intercalados por seis cenas "Ponte".
2. **A RECUSA.** Varridas as specs de longo da frota, o trilho derivado cabe em
   uma MINORIA — na geracao antiga quase toda cena e `titulo`. Encolher a fonte
   ate caber seria o §3.8 em forma de faixa ilegivel, e por isso ele LEVANTA.
3. **A contraprova no outro sentido:** as duas specs do formato atual que servem
   de origem continuam cabendo. Sem isso o teste passaria recusando tudo.
"""

import glob
import json
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio  # noqa: E402
import fabrica as FB  # noqa: E402
import trilho  # noqa: E402

PAL = {"bg": "#F4EFE6", "ink": "#1B1A17", "c1": "#C8502A", "c2": "#2B6CB0"}


def _longo(pacote):
    with open(os.path.join(RAIZ, "fabrica", "specs", pacote + ".json")) as f:
        return json.load(f)["longo"]


def _especs_de_longo():
    saida = []
    for f in glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json")):
        try:
            sp = json.load(open(f))
        except Exception:
            continue
        longo = sp.get("longo") or []
        if len(longo) >= 20 and sp.get("voz") in ensaio.MODELO_VOZ:
            saida.append((os.path.basename(f), longo))
    return saida


def test_kicker_REPETIDO_nao_e_capitulo():
    """A regra do separador, ancorada no caso real que a produziu."""
    longo = _longo("labtreinamento-002")
    titulos = [(c.get("kicker") or "") for c in longo if c.get("layout") == "titulo"]
    assert titulos.count("Ponte") > 1, (
        "o `labtreinamento-002` perdeu as cenas 'Ponte' — sem elas este arquivo "
        "nao mede a regra do separador e passa por vacuidade."
    )
    caps = trilho.capitulos_do_longo(longo)
    assert "Ponte" not in caps
    assert len(caps) < len(titulos), "nada foi filtrado"
    assert len(set(caps)) == len(caps), "o trilho saiu com capitulo repetido"


def _um_que_cabe():
    """Uma spec do disco cujo trilho derivado CABE — DERIVADA, nunca nomeada.

    Esta funcao substitui a constante `ATUAIS`, que trazia
    `epomeno-epipedo-013` e `labtreinamento-002` cravados. Em 19/10 as 12:3x a
    janela segura do portao `layout` encolheu a largura util de 1709 para 1442
    px e o `-013` deixou de caber — e os quatro testes que o nomeavam
    reprovaram de uma vez. Era identidade onde havia propriedade (743/753/761),
    pela quinta vez.
    """
    for pacote, caps in _especs_que_cabem():
        return pacote, caps
    raise AssertionError(
        "nenhuma spec do disco tem trilho que cabe — o arquivo perdeu a "
        "ancora e passaria por vacuidade em vez de medir"
    )


def _especs_que_cabem():
    saida = []
    for pacote, longo in _especs_de_longo():
        caps = trilho.capitulos_do_longo(longo)
        if caps and trilho.cabe(caps, 1920, 1080):
            # `_especs_de_longo` devolve o nome COM `.json`; o `_longo`
            # acrescenta a extensao. Pego na primeira execucao.
            saida.append((pacote[:-5] if pacote.endswith('.json') else pacote, caps))
    return sorted(saida)


def test_existe_spec_que_CABE_e_spec_que_NAO_cabe():
    """Contraprova nos DOIS sentidos: sem isto, recusar tudo passaria.

    E aceitar tudo tambem — e e por isso que o lado de cima tambem vai cobrado.
    """
    cabem = _especs_que_cabem()
    total = len(_especs_de_longo())
    assert cabem, "nenhuma cabe: `aplica_no_longo` recusaria toda a frota"
    assert len(cabem) < total, (
        f"as {total} specs cabem — a recusa deixou de existir, e esta nota "
        "sobre a janela segura tem de ser relida em vez de reaproveitada"
    )
    for pacote, caps in cabem:
        assert 4 <= len(caps) <= 12, f"{pacote}: {len(caps)} capitulos"


def test_aplica_poe_o_campo_em_TODA_cena():
    longo = _longo(_um_que_cabe()[0])
    n = trilho.aplica_no_longo(longo)
    assert n == len(trilho.capitulos_do_longo(longo))
    assert all("trilho" in c and "trilho_atual" in c for c in longo), (
        "cena sem o campo sairia sem a faixa, e o trilho e PERMANENTE"
    )
    atuais = [c["trilho_atual"] for c in longo]
    assert atuais == sorted(atuais), "o destaque voltou para tras"
    assert atuais[0] == 0 and atuais[-1] == n - 1, "o destaque nao percorreu tudo"


def test_aplica_e_IDEMPOTENTE():
    """Rodar duas vezes nao pode mudar nada — o render pode chamar de novo."""
    longo = _longo(_um_que_cabe()[0])
    trilho.aplica_no_longo(longo)
    antes = [(c["trilho"], c["trilho_atual"]) for c in longo]
    trilho.aplica_no_longo(longo)
    assert [(c["trilho"], c["trilho_atual"]) for c in longo] == antes


def test_o_campo_derivado_CHEGA_ao_SVG():
    """O defeito das 04:2x era desenhar o fundo e esquecer o conteudo."""
    longo = _longo(_um_que_cabe()[0])
    trilho.aplica_no_longo(longo)
    svg = FB.svg_cena(longo[7], PAL, 1920, 1080)
    caps = trilho.capitulos_do_longo(longo)
    assert caps[0] in svg and caps[-1] in svg, "o trilho derivado nao chegou ao SVG"


def test_ele_LEVANTA_em_vez_de_encolher_a_fonte():
    """Trilho que nao cabe e faixa ilegivel — o §3.8 em forma de tipografia."""
    longo = [{"layout": "titulo", "kicker": f"Capitulo numero {i} com nome longo",
              "nar": "x"} for i in range(40)]
    assert not trilho.cabe(trilho.capitulos_do_longo(longo), 1920, 1080)
    with pytest.raises(ValueError, match="NAO cabe"):
        trilho.aplica_no_longo(longo)


def test_ZERO_capitulos_levanta_em_vez_de_faixa_vazia():
    """Ausencia de leitura nao e valor vazio — 739."""
    with pytest.raises(ValueError, match="ZERO capitulos"):
        trilho.aplica_no_longo([{"layout": "item", "kicker": "a", "nar": "x"}])


def test_a_MINORIA_da_frota_cabe_e_isso_vai_MEDIDO():
    """A varredura sai do DISCO, e o numero nao esta cravado no teste.

    O que se cobra e a PROPRIEDADE: a maioria NAO cabe (a geracao antiga poe
    quase toda cena em `titulo`), e ainda assim existe um conjunto que cabe. Se
    um dos dois lados desaparecer, esta nota tem de ser relida — nao o numero
    movido, que e o defeito do 743/753/761.
    """
    specs = _especs_de_longo()
    assert len(specs) >= 50, (
        f"a varredura achou {len(specs)} specs de longo — com poucas este teste "
        "passa por vacuidade, o defeito do 743 em forma de glob."
    )
    cabem = [n for n, L in specs
             if trilho.capitulos_do_longo(L)
             and trilho.cabe(trilho.capitulos_do_longo(L), 1920, 1080)]
    assert cabem, "NENHUMA spec cabe — o instrumento passou a recusar tudo"
    assert len(cabem) < len(specs) / 2, (
        "a maioria passou a caber: a geracao antiga foi reescrita, ou o `cabe` "
        "afrouxou. Releia a nota em vez de mover o numero."
    )


def test_o_MOTIVO_da_recusa_continua_escrito_no_modulo():
    """Conserto sem motivo escrito volta calado."""
    fonte = open(os.path.join(RAIZ, "fabrica", "trilho.py")).read()
    assert "separador" in fonte, "a regra do kicker repetido perdeu o motivo"
    assert "3.8" in fonte, "a razao da recusa (faixa ilegivel) saiu do modulo"
    assert "Ponte" in fonte, "o caso MEDIDO que produziu a regra foi apagado"
