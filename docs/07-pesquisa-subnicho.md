# Pesquisa do subnicho — resultados reais

Levantamento feito em 03/08/2026 sobre 144 vídeos dos canais de referência do
subnicho indonésio de dinheiro/trabalho/status. Ordenado por **views/dia**, não
por views absolutas.

## Canais de referência

| Canal | Vídeos no catálogo | Observação |
|---|---|---|
| **Raymond Chin** | 1.561 | Domina o nicho. Pessoa real, com rosto e autoridade |
| **Finance Clipper** | 293 | Clipes curtos de um comentarista |
| **Grind Theory** | 44 | **A referência mais replicável** — canal pequeno, alta velocidade |

## A primeira busca deu errado — e isso foi informativo

Buscar termos amplos ordenados por views trouxe **comédia de sketch**, não o
nicho: "Orang Kaya vs Miskin" (94k views/dia), conteúdo infantil, drama.

Esse cluster é conteúdo curto e repetitivo — exatamente o que
`03-compliance-monetizacao.md` identifica como risco. **Decisão registrada:
não perseguir esse formato.** A lição prática: pesquisar pelos *canais* do nicho
dá sinal muito melhor que buscar por *termos* amplos.

## O achado central: evergreen vs. notícia

| Tipo | Vídeos | Média views/dia |
|---|---|---|
| Ancorado em notícia | 10 | **25.887** |
| Evergreen | 30 | 16.447 |

Notícia performa ~57% melhor. **E mesmo assim a recomendação é evergreen.**

Motivo: os vídeos de notícia do Raymond Chin comentam política e economia
indonésias correntes (Prabowo, Sri Mulyani, PHK Tokopedia, PLN, IPO da RANS).
Isso exige apuração real e atualizada, e a autoridade dele — rosto, nome,
histórico — é o que sustenta o comentário.

Um canal automatizado e sem rosto que tentasse isso produziria comentário
político raso sobre fatos que não apurou, em um idioma que o operador não lê.
É errado do ponto de vista editorial e arriscado do ponto de vista de política
de plataforma.

**16.447 views/dia em evergreen é resultado excelente** e é automatizável.

## Os padrões que funcionam (base dos eixos temáticos)

Extraídos dos títulos de melhor performance:

1. **Pergunta provocativa** — "Kenapa..." (por quê), "Kok bisa..." (como pode)
   - *Jawaban Kenapa Orang Pintar OGAH di Indonesia* — 13.355/dia
2. **Paradoxo** — tem X mas continua Y
   - *BANYAK ORANG KAYA, MENTAL MISKIN* — 24.659/dia
3. **Alerta de risco** — caixa alta, urgência
   - *HATI HATI DIPECAT, KARYAWAN GAKBISA AI* — 75.978/dia no primeiro dia
4. **Comparação de escolhas**
   - *Lebih Penting GAJI BESAR atau PENGALAMAN BANYAK?* — 15.225/dia
5. **Realidade dura**
   - *Banyak Orang Indonesia Udah Putus Asa Buat Cari Kerja* — 26.689/dia
6. **Método prático**
   - *Cara ubah kerja 4 jam jadi 4 menit* — 18.172/dia
7. **Geração/grupo sob análise**
   - *Gen Z: Generasi Pertama yang Lebih Bodoh dari Orang Tuanya* — 15.307/dia

Esses sete viraram os `eixos_tematicos` em `config/default.yaml`. Não foram
inventados — cada um veio de um padrão medido.

## Grind Theory é a referência a estudar

Raymond Chin tem 1.561 vídeos e autoridade pessoal construída. Não é modelo
replicável para canal novo e sem rosto.

**Grind Theory tem 44 vídeos** e coloca conteúdo a 20.582 views/dia. Escala e
formato compatíveis com o ponto de partida do Setiap Level — e o tema é
exatamente carreira e decisões.

## Limites deste levantamento

- Amostra de 3 canais. Vale ampliar com mais referências do nicho.
- Views/dia usa a média desde a publicação; não captura a curva real.
- **Não há dado de CTR nem de retenção** aqui — são métricas privadas do dono do
  canal. Os pilares 2 e 3 só ficam mensuráveis com o YouTube Analytics do
  próprio canal, via `maquina diagnosticar`.

## Refazer

```bash
maquina pesquisar "<termo>"            # mostra
maquina pesquisar "<termo>" --aplicar  # grava as palavras-chave
```

Revisar a cada 2-3 meses, ou quando a performance do canal mudar de patamar.
