# Oceano azul + fluxo noturno de produção (04/08/2026)

Direção do operador: diversificar nichos (finanças, games, receitas/culinária)
e idiomas — incluindo mercados pouco disputados (turco, grego, hindi, polonês).
Este doc traz os dados, a matriz v2 e o fluxo "1 vídeo por canal → Drive →
upload noturno manual".

## RPM por país — dados 2026 (fontes no rodapé)

| País/idioma | CPM típico | RPM esperado | Leitura oceano azul |
|---|---|---|---|
| EUA (inglês) | US$ 8–20 RPM | topo | Máxima receita, máxima concorrência |
| **Polônia (polonês)** | US$ 2,52 | ~US$ 1,0–1,3 | **Melhor razão RPM ÷ concorrência da lista** |
| Grécia (grego) | US$ 2,00 | ~US$ 0,8–1,1 | Pouquíssima oferta; mercado pequeno (10 mi) |
| Turquia (turco) | US$ 0,75–1,10 | ~US$ 0,5–1,1 | 85 mi pessoas, YouTube gigante, oferta baixa |
| Índia (hindi) | US$ 0,83 | ~US$ 0,8 | Volume colossal compensa RPM baixo |
| Indonésia (id) | US$ 0,74 | ~US$ 0,7 (geral) / 1–5 (finanças) | Nossa base atual |

Nicho multiplica o RPM base: finanças 2–4×, games ~1× (volume alto),
culinária 1,5–2× (anunciante de CPG paga bem).

- A tese oceano azul é real: em polonês/turco/grego há fração da oferta de
  conteúdo faceless bem produzido; um vídeo mediano em inglês morre, o mesmo
  vídeo em polonês compete com dez, não dez mil.
- Contra-peso: mercados pequenos têm teto menor. O portfólio equilibra:
  EN (teto alto) + oceano azul (tração rápida) + ID/BR/ES (volume).

## Matriz v2 do portfólio (proposta — 3 nichos × 10 idiomas)

| # | Canal | Nicho | Idioma | Estilo | Voz edge-tts |
|---|---|---|---|---|---|
| 1 | Setiap Level | finanças | Indonésio | doodle | id-ID-ArdiNeural |
| 2 | Next Level Money | finanças | Inglês | voxlite | en-US-AndrewNeural |
| 3 | Kolejny Poziom | finanças | **Polonês** | voxlite | pl-PL-MarekNeural |
| 4 | Seviye Seviye | finanças | **Turco** | voxlite | tr-TR-AhmetNeural |
| 5 | Epómeno Epípedo | finanças | **Grego** | doodle | el-GR-NestorasNeural |
| 6 | Agla Level | finanças | **Hindi** | doodle | hi-IN-MadhurNeural |
| 7 | Level Ekonomi Game | economia dos games | Inglês | voxlite | en-GB-RyanNeural |
| 8 | Nível do Jogo | games/indústria | Português-BR | voxlite | pt-BR-AntonioNeural |
| 9 | Resep Naik Level | receitas econômicas | Indonésio | doodle | id-ID-GadisNeural |
| 10 | Cocina por Niveles | receitas econômicas | Espanhol | doodle | es-MX-JorgeNeural |

Notas de nicho:
- **Games**: não competir com gameplay (saturado). O ângulo é "a economia dos
  games" — quanto ganha um estúdio, por que skin custa caro, a matemática do
  free-to-play. É o nosso formato explicador aplicado a games (CPM de negócio,
  não de gameplay).
- **Receitas**: ângulo "cozinha + dinheiro" — receitas de baixo custo, quanto
  custa por porção, marmita da semana por X. Ilustrável em doodle, foge da
  guerra de vídeo filmado, casa com o DNA de finanças do portfólio.
- Todos os canais mantêm o mesmo motor (roteiro → SVG → voz → render → SEO);
  muda idioma, voz, paleta e eixos.

## O fluxo noturno (1 vídeo/canal → Drive → você sobe à noite)

Por canal, a máquina produz e salva numa subpasta do Drive
(`Setiap Level — Videos/<canal>/`):

1. `video.mp4` — longo 16:9, legendas queimadas, +faststart
2. `thumbnail.png` — 1280×720, 3 palavras grandes máx, contraste alto
3. `logo.png` — avatar 800×800 do canal (identidade da paleta)
4. `copy.md` — título (≤100c, keyword nos 5 primeiros termos), descrição
   completa (200+ palavras, keyword nas 150 primeiras posições, capítulos
   com timestamps, CTA, disclosure de conteúdo sintético), 8–15 tags,
   comentário fixado, configurações do Studio (idioma, categoria, público)
5. `capa.png` — banner 2560×1440 (quando canal novo)

Upload noturno (2 min/vídeo): Studio → Enviar → colar copy.md → thumbnail →
agendar. Checklist no próprio copy.md.

## Hacks/práticas para o 1º mês (com base em dados, não mito)

1. **Primeiras 24h decidem o teste do algoritmo**: publicar sempre no mesmo
   horário local do público-alvo (19h–21h), responder todo comentário na
   primeira hora, comentário fixado com pergunta.
2. **Título/thumb par de teste**: manter padrão de 3 palavras na thumb; se
   CTR <4% em 48h, trocar a thumb (YouTube re-testa).
3. **Retenção > tudo**: cold open com o dado mais forte nos primeiros 8s;
   sem intro, sem "bem-vindos".
4. **Shorts como funil**: 1 short/dia cortado do longo, com CTA falado para
   o vídeo completo.
5. **Sem truque proibido**: nada de sub4sub, compra de views, tags enganosas
   — em canal novo o YPP review derruba tudo.
6. **Métricas reais semanais**: `maquina diagnosticar` + comparação com o
   benchmark do nicho; a decisão do próximo vídeo sai do dado, não do gosto.

## A meta de US$ 2.000/mês — honestidade obrigatória

AdSense no mês 1 é matematicamente impossível: o YPP exige 1.000 inscritos +
4.000h (ou 10M views de Shorts) + análise humana. **Nenhum canal novo fatura
AdSense no primeiro mês.** O que o 1º mês constrói: catálogo, dados de CTR/
retenção e os primeiros milhares de views que alimentam o YPP.

Caminho realista para US$ 2.000/mês (cenário base, 10 canais ativos):
- Dia 120: ~US$ 400–600/mês (primeiros canais monetizados)
- **Dia ~200–240: cruza US$ 2.000/mês**
- Dia 365: ~US$ 5.500–6.500/mês

Aceleradores possíveis antes do YPP: afiliados nos vídeos de finanças/receitas
(links na descrição desde o dia 1 — Amazon/Shopee/Hotmart conforme mercado) e
licenciamento de conteúdo. São centavos no início, mas são os únicos dólares
que existem antes da monetização.

## Fontes

- [Dynamoi — RPM 89 mercados 2026](https://dynamoi.com/data/youtube-adsense-rpm)
- [IncomeFromViews — RPM por país 2026](https://incomefromviews.com/blog/youtube-rpm-by-country/)
- [TubeAnalytics — CPM por país](https://www.tubeanalytics.net/blog/youtube-cpm-by-country)
- [YTface — CPM rates by country](https://www.ytface.com/cpm-rates-by-country)
- docs/11 (RPM por nicho) e docs/12 (portfólio, compliance)
