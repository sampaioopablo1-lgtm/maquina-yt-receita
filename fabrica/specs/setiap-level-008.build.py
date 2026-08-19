#!/usr/bin/env python3
"""Monta a spec setiap-level-008 — o mesmo saldo, dois impostos.

PAUTA, medida em 19/08/2026. Tres eixos nesta rodada:

    BPJS Ketenagakerjaan / JHT      mediana 126,7 v/d   (n=20)
    KPR / rumah pertama             mediana  14,3       (n=16)  <- limpo
    pajak PPh 21                    mediana   3,1       (n=19)  <- MORTO

O 14,3 do KPR e a mediana DEPOIS de tirar os quatro ruidos de busca; com eles
dentro dava 16,1 em n=19. Tirar ruido baixou a mediana, nao subiu: o ruido
estava em cima.

O eixo de KPR merece nota: os dois topos aparentes (6490,0 e 3141,7 v/d) sao
RUIDO DE BUSCA — um video em ingles do Evan Carmichael e uma novela chinesa
legendada. Descartados, o eixo inteiro de KPR indonesio cabe abaixo de 32
v/d. Outlier que nao e do eixo nao e outlier: e falha da consulta.

O eixo de pajak PPh 21 esta 41 vezes abaixo do escolhido e fica gravado como
medido-e-morto.

Outliers do eixo escolhido (>= 380,2):

    Cara Mencairkan JHT Lewat JMO Terbaru 2026        1043,7 v/d
    Cara Mencairkan BPJS Ketenagakerjaan Online        768,3
    Cara Cairkan Saldo BPJS Ketenagakerjaan Online     696,5
    Tanpa Perlu Resign, Ini Cara Mudah Klaim JHT       526,0

Os tres primeiros sao TUTORIAL de aplicativo, que nao e o que este canal faz.
Modelo a ESTRUTURA do quarto — "sem fazer o que voce supoe obrigatorio, eis o
resultado" — e a do vizinho de 210,8 ("Kena PHK? JHT Tak Bisa Langsung
Dicairkan, Ini Aturannya"), que e "voce supoe X, a regra diz Y".

NUMEROS VERIFICADOS (fontes que batem entre si; acesso 19/08/2026):

  Ortax (18/04/2025) e DDTCNews (30/06/2026), ambos citando PP 68/2009 e
  PMK 16/PMK.03/2010:
    PPh 21 FINAL sobre JHT pago sekaligus:
        0%  ate Rp50.000.000
        5%  acima de Rp50.000.000
    "sekaligus" = pagamento parcial OU total dentro de no maximo DOIS ANOS
    CALENDARIO. Citacao literal do Ortax: "pembayaran sebagian atau seluruh
    manfaat dilakukan dalam jangka waktu paling lama 2 tahun kalender".
    Passado esse prazo: "manfaat JHT dikenakan PPh Pasal 21 tidak final
    dengan tarif progresif sesuai Pasal 17 UU PPh".
    E a linha que e a espinha deste video: "PPh Pasal 21 tidak final juga
    berlaku untuk manfaat JHT yang diambil lebih dari 2 tahun setelah peserta
    mengambil JHT sebagian (10% atau 30%)."

  PP 46/2015: JHT pago integralmente aos 56 anos, por morte ou invalidez
  total permanente; com 10 anos de filiacao pode-se sacar 10% ou 30%.

  Tarifas do Pasal 17 pos UU HPP (pajakku, online-pajak, binus — concordam):
        5%   ate Rp60.000.000
        15%  Rp60.000.000 a Rp250.000.000
        25%  Rp250.000.000 a Rp500.000.000
        30%  Rp500.000.000 a Rp5.000.000.000
        35%  acima de Rp5.000.000.000

  Kemenkeu/DJP, janeiro a maio de 2026 (Tirto, Liputan6, RRI, DDTCNews, IKPI
  — todos com os mesmos numeros): 1.720.000 pedidos de saque; 1.640.000
  (95,45%) a 0%; 78.441 pedidos atingiram os 5%. O ministro Purbaya estuda
  rever a regra; centrais sindicais pedem 0% para todo valor.

A CONTA LADO A LADO (aritmetica minha sobre as tarifas acima, mesmo saldo de
Rp300.000.000 — o exemplo do proprio Ortax):
    sekaligus:  0% x 50jt + 5% x 250jt              = Rp12.500.000
    progressivo: 5% x 60jt + 15% x 190jt + 25% x 50jt = Rp44.000.000
    razao 3,52x — e o progressivo AINDA se soma aos outros rendimentos,
    porque deixou de ser final. Por isso o roteiro diz "no minimo".

O QUE NAO ENTRA: nenhuma promessa de economia, nenhuma instrucao para adiar
ou antecipar saque. O video descreve o mecanismo e manda conferir a data do
primeiro saque. Regra sob revisao entra como ressalva, nao como previsao.

SIMILARIDADE vs os dez longos do canal: nenhum toca BPJS, JHT ou saque de
fundo. O mais proximo e "Kena PHK 2026: Berapa Lama Pesangon Bertahan", que
trata de PESANGON — outro instrumento, outra pergunta, outro pagador.

TRILHA: Wholesome, a identidade do canal (config/canais/setiap-level.yaml).

DIMENSIONAMENTO. id-ID-ArdiNeural = 18,72 chars/s + 1,079 s/frase.
Alvo no MEIO da janela: ~13,2 min. Entregue: 10.597 chars em 90 cenas.
A voz indonesia e rapida e pausa pouco, entao o mesmo relogio pede MAIS
texto que o polones — 10.597 contra 9.804 chars para os mesmos 13,2 min.
Foi isso que empurrou o roteiro para 99 cenas antes de eu juntar as cenas
irmas de volta para 90, dentro da janela de 70 a 90.
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
T("Saldo sama", "pajak beda",
  "Dua orang keluar dari perusahaan di bulan yang sama. Saldo Jaminan Hari "
  "Tua mereka sama persis.",
  cap="Saldo sama, pajak beda")
I("Tapi yang diterima", "tidak sama",
  "Yang satu membayar pajak dua belas juta lima ratus ribu rupiah. Yang lain "
  "membayar empat puluh empat juta rupiah.")
I("Bukan salah hitung", "begitulah aturannya",
  "Ini bukan salah hitung kantor pajak. Ini memang hasil dari aturan yang "
  "berlaku sekarang.")
I("Yang membedakan", "satu tanggal",
  "Yang membedakan bukan besar saldo. Yang membedakan adalah satu tanggal di "
  "masa lalu yang hampir tidak ada yang mencatat.")
I("Kenapa ini penting", "kamu merencanakan dari angka kotor",
  "Masalahnya praktis. Kalau kamu merencanakan hidup setelah resign dari "
  "angka saldo di aplikasi, kamu merencanakan dari angka yang belum dipotong.")
I("Kabar baiknya dulu", "sebagian besar bebas",
  "Kabar baiknya perlu disebut lebih dulu. Sebagian besar peserta tidak "
  "membayar apa pun.")
I("Angka resminya", "satu juta enam ratus empat puluh ribu",
  "Dari Januari sampai Mei dua ribu dua puluh enam, ada satu juta tujuh ratus "
  "dua puluh ribu klaim. Sebanyak satu juta enam ratus empat puluh ribu di "
  "antaranya kena tarif nol persen.")
I("Yang kena tarif", "tujuh puluh delapan ribu",
  "Hanya tujuh puluh delapan ribu empat ratus empat puluh satu klaim yang "
  "kena tarif lima persen. Itu angka Kementerian Keuangan.")
I("Jadi kenapa dibahas", "karena yang kena, kena keras",
  "Jadi kenapa ini dibahas? Karena yang jatuh di sisi lain aturan bisa "
  "membayar berkali lipat, dan biasanya baru tahu saat uang sudah masuk.")
I("Berapa besar taruhannya", "puluhan juta rupiah",
  "Selisih antara dua skenario itu bisa puluhan juta rupiah. Itu bukan "
  "detail administratif, itu beberapa bulan biaya hidup.")
L("Yang akan kita bahas", ["Kapan JHT boleh dicairkan",
                           "Tarif final: nol dan lima persen",
                           "Jam dua tahun yang mengubah semuanya",
                           "Kalau lewat: tarif progresif",
                           "Hitungan berdampingan"],
  "Lima bagian. Kapan JHT boleh cair. Berapa tarif finalnya. Apa itu jam dua "
  "tahun. Apa yang terjadi kalau lewat. Dan hitungannya berdampingan.")
I("Satu hal dulu", "ini bukan nasihat pajak",
  "Satu hal dulu. Ini bukan nasihat pajak dan bukan ajakan mempercepat atau "
  "menunda pencairan. Kita membahas mekanisme.")
I("Aturan kanal", "angka dengan sumber",
  "Dan aturan kanal tetap berlaku. Angka dengan sumber dan tanggal. Yang "
  "tidak bisa diukur, tidak kita ucapkan.")
T("Kita mulai", "kapan JHT boleh cair?",
  "Kita mulai dari yang paling dasar, karena dari sini semuanya mengalir. "
  "Kapan JHT sebenarnya boleh dicairkan?")

# ------------------------------------------------------------------ cap 2
T("Tiga keadaan", "untuk manfaat penuh",
  "Menurut Peraturan Pemerintah nomor empat puluh enam tahun dua ribu lima "
  "belas, manfaat penuh dibayar dalam tiga keadaan.",
  cap="Kapan JHT boleh dicairkan")
I("Pertama", "usia lima puluh enam",
  "Pertama, saat peserta mencapai usia lima puluh enam tahun.")
I("Kedua dan ketiga", "meninggal atau cacat total",
  "Kedua, saat peserta meninggal dunia. Ketiga, saat mengalami cacat total "
  "tetap.")
I("Dalam tiga keadaan itu", "dibayar sekaligus",
  "Dalam ketiga keadaan itu manfaat dibayarkan sekaligus. Ini jalur yang "
  "paling sederhana secara pajak.")
I("Tapi ada jalur lain", "sepuluh tahun kepesertaan",
  "Tapi ada jalur lain yang jauh lebih sering dipakai. Peserta dengan masa "
  "kepesertaan paling singkat sepuluh tahun boleh mengambil sebagian.")
I("Berapa yang boleh", "sepuluh atau tiga puluh persen",
  "Yang boleh diambil adalah sepuluh persen untuk keperluan lain, atau tiga "
  "puluh persen untuk kepemilikan rumah.")
I("Kapan orang memakainya", "renovasi, sekolah, usaha",
  "Jalur ini biasanya dipakai untuk renovasi rumah, biaya sekolah anak, "
  "atau modal usaha kecil. Semuanya alasan yang masuk akal.")
I("Terdengar aman", "uangnya memang milikmu",
  "Terdengar aman, dan memang uangnya milikmu. Banyak orang mengambilnya "
  "tanpa berpikir dua kali.")
I("Di sinilah jamnya mulai", "tanggal itu dicatat",
  "Tapi di sinilah jam yang tadi saya sebut mulai berjalan. Tanggal "
  "pengambilan sebagian itu dicatat, dan nanti dipakai.")
I("Sebelum ke sana", "kita perlu tarifnya",
  "Sebelum sampai ke akibatnya, kita perlu tahu tarifnya dulu. Tanpa itu "
  "perbedaannya tidak kelihatan.")
I("Catat satu hal", "tanggal, bukan jumlah",
  "Kalau kamu hanya mencatat satu hal dari bagian ini, catat "
  "tanggalnya. Bukan jumlah yang kamu ambil.")
T("Sudah jelas", "sekarang tarifnya",
  "Kita sudah tahu kapan JHT bisa cair. Berapa pajaknya kalau cair?")

# ------------------------------------------------------------------ cap 3
T("Dua tarif", "nol dan lima",
  "Dasarnya ada di Peraturan Pemerintah nomor enam puluh delapan tahun dua "
  "ribu sembilan, dan di aturan menteri keuangan turunannya.",
  cap="Tarif final: nol dan lima persen")
I("Tarif pertama", "nol persen",
  "Tarif pertama adalah nol persen. Itu berlaku atas penghasilan bruto "
  "sampai dengan lima puluh juta rupiah.")
I("Tarif kedua", "lima persen",
  "Tarif kedua adalah lima persen. Itu berlaku atas bagian di atas lima "
  "puluh juta rupiah.")
I("Perhatikan katanya", "bagian di atas",
  "Perhatikan kata bagiannya. Yang kena lima persen bukan seluruh saldo, "
  "hanya kelebihan di atas batas tadi.")
I("Contoh cepat", "saldo delapan puluh juta",
  "Contohnya, dengan saldo delapan puluh juta rupiah, yang kena lima persen "
  "hanya tiga puluh juta rupiah. Sisanya nol.")
I("Siapa yang memotong", "dipotong di sumber",
  "Pajaknya tidak perlu kamu setor sendiri. Pemotongan dilakukan "
  "langsung saat manfaat dibayarkan, jadi yang masuk rekening sudah bersih.")
I("Dan pajaknya", "final",
  "Yang lebih penting, pajak ini bersifat final. Final artinya selesai di "
  "situ.")
I("Apa untungnya final", "tidak digabung",
  "Untungnya nyata. Penghasilan itu tidak digabungkan dengan gaji atau "
  "penghasilan lain di surat pemberitahuan tahunanmu.")
I("Bandingkan dengan gaji", "gaji digabung, ini tidak",
  "Bandingkan dengan gaji bulanan, yang digabung dan bisa mendorongmu ke "
  "lapisan tarif lebih tinggi. Penghasilan final tidak melakukan itu.")
I("Karena itu sebagian besar", "membayar nol",
  "Karena batasnya lima puluh juta rupiah, sebagian besar peserta memang "
  "membayar nol. Itu yang terlihat di angka Kementerian Keuangan tadi.")
I("Satu salah paham", "kena PHK bukan progresif",
  "Ada satu salah paham yang perlu diluruskan. Pencairan karena pemutusan "
  "hubungan kerja tetap masuk tarif final ini, bukan tarif progresif.")
I("Itu ditegaskan", "oleh otoritas pajak",
  "Itu ditegaskan langsung oleh otoritas pajak pada pertengahan tahun ini, "
  "setelah ramai anggapan sebaliknya.")
T("Kalau begitu", "kok bisa beda tiga kali lipat?",
  "Kalau tarifnya seringan itu, bagaimana ceritanya ada yang membayar tiga "
  "kali lipat lebih banyak?")

# ------------------------------------------------------------------ cap 4
T("Jam dua tahun", "definisi sekaligus",
  "Jawabannya ada pada satu definisi yang jarang dibaca. Definisi kata "
  "sekaligus.",
  cap="Jam dua tahun")
I("Yang kamu kira", "sekali transfer",
  "Kita cenderung mengira sekaligus berarti satu kali transfer, semuanya "
  "sekarang.")
I("Yang tertulis", "dua tahun kalender",
  "Yang tertulis lain. Sekaligus berarti pembayaran sebagian atau seluruh "
  "manfaat dalam jangka waktu paling lama dua tahun kalender.")
I("Baca ulang", "sebagian juga masuk",
  "Bacalah bagian sebagiannya sekali lagi. Pengambilan sepuluh atau tiga "
  "puluh persen tadi juga masuk hitungan itu.")
I("Artinya", "jam mulai di saku pertama",
  "Artinya jam dua tahun mulai berjalan sejak pembayaran pertama. Bukan "
  "sejak kamu berhenti bekerja.")
I("Kenapa ada batas waktu", "supaya tidak dipecah",
  "Batas waktu itu ada supaya satu manfaat tidak dipecah menjadi banyak "
  "potongan kecil demi mengejar tarif nol berkali-kali.")
I("Yang di dalam jam", "tetap final",
  "Semua yang dibayarkan di dalam jendela dua tahun itu tetap memakai tarif "
  "final yang tadi.")
I("Yang di luar", "berubah sifat",
  "Yang dibayarkan setelah jendela itu lewat berubah sifat sepenuhnya.")
I("Kalimat kuncinya", "lebih dari dua tahun",
  "Aturannya menyebut hal ini secara langsung: manfaat yang diambil lebih "
  "dari dua tahun setelah peserta mengambil sebagian, tidak lagi final.")
I("Jadi urutannya penting", "bukan hanya jumlahnya",
  "Jadi yang menentukan bukan hanya berapa yang kamu ambil. Yang menentukan "
  "juga kapan kamu mulai mengambil.")
I("Dan itu tidak diingatkan", "tidak ada notifikasi",
  "Dan tidak ada notifikasi yang mengingatkan. Tanggal itu ada di riwayat "
  "klaimmu, dan hanya kamu yang bisa membukanya.")
I("Yang membuatnya sunyi", "jaraknya bertahun-tahun",
  "Yang membuat aturan ini sunyi adalah jaraknya. Antara pengambilan "
  "pertama dan pencairan terakhir bisa lewat lima atau sepuluh tahun.")
T("Kita tahu jamnya", "apa yang terjadi kalau lewat?",
  "Kita sudah tahu jamnya. Apa persisnya yang terjadi kalau jendela itu "
  "lewat?")

# ------------------------------------------------------------------ cap 5
T("Tidak final lagi", "masuk tarif progresif",
  "Kalau lewat, manfaat JHT dikenakan pajak yang tidak final, dengan tarif "
  "progresif menurut pasal tujuh belas undang-undang pajak penghasilan.",
  cap="Kalau lewat: tarif progresif")
I("Progresif artinya", "berlapis",
  "Progresif artinya berlapis. Semakin besar jumlahnya, semakin tinggi tarif "
  "di lapisan atasnya.")
I("Lapisan pertama", "lima persen",
  "Lapisan pertama lima persen, sampai dengan enam puluh juta rupiah.")
I("Lapisan kedua", "lima belas persen",
  "Lapisan kedua lima belas persen, sampai dengan dua ratus lima puluh juta "
  "rupiah.")
I("Lapisan ketiga", "dua puluh lima persen",
  "Lapisan ketiga dua puluh lima persen, sampai dengan lima ratus juta "
  "rupiah.")
I("Dua lapisan teratas", "tiga puluh dan tiga puluh lima",
  "Lalu tiga puluh persen sampai lima miliar rupiah, dan tiga puluh lima "
  "persen di atasnya.")
I("Sama seperti tadi", "berlaku per bagian",
  "Sama seperti tarif final, lapisan ini berlaku per bagian. Bukan satu "
  "tarif tunggal atas seluruh jumlah.")
I("Bandingkan sekarang", "lima persen jadi lima belas",
  "Bandingkan dengan tarif final tadi. Bagian yang sebelumnya kena lima "
  "persen kini bisa masuk lapisan lima belas atau dua puluh lima persen.")
I("Tapi ada yang lebih berat", "kata tidak final",
  "Ada satu hal yang lebih berat dari tarifnya sendiri, dan itu tersembunyi "
  "di kata tidak final.")
I("Tidak final berarti", "digabung",
  "Tidak final berarti penghasilan itu digabungkan dengan penghasilanmu yang "
  "lain di tahun yang sama.")
I("Kalau kamu masih bekerja", "menumpuk di atas gaji",
  "Kalau saat itu kamu sudah bekerja lagi, jumlah ini menumpuk di atas "
  "gajimu. Ia masuk dari lapisan tempat gajimu berhenti, bukan dari nol.")
I("Ada konsekuensi lain", "masuk laporan tahunan",
  "Ada konsekuensi administratif juga. Penghasilan yang tidak final ikut "
  "masuk perhitungan surat pemberitahuan tahunanmu.")
I("Karena itu", "hitungan kita konservatif",
  "Karena itu hitungan yang akan saya tunjukkan sebentar lagi adalah batas "
  "bawah. Kenyataannya bisa lebih tinggi.")
T("Teorinya cukup", "mari lihat angkanya",
  "Teorinya sudah cukup. Sekarang pertanyaan yang sebenarnya: atas saldo "
  "yang sama, berapa persisnya selisihnya?")

# ------------------------------------------------------------------ cap 6
T("Saldo yang sama", "tiga ratus juta",
  "Ambil satu saldo yang sama untuk keduanya: tiga ratus juta rupiah. Ini "
  "contoh yang dipakai juga oleh literatur pajak.",
  cap="Hitungan berdampingan")
I("Kenapa angka ini", "cukup besar untuk terlihat",
  "Saldo sebesar ini dipilih karena cukup besar untuk melewati batas "
  "lima puluh juta rupiah. Di bawah batas itu kedua skenario sama saja.")
I("Skenario pertama", "semua di dalam jendela",
  "Skenario pertama. Seluruhnya dicairkan di dalam jendela dua tahun, jadi "
  "tarif final berlaku.")
I("Bagian pertama", "nol",
  "Lima puluh juta rupiah pertama kena nol persen. Pajaknya nol.")
I("Bagian kedua", "lima persen",
  "Sisanya, dua ratus lima puluh juta rupiah, kena lima persen.")
I("Totalnya", "dua belas juta lima ratus ribu",
  "Totalnya dua belas juta lima ratus ribu rupiah. Itu sekitar empat persen "
  "dari saldo.")
I("Skenario kedua", "lewat jendela",
  "Skenario kedua. Orang ini mengambil sebagian lebih dari dua tahun "
  "sebelumnya, jadi sisanya jatuh ke tarif progresif.")
I("Lapisan pertama", "tiga juta",
  "Enam puluh juta rupiah pertama kena lima persen. Itu tiga juta rupiah.")
I("Lapisan kedua", "dua puluh delapan juta lima ratus ribu",
  "Lapisan berikutnya, seratus sembilan puluh juta rupiah, kena lima belas "
  "persen. Itu dua puluh delapan juta lima ratus ribu rupiah.")
I("Lapisan ketiga", "dua belas juta lima ratus ribu",
  "Sisa lima puluh juta rupiah kena dua puluh lima persen. Itu dua belas "
  "juta lima ratus ribu rupiah.")
B("Pajak atas saldo yang sama", ["Final", "Progresif"], [28, 100],
  "Jumlahnya empat puluh empat juta rupiah, atas saldo yang persis sama.")
I("Selisihnya", "tiga koma lima kali",
  "Selisihnya sekitar tiga koma lima kali lipat. Tiga puluh satu juta lima "
  "ratus ribu rupiah lebih banyak.")
I("Dalam persen", "empat persen lawan lima belas",
  "Dalam persentase, yang pertama membayar sekitar empat persen dari "
  "saldonya. Yang kedua membayar sekitar lima belas persen.")
I("Dan ingat", "ini masih batas bawah",
  "Dan ingat catatan tadi. Angka kedua masih batas bawah, karena belum "
  "ditumpuk di atas penghasilan lain.")
I("Apa yang membedakan", "bukan keputusan besar",
  "Yang membedakan keduanya bukan keputusan besar. Hanya satu pengambilan "
  "sebagian, bertahun-tahun sebelumnya.")
T("Angkanya jelas", "apa yang bisa salah?",
  "Angkanya sudah jelas. Sekarang, kesalahan apa yang paling sering "
  "terjadi?")

# ------------------------------------------------------------------ cap 7
T("Empat kesalahan", "yang paling mahal",
  "Kesalahan pertama adalah mengambil sepuluh atau tiga puluh persen tanpa "
  "mencatat tanggalnya.",
  cap="Empat kesalahan")
I("Kenapa mahal", "tanggal itu yang dipakai",
  "Mahal karena justru tanggal itulah yang nanti menentukan tarif atas sisa "
  "saldomu.")
I("Kesalahan kedua", "mengira PHK berarti progresif",
  "Kedua, mengira pencairan karena pemutusan hubungan kerja otomatis kena "
  "progresif. Itu keliru, dan sudah diluruskan otoritas pajak.")
I("Kesalahan ketiga", "merencanakan dari angka kotor",
  "Ketiga, menyusun rencana dari angka saldo di aplikasi. Angka itu belum "
  "dipotong apa pun.")
I("Kesalahan keempat", "menunggu tanpa tahu jamnya",
  "Keempat, menunda sisa pencairan tanpa tahu bahwa jendelanya sedang "
  "berjalan. Menunggu bisa memindahkanmu ke tarif yang lain.")
I("Satu hal yang tidak saya sarankan", "buru-buru mencairkan",
  "Satu hal yang tidak saya sarankan adalah buru-buru mencairkan hanya "
  "karena video ini. Uang yang keluar lebih awal juga punya biayanya.")
I("Yang bisa kamu lakukan", "buka riwayat klaim",
  "Yang bisa kamu lakukan hari ini cuma satu, dan gratis. Buka riwayat "
  "klaimmu dan cari tanggal pengambilan pertama.")
I("Kalau belum pernah", "jendelamu belum jalan",
  "Kalau kamu belum pernah mengambil sebagian, jendelamu belum berjalan sama "
  "sekali. Itu kabar baik dan perlu kamu ketahui.")
I("Kalau sudah pernah", "hitung dari tanggal itu",
  "Kalau sudah pernah, hitung dua tahun dari tanggal itu. Dari situ kamu "
  "tahu di sisi mana kamu berdiri.")
I("Simpan buktinya", "bukti potong",
  "Simpan juga bukti potong pajaknya. Itu dokumen yang kamu perlukan "
  "kalau nanti ada pertanyaan atas laporan tahunanmu.")
I("Dan tanyakan", "sebelum menandatangani",
  "Lalu tanyakan langsung ke petugas, sebelum menandatangani apa pun, tarif "
  "mana yang akan dipakai atas klaimmu.")
I("Satu ressalva jujur", "aturannya sedang ditinjau",
  "Satu catatan jujur untuk menutup. Aturan pajak atas JHT sedang ditinjau "
  "ulang oleh menteri keuangan.")
I("Apa yang diminta", "nol persen untuk semua",
  "Serikat pekerja meminta tarifnya menjadi nol persen untuk semua nilai. "
  "Sampai ada aturan baru, yang berlaku adalah yang kita bahas hari ini.")
L("Ringkasan", ["Tarif final: nol dan lima persen",
                "Batasnya lima puluh juta rupiah",
                "Sekaligus artinya dua tahun kalender",
                "Ambil sebagian memulai jamnya",
                "Lewat jendela: tarif progresif"],
  "Lima hal untuk diingat. Tarif finalnya nol dan lima persen. Batasnya lima "
  "puluh juta rupiah. Sekaligus berarti dua tahun kalender. Mengambil "
  "sebagian memulai jam itu. Dan lewat jendela, tarifnya progresif.")
I("Kalau cuma satu hal", "cari tanggalnya",
  "Kalau dari video ini kamu hanya melakukan satu hal, cari tanggal "
  "pengambilan pertamamu.")
I("Kenapa justru itu", "dari sana semuanya mengalir",
  "Karena dari tanggal itulah semua sisanya mengalir. Sisanya hanya "
  "aritmetika di sekitarnya.")
C("Setiap Level", "dengan angka dan sumber",
  "Sekian. Setiap Level, dengan angka dan sumbernya, bukan dengan kesan.")

# ------------------------------------------------------- juntar cenas irmas
# A janela de cenas e 70 a 90. Ao dimensionar para o meio da janela de tempo
# o roteiro chegou a 99 cenas, porque a voz indonesia e rapida (18,72 chars/s)
# e pede MAIS texto para o mesmo relogio. Em vez de cortar conteudo — que e o
# que sustenta os 13 minutos — junto cenas que ja eram um pensamento so.
# Nenhum caractere de narracao se perde: o texto e concatenado.
JUNTAR = [
    ("Pertama", "Kedua dan ketiga", "Tiga keadaan itu", "usia, meninggal, cacat"),
    ("Dan pajaknya", "Apa untungnya final", "Dan pajaknya final", "tidak digabung"),
    ("Yang kamu kira", "Yang tertulis", "Yang kamu kira", "dan yang tertulis"),
    ("Yang di luar", "Kalimat kuncinya", "Yang di luar", "berubah sifat"),
    ("Lapisan pertama", "Lapisan kedua", "Dua lapisan pertama", "lima dan lima belas"),
    ("Lapisan ketiga", "Dua lapisan teratas", "Lapisan sisanya", "dua puluh lima ke atas"),
    ("Bagian pertama", "Bagian kedua", "Dua bagiannya", "nol lalu lima persen"),
    ("Lapisan pertama", "Lapisan kedua", "Dua lapisan pertama", "tiga dan dua puluh delapan juta"),
    ("Kalau cuma satu hal", "Kenapa justru itu", "Kalau cuma satu hal", "cari tanggalnya"),
]
for ka, kb, novo_k, novo_p in JUNTAR:
    for i in range(len(CENAS) - 1):
        if CENAS[i].get("kicker") == ka and CENAS[i + 1].get("kicker") == kb:
            CENAS[i]["nar"] = CENAS[i]["nar"] + " " + CENAS[i + 1]["nar"]
            CENAS[i]["kicker"] = novo_k
            if "preco" in CENAS[i]:
                CENAS[i]["preco"] = novo_p
            del CENAS[i + 1]
            break
    else:
        raise SystemExit(f"par nao encontrado: {ka!r} + {kb!r}")

SHORT = [
    {"layout": "titulo", "kicker": "Saldo JHT sama", "sub": "pajak beda",
     "nar": "Dua orang, saldo Jaminan Hari Tua sama persis. Pajaknya beda "
            "tiga kali lipat.", "sem_cap": True},
    {"layout": "item", "kicker": "Kalau sekaligus", "preco": "nol dan lima persen",
     "nar": "Kalau cair di dalam jendela dua tahun, tarifnya final. Nol "
            "persen sampai lima puluh juta rupiah.", "sem_cap": True},
    {"layout": "item", "kicker": "Kalau lewat", "preco": "progresif",
     "nar": "Kalau lewat jendela itu, tarifnya jadi progresif dan digabung "
            "dengan penghasilan lain.", "sem_cap": True},
    {"layout": "item", "kicker": "Yang memulai jam", "preco": "ambil sebagian",
     "nar": "Dan yang memulai jamnya adalah pengambilan sepuluh atau tiga "
            "puluh persen bertahun-tahun lalu.", "sem_cap": True},
    {"layout": "item", "kicker": "Bedanya", "preco": "tiga koma lima kali",
     "nar": "Atas saldo tiga ratus juta rupiah, selisihnya tiga koma lima "
            "kali lipat.", "sem_cap": True},
    {"layout": "cta", "kicker": "Cek tanggalnya", "sub": "di video lengkap",
     "nar": "Cara mengeceknya ada di video lengkap.", "sem_cap": True},
]

COPY = """# Pencairan JHT 2026: saldo sama, pajak bisa beda tiga kali lipat

## JUDUL
Pencairan JHT: Saldo Sama Rp300 Juta, Pajak Rp12,5 Juta atau Rp44 Juta

## DESKRIPSI
Dua orang keluar dari perusahaan di bulan yang sama, dengan saldo Jaminan Hari Tua yang sama persis. Yang satu membayar pajak Rp12,5 juta, yang lain membayar Rp44 juta. Ini bukan salah hitung — ini hasil dari satu definisi yang jarang dibaca, dan dari satu tanggal di masa lalu yang hampir tidak ada yang mencatat.

Kabar baiknya perlu disebut lebih dulu: sebagian besar peserta tidak membayar apa pun. Dari 1,72 juta klaim JHT sepanjang Januari–Mei 2026, sebanyak 1,64 juta klaim kena tarif 0% karena nilainya tidak melebihi Rp50 juta. Hanya 78.441 klaim yang kena tarif 5%. Itu angka Kementerian Keuangan.

Tarif PPh Pasal 21 atas pencairan JHT yang dibayarkan sekaligus diatur di PP 68/2009 dan PMK 16/PMK.03/2010: 0% atas penghasilan bruto sampai dengan Rp50 juta, dan 5% atas bagian di atasnya. Sifatnya final — tidak digabungkan dengan penghasilan lain. Perlu diluruskan juga satu salah paham yang sempat ramai: pencairan karena PHK tetap masuk tarif final ini, bukan tarif progresif.

Persoalannya ada pada arti kata "sekaligus". Menurut aturannya, sekaligus berarti pembayaran sebagian atau seluruh manfaat dalam jangka waktu paling lama 2 tahun kalender. Artinya jam dua tahun itu mulai berjalan sejak pembayaran pertama — termasuk pengambilan sebagian 10% atau 30% yang boleh diambil setelah 10 tahun kepesertaan. Manfaat yang diambil lebih dari 2 tahun setelah pengambilan sebagian itu tidak lagi final, melainkan kena tarif progresif Pasal 17 UU PPh: 5% sampai Rp60 juta, 15% sampai Rp250 juta, 25% sampai Rp500 juta, 30% sampai Rp5 miliar, dan 35% di atasnya.

Di video ini kita letakkan dua skenario itu berdampingan atas saldo yang sama, Rp300 juta, lalu membahas empat kesalahan yang paling sering terjadi dan satu langkah gratis yang bisa kamu lakukan hari ini: membuka riwayat klaim dan mencari tanggal pengambilan pertama.

Catatan: aturan pajak atas JHT sedang ditinjau ulang oleh Menteri Keuangan, dan serikat pekerja meminta tarif 0% untuk semua nilai. Sampai ada aturan baru, yang berlaku adalah yang dibahas di sini. Materi ini bersifat edukasi, bukan nasihat pajak, dan bukan ajakan mempercepat atau menunda pencairan.

## BAB
{CAPITULOS}

## KOMENTAR
Satu pertanyaan, karena jawabannya sering mengejutkan: kamu pernah mengambil JHT sebagian 10% atau 30%? Kalau pernah, kamu ingat tahun berapa? Tidak perlu menyebut nominal. Saya kumpulkan jawabannya untuk materi berikutnya. Kalau kamu ingin hitungan yang sama dibuat untuk pesangon, tulis saja di kolom komentar.

## HASHTAG
#JHT #BPJSKetenagakerjaan #SetiapLevel

## TAG
jht, bpjs ketenagakerjaan, pencairan jht, pajak jht, pph 21 final, tarif progresif, pasal 17, jmo, klaim jht, saldo jht, phk 2026, pesangon, keuangan pribadi, indonesia, setiap level

## PENGATURAN STUDIO
- Bahasa: Indonesia (id) | Kategori: Edukasi (27)
- Tidak dibuat untuk anak-anak
- Deklarasi konten sintetis: YA (suara AI)
- Lokasi: Indonesia | Lisensi: lisensi YouTube standar
- Iklan mid-roll: aktif (di atas 8 menit)

## MUSIK / LISENSI
{TRILHA}

## SUMBER
Tarif dan definisi berasal dari Peraturan Pemerintah Nomor 68 Tahun 2009 dan Peraturan Menteri Keuangan Nomor 16/PMK.03/2010, sebagaimana diuraikan oleh Ortax (18 April 2025) dan DDTCNews (30 Juni 2026), yang saling bersesuaian: PPh Pasal 21 final atas pencairan JHT sekaligus sebesar 0% atas penghasilan bruto sampai dengan Rp50.000.000 dan 5% atas bagian di atasnya; "sekaligus" didefinisikan sebagai pembayaran sebagian atau seluruh manfaat dalam jangka waktu paling lama 2 tahun kalender; manfaat yang diambil lebih dari 2 tahun setelah pengambilan sebagian (10% atau 30%) dikenakan PPh Pasal 21 tidak final dengan tarif progresif Pasal 17 UU PPh. Ketentuan pencairan (usia 56 tahun, meninggal dunia, cacat total tetap; pengambilan sebagian 10–30% setelah masa kepesertaan paling singkat 10 tahun) berasal dari Peraturan Pemerintah Nomor 46 Tahun 2015. Lapisan tarif Pasal 17 pasca UU HPP (5% s.d. Rp60 juta; 15% s.d. Rp250 juta; 25% s.d. Rp500 juta; 30% s.d. Rp5 miliar; 35% di atasnya) dikutip dari pajakku dan online-pajak, yang sama nilainya. Data klaim Januari–Mei 2026 (1,72 juta klaim; 1,64 juta atau 95,45% kena tarif 0%; 78.441 klaim kena tarif 5%) berasal dari Kementerian Keuangan dan Direktorat Jenderal Pajak, sebagaimana dilaporkan secara konsisten oleh Tirto, Liputan6, RRI, DDTCNews dan IKPI (akses 19 Agustus 2026). Perhitungan berdampingan atas saldo Rp300.000.000 adalah aritmetika langsung atas tarif-tarif di atas dan disebut sebagai batas bawah, karena penghasilan yang tidak final digabungkan dengan penghasilan lain pada tahun yang sama. Materi edukasi; bukan nasihat pajak, bukan rekomendasi produk, dan bukan ajakan mempercepat atau menunda pencairan.
"""

SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-008",
    "idioma": "id",
    "voz": "id-ID-ArdiNeural",
    "trilha": "Wholesome",  # identidade do canal, conferida pelo portao
    "paleta": {"ink": "#14213D", "c1": "#E5A200", "c2": "#00897B", "bg": "#F7F3E8"},
    "thumb": {"l1": "SALDO SAMA", "l2": "pajak beda 3x"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = "fabrica/specs/setiap-level-008.json"
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
