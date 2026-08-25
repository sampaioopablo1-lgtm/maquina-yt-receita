#!/usr/bin/env python3
"""Monta a spec setiap-level-011.

ALAVANCA ATACADA: **A — conversao short -> inscrito**, e este canal da a
medida mais nitida que a frota ja produziu dela.

NUMERO DE PARTIDA, medido em 25/08/2026 em `metricas` x `videos`, short a
short:

    566 views -> 0 inscritos   "3 Kebiasaan Kecil yang Menghabiskan Gajimu"
    126 views -> 0 inscritos   "4 Pilar: urutannya yang menentukan"
    106 views -> 0 inscritos   "BPJS Kesehatan: kelas dihapus"
     75 views -> 0 inscritos   "Pencairan JHT: Rp12,5 juta atau Rp44 juta"
    185 views -> 1 inscrito    "Gaji naik. Bulanmu sama. Kenapa?"      0,54%
     12 views -> 1 inscrito    "Bunga Deposito: berapa yang benar-benar
                                kamu simpan setelah pajak dan inflasi"  8,33%

Os TRES mais vistos somam 798 views e ZERO inscritos. O menos visto do acervo,
com doze views, converteu 8,33%. Isso repete o aprendizado 482 num segundo
canal e num segundo idioma — mas aqui ele fica mais afiado, e a versao afiada e
o que esta spec testa.

NAO E "metodo contra fato". O short do JHT ("saldo igual, imposto de doze
virgula cinco ou quarenta e quatro milhoes") E uma conta, e converteu zero. O
que separa os dois que converteram nao e ter conta: e a conta ser sobre O
DINHEIRO DE QUEM ASSISTE, na segunda pessoa. "Berapa yang benar-benar KAMU
simpan". "Bulan-MU sama". O do JHT calcula o saldo de um sujeito hipotetico de
trezentos milhoes; quem ganha cinco milhoes por mes nao se ve ali.

HIPOTESE DESTA RODADA: short cuja conta o espectador faz no PROPRIO
contracheque converte acima de 1%. E o numero que fecha o experimento.

O QUE NAO DEU, e vale dizer com todas as letras: o LONGO. Quatorze longos, 18
views somadas, zero inscritos, mediana de 0,07 views/dia. O veredito
`v_maquina_licoes` e `suspenso`, que manda o piso de 8 min e o melhor material
no SHORT. Este pacote obedece: o longo fica no piso e o cuidado esta no short.
Gastar craft na retencao de um longo que recebe uma view por semana seria
otimizar a variavel errada — e a alavanca B (aprendizado 483) foi medida no
kolejny-poziom, que tem distribuicao, nao aqui.

--------------------------------------------------------------------- A PAUTA

Eixo: **PPh 21 e o sistema TER**. Nunca usado neste canal. Os publicados
cobrem gaji, dana darurat, deposito, JHT, pinjol, PHK, BPJS Kesehatan,
50-30-20, skill stacking, belanja semanal e Gen Z — imposto de renda sobre o
salario, nunca.

E e a pauta mais "segunda pessoa" que existe neste nicho: o numero sai do
contracheque do proprio espectador, e ele consegue conferir hoje a noite.

FONTES INSTITUCIONAIS, duas que se confirmam:

  1. DIRETORIA GERAL DE IMPOSTOS (pajak.go.id), o proprio fisco:
       TER Bulanan tem tres categorias por status de PTKP.
       Kategori A .... TK/0 e TK/1 (PTKP 54 juta) e K/0 (54,8 juta),
                       44 faixas, teto de 34%.
       Kategori B .... TK/2 e TK/3 (63 juta), K/1 e K/2 (67,5 juta),
                       40 faixas, teto de 34%.
       Kategori C .... K/3 (72 juta), 41 faixas, teto de 34%.
       Janeiro a novembro usam TER; DEZEMBRO usa a tarifa do Pasal 17.
       Exemplo de faixa citado pelo proprio DJP: bruto de 9.650.001 a
       10.050.000 -> tarifa efetiva de 2%.
       Pasal 17 (UU HPP): 5% ate 60 juta; 15% de 60 a 250 juta; 25% de 250
       a 500 juta; 30% de 500 juta a 5 miliar; 35% acima.
       Biaya jabatan: 5% do bruto, teto de 500 mil por mes / 6 juta por ano.

  2. JDIH KEMENKEU (jdih.kemenkeu.go.id), base legal do Ministerio das
     Financas, que hospeda a PMK 168 Tahun 2023 — a norma que institui o TER —
     e a PMK 250/PMK.03/2008, que fixa o biaya jabatan.

A CONTA COMPLETA, e ela e o coracao do video. Gaji bruto 10 juta/mes, TK/0:

    jan-nov (TER A) .... 10 juta cai na faixa de 2% -> 200 mil por mes
                         onze meses -> 2,2 juta ja retidos
    dezembro (Pasal 17)  bruto do ano ......... 120 juta
                         biaya jabatan 5% ..... 6 juta (bate no teto exato)
                         neto ................. 114 juta
                         PTKP TK/0 ............ 54 juta
                         PKP .................. 60 juta
                         PPh do ano 5% ........ 3 juta
                         menos o ja retido .... 2,2 juta
                         RETIDO EM DEZEMBRO ... 800 mil

Ou seja: em dezembro sai QUATRO VEZES o de um mes comum, e nao e erro do RH.
O TER e aproximacao; dezembro e o acerto de contas.

O QUE O VIDEO DIZ EM VOZ ALTA: o exemplo NAO inclui contribuicao dedutivel de
pensao/JHT do empregado, nem THR, nem bonus. Com eles o PKP cai e a conta muda.
Nao e aconselhamento fiscal.

ACENTOS. Indonesio nao usa diacritico; o cuidado aqui e outro — numero por
extenso sempre, porque o TTS soletra digito cru errado.
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
# O metodo inteiro — achar a categoria e multiplicar — sai nos capitulos 1 a 3.

# ------------------------------------------------------------------- cap 1
T("Slip gajimu", "punya satu angka tetap",
  "Di slip gajimu ada satu angka yang dipotong setiap bulan, dan besarnya "
  "hampir tidak pernah berubah dari Januari sampai November.",
  cap="Angka tetap di slip gajimu")
I("Lalu Desember", "angkanya melompat",
  "Lalu datang Desember dan angka itu melompat. Banyak orang mengira kantor "
  "salah hitung.")
I("Bukan salah hitung", "itu memang aturannya",
  "Bukan salah hitung. Itu memang cara kerja pemotongan pajak penghasilan "
  "sejak sistemnya diubah.")
I("Namanya TER", "tarif efektif rata-rata",
  "Sistemnya bernama tarif efektif rata-rata, disingkat TER, dan diatur lewat "
  "peraturan menteri keuangan.")
I("Yang berubah", "rumusnya, bukan tarifnya",
  "Yang berubah bukan besar pajaknya. Yang berubah adalah cara menghitung "
  "potongan bulanan.")
I("Yang dipotong itu", "cicilan, bukan tagihan",
  "Satu hal yang perlu jelas dulu: potongan bulanan itu bukan tagihan pajakmu. "
  "Itu cicilan di muka atas pajak setahun.")
I("Makanya ada Desember", "bulan penutup",
  "Karena itu ada bulan penutup. Kalau cicilannya kurang, kekurangannya "
  "ditagih sekaligus di akhir tahun.")
I("Sistem ini baru", "slip lama beda",
  "Sistem TER dipakai sejak dua ribu dua puluh empat, jadi slip lama dan slip "
  "sekarang memang berbeda polanya.")
I("Hari ini", "kamu bisa hitung sendiri",
  "Hari ini kamu akan bisa menghitung sendiri berapa yang keluar tiap bulan, "
  "dan berapa yang keluar di Desember.")

# ------------------------------------------------------------------- cap 2
T("Langkah satu", "cari statusmu",
  "Langkah pertama, dan ini yang menentukan segalanya: cari status PTKP-mu.",
  cap="Cari kategori TER kamu")
I("Apa itu PTKP", "penghasilan tidak kena pajak",
  "PTKP adalah penghasilan tidak kena pajak, dan besarnya tergantung status "
  "kawin dan jumlah tanggungan.")
I("Kode TK dan K", "lajang atau kawin",
  "Kodenya sederhana. Huruf TK berarti tidak kawin, huruf K berarti kawin, "
  "dan angka di belakangnya adalah jumlah tanggungan.")
I("Kategori A", "TK nol, TK satu, K nol",
  "Kalau statusmu TK nol, TK satu, atau K nol, kamu masuk kategori A. Di sana "
  "PTKP-nya lima puluh empat juta atau lima puluh empat koma delapan juta.")
I("Kategori B", "empat status di tengah",
  "Kategori B menampung empat status di tengah. Dua di antaranya berstatus "
  "tidak kawin dengan tanggungan, dua lagi berstatus kawin. PTKP-nya berkisar "
  "dari enam puluh tiga juta sampai enam puluh tujuh koma lima juta.")
I("Kategori C", "K tiga",
  "Dan status K tiga masuk kategori C, dengan PTKP tujuh puluh dua juta.")
I("Arti angka PTKP", "bagian yang tidak dipajaki",
  "Angka PTKP itu bukan hiasan. Dia adalah bagian penghasilan setahun yang "
  "tidak dikenai pajak sama sekali.")
I("Contohnya", "lima puluh empat juta bebas",
  "Untuk status TK nol, lima puluh empat juta pertama dalam setahun tidak "
  "dipajaki. Pajak baru mulai dihitung di atas itu.")
I("Statusmu ada di slip", "atau tanya HR",
  "Status ini biasanya tercetak di slip gajimu. Kalau tidak ada, itu satu "
  "pertanyaan singkat ke bagian HR.")

# ------------------------------------------------------------------- cap 3
T("Langkah dua", "satu perkalian",
  "Langkah kedua, dan hanya ini yang perlu kamu lakukan setiap bulan.",
  cap="Kalikan brutomu dengan tarifnya")
I("Ambil brutomu", "bukan yang diterima",
  "Ambil penghasilan bruto sebulan, bukan yang kamu terima di rekening. "
  "Bruto adalah sebelum semua potongan.")
I("Cari barismu", "di tabel kategorimu",
  "Cari baris penghasilan itu di tabel kategorimu. Setiap kategori punya "
  "puluhan lapisan, dan setiap lapisan punya satu tarif.")
I("Contoh dari fiskus", "dua persen",
  "Contoh yang dipakai sendiri oleh direktorat pajak: bruto antara sembilan "
  "koma enam lima juta dan sepuluh koma nol lima juta kena tarif dua persen.")
I("Lalu kalikan", "itu potonganmu",
  "Kalikan brutomu dengan tarif itu. Hasilnya adalah potongan pajak bulananmu, "
  "dan itu berlaku dari Januari sampai November.")
I("Sepuluh juta", "dua ratus ribu",
  "Untuk gaji sepuluh juta, dua persen berarti dua ratus ribu rupiah keluar "
  "setiap bulan.")
I("Bruto termasuk apa", "gaji pokok dan tunjangan",
  "Bruto bukan cuma gaji pokok. Dia mencakup tunjangan tetap dan komponen "
  "lain yang kamu terima bulan itu.")
I("Bedanya dengan Pasal 17", "tarifnya kena seluruh bruto",
  "Perhatikan satu hal: tarif efektif dikalikan ke seluruh bruto, bukan ke "
  "sebagian. Itu yang membuat perkaliannya sesederhana ini.")
I("Itu seluruh metodenya", "sisanya penjelasan",
  "Itu seluruh metodenya. Sisa video ini adalah alasannya, contoh lengkapnya, "
  "dan hal-hal yang tidak masuk hitungan.")

# ============ ate aqui, ~200 segundos. O que segue aprofunda. ===============

# ------------------------------------------------------------------- cap 4
T("Kenapa Desember", "beda sendiri",
  "Sekarang bagian yang membuat orang bingung setiap akhir tahun.",
  cap="Kenapa Desember dihitung ulang")
I("TER itu perkiraan", "bukan hitungan final",
  "TER adalah perkiraan yang rapi. Dia membagi beban pajak setahun ke dalam "
  "sebelas bulan, tanpa menghitung ulang apa pun.")
I("Desember memakai Pasal 17", "tarif berlapis",
  "Di Desember pemberi kerja berhenti memakai TER dan memakai tarif berlapis "
  "Pasal 17, yaitu tarif yang sesungguhnya.")
I("Lapisan pertama", "lima persen",
  "Lapisan pertama adalah lima persen untuk penghasilan kena pajak sampai "
  "enam puluh juta setahun.")
I("Lapisan berikutnya", "lima belas persen",
  "Di atas enam puluh juta sampai dua ratus lima puluh juta tarifnya lima "
  "belas persen.")
I("Lalu naik lagi", "dua puluh lima persen",
  "Di atas dua ratus lima puluh juta sampai lima ratus juta tarifnya dua "
  "puluh lima persen, dan terus naik dari sana.")
I("Bukan atas bruto", "atas penghasilan kena pajak",
  "Satu koreksi penting: tarif berlapis itu tidak dikenakan ke bruto. Dia "
  "dikenakan ke penghasilan kena pajak, yaitu setelah pengurang dan PTKP.")
I("Dan hanya kelebihannya", "bukan seluruhnya",
  "Dan kalau penghasilan kena pajakmu melewati satu lapisan, tarif yang lebih "
  "tinggi hanya mengenai kelebihannya, bukan seluruh penghasilan.")
I("Jadi naik gaji", "tetap menguntungkan",
  "Jadi naik gaji tidak pernah membuat uang yang kamu bawa pulang jadi lebih "
  "kecil. Yang naik hanya pajak atas bagian tambahannya.")
I("Selisihnya di Desember", "itu saja",
  "Pajak setahun dihitung dengan tarif itu, lalu dikurangi semua yang sudah "
  "dipotong Januari sampai November. Sisanya keluar di Desember.")

# ------------------------------------------------------------------- cap 5
T("Contoh lengkap", "gaji sepuluh juta",
  "Mari kita jalankan satu contoh sampai selesai, dengan angka bulat.",
  cap="Contoh lengkap: gaji sepuluh juta")
I("Profilnya", "TK nol, sepuluh juta",
  "Karyawan tetap dengan status TK nol dan penghasilan bruto sepuluh juta "
  "sebulan. Berarti kategori A.")
I("Januari sampai November", "dua ratus ribu",
  "Tarifnya dua persen, jadi potongannya dua ratus ribu sebulan. Sebelas "
  "bulan berarti dua juta dua ratus ribu sudah masuk kas negara.")
I("Bruto setahun", "seratus dua puluh juta",
  "Sekarang hitungan Desember. Bruto setahun adalah seratus dua puluh juta "
  "rupiah.")
I("Biaya jabatan", "enam juta",
  "Dari situ dikurangi biaya jabatan, yaitu lima persen dari bruto dengan "
  "batas enam juta setahun. Di contoh ini pas menyentuh batasnya.")
I("Penghasilan neto", "seratus empat belas juta",
  "Penghasilan neto setahun menjadi seratus empat belas juta rupiah.")
I("Dikurangi PTKP", "enam puluh juta",
  "Dikurangi PTKP lima puluh empat juta, penghasilan kena pajaknya adalah "
  "enam puluh juta rupiah.")
I("Pajak setahun", "tiga juta",
  "Enam puluh juta pas berada di lapisan pertama, jadi pajaknya lima persen, "
  "yaitu tiga juta rupiah setahun.")
I("Yang sudah dipotong", "dua juta dua ratus ribu",
  "Yang sudah dipotong sepanjang tahun adalah dua juta dua ratus ribu rupiah.")
B("Potongan bulanan", ["Jan-Nov", "Desember"], [25, 100],
  "Selisihnya, yang keluar di Desember, adalah delapan ratus ribu rupiah.")
I("Empat kali lipat", "dan itu benar",
  "Empat kali potongan bulan biasa, dalam satu bulan. Bukan kesalahan, dan "
  "bukan pajak baru.")
I("Kenapa selisihnya ada", "TER membulatkan",
  "Selisih itu muncul karena TER membulatkan sepanjang tahun, dan Desember "
  "yang membereskan pembulatannya.")

# ------------------------------------------------------------------- cap 6
T("Yang tidak masuk", "dan bisa mengubah hasilnya",
  "Sekarang jujur soal apa yang contoh tadi tidak masukkan.",
  cap="Yang contoh ini tidak masukkan")
I("Iuran pensiun", "mengurangi neto",
  "Iuran pensiun atau jaminan hari tua yang kamu bayar sendiri mengurangi "
  "penghasilan neto, jadi pajak setahunmu jadi lebih kecil.")
I("THR dan bonus", "menambah bruto",
  "THR dan bonus menambah bruto di bulan diterimanya, dan itu menaikkan "
  "potongan di bulan tersebut.")
I("Pindah kerja", "hitungannya terpisah",
  "Kalau kamu pindah kerja di tengah tahun, tiap pemberi kerja menghitung "
  "bagiannya sendiri, dan penyesuaiannya terjadi di SPT tahunanmu.")
I("Bisa juga sebaliknya", "Desember lebih ringan",
  "Selisihnya tidak selalu menambah. Kalau TER memotong lebih banyak dari "
  "pajak setahunmu, potongan Desember justru jadi lebih kecil.")
I("Bruto yang naik turun", "tarifnya ikut pindah",
  "Kalau brutomu berubah tiap bulan karena lembur, kamu bisa pindah lapisan, "
  "dan tarif efektifmu ikut berubah bulan itu.")
I("Karena itu", "hitung ulang tiap bulan",
  "Karena itu, hitung ulang pembagian tadi setiap kali brutomu berubah. Satu "
  "pembagian, lima detik.")
I("Kalau statusmu berubah", "menikah atau punya anak",
  "Kalau kamu menikah atau bertambah tanggungan, kategorimu bisa pindah, dan "
  "tarif efektifmu ikut berubah. Laporkan perubahan itu ke HR.")
I("Jadi ini titik awal", "bukan hitungan final",
  "Jadi perlakukan angka ini sebagai titik awal untuk memahami slip gajimu, "
  "bukan sebagai hitungan pajak final.")

# ------------------------------------------------------------------- cap 7
T("Dari mana angkanya", "dua sumber resmi",
  "Dari mana semua angka ini, karena itu pertanyaan yang selalu pantas.",
  cap="Dari mana angkanya")
I("Sumber pertama", "direktorat jenderal pajak",
  "Kategori TER, batas PTKP tiap kategori, dan aturan bahwa Desember memakai "
  "tarif berlapis berasal dari situs direktorat jenderal pajak.")
I("Sumber kedua", "JDIH Kementerian Keuangan",
  "Peraturan yang mendasarinya tersedia di basis hukum kementerian keuangan, "
  "termasuk aturan biaya jabatan.")
I("Yang tidak saya pakai", "kalkulator daring",
  "Saya tidak memakai kalkulator daring atau situs tips mana pun. Angka yang "
  "tidak ada di sumber resmi tidak masuk video ini.")
I("Cara mengeceknya sendiri", "dua kata kunci",
  "Kamu bisa mengeceknya tanpa perantara. Dua kata kunci cukup: peraturan "
  "menteri keuangan seratus enam puluh delapan, dan lampiran tarif efektif.")
I("Di lampiran itu", "tabel lengkapnya",
  "Di lampiran peraturan itulah seluruh lapisan tarif ketiga kategori "
  "tercetak, baris demi baris.")
I("Dan ini bukan usulan", "sudah berlaku",
  "Satu penegasan: yang saya jelaskan di sini bukan rencana atau usulan. Ini "
  "aturan yang sudah berlaku dan sudah ada di slip gajimu.")
I("Kenapa itu penting", "ini soal pajak",
  "Untuk urusan pajak, salah angka bukan sekadar keliru: yang menanggung "
  "akibatnya adalah orang yang mempraktikkannya. Lebih baik mengatakan lebih "
  "sedikit dan yakin akan yang sedikit itu.")

# ------------------------------------------------------------------- cap 8
T("Malam ini", "tiga hal",
  "Tiga hal yang bisa kamu lakukan malam ini, semuanya di satu halaman.",
  cap="Yang kamu lakukan malam ini")
I("Pertama", "buka slip gajimu",
  "Buka slip gaji bulan lalu dan cari dua angka: penghasilan bruto, dan "
  "potongan pajak penghasilan.")
I("Kedua", "bagi yang satu dengan yang lain",
  "Bagi potongan itu dengan brutonya. Hasilnya dalam persen adalah tarif "
  "efektif yang sedang dipakai untukmu.")
L("Ketiga", ["Status PTKP saya",
             "Tarif efektif saya",
             "Berapa potongan Desember saya"],
  "Lalu tulis tiga baris: status PTKP saya, tarif efektif saya, dan perkiraan "
  "potongan Desember saya.")
I("Baris ketiga itu", "yang paling berguna",
  "Baris ketiga yang paling berguna, karena Desember adalah bulan yang paling "
  "sering tidak sesuai dugaan orang.")
I("Simpan angkanya", "bandingkan Desember nanti",
  "Simpan catatan itu sampai Desember. Waktu slip Desember keluar, kamu punya "
  "pembanding, bukan cuma rasa kaget.")
I("Ringkasnya", "TER lalu Pasal 17",
  "Ringkasnya: Januari sampai November potonganmu adalah tarif efektif dikali "
  "bruto, dan Desember adalah pajak setahun dikurangi semua yang sudah "
  "dipotong.")
C("Setiap Level", "hitung punyamu",
  "Lakukan satu hal hari ini: hitung tarif efektifmu sendiri dan tulis "
  "angkanya. Di sini kita ambil satu angka dari hidupmu dan mengubahnya jadi "
  "tindakan yang kamu kerjakan sendiri. Kalau itu yang kamu cari, "
  "berlanggananlah.")


# -------------------------------------------------------------------- short
#
# ESTE E O ENTREGAVEL DESTA RODADA. O veredito do canal e `suspenso`: melhor
# material no short. E a forma segue o que converteu — SEGUNDA PESSOA, o
# dinheiro de quem assiste, e a conta feita ali dentro, nao prometida.
SHORT = [
    {"layout": "titulo", "kicker": "Potongan Desember",
     "sub": "empat kali bulan biasa",
     "nar": "Potongan pajak di slip gajimu bulan Desember bisa empat kali "
            "lipat bulan biasa. Ini cara tahu punyamu.", "sem_cap": True},
    {"layout": "item", "kicker": "Buka slip gajimu", "preco": "ambil dua angka",
     "nar": "Ambil penghasilan bruto sebulan dan potongan pajaknya, lalu bagi "
            "yang kedua dengan yang pertama.", "sem_cap": True},
    {"layout": "item", "kicker": "Itu tarifmu", "preco": "berlaku Jan sampai Nov",
     "nar": "Hasilnya adalah tarif efektifmu, dan itu yang dipakai dari "
            "Januari sampai November.", "sem_cap": True},
    {"layout": "item", "kicker": "Desember lain", "preco": "pajak setahun dikurangi",
     "nar": "Desember dihitung ulang: pajak setahun dikurangi semua yang sudah "
            "dipotong. Sisanya keluar sekaligus.", "sem_cap": True},
    {"layout": "cta", "kicker": "Setiap Level", "sub": "tulis angkamu",
     "nar": "Hitung tarif efektifmu malam ini dan tulis angkanya. Di sini "
            "setiap angka jadi tindakan yang kamu kerjakan sendiri.",
     "sem_cap": True},
]

COPY = """# PPh 21 TER: tarif efektifmu dan kenapa Desember beda

## TITULO
PPh 21 TER: Cara Hitung Tarif Efektifmu Sendiri dan Kenapa Desember Beda

## DESCRICAO
Di slip gajimu ada satu angka yang dipotong setiap bulan dan hampir tidak pernah berubah dari Januari sampai November — lalu di Desember angka itu melompat. Itu bukan kesalahan hitung kantor. Video ini menunjukkan cara menghitung sendiri tarif efektifmu, memakai dua angka yang sudah ada di slip gajimu, dan cara memperkirakan potongan Desember sebelum bulannya tiba.

CARA CEPAT MENGETAHUI TARIFMU (dua angka, satu pembagian)

Buka slip gaji bulan lalu. Ambil penghasilan bruto sebulan, lalu ambil potongan PPh 21. Bagi potongan dengan bruto. Hasilnya dalam persen adalah tarif efektif yang sedang dipakai untukmu dari Januari sampai November.

SISTEM TER (sumber: Direktorat Jenderal Pajak)

TER Bulanan punya tiga kategori yang ditentukan oleh status PTKP. Kategori A untuk status TK/0 dan TK/1 (PTKP Rp54.000.000) serta K/0 (Rp54.800.000), dengan 44 lapisan tarif. Kategori B untuk TK/2 dan TK/3 (Rp63.000.000) serta K/1 dan K/2 (Rp67.500.000), dengan 40 lapisan. Kategori C untuk K/3 (Rp72.000.000), dengan 41 lapisan. Tarif tertinggi di ketiga kategori adalah 34%. Contoh lapisan yang dipakai DJP sendiri: penghasilan bruto Rp9.650.001 sampai Rp10.050.000 dikenakan tarif efektif 2%.

Yang berubah bukan besarnya pajak, melainkan rumus pemotongan bulanannya. TER bukan jenis pajak baru.

KENAPA DESEMBER DIHITUNG ULANG

Masa pajak Januari sampai November memakai TER. Desember memakai tarif berlapis Pasal 17: 5% sampai Rp60.000.000 penghasilan kena pajak; 15% di atas Rp60.000.000 sampai Rp250.000.000; 25% di atas Rp250.000.000 sampai Rp500.000.000; 30% di atas Rp500.000.000 sampai Rp5.000.000.000; dan 35% di atasnya. Pajak setahun dihitung dengan tarif itu, lalu dikurangi seluruh potongan Januari sampai November. Selisihnya keluar di Desember.

CONTOH LENGKAP: GAJI BRUTO Rp10.000.000, STATUS TK/0

Januari sampai November: tarif 2%, potongan Rp200.000 per bulan, total Rp2.200.000. Desember: bruto setahun Rp120.000.000; dikurangi biaya jabatan 5% dengan batas Rp6.000.000 setahun, jadi Rp6.000.000; penghasilan neto Rp114.000.000; dikurangi PTKP TK/0 Rp54.000.000, penghasilan kena pajak Rp60.000.000; pajak setahun 5% = Rp3.000.000; dikurangi Rp2.200.000 yang sudah dipotong, potongan Desember menjadi Rp800.000 — empat kali potongan bulan biasa.

YANG TIDAK MASUK HITUNGAN INI: iuran pensiun atau JHT yang kamu bayar sendiri (mengurangi neto, jadi pajak setahun lebih kecil), THR dan bonus (menambah bruto di bulan diterimanya), dan perpindahan kerja di tengah tahun (tiap pemberi kerja menghitung bagiannya sendiri, penyesuaian terjadi di SPT Tahunan). Perlakukan angka di video ini sebagai titik awal untuk memahami slip gajimu, bukan sebagai perhitungan pajak final. Ini bukan nasihat perpajakan.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Bagi potongan PPh 21 di slip gajimu dengan penghasilan brutomu, lalu tulis satu angka di komentar: tarif efektifmu dalam persen. Bukan gajimu — cukup persennya. Saya penasaran berapa banyak dari kamu yang ada di bawah 3%, karena itu kelompok yang paling kaget waktu Desember datang.

## HASHTAGS
#PPh21 #PajakGaji #SetiapLevel

## TAGS
pph 21, ter pph 21, tarif efektif rata rata, pajak gaji, potongan pajak desember, ptkp, tk/0, biaya jabatan, pasal 17, slip gaji, pajak penghasilan karyawan, hitung pajak gaji, spt tahunan, pmk 168, keuangan pribadi

## CONFIGURACOES DO STUDIO
- Idioma: Indonesio (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Os numeros vem de DUAS fontes institucionais que se confirmam. (1) DIRETORIA GERAL DE IMPOSTOS (pajak.go.id), o proprio fisco indonesio: o TER Bulanan tem tres categorias definidas pelo status de PTKP — A para TK/0 e TK/1 (PTKP 54.000.000) e K/0 (54.800.000), com 44 faixas; B para TK/2 e TK/3 (63.000.000) e K/1 e K/2 (67.500.000), com 40 faixas; C para K/3 (72.000.000), com 41 faixas; teto de 34% nas tres. Janeiro a novembro usam TER e DEZEMBRO usa a tarifa do Pasal 17. A faixa de exemplo (bruto de 9.650.001 a 10.050.000 com tarifa efetiva de 2%) e citada pelo proprio DJP. As faixas do Pasal 17 (UU HPP) — 5% ate 60 juta, 15% ate 250 juta, 25% ate 500 juta, 30% ate 5 miliar, 35% acima — tambem saem do DJP. (2) JDIH KEMENKEU (jdih.kemenkeu.go.id), a base de legislacao do Ministerio das Financas, que hospeda a PMK 168 Tahun 2023, norma que institui o TER, e a PMK 250/PMK.03/2008, que fixa o biaya jabatan em 5% do bruto com teto de 500.000 por mes ou 6.000.000 por ano. A CONTA DE DEZEMBRO FOI DERIVADA, nao copiada: 120.000.000 de bruto menos 6.000.000 de biaya jabatan da 114.000.000 de neto; menos 54.000.000 de PTKP da 60.000.000 de PKP; 5% disso da 3.000.000 de imposto anual; menos os 2.200.000 ja retidos em onze meses restam 800.000 em dezembro, quatro vezes o mes comum. NAO foi usado nenhum calculador ou portal de dicas. O video diz em voz alta que o exemplo nao inclui iuran pensiun/JHT do empregado, THR, bonus nem troca de emprego no meio do ano, e que nao e aconselhamento fiscal.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/setiap-level-011.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-011",
    "idioma": "id",
    "voz": "id-ID-ArdiNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#14202E", "c1": "#1B7F79", "c2": "#E4913C",
               "bg": "#F1F6F5"},
    "thumb": {"l1": "Tarif efektifmu", "l2": "cek slip gaji"},
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
    grava(SPEC, "fabrica/specs/setiap-level-011.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
