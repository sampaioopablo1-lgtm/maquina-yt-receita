# Funil de leads — Mentoria "O Próximo Cliente"

> Escrito em 04/09/2026, a partir da montagem da campanha `REC | TOPO` no
> Gerenciador de Anúncios. Este documento é o mapa do funil: o que cada campanha
> faz, quem entra, quem sai e o que medir. Iniciativa separada dos canais do
> YouTube — vive aqui porque o repositório é o caderno de decisões do dono.

## A oferta, em uma linha

Mentoria para donos de pequenos negócios que querem **gerar cliente por conta
própria com tráfego pago para o WhatsApp** — parar de depender de indicação e não
precisar contratar agência.

O lead qualificado é o empresário que **já tem produto e clientes**, **sente que
o negócio vive de indicação** e **está disposto a investir em anúncio** — mas não
sabe montar. Quem ainda não tem faturamento, ou quer que alguém faça por ele, não
é aluno de mentoria: é cliente de agência.

## O funil em três camadas

```
[1] REC | TOPO  ───────►  público frio assiste vídeo (ThruPlay, ≥15s)
        │
        │  gera os públicos personalizados de vídeo (VV_*)
        ▼
[2] LEAD | MEIO ───────►  só quem assistiu recebe o anúncio com formulário
        │
        │  formulário "maior intenção" com perguntas de qualificação
        ▼
[3] WhatsApp    ───────►  triagem humana, chamada de diagnóstico, oferta
```

| Camada | Campanha | Objetivo no Gerenciador | Quem entra | Função |
|---|---|---|---|---|
| 1 | `REC \| TOPO` | Reconhecimento → Maximizar ThruPlay | Frio, segmentado por perfil de dono de negócio | Aquecer e **construir público** |
| 2 | `LEAD \| MEIO` | Cadastro → Formulários instantâneos | Quem assistiu os vídeos da camada 1 | Capturar lead **qualificado** |
| 3 | `RMK \| FUNDO` (semana 3+) | Cadastro → Formulários instantâneos | Abriu o formulário e não enviou | Recuperar quem hesitou |

A camada 2 **não roda sozinha**: sem a camada 1 rodando antes, o público
personalizado fica vazio e o conjunto não entrega. A ordem de ativação está no
cronograma no fim.

## Camada 1 — `REC | TOPO` (o que está no print e o que ajustar)

O que já está certo no conjunto `ADM DE PÁGINAS`:

- Otimização em **ThruPlay**. É exatamente a métrica que alimenta o público de
  vídeo: quem passou dos 15 segundos (ou viu o vídeo inteiro, se for mais curto).
- **Página**: O Próximo Cliente.
- **Lance**: volume mais alto. Correto para reconhecimento — não há motivo para
  meta de custo nesta fase.
- **Controle de frequência**: limite de 2 impressões a cada 7 dias. Bom para
  topo. Não deixe a Meta mostrar o mesmo vídeo cinco vezes para quem ignorou.

O que precisa mudar antes de ativar:

| Item | Como está | O que fazer | Por quê |
|---|---|---|---|
| Orçamento | Vazio (erro `#1885272`) | Mínimo é R$ 5,21/dia. Começar com **R$ 25–30/dia** | Com R$ 5 o público de vídeo demora semanas para ter volume. A camada 2 precisa de milhares de ThruPlays para entregar |
| Público estimado | 154–182 milhões | Trazer para a faixa de **2–15 milhões** | 154 milhões é o Brasil inteiro. O nome do conjunto diz "administradores de página", mas a segmentação não está aplicada (ou o Advantage+ está expandindo) |
| Nome do conjunto | `ADM DE PÁGINAS` | Manter, mas fazer o nome descrever a segmentação real | O nome vira o rótulo do público personalizado depois |
| Posicionamentos | Padrão | Reels, Feed e Stories (Facebook e Instagram), criativo **9:16** | Vídeo curto vertical é onde o ThruPlay sai mais barato |

Segmentação sugerida para o conjunto (verificar no Gerenciador, porque a Meta
vem removendo opções detalhadas):

- **Idade**: 25 a 55.
- **Localização**: Brasil, ou só os estados onde a mentoria consegue atender no
  fuso horário e sotaque do público.
- **Comportamentos** → Atividades digitais → *Administradores de Página do
  Facebook* (donos de página de negócio) e *Pequenos empresários*.
- **Interesses**: Empreendedorismo, Pequenas e médias empresas, Anúncios do
  Facebook, Meta Business Suite, Marketing digital.
- Deixar o **Advantage+ de público desligado** neste conjunto. Aqui a intenção é
  encher o público de vídeo com o perfil certo, não com quem a Meta achar que
  assiste mais.

Criar um segundo conjunto de teste, `INTERESSES`, só com os interesses acima
(sem os comportamentos), para comparar custo por ThruPlay entre os dois. Mesmo
orçamento, mesma criativa, sete dias.

### Criativos de topo

Regra do formato: o corte que importa é o **segundo 15**. Tudo que o vídeo precisa
dizer para o público certo se reconhecer tem que acontecer antes disso. Vídeos de
20 a 40 segundos, gancho nos 3 primeiros segundos, legenda queimada, sem música
alta por cima da fala.

Cinco ângulos para rodar em paralelo (um vídeo por ângulo, todos no mesmo conjunto):

| # | Ângulo | Gancho (primeiros 3s) | Virada antes dos 15s |
|---|---|---|---|
| 1 | Dor da indicação | "Seu negócio vive de indicação?" | Indicação não escala e não é previsível — é sorte com nome bonito |
| 2 | Agência | "Pagou agência e não viu cliente novo?" | Agência vende relatório; você precisa de conversa no WhatsApp |
| 3 | Método | "Um anúncio que gera conversa no WhatsApp tem 3 partes" | Lista as 3 (oferta, público, chamada) — sem ensinar como |
| 4 | Prova | "Esse [ramo] estava parado; olha o WhatsApp dele hoje" | Print de conversas chegando, número de leads na semana |
| 5 | Custo | "Quanto custa um cliente novo no seu ramo?" | Mostra que R$ 20/dia já gera conversa, se o anúncio for certo |

Um único CTA no fim, leve: "segue a página / vê o próximo vídeo". Topo não pede
formulário — quem pede aqui paga caro e recebe curioso.

## Públicos personalizados (criar antes da camada 2)

Gerenciador → Públicos → Criar público → Personalizado → **Vídeo**. Selecionar
todos os vídeos da campanha `REC | TOPO`.

| Nome | Critério | Retenção | Uso |
|---|---|---|---|
| `VV_THRUPLAY_30D` | Assistiu ThruPlay (15s ou completo) | 30 dias | Público principal da camada 2 |
| `VV_50_60D` | Assistiu 50% | 60 dias | Empilha com o de cima |
| `VV_75_90D` | Assistiu 75% | 90 dias | Mais quente; base do lookalike |
| `ENGAJ_IG_90D` | Engajou com o perfil do Instagram | 90 dias | Soma na camada 2 |
| `ENGAJ_FB_90D` | Engajou com a Página | 90 dias | Soma na camada 2 |
| `FORM_ABRIU_90D` | Abriu o formulário e não enviou | 90 dias | Camada 3 (remarketing) |
| `FORM_ENVIOU_180D` | Enviou o formulário | 180 dias | **Exclusão** em todas as camadas |

Quando `VV_75_90D` passar de mil pessoas, criar o **semelhante 1%** dele e testar
como terceiro conjunto de topo. É o público frio mais barato que existe depois
que o funil já tem histórico.

## Camada 2 — `LEAD | MEIO`

Configuração:

- **Objetivo**: Cadastro. Local de conversão: **Formulários instantâneos**.
- **Público**: `VV_THRUPLAY_30D` + `VV_50_60D` + `ENGAJ_IG_90D` + `ENGAJ_FB_90D`.
  **Excluir** `FORM_ENVIOU_180D`. Sem interesses, sem idade além de 25–55 — o
  público já está filtrado pelo comportamento.
- **Frequência**: aqui pode subir para 3–4 a cada 7 dias; é gente que já viu o vídeo.
- **Orçamento**: começar com metade do que roda no topo. Quando o custo por lead
  qualificado estabilizar, inverter a proporção.
- **Ativar só quando** `VV_THRUPLAY_30D` tiver mais de **5 mil pessoas**. Abaixo
  disso o conjunto fica em aprendizado eterno.

### O formulário

Tipo **Maior intenção** (tem tela de revisão antes de enviar — corta o dedo
nervoso e sobe a qualidade). Campos:

| Ordem | Pergunta | Tipo | Para que serve |
|---|---|---|---|
| 1 | Nome | Preenchido pela Meta | — |
| 2 | WhatsApp | Preenchido pela Meta (telefone) | Canal da camada 3 |
| 3 | Qual o ramo do seu negócio? | Texto curto | Personalizar a abordagem |
| 4 | Faturamento mensal aproximado | Múltipla escolha: até 5 mil / 5–15 mil / 15–50 mil / acima de 50 mil | **Qualificação** |
| 5 | Hoje seus clientes vêm principalmente de… | Múltipla escolha: indicação / redes sociais / anúncio / ponto físico | Confirma a dor |
| 6 | Você já anuncia? | Múltipla escolha: nunca / eu mesmo / agência | Segmenta o discurso |
| 7 | Quanto consegue investir por mês em anúncio? | Múltipla escolha: até 300 / 300–1.000 / 1.000–3.000 / acima de 3.000 | **Qualificação** |

Lead **qualificado** = faturamento a partir da segunda faixa **e** disposição de
investir a partir da segunda faixa. Os demais recebem material gratuito e ficam
na base para o próximo ciclo.

Tela de agradecimento: botão **"Falar no WhatsApp"** com mensagem pré-preenchida
("Oi, acabei de preencher o formulário da mentoria O Próximo Cliente. Meu ramo
é ___"). Quem clica aqui é o lead mais quente do dia.

### Criativos de meio

O público já viu o vídeo. O anúncio reconhece isso e pede a ação:

- "Você viu como um anúncio gera conversa no WhatsApp. Agora vamos montar o seu.
  Preenche o formulário e eu te chamo."
- Vídeo de 30–60s do mentor falando direto para a câmera, explicando **o que
  acontece depois do formulário** (chamada de diagnóstico, sem compromisso).
- Um criativo estático com o print do WhatsApp de aluno e a chamada
  "Quantas conversas chegaram hoje no seu?".

## Camada 3 — WhatsApp e `RMK | FUNDO`

- Todo lead qualificado recebe mensagem em **até 15 minutos** no horário
  comercial. Depois de uma hora a taxa de resposta despenca.
- Roteiro de triagem: confirmar ramo, confirmar dor (de onde vêm os clientes),
  agendar chamada de diagnóstico. A oferta da mentoria acontece na chamada, não
  no WhatsApp.
- `RMK | FUNDO`: público `FORM_ABRIU_90D`, exclusão `FORM_ENVIOU_180D`, orçamento
  pequeno, criativo que responde a objeção ("não é agência, não é curso gravado —
  é você montando o seu anúncio com acompanhamento").

## Métricas e gatilhos de decisão

Pontos de partida, não metas. Depois de duas semanas os números do próprio
funil substituem estes.

| Camada | Métrica | Ponto de partida | Gatilho |
|---|---|---|---|
| 1 | Custo por ThruPlay | ≤ R$ 0,15 | Criativo acima de 2× a média do conjunto após R$ 50 gastos → pausar |
| 1 | Taxa de gancho (3s ÷ impressões) | ≥ 25% | Abaixo disso o problema é o primeiro segundo, não o público |
| 1 | Taxa de ThruPlay (ThruPlay ÷ impressões) | ≥ 15% | Abaixo disso a virada está depois do segundo 15 |
| 2 | Custo por lead | R$ 15–40 | Só importa combinado com a linha de baixo |
| 2 | Taxa de qualificação | ≥ 40% | Abaixo disso, trocar o público (só `VV_75_90D`) ou endurecer o formulário |
| 2 | Custo por lead **qualificado** | derivado | É o número que decide orçamento |
| 3 | Resposta no WhatsApp em 15 min | ≥ 60% | Se cair, o gargalo é atendimento, não anúncio |
| 3 | Lead qualificado → chamada agendada | ≥ 30% | Abaixo disso, revisar o roteiro de triagem |

Escalar vencedor: subir orçamento em **20% a cada 48h**, nunca dobrar de uma vez
— dobrar reinicia o aprendizado do conjunto.

## Nomenclatura

```
Campanha:   REC | TOPO          LEAD | MEIO          RMK | FUNDO
Conjunto:   ADM DE PÁGINAS      VV+ENGAJ             FORM ABRIU
            INTERESSES          VV75 (teste)
            LAL1 VV75 (sem. 4)
Anúncio:    [ângulo]-[formato]-[data]   ex.: indicacao-reels-0409
```

O nome do anúncio carrega o ângulo porque é por ângulo que a decisão de pausar
ou escalar é tomada, não por vídeo.

## Cronograma

| Semana | O que ativar | O que olhar |
|---|---|---|
| 1 | `REC \| TOPO` com dois conjuntos e cinco ângulos | Custo por ThruPlay e taxa de gancho por ângulo. Pausar os dois piores no dia 5 |
| 2 | Criar os públicos personalizados. Ativar `LEAD \| MEIO` quando `VV_THRUPLAY_30D` > 5 mil | Custo por lead e taxa de qualificação |
| 3 | `RMK \| FUNDO`. Novo lote de criativos de topo (variações dos vencedores) | Custo por lead qualificado; tempo de resposta no WhatsApp |
| 4 | Semelhante 1% de `VV_75_90D` como terceiro conjunto de topo | Se o semelhante bater o conjunto manual, ele vira o principal |

## Checklist antes de ligar a camada 1

- [ ] Orçamento preenchido (acima de R$ 5,21; sugerido R$ 25–30/dia)
- [ ] Público estimado entre 2 e 15 milhões
- [ ] Advantage+ de público desligado no conjunto
- [ ] Cinco vídeos 9:16, todos com a virada antes do segundo 15, legendados
- [ ] Pixel/Conjunto de dados vinculado à conta (para os públicos de engajamento)
- [ ] Perfil do Instagram conectado à Página no conjunto de anúncios
- [ ] Nome dos anúncios seguindo `[ângulo]-[formato]-[data]`

## Fora de escopo (decidido não fazer agora)

- Tráfego direto para o WhatsApp no topo. Chega curioso, e a triagem vira o gargalo.
- Landing page própria. O formulário instantâneo converte melhor no celular e não
  exige domínio, hospedagem nem pixel configurado para começar.
- Campanha de vendas com pixel. Não há evento de compra rastreável; a venda
  acontece na chamada.
