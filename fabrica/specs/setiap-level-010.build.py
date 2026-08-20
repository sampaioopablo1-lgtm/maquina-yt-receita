#!/usr/bin/env python3
"""Monta a spec setiap-level-010.

CANAL. Veredito `suspenso`, e e o pior da frota: 11 longos medidos a 0,10
views/DIA de mediana, 8 shorts a 2,14 (topo 33,67), 956 views no acervo
inteiro. A regra do veredito manda escrever o longo NO PISO da faixa — mais
perto de 8 min que de 15 — e por o melhor material no SHORT. E o que esta feito
aqui, e por isso este longo tem 8 e pouco e nao 13.

Isso CONTRARIA a preferencia de 12 a 15 min da rotina, de proposito e dentro do
piso duro dela ("NUNCA abaixo de 8 min"). Onze longos a 0,10 v/d nao sao
amostra pequena: sao onze tentativas de dizer a mesma coisa em quinze minutos
para ninguem.

EIXO. Os titulos publicados cobrem gaji, dana darurat, deposito, JHT (que e
BPJS KETENAGAKERJAAN), pinjol, PHK, 50-30-20, skill stacking, belanja semanal e
Gen Z. BPJS KESEHATAN nunca foi tocado — programa diferente, orgao diferente. O
eixo `bpjs-kesehatan-kris` tem 4 outliers e ZERO usados, com topo em 5.012,3
v/d no formato "nota de imprensa", que e o formato de n=8 deste canal.

UMA ADVERTENCIA SOBRE O BANCO, porque ela quase me levou para o eixo errado. O
topo do `dana-pendidikan` (13.371,8 e 29.393,0 v/d) e C-drama e video de "AI"
classificado no eixo por engano — "Istri selingkuh...", "Mobilku disita...".
Numero grande em linha suja nao e sinal, e ruido com casas decimais. Mesma
familia do aprendizado 409: julgar o CONTEUDO, nao o rotulo.

A PAUTA, e ela nasceu de uma CONTRADICAO entre as duas passagens de busca.

  A primeira passagem afirmou: "denda keterlambatan dihapus sejak 1 Juli 2026".
  A segunda derrubou: a regra de nao cobrar multa por atraso vale desde
  1 Juli 2016 — DEZ ANOS antes. Um digito. E a multa que EXISTE e outra: a de
  internacao dentro de 45 dias apos a reativacao.

  Se eu tivesse parado na primeira fonte, o video afirmaria como novidade de
  agosto uma regra de 2016. A exigencia de duas fontes que batem existe para
  exatamente isto, e desta vez ela pegou.

O QUE ESTA CONFIRMADO NAS DUAS PASSAGENS:

    base legal do KRIS ......... Perpres 59 Tahun 2024
    ate 2 de agosto de 2026 .... valia a tarifa da Perpres 63 Tahun 2022
    iuran em 2026 .............. Kelas 1 Rp150.000
                                 Kelas 2 Rp100.000
                                 Kelas 3 Rp35.000    (estaveis o ano inteiro)
    tarifa do KRIS ............. AINDA NAO DEFINIDA pelo governo
    implantacao ................ gradual, ao longo de cerca de dois anos
    multa por atraso ........... nao existe desde 1 Juli 2016
    multa que existe ........... internacao em ate 45 dias apos reativar

A TESE, e ela e o oposto de uma manchete: as classes estao sendo extintas e o
que voce paga NAO mudou, porque a tarifa nova nao existe ainda. Quem esta
esperando o boleto subir esta esperando um numero que o governo nao publicou.

O QUE O VIDEO NAO FAZ: nao diz que a tarifa vai subir, nem que vai ficar igual.
Ninguem sabe — e dizer "ainda nao foi definida" e a unica frase honesta
disponivel. Tambem nao promete data para a definicao.
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


# ---------------------------------------------------------------- cap 1 (9)
T("Kelas 1, 2, 3 dihapus", "dan iuranmu tidak berubah",
  "Kelas satu, dua dan tiga BPJS Kesehatan sedang dihapus. Dan yang kamu bayar "
  "bulan ini tidak berubah sama sekali. Dua-duanya benar.",
  cap="Yang berubah dan yang tidak")
I("Kenapa dua-duanya benar", "tarif KRIS belum ada",
  "Alasannya sederhana dan hampir tidak ada yang menyebutnya: tarif untuk "
  "sistem baru belum ditetapkan pemerintah.")
I("Jadi kamu bayar apa", "tarif lama",
  "Selama angka itu belum keluar, yang berlaku tetap tarif lama. Bukan "
  "kelonggaran, bukan penundaan — cuma belum ada angka pengganti.")
I("Dasar hukumnya", "Perpres lima sembilan",
  "Aturan yang menghapus kelas adalah Peraturan Presiden nomor lima puluh "
  "sembilan tahun dua ribu dua puluh empat.")
I("Namanya", "KRIS",
  "Sistem penggantinya bernama K R I S: Kelas Rawat Inap Standar. Satu standar "
  "kamar untuk semua peserta, tanpa pembedaan kelas.")
T("Satu hal yang TIDAK saya lakukan", "menebak tarif",
  "Sebelum lanjut: saya tidak akan menebak berapa tarif barunya, dan tidak "
  "akan bilang naik atau tetap. Angkanya belum ada. Titik.")
I("Yang saya lakukan", "yang sudah pasti",
  "Yang saya bawa cuma yang sudah tertulis: tanggalnya, tarif yang berlaku "
  "sekarang, dan tiga hal yang banyak orang kira berubah padahal tidak.")
L("Isinya", ["Tanggal yang benar", "Tarif yang berlaku sekarang",
             "Tiga salah kaprah", "Yang perlu kamu lakukan",
             "Cara membaca berita soal ini"],
  "Lima bagian: tanggal yang benar, tarif yang berlaku sekarang, tiga salah "
  "kaprah yang beredar, apa yang perlu kamu lakukan, dan cara membaca berita "
  "soal ini tanpa ketipu.")
I("Mulai dari tanggal", "yang paling sering keliru",
  "Mulai dari tanggal, karena di situ kekeliruannya paling sering.")

# ---------------------------------------------------------------- cap 2 (9)
T("Dua Agustus", "batas tarif lama",
  "Tanggal yang perlu kamu pegang adalah dua Agustus tahun ini. Sampai hari "
  "itu, iuran masih dihitung dengan tarif Peraturan Presiden nomor enam puluh "
  "tiga.",
  cap="Tanggal yang benar")
I("Setelah itu", "peralihan, bukan sakelar",
  "Setelah tanggal itu dimulai peralihan ke KRIS. Peralihan, bukan sakelar "
  "yang ditekan dalam semalam — dan perbedaan itu yang bikin dua orang bisa "
  "sama-sama benar waktu satu bilang sudah berlaku dan satu bilang belum.")
I("Berapa lama", "sekitar dua tahun",
  "Penerapannya bertahap, direncanakan sekitar dua tahun. Rumah sakit perlu "
  "menyesuaikan ruangan, dan itu tidak selesai dalam sebulan.")
I("Artinya buat kamu", "tidak ada yang perlu diurus",
  "Buat peserta, artinya tidak ada formulir, tidak ada pendaftaran ulang, dan "
  "tidak ada tombol yang harus kamu tekan.")
B("Dua garis waktu", ["Aturan terbit", "Selesai diterapkan"], [100, 22],
  "Jarak antara aturan terbit dan penerapan penuh itulah yang bikin banyak "
  "orang mengira kebijakan ini batal. Tidak batal — cuma pelan.")
I("Kenapa terasa membingungkan", "berita datang dua kali",
  "Beritanya juga muncul dua kali: sekali waktu aturannya terbit, sekali lagi "
  "waktu tanggal peralihan tiba. Judul yang sama, dua tahun berbeda.")
I("Cara memastikan sendiri", "cek nomor Perpres",
  "Cara paling cepat memastikan sebuah berita soal ini: lihat nomor Perpres "
  "yang disebut. Kalau tidak menyebut nomor, perlakukan sebagai kabar.")
I("Yang tidak punya tanggal", "tarif KRIS",
  "Dan satu hal yang memang belum punya tanggal: besaran iuran KRIS. Belum "
  "ditetapkan, jadi belum ada yang bisa dikutip.")
I("Sekarang angkanya", "yang berlaku hari ini",
  "Sekarang angka yang benar-benar berlaku hari ini:")

# ---------------------------------------------------------------- cap 3 (9)
T("Seratus lima puluh ribu", "kelas satu",
  "Kelas satu: seratus lima puluh ribu rupiah per orang per bulan.",
  cap="Tarif yang berlaku sekarang")
I("Kelas dua", "seratus ribu",
  "Kelas dua: seratus ribu rupiah per orang per bulan.")
I("Kelas tiga", "tiga puluh lima ribu",
  "Kelas tiga: tiga puluh lima ribu rupiah per orang per bulan.")
I("Sejak kapan segini", "sepanjang tahun ini",
  "Ketiga angka itu bertahan sepanjang dua ribu dua puluh enam. Tidak naik di "
  "Februari, tidak naik di Juli, tidak naik di Agustus.")
B("Yang dibayar per bulan", ["Kelas 1", "Kelas 2", "Kelas 3"], [100, 67, 23],
  "Perbandingannya begini: kelas tiga kurang dari seperempat kelas satu. "
  "Selisih itulah yang selama ini menentukan kamar.")
I("Kalau satu keluarga", "kalikan jumlah orang",
  "Iuran dihitung per orang, bukan per keluarga. Ambil contoh keluarga empat "
  "orang.")
I("Di kelas satu", "enam ratus ribu",
  "Di kelas satu, keluarga itu membayar enam ratus ribu rupiah sebulan.")
I("Di kelas tiga", "seratus empat puluh ribu",
  "Keluarga yang sama di kelas tiga membayar seratus empat puluh ribu. Jarak "
  "antara dua angka itu yang selama ini menentukan kamar.")
I("Peserta PBI", "dibayar negara",
  "Peserta yang masuk kategori penerima bantuan iuran tidak membayar sendiri: "
  "iurannya ditanggung negara. Kelompok ini tidak terpengaruh perubahan tarif "
  "apa pun, dan itu penting disebut karena sebagian besar kepanikan soal "
  "kenaikan beredar justru di kelompok yang tidak membayar iuran sendiri.")
I("Pekerja formal", "potongan gaji",
  "Buat pekerja formal, iuran dipotong dari gaji dengan persentase, dibagi "
  "antara kamu dan pemberi kerja — bukan angka tetap di atas. Jadi kalau kamu "
  "karyawan, angka yang kamu bayar bergerak mengikuti gaji, bukan mengikuti "
  "kelas. Ini juga sebabnya banyak karyawan tidak pernah tahu berapa iurannya: "
  "potongannya tidak pernah muncul sebagai tagihan.")
I("Sekarang salah kaprahnya", "tiga yang sering",
  "Dengan angka-angka itu di tangan, sekarang tiga salah kaprah yang paling "
  "sering saya temui:")

# ---------------------------------------------------------------- cap 4 (10)
T("Salah kaprah pertama", "denda telat bayar",
  "Pertama: banyak yang mengira denda keterlambatan baru dihapus tahun ini.",
  cap="Tiga salah kaprah")
I("Yang benar", "sejak dua ribu enam belas",
  "Yang benar: tidak ada denda hanya karena telat bayar, dan itu berlaku sejak "
  "satu Juli dua ribu enam belas. Sepuluh tahun lalu.")
I("Kenapa keliru", "satu digit",
  "Kekeliruannya cuma satu digit di angka tahun, dan digit itu mengubah kabar "
  "lama jadi berita baru.")
I("Tapi ada denda lain", "empat puluh lima hari",
  "Tapi ada denda yang memang ada, dan ini yang perlu kamu tahu: kalau kamu "
  "rawat inap dalam empat puluh lima hari setelah kepesertaan aktif kembali, "
  "denda bisa dikenakan.")
I("Bedanya penting", "telat bayar vs rawat inap",
  "Jadi bedanya begini: telat bayar sendiri tidak didenda. Yang didenda adalah "
  "memakai rawat inap terlalu cepat setelah status kembali aktif.")
T("Salah kaprah kedua", "kartu harus diganti",
  "Kedua: bahwa kartu lama tidak berlaku dan harus diganti.")
I("Yang benar", "tidak ada penggantian",
  "Tidak ada program penggantian kartu untuk peralihan ini. Kalau ada yang "
  "menghubungi kamu menawarkan pengurusan kartu baru dengan biaya, itu bukan "
  "dari BPJS.")
T("Salah kaprah ketiga", "semua jadi kelas tiga",
  "Ketiga, dan ini yang paling banyak beredar: bahwa semua peserta otomatis "
  "turun ke kelas tiga.")
I("Yang benar", "standar tunggal",
  "KRIS bukan menurunkan semua orang ke kelas terbawah. KRIS menetapkan satu "
  "standar kamar rawat inap yang sama untuk semua peserta — bukan kelas tiga "
  "untuk semua orang, tapi satu standar yang berlaku untuk semua orang. "
  "Kedengarannya mirip, artinya jauh berbeda.")
I("Bedanya nyata", "standar naik untuk sebagian",
  "Bedanya nyata: untuk sebagian peserta standar kamarnya justru naik, karena "
  "standar tunggal itu ditetapkan dengan kriteria minimum yang harus dipenuhi "
  "rumah sakit.")

# ---------------------------------------------------------------- cap 5 (10)
T("Empat hal", "yang benar-benar berguna",
  "Empat hal yang berguna dilakukan, dan semuanya gratis.",
  cap="Yang perlu kamu lakukan")
I("Pertama", "cek status kepesertaan",
  "Pertama: cek status kepesertaanmu di aplikasi Mobile JKN. Yang menentukan "
  "layanan bukan kelas, tapi status aktif atau tidak.")
I("Kenapa itu dulu", "status mati diam-diam",
  "Status bisa jadi tidak aktif tanpa kamu sadari — misalnya setelah berhenti "
  "kerja, waktu iuran berpindah dari perusahaan ke kamu sendiri. Peralihan itu "
  "tidak mengirim pemberitahuan ke mana pun, dan biasanya orang baru tahu di "
  "loket rumah sakit, pada hari yang paling buruk untuk mengetahuinya.")
I("Kedua", "cek tunggakan",
  "Kedua: cek apakah ada tunggakan. Tidak ada denda atas tunggakan itu "
  "sendiri, tapi status baru aktif lagi setelah dilunasi.")
I("Ketiga", "ingat empat puluh lima hari",
  "Ketiga: kalau kamu baru saja mengaktifkan kembali, catat tanggalnya. "
  "Empat puluh lima hari sejak itu adalah jendela yang perlu kamu tahu.")
I("Keempat", "abaikan kabar tanpa nomor",
  "Keempat: setiap kabar soal tarif baru, cari nomor peraturannya. Sampai ada "
  "Perpres yang menetapkan iuran KRIS, tidak ada angka resmi untuk dikutip.")
T("Yang saya tidak tahu", "dan tidak akan karang",
  "Dan satu hal yang jujur saya tidak tahu.")
I("Kapan tarifnya keluar", "tidak ada tanggal",
  "Kapan besaran iuran KRIS ditetapkan? Tidak ada tanggal yang diumumkan. "
  "Siapa pun yang memberi kamu tanggal pasti sedang menebak.")
I("Kalau berubah", "kamu akan tahu dari boleh",
  "Kalau nanti berubah, kamu akan tahu dari tagihanmu sendiri sebelum tahu "
  "dari judul berita mana pun.")
T("Cara membaca berita soal ini", "tiga pertanyaan",
  "Sebelum penutup, tiga pertanyaan yang bisa kamu pakai untuk berita apa pun "
  "soal BPJS — bukan cuma yang ini.",
  cap="Cara membaca berita soal ini")
I("Pertanyaan pertama", "nomor peraturannya mana",
  "Pertama: peraturan mana yang disebut, lengkap dengan nomor dan tahun? "
  "Berita yang benar hampir selalu menyebutkannya, karena itu sumbernya.")
I("Kalau tidak ada nomor", "perlakukan sebagai kabar",
  "Kalau tidak ada nomor, itu belum tentu salah — tapi belum bisa kamu pakai "
  "untuk mengambil keputusan uang.")
I("Pertanyaan kedua", "tahunnya kapan",
  "Kedua: periksa tahun di setiap angka. Salah kaprah soal denda tadi hidup "
  "sepuluh tahun cuma karena satu digit tahun yang meleset.")
I("Pertanyaan ketiga", "sudah berlaku atau baru terbit",
  "Ketiga: aturannya sudah berlaku, atau baru terbit? Untuk kebijakan bertahap "
  "seperti KRIS, dua hal itu bisa berjarak dua tahun.")
B("Jarak yang bikin bingung", ["Terbit", "Berlaku penuh"], [100, 20],
  "Jarak itulah yang bikin judul yang sama muncul dua kali dan terasa seperti "
  "dua kebijakan berbeda.")
I("Kenapa ini berguna", "berlaku untuk apa saja",
  "Tiga pertanyaan itu bukan cuma untuk BPJS. Pajak, subsidi, aturan pinjol — "
  "polanya sama, dan yang menyesatkan hampir selalu sama juga.")
I("Satu kebiasaan", "cek sebelum meneruskan",
  "Dan satu kebiasaan kecil: sebelum meneruskan pesan berantai soal tarif, "
  "cari nomor peraturannya sendiri. Butuh dua menit.")
C("Setiap Level", "angka dulu, opini nanti",
  "Buka Mobile JKN hari ini dan cek satu hal: status kepesertaanmu aktif atau "
  "tidak. Itu saja. Kalau video ini menghemat waktumu, tinggalkan subscribe.")

# ---------------------------------------------------------------- short
#
# O canal esta `suspenso`: e o SHORT que carrega este pacote, e ele entrega
# sozinho a contradicao, os tres numeros e a acao. O longo e continuacao
# opcional, nunca condicao.
SHORT = [
    {"layout": "titulo", "kicker": "Kelas 1, 2, 3 dihapus",
     "sub": "iuranmu tidak berubah",
     "nar": "Kelas BPJS dihapus, dan yang kamu bayar tidak berubah. Dua-duanya "
            "benar.", "sem_cap": True},
    {"layout": "item", "kicker": "Alasannya", "preco": "tarif KRIS belum ada",
     "nar": "Tarif sistem baru belum ditetapkan pemerintah. Selama belum ada "
            "angka, yang berlaku tarif lama.", "sem_cap": True},
    {"layout": "item", "kicker": "Yang berlaku",
     "preco": "150rb / 100rb / 35rb",
     "nar": "Kelas satu seratus lima puluh ribu, kelas dua seratus ribu, kelas "
            "tiga tiga puluh lima ribu.", "sem_cap": True},
    {"layout": "item", "kicker": "Bukan turun kelas",
     "preco": "satu standar untuk semua",
     "nar": "KRIS bukan menurunkan semua ke kelas tiga. Satu standar kamar "
            "untuk semua peserta.", "sem_cap": True},
    {"layout": "item", "kicker": "Yang bisa didenda",
     "preco": "rawat inap 45 hari",
     "nar": "Telat bayar tidak didenda. Yang didenda: rawat inap dalam empat "
            "puluh lima hari setelah aktif kembali.", "sem_cap": True},
    {"layout": "cta", "kicker": "Setiap Level", "sub": "cek hari ini",
     "nar": "Buka Mobile JKN dan cek status kepesertaanmu.", "sem_cap": True},
]

COPY = """# KRIS BPJS Kesehatan: kelas dihapus, iuran tidak berubah

## TITULO
BPJS Kesehatan 2026: Kelas Dihapus Tapi Iuranmu Tidak Berubah — Ini Sebabnya

## DESCRICAO
Kelas 1, 2, dan 3 BPJS Kesehatan sedang dihapus. Dan yang kamu bayar bulan ini tidak berubah sama sekali. Dua-duanya benar — dan alasannya hampir tidak pernah disebut di judul berita: besaran iuran untuk sistem baru belum ditetapkan pemerintah. Selama angka pengganti belum ada, yang berlaku tetap tarif lama.

DASAR HUKUM DAN TANGGAL

Aturan yang menghapus sistem kelas adalah Peraturan Presiden Nomor 59 Tahun 2024. Sistem penggantinya bernama KRIS — Kelas Rawat Inap Standar — yang menetapkan satu standar kamar rawat inap untuk semua peserta. Sampai 2 Agustus 2026, iuran dihitung dengan tarif Perpres Nomor 63 Tahun 2022. Setelah itu dimulai peralihan, yang direncanakan bertahap selama sekitar dua tahun. Buat peserta tidak ada formulir, tidak ada pendaftaran ulang, dan tidak ada tombol yang harus ditekan.

TARIF YANG BERLAKU SEKARANG

Kelas 1: Rp150.000 per orang per bulan. Kelas 2: Rp100.000. Kelas 3: Rp35.000. Ketiganya bertahan sepanjang 2026 — tidak naik di Februari, tidak naik di Juli, tidak naik di Agustus. Iuran dihitung per orang, bukan per keluarga: keluarga empat orang di kelas 1 membayar Rp600.000 sebulan. Peserta PBI tidak membayar sendiri, iurannya ditanggung negara. Pekerja formal membayar lewat potongan gaji dengan persentase yang dibagi dengan pemberi kerja, bukan angka tetap di atas.

TIGA SALAH KAPRAH YANG BEREDAR

Pertama: banyak yang mengira denda keterlambatan baru dihapus tahun ini. Yang benar — tidak ada denda hanya karena telat bayar, dan itu berlaku sejak 1 Juli 2016. Sepuluh tahun lalu. Kekeliruannya satu digit di angka tahun. Tapi ada denda yang memang ada: rawat inap dalam 45 hari setelah kepesertaan aktif kembali.

Kedua: bahwa kartu lama harus diganti. Tidak ada program penggantian kartu untuk peralihan ini. Kalau ada yang menawarkan pengurusan kartu baru dengan biaya, itu bukan dari BPJS.

Ketiga, yang paling banyak beredar: bahwa semua peserta otomatis turun ke kelas 3. KRIS bukan menurunkan semua orang ke kelas terbawah — KRIS menetapkan satu standar yang sama, dengan kriteria minimum yang harus dipenuhi rumah sakit. Untuk sebagian peserta, standar kamarnya justru naik.

YANG PERLU KAMU LAKUKAN

Cek status kepesertaan di Mobile JKN (yang menentukan layanan bukan kelas, tapi status aktif). Cek tunggakan. Kalau baru mengaktifkan kembali, catat tanggalnya karena 45 hari sejak itu adalah jendela yang perlu kamu tahu. Dan untuk setiap kabar soal tarif baru, cari nomor peraturannya.

YANG TIDAK ADA DI VIDEO INI

Saya tidak menebak berapa tarif KRIS, dan tidak bilang naik atau tetap — angkanya belum ada. Saya juga tidak memberi tanggal kapan besaran itu ditetapkan, karena tidak ada tanggal yang diumumkan. Siapa pun yang memberi tanggal pasti sedang menebak.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Pertanyaan buat kalian, dan jawabannya lebih beragam dari yang kelihatan: kelas berapa kalian sekarang, dan apakah tagihan bulan ini berbeda dari bulan lalu? Saya kumpulkan jawabannya untuk materi berikutnya — yang saya cari khususnya: ada tidak yang tagihannya sudah berubah, karena kalau ada, itu informasi yang belum masuk berita mana pun.

## HASHTAGS
#BPJSKesehatan #KRIS #SetiapLevel

## TAGS
bpjs kesehatan, kris bpjs, iuran bpjs 2026, kelas bpjs dihapus, perpres 59 2024, mobile jkn, bpjs kesehatan 2026, kelas rawat inap standar, denda bpjs, tunggakan bpjs, jkn, keuangan pribadi, asuransi kesehatan, bpjs terbaru, iuran kesehatan

## CONFIGURACOES DO STUDIO
- Idioma: Bahasa Indonesia (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao > 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Dasar hukum KRIS: Perpres No. 59 Tahun 2024. Tarif sampai 2 Agustus 2026: Perpres No. 63 Tahun 2022. Iuran 2026 (Kelas 1 Rp150.000, Kelas 2 Rp100.000, Kelas 3 Rp35.000) dan ketentuan denda dikonfirmasi lewat dua pencarian terpisah dengan sumber independen yang saling cocok. Besaran iuran KRIS BELUM ditetapkan pemerintah pada tanggal video ini dibuat — video ini tidak memperkirakan angkanya maupun tanggal penetapannya. Ketentuan "tidak ada denda karena telat bayar" berlaku sejak 1 Juli 2016, bukan 2026: klaim yang menyebut 2026 keliru satu digit dan beredar luas. Denda yang tetap berlaku adalah untuk rawat inap dalam 45 hari setelah kepesertaan aktif kembali. Peserta PBI, pekerja formal, dan peserta mandiri punya skema pembayaran berbeda — angka di atas adalah untuk peserta mandiri. Materi ini edukasi keuangan pribadi, bukan nasihat asuransi, dan bukan pengganti informasi resmi dari BPJS Kesehatan.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/setiap-level-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-010",
    "idioma": "id",
    "voz": "id-ID-ArdiNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#14202E", "c1": "#1B7F79", "c2": "#E4913C",
               "bg": "#F1F6F5"},
    "thumb": {"l1": "Kelas dihapus", "l2": "iuran tetap"},
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
    grava(SPEC, "fabrica/specs/setiap-level-010.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
