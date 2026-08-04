# Auditoria do canal @SetiapLevelID

Levantada em 04/08/2026 via YouTube Data API.

## Identidade

| Campo | Valor |
|---|---|
| ID | `UCf4-ZFoZQWKJotZNdi4Yl7w` |
| Handle | [@setiaplevelid](https://www.youtube.com/@SetiapLevelID) |
| Título | Setiap Level |
| Criado em | 03/08/2026 |
| Playlist de uploads | `UUf4-ZFoZQWKJotZNdi4Yl7w` |
| Inscritos / vídeos / views | 0 / 0 / 0 |

Posicionamento declarado na descrição: como dinheiro, trabalho, status e
pequenas decisões moldam a vida — através de animação simples, histórias e
dados fáceis de entender.

## Configurações corretas

| Item | Valor | Confere com |
|---|---|---|
| `madeForKids` | `false` | `canal.publico_infantil: false` |
| `privacyStatus` | `public` | — |
| `isLinked` | `true` | conta vinculada |
| Avatar e banner | configurados | — |
| Palavras-chave | preenchidas | incorporadas ao `referencias_titulo` |

## Três desalinhamentos

### 1. Limite de 15 minutos ⚠️ bloqueia a estratégia

`longUploadsStatus` retorna `longUploadsUnspecified`. Sem verificação da conta
por telefone, o YouTube limita uploads a **15 minutos**.

A estratégia definida é vídeo longo (`Formato.LONGO` mira 8+ min para liberar
múltiplos blocos de anúncio; a referência estudada usa 40-60 min).

O valor `unspecified` pode ser apenas efeito de o canal não ter uploads ainda —
não é conclusivo pela API. **Confirmar em** YouTube Studio → Configurações →
Canal → Recursos disponíveis. Se "Vídeos com mais de 15 minutos" não estiver
liberado, verificar por telefone **antes** de produzir.

### 2. "Animação" prometida, imagem estática entregue

A descrição promete *animasi sederhana* e as palavras-chave incluem
*animasi edukasi*. A pipeline atual gera **imagens estáticas com Ken Burns**
(zoom lento), não animação.

Isso é uma promessa não cumprida, e bate direto no pilar 3: quem clica esperando
animação e encontra slideshow abandona.

Duas saídas:
- **Imediata e honesta:** ajustar a descrição do canal (trocar "animação" por
  "visual" / "gráficos").
- **Trabalho real:** evoluir a pipeline para animação de verdade (b-roll em
  vídeo, gráficos animados). Está no backlog de `04-roadmap.md`.

### 3. País do canal: Brasil

`country: BR`, com conteúdo em indonésio para audiência indonésia.

Não bloqueia nada, mas é incoerente com o posicionamento e pode influenciar
sinais de recomendação e a configuração de monetização depois. Considerar mudar
para `ID` no Studio.

## Estado da autorização

A conexão do Composio autorizou a conta Google, mas **não o canal** —
`channels.list(mine=true)` retorna vazio. Leitura de dados públicos funciona;
upload e Analytics, não.

Corrigir reconectando e **selecionando Setiap Level** na tela do Google, ou pelo
caminho próprio (`maquina auth-youtube`), que já valida o canal autorizado e
falha se for o errado.
