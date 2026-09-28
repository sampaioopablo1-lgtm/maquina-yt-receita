#!/usr/bin/env python3
"""Link da SDR: formulário primeiro, agenda no final (pedido do dono, 28/09).

Antes: "Abrir agendamento com a ficha preenchida" abria o calendário "Agendamento pela SDR",
que mostra o horário ANTES da ficha. Agora abre o formulário "Qualificação e agendamento — SDR"
com TUDO o que o CRM já sabe (anúncio + BANT + empresa); ao enviar, o formulário redireciona
para o calendário, e o calendário (contato fixo, `stickyContact`) reconhece o lead.

Também corrige as chaves `investimento_mensal_em_an%C3%BAncios` / `investe_em_an%C3%BAncios`,
que não batiam com a chave do formulário (sem acento) e por isso nunca preenchiam.
"""
import json, re, sys
import ghl_interno as g

FORM = "https://api.leadconnectorhq.com/widget/form/ww2ruVG5CdJ7rWJ83Gbf"
# chave de preenchimento do formulário (hiddenFieldQueryKey) -> campo do contato
CAMPOS = [("first_name", "first_name"), ("phone", "phone"), ("email", "email"),
          ("empresa", "empresa"), ("segmento", "segmento"), ("site", "site"), ("instagram", "instagram"),
          ("necessidade", "necessidade"), ("urgncia", "urgncia"),
          ("investimento_mensal_em_anncios", "investimento_mensal_em_anncios"),
          ("investe_em_anncios", "investe_em_anncios"), ("prazo", "prazo"),
          ("dor_principal", "dor_principal"), ("clientes_novos_por_ms", "clientes_novos_por_ms"),
          ("quem_atende_os_leads", "quem_atende_os_leads"), ("tem_time_comercial", "tem_time_comercial"),
          ("canal_principal_de_venda", "canal_principal_de_venda"), ("usa_crm", "usa_crm"),
          ("plataformas_de_anncio", "plataformas_de_anncio"), ("j_teve_agncia", "j_teve_agncia"),
          ("experincia_com_agncia", "experincia_com_agncia"), ("budget", "budget"),
          ("b__quanto_pode_investir", "b__quanto_pode_investir"), ("decisor", "decisor")]
LINK = FORM + "?" + "&".join("%s={{contact.%s}}" % (k, c) for k, c in CAMPOS) + "&sdr_responsvel=Andreyna%20Siqueira"
VELHO = re.compile(r"https?://[^\"'\s<>\x5c]*widget/booking/oOfR9ADPJM0WyVyHRgKE\?[^\"'\s<>\x5c]*")


def main(seco):
    for nome in ("Fechar Horário", "Pós-ligação v3"):
        w = g.por_nome(nome)
        cur = g.ler(w["id"])
        nos = cur["workflowData"]["templates"]
        s = json.dumps(nos, ensure_ascii=False)
        n = len(VELHO.findall(s))
        novo = json.loads(VELHO.sub(LINK.replace("\\", "\\\\"), s))
        print("%s v%s: %d link(s) trocado(s)" % (nome, cur.get("version"), n))
        if seco or not n:
            continue
        g.exportar(w["id"], "../.local/bkp-copy-27-09/%s-antes-form-primeiro.json" % nome.replace(" ", "_"))
        g.put(cur, novo)
        d = g.ler(w["id"])
        s2 = json.dumps(d["workflowData"]["templates"], ensure_ascii=False)
        print("   relido: %s v%s, links novos=%d, velhos=%d" % (d["status"], d["version"], s2.count(FORM + "?"),
                                                              len(VELHO.findall(s2))))


if __name__ == "__main__":
    main("--seco" in sys.argv)
