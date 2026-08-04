# Portfólio de 10 canais — lançamento simultâneo (decisão de 04/08/2026)

Decisão do operador: começar com 10 canais ativos, todos a custo R$ 0
(doodle + Vox-lite na própria máquina; sem Higgsfield). Este doc define a
matriz de diferenciação — a defesa contra classificação como rede de spam —
e os limites operacionais reais.

## A matriz (cada canal = identidade distinta)

| # | Canal (nome sugerido) | Modelo | Idioma/mercado | Nicho | Voz edge-tts | Paleta |
|---|---|---|---|---|---|---|
| 1 | **Setiap Level** (existente) | doodle | Indonésio | dinheiro/carreira/status | id-ID-ArdiNeural | preto + 2 acentos |
| 2 | Next Level Money | Vox-lite | Inglês (EUA) | economia/dinheiro/poder | en-US-AndrewNeural | editorial: creme/vermelho |
| 3 | Cada Nível | doodle | PT-BR | finanças pessoais/carreira | pt-BR-AntonioNeural | azul/amarelo |
| 4 | Cada Nivel | doodle | Espanhol (MX/LatAm) | finanzas/trabajo | es-MX-JorgeNeural | verde/laranja |
| 5 | Level Berikutnya | doodle | Indonésio | psicologia do dinheiro/hábitos | id-ID-GadisNeural (fem.) | roxo/rosa |
| 6 | The Power Map | Vox-lite | Inglês (global) | geopolítica/economia | en-GB-RyanNeural | sépia/burnt-orange (diorama) |
| 7 | Money Machines | Vox-lite | Inglês | como empresas/indústrias ganham dinheiro | en-US-GuyNeural | azul-marinho/dourado |
| 8 | Escala Global | Vox-lite | Espanhol | economía/geopolítica explicada | es-ES-AlvaroNeural | cinza/vermelho |
| 9 | Por Trás do Dinheiro | Vox-lite | PT-BR | economia/negócios explicados | pt-BR-FabioNeural | verde-escuro/branco |
| 10 | Daily Ladder | doodle | Inglês | hábitos/produtividade/renda | en-AU-WilliamNeural | teal/coral |

Regras de diferenciação (anti-rede): estilo visual próprio por canal (paleta,
espessura de traço, layout), voz distinta, nichos que não se sobrepõem no
mesmo idioma, descrições/branding independentes, e **nunca** o mesmo roteiro
traduzido publicado em dois canais na mesma semana.

## Limites operacionais reais

- **Cota da YouTube API**: `videos.insert` custa 1.600 unidades; cota padrão
  de 10.000/dia ≈ **6 uploads/dia por projeto**. 10 canais × 1 longo/dia = 10.
  → No formulário de auditoria (docs/10), ajustar o caso de uso para "my own
  channels (up to 10)" e **pedir extensão de cota junto** (~32.000/dia).
- **Antes da auditoria aprovada**: upload é manual no Studio. Cadência interina
  viável: **3 longos/semana por canal** (30 uploads/semana, ~45 min/dia do
  operador, usando agendamento nativo do Studio em 1 sessão semanal por canal).
  Cadência plena (1/dia/canal) liga quando a API liberar.
- **Contas**: os 10 canais podem ser canais de marca (brand accounts) sob o
  mesmo Gmail — gestão simples. Trocar o país de cada canal no Studio.
- **Compliance por canal**: teto 3/dia, similaridade ≤0,65 vs últimos 30,
  divulgação de conteúdo sintético — tudo já na máquina, aplicado por canal.

## Projeção revisada (10 canais desde o dia 1, cenário base)

Blend: 5 doodle (~US$ 18×t/mês cada) + 5 Vox-lite (RPM maior, ~US$ 96×t EN;
ES/PT-BR ~US$ 30-40×t). Receita potencial total ≈ US$ 450-570 × t (mês).

| Marco | Potencial/mês | Real (pós-YPP)/mês |
|---|---|---|
| Dia 30 | ~US$ 500 | US$ 0 |
| Dia 90 | ~US$ 1.500 | US$ 0-200 |
| Dia 120 | ~US$ 2.000 | ~US$ 400-600 (primeiros YPP) |
| Dia 180 | ~US$ 3.000 | ~US$ 2.000-2.500 |
| Dia 365 | ~US$ 6.000-6.800 | ~US$ 5.500-6.500 |

Pessimista ÷3 · Otimista ×3 · Risco de colapso em rede (~25% no lançamento
simultâneo): receita 0 — mitigado pela matriz de diferenciação acima.
Vantagem vs. escalonado: +US$ 3.000/mês no mês 12. Custo: variância maior.

## Sequência de ativação

1. Operador: criar os 9 canais de marca no Studio (nome, país, descrição,
   arte — a máquina gera os pacotes de branding de cada um)
2. Máquina: refatorar config multi-canal (`config/canais/*.yaml`, coluna
   `canal` no Supabase, CLI `--canal`)
3. Operador: enviar formulário de auditoria já com os 10 canais e extensão
   de cota (docs/10 atualizado)
4. Lançamento interino: 3 longos/semana/canal com agendamento no Studio
5. Auditoria aprovada → 1 longo/dia/canal automático via `publicacao.yml`
