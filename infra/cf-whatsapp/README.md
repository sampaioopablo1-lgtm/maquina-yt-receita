# opc-whatsapp — agente de WhatsApp como Cloudflare Worker

Mesmo agente da pasta `maquina-whatsapp/` (Flask), portado pro Cloudflare, que o Pablo já usa. Grátis, sem servidor, publica sozinho a cada push nesta pasta.

**Aproveita o que já existe:** app **OPC Automação** (`2159128187972575`), usuário do sistema **Integracao** (token `META_ACCESS_TOKEN`), a página com o WhatsApp vinculado, e a conta Cloudflare.

## Ligar (uma vez)
1. **Meta for Developers → app OPC Automação → Adicionar produto → WhatsApp.** Em *Configuração da API*, escolher o número já vinculado à página (coexistência). Copiar o **Phone Number ID**.
2. **Token:** Business → Usuários do sistema → Integracao → Gerar token → marcar também `whatsapp_business_messaging` e `whatsapp_business_management`. (Se o token atual já tem, pula.)
3. **Cloudflare → Workers & Pages → Create → Import a repository → `maquina-yt-receita`**:
   - Project name `opc-whatsapp` · Branch `claude/opc-pablo-reel-ryxld4` · Root directory `infra/cf-whatsapp` · Deploy command `npx wrangler deploy`.
4. **Worker → Settings → Variables and Secrets** (tipo Secret): `META_ACCESS_TOKEN`, `WA_PHONE_NUMBER_ID`, `WA_VERIFY_TOKEN` (uma senha que você inventa), `WA_APP_SECRET` (app → Configurações → Básico), `ANTHROPIC_API_KEY`. Depois **Redeploy**.
5. **Meta → app → WhatsApp → Configuração → Webhooks:** URL `https://opc-whatsapp.<sua-conta>.workers.dev/webhook`, token de verificação = o `WA_VERIFY_TOKEN`, assinar **messages**.
6. Mandar um "oi" de outro celular.

## Como funciona
Mensagem chega → marca lida + "digitando" → espera 8 s juntando o que vier → Claude (roteiro em `prompt.md`) → responde em blocos → se for o cliente certo manda o Calendly com o nome preenchido → se sair do roteiro, devolve pro Pablo (avisa no WhatsApp dele) e para.

Histórico e registros ficam no KV `opc-whatsapp` (chaves `hist:`, `pause:`, `lead:`). Pra editar o roteiro: mudar `prompt.md` e rodar `python3 gerar_prompt.py`.
