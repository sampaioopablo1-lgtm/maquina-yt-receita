# Proposta — uma reunião agendada por dia útil

*14/09/2026. Pedido do Pablo: "encontre de fato a proposta que agenda reuniões todos os dias".*
*Meta: 22 reuniões/mês. Tudo abaixo é conta, não promessa — as taxas são de mercado até o funil ter as dele.*

## A conta de trás pra frente

Uma reunião por dia exige, por canal, este volume:

| Canal | Taxa até a reunião | Volume pra 1/dia | Custo/dia | A lista de 2.000 dura |
|---|---|---|---|---|
| E-mail frio (cadência de 5 já pronta) | 0,4% por prospect (a conta da própria cadência) | **50 prospects novos/dia** | R$ 0 além do já orçado | 40 dias |
| WhatsApp template oficial | ~10% respondem × ~25% agendam = 2,5% | **40 envios/dia** | R$ 12 (R$ 264/mês) | 50 dias |
| Formulário de lead (anúncio, rodando) | 20 leads em 14 dias = 1,4/dia; IA qualifica, ~40% agendam | precisa de **2,5 leads/dia** | ~R$ 20 (hoje gasta ~R$ 17) | não depende de lista |
| Lista comercial do app (250 grátis/mês) | 2,5% | 250/mês = 6 reuniões/mês | R$ 0 | 8 meses |

Nenhum canal sozinho dá 1/dia sem apertar. **Somando três, dá com folga.**

## A proposta

```
E-MAIL       50/dia da base de 2.000, com link wa.me no toque 3   → ~1,0 reunião/dia
WHATSAPP     30/dia template oficial (os que não têm e-mail)      → ~0,75/dia
FORMULÁRIO   anúncio como está, IA qualifica na resposta          → ~0,5/dia
                                                                  ─────────────────
                                                                  ~2 reuniões/dia na conta
                                                                  → 1/dia com metade da taxa
```

A conta foi feita pra sobrar. Se as taxas reais forem metade das de mercado, ainda fecha 1/dia.

## Custo

| | |
|---|---|
| E-mail | já orçado na cadência |
| WhatsApp 30/dia | R$ 198/mês |
| Anúncio | o que já roda (~R$ 500/mês) |
| IA + n8n | R$ 50 a 90 |
| **Total novo** | **~R$ 250 a 290/mês** |

Custo por reunião, se der 22/mês com tudo somado: **~R$ 35**. Um SDR humano custa R$ 4.000+.

## O problema que aparece no dia 40

A lista de 2.000 acaba. E-mail a 50/dia mais WhatsApp a 30/dia consomem 80 contatos por dia útil.
**Sem combustível novo, a máquina para em 5 a 6 semanas.**

Combustível que já existe:
- as varreduras da Biblioteca de Anúncios (a `LISTA — clinicas do Rio` já tem dezenas de empresas
  que anunciam e erram — a melhor prova que existe pra abrir conversa)
- base de CNPJ por nicho e bairro (LeadCNPJ tem 69M, Econodata idem, a partir de R$ 137/mês)

Ou seja: a lista de 2.000 é a partida, não o motor. O motor é **50 a 80 contatos novos por dia**,
que hoje eu já tiro da Biblioteca a cada rodada horária.

## O que decide se dá 1/dia ou 0,3/dia

Não é o volume. É a mensagem. Genérica responde 1-5%. Com a prova específica da empresa
("seu anúncio no ar desde novembro de 2024 leva pra um link quebrado") responde 15-25%.
Por isso a Camada 1 da arquitetura existe: cruzar cada contato com a Biblioteca antes de mandar.

## O que o Pablo faz

1. Manda o CSV. **É o único bloqueio real de tudo acima.**
2. Confirma o número atual em coexistência.
3. Verifica o Meta Business e habilita a Cloud API (destrava os 30/dia de WhatsApp).
4. Atende as reuniões.

## O que eu faço, na ordem

| Semana | Entrega | Reuniões esperadas |
|---|---|---|
| 1 | base limpa, classificada, cruzada com a Biblioteca; cadência de e-mail no ar a 50/dia | primeiras respostas |
| 2 | n8n + agente de conversa; IA atende o formulário | 0,5/dia |
| 3 | Cloud API em coexistência; template aprovado; 30/dia de WhatsApp | 1/dia |
| 4 | auto-stop, relatório diário, combustível novo da Biblioteca entrando | 1 a 2/dia |
