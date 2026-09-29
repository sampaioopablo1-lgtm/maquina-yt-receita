#!/usr/bin/env python3
"""Roteiro de ligação do Power Dialer com o botão da FICHA do próprio lead (28/09; o formulário externo saiu).

O painel "Roteiro" do Power Dialer busca o roteiro com `replaceVariables=true&contactId=<lead na
linha>` (lido no código do discador), então `{{contact.…}}` vira o dado do lead da ligação.
Resultado: em qualquer ligação, a SDR clica em "Abrir ficha e agendar" e o formulário abre com
os dados daquele lead; ao enviar, abre a agenda do closer.
"""
import json, sys
import ghl_interno as g

NOME = "Roteiro SDR + ficha do lead"
FICHA = "https://app.wesalescrm.com/v2/location/%s/contacts/detail/{{contact.id}}" % g.LOC
HTML = f"""
<p><a href="{FICHA}" target="_blank" style="display:inline-block;background:#155EEF;color:#fff;padding:10px 16px;border-radius:8px;font-weight:700;text-decoration:none">👤 Abrir a ficha de {{{{contact.first_name}}}}</a>
&nbsp; <a href="https://api.whatsapp.com/send?phone={{{{contact.phone_raw}}}}" target="_blank" style="display:inline-block;background:#16A34A;color:#fff;padding:10px 16px;border-radius:8px;font-weight:700;text-decoration:none">📱 Ligar pelo WhatsApp</a></p>
<p><b>Já respondeu no anúncio (não pergunte de novo, só confirme):</b><br>
Principal desafio: <i>{{{{contact.dor_principal}}}}</i><br>
Quando quer resolver: <i>{{{{contact.urgncia}}}}</i> · Toparia investir/mês: <i>{{{{contact.investimento_mensal_em_anncios}}}}</i></p>
<hr>
<p><b>1. Abertura (10 s)</b> — "Oi, {{{{contact.first_name}}}}! Aqui é a Andreyna, da O Próximo Cliente. Você deixou seu contato no nosso anúncio agora há pouco. Me conta: o que está travando as vendas aí hoje?"</p>
<p><b>2. Dor (até 3 min)</b> — sintoma → causa → custo → o que mudou agora → o que já tentou. Uma pergunta por vez; depois, silêncio.</p>
<p><b>3. Qualificar (2 min) — preencha na ficha, bloco Q1–Q6, enquanto ele fala:</b><br>
Q1 Dor principal · Q2 Clientes novos por mês · Q3 Quem atende os leads · Q4 Budget (tem / precisa aprovar / não tem) · Q5 Decisor · Q6 Prazo</p>
<p><b>4. Resumir e agendar</b> — "Deixa eu ver se entendi: …. É isso?" → "Fica melhor [dia] às [hora] ou [dia] às [hora]?" Na ficha, clique no <b>ícone de calendário (Marcar reunião)</b> → agenda <b>Agendamento pela SDR</b> (seg–sex 18:00 · 19:30 · 21:00 · sáb 09:00 · 10:30). O lead já vem selecionado.</p>
<p><b>5. Travar</b> — "Te mando agora a confirmação no WhatsApp. Traz dois números do último mês: quantos contatos chegaram e quantos viraram venda."</p>
<p style="font-size:13px;color:#475467">Depois da ligação: <b>Canal da tentativa</b> e <b>Resultado</b> no topo da ficha. Não atendeu no telefone? <b>Ligar pelo WhatsApp</b> e marque Canal = WhatsApp. Nunca abrir com "tem um minutinho?".</p>
""".strip()


def main():
    base = "/phone-system/locations/%s/call-scripts" % g.LOC
    ex = [s for s in (g.pedir("GET", base + "?page=1&limit=100").get("data") or []) if s.get("scriptName") == NOME]
    corpo = {"scriptName": NOME, "scriptContent": {"contentType": "html", "contentBody": HTML}}
    if "--seco" in sys.argv:
        print(HTML[:600]); return
    if ex:
        r = g.pedir("PUT", base + "/" + ex[0]["id"], corpo)
    else:
        r = g.pedir("POST", base, corpo)
    print(json.dumps(r, ensure_ascii=False)[:300])


if __name__ == "__main__":
    main()
