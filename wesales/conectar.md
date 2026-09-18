# Conectar sem OAuth, sem marketplace, sem e-mail de aprovação

Este é o caminho curto. Ele não passa pelo app do marketplace, não abre tela de
autorização e **não depende de e-mail nenhum**. É o que a comunidade que liga
GoHighLevel ao Claude Code usa no dia a dia.

## Por que o outro caminho travou

O app `lc-mcp - Anthropic` é um app **público de marketplace**: instalar exige
o fluxo OAuth completo, com tela de consentimento, escolha de subconta e, em
várias contas, verificação por e-mail. Se esse e-mail não chega — e no seu caso
não chegou — não existe o que clicar. A página fica de pé e nada avança.

O Private Integration Token não tem nada disso. Ele nasce dentro da sua própria
subconta, na hora, e é seu.

## O que você faz (uma vez, ~3 minutos)

### 1. Criar o token na subconta

Subconta da WeSales → **Settings → Private Integrations → Create New Integration**

Nome: `Claude Code SDR`

Escopos a marcar:

| Área | Acesso |
|---|---|
| Locations | Ver |
| Contacts | Ver e editar |
| Custom Fields | Ver e editar |
| Tags | Ver e editar |
| Opportunities | Ver e editar |
| Calendars | Ver |
| Conversations | Ver e editar |
| Tasks | Ver e editar |
| Forms | Ver |
| Workflows | Ver |

Clique em criar e **copie o token na hora** — ele começa com `pit-` e só
aparece uma vez. Se perder, cria outro; não tem problema.

### 2. Pegar o Location ID

Subconta → **Settings → Business Profile**. É o código com letras e números.
(Também aparece no meio da URL quando você está dentro da subconta.)

### 3. Guardar os dois como variáveis de ambiente

Nas configurações do ambiente do Claude Code (o mesmo lugar onde ficam as
outras chaves do projeto), crie:

```
WESALES_PIT=pit-...................
WESALES_LOCATION_ID=..............
```

**O token não entra no repositório.** O `.mcp.json` versionado referencia só o
nome da variável.

### 4. Abrir uma conversa nova

Servidor MCP carrega no início da sessão. Na conversa nova, escreva:

> roda a Etapa 1 do wesales/auditoria-etapa1.md

## O que já está pronto do meu lado

O `.mcp.json` na raiz do repositório, commitado:

```json
{
  "mcpServers": {
    "wesales": {
      "type": "http",
      "url": "https://services.leadconnectorhq.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${WESALES_PIT}",
        "locationId": "${WESALES_LOCATION_ID}",
        "Version": "2021-07-28"
      }
    }
  }
}
```

Sessão do Claude Code na nuvem carrega servidor de `.mcp.json` **sem pedir
confirmação** — é sessão não interativa. Então, com as duas variáveis
definidas, a próxima sessão já nasce conectada.

## Detalhes que evitam dor de cabeça

- **Tem que ser o token `pit-`.** Chave de API comum ou de v1 não funciona e é
  a causa nº 1 de erro 401 nesse setup.
- **Um token por subconta.** Cada PIT fica preso a uma location. Para uma
  segunda subconta, outro token e outra entrada no `.mcp.json`.
- **O cabeçalho `Version: 2021-07-28`** é o que a API v2 espera. Sem ele,
  algumas rotas respondem errado.
- **Se `WESALES_PIT` ficar vazio**, o servidor aparece quebrado em toda sessão
  deste repositório. Não estraga nada, mas polui. Se você desistir do caminho,
  é só apagar o `.mcp.json`.
- **Revogar é fácil:** Settings → Private Integrations → apagar a integração.
  Corta o acesso na hora, sem mexer em mais nada.

## E se você preferir o OAuth depois

O caminho do conector personalizado continua valendo, e é melhor para
multi-conta: claude.ai → Configurações → Conectores → Adicionar conector
personalizado → `https://services.leadconnectorhq.com/mcp/anthropic/v2`.
Os dois podem coexistir. Mas para sair do zero hoje, o PIT é o mais curto.
