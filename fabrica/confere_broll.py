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

E AQUI ESTE PORTAO ESTAVA SONDANDO O HOST ERRADO. Medido em 04/10/2026, no
agla-level-009: a spec chegou com os tres `broll_url` JA resolvidos pelo
`prebusca_broll.py`, e este portao reprovou o pacote de qualquer jeito, porque
exigia chave e sondava `api.pexels.com` — que e exatamente o host que o render
nao usa mais quando o link esta na spec. Zero segundos de render gastos, mas
tambem zero pacote: o portao reprovou por uma dependencia que a spec havia
removido.

A pergunta certa e sempre "o footage chega ate o render?", e a resposta depende
de QUEM vai busca-lo:

  * cena com `broll_url` na spec: o render so baixa do CDN
    (`videos.pexels.com`), sem chave e sem cota. Entao o portao sonda o CDN,
    naquele link, com um Range de 1 KiB. Isso e mais forte que a sonda antiga
    — confere o arquivo QUE VAI SER USADO, nao um resultado de busca qualquer.
  * cena sem `broll_url`: o render ainda chama a API. Ai valem a chave e a
    busca, como sempre.

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
    from prebusca_broll import _cdn_responde

    # CENAS JA RESOLVIDAS: o render nao chama a API por elas, entao o portao
    # tambem nao. Sonda o CDN no link exato que vai ser baixado.
    resolvidas = [i for i in pedem if (sp["longo"][i].get("broll_url") or "").strip()]
    if resolvidas:
        print(f"{len(resolvidas)}/{len(pedem)} cenas broll com link na spec — "
              f"sondando o CDN, nao a API")
        ruins = []
        for i in resolvidas:
            link = sp["longo"][i]["broll_url"].strip()
            if _cdn_responde(link):
                print(f"  cena {i:2d}: CDN entrega {link.rsplit('/', 1)[-1]}")
            else:
                ruins.append(i)
        if ruins:
            print(f"CDN NAO ENTREGA {len(ruins)} de {len(resolvidas)} clipes "
                  f"resolvidos (cenas {ruins}).")
            print("O link esta na spec mas videos.pexels.com nao responde a "
                  "este runner. Renderizar agora entrega desenho onde a spec "
                  "pede footage.")
            print("Caminhos: refazer a pre-busca "
                  "(`python3 fabrica/prebusca_broll.py <spec> --conferir`) de "
                  "onde o CDN responde, ou tirar o layout broll da spec.")
            return 1

    por_buscar = [i for i in pedem if i not in resolvidas]
    if not por_buscar:
        print(f"sonda ok: {len(resolvidas)}/{len(pedem)} cenas com footage que "
              f"o CDN entrega; nenhuma depende da API")
        return 0

    k = BR.chave()
    if not k:
        print(f"CHAVE DO PEXELS AUSENTE: {BR.ORIGEM_DA_CHAVE}")
        print(f"A spec {sp.get('pacote')} tem {len(por_buscar)} cena(s) com "
              f"footage e SEM link na spec; sem chave elas viram desenho e o "
              f"pacote nao e o que a spec descreve.")
        print("Conserto: gravar a chave no banco e disparar de novo —")
        print("  insert into config (chave, valor) values "
              "('pexels_api_key', to_jsonb('<chave>'::text))")
        print("  on conflict (chave) do update set valor = excluded.valor;")
        return 1
    print(f"chave do Pexels ok ({BR.ORIGEM_DA_CHAVE}) para "
          f"{len(por_buscar)} cena(s) broll sem link na spec")

    # Ter a chave nao e chegar ao Pexels. No epomeno-epipedo-004 a chave veio
    # do banco e as 7 cenas morreram em `TimeoutError` — a mesma chave que
    # respondia do sandbox nao respondia do runner. Uma busca de verdade
    # aqui custa uma chamada e responde em segundos o que o render responde
    # em vinte minutos.
    q = next((sp["longo"][i].get("broll_q") for i in por_buscar
              if sp["longo"][i].get("broll_q")), None)
    if not q:
        print("nenhuma cena broll declara broll_q — nada a sondar")
        return 1
    try:
        dados = BR.buscar(q, k)
    except Exception as e:
        print(f"PEXELS INALCANCAVEL DAQUI: {type(e).__name__}: {e}")
        print(f"A chave resolve, mas a busca por '{q}' nao completou em "
              f"3 tentativas. Renderizar agora entrega {len(por_buscar)} cena(s) "
              f"de desenho onde a spec pede footage — o pacote sai diferente do "
              f"que foi desenhado, e isso so apareceria olhando frame.")
        print("Caminhos: resolver os links fora do runner "
              "(`python3 fabrica/prebusca_broll.py <spec>` de onde a API "
              "responde), ou tirar o layout broll da spec e despachar de novo.")
        return 1
    n = len(dados.get("videos", []))
    print(f"sonda ok: '{q}' devolveu {n} resultado(s)")
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "spec.json"))
