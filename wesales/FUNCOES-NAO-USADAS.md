# Funções do GHL que a conta não usa — medido em 27/09 21:25

Fonte: `tools/inventario_ghl.py` (Action `inventario`, run 36351678934). Só leitura, pela API
pública. **A API não enxerga** Call Center/Power dialer, gatilhos do discador, Smart Lists,
dashboards, Email Services e configurações de telefone da tela; o que foi feito lá não
aparece aqui e não é tratado como faltando.

## Achados que afetam terça 29/09

| # | Achado (medido) | Por que importa | Sugestão |
|---|---|---|---|
| 1 | Governador do WhatsApp: a Action só roda a partir do branch padrão, e as travas `wa-aguardando` não estão na lista do que a sessão do PC gravou | sem as travas, o limite de 15/dia não vale; o MI-0 de seg 08:30 sai para todos de uma vez | gravar as travas antes de seg 08:30 **e** levar a Action para o branch padrão |
| 2 | Snippets: 0 de SMS, 0 de WhatsApp, 0 de e-mail | o que passa de 15/dia vira manual; a SDR vai digitar tudo | criar snippets com os 20 textos do `COPY-WHATSAPP.md` (atalho `/` na conversa) |
| 3 | Número +55 11 5026-6034: só voz, `forwardingNumber` vazio, `inboundCallService` nulo | o lead que retorna a ligação perdida do Power pode cair no vazio | na tela Phone System: encaminhar para o celular da SDR ou pôr correio de voz |
| 4 | Calendário: texto de consentimento em inglês, `allowBookingAfter = 0`, `notifications = []` | lead vê inglês no agendamento; pode marcar para daqui a 5 min; closer não recebe aviso nativo | traduzir o consentimento; antecedência mínima de 2–3 h; ligar aviso ao closer |
| 5 | 2 links de gatilho "Agendar com o closer" (URLs diferentes, mesmo calendário) | relatório de clique dividido em dois | usar um só nas mensagens; o outro fica sem uso (não apagar sem conferir) |
| 6 | Assinatura da subconta `trialing` | trial que vence pausa a conta | conferir a data de fim do trial no painel da agência |

## Não usado, sem efeito em terça (decisão do dono)

- Valores personalizados: 0. Nome da empresa, link de reunião e nome do closer estão escritos à mão em 42 textos.
- Propostas e contratos: 0, com a etapa FORMALIZAR no funil. Serve para o closer mandar proposta e contrato com assinatura.
- Produtos, faturas, pagamentos: 0 e nenhum provedor ligado.
- Empresas (Companies): 0. O campo `Empresa` está vazio em 64 de 64 contatos.
- Modelos de e-mail do builder: 3 com nome genérico ("Email Template 1/2/3").
- Perfil da conta: site e redes sociais vazios (aparecem no rodapé do e-mail).
- Social Planner: só a página do Facebook, nenhum post. Funis/sites, blogs, pesquisas, cursos: 0.
- Base de conhecimento, Conversation AI, Voice AI: ficam desligados, pela regra de não usar IA paga.
