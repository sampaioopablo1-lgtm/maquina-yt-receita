# Compliance e monetização — o que pode derrubar o canal

Esta é a parte que a maioria dos "métodos" ignora e que decide se o canal vira receita ou
vira trabalho perdido. A máquina tem verificações automáticas para cada item aqui
(`src/maquina/stages/compliance.py`).

## Requisitos do YPP (Programa de Parcerias do YouTube)

Não existe pagamento por visualização fora do YPP. Para **receita de anúncios** é
necessário atingir **1.000 inscritos** E uma destas alternativas:

- **4.000 horas** públicas de exibição em 12 meses, ou
- **10 milhões** de visualizações válidas de Shorts em 90 dias.

Existe também o **tier de entrada antecipada**: **500 inscritos + 3 uploads públicos em
90 dias + 3.000 horas** (ou 3M de views de Shorts). Ele **não libera receita de
anúncios** — libera financiamento por fãs (Super Thanks, membros) e recursos de
Shopping. É um marco intermediário útil, não a monetização principal.

Além disso, o canal passa por **revisão humana** de conformidade. Aprovação não é
automática ao bater a métrica.

Referência: https://support.google.com/youtube/answer/13429240

**Implicação direta:** o número de Shorts necessário para monetizar por Shorts é
impraticável para canal novo. O caminho realista é **horas de exibição via vídeo longo**.
Isso reforça a decisão de formato do playbook.

## Os três riscos reais de desmonetização

### 1. Conteúdo produzido em massa / repetitivo
Política de monetização: conteúdo genérico, repetitivo, feito em massa ou baseado em
template — incluindo slideshows de baixo valor — pode ter monetização negada ou removida.

https://support.google.com/youtube/answer/1311392

O modelo ingênuo de "roteiro IA + voz IA + imagens parecidas + zoom automático" cai
exatamente nessa descrição. **Usar IA não é o problema; ausência de valor original é.**

### 2. Spam por automação em escala
Produção automatizada em grande escala com variações mínimas entre vídeos é tratada como
spam.

https://support.google.com/youtube/answer/2801973

**Implicação para esta máquina:** ela é deliberadamente limitada. Existe um teto de
publicações por dia configurável (`publish.max_per_day`) e uma verificação de
similaridade entre roteiros antes de publicar. Uma máquina que posta 1.000 vídeos/dia não
é mais eficiente — é mais rápida para ser banida.

### 3. Divulgação de conteúdo sintético
Conteúdo sintético **realista** (que possa ser confundido com real: pessoas, eventos,
locais) **deve** ser divulgado no upload. Animação claramente fictícia normalmente não
exige.

https://support.google.com/youtube/answer/14328491

A máquina define a flag de conteúdo alterado/sintético no upload conforme o tipo de
asset gerado — não fica a critério do operador esquecer.

## Barreiras que a máquina aplica antes de publicar

| Verificação | Regra | Bloqueia? |
|---|---|---|
| Similaridade de roteiro vs. últimos N vídeos | > 0.75 → rejeita | Sim |
| Título duplicado/quase idêntico no canal | rejeita | Sim |
| Teto diário de publicações | padrão: 2 | Sim |
| Divulgação de conteúdo sintético | automática por tipo de asset | — |
| Revisão humana antes do upload | obrigatória por padrão (`require_review: true`) | Sim |
| Duração mínima para blocos de anúncio | ≥ 8 min no formato longo | Alerta |

**A revisão humana é padrão e intencional.** O gargalo de qualidade é o que separa este
projeto de uma fábrica de spam. `--yes` existe para quem quiser desligar, mas o default é
revisar.

## O que a máquina NÃO faz (por decisão)

- Não copia thumbnail, roteiro ou identidade visual de canal específico.
- Não gera volume ilimitado.
- Não publica sem divulgação de conteúdo sintético quando aplicável.
- Não promete retorno financeiro. As metas do projeto são operacionais (CTR, retenção,
  constância), não de receita.

## Nota sobre expectativa de receita

As promessas do tipo "R$ 6 mil em um vídeo" circulando no material de origem não vêm
acompanhadas de RPM, período, origem da receita, despesas ou retenção — não são
verificáveis e não devem ser usadas como base de planejamento.

Dois fatores que mudam a conta de forma relevante e que valem checar antes de escalar:

- **RPM varia enormemente por idioma/geografia.** O canal definido (`Setiap Level`,
  indonésio) atinge um mercado grande em audiência mas historicamente de RPM baixo
  comparado a EUA/UE. Volume de views ≠ receita equivalente.
- **Custo de produção por vídeo é real** (TTS, imagens, LLM). O
  `maquina cost` calcula o custo por vídeo para você comparar com o RPM observado, em
  vez de estimar no escuro.
