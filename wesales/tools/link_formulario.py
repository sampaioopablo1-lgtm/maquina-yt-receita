#!/usr/bin/env python3
"""Link "formulário + agenda" de cada lead, para a coluna da Minha fila (29/09, pedido do dono).

É o mesmo link que os workflows mandam para a SDR (gravar_link_form_primeiro.py): abre o
formulário "Qualificação e agendamento — SDR" já preenchido com o que o CRM sabe do lead e, ao
enviar, leva para a agenda com o contato fixo. Aqui ele é montado com os VALORES do contato
(só os preenchidos, para o link ficar curto) e gravado no campo "Link: formulário + agenda".
Roda no relógio; escreve só quando o link mudou.

    python3 link_formulario.py            # DRY
    python3 link_formulario.py --aplicar
"""
from __future__ import annotations

import sys
import urllib.parse
from collections import Counter

from atuador_filas import CONECTAR, LOC, contatos, etapa_por_contato, pedir

FORM = "https://api.leadconnectorhq.com/widget/form/ww2ruVG5CdJ7rWJ83Gbf"
CAMPO = "GX7Z8yRGeERXCUgNbL3W"
PADRAO = {"first_name": "firstName", "phone": "phone", "email": "email"}
CHAVES = ["first_name", "phone", "email", "empresa", "segmento", "site", "instagram", "necessidade", "urgncia",
          "investimento_mensal_em_anncios", "investe_em_anncios", "prazo", "dor_principal",
          "clientes_novos_por_ms", "quem_atende_os_leads", "tem_time_comercial", "canal_principal_de_venda",
          "usa_crm", "plataformas_de_anncio", "j_teve_agncia", "experincia_com_agncia", "budget",
          "b__quanto_pode_investir", "decisor"]


def montar(c, por_chave) -> str:
    """Pura: link com os valores preenchidos do contato."""
    vals = {f["id"]: f.get("value") for f in c.get("customFields") or []}
    ps = []
    for k in CHAVES:
        v = c.get(PADRAO[k]) if k in PADRAO else vals.get(por_chave.get(k))
        if isinstance(v, list):
            v = ", ".join(map(str, v))
        if v not in (None, "", []):
            ps.append((k, str(v)))
    ps.append(("sdr_responsvel", "Andreyna Siqueira"))
    return FORM + "?" + urllib.parse.urlencode(ps, quote_via=urllib.parse.quote)


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    por_chave = {f["fieldKey"].split(".", 1)[1]: f["id"]
                 for f in pedir("GET", "/locations/%s/customFields" % LOC)["customFields"] if f.get("fieldKey")}
    etapas = etapa_por_contato()
    cont = Counter()
    for c in contatos():
        if etapas.get(c["id"]) != CONECTAR and "confirmar-reuniao" not in (c.get("tags") or []):
            continue
        link = montar(c, por_chave)
        atual = next((f.get("value") for f in c.get("customFields") or [] if f["id"] == CAMPO), None)
        if atual == link:
            cont["igual"] += 1
            continue
        cont["gravar"] += 1
        if aplicar:
            pedir("PUT", "/contacts/%s" % c["id"], {"customFields": [{"id": CAMPO, "value": link}]})
    print("link formulário + agenda%s: %s | exemplo: %s" % ("" if aplicar else " (DRY)", dict(cont), link[:160] if cont else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
