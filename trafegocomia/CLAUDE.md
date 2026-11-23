# Tráfego com IA (@trafegocom.ia): memória do projeto

Leia isto antes de qualquer tarefa do @trafegocom.ia. É a fonte única das decisões já tomadas:
**não recomece do zero, não contradiga sem dizer por quê, e atualize este arquivo quando algo mudar.**
Branch de trabalho: `ccr-193f026c-cfpyom` (repo `sampaioopablo1-lgtm/maquina-yt-receita`).

## 1. Decisões em vigor (as mais recentes valem)

| tema | decisão | quando |
|---|---|---|
| **Público** | **GESTOR DE TRÁFEGO** autônomo/iniciante, 1 a 10 clientes. NÃO dono de negócio, NÃO designer. | 23/11/2026 |
| **Promessa** | "Conecte a IA ao Gerenciador e atenda mais clientes no mesmo tempo. Relatório, variações e campanhas pedidos em português; a estratégia continua sua." | 23/11/2026 |
| **Produto** | Clube Tráfego com IA, **assinatura mensal R$ 29,90**, cartão + Pix Automático, 7 dias de garantia, cancela quando quiser. Teste futuro: R$ 47 a 67. | 23/11/2026 |
| **Funil** | Anúncio → **checkout da Kiwify usado como página de vendas** (sem página no meio) → compra. | 23/11/2026 |
| **Verba** | R$ 6/dia: 1 campanha Vendas, 1 conjunto, 4 a 6 anúncios, otimizar **visualização da página de destino**; passar para Compra com ~50 compras/semana. | 23/11/2026 |
| **Reels orgânicos** | **ATIVOS: 12 por dia** no @trafegocom.ia, tarefa agendada a cada 2 h desde as 07:00 BRT (id `trig_01V2wxLwPZZPpkHmXtPzx4HA`), 1 Reel por execução, com aprendizado. Procedimento: `trafegocomia/reels/ROTINA.md`. | 23/11/2026 |
| **Aprovação** | "Tudo aprovado, não precisa me pedir outras aprovações", **exceto** ações irreversíveis ou com dinheiro: publicar campanha, ativar vendas, mudar preço, pagamento. Essas ficam PAUSADAS para ele. | — |

Por que gestor e não dono de negócio: "Claude ligado ao Gerenciador" é técnico demais para o dono e tem
custo escondido (plano pago da IA, que é mais caro que o clube); o gestor é consciente, já paga por
ferramenta e compra demonstração. O mercado paga por isso (ver §4).

## 2. Regras que não se negociam
- **Nada de resultado, depoimento ou número inventado.** Sem caso real, sem número de resultado.
- **Sem cronômetro falso** no checkout; sem escassez que não existe.
- Conversa com IA nos criativos é **ilustração** e vai marcada como tal.
- **Não usar marca alheia** (logo, arte, fonte de Netflix, GTA, Rockstar, Anthropic). Citar nome em notícia ou comparação é ok.
- Número sobre o mundo (preço de terceiro, data) só com fonte e data na peça.
- FAQ diz em letra que **a IA tem custo à parte**, e toda peça que compara preço (Netflix, GTA) também diz "plano da IA cobrado à parte".
- Comparação com a Netflix: **só contra o plano Padrão** (R$ 51,90). O plano com anúncios (R$ 25,90) é MAIS barato que o clube.
- Promessa "em 1 minuto" é do dono, não medida: preferir "em minutos".
- Nunca commit de chave, senha ou licença.
- Imagem de checkout: menor texto ≥ 44 px em arte de 1080 (≥ 80 px em 2000). Coluna lateral do checkout **só texto**, nunca imagem.

## 3. O que falta (bloqueia venda)
1. **Lista do que o clube entrega** → preencher `trafegocomia/checkout/landing.json` (`recebe`) e regerar a página.
2. **Gravação real da tela** com a IA operando uma conta (30 a 60 s) → montar o vídeo principal sobre ela.
3. Checkout publicado na Kiwify → link `pay.kiwify.com.br/...` (o dono roda `saida/gestores/PROMPT-CHECKOUT.md`).
4. Conta de anúncios "Tráfego com IA" (BRL, America/Sao_Paulo) + Página + Instagram vinculados + pixel com token da API de Conversões na Kiwify.
5. Campanha criada pausada (`saida/gestores/PROMPT-CAMPANHA.md`, 6 anúncios da seção "No ar no teste" do `COPY.md`), revisada e ativada pelo dono. A reserva (g4, gta-11, gta-12) entra no lugar dos 2 piores depois de 3 a 4 dias. **GTA perde força em 2 a 3 semanas a partir de 19/11/2026.**
6. ~~Instagram no Composio~~ conectado em 23/11 (conta `trafegocom-ia`, id `instagram_ceps-waily`). Linha de base: 0 seguidores, 5 posts, alcance de 1 a 6 por Reel.

## 4. Pesquisa (fatos com fonte)
- `pesquisa/analise-2026-11-23.md`: 242 anúncios do nicho na Biblioteca de Anúncios; os validados (174 a 676 dias) usam carrossel, dica concreta, gancho de notícia de IA, "comente palavra → DM".
- `pesquisa/analise-gta6-2026-11-23.md`: GTA 6 (lançamento 19/11/2026, US$ 3,79 bi no 1º dia, R$ 449,90 no BR).
- `pesquisa/lps/`: 20 páginas de destino capturadas no celular; checkouts Kiwify estudados. `lps/desktop/medidas.json`:
  **checkout Kiwify no computador tem 984 px: cabeçalho 984, coluna principal ~670, lateral ~284; no celular ~390 e o
  FORMULÁRIO VEM PRIMEIRO** (o que vende vai nas imagens acima dele).
- **Concorrente direto:** trafego17.zxlab.com.br (Rafael Castro) vende "Claude Code + Meta Ads" a **R$ 17 vitalício**
  (Black Friday) para gestores. Diferencial nosso: continuidade (clube, atualização, comunidade), não preço.
- Outros que vendem IA para gestor: Luiz Otávio (Meta Ads com IA, R$ 127), The Skill (CopyOS, R$ 67), Criativivo (500 dias no ar).
- Netflix BR desde 15/10/2026: com anúncios R$ 25,90 · Padrão R$ 51,90 · Premium R$ 71,90.
- Funil (premissas do dono): LTV ≈ 3 × R$ 26,91 ≈ R$ 81; clique empata em ~R$ 1,60 com conversão de 2% (R$ 0,80 a 1%).

## 5. Onde está cada coisa
| o quê | arquivo | como regerar |
|---|---|---|
| **COPY de todos os anúncios (fonte única)** | `saida/gestores/COPY.md` | editar o .md |
| **Criativos para gestor** (g1 a g4, feed/stories) | `saida/gestores/criativos/` | `FONTES_DIR=… node trafegocomia/anuncios/gera-gestor.js saida/gestores/criativos` |
| **GTA 6 para gestor** (gta-11, 12, 13) | `saida/gestores/criativos/gta-*` | `node trafegocomia/anuncios/gera-gta-gestor.js saida/gestores/criativos` |
| **Vídeo Netflix para gestor** (43 s, preto e vermelho) | `saida/gestores/criativos/netflix-gestor.mp4` | `python3 trafegocomia/v2/produz.py trafegocomia/v2/menos-que-netflix-gestor.json …` |
| **Checkout para gestor** (topo, como funciona, pop-up, página inteira e 7 partes) | `saida/gestores/checkout/` | `node trafegocomia/checkout/gera-gestor.js …` e `landing-gestor.js …` |
| Prompts para o terminal local | `saida/gestores/PROMPT-CHECKOUT.md`, `PROMPT-CAMPANHA.md` | editar o .md |
| Vídeo "Claude no Gerenciador" (serve ao gestor) | `saida/anuncios-2026-11-23/video/09-claude-no-gerenciador.mp4` | `python3 trafegocomia/v2/produz.py trafegocomia/v2/claude-gerenciador.json …` |
| Logo (quadrado, ícone, horizontal; escuro, claro, transparente) | `saida/marca/` | `node trafegocomia/marca/logo.js saida/marca` |
| Roteiro de montagem do checkout + tabela de tamanhos | `saida/checkout-kiwify/ROTEIRO.md` | — |
| *(FORA DE USO, eram para dono de negócio)* criativos 01 a 13 (menos o vídeo 09), Netflix 10, GTA 11 a 13 antigos, checkout | `saida/anuncios-2026-11-23/`, `saida/checkout-kiwify/` | só referência |
| Motor de vídeo v2 (HTML animado + edge-tts + ffmpeg; campos `chat`, `list`, `vs`, `tema`) | `trafegocomia/v2/` | `produz.py roteiro.json saida.mp4 capa.png` |

`FONTES_DIR` = pasta com `montserrat-latin-900-normal.woff2` e `-800-` (`npm i @fontsource/montserrat`, pasta `files/`).
Identidade: fundo `#111827`, azul `#1D4ED8`, destaque `#3B82F6`, verde `#22C55E`, Montserrat 900/800, selo "📢 IA".

## 6. IDs e links
- Instagram: https://www.instagram.com/trafegocom.ia/
- Produto Kiwify (construtor do checkout): https://dashboard.kiwify.com/products/edit/59009690-e740-11f1-9972-d949ca894c7b?tab=checkout-builder
- Conta de anúncios a criar: "Tráfego com IA". Campanha: `TCIA | Gestores | Vendas | Teste criativos`, conjunto `BR | 22-50 | Gestores | LPV`.
- UTMs: `utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`

## 7. Como operar a partir do terminal local
- Mexer no painel da Kiwify ou no Gerenciador: **Claude in Chrome** (Chrome logado, extensão ligada; `/chrome` no Claude Code).
  A sessão na nuvem NÃO alcança o navegador nem o login do dono.
- Regra de corte da campanha: não mexer por 3 a 4 dias; depois desligar os 2 piores por custo por visualização da página de destino.
- Ao terminar uma tarefa: atualizar §1 e §3 deste arquivo, commitar e dar push no branch.
