# Destravar: os 4 campos que liberam o "Modo ativo"

Pesquisado e confirmado em 11/09/2026 na documentação e no aviso oficial da Meta
sobre modos de aplicativo. **Não é revisão de aplicativo. Não é verificação de
negócio. São quatro campos num formulário.**

## Por que é só isso

O erro `1885183` diz: *"Ads creative post was created by an app that is in
development mode. It must be in public to create this ad."* Quem assina o post
oculto de um anúncio de formulário é o **aplicativo do token** — e o OPC
Automação está em desenvolvimento.

Revisão de aplicativo (App Review) só é exigida para mexer em ativos de
**terceiros** ou em dados de usuários que não são do app. Aqui é o contrário:
o token é de usuário do sistema e só toca a conta e a Página do próprio
portfólio do Pablo. Para esse caso a Meta pede apenas que o app saia do modo de
desenvolvimento — e o botão "Modo ativo" só fica disponível depois que quatro
campos das Configurações Básicas estiverem preenchidos.

## Os quatro campos

`developers.facebook.com/apps/2159128187972575/settings/basic/`

| Campo | O que pôr | Situação |
|---|---|---|
| **URL da Política de Privacidade** | `https://<site>.netlify.app/politica-de-privacidade.html` | ✅ **pronta e no ar** — publicada neste commit |
| **Ícone do app (1024×1024)** | `entregas/campanha/imagens/icone-app-opc-1024.png` | ✅ **pronto** — é só subir o arquivo |
| **Categoria do app** | *Business and Pages* | escolher na lista |
| **Uso comercial (Business Use)** | *Support my own business* | escolher na lista |

Vale a pena preencher também, na mesma tela, a **URL de instruções de exclusão
de dados**: `https://<site>.netlify.app/exclusao-de-dados.html` — também já está
no ar. A Meta pede essa quando o app toca dados de pessoas, e o formulário de
lead toca.

> Troque `<site>` pelo nome do projeto no Netlify (o mesmo que aparece nos
> deploys do repositório). As duas páginas republicam sozinhas a cada push nesta
> branch.

## Depois de virar a chave

1. No topo do painel do app, a chave **"Em desenvolvimento" → "Modo ativo"**.
2. Guardar um token de usuário do sistema novo em
   Settings → Secrets → Actions como `META_ACCESS_TOKEN`.
3. Dar push em `entregas/campanha/ANUNCIOS — spec dos conjuntos.json`.

O workflow `anuncios-meta.yml` publica as 10 peças AG **pausadas**, cinco em
cada conjunto da FASE 3, cada uma com o formulário `2412763482587375` grudado.
Aí é o botão de ativar no gerenciador, e mais nada.

## O que NÃO precisa

- Revisão de aplicativo (2 a 4 semanas) — é para ativo de terceiro.
- Verificação de negócio com documento — é para o nível Full da API de
  Marketing, que esta conta não usa.
- Nenhum app de terceiro. O caminho do Supermetrics continua documentado em
  `CAMINHO — publicar pelo Supermetrics.md` como plano B, mas com a chave virada
  ele deixa de ser necessário.
