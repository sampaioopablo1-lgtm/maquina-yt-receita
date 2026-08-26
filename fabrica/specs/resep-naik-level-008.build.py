#!/usr/bin/env python3
"""Monta a spec resep-naik-level-008.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA: 172 views no canal inteiro, ZERO inscritos, mediana de
4,83 views por dia por short e topo de 10,34.

O QUE DEU CERTO: o canal tem distribuicao. O topo de 10,34 views por dia e o
quarto melhor da frota, e isso num canal de nicho estreito.

O QUE NAO DEU, e o aprendizado 508 ja tinha dito: os tres eixos anteriores sao
o MESMO gesto repetido.

    005  arroz: BPS diz Rp15.545, no mercado pode ser Rp50 mil
    006  oleo de cozinha: o HET de Rp15.700 nao subiu, confira o seu
    007  GLP de 3 kg: nao existe preco nacional, ache o HET da sua regiao

Nos tres o espectador COMPARA um preco oficial com o preco que ele paga. A
conta acaba na porta do mercado, ele nao decide nada, e o quarto video igual
seria o quarto "confira se estao te cobrando certo". A superficie de preco
regulado do nicho acabou — e disso que fala o 508.

O QUE MUDEI: o objeto medido deixa de ser o PRECO e passa a ser o CONSUMO da
propria casa. A conta roda no que a familia termina por mes, a escolha e dela
todo dia, e o resultado nao depende de preco nenhum — o que e o unico jeito de
sair de um eixo esgotado sem sair do tema da cozinha.

E ha um instrumento que faz a conta caber em qualquer cozinha: as duas rotas
publicam os limites em SENDOK, nao so em grama. Quem tem colher tem balanca.

OS NUMEROS, e as duas rotas institucionais

  - Acucar: 50 g por pessoa por dia, equivalente a 4 colheres de sopa.
  - Sal: 2.000 mg de sodio por pessoa por dia, equivalente a 1 colher de cha.
  - Gordura: 67 g por pessoa por dia, equivalente a 5 colheres de sopa.

    rota 1  Kementerian Kesehatan (kemkes.go.id) — a Permenkes 30/2013, nas
            paginas da Promkes e da Ditjen P2P/P2PTM
    rota 2  BPOM (pom.go.id) — "Batas Maksimal Konsumsi Gula, Garam, Dan
            Lemak" e "Batasi Konsumsi Gula, Garam dan Lemakmu", com os mesmos
            gramas e as mesmas colheres

O QUE FICOU DE FORA, e o video diz em voz alta

  - PRECO de acucar, sal ou oleo. Alem de variar por regiao e por semana, e
    exatamente o eixo esgotado. O espectador usa a nota do proprio mercado.
  - Qualquer afirmacao de risco de doenca para uma pessoa especifica, e
    qualquer dieta, dose ou prescricao.
  - O limite de 67 g e de GORDURA TOTAL do dia, nao so do oleo de cozinha.
    Medir so o oleo da um PISO do consumo, nunca o total — e o video dedica um
    capitulo a isso para a conta nao ser usada errado.
  - Necessidade individual varia com idade, atividade e condicao de saude.
    Estes sao valores de referencia populacional.
"""
import json

CENAS = []


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def L(kicker, itens, nar):
    CENAS.append({"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ---------------------------------------- 1. Tiga bahan
T("Dapur Anda punya angka", "yang belum pernah dihitung",
  "Dapur Anda punya satu angka yang hampir tidak pernah dihitung siapa pun.",
  cap="Tiga bahan, satu takaran")
I("Bukan harga", "kali ini bukan harga",
  "Kali ini bukan harga. Harga sudah kita bahas berkali-kali di kanal ini.")
T("Kali ini yang dihitung", "adalah pemakaian",
  "Yang dihitung sekarang adalah pemakaian rumah Anda sendiri.")
L("Tiga bahan saja", ["gula", "garam", "minyak"],
  "Tiga bahan saja: gula, garam, dan minyak goreng.")
T("Ketiganya punya batas", "yang sudah diterbitkan",
  "Ketiganya punya batas harian yang sudah diterbitkan, per orang, per hari.")
I("Dan batasnya dalam sendok", "bukan cuma dalam gram",
  "Dan yang membuat ini bisa dikerjakan: batasnya juga ditulis dalam sendok, "
  "bukan cuma dalam gram.")
T("Dan ketiganya dibeli dengan uang", "uang dapur Anda",
  "Dan ketiganya dibeli dengan uang dapur Anda sendiri, setiap bulan, "
  "tanpa pernah dijumlahkan.")
T("Punya sendok berarti punya timbangan", "itu intinya",
  "Artinya siapa pun yang punya sendok makan sudah punya alat ukurnya.")
T("Ini bukan nasihat medis", "dan bukan diet",
  "Satu hal dulu: ini bukan nasihat medis dan bukan program diet. Ini angka "
  "resmi, dan cara menghitungnya di rumah Anda.")

# ---------------------------------------- 2. Dari mana
T("Dari mana angkanya", "dua lembaga, angka yang sama",
  "Sebelum menghitung, dari mana angkanya. Dua lembaga yang berbeda, dan "
  "keduanya menyebut angka yang sama.",
  cap="Dari mana angkanya")
I("Yang pertama", "Kementerian Kesehatan",
  "Yang pertama Kementerian Kesehatan, lewat Permenkes tahun dua ribu tiga "
  "belas dan halaman-halaman promosi kesehatannya.")
I("Yang kedua", "BPOM",
  "Yang kedua BPOM, di halaman tentang batas maksimal konsumsi gula, garam, "
  "dan lemak.")
T("Dua lembaga berbeda", "satu angka yang sama",
  "Dua lembaga berbeda menerbitkan angka yang sama. Itu syarat sebuah angka "
  "boleh masuk ke video di kanal ini.")
I("Gula", "lima puluh gram sehari",
  "Gula: lima puluh gram per orang per hari. Setara empat sendok makan.")
I("Garam", "dua ribu miligram natrium",
  "Garam: dua ribu miligram natrium per orang per hari. Setara satu sendok "
  "teh.")
I("Lemak", "enam puluh tujuh gram",
  "Lemak: enam puluh tujuh gram per orang per hari. Setara lima sendok makan.")
T("Empat, satu, lima", "itu saja yang perlu diingat",
  "Empat sendok makan, satu sendok teh, lima sendok makan. Itu saja yang "
  "perlu diingat dari seluruh video ini.")

# ---------------------------------------- 3. Hitungan
T("Sekarang hitungannya", "tiga langkah",
  "Sekarang hitungannya. Tiga langkah, dan semuanya di dapur Anda sendiri.",
  cap="Hitungan sebulan Anda")
I("Langkah satu", "catat yang habis sebulan",
  "Langkah satu: catat berapa banyak gula, garam, dan minyak yang habis di "
  "rumah Anda selama sebulan.")
T("Kemasannya sudah menulis beratnya", "jadi tinggal dijumlahkan",
  "Kemasannya sudah menulis beratnya. Jadi tinggal menjumlahkan yang dibeli "
  "dan dipakai.")
I("Langkah dua", "bagi jumlah orang",
  "Langkah dua: bagi angka itu dengan jumlah orang yang makan di rumah.")
I("Langkah tiga", "bagi tiga puluh hari",
  "Langkah tiga: bagi lagi dengan tiga puluh hari. Sekarang angkanya per "
  "orang per hari.")
T("Dan baru sekarang", "dibandingkan",
  "Dan baru sekarang angka itu boleh dibandingkan dengan batas tadi.")
T("Contoh yang bulat", "supaya mekanismenya terlihat",
  "Contoh dengan angka bulat, supaya mekanismenya terlihat.")
T("Tiga kilo gula, empat orang", "sebulan",
  "Misalnya tiga kilogram gula habis sebulan di rumah berisi empat orang.")
T("Hasilnya", "dua puluh lima gram sehari",
  "Dibagi empat orang, lalu dibagi tiga puluh hari, hasilnya sekitar dua "
  "puluh lima gram per orang per hari. Setengah dari batas.")

# ---------------------------------------- 4. Sendok
T("Kalau kemasan tidak membantu", "pakai sendok",
  "Kalau di rumah Anda gula dan minyak dibeli curah, kemasan tidak membantu. "
  "Di situ sendok mengambil alih.",
  cap="Sendok sudah cukup")
I("Cara sendok", "hitung yang masuk masakan",
  "Caranya: selama seminggu, hitung sendok yang benar-benar masuk ke "
  "masakan.")
T("Satu minggu cukup", "tidak perlu sebulan",
  "Satu minggu sudah cukup untuk cara ini, karena yang dihitung kejadian "
  "harian, bukan belanja.")
I("Lalu bagi", "orang dan hari",
  "Lalu dibagi jumlah orang dan jumlah hari, persis seperti tadi.")
T("Dua cara, satu jawaban", "dan itu bagus",
  "Jadi ada dua cara masuk: lewat kemasan sebulan, atau lewat sendok "
  "seminggu.")
T("Kalau hasilnya mirip", "berarti catatan Anda rapi",
  "Kalau keduanya memberi angka yang mirip, catatan Anda rapi. Kalau jauh "
  "berbeda, biasanya ada yang lupa dicatat.")
T("Catat saat memasak", "bukan malam harinya",
  "Catat sewaktu memasak, bukan malam harinya sambil mengingat-ingat. "
  "Ingatan selalu meleset ke arah yang sama.")
I("Yang paling sering lupa", "gorengan dan minuman manis",
  "Yang paling sering lupa dicatat: minyak untuk gorengan, dan gula di dalam "
  "minuman.")
T("Minuman manis itu gula juga", "walaupun bukan dari toples",
  "Gula di dalam minuman tetap gula, walaupun tidak diambil dari toples di "
  "dapur.")

# ---------------------------------------- 5. O piso
T("Sekarang bagian jujur", "angka minyak itu lantai",
  "Sekarang bagian yang harus jujur, dan ini penting supaya hitungan tadi "
  "tidak dipakai salah.",
  cap="Angka minyak itu lantai, bukan atap")
I("Batas enam puluh tujuh gram", "adalah lemak total",
  "Batas enam puluh tujuh gram itu untuk lemak total sehari. Bukan hanya "
  "minyak goreng.")
T("Lemak juga ada di dalam bahan", "bukan cuma di wajan",
  "Lemak juga ada di dalam daging, telur, santan, keju, dan makanan kemasan.")
T("Jadi kalau Anda mengukur minyak", "Anda mengukur sebagian",
  "Jadi kalau Anda hanya mengukur minyak goreng, Anda sedang mengukur "
  "sebagian saja.")
I("Artinya", "angkanya lantai, bukan atap",
  "Artinya angka yang Anda dapat adalah lantai, bukan atap. Konsumsi "
  "sebenarnya ada di atasnya.")
T("Dan itu tetap berguna", "justru karena jujur",
  "Dan itu tetap berguna. Kalau minyak saja sudah mendekati batas, sisanya "
  "sudah pasti melewati.")
T("Untuk gula dan garam", "ceritanya mirip",
  "Untuk gula dan garam ceritanya mirip: yang dari dapur terhitung, yang "
  "dari makanan kemasan tidak.")
T("Itu sebabnya label ada", "dan itu video lain",
  "Di situlah label kemasan masuk, dan itu hitungan lain untuk hari lain.")

# ---------------------------------------- 6. Onde para
T("Di mana hitungan ini berhenti", "dan berhentinya jelas",
  "Di mana hitungan ini berhenti, karena berhentinya cukup jelas.",
  cap="Di mana hitungan ini berhenti")
T("Ini angka rujukan penduduk", "bukan resep perorangan",
  "Angka tadi adalah rujukan untuk penduduk secara umum. Kebutuhan tiap orang "
  "berbeda menurut usia, aktivitas, dan kondisi kesehatan.")
I("Tidak ada harga di sini", "sengaja",
  "Tidak ada satu pun harga di video ini, dan itu disengaja. Harga berbeda "
  "tiap daerah dan tiap minggu.")
T("Nota belanja Anda lebih akurat", "daripada rata-rata mana pun",
  "Nota belanja Anda sendiri lebih akurat daripada rata-rata mana pun yang "
  "bisa saya sebutkan.")
I("Dan bukan soal masakan daerah", "tidak ada masakan yang dilarang",
  "Tidak ada masakan yang dilarang di sini, dan tidak ada resep yang "
  "dihakimi. Yang diukur takaran, bukan menu.")
T("Ini juga bukan diagnosis", "dan bukan dosis",
  "Ini juga bukan diagnosis, bukan dosis, dan bukan anjuran pengobatan.")
I("Kalau ada kondisi kesehatan", "bicarakan dengan tenaga kesehatan",
  "Kalau ada kondisi kesehatan, kehamilan, atau pengobatan yang sedang "
  "berjalan, bicarakan dengan tenaga kesehatan sebelum mengubah apa pun.")
T("Yang video ini berikan", "adalah satu angka rumah Anda",
  "Yang video ini berikan hanya satu hal: satu angka milik rumah Anda, yang "
  "bisa dibandingkan dengan angka resmi.")

# ---------------------------------------- 7. Trinta dias
T("Tiga puluh hari", "dan satu catatan",
  "Jadi tugas bulan ini kecil saja.",
  cap="Tiga puluh hari, satu catatan")
L("Catat tiga baris", ["gula yang habis", "garam yang habis",
                       "minyak yang habis"],
  "Catat tiga baris: gula yang habis, garam yang habis, minyak yang habis.")
I("Di akhir bulan", "bagi orang, lalu bagi hari",
  "Di akhir bulan, bagi jumlah orang, lalu bagi jumlah hari.")
T("Bandingkan dengan empat, satu, lima", "dalam sendok",
  "Bandingkan hasilnya dengan empat sendok makan, satu sendok teh, dan lima "
  "sendok makan.")
T("Simpan catatannya", "supaya bulan depan ada pembanding",
  "Simpan catatan itu. Bulan depan Anda punya pembanding, dan membandingkan "
  "rumah Anda dengan rumah Anda sendiri jauh lebih berguna.")
T("Satu bulan belum pola", "tiga bulan sudah",
  "Satu bulan belum menunjukkan pola. Tiga bulan sudah, dan pola itulah yang "
  "bisa diubah.")
I("Dan kalau angkanya tinggi", "itu informasi, bukan vonis",
  "Kalau angkanya keluar tinggi, itu informasi, bukan vonis. Yang tidak "
  "diukur memang tidak bisa diperbaiki.")
C("Mulai catat hari ini", "dan tulis hasilnya",
  "Mulai catat hari ini, dan tulis di kolom komentar berapa hasil rumah Anda "
  "untuk salah satu dari tiga bahan itu. Kalau hitungan dengan sumber resmi "
  "seperti ini berguna, silakan berlangganan — di sini angkanya selalu dari "
  "dua lembaga, dan kalau keduanya berbeda saya bilang.")

SHORT = [
    {"layout": "titulo", "kicker": "Batasnya ditulis dalam sendok",
     "sub": "bukan cuma dalam gram",
     "nar": "Batas harian gula, garam, dan minyak ditulis juga dalam sendok. "
            "Jadi siapa pun bisa mengukurnya.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Empat, satu, lima",
     "sub": "per orang per hari",
     "nar": "Empat sendok makan gula, satu sendok teh garam, lima sendok "
            "makan minyak. Per orang, per hari.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Hitungnya begini",
     "sub": "sebulan, orang, hari",
     "nar": "Catat yang habis sebulan, bagi jumlah orang, lalu bagi tiga "
            "puluh hari.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Baru sesudah itu",
     "sub": "angkanya bisa dibandingkan",
     "nar": "Baru sesudah itu angka rumah Anda bisa dibandingkan dengan "
            "batasnya.", "sem_cap": True},
    {"layout": "cta", "kicker": "Satu angka menipu",
     "sub": "dan itu yang minyak",
     "nar": "Ada satu dari tiga angka itu yang menipu, dan penjelasannya ada "
            "di video lengkap di bawah.", "sem_cap": True},
]

THUMB = {"l1": "Empat, satu, lima", "l2": "per orang per hari"}

COPY = """# Tiga bahan, satu takaran, dan hitungannya ada di dapur Anda

## TITULO
Gula, Garam, Minyak: Empat Sendok, Satu Sendok Teh, Lima Sendok — Hitung Rumah Anda

## DESCRICAO
Dapur Anda punya satu angka yang hampir tidak pernah dihitung siapa pun, dan kali ini angka itu bukan harga. Yang dihitung di sini adalah pemakaian rumah Anda sendiri, untuk tiga bahan saja: gula, garam, dan minyak goreng. Ketiganya punya batas harian yang sudah diterbitkan, per orang per hari — dan yang membuat hitungan ini bisa dikerjakan siapa pun adalah bahwa batasnya juga ditulis dalam sendok, bukan hanya dalam gram. Siapa punya sendok makan sudah punya alat ukurnya.

Angkanya berasal dari dua lembaga yang berbeda dan keduanya menyebut hal yang sama: Kementerian Kesehatan, lewat Permenkes tahun 2013 dan halaman promosi kesehatannya, dan BPOM, di halaman tentang batas maksimal konsumsi gula, garam, dan lemak. Gula: 50 gram per orang per hari, setara empat sendok makan. Garam: 2.000 miligram natrium per orang per hari, setara satu sendok teh. Lemak: 67 gram per orang per hari, setara lima sendok makan. Empat, satu, lima — itu saja yang perlu diingat.

Hitungannya tiga langkah dan semuanya di rumah: catat berapa banyak gula, garam, dan minyak yang habis selama sebulan, bagi dengan jumlah orang yang makan di rumah, lalu bagi lagi dengan 30 hari. Baru sesudah itu angkanya boleh dibandingkan dengan batas tadi. Ada juga jalur kedua untuk rumah yang membeli curah: menghitung sendok yang benar-benar masuk ke masakan selama seminggu. Kalau kedua jalur memberi angka yang mirip, catatan Anda rapi; kalau jauh berbeda, biasanya ada yang lupa dicatat — paling sering minyak gorengan dan gula di dalam minuman.

Satu bab dipakai khusus untuk bagian yang harus jujur: batas 67 gram itu untuk lemak total sehari, bukan hanya minyak goreng. Lemak juga ada di dalam daging, telur, santan, keju, dan makanan kemasan. Jadi kalau Anda hanya mengukur minyak, angka yang Anda dapat adalah lantai, bukan atap — konsumsi sebenarnya ada di atasnya. Itu tetap berguna, justru karena jujur: kalau minyak saja sudah mendekati batas, sisanya sudah pasti melewati.

Tidak ada satu pun harga di video ini, dan itu disengaja. Video ini juga bukan nasihat medis, bukan diagnosis, bukan dosis, dan bukan program diet.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Coba satu bahan saja dulu, yang paling gampang dicatat di rumah Anda, lalu tulis hasilnya di sini: berapa gram per orang per hari yang keluar, dan bahan mana yang Anda pilih. Saya ingin tahu bahan mana yang paling sering meleset dari perkiraan orang — dugaan saya minyak, karena minyak gorengan hampir tidak pernah masuk hitungan siapa pun, tapi itu dugaan saya dan saya lebih percaya angka dari dapur yang benar-benar dicatat.

## HASHTAGS
#UangDapur #GulaGaramLemak #ResepNaikLevel

## TAGS
batas konsumsi gula garam lemak, gula 50 gram per hari, garam 1 sendok teh, minyak 5 sendok makan, permenkes 30 2013, bpom gula garam lemak, hitung konsumsi rumah tangga, uang dapur, masak hemat, konsumsi gula harian, natrium 2000 mg, lemak total harian, dapur keluarga indonesia, catatan belanja bulanan, gizi keluarga

## CONFIGURACOES DO STUDIO
- Idioma: Indonesio (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Consultado em 26 de agosto de 2026. Os tres limites foram conferidos em DUAS rotas institucionais independentes que se confirmam. (1) KEMENTERIAN KESEHATAN (kemkes.go.id): a Permenkes numero 30 de 2013 e as paginas da Direcao de Promocao da Saude e da Ditjen P2P/P2PTM sobre a recomendacao diaria de acucar, sal e gordura. (2) BPOM (pom.go.id): as paginas "Batas Maksimal Konsumsi Gula, Garam, Dan Lemak" e "Batasi Konsumsi Gula, Garam dan Lemakmu". As duas publicam os mesmos valores, e nas mesmas duas unidades: acucar 50 g por pessoa por dia, equivalente a 4 colheres de sopa; sal 2.000 mg de sodio por pessoa por dia, equivalente a 1 colher de cha; gordura 67 g por pessoa por dia, equivalente a 5 colheres de sopa.

AVISO SOBRE OS NUMEROS — o que foi descartado e por que. (a) Nenhum PRECO de acucar, sal ou oleo entra neste video. Alem de variar por regiao e por semana, preco regulado ja foi o eixo dos tres videos anteriores deste canal e a superficie dele se esgotou; a nota do mercado do proprio espectador descreve a casa dele melhor do que qualquer media. (b) O limite de 67 g e de GORDURA TOTAL do dia e nao apenas do oleo de cozinha — medir so o oleo entrega um PISO do consumo, jamais o total, e o video dedica um capitulo inteiro a esse ponto justamente para a conta nao ser usada errado. O mesmo vale para acucar e sal: o que vem do armario e contado, o que vem de alimento embalado nao. (c) Nao ha aqui nenhuma afirmacao de risco de doenca para uma pessoa especifica, nem dieta, dose, diagnostico ou prescricao. As necessidades individuais variam com idade, atividade e condicao de saude, e os valores citados sao referencias populacionais. Este e material educativo e nao substitui consulta com profissional de saude; quem tem condicao de saude, gravidez ou tratamento em curso decide qualquer mudanca com quem acompanha o caso.
"""

SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-008",
    "idioma": "id",
    "voz": "id-ID-GadisNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#1F2430", "c1": "#C2410C", "c2": "#0E7490", "bg": "#FAF5EF"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "resep-naik-level-008.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
