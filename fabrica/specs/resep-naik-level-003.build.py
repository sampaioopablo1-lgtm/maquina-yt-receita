#!/usr/bin/env python3
"""Monta a spec resep-naik-level-003.

PAUTA, medida em 14/08/2026 e gravada em pautas_banco (54 linhas, inclusive os
mortos). Grupo de pares legitimo n=54, mediana 38,0 views/dia — depois de
descartar 46 videos por idioma e 16 por serem short-drama, um nicho vizinho que
a busca traz junto e que domina o topo bruto (ate 15.555 v/d) sem ter relacao
nenhuma com o tema.

    formato                                    n   mediana   topo
    menu/receita                               2       3,8    6,4   <- MORTO
    haul de belanja com budget                19      40,9  478,5
    sistema de gestao do dinheiro da cozinha   9      40,2 1167,4   <- outlier
    lista de truques                           9      54,6  566,5

O achado que decide esta spec: RECEITA e o formato mais morto do nicho, e e o
que da nome ao canal. O config diz "masakan hemat dan uang dapur" — a demanda
esta toda na metade `uang dapur`. Entao nao ha receita nenhuma aqui.

OUTLIER: Pucuk Asa, "4 STRATEGI ISTRI MENGATUR UANG 50-100RB PERHARI UNTUK
KEBUTUHAN DAPUR" — 103.847 views em 89 dias = 1.167,4 v/d, trinta vezes a
mediana. Modelo a ESTRUTURA dele, nunca o assunto:

    [N] STRATEGI + [QUEM] + MENGATUR UANG + [FAIXA CONCRETA] + [PERIODO]
    + UNTUK [FIM]

EIXO NAO USADO: nenhum dos 54 pares cita o painel oficial de precos. O PIHPS do
Bank Indonesia (bi.go.id/hargapangan) e o Panel Harga da Badan Pangan Nasional
(panelharga.badanpangan.go.id) publicam o preco do arroz por qualidade — Bawah
I e II, Medium I e II, Super I e II — atualizado por dia e por regiao. E de
graca, e o nicho inteiro ignora.

Isso resolve tambem o problema de validade: um video que cita "Rp15.650" morre
em duas semanas. Um video que ensina a LER o painel continua certo, e o preco
sai da fonte em vez de sair do roteiro.

DOR DATADA (duas fontes que batem, veja a nota de fontes da copy):
  * meados de agosto/2026: beras premium e medium sobem Rp500 a Rp1.500/kg em
    duas semanas
  * inicio de junho/2026: beras kualitas bawah I +7,56% para Rp15.650/kg
  * inicio de junho/2026: rupiah passa de Rp18.000 por dolar

SIMILARIDADE vs os dois pacotes anteriores do MESMO canal:
  -001 "5 Makan Malam Enak di Bawah Rp10.000 per Porsi"  -> lista com preco
  -002 "Belanja Mingguan Rp100.000: Daftar Persis 7 Hari" -> haul com budget
Este e SISTEMA, nao lista nem haul: nenhuma lista de compras, nenhum cardapio.
O eixo (painel oficial + amplop que se move) nao aparece em nenhum dos dois.

DIMENSIONAMENTO pelo modelo de dois termos da voz (fabrica/ensaio.py):
id-ID-GadisNeural = 17,42 chars/s de fala + 1,376 s por frase. A pausa dela e a
segunda maior do portfolio, entao cabe MENOS texto por cena que numa voz de
pausa curta: ~126 chars por cena, nao os ~150 do portugues da Thalita.
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
T("Sabtu pagi", "uang yang sama",
  "Sabtu pagi, kamu ke pasar dengan uang yang sama seperti minggu lalu. "
  "Kantong belanjamu pulang lebih ringan. Kamu tidak salah hitung.",
  cap="Sabtu pagi di pasar")
I("Berapa yang naik", "lima ratus sampai seribu lima ratus",
  "Pertengahan Agustus dua ribu dua puluh enam, harga beras di banyak daerah "
  "naik lima ratus sampai seribu lima ratus rupiah per kilogram.")
I("Dalam berapa lama", "dua minggu",
  "Kenaikan itu terjadi hanya dalam dua minggu. Bukan setahun, bukan sebulan.")
I("Dan bukan sekali", "awal Juni juga",
  "Dan itu bukan kejadian tunggal. Awal Juni beras kualitas bawah sudah naik "
  "lebih dari tujuh persen dalam satu putaran.")
I("Rupiah ikut bergerak", "menembus delapan belas ribu",
  "Di bulan yang sama rupiah sempat menembus delapan belas ribu per dolar "
  "Amerika. Barang impor ikut terseret, dan minyak goreng termasuk.")
I("Yang kamu rasakan", "bukan persen",
  "Tapi kamu tidak merasakan persen. Kamu merasakan lauk yang mengecil di hari "
  "Kamis, dan itu jauh lebih jelas daripada grafik mana pun.")
I("Reaksi pertama", "menyalahkan diri sendiri",
  "Reaksi pertama hampir selalu sama. Pasti aku yang boros. Pasti aku kurang "
  "pintar mengatur uang.")
I("Penjelasan itu nyaman", "tapi tidak menjelaskan",
  "Penjelasan itu nyaman karena cepat selesai. Tapi ia tidak menjelaskan kenapa "
  "jutaan rumah tangga mengalami hal yang sama di bulan yang sama.")
I("Ada penjelasan lain", "dan yang ini bisa diperbaiki",
  "Ada penjelasan lain yang lebih sederhana. Dan yang satu ini bisa kamu "
  "perbaiki minggu ini juga.")
L("Yang kita bangun", ["Kenapa anggaran telat", "Panel harga resmi",
                       "Tiga angka", "Amplop yang bergerak", "Kesalahan mahal"],
  "Lima bagian. Kenapa anggaranmu selalu telat. Panel harga resmi yang gratis. "
  "Tiga angka yang dicatat. Amplop yang ikut bergerak. Dan kesalahan yang "
  "paling mahal.")
I("Tidak perlu aplikasi", "buku tulis cukup",
  "Tidak perlu aplikasi dan tidak perlu langganan apa pun. Buku tulis biasa "
  "sudah cukup, dan justru itu yang paling awet.")
I("Satu hal dulu", "ini bukan soal makan sedikit",
  "Satu hal perlu jelas sejak awal. Ini bukan tentang makan lebih sedikit. Ini "
  "tentang tahu harga sebelum berdiri di depan pedagang.")
T("Jadi", "kenapa selalu telat?",
  "Kalau begitu pertanyaannya berubah. Kenapa anggaran yang kamu susun rapi "
  "selalu kalah cepat dari harga?")

# ---------------------------------------------------------------- cap 2
T("Anggaranmu", "tahu harga bulan lalu",
  "Jawabannya ada di tanggal. Anggaran yang kamu pakai hari ini dibuat dari "
  "harga bulan lalu, dan tidak ada yang memperbaruinya.",
  cap="Anggaranmu tahu harga bulan lalu")
I("Cara anggaran dibuat", "dari ingatan",
  "Kebanyakan anggaran dapur lahir dari ingatan. Kamu ingat beras kira-kira "
  "sekian, telur kira-kira sekian, lalu angka itu dipakai berbulan-bulan.")
I("Ingatan tidak diperbarui", "harga diperbarui tiap hari",
  "Masalahnya ingatan tidak ikut naik. Harga di pasar berubah setiap hari, dan "
  "angka di kepalamu berhenti di hari kamu terakhir memperhatikannya.")
I("Selisihnya kecil", "sampai dikali tiga puluh",
  "Selisih per barang memang kecil. Tapi ia dikalikan jumlah barang, lalu "
  "dikalikan jumlah hari, dan di situ ia berhenti terasa kecil.")
I("Itu sebabnya", "uang habis lebih cepat",
  "Itu sebabnya uang belanja habis lebih cepat tanpa kamu berbelanja lebih "
  "banyak. Isi kantongmu sama, isi anggaranmu yang ketinggalan.")
I("Bedanya penting", "boros dan telat itu lain",
  "Dan bedanya penting. Boros artinya kamu membeli lebih banyak. Telat artinya "
  "kamu membeli hal yang sama dengan angka yang sudah kedaluwarsa.")
I("Yang kedua bisa dibetulkan", "tanpa mengurangi apa pun",
  "Yang pertama minta kamu menahan diri. Yang kedua cuma minta angka yang "
  "benar, dan tidak menyuruhmu mengurangi apa pun.")
I("Berapa sering diperbarui", "sekali seminggu cukup",
  "Lalu seberapa sering angkanya harus diperbarui? Sekali seminggu sudah "
  "cukup, dan setiap hari malah membuat orang berhenti mencatat.")
I("Dari mana angkanya", "bukan dari tebakan",
  "Pertanyaan berikutnya lebih penting. Angka yang benar itu diambil dari "
  "mana, kalau bukan dari tebakan sendiri?")
I("Bertanya ke pedagang", "sudah terlambat",
  "Bertanya ke pedagang saat sudah berdiri di lapak itu terlambat. Di titik "
  "itu kamu sedang menawar, bukan sedang merencanakan.")
I("Bertanya ke tetangga", "harga daerah lain",
  "Bertanya ke tetangga juga meleset. Harga berbeda antar daerah, kadang cukup "
  "jauh, dan pengalaman orang lain bukan harga pasarmu.")
T("Padahal", "angkanya sudah ada",
  "Padahal angka resminya sudah ada, diperbarui tiap hari, dan bisa dibuka "
  "gratis. Di mana?")

# ---------------------------------------------------------------- cap 3
T("Panel harga resmi", "gratis, dan hampir tak dipakai",
  "Pemerintah menerbitkan harga pangan harian lewat panel resmi. Badan Pangan "
  "Nasional punya satu, dan Bank Indonesia punya satu lagi.",
  cap="Panel harga yang hampir tak dipakai")
I("Apa yang ada di sana", "harga per komoditas",
  "Di dalamnya ada harga per komoditas. Beras dan telur. Cabai dan gula. "
  "Minyak goreng dan daging ayam.")
I("Beras dipecah", "per kualitas",
  "Beras tidak ditulis sebagai satu angka. Ia dipecah per kualitas, dari bawah "
  "sampai super, karena yang kamu beli belum tentu yang diberitakan.")
I("Ini yang sering keliru", "berita pakai angka mana",
  "Dan di situ letak salah paham yang sering terjadi. Berita menyebut satu "
  "angka, kamu membeli kualitas lain, lalu keduanya terasa tidak cocok.")
I("Ada per daerah juga", "bukan rata-rata nasional",
  "Panel itu juga memisahkan per provinsi. Rata-rata nasional hampir tidak "
  "berguna untuk dapurmu, karena kamu tidak belanja di rata-rata.")
I("Berapa lama membukanya", "kurang dari lima menit",
  "Membukanya butuh kurang dari lima menit. Pilih daerahmu, catat komoditas "
  "yang kamu beli rutin, dan sudah.")
I("Bukan untuk menawar", "untuk merencanakan",
  "Panel ini bukan alat menawar. Pedagang punya biaya sendiri dan harga eceran "
  "wajar berbeda dari harga acuan.")
I("Gunanya lain", "tahu arah, bukan menang debat",
  "Gunanya adalah tahu arah. Naik, turun, atau diam. Itu saja sudah mengubah "
  "keputusan belanjamu minggu ini.")
I("Kalau naik", "belanja lebih awal",
  "Kalau arahnya naik, kamu memajukan belanja barang tahan lama. Bukan "
  "memborong, hanya memajukan.")
I("Kalau turun", "tunda yang bisa ditunda",
  "Kalau arahnya turun, kamu menunda yang memang bisa ditunda. Keputusan yang "
  "sama, cuma pindah beberapa hari.")
I("Kalau diam", "jangan ubah apa pun",
  "Dan kalau harganya diam, kamu tidak mengubah apa pun. Tidak melakukan apa "
  "pun juga sebuah keputusan, asal kamu tahu alasannya.")
T("Sekarang", "apa yang dicatat?",
  "Panelnya sudah terbuka. Tinggal satu hal, dan ini bagian yang membuatnya "
  "jadi kebiasaan: apa yang kamu catat?")

# ---------------------------------------------------------------- cap 4
T("Tiga angka", "cuma tiga",
  "Kamu mencatat tiga angka per komoditas. Bukan sepuluh, bukan semua isi "
  "panel. Tiga.",
  cap="Tiga angka yang kamu catat")
L("Per komoditas", ["Harga panel", "Harga yang kamu bayar", "Selisihnya"],
  "Harga di panel. Harga yang benar-benar kamu bayar. Dan selisih antara "
  "keduanya.")
I("Kolom pertama", "harga panel hari itu",
  "Kolom pertama diisi sebelum berangkat. Itu harga panel di hari itu, untuk "
  "daerahmu, untuk kualitas yang biasa kamu beli.")
I("Kolom kedua", "struk atau ingatan segar",
  "Kolom kedua diisi sepulang belanja. Ambil dari struk, atau dari ingatan "
  "yang masih segar, bukan dari perkiraan minggu depan.")
I("Kolom ketiga", "yang paling berguna",
  "Kolom ketiga adalah selisihnya, dan justru kolom itu yang paling berguna. "
  "Ia memberitahu berapa jarak antara acuan dan lapak langgananmu.")
I("Selisih itu tetap", "dan itu kabar baik",
  "Untuk satu pedagang, selisih itu biasanya cukup stabil. Artinya setelah "
  "beberapa minggu kamu bisa menebak harga sebelum sampai di pasar.")
I("Berapa komoditas", "lima sampai delapan",
  "Jangan mencatat semuanya. Lima sampai delapan komoditas yang paling sering "
  "kamu beli sudah menutup sebagian besar belanjamu.")
I("Kalau lebih dari itu", "catatan berhenti",
  "Kalau daftarnya terlalu panjang, catatan berhenti di minggu ketiga. Itu "
  "pola yang sama di semua kebiasaan baru.")
B("Kemana uangnya", ["Beras", "Lauk", "Sayur", "Minyak"], [100, 78, 45, 30],
  "Dan ketika tiga bulan berlalu, kamu punya gambar. Bukan perasaan tentang "
  "apa yang mahal, tapi urutan yang bisa dilihat.")
I("Gambar itu mengubah", "urutan prioritas",
  "Gambar itu mengubah keputusan. Barang di batang tertinggi layak dicari "
  "alternatifnya. Barang di batang terpendek tidak usah dipikirkan lagi.")
I("Itu menghemat tenaga", "bukan cuma uang",
  "Dan itu menghemat sesuatu yang jarang dihitung. Tenaga. Kamu berhenti "
  "menawar hal-hal yang tidak menggerakkan total belanjamu.")
T("Angkanya sudah ada", "lalu uangnya bagaimana?",
  "Sekarang angkanya kamu punya. Pertanyaan terakhir yang tersisa adalah soal "
  "uangnya sendiri:")

# ---------------------------------------------------------------- cap 5
T("Amplop", "yang ikut bergerak",
  "Sistem amplop sudah lama dipakai, dan ada satu hal yang membuatnya gagal "
  "belakangan ini. Amplopnya tidak pernah berubah isinya.",
  cap="Amplop yang ikut bergerak")
I("Amplop tetap", "harga tidak tetap",
  "Kamu memasukkan jumlah yang sama tiap minggu, sementara harga di luar terus "
  "bergerak. Amplop yang diam melawan harga yang berjalan.")
I("Akibatnya", "bukan hemat, tapi kurang",
  "Akibatnya bukan hemat. Akibatnya kurang di hari Kamis, setiap minggu. Dan "
  "orang menyalahkan dirinya lagi.")
I("Perbaikannya kecil", "satu amplop tambahan",
  "Perbaikannya kecil dan hanya butuh satu amplop lagi. Namanya amplop selisih.")
I("Isinya berapa", "dari kolom ketiga",
  "Isinya diambil dari kolom ketiga catatanmu. Kalau harga panel naik, "
  "kenaikan itu yang masuk ke amplop selisih.")
I("Kalau harga turun", "isinya tidak diambil",
  "Dan kalau harga turun, uang di amplop itu tidak diambil. Ia menumpuk, dan "
  "menjadi bantalan untuk minggu yang buruk berikutnya.")
I("Itu yang membedakan", "bantalan, bukan kejutan",
  "Perbedaannya di situ. Kenaikan harga berhenti menjadi kejutan dan berubah "
  "menjadi pos yang sudah punya tempat.")
I("Berapa besar bantalannya", "biasanya kecil",
  "Bantalan itu biasanya lebih kecil dari yang orang kira. Karena bukan seluruh "
  "belanja yang naik, hanya beberapa barang.")
I("Dan itu terlihat", "di catatanmu sendiri",
  "Dan itu terlihat di catatanmu sendiri, bukan di berita. Berita bicara "
  "tentang rata-rata; catatanmu bicara tentang dapurmu.")
I("Kalau uangnya tidak ada", "dahulukan yang bergerak",
  "Kalau amplop selisih tidak bisa diisi bulan ini, dahulukan komoditas yang "
  "paling bergerak. Beras hampir selalu masuk daftar itu.")
I("Bukan berarti berhasil selalu", "ada bulan yang memang berat",
  "Dan ini perlu dikatakan jujur. Ada bulan yang memang tidak cukup, dan "
  "catatan rapi tidak mengubah harga.")
I("Yang berubah", "kamu tahu lebih awal",
  "Yang berubah adalah waktunya. Kamu tahu di hari Senin, bukan di hari Kamis, "
  "dan seminggu lebih awal itu ruang untuk memutuskan.")
T("Sistemnya sudah utuh", "apa yang merusaknya?",
  "Sampai di sini sistemnya sudah utuh. Tinggal mengenali empat hal yang "
  "paling sering merusaknya:")

# ---------------------------------------------------------------- cap 6
T("Kesalahan pertama", "memborong saat panik",
  "Yang pertama adalah memborong ketika berita bilang harga naik. Terasa "
  "cerdas, dan hampir selalu merugikan.",
  cap="Empat kesalahan yang mahal")
I("Kenapa merugi", "uang terkunci",
  "Uangmu terkunci di barang, dan sebagian barang itu rusak sebelum habis. "
  "Beras berkutu dan minyak berubah bau bukan hal langka.")
I("Bedanya dengan memajukan", "jumlahnya",
  "Memajukan belanja berbeda dari memborong. Memajukan artinya membeli jumlah "
  "yang sama lebih awal. Memborong artinya membeli jumlah yang lebih besar.")
I("Kesalahan kedua", "ganti merek tanpa hitung",
  "Yang kedua adalah pindah ke merek lebih murah tanpa menghitung harga per "
  "satuan. Kemasan mengecil lebih sering daripada harga naik.")
I("Cara memeriksanya", "bagi dengan isinya",
  "Memeriksanya gampang. Bagi harga dengan gram atau mililiter yang tertulis, "
  "dan bandingkan angka itu, bukan angka di rak.")
I("Kesalahan ketiga", "mencatat tanpa tanggal",
  "Yang ketiga adalah mencatat harga tanpa tanggal. Catatan tanpa tanggal "
  "tidak bisa dibandingkan, dan tiga bulan lagi ia cuma daftar angka.")
I("Kesalahan keempat", "memakai rata-rata nasional",
  "Yang keempat adalah memakai angka rata-rata nasional untuk dapur sendiri. "
  "Itu angka yang benar untuk pertanyaan yang berbeda.")
I("Yang menyatukan keempatnya", "angka tanpa konteks",
  "Keempatnya punya akar yang sama. Angka dipakai tanpa konteks, dan angka "
  "tanpa konteks memberi rasa yakin yang keliru.")
I("Dan itu lebih berbahaya", "daripada tidak mencatat",
  "Merasa yakin dengan angka yang salah lebih berbahaya daripada tidak "
  "mencatat sama sekali. Karena sekarang ada dokumen yang membenarkanmu.")
I("Aturan satu kalimat", "tanggal, daerah, kualitas",
  "Satu kalimat menutup keempatnya. Setiap angka yang kamu catat punya "
  "tanggal, punya daerah, dan punya kualitas.")
T("Lalu", "bagaimana ini bertahan?",
  "Sistemnya sekarang benar. Yang tersisa cuma satu, dan ini yang menentukan "
  "apakah ia masih hidup bulan depan:")

# ---------------------------------------------------------------- cap 7
T("Bertahan", "tiga kebiasaan",
  "Catatan seperti ini mati karena rutinitas, tidak pernah karena rumusnya. "
  "Tiga kebiasaan sudah cukup.",
  cap="Supaya ini bertahan")
I("Pertama", "hari dan jam yang tetap",
  "Pertama, satu hari tetap dalam seminggu untuk membuka panel. Hari yang "
  "berpindah-pindah adalah kebiasaan yang tidak pernah terbentuk.")
I("Kedua", "satu buku, bukan banyak kertas",
  "Kedua, satu buku saja. Catatan yang tersebar di banyak kertas dan banyak "
  "aplikasi hilang dalam dua bulan.")
I("Ketiga", "satu orang yang bertanggung jawab",
  "Ketiga, satu orang yang memegangnya. Catatan milik semua orang adalah "
  "catatan milik siapa pun.")
I("Bagi tugasnya", "kalau berdua",
  "Kalau di rumah ada dua orang dewasa, bagi tugasnya. Satu membuka panel, "
  "satu mengisi kolom belanja.")
I("Yang jangan dilakukan", "menyalahkan lewat catatan",
  "Satu hal yang jangan dilakukan. Jangan memakai catatan itu untuk "
  "menyalahkan siapa pun di rumah.")
I("Kalau itu terjadi", "catatan berhenti diisi",
  "Begitu catatan berubah jadi alat menyalahkan, ia berhenti diisi dengan "
  "jujur. Dan catatan yang tidak jujur lebih buruk daripada tidak ada.")
L("Ringkasnya", ["Panel dulu", "Tiga kolom", "Amplop selisih",
                 "Tanggal dan daerah", "Satu pemegang"],
  "Ringkasnya begini. Buka panel sebelum belanja. Catat tiga kolom. Sediakan "
  "amplop selisih. Beri tanggal dan daerah. Dan tunjuk satu pemegang.")
I("Bagian yang jarang dilakukan", "kolom selisih",
  "Bagian yang hampir tidak pernah dilakukan orang adalah kolom selisih. "
  "Tanpa dia, catatanmu cuma daftar harga.")
I("Kalau cuma satu hal", "buka panelnya sekali",
  "Kalau kamu hanya melakukan satu hal setelah video ini, buka panel harga "
  "untuk daerahmu satu kali. Cuma satu kali.")
I("Waktunya", "lebih cepat dari antre",
  "Itu memakan waktu lebih sedikit daripada mengantre di kasir. Dan angka "
  "pertama yang kamu lihat biasanya sudah mengubah daftar belanjamu.")
C("Resep Naik Level", "uang dapur, bukan resep",
  "Kalau kamu sudah membuka panelnya, tulis di komentar berapa selisih beras "
  "di daerahmu. Aku sedang mengumpulkan angka itu.")
C("Resep Naik Level", "uang dapur, bukan resep",
  "Dan kalau ada pos belanja lain yang mau dibedah, sebutkan. Yang paling "
  "banyak diminta akan dibuat lebih dulu.")

SHORT = [
    {"layout": "titulo", "kicker": "Uang belanja habis", "sub": "bukan karena boros",
     "nar": "Uang belanjamu habis lebih cepat, dan kemungkinan besar bukan "
            "karena kamu boros.", "sem_cap": True},
    {"layout": "item", "kicker": "Penyebabnya", "preco": "anggaran kedaluwarsa",
     "nar": "Anggaranmu memakai harga bulan lalu. Harga di pasar berubah tiap "
            "hari.", "sem_cap": True},
    {"layout": "item", "kicker": "Yang tidak dipakai orang", "preco": "panel harga resmi",
     "nar": "Badan Pangan Nasional menerbitkan harga harian per daerah dan per "
            "kualitas. Gratis.", "sem_cap": True},
    {"layout": "item", "kicker": "Catat tiga angka", "preco": "panel, bayar, selisih",
     "nar": "Harga panel, harga yang kamu bayar, dan selisihnya. Selisih itu "
            "yang menebak harga minggu depan.", "sem_cap": True},
    {"layout": "cta", "kicker": "Resep Naik Level", "sub": "sistem lengkapnya",
     "nar": "Buka panelnya sekali minggu ini. Sistem lengkapnya ada di video "
            "panjang.", "sem_cap": True},
]

COPY = """# Sistem uang dapur saat harga bergerak

## JUDUL
5 Strategi Ibu Mengatur Uang Dapur Saat Harga Beras Naik Tiap Minggu (2026)

## DESKRIPSI
Sabtu pagi kamu ke pasar dengan uang yang sama seperti minggu lalu, dan kantong belanjamu pulang lebih ringan. Kamu tidak salah hitung.

Pertengahan Agustus 2026 harga beras di banyak daerah naik antara Rp500 dan Rp1.500 per kilogram hanya dalam dua minggu. Awal Juni beras kualitas bawah sudah naik lebih dari tujuh persen dalam satu putaran, di bulan yang sama ketika rupiah sempat menembus Rp18.000 per dolar Amerika.

Reaksi pertama hampir selalu sama: pasti aku yang boros. Penjelasan itu nyaman karena cepat selesai, tapi ia tidak menjelaskan kenapa jutaan rumah tangga mengalami hal yang sama di bulan yang sama.

Ada penjelasan lain yang lebih sederhana, dan yang ini bisa diperbaiki minggu ini juga: anggaranmu memakai harga bulan lalu, dan tidak ada yang memperbaruinya. Boros artinya kamu membeli lebih banyak. Telat artinya kamu membeli hal yang sama dengan angka yang sudah kedaluwarsa. Yang kedua tidak menyuruhmu mengurangi apa pun.

Video ini membangun sistemnya dari nol, tanpa aplikasi dan tanpa langganan. Buku tulis biasa sudah cukup.

Isinya: kenapa anggaran dapur selalu kalah cepat dari harga, dan kenapa selisih kecil per barang berhenti terasa kecil setelah dikalikan jumlah barang dan jumlah hari.

Panel harga resmi yang hampir tidak dipakai siapa pun. Badan Pangan Nasional dan Bank Indonesia menerbitkan harga pangan harian, dipecah per komoditas, per kualitas beras dari bawah sampai super, dan per daerah. Rata-rata nasional hampir tidak berguna untuk dapurmu, karena kamu tidak belanja di rata-rata.

Tiga angka yang kamu catat per komoditas: harga panel sebelum berangkat, harga yang benar-benar kamu bayar, dan selisih antara keduanya. Kolom ketiga yang paling berguna, karena selisih terhadap pedagang langgananmu biasanya stabil — setelah beberapa minggu kamu bisa menebak harga sebelum sampai di pasar. Cukup lima sampai delapan komoditas; daftar yang terlalu panjang berhenti diisi di minggu ketiga.

Amplop selisih: kenapa sistem amplop gagal belakangan ini, dan perbaikan kecil yang membuat kenaikan harga berhenti menjadi kejutan dan berubah menjadi pos yang sudah punya tempat.

Dan empat kesalahan yang paling mahal, termasuk memborong saat panik (uangmu terkunci di barang, sebagian rusak sebelum habis), pindah merek tanpa menghitung harga per satuan karena kemasan mengecil lebih sering daripada harga naik, dan mencatat angka tanpa tanggal.

Satu kalimat menutup semuanya: setiap angka yang kamu catat punya tanggal, punya daerah, dan punya kualitas.

## BAB
{CAPITULOS}

## KOMENTAR
Satu pertanyaan, karena jawabannya pasti berbeda-beda: berapa selisih harga beras antara panel resmi dan lapak langgananmu di daerahmu? Aku sedang mengumpulkan angka itu untuk video berikutnya. Sebutkan juga daerahmu, karena tanpa itu angkanya tidak bisa dibandingkan.

## HASHTAG
#UangDapur #HargaBeras #ResepNaikLevel

## TAG
uang dapur, atur uang belanja, harga beras 2026, panel harga pangan, belanja hemat, ibu rumah tangga, keuangan rumah tangga, sistem amplop, harga sembako, inflasi pangan, catatan belanja, hemat belanja bulanan, bapanas, harga pangan harian, dapur hemat

## PENGATURAN STUDIO
- Bahasa: Indonesia (id) | Kategori: Pendidikan (27)
- Bukan untuk anak-anak
- Pengungkapan konten yang diubah atau sintetis: YA (suara dibuat dengan AI)
- Lokasi: Indonesia | Lisensi: Lisensi YouTube standar
- Iklan tengah: aktif (durasi di atas delapan menit)

## MUSIK / LISENSI
{TRILHA}

## CATATAN SUMBER
Angka kenaikan harga di video ini berasal dari laporan media Indonesia pada Juni dan Agustus 2026 yang saling bersesuaian: kenaikan beras premium dan medium sekitar Rp500 sampai Rp1.500 per kilogram dalam dua minggu di pertengahan Agustus 2026, kenaikan beras kualitas bawah lebih dari tujuh persen pada awal Juni 2026, dan nilai tukar rupiah yang sempat menembus Rp18.000 per dolar Amerika pada periode yang sama. Angka-angka itu BERUBAH CEPAT dan sengaja tidak dijadikan dasar perhitungan mana pun di video ini — justru itu alasan sistemnya mengambil harga dari panel resmi, bukan dari angka yang disebut di sini. Harga harian resmi dapat diperiksa sendiri di Panel Harga Pangan Badan Pangan Nasional dan di Pusat Informasi Harga Pangan Strategis Bank Indonesia, keduanya gratis dan dipisahkan per daerah serta per kualitas. Video ini adalah materi edukasi tentang cara menyusun catatan belanja rumah tangga; ini bukan nasihat keuangan, bukan nasihat investasi, dan bukan rekomendasi membeli komoditas apa pun.
"""

SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-003",
    "idioma": "id",
    "voz": "id-ID-GadisNeural",
    # canais.trilha do banco. Sem este campo o credito CC-BY sai do hash,
    # e o hash ja creditou Cipher2 para um canal registrado em Deliberate_Thought.
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#3A1008", "c1": "#C1440E", "c2": "#E8B84B", "bg": "#FDF6EC"},
    "thumb": {"l1": "HARGA NAIK TIAP MINGGU", "l2": "anggaranmu tidak tahu"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/resep-naik-level-003.json"
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
