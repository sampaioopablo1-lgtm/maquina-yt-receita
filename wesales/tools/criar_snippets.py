#!/usr/bin/env python3
"""Mensagens prontas (snippets) para a SDR — atalho "/" na conversa (29/09, pedido do dono).

Textos aprovados em COPY-WHATSAPP.md (regra: não pede permissão, não avisa que vai ligar,
termina com pergunta). Tipo "sms" = canal do Stevo (WhatsApp pelo QR). Idempotente pelo nome.
A API pública não cria snippet (401 de escopo); vai pela interna (token de sessão).
"""
import sys
import ghl_interno as g

N = "{{contact.first_name}}"
SNIPPETS = [
    ("1 · Primeiro contato (MI-0)", "Oi, %s! Aqui é da O Próximo Cliente, vi que você pediu contato. Pergunta direta: hoje o cliente novo de vocês vem mais de indicação ou de anúncio? Quem depende de indicação costuma ter mês bom e mês vazio. É o seu caso?" % N),
    ("2 · Não atendeu — dor", "%s, você deixou seu contato porque alguma coisa não está fechando na captação de clientes. O que pesa mais hoje: pouca gente chegando ou gente chegando e não comprando?" % N),
    ("3 · Contatos x vendas", "Oi, %s! Aqui é da O Próximo Cliente. Pergunta rápida: quantos contatos vocês receberam no último mês e quantos viraram venda? Se a resposta for \"não sei\", tem dinheiro ficando pelo caminho." % N),
    ("4 · Tempo de resposta", "%s, a maioria dos negócios que atendemos não tinha problema de anúncio: tinha contato chegando e ninguém respondendo a tempo. Aí dentro, quanto tempo leva hoje pra alguém responder um cliente novo?" % N),
    ("5 · Indicação ou anúncio", "%s, uma linha só: hoje o cliente novo de vocês vem mais por indicação ou por anúncio? Indicação é ótima até o mês em que ela não vem." % N),
    ("6 · O que travou", "%s, se captar cliente não fosse um problema aí, você não teria deixado seu contato. O que travou: falta de gente chegando ou gente que chega e some?" % N),
    ("7 · Fechar horário", "%s, foi bom falar com você. O que você me contou não se resolve sozinho, e cada semana parada é cliente indo pro concorrente. Qual dia desta semana fica melhor pra gente sentar 1 hora e resolver isso?" % N),
    ("8 · Fechar horário (2ª)", "%s, enquanto a gente não senta, seus anúncios seguem trazendo contato que não vira venda. Tenho manhã e tarde nos próximos dias. Qual você prefere?" % N),
    ("9 · Confirmar reunião (Calendly)", "%s, sua reunião com a O Próximo Cliente está marcada. Traz dois números do último mês: quantos contatos chegaram e quantos viraram venda. Com eles a gente já enxerga onde tem dinheiro parado. Confirma pra mim que o horário segue bom?" % N),
    ("10 · Faltou na reunião", "%s, a gente tinha marcado pra olhar por que os contatos não viram cliente, e esse problema continua aí. Qual dia desta semana funciona pra remarcar?" % N),
    ("11 · Reunião cancelada", "%s, vi que a reunião foi cancelada. O problema que te fez marcar não foi cancelado junto. Qual dia desta semana fica melhor pra gente remarcar?" % N),
    ("12 · Quem responde o lead", "Boa! Me conta: hoje, quando um contato chega do anúncio, quem responde e em quanto tempo?"),
    ("13 · Encerrar", "%s, vou encerrar por aqui. Fica uma pergunta: quantos clientes você deixou de fechar este mês porque ninguém respondeu a tempo? Se quiser descobrir, responde esta mensagem." % N),
]


def main():
    L = g.LOC
    ja = {t["name"] for t in g.pedir("GET", "/locations/%s/templates?originId=%s&deleted=false&limit=200" % (L, L)).get("templates", [])}
    for nome, corpo in SNIPPETS:
        if nome in ja:
            print("já existe:", nome)
            continue
        if "--seco" not in sys.argv:
            g.pedir("POST", "/locations/%s/templates" % L,
                    {"name": nome, "type": "sms", "originId": L, "template": {"body": corpo, "attachments": []}})
        print("criado:", nome)
    fim = g.pedir("GET", "/locations/%s/templates?originId=%s&deleted=false&limit=200" % (L, L)).get("templates", [])
    print("total de snippets:", len(fim))


if __name__ == "__main__":
    main()
