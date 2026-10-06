"""setiap-level-015 — duas carteiras do BPJS, e a errada e a que cobra.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

O NUMERO DE PARTIDA, do PROPRIO canal e com a ULTIMA leitura de `metricas`
(aprendizado 592 — a trava do 549 acusou 170 quedas em 4.046 linhas lifetime
nesta rodada, entao `max(views)` esta proibido):

    pacote  short -> longo  dur    forma do titulo
    010        105 ->  20   521s   orgao nomeado + ano + PARADOXO resolvido
    007          0 ->  10   787s   evento nomeado + pergunta contavel + 4 passos
    006         18 ->   9  1696s   orgao nomeado (OJK) + ano + sistema
    008         76 ->   6   793s   dois numeros para o mesmo saldo
    009         12 ->   5   779s   pergunta sobre o proprio dinheiro
    005        185 ->   2   854s   listicle ("5 Biaya yang Ikut Naik")
    004        126 ->   2  1716s   conselho de sistema generico
    003         33 ->   2  1545s   meta inventada (Rp100 Juta)
    014         18 ->   2   539s   metodo, mas titulo em pergunta pura
    013         76 ->   1   549s   pergunta pura
    012          1 ->   0   564s   pergunta pura
    (so short)  566 ->   0     —   teste de 26 s

O QUE DEU CERTO: o 010, e com folga — vinte views de longo, o DOBRO do segundo
colocado, e e o mais curto entre os de cima (521 s). O titulo dele nomeia um
orgao (BPJS Kesehatan), traz o ano e monta um PARADOXO que ele mesmo resolve:
"Kelas Dihapus Tapi Iuranmu Tidak Berubah — Ini Sebabnya". O 007 e o segundo
com dez, e o caso mais interessante do canal: ZERO views de short e dez de
longo, ou seja, o longo foi achado INTEIRAMENTE fora do short.

O QUE NAO DEU: duas coisas, e as duas sao de forma, nao de assunto.
  1. Os tres maiores shorts do canal (566, 185 e 126 views) entregaram ZERO,
     DUAS e DUAS views de longo. Short que estoura nao traz ninguem.
  2. Os quatro titulos que sao PERGUNTA PURA (009, 013, 012 e 014) somam OITO
     views de longo nos quatro. Os tres que nomeiam orgao e resolvem um
     paradoxo ou contam passos (010, 007, 006) somam TRINTA E NOVE. Isso e a
     direcao dos aprendizados 589/595 aparecendo dentro deste canal.
  E os dois videos mais longos do canal (1716 s e 1545 s) deram duas views cada.

O QUE VOU MUDAR: copiar a forma do 010 — orgao nomeado, paradoxo que o proprio
titulo promete resolver, sem ponto de interrogacao — e ficar no PISO de oito
minutos em vez do teto. E o short entrega o METODO inteiro, nao a manchete.

VEREDITO DO CANAL: `canal frio` (v_maquina_licoes, 15 shorts e 18 longos
medidos, 1.300 views, mediana de longo 0,03). Pela rotina isso manda eixo novo
e piso de 8 minutos por analogia com `suspenso`.

EIXO, e por que ele e novo. Os onze pacotes medidos falam de BPJS Kesehatan
(classe), PHK e pesangon, pinjol e OJK, saque do JHT, juros de deposito,
inflacao do salario, alocacao de salario, matematica do salario diario, taxas
do extrato, PPh 21 TER, parcelamento sem juros e deposito contra SBN. NENHUM
fala do OUTRO BPJS — o BPJS Ketenagakerjaan — nem da fronteira entre os dois.
Este fala: sao DUAS carteiras, de dois orgaos, com duas regras, e usar a errada
num acidente de trabalho e o erro caro. E ha um prazo de cinco anos correndo.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ESTE VIDEO NAO CITA NENHUM VALOR EM RUPIAS. Nem um. Decisao de desenho: valor
# de teto, de reembolso e de iuran muda por regulamento e por ano, e video que
# cita a cifra nasce com data de validade. O que entra sao fatos de ESTRUTURA,
# fechados em DUAS instituicoes diferentes:
#
#   * a PP 82/2019, que altera a PP 44/2015 sobre a execucao do JKK e do JKM,
#     esta EM VIGOR. Fonte 1: jdih.kemnaker.go.id (Biro Hukum do Ministerio do
#     Trabalho, status "Berlaku", estabelecida em 29/11/2019, promulgada em
#     02/12/2019, LNRI 2019 numero 231). Fonte 2: bpjsketenagakerjaan.go.id,
#     que publica o texto integral em /assets/uploads/peraturan/.
#   * o JKK cobre acidente de trabalho E doenca causada pelo trabalho
#     (penyakit akibat kerja), com atendimento de saude "sesuai kebutuhan
#     medis" e com beneficios que vao alem do tratamento. Fonte 1: o texto da
#     PP 82/2019, Pasal 25. Fonte 2: a pagina institucional de beneficios do
#     proprio BPJS Ketenagakerjaan (/penerima-upah.html), que lista os mesmos
#     itens.
#   * Pasal 26: o direito de reivindicar o beneficio do JKK PRESCREVE em cinco
#     anos, contados do acidente ou do dia em que a doenca do trabalho foi
#     DIAGNOSTICADA. Fonte: o texto da PP 82/2019, cuja vigencia o Ministerio
#     confirma. Este e o unico numero do video, e ele e um PRAZO, nao uma
#     cifra.
#
# DESCARTADO, e por que — isto e o que eu QUERIA dizer e nao disse:
#   * os percentuais da santunan sementara tidak mampu bekerja (o salario pago
#     enquanto a pessoa nao pode trabalhar, que a pagina do BPJS descreve como
#     cem por cento nos dois primeiros semestres e metade a partir do
#     terceiro). Eram o coracao da conta, e NAO ENTRAM: fechei esses numeros em
#     UMA fonte so. O PDF da PP 44/2015 no site do BPJS baixou truncado nesta
#     rodada e o JDIH do Ministerio nao expoe o texto, entao o numero nao bateu
#     em duas fontes. Fica para a rodada que conseguir o texto.
#   * nenhum valor de reembolso de transporte, de homecare, de teto de salario
#     ou de iuran.
#   * nao digo quanto alguem vai receber, porque isso depende do caso e do
#     laudo, e nao digo que caso nenhum e ou nao e acidente de trabalho.
#
# TAMBEM FORA: isto nao e orientacao juridica e nao manda ninguem processar
# ninguem. O video diz onde o prazo esta escrito e manda a pessoa conferir o
# proprio caso na fonte.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: a DATA dele. Quantos meses sobraram dos
# cinco anos dele, contados do acidente dele ou do diagnostico dele. E
# aritmetica que ele faz com o proprio calendario, e e por isso que esta pauta
# sobrevive sem cifra nenhuma.
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
    # Trabalhadores conversando NO TRABALHO. A cena abre dizendo "kalau kamu
    # pekerja penerima upah" — se voce e trabalhador com salario. O clipe e
    # isso, e tem 16 s para uma cena de 10,3 s.
    4293960: ("https://videos.pexels.com/video-files/4293960/4293960-hd_1920_1080_25fps.mp4",
              "Tiger Lily",
              "https://www.pexels.com/video/men-having-a-conversation-while-at-work-4293960/"),
    # Trabalhadores asiaticos carregando caixas em caminhao, de um autor
    # indonesio. A cena fala do acidente que acontece TRABALHANDO, e o clipe
    # mostra o trabalho manual onde ele acontece — nao um acidente encenado,
    # de proposito. 19 s para uma cena de 8,1 s.
    37546343: ("https://videos.pexels.com/video-files/37546343/15909642_1920_1080_30fps.mp4",
               "setengah lima sore",
               "https://www.pexels.com/video/asian-workers-loading-boxes-into-truck-37546343/"),
    # Pessoa MARCANDO data no calendario, que e exatamente o que a cena manda
    # fazer. Rejeitei o 9057574 ("writing DAY OFF on a calendar") de proposito:
    # a data do capitulo e a do acidente ou do diagnostico, e um clipe
    # escrevendo "dia de folga" diria o contrario da narracao. 11 s para 9,2 s.
    9057559: ("https://videos.pexels.com/video-files/9057559/9057559-hd_1920_1080_25fps.mp4",
              "SHVETS production",
              "https://www.pexels.com/video/a-person-marking-on-calendar-9057559/"),
    # Profissional de saude PREENCHENDO FORMULARIO. O capitulo existe para
    # dizer que vale a data escrita no documento medico, nao a da lembranca —
    # o clipe e a data sendo escrita. Rejeitei os dois de paramedico em ficha
    # (8944117, 8944450): paramedico e emergencia, que e o capitulo 5, nao o
    # diagnostico. 11 s para uma cena de 9,2 s.
    8944537: ("https://videos.pexels.com/video-files/8944537/8944537-hd_1920_1080_25fps.mp4",
              "Kampus Production",
              "https://www.pexels.com/video/close-up-footage-of-medical-practitioner-filling-up-a-form-8944537/"),
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
# A resposta — qual programa cobre o caso e quantos meses sobraram do prazo —
# fecha no capitulo 3.

# -------------------------------------------------------------------- cap 1
B("Dua jaminan, bukan satu", "dan kartu kesehatanmu bukan yang itu",
  "Kalau kamu pekerja penerima upah, kamu terdaftar di dua jaminan sosial yang "
  "berbeda, bukan satu. Keduanya resmi, dan keduanya punya aturan sendiri.",
  "workers talking at their workplace", 4293960,
  cap="Dua jaminan, bukan satu")
T("Kenapa ini penting", "karena yang satu tidak menanggung urusan yang lain",
  "Ini penting karena kalau kamu cedera saat bekerja, yang menanggung bukan "
  "jaminan kesehatan biasa. Ada program lain yang dibuat khusus untuk itu.")
T("Yang pertama", "jaminan kesehatan untuk sakit sehari-hari",
  "Yang pertama kamu sudah kenal: jaminan kesehatan, yang dipakai untuk sakit "
  "sehari-hari dan jalannya lewat rujukan berjenjang dari faskes pertama.")
T("Yang kedua", "jaminan kecelakaan kerja",
  "Yang kedua namanya jaminan kecelakaan kerja, disingkat J K K, dan dia "
  "diselenggarakan oleh badan yang berbeda, bukan badan yang sama.")
T("Bedanya bukan soal rumah sakit", "bedanya soal PENYEBAB",
  "Yang memisahkan keduanya bukan rumah sakitnya dan bukan penyakitnya. Yang "
  "memisahkan adalah PENYEBABNYA: apakah kondisi itu datang dari pekerjaanmu.")
T("Contoh yang paling jelas", "punggung, pendengaran, pernapasan",
  "Contoh paling jelas bukan jatuh dari tangga. Punggung yang rusak karena "
  "mengangkat tiap hari, pendengaran yang turun karena kebisingan mesin.")
T("Dan ada hal ketiga", "yang ini cuma kamu yang punya",
  "Dan ada hal ketiga, yang tidak ada di situs mana pun: tanggal kejadian di "
  "kalendermu sendiri. Itu yang akan kita hitung sebentar lagi.")

# -------------------------------------------------------------------- cap 2
B("Yang ditanggung JKK", "dua hal, bukan satu",
  "J K K tidak menanggung satu hal, tapi dua. Yang pertama jelas: kecelakaan "
  "yang terjadi saat kamu bekerja.",
  "manual workers loading boxes", 37546343,
  cap="Yang ditanggung JKK")
T("Yang kedua jarang diketahui", "penyakit akibat kerja",
  "Yang kedua hampir tidak ada yang tahu: penyakit yang disebabkan oleh "
  "lingkungan kerjamu. Dalam aturannya ini disebut penyakit akibat kerja.")
T("Itu bukan sakit biasa", "dan itu bukan istilah longgar",
  "Penyakit akibat kerja bukan istilah longgar dan bukan sakit biasa yang "
  "kebetulan muncul saat kamu bekerja. Dia punya definisi dan punya diagnosis.")
T("Layanan kesehatannya", "sesuai kebutuhan medis",
  "Untuk kasus yang masuk J K K, layanan kesehatan diberikan sesuai kebutuhan "
  "medis. Itu rumusan yang dipakai di dalam peraturannya sendiri.")
T("Dan manfaatnya lebih dari obat", "ada santunan, ada beasiswa",
  "Manfaat J K K juga tidak berhenti di pengobatan. Ada santunan untuk masa "
  "tidak mampu bekerja, santunan cacat, santunan kematian, dan beasiswa anak.")
T("Dasar hukumnya bisa kamu buka", "peraturan pemerintah, bukan berita",
  "Semua ini tertulis di peraturan pemerintah yang bisa kamu buka sendiri. "
  "Bukan di berita tentang peraturan, tapi di dokumen peraturannya.")
T("Saya sengaja tidak menyebut angkanya", "dan itu bukan kelalaian",
  "Saya sengaja tidak menyebut nominal mana pun di sini. Nominal berubah lewat "
  "peraturan baru, dan video yang menyebut nominal lahir dengan tanggal mati.")

# -------------------------------------------------------------------- cap 3
B("Hitung batas waktumu", "lima tahun, dan jamnya sudah jalan",
  "Sekarang bagian yang mengubah urusan ini jadi mendesak. Hak menuntut "
  "manfaat J K K punya batas waktu, dan batasnya lima tahun.",
  "person marking a date on a calendar", 9057559,
  cap="Hitung batas waktumu")
T("Dari kapan dihitung", "dua tanggal yang berbeda",
  "Dan lima tahun itu dihitung dari dua tanggal yang berbeda, tergantung "
  "kasusnya. Membedakan keduanya adalah seluruh isi bagian ini.")
T("Kalau kecelakaan", "dari hari kejadiannya",
  "Kalau yang terjadi adalah kecelakaan kerja, hitungannya mulai dari hari "
  "kejadiannya. Tanggal itu biasanya kamu ingat dan ada di catatan kantor.")
T("Kalau penyakit akibat kerja", "dari hari DIAGNOSISNYA",
  "Kalau yang terjadi adalah penyakit akibat kerja, hitungannya mulai dari "
  "hari penyakit itu DIDIAGNOSIS, bukan dari hari kamu mulai merasa tidak enak.")
T("Sekarang hitung punyamu", "ambil kalender dan kurangi",
  "Sekarang angka ketiga, yang kamu hitung sendiri. Ambil tanggal kejadian "
  "atau tanggal diagnosis, tambah lima tahun, lalu kurangi dengan hari ini.")
T("Itu sisa waktumu", "dalam bulan, bukan dalam perasaan",
  "Hasilnya adalah sisa waktumu, dan tulis dalam bulan supaya terbaca. Sisa "
  "video ini hanya untuk satu hal: supaya kamu tidak salah membaca angka itu.")

T("Tulis di satu baris", "tanggal, lima tahun, sisa",
  "Tulis ketiganya berdampingan di satu baris: tanggalnya, tanggal batasnya, "
  "dan sisa bulannya. Satu baris itu adalah seluruh jawabannya.")

# -------------------------------------------------------------------- cap 4
B("Kenapa tanggal diagnosis", "dan bukan tanggal kamu merasa sakit",
  "Hal pertama yang harus kamu tahu: untuk penyakit akibat kerja, yang dipakai "
  "adalah tanggal diagnosis, dan itu bukan pilihan yang dibuat sembarangan.",
  "health professional filling in a dated form", 8944537,
  cap="Kenapa tanggal diagnosis")
T("Karena awalnya tidak kelihatan", "penyakit kerja datang perlahan",
  "Penyakit akibat kerja sering datang perlahan selama bertahun-tahun. Tidak "
  "ada hari pertama yang bisa ditunjuk, jadi tanggal mulai merasa tidak dipakai.")
T("Diagnosis itu tanggal yang tertulis", "ada di dokumen, bukan di ingatan",
  "Diagnosis, sebaliknya, punya tanggal yang tertulis di dokumen medis. Itu "
  "tanggal yang bisa dibuktikan, dan karena itu dia yang jadi titik mulai.")
T("Konsekuensinya satu", "diagnosis yang tertunda menunda jamnya",
  "Konsekuensinya langsung: selama penyakitnya belum didiagnosis, jam lima "
  "tahun itu belum mulai jalan untuk kasus penyakit akibat kerja.")
T("Tapi jangan dibaca sebaliknya", "menunda periksa bukan strategi",
  "Jangan dibaca sebaliknya. Menunda pemeriksaan bukan cara memperpanjang "
  "waktu, karena tanpa diagnosis tidak ada yang bisa diajukan sama sekali.")
T("Dan jangan pakai tanggal keluhan", "yang dipakai tanggal dokumennya",
  "Jadi jangan pakai tanggal kamu mulai mengeluh ke teman kerja. Yang dipakai "
  "adalah tanggal yang tertulis di dokumen medis, dan cuma itu.")
T("Yang perlu kamu simpan", "tanggalnya, bukan ingatanmu",
  "Yang perlu kamu lakukan sederhana: simpan tanggal yang tertulis di dokumen, "
  "bukan perkiraan dari ingatan. Dokumen bertanggal adalah seluruh buktinya.")

# -------------------------------------------------------------------- cap 5
T("Kenapa kartu bisa tertukar", "dan ini bukan tanda apa-apa",
  "Sekarang bagian yang paling sering disalahpahami. Ada banyak alasan sah "
  "kenapa orang memakai kartu yang satu untuk urusan yang seharusnya di satu lagi.",
  cap="Kenapa kartu bisa tertukar")
T("Alasan pertama", "di ruang gawat darurat tidak ada yang bertanya",
  "Alasan pertama: saat kejadian, yang penting adalah ditangani. Di ruang "
  "gawat darurat tidak ada yang berhenti untuk menanyakan penyebab pekerjaan.")
T("Alasan kedua", "kartu kesehatan yang selalu di dompet",
  "Alasan kedua: kartu jaminan kesehatan ada di dompet dan sudah biasa "
  "dipakai, sementara yang satu lagi jarang dikeluarkan sepanjang tahun.")
T("Alasan ketiga", "penyebab kerja baru jelas belakangan",
  "Alasan ketiga: kaitan dengan pekerjaan sering baru jelas berbulan-bulan "
  "kemudian, apalagi untuk kondisi yang tumbuh perlahan seperti pendengaran.")
T("Alasan keempat", "kantor pun kadang tidak melaporkan",
  "Alasan keempat: pelaporan ke program kecelakaan kerja adalah kewajiban "
  "pemberi kerja, dan kewajiban yang tidak dijalankan bukan kesalahan pekerja.")
T("Alasan kelima", "nama programnya pun mirip",
  "Alasan kelima, dan yang paling sederhana: nama kedua badan itu mirip dan "
  "keduanya disebut B P J S dalam percakapan sehari-hari.")
T("Jadi hati-hati menyimpulkan", "salah kartu bukan berarti curang",
  "Jadi kalau kartu yang dipakai ternyata yang salah, itu bukan bukti niat "
  "buruk siapa pun. Itu cuma tanda bahwa kasusnya perlu diperiksa lagi.")

# -------------------------------------------------------------------- cap 6
T("Apa arti batas lima tahun", "dan apa yang bukan artinya",
  "Setelah empat alasan itu disingkirkan, baru batas lima tahun mulai "
  "berbicara. Tapi dia berbicara lebih pelan daripada yang orang kira.",
  cap="Apa arti batas lima tahun")
T("Artinya yang pertama", "batasnya ada di peraturannya",
  "Artinya yang pertama: batas itu tertulis di peraturan pemerintah, bukan di "
  "kebijakan kantor dan bukan di kebijakan rumah sakit.")
T("Artinya yang kedua", "lewat batas, haknya gugur",
  "Artinya yang kedua: kalau batasnya lewat, hak menuntut manfaatnya gugur. "
  "Itu kata yang dipakai peraturannya, dan dia tidak punya arti lain.")
T("Yang BUKAN artinya", "bukan berarti kamu pasti dapat",
  "Yang bukan artinya: masih di dalam lima tahun tidak berarti kamu pasti "
  "menerima sesuatu. Batas waktu hanya menjaga pintunya tetap terbuka.")
T("Dan bukan berarti besarnya pasti", "nominal tergantung kasus",
  "Dan tidak berarti besarnya sudah pasti. Berapa yang diterima tergantung "
  "kasusnya dan dokumennya, dan itu bukan sesuatu yang video bisa janjikan.")
T("Dan bukan berarti otomatis", "mengajukan tetap harus dilakukan",
  "Dan tidak berarti prosesnya jalan sendiri. Batas waktu cuma mengukur "
  "sampai kapan pengajuan masih bisa diterima, bukan menggantikan pengajuan.")
T("Jadi yang kamu dapat hari ini", "satu tanggal dan satu sisa",
  "Jadi yang kamu dapat dari video ini bukan janji. Yang kamu dapat adalah "
  "satu tanggal yang jelas dan sisa waktu yang kamu hitung sendiri.")

# -------------------------------------------------------------------- cap 7
T("Yang video ini tidak katakan", "dan ini bagian yang biasanya dilewati",
  "Sekarang bagian yang biasanya dilewati. Ini hal-hal yang sengaja tidak ada "
  "di video ini, dan alasannya saya tulis satu per satu.",
  cap="Yang video ini tidak katakan")
T("Tidak ada nominal", "tidak satu rupiah pun",
  "Pertama: tidak ada nominal di sini, tidak satu rupiah pun. Angka iuran, "
  "teto dan penggantian berubah lewat peraturan baru dan ini bukan tempatnya.")
T("Tidak ada persentase santunan", "dan ini yang paling saya ingin katakan",
  "Kedua, dan ini yang paling ingin saya katakan: persentase santunan masa "
  "tidak mampu bekerja tidak masuk, karena saya hanya menemukannya di satu sumber.")
T("Kenapa itu penting", "satu sumber bukan konfirmasi",
  "Satu sumber resmi bukan konfirmasi. Aturan yang saya pakai sederhana: "
  "angka yang tidak sama di dua sumber resmi tidak masuk ke video.")
T("Tidak ada penilaian kasus", "saya tidak tahu kasusmu",
  "Ketiga: saya tidak menilai kasus siapa pun. Apakah sebuah kejadian masuk "
  "kecelakaan kerja ditentukan oleh dokumen dan pemeriksaan, bukan oleh video.")
T("Tidak ada janji hasil", "dua kasus sama bisa beda",
  "Dan kelima: tidak ada janji hasil di sini. Dua kasus yang terlihat sama "
  "bisa berakhir berbeda, karena dokumennya berbeda.")
T("Dan ini bukan nasihat hukum", "ini cara membaca tanggal",
  "Dan keempat: ini bukan nasihat hukum. Yang video ini ajarkan adalah cara "
  "membaca satu tanggal dan menghitung sisa waktu dari tanggal itu.")

# -------------------------------------------------------------------- cap 8
T("Empat langkah", "dari awal sampai selesai",
  "Sekarang seluruh pemeriksaan dalam empat langkah, supaya kamu bisa "
  "melakukannya setelah video ini ditutup.",
  cap="Empat langkah")
T("Langkah satu", "tulis dua tanggal",
  "Langkah satu: tulis dua tanggal di selembar kertas. Tanggal kejadian kalau "
  "kecelakaan, dan tanggal diagnosis kalau penyakit akibat kerja.")
T("Langkah dua", "tambah lima tahun",
  "Langkah dua: tambahkan lima tahun ke tanggal yang berlaku untuk kasusmu. "
  "Itu tanggal terakhir pintunya masih terbuka.")
T("Langkah tiga", "kurangi dengan hari ini",
  "Langkah tiga: kurangi tanggal itu dengan hari ini, dan tulis hasilnya dalam "
  "bulan. Dalam bulan, bukan dalam tahun, supaya tidak terasa jauh.")
T("Langkah empat", "cari dokumen bertanggalnya",
  "Langkah empat: cari dokumen yang memuat tanggal itu. Surat keterangan, "
  "laporan kantor atau rekam medis — yang penting tanggalnya tertulis di sana.")
T("Ulangi tiap tahun", "sisa bulanmu berubah sendiri",
  "Dan ulangi hitungan itu sekali setahun, karena sisa bulanmu berubah tanpa "
  "kamu melakukan apa pun. Angka yang kamu tulis hari ini akan mengecil.")
T("Dan satu catatan", "kalau tanggalnya tidak ada, itu langkah pertamamu",
  "Satu catatan terakhir: kalau tidak ada dokumen bertanggal, itu bukan jalan "
  "tertutup. Itu justru langkah pertamamu, dan dia tidak bisa menunggu.")

C("Tulis sisa bulanmu", "bukan kasusmu",
  "Tulis di komentar hanya berapa bulan yang tersisa dari hitunganmu, dan "
  "jenis kasusnya. Jangan tulis nama kantor atau rincian medismu.")

THUMB = {"l1": "Dua kartu", "l2": "5 tahun"}


SHORT = [
    {"layout": "titulo", "kicker": "Dua kartu, satu kejadian",
     "sub": "dan yang salah yang bikin repot",
     "nar": "Kamu punya dua jaminan sosial, bukan satu. Dan kecelakaan kerja "
            "bukan urusan kartu kesehatanmu.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Satu", "sub": "jaminan kecelakaan kerja",
     "nar": "Satu: kecelakaan kerja dan penyakit akibat kerja masuk program "
            "yang lain, dari badan yang lain.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Dua", "sub": "ada batas lima tahun",
     "nar": "Dua: hak menuntutnya gugur setelah lima tahun, dan jamnya sudah "
            "jalan sekarang.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Tiga", "sub": "dari tanggal mana",
     "nar": "Tiga: dari hari kejadian kalau kecelakaan, dari hari diagnosis "
            "kalau penyakit akibat kerja.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Hitung", "sub": "tambah lima, kurangi hari ini",
     "nar": "Tambah lima tahun ke tanggal itu, kurangi hari ini, dan tulis "
            "sisanya dalam bulan. Itu angkamu.", "sem_cap": True},
]


COPY = """# setiap-level-015

## TITULO
Dua Kartu BPJS, Satu Kecelakaan: Ada Batas 5 Tahun dan Jamnya Sudah Jalan

## TITULO SHORT
Dua kartu BPJS: 5 tahun, dari tanggal mana

## DESCRICAO
Kalau kamu pekerja penerima upah, kamu terdaftar di dua jaminan sosial yang
berbeda — bukan satu. Dan kecelakaan kerja bukan urusan kartu jaminan
kesehatan yang ada di dompetmu. Video ini tidak menyebut satu nominal pun, dan
itu disengaja. Yang diajarkan adalah cara mengetahui kasus mana masuk program
mana, dan cara menghitung sendiri sisa batas waktumu.

Jaminan kecelakaan kerja, disingkat JKK, tidak menanggung satu hal tapi dua:
kecelakaan yang terjadi saat bekerja, dan penyakit yang disebabkan oleh
lingkungan kerja — yang dalam aturannya disebut penyakit akibat kerja. Untuk
kasus yang masuk JKK, layanan kesehatan diberikan sesuai kebutuhan medis, dan
manfaatnya tidak berhenti di pengobatan: ada santunan masa tidak mampu
bekerja, santunan cacat, santunan kematian dan beasiswa anak.

Yang paling sering tidak diketahui adalah batas waktunya. Hak menuntut manfaat
JKK gugur setelah lima tahun. Dan lima tahun itu dihitung dari dua tanggal yang
berbeda: dari hari kejadian kalau yang terjadi adalah kecelakaan kerja, dan
dari hari penyakit itu DIDIAGNOSIS kalau yang terjadi adalah penyakit akibat
kerja — bukan dari hari pertama kamu merasa tidak enak. Perbedaan itu yang
membuat banyak kasus penyakit kerja terhitung salah.

Angka ketiga hanya kamu yang punya: tanggal di kalendermu. Ambil tanggal
kejadian atau tanggal diagnosis, tambahkan lima tahun, kurangi dengan hari
ini, dan tulis hasilnya dalam bulan.

Sebelum menyimpulkan apa pun, video ini menyebut empat alasan sah kenapa orang
memakai kartu yang salah: di ruang gawat darurat tidak ada yang menanyakan
penyebab pekerjaan; kartu kesehatan yang selalu ada di dompet; kaitan dengan
pekerjaan yang baru jelas berbulan-bulan kemudian; dan pelaporan yang menjadi
kewajiban pemberi kerja. Kartu yang salah bukan bukti niat buruk siapa pun.

Dasar hukumnya adalah Peraturan Pemerintah Nomor 82 Tahun 2019, yang mengubah
Peraturan Pemerintah Nomor 44 Tahun 2015 tentang penyelenggaraan JKK dan JKM.
Statusnya berlaku, dan teksnya bisa kamu buka sendiri — bukan berita tentang
peraturan, tapi dokumen peraturannya.

Video ini tidak menyebut nominal apa pun, tidak menyebut persentase santunan,
tidak menilai kasus siapa pun, dan bukan nasihat hukum. Persentase santunan
masa tidak mampu bekerja sengaja tidak masuk karena hanya ditemukan di satu
sumber resmi, dan satu sumber bukan konfirmasi.

Bab:
00:00 Dua jaminan, bukan satu
01:08 Yang ditanggung JKK
02:16 Hitung batas waktumu
03:24 Kenapa tanggal diagnosis
04:32 Kenapa kartu bisa tertukar
05:40 Apa arti batas lima tahun
06:48 Yang video ini tidak katakan
07:56 Empat langkah

Tulis di komentar hanya berapa bulan yang tersisa dari hitunganmu dan jenis
kasusnya — jangan tulis nama kantor atau rincian medismu.

## DISCLOSURE
Narasi dan visual video ini dibuat dengan kecerdasan buatan. Fakta yang disebut
berasal dari sumber resmi yang disebutkan dalam deskripsi.

## HASHTAGS
#JKK #BPJSKetenagakerjaan #HakPekerja

## TAGS
jaminan kecelakaan kerja, jkk bpjs ketenagakerjaan, penyakit akibat kerja, batas waktu klaim jkk, pp 82 tahun 2019, bpjs ketenagakerjaan, beda bpjs kesehatan dan ketenagakerjaan, santunan kecelakaan kerja, hak pekerja penerima upah, cara klaim jkk, kecelakaan saat bekerja, dokumen bertanggal klaim, kedaluwarsa klaim lima tahun, lapor kecelakaan kerja, pekerja penerima upah

## COMENTARIO FIXADO
Empat langkah: tulis tanggal kejadian atau tanggal diagnosis → tambah lima
tahun → kurangi dengan hari ini dan tulis sisanya dalam bulan → cari dokumen
yang memuat tanggal itu. Kalau dokumen bertanggalnya tidak ada, itu langkah
pertamamu. Tulis di sini hanya sisa bulanmu dan jenis kasusnya.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/setiap-level-015.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "setiap-level",
    "pacote": "setiap-level-015",
    "idioma": "id",
    "voz": "id-ID-ArdiNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1E2A38", "c1": "#C2410C", "c2": "#0F766E", "bg": "#F7F4EE"},
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena, GAP_CENA_S
    grava(SPEC, "fabrica/specs/setiap-level-015.json")
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
        t += duracao_cena(c.get("nar", ""), SPEC["voz"]) + GAP_CENA_S
    if ult:
        print(f"  cap {ult[0]!r}: {t - ult[1]:.1f}s  (ultimo)")
