"""resep-naik-level-011 — dois precos oficiais, e o terceiro e o do recibo dele.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

O NUMERO DE PARTIDA, do PROPRIO canal e com a ULTIMA leitura de `metricas`.
Este numero MUDOU hoje, e a mudanca importa: ate a rodada das 03:08 eu lia este
canal com `max(views)` e via o pacote 006 com 986 views de longo. Com a ultima
leitura ele tem SEIS. As 986 eram leitura contaminada das coletas de 01/09 e
20/09 (aprendizados 592 e 593). O canal limpo e este:

    pacote  short -> longo   forma do titulo
    005        63 ->  5      mercadoria + preco oficial (beras, BPS)
    006        26 ->  6      mercadoria + preco oficial (minyak, HET)
    007        44 ->  6      mercadoria + preco oficial (LPG, HET)
    008       994 ->  6      mercadoria + medida oficial (gula/garam/minyak)
    003        15 ->  0      listicle ("5 Strategi Ibu...")
    004        41 ->  0      meta inventada ("Menu Hemat Rp100 Ribu")
    009     1.064 ->  0      pergunta ("Masak Sendiri atau Beli Jadi?")

O QUE DEU CERTO: nada, em termos absolutos — o teto do canal e SEIS views de
longo em sete pacotes. Mas a forma separa: os quatro que nomeiam mercadoria com
referencia oficial deram cinco e seis; os tres que sao listicle, meta ou
pergunta deram ZERO. E o sinal e limpo justamente porque os dois shorts que
estouraram (994 e 1.064 views) estao um de cada lado e entregaram seis e zero.

O QUE NAO DEU: o longo ser achado. Sete pacotes, vinte e tres views de longo
somadas. Isso nao se conserta escolhendo a oitava mercadoria.

O QUE VOU MUDAR: parar de fazer o video de UMA mercadoria e fazer o video do
METODO que serve para todas. O que o canal nomeia bem — orgao, programa, preco
de referencia — passa a ser o ASSUNTO, nao o enfeite do titulo.

EIXO, e por que ele e novo. Os sete pacotes falam de beras, minyak goreng, LPG,
gula/garam/minyak, menu da semana, cozinhar contra comprar pronto e desperdicio.
Todos sao UMA mercadoria ou UM habito. NENHUM ensina onde esta o preco oficial e
como le-lo. Este ensina: existem DOIS numeros oficiais para o mesmo item, de
dois orgaos diferentes, e o recibo da pessoa e o terceiro.

VEREDITO DO CANAL: `suspenso` (v_maquina_licoes, 7 shorts e 11 longos medidos,
2.329 views). Pela rotina isso manda PISO de 8 minutos e O MELHOR MATERIAL NO
SHORT. O short entrega o metodo inteiro, nao a manchete — o 009 ja provou o
custo do contrario: mil e sessenta e quatro views de short e ZERO de longo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTE VIDEO NAO CITA NENHUM PRECO. Nem um. E essa e a decisao de desenho, nao
# uma limitacao: preco de referencia muda por regulamento e por semana, e um
# video que cita a cifra nasce com data de validade. O que entra sao fatos de
# ESTRUTURA, conferidos em DUAS instituicoes diferentes:
#
#   * existe um preco de referencia oficial chamado HAP, com DOIS niveis — um
#     no produtor e um no consumidor — fixado por Peraturan Badan Pangan
#     Nasional. Fonte: badanpangan.go.id (pagina de regulacao e os proprios
#     Perbadan 6/2024, de milho, ovo e frango, e 12/2024, de soja, cebola,
#     pimenta, acucar e carne).
#   * existe uma pesquisa de preco ao consumidor feita semanalmente em mercados
#     tradicionais, publicada por cidade. Fonte: bps.go.id (Survei Harga
#     Konsumen, publicacao do movimento semanal de precos de varejo nas
#     capitais).
#
# DESCARTADO, e por que: nenhuma CIFRA de HAP, de HET ou de media do BPS entra.
# Tambem nao afirmo que todo item do mercado tem HAP — digo quais categorias os
# dois Perbadan citados cobrem, e mando a pessoa conferir a lista vigente na
# fonte. E nao trato de HET, que e outro instrumento e de outro orgao, porque
# nao o fechei em duas fontes nesta rodada.
#
# TAMBEM FORA: nao digo que diferenca entre o recibo e a referencia e
# irregularidade. O video lista as razoes legitimas de diferenca ANTES de
# qualquer leitura, e diz explicitamente que preco acima da referencia nao e,
# por si, prova de nada.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: o preco por unidade no recibo dele,
# calculado por ele, comparado com dois numeros que ele mesmo vai buscar.
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


# Link gravado na spec pela busca via `pg_net` dentro do banco, que e onde a
# chave do Pexels mora. Com o link gravado o pacote fica reproduzivel.
BROLL = {
    # Mercado tradicional em Wamena, Indonesia. A narracao fala de "barang yang
    # sama di pasar" — o clipe e exatamente isso, e no pais do canal.
    37840670: ("https://videos.pexels.com/video-files/37840670/16051649_1920_1080_30fps.mp4",
               "Adiardi Zulfansyah",
               "https://www.pexels.com/video/vibrant-street-market-in-wamena-indonesia-37840670/"),
    # Pessoa CONFERINDO documentos. A narracao diz que o HAP e fixado por
    # peraturan badan — documento que se abre e se le, nao noticia sobre ele.
    6814544: ("https://videos.pexels.com/video-files/6814544/6814544-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/a-man-checking-the-documents-6814544/"),
    # Pessoa conferindo RECIBOS, com cara neutra. Rejeitei o 5981296 ("worrisome
    # look for over spending") de proposito: o capitulo inteiro existe para
    # dizer que diferenca NAO e sinal de irregularidade, e um clipe de susto
    # diria o contrario da narracao.
    5981291: ("https://videos.pexels.com/video-files/5981291/5981291-hd_1366_720_25fps.mp4",
              "https://kaboompics.com/",
              "https://www.pexels.com/video/a-woman-checking-and-accounting-receipts-5981291/"),
    # Mao escrevendo uma LISTA numerada. O capitulo e "empat langkah" — quatro
    # passos — e o clipe mostra os passos sendo escritos.
    29568794: ("https://videos.pexels.com/video-files/29568794/12727336_1920_1080_25fps.mp4",
               "Jakub Zerdzicki",
               "https://www.pexels.com/video/hand-writing-checklist-at-work-desk-29568794/"),
}


def B(kicker, sub, nar, q, pexels_id, cap=None):
    link, autor, pagina = BROLL[pexels_id]
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q, "broll_url": link,
         "broll_credito": {"pexels_id": pexels_id, "autor": autor,
                           "url": pagina}}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================== OS PRIMEIROS 200 SEGUNDOS ==========================
# A resposta — o numero do espectador e a comparacao — fecha no capitulo 3.

# -------------------------------------------------------------------- cap 1
B("Ada dua angka resmi", "dan keduanya bukan angka di struk Anda",
  "Untuk barang yang sama di pasar, pemerintah punya lebih dari satu angka "
  "resmi. Dan tidak satu pun dari keduanya adalah angka di struk Anda.",
  "traditional street market in Indonesia", 37840670,
  cap="Ada dua angka resmi")
T("Kenapa ini penting", "karena Anda sedang membandingkan apa",
  "Ini penting karena menentukan Anda sedang membandingkan apa dengan apa. "
  "Membandingkan struk dengan angka yang salah membuat kesimpulan ikut salah.")
T("Angka pertama", "harga acuan yang ditetapkan",
  "Angka pertama adalah harga acuan yang ditetapkan lewat peraturan. Itu "
  "keputusan, bukan hasil pengukuran pasar.")
T("Angka kedua", "harga yang diukur di pasar",
  "Angka kedua adalah harga yang benar-benar diukur di pasar oleh petugas, "
  "setiap minggu. Itu pengukuran, bukan keputusan.")
T("Keduanya resmi", "tapi menjawab pertanyaan berbeda",
  "Keduanya sama-sama resmi dan sama-sama benar. Yang berbeda adalah "
  "pertanyaan yang mereka jawab, dan karena itu angkanya jarang sama.")
T("Angka ketiga", "yang ini hanya Anda yang punya",
  "Dan ada angka ketiga, yang tidak ada di situs mana pun: harga per satuan "
  "di struk belanja Anda sendiri. Itu yang akan kita hitung.")

# -------------------------------------------------------------------- cap 2
B("Yang pertama namanya HAP", "harga acuan",
  "Angka pertama punya nama: harga acuan, disingkat HAP. Ia ditetapkan oleh "
  "Badan Pangan Nasional lewat peraturan badan.",
  "person checking an official document", 6814544,
  cap="Yang pertama namanya HAP")
T("Dua tingkat", "produsen dan konsumen",
  "Dan HAP punya dua tingkat, bukan satu. Ada acuan di tingkat produsen dan "
  "ada acuan di tingkat konsumen, dan angkanya berbeda.")
T("Yang mana untuk Anda", "yang tingkat konsumen",
  "Yang Anda pakai untuk membandingkan belanja adalah yang tingkat konsumen. "
  "Yang tingkat produsen adalah untuk petani dan peternak.")
T("Salah tingkat", "salah kesimpulan",
  "Mengambil angka tingkat produsen dan membandingkan dengan struk pasar "
  "selalu menghasilkan selisih besar yang tidak berarti apa-apa.")
T("Di mana tertulis", "di peraturan badan itu sendiri",
  "HAP tertulis di peraturan badan yang bisa Anda buka sendiri. Bukan di "
  "berita tentang peraturan, tapi di dokumen peraturannya.")
T("Kenapa saya tidak sebut angkanya", "karena angka itu berubah",
  "Saya sengaja tidak menyebut angkanya di sini. Angka acuan berubah lewat "
  "peraturan baru, dan video yang menyebut angka lahir dengan tanggal mati.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
T("Yang kedua diukur", "survei harga konsumen",
  "Angka kedua datang dari survei harga konsumen, yang mengukur harga nyata "
  "di pasar tradisional setiap minggu.",
  cap="Yang kedua diukur, bukan ditetapkan")
T("Siapa yang mengukur", "badan statistik",
  "Yang mengukur adalah badan statistik, dan hasilnya diterbitkan per kota. "
  "Jadi ada angka untuk kota Anda, bukan hanya angka nasional.")
T("Sekarang angka Anda", "harga per satuan dari struk",
  "Sekarang angka ketiga, yang Anda hitung sendiri. Ambil struk terakhir dan "
  "cari satu barang yang juga ada di daftar acuan.")
T("Bagi", "harga dibagi isi",
  "Bagi harga yang Anda bayar dengan isi kemasan dalam satuan yang sama. "
  "Kalau acuannya per kilogram, hitung punya Anda per kilogram juga.")
T("Itu angka Anda", "sekarang ada tiga di tangan",
  "Hasilnya adalah angka Anda. Sekarang Anda punya tiga angka untuk barang "
  "yang sama: yang ditetapkan, yang diukur, dan yang Anda bayar.")
T("Catat ketiganya", "sebelum menyimpulkan apa pun",
  "Catat ketiganya berdampingan. Sisa video ini hanya untuk satu hal: supaya "
  "Anda tidak salah membaca selisih di antara mereka.")

# -------------------------------------------------------------------- cap 4
T("Tidak semua barang punya acuan", "daftarnya terbatas",
  "Hal pertama yang harus Anda tahu: tidak semua isi keranjang belanja punya "
  "harga acuan. Daftarnya terbatas dan ditulis di peraturan.",
  cap="Tidak semua barang punya acuan")
T("Yang ada di satu peraturan", "jagung, telur, daging ayam",
  "Satu peraturan mengatur acuan untuk jagung, telur ayam ras dan daging ayam "
  "ras. Tiga komoditas, satu dokumen.")
T("Yang ada di peraturan lain", "kedelai, bawang, cabai, gula, daging",
  "Peraturan lain mengatur kedelai, bawang merah, bawang putih, cabai, gula "
  "konsumsi dan daging sapi atau kerbau.")
T("Kalau barang Anda tidak ada", "bandingkan dengan yang diukur saja",
  "Kalau barang yang Anda beli tidak ada di daftar, Anda masih punya angka "
  "kedua. Bandingkan struk dengan harga pasar yang diukur di kota Anda.")
T("Daftar bisa berubah", "periksa yang berlaku",
  "Daftar itu juga bisa berubah lewat peraturan baru. Jadi periksa daftar "
  "yang sedang berlaku, jangan percaya daftar dari video mana pun.")
T("Termasuk video ini", "saya pun bisa ketinggalan",
  "Termasuk video ini. Saya menyebut dua peraturan yang saya baca, dan "
  "peraturan ketiga bisa terbit besok tanpa saya tahu.")

# -------------------------------------------------------------------- cap 5
B("Kenapa struk Anda berbeda", "dan ini bukan tanda apa-apa",
  "Sekarang bagian yang paling sering disalahpahami. Ada banyak alasan sah "
  "kenapa struk Anda berbeda dari kedua angka resmi itu.",
  "checking shopping receipts on a table", 5981291,
  cap="Kenapa struk Anda berbeda")
T("Alasan pertama", "kualitas bukan barang yang sama",
  "Pertama, kualitas. Beras premium dan beras medium adalah barang berbeda, "
  "dan acuan menyebut kualitas mana yang dimaksud.")
T("Alasan kedua", "kota Anda bukan rata-rata nasional",
  "Kedua, tempat. Harga yang diukur dipublikasikan per kota, dan rata-rata "
  "nasional hampir tidak pernah sama dengan kota mana pun.")
T("Alasan ketiga", "pasar dan ritel modern berbeda",
  "Ketiga, jenis toko. Pasar tradisional dan ritel modern punya struktur "
  "biaya berbeda, dan survei mingguan itu mengukur pasar tradisional.")
T("Alasan keempat", "ukuran kemasan menipu",
  "Keempat, ukuran kemasan. Kemasan yang bukan satu kilogram membuat harga "
  "terlihat lebih murah sampai Anda membagi.")
T("Alasan kelima", "tanggal struk bukan minggu survei",
  "Kelima, tanggal. Struk bulan lalu dibandingkan dengan survei minggu ini "
  "adalah perbandingan dua waktu yang berbeda.")

# -------------------------------------------------------------------- cap 6
T("Apa arti selisihnya", "dan apa yang bukan artinya",
  "Setelah lima alasan itu disingkirkan, barulah selisih mulai berbicara. "
  "Tapi ia berbicara lebih pelan daripada yang orang kira.",
  cap="Apa arti selisihnya")
T("Selisih kecil", "itu normal",
  "Selisih kecil adalah keadaan normal. Harga acuan bukan harga pas, dan "
  "pasar bergerak di sekitarnya setiap hari.")
T("Selisih besar sekali", "itu pertanyaan, bukan jawaban",
  "Selisih yang sangat besar adalah pertanyaan, bukan jawaban. Pertanyaannya: "
  "apakah saya membandingkan kualitas, kota dan satuan yang sama.")
T("Yang paling sering", "jawabannya satuan",
  "Dalam pengalaman menghitung, jawaban yang paling sering muncul adalah "
  "satuan. Orang membandingkan harga per bungkus dengan acuan per kilogram.")
T("Harga di atas acuan", "bukan bukti pelanggaran",
  "Dan harga di atas acuan bukan bukti pelanggaran. Acuan adalah rujukan "
  "kebijakan, dan menilai pelanggaran bukan pekerjaan video ini.")
T("Yang video ini berikan", "cara menghitung, bukan vonis",
  "Yang video ini berikan hanya cara menghitung dan cara membandingkan. Vonis "
  "apa pun tentang harga bukan bagian dari sini.")

# -------------------------------------------------------------------- cap 7
T("Yang video ini tidak katakan", "batasnya perlu jelas",
  "Sekarang bagian yang biasanya dilewati. Ini hal-hal yang sengaja tidak ada "
  "di video ini.",
  cap="Yang video ini tidak katakan")
T("Tidak ada satu angka pun", "dan itu disengaja",
  "Tidak ada satu angka harga pun yang saya sebut. Angka acuan berubah lewat "
  "peraturan, dan saya tidak mau video ini menua dalam sebulan.")
T("Tidak membahas HET", "itu instrumen lain",
  "Tidak membahas harga eceran tertinggi, yang merupakan instrumen lain dari "
  "lembaga lain. Saya tidak memeriksanya di dua sumber resmi hari ini.")
T("Tidak menilai pedagang", "tidak satu pun",
  "Tidak menilai pedagang, pasar atau toko mana pun. Selisih angka bukan "
  "tuduhan terhadap siapa pun.")
T("Tidak menyarankan laporan", "itu keputusan Anda",
  "Tidak menyarankan Anda melapor ke mana pun. Kalau Anda memutuskan "
  "melakukannya, itu keputusan Anda dan bukan anjuran saya.")
T("Yang saya lakukan", "membaca sumber dan memecah langkah",
  "Yang saya lakukan hanyalah membaca dua sumber resmi dan memecah "
  "perbandingan menjadi langkah-langkah yang bisa Anda ulang sendiri.")

# -------------------------------------------------------------------- cap 8
B("Empat langkah", "dari awal sampai akhir",
  "Sekarang seluruh perbandingan dalam empat langkah, supaya Anda bisa "
  "melakukannya setelah video ini ditutup.",
  "hand writing a numbered checklist", 29568794,
  cap="Empat langkah")
T("Langkah satu", "pilih satu barang dari struk",
  "Langkah satu: ambil struk terakhir dan pilih satu barang yang juga ada di "
  "daftar acuan. Mulai dari satu, jangan sepuluh.")
T("Langkah dua", "hitung harga per satuan",
  "Langkah dua: bagi harga yang Anda bayar dengan isi kemasan, dalam satuan "
  "yang sama dengan satuan acuan.")
T("Langkah tiga", "cari dua angka resmi itu",
  "Langkah tiga: buka peraturan badan pangan untuk acuan tingkat konsumen, "
  "dan publikasi badan statistik untuk harga terukur di kota Anda.")
T("Langkah empat", "bandingkan dan baca pelan",
  "Langkah empat: sejajarkan ketiga angka dan lewati lima alasan sah tadi "
  "sebelum menyimpulkan apa pun.")
C("Tulis selisih Anda di bawah", "hanya selisihnya, bukan belanja Anda",
  "Di kolom komentar, tulis hanya selisih yang Anda temukan dan barang apa "
  "itu. Bukan total belanja Anda. Saya ingin tahu barang mana yang paling "
  "sering meleset.")


# ================================== SHORT ====================================
# Veredito `suspenso`: o MELHOR MATERIAL vai no short. Entao o short entrega o
# metodo COMPLETO — tres angka e a divisao — e nao a manchete. O 009 provou o
# custo do contrario: mil e sessenta e quatro views de short e ZERO de longo.

SHORT = [
    {"layout": "titulo", "kicker": "Tiga angka, satu barang",
     "sub": "dan dua di antaranya resmi",
     "nar": "Untuk barang yang sama ada tiga angka. Dua resmi, satu punya "
            "Anda.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Satu", "sub": "acuan tingkat konsumen",
     "nar": "Satu: harga acuan tingkat konsumen, yang ditetapkan lewat "
            "peraturan.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dua", "sub": "harga terukur di kota Anda",
     "nar": "Dua: harga yang diukur di pasar kota Anda, diterbitkan tiap "
            "minggu.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Tiga", "sub": "harga dibagi isi",
     "nar": "Tiga: harga di struk Anda dibagi isi kemasan, dalam satuan yang "
            "sama.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Bandingkan", "sub": "satuan dulu, baru simpulkan",
     "nar": "Lalu bandingkan. Kalau selisihnya besar, periksa satuan dulu, "
            "bukan pedagangnya.", "sem_cap": True},
]


THUMB = {"l1": "Dua angka", "l2": "resmi"}


COPY = """# resep-naik-level-011

## TITULO
HAP dan Panel Harga: 2 Angka Resmi untuk Barang yang Sama, dan Struk Anda

## TITULO SHORT
HAP dan harga terukur: 2 angka resmi

## DESCRICAO
Untuk satu barang yang sama di pasar, ada lebih dari satu angka resmi — dan
tidak satu pun dari keduanya adalah angka yang Anda bayar. Video ini tidak
menyebut satu harga pun, dan itu disengaja. Yang diajarkan adalah cara
menemukan kedua angka itu sendiri dan membandingkannya dengan struk Anda.

Angka pertama adalah harga acuan, disingkat HAP, yang ditetapkan lewat
Peraturan Badan Pangan Nasional. HAP punya dua tingkat: satu di tingkat
produsen dan satu di tingkat konsumen. Untuk membandingkan belanja rumah
tangga, yang dipakai adalah yang tingkat konsumen — mengambil angka tingkat
produsen selalu menghasilkan selisih besar yang tidak berarti apa-apa.

Angka kedua bukan ditetapkan, melainkan diukur: survei harga konsumen yang
dilakukan di pasar tradisional setiap minggu oleh badan statistik, dan
diterbitkan per kota. Karena itu ada angka untuk kota Anda, bukan hanya
rata-rata nasional.

Angka ketiga hanya Anda yang punya: harga per satuan di struk Anda. Bagi harga
yang Anda bayar dengan isi kemasan, dalam satuan yang sama dengan satuan acuan.

Sebelum menyimpulkan apa pun dari selisihnya, video ini menyebut lima alasan
sah kenapa ketiga angka itu berbeda: kualitas yang tidak sama, kota yang bukan
rata-rata nasional, pasar tradisional dibanding ritel modern, ukuran kemasan,
dan tanggal struk yang bukan minggu survei.

Tidak semua barang punya harga acuan. Dua peraturan yang disebut di video
mencakup jagung, telur ayam ras dan daging ayam ras pada satu peraturan, dan
kedelai, bawang merah, bawang putih, cabai, gula konsumsi serta daging sapi
atau kerbau pada peraturan lain. Daftar yang berlaku harus diperiksa di
sumbernya, bukan di video mana pun.

Video ini tidak membahas harga eceran tertinggi, tidak menilai pedagang atau
toko mana pun, dan tidak menyarankan pelaporan ke mana pun. Harga di atas acuan
bukan bukti pelanggaran.

Bab:
00:00 Ada dua angka resmi
01:11 Yang pertama namanya HAP
02:21 Yang kedua diukur, bukan ditetapkan
03:30 Tidak semua barang punya acuan
04:38 Kenapa struk Anda berbeda
05:47 Apa arti selisihnya
06:58 Yang video ini tidak katakan
08:04 Empat langkah

Tulis di komentar hanya selisih yang Anda temukan dan barang apa itu — bukan
total belanja Anda.

## DISCLOSURE
Narasi dan visual video ini dibuat dengan kecerdasan buatan. Fakta yang disebut
berasal dari sumber resmi yang disebutkan dalam deskripsi.

## HASHTAGS
#HargaPangan #BelanjaCerdas #HAP

## TAGS
harga acuan pangan, hap konsumen, badan pangan nasional, peraturan badan pangan, survei harga konsumen, harga pasar tradisional, harga per kilogram, cara hitung harga satuan, struk belanja, harga telur ayam ras, harga daging ayam ras, cabai bawang gula, harga beras, belanja dapur, menghitung harga

## COMENTARIO FIXADO
Empat langkah: pilih satu barang dari struk → bagi harga dengan isi kemasan →
cari acuan tingkat konsumen dan harga terukur kota Anda → bandingkan, dan
periksa satuan dulu sebelum menyimpulkan. Tulis di sini hanya selisihnya dan
barang apa, bukan total belanja.

## MUSICA / LICENCA
Trilha: Deliberate_Thought (biblioteca livre do pacote). B-roll: Pexels, crédito
por clipe em broll_creditos.json.

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum preco — nenhum — e isso e desenho, nao limitacao:
preco de referencia muda por regulamento e por semana, e video que cita a cifra
nasce com data de validade. O que entra sao fatos de ESTRUTURA, conferidos em
DUAS instituicoes diferentes. Da Badan Pangan Nasional (badanpangan.go.id, a
pagina de regulacao e os proprios Perbadan 6/2024 e 12/2024): existe um preco de
referencia chamado HAP, ele tem dois niveis — produtor e consumidor — e as
categorias cobertas por esses dois regulamentos sao milho, ovo e frango num, e
soja, cebola, alho, pimenta, acucar e carne no outro. Do BPS (bps.go.id): existe
uma pesquisa de preco ao consumidor feita semanalmente em mercado tradicional e
publicada por cidade. DESCARTADO: nenhuma cifra de HAP, de HET ou de media do
BPS; e o HET como instrumento, que e de outro orgao e nao foi fechado em duas
fontes nesta rodada. TAMBEM FORA: o video nao afirma que diferenca entre recibo
e referencia e irregularidade, lista cinco razoes legitimas antes de qualquer
leitura, e diz que preco acima da referencia nao e prova de nada. O numero que
decide e do espectador: o preco por unidade do recibo dele.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/resep-naik-level-011.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-011",
    "idioma": "id",
    "voz": "id-ID-GadisNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#20303A", "c1": "#B7410E", "c2": "#3E7C59", "bg": "#FAF5EF"},
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/resep-naik-level-011.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
    t, ult = 0.0, None
    for c in CENAS:
        if c.get("cap"):
            if ult:
                print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
            ult = (c["cap"], t)
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s")
