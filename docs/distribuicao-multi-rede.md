# Distribuição multi-rede — o que foi medido, o que entrou, o que é do dono

**Pedido do dono, 29/10/2026 (voz, transcrito):** *"preciso ter uma skill que
produza o vídeo [...] e esse mesmo vídeo ele possa ser publicado automaticamente
no Instagram, no TikTok, no YouTube, em outras redes sociais disponíveis, para
que gere tráfego e assim as pessoas acessem o perfil e o link da bio para comprar
o meu curso ou o meu aplicativo. Faça uma pesquisa."*

Este documento é a pesquisa — feita sobre o que **existe nesta máquina e neste
ambiente**, não sobre a web, que o proxy bloqueia e que a rotina já mediu como
fonte inútil para tendência (§5). Cada afirmação diz de onde saiu.

## 1. As rotas que existem, medidas

| rota | automática? | redes | o que falta | fonte |
|---|---|---|---|---|
| **Upload-Post API** (skill `.claude/skills/upload-post/`, já no repo) | **SIM** — uma chamada HTTP por peça, N redes | Instagram, TikTok, Threads, X, LinkedIn, Facebook, Pinterest, Bluesky, Reddit (e YouTube, que aqui é recusado) | conta no serviço, contas conectadas, um **perfil por canal**, a chave como segredo do GitHub | `.claude/skills/upload-post/SKILL.md`, `.claude/skills/upload-post/references/platforms.md`, `.claude/skills/upload-post/references/requirements.md` |
| TikTok pela Higgsfield (`docs/tiktok-sondado.md`) | **NÃO** — exige o dono num widget a cada peça e o asset hospedado lá | só TikTok | — | sondado em 10/2026 |
| Composio `YOUTUBE_UPLOAD_VIDEO` | proibida | YouTube | — | 6/6 apagados (trava do núcleo) |
| Facebook MCP desta sessão | é de **anúncios** (campanhas, catálogos, insights), não de post orgânico | — | — | lista de ferramentas da sessão |
| YouTube | **já automático** | YouTube | nada — `retomar.yml` publica com `YT_OAUTH_JSON` | em produção desde 12/10 |

**Logo a única rota automática para as redes que o dono nomeou é a do
Upload-Post**, e ela já estava documentada no repo como skill — faltava o código
que liga a peça publicada à chamada, e é isso que entrou.

**A tentativa de ler a documentação viva** (`docs.upload-post.com/llm.txt`)
levou **403 ao CONNECT** do proxy, que é política e não se retesta. O que vale
é a referência da skill no repo, e é dela que saem os limites abaixo.

## 2. O que o formato da frota cabe em cada rede

O short da frota mede **41 a 45 s reais**, 9:16, H.264/AAC (medido na série
de resíduo e no `som-medido.jsonl`). O longo mede **8 a 10 min**, 16:9.

| rede | teto de vídeo | short cabe? | longo cabe? |
|---|---|---|---|
| Instagram Reels | 90 s, 9:16 | **sim** | não |
| TikTok | 3 s a 10 min | **sim** | sim (9:16 recomendado; o nosso é 16:9) |
| Threads | 5 min | sim | não |
| X | 140 s, 512 MB | sim | não |
| Bluesky | 60 s, 50 MB, 50/dia | sim | não |
| LinkedIn | 3 s a 10 min | sim | sim |
| Pinterest | 4 s a 15 min | sim | sim |
| Facebook | 240 min | sim | sim |

Os tetos vivem em `fabrica/distribuicao.TETO_S` com esta procedência, e o
instrumento **mede a duração do arquivo com ffprobe** antes de decidir — nunca
pela previsão, que erra para os dois lados (banda de 5,2 s no short).

## 3. O link da bio — por que o CTA é assim

Instagram e TikTok **não tornam clicável** um link na legenda. O caminho que o
dono descreveu — vídeo → perfil → link da bio → curso/app — é o único que
funciona nessas duas redes, logo:

- a **legenda** = título curto do short + CTA *"o link está na bio"* na língua
  do canal + hashtags (até 2.200 caracteres);
- o **primeiro comentário** (`first_comment`, onde a rede aceita) = primeiro
  parágrafo da descrição + CTA + o link em si;
- o **link da bio** de cada canal é dado do dono, em
  `fabrica/perfis_sociais.json`. Sem ele o CTA sai e o link não — e o relato
  diz isso.

O que o instrumento **não** faz: não gera uma landing page, não encurta link,
não mede clique. Clique na bio é métrica da própria rede; sem o escopo de
analytics (pendência conhecida) ela não entra aqui.

## 4. O que entrou nesta rodada

- `fabrica/perfis_sociais.json` — mapa canal → perfil do Upload-Post, link da
  bio, redes e CTA na língua do canal. **`perfil` nulo = o instrumento recusa.**
- `fabrica/distribuicao.py` — dono único: payload a partir dos donos que já
  existem (`publicar.ler_copy`, `canal.da_spec`), conferência de duração por
  rede (nomeia as que não cabem), chamada à API com a chave em arquivo `0600`
  lido por `curl -K` (nunca em argv nem stdout), parque
  `docs/pendente/distribuicoes.jsonl` que recusa repetir a mesma peça na mesma
  rede. YouTube é **recusado** aqui — o dono dele é o `retomar.yml`.
- `.github/workflows/distribuir.yml` — baixa o MESMO artefato do render pelo
  nome (`pacote-<pacote>`), mede com ffprobe, chama o módulo, sobe o parque
  como artefato. Para no primeiro passo se o segredo estiver vazio.
- `.claude/skills/produzir-e-distribuir/SKILL.md` — a ordem da rodada inteira,
  com um dono por passo e só ponteiros.
- Testes em `tests/test_a_distribuicao_nao_tinha_dono.py`.

## 5. O que é do DONO (sem isto, nada é distribuído)

1. Criar conta no **upload-post.com** e **conectar** as contas de Instagram e
   TikTok (e as outras que quiser) de cada canal. Conectar conta é decisão do
   dono; a máquina não abre presença em rede nova sozinha.
2. Criar **um perfil por canal** no painel (ex.: `labtreinamento`,
   `epomeno-epipedo`, `kolejny-poziom`) e escrever o nome em
   `fabrica/perfis_sociais.json` → `perfil`.
3. Escrever o **link da bio** de cada canal no mesmo arquivo → `link_da_bio`,
   e pôr esse link na bio dos perfis.
4. Gerar a **API key** no painel e colá-la no GitHub como segredo
   `UPLOAD_POST_API_KEY` (Settings → Secrets and variables → Actions). O proxy
   desta sessão bloqueia a API de secrets, logo é colagem do dono; **não cole
   a chave no chat**.
5. Conferir o plano do Upload-Post: o número de uploads por mês tem teto por
   plano, e a frota publica ~24 shorts/dia. Esse número não está medido aqui —
   quem o diz é o painel do serviço.

Depois disso a rodada dispara o `distribuir.yml` depois do `retomar.yml`, e a
linha do parque entra no repo como os outros quatro parques.

## 6. O que NÃO está afirmado

- Que distribuir traga inscrito ou venda: isso é medida futura, por clique na
  bio e pela conversão do curso, e nenhuma das duas está instrumentada.
- Que o longo 16:9 renda no TikTok: cabe pelo teto de duração, mas a referência
  da skill recomenda 9:16; se o dono quiser, o reframe é outro passo.
- Qualquer número sobre o próprio Upload-Post (preço, cota mensal, prazo de
  processamento) — a documentação viva está bloqueada pelo proxy e o que a
  skill traz é forma, não número.
