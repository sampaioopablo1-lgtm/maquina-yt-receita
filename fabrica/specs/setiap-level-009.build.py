#!/usr/bin/env python3
"""Monta a spec setiap-level-009 — o numero do cartaz nao e o numero que fica.

PAUTA, medida em 19/08/2026. Tres eixos nesta rodada, ja LIMPOS de ruido de
busca antes de calcular a mediana (aprendizado 336):

    investasi / emas / reksadana    mediana 34,4 v/d   (n=19)  <- escolhido
    dana pendidikan                 mediana  9,7       (n=16)
    BPJS Kesehatan / KRIS           mediana  0,5       (n=20)  <- MORTO

Os dois descartados ensinam coisas diferentes, e por isso os dois ficam
gravados:

  dana-pendidikan tinha mediana BRUTA de 13,8 com quatro novelas dubladas de
  118 a 163 minutos no topo ("Istri selingkuh", "Mobilku disita"...). Limpo,
  cai para 9,7. Mesmo padrao do KPR de uma hora atras.

  BPJS Kesehatan e o caso INVERSO do KPR: o topo e legitimo e enorme — a
  tvOnenews com 81.524 views em 16 dias, 5013,9 v/d, sobre o fim das classes
  1, 2 e 3 — mas a cauda e um enxame de canais-fazenda ("AWAS! BPJS berubah
  total") medindo de 0,1 a 0,9 v/d. Demanda alta pela NOTICIA, nenhuma pelo
  formato. Mediana 0,5. Nao da para construir um longo ali.

Outliers do eixo escolhido (>= 103,2):

    Contek Portfolio Investasi 10 Miliar ETF Gue Sebagai Karyawan  5428,8 v/d
    HANYA Butuh 5 Investasi ETF ini UNTUK PENSIUN CEPAT            2368,3
    POV: Begini Rasanya Punya 100 Lot Saham Bank Favorit Lo        1001,3
    Baru Gajian? Lakukan Ini Sebelum Uangmu Habis                   244,1
    5 Investasi Terbaik untuk Ibu Rumah Tangga Pemula               188,5
    Nabung Rp10.000 Sehari Bisa Jadi Berapa?                        119,6

Modelo a ESTRUTURA do ultimo — valor pequeno e concreto seguido de "vira
quanto?" — que e tambem o formato que ESTE canal ja mediu como bom
("valor inicial minusculo concreto", 310,0 v/d em v_maquina_formatos). Nao
modelo o topo: portfolio de dez bilhoes nao e a vida de quem assiste este
canal, e copiar aquele assunto seria mentir sobre o publico.

NUMEROS VERIFICADOS (fontes que batem entre si; acesso 19/08/2026):

  BI Rate — decidido HOJE, 19/08/2026, na RDG de 18 e 19 de agosto:
      BI Rate            5,75%   (terceiro mes seguido sem mudanca)
      Deposit Facility   4,75%
      Lending Facility   6,50%
    Fontes concordantes: Kompas, CNN Indonesia, CNBC Indonesia, Republika,
    Antara e Sindonews, todas citando o Bank Indonesia.

  Inflacao — BPS, dado de julho de 2026 divulgado em 03/08/2026:
      inflasi tahunan (yoy)   2,88%
      inflasi inti (yoy)      2,76%
      IHK  108,60 (jul/2025) -> 111,73 (jul/2026)
    Fontes concordantes: Beritasatu, Jawapos, Kompas, Republika, Aspek.

  Imposto sobre juros de deposito — PPh Pasal 4 ayat 2, FINAL:
      20% sobre o valor bruto dos juros
      isento quando o saldo nao passa de Rp7.500.000
    Base legal: PP 131 Tahun 2000, em vigor desde 01/01/2001.
    Fontes concordantes: Ortax e o tax-guide do Pajakku, que reproduz o PP.

O QUE NAO ENTRA: a taxa de garantia do LPS. A busca devolveu 7,75% sem data,
e esse numero parece ser historico, nao de agosto de 2026. Sem duas fontes
datadas que batam, fica de fora — o roteiro nao precisa dele.

Tambem NAO cito taxa de deposito de banco nenhum. Elas variam por banco e
por prazo, e eu nao tenho fonte institucional para uma taxa especifica. O
roteiro trata a taxa nominal como PREMISSA declarada em voz alta ("suponha
que o teu deposito pague tanto"), e todo o resto — imposto e inflacao — sai
de numero com fonte.

SIMILARIDADE vs os onze longos do canal: nenhum trata de deposito, inflacao
ou retorno real. O mais proximo e "Cara Atur Gaji 2026: Dana Darurat,
Cicilan, Investasi, Pensiun", que ALOCA o dinheiro entre quatro pilares;
este pergunta quanto um pilar especifico realmente devolve depois de
imposto e inflacao. Pergunta diferente, instrumento diferente.

TRILHA: Wholesome, a identidade do canal.

DIMENSIONAMENTO. id-ID-ArdiNeural = 18,72 chars/s + 1,079 s/frase.
Alvo no MEIO da janela: ~13,2 min, ~10.600 chars. Desta vez ja miro 88
cenas na primeira escrita, aplicando o aprendizado 337: com esta voz o
mesmo relogio pede mais texto, entao cena curta demais estoura a contagem.
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
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar,
                  "sem_cap": True})


# ------------------------------------------------------------------ cap 1
T("Angka di brosur", "bukan angka yang tinggal",
  "Bank memasang satu angka di brosur deposito. Yang tinggal di kantongmu "
  "adalah angka lain, dan jaraknya lebih besar dari yang kamu kira.",
  cap="Angka brosur bukan angka simpan")
I("Bukan tipuan", "cuma dua potongan",
  "Ini bukan tipuan dan tidak ada yang disembunyikan. Cuma ada dua potongan "
  "yang tidak muncul di halaman depan.")
I("Potongan pertama", "pajak",
  "Potongan pertama adalah pajak atas bunganya. Ia dipotong langsung, sebelum "
  "uang itu sampai ke rekeningmu.")
I("Potongan kedua", "inflasi",
  "Potongan kedua adalah inflasi. Ia tidak muncul di mutasi rekening sama "
  "sekali, tapi ia yang menentukan apakah kamu benar-benar maju.")
I("Kenapa sekarang", "keputusan hari ini",
  "Dan kenapa hari ini. Bank Indonesia baru saja mengumumkan keputusannya, "
  "jadi angka acuannya masih hangat.")
I("BI Rate", "lima koma tujuh lima persen",
  "Suku bunga acuan ditahan di lima koma tujuh lima persen. Ini bulan ketiga "
  "berturut-turut tanpa perubahan.")
I("Dua angka pendamping", "fasilitas simpanan dan pinjaman",
  "Suku bunga fasilitas simpanan ada di empat koma tujuh lima persen, dan "
  "fasilitas pinjaman di enam koma lima nol persen.")
I("Dan inflasinya", "dua koma delapan delapan persen",
  "Sementara itu inflasi tahunan per Juli tercatat dua koma delapan delapan "
  "persen menurut Badan Pusat Statistik.")
I("Sudah kelihatan", "jaraknya tipis",
  "Letakkan dua angka itu berdampingan dan masalahnya sudah kelihatan. "
  "Jarak antara bunga dan inflasi lebih tipis dari yang terasa.")
I("Lalu pajak masuk", "dan jaraknya menyempit lagi",
  "Lalu pajak masuk ke tengah-tengahnya, dan jarak yang sudah tipis itu "
  "menyempit lagi.")
I("Kenapa ini bukan detail", "uang yang mengendap lama",
  "Ini bukan detail akuntansi. Untuk uang yang mengendap bertahun-tahun, "
  "selisih satu dua persen setahun berubah jadi angka yang terasa. Dan "
  "hampir semua orang punya uang yang mengendap.")
L("Yang akan kita bahas", ["Kenapa bunga brosur bukan bunga bersih",
                           "Pajak dua puluh persen dan pengecualiannya",
                           "Inflasi: potongan yang tak terlihat",
                           "Hitungan penuh atas sepuluh juta rupiah",
                           "Kapan deposito tetap masuk akal"],
  "Lima bagian. Kenapa bunga brosur bukan bunga bersih. Pajaknya berapa dan "
  "kapan tidak kena. Bagaimana inflasi memotong tanpa terlihat. Hitungan "
  "penuhnya. Dan kapan deposito tetap pilihan yang benar.")
I("Satu hal dulu", "ini bukan ajakan",
  "Satu hal dulu. Ini bukan ajakan membeli atau menjual apa pun, dan tidak "
  "menyebut bank mana pun. Kita membahas mekanisme.")
I("Aturan kanal", "angka dengan sumber",
  "Aturan kanal tetap berlaku. Angka dengan sumber dan tanggal. Yang tidak "
  "bisa diukur, tidak kita ucapkan.")
T("Kita mulai", "kenapa dua angka itu beda?",
  "Kita mulai dari pertanyaan yang paling sering muncul. Kenapa bunga yang "
  "dijanjikan dan bunga yang diterima bisa beda?")

# ------------------------------------------------------------------ cap 2
T("Bunga brosur", "selalu bruto",
  "Angka yang dipasang di brosur selalu angka bruto. Artinya, itu jumlah "
  "sebelum potongan apa pun.",
  cap="Bunga brosur bukan bunga bersih")
I("Itu bukan kesalahan", "memang standarnya",
  "Itu bukan kesalahan bank. Menampilkan bunga bruto memang cara standar di "
  "seluruh industri, supaya angkanya bisa dibandingkan antarbank.")
I("Tapi buat kamu", "yang penting yang bersih",
  "Tapi buat kamu yang menaruh uang, angka yang berarti hanya satu. Yang "
  "bersih, setelah potongan.")
I("Bedanya ke mana", "ke kas negara",
  "Selisihnya tidak hilang. Ia masuk ke kas negara sebagai pajak penghasilan "
  "atas bunga.")
I("Dipotong di mana", "di bank, otomatis",
  "Pemotongannya terjadi di bank, otomatis. Kamu tidak perlu melapor atau "
  "menyetor sendiri.")
I("Praktisnya", "yang masuk sudah bersih",
  "Praktisnya, yang masuk ke rekeningmu tiap jatuh tempo sudah bersih. "
  "Karena itu banyak orang tidak pernah sadar ada potongan.")
I("Di situ jebakannya", "membandingkan bruto dengan bruto",
  "Dan di situ jebakannya. Orang membandingkan bunga bruto deposito dengan "
  "imbal hasil bersih instrumen lain, lalu menyimpulkan salah.")
I("Contoh salah kaprah", "membandingkan dengan reksadana",
  "Contoh yang paling sering saya lihat: orang membandingkan bunga bruto "
  "deposito dengan imbal hasil reksadana pasar uang yang sudah bersih. "
  "Deposito jadi terlihat unggul padahal belum tentu.")
I("Perbandingan yang adil", "bersih lawan bersih",
  "Perbandingan yang adil selalu bersih lawan bersih. Kalau tidak, kamu "
  "sedang membandingkan dua hal yang berbeda.")
T("Sudah jelas", "berapa pajaknya?",
  "Kita tahu ada potongan. Berapa persisnya, dan apakah selalu kena?")

# ------------------------------------------------------------------ cap 3
T("Dua puluh persen", "dan bersifat final",
  "Bunga deposito dan tabungan dikenakan pajak penghasilan sebesar dua puluh "
  "persen dari jumlah bruto, dan sifatnya final.",
  cap="Pajak dua puluh persen")
I("Dasar hukumnya", "peraturan tahun dua ribu",
  "Dasarnya adalah Peraturan Pemerintah nomor seratus tiga puluh satu tahun "
  "dua ribu, yang berlaku sejak awal tahun dua ribu satu.")
I("Final artinya", "selesai di situ",
  "Final artinya selesai di situ. Bunga itu tidak digabungkan lagi dengan "
  "penghasilanmu yang lain di laporan tahunan.")
I("Itu ada sisi baiknya", "tidak mendorong ke lapisan atas",
  "Ada sisi baiknya. Bunga deposito tidak mendorongmu naik ke lapisan tarif "
  "yang lebih tinggi, seperti yang terjadi pada penghasilan biasa.")
I("Bandingkan dengan gaji", "gaji digabung, ini tidak",
  "Bandingkan dengan gaji bulanan. Gaji digabungkan dan bisa mendorongmu "
  "ke lapisan tarif berikutnya. Bunga deposito berhenti di tarif "
  "tunggalnya sendiri.")
I("Dan ada pengecualian", "batas tujuh setengah juta",
  "Ada juga pengecualian yang jarang disebut. Kalau saldonya tidak melebihi "
  "tujuh juta lima ratus ribu rupiah, bunganya tidak dipotong pajak.")
I("Baca batasnya baik-baik", "soal saldo, bukan bunga",
  "Perhatikan bahwa batas itu soal saldo, bukan soal besar bunganya. Ini "
  "sering tertukar.")
I("Untuk siapa ini berguna", "yang baru mulai",
  "Buat siapa aturan ini berguna? Buat orang yang baru mulai menabung dengan "
  "jumlah kecil, dan mengira pasti kena potongan.")
I("Tapi jangan dipecah", "itu bukan celah",
  "Tapi ini bukan celah untuk memecah simpanan besar menjadi banyak deposito "
  "kecil. Ketentuannya memang mengantisipasi pemecahan seperti itu.")
I("Efek praktisnya", "seperlima bunga hilang",
  "Efek praktis dari tarif ini sederhana. Dari setiap lima rupiah bunga yang "
  "dijanjikan, satu rupiah tidak pernah sampai padamu.")
T("Pajak sudah jelas", "sekarang yang tak terlihat",
  "Potongan pertama sudah jelas dan bisa dihitung. Bagaimana dengan yang "
  "tidak muncul di mana-mana?")

# ------------------------------------------------------------------ cap 4
T("Inflasi", "potongan tanpa kuitansi",
  "Inflasi adalah potongan yang tidak punya kuitansi. Saldomu naik, tapi apa "
  "yang bisa kamu beli dengan saldo itu turun.",
  cap="Inflasi: potongan tak terlihat")
I("Angkanya sekarang", "dua koma delapan delapan persen",
  "Angka resminya, inflasi tahunan per Juli dua ribu dua puluh enam, adalah "
  "dua koma delapan delapan persen.")
I("Dari mana angka itu", "indeks harga konsumen",
  "Angka itu datang dari indeks harga konsumen, yang naik dari seratus "
  "delapan koma enam nol menjadi seratus sebelas koma tujuh tiga dalam "
  "setahun.")
I("Ada juga inflasi inti", "dua koma tujuh enam persen",
  "Ada juga inflasi inti, yang membuang komponen paling bergejolak. "
  "Angkanya dua koma tujuh enam persen.")
I("Kenapa dua angka", "satu lebih stabil",
  "Dua angka itu ada karena yang satu lebih stabil dari yang lain. Untuk "
  "keputusan jangka panjang, yang inti biasanya lebih berguna.")
I("Satu peringatan soal angka ini", "inflasimu bisa beda",
  "Satu peringatan yang jujur. Angka inflasi itu rata-rata nasional atas "
  "keranjang belanja tertentu. Kalau pengeluaranmu berat di komponen yang "
  "naik lebih cepat, inflasi yang kamu rasakan lebih tinggi.")
I("Apa artinya buat simpanan", "titik impas",
  "Buat uang yang mengendap, artinya begini. Ada satu titik impas, dan di "
  "bawah titik itu kamu mundur meski saldomu naik.")
I("Titik impasnya", "bunga bersih sama dengan inflasi",
  "Titik impasnya adalah saat bunga bersihmu persis sama dengan inflasi. Di "
  "situ dayamu beli tidak bertambah sama sekali.")
I("Perhatikan katanya", "bunga BERSIH",
  "Perhatikan kata bersih di kalimat tadi. Titik impasnya diukur setelah "
  "pajak, bukan sebelum.")
I("Itu yang bikin kaget", "syaratnya lebih tinggi dari dugaan",
  "Dan itu yang biasanya mengagetkan orang. Bunga bruto yang dibutuhkan untuk "
  "sekadar impas lebih tinggi dari angka inflasi itu sendiri.")
I("Dan ia bekerja tiap tahun", "ke arah yang berlawanan",
  "Inflasi juga bekerja seperti bunga majemuk, hanya ke arah yang "
  "berlawanan. Ia menggerus dasar yang sudah tergerus tahun sebelumnya.")
T("Dua potongan sudah jelas", "mari hitung penuh",
  "Kita sudah punya kedua potongan dan kedua angkanya. Berapa hasilnya kalau "
  "dijalankan sampai habis?")

# ------------------------------------------------------------------ cap 5
T("Sepuluh juta rupiah", "satu tahun",
  "Ambil satu angka yang mudah dibayangkan. Sepuluh juta rupiah, disimpan "
  "satu tahun penuh.",
  cap="Hitungan penuh sepuluh juta")
I("Satu premis dulu", "saya asumsikan bunganya",
  "Satu premis yang saya sebut terus terang. Tarif deposito berbeda tiap bank "
  "dan tiap tenor, jadi angka bunga di sini adalah asumsi, bukan kutipan.")
I("Asumsinya", "lima koma lima persen",
  "Anggap saja depositomu memberi lima koma lima persen setahun. Kamu bisa "
  "mengganti angka ini dengan tarif bankmu sendiri.")
I("Bunga brutonya", "lima ratus lima puluh ribu",
  "Bunga bruto setahun jadi lima ratus lima puluh ribu rupiah. Ini angka yang "
  "muncul di brosur.")
I("Pajaknya", "seratus sepuluh ribu",
  "Pajak dua puluh persen atas jumlah itu adalah seratus sepuluh ribu rupiah.")
I("Bunga bersihnya", "empat ratus empat puluh ribu",
  "Yang benar-benar masuk ke rekeningmu adalah empat ratus empat puluh ribu "
  "rupiah. Itu setara empat koma empat persen.")
I("Sekarang inflasi", "dua ratus delapan puluh delapan ribu",
  "Sekarang inflasi. Dengan dua koma delapan delapan persen, daya beli "
  "sepuluh juta rupiahmu berkurang setara dua ratus delapan puluh delapan "
  "ribu rupiah.")
B("Dari bunga brosur ke sisa nyata", ["Bruto", "Bersih", "Nyata"],
  [100, 80, 28],
  "Sisa nyatanya seratus lima puluh dua ribu rupiah. Dari lima ratus lima "
  "puluh ribu yang dijanjikan.")
I("Dalam persen", "sekitar satu setengah",
  "Dalam persentase, keuntungan nyatamu sekitar satu koma lima persen "
  "setahun. Bukan lima koma lima.")
I("Perhatikan proporsinya", "yang tersisa kurang dari sepertiga",
  "Perhatikan proporsinya, karena di situ kejutannya. Yang tersisa kurang "
  "dari sepertiga angka yang dipasang di brosur.")
I("Dan ini kasus normal", "bukan skenario buruk",
  "Dan ini bukan skenario buruk. Ini hitungan dengan angka resmi hari ini, "
  "pada asumsi bunga yang wajar.")
I("Cara memakai hitungan ini", "ganti satu angka",
  "Cara memakai hitungan ini gampang. Ganti satu angka saja, yaitu tarif "
  "bankmu, dan seluruh urutannya tetap berlaku persis sama.")
I("Kalau bunganya lebih rendah", "titik impas mendekat",
  "Kalau bunga bankmu lebih rendah dari asumsi tadi, sisa nyatanya mengecil "
  "cepat. Di bawah kira-kira tiga koma enam persen bruto, kamu berhenti maju.")
T("Angkanya sudah jelas", "lalu deposito untuk apa?",
  "Kalau sisanya setipis itu, buat apa deposito ada?")

# ------------------------------------------------------------------ cap 6
T("Deposito punya tugas", "bukan tumbuh",
  "Deposito bukan alat untuk menumbuhkan kekayaan, dan memang tidak pernah "
  "dirancang untuk itu.",
  cap="Kapan deposito tetap masuk akal")
I("Tugasnya", "menjaga, bukan menambah",
  "Tugasnya menjaga nilai dan memastikan uangnya ada saat dibutuhkan. Itu "
  "pekerjaan yang berbeda dari menumbuhkan.")
I("Kasus pertama", "dana darurat",
  "Kasus pertama yang jelas adalah dana darurat. Uang yang harus ada persis "
  "saat keadaan memburuk.")
I("Kenapa cocok", "nilainya tidak berayun",
  "Cocok karena nilainya tidak berayun. Dana darurat yang turun tiga puluh "
  "persen justru gagal tepat saat kamu memerlukannya.")
I("Kasus kedua", "tujuan dekat",
  "Kasus kedua adalah uang untuk tujuan yang dekat. Biaya yang sudah pasti "
  "keluar dalam satu atau dua tahun.")
I("Kenapa cocok", "waktunya terlalu pendek",
  "Untuk jangka sependek itu, instrumen yang bisa turun bukan pilihan. "
  "Waktunya tidak cukup untuk pulih.")
I("Kasus ketiga", "menunggu keputusan",
  "Kasus ketiga adalah uang yang sedang menunggu. Kamu belum memutuskan mau "
  "diapakan, dan tidak mau ia menganggur begitu saja.")
I("Di ketiga kasus itu", "satu setengah persen cukup",
  "Di ketiga kasus itu, keuntungan nyata satu setengah persen sudah "
  "memadai. Kamu memang tidak sedang membayar untuk pertumbuhan.")
I("Ada juga sisi biaya", "uang terkunci",
  "Ada sisi lain yang perlu disebut. Uang di deposito terkunci sampai "
  "jatuh tempo, dan itu punya harga tersendiri saat peluang lain muncul.")
I("Yang tidak cocok", "dana pensiun puluhan tahun",
  "Yang tidak cocok adalah menaruh dana pensiun puluhan tahun di sana. "
  "Selisih kecil tiap tahun jadi jurang besar dalam tiga puluh tahun.")
I("Jadi pertanyaannya bukan", "bagus atau jelek",
  "Jadi pertanyaan yang benar bukan apakah deposito bagus atau jelek. "
  "Pertanyaannya adalah untuk pekerjaan yang mana.")
T("Sudah jelas tugasnya", "apa yang sering salah?",
  "Tugasnya sudah jelas. Kesalahan apa yang paling sering terjadi di "
  "sekitarnya?")

# ------------------------------------------------------------------ cap 7
T("Empat kesalahan", "yang paling mahal",
  "Kesalahan pertama adalah membandingkan bunga bruto deposito dengan imbal "
  "hasil bersih instrumen lain.",
  cap="Empat kesalahan")
I("Kenapa mahal", "menang di atas kertas saja",
  "Mahal karena deposito jadi terlihat menang di atas kertas, padahal "
  "perbandingannya tidak setara sejak awal.")
I("Kesalahan kedua", "lupa inflasi",
  "Kedua, melihat saldo naik dan menyimpulkan bahwa kamu maju. Saldo naik "
  "dan daya beli turun bisa terjadi bersamaan.")
I("Kesalahan ketiga", "menaruh dana jangka panjang",
  "Ketiga, memakai deposito untuk uang yang tidak akan disentuh belasan "
  "tahun. Itu memakai alat yang salah untuk pekerjaan yang salah.")
I("Kesalahan keempat", "mengejar tenor terpanjang",
  "Keempat, mengunci tenor terpanjang demi bunga sedikit lebih tinggi, lalu "
  "membutuhkan uangnya di tengah jalan.")
I("Kenapa itu mahal", "penalti memakan selisihnya",
  "Penalti pencairan sebelum jatuh tempo biasanya memakan lebih dari selisih "
  "bunga yang kamu kejar.")
I("Yang bisa kamu lakukan", "hitung bersihmu sendiri",
  "Yang bisa kamu lakukan hari ini gratis. Ambil tarif bankmu, kurangi dua "
  "puluh persen, lalu kurangi inflasi.")
I("Angka itu namanya", "keuntungan nyata",
  "Angka yang keluar dari situ adalah keuntungan nyatamu. Itu satu-satunya "
  "angka yang layak dibandingkan dengan apa pun.")
I("Lalu tanyakan", "untuk pekerjaan apa",
  "Lalu tanyakan untuk pekerjaan apa uang ini ada. Kalau jawabannya menjaga, "
  "deposito masuk akal walau angkanya tipis.")
I("Satu catatan jujur", "angka berubah",
  "Satu catatan jujur untuk menutup. Suku bunga acuan dan inflasi berubah "
  "tiap bulan, jadi hitungan ini perlu diulang, bukan dihafal.")
I("Yang tidak berubah", "urutan potongannya",
  "Yang tidak berubah adalah urutannya. Bruto, lalu pajak, lalu inflasi. "
  "Urutan itu tetap sama berapa pun angkanya.")
I("Kenapa urutannya penting", "pajak dulu, baru inflasi",
  "Urutan itu penting karena banyak orang mengurangi inflasi dari bunga "
  "bruto dan berhenti di situ. Pajaknya harus keluar lebih dulu, dan "
  "hasilnya berbeda.")
L("Ringkasan", ["Bunga brosur selalu bruto",
                "Pajak dua puluh persen, final",
                "Bebas bila saldo di bawah tujuh setengah juta",
                "Inflasi Juli dua koma delapan delapan persen",
                "Yang dibandingkan: keuntungan nyata"],
  "Lima hal untuk diingat. Bunga brosur selalu bruto. Pajaknya dua puluh "
  "persen dan final. Ada pembebasan untuk saldo kecil. Inflasi terakhir dua "
  "koma delapan delapan persen. Dan yang dibandingkan selalu keuntungan nyata.")
I("Kalau cuma satu hal", "hitung yang nyata",
  "Kalau dari video ini kamu melakukan satu hal saja, hitung keuntungan "
  "nyata dari simpanan yang sudah kamu punya sekarang.")
I("Kenapa justru itu", "keputusan lain mengikuti",
  "Karena begitu angka itu ada di depanmu, semua keputusan berikutnya jadi "
  "jauh lebih mudah diambil.")
C("Setiap Level", "dengan angka dan sumber",
  "Sekian. Setiap Level, dengan angka dan sumbernya, bukan dengan kesan.")

SHORT = [
    {"layout": "titulo", "kicker": "Bunga deposito", "sub": "bukan yang kamu simpan",
     "nar": "Bunga yang dipasang bank di brosur bukan bunga yang tinggal di "
            "kantongmu.", "sem_cap": True},
    {"layout": "item", "kicker": "Potongan pertama", "preco": "pajak dua puluh persen",
     "nar": "Bunga deposito kena pajak final dua puluh persen. Dipotong "
            "otomatis di bank.", "sem_cap": True},
    {"layout": "item", "kicker": "Potongan kedua", "preco": "inflasi",
     "nar": "Lalu inflasi tahunan, yang per Juli tercatat dua koma delapan "
            "delapan persen.", "sem_cap": True},
    {"layout": "item", "kicker": "Contohnya", "preco": "lima ratus lima puluh ribu",
     "nar": "Dari lima ratus lima puluh ribu rupiah bunga setahun, yang benar "
            "benar tersisa sekitar seratus lima puluh dua ribu.", "sem_cap": True},
    {"layout": "item", "kicker": "Artinya", "preco": "kurang dari sepertiga",
     "nar": "Kurang dari sepertiga angka yang dijanjikan di brosur.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Hitungannya", "sub": "di video lengkap",
     "nar": "Hitungan penuhnya ada di video lengkap.", "sem_cap": True},
]

COPY = """# Bunga deposito 2026: berapa yang benar-benar kamu simpan

## JUDUL
Bunga Deposito 2026: Berapa yang Benar-Benar Kamu Simpan Setelah Pajak dan Inflasi

## DESKRIPSI
Bank memasang satu angka di brosur deposito, dan yang tinggal di kantongmu adalah angka lain. Ini bukan tipuan dan tidak ada yang disembunyikan — cuma ada dua potongan yang tidak muncul di halaman depan: pajak atas bunga, yang dipotong otomatis sebelum uangnya sampai ke rekeningmu, dan inflasi, yang tidak muncul di mutasi rekening sama sekali tapi menentukan apakah kamu benar-benar maju.

Konteksnya hari ini. Bank Indonesia menahan BI Rate di 5,75% pada Rapat Dewan Gubernur 18–19 Agustus 2026, bulan ketiga berturut-turut tanpa perubahan; suku bunga Deposit Facility 4,75% dan Lending Facility 6,50%. Sementara itu Badan Pusat Statistik mencatat inflasi tahunan Juli 2026 sebesar 2,88%, dengan inflasi inti 2,76%, seiring naiknya Indeks Harga Konsumen dari 108,60 menjadi 111,73 dalam setahun.

Pajaknya diatur di PP 131 Tahun 2000: bunga deposito dan tabungan dikenakan PPh sebesar 20% dari jumlah bruto, dan sifatnya final — tidak digabungkan lagi dengan penghasilan lain di laporan tahunan. Ada pengecualian yang jarang disebut: bila saldonya tidak melebihi Rp7.500.000, bunganya tidak dipotong. Perhatikan bahwa batas itu soal saldo, bukan soal besar bunganya.

Di video ini kita jalankan hitungannya sampai habis atas Rp10 juta selama setahun. Tarif deposito berbeda tiap bank dan tiap tenor, jadi angka bunganya kami sebut terus terang sebagai asumsi, bukan kutipan — kamu bisa menggantinya dengan tarif bankmu sendiri. Dari bunga bruto, dikurangi pajak, lalu dikurangi inflasi, yang tersisa ternyata kurang dari sepertiga angka yang dipasang di brosur.

Lalu bagian yang lebih penting: kapan deposito tetap pilihan yang benar. Ada tiga pekerjaan yang memang cocok untuknya — dana darurat, tujuan yang tinggal satu atau dua tahun lagi, dan uang yang sedang menunggu keputusan. Untuk ketiganya, keuntungan nyata yang tipis sudah memadai, karena kamu memang tidak sedang membayar untuk pertumbuhan. Kita tutup dengan empat kesalahan yang paling sering terjadi dan satu langkah gratis yang bisa kamu lakukan hari ini.

Catatan: suku bunga acuan dan inflasi berubah tiap bulan, jadi hitungan ini perlu diulang, bukan dihafal. Materi edukasi; bukan ajakan membeli atau menjual produk apa pun, dan tidak menyebut bank mana pun.

## BAB
{CAPITULOS}

## KOMENTAR
Satu pertanyaan, karena jawabannya sering mengejutkan: kamu tahu berapa tarif bunga deposito atau tabunganmu sekarang, tanpa mengeceknya dulu? Tidak perlu menyebut nominal atau nama bank — cukup jawab tahu atau tidak. Saya kumpulkan jawabannya untuk materi berikutnya. Kalau kamu ingin hitungan yang sama dibuat untuk reksadana pasar uang, tulis saja di kolom komentar.

## HASHTAG
#Deposito #KeuanganPribadi #SetiapLevel

## TAG
deposito, bunga deposito, pajak bunga deposito, pph final, bi rate, inflasi 2026, bps, keuntungan nyata, dana darurat, tabungan, investasi pemula, reksadana pasar uang, keuangan pribadi, indonesia, setiap level

## PENGATURAN STUDIO
- Bahasa: Indonesia (id) | Kategori: Edukasi (27)
- Tidak dibuat untuk anak-anak
- Deklarasi konten sintetis: YA (suara AI)
- Lokasi: Indonesia | Lisensi: lisensi YouTube standar
- Iklan mid-roll: aktif (di atas 8 menit)

## MUSIK / LISENSI
{TRILHA}

## SUMBER
Suku bunga acuan: Bank Indonesia menahan BI Rate di 5,75% pada Rapat Dewan Gubernur 18–19 Agustus 2026 — bulan ketiga berturut-turut — dengan Deposit Facility 4,75% dan Lending Facility 6,50%; dilaporkan secara konsisten oleh Kompas, CNN Indonesia, CNBC Indonesia, Republika, Antara dan Sindonews, semuanya mengutip Bank Indonesia (akses 19 Agustus 2026). Inflasi: Badan Pusat Statistik mencatat inflasi tahunan Juli 2026 sebesar 2,88% dan inflasi inti 2,76%, dengan Indeks Harga Konsumen naik dari 108,60 (Juli 2025) menjadi 111,73 (Juli 2026); dilaporkan secara konsisten oleh Beritasatu, Jawapos, Kompas, Republika dan Aspek. Pajak: PPh atas bunga deposito dan tabungan sebesar 20% dari jumlah bruto dan bersifat final, serta pembebasan bila saldo tidak melebihi Rp7.500.000, diatur dalam Peraturan Pemerintah Nomor 131 Tahun 2000 yang berlaku sejak 1 Januari 2001; sebagaimana diuraikan oleh Ortax dan tax-guide Pajakku, yang sama isinya. Tarif bunga deposito yang dipakai dalam simulasi adalah ASUMSI yang disebut terus terang di dalam video, bukan kutipan dari bank mana pun, karena tarif berbeda antarbank dan antartenor; hitungan turunannya (bunga bruto, potongan pajak, bunga bersih, dan sisa setelah inflasi) adalah aritmetika langsung atas asumsi tersebut dan atas angka resmi di atas. Tingkat bunga penjaminan LPS sengaja TIDAK disebutkan karena tidak ditemukan dua sumber bertanggal yang bersesuaian untuk Agustus 2026. Materi edukasi; bukan nasihat investasi, bukan rekomendasi produk, dan tidak menyebut bank mana pun.
"""

SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-009",
    "idioma": "id",
    "voz": "id-ID-ArdiNeural",
    "trilha": "Wholesome",  # identidade do canal, conferida pelo portao
    "paleta": {"ink": "#14213D", "c1": "#E5A200", "c2": "#00897B", "bg": "#F7F3E8"},
    "thumb": {"l1": "BUNGA 5,5%", "l2": "sisanya 1,5%"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/setiap-level-009.json"
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
