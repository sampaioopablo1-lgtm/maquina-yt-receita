#!/usr/bin/env python3
"""Inventário de módulos do GHL na subconta — LEITURA PURA.

Para cada menu/módulo que a API pública expõe, lista o que existe na conta
(quantidade e até 20 nomes). Serve para responder "o que o sistema tem e a
gente já usa" sem suposição. Nada é escrito.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from campos_bant import ghl, LOC  # noqa: E402

A = "altId=%s&altType=location" % LOC
MODULOS = [
    ("Local (configurações)", "/locations/%s" % LOC, None),
    ("Calendários", "/calendars/?locationId=%s&showDrafted=true" % LOC, "calendars"),
    ("Grupos de calendário", "/calendars/groups?locationId=%s" % LOC, "groups"),
    ("Usuários", "/users/?locationId=%s" % LOC, "users"),
    ("Workflows", "/workflows/?locationId=%s" % LOC, "workflows"),
    ("Links de gatilho", "/links/?locationId=%s" % LOC, "links"),
    ("Valores personalizados", "/locations/%s/customValues" % LOC, "customValues"),
    ("Tags", "/locations/%s/tags" % LOC, "tags"),
    ("Modelos/snippets (SMS)", "/locations/%s/templates?originId=%s&type=sms&limit=100" % (LOC, LOC), "templates"),
    ("Modelos/snippets (WhatsApp)", "/locations/%s/templates?originId=%s&type=whatsapp&limit=100" % (LOC, LOC), "templates"),
    ("Modelos/snippets (e-mail)", "/locations/%s/templates?originId=%s&type=email&limit=100" % (LOC, LOC), "templates"),
    ("Modelos de e-mail (builder)", "/emails/builder?locationId=%s&limit=100" % LOC, "builders"),
    ("Formulários", "/forms/?locationId=%s&limit=50" % LOC, "forms"),
    ("Pesquisas (surveys)", "/surveys/?locationId=%s&limit=50" % LOC, "surveys"),
    ("Funis e sites", "/funnels/funnel/list?locationId=%s&limit=50" % LOC, "funnels"),
    ("Produtos", "/products/?locationId=%s&limit=50" % LOC, "products"),
    ("Propostas/contratos", "/proposals/document?locationId=%s&limit=50" % LOC, "documents"),
    ("Modelos de proposta", "/proposals/templates?locationId=%s&limit=50" % LOC, "data"),
    ("Faturas", "/invoices/?%s&limit=20&offset=0" % A, "invoices"),
    ("Pedidos (pagamentos)", "/payments/orders?%s&limit=20" % A, "data"),
    ("Assinaturas", "/payments/subscriptions?%s&limit=20" % A, "data"),
    ("Integração de pagamento", "/payments/integrations/provider/whitelabel?%s" % A, None),
    ("Campanhas", "/campaigns/?locationId=%s" % LOC, "campaigns"),
    ("Pipelines", "/opportunities/pipelines?locationId=%s" % LOC, "pipelines"),
    ("Redes sociais (contas)", "/social-media-posting/%s/accounts" % LOC, None),
    ("Blogs", "/blogs/site/all?locationId=%s&skip=0&limit=20" % LOC, "data"),
    ("Mídias", "/medias/files?%s&sortBy=createdAt&sortOrder=desc&limit=20" % A, "files"),
    ("Objetos personalizados", "/objects/?locationId=%s" % LOC, "objects"),
    ("Associações", "/associations/?locationId=%s&skip=0&limit=50" % LOC, "associations"),
    ("Empresas (businesses)", "/businesses/?locationId=%s" % LOC, "businesses"),
    ("Voice AI (agentes)", "/voice-ai/agents?locationId=%s" % LOC, "agents"),
    ("Conversation AI (agentes)", "/conversation-ai/agents/search?locationId=%s" % LOC, "agents"),
    ("Base de conhecimento", "/knowledge-bases/?locationId=%s" % LOC, "knowledgeBases"),
    ("Números de telefone", "/phone-system/numbers/location/%s" % LOC, "numbers"),
    ("Pools de números", "/phone-system/number-pools?locationId=%s" % LOC, "numberPools"),
    ("Cursos/membership", "/courses/?locationId=%s" % LOC, None),
    ("Loja (coleções)", "/products/collections?altId=%s&altType=location&limit=20" % LOC, "data"),
    ("Contatos (total)", "/contacts/?locationId=%s&limit=1" % LOC, None),
    ("Conversas (total)", "/conversations/search?locationId=%s&limit=1" % LOC, None),
]


def nomes(lista) -> list:
    out = []
    for x in lista[:20]:
        if isinstance(x, dict):
            out.append(x.get("name") or x.get("title") or x.get("fieldKey") or x.get("id"))
        else:
            out.append(str(x))
    return out


def main() -> int:
    for rot, rota, chave in MODULOS:
        st, r = ghl("GET", rota, tolerar=(400, 401, 403, 404, 422, 500))
        if st != 200 or not isinstance(r, dict):
            print("\n## %s — HTTP %s %s" % (rot, st, str(r)[:160]))
            continue
        if chave and isinstance(r.get(chave), list):
            lst = r[chave]
            total = r.get("total") or r.get("count") or len(lst)
            print("\n## %s — %s" % (rot, total))
            for n in nomes(lst):
                print("   - %s" % n)
        else:
            resumo = {k: (v if not isinstance(v, (list, dict)) else ("[%d]" % len(v) if isinstance(v, list) else "{…}"))
                      for k, v in list(r.items())[:25]}
            if rot.startswith("Local"):
                loc = r.get("location") or {}
                resumo = {k: loc.get(k) for k in ("name", "timezone", "email", "phone", "website")}
                resumo["settings"] = loc.get("settings")
                resumo["social"] = loc.get("social")
            print("\n## %s\n   %s" % (rot, json.dumps(resumo, ensure_ascii=False)[:900]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
