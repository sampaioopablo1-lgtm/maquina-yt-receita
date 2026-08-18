#!/usr/bin/env python3
"""Monta a spec resep-naik-level-004.

PAUTA, medida em 18/08/2026 e gravada em pautas_banco (canal com 61 linhas,
nicho_mediana_vd=278,9). Tres buscas novas (harga beras, menu hemat, 50 ribu
sehari) somaram 7 pares ineditos. O que a medicao de hoje mostra:

    formato                              exemplo vivo                      v/d
    orcamento fixo x periodo             "SULAP 100 RIBU! Dapur Aman
                                          Seminggu" (4 dias no ar)       691,5
    orcamento fixo x periodo             "Uang 50 Ribu Untuk 3 Hari"     278,9
    drama de IA sobre comida             (outlier de outro formato)       alto

O formato que performa no nicho e ORCAMENTO CONCRETO x PERIODO no titulo. O
outlier de drama nao e o nosso formato e fica de fora de proposito.

EIXO NAO USADO: todos esses videos funcionam por vibe — mostram o carrinho, a
panela e o total, e NENHUM faz a conta que decide se aquele total serve para a
casa de quem assiste. E exatamente por isso o espectador falha ao reproduzir:
o video calcula para duas bocas com rack cheio e preco do mercado do criador.
A casa do -004 e essa conta: os tres numeros que o video nao filma (bocas,
estoque inicial, preco da regiao), a divisao anggaran/orang/hari e a folha de
seis linhas que transforma qualquer menu viral em decisao propria.

NUMEROS: nenhum preco absoluto de alimento e afirmado. Os unicos fatos datados
sao os JA VERIFICADOS na -003 (beras +Rp500 a 1.500/kg em duas semanas de
agosto/2026; painel diario da Badan Pangan) — continuidade proposital com o
video anterior do canal. As divisoes (seratus ribu / tujuh hari / empat belas
ribu) sao ilustracoes aritmeticas, declaradas como tal na nota de fontes.

SIMILARIDADE vs os tres pacotes anteriores do MESMO canal:
  -001 "5 Makan Malam Enak di Bawah Rp10.000 per Porsi"   -> lista com preco
  -002 "Belanja Mingguan Rp100.000: Daftar Persis 7 Hari" -> haul com lista
  -003 "5 Strategi Ibu Mengatur Uang..."                  -> painel + 3 colunas
Este NAO da lista, NAO da cardapio e NAO repete o sistema de colunas: e a
matematica de ADAPTAR menu alheio. O painel aparece uma vez (linha 4 da
folha), como fonte — continuidade, nao repeticao.

DIMENSIONAMENTO pelo agregado de producao (fabrica/ensaio.py, n=86):
id-ID-GadisNeural = 14,55 chars/s + 1,276 s/frase — a voz mais lenta do
portfolio. ~7.800 chars em ~75 cenas fecham ~12,9 min; o teto de 15 min fica
com folga de mais de 2 min contra o erro de calibracao ja visto nesta voz.
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


# ---------------------------------------------------------------- cap 1
T("Kamu pernah lihat", "video seratus ribu",
  "Satu video muncul di berandamu. Uang seratus ribu, katanya, cukup untuk "
  "makan seminggu.",
  cap="Video seratus ribu itu")
I("Videonya meyakinkan", "masakannya jadi",
  "Videonya tidak bohong. Masakannya benar-benar jadi, dan totalnya "
  "benar-benar seratus ribu.")
I("Lalu kamu coba", "di dapurmu sendiri",
  "Lalu kamu mencobanya di dapurmu sendiri. Menu yang sama, urutan yang sama.")
I("Hasilnya", "habis di hari Rabu",
  "Hasilnya berbeda. Uangnya habis di hari Rabu, dan sisa minggunya berjalan "
  "dengan rasa bersalah.")
I("Kesimpulan yang biasa", "aku yang gagal",
  "Kesimpulan yang biasa muncul: pasti aku yang gagal. Pasti tanganku yang "
  "boros.")
I("Kesimpulan yang benar", "hitungannya beda",
  "Kesimpulan yang benar lebih sederhana. Hitungan di video itu bukan "
  "hitungan rumahmu.")
I("Bukan salah videonya", "angkanya tidak lengkap",
  "Ini bukan soal videonya jujur atau tidak. Angkanya saja yang tidak lengkap "
  "untuk dapur orang lain.")
L("Yang kita bedah", ["Angka tersembunyi", "Matematika protein",
                      "Lembar enam baris", "Menyesuaikan menu",
                      "Kesalahan mahal"],
  "Lima bagian. Angka yang tidak disebut video. Matematika protein. Lembar "
  "enam baris. Cara menyesuaikan menu orang lain. Dan kesalahan yang mahal.")
I("Satu hal dulu", "bukan makan lebih sedikit",
  "Satu hal perlu jelas dari awal. Ini bukan tentang makan lebih sedikit, "
  "tapi tentang menghitung sebelum meniru.")
T("Jadi", "angka apa yang hilang?",
  "Kalau videonya jujur tapi hasilmu beda, pertanyaannya tinggal satu. Angka "
  "apa yang tidak ikut difilmkan?")

# ---------------------------------------------------------------- cap 2
T("Angka pertama", "jumlah orang",
  "Angka pertama yang jarang disebut: menu itu dihitung untuk berapa orang.",
  cap="Angka yang tidak ikut difilmkan")
I("Porsi video", "sering dua orang",
  "Banyak menu hemat dihitung untuk dua porsi. Rumahmu mungkin berisi lima.")
I("Efeknya", "bukan tambah sedikit",
  "Efeknya bukan menambah sedikit. Setiap lauk dan setiap bumbu ikut "
  "dikalikan jumlah kepala.")
I("Angka kedua", "isi rak sebelum mulai",
  "Angka kedua adalah isi dapur sebelum menu dimulai. Dapur di video sudah "
  "punya minyak, bumbu, dan beras.")
I("Yang difilmkan", "hanya belanja tambahan",
  "Yang masuk kamera hanya belanja tambahannya. Rak yang sudah penuh tidak "
  "pernah dihitung sebagai biaya.")
I("Kalau rakmu kosong", "minggu pertama pasti kalah",
  "Kalau rakmu kosong, minggu pertamamu pasti lebih mahal dari video mana "
  "pun. Itu bukan kegagalan.")
I("Angka ketiga", "harga daerahmu",
  "Angka ketiga adalah harga di daerahmu. Harga beras berbeda antar daerah "
  "dan antar kualitas.")
I("Buktinya masih hangat", "naik dalam dua minggu",
  "Buktinya masih hangat. Pertengahan Agustus, harga beras di banyak daerah "
  "naik hanya dalam dua minggu.")
I("Berapa naiknya", "sampai seribu lima ratus",
  "Kenaikannya antara lima ratus dan seribu lima ratus rupiah per kilogram, "
  "tergantung daerah dan kualitas.")
I("Artinya", "total video cepat basi",
  "Artinya total belanja di video punya tanggal kedaluwarsa. Angka yang "
  "difilmkan bulan lalu bukan angka bulan ini.")
T("Tiga angka itu", "milik rumahmu",
  "Jumlah orang, isi rak, harga daerah. Tiga-tiganya milik rumahmu. Lalu "
  "dari mana mulai menghitung?")

# ---------------------------------------------------------------- cap 3
T("Satu pembagian", "yang mengubah semuanya",
  "Semua dimulai dari satu pembagian. Anggaran seminggu, dibagi jumlah "
  "orang, dibagi jumlah hari.",
  cap="Matematika protein")
I("Contohnya", "empat belas ribu sehari",
  "Seratus ribu dibagi tujuh hari itu sekitar empat belas ribu sehari. Dan "
  "itu untuk seisi rumah, bukan per orang.")
I("Per orang", "baru terasa jujur",
  "Untuk empat orang, jatahnya sekitar tiga ribu lima ratus per orang per "
  "hari. Angka itu yang jujur.")
I("Angka itu kecil", "dan justru itu gunanya",
  "Angka itu terasa kecil, dan justru itu gunanya. Ia langsung memberitahu "
  "kelas menu mana yang masuk akal untukmu.")
I("Di mana uang habis", "di lauk",
  "Di dapur, uang tidak habis di nasi. Uang habis di lauk, karena protein "
  "adalah baris termahal.")
I("Karbohidrat", "murah dan stabil",
  "Nasi dan karbohidrat lain relatif murah per porsi. Bukan di situ "
  "pertarungannya.")
I("Protein", "penentu anggaran",
  "Protein yang menentukan. Telur, tempe, dan tahu ada di satu kelas harga. "
  "Ayam dan daging di kelas yang lain.")
I("Rahasia menu viral", "kelas proteinnya",
  "Menu seratus ribu bisa jadi karena proteinnya dipilih dari kelas yang "
  "murah. Bagian itu layak ditiru.")
I("Yang tidak bisa ditiru", "jumlahnya",
  "Yang tidak bisa ditiru mentah-mentah adalah jumlahnya, karena jumlah "
  "mengikuti isi rumahmu.")
I("Cara membandingkan", "harga per porsi",
  "Bandingkan protein dengan harga per porsi, bukan harga per bungkus. "
  "Bungkus besar yang tidak habis bukan penghematan.")
T("Hitungannya ada", "tinggal ditulis",
  "Pembagiannya sudah kamu punya. Sekarang kita taruh di selembar kertas, "
  "supaya tidak tinggal di kepala.")

# ---------------------------------------------------------------- cap 4
T("Lembar enam baris", "sekali seminggu",
  "Sistemnya muat di selembar kertas. Enam baris, diisi sekali seminggu, "
  "sebelum belanja.",
  cap="Lembar enam baris")
I("Baris pertama", "jumlah orang",
  "Baris pertama: jumlah orang yang makan dari dapurmu minggu ini. Termasuk "
  "yang cuma makan malam.")
I("Baris kedua", "anggaran minggu ini",
  "Baris kedua: anggaran minggu ini. Angka yang sungguh ada di dompet, bukan "
  "angka yang kamu harapkan.")
I("Baris ketiga", "hasil pembagian",
  "Baris ketiga: anggaran dibagi orang, dibagi hari. Satu-satunya "
  "perhitungan di lembar ini.")
I("Baris keempat", "harga beras daerahmu",
  "Baris keempat: harga beras di daerahmu minggu ini. Ambil dari panel harga "
  "resmi Badan Pangan, bukan dari ingatan.")
I("Kenapa beras duluan", "jangkar belanja",
  "Beras ditulis duluan karena ia jangkar belanja. Kalau jangkarnya naik, "
  "semua baris di bawahnya ikut menyesuaikan.")
I("Baris kelima", "jatah protein",
  "Baris kelima: jatah protein per hari, dipilih dari kelas harga yang masuk "
  "di baris ketiga.")
I("Baris keenam", "sisa untuk sayur dan bumbu",
  "Baris keenam: sisanya, untuk sayur dan bumbu. Sisa itu ditulis, bukan "
  "dikira-kira.")
B("Bentuk belanjamu", ["Beras", "Protein", "Sayur", "Bumbu"],
  [90, 100, 50, 25],
  "Kalau enam baris itu diisi jujur, bentuk belanjamu kelihatan. Protein dan "
  "beras hampir selalu jadi batang tertinggi.")
I("Lima menit", "sebelum ke pasar",
  "Mengisinya butuh sekitar lima menit, sekali seminggu. Lebih cepat "
  "daripada memilih video menu berikutnya.")
I("Fungsi lembarnya", "penyaring video",
  "Lembar itu juga penyaring. Setiap menu viral yang lewat tinggal diuji: "
  "cocok dengan baris ketigamu atau tidak.")
T("Kalau cocok", "bagaimana menirunya?",
  "Dan kalau menunya lolos saringan, cara menirunya pun ada aturannya:")

# ---------------------------------------------------------------- cap 5
T("Aturan pertama", "skalakan porsinya",
  "Aturan pertama: skalakan porsinya. Menu untuk dua orang dikalikan dulu ke "
  "jumlah rumahmu, baru dihitung ulang totalnya.",
  cap="Menyesuaikan menu orang lain")
I("Jangan kaget", "totalnya berubah",
  "Setelah dikalikan, totalnya hampir pasti melewati angka di judul video. "
  "Itu bukan menu yang bohong. Itu perkalian.")
I("Aturan kedua", "tukar protein sekelas",
  "Aturan kedua: protein boleh ditukar selama kelas harganya sama. Tempe dan "
  "telur saling menggantikan dengan mulus.")
I("Yang sering salah", "naik kelas diam-diam",
  "Yang sering terjadi: mengganti tempe dengan ayam karena bosan, lalu heran "
  "anggarannya jebol. Itu naik kelas, bukan menukar.")
I("Aturan ketiga", "tiru strukturnya",
  "Aturan ketiga: yang paling berharga dari menu viral bukan resepnya, tapi "
  "strukturnya.")
I("Struktur itu apa", "masak sekali, makan dua kali",
  "Misalnya masak sekali untuk dua waktu makan, atau bumbu dasar yang sama "
  "untuk beberapa masakan. Struktur bebas dibawa pulang.")
I("Aturan keempat", "harga dari daerahmu",
  "Aturan keempat: harga selalu diambil dari daerahmu, bukan dari keterangan "
  "video. Panel resmi lebih dekat ke lapakmu daripada kolom komentar.")
I("Ukuran keberhasilan", "baris ketigamu",
  "Ukuran keberhasilanmu bukan total di video. Ukurannya apakah belanjamu "
  "masuk di baris ketiga lembarmu sendiri.")
I("Kalau tidak masuk", "geser satu hal saja",
  "Kalau tidak masuk, jangan buang menunya. Geser satu hal saja: kelas "
  "protein, atau jumlah masakan berbumbu.")
I("Menu yang sama", "dua rumah, dua angka",
  "Menu yang sama akan menghasilkan angka berbeda di dua rumah. Dan "
  "dua-duanya bisa benar.")
T("Sampai sini aman", "kecuali empat jebakan",
  "Sampai di sini sistemnya jalan. Yang bisa merusaknya tinggal empat "
  "kebiasaan, dan semuanya terasa masuk akal:")

# ---------------------------------------------------------------- cap 6
T("Kesalahan pertama", "meniru mentah-mentah",
  "Kesalahan pertama: meniru menu mentah-mentah, porsi dan totalnya "
  "sekaligus. Itu memindahkan dapur orang lain ke rumahmu.",
  cap="Empat kesalahan yang mahal")
I("Kesalahan kedua", "lupa isi rak",
  "Kesalahan kedua: membandingkan minggu pertamamu dengan video. Dapur video "
  "mulai dari rak penuh, dapurmu mungkin tidak.")
I("Perbaikannya", "nilai di minggu ketiga",
  "Perbaikannya sederhana: nilai sistem ini di minggu ketiga, bukan minggu "
  "pertama. Rak butuh waktu untuk terisi.")
I("Kesalahan ketiga", "menghitung per masakan",
  "Kesalahan ketiga: menghitung per masakan, bukan per minggu. Masakan murah "
  "yang bahannya cuma dipakai sekali itu mahal.")
I("Ukur yang adil", "sisa bahan ikut dihitung",
  "Bahan yang bersisa dan terpakai lagi menurunkan biaya masakan berikutnya. "
  "Hitungannya baru adil kalau seminggu penuh.")
I("Kesalahan keempat", "mengejar angka judul",
  "Kesalahan keempat: mengejar angka di judul video. Angka judul dibuat "
  "untuk diklik, bukan untuk dapurmu.")
I("Empat-empatnya", "akar yang sama",
  "Empat-empatnya berakar sama: memakai angka orang lain untuk keputusan "
  "rumah sendiri.")
I("Penangkalnya", "satu kalimat",
  "Penangkalnya satu kalimat. Angka yang boleh masuk lembarmu hanyalah angka "
  "yang datang dari rumahmu atau dari panel resmi.")
I("Sisanya", "inspirasi, bukan patokan",
  "Video menu tetap berguna sebagai ide masakan dan struktur. Ia berhenti "
  "berguna saat dijadikan patokan angka.")
T("Terakhir", "supaya tidak mati minggu depan",
  "Tinggal menjaga supaya lembar ini bertahan lebih dari seminggu.")

# ---------------------------------------------------------------- cap 7
T("Umurnya seminggu", "dan memang begitu",
  "Lembar ini umurnya memang seminggu. Minggu baru, lembar baru. Yang lama "
  "jangan dibuang.",
  cap="Supaya bertahan")
I("Kenapa disimpan", "polamu kelihatan",
  "Setelah beberapa lembar terkumpul, pola rumahmu kelihatan. Baris mana "
  "yang selalu jebol, minggu mana yang selalu berat.")
I("Ritualnya", "hari yang sama",
  "Isi lembarnya di hari yang sama tiap minggu, sebelum belanja besar. Hari "
  "yang berpindah-pindah membunuh kebiasaan.")
I("Pemegangnya", "satu orang",
  "Satu orang yang memegang lembarnya. Catatan milik semua orang berakhir "
  "jadi milik tidak seorang pun.")
I("Yang dilarang", "menyalahkan lewat lembar",
  "Dan jangan pakai lembar itu untuk menyalahkan siapa pun di rumah. Lembar "
  "yang menakutkan berhenti diisi dengan jujur.")
L("Ringkasnya", ["Bagi dulu anggaranmu", "Enam baris", "Protein sekelas",
                 "Harga daerahmu", "Nilai per minggu"],
  "Ringkasnya begini. Bagi anggaranmu per orang per hari. Isi enam baris. "
  "Tukar protein hanya sekelas. Pakai harga daerahmu. Dan nilai per minggu, "
  "bukan per masakan.")
I("Kalau cuma satu hal", "lakukan pembagiannya",
  "Kalau kamu cuma sempat satu hal setelah video ini, lakukan pembagiannya. "
  "Anggaran, dibagi orang, dibagi hari.")
I("Waktunya", "lebih cepat dari satu video",
  "Itu lebih cepat daripada menonton satu video menu lagi. Dan angkanya akan "
  "mengubah cara kamu menonton semuanya.")
C("Resep Naik Level", "uang dapur, bukan resep",
  "Kalau pembagianmu sudah ketemu, tulis angkanya di komentar. Jatah per "
  "orang per hari di rumahmu, dan untuk berapa orang.")
C("Resep Naik Level", "uang dapur, bukan resep",
  "Aku sedang mengumpulkan angka itu dari banyak rumah. Kalau ada pos dapur "
  "lain yang mau dibedah, sebutkan. Yang paling diminta dibuat lebih dulu.")

SHORT = [
    {"layout": "titulo", "kicker": "Menu seratus ribu gagal",
     "sub": "bukan salahmu",
     "nar": "Menu seratus ribu seminggu itu benar di video, dan gagal di "
            "dapurmu. Kamu tidak salah masak.", "sem_cap": True},
    {"layout": "item", "kicker": "Yang tidak difilmkan", "preco": "tiga angka",
     "nar": "Videonya tidak memfilmkan tiga angka: jumlah orang, isi rak, "
            "dan harga daerahmu.", "sem_cap": True},
    {"layout": "item", "kicker": "Hitungan yang jujur", "preco": "bagi dua kali",
     "nar": "Bagi anggaranmu dengan jumlah orang, lalu dengan tujuh hari. "
            "Itu angka dapurmu yang sebenarnya.", "sem_cap": True},
    {"layout": "item", "kicker": "Baru bandingkan", "preco": "menu apa pun",
     "nar": "Setelah itu, menu viral mana pun bisa diuji: cocok dengan "
            "angkamu, atau cuma cocok di video.", "sem_cap": True},
    {"layout": "cta", "kicker": "Resep Naik Level", "sub": "lembar lengkapnya",
     "nar": "Lembar enam barisnya ada di video panjang. Lakukan pembagiannya "
            "hari ini.", "sem_cap": True},
]

COPY = """# Matematika di balik menu seratus ribu seminggu

## JUDUL
Menu Hemat Rp100 Ribu Seminggu: Matematika yang Tidak Difilmkan Siapa Pun

## DESKRIPSI
Satu video muncul di berandamu: uang Rp100.000 cukup untuk makan seminggu. Videonya tidak bohong — masakannya jadi, totalnya benar. Lalu kamu mencobanya di dapurmu sendiri, dan uangnya habis di hari Rabu.

Kesimpulan yang biasa muncul: pasti aku yang gagal. Kesimpulan yang benar lebih sederhana: hitungan di video itu bukan hitungan rumahmu, dan tidak pernah dimaksudkan begitu.

Video ini membedah matematika yang video menu tidak filmkan.

TIGA ANGKA YANG TIDAK IKUT DIFILMKAN. Menu itu dihitung untuk berapa orang — banyak menu hemat dibuat untuk dua porsi, sementara rumahmu berisi lima. Isi rak sebelum menu dimulai — dapur di video sudah punya minyak, bumbu dan beras, dan rak penuh itu tidak pernah dihitung sebagai biaya. Dan harga di daerahmu — pertengahan Agustus 2026 harga beras di banyak daerah naik antara Rp500 dan Rp1.500 per kilogram hanya dalam dua minggu, jadi total belanja yang difilmkan bulan lalu bukan angka bulan ini.

SATU PEMBAGIAN YANG MENGUBAH SEMUANYA. Anggaran seminggu dibagi jumlah orang, dibagi jumlah hari. Rp100.000 dibagi tujuh hari itu sekitar Rp14.000 sehari untuk seisi rumah; untuk empat orang, sekitar Rp3.500 per orang per hari. Angka itu terasa kecil, dan justru itu gunanya: ia langsung memberitahu kelas menu mana yang masuk akal untukmu.

MATEMATIKA PROTEIN. Uang dapur tidak habis di nasi — ia habis di lauk, karena protein adalah baris termahal. Menu viral bisa murah karena proteinnya dipilih dari kelas harga yang murah. Bagian itu layak ditiru; jumlahnya tidak, karena jumlah mengikuti isi rumahmu.

LEMBAR ENAM BARIS. Jumlah orang, anggaran minggu ini, hasil pembagian, harga beras daerahmu dari panel resmi Badan Pangan, jatah protein per hari, dan sisa untuk sayur dan bumbu. Diisi lima menit, sekali seminggu, sebelum belanja. Lembar ini sekaligus penyaring: setiap menu viral tinggal diuji cocok atau tidak dengan baris ketigamu.

CARA MENYESUAIKAN MENU ORANG LAIN. Skalakan porsinya dulu. Tukar protein hanya di kelas harga yang sama. Tiru strukturnya, bukan totalnya. Dan ambil harga dari daerahmu, bukan dari keterangan video.

EMPAT KESALAHAN YANG MAHAL, termasuk membandingkan minggu pertamamu dengan dapur video yang mulai dari rak penuh, dan menghitung per masakan padahal hitungan yang adil adalah per minggu.

Menu yang sama menghasilkan angka berbeda di dua rumah — dan dua-duanya bisa benar. Itu inti videonya.

## BAB
{CAPITULOS}

## KOMENTAR
Satu pertanyaan, karena jawabannya pasti berbeda di tiap rumah: setelah kamu bagi anggaran dengan jumlah orang dan tujuh hari, berapa jatah per orang per hari di rumahmu — dan untuk berapa orang? Aku sedang mengumpulkan angka itu dari banyak rumah untuk video berikutnya. Kalau ada pos dapur lain yang mau dibedah, sebutkan juga.

## HASHTAG
#MenuHemat #UangDapur #ResepNaikLevel

## TAG
menu hemat, menu 100 ribu, menu seminggu, uang dapur, anggaran belanja, masak hemat, menu murah, menu keluarga, atur uang belanja, keuangan rumah tangga, harga beras 2026, dapur hemat, belanja mingguan, tips hemat, resep naik level

## PENGATURAN STUDIO
- Bahasa: Indonesia (id) | Kategori: Pendidikan (27)
- Bukan untuk anak-anak
- Pengungkapan konten yang diubah atau sintetis: YA (suara dibuat dengan AI)
- Lokasi: Indonesia | Lisensi: Lisensi YouTube standar
- Iklan tengah: aktif (durasi di atas delapan menit)

## MUSIK / LISENSI
{TRILHA}

## CATATAN SUMBER
Satu-satunya fakta harga berwaktu di video ini adalah kenaikan harga beras sekitar Rp500 sampai Rp1.500 per kilogram dalam dua minggu pada pertengahan Agustus 2026, sesuai laporan media Indonesia yang saling bersesuaian pada periode itu, dan keberadaan panel harga pangan harian resmi (Panel Harga Pangan Badan Pangan Nasional dan Pusat Informasi Harga Pangan Strategis Bank Indonesia), keduanya gratis dan dipisahkan per daerah serta per kualitas. Angka Rp100.000, Rp14.000 dan Rp3.500 adalah ILUSTRASI ARITMETIKA dari sebuah pembagian, bukan klaim harga pangan atau klaim kecukupan gizi; jumlah yang benar untuk rumahmu keluar dari lembar yang kamu isi sendiri, bukan dari video ini. Tidak ada harga bahan makanan spesifik yang diklaim di sini, dan justru itu intinya: setiap angka diambil dari rumahmu atau dari panel resmi, pada tanggalmu sendiri. Video ini materi edukasi tentang cara menghitung belanja dapur rumah tangga; ini bukan nasihat keuangan dan bukan nasihat gizi.
"""

SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-004",
    "idioma": "id",
    "voz": "id-ID-GadisNeural",
    # canais.trilha do banco. Sem este campo o credito CC-BY sai do hash,
    # e o hash ja creditou Cipher2 para um canal registrado em Deliberate_Thought.
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#3A1008", "c1": "#C1440E", "c2": "#E8B84B", "bg": "#FDF6EC"},
    "thumb": {"l1": "MENU 100 RIBU SEMINGGU", "l2": "kenapa gagal di rumahmu"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/resep-naik-level-004.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")

    from ensaio import MODELO_VOZ, duracao_estimada  # noqa: E402
    R, P = MODELO_VOZ[SPEC["voz"]]
    dl = duracao_estimada(CENAS, SPEC["voz"])
    ds = duracao_estimada(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"voz {SPEC['voz']}: {R} chars/s + {P} s/frase")
    print(f"longo: {sum(len(c['nar']) for c in CENAS)} chars -> {dl/60:.1f} min")
    print(f"short: {sum(len(c['nar']) for c in SHORT)} chars -> {ds:.0f} s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
