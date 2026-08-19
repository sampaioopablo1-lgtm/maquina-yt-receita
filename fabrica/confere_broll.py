#!/usr/bin/env python3
"""A spec pede footage do Pexels? Entao o footage precisa ser ALCANCAVEL antes do render.

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

E por que uma SONDA e nao so a chave? Porque ter a chave nao e chegar ao
Pexels. No epomeno-epipedo-004 a chave veio do banco — o log diz "banco
(config.pexels_api_key)" — e mesmo assim as 7 cenas cairam, todas em
`TimeoutError: The read operation timed out`. A mesma chave respondia do
sandbox e nao respondia do runner. So uma busca de verdade separa "a linha
existe" de "o footage vem".

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

    # Ter a chave nao e chegar ao Pexels. No epomeno-epipedo-004 a chave veio
    # do banco e as 7 cenas morreram em `TimeoutError` — a mesma chave que
    # respondia do sandbox nao respondia do runner. Uma busca de verdade
    # aqui custa uma chamada e responde em segundos o que o render responde
    # em vinte minutos.
    q = next((c["broll_q"] for c in sp["longo"]
              if c.get("layout") == "broll" and c.get("broll_q")), None)
    if not q:
        print("nenhuma cena broll declara broll_q — nada a sondar")
        return 1
    try:
        dados = BR.buscar(q, k)
    except Exception as e:
        print(f"PEXELS INALCANCAVEL DAQUI: {type(e).__name__}: {e}")
        print(f"A chave resolve, mas a busca por '{q}' nao completou em "
              f"3 tentativas. Renderizar agora entrega {len(pedem)} cenas de "
              f"desenho onde a spec pede footage — o pacote sai diferente do "
              f"que foi desenhado, e isso so apareceria olhando frame.")
        print("Caminhos: conferir se o Pexels responde a este runner, ou "
              "tirar o layout broll da spec e despachar de novo.")
        return 1
    n = len(dados.get("videos", []))
    print(f"sonda ok: '{q}' devolveu {n} resultado(s)")
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "spec.json"))
