#!/usr/bin/env python3
"""Monta a spec resep-naik-level-006.

CANAL. Veredito `suspenso` — e ele MUDOU nesta hora, por causa de um defeito
que eu corrigi antes de escrever isto.

  A `v_maquina_licoes` apagava o veredito do LONGO quando a amostra de SHORTS
  era fina: bastava `shorts_medidos < 3` para tudo virar 'sem dado'. Este canal
  tem SEIS longos medidos a 0,00 views/dia — a evidencia exata que `suspenso`
  existe para agir — e lia 'sem dado' porque so dois shorts tinham sido
  medidos. Seis medidas descartadas por causa de uma amostra que nao era a
  delas.
  A visao foi corrigida (migracao
  `licoes_veredito_do_longo_nao_depende_da_amostra_de_short`) e conferida nos
  treze canais ANTES de aplicar: um so mudou, este. Os doze outros mantiveram
  o veredito, inclusive os dois `liberado` e os dois `canal frio`.

Entao o longo aqui vai NO PISO da faixa (8 e pouco, nao 13) e o melhor
material vai no SHORT, que e o que a regra do `suspenso` manda. Seis longos a
zero view por dia nao pedem um setimo mais longo.

EIXO. Os tres titulos publicados sao todos a mesma coisa: uang dapur e harga
beras. O banco de pautas deste canal esta praticamente esgotado — 6 dos 8
outliers ja usados — e a unica linha "livre" no topo e LIXO: "Uang Belanja
Cuma 50 Ribu, Tapi Mertua Nuntut Makan Restoran (drama AI)", 6.057,0 v/d, do
canal gabutstudioID. E drama ficcional gerado por IA, a mesma contaminacao que
eu peguei no setiap-level horas atras (aprendizado 417). Descartada de novo.

  Como o banco nao tinha eixo utilizavel, a pauta veio de pesquisa nova — que
  e o que o PASSO 0 manda fazer quando o banco nao responde.

FORMATO. A estrutura que performa no nicho e "numero + cifra concreta +
publico nomeado": "4 STRATEGI ISTRI MENGATUR UANG 50-100RB PERHARI" mede
1.167,4 v/d; "Tips Belanja Mingguan Hemat Ala Ibu Rumah Tangga, Budget Rp150
Ribu", 478,5. O titulo daqui leva a cifra oficial no comeco.

A PAUTA — e ela tambem nasceu de fontes que se contradiziam.

  A primeira passagem de busca devolveu manchetes em duas direcoes:
    "Pemerintah sepakat menaikkan HET Minyakita"        (ANTARA)
    "HET Minyakita Naik Dua Minggu Lagi"                (Liputan6)
    "Kemendag Tegaskan HET Tetap di Rp15.700"           (RCTI+)
    "HET Minyakita Batal Naik"                          (detikFinance)

  A segunda passagem resolveu, e varios veiculos independentes batem:
    HET .............. Rp15.700 por litro, MANTIDO
    aumento .......... CANCELADO, anunciado pelo Mendag Budi Santoso
                       em 12 de junho de 2026
    inalterado desde . agosto de 2024
    motivo ........... o aumento exigia estabilidade do preco do CPO, e a
                       condicao nao foi atendida
    em vez disso ..... reforco da distribuicao via Perum Bulog e ID FOOD nos
                       mercados tradicionais
    regra de comercio  Kepmendag 2396/2025 (Domestic Price Obligation)

  Fontes que coincidem: CNN Indonesia, CNBC Indonesia, Bisnis, Tribunnews,
  ANTARA (agencia estatal) e sawitindonesia. Duas passagens, muitos veiculos.

A TESE: o aumento que voce ouviu falar foi cancelado, o teto legal e
Rp15.700 — e o preco que voce paga provavelmente nao e esse. A distancia entre
os dois e a unica coisa que importa para o seu orcamento, e so voce pode
medi-la.

O QUE O VIDEO NAO FAZ: NAO afirma um preco de mercado. Nao tenho fonte para o
preco de rua de cada regiao, e inventar um numero "medio" aqui seria pior que
nao dizer nada — a espectadora usaria o meu numero em vez de olhar o dela.
Tambem nao promete que o aumento nao vem, nem da data para ele.
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


def B(kicker, itens, alturas, nar):
    CENAS.append({"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ---------------------------------------------------------------- cap 1 (10)
T("Batal naik", "tapi ini cuma setengah kabar",
  "Kenaikan harga MinyaKita dibatalkan. Kedengarannya kabar baik, dan sebenarnya "
  "itu cuma setengah kabarnya.",
  cap="Batal naik, dan kenapa cuma setengah kabar")
I("Angka resminya", "lima belas ribu tujuh ratus",
  "Harga eceran tertinggi MinyaKita tetap lima belas ribu tujuh ratus rupiah "
  "per liter.")
I("Siapa yang mengumumkan", "Menteri Perdagangan",
  "Pembatalan itu diumumkan langsung oleh Menteri Perdagangan pada bulan Juni "
  "tahun ini.")
I("Sudah berapa lama", "sejak Agustus dua ribu dua puluh empat",
  "Dan angka itu sendiri tidak berubah sejak Agustus dua ribu dua puluh empat. "
  "Sudah dua tahun.")
I("Kenapa jadi batal", "syaratnya belum terpenuhi",
  "Rencana kenaikan itu mensyaratkan harga minyak sawit mentah stabil dulu. "
  "Syarat itu dinilai belum terpenuhi, jadi rencananya ditahan.")
I("Yang dipilih pemerintah", "distribusi, bukan harga",
  "Sebagai gantinya pemerintah memilih membenahi distribusi lewat Bulog dan ID "
  "Food, supaya MinyaKita lebih gampang ditemukan di pasar rakyat.")
T("Sekarang setengah yang hilang", "harga di pasarmu",
  "Sekarang bagian yang hampir tidak pernah masuk judul berita.")
I("Yang menentukan belanjamu", "bukan angka resmi",
  "Yang menentukan uang dapurmu bukan angka resmi itu. Yang menentukan adalah "
  "harga yang benar-benar kamu bayar di pasar, minggu ini.")
I("Dan itu saya tidak tahu", "tidak ada sumbernya",
  "Berapa harganya di pasarmu, saya tidak tahu. Tidak ada sumber untuk harga "
  "jalanan tiap daerah, dan mengarang angka rata-rata di sini justru lebih "
  "buruk daripada diam.")
I("Kenapa lebih buruk", "kamu akan pakai angka saya",
  "Lebih buruk karena kamu akan memakai angka saya, bukan angka pasarmu "
  "sendiri. Padahal yang menentukan belanjamu cuma yang kedua.")

# ---------------------------------------------------------------- cap 2 (10)
T("Yang saya bawa", "cara mengukur jaraknya",
  "Jadi yang saya bawa bukan harganya, tapi cara mengukur jarak antara angka "
  "resmi dan yang kamu bayar.",
  cap="Cara mengukur jarak itu")
I("Hitungannya satu pengurangan", "harga kamu dikurangi HET",
  "Hitungannya cuma satu pengurangan. Harga yang kamu bayar, dikurangi lima "
  "belas ribu tujuh ratus.")
I("Kalau hasilnya nol", "kamu dapat harga resmi",
  "Kalau hasilnya nol, kamu memang dapat harga resmi. Sekalian pastikan yang "
  "kamu beli itu MinyaKita, dengan melihat labelnya.")
I("Kalau di atas nol", "kalikan pemakaian sebulan",
  "Kalau hasilnya di atas nol, kalikan dengan berapa liter yang rumahmu pakai "
  "dalam sebulan. Ini hitungan yang hampir tidak ada yang melakukan.")
I("Contohnya begini", "empat liter sebulan",
  "Contoh. Rumah yang memakai empat liter sebulan, dan membayar dua ribu lebih "
  "mahal di tiap liter.")
I("Sebulan", "delapan ribu",
  "Selisihnya delapan ribu rupiah sebulan.")
I("Setahun", "sembilan puluh enam ribu",
  "Setahun jadi sembilan puluh enam ribu rupiah.")
I("Kenapa angka ini penting", "hilang tanpa terasa",
  "Angka segitu tidak membuat siapa pun bangkrut. Justru itu masalahnya: dia "
  "hilang tanpa terasa, karena tidak pernah muncul sebagai satu pengeluaran.")
B("Dua angka yang beda", ["HET resmi", "Harga di pasarmu"], [100, 100],
  "Saya sengaja menggambar dua batang ini sama tinggi. Punyamu belum tentu "
  "sama, dan mencari tahu selisihnya itulah tugas dari video ini.")
I("Kenapa harganya bisa beda", "ongkos, perantara, stok",
  "Penyebab selisihnya sudah diketahui: ongkos angkut, jumlah perantara, dan "
  "ketersediaan stok di daerahmu.")
I("Yang paling besar pengaruhnya", "jarak dan stok",
  "Dari ketiganya, yang paling terasa biasanya jarak dari gudang dan stok yang "
  "ada minggu itu. Dua-duanya berubah tiap bulan.")
I("Artinya harga bergerak", "bukan garis lurus",
  "Artinya harga di pasarmu bukan garis lurus. Dia naik turun, dan cuma "
  "catatan yang bisa memperlihatkan arahnya.")

# ---------------------------------------------------------------- cap 3 (9)
T("Tiga hal", "yang bisa kamu lakukan minggu ini",
  "Tiga hal untuk dikerjakan minggu ini. Ketiganya gratis dan tidak sampai "
  "sepuluh menit.",
  cap="Tiga hal untuk minggu ini")
I("Pertama", "catat harga dan tanggalnya",
  "Pertama, catat harga yang kamu bayar, lengkap dengan tanggalnya. Satu baris "
  "di buku atau di catatan ponsel sudah cukup.")
I("Kenapa harus pakai tanggal", "supaya bisa dibandingkan",
  "Tanggalnya penting, karena harga tanpa tanggal tidak bisa dibandingkan "
  "dengan apa pun.")
I("Hasilnya tiga bulan lagi", "datamu sendiri",
  "Dengan tanggal, dalam tiga bulan kamu punya datamu sendiri. Bukan data "
  "nasional, tapi data pasarmu.")
I("Kedua", "bandingkan dua tempat",
  "Kedua, cek harga di dua tempat pada minggu yang sama. Pasar tradisional dan "
  "warung dekat rumah.")
I("Yang sering muncul", "selisih antar-tempat lebih besar",
  "Sering kali selisih antara dua tempat itu lebih besar daripada selisih "
  "terhadap harga resmi.")
I("Artinya apa", "keputusan pindah tempat",
  "Kalau memang begitu di daerahmu, keputusan yang menghemat bukan menawar, "
  "tapi pindah tempat belanja.")
I("Ketiga", "pastikan labelnya MinyaKita",
  "Ketiga, pastikan yang kamu beli memang MinyaKita. Harga resmi tadi berlaku "
  "untuk merek itu, bukan untuk minyak goreng secara umum.")
I("Kenapa ini sering keliru", "membandingkan dua barang beda",
  "Membandingkan harga minyak merek lain dengan harga resmi MinyaKita berarti "
  "membandingkan dua barang yang berbeda, dan kesimpulannya jadi salah.")
I("Kalau di pasarmu tidak ada", "itu juga informasi",
  "Dan kalau MinyaKita memang tidak ada di pasarmu minggu ini, catat itu juga. "
  "Barang yang tidak ada adalah informasi, bukan kegagalan mencatat.")
I("Kenapa itu berguna", "distribusi sedang dibenahi",
  "Berguna karena justru distribusi yang sedang dibenahi. Catatan tentang "
  "kapan barangnya ada dan kapan tidak menunjukkan apakah perbaikannya sampai "
  "ke daerahmu.")

# ---------------------------------------------------------------- cap 4 (9)
T("Kenapa distribusi", "dan bukan harga",
  "Satu bagian lagi yang membantu memahami kenapa keputusannya seperti itu.",
  cap="Kenapa yang dibenahi distribusi")
I("Menaikkan harga resmi", "tidak menambah barang",
  "Menaikkan angka resmi tidak menambah satu liter pun minyak di pasar. Yang "
  "berubah cuma batas atasnya.")
I("Kalau barangnya sedikit", "harga tetap di atas",
  "Kalau barangnya memang sedikit di suatu daerah, harga di sana tetap di atas "
  "batas, berapa pun batasnya ditetapkan.")
I("Karena itu Bulog", "menambah jalur masuk",
  "Karena itu pilihannya jatuh ke Bulog dan ID Food: menambah jalur masuk "
  "barang ke pasar rakyat.")
I("Apa artinya buat kamu", "ketersediaan bisa berubah",
  "Buat kamu artinya satu hal praktis: ketersediaan di pasarmu bisa berubah "
  "dalam beberapa bulan ke depan, ke arah yang lebih baik.")
I("Cara memantaunya", "catatan tadi",
  "Dan cara memantau perubahan itu adalah catatan yang tadi saya minta. Tanpa "
  "catatan, perbaikan atau perburukan sama-sama tidak terasa.")
T("Satu kesalahan yang mahal", "menimbun waktu harga turun",
  "Ada satu kebiasaan yang kelihatan hemat dan sering tidak.")
I("Kesalahannya", "beli banyak sekaligus",
  "Waktu harga turun sedikit, godaannya adalah membeli banyak sekaligus untuk "
  "stok berbulan-bulan.")
I("Kenapa berisiko", "minyak punya umur",
  "Masalahnya minyak goreng punya umur simpan, dan cara menyimpannya di rumah "
  "menentukan apakah umur itu tercapai.")
I("Aturan sederhananya", "stok sebulan, bukan setahun",
  "Aturan yang aman: stok secukupnya untuk sebulan. Selisih beberapa ribu "
  "rupiah tidak sebanding dengan satu liter yang terbuang.")
I("Yang benar-benar menghemat", "tempat belanja, bukan borongan",
  "Yang benar-benar menghemat bukan borongan, tapi memilih tempat belanja "
  "dengan selisih paling kecil. Dan itu kembali ke catatanmu.")
T("Kalau harganya nanti naik", "apa yang berubah",
  "Sekarang bagian yang berguna disiapkan dari sekarang: apa yang berubah "
  "kalau suatu hari angka resmi itu memang naik.",
  cap="Kalau nanti benar-benar naik")
I("Yang naik dulu", "batas atasnya",
  "Yang naik lebih dulu adalah batas atasnya, bukan otomatis harga di pasarmu. "
  "Dua hal yang berbeda, walau namanya mirip.")
I("Di daerah yang stoknya cukup", "harga bisa tidak berubah",
  "Di daerah yang stoknya cukup, harga bisa saja tidak bergerak, karena "
  "harganya memang sudah di bawah batas.")
I("Di daerah yang stoknya seret", "harga sudah di atas",
  "Di daerah yang stoknya seret, harganya sering sudah di atas batas — jadi "
  "batas baru cuma mengejar kenyataan.")
I("Cara tahu kamu di mana", "catatanmu menjawab",
  "Dan cara mengetahui kamu ada di kelompok yang mana bukan menebak: catatan "
  "tiga bulan yang tadi saya minta sudah menjawab.")
B("Dua kemungkinan", ["Harga di bawah batas", "Harga di atas batas"],
  [62, 100],
  "Dua kemungkinan yang sangat berbeda, dan cuma catatan sendiri yang bisa "
  "memberi tahu kamu ada di sebelah mana.")
I("Kalau kamu di kelompok pertama", "kenaikan belum tentu terasa",
  "Kalau catatanmu menunjukkan harga di bawah batas, kenaikan batas belum "
  "tentu langsung terasa di belanjamu. Ada ruang di antara keduanya.")
I("Kalau kamu di kelompok kedua", "sudah terasa sejak lama",
  "Kalau catatanmu menunjukkan harga di atas batas, kamu sebenarnya sudah "
  "membayar kenaikan itu sejak lama, tanpa ada pengumuman apa pun.")
I("Dan itu yang paling sering", "di daerah yang jauh",
  "Dan kelompok kedua ini paling sering muncul di daerah yang jauh dari "
  "gudang, yang justru paling jarang dibicarakan di berita.")
I("Makanya catatan itu penting", "berita tidak bicara tentangmu",
  "Karena itu catatan pribadi lebih berguna daripada berita nasional: berita "
  "bicara tentang rata-rata, dan rata-rata bukan dapurmu.")
T("Satu hal untuk diingat", "kalau cuma satu",
  "Kalau dari semua ini kamu cuma mau mengingat satu hal.",
  cap="Satu hal untuk diingat")
I("Bukan angka resminya", "tapi selisihmu",
  "Yang perlu diingat bukan angka lima belas ribu tujuh ratus itu. Itu gampang "
  "dicari kapan saja.")
I("Yang tidak ada di mana pun", "selisih di pasarmu",
  "Yang tidak ada di berita mana pun adalah selisih di pasarmu. Itu cuma kamu "
  "yang bisa mengukur, dan hasilnya cuma berguna buat kamu.")
I("Butuh berapa lama", "sepuluh detik seminggu",
  "Mencatatnya butuh sepuluh detik seminggu. Setelah tiga bulan, kamu punya "
  "sesuatu yang tidak dimiliki siapa pun tentang dapurmu sendiri.")
T("Dua hal yang tidak saya janjikan", "supaya jelas",
  "Terakhir, dua hal yang tidak akan saya janjikan.")
I("Pertama", "bahwa harga tidak akan naik",
  "Saya tidak bilang harganya tidak akan naik. Pembatalan terjadi sekarang, "
  "dan alasannya kondisi pasar yang bisa berubah.")
I("Kedua", "tanggal keputusan berikutnya",
  "Dan saya tidak memberi tanggal kapan keputusan berikutnya diambil, karena "
  "memang tidak ada tanggal yang diumumkan.")
C("Resep Naik Level", "angka dulu, resep nanti",
  "Catat hari ini berapa kamu membayar per liter, lengkap dengan tanggalnya. "
  "Itu saja. Kalau video ini menghemat uangmu, tinggalkan langganan.")


# ---------------------------------------------------------------------- short
#
# O canal esta `suspenso`: e o SHORT que carrega este pacote. Ele entrega
# sozinho a cifra oficial, a data, o que o governo fez no lugar e a acao.
SHORT = [
    {"layout": "titulo", "kicker": "MinyaKita batal naik",
     "sub": "HET tetap Rp15.700",
     "nar": "Kenaikan harga MinyaKita dibatalkan. Batas atasnya tetap lima "
            "belas ribu tujuh ratus rupiah per liter.", "sem_cap": True},
    {"layout": "item", "kicker": "Sejak kapan", "preco": "Agustus 2024",
     "nar": "Angka itu tidak berubah sejak Agustus dua ribu dua puluh empat.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Kenapa batal", "preco": "syarat CPO",
     "nar": "Kenaikannya mensyaratkan harga minyak sawit mentah stabil, dan "
            "syarat itu belum terpenuhi.", "sem_cap": True},
    {"layout": "item", "kicker": "Yang menentukan", "preco": "harga di pasarmu",
     "nar": "Tapi yang menentukan uang dapurmu bukan batas atasnya. Yang "
            "menentukan adalah harga di pasarmu.", "sem_cap": True},
    {"layout": "cta", "kicker": "Resep Naik Level", "sub": "catat hari ini",
     "nar": "Catat hari ini berapa kamu bayar per liter, lengkap dengan "
            "tanggalnya.", "sem_cap": True},
]

COPY = """# MinyaKita: alta cancelada, teto Rp15.700 — e o preço que você paga

## TITULO
Minyak Goreng 2026: HET Rp15.700 Batal Naik, Tapi Cek Harga Aslimu Dulu

## DESCRICAO
Kenaikan harga MinyaKita dibatalkan. Kedengarannya kabar baik — dan cuma setengahnya, karena yang menentukan belanja dapurmu bukan angka resmi, tapi harga yang benar-benar kamu bayar di pasar.

ANGKA RESMINYA, DENGAN SUMBER

Harga Eceran Tertinggi (HET) MinyaKita tetap Rp15.700 per liter. Pembatalan kenaikan diumumkan Menteri Perdagangan pada Juni 2026. Angka Rp15.700 itu sendiri tidak berubah sejak Agustus 2024. Alasan pembatalan: rencana kenaikan mensyaratkan stabilitas harga CPO (crude palm oil), dan syarat itu dinilai belum terpenuhi. Sebagai gantinya, pemerintah memilih memperkuat DISTRIBUSI — lewat Perum Bulog dan ID FOOD, terutama ke pasar-pasar rakyat — bukan menaikkan harga. Tata niaga MinyaKita diatur dalam Kepmendag Nomor 2396 Tahun 2025 tentang Domestic Price Obligation.

YANG TIDAK ADA DI VIDEO INI, DAN KENAPA

Saya TIDAK menyebut berapa harga MinyaKita di pasar. Saya tidak punya sumber untuk harga jalanan tiap daerah, dan mengarang angka "rata-rata" di sini justru lebih buruk daripada diam: kamu akan memakai angka saya, bukan angka pasarmu sendiri. Yang saya bawa bukan harganya — tapi cara mengukur JARAK antara HET dan yang kamu bayar.

CARA MENGUKUR JARAK ITU

Kurangkan: harga yang kamu bayar dikurangi Rp15.700. Kalau nol, kamu dapat harga resmi (dan pastikan itu memang MinyaKita, lihat labelnya). Kalau di atas, kalikan dengan jumlah liter yang rumahmu pakai sebulan. Contoh hitungannya: rumah yang memakai 4 liter sebulan dan membayar Rp2.000 lebih mahal per liter mengeluarkan Rp8.000 lebih banyak sebulan — Rp96.000 setahun. Tidak membuat bangkrut siapa pun, dan justru itu jenis angka yang hilang tanpa terasa.

Kenapa harganya bisa beda dari HET? Ongkos angkut, jumlah perantara, dan ketersediaan di daerahmu. Itu juga sebabnya pemerintah memilih membenahi distribusi lebih dulu.

TIGA HAL UNTUK MINGGU INI (semuanya gratis)

1) Catat harga yang kamu bayar, LENGKAP DENGAN TANGGAL. Harga tanpa tanggal tidak bisa dibandingkan dengan apa pun; dengan tanggal, dalam tiga bulan kamu punya datamu sendiri.
2) Bandingkan dua tempat di minggu yang sama — pasar tradisional dan warung dekat rumah. Sering kali selisih antar-keduanya lebih besar daripada selisih terhadap HET, dan itu mengubah keputusan mau belanja di mana.
3) Pastikan yang kamu beli memang MinyaKita. HET itu berlaku untuk merek tersebut, bukan untuk minyak goreng secara umum — membandingkan harga minyak lain dengan HET MinyaKita berarti membandingkan dua barang berbeda.

DUA HAL YANG TIDAK SAYA JANJIKAN

Saya tidak bilang harga tidak akan naik: pembatalan terjadi sekarang, dan alasannya adalah kondisi pasar yang bisa berubah. Saya juga tidak memberi tanggal kapan keputusan berikutnya diambil, karena tidak ada tanggal yang diumumkan.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Satu pertanyaan, dan jawabannya yang paling saya butuhkan: berapa harga MinyaKita di pasarmu minggu ini, dan kamu di kota mana? Saya kumpulkan angkanya untuk materi berikutnya — karena justru inilah data yang tidak ada di berita mana pun, dan cuma kalian yang punya.

## HASHTAGS
#MinyaKita #UangDapur #ResepNaikLevel

## TAGS
minyakita, minyak goreng, het minyakita, harga minyak goreng 2026, uang dapur, belanja bulanan, hemat belanja, ibu rumah tangga, kemendag, bulog, id food, harga pangan, dapur hemat, keuangan keluarga, pasar tradisional

## CONFIGURACOES DO STUDIO
- Idioma: Bahasa Indonesia (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: desativados (duracao abaixo de 8 minutos e meio)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
HET MinyaKita de Rp15.700/litro, cancelamento do aumento anunciado pelo Ministro do Comercio em junho de 2026, valor inalterado desde agosto de 2024, condicao nao atendida (estabilidade do preco do CPO) e reforco de distribuicao via Perum Bulog e ID FOOD: conferidos em DUAS passagens de busca com veiculos independentes que coincidem — CNN Indonesia, CNBC Indonesia, Bisnis, Tribunnews, ANTARA (agencia estatal) e sawitindonesia. A primeira passagem trouxe manchetes CONTRADITORIAS (umas afirmando que o aumento sairia em duas semanas, outras que fora cancelado); a segunda resolveu a favor do cancelamento, e o registro dessa contradicao fica aqui de proposito. Este video NAO afirma preco de mercado em nenhuma regiao: nao ha fonte para isso e um numero medio inventado substituiria a medicao da propria espectadora. Nao ha previsao sobre aumento futuro nem data. O HET vale para a marca MinyaKita, nao para oleo de cozinha em geral. Material educativo de orcamento domestico.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/resep-naik-level-006.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-006",
    "idioma": "id",
    "voz": "id-ID-GadisNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#2A1E16", "c1": "#C4622D", "c2": "#3E8E6F",
               "bg": "#FBF4EC"},
    "thumb": {"l1": "Rp15.700", "l2": "batal naik"},
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/resep-naik-level-006.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
