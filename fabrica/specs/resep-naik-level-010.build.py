#!/usr/bin/env python3
"""Monta a spec resep-naik-level-010.

ALAVANCA ATACADA: **A — conversao pela FORMA**, mas aqui a conversao que falha
nao e short -> inscrito: e **short -> longo**, e este canal tem o sinal mais
limpo da frota sobre ela.

NUMERO DE PARTIDA, medido em 04/10/2026 em dado de vida inteira (ultima linha
de `videos.list` por video — nunca `max(views)`, aprendizado 557):

    pacote   short    longo    travessia
    004        41       26       63,4%
    005        63        5        7,9%
    006        26        6       23,1%
    007        44        6       13,6%
    008       994        6        0,60%
    009      1064        0        0,00%

    resep-naik-level: 23 pacotes, 2.329 views de canal
    veredito: `suspenso`

O QUE DEU CERTO, e e grande: os shorts 008 e 009 fizeram **994 e 1.064 views**.
Fora do epomeno-epipedo (1.444 e 1.714) nao existe short assim na frota. Este
canal SABE fazer short que anda.

O QUE NAO DEU, e e a coisa mais nitida que eu medi ate hoje: **a travessia e
inversamente proporcional ao alcance do short.** O short de 41 views levou 63%
da sua audiencia para o longo. O de 1.064 levou ZERO — o longo do 009 esta com
views zero e `sem_sinal`. Nao e ruido: a serie e monotona nos dois extremos.

E da para dizer por que, e a causa esta no proprio registro: **nos seis pares,
o titulo do longo e IDENTICO ao titulo do short.** O 009 e o caso puro — a
copy dele nao tem secao `## TITULO SHORT`, entao o short herdou os oitenta e um
caracteres do longo (aprendizado 548, que so foi corrigido em 02/10). Quem
assistiu ao short ve, no fim, um convite para um video cujo titulo diz que ele
JA VIU AQUILO. O CTA nao esta prometendo nada.

Tambem da para ver DUAS audiencias, e isso muda o desenho:
  * titulo com numero institucional (Beras Rp15.545 da BPS, HET do minyak
    goreng, LPG sem preco nacional, Menu Rp100 mil) -> alcance pequeno,
    travessia de 7,9% a 63%. Publico morno, poucos, atravessam.
  * titulo com contagem na propria cozinha (Gula/Garam/Minyak "quatro colheres,
    uma colher de cha, cinco colheres"; Masak sendiri ou comprar feito, preco
    por porcao) -> alcance grande, travessia ~zero. Publico frio, muitos, nao
    atravessam.
Isso tem a MESMA forma do aprendizado 482 no epomeno (os dois shorts mais
vistos converteram 0,13%; o menos visto converteu 1,47%). Alcance grande vem de
um publico diferente, e nao do mesmo publico em maior numero.

O QUE MUDO POR CAUSA DISSO — e so isto, para a medida ficar legivel:
1. **O SHORT MANTEM A FORMA QUE VENCEU**: contagem fechada na propria cozinha,
   com o resultado. E o que mediu 994 e 1.064.
2. **OS DOIS TITULOS PASSAM A SER DIFERENTES.** O short tem secao
   `## TITULO SHORT` propria, com a conta. O titulo do LONGO promete
   exatamente o que o short NAO entrega: de onde o numero vem e os quatro
   lugares onde ele e feito. Primeira vez neste canal que o CTA aponta para
   algo novo.
3. **TRES CENAS COM FOOTAGE** (`layout: "broll"`), link resolvido na spec pela
   pre-busca. Este canal nunca teve uma cena broll, e a pauta pede: tempo de
   sampah, struk, lista de belanja.

O que NAO mudo: voz, paleta, trilha e idioma ficam. Tres variaveis de uma vez
ja e o limite.

--------------------------------------------------------------- DIMENSIONAMENTO

`suspenso`: piso de oito minutos, e o melhor material vai no short. Com o longo
em 0,11 views/dia de mediana, dimensionar para treze minutos seria gastar render
em algo que ninguem termina.

Oito capitulos, cada um com ~68s NA ESTIMATIVA — nunca 60, e nunca entre 60 e
64,2 (`prontidao.MARGEM_CAP`, aprendizado 553). A id-ID-GadisNeural desvia
+1,7%, que empurra o capitulo para CIMA e e o lado seguro do portao; mas o
desvio nao tem sinal fixo, entao a margem fica de pe.

A resposta fecha no fim do capitulo 3. O tempo REAL sai do `legendas.srt`.

Cenas de footage com narracao CURTA (~10s) de proposito: `escolher` recusa
clipe mais curto que a fala e `FOLGA_S` cobra 3s acima da estimativa.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **o unico gasto da casa que nao tem struk — o que foi comprado e
jogado fora sem ser comido.**

Os eixos ja publicados neste canal sao beras/BPS, menu de Rp100 mil, minyak
goreng/HET, LPG 3 kg, gula-garam-minyak em colheres, e masak sendiri contra
beli jadi. Nenhum deles e desperdicio. E ele e o unico da lista em que o
espectador tem os dois numeros em casa AGORA, sem depender de preco oficial
nenhum.

ESTRUTURA DO OUTLIER: `v_maquina_formatos` mede "sistema de gestao do dinheiro
da cozinha" como o formato de melhor desempenho do nicho (vd mediana 1.167,4,
medido em 13/08/2026), acima de "lista de truques" (566,5) e "haul de belanja
com budget" (433,3). Este pacote e um sistema, nao uma lista.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que ele comprou com o dinheiro dele;
2. e ESCOLHA COM PRAZO — a proxima ida ao mercado;
3. o SHORT entrega a conta — a soma fechada, com o resultado.

FONTES: este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao
institucional. Nao cita preco de nada, nao cita HET, nao cita media nacional de
desperdicio, nao cita estudo e nao cita nome de mercado nem de marca. Os dois
numeros da conta sao do proprio espectador: o que ele jogou fora (que ele ve) e
o preco daquilo (que esta no struk dele). Nao ha numero meu para certificar em
duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa
da regiao dele.

O QUE O VIDEO NAO FAZ: nao diz quanto e "muito" desperdicio, nao compara o
espectador com media nenhuma, nao culpa ninguem, nao promete economia em
porcentagem e nao e aconselhamento financeiro.
"""
import json

CENAS = []

# Links resolvidos em 04/10/2026 pela pre-busca rodada do sandbox, onde
# `api.pexels.com` responde — do runner do GitHub ela da TimeoutError e do meu
# runner o proxy devolve 403 para os dois hosts. `--conferir`: 3/3 clipes que o
# CDN entrega. Com o link gravado o pacote tambem fica REPRODUZIVEL: sem ele,
# dois renders da mesma spec pegam clipes diferentes, porque o Pexels reordena.
#
# A CENA 0 FOI ESCOLHIDA A MAO, e o motivo importa. A busca por "food scraps in
# a kitchen trash bin" devolveu 7668957, que e PAPEL AMASSADO num cesto — e o
# capitulo fala do lixo de COMIDA. Sondei cinco consultas e o Pexels nao tem
# lixo de alimento: "throwing food into the garbage" devolve papel amassado nas
# duas primeiras posicoes, e "vegetable peels and food waste" devolve gente
# descascando legume, que e exatamente o que o capitulo 6 diz que NAO conta.
# Clipe que contradiz a narracao e pior que nenhum clipe. 6994930 e uma pessoa
# conferindo o que tem dentro da geladeira: fala do mesmo assunto sem afirmar
# nada, e ainda antecipa a quarta causa do capitulo 4 ("esquecer que o
# alimento existe").
BROLL = {
    6994930: ("https://videos.pexels.com/video-files/6994930/6994930-hd_1280_720_30fps.mp4",
              "Kindel Media",
              "https://www.pexels.com/video/woman-checking-items-inside-her-refrigerator-6994930/"),
    6962695: ("https://videos.pexels.com/video-files/6962695/6962695-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/a-person-typing-on-calculator-6962695/"),
    5717448: ("https://videos.pexels.com/video-files/5717448/5717448-hd_1280_720_25fps.mp4",
              "Polina",
              "https://www.pexels.com/video/person-writing-a-new-year-resolution-5717448/"),
}


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def B(kicker, sub, nar, q, pexels_id=None, cap=None):
    """Abertura de capitulo COM FOOTAGE.

    `copy_md` aceita `broll` ao lado de `titulo` como cena que abre secao.
    `broll_q` fica gravado mesmo com o link resolvido: e o que permite refazer
    a pre-busca no dia em que o clipe sair do Pexels.
    """
    c = {"layout": "broll", "kicker": kicker, "sub": sub, "nar": nar,
         "broll_q": q}
    if pexels_id and pexels_id in BROLL:
        link, autor, pagina = BROLL[pexels_id]
        c["broll_url"] = link
        c["broll_credito"] = {"pexels_id": pexels_id, "autor": autor,
                              "url": pagina}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def I(kicker, preco, nar):
    CENAS.append({"layout": "item", "kicker": kicker, "preco": preco,
                  "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ======================= OS PRIMEIROS 200 SEGUNDOS ===========================

# -------------------------------------------------------------------- cap 1
B("Satu pengeluaran di rumah", "yang tidak punya struk",
  "Ada satu pengeluaran di rumah Anda yang tidak pernah punya struk. Isinya "
  "tempat sampah dapur, dan tidak ada yang menimbangnya.",
  "person checking what is inside the refrigerator", 6994930,
  cap="Angka yang tidak pernah ditimbang")
I("Semua yang lain tercatat", "yang ini tidak",
  "Belanja punya struk. Listrik punya tagihan. Cicilan punya tanggal. Yang "
  "dibuang tidak punya apa-apa — jadi tidak pernah masuk hitungan siapa pun, "
  "termasuk hitungan Anda sendiri.")
I("Dan ini bukan soal salah", "ini soal ukuran",
  "Ini bukan soal menyalahkan siapa pun. Setiap rumah membuang sesuatu. Yang "
  "perlu Anda tahu cuma ukurannya, karena ukuran itulah yang menentukan apa "
  "yang berubah di belanja berikutnya.")
I("Tidak ada angka saya", "dua-duanya angka Anda",
  "Dalam hitungan ini tidak ada satu pun angka saya. Tidak ada harga, tidak "
  "ada rata-rata, tidak ada nama pasar. Dua angkanya ada di rumah Anda hari "
  "ini: satu di tempat sampah, satu di struk.")
I("Dan batas waktunya jelas", "belanja berikutnya",
  "Batas waktunya juga milik Anda sendiri: belanja berikutnya. Dua bab lagi "
  "dan hitungannya sudah selesai.")

# -------------------------------------------------------------------- cap 2
T("Angka pertama", "dari tempat sampah",
  "Angka pertama datang dari tempat sampah, dan cara mengambilnya penting — "
  "kalau salah, angkanya jadi besar tanpa alasan.",
  cap="Angka pertama: dari tempat sampah")
I("Yang dihitung", "dulunya makanan",
  "Yang dihitung cuma satu jenis: barang yang tadinya makanan dan dibuang "
  "tanpa dimakan. Sayur yang layu di kulkas, nasi sisa yang basi, lauk yang "
  "tidak dihabiskan, buah yang telat.")
I("Yang tidak dihitung", "memang bukan makanan",
  "Yang tidak dihitung: kulit, tulang, biji, ampas, cangkang. Itu memang tidak "
  "pernah akan masuk mulut siapa pun, jadi memasukkannya cuma membesarkan "
  "angka dan mengaburkan masalahnya.")
I("Jadi hari ini", "satu catatan saja",
  "Jadi hari ini, satu catatan saja, di kertas atau di ponsel. Setiap kali ada "
  "yang dibuang tanpa dimakan, tulis namanya dan kira-kira berapa banyak. "
  "Bukan dari ingatan — saat kejadian.")
I("Satu minggu cukup", "tujuh hari saja",
  "Satu minggu sudah cukup untuk angka yang jujur. Tujuh hari, karena belanja "
  "dan masak berulang dalam tujuh hari — satu hari saja bisa kebetulan.")

# -------------------------------------------------------------------- cap 3
B("Angka kedua", "sudah tercetak",
  "Angka kedua tidak perlu Anda taksir. Angka itu sudah tercetak, dan ada di "
  "struk belanja Anda sendiri.",
  "hands holding a paper receipt", 6962695,
  cap="Angka kedua, dan jumlahnya")
I("Cari harganya", "satu per satu",
  "Ambil struk minggu ini dan cari harga setiap barang yang ada di catatan "
  "Anda. Kalau yang dibuang cuma separuh, ambil separuh harganya. Kalau "
  "barangnya dibeli tanpa struk, pakai harga terakhir yang Anda ingat bayar.")
I("Lalu jumlahkan", "itu angka seminggu",
  "Lalu jumlahkan semuanya. Itu angka seminggu Anda, dalam rupiah: uang yang "
  "sudah keluar dari dompet Anda dan tidak pernah jadi makanan.")
I("Kali lima puluh dua", "itu angka setahun",
  "Dan kalikan lima puluh dua. Itu angka setahun. Bukan ramalan — itu minggu "
  "Anda sendiri, diulang seperti minggu memang berulang.")
I("Hitungannya selesai", "sisanya: dari mana",
  "Hitungannya sudah selesai. Bab-bab berikutnya menjawab pertanyaan yang baru "
  "muncul sekarang: kenapa angkanya sebesar itu, dan di mana dia dibuat.")

# ================= DEPOIS DA RESPOSTA — POR QUE CONTINUAR ====================

# -------------------------------------------------------------------- cap 4
T("Kenapa angkanya besar", "empat tempat, bukan satu",
  "Angka itu hampir selalu lebih besar dari yang diduga, dan penyebabnya bukan "
  "satu. Ada empat tempat berbeda, dan tiap tempat punya jalan keluar sendiri.",
  cap="Empat tempat angkanya dibuat")
I("Pertama", "dibeli terlalu banyak",
  "Pertama: dibeli lebih banyak dari yang akan dimasak. Belanja sering dibuat "
  "untuk seminggu penuh, padahal masaknya tidak tujuh hari — ada hari pesan "
  "dari luar, ada hari makan di tempat lain.")
I("Kedua", "disimpan dengan cara salah",
  "Kedua: disimpan dengan cara yang memperpendek umurnya. Barang yang sama "
  "bisa bertahan dua hari atau dua minggu, dan yang menentukan cuma di mana "
  "dan bagaimana dia ditaruh.")
I("Ketiga", "dimasak lebih dari yang dimakan",
  "Ketiga: dimasak lebih banyak dari yang dimakan. Ini yang paling sering "
  "berulang, karena porsi diukur dengan tangan, bukan dengan jumlah orang yang "
  "benar-benar akan makan hari itu.")
I("Keempat", "lupa barangnya ada",
  "Keempat, dan yang paling sunyi: lupa barangnya ada. Yang tidak terlihat "
  "tidak dimasak, dan yang tidak dimasak akhirnya dibuang — tanpa pernah "
  "diputuskan oleh siapa pun.")

# -------------------------------------------------------------------- cap 5
B("Empat penyebab", "empat langkah",
  "Empat penyebab, empat langkah. Dan keempatnya bisa mulai di belanja "
  "berikutnya, tanpa alat apa pun.",
  "person writing a shopping list on paper", 5717448,
  cap="Empat langkah, satu per penyebab")
I("Untuk yang pertama", "belanja untuk hari masak",
  "Untuk yang pertama: hitung dulu berapa hari Anda benar-benar akan masak "
  "minggu ini, lalu belanja untuk hari-hari itu. Bukan untuk tujuh hari karena "
  "seminggu ada tujuh hari.")
I("Untuk yang kedua", "satu barang, satu kali",
  "Untuk yang kedua: ambil satu barang yang paling sering layu di rumah Anda, "
  "dan cari satu kali saja cara menyimpannya lebih lama. Satu barang, bukan "
  "semua — yang satu itu sudah mengubah angkanya.")
I("Untuk yang ketiga", "hitung orangnya dulu",
  "Untuk yang ketiga: sebelum menakar, hitung berapa orang yang makan hari "
  "ini. Masak untuk jumlah itu, dan kalau memang mau ada sisa, putuskan "
  "sisanya untuk besok — bukan kebetulan.")
I("Untuk yang keempat", "yang terlihat, dimasak",
  "Untuk yang keempat: taruh yang paling cepat rusak di tempat yang pertama "
  "Anda lihat saat membuka kulkas. Yang terlihat akan dimasak. Itu seluruh "
  "triknya.")

# -------------------------------------------------------------------- cap 6
T("Yang sengaja tidak masuk", "supaya angkanya jujur",
  "Sekarang bagian yang lebih baik dikatakan daripada disembunyikan: ada tiga "
  "hal yang sengaja TIDAK masuk hitungan ini.",
  cap="Yang tidak masuk hitungan")
I("Kulit, tulang, ampas", "bukan kerugian",
  "Kulit, tulang, biji dan ampas tidak masuk, dan tidak boleh masuk. Itu tidak "
  "pernah akan dimakan, jadi dia bukan uang yang hilang — dia bagian dari "
  "harga bahan yang memang begitu.")
I("Yang Anda berikan", "tidak dibuang",
  "Yang Anda berikan ke orang lain juga tidak masuk. Itu bukan dibuang, itu "
  "dipakai — cuma bukan oleh Anda. Memasukkannya akan membuat angka Anda "
  "terlihat buruk karena hal yang baik.")
I("Yang masih sempat", "dibekukan atau dimasak",
  "Dan yang masih sempat dibekukan atau dimasak sebelum rusak tidak masuk "
  "juga. Dia selamat. Hitungan ini cuma tentang yang sudah tidak bisa "
  "diselamatkan lagi.")
I("Dan satu hasil mungkin", "angkanya kecil",
  "Satu kemungkinan terakhir, dan itu hasil yang sah: angka Anda keluar kecil. "
  "Kalau begitu, rumah Anda sudah rapi di sisi ini, dan uangnya hilang di "
  "tempat lain — bukan di sini.")

# -------------------------------------------------------------------- cap 7
T("Belanja berikutnya", "satu perubahan saja",
  "Angka itu sekarang ada. Kerjanya cuma satu, dan terjadi di belanja "
  "berikutnya.",
  cap="Belanja berikutnya: satu perubahan")
I("Jangan ubah semuanya", "satu hal cukup",
  "Jangan ubah empat hal sekaligus. Pilih satu penyebab yang paling besar di "
  "catatan Anda, dan kerjakan cuma itu selama satu bulan.")
I("Ukur lagi setelah sebulan", "dua angka, bukan satu",
  "Lalu ulangi pencatatan satu minggu lagi, sebulan kemudian. Sekarang Anda "
  "punya dua angka, dan selisih dua angka itu yang memberi tahu apakah "
  "langkahnya bekerja — bukan perasaan.")
I("Dan kalau tidak berubah", "ganti penyebabnya",
  "Kalau angkanya tidak berubah, berarti Anda memilih penyebab yang salah, "
  "bukan berarti caranya tidak jalan. Ganti ke penyebab berikutnya dan ukur "
  "lagi.")
I("Yang tidak video ini bilang", "berapa yang wajar",
  "Dan satu hal yang video ini tidak akan bilang: berapa angka yang wajar. "
  "Itu tergantung berapa orang di rumah Anda dan apa yang Anda masak, dan itu "
  "Anda yang tahu, bukan saya. Yang bisa saya bilang cuma ini: angka yang "
  "turun bulan depan lebih berguna daripada angka yang kecil hari ini.")

# -------------------------------------------------------------------- cap 8
T("Hari ini, tiga langkah", "tanpa alat apa pun",
  "Jadi hari ini, tiga langkah, dan ketiganya pakai barang yang sudah ada di "
  "rumah Anda.",
  cap="Tiga langkah hari ini")
I("Langkah pertama", "satu catatan, tujuh hari",
  "Pertama: buka satu catatan di ponsel dan beri nama minggu ini. Setiap kali "
  "ada yang dibuang tanpa dimakan, tulis namanya dan jumlahnya saat itu juga.")
I("Langkah kedua", "simpan struknya",
  "Kedua: simpan struk belanja minggu ini, jangan dibuang. Tanpa struk, angka "
  "kedua jadi taksiran, dan taksiran tidak bisa dibandingkan bulan depan.")
I("Langkah ketiga", "jumlahkan, lalu kali lima puluh dua",
  "Ketiga: di hari ketujuh, cocokkan catatan dengan struk, jumlahkan, dan "
  "kalikan lima puluh dua. Itu angka Anda, dan dia baru ada karena Anda "
  "mencatatnya.")
C("Tulis selisihnya di bawah", "bukan belanja, bukan gaji",
  "Dan di kolom komentar, tulis satu hal saja: angka seminggu Anda, dalam "
  "rupiah. Bukan total belanja, bukan penghasilan — cuma yang dibuang.")


# =============================== O SHORT =====================================
# A FORMA QUE VENCEU NESTE CANAL: contagem fechada na propria cozinha, com o
# resultado. Foi ela que mediu 994 e 1.064 views. O que fica para o longo e DE
# ONDE o numero vem, nao o numero.

SHORT = [
    {"layout": "titulo", "kicker": "Pengeluaran tanpa struk",
     "sub": "isinya tempat sampah",
     "nar": "Ada satu pengeluaran di rumah Anda yang tidak punya struk: isi "
            "tempat sampah dapur.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Pertama", "sub": "catat yang dibuang",
     "nar": "Pertama: tujuh hari, catat apa saja yang dibuang tanpa dimakan. "
            "Bukan kulit, bukan tulang.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Kedua", "sub": "harganya ada di struk",
     "nar": "Kedua: cari harganya di struk belanja Anda sendiri, lalu "
            "jumlahkan.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Itu angka seminggu",
     "sub": "kali lima puluh dua",
     "nar": "Itu angka seminggu Anda. Kalikan lima puluh dua, dan itu angka "
            "setahun.", "sem_cap": True},
    {"layout": "cta", "kicker": "Di mana angkanya dibuat",
     "sub": "empat tempat, di bawah",
     "nar": "Di mana angka itu dibuat, ada empat tempat, dan semuanya di video "
            "di bawah.", "sem_cap": True},
]

THUMB = {"l1": "Uang di", "l2": "tempat sampah"}

COPY = """# Uang yang dibuang sebelum dimakan: dari mana angkanya datang

## TITULO
Uang yang Dibuang Sebelum Dimakan: Empat Tempat Angka Itu Dibuat

## TITULO SHORT
Pengeluaran yang tidak punya struk

## DESCRICAO
Belanja punya struk. Listrik punya tagihan. Cicilan punya tanggal jatuh tempo. Tapi ada satu pengeluaran di rumah Anda yang tidak punya apa-apa, dan karena itu tidak pernah masuk hitungan siapa pun, termasuk hitungan Anda sendiri: isi tempat sampah dapur. Barang yang sudah dibeli dengan uang Anda, lalu dibuang tanpa pernah dimakan.

Dalam video ini tidak ada satu pun angka saya. Tidak ada harga, tidak ada HET, tidak ada rata-rata nasional, tidak ada nama pasar atau merek. Dua angka hitungannya ada di rumah Anda hari ini, dan dua-duanya milik Anda: satu ada di tempat sampah, satu lagi sudah tercetak di struk belanja Anda.

Cara mengambil angka pertama penting, karena kalau salah, angkanya jadi besar tanpa alasan. Yang dihitung cuma barang yang tadinya makanan dan dibuang tanpa dimakan: sayur yang layu, nasi yang basi, lauk yang tidak dihabiskan, buah yang telat. Yang tidak dihitung adalah kulit, tulang, biji, ampas dan cangkang — itu memang tidak pernah akan dimakan siapa pun. Catat saat kejadian, bukan dari ingatan, selama tujuh hari, karena belanja dan masak berulang dalam tujuh hari dan satu hari saja bisa kebetulan.

Angka kedua tidak perlu ditaksir. Ambil struk minggu ini dan cari harga setiap barang yang ada di catatan Anda; kalau yang dibuang cuma separuh, ambil separuh harganya. Jumlahkan semuanya, dan itu angka seminggu Anda dalam rupiah. Kalikan lima puluh dua untuk angka setahun — bukan ramalan, cuma minggu Anda sendiri diulang seperti minggu memang berulang.

Satu bab menjawab kenapa angkanya hampir selalu lebih besar dari yang diduga, dan di situ ada empat tempat berbeda yang masing-masing punya jalan keluar sendiri: dibeli lebih banyak dari yang akan dimasak; disimpan dengan cara yang memperpendek umurnya; dimasak lebih banyak dari yang dimakan; dan yang paling sunyi, lupa barangnya ada. Bab setelahnya memberi satu langkah untuk tiap penyebab, dan semuanya bisa mulai di belanja berikutnya tanpa alat apa pun.

Satu bab lagi tentang apa yang sengaja TIDAK masuk hitungan, karena lebih baik dikatakan daripada disembunyikan: kulit dan tulang, yang Anda berikan ke orang lain, dan yang masih sempat dibekukan atau dimasak sebelum rusak. Dan ada satu kemungkinan yang juga hasil yang sah — angka Anda keluar kecil, yang berarti uangnya hilang di tempat lain, bukan di sini.

Bab terakhir tentang cara memakai angka itu: pilih satu penyebab saja, kerjakan sebulan, lalu ukur lagi satu minggu. Selisih dua angka itulah yang memberi tahu apakah langkahnya bekerja — bukan perasaan.

Di akhir, tiga langkah, semuanya dengan barang yang sudah ada di rumah Anda hari ini.

Footage: Pexels (lisensi bebas) — Kindel Media, Mikhail Nilov, Polina.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Setelah tujuh hari, tulis satu hal saja di bawah: angka seminggu Anda, dalam rupiah. Bukan total belanja, bukan penghasilan — cuma yang dibuang tanpa dimakan. Dan kalau angkanya kecil, tulis juga; saya mau tahu seberapa jauh angka ini berbeda antar rumah.

## HASHTAGS
#DapurHemat #UangDapur #ResepNaikLevel

## TAGS
sisa makanan, buang makanan, hemat uang dapur, uang belanja dapur, cara hemat belanja dapur, struk belanja, catat pengeluaran dapur, menyimpan sayur agar tahan lama, porsi masak, belanja mingguan, kulkas rapi, hemat rumah tangga, keuangan rumah tangga, dapur hemat, menghitung pengeluaran

## CONFIGURACOES DO STUDIO
- Idioma: Indonesio (id) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Indonesia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita preco de alimento, nao cita HET, nao cita media nacional nem regional de desperdicio, nao cita estudo, nao cita nome de mercado nem de marca, e nao compara o espectador com media nenhuma. Os dois numeros da conta sao do proprio espectador: o que ele jogou fora sem comer (que ele observa e anota na semana) e o preco daquilo (que esta impresso no struk dele). Nao ha numero meu para certificar em duas fontes, e por isso nao ha numero meu que possa envelhecer nem que dependa da regiao, do mercado ou do tamanho da familia dele. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) qualquer estatistica de desperdicio de alimentos, porque ela so serviria para dizer ao espectador se ele esta acima ou abaixo da media, e o video nao faz essa comparacao — a conta e sobre a casa dele, nao sobre o pais; (2) qualquer preco de referencia, porque varia por regiao e por semana na Indonesia, e um preco meu tornaria a conta errada para a maioria de quem assiste, justamente quando o preco certo esta impresso no papel que ele tem na mao; (3) qualquer prazo de validade ou tempo de conservacao em dias, porque depende do produto, da embalagem e da geladeira dele, e citar um numero ali seria afirmacao que eu nao posso certificar. O video tambem nao diz quanto desperdicio e "muito", nao culpa ninguem, nao promete economia em porcentagem e nao e aconselhamento financeiro. SOBRE O FOOTAGE: tres cenas usam b-roll do Pexels sob licenca livre, com os tres clipes resolvidos NA SPEC (`broll_url`, `broll_credito`) em vez de buscados em tempo de render. A cena 0 foi escolhida A MAO depois que a busca devolveu papel amassado num cesto para um capitulo que fala de lixo de COMIDA: o Pexels nao tem o assunto, e clipe que contradiz a narracao e pior que nenhum clipe. Os autores vao creditados por nome na propria descricao: Kindel Media, Mikhail Nilov e Polina.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/resep-naik-level-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "resep-naik-level",
    "pacote": "resep-naik-level-010",
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
    grava(SPEC, "fabrica/specs/resep-naik-level-010.json")
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
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
