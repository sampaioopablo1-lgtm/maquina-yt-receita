#!/usr/bin/env python3
"""Monta a spec setiap-level-013.

ALAVANCA ATACADA: **A — conversao short -> inscrito, pela FORMA.**

NUMERO DE PARTIDA, medido em 31/08/2026 (`v_maquina_licoes`):

    setiap-level ..... 13 shorts medidos, 16 longos medidos
                       short: mediana 1,04 views/dia, topo 20,44
                       longo: mediana 0,05 views/dia
                       veredito: `suspenso`
                       1.158 views totais no canal

O QUE DEU CERTO — e o numero e o do aprendizado 482, de novo, neste canal:
os dois unicos shorts que trouxeram inscrito foram "Bunga Deposito 2026:
berapa yang benar-benar kamu simpan setelah pajak" (doze views, UM inscrito,
retencao 66,97% — a maior do canal) e "Gaji naik. Bulanmu sama. Kenapa?"
(cento e oitenta e cinco views, um inscrito). O short MAIS visto do canal,
"3 Kebiasaan Kecil yang Diam-Diam Menghabiskan Gajimu", tem quinhentas e
setenta e nove views e converteu ZERO. O de cento e seis views sobre a
mudanca de classe do BPJS, com quase cinquenta por cento de retencao,
tambem converteu zero.

A diferenca nao e o alcance: os dois que converteram entregam uma CONTA que
a pessoa faz no proprio dinheiro. Os que nao converteram entregam FATO sobre
o mundo — uma regra que mudou, uma lista de habitos.

O QUE NAO DEU: o longo. Mediana de 0,05 views/dia, e os tres ultimos (27/08,
25/08 e 20/08) somam cinco views. E nao e duracao: eles JA foram encurtados
para quinhentos e vinte a quinhentos e noventa segundos e continuam sem
publico. Os antigos de mil e quinhentos a mil e setecentos segundos tinham
retencao entre zero e dois virgula quatro por cento — alongar matava —, mas
encurtar sozinho nao trouxe ninguem. Neste canal quem traz gente e o short.

O QUE MUDO POR CAUSA DISSO: o veredito `suspenso` ja manda o piso de oito
minutos e o melhor material no short. Eu vou alem e trato o SHORT como o
produto e o longo como o destino de quem quis a conta inteira: o short entrega
a subtracao fechada, com o metodo aplicavel, e nao a manchete.

--------------------------------------------------------------- DIMENSIONAMENTO

Veredito `suspenso` => PISO de oito minutos (alavanca B). Oito capitulos, e nao
nove, porque `copy_md` so abre capitulo sessenta segundos depois do anterior:
em quatrocentos e oitenta segundos nove capitulos nao cabem. A RESPOSTA fecha
no capitulo 3, dentro dos primeiros duzentos segundos.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO neste canal: **o preco de parcelar**. Os eixos ja publicados sao
imposto (deposito/SBN, PPh 21, JHT), BPJS, PHK/pesangon, limite de pinjol,
salario e habitos. Parcelamento "sem juros" nunca foi ao ar aqui.

A FORMA e a do outlier medido no proprio banco de pautas do canal — "All In
KPR atau Sekolah Anak? Waspada Jebakan Kelas Menegah!", cinco mil duzentas e
cinquenta e seis views/dia, `performa`, ainda nao usado: ESCOLHA BINARIA em
segunda pessoa. E a mesma forma que em 31/08 moveu o longo acima da mediana em
dois canais (aprendizado 532). Assunto NAO copiado — aquele e financiamento
imobiliario contra escola, este e a vista contra parcelado.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o preco a vista e as parcelas que ele mesmo pagaria;
2. e ESCOLHA COM PRAZO — o botao de pagar, agora, na tela;
3. o SHORT entrega a conta — a soma das parcelas menos o preco a vista.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita taxa de administracao, nao cita juro, nao cita regra da
OJK, nao cita nome de aplicativo nem de banco. Os dois numeros da conta estao
os dois na tela do proprio espectador, no momento da compra. Nao ha numero meu
para certificar em duas fontes, e por isso nao ha numero meu que possa
envelhecer nem que dependa de qual aplicativo ele usa.

O QUE O VIDEO NAO FAZ: nao diz que parcelar e bom ou ruim, nao recomenda nem
condena nenhum servico, nao promete economia e nao e aconselhamento financeiro.
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


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================

# -------------------------------------------------------------------- cap 1
T("Satu tombol", "yang kamu klik cepat",
  "Ada satu tombol yang kamu klik hampir tanpa berpikir. Tombol yang membagi "
  "harga jadi beberapa bulan.",
  cap="Tombol yang diklik cepat")
I("Namanya menenangkan", "nol persen",
  "Namanya menenangkan. Nol persen. Dan kata nol itu bekerja: begitu kamu "
  "membacanya, kamu berhenti memeriksa.")
I("Padahal itu pilihan", "bukan keharusan",
  "Padahal itu pilihan, bukan keharusan. Tidak ada yang memaksamu. Kamu yang "
  "memilih, dan kamu memilih lagi di belanja berikutnya.")
I("Dan pilihannya punya batas waktu", "sekarang, di layar",
  "Pilihan ini juga punya batas waktu yang jelas. Bukan minggu depan: "
  "sekarang, di layar, sebelum kamu menekan bayar.")
I("Yang jarang dilakukan", "membandingkan",
  "Yang jarang dilakukan orang cuma satu hal: membandingkan dua angka yang "
  "sudah ada di layar yang sama.")
I("Dua angka itu", "milikmu",
  "Dua angka itu bukan milik saya dan bukan milik aplikasinya. Dua duanya "
  "milikmu, dan dua duanya sudah tertulis di depan matamu.")
I("Yang akan kamu dapat", "satu pengurangan",
  "Dalam beberapa menit kamu bisa melakukan perhitungan ini sendiri. Satu "
  "pengurangan, dan satu pembagian kalau kamu mau melihatnya lebih jelas. "
  "Tanpa aplikasi tambahan dan tanpa istilah keuangan.")

# -------------------------------------------------------------------- cap 2
T("Dua angka", "di layar yang sama",
  "Perhitungannya punya dua sisi, dan kesalahan paling umum adalah cuma "
  "melihat satu.",
  cap="Dua angka di layar yang sama")
I("Angka pertama", "harga tunai",
  "Angka pertama adalah harga kalau kamu bayar sekaligus hari ini. Harga "
  "tunai. Biasanya dia yang paling terlihat.")
I("Angka kedua", "bukan besar cicilan",
  "Angka kedua bukan besar cicilan per bulan. Cicilan per bulan memang "
  "dirancang supaya terasa ringan, dan itu tugasnya.")
I("Angka kedua", "totalnya",
  "Angka kedua adalah cicilan per bulan dikali jumlah bulannya. Totalnya. "
  "Itu yang benar benar keluar dari rekeningmu sampai selesai.")
I("Lalu tambahkan", "yang menempel",
  "Lalu tambahkan apa saja yang menempel pada cicilan itu dan tidak menempel "
  "pada pembayaran tunai. Biaya yang besarnya sama di dua jalur tidak "
  "mengubah perbandingan; yang penting hanya yang berbeda.")
I("Sekarang dua duanya", "dalam satuan yang sama",
  "Sekarang dua angka itu ada dalam satuan yang sama: rupiah, sampai lunas. "
  "Bukan rupiah per bulan lawan rupiah sekaligus.")
I("Dan perbandingan berhenti jadi selera", "jadi aritmetika",
  "Begitu satuannya sama, perbandingannya berhenti jadi selera dan berubah "
  "jadi aritmetika. Dan aritmetika tidak tergantung siapa yang bicara.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
T("Hitungnya", "kurangkan, lalu bagi",
  "Jadi begini perhitungannya. Satu pengurangan, dan satu pembagian kalau "
  "kamu mau angkanya lebih terasa.",
  cap="Hitungnya: kurangkan lalu bagi")
I("Langkah satu", "total semua cicilan",
  "Langkah pertama: cicilan per bulan dikali jumlah bulan. Catat hasilnya.")
I("Langkah dua", "tambahkan biayanya",
  "Langkah kedua: tambahkan biaya yang cuma muncul di jalur cicilan. Catat "
  "lagi hasilnya.")
I("Langkah tiga", "kurangi harga tunai",
  "Langkah ketiga: kurangi angka itu dengan harga tunai. Yang tersisa adalah "
  "harga dari membagi pembayaran.")
I("Kalau hasilnya nol", "benar benar nol",
  "Kalau hasilnya nol, cicilannya memang benar benar nol persen, dan membagi "
  "pembayaran tidak menagih apa apa darimu.")
I("Kalau hasilnya positif", "itu harganya",
  "Kalau hasilnya positif, itulah harga yang kamu bayar untuk menunda. Bukan "
  "bunga, bukan istilah teknis. Selisih, dalam rupiah.")
I("Pembagiannya", "per bulan menunda",
  "Dan kalau mau lebih terasa: bagi selisih itu dengan jumlah bulannya. Itu "
  "harga menunda, per bulan. Angka per bulan biasanya lebih mudah "
  "dibandingkan dengan hal hal lain yang kamu bayar tiap bulan.")
I("Itu jawabannya", "dan sudah selesai",
  "Itu jawabannya, dan perhitungannya selesai di sini. Sisa video ini soal di "
  "mana angkanya bersembunyi dan kapan hasilnya menipu.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Di mana angkanya", "bersembunyi",
  "Sekarang bagian yang bikin banyak orang salah hitung: di mana angka angka "
  "itu bersembunyi.",
  cap="Di mana angkanya bersembunyi")
I("Harga tunai", "kadang berubah",
  "Harga tunai kadang berubah begitu kamu memilih cicilan. Periksa dia di dua "
  "keadaan, bukan cuma satu.")
I("Biaya layanan", "per transaksi",
  "Ada biaya layanan yang muncul sekali per transaksi. Dia kecil di layar dan "
  "utuh di rekening.")
I("Biaya bulanan", "ikut tiap bulan",
  "Ada juga biaya yang ikut tiap bulan bersama cicilannya. Yang ini dikali "
  "jumlah bulan, sama seperti cicilannya.")
I("Ongkos kirim", "kadang beda",
  "Ongkos kirim kadang berbeda antara dua jalur pembayaran. Kalau berbeda, "
  "selisihnya masuk hitungan.")
I("Promo yang hilang", "juga selisih",
  "Dan kalau ada potongan yang hanya berlaku untuk pembayaran tunai, "
  "kehilangan potongan itu juga bagian dari harga menunda.")
I("Semua itu satu tempat", "sisi cicilan",
  "Semua yang cuma ada di jalur cicilan masuk ke satu tempat: sisi cicilan. "
  "Jangan sebar mereka, nanti hilang satu satu.")
I("Kalau ragu", "catat dua kali",
  "Kalau ragu, lakukan hal paling sederhana: catat total yang harus dibayar "
  "di dua jalur, di layar yang sama, sebelum menekan bayar. Layar terakhir "
  "sebelum pembayaran biasanya menampilkan angka yang paling lengkap, dan "
  "di situlah tempat terbaik untuk mencatatnya.")

# -------------------------------------------------------------------- cap 5
T("Yang tidak masuk", "hitungan ini",
  "Ada hal hal yang perhitungan ini memang tidak tangkap, dan lebih jujur "
  "menyebutnya daripada berpura pura.",
  cap="Yang tidak masuk hitungan")
I("Arus kasmu", "punya nilai",
  "Yang pertama: arus kas. Menahan uang di rekening bulan ini punya nilai "
  "nyata, terutama kalau dana daruratmu tipis.")
I("Kadang menunda", "memang layak",
  "Artinya membayar selisih untuk tidak mengosongkan rekening bisa masuk "
  "akal. Perhitungan ini tidak melarang itu — dia cuma memberi tahu harganya.")
I("Yang kedua", "uang yang menganggur",
  "Yang kedua: uang yang tidak jadi kamu keluarkan hari ini mungkin bekerja "
  "di tempat lain. Kalau memang bekerja, itu poin untuk cicilan.")
I("Tapi jujur di sini", "apakah benar bekerja",
  "Tapi jujurlah di bagian ini. Kalau uang itu cuma mengendap di rekening "
  "harian, dia tidak bekerja, dan poin itu gugur.")
I("Yang ketiga", "kebiasaan",
  "Yang ketiga tidak berbentuk angka: membagi pembayaran membuat belanja "
  "terasa lebih ringan, dan yang terasa ringan cenderung lebih sering.")
I("Itu tidak masuk rumus", "tapi masuk rekening",
  "Itu tidak masuk rumus mana pun, tapi dia masuk ke rekeningmu di akhir "
  "bulan. Perhatikan sendiri, dan lihat apakah polanya ada. Cara paling "
  "jujur memeriksanya adalah menghitung berapa kali kamu memakai fasilitas "
  "itu tahun lalu, bukan menebak seberapa sering rasanya.")

# -------------------------------------------------------------------- cap 6
T("Kasus yang menipu", "nol yang bukan nol",
  "Sekarang kasus yang menipu hampir semua orang, dan dia layak satu bab "
  "sendiri.",
  cap="Kasus yang menipu")
I("Kadang nolnya benar", "dan selisihnya nol",
  "Kadang nolnya memang benar. Kamu hitung, selisihnya nol, dan membagi "
  "pembayaran tidak menagih apa apa. Itu ada, dan itu bagus.")
I("Kadang harganya", "sudah dinaikkan",
  "Kadang yang terjadi lain: harga tunainya sendiri sudah dinaikkan supaya "
  "cicilannya bisa disebut nol persen.")
I("Cara memeriksanya", "harga di tempat lain",
  "Cara memeriksanya sederhana: lihat harga barang yang sama di tempat lain "
  "yang tidak menawarkan cicilan itu. Satu tempat pembanding sudah cukup, "
  "asalkan barangnya benar benar sama dan bukan versi yang berbeda.")
I("Kalau harganya sama", "nolnya benar",
  "Kalau harganya kurang lebih sama, nolnya benar. Kalau di tempat lain jauh "
  "lebih murah, selisih itu sudah kamu bayar di muka.")
I("Dan itu tidak muncul", "di rumus tadi",
  "Dan selisih jenis ini tidak muncul di rumus tadi, karena rumusnya memakai "
  "harga tunai yang sedang ditawarkan padamu, bukan harga wajarnya.")
I("Dua duanya sah", "tergantung angkamu",
  "Dua duanya jawaban yang sah, dan tidak ada yang benar secara umum. Yang "
  "benar adalah yang ditunjuk angkamu. Yang tidak sah cuma satu: mengklik "
  "tanpa pernah melihat.")

# -------------------------------------------------------------------- cap 7
T("Dari satu belanja", "ke satu tahun",
  "Sekarang langkah yang mengubah cara kamu merasakan ukurannya.",
  cap="Dari satu belanja ke satu tahun")
I("Satu belanja", "terasa kecil",
  "Selisih pada satu belanja biasanya terasa kecil. Memang kecil, dan itu "
  "sebabnya dia lolos.")
I("Kalikan", "dengan yang tahun lalu",
  "Kalikan dengan jumlah belanja yang kamu cicil tahun lalu. Perilaku yang "
  "sama, dijumlahkan.")
I("Lalu lihat ke depan", "keputusannya berulang",
  "Lalu lihat ke depan: keputusan ini berulang, dan hasilnya berulang "
  "bersamanya, dengan tanda yang sama.")
I("Bandingkan dengan sesuatu", "yang kamu kenal",
  "Supaya ukurannya terasa, bandingkan dengan sesuatu yang kamu kenal. Kalau "
  "setahun selisihnya setara satu belanja bulanan penuh, itu satu cerita. "
  "Kalau setara satu kopi, itu cerita yang sangat berbeda.")
I("Dan hasilnya bisa nol", "itu juga jawaban",
  "Bisa juga hasilnya nol setahun penuh, dan itu jawaban yang sepenuhnya "
  "baik. Artinya kamu memakai fasilitas yang memang gratis, dan tidak ada "
  "yang perlu kamu ubah. Perhitungan yang berakhir di nol tetap berguna, "
  "karena sekarang kamu tahu, dan tidak lagi menebak.")
I("Bagusnya", "keputusannya kembali",
  "Bagusnya, keputusan ini kembali setiap kali kamu belanja, dan kembali "
  "utuh. Satu tahun yang buruk tidak mengikat tahun berikutnya.")

# -------------------------------------------------------------------- cap 8
T("Yang bisa kamu lakukan", "hari ini",
  "Kita tutup dengan yang bisa kamu lakukan hari ini, dalam tiga langkah.",
  cap="Yang bisa kamu lakukan hari ini")
L("Tiga langkah",
  ["Total semua cicilan", "Tambah biayanya", "Kurangi harga tunai"],
  "Pertama: cicilan per bulan dikali jumlah bulan. Kedua: tambahkan biaya "
  "yang cuma ada di jalur cicilan. Ketiga: kurangi dengan harga tunai.")
I("Lakukan sekali", "pada belanja terakhirmu",
  "Lakukan sekali saja pada belanja terakhir yang kamu cicil. Angkanya masih "
  "ada di riwayat transaksimu.")
I("Kalau nol", "kamu sudah tahu",
  "Kalau hasilnya nol, kamu sudah tahu dan tidak perlu ragu lagi di lain "
  "waktu pada tempat yang sama.")
I("Kalau positif", "sekarang ada harganya",
  "Kalau positif, sekarang keputusanmu punya harga yang terlihat. Kamu masih "
  "boleh membayarnya — bedanya, kamu tahu.")
I("Dan simpan angkanya", "untuk lain kali",
  "Simpan angka itu di kepala untuk lain kali. Di tempat yang sama, dengan "
  "jangka waktu yang sama, hasilnya biasanya berulang, dan kamu tidak perlu "
  "menghitung ulang dari nol setiap belanja.")
C("Tulis angkamu", "di kolom komentar",
  "Kalau kamu menghitung, tulis satu angka saja di kolom komentar: selisihnya, "
  "dengan tandanya. Saya ingin tahu seberapa jauh angka itu menyebar.")

# =============================== O SHORT =====================================
# Regra do `suspenso`: o melhor material vai para o short. Ele entrega a
# subtracao inteira, nao a manchete.

SHORT = [
    {"layout": "titulo", "kicker": "Cicilan nol persen",
     "sub": "benar benar nol?",
     "nar": "Cicilan nol persen. Kata nol itu bekerja: begitu kamu membacanya, "
            "kamu berhenti memeriksa.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dua angka", "sub": "ada di layarmu",
     "nar": "Padahal dua angka yang kamu butuhkan ada di layar yang sama, "
            "sebelum kamu menekan bayar.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Angka pertama", "sub": "harga tunai",
     "nar": "Angka pertama: harga kalau kamu bayar sekaligus hari ini.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Angka kedua", "sub": "cicilan kali bulan",
     "nar": "Angka kedua: cicilan per bulan dikali jumlah bulan, ditambah "
            "biaya yang cuma ada di jalur cicilan.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Kurangkan", "sub": "itu jawabannya",
     "nar": "Kurangi yang kedua dengan yang pertama. Kalau nol, nolnya benar. "
            "Kalau positif, itu harga menunda, dalam rupiah.", "sem_cap": True},
    {"layout": "cta", "kicker": "Kapan hasilnya menipu",
     "sub": "ada di video lengkap",
     "nar": "Kapan hasil nol pun masih menipu, ada di video lengkap di tautan "
            "bawah.", "sem_cap": True},
]

THUMB = {"l1": "Tunai atau", "l2": "cicilan nol"}

COPY = """# Cicilan nol persen: harga dari membagi pembayaran, dihitung dengan angkamu sendiri

## TITULO
Bayar Tunai atau Cicilan 0%? Hitung Selisihnya Sebelum Kamu Klik Bayar

## DESCRICAO
Ada satu tombol yang hampir semua orang klik tanpa berpikir: tombol yang membagi harga jadi beberapa bulan. Namanya menenangkan — nol persen — dan kata nol itu bekerja, karena begitu kamu membacanya kamu berhenti memeriksa. Padahal ini pilihan, bukan keharusan, dan pilihannya punya batas waktu yang sangat jelas: sekarang, di layar, sebelum kamu menekan bayar.

Video ini tidak menyebut satu pun angka milik saya. Tidak ada tarif, tidak ada biaya administrasi, tidak ada nama aplikasi maupun bank. Dua angka yang dipakai dua duanya milikmu, dan dua duanya sudah ada di layar yang sama pada saat kamu belanja.

Perhitungannya: cicilan per bulan dikali jumlah bulan, lalu tambahkan biaya apa pun yang hanya muncul di jalur cicilan dan tidak muncul di pembayaran tunai, lalu kurangi dengan harga tunai. Kalau hasilnya nol, cicilannya memang benar benar nol persen. Kalau hasilnya positif, itulah harga yang kamu bayar untuk menunda — bukan bunga, bukan istilah teknis, cuma selisih dalam rupiah. Bagi selisih itu dengan jumlah bulannya kalau kamu ingin merasakannya per bulan.

Ada satu bab tentang di mana angka angka itu bersembunyi: harga tunai yang kadang berubah begitu kamu memilih cicilan, biaya layanan sekali per transaksi, biaya yang ikut tiap bulan, ongkos kirim yang berbeda antar jalur pembayaran, dan potongan yang hilang kalau kamu tidak membayar tunai.

Ada juga bab tentang apa yang perhitungan ini TIDAK tangkap, karena lebih jujur menyebutnya: nilai arus kas ketika dana daruratmu tipis, uang yang mungkin bekerja di tempat lain kalau memang benar benar bekerja, dan kenyataan bahwa belanja yang terasa ringan cenderung lebih sering — yang tidak masuk rumus mana pun tapi masuk ke rekeningmu di akhir bulan.

Dan ada bab untuk kasus yang menipu: kadang nolnya memang benar, kadang harga tunainya sendiri sudah dinaikkan supaya cicilannya bisa disebut nol persen. Cara memeriksanya ada di dalam video, dan selisih jenis itu memang tidak muncul di rumus tadi.

Penutupnya adalah tiga langkah yang bisa kamu lakukan hari ini pada belanja terakhir yang kamu cicil, memakai angka yang masih ada di riwayat transaksimu.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Coba hitung pada belanja terakhir yang kamu cicil, lalu tulis satu angka saja di sini: selisihnya, dengan tandanya. Tanpa nama toko, tanpa nama aplikasi, cukup selisihnya. Saya ingin melihat seberapa jauh angka itu menyebar di antara orang yang memakai fasilitas yang sama.

## HASHTAGS
#KeuanganPribadi #Cicilan #SetiapLevel

## TAGS
cicilan nol persen, bayar tunai atau cicilan, paylater, hitung cicilan, biaya cicilan, harga tunai, keuangan pribadi, atur keuangan, belanja online, biaya tersembunyi, cicilan kartu kredit, bunga cicilan, dompet digital, keputusan belanja, hitung sendiri

## CONFIGURACOES DO STUDIO
- Idioma: Bahasa Indonesia (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita taxa de administracao, nao cita juro, nao cita regra de orgao regulador, nao cita nome de aplicativo nem de banco e nao compara servicos entre si. Os dois numeros da conta sao do proprio espectador e os dois aparecem na mesma tela no momento da compra: o preco a vista e o total das parcelas mais o que so existe no caminho parcelado. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa de qual aplicativo ele usa. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer percentual de taxa ou de juro. Esses valores mudam por loja, por promocao e por data, e citar um so deles tornaria a conta errada para a maioria de quem assiste. O video tambem nao diz que parcelar e bom ou ruim — as duas respostas sao legitimas e dependem do numero de cada um —, nao recomenda nem condena nenhum servico, nao promete economia e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/setiap-level-013.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-013",
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
    grava(SPEC, "fabrica/specs/setiap-level-013.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
