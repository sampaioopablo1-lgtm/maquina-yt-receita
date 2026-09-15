# AgendouAI — API pública v1 (resumo)

Base: `https://api.agendou.io/api/public/v1` · header `X-API-Key: lk_...` · chave criada em "API Keys" (só admin).
**Status daqui: bloqueado pelo proxy da sessão (CONNECT 403).** Usar só em ferramenta externa (n8n, Make, script no PC do Pablo).
Plano Starter: 60 req/min, 1.000/dia.

| Endpoint | Pra quê |
|---|---|
| `GET /agendamentos?data_inicio&data_fim&status` | listar reuniões marcadas pela IA (nome, telefone, data_hora, status) |
| `GET /agendamentos/:id` | detalhe + `google_event_link` |
| `POST /agendamentos` | marcar reunião (precisa `profissional_id`, `servico_id`, `cliente_telefone`, `data_hora`) — cria evento no Google Calendar |
| `PUT /agendamentos/:id` | mudar hora/status (agendado, confirmado, concluido, cancelado, perdido) |
| `DELETE /agendamentos/:id` | cancelar (soft delete) |
| `GET /profissionais` · `GET /servicos` | ids necessários pro POST |
| `GET /horarios-disponiveis?profissional_id&servico_id&data` | horários livres |
| `GET/POST /clientes` | upsert por telefone |
| `POST /webhook/chatbot` | `{telefone, mensagem, acao: agendar|consultar|cancelar|transferir}` → a IA responde |

## Onde isso seria útil (quando houver ferramenta fora do proxy)
1. **Lead do formulário Meta → Agendou:** `POST /clientes` com nome+telefone, e a IA já sabe quem é quando a pessoa chamar no zap.
2. **Métrica do teste (custo por reunião):** `GET /agendamentos` por período, cruzado com gasto do Meta. Hoje faço o mesmo lendo o Google Calendar.
3. **Status "concluido/perdido":** marcar depois da reunião pra medir comparecimento.

Fonte de verdade enquanto a API estiver inacessível: **Google Calendar** (o Agendou grava lá).
