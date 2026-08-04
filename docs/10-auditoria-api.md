# Auditoria da YouTube API — o desbloqueio definitivo da publicação automática

## Por que isso é O caminho

Regra oficial do YouTube: **todo vídeo enviado via API por projeto não auditado
(criado após 28/07/2020) fica restrito a privado** — e na prática, em canais
novos, é removido. Foi exatamente o que derrubou nossos 6 uploads via app de
terceiro. A auditoria de compliance é o processo oficial que remove essa
restrição **para o seu próprio projeto**.

Depois de aprovado: `videos.insert` público funciona, para sempre, sem
intermediário — e o workflow `publicacao.yml` da máquina assume o clique final.

## Pré-requisito (15 min) — sem isto não há o que auditar

A auditoria é **por projeto de API**. Você precisa do projeto próprio:

1. [console.cloud.google.com](https://console.cloud.google.com) → criar projeto
   (nome: `setiap-level-machine`)
2. **APIs e serviços → Biblioteca** → ativar **YouTube Data API v3**
3. **Tela de permissão OAuth** → Externo → preencher nome/e-mail → em
   *Usuários de teste*, adicionar o próprio Gmail
4. **Credenciais → Criar credenciais → ID do cliente OAuth → App para computador**
   → baixar o JSON → salvar como `secrets/client_secret.json`
5. Anotar o **Project number** (página inicial do projeto) — o formulário pede
6. Rodar `maquina auth-youtube` uma vez (valida o fluxo e o canal)

## O formulário

📋 **[YouTube API Services — Audit and Quota Extension Form](https://support.google.com/youtube/contact/yt_api_form)**

Preencha logado no mesmo Gmail do projeto. Abaixo, as respostas prontas —
ajuste o que estiver entre colchetes.

## Respostas prontas (inglês, para colar)

**Contact / developer info**
- Name: `[seu nome completo]`
- Email: `sampaioopablo@gmail.com`
- Organization: `Individual developer (personal project)`
- Country: `Brazil`

**API Project details**
- Project number: `[número do projeto no Cloud Console]`
- API Client type: `Internal application (single user — channel owner)`
- Audience: `This API client is used exclusively by me, the owner of the
  YouTube channel "Setiap Level" (UCf4-ZFoZQWKJotZNdi4Yl7w), to upload and
  manage videos on my own channel. It is not distributed to any third party
  and has no external users.`

**Use case description** (o campo mais importante — rejeições comuns vêm de
descrição vaga):

```
I run an educational YouTube channel ("Setiap Level") that publishes
animated explainer videos about personal finance and careers. I built an
internal content pipeline that renders my videos (script, illustrations,
narration, subtitles) and I want it to upload the finished files to my own
channel on a schedule.

The API client:
- Uploads finished videos to my own channel via videos.insert
  (title, description, tags, category, privacy status, publishAt)
- Sets custom thumbnails via thumbnails.set
- Reads my own channel/video metadata via channels.list and videos.list
- Reads my own performance metrics via the YouTube Analytics API
  (views, impressions CTR, audience retention) to inform content decisions

It does NOT access any other user's data, does not scrape, does not store
third-party data, and has no public-facing interface. OAuth consent is
granted only by my own Google account (channel owner). Expected volume:
1-3 uploads per day, well within default quota.
```

**Scopes used**
```
https://www.googleapis.com/auth/youtube.upload
https://www.googleapis.com/auth/youtube
https://www.googleapis.com/auth/yt-analytics.readonly
```

**Data storage / privacy**
```
The client stores only: OAuth tokens for my own account (locally / in CI
secrets), and metadata of my own videos in a private database I control
(Supabase) for scheduling and analytics. No third-party user data is
collected, stored, or shared. Data is never sold or transferred.
```

**Quota request**: manter a padrão (10.000/dia) — pedir aumento junto costuma
atrasar; dá para pedir depois. O objetivo aqui é o **compliance audit** que
libera uploads públicos.

**Screenshots/demo** (se pedirem): capturas do fluxo OAuth do
`maquina auth-youtube`, da CLI `maquina publicar` e da tabela `videos` no
Supabase bastam para demonstrar o uso interno.

## Dicas de aprovação (das rejeições mais comuns)

- **Seja específico** no caso de uso — "automatizar uploads do meu próprio
  canal" com detalhes técnicos passa; "ferramenta de automação" genérica não.
- **Uso interno, usuário único** simplifica tudo: sem política de privacidade
  pública obrigatória, sem verificação de marca.
- Não peça mais cota do que precisa.
- Responda e-mails do time da API rapidamente — o processo é iterativo.

## Prazo e o que fazer enquanto isso

Relatos da comunidade: dias a poucas semanas. Enquanto não aprova:

- Publicação continua **manual pelo Studio** (2 min por vídeo, comprovadamente
  estável) com os pacotes de copy que a máquina gera.
- Todo o resto (roteiro → arte → voz → render → SEO) segue automático.

Aprovado, ativa-se: `YT_TOKEN_JSON` nos secrets → `publicacao.yml` no Actions →
publicação 100% automática com o OAuth próprio.

## Fontes oficiais

- [Formulário de auditoria e extensão de cota](https://support.google.com/youtube/contact/yt_api_form)
- [Guia oficial: quota and compliance audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)
- [videos.insert — restrição de projetos não auditados](https://developers.google.com/youtube/v3/docs/videos)
- [Developer Policies da YouTube API](https://developers.google.com/youtube/terms/developer-policies)
