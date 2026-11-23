#!/usr/bin/env python3
"""Aprendizado dos Reels do @trafegocom.ia. Sem rede: quem le o Instagram e a rotina (Composio).

Uso:
  python3 aprende.py midia.json [seguidores]
    midia.json = lista de midias do INSTAGRAM_GET_IG_USER_MEDIA com
                 fields=id,timestamp,permalink,insights.metric(views,reach,saved,shares,total_interactions)
    seguidores = followers_count lido agora (opcional)

Grava desempenho.json (ultima leitura de cada midia) e seguidores.jsonl, e imprime o RANKING
por familia de tema, cruzando com publicados.jsonl (o que a rotina publicou, com familia).

Regras:
  * so entra no ranking peca com >= 24 h (antes disso a distribuicao ainda esta acontecendo);
  * a nota de cada peca e views + 5*(shares+saved): compartilhar e salvar pesam mais para
    alcancar quem nao segue (sinal declarado pelo Instagram: envios por alcance);
  * familia com menos de 3 pecas maduras sai como "pouco dado", nunca como vencedora.
"""
import json, os, sys, datetime as dt, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(AQUI, "publicados.jsonl")
DES = os.path.join(AQUI, "desempenho.json")
SEG = os.path.join(AQUI, "seguidores.jsonl")
MIN_H, MIN_N = 24, 3


def met(m):
    out = {}
    for x in ((m.get("insights") or {}).get("data") or []):
        v = (x.get("values") or [{}])[0].get("value")
        out[x["name"]] = v
    return out


def nota(d):
    return (d.get("views") or 0) + 5 * ((d.get("shares") or 0) + (d.get("saved") or 0))


def carrega_pub():
    if not os.path.exists(PUB):
        return {}
    return {r["ig_id"]: r for r in (json.loads(l) for l in open(PUB) if l.strip())}


def main():
    midia = json.load(open(sys.argv[1]))
    if isinstance(midia, dict):
        midia = midia.get("data", midia)
    agora = dt.datetime.now(dt.timezone.utc)
    des = json.load(open(DES)) if os.path.exists(DES) else {}
    for m in midia:
        d = met(m)
        d.update(ts=m.get("timestamp"), link=m.get("permalink"), lido=agora.isoformat(timespec="seconds"))
        des[m["id"]] = d
    json.dump(des, open(DES, "w"), indent=1, ensure_ascii=False)
    if len(sys.argv) > 2:
        with open(SEG, "a") as f:
            f.write(json.dumps({"em": agora.isoformat(timespec="seconds"), "seguidores": int(sys.argv[2])}) + "\n")

    pub = carrega_pub()
    fam = {}
    for ig, d in des.items():
        r = pub.get(ig)
        if not r or not d.get("ts"):
            continue
        idade = (agora - dt.datetime.fromisoformat(d["ts"].replace("+0000", "+00:00"))).total_seconds() / 3600
        if idade < MIN_H:
            continue
        fam.setdefault(r["familia"], []).append(nota(d))

    print("RANKING por familia (pecas com >= %d h; nota = views + 5x(compart.+salv.))" % MIN_H)
    linhas = sorted(((st.median(v), k, len(v)) for k, v in fam.items()), reverse=True)
    for med, k, n in linhas:
        print("  %-28s mediana %6.1f  n=%d %s" % (k, med, n, "" if n >= MIN_N else "(pouco dado)"))
    if not linhas:
        print("  ainda sem peca madura da rotina: escolha familias do banco sem preferencia")
    if os.path.exists(SEG):
        s = [json.loads(l) for l in open(SEG) if l.strip()]
        if len(s) >= 2:
            print("SEGUIDORES: %d -> %d desde %s" % (s[0]["seguidores"], s[-1]["seguidores"], s[0]["em"][:10]))


if __name__ == "__main__":
    main()
