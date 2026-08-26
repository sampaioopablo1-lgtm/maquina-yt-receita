#!/usr/bin/env python3
"""Monta a spec setiap-level-012.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA, medido neste canal:

    setiap-level-009            short   12 views  1 insc  8,333%  ret 67,0%
    setiap-level-005            short  185 views  1 insc  0,541%  ret 29,2%
    3-kebiasaan-kecil           short  566 views  0 insc  0,000%  ret 38,2%
    setiap-level-004            short  126 views  0 insc  0,000%
    setiap-level-010            short  106 views  0 insc  0,000%
    setiap-level-008            short   75 views  0 insc  0,000%

O QUE DEU CERTO: o 009 — "Bunga Deposito 2026: Berapa yang Benar-Benar Kamu
Simpan" (juros de deposito: quanto voce REALMENTE guarda). Doze views e um
inscrito. A amostra e minuscula e a taxa nao vale como magnitude, mas a FORMA
vale: e a conta do dinheiro dele, sobre uma escolha que ele faz.

O QUE NAO DEU: o mais visto do canal, com 566 views, converteu zero. Quarto
canal seguido em que isso acontece.

E O 008 E O CONTRAEXEMPLO QUE ENSINA MAIS. "Pencairan JHT: Saldo Sama Rp300
Juta" e uma escolha de verdade — como sacar — e mesmo assim converteu zero com
75 views. A diferenca esta no aprendizado 487: ele faz a conta sobre um SALDO
HIPOTETICO de trezentos milhoes, nao sobre o dinheiro de quem assiste. Escolha
real, dinheiro de outra pessoa.

Entao sao TRES condicoes, e as tres precisam estar juntas:
  1. o dinheiro E DELE, em segunda pessoa            (aprendizado 487)
  2. e uma ESCOLHA que ele faz, nao algo imposto     (aprendizado 502)
  3. o video entrega a CONTA, nao so o fato          (aprendizado 482)

O QUE MUDEI: esta pauta e a continuacao natural do 009 sem repeti-lo. O 009
ensinou quanto sobra de um deposito; este mostra a alternativa e como comparar
as duas com o proprio dinheiro. Escolha, dele, com conta.

VEREDITO `suspenso` (piso de oito minutos, melhor material no short), e a
alavanca B mandando ir ao piso.

OS NUMEROS, e as duas rotas institucionais

  - PPh final sobre juros de deposito: 20%
  - PPh final sobre cupom de SBN ritel: 10%, desde 2022, base legal PP 91/2021

    rota 1  Direktorat Jenderal Pajak (pajak.go.id) — "Berinvestasi Melalui
            SBN" e a pagina do PPh Pasal 4 ayat (2)
    rota 2  Kemenkeu — DJPPR (djppr.kemenkeu.go.id), o material do DJPb e a
            Media Keuangan do proprio ministerio

O QUE FICOU DE FORA, e o video diz em voz alta

  - O CUPOM da serie corrente e a janela de oferta. Mudam a cada emissao, e
    citar um numero de hoje seria dar uma informacao que envelhece em semanas.
    O video ensina a comparar e manda olhar o calendario oficial.
  - Qualquer projecao de rendimento de deposito. A taxa varia por banco e por
    prazo; o video ensina a pegar a do proprio extrato.

O eixo — comparar dois destinos do MESMO dinheiro pela regra tributaria — nao
existe nos onze titulos no ar do canal.
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


# ------------------------------------------- 1. Satu uang, dua tempat
T("Uang yang sama", "dua tempat berbeda",
  "Uang yang sama, ditaruh di dua tempat berbeda, pulang ke kamu dengan jumlah "
  "yang berbeda. Bukan karena bunganya. Karena pajaknya.",
  cap="Satu uang, dua tempat")
T("Dan bedanya", "bukan angka kecil",
  "Dan bedanya bukan angka kecil yang bisa diabaikan. Ini selisih yang "
  "terlihat setiap kali bunga masuk ke rekeningmu.")
I("Yang kamu pilih", "bukan bunganya",
  "Yang kamu pilih di sini bukan besar bunganya. Yang kamu pilih adalah aturan "
  "pajak mana yang berlaku untuk uangmu.")
T("Ini keputusanmu", "bukan sesuatu yang terjadi padamu",
  "Ini keputusan yang kamu ambil sendiri. Bukan sesuatu yang terjadi padamu "
  "tanpa kamu minta.")
T("Kebanyakan orang", "membandingkan yang salah",
  "Kebanyakan orang membandingkan dua angka yang dipajang, lalu memilih yang "
  "lebih besar. Padahal dua angka itu belum dipotong apa apa.")
T("Yang dipajang", "belum tentu yang kamu terima",
  "Yang dipajang adalah bruto. Yang masuk ke rekeningmu adalah bersih. Jarak "
  "antara keduanya diatur oleh aturan yang tidak ditulis di brosur.")
T("Dan jaraknya", "tidak sama di kedua tempat",
  "Dan inilah kuncinya: jarak itu tidak sama di kedua tempat. Satu tempat "
  "memotong lebih banyak dari yang lain, selalu.")
I("Di akhir video", "kamu bisa hitung sendiri",
  "Di akhir video kamu bisa menghitung sendiri, dengan angka di rekeningmu. "
  "Bukan dengan contoh saya.")

# ------------------------------------------- 2. Pajaknya beda
T("Angkanya dulu", "karena semuanya berdiri di atasnya",
  "Kita mulai dari angkanya, karena seluruh keputusan berdiri di atas dua "
  "angka ini saja.",
  cap="Pajaknya memang beda")
I("Bunga deposito", "pajak final dua puluh persen",
  "Bunga deposito dan tabungan dikenakan pajak penghasilan final sebesar dua "
  "puluh persen dari jumlah bruto.")
I("Kupon SBN ritel", "pajak final sepuluh persen",
  "Kupon surat berharga negara ritel dikenakan pajak final sebesar sepuluh "
  "persen dari nilai kuponnya.")
T("Dua puluh dan sepuluh", "untuk uang yang sama",
  "Dua puluh persen di satu sisi, sepuluh persen di sisi lain, untuk uang yang "
  "sama dan orang yang sama.")
T("Tarif ini turun", "sejak dua ribu dua puluh dua",
  "Tarif sepuluh persen itu bukan hal baru. Sebelumnya lebih tinggi, lalu "
  "diturunkan lewat peraturan pemerintah, dan berlaku sejak dua ribu dua "
  "puluh dua.")
T("Selisihnya sepuluh poin", "dari bunga, bukan dari pokok",
  "Selisihnya sepuluh poin persen, dan itu dihitung dari bunganya, bukan dari "
  "pokok simpananmu. Jadi jangan bandingkan dengan nominal tabunganmu.")
I("Artinya sederhana", "ambil seratus ribu bunga",
  "Artinya sederhana. Ambil seratus ribu rupiah bunga. Di deposito, yang "
  "dipotong adalah dua puluh ribu. Di kupon, separuhnya.")
T("Final artinya", "selesai di situ",
  "Kata final di sini punya arti teknis: pajaknya sudah selesai, tidak "
  "dihitung ulang saat kamu melapor pajak tahunan.")

# ------------------------------------------- 3. Hitung sendiri
T("Sekarang hitung", "dengan angkamu",
  "Sekarang bagian yang membuat video ini berguna: hitung dengan angkamu "
  "sendiri, bukan dengan angka bulat yang saya karang.",
  cap="Hitung dengan angkamu")
L("Dua angka dari rekeningmu", ["Nominal yang mau kamu simpan",
                                "Bunga per tahun yang ditawarkan"],
  "Ambil dua angka: nominal yang mau kamu simpan, dan bunga per tahun yang "
  "ditawarkan padamu hari ini.")
I("Langkah satu", "kalikan untuk dapat bruto",
  "Kalikan keduanya. Hasilnya adalah bunga bruto setahun, dan ini adalah angka "
  "yang dipajang di brosur.")
I("Langkah dua", "kali nol koma delapan",
  "Untuk deposito, kalikan bruto tadi dengan nol koma delapan. Itu yang benar "
  "benar sampai ke kamu setelah pajak dua puluh persen.")
I("Langkah tiga", "kali nol koma sembilan",
  "Untuk kupon SBN, kalikan dengan nol koma sembilan. Pajaknya sepuluh persen, "
  "jadi yang tersisa lebih banyak.")
T("Bandingkan dua hasil itu", "bukan dua brosurnya",
  "Bandingkan dua hasil akhir itu. Jangan pernah membandingkan dua brosur, "
  "karena brosur menulis bruto dan dompetmu menerima bersih.")
T("Ulangi untuk jangka panjang", "kalikan jumlah tahunnya",
  "Kalau uangnya akan disimpan beberapa tahun, kalikan selisih tadi dengan "
  "jumlah tahunnya. Angka kecil per tahun berubah wujud di situ.")
T("Itu bukan trik", "itu cuma perkalian",
  "Ini bukan trik hitung dan bukan janji. Cuma perkalian yang jarang orang "
  "lakukan karena brosur tidak memintanya.")
T("Selisihnya", "mungkin mengejutkanmu",
  "Selisih antara keduanya sering lebih besar dari yang orang kira, terutama "
  "kalau nominalmu besar atau jangka waktunya panjang.")

# ------------------------------------------- 4. Kenapa jarang dibahas
T("Kenapa jarang", "ada yang membahas ini",
  "Pertanyaan yang wajar: kalau bedanya sejelas itu, kenapa jarang dibahas?",
  cap="Kenapa jarang dibahas")
T("Karena brosur", "menulis angka bruto",
  "Sebagian besar karena semua brosur menulis angka bruto. Pajak dipotong "
  "belakangan, dan yang dipotong tidak muncul di iklan.")
T("Dan karena kebiasaan", "deposito lebih dikenal",
  "Sebagian lagi karena kebiasaan. Deposito sudah dikenal puluhan tahun, dan "
  "kebiasaan jarang diperiksa ulang dengan kalkulator.")
I("Padahal pemeriksaannya", "dua menit",
  "Padahal pemeriksaannya hanya butuh dua menit dan dua perkalian, seperti "
  "yang barusan kita lakukan.")
T("Perhatikan juga", "biaya lain di luar pajak",
  "Perhatikan juga biaya di luar pajak: biaya administrasi, biaya penutupan "
  "lebih awal, atau minimum saldo. Itu semua memotong hasil bersihmu juga.")
T("Masukkan ke hitungan yang sama", "supaya adil",
  "Masukkan biaya biaya itu ke dalam hitungan yang sama, supaya kamu "
  "membandingkan dua hasil akhir dan bukan dua janji.")
T("Cara memeriksanya", "baca dokumen, bukan iklan",
  "Cara memeriksanya selalu sama: baca lembar ketentuan, bukan materi "
  "promosinya. Biaya selalu ada di dokumen, hampir tidak pernah di iklan.")
T("Kalau tidak ketemu", "tanyakan langsung",
  "Kalau kamu tidak menemukannya, tanyakan langsung sebelum menandatangani. "
  "Pertanyaan itu gratis, dan jawabannya mengubah hitunganmu.")
T("Ini pola yang berulang", "di banyak keputusan uang",
  "Ini pola yang berulang di banyak keputusan uang: yang diiklankan adalah "
  "bruto, yang kamu terima adalah bersih, dan jarak antara keduanya adalah "
  "aturan yang tidak diiklankan.")

# ------------------------------------------- 5. Apa yang kamu lepas
T("Tapi ada harganya", "dan harus jujur",
  "Tapi tidak ada yang gratis. Kalau satu sisi lebih menguntungkan, ada "
  "sesuatu yang kamu lepaskan, dan saya harus jujur soal itu.",
  cap="Apa yang kamu lepaskan")
T("Deposito", "jangkanya kamu yang atur",
  "Deposito jangka waktunya kamu yang atur, sering hanya beberapa bulan, dan "
  "kamu tahu persis kapan uangnya kembali.")
T("SBN ritel", "punya jangka waktu sendiri",
  "SBN ritel punya jangka waktu yang sudah ditentukan, biasanya beberapa "
  "tahun, dan aturan pencairan lebih awal berbeda tiap seri.")
I("Jadi pertanyaannya", "kapan uang ini kamu butuhkan",
  "Jadi pertanyaan sebenarnya bukan mana yang lebih tinggi. Pertanyaannya: "
  "kapan uang ini kamu butuhkan kembali?")
T("Kalau butuh cepat", "selisih pajak tidak menolong",
  "Kalau uangnya mungkin kamu butuhkan dalam waktu dekat, selisih pajak tidak "
  "menolong. Yang menolong adalah bisa mengambilnya.")
T("Ada jalan tengah juga", "tidak harus semua",
  "Ada jalan tengah yang sering dilupakan: kamu tidak harus memindahkan "
  "semuanya. Sebagian tetap likuid, sebagian ditempatkan jangka panjang.")
T("Pembagiannya", "mengikuti kebutuhanmu",
  "Pembagiannya mengikuti kapan kamu butuh, bukan mengikuti mana yang "
  "bunganya lebih tinggi. Kebutuhan lebih dulu, imbal hasil sesudahnya.")
T("Kalau tidak butuh cepat", "selisihnya bekerja untukmu",
  "Kalau memang tidak kamu butuhkan dalam waktu dekat, selisih pajak itu "
  "bekerja untukmu setiap kali kupon dibayarkan.")

# ------------------------------------------- 6. Yang tidak saya sebut
T("Bagian paling jujur", "yang tidak saya sebutkan",
  "Sekarang bagian paling jujur dari video ini: ada dua angka yang sengaja "
  "tidak saya sebutkan, dan saya jelaskan alasannya.",
  cap="Yang tidak saya sebutkan")
I("Pertama", "kupon seri yang sedang ditawarkan",
  "Pertama, besar kupon seri yang sedang ditawarkan. Angka itu berubah tiap "
  "penerbitan, dan menyebutkannya membuat video ini basi dalam hitungan "
  "minggu.")
I("Kedua", "bunga deposito di bankmu",
  "Kedua, bunga deposito yang berlaku. Itu berbeda antar bank dan antar "
  "jangka waktu, dan yang berlaku untukmu ada di penawaran bankmu sendiri.")
T("Yang saya berikan", "tidak berubah",
  "Yang saya berikan justru bagian yang tidak berubah: aturan pajaknya, dan "
  "cara membandingkan. Itu tetap berlaku tahun depan.")
T("Jadwal resminya", "ada di kalender penerbitan",
  "Jadwal penawaran seri berikutnya diumumkan di kalender penerbitan resmi, "
  "dan di situ juga tercantum kuponnya.")
T("Saya sebut ini", "karena ini ukuran kepercayaan",
  "Saya sebutkan bagian ini karena ukuran layak tidaknya sebuah video bukan "
  "apa yang disebut, tapi apa yang sengaja tidak disebut.")
T("Angka yang ditebak", "membuat kamu salah putusan",
  "Angka yang ditebak bisa membuatmu salah mengambil keputusan, dan yang "
  "menanggung akibatnya kamu, bukan saya.")
T("Kalau ada yang menjanjikan", "angka pasti, curigai",
  "Dan kalau ada yang menjanjikan angka pasti untuk masa depan, curigai. "
  "Tidak ada lembaga yang menjamin imbal hasil ke depan.")

# ------------------------------------------- 7. Untuk siapa
T("Untuk siapa masuk akal", "dan untuk siapa tidak",
  "Saya tidak akan bilang semua orang harus pindah. Saya berikan kerangkanya, "
  "dan kamu yang mencocokkan.",
  cap="Untuk siapa masuk akal")
L("SBN lebih masuk akal kalau", ["Uangnya memang untuk jangka panjang",
                                 "Kamu sudah punya dana darurat terpisah",
                                 "Kamu tidak berencana memakainya tahun ini"],
  "SBN lebih masuk akal kalau uangnya memang untuk jangka panjang, dana "
  "daruratmu sudah terpisah, dan kamu tidak berencana memakainya tahun ini.")
L("Deposito lebih masuk akal kalau", ["Uangnya bisa dipakai sewaktu waktu",
                                      "Jangkanya pendek dan pasti",
                                      "Kamu belum punya dana darurat"],
  "Deposito lebih masuk akal kalau uangnya bisa kamu pakai sewaktu waktu, "
  "jangkanya pendek dan pasti, atau dana daruratmu belum terbentuk.")
T("Urutannya tetap sama", "dana darurat lebih dulu",
  "Dan urutannya tidak berubah: dana darurat lebih dulu, baru yang jangka "
  "panjang. Ini bukan selera, ini urutan yang melindungi kamu.")
T("Kalau kamu di tengah", "hitungan yang menjawab",
  "Kalau kamu tidak persis masuk salah satu daftar, kerangka tidak akan "
  "menjawab. Yang menjawab adalah hitungan dengan angkamu sendiri.")
T("Dan hitungan itu", "sudah kamu punya sekarang",
  "Dan hitungan itu sudah kamu punya sekarang, dari bab sebelumnya. Dua "
  "perkalian, dua menit, angka rekeningmu.")
I("Kalau masih ada utang mahal", "itu yang pertama",
  "Kalau masih ada utang berbunga tinggi, itu yang pertama diselesaikan. "
  "Bunganya biasanya lebih besar dari selisih pajak mana pun.")

# ------------------------------------------- 8. Minggu ini
T("Minggu ini", "tiga langkah",
  "Tiga langkah untuk minggu ini, dan semuanya pakai angkamu sendiri.",
  cap="Tiga langkah minggu ini")
L("Langkah satu dan dua", ["Cek bunga deposito yang ditawarkan padamu",
                           "Kalikan dengan nol koma delapan"],
  "Cek bunga deposito yang ditawarkan padamu sekarang, lalu kalikan hasilnya "
  "dengan nol koma delapan untuk melihat yang bersih.")
L("Langkah tiga", ["Buka kalender penerbitan SBN ritel",
                   "Kalikan kuponnya dengan nol koma sembilan"],
  "Lalu buka kalender penerbitan resmi, lihat kupon seri berikutnya, dan "
  "kalikan dengan nol koma sembilan.")
T("Bandingkan dua angka itu", "dan catat tanggalnya",
  "Bandingkan dua angka bersih itu, catat hasilnya beserta tanggalnya, dan "
  "kamu punya dasar keputusan yang bukan perasaan.")
T("Simpan catatannya", "beserta tanggal",
  "Simpan catatan itu beserta tanggalnya di satu tempat. Enam bulan lagi "
  "angkanya berubah, dan kamu akan senang punya pembanding.")
T("Tanpa catatan", "kamu mengulang dari nol",
  "Tanpa catatan, setiap kali kamu harus mengulang dari nol dan mengandalkan "
  "ingatan. Ingatan buruk dalam urusan angka.")
T("Yang penting bukan hasilnya", "tapi kamu punya caranya",
  "Yang penting bukan mana yang menang hari ini. Yang penting kamu punya cara "
  "menghitungnya sendiri, kapan pun angkanya berubah.")
C("Hitung malam ini", "dan tulis hasilnya",
  "Hitung malam ini dan tulis hasilnya di komentar. Kalau hitungan seperti ini "
  "berguna buat kamu, subscribe — di sini setiap angka berubah jadi langkah "
  "yang kamu kerjakan sendiri.")


# ---------------------------------------------------------------------------
# O SHORT: escolha, dinheiro dele, a conta — e aponta para o longo (493).
SHORT = [
    {"layout": "titulo", "kicker": "Uang yang sama", "sub": "dua tempat",
     "nar": "Uang yang sama, ditaruh di dua tempat, pulang ke kamu dengan "
            "jumlah berbeda. Bukan karena bunganya.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Tapi karena", "sub": "pajaknya",
     "nar": "Tapi karena pajaknya. Dan ini yang kamu pilih sendiri, bukan yang "
            "terjadi padamu.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Bunga deposito", "sub": "dua puluh persen",
     "nar": "Bunga deposito kena pajak final dua puluh persen dari bruto.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Kupon SBN ritel", "sub": "sepuluh persen",
     "nar": "Kupon surat berharga negara ritel kena sepuluh persen. Uang yang "
            "sama, orang yang sama.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Hitungnya", "sub": "kali nol koma delapan",
     "nar": "Bunga brutomu kali nol koma delapan untuk deposito. Kali nol koma "
            "sembilan untuk kupon.", "sem_cap": True},
    {"layout": "cta", "kicker": "Lalu apa yang kamu lepas",
     "sub": "itu di video lengkap",
     "nar": "Apa yang kamu lepaskan sebagai gantinya, dan untuk siapa ini "
            "masuk akal, ada di video lengkap di tautan bawah.",
     "sem_cap": True},
]

THUMB = {"l1": "20% atau 10%", "l2": "uang yang sama"}

COPY = """# Uang yang sama, aturan pajak berbeda — dan selisihnya masuk ke dompetmu

## TITULO
Deposito atau SBN Ritel? Pajak 20% Lawan 10% untuk Uang yang Sama

## DESCRICAO
Uang yang sama, ditaruh di dua tempat berbeda, pulang ke kamu dengan jumlah yang berbeda — dan penyebabnya bukan besar bunganya, melainkan aturan pajaknya. Yang kamu pilih di sini sebenarnya bukan angka di brosur, tapi aturan pajak mana yang berlaku untuk uangmu. Ini keputusan yang kamu ambil sendiri, bukan sesuatu yang terjadi padamu tanpa kamu minta.

Dua angka yang menjadi dasar seluruh keputusan: bunga deposito dan tabungan dikenakan Pajak Penghasilan final sebesar 20% dari jumlah bruto, sedangkan kupon Surat Berharga Negara ritel dikenakan pajak final sebesar 10% dari nilai kupon. Tarif 10% untuk SBN itu bukan hal baru — sebelumnya lebih tinggi, lalu diturunkan lewat Peraturan Pemerintah Nomor 91 Tahun 2021 dan berlaku sejak 2022. Kata "final" di sini punya arti teknis: pajaknya selesai di situ dan tidak dihitung ulang saat pelaporan pajak tahunan.

Bagian utama video adalah perhitungan yang kamu lakukan dengan angka rekeningmu sendiri, bukan dengan contoh bulat. Ambil nominal yang mau kamu simpan dan bunga per tahun yang ditawarkan padamu; kalikan keduanya untuk mendapat bunga bruto setahun — inilah angka yang dipajang di brosur. Untuk deposito, kalikan bruto itu dengan 0,8. Untuk kupon SBN, kalikan dengan 0,9. Bandingkan dua hasil akhir tersebut, jangan pernah dua brosurnya, karena brosur menulis bruto sementara dompetmu menerima bersih.

Video juga jujur tentang harganya. Deposito jangka waktunya kamu yang atur dan kamu tahu persis kapan uangnya kembali; SBN ritel punya jangka waktu yang sudah ditentukan dan aturan pencairan lebih awal yang berbeda tiap seri. Maka pertanyaan sebenarnya bukan mana yang lebih tinggi, melainkan kapan uang itu kamu butuhkan kembali.

Ada satu bab khusus untuk dua angka yang sengaja tidak disebutkan: besar kupon seri yang sedang ditawarkan, dan bunga deposito yang berlaku di bankmu. Keduanya berubah, dan menyebutkannya akan membuat video ini basi dalam hitungan minggu. Yang diberikan justru bagian yang tidak berubah — aturan pajaknya dan cara membandingkannya.

Penutupnya adalah kerangka untuk siapa masing masing pilihan masuk akal, dengan urutan yang tidak berubah: utang berbunga tinggi lebih dulu, lalu dana darurat, baru penempatan jangka panjang.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Coba hitung malam ini dan tulis hasilnya di sini: nominal yang kamu pertimbangkan, bunga yang ditawarkan bankmu, dan berapa selisih bersihnya setelah dikali 0,8 dan 0,9. Saya penasaran seberapa besar selisih itu di angka nyata orang, karena di contoh mana pun ia selalu terlihat kecil sampai dikalikan nominal sungguhan.

## HASHTAGS
#SBNRitel #Deposito #SetiapLevel

## TAGS
sbn ritel, deposito, pajak bunga deposito, pajak kupon sbn, pph final, investasi pemula, dana darurat, surat berharga negara, bunga bersih, keuangan pribadi, menabung atau investasi, pajak penghasilan final, perbandingan investasi, tabungan 2026, setiap level

## CONFIGURACAO DE STUDIO
- Idioma: Bahasa Indonesia (id) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Indonésia | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ligado (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Diperiksa pada 26 Agustus 2026. Dua angka inti video ini dikonfirmasi di dua sumber institusional yang berbeda: (1) Direktorat Jenderal Pajak (pajak.go.id) — halaman "Berinvestasi Melalui SBN" dan halaman PPh Pasal 4 ayat (2); (2) Kementerian Keuangan — DJPPR (djppr.kemenkeu.go.id), materi DJPb, dan Media Keuangan Kemenkeu. Keduanya menyatakan hal yang sama: bunga deposito dan tabungan dikenakan PPh final 20% dari bruto, sedangkan kupon SBN ritel dikenakan PPh final 10%, dengan dasar hukum Peraturan Pemerintah Nomor 91 Tahun 2021 yang berlaku sejak 2022.

YANG TIDAK ADA DI VIDEO INI DAN ALASANNYA. (a) Besar kupon seri SBN ritel yang sedang atau akan ditawarkan tidak disebutkan: angka itu berubah pada setiap penerbitan, dan menyebut angka hari ini akan menyesatkan penonton yang menonton beberapa minggu kemudian. Jadwal dan kupon seri berikutnya diumumkan pada kalender penerbitan resmi. (b) Bunga deposito tidak disebutkan: berbeda antar bank dan antar jangka waktu, sehingga yang berlaku adalah penawaran di bank penonton sendiri. (c) Tidak ada proyeksi imbal hasil ke depan — tidak ada lembaga yang menjaminnya, dan video menyatakan ini secara eksplisit. (d) Aturan pencairan lebih awal berbeda tiap seri dan tidak dikuantifikasi di sini. Video ini bukan rekomendasi investasi maupun nasihat keuangan pribadi; ia menjelaskan aturan pajak yang berlaku dan cara menghitung sendiri.
"""

SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-012",
    "idioma": "id",
    "voz": "id-ID-ArdiNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#14453D", "c1": "#D1495B", "c2": "#EDAE49", "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "setiap-level-012.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
