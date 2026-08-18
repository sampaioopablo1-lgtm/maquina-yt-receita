# Jazz Imobiliária — feed dos portais

**Este diretório é do projeto da JAZZ IMOBILIÁRIA, não da máquina de YouTube.**
Os dois projetos dividem este repositório por herança histórica; a fronteira
é esta pasta. Nada aqui toca canais, vozes, produção ou publicação de vídeo
da máquina — e nada da máquina deve importar daqui.

## O que vive aqui

- `supabase/migrations/` — migrações do projeto Supabase da Jazz
  (`cscczluzpblzhvojxanp`), aplicadas via MCP. Feed VRSync, captação,
  geocode, vigias, tours, descrições.
- `supabase/functions/` — Edge Functions da Jazz (visita virtual, tour 360,
  gerador de XML smart-feed-nativo, fábricas de mídia token-gated).
- `scripts/` — scripts das fábricas que rodam no runner do Actions.
- `tour-virtual/` — página antiga do piloto de slideshow (histórico).
- Workflows: `.github/workflows/jazz-*.yml` (prefixo obrigatório).

## Segredos

Os secrets `SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` do repositório são da
MÁQUINA YT — **não** usar em nada da Jazz (já causou um 404 em produção).
Tudo da Jazz autentica com o secret `AUDITORIA_TOKEN` contra Edge Functions
token-gated; o valor mora em `integracao_credenciais.auditoria_interna_token`
no banco da Jazz e nunca entra no repositório.

## Migração futura

Quando o repositório próprio (`jazz-orquestra-feed`) for criado, esta pasta
inteira muda para lá, junto com os workflows `jazz-*`. A criação do repo
exige permissão que o app do GitHub desta sessão não tem (403) — é um passo
do dono da conta.
