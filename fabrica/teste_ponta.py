#!/usr/bin/env python3
"""Gera a spec de um short de TESTE, curto, para exercitar o pipeline inteiro.

POR QUE ISTO EXISTE (12/10/2026). O dono pediu "teste de ponta a ponta de um
short de 3 segundos". Duas coisas tornam isso impossivel pelo caminho normal, e
nenhuma delas e burocracia:

  1. o portao `duracao` recusa short abaixo de 30 s. Isso e desenho, nao
     obstaculo: peca curta demais nao recebe distribuicao e, pior, um video de
     tres segundos num canal que esta tentando passar pelo portao de conteudo
     INAUTENTICO do YPP e exatamente o tipo de peca que esse portao existe para
     barrar. **Baixar o limiar para caber o teste seria usar o teste para
     justificar afrouxar producao**, que e o inverso do que portao serve;
  2. a spec viveria em `fabrica/specs/`, que a suite inteira varre — uma spec
     de teste ali somaria falhas a linha de base e sujaria a contagem que a
     rotina usa para saber se alguem quebrou alguma coisa.

Entao este modulo gera a spec FORA do repositorio, em caminho passado por
argumento, e o teste roda ate o render e PARA antes de publicar. O que ele
prova: roteiro, narracao, SVG, camadas, motion, legenda queimada, montagem,
copy e os portoes de imagem. O que ele NAO prova e o upload — e esse ja foi
provado em producao no run 38175747708 (`epomeno-epipedo-s016` = 6TNDVugoz5I).

A spec herda paleta e voz de uma spec real do canal para que o teste exercite
a MESMA tipografia e o MESMO motor de voz da producao. O texto e proprio e
declara que e teste, para que nenhum trecho dele possa ser confundido com
roteiro aproveitavel.
"""

from __future__ import annotations

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Herda de uma spec real: paleta, voz e idioma sao os da producao, porque um
# teste com fonte e voz diferentes nao testaria o que vai ao ar.
MOLDE = "fabrica/specs/epomeno-epipedo-s016.json"

# Uma frase por cena, curta — a mesma regra do esqueleto de producao (a
# sobrecarga por cena e P + 0,300, e P e por VOZ e por FRASE).
CENAS = [
    {"layout": "titulo", "kicker": "Teste", "sub": "da linha de montagem",
     "nar": "Teste da linha de montagem.", "sem_cap": True},
]


def monta(destino: str) -> dict:
    molde = json.load(open(os.path.join(RAIZ, MOLDE)))
    sp = {
        "slug": "_teste-ponta-a-ponta",
        "pacote": "_teste-ponta-a-ponta",
        "idioma": molde.get("idioma"),
        "voz": molde.get("voz"),
        "paleta": molde.get("paleta"),
        "thumb": molde.get("thumb"),
        "trilha": molde.get("trilha"),
        # `longo: []` e o que marca SO_SHORT em etapas.py.
        "longo": [],
        "short": CENAS,
        # Sem `longo_existente`: o teste NAO consome origem de pauta. Origem e
        # recurso escasso (cinco livres medidas em 12/10) e gastar uma num
        # teste seria pagar com pauta o que nao precisa ser pago.
    }
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    with open(destino, "w") as f:
        json.dump(sp, f, ensure_ascii=False, indent=2)
    return sp


def main() -> int:
    destino = sys.argv[1] if len(sys.argv) > 1 else "/tmp/teste/spec.json"
    sp = monta(destino)
    print(f"::notice::spec de teste em {destino} — "
          f"{len(sp['short'])} cena(s), canal de molde {MOLDE}")
    print("::notice::esta spec NAO consome origem de pauta e NAO sera publicada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
