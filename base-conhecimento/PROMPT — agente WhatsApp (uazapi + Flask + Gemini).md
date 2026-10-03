# PROMPT — Agente de IA no WhatsApp via uazapi (Flask + Gemini)

*Enviado pelo Pablo em 14/09/2026. Prompt pronto para construir o MVP do agente.*
*Documentação de apoio: `base-conhecimento/uazapi — llms.txt`.*
*Leia antes o `README.md` desta pasta: a uazapi é API **não oficial** e isso muda onde este agente pode ser usado com segurança.*

---

PROMPT
# 🎯 TAREFA: Agente de IA no WhatsApp via UAZAPI (Flask, Python)
Você é um engenheiro Python sênior. Construa uma aplicação **Flask mínima, funcional e pronta pra rodar** que conecta o WhatsApp (via UAZAPI) a um LLM (**Google Gemini 2.5 Flash**), com **buffer de mensagens com debounce configurável** e **envio de respostas separadas em múltiplas mensagens**.
## 📚 Documentação anexa
Você recebeu o arquivo **`llms-uazapi.txt`** junto com este prompt. Ele contém a documentação completa da UAZAPI adaptada pra LLMs: todos os endpoints (instâncias, mensagens, mídia, grupos, contatos, campanhas), formatos de payload, estrutura de webhook, eventos e exemplos.
**Regras de uso da doc:**
- Para o MVP descrito abaixo, você só precisa de 3 endpoints (`/send/text`, `/send/presence`, `/send/read`) e do payload de webhook `event=message` — já resumidos aqui no prompt.
- **Consulte `llms-uazapi.txt`** sempre que: (a) tiver dúvida sobre algum campo ou comportamento, (b) precisar escrever o README explicando como configurar o webhook na UAZAPI, (c) for adicionar suporte futuro a mídia, grupos, botões interativos, etc.
- Não invente endpoints nem campos — se algo não está no doc, não existe.
## 🧭 Princípios não-negociáveis
- **KISS extremo**: código óbvio, curto, sem abstrações desnecessárias.
- **Zero infra externa**: sem Redis, sem banco, sem Celery. Tudo em memória + `threading`.
- **Arquitetura pronta pra receber tools (function calling do Gemini) depois**, mas **sem tools agora** — apenas o parâmetro existe e fica `None`.
- **Código total < 400 linhas** somando todos os arquivos.
## 📦 Stack
- Python 3.11+
- `flask`, `requests`, `google-genai`, `python-dotenv`
> ⚠️ Use o SDK **novo e unificado** `google-genai` (`pip install google-genai`), **não** o antigo `google-generativeai`. Import: `from google import genai`.
## 📁 Estrutura de arquivos
```
.
├── app.py            # Flask + rota /webhook + pipeline de flush
├── uazapi.py         # cliente UAZAPI (send_text, send_presence, mark_read)
├── llm.py            # cliente Gemini (generate_reply com hook pra tools)
├── buffer.py         # debounce buffer por usuário (threading.Timer)
├── memory.py         # histórico de conversa por usuário (dict + lock)
├── requirements.txt
├── .env.example
└── README.md
```
## 🔐 Variáveis de ambiente (.env.example)
```
UAZAPI_BASE_URL=https://seudominio.uazapi.com
UAZAPI_INSTANCE_TOKEN=cole_o_token_da_instancia_aqui
GEMINI_API_KEY=cole_a_api_key_do_aistudio_aqui
GEMINI_MODEL=gemini-2.5-flash
BUFFER_SECONDS=8
MAX_HISTORY=20
SYSTEM_PROMPT=Você é um assistente útil que responde no WhatsApp. Seja breve, natural, use quebras de parágrafo (\n\n) quando fizer sentido dividir ideias.
PORT=5000
```
## 🔁 Fluxo end-to-end (decore esse fluxo)
1. UAZAPI faz `POST /webhook` no seu Flask com um evento `message`.
2. App **ignora** se: `fromMe=true`, `isGroup=true`, ou `type != "text"`.
3. App chama `uazapi.mark_read(number, message_id)`.
4. App joga o texto no **buffer do remetente**.
5. Buffer espera `BUFFER_SECONDS` **desde a última mensagem** (debounce: cada msg nova reseta o timer).
6. Quando o timer dispara, `flush(user)` executa:
   - Envia `presence=composing` (digitando)
   - Concatena as mensagens bufferizadas em **um único turno `user`** (separadas por `\n`)
   - Acrescenta ao histórico do usuário
   - Chama `llm.generate_reply(history, system, tools=None)`
   - Acrescenta a resposta ao histórico (role `"model"`)
   - **Divide a resposta em chunks** e envia cada um como mensagem separada via UAZAPI, com `composing` entre elas e `time.sleep(1 + len(chunk)/200)` simulando digitação humana
   - Envia `presence=paused` no fim
## 🧱 Detalhamento dos módulos
### `uazapi.py`
Três funções síncronas puras (referência completa dos endpoints na seção "ENDPOINTS — ENVIAR MENSAGEM" do `llms-uazapi.txt`). Todas usam header `{"token": UAZAPI_INSTANCE_TOKEN, "Content-Type": "application/json"}`. Em erro HTTP: `print` curto e segue — **não levanta exceção**.
| Função | Método/Endpoint | Body |
|---|---|---|
| `send_text(number, text)` | `POST /send/text` | `{"number": "...", "text": "..."}` |
| `send_presence(number, presence)` | `POST /send/presence` | `{"number": "...", "presence": "composing"\|"paused"}` |
| `mark_read(number, message_id)` | `PUT /send/read` | `{"number": "...", "messageId": "..."}` |
### `llm.py`
```python
from google import genai
from google.genai import types
_client = genai.Client(api_key=GEMINI_API_KEY)
def generate_reply(history: list[dict], system: str, tools: list | None = None) -> str:
    """Chama Gemini generate_content. tools=None hoje; preparado pra function calling depois."""
    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=1024,
        tools=tools,  # None hoje
    )
    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=history,
        config=config,
    )
    # TODO: handle function_call parts quando tools for usado
    return (response.text or "").strip()
```
### `memory.py`
Dict global `{number: [{"role": "user"|"model", "parts": [{"text": "..."}]}, ...]}` protegido por `threading.Lock`.
> ⚠️ Use **`"model"`** (não `"assistant"`) e estrutura **`parts: [{"text": ...}]`** — é o formato nativo do Gemini, evita conversões.
Funções:
- `append(user, role, text)` — monta `{"role": role, "parts": [{"text": text}]}`
- `get(user) -> list` — retorna o histórico pronto pra mandar pro Gemini
- `reset(user)`
- Trunca pra manter no máximo `MAX_HISTORY` mensagens (do mais recente).
### `buffer.py`
Para cada usuário, mantém:
- Lista de strings pendentes
- Um `threading.Timer` ativo (ou None)
API:
```python
class MessageBuffer:
    def __init__(self, wait_seconds: float, on_flush: Callable[[str, list[str]], None]): ...
    def add(self, user: str, text: str) -> None:
        # com lock: append à lista, cancela timer anterior, cria novo Timer(wait_seconds, self._flush, [user])
```
`_flush(user)` retira a lista pendente, limpa o estado do usuário e chama `on_flush(user, texts)` numa thread (já está numa, ok). Tudo sob `threading.Lock`.
### `app.py`
- `load_dotenv()` no topo
- Instancia `MessageBuffer(BUFFER_SECONDS, on_flush=handle_flush)`
- `GET /` → retorna `"ok"` (healthcheck)
- `POST /webhook` → parse JSON, valida, extrai `number = data["from"].split("@")[0]`, chama `mark_read`, `buffer.add(number, body)`, retorna `{"ok": true}` em < 100ms (não bloqueia)
- `handle_flush(user, texts)`:
```
  send_presence(user, "composing")
  user_turn = "\n".join(texts)
  memory.append(user, "user", user_turn)
  reply = llm.generate_reply(memory.get(user), SYSTEM_PROMPT)
  memory.append(user, "model", reply)
  for chunk in split_reply(reply):
      send_presence(user, "composing")
      time.sleep(1 + len(chunk) / 200)
      send_text(user, chunk)
  send_presence(user, "paused")
```
- `split_reply(text)`: split por `\n\n`; se algum pedaço > 800 chars, quebra por `. ` (mantendo o ponto). Remove strings vazias.
- `if __name__ == "__main__": app.run(host="0.0.0.0", port=PORT)`
## 📨 Payload de webhook (referência rápida — detalhes completos em `llms-uazapi.txt`, seção "WEBHOOK — CONFIGURAÇÃO E EVENTOS")
```json
{
  "event": "message",
  "data": {
    "id": "ABCDEF123",
    "from": "5511999999999@s.whatsapp.net",
    "fromMe": false,
    "body": "Oi, tudo bem?",
    "type": "text",
    "pushName": "João",
    "isGroup": false
  }
}
```
Extrair `number` removendo `@s.whatsapp.net`. Ignorar qualquer evento que não seja `event == "message"`.
## 📝 README.md (escreva também)
Deve conter, em ordem:
1. O que é (3 linhas)
2. `pip install -r requirements.txt`
3. `cp .env.example .env` e preencher (mencionar que `GEMINI_API_KEY` se obtém grátis em https://aistudio.google.com/apikey)
4. `python app.py`
5. Expor com `ngrok http 5000`
6. Configurar webhook na UAZAPI — **consulte `llms-uazapi.txt` seção "ENDPOINTS — WEBHOOK"** e gere o `curl` pronto: `PUT {UAZAPI_BASE_URL}/webhook` com body `{"webhookUrl": "https://SEU-NGROK.ngrok.io/webhook", "events": ["message"]}` e header `token: <INSTANCE_TOKEN>`
7. Seção **"Adicionando tools no futuro"** — apontar pro `llm.py` onde o `tools` param já existe; explicar que basta passar `tools=[types.Tool(function_declarations=[...])]` e tratar `response.candidates[0].content.parts` procurando `part.function_call`
8. Seção **"Expandindo features"** — lista curta apontando pro `llms-uazapi.txt` pra: receber mídia (`/send/download-media`), enviar imagem/áudio (`/send/image`, `/send/audio`), botões interativos (`/send/menu`), suporte a grupos, etc.
## ✅ Definição de pronto
- `pip install -r requirements.txt && python app.py` sobe sem erros
- `python -m py_compile app.py uazapi.py llm.py buffer.py memory.py` passa limpo
- Mensagens recebidas em janela de `BUFFER_SECONDS` viram **um único turno** pro Gemini
- Resposta do Gemini chega no WhatsApp **dividida em mensagens separadas** com indicador de "digitando" entre elas
- Histórico por usuário é mantido entre turnos (mesma execução do processo)
- Código total < 400 linhas
## 🚫 Restrições explícitas
- Nada de `async`/`await` — `threading` resolve
- Nada de Blueprints, Flask-RESTful, classes além de `MessageBuffer`
- Nada de SQLite ou arquivo de persistência — perder histórico no restart é OK
- Não logar payloads inteiros — só `print` curtos tipo `[buffer] flush user=5511999 msgs=3` e `[llm] reply len=412`
- Não implementar tools agora, só deixar o parâmetro pronto
- **Não use o SDK antigo `google-generativeai`** — só o novo `google-genai`
- **Não invente endpoints da UAZAPI** — qualquer coisa fora dos 3 endpoints do MVP, confirme em `llms-uazapi.txt` antes
## 🎬 Entrega
Escreva **todos os arquivos completos** (sem `...` ou TODOs além do explícito em `llm.py`). Ao final, mostre um exemplo simulado dos logs do fluxo completo: webhook recebido → buffer espera → flush → Gemini → 3 mensagens enviadas.
