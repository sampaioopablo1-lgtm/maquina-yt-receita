# Agente de WhatsApp — uazapi + Flask + Gemini (grátis)

Responde no WhatsApp do Pablo pelo roteiro de `prompt.md`: se identifica como assistente, qualifica, manda o Calendly pro cliente certo, e devolve pro Pablo (avisando no WhatsApp dele) quando sai do roteiro. Junta mensagens em sequência num turno só e responde em várias mensagens com "digitando". Construído conforme a documentação enviada (`base-conhecimento/`).

> **Aviso, uma vez:** a uazapi conecta por QR Code (não é a API oficial da Meta). Desde jan/2026 a Meta detecta esse tipo de conexão e pode restringir o número. Este agente **só responde** — nunca inicia conversa — o que é o uso de menor risco, mas o risco existe e é do número conectado. A versão oficial (Cloud API) está em `maquina-whatsapp/` e `infra/cf-whatsapp/`.

## Rodar
1. `pip install -r requirements.txt`
2. `cp .env.example .env` e preencher. `GEMINI_API_KEY` é grátis em https://aistudio.google.com/apikey.
3. `python app.py`
4. Expor: `ngrok http 5000`
5. Webhook na uazapi (seção "ENDPOINTS — WEBHOOK" do `llms-uazapi.txt`):
```
curl -X PUT "$UAZAPI_BASE_URL/webhook" -H "token: $UAZAPI_INSTANCE_TOKEN" -H "Content-Type: application/json" \
  -d '{"webhookUrl":"https://SEU-NGROK.ngrok.io/webhook","events":["message"]}'
```
6. Mandar "oi" de outro celular.

## Adicionando tools no futuro
`llm.py` já recebe `tools`. Passe `tools=[types.Tool(function_declarations=[...])]` e trate `response.candidates[0].content.parts` procurando `part.function_call`. Hoje o agendamento e a devolução pro humano vão pelo prompt (link direto e marcador `#HUMANO`), sem function calling.

## Expandindo (ver `llms-uazapi.txt`)
Receber mídia (`/send/download-media`) · enviar imagem/áudio (`/send/image`, `/send/audio`) · botões (`/send/menu`) · grupos.

## Exemplo de log de um fluxo
```
[webhook] event=message from=5521999999999
[buffer] flush user=5521999999999 msgs=2
[llm] reply len=412
[uazapi] POST /send/presence -> composing
[uazapi] POST /send/text (1/3)
[uazapi] POST /send/text (2/3)
[uazapi] POST /send/text (3/3)
[uazapi] POST /send/presence -> paused
```
