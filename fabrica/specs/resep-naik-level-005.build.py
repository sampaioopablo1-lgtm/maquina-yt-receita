#!/usr/bin/env python3
"""Monta a spec resep-naik-level-005.

POR QUE ESTE TEMA, E POR QUE NESTE FORMATO

O acervo do nicho tem sessenta pautas medidas (13 e 18/08/2026) e uma
assinatura que nao falha: TODO outlier tem CIFRA EM RUPIAS mais PERIODO no
titulo.

    Uang Belanja Cuma 50 Ribu ... (drama)      6.057,0 v/d
    4 STRATEGI ... UANG 50-100RB PERHARI       1.167,4
    SULAP 100 RIBU! Dapur Aman Seminggu          691,5
    Tips Belanja Mingguan ... Budget 150 Ribu    478,5
    Uang 50 Ribu Untuk 3 Hari                    278,9
    ---- mediana dos neutros (n=33)               54,6
    ---- mediana dos mortos  (n=14)                4,7

As DOZE pautas que este canal tem em banco sao todas do tipo "kenapa X salah",
sem cifra e sem periodo. Elas foram pesquisadas por ASSUNTO, nao por FORMATO.
Usar uma delas como titulo seria escrever no formato que o proprio nicho mede
como morto — entao o assunto vem do banco e a ESTRUTURA vem do outlier, que e
o que a rotina pede.

O canal ja usou "Menu Hemat Rp100 Ribu Seminggu" (18/08) e "5 Strategi Ibu
Mengatur Uang Dapur Saat Harga Beras Naik" (17/08). Similaridade do titulo
novo contra o acervo do canal: 0,378, contra o teto de 0,65.

A DOR DATADA, confirmada por duas fontes que batem, uma delas institucional:

  BPS, primeira semana de agosto de 2026, via CNN Indonesia (10/08) e CNBC
  Indonesia (10/08), os dois citando os mesmos numeros do BPS:
    - arroz, media nacional de todas as qualidades: Rp15.545/kg, +0,16% vs julho
    - faixa entre regioes: Rp12.500 (minimo) a Rp50.000/kg (maximo, em
      Pegunungan Bintang, Intan Jaya e Nabire)
    - oleo de cozinha: Rp20.221/litro, -0,04% vs julho, de Rp15.500 a Rp60.000
  BPS/Bapanas, mesma semana:
    - IPH do arroz em alta em 106 kabupaten/kota, contra 155 na ultima semana
      de julho — o menor numero em dois meses
    - IPH em queda em 21 provincias
  BPS via Tribun/AEPI e ANTARA:
    - o arroz subiu SETE MESES SEGUIDOS, de janeiro a julho de 2026

O GIRO. A leitura obvia da noticia e "a alta acabou, subiu so nol koma um
seis". O video mostra por que essa leitura quebra o orcamento de quem cozinha:
a media nacional nao e o preco de ninguem. Entre o minimo e o maximo ha QUATRO
VEZES de diferenca, e a variacao mensal pequena esconde sete meses de acumulo.

O QUE ESTE ROTEIRO NAO FAZ, de proposito: nao preve preco, nao promete
economia em rupias, e nao diz que o numero do BPS esta errado. Ele diz que o
numero do BPS responde a OUTRA pergunta — a do pais — e ensina a montar a
referencia da propria cozinha. Isso esta dito na cena e na descricao.

TAXA DA VOZ. id-ID-GadisNeural, MODELO_VOZ de ensaio.py: R = 14,12 chars/s,
P = 1,318 s por frase. Densidade medida do canal: 2,07 frases por cena no
longo, 1,80 no short. Orcamento para oitenta cenas em 810 s: 8.025 caracteres.
Faixa do short: 243 a 365 caracteres.
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


# ------------------------------------------------ 1. Angka yang tidak cocok
T("Lima belas ribu", "kata angka resmi",
  "Bulan ini ada satu angka yang beredar di mana-mana. Harga beras rata-rata "
  "nasional: lima belas ribu lima ratus empat puluh lima rupiah per kilo.",
  cap="Angka yang tidak cocok")
I("Naik berapa", "nol koma satu enam persen",
  "Dibanding bulan Juli, itu naik nol koma satu enam persen. Kecil sekali. "
  "Hampir tidak terasa kalau dibaca di layar.")
T("Tapi", "belanja Anda bilang lain",
  "Lalu Anda pulang dari pasar. Uangnya habis lebih cepat dari minggu lalu. "
  "Dan angka tadi tidak menjelaskan apa pun.")
T("Pertanyaannya", "siapa yang salah",
  "Jadi siapa yang salah di sini? Badan statistik, atau perasaan Anda?")
T("Jawabannya", "tidak keduanya",
  "Tidak keduanya. Dua-duanya benar. Yang salah adalah cara angka itu dipakai.")
I("Yang dijawab angka itu", "pertanyaan negara",
  "Angka rata-rata nasional menjawab pertanyaan tentang negara. Bukan "
  "pertanyaan tentang dapur Anda.")
T("Dua pertanyaan berbeda", "satu angka saja",
  "Itu dua pertanyaan yang berbeda. Dan selama ini kita pakai satu angka "
  "untuk menjawab keduanya.")
L("Yang akan kita bongkar", ["Kenapa rata-rata menyesatkan",
                             "Jarak harga antar daerah",
                             "Cara bikin acuan sendiri"],
  "Di video ini kita bongkar tiga hal. Kenapa rata-rata menyesatkan. Berapa "
  "jauh jarak harga antar daerah. Dan cara membuat acuan Anda sendiri.")
T("Yang tidak dijanjikan", "ramalan harga",
  "Yang tidak dijanjikan: video ini tidak meramal harga. Tidak ada yang bisa.")
I("Sumbernya", "badan statistik",
  "Semua angka di sini dari Badan Pusat Statistik, minggu pertama Agustus dua "
  "ribu dua puluh enam. Saya sebutkan sumbernya setiap kali.")
T("Kenapa itu penting", "supaya bisa dicek",
  "Kenapa itu penting? Supaya Anda bisa cek sendiri, dan tidak perlu percaya "
  "pada saya.")
C("Mulai", "dari yang paling sering salah dibaca",
  "Kita mulai dari bagian yang paling sering salah dibaca. Kata rata-rata.")

# ------------------------------------------ 2. Tujuh bulan, bukan satu minggu
T("Tujuh bulan", "bukan satu bulan",
  "Naik nol koma satu enam persen terdengar seperti tidak ada apa-apa. "
  "Sampai Anda lihat berapa lama itu sudah terjadi.",
  cap="Tujuh bulan, bukan satu minggu")
I("Berapa lama", "Januari sampai Juli",
  "Harga beras naik tujuh bulan berturut-turut. Dari Januari sampai Juli tahun "
  "ini. Setiap bulan naik sedikit.")
T("Masalahnya", "sedikit itu menumpuk",
  "Dan di sinilah letak masalahnya. Sedikit itu menumpuk.")
T("Bayangkan", "satu tangga",
  "Bayangkan satu tangga. Setiap anak tangga rendah. Tidak ada yang terasa "
  "berat saat dinaiki.")
T("Tapi setelah tujuh", "Anda sudah di lantai lain",
  "Tapi setelah tujuh anak tangga, Anda sudah berada di lantai yang lain. "
  "Padahal tidak ada satu langkah pun yang terasa besar.")
I("Itu yang terjadi", "pada uang belanja",
  "Itu persis yang terjadi pada uang belanja Anda. Tidak ada bulan yang "
  "terasa mencekik. Tapi tahun ini terasa jauh lebih berat dari tahun lalu.")
T("Kenapa terlewat", "karena kita baca bulanan",
  "Kenapa ini terlewat? Karena berita menyajikan angka bulanan, dan kita "
  "membacanya juga bulanan.")
T("Ubah kacamatanya", "baca per tujuh bulan",
  "Coba ubah kacamatanya. Jangan tanya berapa naiknya bulan ini. Tanya berapa "
  "naiknya sejak Januari.")
L("Dua pertanyaan", ["Naik berapa bulan ini",
                     "Naik berapa sejak Januari"],
  "Dua pertanyaan, dua jawaban yang sangat berbeda. Yang pertama menenangkan. "
  "Yang kedua menjelaskan dompet Anda.")
I("Kabar baiknya", "kenaikan melambat",
  "Ada kabar baiknya juga, dan itu nyata. Menurut Badan Pusat Statistik, "
  "kenaikan mulai melambat di awal Agustus.")
T("Melambat", "bukan turun",
  "Tapi melambat bukan berarti turun. Tangga berhenti naik secepat sebelumnya. "
  "Anda tetap berdiri di lantai yang sama.")
C("Sekarang", "bagian yang jarang dibaca",
  "Sekarang bagian dari data bulan ini yang paling jarang dibaca. Jarak antar "
  "daerah.")

# --------------------------------------------- 3. Jarak yang empat kali lipat
T("Angka yang sama", "dua dunia berbeda",
  "Rata-rata nasional beras minggu itu: lima belas ribu lima ratus empat puluh "
  "lima rupiah. Sekarang lihat ujung-ujungnya.",
  cap="Jarak yang empat kali lipat")
B("Sebaran harga beras", ["Termurah", "Rata-rata", "Termahal"], [0.25, 0.31, 1.0],
  "Harga terendah yang tercatat: dua belas ribu lima ratus rupiah per kilo. "
  "Harga tertinggi: lima puluh ribu rupiah per kilo.")
I("Selisihnya", "empat kali lipat",
  "Itu selisih empat kali lipat. Beras yang sama, negara yang sama, minggu yang "
  "sama.")
T("Di mana yang termahal", "daerah paling jauh",
  "Yang tertinggi tercatat di daerah seperti Pegunungan Bintang, Intan Jaya, dan "
  "Nabire. Ongkos angkut ke sana jauh lebih mahal.")
T("Artinya", "rata-rata itu titik kosong",
  "Artinya rata-rata itu adalah titik yang hampir tidak ditempati siapa pun. "
  "Sangat sedikit orang yang benar-benar membayar harga rata-rata.")
T("Bukan cuma antar pulau", "antar pasar juga",
  "Dan ini bukan cuma soal antar pulau. Di kota yang sama, dua pasar bisa beda "
  "harga. Anda mungkin sudah tahu itu.")
I("Bukti dari data", "seratus enam daerah",
  "Data minggu itu mencatat kenaikan indeks harga beras di seratus enam "
  "kabupaten dan kota.")
I("Minggu sebelumnya", "seratus lima puluh lima",
  "Minggu terakhir Juli angkanya seratus lima puluh lima. Jadi jumlah daerah "
  "yang masih naik memang berkurang.")
T("Sementara itu", "dua puluh satu provinsi turun",
  "Sementara itu indeks harga turun di dua puluh satu provinsi. Naik dan turun "
  "terjadi bersamaan, di negara yang sama.")
T("Rata-rata menutupi itu", "semuanya jadi satu angka",
  "Rata-rata menutupi semua itu. Naik, turun, jauh, dekat, semuanya diperas "
  "jadi satu angka.")
I("Bukan berarti salah", "angka itu perlu",
  "Bukan berarti angka itu salah atau tidak berguna. Pemerintah butuh satu "
  "angka untuk melihat seluruh negeri.")
C("Tapi Anda", "belanja di satu pasar",
  "Tapi Anda tidak belanja di seluruh negeri. Anda belanja di satu pasar.")

# ------------------------------------------------ 4. Harga acuan Anda sendiri
T("Jadi", "bikin acuan sendiri",
  "Jadi solusinya sederhana, dan tidak butuh aplikasi apa pun. Anda bikin "
  "harga acuan Anda sendiri.",
  cap="Harga acuan Anda sendiri")
T("Alatnya", "buku tulis juga bisa",
  "Alatnya bebas. Buku tulis, catatan di ponsel, atau satu lembar di kulkas. "
  "Yang penting bentuknya tetap.")
L("Empat kolom", ["Nama barang", "Satuan", "Harga", "Tanggal dan tempat"],
  "Empat kolom saja. Nama barang. Satuan. Harga. Lalu tanggal dan tempat "
  "belinya.")
I("Kolom satuan", "yang paling sering dilewat",
  "Kolom satuan itu yang paling sering dilewat, dan justru yang paling "
  "menentukan.")
T("Kenapa", "biar bisa dibandingkan",
  "Kenapa? Karena tanpa satuan, dua harga tidak bisa dibandingkan sama sekali.")
I("Contohnya", "bungkus versus kilo",
  "Beras satu bungkus harganya sekian. Beras satu kilo harganya sekian. Kalau "
  "bungkusnya tidak ditimbang, dua angka itu tidak bicara.")
T("Aturannya", "selalu ke satuan standar",
  "Aturannya: selalu ubah ke satuan standar. Per kilo, per liter, per butir. "
  "Sekali saja, waktu mencatat.")
L("Berapa barang", ["Delapan sampai sepuluh",
                     "Yang dibeli tiap minggu",
                     "Bukan yang sesekali"],
  "Berapa barang yang perlu dicatat? Delapan sampai sepuluh. Pilih yang Anda "
  "beli hampir tiap minggu, bukan yang sesekali.")
T("Kenapa dibatasi", "biar bertahan",
  "Kenapa dibatasi? Karena daftar yang terlalu panjang akan berhenti diisi "
  "dalam dua minggu. Ini soal bertahan, bukan soal lengkap.")
I("Tanggal itu wajib", "harga tanpa tanggal tidak berarti",
  "Dan tanggal itu wajib. Harga tanpa tanggal tidak berarti apa-apa bulan "
  "depan.")
T("Setelah empat minggu", "Anda punya sesuatu",
  "Setelah empat minggu Anda punya sesuatu yang tidak dimiliki berita mana "
  "pun. Harga rata-rata dapur Anda.")
C("Dengan itu", "kita bisa berhitung",
  "Dan dengan angka itu, kita akhirnya bisa berhitung.")

# ------------------------------------- 5. Anggaran mingguan dari harga Anda
T("Urutannya", "sering terbalik",
  "Kebanyakan orang menentukan uang belanja dulu, lalu memaksa menunya masuk. "
  "Urutan itu terbalik.",
  cap="Anggaran mingguan dari harga Anda")
T("Urutan yang benar", "pemakaian dulu",
  "Urutan yang benar dimulai dari pemakaian. Berapa yang benar-benar habis di "
  "rumah Anda dalam seminggu.")
I("Contoh beras", "ditimbang, bukan ditebak",
  "Ambil beras. Jangan ditebak. Timbang sekali, atau catat berapa lama satu "
  "karung bertahan.")
T("Lalu kalikan", "dengan harga Anda",
  "Lalu kalikan pemakaian itu dengan harga dari catatan Anda sendiri. Bukan "
  "harga di berita.")
L("Tiga langkah", ["Pemakaian seminggu", "Kali harga Anda", "Itu anggaran"],
  "Tiga langkah. Pemakaian seminggu. Dikali harga Anda. Hasilnya anggaran "
  "mingguan yang nyata.")
T("Bedanya besar", "angka ini milik Anda",
  "Bedanya besar. Angka ini tidak dipinjam dari siapa pun. Dia keluar dari "
  "dapur Anda sendiri.")
I("Kalau hasilnya lebih besar", "dari uang yang ada",
  "Sering kali hasilnya lebih besar dari uang yang tersedia. Itu bukan "
  "kegagalan. Itu informasi.")
T("Sekarang Anda tahu", "selisihnya di mana",
  "Sekarang Anda tahu selisihnya berapa, dan di barang yang mana. Sebelumnya "
  "yang Anda tahu cuma uangnya kurang.")
L("Tiga cara menutup selisih", ["Kurangi jumlah",
                                 "Ganti barang",
                                 "Pindah tempat beli"],
  "Ada tiga cara menutup selisih. Kurangi jumlahnya. Ganti barangnya. Atau "
  "pindah tempat belinya.")
T("Yang ketiga", "paling jarang dicoba",
  "Yang ketiga paling jarang dicoba, padahal datanya sudah bilang jarak antar "
  "tempat itu besar.")
I("Catat hasilnya", "biar tahu mana yang jalan",
  "Dan catat mana yang Anda pilih. Bulan depan Anda perlu tahu cara mana yang "
  "benar-benar jalan.")
C("Sekarang", "kapan harus berubah",
  "Terakhir dari bagian hitungan: kapan Anda harus mengubah rencana.")

# --------------------------------------------- 6. Titik picu, bukan panik
T("Masalah kedua", "kapan bereaksi",
  "Ada masalah kedua yang jarang dibahas. Bukan berapa harganya, tapi kapan "
  "Anda harus bereaksi.",
  cap="Titik picu, bukan panik")
T("Dua kesalahan", "sama mahalnya",
  "Ada dua kesalahan di sini, dan keduanya sama mahalnya.")
I("Kesalahan pertama", "bereaksi ke setiap berita",
  "Yang pertama: berganti menu setiap kali ada berita harga naik. Belanja jadi "
  "kacau, dan hemat tidak pernah datang.")
I("Kesalahan kedua", "tidak bereaksi sama sekali",
  "Yang kedua: tidak bereaksi sama sekali sampai uangnya habis di hari kedua "
  "puluh lima.")
T("Jalan tengahnya", "aturan yang ditulis",
  "Jalan tengahnya bukan perasaan. Jalan tengahnya adalah satu aturan yang "
  "Anda tulis sebelum harganya naik.")
L("Bentuk aturannya", ["Barang apa", "Naik berapa persen", "Lalu apa"],
  "Bentuknya sederhana. Barang apa. Naik berapa persen dari acuan Anda. Lalu "
  "tindakannya apa.")
I("Contohnya", "satu kalimat saja",
  "Contoh satu kalimat. Kalau telur naik lebih dari sepersepuluh dari acuan "
  "saya, minggu itu saya tukar dengan tahu dan tempe.")
T("Kenapa ditulis dulu", "supaya bukan panik",
  "Kenapa harus ditulis lebih dulu? Karena keputusan yang diambil saat panik "
  "hampir selalu lebih mahal.")
T("Berapa aturan", "dua atau tiga cukup",
  "Berapa aturan yang perlu? Dua atau tiga saja. Untuk barang yang paling "
  "besar porsinya di belanja Anda.")
I("Batasnya milik Anda", "bukan dari norma mana pun",
  "Dan angka batasnya Anda yang tentukan. Tidak ada lembaga mana pun yang "
  "menetapkan berapa persen itu terlalu banyak untuk dapur Anda.")
C("Terakhir", "batas video ini",
  "Sebelum ditutup, satu bagian yang jarang ada di video seperti ini. Batasnya.")

# ------------------------------------- 7. Yang tidak dijanjikan video ini
T("Batas pertama", "ini bukan ramalan",
  "Batas pertama, dan yang paling penting. Tidak ada di video ini yang meramal "
  "harga bulan depan.",
  cap="Yang tidak dijanjikan video ini")
T("Yang bisa dilakukan", "mengukur yang sudah terjadi",
  "Yang bisa Anda lakukan hanya mengukur apa yang sudah terjadi, dengan lebih "
  "teliti dari sebelumnya.")
I("Batas kedua", "angka nasional tetap berguna",
  "Batas kedua. Angka rata-rata nasional tidak salah dan tidak percuma. Dia "
  "menjawab pertanyaan tentang negara, dan itu memang perlu.")
T("Yang keliru", "memakainya untuk dapur",
  "Yang keliru cuma satu: memakai angka itu untuk memutuskan belanja satu "
  "keluarga.")
I("Batas ketiga", "ini tidak menjanjikan hemat",
  "Batas ketiga. Mencatat harga tidak otomatis membuat belanja lebih murah. "
  "Dia membuat belanja lebih terbaca.")
T("Kadang hasilnya", "belanja naik",
  "Kadang hasilnya justru sebaliknya. Anda sadar selama ini kurang membeli "
  "sesuatu yang memang dibutuhkan.")
T("Itu tetap kemajuan", "keputusan jadi sadar",
  "Itu tetap kemajuan. Keputusannya jadi Anda yang ambil, bukan harga yang "
  "ambil untuk Anda.")
L("Yang dibawa pulang", ["Catat delapan barang",
                          "Pakai satuan standar",
                          "Tulis satu aturan"],
  "Tiga hal untuk dibawa pulang. Catat delapan barang. Pakai satuan standar. "
  "Tulis satu aturan sebelum harga naik.")
I("Mulai kapan", "belanja berikutnya",
  "Mulainya kapan? Belanja berikutnya. Bukan bulan depan, dan bukan setelah "
  "beli buku baru.")
T("Empat minggu lagi", "Anda punya acuan",
  "Empat minggu lagi Anda sudah punya acuan sendiri. Dan berita harga tidak "
  "lagi jadi satu-satunya angka yang Anda punya.")
C("Video berikutnya", "belanja mingguan versus bulanan",
  "Di video berikutnya kita pakai catatan itu untuk satu pertanyaan yang sering "
  "salah dijawab. Belanja mingguan atau bulanan, mana yang benar-benar hemat?")

# ---------------------------------------------------------------- o short
# Video inteiro por si, nao um trecho do longo: abre pelo RESULTADO (a faixa
# de quatro vezes), nao pelo contexto. Em canal frio e o short que entrega —
# no setiap-level os shorts medem 19,32 v/d contra 0,15 dos longos.
SHORT = [
    {"layout": "titulo", "kicker": "Dua belas ribu", "sub": "harga terendah",
     "nar": "Beras termurah dua belas ribu lima ratus rupiah per kilo.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Lima puluh ribu", "sub": "harga tertinggi",
     "nar": "Termahal lima puluh ribu. Minggu yang sama.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Rata-rata", "sub": "lima belas ribu",
     "nar": "Rata-ratanya lima belas ribu. Hampir tak ada yang bayar segitu.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Artinya", "sub": "bukan harga Anda",
     "nar": "Angka itu soal negara. Bukan soal dapur Anda.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Yang dipakai", "sub": "catatan sendiri",
     "nar": "Catat delapan barang: nama, satuan, harga, tanggal.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Empat minggu", "sub": "acuan Anda jadi",
     "nar": "Empat minggu lagi acuannya milik Anda. Hitungannya di video lengkap.",
     "sem_cap": True},
]

THUMB = {"l1": "Rp15.545 atau Rp50.000", "l2": "harga beras yang mana?"}

COPY = """# Harga acuan dapur sendiri: kenapa rata-rata nasional tidak cukup

## TITULO
Beras Rp15.545 Kata BPS, di Pasar Bisa Rp50 Ribu: Cara Hitung Uang Dapur Mingguan Anda Sendiri

## DESCRICAO
Badan Pusat Statistik mencatat harga beras rata-rata nasional semua kualitas pada minggu pertama Agustus 2026 sebesar Rp15.545 per kilogram, naik 0,16 persen dibanding Juli 2026. Angka itu terdengar kecil. Tapi banyak pembaca berita merasa uang belanjanya justru habis lebih cepat.

Dua-duanya benar. Yang keliru adalah cara angka rata-rata dipakai.

Pada minggu yang sama, BPS mencatat harga beras terendah Rp12.500 per kilogram dan tertinggi Rp50.000 per kilogram — daerah dengan harga tertinggi antara lain Pegunungan Bintang, Intan Jaya, dan Nabire, yang ongkos angkutnya jauh lebih mahal. Itu selisih empat kali lipat untuk komoditas yang sama, di negara yang sama, di minggu yang sama. Rata-rata nasional adalah titik yang hampir tidak ditempati siapa pun.

Kenaikan kecil bulanan juga menyembunyikan hal lain: harga beras naik tujuh bulan berturut-turut, dari Januari sampai Juli 2026. Setiap bulan naik sedikit, dan sedikit itu menumpuk. Kabar baiknya, kenaikan mulai melambat — kenaikan indeks harga beras tercatat di 106 kabupaten/kota pada minggu pertama Agustus, turun dari 155 kabupaten/kota di minggu terakhir Juli, dan indeks harga turun di 21 provinsi. Melambat bukan berarti turun.

Video ini tidak meramal harga, dan tidak menjanjikan penghematan dalam rupiah. Isinya satu sistem yang bisa dipakai siapa saja tanpa aplikasi:

Harga acuan sendiri — empat kolom saja: nama barang, satuan, harga, tanggal dan tempat beli. Kolom satuan adalah yang paling sering dilewat dan justru paling menentukan, karena tanpa satuan standar dua harga tidak bisa dibandingkan. Delapan sampai sepuluh barang yang Anda beli hampir tiap minggu sudah cukup; daftar yang terlalu panjang berhenti diisi dalam dua minggu.

Anggaran mingguan — urutannya dimulai dari pemakaian nyata di rumah Anda, dikali harga dari catatan Anda sendiri, bukan harga di berita. Kalau hasilnya lebih besar dari uang yang tersedia, itu bukan kegagalan melainkan informasi: sekarang Anda tahu selisihnya berapa dan di barang yang mana.

Titik picu — satu aturan yang ditulis sebelum harga naik, bukan saat panik. Barang apa, naik berapa persen dari acuan Anda, lalu tindakannya apa. Dua atau tiga aturan sudah cukup, dan angka batasnya Anda yang tentukan.

Dan bagian yang jarang ada: batas dari semua ini. Angka rata-rata nasional tidak salah — dia menjawab pertanyaan tentang negara. Mencatat harga tidak otomatis membuat belanja lebih murah; dia membuat belanja lebih terbaca.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Dua pertanyaan, karena jawabannya pasti beda jauh antar daerah: berapa harga beras per kilo di pasar Anda minggu ini, dan di kota mana? Saya sedang mengumpulkan jawabannya untuk video berikutnya, tentang belanja mingguan versus bulanan.

## HASHTAGS
#UangDapur #HargaBeras #ResepNaikLevel

## TAGS
harga beras, uang dapur, anggaran belanja, belanja mingguan, hemat belanja, harga pangan, bps, inflasi pangan, ibu rumah tangga, atur keuangan, dapur hemat, harga sembako, catatan belanja, biaya dapur, keuangan keluarga

## CONFIGURACAO DE STUDIO
- Idioma: Bahasa Indonesia (id) | Categoria: Educacao (27)
- Tidak dibuat untuk anak-anak
- Pengungkapan konten yang diubah atau sintetis: YA (suara dihasilkan AI)
- Lokasi: Indonesia | Lisensi: Lisensi standar YouTube
- Iklan di tengah: aktif (durasi di atas delapan menit)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Seluruh angka harga berasal dari Badan Pusat Statistik (BPS) untuk minggu pertama Agustus 2026, sebagaimana dilaporkan CNN Indonesia dan CNBC Indonesia pada 10 Agustus 2026: harga beras rata-rata nasional Rp15.545 per kilogram (naik 0,16 persen dibanding Juli), rentang Rp12.500 sampai Rp50.000 per kilogram, dan minyak goreng Rp20.221 per liter (turun 0,04 persen). Jumlah kabupaten/kota dengan kenaikan indeks perkembangan harga beras (106, turun dari 155) dan penurunan indeks di 21 provinsi juga bersumber dari BPS untuk periode yang sama. Kenaikan harga beras tujuh bulan berturut-turut (Januari sampai Juli 2026) dilaporkan berdasarkan data BPS. Diakses pada 20 Agustus 2026. Angka bisa berubah setelah rilis berikutnya — periksa kembali di bps.go.id dan di Pusat Informasi Harga Pangan Strategis Bank Indonesia. Contoh batas persentase pada bagian titik picu adalah contoh, bukan ketentuan dari lembaga mana pun. Video ini bersifat edukatif tentang pencatatan harga dan penyusunan anggaran rumah tangga, bukan nasihat keuangan atau gizi.
"""

SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-005",
    "idioma": "id",
    "voz": "id-ID-GadisNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#3A1008", "c1": "#C1440E", "c2": "#E8B84B", "bg": "#FDF6EC"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "resep-naik-level-005.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
