# Próximo vídeo longo — Setiap Level

## Decisão

Eixo confirmado: **divida/pinjol — sistema 4 pilares**.

Benchmark de referência: Rory Asyari (canal pinjol/divida, frio) → 9.467 views/dia median.
Diagnóstico do canal: 0 views nos longos = canal frio, não falha de conteúdo.
Shorts são o motor de tração — mas o longo precisa existir para reter quem chega.

---

## Título escolhido

```
7 Langkah Bebas dari Pinjol dalam 90 Hari: Sistem yang Benar-Benar Berhasil
```

*(7 Passos Livres do Pinjol em 90 Dias: Sistema que Realmente Funciona)*

**Fórmula aplicada**: número exato + segunda pessoa implícita + prazo concreto + anti-genérico.

### Alternativas (caso título acima falhe na similaridade):

```
Saya Lunasi 5 Pinjol dalam 3 Bulan: Rencana Nyata, Bukan Motivasi
Cara Keluar dari Hutang Pinjol Tanpa Stres: 4 Langkah yang Benar
Berapa Lama Kamu Bisa Bebas dari Pinjol? Hitung Bareng Saya
```

---

## Ângulo editorial

Sistema completo 4 pilares (não motivação, não conselho genérico):

1. **Dana darurat** — reserva de emergência mínima antes de qualquer amortização
2. **Hutang aktif** — ranking de dívidas por taxa, método avalanche adaptado
3. **Investasi awal** — R$ mínimo para bater inflação enquanto paga dívida
4. **Perlindungan pensiun** — proteção previdenciária básica (BPJS Ketenagakerjaan)

Tese central: a maioria falha porque ataca a dívida sem reserva → qualquer imprevisto recria a dívida.

---

## Estrutura do roteiro (12–15 min)

| Capítulo | Conteúdo | Duração est. |
|----------|----------|--------------|
| 0. Gancho | Número concreto: "Rata-rata orang Indonesia butuh 2 tahun keluar dari pinjol. Saya tunjukkan cara 90 hari." | 0:00–0:15 |
| 1. O erro que todo mundo comete | Atacar dívida sem reserva → o ciclo não para | 0:15–2:00 |
| 2. Pilar 1: Dana darurat | Mínimo 1 bulan pengeluaran antes de amortizar | 2:00–4:00 |
| 3. Pilar 2: Ranking das dívidas | Taxa → ranking → método avalanche adaptado | 4:00–6:30 |
| 4. Pilar 3: Investasi minimal | Por que não zerar tudo antes de investir | 6:30–9:00 |
| 5. Pilar 4: Proteksi | BPJS, bukan asuransi jiwa dulu | 9:00–11:00 |
| 6. Simulação 90 dias | Exemplo com gaji 4jt, hutang 8jt | 11:00–13:30 |
| 7. Fechamento | Síntese + pergunta para comentários | 13:30–14:30 |

**Total estimado**: ~14 min | ~2.100 palavras de narração

---

## Como produzir

### Opção A — comando direto (via workflow dispatch)

No GitHub Actions → `Producao de video` → Run workflow:
- **formato**: longo
- **titulo**: `7 Langkah Bebas dari Pinjol dalam 90 Hari: Sistem yang Benar-Benar Berhasil`
- **quantidade**: (deixar vazio — título explícito produz 1 vídeo)

### Opção B — via CLI local

```bash
export MAQ_CANAL=setiap-level
maquina produzir \
  "7 Langkah Bebas dari Pinjol dalam 90 Hari: Sistem yang Benar-Benar Berhasil" \
  --angulo "sistema 4 pilares: dana darurat, hutang aktif, investasi awal, perlindungan pensiun" \
  --formato longo
```

---

## Tags recomendadas

```
pinjol, hutang, bebas hutang, keuangan pribadi, dana darurat, investasi,
cicilan, finansial, gaji, ekonomi indonesia, cara keluar hutang, pinjol legal
```

---

## Checklist antes de publicar

- [ ] Duração ≥ 8 min (requisito de múltiplos blocos de anúncio)
- [ ] Thumbnail: texto ≤ 3 palavras, rosto/gráfico forte, contraste alto
- [ ] Descrição com timestamps dos 7 capítulos
- [ ] Tags: 12–15, mistura broad + specific
- [ ] Legenda .srt baixada do artefato e carregada no YouTube Studio
- [ ] `conteudo_sintetico: true` confirmado no upload
