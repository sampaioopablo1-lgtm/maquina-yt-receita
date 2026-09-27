#!/usr/bin/env python3
"""Fecha a janela das cadencias ate a abertura da operacao, e reabre depois.

O PROBLEMA, medido em 27/09/2026 (domingo):

A operacao comercial comeca **terca 29/09**. Mas o backfill do G-03 ja moveu 38
oportunidades para `CONECTAR` em 24/09, e as duas cadencias disparam no mesmo
gatilho — `pipeline_stage_updated`, "movido para CONECTAR". Como os leads JA
estao lá, nada sera movido na terca: o gatilho nao vai disparar.

Pior: a cadencia JA ENTROU e esta parada. Prova nos campos do `Carlos Andrade`:
`Tentativa nº` = 0 e `Permissão WhatsApp` = "Não solicitado" (os nos de campo
rodaram), e `atraso-1a-tentativa` ainda presente (a 1a tentativa NAO rodou).
Campo e tag rodam fora do horario; **so a mensagem espera a janela.**

A janela das duas e `days [1,2,3,4,5]`, 08:30-18:30. **A proxima abertura e
SEGUNDA, 28/09 08:30** — e ai 37 mensagens saem sozinhas, um dia antes da
operacao, sem SDR na mesa. Protegidos por `nao-perturbe`/`pausado`: 1 de 38.

O CONSERTO, e por que e a janela e nao o lead:

- voltar a oportunidade para `NOVO LEAD` **nao desinscreve** do workflow
  (`APRENDIZADOS-CRM.md`): a execucao parada continuaria disparando segunda;
- `nao-perturbe` nos 37 faria a execucao tentar, o canal bloquear e a cadencia
  **seguir adiante** — queima a MI-0 em silencio;
- mexer na janela segura TODA execucao parada, sem tocar em contato nenhum, e
  desfaz-se numa linha.

`--fechar` deixa `days: [2]` — **so terca**. Nada dispara segunda, e a abertura
acontece sozinha na terca as 08:30, sem depender de ninguem lembrar nem de cron
(`schedule` do GitHub Actions **so roda no branch padrao**, e este trabalho nao
esta nele). Depois da terca, `--abrir` devolve `[1,2,3,4,5]`.

LIMITE DE EXECUCAO, declarado: editar workflow usa a API interna, com bearer de
sessao logada (`../.local/_ghl_bearer.txt`, renovado por navegador headless).
Isso **nao roda em GitHub Action nem em contêiner** — so no PC do dono. O
`--dump` confere tudo offline; o passo a passo pela tela esta no fim deste
docstring.

Uso:  python patch_janela_abertura.py --dump             # confere, sem rede
      python patch_janela_abertura.py --fechar           # plano, nao grava
      python patch_janela_abertura.py --fechar --aplicar  # grava
      python patch_janela_abertura.py --abrir --aplicar   # depois da terca

PELA TELA (equivalente, 2 cliques por cadencia):
  Automation > Cadência Inbound > Settings (engrenagem) > Execution window
    desmarque Seg, Qua, Qui, Sex — deixe so Ter.  Salve e publique.
  Repita em Cadência 12x30. Depois da terca, remarque os cinco dias.
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ALVOS = ["Cadência Inbound", "Cadência 12x30"]
AQUI = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(AQUI, "..", "workflows-json")
BACKUP = os.path.join(DUMPS, "_antes-janela-abertura")

# Terca = 2 na numeracao do GHL (o dump mostra [1,2,3,4,5] para seg-sex).
SO_TERCA = [2]
SEG_A_SEX = [1, 2, 3, 4, 5]


def nova_janela(atual, dias):
    """Mesma janela, so trocando os dias. Horario intacto, de proposito."""
    j = copy.deepcopy(atual or {})
    j["days"] = list(dias)
    j.setdefault("startHour", 8)
    j.setdefault("startMinute", 30)
    j.setdefault("endHour", 18)
    j.setdefault("endMinute", 30)
    return j


def descreve(j):
    if not j:
        return "(sem janela)"
    nomes = {1: "seg", 2: "ter", 3: "qua", 4: "qui", 5: "sex", 6: "sab", 0: "dom", 7: "dom"}
    dias = ", ".join(nomes.get(d, str(d)) for d in (j.get("days") or [])) or "NENHUM"
    return "%s  %02d:%02d-%02d:%02d" % (dias, j.get("startHour", 0), j.get("startMinute", 0),
                                        j.get("endHour", 0), j.get("endMinute", 0))


def le_dump(nome):
    caminho = os.path.join(DUMPS, nome + ".json")
    if not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8") as fh:
        dado = json.load(fh)
    return (dado.get("workflow") or dado) if isinstance(dado, dict) else None


def main():
    fechar = "--fechar" in sys.argv
    abrir = "--abrir" in sys.argv
    if fechar == abrir:
        print("escolha exatamente um: --fechar ou --abrir")
        return 2
    dias = SO_TERCA if fechar else SEG_A_SEX
    aplicar = "--aplicar" in sys.argv

    if "--dump" in sys.argv:
        print("MODO --dump: nada e lido da conta e nada e gravado.\n")
        for nome in ALVOS:
            wf = le_dump(nome)
            if wf is None:
                print("== %s: sem dump" % nome)
                continue
            atual = wf.get("window")
            print("== %-20s [%s]" % (nome, wf.get("status")))
            print("   agora : %s" % descreve(atual))
            print("   ficaria: %s" % descreve(nova_janela(atual, dias)))
        print("\nRode sem --dump, no PC do dono, para falar com a conta.")
        return 0

    # Daqui para baixo precisa do bearer de sessao logada.
    try:
        import ghl_api as g
        from patch_funil_reuniao import put            # put preserva o resto
    except Exception as e:
        print("nao foi possivel carregar o cliente interno: %s" % e)
        print("Este script so roda no PC do dono (bearer de sessao logada).")
        print("Use --dump aqui, ou o passo a passo pela tela no docstring.")
        return 2

    c = g.client()
    ids = {w.get("name"): w["id"] for w in c.request("GET", "/workflow/" + g.LOC)}
    for nome in ALVOS:
        if nome not in ids:
            print("== %s: nao existe nesta subconta" % nome)
            continue
        cur = c.request("GET", "/workflow/" + g.LOC + "/" + ids[nome])
        atual = cur.get("window")
        alvo = nova_janela(atual, dias)
        print("== %-20s [%s]" % (nome, cur.get("status")))
        print("   agora : %s" % descreve(atual))
        print("   alvo  : %s" % descreve(alvo))
        if (atual or {}).get("days") == alvo["days"]:
            print("   ja esta assim — nada a fazer (idempotente)")
            continue
        if not aplicar:
            continue
        os.makedirs(BACKUP, exist_ok=True)
        g.export(c, ids[nome], os.path.join(BACKUP, nome + ".json"))
        tpl = (cur.get("workflowData") or {}).get("templates") or []
        cur["window"] = alvo                       # o `put` manda cur["window"]
        put(c, cur, tpl)                           # levanta se a conta recusar
        v = c.request("GET", "/workflow/" + g.LOC + "/" + ids[nome])
        print("   gravado: %s  (nos: %d, status: %s)"
              % (descreve(v.get("window")),
                 len((v.get("workflowData") or {}).get("templates") or []), v.get("status")))
        g.export(c, ids[nome], os.path.join(DUMPS, nome + ".json"))
    if not aplicar:
        print("\n(nada foi gravado — rode com --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
