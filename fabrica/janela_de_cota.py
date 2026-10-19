"""Quantos envios a janela de cota ja levou — contado, nao lembrado.

POR QUE ESTE MODULO EXISTE (19/10/2026). Eu contei as pecas da janela DE CABECA
duas vezes e errei as duas, na mesma direcao:

  * as 00:2x escrevi *"ontem a frota fechou o dia em seis pecas"*, quando o dia
    tinha dezessete depois das 07:00 — eu tinha contado as seis ULTIMAS;
  * as 04:1x escrevi *"doze envios na janela, logo a cota e >= 19.200"*, quando
    a janela tinha vinte e quatro. **Errado pela METADE.**

E as duas vezes a regra certa ja estava escrita no `CLAUDE.md`, por mim: *"conte
as pecas da JANELA (desde 07:00 UTC), nao do dia calendario"*. **Eu nao apliquei
ao meu proprio numero** — que e o item 3 da §10: toda conta que eu faco a mao
vira um erro meu.

**A JANELA VIRA AS 07:00 UTC**, que e a meia-noite do Pacifico (PDT em outubro
de 2026). Rodada entre 00:00 e 07:00 UTC herda a cota do dia anterior.

**A FONTE e o parque**, `docs/pendente/duracoes-a-medir.jsonl`, porque desde
18/10 as 06:1x TODA peca publicada entra nele com `youtube_id` — logo ele e o
log dos envios, e nao depende do banco (o `execute_sql` esta negado) nem da
minha memoria das ultimas rodadas.

**O QUE ELE NAO AFIRMA:** o TETO da cota. Ele devolve o PISO — o que ja passou
sem um `403 quota` — e quem acha o teto e o primeiro `403` de rodada normal, que
nao custa nada porque requisicao recusada nao consome cota.
"""
import datetime
import json
import os

CUSTO_VIDEOS_INSERT = 1600   # unidades, medido; `captions.insert` custa 400
HORA_DA_VIRADA = 7           # UTC, meia-noite do Pacifico em outubro de 2026
PARQUE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "docs", "pendente", "duracoes-a-medir.jsonl")


def abertura(agora: datetime.datetime) -> datetime.datetime:
    """O instante em que a janela corrente abriu."""
    if agora.tzinfo is None:
        raise ValueError("passe hora com fuso: janela de cota e em UTC")
    agora = agora.astimezone(datetime.timezone.utc)
    hoje = agora.replace(hour=HORA_DA_VIRADA, minute=0, second=0, microsecond=0)
    return hoje if agora >= hoje else hoje - datetime.timedelta(days=1)


def envios(agora: datetime.datetime, caminho: str | None = None) -> list[dict]:
    """As pecas publicadas na janela corrente, por id DISTINTO.

    Conta por `youtube_id` e nao por linha: duas linhas do mesmo id seriam uma
    reescrita, nao dois envios — o erro que ja produziu um ponto fantasma na
    serie do residuo em 18/10.
    """
    corte = abertura(agora)
    vistos, fora = set(), []
    with open(caminho or PARQUE, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            d = json.loads(linha)
            yid = d.get("youtube_id")
            if not yid or yid in vistos:
                continue
            quando = datetime.datetime.fromisoformat(
                d["em"].replace("Z", "+00:00"))
            if quando >= corte:
                vistos.add(yid)
                fora.append(d)
    return sorted(fora, key=lambda d: d["em"])


def piso(agora: datetime.datetime, caminho: str | None = None) -> dict:
    e = envios(agora, caminho)
    return {"abertura": abertura(agora), "envios": len(e),
            "unidades": len(e) * CUSTO_VIDEOS_INSERT,
            "primeiro": e[0]["pacote"] if e else None,
            "ultimo": e[-1]["pacote"] if e else None}


def relato(agora: datetime.datetime | None = None,
           caminho: str | None = None) -> str:
    agora = agora or datetime.datetime.now(datetime.timezone.utc)
    p = piso(agora, caminho)
    linhas = [
        f"JANELA DE COTA aberta em {p['abertura']:%Y-%m-%d %H:%M} UTC "
        f"(vira as {HORA_DA_VIRADA:02d}:00): **{p['envios']} envios**, "
        f"{p['unidades']} unidades a {CUSTO_VIDEOS_INSERT} cada."]
    if p["envios"]:
        linhas.append(f"  do {p['primeiro']} ao {p['ultimo']}, ids DISTINTOS.")
    linhas.append("  isto e o PISO da cota deste projeto: o que ja passou sem "
                  "um 403. O TETO segue desconhecido, e quem o acha e o "
                  "primeiro 403 de rodada normal — recusa nao gasta.")
    return "\n".join(linhas)


if __name__ == "__main__":
    print(relato())
