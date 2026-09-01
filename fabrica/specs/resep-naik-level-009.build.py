#!/usr/bin/env python3
"""Monta a spec resep-naik-level-009.

ALAVANCA ATACADA: **A — conversao short -> inscrito.** E esta rodada mexe numa
variavel que NENHUM pacote da frota mexeu ate hoje: o PEDIDO do short.

NUMERO DE PARTIDA, medido em 31/08 e 01/09/2026:

    resep-naik-level ... 22 pacotes, 1.188 views totais, ZERO inscritos
                         short: mediana 3,88 views/dia, TOPO 219,95
                         longo: mediana 0,00 views/dia
                         veredito: `suspenso`

O QUE DEU CERTO — e e o segundo maior alcance da frota: o short do
`resep-naik-level-008` tem NOVECENTAS E OITENTA E SEIS views. E ele fez tudo
certo pela regra de hoje: entrega o metodo FECHADO dentro do short — anote o
que acabou no mes, divida pelo numero de pessoas, divida por trinta dias — e
guarda para o longo apenas uma ressalva.

O QUE NAO DEU: **zero inscritos, com novecentas e oitenta e seis views.**

E isso derruba metade do que eu escrevi ontem. O aprendizado 539 nasceu do
`labtreinamento-006`: mil e noventa e sete views, zero inscritos, e um short
que SEGUROU a conta. Eu conclui que a conta fechada era o que convertia. Este
canal e o contra-exemplo limpo: mesma faixa de alcance, conta ENTREGUE, e
tambem zero. O 539 foi corrigido — segurar a conta nao converte, mas entregar
tambem nao basta.

O QUE MUDO POR CAUSA DISSO, e e uma coisa so: **o pedido**. Os vinte e dois
pacotes deste canal, e os dois shorts de mil views da frota, gastam o unico
pedido que tem num clique para o video completo. E o video completo fica com
ZERO view. Em canal sem inscrito nenhum, o longo nao e o ativo — a inscricao e.
Entao o short desta rodada entrega a conta fechada E pede a inscricao, amarrada
ao metodo: se essa conta serviu, a proxima vem aqui. Nao aponta para o longo.
(Experimento 26, pre-registrado antes do render.)

O resto do canal fica igual de proposito, para a variavel ficar isolada: mesma
voz, mesma trilha, mesmo formato, mesmo tipo de conta.

--------------------------------------------------------------- DIMENSIONAMENTO

Veredito `suspenso` => PISO de oito minutos, e o melhor material no short.
Oito capitulos, cada um com ~64s NA ESTIMATIVA e nunca 60 — aprendizado 537,
medido ontem: o desvio da estimativa nao tem sinal fixo, e capitulo desenhado
no limite some do `copy_md` quando a voz corre curta. A resposta fecha ate
~192s na estimativa, e o tempo REAL vai ser conferido no copy.md renderizado.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **cozinhar contra comprar pronto — o preco por porcao da propria
compra**. Os eixos ja publicados aqui sao consumo de acucar/sal/oleo, HET do
gas de tres quilos, HET do oleo de cozinha, preco do arroz do BPS contra o
mercado, cardapio de cem mil por semana e cinco estrategias. Nenhum deles
compara os dois caminhos com o dinheiro dele.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que ele paga pelo prato pronto e o que ele gasta nos
   ingredientes;
2. e ESCOLHA COM PRAZO — o jantar de hoje, a compra de amanha;
3. o SHORT entrega a conta — a divisao fechada, com o resultado.

FONTES: este video NAO faz nenhuma afirmacao institucional e NAO cita nenhum
numero meu. Nao cita preco de ingrediente, nao cita HET, nao cita indice, nao
cita nome de aplicativo, de mercado nem de restaurante. Os dois numeros da
conta estao na nota da compra dele e no preco que ele paga pelo prato pronto.
Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu
que possa envelhecer nem que dependa da regiao dele.

O QUE O VIDEO NAO FAZ: nao diz que cozinhar e sempre mais barato, nao condena
comprar pronto, nao recomenda estabelecimento nenhum e nao e aconselhamento
financeiro nem nutricional.
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
T("Setiap hari Anda memilih", "tanpa menghitung",
  "Hampir setiap hari Anda memilih antara memasak sendiri dan membeli yang "
  "sudah jadi. Dan hampir selalu pilihan itu diambil tanpa satu pun angka.",
  cap="Pilihan yang diambil tanpa angka")
I("Bukan soal hemat", "soal tahu",
  "Ini bukan ajakan berhemat. Ini soal tahu berapa selisihnya — pertanyaan "
  "lain, dan jauh lebih berguna.")
I("Dan batas waktunya jelas", "makan malam nanti",
  "Batas waktunya juga jelas: makan malam nanti, atau belanja besok pagi. "
  "Jadi angkanya berguna hari ini, bukan suatu saat nanti.")
I("Yang sering dikira", "masak selalu lebih murah",
  "Banyak orang menganggap memasak sendiri pasti lebih murah. Kadang benar, "
  "kadang tidak, dan yang menentukan bukan pendapat siapa pun.")
I("Dua angka", "sudah ada di rumah Anda",
  "Dua angka yang dibutuhkan sudah ada di rumah Anda: struk belanja terakhir, "
  "dan harga yang biasa Anda bayar untuk lauk itu.")
I("Yang akan Anda dapat", "satu pembagian",
  "Sebentar lagi Anda bisa menghitungnya sendiri. Satu pembagian, dan satu "
  "perbandingan.")

# -------------------------------------------------------------------- cap 2
T("Dua sisi", "bahan dan porsi",
  "Hitungan ini punya dua sisi, dan kesalahan paling umum adalah membandingkan "
  "yang tidak sebanding.",
  cap="Dua sisi: bahan dan porsi")
I("Sisi pertama", "harga beli jadi",
  "Sisi pertama gampang: harga satu porsi yang biasa Anda beli sudah jadi. "
  "Catat apa adanya.")
I("Sisi kedua", "belanja untuk lauk yang sama",
  "Sisi kedua: total belanja bahan untuk membuat lauk yang sama di rumah. "
  "Semua bahan, bukan hanya yang utama.")
I("Termasuk yang sedikit", "bumbu dan minyak",
  "Termasuk bumbu dan minyak. Yang sedikit itu tetap dibeli dengan uang.")
I("Lalu hitung porsinya", "jujur",
  "Lalu hitung berapa porsi yang benar-benar jadi dari belanja itu. Jujur "
  "saja, sesuai yang biasa Anda sajikan.")
I("Ini yang sering keliru", "porsi rumah beda",
  "Di sinilah banyak orang keliru: porsi di rumah biasanya lebih besar "
  "daripada porsi yang dibeli.")
I("Sekarang sebanding", "per porsi lawan per porsi",
  "Setelah porsinya dihitung, kedua sisi jadi sebanding: satu porsi lawan "
  "satu porsi. Sekarang ini bukan pendapat lagi, ini hitungan.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
T("Hitungnya", "bagi lalu bandingkan",
  "Jadi hitungannya. Satu pembagian, lalu satu perbandingan.",
  cap="Hitungnya: bagi lalu bandingkan")
I("Langkah satu", "total bahan",
  "Langkah pertama: jumlahkan semua bahan yang dibeli untuk lauk itu. Catat "
  "totalnya.")
I("Langkah dua", "bagi jumlah porsi",
  "Langkah kedua: bagi total itu dengan jumlah porsi yang jadi. Hasilnya "
  "adalah harga satu porsi buatan rumah.")
I("Langkah tiga", "bandingkan",
  "Langkah ketiga: bandingkan angka itu dengan harga satu porsi yang biasa "
  "Anda beli. Selisihnya, dalam rupiah, adalah jawabannya.")
I("Kalau masak lebih murah", "itu selisihnya",
  "Kalau buatan rumah lebih murah, itulah yang Anda simpan tiap kali memasak "
  "lauk itu.")
I("Kalau lebih mahal", "itu juga jawaban",
  "Kalau ternyata lebih mahal, itu jawaban yang sama sahnya. Artinya untuk "
  "lauk ini, membeli jadi memang masuk akal.")
I("Hitungan selesai", "sisanya penjelasan",
  "Hitungannya selesai di sini dan Anda sudah bisa melakukannya. Sisa video "
  "ini soal di mana angkanya bersembunyi dan kapan hasilnya menipu.")

# ================== DEPOIS DA RESPOSTA — POR QUE CONTINUAR ===================

# -------------------------------------------------------------------- cap 4
T("Di mana angkanya", "bersembunyi",
  "Sekarang bagian yang membuat banyak orang salah hitung: di mana angkanya "
  "bersembunyi.",
  cap="Di mana angkanya bersembunyi")
I("Gas", "dipakai, tidak dihitung",
  "Gas terpakai setiap kali memasak, tapi hampir tidak pernah masuk hitungan. "
  "Perkirakan saja, dan masukkan.")
I("Minyak yang tersisa", "jangan dihitung penuh",
  "Minyak yang masih tersisa di botol jangan dihitung penuh. Yang masuk "
  "hitungan hanya bagian yang terpakai untuk lauk itu.")
I("Bumbu yang sudah ada", "tetap ada harganya",
  "Bumbu yang sudah ada di dapur terasa gratis, padahal dulu dibeli. Kalau "
  "sulit dipisah, perkirakan bagian kecilnya.")
I("Yang terbuang", "juga masuk",
  "Bahan yang layu atau tidak sempat dimasak juga masuk, karena uangnya sudah "
  "keluar.")
I("Kalau bingung", "cukup satu lauk",
  "Kalau semua ini terasa rumit, lakukan untuk satu lauk saja, yang paling "
  "sering Anda beli. Satu lauk sudah cukup untuk tahu polanya.")
I("Dan perkiraan boleh", "asal ke bawah",
  "Perkiraan boleh dipakai, asal condong ke bawah untuk sisi rumah. Kalau "
  "dengan perkiraan hemat pun hasilnya sudah jelas, hasilnya memang jelas.")

# -------------------------------------------------------------------- cap 5
T("Yang tidak masuk", "hitungan ini",
  "Ada hal-hal yang hitungan ini tidak tangkap, dan lebih jujur menyebutnya.",
  cap="Yang tidak masuk hitungan")
I("Waktu Anda", "punya nilai",
  "Yang pertama: waktu. Memasak memakan waktu, dan waktu Anda punya nilai, "
  "walaupun tidak keluar dari dompet.")
I("Termasuk yang sesudahnya", "cuci dan beres-beres",
  "Termasuk yang sesudahnya: mencuci dan membereskan. Itu bagian dari "
  "memasak, bukan tambahan.")
I("Kedua", "tenaga di hari sibuk",
  "Yang kedua: tenaga. Di hari yang sudah panjang, membeli jadi bisa masuk "
  "akal walaupun lebih mahal.")
I("Hitungan ini tidak melarang", "hanya memberi harganya",
  "Hitungan ini tidak melarang apa pun. Ia hanya memberi tahu berapa harga "
  "dari kemudahan itu, supaya Anda memilih dengan sadar.")
I("Ketiga", "porsi lebih dan besok",
  "Yang ketiga: masak sekali sering menghasilkan porsi lebih untuk besok. "
  "Itu menurunkan harga per porsi, dan sering terlupakan.")
I("Keempat", "selera dan kebiasaan",
  "Dan yang terakhir tidak berbentuk angka: ada lauk yang di rumah tidak "
  "pernah sama rasanya. Itu alasan yang sah, asal Anda tahu harganya.")

# -------------------------------------------------------------------- cap 6
T("Kasus yang menipu", "yang dimasak banyak",
  "Sekarang kasus yang menipu hampir semua orang.",
  cap="Kasus yang menipu")
I("Ada lauk", "yang murah karena banyak",
  "Ada lauk yang dijual murah justru karena dimasak dalam jumlah besar. Di "
  "rumah, jumlah kecil tidak bisa menandinginya.")
I("Itu bukan kekalahan", "itu skala",
  "Itu bukan berarti Anda gagal berhemat. Itu skala, dan skala memang bekerja "
  "seperti itu.")
I("Ada juga sebaliknya", "yang mahal karena rumit",
  "Sebaliknya, ada lauk yang dijual mahal karena rumit atau lama, padahal "
  "bahannya sederhana. Di situ selisihnya paling besar.")
I("Maka jangan digeneralkan", "hitung per lauk",
  "Karena itu jangan menyimpulkan untuk semua masakan sekaligus. Hitung per "
  "lauk, dan Anda akan menemukan dua kelompok yang berbeda.")
I("Yang murah dibeli", "biarkan dibeli",
  "Lauk yang memang murah dibeli, biarkan dibeli. Tidak ada yang perlu "
  "dibuktikan di situ.")
I("Keduanya sah", "angka Anda yang menentukan",
  "Memasak dan membeli dua-duanya sah, dan tidak ada yang benar secara umum. "
  "Yang benar adalah yang ditunjuk angka Anda. Yang tidak sah hanya memilih "
  "terus-menerus tanpa pernah melihat.")

# -------------------------------------------------------------------- cap 7
T("Dari satu porsi", "ke sebulan",
  "Sekarang langkah yang membuat ukurannya terasa.",
  cap="Dari satu porsi ke sebulan")
I("Satu porsi", "terasa kecil",
  "Selisih pada satu porsi biasanya terasa kecil. Memang kecil, dan itu "
  "sebabnya ia lolos setiap kali.")
I("Kalikan", "berapa kali sebulan",
  "Kalikan dengan berapa kali dalam sebulan Anda membeli lauk itu. Perilaku "
  "yang sama, dijumlahkan.")
I("Lalu jumlah orang", "di rumah",
  "Lalu kalikan dengan jumlah orang yang makan. Angkanya berubah cepat.")
I("Bandingkan", "dengan yang Anda kenal",
  "Untuk merasakan ukurannya, bandingkan dengan sesuatu yang Anda kenal: "
  "belanja mingguan, atau tagihan bulanan.")
I("Dan bisa juga kecil", "itu pun jawaban",
  "Bisa juga hasilnya kecil dan tidak ada yang perlu diubah. Itu pun jawaban "
  "penuh, dan sekarang ia hitungan, bukan dugaan.")
I("Bagusnya", "pilihannya kembali besok",
  "Bagusnya, pilihan ini kembali besok, dan kembali utuh. Satu bulan yang "
  "mahal tidak mengikat bulan berikutnya.")

# -------------------------------------------------------------------- cap 8
T("Yang bisa dilakukan", "hari ini",
  "Kita tutup dengan yang bisa dilakukan hari ini, dalam tiga langkah.",
  cap="Yang bisa dilakukan hari ini")
L("Tiga langkah",
  ["Pilih satu lauk", "Jumlahkan bahannya", "Bagi jumlah porsinya"],
  "Pertama: pilih satu lauk yang paling sering Anda beli jadi. Kedua: "
  "jumlahkan semua bahan untuk membuatnya di rumah. Ketiga: bagi dengan "
  "jumlah porsi yang jadi.")
I("Bandingkan sekali", "lalu simpan angkanya",
  "Bandingkan sekali dengan harga belinya, lalu simpan angka itu. Untuk lauk "
  "yang sama, hasilnya biasanya berulang.")
I("Jangan ubah semuanya", "satu lauk dulu",
  "Jangan mengubah seluruh menu sekaligus. Satu lauk dulu, yang selisihnya "
  "paling besar.")
I("Dan kalau selisihnya kecil", "Anda sudah tahu",
  "Dan kalau selisihnya kecil, Anda sudah tahu, dan tidak perlu ragu lagi "
  "setiap kali memilih.")
# EXPERIMENTO 26: o pedido e a INSCRICAO, nao o clique para o longo.
C("Tulis angka Anda", "di kolom komentar",
  "Kalau Anda menghitung, tulis satu angka saja di kolom komentar: selisih per "
  "porsi, dengan tandanya. Tanpa nama tempat, cukup selisihnya.")

# =============================== O SHORT =====================================
# EXPERIMENTO 26 — a variavel desta rodada.
# O short entrega a conta FECHADA (aprendizado 539) E gasta o pedido na
# INSCRICAO, amarrada ao metodo. Nao aponta para o video completo, porque nos
# 22 pacotes anteriores esse pedido levou a zero view no longo e zero inscrito.

SHORT = [
    {"layout": "titulo", "kicker": "Masak atau beli jadi",
     "sub": "berapa selisihnya?",
     "nar": "Masak sendiri atau beli jadi? Hitung selisihnya sekarang, dengan "
            "struk belanja Anda.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Pilih satu lauk",
     "sub": "yang sering Anda beli",
     "nar": "Pilih satu lauk yang sering Anda beli jadi.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Jumlahkan bahannya",
     "sub": "semua, termasuk bumbu",
     "nar": "Jumlahkan semua bahannya, termasuk bumbu dan minyak.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Bagi jumlah porsi",
     "sub": "lalu bandingkan",
     "nar": "Bagi dengan jumlah porsi yang jadi. Itu harga satu porsi buatan "
            "rumah. Bandingkan dengan harga belinya: selisihnya adalah "
            "jawaban Anda.", "sem_cap": True},
    {"layout": "cta", "kicker": "Kalau hitungan ini berguna",
     "sub": "subscribe, yang berikutnya di sini",
     "nar": "Kalau hitungan ini berguna, subscribe. Tiap minggu satu hitungan "
            "dapur seperti ini.", "sem_cap": True},
]

THUMB = {"l1": "Masak atau", "l2": "beli jadi"}

COPY = """# Harga satu porsi buatan rumah, dihitung dari struk belanja Anda sendiri

## TITULO
Masak Sendiri atau Beli Jadi? Hitung Harga Per Porsi dari Belanjaan Anda Sendiri

## DESCRICAO
Hampir setiap hari Anda memilih antara memasak sendiri dan membeli yang sudah jadi, dan hampir selalu pilihan itu diambil tanpa satu pun angka. Video ini bukan ajakan berhemat. Ini soal tahu berapa selisihnya, yang merupakan pertanyaan lain dan jauh lebih berguna — dan batas waktunya jelas: makan malam nanti, atau belanja besok pagi.

Tidak ada satu pun angka milik saya di video ini. Tidak ada harga bahan, tidak ada HET, tidak ada indeks, tidak ada nama pasar, aplikasi, atau rumah makan. Dua angka yang dipakai sudah ada di rumah Anda: struk belanja terakhir, dan harga yang biasa Anda bayar untuk lauk itu.

Hitungannya satu pembagian. Jumlahkan semua bahan yang dibeli untuk lauk itu — termasuk bumbu, minyak, dan yang dipakai sedikit-sedikit, karena yang sedikit itu tetap dibeli dengan uang. Lalu bagi dengan jumlah porsi yang benar-benar jadi, jujur sesuai yang biasa Anda sajikan. Hasilnya adalah harga satu porsi buatan rumah. Bandingkan dengan harga satu porsi yang biasa Anda beli, dan selisihnya dalam rupiah adalah jawabannya.

Bagian yang paling sering keliru adalah porsi: porsi di rumah biasanya lebih besar daripada porsi yang dibeli, dan kalau tidak dihitung, perbandingannya berat sebelah.

Ada satu bab tentang di mana angkanya bersembunyi: gas yang terpakai tapi tidak pernah dihitung, minyak yang masih tersisa di botol dan tidak boleh dihitung penuh, bumbu yang sudah ada di dapur dan terasa gratis padahal dulu dibeli, serta bahan yang layu dan tidak sempat dimasak.

Ada bab tentang apa yang hitungan ini TIDAK tangkap, karena lebih jujur menyebutnya: waktu Anda dan pekerjaan sesudahnya, tenaga di hari yang sudah panjang, porsi lebih untuk besok yang justru menurunkan harga per porsi, dan lauk yang di rumah tidak pernah sama rasanya. Hitungan ini tidak melarang apa pun — ia hanya memberi tahu harga dari kemudahan itu.

Dan ada kasus yang menipu: lauk yang dijual murah justru karena dimasak dalam jumlah besar, yang di rumah tidak bisa ditandingi dalam jumlah kecil. Itu skala, bukan kegagalan berhemat. Karena itu hitung per lauk, jangan menyimpulkan untuk seluruh menu sekaligus.

Penutupnya tiga langkah untuk hari ini, dengan angka yang sudah ada di dapur Anda.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Coba hitung untuk satu lauk yang paling sering Anda beli jadi, lalu tulis satu angka saja di sini: selisih per porsi, dengan tandanya. Tanpa nama tempat, tanpa harga belanja, cukup selisihnya. Saya ingin tahu seberapa jauh angka itu berbeda antar rumah.

## HASHTAGS
#UangDapur #MasakSendiri #ResepNaikLevel

## TAGS
masak sendiri atau beli jadi, harga per porsi, hitung uang dapur, biaya masak di rumah, belanja dapur hemat, menghitung porsi, biaya bahan masakan, uang belanja bulanan, masak hemat, beli lauk matang, biaya gas masak, sisa bahan, atur keuangan rumah tangga, dapur hemat, hitung sendiri

## CONFIGURACOES DO STUDIO
- Idioma: Bahasa Indonesia (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita preco de ingrediente, nao cita HET, nao cita indice de inflacao, nao cita nome de mercado, de aplicativo nem de rumah makan, e nao compara estabelecimentos entre si. Os dois numeros da conta sao do proprio espectador: o total dos ingredientes esta na nota da compra dele, e o preco do prato pronto e o que ele mesmo paga. Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa da regiao dele — o que importa aqui, porque preco de alimento no pais varia muito por provincia e por semana. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA: qualquer preco de ingrediente ou de porcao. Citar um so deles tornaria a conta errada para a maioria de quem assiste, e o video precisa exatamente do contrario. O video tambem nao diz que cozinhar e sempre mais barato — as duas respostas sao legitimas e dependem do numero de cada casa —, nao condena comprar pronto, nao recomenda estabelecimento nenhum e nao e aconselhamento financeiro nem nutricional.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/resep-naik-level-009.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-009",
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
    from ensaio import duracao_estimada, duracao_estimada_short
    grava(SPEC, "fabrica/specs/resep-naik-level-009.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
