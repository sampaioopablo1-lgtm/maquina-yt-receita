# Máquina de WhatsApp — agente que qualifica e agenda

Responde no WhatsApp do Pablo pela **API oficial da Meta (Cloud API), em coexistência com o número atual**. Quem escreve — vindo de formulário, e-mail, link `wa.me` ou anúncio — é atendido pelo assistente, que segue o roteiro do `prompt.md`, qualifica e manda o link do Calendly. Quando a conversa sai do roteiro, devolve pro Pablo e avisa no WhatsApp dele.

**Só responde. Nunca manda a primeira mensagem.** Sem QR Code, sem chip, sem risco de banimento.

## Arquivos
- `app.py` — webhook (verificação + recebimento), assinatura, fila
- `buffer.py` — junta mensagens em sequência (8 s de espera desde a última)
- `memory.py` — histórico por contato, em memória
- `llm.py` — Claude com duas ferramentas: `agendar_reuniao`, `passar_para_humano`
- `whatsapp.py` — envio, "lida", "digitando", resposta em várias mensagens
- `prompt.md` — o roteiro (edite aqui, não no código)
- `leads.jsonl` — gerado em produção: reuniões oferecidas e devoluções

## O que o Pablo precisa fazer uma vez (≈ 30 min)
1. **Meta for Developers** → criar app do tipo *Business* → adicionar o produto **WhatsApp**.
2. **Coexistência**: em WhatsApp → Configuração da API → *Conectar número existente do WhatsApp Business* → seguir o fluxo no celular (o app continua funcionando).
3. Copiar `WA_PHONE_NUMBER_ID` e gerar um **token permanente** (Business Settings → System Users → Add → token com `whatsapp_business_messaging` e `whatsapp_business_management`) → `WA_TOKEN`.
4. Copiar o **App Secret** (Configurações do app → Básico) → `WA_APP_SECRET`.
5. Subir este serviço (abaixo) e, em WhatsApp → Configuração → Webhooks, cadastrar `https://SEU-DOMINIO/webhook` com o `WA_VERIFY_TOKEN` que você inventou; assinar o campo **messages**.
6. `ANTHROPIC_API_KEY` em console.anthropic.com.

## Subir (Railway, Render ou VPS)
```
cp .env.example .env   # preencher
docker build -t maquina-whatsapp . && docker run --env-file .env -p 5000:5000 maquina-whatsapp
```
Sem Docker: `pip install -r requirements.txt && python app.py`.

## Custo
- WhatsApp: R$ 0 — quem escreve primeiro abre a janela de atendimento (até 30/09 ilimitada; a partir de 01/10, 1.000 mensagens grátis por mês no número).
- Claude: ~R$ 0,10 a 0,30 por conversa completa.
- Servidor: R$ 0 (Railway/Render free) a R$ 30/mês.

## O que ainda não faz (de propósito, por enquanto)
- Não cria evento no Google Agenda: o Calendly faz isso ao marcar.
- Não grava no Clint: quando o conector voltar, o `leads.jsonl` vira a fonte.
- Não responde mídia (áudio, imagem): só texto. Quem mandar áudio recebe silêncio; próxima versão.
