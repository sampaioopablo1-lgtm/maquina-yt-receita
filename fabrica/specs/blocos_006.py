"""Blocos narrativos do setiap-level-006 — o teto legal da divida de pinjol.

PAUTA. Grupo de pares legitimo medido em 2026-08-05: n=7, mediana 7,6 views/dia,
outlier >= 23. Tres outliers, todos com a mesma assinatura — numero especifico
em prazo especifico: 1.759 v/d (painel com CFPs nomeados), 1.693 v/d ("hutang
miliaran, modal 500 ribu"), 892 v/d ("58 pinjol, 120 juta, 4 bulan"). O formato
morto e inequivoco: guia generico. "Strategi Melunasi Hutang | Panduan Lengkap"
marca 0,3 v/d.

FRONTEIRA EDITORIAL. O nicho vizinho de "galbay" (calote proposital) tem 5.708
videos e entrega bem — 397 e 280 v/d nas amostras. Fica de fora. Este video diz
o contrario: existe um teto legal, e conhece-lo e o que devolve o controle.

TESE. Juros mais multa nao podem passar de 100% do principal. Voce nunca deve
legalmente mais que o dobro do que pegou.

FONTES (SEOJK 19/2023, confirmada em multiplos veiculos em 2026-08-05):
  - Juros consumo: 0,3%/dia (2024) -> 0,2%/dia (2025) -> 0,1%/dia (2026)
  - Juros produtivo: 0,1%/dia -> 0,067%/dia (2026)
  - Multa por atraso: maximo 0,1%/dia
  - Teto total de juros + multa: 100% do principal

IDIOMA. Toda a narracao e em indonesio. A primeira versao deste arquivo derrapou
para portugues a partir do capitulo 2 e teria produzido um video inutilizavel —
o linter de narracao nao pega troca de idioma, so o autor pega.

DIMENSIONAMENTO: duracao = chars/20,58 + frases x 0,96 + cenas x 1,08. Alvo 840s.
"""

BLOCOS = [
 ("Angka yang tidak pernah disebut", [
  ("titulo", "Kamu sedang membayar", "tanpa tahu batasnya",
   "Kalau kamu sedang membayar pinjaman online sekarang, kemungkinan besar kamu tahu berapa cicilanmu bulan ini. Dan kemungkinan besar kamu tidak tahu berapa maksimal yang boleh ditagih dari kamu sampai kapan pun."),
  ("titulo", "Kedua hal itu", "tidak sama",
   "Aplikasi menampilkan yang pertama dengan huruf besar di layar depan. Yang kedua tidak muncul di layar mana pun, padahal justru yang kedua adalah pagar yang melindungi kamu."),
  ("item", "Video ini bukan", "cara menghindari bayar",
   "Sebelum lanjut, satu hal perlu jelas. Video ini bukan tentang cara menghindari pembayaran, dan bukan tentang menunggu utang hangus dengan sendirinya."),
  ("titulo", "Itu jalan lain", "dan bukan jalan ini",
   "Ada banyak konten yang membahas jalan itu, dan akibatnya bukan urusan video ini. Yang dibahas di sini adalah angka yang berlaku secara hukum, dan apa yang angka itu ubah dalam posisimu."),
  ("lista", "Empat angka", ["Bunga harian", "Denda harian", "Batas total", "Kapan batas tercapai"],
   "Empat angka, semuanya dari aturan yang berlaku sekarang, dan semuanya bisa kamu periksa sendiri di sumber resmi."),
  ("item", "Kenapa ini penting", "posisi tawar",
   "Karena orang yang tahu berapa maksimal bisa ditagih darinya duduk di meja yang berbeda dari orang yang tidak tahu."),
  ("titulo", "Mari mulai", "dari yang paling dasar",
   "Mari mulai dari angka yang paling sering disalahpahami, dan yang justru turun tahun ini:"),
 ]),
 ("Bunga harian, dan berapa persisnya", [
  ("titulo", "Bunga pinjol", "dihitung per hari",
   "Bunga pinjaman online tidak dihitung per bulan seperti kredit bank. Ia dihitung per hari, dan itu satu-satunya alasan angkanya terlihat kecil di layar."),
  ("item", "Untuk pinjaman konsumtif", "nol koma satu persen per hari",
   "Untuk pinjaman konsumtif jangka pendek, batas maksimalnya sekarang nol koma satu persen per hari."),
  ("titulo", "Angka itu turun", "dan turun dua kali",
   "Dan angka itu tidak selalu segitu. Ia turun, dan turun bertahap dengan tanggal yang jelas di kalender."),
  ("barras", "Bunga harian konsumtif", ["2024", "2025", "2026"], [100, 67, 33],
   "Di dua ribu dua puluh empat batasnya nol koma tiga persen per hari. Di dua ribu dua puluh lima, nol koma dua persen. Sekarang, nol koma satu persen."),
  ("item", "Artinya", "sepertiga dari dulu",
   "Artinya siapa pun yang meminjam nominal sama hari ini membayar sepertiga bunga harian dibanding dua tahun lalu, selama pemberi pinjamannya legal."),
  ("titulo", "Untuk pinjaman produktif", "angkanya lain lagi",
   "Untuk pinjaman produktif, yaitu yang diambil sebagai modal usaha kecil, batasnya bahkan lebih rendah."),
  ("item", "Produktif di 2026", "nol koma nol enam tujuh persen",
   "Nol koma nol enam tujuh persen per hari, dari sebelumnya nol koma satu persen."),
  ("titulo", "Selisih itu", "bukan kebetulan",
   "Selisih antara keduanya bukan kebetulan. Uang yang dipinjam untuk berproduksi memang dibuat lebih murah daripada uang yang dipinjam untuk konsumsi, dan itu tertulis di aturannya."),
  ("titulo", "Sekarang bagian", "yang jarang dipisahkan",
   "Sekarang bagian yang jarang dipisahkan dengan benar, dan di situlah hitungan kebanyakan orang mulai kacau:"),
 ]),
 ("Denda, yang dihitung terpisah", [
  ("titulo", "Terlambat", "menyalakan jam kedua",
   "Ketika pembayaran terlambat, bukan bunganya yang naik. Yang terjadi adalah sebuah jam kedua mulai berjalan di sebelah jam pertama."),
  ("item", "Denda keterlambatan", "maksimal nol koma satu persen per hari",
   "Denda keterlambatan itu punya batas sendiri: maksimal nol koma satu persen per hari."),
  ("titulo", "Ia tidak menggantikan bunga", "ia menambah",
   "Dan ia tidak menggantikan bunga. Ia menambah. Orang yang menunggak pinjaman konsumtif bisa sedang menumpuk keduanya sekaligus."),
  ("item", "Digabung", "nol koma dua persen per hari",
   "Digabung, pada kondisi terburuk yang masih legal, jadi nol koma dua persen per hari."),
  ("titulo", "Terlihat kecil", "dan di situ jebakannya",
   "Nol koma dua persen per hari terlihat kecil karena kepala kita membandingkannya dengan bunga bulanan. Keduanya tidak sebanding."),
  ("item", "Dalam tiga puluh hari", "enam persen",
   "Dalam tiga puluh hari, nol koma dua persen per hari menjadi enam persen. Atas nilai pinjaman, setiap bulan."),
  ("titulo", "Untuk utang produktif", "dasarnya berbeda",
   "Untuk utang produktif dendanya juga dibatasi nol koma satu persen per hari, tetapi dihitung dari sisa pokok pinjaman, bukan dari nilai awal."),
  ("item", "Perbedaan itu", "mengubah angka akhirnya",
   "Perbedaan itu terdengar teknis padahal tidak: ia mengubah berapa yang kamu tanggung di bulan kedua belas."),
  ("titulo", "Dan justru di sini", "masuk angka utamanya",
   "Dan justru di sini masuk angka yang menjadi judul video ini:"),
 ]),
 ("Pagar yang hampir tidak ada yang tahu", [
  ("titulo", "Ada batas", "untuk totalnya",
   "Ada batas untuk totalnya. Bukan untuk cicilannya, bukan untuk bunga hariannya: untuk jumlah seluruh yang boleh ditagih di luar pokok yang kamu terima."),
  ("item", "Batasnya", "seratus persen dari pokok",
   "Bunga ditambah denda tidak boleh melebihi seratus persen dari nilai pokok pinjaman."),
  ("titulo", "Satu kalimat", "kamu tidak pernah berutang tiga kali lipat",
   "Diterjemahkan ke isi dompetmu: total yang bisa dituntut darimu paling banyak dua kali lipat dari yang kamu pinjam."),
  ("item", "Pinjam lima juta", "maksimal sepuluh juta",
   "Pinjam lima juta rupiah. Maksimal yang sah ditagih darimu sepuluh juta rupiah, dihitung dari semuanya."),
  ("titulo", "Tidak peduli", "berapa bulan berlalu",
   "Dan itu tidak bergantung pada berapa bulan sudah lewat. Lewat dua belas bulan atau tiga puluh enam bulan, batasnya sama."),
  ("titulo", "Karena itu", "batas ini mengubah percakapan",
   "Karena itu mengetahui angka ini mengubah percakapan. Utang orang yang menunggak tidak tumbuh selamanya, ia berhenti di titik yang sudah ditentukan."),
  ("item", "Yang tidak tahu", "membayar di atas batas",
   "Yang tidak tahu hal ini membayar tagihan yang sudah melewati batas, sambil mengira dirinya masih berutang."),
  ("titulo", "Jadi pertanyaan yang berguna", "berubah jadi hitungan",
   "Jadi pertanyaan yang berguna bukan lagi berapa utang saya, melainkan sebuah hitungan sederhana:"),
 ]),
 ("Kapan batas itu tercapai", [
  ("titulo", "Hitungannya", "muat dalam satu baris",
   "Hitungannya muat dalam satu baris. Bunga ditambah denda, pada kondisi terburuk yang legal, jadi nol koma dua persen per hari."),
  ("item", "Untuk mencapai seratus persen", "lima ratus hari",
   "Untuk menumpuk seratus persen dari pokok pada nol koma dua persen per hari dibutuhkan lima ratus hari."),
  ("item", "Lima ratus hari", "sekitar enam belas bulan",
   "Lima ratus hari sedikit lebih dari enam belas bulan. Satu tahun empat bulan."),
  ("titulo", "Setelah titik itu", "angkanya membeku",
   "Setelah titik itu, angkanya membeku. Tidak ada lagi yang boleh ditambahkan secara sah, sejauh apa pun waktu berjalan."),
  ("titulo", "Kalau tidak menunggak", "hanya bunga yang jalan",
   "Kalau tidak ada keterlambatan dan hanya bunga nol koma satu persen per hari yang berjalan, batasnya butuh waktu dua kali lipat."),
  ("item", "Seribu hari", "hampir tiga tahun",
   "Seribu hari, atau hampir tiga tahun. Itulah rentang paling panjang di mana utang konsumtif yang legal masih bisa tumbuh."),
  ("titulo", "Simpan dua angka ini", "keduanya adalah penggaris",
   "Simpan dua angka ini. Lima ratus hari kalau menunggak, seribu hari kalau tidak. Keduanya adalah penggaris untuk memeriksa tagihan apa pun yang datang."),
  ("titulo", "Tapi ada satu syarat", "yang harus disebut terang-terangan",
   "Tapi ada satu syarat di balik semua ini, dan syarat itu harus disebut terang-terangan:"),
 ]),
 ("Apa yang berada di luar pagar", [
  ("titulo", "Semua ini berlaku", "untuk pemberi pinjaman terdaftar",
   "Semua yang dibahas sampai di sini berlaku untuk pemberi pinjaman yang terdaftar dan diawasi. Bagi yang beroperasi di luar pendaftaran, tidak ada batas apa pun, karena tidak ada aturan yang ia ikuti."),
  ("item", "Pemeriksaan pertama", "adalah status terdaftar",
   "Karena itu pemeriksaan pertama, sebelum membahas angka mana pun, adalah apakah pemberi pinjamanmu ada di daftar resmi penyelenggara terdaftar."),
  ("titulo", "Daftar itu", "publik dan diperbarui",
   "Daftar itu bersifat publik, diterbitkan oleh otoritas pengawas, dan diperbarui secara berkala. Memeriksanya makan waktu beberapa menit saja."),
  ("titulo", "Kalau namanya tidak ada", "percakapannya berbeda",
   "Kalau namanya tidak ada di sana, percakapannya berubah sifat sepenuhnya, dan menjadi urusan pelaporan, bukan negosiasi nominal."),
  ("item", "Satu tanda praktis", "penagihan di luar batas",
   "Satu tanda praktis yang muncul lebih awal: penagihan yang melibatkan kontak di ponselmu atau menekan orang-orang terdekat berada di luar cara yang diizinkan, berapa pun nilai utangnya."),
  ("titulo", "Ini tidak menghapus utang", "dan itu penting dikatakan",
   "Mengakui hal ini tidak menghapus nominal yang sudah kamu terima, dan tidak jujur kalau saya menyiratkan sebaliknya. Yang berubah adalah kepada siapa kamu bertanggung jawab, dan dengan batas apa."),
  ("titulo", "Dengan status terperiksa", "sisanya bagian praktis",
   "Dengan status terdaftar sudah diperiksa dan angka-angka di tangan, sisanya adalah bagian praktis, yaitu apa yang dikerjakan besok pagi:"),
 ]),
 ("Apa yang dilakukan dengan angka ini", [
  ("titulo", "Tiga langkah", "tidak satu pun butuh uang baru",
   "Tiga langkah, dan tidak satu pun dari ketiganya menuntut uang yang belum kamu punya."),
  ("item", "Pertama", "tulis pokok tiap utang",
   "Pertama, tulis nilai pokok setiap utang secara terpisah. Bukan saldo yang ditampilkan aplikasi, melainkan berapa yang masuk ke rekeningmu di hari pencairan."),
  ("titulo", "Selisih itu", "adalah seluruh hitungannya",
   "Selisih antara keduanya adalah seluruh hitungan ini. Saldo yang tampil sudah memuat semua yang ditambahkan; pokok adalah dasar yang dipakai menghitung batas."),
  ("item", "Kedua", "bandingkan tagihan dengan dua kali pokok",
   "Kedua, bandingkan total yang sudah ditagih dengan dua kali nilai pokok. Kalau totalnya sudah lewat, ada tagihan di atas batas, dan itu bisa dipersoalkan secara resmi."),
  ("item", "Ketiga", "bayar berdasarkan biaya harian",
   "Ketiga, urutkan utangmu berdasarkan biaya hariannya, bukan berdasarkan besarnya. Utang kecil yang menunggak berjalan di nol koma dua persen per hari dan memakan lebih banyak daripada utang besar yang lancar."),
  ("titulo", "Urutan itu", "melawan naluri",
   "Urutan itu melawan naluri, karena utang yang besar terasa lebih menakutkan. Tapi yang menguras bulanmu adalah yang berjalan paling cepat, bukan yang paling besar."),
  ("titulo", "Tidak satu pun dari tiga", "melunasi apa pun",
   "Tidak satu pun dari ketiga langkah itu melunasi apa pun dengan sendirinya, dan menjanjikan sebaliknya akan jadi kebohongan. Yang mereka kerjakan adalah hal lain."),
  ("item", "Yang mereka kerjakan", "mengembalikan angkanya",
   "Mereka mengembalikan angka yang sebenarnya kepadamu: berapa lagi yang masih boleh bertambah, sampai kapan, dan berapa yang sudah melewati batas."),
  ("titulo", "Dan itulah", "yang mengubah posisimu",
   "Dan memiliki angka itu, bukan kebaikan hati penagih, yang mengubah posisimu dalam percakapan."),
  ("cta", "Angka mana", "yang belum kamu tahu",
   "Dari empat angka di video ini, mana yang belum kamu ketahui sebelum menonton? Tulis di kolom komentar, karena itu membantu saya tahu bagian mana yang perlu dijelaskan lebih hati-hati lain kali."),
 ]),
]
