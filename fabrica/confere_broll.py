#!/usr/bin/env python3
"""A spec pede footage do Pexels? Entao a chave precisa existir ANTES do render.

Por que este portao existe (19/08/2026). O agla-level-004 declarou 7 cenas
com layout "broll" e entregou 7 cenas de desenho. As sete cairam no fallback
silencioso, e a causa nao era rede nem busca sem resultado: `config
.pexels_api_key` simplesmente NAO EXISTIA no banco. A chave tinha sido usada
num teste de fumaca local e nunca gravada — testar uma chave nao a instala
(aprendizado 309).

O custo do jeito antigo: 20 minutos de render para produzir um pacote que
nao e o que a spec descreve, descoberto depois, olhando frame.

E o "enfeite nunca derruba render"? Continua valendo, e este portao nao o
contradiz — ele separa dois casos que so parecem iguais:

  * durante o render, uma cena que perde o footage (rede, busca vazia, clipe
    corrompido) cai no desenho e o render segue. Um tropeco nao vale um
    pacote perdido.
  * ANTES do render, saber que NENHUMA cena tera footage e saber que o
    pacote inteiro sai diferente do que foi desenhado. Ai falhar custa dois
    segundos e um novo disparo; nao falhar custa vinte minutos e uma vaga de
    publicacao.

Uso:
    python3 fabrica/confere_broll.py spec.json
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def cenas_com_broll(sp: dict) -> list[int]:
    return [i for i, c in enumerate(sp.get("longo", []))
            if c.get("layout") == "broll"]


def main(caminho: str) -> int:
    sp = json.load(open(caminho, encoding="utf-8"))
    pedem = cenas_com_broll(sp)
    if not pedem:
        print("sem cenas broll — nada a conferir")
        return 0

    import broll as BR

    k = BR.chave()
    if not k:
        print(f"CHAVE DO PEXELS AUSENTE: {BR.ORIGEM_DA_CHAVE}")
        print(f"A spec {sp.get('pacote')} declara {len(pedem)} cenas com "
              f"footage; sem chave todas viram desenho e o pacote nao e o que "
              f"a spec descreve.")
        print("Conserto: gravar a chave no banco e disparar de novo —")
        print("  insert into config (chave, valor) values "
              "('pexels_api_key', to_jsonb('<chave>'::text))")
        print("  on conflict (chave) do update set valor = excluded.valor;")
        return 1
    print(f"chave do Pexels ok ({BR.ORIGEM_DA_CHAVE}) para "
          f"{len(pedem)} cenas broll")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "spec.json"))
