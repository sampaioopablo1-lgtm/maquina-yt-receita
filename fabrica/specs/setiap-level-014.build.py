#!/usr/bin/env python3
"""Monta a spec setiap-level-014.

ALAVANCA ATACADA: **A — conversao short -> inscrito**, por EIXO NOVO. Veredito
`canal frio`, e a rotina manda eixo novo, nao mais um video igual.

NUMERO DE PARTIDA, lido em 01/09/2026 21:15Z ja com o dado corrigido do
aprendizado 549:

    setiap-level ...... 2 inscritos, 31 videos, 1.168 views
                        short: mediana 0,95 views/dia, topo 19,67
                        longo: mediana 0,06 views/dia, topo 0,67
                        veredito: `canal frio`

O QUE DEU CERTO, e o canal e muito claro sobre isso:

    "3 Kebiasaan Kecil yang Menghabiskan Gajimu" .. short 566 views | 26 s
    "Gaji naik. Bulanmu sama. Kenapa?" ............ short 185 views | 30 s
    "4 Pilar: urutannya yang menentukan" .......... short 126 views | 41 s

Os tres maiores shorts do canal falam de COMPORTAMENTO — um habito que o
espectador tem sem perceber. E os dois maiores sao tambem os mais CURTOS do
canal: vinte e seis e trinta segundos.

O QUE NAO DEU: regulacao. Os shorts sobre regra publicada — BPJS, JHT, pinjol,
PPh 21, PHK — fizeram 105, 75, 18, 0 e 0. Sao a maioria dos videos recentes do
canal e sao os que menos andam.

E OS LONGOS, TODOS. O melhor longo do canal fez OITO views. Os tres longos mais
recentes fizeram zero, zero e zero. Vale notar de onde o canal veio: ha longos
de 1.716 s, 1.696 s e 1.545 s publicados em 05 e 12/08, de vinte e cinco a
vinte e oito minutos, todos com uma ou duas views.

O QUE MUDO POR CAUSA DISSO:

1. **O EIXO SAI DA REGULACAO E VOLTA PRO COMPORTAMENTO.** Nenhum dos trinta e
   um videos do canal fala do que o BANCO cobra do espectador. Este fala, e o
   numero que decide nao vem de lei nenhuma: vem do extrato dele.

2. **O SHORT FICA CURTO DE PROPOSITO.** O padrao da frota e quarenta segundos;
   aqui os dois maiores tem vinte e seis e trinta. Este vai para a casa dos
   trinta, e isso e uma mudanca deliberada baseada no numero DESTE canal, nao
   uma regra da frota.

3. **NENHUM NUMERO EXTERNO CARREGA O VIDEO.** Tentei conferir o teto de tarifa
   do BI-FAST no bi.go.id e o site nao respondeu; a busca so devolveu noticia,
   nao fonte oficial. Entao redesenhei a pauta para que o numero que decide
   seja o DO ESPECTADOR — as linhas de taxa no extrato dele. Nao ha tabela de
   tarifa de banco nenhum neste video, e o aviso diz por que.

A CONTA, entregue no capitulo 2 (~130 s estimados):
    passo 1: no extrato de doze meses, some toda linha com "biaya" ou "adm"
    passo 2: divida por doze -> o que a conta te custa por mes
    passo 3: divida o total anual pelo seu saldo medio -> o percentual ao ano
             que voce paga so para guardar o proprio dinheiro

O passo 3 e o que fecha a pauta: quem tem pouco saldo paga percentual alto, e
esse percentual costuma passar do juro que o mesmo banco paga no deposito. O
canal ja fez "Bunga Deposito 2026" pelo lado do rendimento; este e o outro lado
da mesma conta, e por isso conversa com o que ja existe sem repetir.

DIMENSIONAMENTO: `canal frio` nao define faixa. Mesma analogia que usei no
nivel-do-jogo-009 — piso de oito minutos, e digo que e analogia. Alvo ~515 s,
8 capitulos, resposta fechada antes dos 200 s.
"""

C1 = [
    {"layout": "titulo", "kicker": "Uangmu diam di bank",
     "sub": "tapi tidak diam-diam saja",
     "cap": "Biaya yang tidak pernah kamu setujui",
     "nar": "Uangmu di bank tidak hanya diam. Setiap bulan ada angka kecil "
            "yang keluar dari saldomu, dan kamu tidak pernah menekan tombol "
            "apa pun untuk itu."},
    {"layout": "item", "kicker": "Bukan transaksimu", "preco": "tapi tetap keluar",
     "sem_cap": True,
     "nar": "Itu bukan belanjamu dan bukan transfermu. Itu biaya, dan dia "
            "keluar sendiri."},
    {"layout": "item", "kicker": "Namanya beda-beda", "preco": "biaya, adm, admin",
     "sem_cap": True,
     "nar": "Di mutasi rekening namanya bermacam-macam: biaya administrasi, "
            "biaya kartu, biaya di bawah saldo minimum, biaya tarik tunai di "
            "mesin bank lain."},
    {"layout": "item", "kicker": "Satu per satu kecil", "preco": "itu sebabnya lolos",
     "sem_cap": True,
     "nar": "Satu per satu angkanya kecil, dan justru karena kecil dia lolos "
            "dari perhatianmu setiap bulan."},
    {"layout": "item", "kicker": "Setahun", "preco": "jadi angka lain",
     "sem_cap": True,
     "nar": "Tapi dikali dua belas bulan, dia berhenti menjadi angka kecil."},
    {"layout": "item", "kicker": "Aku tidak akan tebak angkanya",
     "preco": "kamu yang punya", "sem_cap": True,
     "nar": "Aku tidak akan menebak berapa punyamu, dan aku tidak akan "
            "menyebut tarif bank mana pun di video ini. Angkanya ada di "
            "rekeningmu sendiri."},
    {"layout": "item", "kicker": "Yang hemat pun kena", "preco": "ini bukan soal disiplin",
     "sem_cap": True,
     "nar": "Dan ini bukan soal boros atau hemat. Orang yang paling disiplin "
            "mencatat pengeluaran pun jarang mencatat baris ini, karena dia "
            "tidak pernah muncul sebagai keputusan."},
    {"layout": "item", "kicker": "Tiga langkah", "preco": "dan satu persentase",
     "sem_cap": True,
     "nar": "Tiga langkah, dan di akhirnya kamu dapat satu persentase yang "
            "biasanya bikin kaget. Kita mulai sekarang."},
]

C2 = [
    {"layout": "titulo", "kicker": "Buka mutasi rekening", "sub": "dua belas bulan",
     "cap": "Tiga langkah di mutasimu",
     "nar": "Buka aplikasi bankmu dan cari mutasi rekening. Ambil dua belas "
            "bulan terakhir, bukan satu bulan."},
    {"layout": "item", "kicker": "Langkah 1", "preco": "jumlahkan semua 'biaya'",
     "sem_cap": True,
     "nar": "Langkah satu: cari setiap baris yang memuat kata biaya, adm, "
            "atau admin, dan jumlahkan semuanya."},
    {"layout": "item", "kicker": "Termasuk yang ini", "preco": "sering terlewat",
     "sem_cap": True,
     "nar": "Jangan lewatkan biaya transfer antarbank, biaya tarik tunai di "
            "mesin bank lain, dan biaya cek saldo di mesin bank lain."},
    {"layout": "item", "kicker": "Langkah 2", "preco": "bagi dua belas",
     "sem_cap": True,
     "nar": "Langkah dua: bagi total itu dengan dua belas. Itulah harga bulanan "
            "rekeningmu, yang tidak pernah tertulis di mana pun."},
    {"layout": "item", "kicker": "Langkah 3", "preco": "bagi dengan saldo rata-rata",
     "sem_cap": True,
     "nar": "Langkah tiga, dan ini yang menentukan: bagi total setahun itu "
            "dengan saldo rata-ratamu, lalu kalikan seratus."},
    {"layout": "item", "kicker": "Hasilnya", "preco": "persen per tahun",
     "sem_cap": True,
     "nar": "Hasilnya adalah persentase per tahun yang kamu bayar hanya untuk "
            "menyimpan uangmu sendiri. Itu hitungannya, dan sudah selesai."},
    {"layout": "item", "kicker": "Kalau aplikasimu bisa", "preco": "unduh mutasinya",
     "sem_cap": True,
     "nar": "Kalau aplikasimu bisa mengunduh mutasi sebagai berkas, unduh "
            "saja dan cari kata biaya. Itu memotong pekerjaan tadi jadi "
            "beberapa detik."},
    {"layout": "item", "kicker": "Sisanya", "preco": "arti dari angka itu",
     "sem_cap": True,
     "nar": "Sisa video ini adalah arti dari angka itu, dan apa yang bisa kamu "
            "lakukan setelah melihatnya."},
]

C3 = [
    {"layout": "titulo", "kicker": "Kenapa persentase", "sub": "bukan rupiah",
     "cap": "Kenapa yang penting persentase, bukan rupiah",
     "nar": "Kenapa aku minta persentase, dan bukan cukup jumlah rupiahnya?"},
    {"layout": "item", "kicker": "Biaya itu tetap", "preco": "saldomu tidak",
     "sem_cap": True,
     "nar": "Karena biaya administrasi biasanya angka tetap. Bank memotong "
            "jumlah yang sama, entah saldomu besar atau kecil."},
    {"layout": "item", "kicker": "Saldo besar", "preco": "persentase kecil",
     "sem_cap": True,
     "nar": "Kalau saldomu besar, potongan tetap itu jadi persentase yang "
            "hampir tidak terasa."},
    {"layout": "item", "kicker": "Saldo kecil", "preco": "persentase besar",
     "sem_cap": True,
     "nar": "Kalau saldomu kecil, potongan yang sama persis berubah jadi "
            "persentase yang besar. Angkanya sama, bebannya tidak."},
    {"layout": "item", "kicker": "Jadi", "preco": "yang saldonya kecil bayar lebih mahal",
     "sem_cap": True,
     "nar": "Jadi dalam hitungan persen, yang saldonya paling kecil justru "
            "membayar paling mahal untuk layanan yang sama."},
    {"layout": "item", "kicker": "Itu sebabnya", "preco": "rupiah menipu",
     "sem_cap": True,
     "nar": "Itu sebabnya melihat rupiahnya saja menipu. Sepuluh ribu sebulan "
            "terdengar murah sampai kamu tahu itu berapa persen dari saldomu."},
    {"layout": "item", "kicker": "Contoh cara berpikirnya", "preco": "bukan angkamu",
     "sem_cap": True,
     "nar": "Cara berpikirnya begini, dan angkanya cuma contoh: potongan tetap "
            "yang sama menjadi dua persen setahun bagi yang saldonya sepuluh "
            "juta, dan dua puluh persen bagi yang saldonya satu juta."},
    {"layout": "item", "kicker": "Dan sekarang", "preco": "bandingkan",
     "sem_cap": True,
     "nar": "Dan begitu kamu punya persennya, kamu bisa membandingkannya "
            "dengan sesuatu yang selama ini kamu kejar."},
]

C4 = [
    {"layout": "titulo", "kicker": "Bandingkan dengan bunga",
     "sub": "yang kamu terima", "cap": "Bandingkan dengan bunga yang kamu terima",
     "nar": "Sekarang bandingkan persentase tadi dengan bunga yang bank bayar "
            "ke kamu."},
    {"layout": "item", "kicker": "Cari di aplikasi", "preco": "bunga tabungan",
     "sem_cap": True,
     "nar": "Bunga tabunganmu ada di aplikasi yang sama, biasanya di bagian "
            "informasi produk atau di suku bunga."},
    {"layout": "item", "kicker": "Dua angka", "preco": "berhadapan",
     "sem_cap": True,
     "nar": "Sekarang kamu punya dua angka yang berhadapan: berapa persen "
            "yang kamu bayar, dan berapa persen yang kamu terima."},
    {"layout": "item", "kicker": "Untuk banyak orang", "preco": "yang dibayar lebih besar",
     "sem_cap": True,
     "nar": "Untuk rekening dengan saldo kecil, yang dibayar sering lebih "
            "besar daripada yang diterima. Artinya rekening itu bukan tempat "
            "menabung."},
    {"layout": "item", "kicker": "Itu bukan tuduhan", "preco": "itu aritmetika",
     "sem_cap": True,
     "nar": "Itu bukan tuduhan ke bank mana pun. Itu aritmetika dari dua angka "
            "yang keduanya ada di aplikasimu."},
    {"layout": "item", "kicker": "Dan pajak", "preco": "masih di sisi bunga",
     "sem_cap": True,
     "nar": "Dan ingat, bunga yang kamu terima masih dipotong pajak, sedangkan "
            "biaya yang kamu bayar tidak dipotong apa pun."},
    {"layout": "item", "kicker": "Kalau hasilnya kecil", "preco": "itu juga jawaban",
     "sem_cap": True,
     "nar": "Kalau ternyata persenmu kecil dan bunganya lebih besar, itu juga "
            "jawaban yang berguna: berarti rekeningmu memang sudah cocok "
            "dengan saldomu dan kamu tidak perlu mengubah apa pun."},
    {"layout": "item", "kicker": "Selisihnya", "preco": "makin lebar",
     "sem_cap": True,
     "nar": "Jadi selisih yang kamu lihat tadi sebenarnya sedikit lebih lebar "
            "daripada yang tertulis."},
]

C5 = [
    {"layout": "titulo", "kicker": "Kenapa ini luput", "sub": "dari semua orang",
     "cap": "Kenapa potongan ini luput bertahun-tahun",
     "nar": "Kenapa hal sesederhana ini bisa luput bertahun-tahun dari orang "
            "yang sebenarnya hemat?"},
    {"layout": "item", "kicker": "Alasan satu", "preco": "tidak ada tagihan",
     "sem_cap": True,
     "nar": "Alasan pertama: tidak ada tagihan. Listrik dan air mengirim "
            "tagihan setiap bulan, dan angkanya kamu lihat."},
    {"layout": "item", "kicker": "Biaya bank", "preco": "langsung dipotong",
     "sem_cap": True,
     "nar": "Biaya bank tidak menagih. Dia langsung memotong dari saldo, dan "
            "yang kamu lihat cuma saldo yang sudah berkurang."},
    {"layout": "item", "kicker": "Alasan dua", "preco": "kamu tidak memilihnya",
     "sem_cap": True,
     "nar": "Alasan kedua: kamu tidak memilih pengeluaran ini. Semua "
            "pengeluaran lain kamu putuskan; yang ini datang sendiri."},
    {"layout": "item", "kicker": "Otak kita", "preco": "menghitung keputusan",
     "sem_cap": True,
     "nar": "Dan kita cenderung hanya menghitung apa yang kita putuskan. Yang "
            "datang sendiri tidak masuk hitungan bulanan siapa pun."},
    {"layout": "item", "kicker": "Alasan tiga", "preco": "nilainya kecil",
     "sem_cap": True,
     "nar": "Alasan ketiga, yang paling sederhana: nilainya kecil, dan hal "
            "kecil yang berulang selalu lebih besar daripada terasanya."},
    {"layout": "item", "kicker": "Sama seperti langganan", "preco": "yang lupa dibatalkan",
     "sem_cap": True,
     "nar": "Polanya sama persis dengan langganan aplikasi yang lupa kamu "
            "batalkan. Bedanya, langganan masih mengirim surel; potongan bank "
            "tidak mengirim apa-apa."},
    {"layout": "item", "kicker": "Karena itu", "preco": "hitung setahun, bukan sebulan",
     "sem_cap": True,
     "nar": "Karena itu langkah pertama tadi memakai dua belas bulan. Satu "
            "bulan tidak akan pernah membuatmu bertindak."},
]

C6 = [
    {"layout": "titulo", "kicker": "Sudah lihat angkanya", "sub": "lalu apa",
     "cap": "Empat hal yang bisa kamu lakukan",
     "nar": "Kamu sudah punya angkanya. Sekarang empat hal yang bisa kamu "
            "lakukan, dari yang paling gampang."},
    {"layout": "item", "kicker": "Satu", "preco": "cek saldo minimum",
     "sem_cap": True,
     "nar": "Pertama, cek apakah ada baris biaya di bawah saldo minimum. Kalau "
            "ada, itu biaya yang hilang hanya dengan menjaga saldo di atas "
            "batas."},
    {"layout": "item", "kicker": "Dua", "preco": "berhenti tarik di mesin lain",
     "sem_cap": True,
     "nar": "Kedua, lihat berapa kali kamu tarik tunai atau cek saldo di mesin "
            "bank lain. Itu biaya yang hilang hanya dengan berpindah mesin."},
    {"layout": "item", "kicker": "Tiga", "preco": "rekening yang menganggur",
     "sem_cap": True,
     "nar": "Ketiga, dan ini yang paling sering: rekening lama yang tidak kamu "
            "pakai lagi tapi tetap dipotong biaya administrasi setiap bulan."},
    {"layout": "item", "kicker": "Rekening menganggur", "preco": "bayar tanpa dipakai",
     "sem_cap": True,
     "nar": "Rekening yang tidak dipakai tetap membayar. Menutupnya secara "
            "resmi menghentikan potongan itu; membiarkannya tidak."},
    {"layout": "item", "kicker": "Empat", "preco": "bandingkan jenis rekening",
     "sem_cap": True,
     "nar": "Keempat, tanyakan ke bankmu sendiri apakah ada jenis rekening "
            "dengan biaya administrasi lebih rendah untuk profil sepertimu."},
    {"layout": "item", "kicker": "Sebelum menutup", "preco": "pindahkan yang menempel",
     "sem_cap": True,
     "nar": "Sebelum menutup rekening lama, pastikan tidak ada autodebet atau "
            "tagihan yang masih menempel di sana, supaya tidak ada yang gagal "
            "bayar setelahnya."},
    {"layout": "item", "kicker": "Aku tidak menyebut bank", "preco": "sengaja",
     "sem_cap": True,
     "nar": "Aku sengaja tidak menyebut bank mana pun, karena tarif berubah "
            "dan aku hanya mau kamu memakai angka yang bisa kamu lihat sendiri "
            "hari ini."},
]

C7 = [
    {"layout": "titulo", "kicker": "Sebelum pindah bank", "sub": "hitung dulu",
     "cap": "Sebelum pindah, hitung dulu",
     "nar": "Godaan setelah melihat angkanya adalah langsung pindah bank. "
            "Tunggu sebentar."},
    {"layout": "item", "kicker": "Pindah juga ada biayanya", "preco": "bukan cuma uang",
     "sem_cap": True,
     "nar": "Pindah bank juga ada ongkosnya, dan tidak semuanya berupa uang."},
    {"layout": "item", "kicker": "Gaji", "preco": "masuk ke rekening mana",
     "sem_cap": True,
     "nar": "Cek dulu ke mana gajimu masuk. Kalau kantormu hanya transfer ke "
            "bank tertentu, kamu akan menambah satu transfer setiap bulan."},
    {"layout": "item", "kicker": "Autodebet", "preco": "cicilan, listrik, langganan",
     "sem_cap": True,
     "nar": "Cek juga autodebet yang menempel di rekening itu: cicilan, "
            "tagihan, langganan. Semuanya harus dipindahkan satu per satu."},
    {"layout": "item", "kicker": "Hitung yang jujur", "preco": "selisih setahun",
     "sem_cap": True,
     "nar": "Hitungan yang jujur adalah selisih biaya setahun dikurangi ongkos "
            "pindah setahun. Kalau selisihnya kecil, tidak perlu pindah."},
    {"layout": "item", "kicker": "Sering kali", "preco": "cukup benahi yang ada",
     "sem_cap": True,
     "nar": "Sering kali tiga langkah di bagian sebelumnya sudah menghapus "
            "sebagian besar biayanya tanpa pindah ke mana pun."},
    {"layout": "item", "kicker": "Satu rekening lagi", "preco": "kadang lebih mahal",
     "sem_cap": True,
     "nar": "Dan hati-hati dengan jalan tengah yang kelihatan aman: membuka "
            "rekening baru tanpa menutup yang lama berarti kamu membayar dua "
            "biaya administrasi, bukan satu."},
    {"layout": "item", "kicker": "Dan kalau memang pindah", "preco": "jangan tinggalkan yang lama",
     "sem_cap": True,
     "nar": "Dan kalau kamu memang pindah, tutup yang lama secara resmi. "
            "Meninggalkannya terbuka berarti membayar dua rekening."},
]

C8 = [
    {"layout": "titulo", "kicker": "Sekarang, di aplikasimu", "sub": "tiga langkah",
     "cap": "Tiga langkah, sekarang",
     "nar": "Sebelum video ini selesai, buka aplikasimu dan lakukan tiga "
            "langkahnya."},
    {"layout": "item", "kicker": "Langkah 1", "preco": "jumlahkan 12 bulan",
     "sem_cap": True,
     "nar": "Satu: di mutasi dua belas bulan, jumlahkan setiap baris yang "
            "memuat kata biaya atau adm."},
    {"layout": "item", "kicker": "Langkah 2", "preco": "bagi 12",
     "sem_cap": True,
     "nar": "Dua: bagi dengan dua belas, dan kamu tahu harga bulanan "
            "rekeningmu."},
    {"layout": "lista", "kicker": "Langkah 3 — persentasenya", "sem_cap": True,
     "itens": ["total setahun ÷ saldo rata-rata × 100",
               "bandingkan dengan bunga tabunganmu",
               "kalau yang dibayar lebih besar, benahi"],
     "nar": "Tiga: bagi total setahun dengan saldo rata-ratamu, kali seratus, "
            "lalu bandingkan dengan bunga yang kamu terima."},
    {"layout": "item", "kicker": "Yang paling cepat", "preco": "rekening menganggur",
     "sem_cap": True,
     "nar": "Kalau kamu hanya sempat satu hal, cari rekening lama yang tidak "
            "kamu pakai. Itu biasanya potongan terbesar yang paling mudah "
            "dihentikan."},
    {"layout": "item", "kicker": "Tidak ada tarif bank di video ini",
     "preco": "alasannya di deskripsi", "sem_cap": True,
     "nar": "Sengaja tidak ada satu pun tarif bank di video ini, dan aku "
            "tulis alasannya di deskripsi."},
    {"layout": "item", "kicker": "Ulangi setahun lagi", "preco": "tarif berubah",
     "sem_cap": True,
     "nar": "Dan catat di kalendermu untuk mengulang hitungan ini tahun depan. "
            "Tarif berubah tanpa pengumuman, dan mutasimu adalah satu-satunya "
            "tempat perubahan itu terlihat."},
    {"layout": "cta", "kicker": "Berapa persen punyamu?",
     "sub": "tulis di komentar", "sem_cap": True,
     "nar": "Tulis di komentar berapa persen yang keluar. Di kanal ini setiap "
            "video berakhir dengan hitungan yang kamu kerjakan di uangmu "
            "sendiri; kalau berguna, subscribe."},
]

CENAS = C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8

# SHORT DELIBERADAMENTE CURTO: os dois maiores shorts do canal tem 26 s e 30 s,
# contra os 40 s do padrao da frota. A mudanca vem do numero DESTE canal.
SHORT = [
    {"layout": "titulo", "kicker": "Bank memotong tiap bulan",
     "sub": "tanpa kamu tekan apa pun", "sem_cap": True,
     "nar": "Setiap bulan bank memotong biaya dari saldomu, dan kamu tidak "
            "menekan apa pun."},
    {"layout": "titulo", "kicker": "Buka mutasi 12 bulan",
     "sub": "jumlahkan yang tertulis 'biaya'", "sem_cap": True,
     "nar": "Buka mutasi dua belas bulan dan jumlahkan setiap baris yang "
            "tertulis biaya atau adm."},
    {"layout": "titulo", "kicker": "Bagi saldo rata-ratamu",
     "sub": "kali 100", "sem_cap": True,
     "nar": "Bagi totalnya dengan saldo rata-ratamu, kali seratus. Itu persen "
            "yang kamu bayar per tahun."},
    {"layout": "titulo", "kicker": "Bandingkan dengan bunganya",
     "sub": "sering lebih besar", "sem_cap": True,
     "nar": "Bandingkan dengan bunga tabunganmu. Saldo kecil sering membayar "
            "lebih besar daripada yang diterima."},
    {"layout": "cta", "kicker": "Tiap video satu hitungan",
     "sub": "subscribe", "sem_cap": True,
     "nar": "Di sini tiap video satu hitungan di uangmu sendiri. Subscribe."},
]

THUMB = {"l1": "Berapa persen", "l2": "dipotong bank?"}

COPY = """# Biaya bank: berapa persen setahun yang kamu bayar untuk menyimpan uangmu

## JUDUL
Berapa Persen Setahun Kamu Bayar ke Bank? Hitung dari Mutasimu Sendiri

## JUDUL SHORT
Berapa persen dipotong bankmu?

## DESKRIPSI
Setiap bulan ada angka kecil yang keluar dari saldomu tanpa kamu menekan tombol apa pun. Bukan belanjamu, bukan transfermu — biaya. Di mutasi rekening namanya bermacam-macam: biaya administrasi, biaya kartu, biaya di bawah saldo minimum, biaya tarik tunai di mesin bank lain. Satu per satu kecil, dan justru karena kecil dia lolos dari perhatianmu setiap bulan.

Video ini tidak menyebut tarif bank mana pun. Angka yang menentukan ada di rekeningmu sendiri, dan hitungannya tiga langkah.

Langkah satu: buka mutasi rekening dua belas bulan terakhir — bukan satu bulan — dan jumlahkan setiap baris yang memuat kata biaya, adm, atau admin. Jangan lewatkan biaya transfer antarbank, tarik tunai di mesin bank lain, dan cek saldo di mesin bank lain.

Langkah dua: bagi total itu dengan dua belas. Itu harga bulanan rekeningmu, yang tidak pernah tertulis di mana pun.

Langkah tiga, dan ini yang menentukan: bagi total setahun dengan saldo rata-ratamu, lalu kalikan seratus. Hasilnya adalah persentase per tahun yang kamu bayar hanya untuk menyimpan uangmu sendiri.

Kenapa persentase dan bukan rupiah? Karena biaya administrasi biasanya angka tetap: bank memotong jumlah yang sama entah saldomu besar atau kecil. Dalam hitungan persen, yang saldonya paling kecil justru membayar paling mahal untuk layanan yang sama.

Lalu bandingkan persentase itu dengan bunga tabungan yang bank bayar ke kamu — angkanya ada di aplikasi yang sama. Untuk rekening bersaldo kecil, yang dibayar sering lebih besar daripada yang diterima. Itu bukan tuduhan ke bank mana pun; itu aritmetika dari dua angka yang keduanya ada di aplikasimu. Dan ingat: bunga yang kamu terima masih dipotong pajak, sedangkan biaya yang kamu bayar tidak.

Di video juga ada empat hal yang bisa kamu lakukan setelah melihat angkanya, termasuk yang paling sering terlewat — rekening lama yang sudah tidak dipakai tapi tetap dipotong biaya setiap bulan — dan hitungan jujur sebelum memutuskan pindah bank.

## BAB
{CAPITULOS}

## KOMENTAR DISEMATKAN
Tiga langkah, kerjakan sekarang: (1) mutasi 12 bulan → jumlahkan semua baris "biaya"/"adm". (2) bagi 12 → harga bulanan rekeningmu. (3) total setahun ÷ saldo rata-rata × 100 → persen per tahun yang kamu bayar. Bandingkan dengan bunga tabunganmu. Berapa persen punyamu?

## TAGAR
#BiayaAdmin #KeuanganPribadi #SetiapLevel

## TAG
biaya admin bank, biaya administrasi bulanan, mutasi rekening, cara hitung biaya bank, biaya tarik tunai bank lain, saldo minimum rekening, rekening tidak terpakai, bunga tabungan, keuangan pribadi, mengatur keuangan, hemat biaya bank, tutup rekening lama, biaya transfer antarbank, literasi keuangan, cek mutasi rekening

## PENGATURAN STUDIO
Kategori: Edukasi. Bahasa: Indonesia. Bukan untuk anak-anak. Mengandung media sintetis.

## MUSIK / LISENSI
{TRILHA}

## CATATAN TENTANG ANGKA
Video ini sengaja TIDAK memuat satu pun tarif bank — tidak ada tabel biaya administrasi, tidak ada nominal biaya transfer, tidak ada nama bank.

Alasannya jujur dan ini keputusanku: saat menyiapkan video ini aku mencoba memastikan batas tarif transfer BI-FAST langsung di situs Bank Indonesia dan situsnya tidak merespons. Pencarian hanya mengembalikan artikel berita, bukan sumber resmi. Aturannya di kanal ini jelas: angka yang tidak bisa dipastikan di sumber resmi tidak masuk ke video. Jadi angka itu tidak masuk.

Konsekuensinya bukan kelemahan: satu-satunya angka yang menentukan di video ini adalah angka yang kamu baca sendiri di mutasi rekeningmu — total baris "biaya", saldo rata-ratamu, dan bunga tabungan yang tertulis di aplikasimu. Ketiganya tidak perlu sumber pihak ketiga karena ketiganya milikmu.

Yang video ini TIDAK klaim: bahwa bank tertentu mahal atau murah, bahwa bank digital selalu lebih murah, dan bahwa pindah bank selalu menguntungkan. Justru ada satu bagian yang menghitung ongkos pindah sebelum memutuskan. Tarif berubah dan berbeda antar produk di bank yang sama — karena itu yang kupakai adalah mutasimu, bukan tabel siapa pun.
"""


def _copy_existente():
    import json
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "setiap-level-014.json")
    if os.path.exists(p):
        c = json.load(open(p, encoding="utf-8")).get("copy")
        if c:
            return c
    return COPY


SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-014",
    "idioma": "id",
    "voz": "id-ID-ArdiNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1B3A4B", "c1": "#E76F51", "c2": "#F4A259", "bg": "#F4F1EA"},
    "thumb": THUMB,
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
    grava(SPEC, "fabrica/specs/setiap-level-014.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
