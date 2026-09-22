# Conectar o CRM — o caminho que funciona neste ambiente

Descoberta de 18/09/2026, medida e não suposta: **conector do claude.ai não
passa pelo proxy do contêiner; servidor de `.mcp.json` passa.** É por isso que
tudo travou até aqui.

## A assimetria, medida

| Ação | Resultado |
|---|---|
| `curl https://api.cloudflare.com/` de dentro do contêiner | bloqueado |
| Ferramenta MCP do Cloudflare (`workers_list`) | funcionou, listou os Workers reais |
| `curl https://services.leadconnectorhq.com/` | bloqueado |
| Servidor `wesales` do `.mcp.json` | `no rule or allowlist entry allows host services.leadconnectorhq.com` |

Os conectores já ligados nesta conta — Composio, Windsor, Cloudflare, Google
Drive — funcionam porque **quem abre a conexão é a infraestrutura do Claude, não
o contêiner da sessão**. A allowlist de rede do ambiente não se aplica a eles.

Servidor declarado em `.mcp.json` é o oposto: quem conecta é o cliente MCP
rodando dentro do contêiner, e aí a allowlist vale. Por isso o `.mcp.json` foi
removido deste repositório — ele não tinha como funcionar aqui e ainda deixava
um servidor quebrado em toda sessão.

## Antes de criar: já existe um conector pela metade

Verificado em 18/09/2026 no registro de conectores da conta: existe um conector
**`GHL CRM`** com estado **`connect_incomplete`** — criado, nunca finalizado.
`connected: false`, `enabledInChat: false`.

Ou seja, pode não haver nada a criar: basta abrir claude.ai → Configurações →
Conectores → **GHL CRM** e concluir a conexão. Se ele pedir URL e cabeçalhos,
use os do caminho A abaixo.

Na mesma varredura, outros conectores da conta estão em estado incompleto ou
pedindo reconexão: Canva, Clint, Supabase, SUPABASEMETAADS, opsily,
Reap Vídeo IA, Spendflo e Google Calendar. Vale uma passada, porque cada um
deles é uma capacidade que a conta acha que tem e não tem.

## Caminho A — conector do claude.ai com cabeçalho estático

O suporte a **bearer token em conector personalizado** saiu do papel: hoje o
claude.ai aceita cabeçalhos estáticos (`static_headers`), em beta. O
administrador informa a credencial uma vez e o Claude a envia em toda
requisição. Nomes padrão como `authorization` passam direto.

**claude.ai → Configurações → Conectores → Adicionar conector personalizado**

| Campo | Valor |
|---|---|
| URL | `https://services.leadconnectorhq.com/mcp/` |
| Cabeçalho | `Authorization: Bearer pit-...` |
| Cabeçalho | `locationId: 1D53YTI9C7oIMBavcQxV` |
| Cabeçalho | `Version: 2021-07-28` |

Sem OAuth, sem app de marketplace, sem e-mail de aprovação, sem mexer em
allowlist de rede. E como é conector de conta, vale para qualquer sessão, em
qualquer repositório.

Se a sua conta ainda não mostrar campo de cabeçalho (o recurso é beta e pode
exigir administrador da organização), vá para o caminho B.

## Caminho B — MCP próprio hospedado, e o conector aponta para ele

Existem servidores MCP de GoHighLevel open source com deploy de um clique em
Railway, Render ou Vercel. O token fica como variável de ambiente **no serviço**,
e o conector do claude.ai aponta para a URL pública — que, por ser conector de
conta, também não passa pelo proxy do contêiner.

1. Deploy de [mastanley13/GoHighLevel-MCP](https://github.com/mastanley13/GoHighLevel-MCP)
   no Railway (template pronto em `railway.com/deploy/ghl-mcp`)
2. Variáveis do serviço: o token `pit-` e o Location ID
3. Copiar a URL pública e acrescentar `/mcp`
4. claude.ai → Conectores → Adicionar conector personalizado → colar a URL

Mais peças para manter, mas funciona com a interface de conector de hoje, sem
depender do beta de cabeçalhos.

## Caminho C — liberar o host na allowlist

Se preferir manter o `.mcp.json`, o conserto é liberar
`services.leadconnectorhq.com` na política de rede do ambiente. Aí o arquivo
abaixo volta a fazer sentido e o servidor sobe dentro do contêiner:

```json
{
  "mcpServers": {
    "wesales": {
      "type": "http",
      "url": "https://services.leadconnectorhq.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${WESALES_PIT}",
        "locationId": "1D53YTI9C7oIMBavcQxV",
        "Version": "2021-07-28"
      }
    }
  }
}
```

## O token

Subconta → **Settings → Private Integrations → Create New Integration**.

**Armadilha:** a aba "Escopos" nasce bloqueada. Não é permissão — é passo a
passo. Preencha o nome, role a página e clique em **Próximo**, no canto
inferior direito. Só então os escopos abrem.

Escopos: Locations (ver), Contacts, Custom Fields, Tags, Opportunities,
Conversations, Tasks (ver e editar), Calendars, Forms, Workflows (ver).

O token começa com `pit-` e só aparece uma vez. Chave de API comum ou v1 não
funciona — é a causa nº 1 de erro 401. Cada token vale para uma subconta.
Revogar é apagar a integração.

O Location ID desta subconta é `1D53YTI9C7oIMBavcQxV` — está na própria URL do
CRM, não é segredo e não serve para nada sem o token.

## Quando der 403 — medido em 22/09/2026

Um `403` do conector **não** significa, por si só, que o token perdeu acesso.
Medido na mesma sessão, na mesma subconta, com o mesmo token:

| Chamada | `locationId` no parâmetro | Resposta |
|---|---|---|
| `locations_get-custom-fields` | ausente | `403` — `The token does not have access to this location.` |
| `locations_get-location` | ausente | `403` — `Forbidden resource` |
| `opportunities_get-pipelines` | ausente | `422` — `locationId can't be undefined` |
| `opportunities_get-pipelines` | `1D53YTI9C7oIMBavcQxV` | `200` |
| `locations_get-custom-fields` | `1D53YTI9C7oIMBavcQxV` (+ `model: all`) | `200`, 51 campos |

A terceira linha é a prova: a **mesma** ausência de `locationId` que um
endpoint de `opportunities` reporta como `422` explícito, um endpoint de
`locations` reporta como `403` de permissão. O texto do `403` descreve a
consequência, não a causa — e o cabeçalho `locationId` do conector não
substitui o parâmetro na chamada quando a ferramenta o exige.

**Procedimento, nesta ordem:**

1. Repita a chamada com `locationId: 1D53YTI9C7oIMBavcQxV` explícito.
2. Voltou `200` → era resolução de location. Passe `locationId` em **todas**
   as chamadas daquela sessão e siga.
3. Continua `403` → aí sim suspeite do token (revogado, rotacionado, ou
   integração apagada). Confirme na subconta em **Settings → Private
   Integrations**.

Importa porque os dois casos são indistinguíveis pela mensagem, e um token
rotacionado responde igual — confundir os dois custa uma rodada inteira de
diagnóstico errado em qualquer direção.

**Armadilhas de parâmetro, medidas junto:** o `model` de
`locations_get-custom-fields` é o modelo de **dado** do campo (`contact`,
`opportunity`, `all`, `business`, `task`), não um modelo de linguagem; e
`opportunities_get-pipelines` **recusa** `model` como propriedade
desconhecida.

## Depois de conectar

Conversa nova e:

> roda a Etapa 1 do wesales/auditoria-etapa1.md

## Fontes

- [Authentication for connectors — Claude docs](https://claude.com/docs/connectors/building/authentication)
- [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [mastanley13/GoHighLevel-MCP](https://github.com/mastanley13/GoHighLevel-MCP)
- [Deploy GHL MCP no Railway](https://railway.com/deploy/ghl-mcp)
- [Deploying Claude Connectors to Production](https://sunpeak.ai/blogs/deploying-claude-connectors/)
- [Private Integrations Token — HighLevel](https://marketplace.gohighlevel.com/docs/Authorization/PrivateIntegrationsToken/)
