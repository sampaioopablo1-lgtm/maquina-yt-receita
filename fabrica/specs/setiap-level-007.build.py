#!/usr/bin/env python3
"""setiap-level-007 — berapa lama uang pesangon bertahan setelah PHK.

PAUTA (PASSO 0, 17/08/2026). Entre os outliers do `pautas_banco` do canal, o
eixo PHK aparece com forca e NUNCA foi usado: "Korban PHK & Hutang Wajib
Nonton" faz 1.693,1 views/dia. A ESTRUTURA copiada e a dele — publico nomeado
na primeira palavra e promessa numerica concreta. O ASSUNTO nao: ele fala de
pagar divida com fluxo de caixa diario, este fala de quanto tempo o dinheiro da
recisao dura e o que fazer nos primeiros trinta dias.

EIXOS JA USADOS pelo canal, todos evitados aqui: cara atur gaji / quatro pilares
(v-5v7R13BBc), gaji harian Rp100 ribu (G8ocnpQIiyg), gaji naik e inflacao
(fjHksJ8Z0fw), utang pinjol e OJK (iYe04WMYDxQ), skill stacking, gen Z,
50-30-20 e bertahan tres anos. O eixo PHK nao encosta em nenhum deles.

NUMEROS — duas fontes que batem em cada um:
  * 43.805 pessoas atingidas por PHK entre janeiro e julho de 2026, dado do
    Kemnaker. Bisnis.com (10/08/2026) e Pajakonline. Jawa Barat lidera com
    8.830.
  * Pesangon por PP 35/2021 (turunan da UU Cipta Kerja): masa kerja de oito
    anos ou mais da NOVE meses de upah. Confirmado por ANTARA News, Gadjian,
    CATAPA e HRD Forum. O direito tem tres componentes: UP, UPMK e UPH.
  * JKP: 60% do upah por seis meses cheios, sem degrau no meio, com teto de
    upah de Rp5.000.000 — base PP 6/2025. Tempo e Kompas.
  * Requisito do JKP: doze meses de contribuicao dentro dos ultimos vinte e
    quatro. Prazo para pedir: seis meses a contar do PHK.

DIMENSIONAMENTO. id-ID-ArdiNeural com R = 18,72 chars/s e P = 1,079 s/frase.
Este e o modelo com maior n do banco — 282 cenas de PRODUCAO, nao de ensaio.
Vale mais que a bateria de laboratorio de oito amostras que usei no
kolejny-poziom-004 e que ainda errou 10,4% no roteiro real.

DURACAO ALVO. O canal estava escalonado para 1620s sem atender o criterio:
medi os treze videos hoje e os longos de 25-28 min entregam 0,30 views/dia
contra mediana de nicho de 91,25. Baixei `canais.duracao_alvo_s` para 780 e
registrei a evidencia. Esta spec ja nasce com o alvo novo.
"""
import json
import os

SLUG = "setiap-level"
PACOTE = "setiap-level-007"

PALETA = {"bg": "#FFF8F0", "c1": "#0B6E4F", "c2": "#F2A104", "ink": "#1B2021"}


def t(kicker, sub, nar, cap=None, sem_cap=False):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def i(kicker, preco, nar, cap=None, sem_cap=False):
    c = {"layout": "item", "kicker": kicker, "preco": preco, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def li(kicker, itens, nar, cap=None, sem_cap=False):
    c = {"layout": "lista", "kicker": kicker, "itens": itens, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def b(kicker, itens, alturas, nar, cap=None, sem_cap=False):
    c = {"layout": "barras", "kicker": kicker, "itens": itens,
         "alturas": alturas, "nar": nar}
    if cap:
        c["cap"] = cap
    if sem_cap:
        c["sem_cap"] = True
    return c


def cta(kicker, sub, nar):
    return {"layout": "cta", "kicker": kicker, "sub": sub, "nar": nar,
            "sem_cap": True}


LONGO = [
    # ---------- 1. amplop yang terasa banyak ----------
    t("SURAT ITU DATANG", "dan rekeningmu tiba-tiba penuh",
      "Surat PHK datang hari Senin. Hari Jumat rekeningmu penuh — angka paling "
      "besar yang pernah kamu lihat di sana. Dan justru di situ letak "
      "bahayanya.",
      cap="Amplop yang terasa banyak"),
    i("Berapa orang seperti kamu", "empat puluh tiga ribu",
      "Kamu tidak sendirian. Kementerian Ketenagakerjaan mencatat empat puluh "
      "tiga ribu delapan ratus lima orang terkena PHK sepanjang Januari sampai "
      "Juli dua ribu dua puluh enam."),
    i("Provinsi terbanyak", "Jawa Barat",
      "Jawa Barat menyumbang angka terbesar, delapan ribu delapan ratus tiga "
      "puluh orang. Ini bukan kasus langka yang menimpa orang lain."),
    t("PERTANYAAN VIDEO INI", "berapa lama uang itu bertahan",
      "Pertanyaannya bukan berapa besar uang yang kamu terima. Pertanyaannya "
      "berapa lama uang itu bertahan, dan apa yang menentukan lamanya.",
      sem_cap=True),
    li("Yang akan kita hitung",
       ["berapa hakmu", "berapa lama bertahan", "empat langkah pertama"],
       "Kita hitung tiga hal. Berapa sebenarnya hakmu menurut aturan. Berapa "
       "lama uang itu bertahan dengan pengeluaranmu yang sekarang. Dan empat "
       "langkah di tiga puluh hari pertama yang mengubah hitungan itu."),
    i("Aturan mainnya", "angka, bukan semangat",
      "Tidak ada kalimat penyemangat di video ini. Hanya angka, sumbernya, dan "
      "apa yang bisa kamu lakukan dengan angka itu."),

    # ---------- 2. tiga amplop, bukan satu ----------
    t("HAKMU ADA TIGA", "bukan satu angka",
      "Kesalahan pertama dimulai lebih awal dari yang kamu kira: menganggap "
      "pesangon itu satu angka. Menurut aturan, hakmu terdiri dari tiga "
      "komponen.",
      cap="Tiga amplop, bukan satu"),
    li("Tiga komponen itu",
       ["uang pesangon", "penghargaan masa kerja", "penggantian hak"],
       "Uang pesangon, disingkat U P. Uang penghargaan masa kerja, U P M K. Dan "
       "uang penggantian hak, U P H. Tiga pos berbeda, dengan cara hitung yang "
       "berbeda pula."),
    i("Dasar hukumnya", "Peraturan Pemerintah tiga lima",
      "Dasarnya Peraturan Pemerintah nomor tiga puluh lima tahun dua ribu dua "
      "puluh satu, turunan dari Undang-Undang Cipta Kerja. Ini bukan kebijakan "
      "internal perusahaanmu."),
    b("Uang pesangon menurut masa kerja",
      ["satu tahun", "empat tahun", "delapan tahun ke atas"],
      [2, 5, 9],
      "Besarnya naik menurut masa kerja. Satu tahun memberi dua bulan upah. "
      "Empat tahun memberi lima bulan. Delapan tahun atau lebih memberi "
      "sembilan bulan upah, dan di situ tabelnya berhenti naik."),
    i("Yang sering dilupakan", "pengali",
      "Ada satu hal yang sering hilang dalam pembicaraan. Angka di tabel itu "
      "masih dikalikan faktor pengali, dan pengalinya tergantung ALASAN PHK-nya "
      "— efisiensi, penggabungan usaha, atau pelanggaran berat."),
    i("Kenapa itu penting", "selisihnya besar",
      "Selisihnya bukan receh. Alasan yang tertulis di surat PHK-mu bisa "
      "menggandakan atau memotong separuh angka akhirnya."),
    b("Faktor pengali menurut alasan",
      ["pelanggaran berat", "efisiensi perusahaan", "perusahaan tutup rugi"],
      [5, 10, 10],
      "Contohnya begini. PHK karena efisiensi memakai pengali penuh. PHK karena "
      "pelanggaran berat bisa memakai setengah. Dua orang dengan masa kerja "
      "sama bisa pulang dengan angka yang berbeda jauh."),
    t("KOMPONEN KEDUA", "uang penghargaan masa kerja",
      "Komponen kedua, U P M K, punya tabel sendiri dan mulai dihitung dari masa "
      "kerja tiga tahun — bukan dari satu tahun seperti pesangon.",
      sem_cap=True),
    i("Bagaimana naiknya", "lebih landai",
      "Kenaikannya lebih landai daripada pesangon, tapi tetap bertambah "
      "sepanjang masa kerjamu. Untuk masa kerja panjang, ini bukan angka kecil."),
    t("KOMPONEN KETIGA", "uang penggantian hak",
      "Komponen ketiga, U P H, adalah yang paling sering hilang begitu saja "
      "karena tidak ada yang menagihnya.",
      sem_cap=True),
    li("Apa saja isinya",
       ["cuti tahunan yang belum diambil", "biaya pulang ke tempat asal",
        "hal lain di perjanjian kerja"],
       "Isinya cuti tahunan yang belum kamu ambil, biaya pulang ke tempat asal "
       "kalau kamu direkrut dari kota lain, dan hal-hal lain yang tertulis di "
       "perjanjian kerja atau peraturan perusahaan."),
    i("Kenapa sering hilang", "harus kamu sebut",
      "Ini sering hilang karena tidak muncul otomatis di hitungan HRD. Kalau "
      "kamu tidak menyebutkannya, sering kali tidak dibayarkan."),
    t("LANGKAH NOL", "baca alasan di suratmu",
      "Jadi sebelum menghitung apa pun, baca alasan yang tertulis di suratmu. "
      "Itu variabel terbesar dalam seluruh perhitungan ini.",
      sem_cap=True),

    # ---------- 3. uang kedua yang tidak kamu tahu ----------
    t("ADA UANG KEDUA", "namanya JKP",
      "Sekarang bagian yang paling sering terlewat: selain pesangon, ada uang "
      "kedua dari negara. Namanya Jaminan Kehilangan Pekerjaan, disingkat JKP.",
      cap="Uang kedua yang terlewat"),
    i("Berapa besarnya", "enam puluh persen",
      "JKP memberi enam puluh persen dari upahmu, selama enam bulan penuh. "
      "Persentasenya rata setiap bulan, tidak turun di pertengahan seperti "
      "aturan yang lama."),
    i("Dasar aturannya", "Peraturan Pemerintah enam",
      "Besaran ini datang dari Peraturan Pemerintah nomor enam tahun dua ribu "
      "dua puluh lima. Sebelumnya, tiga bulan terakhir dibayar lebih kecil."),
    i("Batas atasnya", "lima juta rupiah",
      "Ada batas atas. Upah yang dipakai menghitung dibatasi lima juta rupiah, "
      "jadi yang bergaji di atas itu tetap dihitung dari lima juta."),
    b("JKP per bulan menurut upah",
      ["upah tiga juta", "upah lima juta", "upah sepuluh juta"],
      [18, 30, 30],
      "Artinya upah tiga juta memberi satu koma delapan juta per bulan. Upah "
      "lima juta memberi tiga juta. Dan upah sepuluh juta juga memberi tiga "
      "juta — bukan enam, karena batas atasnya berlaku."),
    li("Syarat yang harus dipenuhi",
       ["dua belas bulan iuran", "dalam dua puluh empat bulan terakhir",
        "PHK yang tercatat"],
       "Syaratnya tiga. Sudah menjadi peserta minimal dua belas bulan. Dua "
       "belas bulan itu berada dalam dua puluh empat bulan terakhir. Dan PHK-mu "
       "tercatat resmi, dibuktikan dengan tanda terima laporan."),
    t("BATAS WAKTUNYA", "enam bulan",
      "Dan ini yang membuat orang kehilangan haknya bukan karena tidak berhak: "
      "klaim JKP harus diajukan paling lambat enam bulan sejak tanggal PHK.",
      sem_cap=True),
    i("Kenapa banyak yang terlewat", "menunggu terlalu lama",
      "Banyak yang melewatkannya karena menunggu — menunggu tenang dulu, "
      "menunggu dapat kerja dulu. Enam bulan lewat lebih cepat dari yang kamu "
      "rasakan saat sedang mencari kerja."),

    # ---------- 4. berapa lama uang itu bertahan ----------
    i("Satu catatan jujur", "angka ini contoh",
      "Satu catatan jujur sebelum kita mulai. Angka ini contoh, bukan janji. "
      "Punyamu bergantung pada pengali dan pada komponen U P M K dan U P H yang "
      "tadi kita bahas."),
    t("SEKARANG HITUNG", "berapa lama uang itu bertahan",
      "Sekarang kita gabungkan keduanya dan jawab pertanyaan judul. Berapa lama "
      "uang itu bertahan.",
      cap="Berapa lama uang itu bertahan"),
    i("Contoh yang kita pakai", "upah lima juta",
      "Pakai satu contoh sepanjang video: upah lima juta rupiah, masa kerja "
      "delapan tahun, PHK karena efisiensi."),
    i("Pesangon sembilan bulan", "empat puluh lima juta",
      "Sembilan bulan upah memberi empat puluh lima juta rupiah, sebelum "
      "pengali dan sebelum komponen lain."),
    i("JKP enam bulan", "delapan belas juta",
      "JKP memberi tiga juta per bulan selama enam bulan, jadi delapan belas "
      "juta rupiah, dibayarkan bulanan dan bukan sekaligus."),
    b("Dua sumber, satu kolom",
      ["pesangon", "JKP", "total"],
      [45, 18, 63],
      "Digabung, uang yang lewat di tanganmu sekitar enam puluh tiga juta "
      "rupiah. Angka ini terasa seperti tabungan bertahun-tahun yang tiba-tiba "
      "muncul."),
    t("TAPI ITU BUKAN TABUNGAN", "itu gaji yang dibayar di muka",
      "Tapi itu bukan tabungan. Itu gaji beberapa bulan ke depan yang dibayar "
      "di muka, dan cara memperlakukannya menentukan segalanya.",
      sem_cap=True),
    b("Enam puluh tiga juta bertahan berapa lama",
      ["pengeluaran lima juta", "pengeluaran empat juta",
       "pengeluaran tiga juta"],
      [12, 15, 21],
      "Dengan pengeluaran lima juta sebulan, uang itu bertahan sekitar dua "
      "belas setengah bulan. Dengan empat juta, hampir enam belas bulan. Dengan "
      "tiga juta, dua puluh satu bulan."),
    i("Selisih dua juta", "delapan bulan lebih",
      "Perhatikan selisihnya. Potong pengeluaranmu dari lima juta ke tiga. "
      "Waktumu bertambah lebih dari delapan bulan. Dan waktu adalah satu-satunya "
      "hal yang kamu butuhkan untuk mencari kerja tanpa panik."),
    t("KENAPA BEDANYA BESAR", "pembaginya, bukan uangnya",
      "Perhatikan apa yang berubah di tiga hitungan itu. Uangnya sama persis. "
      "Yang berubah cuma pembaginya — dan pembagi itu satu-satunya angka yang "
      "masih kamu kendalikan setelah PHK.",
      sem_cap=True),
    i("Yang tidak kamu kendalikan", "masa kerja dan alasan",
      "Masa kerjamu sudah tertulis. Alasan PHK sudah tertulis. Upahmu sudah "
      "tertulis. Tiga dari empat variabel sudah terkunci sebelum kamu membaca "
      "suratnya."),
    i("Yang kamu kendalikan", "pengeluaran bulanmu",
      "Yang keempat, pengeluaran bulananmu, masih bisa berubah bulan depan. Di "
      "situlah seluruh sisa video ini bekerja."),
    i("Ini bukan soal hemat", "ini soal waktu",
      "Jadi memotong pengeluaran di sini bukan soal berhemat demi berhemat. Itu "
      "cara membeli bulan tambahan untuk menolak tawaran kerja yang buruk."),

    t("SATU POTONGAN LAGI", "pajak",
      "Ada satu potongan yang belum masuk hitungan tadi, dan lebih baik kamu "
      "tahu sekarang daripada saat uangnya masuk: pesangon dikenai pajak "
      "penghasilan.",
      sem_cap=True),
    i("Bagaimana tarifnya", "berlapis",
      "Tarifnya berlapis dan khusus untuk pesangon, bukan tarif gaji biasa. "
      "Bagian pertama dari uangmu dikenai tarif nol persen, dan lapisan di "
      "atasnya bertarif lebih tinggi."),
    i("Artinya buat kamu", "hitung yang bersih",
      "Artinya angka yang masuk rekeningmu lebih kecil dari angka di surat. "
      "Pakai angka BERSIH untuk semua hitungan bulanmu, bukan angka kotor."),
    t("JANGAN LUPA INI JUGA", "BPJS Kesehatanmu",
      "Dan satu hal yang tidak berhubungan dengan uang tunai, tapi bisa "
      "menghancurkan seluruh rencanamu: iuran BPJS Kesehatan yang selama ini "
      "dipotong dari gaji berhenti bersamaan dengan gajimu.",
      sem_cap=True),
    i("Kenapa ini penting", "satu sakit cukup",
      "Satu kejadian sakit tanpa jaminan bisa menghapus seluruh sisa "
      "pesangonmu. Masukkan iuran mandiri ke daftar pengeluaran wajibmu sejak "
      "bulan pertama."),
    i("Berapa besarnya", "kecil dibanding risikonya",
      "Nilainya kecil dibandingkan angka-angka lain di video ini, dan justru "
      "karena kecil ia sering terlupa saat menyusun anggaran."),

    # ---------- 5. tiga puluh hari pertama ----------
    t("TIGA PULUH HARI PERTAMA", "empat langkah",
      "Sekarang bagian yang bisa kamu kerjakan besok. Empat langkah di tiga "
      "puluh hari pertama, berurutan.",
      cap="Tiga puluh hari pertama"),
    i("Langkah satu", "laporkan PHK-mu",
      "Langkah pertama, dalam minggu pertama: laporkan PHK-mu dan ambil tanda "
      "terima laporannya. Tanpa dokumen ini, klaim JKP-mu tidak jalan."),
    i("Kenapa ini nomor satu", "semua bergantung padanya",
      "Ini nomor satu bukan karena paling mendesak rasanya, tapi karena semua "
      "langkah lain bergantung padanya, dan jam enam bulan sudah berjalan."),
    i("Langkah dua", "hitung pengeluaran wajibmu",
      "Langkah kedua: hitung pengeluaran WAJIB bulananmu — sewa, cicilan, "
      "makan, listrik, sekolah anak. Bukan pengeluaran idealmu, pengeluaran "
      "yang tidak bisa kamu hentikan bulan depan."),
    i("Kenapa yang wajib saja", "itu yang jadi penyebut",
      "Angka itu yang menjadi penyebut dalam hitungan tadi. Selama kamu belum "
      "tahu angkanya, kamu tidak tahu kamu punya berapa bulan."),
    i("Langkah tiga", "pisahkan uangnya",
      "Langkah ketiga: pisahkan uang pesangon ke rekening yang berbeda dari "
      "rekening harian. Uang yang terlihat setiap hari akan terpakai setiap "
      "hari."),
    li("Bagi jadi tiga pos",
       ["enam bulan biaya hidup", "cicilan yang jalan terus",
        "sisanya jangan disentuh"],
       "Bagi menjadi tiga pos. Biaya hidup enam bulan ke depan. Cicilan yang "
       "tetap berjalan. Dan sisanya, yang tidak kamu sentuh sampai kamu punya "
       "penghasilan lagi."),
    i("Langkah empat", "jangan lunasi cicilan besar dulu",
      "Langkah keempat, dan yang paling kontra-intuitif: jangan buru-buru "
      "melunasi cicilan besar dengan uang pesangon."),
    i("Alasannya", "uang tunai adalah waktu",
      "Alasannya sederhana. Saat belum ada penghasilan, uang tunai adalah waktu "
      "dan pilihan. Melunasi cicilan menukar keduanya dengan bunga yang "
      "dihemat, dan bunga itu jauh lebih murah dari panik."),
    t("PENGECUALIAN SATU", "kecuali bunganya mencekik",
      "Ada satu pengecualian jujur: kalau cicilanmu berbunga sangat tinggi, "
      "seperti pinjaman online harian, hitungannya berbalik dan melunasi lebih "
      "dulu masuk akal.",
      sem_cap=True),

    # ---------- 6. yang berubah tahun ini ----------
    t("YANG BERUBAH", "dua hal di dua ribu dua puluh lima",
      "Dua hal berubah belakangan ini, dan keduanya menguntungkanmu.",
      cap="Yang berubah tahun ini"),
    i("Perubahan pertama", "enam puluh persen rata",
      "Pertama, JKP sekarang enam puluh persen rata selama enam bulan. Aturan "
      "lama membayar lebih kecil di tiga bulan terakhir."),
    i("Perubahan kedua", "waktu klaim lebih panjang",
      "Kedua, tenggat pengajuan klaim menjadi enam bulan sejak PHK, lebih "
      "panjang dari sebelumnya."),
    i("Yang tidak berubah", "kamu harus mengajukan",
      "Yang tidak berubah: tidak ada yang otomatis. Kamu tetap harus melapor "
      "dan mengajukan sendiri."),
    t("JKP BUKAN CUMA UANG", "ada dua manfaat lain",
      "Dan JKP bukan cuma uang tunai. Ada dua manfaat lain yang jarang "
      "disebut, dan keduanya gratis.",
      sem_cap=True),
    li("Dua manfaat lainnya",
       ["akses informasi pasar kerja", "pelatihan kerja"],
       "Pertama, akses ke informasi pasar kerja. Kedua, pelatihan kerja. "
       "Keduanya bagian dari program yang sama, dan tidak menambah potongan "
       "apa pun."),
    i("Kenapa ini masuk hitungan", "mempersingkat bulan menganggur",
      "Ini masuk hitungan karena tujuan seluruh video ini adalah memperpanjang "
      "waktumu. Mempersingkat bulan menganggur bekerja dari sisi yang lain."),
    li("Tiga dokumen yang disiapkan",
       ["bukti penerimaan PHK", "tanda terima laporan", "kartu kepesertaan"],
       "Siapkan tiga dokumen sejak sekarang. Bukti penerimaan PHK. Tanda terima "
       "laporan PHK. Dan kartu kepesertaanmu."),

    i("Kalau kamu punya usaha sampingan", "hitung sebagai pengurang",
      "Kalau kamu punya penghasilan sampingan, sekecil apa pun, masukkan ke "
      "hitungan sebagai pengurang pengeluaran. Satu juta per bulan mengubah "
      "pembagi dari lima menjadi empat."),
    i("Efeknya pada waktu", "tiga bulan lebih",
      "Satu juta per bulan itu menambah lebih dari tiga bulan pada hitungan tadi, "
      "tanpa memotong satu pun pengeluaranmu."),

    # ---------- 7. kesalahan yang mahal ----------
    t("TIGA KESALAHAN", "yang paling mahal",
      "Sebelum menutup, tiga kesalahan yang paling mahal — dan ketiganya "
      "dilakukan di bulan pertama.",
      cap="Tiga kesalahan mahal"),
    i("Kesalahan pertama", "menunda lapor",
      "Menunda melapor karena merasa belum siap secara mental. Jam enam bulan "
      "tidak menunggu kesiapan siapa pun."),
    i("Kesalahan kedua", "mempertahankan gaya hidup",
      "Mempertahankan pengeluaran seperti masih bergaji, karena rekening "
      "terlihat penuh. Ini yang mengubah dua puluh satu bulan menjadi dua belas "
      "setengah."),
    i("Kesalahan ketiga", "modal usaha di bulan pertama",
      "Memakai seluruh pesangon sebagai modal usaha di bulan pertama, sebelum "
      "biaya hidup enam bulan diamankan lebih dulu."),
    t("BUKAN LARANGAN", "soal urutan",
      "Yang ketiga bukan larangan berusaha. Ini soal urutan: amankan bulan "
      "hidupmu dulu, baru sisihkan modal dari sisanya.",
      sem_cap=True),

    # ---------- 8. empat angka ----------
    t("EMPAT ANGKA", "yang perlu kamu tahu minggu ini",
      "Aku tinggalkan kamu dengan empat angka yang perlu kamu tahu minggu ini.",
      cap="Empat angka untuk minggu ini"),
    li("Angka pertama dan kedua",
       ["masa kerjamu dalam tahun", "alasan PHK di suratmu"],
       "Pertama, masa kerjamu dalam tahun penuh — itu menentukan baris di "
       "tabel. Kedua, alasan PHK yang tertulis di suratmu, karena itu "
       "menentukan pengalinya."),
    li("Angka ketiga dan keempat",
       ["pengeluaran wajib bulananmu", "bulan iuran dalam dua tahun terakhir"],
       "Ketiga, pengeluaran wajib bulananmu — penyebut dari seluruh hitungan. "
       "Keempat, berapa bulan kamu sudah beriuran dalam dua puluh empat bulan "
       "terakhir, karena itu menentukan hakmu atas JKP."),
    i("Kalau keempatnya sudah ada", "hitungannya lima menit",
      "Kalau keempat angka itu sudah ada di tanganmu, seluruh hitungan di video "
      "ini selesai dalam lima menit."),
    t("SATU KALIMAT", "uang itu waktu, bukan tabungan",
      "Kalau hanya satu kalimat yang kamu bawa: uang pesangon bukan tabungan, "
      "itu waktu — dan berapa lama waktunya kamu yang tentukan lewat "
      "pengeluaran bulananmu.",
      sem_cap=True),
    i("Catatan penting", "ini bukan nasihat hukum",
      "Catatan penting: ini penjelasan umum, bukan nasihat hukum. Angka "
      "akhirmu bergantung pada isi surat dan perjanjian kerjamu."),
    cta("SETIAP LEVEL", "hitung empat angkamu minggu ini",
        "Hitung empat angkamu minggu ini, sebelum bulan pertama lewat. Kalau "
        "cara berhitung seperti ini masuk akal buatmu, subscribe."),
]

SHORT = [
    {"layout": "titulo", "kicker": "PESANGON ITU WAKTU",
     "sub": "bukan tabungan",
     "nar": "Uang pesangonmu bukan tabungan. Itu waktu, dan kamu yang menentukan "
            "berapa lama."},
    {"layout": "item", "kicker": "Contoh nyata", "preco": "enam puluh tiga juta",
     "nar": "Upah lima juta, masa kerja delapan tahun. Pesangon dan JKP digabung "
            "sekitar enam puluh tiga juta."},
    {"layout": "barras", "kicker": "Bertahan berapa lama",
     "itens": ["belanja lima juta", "belanja tiga juta"], "alturas": [126, 210],
     "nar": "Dengan pengeluaran lima juta sebulan, dua belas setengah bulan. "
            "Dengan tiga juta, dua puluh satu bulan."},
    {"layout": "item", "kicker": "Selisihnya", "preco": "delapan bulan lebih",
     "nar": "Delapan bulan lebih untuk menolak tawaran kerja yang buruk."},
    {"layout": "item", "kicker": "Jangan lupa ini", "preco": "enam bulan",
     "nar": "Dan klaim JKP-mu hangus kalau lewat enam bulan sejak PHK."},
    {"layout": "cta", "kicker": "EMPAT LANGKAH", "sub": "ada di video panjang",
     "nar": "Empat langkah tiga puluh hari pertama ada di video panjang di "
            "kanal."},
]

COPY = """# Pesangon itu waktu: berapa lama uang PHK bertahan

## JUDUL
Kena PHK 2026: Berapa Lama Pesangon Bertahan dan 4 Langkah Pertama

## DESKRIPSI
Surat PHK datang hari Senin, rekeningmu penuh hari Jumat, dan justru di situ
letak bahayanya. Video ini menghitung berapa lama uang itu benar-benar bertahan
— dan apa yang menentukan lamanya.

Angka-angka yang dipakai di video ini:

• Kementerian Ketenagakerjaan mencatat 43.805 orang terkena PHK sepanjang
Januari–Juli 2026. Jawa Barat menyumbang angka terbesar, 8.830 orang.

• Hak pekerja yang di-PHK terdiri dari tiga komponen, bukan satu: uang pesangon
(UP), uang penghargaan masa kerja (UPMK), dan uang penggantian hak (UPH). Dasar
hukumnya PP No. 35 Tahun 2021, turunan UU Cipta Kerja.

• Masa kerja 8 tahun atau lebih memberi 9 bulan upah sebagai uang pesangon, dan
di situ tabelnya berhenti naik. Angka itu masih dikalikan faktor pengali yang
tergantung ALASAN PHK — variabel terbesar dalam seluruh perhitungan.

• JKP (Jaminan Kehilangan Pekerjaan) memberi 60% upah selama 6 bulan penuh,
rata setiap bulan, dengan batas atas upah Rp5.000.000. Dasarnya PP No. 6 Tahun
2025. Syaratnya: peserta minimal 12 bulan dalam 24 bulan terakhir, dan PHK yang
tercatat resmi.

• Klaim JKP harus diajukan paling lambat 6 bulan sejak tanggal PHK. Banyak orang
kehilangan haknya bukan karena tidak berhak, tapi karena menunggu terlalu lama.

Contoh yang dipakai sepanjang video: upah Rp5 juta, masa kerja 8 tahun. Pesangon
sekitar Rp45 juta dan JKP Rp18 juta, total sekitar Rp63 juta. Dengan pengeluaran
Rp5 juta sebulan uang itu bertahan sekitar 12,6 bulan; dengan Rp3 juta, 21
bulan. Selisih pengeluaran Rp2 juta membeli lebih dari delapan bulan waktu — dan waktu
adalah yang kamu butuhkan untuk menolak tawaran kerja yang buruk.

Empat langkah di 30 hari pertama, berurutan: laporkan PHK dan ambil tanda terima
laporannya; hitung pengeluaran WAJIB bulananmu; pisahkan uang pesangon ke
rekening berbeda; dan jangan buru-buru melunasi cicilan besar — kecuali bunganya
sangat tinggi seperti pinjaman online harian.

Ini penjelasan umum, bukan nasihat hukum. Angka akhirmu bergantung pada isi surat
PHK dan perjanjian kerjamu.

Kalau cara berhitung seperti ini masuk akal buatmu, subscribe.

## BAB
{CAPITULOS}

## KOMENTAR
Empat angka yang perlu kamu tahu minggu ini: 1) masa kerjamu dalam tahun penuh,
2) alasan PHK yang tertulis di suratmu, 3) pengeluaran WAJIB bulananmu, 4) berapa
bulan kamu sudah beriuran dalam 24 bulan terakhir. Kalau keempatnya sudah ada,
seluruh hitungan di video ini selesai dalam lima menit.

## TAGAR
#PHK #pesangon #JKP

## TAG
PHK 2026, pesangon, JKP, BPJS Ketenagakerjaan, uang pesangon, PP 35 2021, hak pekerja, korban PHK, keuangan setelah PHK, dana darurat, UU Cipta Kerja, kehilangan pekerjaan, atur keuangan, cicilan, Kemnaker

## PENGATURAN STUDIO
Kategori 27 (Pendidikan). Bahasa Indonesia, audio Bahasa Indonesia. Bukan untuk
anak-anak. Mengandung konten sintetis — dideklarasikan saat publikasi. Subtitle
dari berkas SRT.

## MUSIK / LISENSI
Wholesome — YouTube Audio Library, tanpa kewajiban atribusi. Level minus dua
puluh delapan desibel terhadap narasi.

## SUMBER
Data PHK Januari–Juli 2026: Kementerian Ketenagakerjaan, dikutip Bisnis.com
(10/08/2026) dan Pajakonline. Pesangon: PP No. 35 Tahun 2021, turunan UU Cipta
Kerja — tabel dikonfirmasi ANTARA News dan Gadjian. JKP: PP No. 6 Tahun 2025,
dikonfirmasi Tempo dan Kompas.
"""

TAGS = [
    "PHK 2026", "pesangon", "JKP", "BPJS Ketenagakerjaan", "uang pesangon",
    "PP 35 2021", "hak pekerja", "korban PHK", "keuangan setelah PHK",
    "dana darurat", "UU Cipta Kerja", "kehilangan pekerjaan", "atur keuangan",
    "cicilan", "Kemnaker",
]

SPEC = {
    "slug": SLUG,
    "pacote": PACOTE,
    "voz": "id-ID-ArdiNeural",
    "idioma": "id",
    "trilha": "Wholesome",
    "paleta": PALETA,
    "thumb": {"l1": "63 JUTA", "l2": "BERTAHAN BERAPA LAMA?"},
    "longo": LONGO,
    "short": SHORT,
    "copy": COPY,
    "tags": TAGS,
    "fonte_pauta": "Korban PHK & Hutang Wajib Nonton (1693,1 v/d)",
}


def _bertahan(total_juta=63.0, belanja_juta=5.0):
    """Quantos meses o dinheiro dura. A conta que o video narra."""
    return total_juta / belanja_juta


if __name__ == "__main__":
    for g in (5.0, 4.0, 3.0):
        print(f"  belanja {g:.0f} juta -> {_bertahan(belanja_juta=g):5.1f} bulan")
    print(f"  selisih 5 para 3: {_bertahan(belanja_juta=3)-_bertahan(belanja_juta=5):.1f} bulan")

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           f"{PACOTE}.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{destino}: {len(LONGO)} cenas, short {len(SHORT)}")
