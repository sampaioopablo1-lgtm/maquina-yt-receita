"""Descricao acima de 5.000 chars: o YouTube recusa e o pacote fica pela metade.

MEDIDO EM 25/08/2026, na publicacao da kolejny-poziom-011. O short subiu
(W_iFAIQWvi8) e o longo tomou HTTP 400 na abertura do upload resumable: a
descricao tinha 5.369 chars contra o teto de 5.000 do `snippet.description`.

O estrago nao e o 400. E a ORDEM: `publicar.py` sobe o short primeiro, porque
e ele que recebe distribuicao. Entao o teto estourado deixa o canal com um
short no ar apontando para um longo que nao existe, e o registro nunca e
gravado — o que cega as duas travas anti-duplicata para o que acabou de subir.

O `_gate_copy` conferia o TETO do titulo e o PISO da descricao, e nunca o teto
dela. Um render inteiro foi gasto para descobrir na API um limite que e
publico e fixo.

Duas coisas alem do teto, e as duas custaram para descobrir:

  1. O portao trocava {CAPITULOS} por "0:00 abertura", treze chars. O bloco
     real de dez capitulos passa de 300. Medir distancia ate um teto com uma
     substituicao treze vezes menor que a real e nao medir.
  2. O `publicar.py` ainda acrescenta "\\n\\nVersao curta: .../shorts/<id>" na
     descricao do longo DEPOIS de `ler_copy`. Sao ~51 chars que a spec nao
     escreve e que a API conta.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import prontidao as P  # noqa: E402

VOZ = "pl-PL-MarekNeural"

MOLDE = """# arquivo

## TITULO
Titulo curto que passa

## DESCRICAO
{CORPO}

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Comentario fixado do video.

## HASHTAGS
#Um #Dois #Tres

## TAGS
uma, outra, terceira

## MUSICA / LICENCA
{TRILHA}
"""


def _spec(corpo, n_caps=10):
    cenas = []
    for i in range(n_caps):
        cenas.append({"layout": "titulo", "kicker": f"k{i}", "sub": "s",
                      "nar": "Otwarcie rozdzialu numer jeden.", "cap": f"Rozdzial numer {i}"})
        cenas.append({"layout": "item", "kicker": f"i{i}", "preco": "p",
                      "nar": "Podstawa sto tysiecy zlotych i dwanascie procent. " * 15,
                      "sem_cap": True})
    return {"slug": "kolejny-poziom", "pacote": "teste-001", "voz": VOZ,
            "longo": cenas, "copy": MOLDE.replace("{CORPO}", corpo)}


def _falhas_de_descricao(sp):
    return [f for f in P._gate_copy(sp) if "descricao com" in f and "chars" in f]


def test_descricao_no_tamanho_certo_passa():
    assert _falhas_de_descricao(_spec("palavra " * 400)) == []


def test_descricao_acima_do_teto_e_barrada():
    """Era este o buraco: passava aqui e tomava 400 na API, depois do render."""
    faltas = _falhas_de_descricao(_spec("palavra " * 900))
    assert faltas, "descricao gigante nao pode passar no portao"
    assert "5000" in faltas[0]


def test_a_mensagem_diz_quantos_chars_cortar():
    """Sem o numero, quem escreve corta no escuro e volta ao portao."""
    msg = _falhas_de_descricao(_spec("palavra " * 900))[0]
    assert "Corte" in msg and any(c.isdigit() for c in msg.split("Corte")[1])


def test_o_portao_reserva_espaco_para_o_link_do_short():
    """O publicar.py soma ~51 chars DEPOIS do ler_copy; a spec nao os escreve."""
    assert P.MAX_DESCRICAO - P.RESERVA_LINK_SHORT < P.MAX_DESCRICAO
    assert P.RESERVA_LINK_SHORT >= len("\n\nVersao curta: https://youtube.com/shorts/") + 11


def test_capitulos_simulados_tem_o_tamanho_do_bloco_real():
    """Trocar dez capitulos por "0:00 abertura" e medir com a regua errada."""
    sp = _spec("palavra " * 10)
    bloco = P._capitulos_plausiveis(sp)
    assert bloco.count("\n") + 1 == 10, "dez capitulos desenhados, dez no bloco"
    assert len(bloco) > 200, f"bloco de {len(bloco)} chars nao representa dez capitulos"


def test_sem_modelo_de_voz_ainda_estima_a_largura():
    """Voz nao medida nao pode fazer o portao medir com treze chars."""
    sp = _spec("palavra " * 10)
    sp["voz"] = "xx-XX-NaoExisteNeural"
    bloco = P._capitulos_plausiveis(sp)
    assert bloco.count("\n") + 1 == 10
    assert len(bloco) > 200


def test_a_spec_real_passa_depois_do_corte():
    """A kolejny-poziom-011, que motivou o portao, ja corrigida."""
    caminho = os.path.join(RAIZ, "fabrica/specs/kolejny-poziom-011.json")
    if not os.path.exists(caminho):
        return
    sp = json.load(open(caminho, encoding="utf-8"))
    assert _falhas_de_descricao(sp) == []
