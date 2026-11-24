# Rotina dos Reels do @trafegocom.ia (3 por dia, com aprendizado)

Pedido do dono em 23/11/2026: criar e publicar Reels no Instagram **@trafegocom.ia** sem PC ligado,
com auto-aprendizado para escolher os próximos temas e ganhar seguidores.
Volume: **12 por dia, decisão do dono em 23/11** ("ao menos 12 por dia"). Eu recomendei 3, porque
num perfil só o excesso pode derrubar o alcance por peça; o aprendizado mede isso: se a mediana de
views por Reel cair semana a semana, diga ao dono com o número. Cada execução da tarefa agendada
(a cada 2 horas: 07:00, 09:00 ... 05:00 de Brasília, a partir de 24/11; em 23/11 saiu o lote r001 a r013 de uma vez, a pedido do dono) faz **1 Reel**.

Leia antes `trafegocomia/CLAUDE.md` (público, regras, identidade). Branch: `ccr-193f026c-cfpyom`.

## Passo a passo de cada execução
1. `git fetch origin ccr-193f026c-cfpyom && git checkout ccr-193f026c-cfpyom && git pull`.
2. **Medir.** Composio, conta `trafegocom-ia` (id `instagram_ceps-waily`):
   `INSTAGRAM_GET_USER_INFO` (ig_user_id `me`, fields `followers_count,media_count`) e
   `INSTAGRAM_GET_IG_USER_MEDIA` (ig_user_id `me`, limit 50, fields
   `id,timestamp,permalink,insights.metric(views,reach,saved,shares,total_interactions)`).
   Salve a lista em `/tmp/midia.json` e rode `python3 trafegocomia/reels/aprende.py /tmp/midia.json <seguidores>`.
3. **Escolher a família** pelo RANKING:
   - 2 de cada 3 Reels: a família de MAIOR mediana com n >= 3 (ou, sem dado, a menos usada);
   - 1 de cada 3: família pouco testada (n < 3) ou nova, para explorar.
   - Nunca a mesma família duas vezes seguidas. Nunca repetir um tema já em `publicados.jsonl`.
4. **Escrever o roteiro** em `trafegocomia/reels/roteiros/rNNN.json` (NNN = próximo número),
   formato do motor v2 (ver `trafegocomia/v2/menos-que-netflix-gestor.json`): 6 a 9 cenas,
   **25 a 45 s**, gancho nos 2 primeiros segundos, uma ideia só, fala natural, CTA no fim.
   `slug` = `rNNN-<tema-curto>`. Use o tema visual da marca (sem `tema` = padrão azul).
   **Método de roteiro (prompts do dono, 24/11), aplicados por você antes de escrever:**
   a) *Ideias:* liste 5 ideias curtas e compartilháveis para gestor de tráfego dentro da família escolhida.
      O prompt original pede "as 10 tendências virais do Instagram": esta sessão NÃO lê tendências do
      Instagram, então a base é o ranking do `aprende.py` + no máximo 1 busca na web por novidade real
      de Meta Ads/IA (com fonte). Nunca invente tendência.
   b) *Dor → gancho:* das ideias, tire a dor do gestor e escreva o gancho em até 10 palavras, direto e
      provocador, sem clichê. Ele vira a 1ª cena (2 primeiros segundos).
   c) *Estrutura de 30 s:* gancho irresistível → história curta (situação do gestor, com uma virada) →
      CTA para comentar ou salvar. Frases curtas, nenhuma enrolação.
   d) *Salvamento:* quando a família for `checklist`, `prompt-pronto` ou `metrica-em-30s`, entregue dicas de
      até 12 palavras, fáceis de aplicar (é o que faz salvar).
   e) *CTA:* escreva 3 CTAs com curiosidade e ação imediata ("comenta X", "salva pra segunda") e use o
      melhor; não repita o CTA do Reel anterior.
   f) *Prova social:* SÓ com resultado real e documentado. Hoje não existe nenhum: não use.
   g) *Reaproveitar:* o roteiro de 7 s, carrossel de 5 slides e post estático ficam para quando o motor
      gerar esses formatos; por enquanto a peça é o Reel (+ o mesmo vídeo no Story).
5. **Renderizar:** `python3 trafegocomia/v2/produz.py trafegocomia/reels/roteiros/rNNN.json
   saida/reels/rNNN.mp4 saida/reels/rNNN-capa.png`. Confira duração (ffprobe) e olhe 2 quadros.
6. **Subir o arquivo:** commit do roteiro + mp4 + capa, `git push origin ccr-193f026c-cfpyom`.
   URL pública: `https://raw.githubusercontent.com/sampaioopablo1-lgtm/maquina-yt-receita/ccr-193f026c-cfpyom/saida/reels/rNNN.mp4`.
7. **Publicar:** `INSTAGRAM_POST_IG_USER_MEDIA` (conta `trafegocom-ia`, ig_user_id `me`,
   media_type `REELS`, video_url, cover_url = capa, caption, share_to_feed true) e depois
   `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` (max_wait_seconds 300). Pegue o permalink.
   No máximo 2 tentativas; se falhar, registre o erro e pare (não marque como publicado).
   **Depois, o mesmo vídeo como Story** (pedido do dono em 23/11): `INSTAGRAM_POST_IG_USER_MEDIA` com
   media_type `STORIES` e o mesmo video_url, e `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`. Se a chamada passar do
   tempo, confira com `INSTAGRAM_GET_IG_USER_STORIES` antes de repetir (Story duplicado é pior que faltando).
8. **Registrar:** acrescente em `trafegocomia/reels/publicados.jsonl` uma linha
   `{"n":"rNNN","ig_id":"...","story_id":"...","permalink":"...","em":"<UTC>","familia":"...","tema":"...","gancho":"..."}`,
   commit `Reel rNNN publicado` e push.
9. **Responder** em uma linha: Reel publicado (link), família, seguidores agora, família líder do ranking.

## Bancos de famílias (público: GESTOR DE TRÁFEGO, 1 a 10 clientes)
| família | o que é |
|---|---|
| `prompt-pronto` | um prompt que faz uma tarefa do gestor (relatório, variações, análise de conjunto) |
| `erro-que-custa` | um erro comum que faz o gestor perder verba ou cliente, e o conserto |
| `operacional-vs-ia` | tarefa que leva horas na mão e o que muda pedindo à IA |
| `biblioteca-de-anuncios` | como achar e ler anúncios validados dos concorrentes do cliente |
| `metrica-em-30s` | uma métrica (CPA, CTR, frequência, CPM) explicada com um exemplo |
| `mito-ou-verdade` | uma crença do meio de tráfego confrontada |
| `checklist` | 3 itens para conferir antes de subir/escalar uma campanha |
| `rotina-do-gestor` | como organizar a semana com vários clientes |
Família nova pode entrar: escreva aqui na tabela, com uma linha do que é.

## Regras (não se negociam)
- **Nada de resultado, número de cliente, depoimento ou print inventado.** Conversa com IA na tela é ilustração e vai marcada.
- Número sobre o mundo (preço, data, recurso novo da Meta) só com fonte conferida na hora; na dúvida, não use número.
- Sem marca alheia (logo, arte). Citar nome é ok.
- **Venda leve:** no máximo 1 a cada 3 Reels fala do Clube (R$ 29,90/mês, "plano da IA cobrado à parte").
  Os outros dão valor e terminam com "segue para mais" ou "comenta X". O link fica na bio.
- Legenda: 1 linha de gancho + 2 a 4 linhas de valor + CTA + até 5 hashtags. Sem travessão.
- O nome é **Clube** Tráfego com IA (não "Club").
- Nunca apagar Reel publicado. Nunca mexer em anúncio, perfil ou outra conta (o @oproximocliente é de outro projeto).
