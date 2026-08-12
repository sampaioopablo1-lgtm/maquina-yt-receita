#!/usr/bin/env python3
"""Gera a spec do setiap-level-004 — "Cara Atur Gaji 2026", sistema de 4 pilares.

A spec sai com ~170 cenas e 50KB de JSON. Escrever isso a mao e caro e fragil;
aqui o texto fica compacto e o script cuida da repeticao de layout, dos capitulos
e da regra do sem_cap nas cenas-ponte.

Fonte da pauta (PASSO 0, 05/08/2026, n=41 videos longos de 90 dias):
  mediana do nicho ........... 27 views/dia
  familia "sistema completo" .. 4757 v/d  <- este formato
  outlier .................... Rory Asyari x Ligwina Hananto, 9467 v/d (350x)
  familia morta .............. "menabung 100 juta" 1,0 v/d; ensaio motivacional 1,0
"""
import json, os

VOZ = "id-ID-ArdiNeural"          # 15,1 chars/s — a voz mais rapida medida
PALETA = {"ink": "#12303A", "c1": "#1B7A8C", "c2": "#F2B134", "bg": "#F0F6F7"}

# Cada cena: (layout, kicker, sub|itens, narracao). alturas entra em barras.
# O primeiro item de cada capitulo recebe 'cap'; os demais viram sem_cap.
CAPS = []


def cap(titulo, cenas):
    CAPS.append((titulo, cenas))


# ============================ 1 ============================
cap("Kenapa gaji selalu habis", [
 ("titulo", "Rp0", "sisa di tanggal 25", "Tanggal dua puluh lima, saldo tinggal nol. Bukan karena kamu boros. Karena uangmu tidak punya urutan."),
 ("titulo", "Rp0", "sisa di tanggal 25", "Sebagian besar konten keuangan memberi kamu satu tips. Menabung. Investasi. Hemat kopi."),
 ("titulo", "1 tips", "= 1 lubang tertutup", "Satu tips menutup satu lubang. Sementara empat lubang lain tetap terbuka dan uangmu tetap bocor."),
 ("lista", "4 pilar", ["Dana darurat", "Cicilan", "Investasi", "Pensiun"], "Ada empat pilar. Dana darurat, cicilan, investasi, dan pensiun. Kamu butuh keempatnya bekerja bersama."),
 ("lista", "4 pilar", ["Dana darurat", "Cicilan", "Investasi", "Pensiun"], "Dan yang paling sering dilewatkan: urutannya. Mengerjakan pilar tiga sebelum pilar satu adalah alasan paling umum sistem keuangan runtuh."),
 ("titulo", "2026", "yang berubah tahun ini", "Video ini memakai angka dua ribu dua puluh enam. Upah minimum, iuran BPJS, dan batas upah pensiun semuanya berubah tahun ini."),
 ("titulo", "5-7%", "kenaikan UMP 2026", "Upah minimum provinsi dua ribu dua puluh enam naik antara lima sampai tujuh persen, berbeda tiap daerah mengikuti biaya hidup dan inflasi setempat."),
 ("titulo", "5-7%", "kenaikan UMP 2026", "Kedengarannya bagus. Tapi kenaikan upah tanpa sistem hanya menaikkan pengeluaran, bukan kekayaan."),
 ("item", "Pertanyaan", "ke mana perginya?", "Coba jujur. Kalau gajimu naik tujuh persen tahun ini, apakah tabunganmu ikut naik tujuh persen?"),
 ("item", "Pertanyaan", "ke mana perginya?", "Kalau jawabannya tidak, masalahnya bukan jumlah. Masalahnya struktur."),
 ("titulo", "Sistem", "bukan motivasi", "Yang akan kamu dapat di sini bukan motivasi. Empat pilar, urutannya, angkanya, dan cara mengeceknya sendiri."),
 ("titulo", "Sistem", "bukan motivasi", "Kalau kamu hanya punya waktu untuk satu bagian, tonton bagian urutan. Di situ letak kesalahan yang paling mahal."),
 ("barras", "Prioritas", ["Darurat", "Cicilan", "Investasi", "Pensiun"], [95, 80, 55, 40], "Bayangkan piramida. Dasar yang lebar menahan yang di atas. Kalau dasarnya tipis, seluruh bangunan bergantung pada keberuntungan."),
 ("barras", "Prioritas", ["Darurat", "Cicilan", "Investasi", "Pensiun"], [95, 80, 55, 40], "Kebanyakan orang membangun dari atas. Beli saham dulu, baru mikir dana darurat kalau sudah kejadian."),
 ("titulo", "1 kejadian", "menghapus 2 tahun", "Satu kejadian tak terduga bisa menghapus dua tahun investasi. Bukan karena pasarnya jelek, tapi karena kamu terpaksa jual di waktu yang salah."),
 ("titulo", "1 kejadian", "menghapus 2 tahun", "Itu bukan risiko pasar. Itu risiko struktur. Dan struktur bisa kamu perbaiki bulan ini juga."),
 ("item", "Aturan", "urutan mengalahkan jumlah", "Satu aturan yang perlu kamu bawa sampai akhir video. Urutan mengalahkan jumlah."),
 ("item", "Aturan", "urutan mengalahkan jumlah", "Orang dengan gaji lebih kecil tapi urutan benar akan menang atas orang bergaji besar dengan urutan acak. Selalu."),
 ("titulo", "Pilar 1", "dana darurat", "Kita mulai dari dasar piramida. Pilar pertama, dan satu-satunya yang tidak boleh kamu lompati."),
 ("titulo", "Pilar 1", "dana darurat", "Dana darurat. Dan pertanyaannya bukan penting atau tidak. Pertanyaannya berapa rupiah, tepatnya."),
])

# ============================ 2 ============================
cap("Pilar 1 — dana darurat: angkanya", [
 ("titulo", "Bukan gaji", "tapi pengeluaran", "Kesalahan pertama soal dana darurat: menghitungnya dari gaji. Yang benar dihitung dari pengeluaran bulanan."),
 ("titulo", "Bukan gaji", "tapi pengeluaran", "Kalau gajimu lima juta tapi pengeluaranmu tiga juta lima ratus ribu, dasar hitungannya tiga juta lima ratus ribu."),
 ("item", "Kenapa", "kamu berhemat saat krisis", "Alasannya sederhana. Saat pendapatan berhenti, kamu tidak hidup dengan gaya gaji penuh. Kamu hidup dengan biaya bertahan."),
 ("lista", "Biaya bertahan", ["Sewa atau cicilan rumah", "Makan", "Transportasi kerja", "Listrik dan air", "Cicilan wajib"], "Biaya bertahan itu: tempat tinggal, makan, transportasi untuk mencari kerja, listrik dan air, serta cicilan yang tidak bisa ditunda."),
 ("lista", "Bukan biaya bertahan", ["Langganan hiburan", "Nongkrong", "Belanja pakaian", "Liburan"], "Bukan biaya bertahan: langganan hiburan, nongkrong, belanja pakaian, liburan. Ini yang berhenti duluan dan memang seharusnya begitu."),
 ("titulo", "3 sampai 6", "bulan pengeluaran", "Angka standarnya tiga sampai enam bulan pengeluaran bertahan. Tapi standar itu dibuat untuk pekerja dengan gaji tetap."),
 ("titulo", "6 sampai 12", "kalau penghasilanmu tidak tetap", "Kalau penghasilanmu tidak tetap — pedagang, ojek daring, freelancer, pekerja harian — angkanya naik jadi enam sampai dua belas bulan."),
 ("item", "Alasan", "pendapatan tidak rata", "Alasannya bukan karena kamu lebih berisiko sebagai orang. Karena pendapatanmu tidak rata, dan bulan buruk bisa datang berturut-turut."),
 ("barras", "Target", ["Gaji tetap", "Campuran", "Harian"], [45, 70, 100], "Tiga profil, tiga target. Gaji tetap tiga sampai enam bulan. Penghasilan campuran enam bulan. Penghasilan harian sembilan sampai dua belas bulan."),
 ("titulo", "Contoh", "pengeluaran Rp3,5 juta", "Mari pakai angka nyata. Pengeluaran bertahan tiga juta lima ratus ribu rupiah per bulan."),
 ("titulo", "Rp21 juta", "target 6 bulan", "Enam bulan berarti dua puluh satu juta rupiah. Angka itu terlihat mustahil kalau kamu lihat sekaligus."),
 ("item", "Jangan lihat total", "lihat cicilan bulanan", "Jadi jangan lihat totalnya. Lihat cicilan bulanannya, persis seperti kamu melihat cicilan motor."),
 ("barras", "Waktu tempuh", ["Rp500rb/bln", "Rp1jt/bln", "Rp1,75jt/bln"], [100, 50, 29], "Lima ratus ribu per bulan: empat puluh dua bulan. Satu juta per bulan: dua puluh satu bulan. Satu juta tujuh ratus lima puluh ribu: dua belas bulan."),
 ("item", "Realistis", "mulai dari 1 bulan", "Kalau semua itu terasa jauh, targetmu bukan enam bulan. Targetmu satu bulan. Satu bulan pengeluaran sudah mengubah cara kamu tidur."),
 ("titulo", "Rekening", "harus terpisah", "Syarat kedua, dan ini yang sering merusak: dana darurat harus di rekening terpisah, tanpa kartu debit yang kamu bawa."),
 ("titulo", "Rekening", "harus terpisah", "Uang yang bisa diambil dalam sepuluh detik bukan dana darurat. Itu saldo."),
 ("lista", "Tempat yang cocok", ["Rekening bank lain tanpa kartu", "Deposito jangka pendek", "Reksa dana pasar uang"], "Tempat yang cocok: rekening bank lain tanpa kartu, deposito jangka pendek, atau reksa dana pasar uang. Semua bisa cair dalam hitungan hari."),
 ("lista", "Tempat yang salah", ["Saham", "Kripto", "Emas fisik", "Uang di rumah"], "Tempat yang salah: saham, kripto, emas fisik, atau uang tunai di rumah. Dua pertama bisa turun tepat saat kamu butuh."),
 ("item", "Uji", "bisa cair dalam 3 hari?", "Ujinya satu kalimat. Bisakah uang ini cair penuh dalam tiga hari tanpa kehilangan nilai? Kalau tidak, itu bukan dana darurat."),
 ("titulo", "Pilar 2", "cicilan", "Dana darurat sudah punya angka. Sekarang pilar kedua, dan ini yang paling sering diam-diam menghabiskan gaji."),
 ("titulo", "Pilar 2", "cicilan", "Cicilan. Bukan soal boleh atau tidak boleh berhutang. Soal berapa batasnya."),
])

# ============================ 3 ============================
cap("Pilar 2 — cicilan dan batas 30%", [
 ("titulo", "30%", "batas total cicilan", "Angka yang perlu kamu ingat: tiga puluh persen. Total seluruh cicilanmu tidak boleh melewati tiga puluh persen penghasilan bersih bulanan."),
 ("titulo", "30%", "batas total cicilan", "Ini bukan angka motivasi. Ini rasio yang dipakai bank saat menilai apakah kamu layak diberi pinjaman."),
 ("item", "Penghasilan bersih", "setelah potongan", "Penghasilan bersih artinya setelah potongan. Setelah pajak, setelah BPJS, setelah semua yang dipotong sebelum uang sampai ke rekeningmu."),
 ("titulo", "Contoh", "bersih Rp4 juta", "Contoh: penghasilan bersih empat juta rupiah. Batas total cicilanmu satu juta dua ratus ribu rupiah."),
 ("barras", "Cicilan Rp4jt bersih", ["Aman <20%", "Batas 30%", "Bahaya >40%"], [53, 80, 100], "Di bawah delapan ratus ribu: aman. Sampai satu juta dua ratus ribu: batas. Di atas satu juta enam ratus ribu: kamu sedang menuju masalah."),
 ("lista", "Yang dihitung", ["Cicilan rumah", "Cicilan kendaraan", "Paylater", "Kartu kredit", "Pinjaman online", "Utang keluarga"], "Yang dihitung: cicilan rumah, kendaraan, paylater, kartu kredit, pinjaman daring, dan utang ke keluarga. Semuanya."),
 ("item", "Paylater", "tetap cicilan", "Paylater terasa bukan utang karena jumlahnya kecil dan prosesnya cepat. Tapi bagi rasio penghasilanmu, dia utang penuh."),
 ("item", "Tiga paylater", "= satu cicilan motor", "Tiga paylater dua ratus ribu adalah enam ratus ribu sebulan. Itu setara satu cicilan motor yang tidak pernah kamu putuskan untuk ambil."),
 ("titulo", "Hitung dulu", "sebelum lanjut", "Berhenti sebentar. Jumlahkan semua cicilanmu bulan ini, lalu bagi dengan penghasilan bersih. Angka itu menentukan tiga pilar berikutnya."),
 ("titulo", "Di atas 30%?", "hentikan pilar 3 dan 4", "Kalau hasilnya di atas tiga puluh persen, jangan lanjut ke investasi. Bunga utangmu hampir pasti lebih tinggi dari imbal hasil investasimu."),
 ("barras", "Bunga per tahun", ["Investasi wajar", "Kartu kredit", "Pinjol"], [12, 60, 100], "Investasi yang wajar memberi sekitar delapan sampai dua belas persen setahun. Kartu kredit menagih sekitar tiga puluh persen. Pinjaman daring bisa jauh lebih tinggi."),
 ("item", "Logikanya", "utang mahal dulu", "Membayar utang tiga puluh persen adalah keuntungan tiga puluh persen yang dijamin. Tidak ada investasi yang bisa menjanjikan itu."),
 ("lista", "Urutan melunasi", ["Bunga tertinggi dulu", "Lalu yang menengah", "Terakhir yang termurah"], "Urutan melunasi: bunga tertinggi lebih dulu, apa pun jumlahnya. Ini menghemat uang paling banyak."),
 ("item", "Cara lain", "yang terkecil dulu", "Ada cara kedua: lunasi yang jumlahnya paling kecil dulu supaya cepat terasa berhasil. Lebih mahal sedikit, tapi lebih banyak orang bertahan sampai selesai."),
 ("item", "Pilih", "yang kamu selesaikan", "Pilih yang benar-benar akan kamu jalankan. Metode terbaik adalah yang kamu selesaikan, bukan yang paling rapi di atas kertas."),
 ("titulo", "Jangan nol", "dana darurat tetap jalan", "Satu peringatan. Saat melunasi utang, jangan hentikan dana darurat sampai nol rupiah."),
 ("titulo", "Jangan nol", "dana darurat tetap jalan", "Tanpa penyangga sama sekali, kejadian kecil memaksa kamu berhutang lagi. Kamu berputar di tempat yang sama."),
 ("item", "Aman", "1 bulan sebagai penyangga", "Tahan satu bulan pengeluaran sebagai penyangga, lalu kerahkan sisanya ke utang. Setelah utang bersih, kembali kejar enam bulan."),
 ("titulo", "Pilar 3", "investasi", "Dua pilar dasar sudah berdiri. Baru sekarang investasi masuk akal."),
 ("titulo", "Pilar 3", "investasi", "Dan pertanyaan pertamanya bukan beli apa. Pertanyaannya untuk kapan."),
 ("item", "Bukan", "instrumen dulu", "Orang bertanya saham atau emas sebelum tahu uangnya dipakai kapan. Itu seperti memilih kendaraan sebelum tahu tujuannya."),
])

# ============================ 4 ============================
cap("Pilar 3 — investasi, setelah dua yang pertama", [
 ("lista", "Tentukan dulu", ["Untuk kapan uangnya dipakai", "Berapa besar target", "Seberapa tahan kalau turun"], "Tiga hal ditentukan sebelum instrumen: kapan uangnya dipakai, berapa targetnya, dan seberapa tahan kamu melihat nilainya turun."),
 ("barras", "Jangka waktu", ["<2 tahun", "2-5 tahun", ">5 tahun"], [30, 65, 100], "Di bawah dua tahun: jangan ambil risiko. Dua sampai lima tahun: risiko sedang. Di atas lima tahun: risiko lebih tinggi jadi masuk akal."),
 ("item", "Kurang 2 tahun", "pasar uang atau deposito", "Uang yang dipakai kurang dari dua tahun sebaiknya di reksa dana pasar uang atau deposito. Imbal hasilnya kecil, tapi tidak akan mengecewakanmu di bulan kamu butuh."),
 ("item", "Lebih 5 tahun", "baru saham masuk akal", "Uang yang tidak disentuh lebih dari lima tahun boleh masuk ke saham atau reksa dana saham. Waktu adalah yang menyerap penurunan."),
 ("titulo", "Rutin", "mengalahkan besar", "Kebiasaan yang paling menentukan bukan besarnya setoran. Tapi rutinnya."),
 ("titulo", "Rp200 ribu", "setiap bulan, otomatis", "Dua ratus ribu rupiah setiap bulan secara otomatis lebih berhasil daripada dua juta sekali setahun kalau lagi ingat."),
 ("item", "Alasan", "kamu tidak perlu memutuskan", "Alasannya bukan matematika. Karena setoran otomatis tidak butuh keputusan, dan keputusan adalah bagian yang paling sering gagal."),
 ("barras", "Rp200rb/bln, 8% setahun", ["5 tahun", "10 tahun", "20 tahun"], [15, 37, 100], "Dua ratus ribu per bulan dengan imbal delapan persen: sekitar empat belas juta dalam lima tahun, tiga puluh enam juta dalam sepuluh tahun, seratus delapan belas juta dalam dua puluh tahun."),
 ("item", "Perhatikan", "lompatannya di akhir", "Perhatikan bentuknya. Sepuluh tahun kedua memberi jauh lebih banyak daripada sepuluh tahun pertama, dengan setoran yang persis sama."),
 ("titulo", "Itu bunga", "atas bunga", "Itulah bunga berbunga. Dan satu-satunya bahan yang tidak bisa kamu beli untuk itu adalah waktu."),
 ("titulo", "Mulai kecil", "lebih baik dari mulai nanti", "Karena itu mulai dengan sepuluh ribu rupiah lebih baik daripada menunggu sampai punya sepuluh juta."),
 ("lista", "Biaya yang menggerus", ["Biaya pembelian", "Biaya pengelolaan tahunan", "Pajak"], "Yang menggerus diam-diam: biaya pembelian, biaya pengelolaan tahunan, dan pajak. Selisih satu persen setahun terasa besar setelah sepuluh tahun."),
 ("item", "Cek", "biaya pengelolaan", "Sebelum membeli produk apa pun, cari biaya pengelolaan tahunannya. Kalau tidak ketemu dalam dua menit, itu sendiri sudah jawaban."),
 ("item", "Hindari", "yang menjanjikan pasti", "Dan hindari apa pun yang menjanjikan hasil pasti setiap bulan. Imbal hasil yang dijamin tinggi adalah tanda paling tua dari penipuan."),
 ("titulo", "Terdaftar", "cek izinnya", "Pastikan produk dan platformnya terdaftar dan diawasi Otoritas Jasa Keuangan. Ini pengecekan lima menit yang menyelamatkan tabungan bertahun-tahun."),
 ("lista", "Tiga pertanyaan", ["Siapa yang mengelola?", "Bagaimana cara cairnya?", "Apa yang terjadi kalau saya butuh mendadak?"], "Tiga pertanyaan sebelum menyetor: siapa yang mengelola, bagaimana cara mencairkan, dan apa yang terjadi kalau kamu butuh mendadak."),
 ("item", "Kalau ragu", "jangan setor", "Kalau salah satu jawabannya tidak jelas, jangan setor. Tidak menyetor bukan kehilangan kesempatan. Itu keputusan."),
 ("titulo", "Pilar 4", "pensiun", "Pilar keempat adalah yang paling mudah ditunda, karena akibatnya baru terasa tiga puluh tahun lagi."),
 ("titulo", "Pilar 4", "pensiun", "Dan justru karena itu, pilar ini yang paling mahal kalau ditunda."),
 ("item", "Kabar baik", "sebagian sudah jalan", "Kabar baiknya: kalau kamu pekerja formal, sebagian pilar ini sudah berjalan tanpa kamu sadari. Tapi hampir pasti tidak cukup."),
 ("item", "Mari lihat", "berapa persisnya", "Mari lihat berapa persisnya, dengan angka dua ribu dua puluh enam."),
])

# ============================ 5 ============================
cap("Pilar 4 — yang BPJS benar-benar bayar", [
 ("lista", "Potongan 2026", ["JHT 5,7%", "JP 3%", "JKM 0,3%", "JKK 0,24-1,74%"], "Empat program di BPJS Ketenagakerjaan tahun dua ribu dua puluh enam. Jaminan Hari Tua lima koma tujuh persen, Jaminan Pensiun tiga persen, Jaminan Kematian nol koma tiga persen, dan Jaminan Kecelakaan Kerja."),
 ("titulo", "JHT 5,7%", "2% kamu, 3,7% perusahaan", "Jaminan Hari Tua lima koma tujuh persen dari upah. Dua persen dipotong dari gajimu, tiga koma tujuh persen dibayar perusahaan."),
 ("titulo", "JP 3%", "1% kamu, 2% perusahaan", "Jaminan Pensiun tiga persen. Satu persen dari kamu, dua persen dari perusahaan."),
 ("item", "Artinya", "3% gaji kamu", "Artinya dari sisi kamu, total tiga persen gaji sudah masuk ke masa tua setiap bulan. Dua persen JHT ditambah satu persen JP."),
 ("item", "Perusahaan", "menambah 5,7%", "Dan perusahaan menambahkan lima koma tujuh persen lagi. Uang ini milikmu, meski tidak pernah lewat rekeningmu."),
 ("titulo", "JKK", "0,24% sampai 1,74%", "Jaminan Kecelakaan Kerja dibayar penuh perusahaan, besarnya nol koma dua empat persen untuk pekerjaan kantor sampai satu koma tujuh empat persen untuk pertambangan."),
 ("titulo", "JKM 0,3%", "sepenuhnya perusahaan", "Jaminan Kematian nol koma tiga persen, juga sepenuhnya dibayar perusahaan."),
 ("item", "Batas upah JP", "dievaluasi tiap tahun", "Satu hal teknis yang penting: batas atas upah untuk perhitungan Jaminan Pensiun dievaluasi setiap tahun mengikuti pertumbuhan ekonomi dan inflasi."),
 ("item", "Artinya", "gaji tinggi tetap dibatasi", "Artinya kalau gajimu di atas batas itu, iuran pensiunmu tetap dihitung dari batas, bukan dari gaji penuh. Selisihnya jadi tanggung jawabmu sendiri."),
 ("titulo", "Pertanyaan", "cukup atau tidak?", "Sekarang pertanyaan yang jarang ditanyakan. Apakah tiga persen ditambah lima koma tujuh persen itu cukup?"),
 ("barras", "Kebutuhan pensiun", ["Yang terkumpul", "Yang dibutuhkan"], [40, 100], "Perkiraan umum: kamu butuh sekitar tujuh puluh persen pengeluaran terakhirmu untuk hidup layak setelah berhenti bekerja."),
 ("item", "Selisihnya", "harus kamu isi sendiri", "Iuran wajib jarang menutup seluruh angka itu, terutama kalau kariermu terputus atau kamu pindah ke sektor informal di tengah jalan."),
 ("item", "Karena itu", "pilar 4 punya dua lapis", "Karena itu pilar keempat punya dua lapis. Lapis wajib dari BPJS, dan lapis tambahan yang kamu bangun sendiri."),
 ("lista", "Lapis tambahan", ["Reksa dana jangka panjang", "Emas untuk sebagian kecil", "Properti kalau memungkinkan"], "Lapis tambahan bisa reksa dana jangka panjang, sebagian kecil emas, atau properti kalau memang memungkinkan. Yang penting: tidak disentuh."),
 ("titulo", "Kunci", "jangan dicairkan", "Kunci pilar ini bukan instrumennya. Kuncinya tidak mencairkannya untuk hal yang bukan darurat."),
 ("item", "Godaan", "JHT bisa diambil", "Godaan terbesar: Jaminan Hari Tua bisa diambil dalam kondisi tertentu. Mengambilnya untuk kebutuhan biasa memindahkan masalah ke usia enam puluh."),
 ("item", "Kalau kamu informal", "kamu bisa daftar mandiri", "Dan kalau kamu pekerja informal, kamu tetap bisa mendaftar BPJS Ketenagakerjaan secara mandiri. Iurannya kecil, perlindungannya nyata."),
 ("titulo", "Ini penting", "6 dari 10 pekerja", "Ini penting karena mayoritas pekerja Indonesia ada di sektor informal, dan sistem wajib tidak menjangkau mereka secara otomatis."),
 ("item", "Untuk mereka", "empat pilar jadi wajib", "Untuk mereka, keempat pilar ini bukan pelengkap. Itu satu-satunya sistem yang ada."),
 ("titulo", "Empat pilar", "sudah lengkap", "Keempat pilar sudah lengkap. Sekarang bagian yang menentukan berhasil atau tidak."),
 ("titulo", "Urutannya", "yang menentukan", "Urutannya. Dan ini bagian yang paling sering dibalik."),
 ("item", "Kenapa terbalik", "yang seru duluan", "Karena pilar tiga dan empat terdengar lebih menarik. Investasi terasa seperti kemajuan. Dana darurat terasa seperti diam di tempat."),
])

# ============================ 6 ============================
cap("Urutan yang menentukan", [
 ("lista", "Urutan yang benar", ["1. Penyangga 1 bulan", "2. Utang mahal", "3. Dana darurat penuh", "4. Investasi", "5. Pensiun tambahan"], "Urutan yang benar ada lima langkah. Penyangga satu bulan, lunasi utang mahal, dana darurat penuh, investasi, lalu pensiun tambahan."),
 ("item", "Langkah 1", "penyangga satu bulan", "Langkah satu: kumpulkan satu bulan pengeluaran. Ini bukan dana darurat penuh. Ini agar kejadian kecil tidak memaksamu berhutang."),
 ("item", "Langkah 2", "utang di atas 15% setahun", "Langkah dua: serang semua utang berbunga di atas lima belas persen setahun. Kartu kredit dan pinjaman daring masuk di sini."),
 ("item", "Langkah 3", "dana darurat penuh", "Langkah tiga: baru kejar tiga sampai enam bulan penuh, atau lebih kalau penghasilanmu tidak tetap."),
 ("item", "Langkah 4", "investasi rutin", "Langkah empat: mulai setoran rutin otomatis. Kecil tidak masalah. Rutin yang penting."),
 ("item", "Langkah 5", "pensiun tambahan", "Langkah lima: tambah lapis pensiun di luar BPJS, dan jangan disentuh."),
 ("titulo", "Boleh tumpang tindih", "tapi jangan dilompati", "Langkah-langkah ini boleh tumpang tindih sedikit. Yang tidak boleh: melompatinya."),
 ("barras", "Kalau dibalik", ["Urutan benar", "Investasi duluan"], [100, 45], "Kalau dibalik, hasilnya bukan sedikit lebih lambat. Hasilnya sering nol, karena satu kejadian memaksa jual rugi dan berhutang sekaligus."),
 ("titulo", "Contoh nyata", "yang sering terjadi", "Contoh yang sering terjadi. Seseorang menabung di saham selama delapan belas bulan tanpa dana darurat."),
 ("item", "Bulan 19", "motor rusak, kerja berhenti", "Bulan kesembilan belas, kendaraannya rusak dan dia tidak bisa bekerja. Dia menjual sahamnya di harga turun, dan tetap kurang."),
 ("item", "Hasilnya", "utang baru bunga tinggi", "Sisanya dia tutup dengan pinjaman daring. Delapan belas bulan disiplin berubah jadi utang berbunga tinggi dalam satu minggu."),
 ("item", "Yang salah", "bukan pilihan sahamnya", "Yang salah bukan pilihan sahamnya. Yang salah urutannya."),
 ("titulo", "Uji sendiri", "3 pertanyaan", "Uji sistemmu sendiri dengan tiga pertanyaan, sekarang juga."),
 ("lista", "Uji cepat", ["Bisa bertahan berapa bulan tanpa pemasukan?", "Berapa persen penghasilan habis untuk cicilan?", "Ada setoran otomatis bulan ini?"], "Satu: kalau pemasukan berhenti hari ini, kamu bertahan berapa bulan? Dua: berapa persen penghasilan habis untuk cicilan? Tiga: ada setoran otomatis bulan ini?"),
 ("item", "Jawaban jujur", "menunjukkan langkahmu", "Jawaban jujur atas tiga pertanyaan itu langsung menunjukkan kamu ada di langkah berapa."),
 ("item", "Dan", "hanya satu langkah yang dikerjakan", "Dan aturannya: kerjakan hanya satu langkah dalam satu waktu. Mengerjakan lima sekaligus adalah cara paling cepat untuk berhenti."),
 ("titulo", "Kenapa satu", "tenaga kamu terbatas", "Alasannya bukan soal uang. Tenaga untuk disiplin itu terbatas, dan membaginya ke lima arah membuat semuanya setengah jadi."),
 ("titulo", "Contoh angka", "tiga gaji nyata", "Supaya konkret, mari jalankan sistem ini di empat situasi penghasilan nyata."),
 ("item", "Bukan gaji ideal", "gaji yang ada", "Bukan gaji ideal. Gaji yang benar-benar ada di sekitarmu."),
 ("item", "Angka", "boleh kamu sesuaikan", "Sesuaikan angkanya dengan situasimu. Yang penting proporsinya, bukan rupiahnya."),
 ("titulo", "Mulai", "dari yang terkecil", "Kita mulai dari yang paling ketat."),
])

# ============================ 7 ============================
cap("Sistem ini di empat penghasilan nyata", [
 ("titulo", "Kasus 1", "bersih Rp2,5 juta", "Kasus pertama. Penghasilan bersih dua juta lima ratus ribu rupiah, tinggal bersama keluarga, pengeluaran bertahan satu juta delapan ratus ribu."),
 ("barras", "Rp2,5jt", ["Bertahan", "Cicilan", "Sisa"], [72, 12, 16], "Pengeluaran bertahan satu juta delapan ratus ribu. Cicilan tiga ratus ribu. Sisa empat ratus ribu rupiah."),
 ("item", "Langkah dia", "penyangga dulu", "Cicilannya dua belas persen, masih aman. Jadi langkahnya bukan utang. Langkahnya penyangga satu bulan."),
 ("item", "Empat ratus ribu", "penyangga dalam 5 bulan", "Empat ratus ribu per bulan menutup satu bulan pengeluaran dalam lima bulan. Bukan cepat, tapi nyata."),
 ("item", "Setelahnya", "bagi dua", "Setelah itu dia membagi dua: dua ratus ribu terus ke dana darurat, dua ratus ribu ke setoran otomatis pertama."),
 ("titulo", "Kasus 2", "bersih Rp5 juta", "Kasus kedua. Penghasilan bersih lima juta rupiah, sudah berkeluarga, pengeluaran bertahan tiga juta enam ratus ribu."),
 ("barras", "Rp5jt", ["Bertahan", "Cicilan", "Sisa"], [72, 36, 12], "Cicilan satu juta delapan ratus ribu rupiah. Itu tiga puluh enam persen. Di atas batas."),
 ("item", "Langkahnya", "utang dulu, bukan investasi", "Sisa yang benar-benar bebas hanya enam ratus ribu. Langkahnya jelas: turunkan cicilan dulu, bukan mulai investasi."),
 ("item", "Targetnya", "turun ke bawah 30%", "Targetnya menurunkan cicilan ke bawah satu juta lima ratus ribu. Setelah itu ruangnya terbuka sendiri."),
 ("item", "Kesalahan umum", "menambah cicilan baru", "Kesalahan paling umum di titik ini: mengambil cicilan baru karena penghasilan naik. Itu memindahkan garis akhir semakin jauh."),
 ("titulo", "Kasus 3", "penghasilan harian", "Kasus ketiga. Pedagang dengan penghasilan harian, rata-rata empat juta sebulan, tapi bulan buruk bisa dua juta."),
 ("barras", "Harian", ["Bulan baik", "Rata-rata", "Bulan buruk"], [100, 80, 50], "Rentangnya lebar. Bulan baik lima juta, rata-rata empat juta, bulan buruk dua juta rupiah."),
 ("item", "Aturannya", "pakai bulan buruk", "Aturan untuk penghasilan tidak tetap: susun anggaran memakai bulan buruk, bukan rata-rata."),
 ("item", "Kelebihan", "masuk ke penyangga", "Semua kelebihan di bulan baik masuk ke dana darurat, bukan ke gaya hidup. Ini yang meratakan penghasilan yang tidak rata."),
 ("item", "Targetnya", "9 sampai 12 bulan", "Dan targetnya lebih tinggi: sembilan sampai dua belas bulan pengeluaran, karena bulan buruk bisa datang berturut-turut."),
 ("titulo", "Pola", "sama di ketiganya", "Perhatikan polanya. Tiga penghasilan berbeda, tapi urutannya sama persis."),
 ("item", "Yang berbeda", "hanya kecepatan", "Yang berbeda hanya kecepatan. Bukan urutannya, bukan pilarnya."),
 ("item", "Karena itu", "sistem ini tidak butuh gaji besar", "Karena itu sistem ini tidak menunggu gaji besar. Dia bekerja dengan penghasilan yang kamu punya sekarang."),
 ("titulo", "Terakhir", "yang merusak sistem", "Terakhir, empat hal yang merusak sistem ini meski semua langkahnya benar."),
 ("titulo", "Terakhir", "yang merusak sistem", "Semuanya pernah terjadi ke orang yang sudah rajin. Jadi ini bukan soal disiplin."),
 ("item", "Ini soal", "jebakan yang bisa diprediksi", "Ini soal jebakan yang bisa diprediksi. Dan yang bisa diprediksi bisa dihindari."),
])

# ============================ 8 ============================
cap("Yang merusak sistem, dan penutup", [
 ("lista", "4 perusak", ["Naik gaya hidup", "Menabung tanpa nama", "Semua sekaligus", "Berhenti karena satu bulan gagal"], "Empat perusak. Gaya hidup ikut naik, menabung tanpa tujuan, mengerjakan semua sekaligus, dan berhenti gara-gara satu bulan gagal."),
 ("item", "Perusak 1", "gaji naik, cicilan naik", "Perusak pertama: setiap kenaikan penghasilan langsung diikuti kenaikan pengeluaran. UMP naik lima sampai tujuh persen, cicilan naik sepuluh."),
 ("item", "Obatnya", "kunci 50% kenaikan", "Obatnya satu aturan. Setiap kali penghasilan naik, setengah kenaikannya langsung masuk ke pilar yang sedang kamu kerjakan, sebelum kamu terbiasa."),
 ("item", "Perusak 2", "tabungan tanpa nama", "Perusak kedua: satu rekening untuk semua tujuan. Uang tanpa nama akan selalu terpakai untuk hal yang paling mendesak hari itu."),
 ("item", "Obatnya", "beri nama tiap rekening", "Obatnya: beri nama. Dana darurat. Sekolah anak. Pensiun. Uang yang punya nama lebih sulit dipakai untuk hal lain."),
 ("item", "Perusak 3", "mengerjakan semua", "Perusak ketiga: mengerjakan empat pilar bersamaan dengan sisa yang kecil. Semuanya bergerak lambat, tidak ada yang terasa selesai, lalu berhenti."),
 ("item", "Obatnya", "satu langkah sampai selesai", "Obatnya: satu langkah sampai selesai, baru pindah. Rasa selesai adalah bahan bakar yang membuatmu bertahan sampai langkah kelima."),
 ("item", "Perusak 4", "satu bulan gagal lalu berhenti", "Perusak keempat, dan yang paling sering: satu bulan gagal lalu berhenti sepenuhnya."),
 ("item", "Kenyataannya", "sistem bertahun-tahun", "Kenyataannya sistem ini berjalan bertahun-tahun. Satu bulan yang gagal hanya satu titik, bukan garis."),
 ("item", "Aturannya", "lanjut bulan depan", "Aturannya sederhana. Lewatkan bulan itu, lanjutkan bulan depan dengan jumlah yang sama. Jangan menambal, jangan berhenti."),
 ("titulo", "Ringkasnya", "empat pilar, satu urutan", "Ringkasnya. Empat pilar: dana darurat, cicilan, investasi, pensiun. Satu urutan yang tidak boleh dilompati."),
 ("lista", "Bawa ini", ["Dana darurat dari pengeluaran, bukan gaji", "Cicilan maksimal 30%", "Rutin mengalahkan besar", "BPJS bukan seluruh pensiunmu"], "Empat kalimat untuk dibawa. Dana darurat dihitung dari pengeluaran. Cicilan maksimal tiga puluh persen. Rutin mengalahkan besar. Dan BPJS bukan seluruh pensiunmu."),
 ("titulo", "Hari ini", "satu langkah saja", "Kalau kamu hanya melakukan satu hal setelah video ini, lakukan yang ini."),
 ("item", "Hitung", "cicilan bagi penghasilan", "Jumlahkan seluruh cicilanmu, bagi dengan penghasilan bersih. Angka itu menentukan langkahmu berikutnya, dan hanya butuh lima menit."),
 ("item", "Di bawah 30%", "kejar penyangga", "Di bawah tiga puluh persen: kejar penyangga satu bulan."),
 ("item", "Di atas 30%", "turunkan dulu", "Di atas tiga puluh persen: turunkan dulu, semua yang lain menunggu."),
 ("titulo", "Bulan depan", "hitung ulang", "Lalu hitung ulang bulan depan. Sistem ini diukur dalam tahun, tapi dijalankan bulan per bulan."),
 ("item", "Angka 2026", "akan berubah lagi", "Angka dua ribu dua puluh enam akan berubah lagi tahun depan. Yang tidak berubah adalah urutannya."),
 ("cta", "Setiap Level", "satu langkah tiap bulan", "Kalau video ini berguna, tinggalkan komentar berisi langkah keberapa kamu sekarang. Saya membaca semuanya."),
 ("cta", "Setiap Level", "satu langkah tiap bulan", "Dan kalau kamu ingin lanjutan tentang salah satu pilar, tulis pilar mana. Yang paling banyak diminta akan dibuat lebih dulu."),
 ("cta", "Setiap Level", "naik satu level tiap bulan", "Terima kasih sudah menonton sampai akhir. Sampai jumpa di video berikutnya di Setiap Level."),
])


# ===== densificacao para a faixa escalonada (25-30 min) =====
# O canal esta escalonado por medicao: no grupo de pares, >=20 min mede 18,5 v/d
# contra 0,6 v/d abaixo disso. Estes blocos entram nos capitulos de maior valor
# em vez de virar capitulo novo, pra manter os 8 capitulos da rotina.

def estende(indice, cenas):
    CAPS[indice][1].extend(cenas)


def insere(indice, pos, cenas):
    """Insere no meio do capitulo. Necessario no ultimo: extend() jogaria o
    bloco DEPOIS das cenas de CTA, e o video continuaria falando apos o
    'terima kasih sudah menonton'."""
    CAPS[indice][1][pos:pos] = cenas


estende(2, [  # cicilan: as armadilhas que mais aparecem
 ("titulo", "Pinjol", "cek izin dulu", "Satu hal yang perlu dicek sebelum apa pun: apakah pemberi pinjamanmu terdaftar dan diawasi Otoritas Jasa Keuangan."),
 ("item", "Kalau tidak terdaftar", "berhenti membayar bunga liar", "Kalau tidak terdaftar, berhenti dan cari bantuan resmi. Penagihan yang mengancam dan bunga tanpa batas bukan sesuatu yang harus kamu tanggung sendiri."),
 ("item", "Gali lubang", "tutup lubang", "Pola paling berbahaya: meminjam untuk membayar pinjaman lain. Setiap putaran menambah biaya, dan jumlahnya naik meski kamu membayar tiap bulan."),
 ("item", "Kalau sudah begitu", "hentikan putarannya", "Kalau kamu sudah di pola itu, langkah pertamanya bukan membayar lebih cepat. Langkah pertamanya berhenti mengambil yang baru."),
 ("lista", "Yang bisa dinegosiasi", ["Perpanjangan tenor", "Keringanan bunga", "Restrukturisasi resmi"], "Yang jarang orang tahu: tenor bisa diperpanjang, bunga bisa diringankan, dan restrukturisasi resmi itu ada. Menghubungi lebih dulu selalu lebih murah daripada menunggu ditagih."),
 ("item", "Menunda", "menambah biaya", "Menunda percakapan itu hanya menambah denda. Pemberi pinjaman resmi lebih memilih kamu membayar sedikit daripada tidak sama sekali."),
 ("titulo", "Catat", "semua utangmu di satu daftar", "Sebelum lanjut, tulis semua utangmu dalam satu daftar: jumlah, bunga, dan tanggal jatuh tempo. Kebanyakan orang tidak pernah melihatnya sekaligus."),
])

estende(4, [  # BPJS: o trabalhador informal
 ("titulo", "Informal", "bisa daftar mandiri", "Untuk pekerja informal, ada jalur mandiri. Kamu mendaftar sendiri dan membayar iuranmu sendiri, tanpa perusahaan."),
 ("item", "Yang bisa diambil", "JKK dan JKM dulu", "Yang paling masuk akal diambil lebih dulu: Jaminan Kecelakaan Kerja dan Jaminan Kematian. Iurannya kecil dan melindungi dari kejadian yang paling merusak."),
 ("item", "Lalu", "tambahkan Hari Tua", "Setelah itu tambahkan Jaminan Hari Tua kalau arus kasmu sudah stabil. Ini yang membangun saldonya pelan-pelan."),
 ("item", "Kenapa penting", "kecelakaan menghapus tabungan", "Kenapa urutan ini: satu kecelakaan kerja bisa menghapus tabungan bertahun-tahun dalam hitungan hari, dan itu risiko yang paling murah dipindahkan."),
 ("titulo", "Cek saldomu", "sekarang juga", "Kalau kamu pekerja formal, cek saldo Jaminan Hari Tua-mu lewat aplikasi resminya. Banyak orang tidak pernah melihatnya sekali pun."),
 ("item", "Yang sering ditemukan", "iuran tidak disetor", "Yang kadang ditemukan: iuran yang dipotong dari gaji ternyata tidak disetorkan. Semakin cepat ketahuan, semakin mudah diperbaiki."),
 ("item", "Pindah kerja", "jangan lupa lanjutkan", "Dan saat pindah kerja, pastikan kepesertaanmu berlanjut. Masa kosong yang panjang mengurangi manfaat pensiunmu nanti."),
])

estende(6, [  # um quarto caso: o casal
 ("titulo", "Kasus 4", "dua penghasilan", "Kasus keempat, yang jarang dibahas. Dua orang bekerja, penghasilan gabungan tujuh juta rupiah."),
 ("barras", "Dua penghasilan", ["Digabung", "Terpisah", "Campuran"], [100, 60, 85], "Ada tiga cara mengaturnya, dan yang paling sering gagal justru yang terlihat paling adil: memisahkan semuanya."),
 ("item", "Kenapa gagal", "tidak ada yang bertanggung jawab", "Kalau semuanya terpisah, tidak ada yang benar-benar bertanggung jawab atas dana darurat bersama. Masing-masing mengira yang lain sudah menyiapkan."),
 ("item", "Yang bekerja", "pos bersama untuk pilar", "Yang paling bertahan: satu pos bersama untuk keempat pilar, lalu sisanya bebas masing-masing tanpa perlu izin."),
 ("item", "Proporsional", "bukan setengah-setengah", "Dan kontribusinya proporsional terhadap penghasilan, bukan dibagi rata. Ini yang mencegah yang berpenghasilan lebih kecil selalu tertinggal."),
 ("item", "Dana darurat", "hitung pengeluaran rumah", "Dana daruratnya dihitung dari pengeluaran rumah tangga, bukan dijumlah dari dua perhitungan terpisah."),
 ("titulo", "Bonus", "dua penghasilan = risiko lebih kecil", "Kabar baiknya: dua sumber penghasilan menurunkan risiko. Kalau satu berhenti, rumah tidak langsung berhenti."),
])

insere(7, -3, [  # calendario mensal — ANTES das 3 cenas de CTA que fecham o video
 ("titulo", "Kalender", "kapan mengerjakan apa", "Supaya sistem ini tidak berhenti di niat, ini kalender bulanannya. Tiga tanggal saja."),
 ("item", "Hari gajian", "pindahkan dulu", "Hari gajian: pindahkan setoran pilar sebelum apa pun. Sebelum belanja, sebelum bayar yang tidak wajib."),
 ("item", "Alasannya", "yang tersisa selalu nol", "Alasannya bukan disiplin. Yang disisakan di akhir bulan hampir selalu nol, berapa pun penghasilanmu."),
 ("item", "Tanggal 15", "cek cicilan", "Tanggal lima belas: lihat rasio cicilanmu dan pengeluaran sampai hari itu. Setengah bulan masih cukup waktu untuk mengoreksi."),
 ("item", "Akhir bulan", "10 menit meninjau", "Akhir bulan: sepuluh menit meninjau. Berapa yang masuk pilar, berapa yang bocor, dan apa satu hal yang akan diubah bulan depan."),
 ("lista", "Tiga tanggal", ["Gajian: pindahkan", "Tanggal 15: koreksi", "Akhir bulan: tinjau"], "Tiga tanggal, total mungkin dua puluh menit sebulan. Itu seluruh biaya perawatan sistem ini."),
 ("item", "Dua puluh menit", "melawan bertahun-tahun", "Dua puluh menit sebulan melawan konsekuensi yang berjalan bertahun-tahun. Ini pertukaran paling murah dalam keuangan pribadi."),
])


# ===================== montagem =====================
def cena(t, primeira, titulo_cap):
    """Traduz a tupla compacta pro dicionario que a fabrica espera.

    Cena-ponte (sem_cap) nao concorre na eleicao de capitulo: sem isso o
    YouTube abre um capitulo no meio de uma frase de transicao.
    """
    lay, kicker = t[0], t[1]
    c = {"layout": lay, "kicker": kicker}
    if lay == "barras":
        c["itens"], c["alturas"], nar = t[2], t[3], t[4]
    elif lay == "lista":
        c["itens"], nar = t[2], t[3]
    elif lay == "item":
        c["preco"], nar = t[2], t[3]
    else:                                   # titulo, cta
        c["sub"], nar = t[2], t[3]
    c["nar"] = nar
    if primeira:
        c["cap"] = titulo_cap
    else:
        c["sem_cap"] = True
    return c


longo = []
for titulo_cap, cenas in CAPS:
    for i, t in enumerate(cenas):
        longo.append(cena(t, i == 0, titulo_cap))

# Short 9:16 — gancho nos 2 primeiros segundos e CTA falado no fim.
short = [
 cena(("titulo", "4 pilar", "bukan 1 tips", "Gajimu habis bukan karena boros. Karena uangmu tidak punya urutan."), False, ""),
 cena(("lista", "Urutannya", ["1. Dana darurat", "2. Cicilan", "3. Investasi", "4. Pensiun"], "Ada empat pilar, dan urutannya menentukan segalanya. Dana darurat, cicilan, investasi, pensiun."), False, ""),
 cena(("titulo", "30%", "batas cicilanmu", "Cek satu angka hari ini. Total cicilan dibagi penghasilan bersih. Di atas tiga puluh persen, semua yang lain menunggu."), False, ""),
 cena(("item", "Investasi", "nomor tiga", "Investasi itu pilar ketiga, bukan pertama. Melompatinya adalah alasan paling umum sistem keuangan runtuh."), False, ""),
 cena(("cta", "Setiap Level", "sistem lengkapnya", "Sistem lengkapnya dengan angka dua ribu dua puluh enam ada di video panjang. Tonton sekarang."), False, ""),
]
for c in short:
    c.pop("sem_cap", None)

spec = {
    "slug": "setiap-level",
    "voz": VOZ,
    "paleta": PALETA,
    "thumb": {"l1": "4 PILAR", "l2": "urutannya"},
    "longo": longo,
    "short": short,
    "copy": "gerado a partir dos capitulos reais apos o render",
}

if __name__ == "__main__":
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setiap-level-004.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False)
    nar_l = sum(len(c["nar"]) for c in longo)
    nar_s = sum(len(c["nar"]) for c in short)
    print(f"cenas longo ....... {len(longo)}")
    print(f"capitulos ......... {len(CAPS)}")
    print(f"chars narracao .... {nar_l}")
    print(f"estimativa @15,1 .. {nar_l/15.1 + len(longo)*0.5:.0f}s = {(nar_l/15.1 + len(longo)*0.5)/60:.1f} min")
    print(f"short ............. {len(short)} cenas, {nar_s} chars, ~{nar_s/15.1 + len(short)*0.5:.0f}s")
    print(f"bytes ............. {os.path.getsize(destino)}")
