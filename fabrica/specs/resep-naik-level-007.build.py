#!/usr/bin/env python3
"""Monta a spec resep-naik-level-007.

ALAVANCA ATACADA: **A — conversao short -> inscrito**. Numero de partida:
**0,00%**. Quatro shorts, 144 views somadas, ZERO inscritos. Doze videos no
canal inteiro, 172 views, zero inscritos.

Isso bate o gatilho da secao 3 da rotina — "canal com 0 inscritos depois de 10
videos merece EIXO NOVO ou pausa". Escolhi EIXO NOVO, e o motivo esta no
numero: os shorts deste canal RECEBEM entrega (mediana 5,51 views/dia, topo
11,94), o que e sinal de que a audiencia existe. O que nao existe e conversao.
Pausar um canal que recebe entrega seria jogar fora o insumo antes de testar a
unica variavel que importa.

O QUE DEU CERTO, short a short:

    63 views  11,94 v/d  "Beras Rp15.545 Kata BPS, di Pasar Bisa Rp50 Ribu"
    41 views   5,65 v/d  "Menu Hemat Rp100 Ribu Seminggu"      (52,0% ret)
    25 views   5,37 v/d  "Minyak Goreng 2026: HET Rp15.700"    (21,5% ret)
    15 views   1,87 v/d  "5 Strategi Ibu Mengatur Uang Dapur"

O melhor de todos e o que poe o numero OFICIAL contra o que a pessoa paga de
verdade: quinze mil e quinhentos segundo o BPS, cinquenta mil no mercado. O
pior e a listinha de cinco estrategias — fato sobre o mundo, exatamente o que o
aprendizado 487 diz que nao converte.

O QUE NAO DEU: o longo, e sem meio-termo. Oito longos e 28 views SOMADAS.
Quatro deles sao a MESMA duplicata publicada pelo cron em quatro dias
seguidos, e tres dessas quatro tem zero view. Veredito `suspenso`.

O QUE VOU MUDAR POR CAUSA DISSO:

  1. EIXO NOVO: LPG 3 kg. Os publicados cobrem beras, minyak goreng, menu
     hemat, belanja semanal e "5 estrategias". O gas de cozinha — que e o
     insumo mais caro e mais regulado da cozinha indonesia — nunca.

  2. A FORMA DO QUE MEDIU MELHOR: numero oficial CONTRA o que a pessoa paga.
     E aqui isso nao e retorica, e a estrutura do assunto: nao existe preco
     nacional do LPG 3 kg. O HET e fixado por Pergub ou Perbup, e difere de
     verdade — Jakarta tem um valor no pangkalan e Jateng e Jatim tem outro.

  3. A CONTA NA SEGUNDA PESSOA (aprendizado 487): o numero de partida e o que
     o espectador PAGOU na ultima compra — ele nao precisa de documento
     nenhum, so da memoria. O short entrega a subtracao inteira.

DURACAO no piso do `suspenso`: pouco acima de 9 min. Neste canal os segundos
vistos ficam entre 8 e 23 — nao ha retencao a defender alongando.

--------------------------------------------------------------------- A PAUTA

FONTES INSTITUCIONAIS, duas que se confirmam e nao se sobrepoem:

  1. KEMENTERIAN ESDM / DITJEN MIGAS (esdm.go.id e migas.esdm.go.id), com
     corroboracao do Setkab (setkab.go.id):
       desde 1 de janeiro de 2024 .... a compra do tubo de 3 kg so e feita
                                       por usuario JA CADASTRADO.
       como se cadastra .............. apresentando KTP e KK no penyalur ou
                                       pangkalan oficial. Usuario de usaha
                                       mikro precisa ainda de foto no local
                                       do negocio.
       quem tem direito .............. rumah tangga (para cozinhar), usaha
                                       mikro (para cozinhar), nelayan sasaran
                                       e petani sasaran, conforme a Perpres
                                       104 de 2007 e a Perpres 38 de 2019.
       limite por compra ............. um tubo por transacao, principio de
                                       "satu KTP satu tabung".

  2. JDIH E GOVERNOS REGIONAIS (jdih.jakarta.go.id, jatengprov.go.id,
     acehprov.go.id, jdih.jabarprov.go.id):
       o HET NAO e nacional ......... e fixado por Peraturan Gubernur ou
                                      Peraturan Bupati, e difere por regiao.
       DKI Jakarta .................. Rp 16.000 no nivel do pangkalan.
       Jawa Tengah .................. Rp 18.000 (Kepgub 540/20 de 2024).
       Jawa Timur ................... Rp 18.000 (desde 15/01/2025).

O CUIDADO QUE O VIDEO TOMA: ele NAO afirma um preco nacional, porque nao
existe. Ele ensina a achar o proprio e diz que os valores citados sao exemplos
de regioes especificas, com a norma que os fixa.

A CONTA, na segunda pessoa e sem documento nenhum: quanto voce pagou menos o
HET da sua regiao, vezes quantos tubos voce usa por mes, vezes doze. Com HET
de dezoito mil e compra a vinte e cinco mil, a diferenca e de sete mil por
tubo; a tres tubos por mes da vinte e um mil por mes e duzentos e cinquenta e
dois mil por ano. Os sete mil sao HIPOTESE do espectador; o HET e que e
fonte.

O QUE O VIDEO NAO FAZ: nao diz o HET de nenhuma regiao alem das citadas, nao
acusa comerciante nenhum, e nao promete que o preco do pangkalan esteja sempre
disponivel.

ACENTOS. Indonesio nao usa diacritico; numeros por extenso sempre.
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


# ============================ OS PRIMEIROS 200 SEGUNDOS ======================
# Achar o proprio HET e fazer a subtracao sai nos capitulos 1 a 3.

# ------------------------------------------------------------------- cap 1
T("Harga tabung melon", "tidak ada harga nasional",
  "Berapa kamu bayar terakhir kali beli tabung gas tiga kilogram? Simpan "
  "angka itu, karena sebentar lagi kita bandingkan.",
  cap="Tidak ada harga nasional")
I("Yang banyak orang kira", "harganya sama di mana-mana",
  "Banyak orang mengira harga tabung melon itu satu angka yang sama di "
  "seluruh Indonesia. Bukan begitu.")
I("Yang sebenarnya", "ditetapkan per daerah",
  "Harga eceran tertinggi, atau HET, ditetapkan lewat peraturan gubernur atau "
  "peraturan bupati di daerah masing-masing.")
I("Artinya", "daerahmu punya angkanya sendiri",
  "Artinya daerahmu punya angka sendiri, dan angka itu resmi, tertulis, dan "
  "bisa kamu cari.")
I("Contoh nyata", "dua daerah, dua angka",
  "Contohnya, di DKI Jakarta HET di tingkat pangkalan ditetapkan enam belas "
  "ribu rupiah. Di Jawa Tengah dan Jawa Timur angkanya delapan belas ribu.")
I("Dan angkanya bisa berubah", "kalau peraturannya diubah",
  "Angka itu juga bisa berubah, karena peraturan daerah bisa direvisi. Jadi "
  "yang berlaku hari ini adalah yang tertulis pada peraturan paling baru.")
I("Jadi pertanyaannya", "bukan mahal atau murah",
  "Jadi pertanyaan yang benar bukan mahal atau murah. Pertanyaannya adalah: "
  "berapa HET di tempat kamu tinggal.")

# ------------------------------------------------------------------- cap 2
T("Cara mencarinya", "tiga tempat",
  "Sekarang cara menemukan angka daerahmu, dan ada tiga tempat.",
  cap="Cara mencari HET daerahmu")
I("Pertama", "papan harga di pangkalan",
  "Yang paling cepat: pangkalan resmi wajib memasang papan harga. Angka di "
  "papan itu adalah HET yang berlaku di sana.")
I("Kedua", "situs pemerintah daerah",
  "Kedua, cari di situs pemerintah provinsi atau kabupaten. Peraturan yang "
  "menetapkan HET diumumkan di sana, lengkap dengan nomornya.")
I("Ketiga", "dinas terkait",
  "Ketiga, dinas perindustrian dan perdagangan daerah biasanya menerbitkan "
  "pengumuman setiap kali angkanya berubah.")
I("Yang kamu cari", "satu angka dan satu nomor",
  "Yang kamu cari cuma dua hal: berapa rupiah, dan nomor peraturan yang "
  "menetapkannya. Nomor itu yang membedakan informasi dari kabar burung.")
I("Kenapa nomornya penting", "biar bisa dicek orang lain",
  "Nomor peraturan penting karena dengan nomor itu siapa pun bisa memeriksa "
  "sendiri. Tanpa nomor, angka cuma cerita.")
I("Catat di tempat yang tetap", "supaya tidak lupa",
  "Catat di catatan ponsel. Angka ini jarang berubah, jadi sekali dicatat, "
  "berlaku lama.")

# ------------------------------------------------------------------- cap 3
T("Hitung selisihnya", "satu pengurangan",
  "Sekarang bagian yang jadi uang, dan cuma satu pengurangan.",
  cap="Hitung selisihmu sendiri")
I("Langkah satu", "harga yang kamu bayar",
  "Ambil angka yang tadi kamu simpan: berapa kamu benar-benar bayar per "
  "tabung.")
I("Langkah dua", "kurangi HET daerahmu",
  "Kurangi dengan HET daerahmu. Hasilnya adalah selisih per tabung, dan "
  "itulah yang kamu bayar di atas harga resmi.")
I("Langkah tiga", "kalikan pemakaian sebulan",
  "Kalikan selisih itu dengan jumlah tabung yang kamu habiskan sebulan.")
I("Contoh angkanya", "tujuh ribu per tabung",
  "Misalnya HET di daerahmu delapan belas ribu dan kamu bayar dua puluh lima "
  "ribu. Selisihnya tujuh ribu rupiah per tabung.")
I("Kalau tiga tabung sebulan", "dua puluh satu ribu",
  "Kalau sebulan habis tiga tabung, itu dua puluh satu ribu rupiah per bulan.")
B("Setahun", ["Sebulan", "Setahun"], [8, 100],
  "Setahun angkanya jadi dua ratus lima puluh dua ribu rupiah. Untuk satu "
  "barang yang harganya sudah ditetapkan pemerintah.")
I("Itu seluruh metodenya", "sisanya penjelasan",
  "Itu seluruh metodenya. Sisa video ini menjelaskan kenapa selisihnya ada, "
  "dan apa yang bisa kamu lakukan soal itu.")

# ============ ate aqui, ~200 segundos. O que segue aprofunda. ===============

# ------------------------------------------------------------------- cap 4
T("Kenapa ada selisih", "rantainya",
  "Kenapa selisih itu muncul sama sekali? Karena rantai penyalurannya "
  "berlapis.",
  cap="Kenapa selisihnya muncul")
I("Pangkalan", "titik resmi terakhir",
  "Pangkalan adalah titik resmi terakhir dalam rantai. HET yang ditetapkan "
  "peraturan daerah berlaku di titik itu.")
I("Pengecer", "di luar rantai resmi",
  "Warung atau pengecer yang membeli dari pangkalan lalu menjual lagi berada "
  "di luar titik itu, dan menambahkan marginnya sendiri.")
I("Karena itu", "harga naik menjauh dari pangkalan",
  "Karena itu harga cenderung naik semakin jauh kamu membeli dari pangkalan. "
  "Bukan karena ada yang salah, tapi karena ada lapisan tambahan.")
I("Yang bisa kamu pilih", "beli langsung di pangkalan",
  "Yang ada di tangan kamu adalah memilih membeli langsung di pangkalan, "
  "kalau jaraknya masuk akal.")
I("Bukan berarti pengecer salah", "mereka juga punya biaya",
  "Ini bukan berarti pengecer berbuat salah. Mereka menanggung ongkos angkut "
  "dan waktu, dan bagi banyak orang kedekatan itu memang ada nilainya.")
I("Hitung ongkosnya juga", "jujur soal jarak",
  "Dan hitung juga ongkos perjalanannya. Kalau selisihnya tujuh ribu tapi "
  "ongkos bolak-balik sepuluh ribu, pangkalan bukan pilihan yang lebih murah.")

# ------------------------------------------------------------------- cap 5
T("Siapa yang berhak", "empat kelompok",
  "Sekarang bagian yang sering disalahpahami: siapa sebenarnya yang berhak "
  "atas tabung bersubsidi ini.",
  cap="Siapa yang berhak memakainya")
L("Kelompok sasaran", ["Rumah tangga, untuk memasak",
                       "Usaha mikro, untuk memasak",
                       "Nelayan sasaran",
                       "Petani sasaran"],
  "Sasarannya empat kelompok: rumah tangga untuk memasak, usaha mikro untuk "
  "memasak, nelayan sasaran, dan petani sasaran.")
I("Dasarnya", "dua peraturan presiden",
  "Dasarnya adalah dua peraturan presiden. Yang pertama bernomor seratus "
  "empat, dari tahun dua ribu tujuh. Yang kedua bernomor tiga puluh delapan, "
  "dari tahun dua ribu sembilan belas.")
I("Perhatikan katanya", "untuk memasak",
  "Perhatikan dua kata yang berulang di sana: untuk memasak. Itu batas yang "
  "membedakan pemakaian yang disasar dari yang tidak.")
I("Kalau kamu punya warung", "kamu termasuk",
  "Kalau kamu punya warung kecil dan memasak untuk dijual, kamu masuk "
  "kategori usaha mikro. Itu bukan penyalahgunaan.")
I("Kalau kamu ragu", "tanya di pangkalan",
  "Kalau kamu ragu masuk kelompok yang mana, itu pertanyaan satu kalimat di "
  "pangkalan resmi. Mereka yang mendata.")
I("Yang membedakan", "bukan besar kecilnya dapur",
  "Yang membedakan bukan besar kecil dapurnya, melainkan kelompok yang "
  "disebut peraturan itu.")

# ------------------------------------------------------------------- cap 6
T("Kenapa harus daftar", "sejak awal 2024",
  "Dan ini yang mengubah cara membeli, banyak orang belum tahu detailnya.",
  cap="Kenapa harus mendaftar")
I("Aturannya", "hanya pengguna terdata",
  "Sejak satu Januari dua ribu dua puluh empat, pembelian tabung tiga "
  "kilogram hanya bisa dilakukan oleh pengguna yang sudah terdata.")
I("Cara mendaftar", "KTP dan KK",
  "Cara mendaftarnya sederhana: tunjukkan KTP dan kartu keluarga di penyalur "
  "atau pangkalan resmi. Tidak ada biaya.")
I("Untuk usaha mikro", "ada satu tambahan",
  "Untuk pengguna usaha mikro ada satu syarat tambahan, yaitu foto diri di "
  "tempat usaha.")
I("Cek statusmu", "cukup bawa KTP",
  "Kalau kamu tidak yakin sudah terdata atau belum, cukup bawa KTP ke "
  "pangkalan resmi dan minta dicek.")
I("Batas per transaksi", "satu KTP satu tabung",
  "Ada juga batas pembelian: satu tabung per transaksi, dengan prinsip satu "
  "KTP satu tabung.")
I("Kalau tabungmu habis malam hari", "pangkalan bisa tutup",
  "Satu hal praktis: pangkalan punya jam buka. Kalau gasmu sering habis malam "
  "hari, punya tabung cadangan lebih murah daripada membeli darurat di luar.")
I("Tujuannya", "subsidi tepat sasaran",
  "Tujuan aturan ini adalah memastikan subsidinya sampai ke kelompok yang "
  "memang disasar, bukan menyulitkan pembeli.")

# ------------------------------------------------------------------- cap 7
T("Dari mana angkanya", "dua sumber resmi",
  "Dari mana semua ini, karena itu pertanyaan yang pantas ditanyakan setiap "
  "kali.",
  cap="Dari mana angkanya")
I("Sumber pertama", "Kementerian ESDM",
  "Aturan pendaftaran, syarat KTP dan kartu keluarga, kelompok sasaran, dan "
  "batas satu tabung per transaksi berasal dari Kementerian Energi dan Sumber "
  "Daya Mineral melalui Direktorat Jenderal Migas.")
I("Sumber kedua", "peraturan daerah",
  "Angka HET berasal dari peraturan daerah masing-masing, yang diumumkan di "
  "situs hukum provinsi dan kabupaten.")
I("Kenapa dua sumber", "dua hal yang berbeda",
  "Dua sumber karena dua hal yang berbeda: siapa boleh membeli diatur pusat, "
  "berapa harganya diatur daerah. Mencampur keduanya bikin salah.")
I("Cara mengeceknya sendiri", "dua kata kunci",
  "Kamu bisa memeriksanya tanpa perantara. Cari pendaftaran pengguna LPG tiga "
  "kilogram di situs Kementerian ESDM, dan HET LPG di situs pemerintah "
  "daerahmu.")
I("Yang tidak saya pakai", "kabar dari grup",
  "Saya tidak memakai kabar dari grup pesan atau portal berita tanpa nomor "
  "peraturan. Angka tanpa dasar resmi tidak masuk video ini.")

# ------------------------------------------------------------------- cap 8
T("Minggu ini", "tiga hal",
  "Tiga hal yang bisa kamu lakukan minggu ini, semuanya gratis.",
  cap="Yang kamu lakukan minggu ini")
I("Pertama", "cari HET daerahmu",
  "Cari HET di daerahmu, lewat papan harga pangkalan atau situs pemerintah "
  "daerah, dan catat nomor peraturannya.")
I("Kedua", "hitung selisihmu",
  "Hitung selisih antara yang kamu bayar dan angka itu, lalu kalikan dengan "
  "pemakaian sebulan.")
L("Ketiga", ["HET di daerah saya",
             "Harga yang saya bayar",
             "Selisih saya setahun"],
  "Dan tulis tiga baris: HET di daerah saya, harga yang saya bayar, dan "
  "selisih saya setahun.")
I("Baris ketiga", "yang bikin bergerak",
  "Baris ketiga yang bikin orang bergerak, karena selisih per tabung terasa "
  "kecil dan selisih setahun tidak.")
I("Kalau kamu belum terdata", "itu satu kunjungan",
  "Dan kalau ternyata kamu belum terdata, itu satu kali ke pangkalan dengan "
  "KTP dan kartu keluarga.")
I("Ringkasnya", "cari, kurangi, kalikan",
  "Ringkasnya: cari HET daerahmu, kurangi dari yang kamu bayar, kalikan "
  "dengan pemakaian bulanan.")
C("Resep Naik Level", "hitung punyamu",
  "Lakukan satu hal hari ini: cari HET daerahmu dan tulis selisihmu setahun. "
  "Di sini kita ambil satu angka dari dapurmu dan mengubahnya jadi hitungan "
  "yang kamu kerjakan sendiri. Kalau itu yang kamu cari, berlangganan.")


# -------------------------------------------------------------------- short
#
# ENTREGA A SUBTRACAO INTEIRA, na segunda pessoa. E o numero de partida e o
# unico que este publico tem sem procurar: o que ele PAGOU. Aprendizado 487.
SHORT = [
    {"layout": "titulo", "kicker": "Tabung melon", "sub": "tidak ada harga nasional",
     "nar": "Berapa kamu bayar tabung gas tiga kilogram terakhir kali? Tidak "
            "ada harga nasional untuk itu.", "sem_cap": True},
    {"layout": "item", "kicker": "HET per daerah", "preco": "Pergub atau Perbup",
     "nar": "Harga eceran tertinggi ditetapkan per daerah, lewat peraturan "
            "gubernur.", "sem_cap": True},
    {"layout": "item", "kicker": "Kurangi", "preco": "yang kamu bayar",
     "nar": "Kurangi HET daerahmu dari yang kamu bayar. Itu selisihmu per "
            "tabung.", "sem_cap": True},
    {"layout": "item", "kicker": "Kalikan sebulan", "preco": "lalu kali dua belas",
     "nar": "Selisih tujuh ribu dengan tiga tabung sebulan jadi dua ratus lima "
            "puluh dua ribu setahun.", "sem_cap": True},
    {"layout": "cta", "kicker": "Resep Naik Level", "sub": "tulis selisihmu",
     "nar": "Cari HET daerahmu dan tulis selisihmu setahun.", "sem_cap": True},
]

COPY = """# LPG 3 kg: tidak ada harga nasional, dan cara menghitung selisihmu

## TITULO
LPG 3 Kg: Tidak Ada Harga Nasional — Cara Cari HET Daerahmu dan Hitung Selisihmu

## DESCRICAO
Berapa kamu bayar terakhir kali beli tabung gas tiga kilogram? Simpan angka itu. Banyak orang mengira harga tabung melon adalah satu angka yang sama di seluruh Indonesia — bukan begitu. Harga eceran tertinggi (HET) ditetapkan lewat peraturan gubernur atau peraturan bupati di daerah masing-masing, jadi daerahmu punya angkanya sendiri, resmi dan tertulis. Video ini menunjukkan cara menemukan angka itu dan mengubahnya jadi satu pengurangan yang bisa kamu kerjakan hari ini.

HET DITETAPKAN PER DAERAH (sumber: peraturan daerah, diumumkan di situs hukum provinsi dan kabupaten)

Contoh nyata dari dua daerah yang berbeda: di DKI Jakarta HET di tingkat pangkalan ditetapkan Rp16.000. Di Jawa Tengah ditetapkan Rp18.000 melalui keputusan gubernur, dan Jawa Timur juga menerapkan Rp18.000. Angka-angka ini adalah contoh daerah tertentu, bukan harga nasional — daerahmu punya peraturannya sendiri.

CARA MENCARI HET DAERAHMU (tiga tempat)

1) Papan harga di pangkalan resmi — pangkalan wajib memasangnya. 2) Situs pemerintah provinsi atau kabupaten, tempat peraturan yang menetapkan HET diumumkan lengkap dengan nomornya. 3) Dinas perindustrian dan perdagangan daerah, yang menerbitkan pengumuman setiap kali angkanya berubah. Yang kamu cari cuma dua hal: berapa rupiah, dan nomor peraturannya.

HITUNG SELISIHMU (satu pengurangan)

Harga yang kamu bayar − HET daerahmu = selisih per tabung. Kalikan dengan jumlah tabung sebulan, lalu kalikan dua belas. Contoh: HET Rp18.000 dan kamu bayar Rp25.000 berarti selisih Rp7.000 per tabung; dengan tiga tabung sebulan itu Rp21.000 per bulan dan Rp252.000 setahun. (Angka Rp25.000 adalah contoh — yang jadi patokan adalah harga yang KAMU bayar.)

KENAPA SELISIHNYA MUNCUL: pangkalan adalah titik resmi terakhir dalam rantai penyaluran, dan HET berlaku di titik itu. Warung atau pengecer yang membeli dari pangkalan lalu menjual lagi berada di luar titik itu dan menambahkan marginnya sendiri. Kalau jaraknya masuk akal, membeli langsung di pangkalan menghilangkan lapisan itu — tapi hitung juga ongkos perjalanannya, karena selisih Rp7.000 tidak menutup ongkos bolak-balik Rp10.000.

SIAPA YANG BERHAK (sumber: Kementerian ESDM / Ditjen Migas)

Sasaran pengguna LPG tabung 3 kg adalah rumah tangga untuk memasak, usaha mikro untuk memasak, nelayan sasaran, dan petani sasaran, sesuai Peraturan Presiden Nomor 104 Tahun 2007 dan Peraturan Presiden Nomor 38 Tahun 2019.

WAJIB TERDATA SEJAK 1 JANUARI 2024: pembelian tabung 3 kg hanya dapat dilakukan oleh pengguna yang sudah terdata. Mendaftarnya cukup menunjukkan KTP dan Kartu Keluarga di penyalur atau pangkalan resmi, tanpa biaya; pengguna usaha mikro perlu tambahan foto diri di tempat usaha. Kalau tidak yakin sudah terdata, bawa KTP ke pangkalan resmi dan minta dicek. Pembelian dibatasi satu tabung per transaksi, dengan prinsip satu KTP satu tabung.

Video ini tidak menyebut HET daerah lain di luar yang dikutip, tidak menuduh pedagang mana pun, dan tidak menjanjikan bahwa stok pangkalan selalu tersedia.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Cari HET di daerahmu, kurangi dari harga yang kamu bayar, lalu tulis satu angka di komentar: selisihmu setahun. Tidak perlu sebut nama warung atau daerahnya kalau tidak mau — cukup angkanya. Saya penasaran berapa banyak yang selisih setahunnya lebih besar dari harga satu tabung penuh.

## HASHTAGS
#LPG3Kg #HargaGas #ResepNaikLevel

## TAGS
lpg 3 kg, tabung melon, het lpg, harga gas melon, pangkalan lpg, subsidi lpg, ktp lpg, daftar lpg 3 kg, usaha mikro, perpres 104 2007, ditjen migas, harga eceran tertinggi, hemat dapur, biaya dapur, ekonomi rumah tangga

## CONFIGURACOES DO STUDIO
- Idioma: Indonesio (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Os numeros vem de DUAS fontes institucionais que tratam de coisas DIFERENTES e por isso nao se sobrepoem. (1) KEMENTERIAN ESDM / DITJEN MIGAS (esdm.go.id e migas.esdm.go.id), com corroboracao do Setkab: desde 1 de janeiro de 2024 a compra do tubo de 3 kg so pode ser feita por usuario ja cadastrado; o cadastro e feito apresentando KTP e Kartu Keluarga no penyalur ou pangkalan oficial, sem custo, com foto no local de trabalho exigida a mais para usuario de usaha mikro; os grupos com direito sao rumah tangga para cozinhar, usaha mikro para cozinhar, nelayan sasaran e petani sasaran, conforme a Perpres 104/2007 e a Perpres 38/2019; e a compra e limitada a um tubo por transacao, no principio "satu KTP satu tabung". (2) PERATURAN DAERAH, publicadas nos sites de JDIH e dos governos provinciais e municipais: o HET NAO e nacional — ele e fixado por Peraturan Gubernur ou Peraturan Bupati e DIFERE por regiao. Os exemplos citados sao DKI Jakarta com Rp 16.000 no nivel do pangkalan, Jawa Tengah com Rp 18.000 por decisao do governador, e Jawa Timur tambem com Rp 18.000. O VIDEO NAO AFIRMA UM PRECO NACIONAL, porque nao existe: ele ensina a achar o proprio e diz em voz alta que os valores citados sao de regioes especificas. NA CONTA DO EXEMPLO, o unico numero que vem de fonte e o HET; os Rp 25.000 pagos sao hipotese explicitamente marcada como tal, porque o valor que vale e o que o proprio espectador pagou. NAO foi usada nenhuma mensagem de grupo nem portal sem numero de norma.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/resep-naik-level-007.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-007",
    "idioma": "id",
    "voz": "id-ID-GadisNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#1F2430", "c1": "#C2410C", "c2": "#0E7490",
               "bg": "#FAF5EF"},
    "thumb": {"l1": "HET beda", "l2": "tiap daerah"},
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
    grava(SPEC, "fabrica/specs/resep-naik-level-007.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
