#!/usr/bin/env python3
"""Monta a spec seviye-seviye-009.

ALAVANCA ATACADA: **A — conversao short -> inscrito**, com a forma da pauta
escolhida pelo que o PROPRIO canal ja mostrou, e o short carregando o
experimento 26.

NUMERO DE PARTIDA, medido em 01/09/2026 video a video (22 registros):

    seviye-seviye ..... 3 inscritos, 4.195 views
                        short: mediana 5,57 views/dia, topo 34,34
                        longo: mediana 22,69 views/dia
                        veredito: `liberado` (12-15 min)
                        NOVE DUPLICATAS no ar do mesmo titulo

E ISTO PRECISA SER DITO ANTES DE QUALQUER LEITURA: das 4.195 views do canal,
2.419 vem de DEZ copias do mesmo video sobre o asgari ucret — cinco longos e
quatro shorts do titulo "Asgari ucret aclik sinirinin altinda", mais um. Sao
quarenta e quatro por cento do canal em UM assunto duplicado (aprendizado 545).
Ler a mediana do canal sem tirar isso e ler o proprio erro de publicacao como
se fosse audiencia.

O QUE SOBRA QUANDO SE TIRA A DUPLICATA — e e o achado desta rodada:

    "Tek Enflasyon Yok" ......... longo 42,04 views/dia | short 8,52
    "Kira Artisi Agustos 2026" .. longo 23,31 views/dia | short 35,95

O melhor longo LIMPO do canal (42,04/dia) veio do short mais fraco dos dois
(8,52/dia). O maior short do canal (35,95/dia) produziu um longo pior. E a
quinta replicacao do aprendizado 543, agora em turco: alcance de short nao
prediz alcance de longo.

O QUE OS DOIS TEM EM COMUM, e e a forma que esta pauta copia: os dois pedem
que o espectador olhe UM PAPEL QUE ELE JA TEM — a cesta dele contra a media da
inflacao, o contrato de aluguel dele contra o teto. Nao e "o que o governo
anunciou". E "o que o SEU papel diz".

Os dois longos com ZERO view do canal sao os dois que falam do numero de
OUTRA pessoa: o aumento do aposentado e o extrato de quem paga o minimo.

O QUE MUDO POR CAUSA DISSO:
1. **A PAUTA** e o holerite do proprio espectador. A conta que ele faz e:
   `brut x 0,85` da o matrah mensal dele; `190.000 / matrah` da o MES em que
   o desconto sobe de 15% para 20% e o liquido dele cai. Ele termina o video
   sabendo o nome de um mes.
2. **A RESPOSTA FECHA CEDO.** A conta inteira e entregue no capitulo 2, por
   volta dos 125 s estimados — nao no fim. Os capitulos 3 a 9 sao o que ela
   significa, nao o suspense dela.
3. **O SHORT** entrega a conta fechada E pede a inscricao, nao o clique no
   longo (experimento 26, aberto em 01/09/2026 com base fixada).
4. **O TITULO DO SHORT E PROPRIO** — este e o primeiro pacote depois do
   conserto do `short_titulo` (aprendizado 548). Ate ontem todo short da frota
   subia com os 60-70 caracteres do titulo do longo.

DIMENSIONAMENTO: veredito `liberado` = faixa de 12 a 15 min, e a rotina manda
o CHAO da faixa. Alvo ~764 s de estimativa (12min44s), 9 capitulos. Os tres
primeiros capitulos sao curtos (66-70 s) para a conta fechar cedo; os seis
seguintes sao longos (~93 s). Nenhum capitulo abaixo de 64 s na estimativa —
abaixo disso o `copy_md` engole o capitulo seguinte (aconteceu no
labtreinamento-007).

AS FONTES, e o que foi descartado:

  * Tarifa 2026 (190.000 / 400.000 / 1.500.000 e %15 / %20 / %27):
    GIB, "Gelir Vergisi Tarifesi 2026", cdn.gib.gov.tr, baixado e lido nesta
    rodada. O instrumento legal e o Gelir Vergisi Genel Tebligi Seri No: 332,
    RG 31/12/2025 sayi 33124 (5. mukerrer) — **nao consegui abrir o
    resmigazete.gov.tr** (timeout em todas as tentativas), entao a segunda
    fonte oficial da tarifa NAO existe nesta rodada. Isso vai escrito no
    AVISO SOBRE OS NUMEROS do video.
  * DESCARTADO: a aliquota de topo. Varias publicacoes profissionais dizem
    "%39"; a folha da propria GIB diz **% 40**. Numero que nao bate nao entra:
    a faixa de topo esta FORA do video inteiro, e o descarte esta no AVISO.
  * %14 + %1 de desconto do trabalhador, e o asgari ucret 33.030,00 bruto /
    28.075,50 liquido: CSGB, "asgari-ucret-2026.pdf", baixado e lido.
  * 33.030,00 CONFIRMADO EM SEGUNDA AUTORIDADE: SGK, genelge 2026/2,
    "Prime Esas Kazanc Miktarlari", sgk.gov.tr.
  * Tavan de 297.270,00 TL/mes: SGK, mesma pagina.

O que o video NAO afirma: nao diz quanto imposto voce paga (isso depende da
isencao do asgari ucret, de BES e de sindicato); diz em que MES a sua aliquota
marginal sobe. Sao perguntas diferentes e o roteiro separa as duas.
"""

# ---------------------------------------------------------------- capitulo 1
C1 = [
    {"layout": "titulo", "kicker": "Maaşın değişmedi",
     "sub": "ama elin daha az para geçti",
     "cap": "Aynı maaş, azalan net",
     "nar": "Zam almadın. Görevin değişmedi. Ama bu ay hesabına geçen para, "
            "geçen ayınkinden daha az. Bordroda bir hata yok."},
    {"layout": "item", "kicker": "Bu bir hata değil", "preco": "bu takvim",
     "sem_cap": True,
     "nar": "Bu bir kesinti hatası değil. Yılın kaçıncı ayında olduğunla "
            "ilgili bir şey."},
    {"layout": "item", "kicker": "Gelir vergisi aylık değil", "preco": "yıllık",
     "sem_cap": True,
     "nar": "Çünkü gelir vergisi senin o ayki maaşına bakmaz. Yılbaşından o "
            "aya kadar biriken toplamına bakar."},
    {"layout": "item", "kicker": "Biriken toplam", "preco": "kümülatif matrah",
     "sem_cap": True,
     "nar": "Bordroda bunun bir adı var: kümülatif vergi matrahı. Her ay "
            "üstüne eklenir, hiç sıfırlanmaz."},
    {"layout": "item", "kicker": "Ve bir yerde", "preco": "eşiği geçer",
     "sem_cap": True,
     "nar": "O toplam yılın bir yerinde bir eşiği geçer. Geçtiği ay, "
            "kesilen oran yükselir ve senin elinde kalan düşer."},
    {"layout": "item", "kicker": "Herkes için aynı ay değil", "preco": "seninki sana özel",
     "sem_cap": True,
     "nar": "Bu ay herkes için aynı değil. Maaşın ne kadarsa, eşiğe o kadar "
            "erken ya da geç varırsın."},
    {"layout": "item", "kicker": "Bu videonun sonunda", "preco": "bir ayın adı",
     "sem_cap": True,
     "nar": "Bu videonun sonunda kendi maaşın için o ayın adını biliyor "
            "olacaksın. İki işlem, ikisi de kendi bordronla."},
]

# ---------------------------------------------------------------- capitulo 2
C2 = [
    {"layout": "titulo", "kicker": "Bordrondaki tek satır",
     "sub": "cevabı veren yer",
     "cap": "İki işlem, kendi bordronla",
     "nar": "Şimdi hesabı yapıyoruz. Elinde tek bir sayı olması yeter: "
            "brüt maaşın."},
    {"layout": "item", "kicker": "Brütten önce ne çıkar", "preco": "yüzde 15",
     "sem_cap": True,
     "nar": "Brütünden önce sosyal güvenlik kesintileri çıkar. Sigorta primi "
            "yüzde on dört, işsizlik sigortası yüzde bir."},
    {"layout": "item", "kicker": "Yüzde 14 artı yüzde 1", "preco": "toplam yüzde 15",
     "sem_cap": True,
     "nar": "Toplamı yüzde on beş. Geriye kalan yüzde seksen beş, verginin "
            "hesaplandığı tutardır. Matrah budur."},
    {"layout": "item", "kicker": "Birinci işlem", "preco": "brüt × 0,85",
     "sem_cap": True,
     "nar": "Birinci işlem: brüt maaşını sıfır virgül seksen beş ile çarp. "
            "Çıkan sayı senin aylık matrahın."},
    {"layout": "item", "kicker": "Birinci eşik", "preco": "190.000 TL",
     "sem_cap": True,
     "nar": "İki bin yirmi altı tarifesinde ilk eşik yüz doksan bin lira. "
            "Bu eşiğe kadar oran yüzde on beş, sonrasında yüzde yirmi."},
    {"layout": "item", "kicker": "İkinci işlem", "preco": "190.000 ÷ matrah",
     "sem_cap": True,
     "nar": "İkinci işlem: yüz doksan bini az önce bulduğun aylık matraha "
            "böl. Çıkan sayıyı yukarı yuvarla."},
    {"layout": "item", "kicker": "Çıkan sayı", "preco": "senin ayın",
     "sem_cap": True,
     "nar": "O sayı, oranının yüzde yirmiye çıktığı aydır. Hesap bu kadar. "
            "Videonun geri kalanı bu sayının ne anlama geldiği."},
]

# ---------------------------------------------------------------- capitulo 3
C3 = [
    {"layout": "titulo", "kicker": "Üç maaş", "sub": "üç farklı ay",
     "cap": "Üç maaş, üç farklı ay",
     "nar": "Hesabı üç maaşla birlikte yapalım, kendi sayını nereye "
            "koyacağını görürsün."},
    {"layout": "item", "kicker": "Brüt 50.000 TL", "preco": "matrah 42.500",
     "sem_cap": True,
     "nar": "Brütü elli bin lira olan biri. Elli bin çarpı sıfır virgül "
            "seksen beş, kırk iki bin beş yüz lira matrah."},
    {"layout": "item", "kicker": "190.000 ÷ 42.500", "preco": "4,47 → 5. ay",
     "sem_cap": True,
     "nar": "Yüz doksan bin bölü kırk iki bin beş yüz, dört virgül beş. "
            "Yani beşinci ayda, mayısta eşiği geçiyor."},
    {"layout": "item", "kicker": "Brüt 75.000 TL", "preco": "matrah 63.750",
     "sem_cap": True,
     "nar": "Brütü yetmiş beş bin lira olan biri. Matrahı altmış üç bin "
            "yedi yüz elli lira."},
    {"layout": "item", "kicker": "190.000 ÷ 63.750", "preco": "2,98 → 3. ay",
     "sem_cap": True,
     "nar": "Yüz doksan bin bölü altmış üç bin yedi yüz elli, iki virgül "
            "dokuz. Üçüncü ayda, martta."},
    {"layout": "item", "kicker": "Brüt 150.000 TL", "preco": "matrah 127.500",
     "sem_cap": True,
     "nar": "Brütü yüz elli bin lira olan biri. Matrahı yüz yirmi yedi bin "
            "beş yüz lira."},
    {"layout": "item", "kicker": "190.000 ÷ 127.500", "preco": "1,49 → 2. ay",
     "sem_cap": True,
     "nar": "Bir virgül beş. Şubatta. Yılın ikinci ayında zaten üst "
            "dilimde."},
    {"layout": "item", "kicker": "Aynı tarife", "preco": "üç ayrı takvim",
     "sem_cap": True,
     "nar": "Aynı tarife, aynı ülke, üç ayrı takvim. Şimdi kendi sayını "
            "koy ve kendi ayını bul."},
]

# ---------------------------------------------------------------- capitulo 4
C4 = [
    {"layout": "titulo", "kicker": "2026 tarifesi", "sub": "üç eşik, üç oran",
     "cap": "2026 tarifesi: eşikler ve oranlar",
     "nar": "Şimdi tarifenin kendisine bakalım. İki bin yirmi altı yılı "
            "gelirlerine uygulanan tarife, Gelir İdaresi Başkanlığının kendi "
            "yayınladığı tabloda şöyle."},
    {"layout": "item", "kicker": "İlk dilim", "preco": "190.000 TL'ye kadar %15",
     "sem_cap": True,
     "nar": "Yüz doksan bin liraya kadar olan kısım yüzde on beş."},
    {"layout": "item", "kicker": "İkinci dilim", "preco": "400.000 TL'ye kadar %20",
     "sem_cap": True,
     "nar": "Yüz doksan bini geçtikten sonra oran yüzde yirmi. Tarifede bu "
            "dilim dört yüz bin liraya kadar sürer."},
    {"layout": "item", "kicker": "Üçüncü dilim", "preco": "ücrette 1.500.000 TL'ye kadar %27",
     "sem_cap": True,
     "nar": "Dört yüz bini de geçersen oran yüzde yirmi yediye çıkar. Ücret "
            "gelirlerinde bu dilim bir milyon beş yüz bine kadar sürer."},
    {"layout": "item", "kicker": "Dikkat", "preco": "sadece FAZLASI",
     "sem_cap": True,
     "nar": "Buradaki en önemli kelime fazlası. Eşiği geçince tüm maaşın "
            "yeni orana geçmez, sadece eşiği aşan kısım geçer."},
    {"layout": "item", "kicker": "Yanlış korku", "preco": "\"tamamı %20 olacak\"",
     "sem_cap": True,
     "nar": "Çok duyulan korku şu: dilim atlayınca maaşımın tamamından yüzde "
            "yirmi kesilir. Öyle değil. İlk yüz doksan bin lira yıl boyunca "
            "yüzde on beşte kalır."},
    {"layout": "item", "kicker": "Ücretli için ayrıcalık", "preco": "üçüncü dilim daha geniş",
     "sem_cap": True,
     "nar": "Bir ayrıntı daha: üçüncü dilim ücret geliri elde edenlerde bir "
            "milyon beş yüz bine kadar. Ücret dışı gelirlerde bir milyonda "
            "biter."},
    {"layout": "item", "kicker": "Yani maaşlı", "preco": "%27'de daha uzun kalır",
     "sem_cap": True,
     "nar": "Yani maaşlı çalışan, yüzde yirmi yedilik dilimde serbest "
            "çalışandan beş yüz bin lira daha uzun kalır."},
    {"layout": "item", "kicker": "Bu videoda", "preco": "üç dilim yeter",
     "sem_cap": True,
     "nar": "Üstünde iki dilim daha var ama onlara hiç girmiyorum. Sebebini "
            "açıklamaya yazdım."},
]

# ---------------------------------------------------------------- capitulo 5
C5 = [
    {"layout": "titulo", "kicker": "Peki ne kadar düşüyor",
     "sub": "beş puanın karşılığı",
     "cap": "Ne kadar düşüyor: beş puanın karşılığı",
     "nar": "Ay geldi, eşiği geçtin. Elindeki para tam olarak ne kadar "
            "azalıyor? Bunun da bir işlemi var."},
    {"layout": "item", "kicker": "Yüzde 15'ten yüzde 20'ye", "preco": "5 puan fark",
     "sem_cap": True,
     "nar": "Oran yüzde on beşten yüzde yirmiye çıkıyor. Aradaki fark beş "
            "puan."},
    {"layout": "item", "kicker": "Tam ay için", "preco": "matrah × 0,05",
     "sem_cap": True,
     "nar": "Tamamen üst dilimde geçen bir ay için kaybın, aylık matrahının "
            "beş yüzde biridir. Yani matrahını sıfır virgül sıfır beş ile "
            "çarp."},
    {"layout": "item", "kicker": "Brüt 50.000 olan", "preco": "ayda 2.125 TL az",
     "sem_cap": True,
     "nar": "Brütü elli bin olanın matrahı kırk iki bin beş yüzdü. Bunun "
            "yüzde beşi iki bin yüz yirmi beş lira. Her ay."},
    {"layout": "item", "kicker": "Brüt 75.000 olan", "preco": "ayda 3.187 TL az",
     "sem_cap": True,
     "nar": "Brütü yetmiş beş bin olan için üç bin yüz seksen yedi lira. "
            "Yine her ay, yıl sonuna kadar."},
    {"layout": "item", "kicker": "Brüt 150.000 olan", "preco": "ayda 6.375 TL az",
     "sem_cap": True,
     "nar": "Brütü yüz elli bin olan için altı bin üç yüz yetmiş beş lira. "
            "Ve o kişi bunu şubattan itibaren yaşıyor."},
    {"layout": "item", "kicker": "Geçiş ayı", "preco": "yarım düşer",
     "sem_cap": True,
     "nar": "Eşiği tam ortasında geçtiğin ayda düşüş daha küçüktür, çünkü o "
            "ayın matrahının sadece bir kısmı yeni dilime girer."},
    {"layout": "item", "kicker": "Ve ocakta", "preco": "her şey sıfırlanır",
     "sem_cap": True,
     "nar": "Ocak geldiğinde kümülatif matrah sıfırlanır ve oran yeniden "
            "yüzde on beşten başlar. Ocak maaşının neden yüksek geldiğinin "
            "cevabı budur."},
    {"layout": "item", "kicker": "Ocak yüksek değil", "preco": "aralık düşüktü",
     "sem_cap": True,
     "nar": "Yani ocakta zam almadın. Aralıkta üst dilimdeydin, ocakta alt "
            "dilime döndün. Aynı maaş, iki farklı kesinti."},
]

# ---------------------------------------------------------------- capitulo 6
C6 = [
    {"layout": "titulo", "kicker": "Asgari ücret istisnası",
     "sub": "neden herkes aynı anda hissetmiyor",
     "cap": "Asgari ücret istisnası",
     "nar": "Bir soru kalıyor: asgari ücretle çalışan biri bu düşüşü neden "
            "yaşamıyor? Cevabı, bordroda gizli olan bir istisnada."},
    {"layout": "item", "kicker": "2026 asgari ücret", "preco": "brüt 33.030,00 TL",
     "sem_cap": True,
     "nar": "İki bin yirmi altı asgari ücreti brüt otuz üç bin otuz lira. "
            "Bu rakam Çalışma ve Sosyal Güvenlik Bakanlığının kendi "
            "tablosunda yazıyor."},
    {"layout": "item", "kicker": "Kesintiler", "preco": "4.954,50 TL",
     "sem_cap": True,
     "nar": "Aynı tabloda kesintiler ayrı ayrı yazıyor. Sigorta primi dört "
            "bin altı yüz yirmi dört lira yirmi kuruş. İşsizlik sigortası üç "
            "yüz otuz lira otuz kuruş."},
    {"layout": "item", "kicker": "Net asgari ücret", "preco": "28.075,50 TL",
     "sem_cap": True,
     "nar": "Toplam dört bin dokuz yüz elli dört lira elli kuruş. Net "
            "asgari ücret yirmi sekiz bin yetmiş beş lira elli kuruş."},
    {"layout": "item", "kicker": "O tabloda olmayan satır", "preco": "gelir vergisi",
     "sem_cap": True,
     "nar": "Şimdi o tabloya dikkatli bak: gelir vergisi satırı yok. "
            "Asgari ücretten gelir vergisi kesilmiyor."},
    {"layout": "item", "kicker": "Sebebi", "preco": "asgari ücret istisnası",
     "sem_cap": True,
     "nar": "Sebebi asgari ücret istisnası. Herkesin maaşının asgari ücret "
            "kadar olan kısmına düşen vergi, o kişinin vergisinden düşülüyor."},
    {"layout": "item", "kicker": "Herkes", "preco": "sadece asgari ücretli değil",
     "sem_cap": True,
     "nar": "Ve bu istisna sadece asgari ücretliye değil, her maaşlıya "
            "uygulanıyor. Brütü iki yüz bin lira olan da bu indirimi alıyor."},
    {"layout": "item", "kicker": "Ama istisna sabit", "preco": "eşik değil",
     "sem_cap": True,
     "nar": "Ama istisna sabit bir tutar. Senin dilim atlaman onu "
            "büyütmüyor. Yani eşiği geçtiğinde düşüşü tamamen hissedersin."},
    {"layout": "item", "kicker": "Bu yüzden", "preco": "ofiste iki farklı hikâye",
     "sem_cap": True,
     "nar": "Aynı ofiste iki kişi. Biri temmuzda maaşının düştüğünü söylüyor, "
            "diğeri hiçbir şey fark etmiyor. İkisi de doğru söylüyor."},
]

# ---------------------------------------------------------------- capitulo 7
C7 = [
    {"layout": "titulo", "kicker": "İkinci eşik", "sub": "400.000 ve yüzde 27",
     "cap": "İkinci eşik: 400.000 ve yüzde 27",
     "nar": "Bazıları için yılda bir değil, iki düşüş var. İkinci eşik dört "
            "yüz bin lira."},
    {"layout": "item", "kicker": "Aynı işlem", "preco": "400.000 ÷ matrah",
     "sem_cap": True,
     "nar": "Hesap birebir aynı: dört yüz bini aylık matrahına böl, yukarı "
            "yuvarla. O ay oranın yüzde yirmi yediye çıkar."},
    {"layout": "item", "kicker": "Brüt 75.000 olan", "preco": "400.000 ÷ 63.750 = 6,27",
     "sem_cap": True,
     "nar": "Brütü yetmiş beş bin olanın matrahı altmış üç bin yedi yüz "
            "elliydi. Dört yüz bini buna böl: altı virgül üç. Yedinci ayda, "
            "temmuzda."},
    {"layout": "item", "kicker": "Aynı kişi için", "preco": "mart ve temmuz",
     "sem_cap": True,
     "nar": "Yani aynı kişi martta bir düşüş, temmuzda ikinci bir düşüş "
            "yaşıyor. Yılda iki kez, ikisi de zam olmadan."},
    {"layout": "item", "kicker": "İkinci düşüş daha sert", "preco": "7 puan",
     "sem_cap": True,
     "nar": "Ve ikincisi daha sert: yüzde yirmiden yüzde yirmi yediye, yedi "
            "puan. Beş değil."},
    {"layout": "item", "kicker": "Brüt 75.000 için", "preco": "ayda 4.462 TL",
     "sem_cap": True,
     "nar": "Matrahının yüzde yedisi. Altmış üç bin yedi yüz elli için bu, "
            "dört bin dört yüz altmış iki lira. Temmuzdan aralığa kadar her "
            "ay."},
    {"layout": "item", "kicker": "Not", "preco": "prim ve ikramiye de sayılır",
     "sem_cap": True,
     "nar": "Bir uyarı: prim, ikramiye ve fazla mesai de matraha girer. "
            "Büyük bir prim aldığın ay, eşiği beklediğinden bir ay önce "
            "geçebilirsin."},
    {"layout": "item", "kicker": "Bu yüzden", "preco": "hesabı prim ayından sonra yenile",
     "sem_cap": True,
     "nar": "Bu yüzden hesabı yılda bir kez değil, büyük bir ödeme aldığın "
            "her seferden sonra yenile."},
    {"layout": "item", "kicker": "Ve bordroda", "preco": "kümülatif satırı doğrular",
     "sem_cap": True,
     "nar": "Zaten bordronun kümülatif matrah satırı sana gerçek toplamı "
            "söyler. Tahminin ile o satır uyuşmuyorsa, doğru olan o satırdır."},
]

# ---------------------------------------------------------------- capitulo 8
C8 = [
    {"layout": "titulo", "kicker": "Bir sınır daha", "sub": "SGK tavanı",
     "cap": "SGK tavanı: 0,85 kuralının bittiği yer",
     "nar": "Anlattığım sıfır virgül seksen beş kuralının bir sınırı var, ve "
            "yüksek maaşlarda bu kural bozulur."},
    {"layout": "item", "kicker": "Prime esas kazanç", "preco": "aylık tavan 297.270,00 TL",
     "sem_cap": True,
     "nar": "Sosyal Güvenlik Kurumunun iki bin yirmi altı genelgesinde aylık "
            "prime esas kazanç üst sınırı iki yüz doksan yedi bin iki yüz "
            "yetmiş lira."},
    {"layout": "item", "kicker": "Alt sınır", "preco": "aylık 33.030,00 TL",
     "sem_cap": True,
     "nar": "Aynı genelgede alt sınır otuz üç bin otuz lira. Yani tavan, "
            "asgari ücretin tam dokuz katı."},
    {"layout": "item", "kicker": "Tavanın üstünde", "preco": "prim artmaz",
     "sem_cap": True,
     "nar": "Brütün bu tavanı aşarsa, aşan kısımdan sigorta primi kesilmez. "
            "Prim tavanda durur."},
    {"layout": "item", "kicker": "Sonuç", "preco": "matrah 0,85'ten büyük olur",
     "sem_cap": True,
     "nar": "Sonuç şu: tavanın üstündeki maaşlarda matrahın brütünün yüzde "
            "seksen beşinden daha büyük olur, çünkü kesinti sabitlenir."},
    {"layout": "item", "kicker": "Yani", "preco": "eşiğe daha da erken varırsın",
     "sem_cap": True,
     "nar": "Yani tavanın üstündeysen, benim verdiğim işlem seni eşiğe "
            "olduğundan geç götürür. Gerçek ayın daha erkendir."},
    {"layout": "item", "kicker": "Kimi ilgilendirir", "preco": "brüt 297.270 üstü",
     "sem_cap": True,
     "nar": "Bu, brütü iki yüz doksan yedi bin liranın üstünde olanları "
            "ilgilendirir. Maaşlıların çok küçük bir kısmı."},
    {"layout": "item", "kicker": "O grup için", "preco": "bordro satırı şart",
     "sem_cap": True,
     "nar": "O gruptaysan çarpma işlemini bırak ve doğrudan bordrondaki "
            "kümülatif matrah satırını oku. Tahmin etme, oku."},
    {"layout": "item", "kicker": "Tavanın altındaysan", "preco": "0,85 doğrudur",
     "sem_cap": True,
     "nar": "Tavanın altındaysan, ki büyük ihtimalle öylesin, sıfır virgül "
            "seksen beş kuralı senin için doğrudur."},
    {"layout": "item", "kicker": "Bir de", "preco": "BES ve sendika",
     "sem_cap": True,
     "nar": "Bordronda bireysel emeklilik ya da sendika aidatı gibi başka "
            "kesintiler varsa, matrahın biraz daha küçüktür ve eşiğe biraz "
            "daha geç varırsın."},
]

# ---------------------------------------------------------------- capitulo 9
C9 = [
    {"layout": "titulo", "kicker": "Şimdi kendi bordronla",
     "sub": "üç adım", "cap": "Kendi bordronla üç adım",
     "nar": "Şimdi videoyu durdurmadan önce hesabı kendi kâğıdınla yapalım. "
            "Üç adım."},
    {"layout": "item", "kicker": "Adım 1", "preco": "brüt × 0,85",
     "sem_cap": True,
     "nar": "Birinci adım: bordrondaki brüt maaşı sıfır virgül seksen beş "
            "ile çarp. Aylık matrahın bu."},
    {"layout": "item", "kicker": "Adım 2", "preco": "190.000 ÷ matrah",
     "sem_cap": True,
     "nar": "İkinci adım: yüz doksan bini bu sayıya böl ve yukarı yuvarla. "
            "Oranının yüzde yirmiye çıktığı ay bu."},
    {"layout": "item", "kicker": "Adım 3", "preco": "matrah × 0,05",
     "sem_cap": True,
     "nar": "Üçüncü adım: matrahını sıfır virgül sıfır beş ile çarp. O aydan "
            "sonra elinde her ay bu kadar az para kalacak."},
    {"layout": "lista", "kicker": "Üç adım", "sem_cap": True,
     "itens": ["brüt × 0,85 = aylık matrah",
               "190.000 ÷ matrah = geçiş ayı",
               "matrah × 0,05 = aylık kayıp"],
     "nar": "Üçü bir arada: çarp, böl, çarp. Kâğıt kalem yeter."},
    {"layout": "item", "kicker": "Doğrulaman gereken tek yer", "preco": "bordronun kümülatif satırı",
     "sem_cap": True,
     "nar": "Sonucu doğrulamak istersen bordronun kümülatif vergi matrahı "
            "satırına bak. Tahminin ile o satır aynı yöne gitmeli."},
    {"layout": "item", "kicker": "Bunu bilmek", "preco": "kesintiyi durdurmaz",
     "sem_cap": True,
     "nar": "Bunu bilmek kesintiyi durdurmaz. Ama o ayı önceden bilirsen, "
            "kira zammını ya da taksitli alışverişi hangi aya "
            "koymayacağını da bilirsin."},
    {"layout": "item", "kicker": "Sayılar nereden geldi", "preco": "açıklamada yazılı",
     "sem_cap": True,
     "nar": "Her sayının hangi resmî belgeden geldiğini açıklamaya tek tek "
            "yazdım. Bir tanesini de çelişkili olduğu için çıkardım, onu da "
            "yazdım."},
    {"layout": "cta", "kicker": "Kendi ayını buldun mu",
     "sub": "yorumlara yaz", "sem_cap": True,
     "nar": "Kendi ayını bulduysan yorumlara sadece ayın adını yaz. Bu "
            "kanalda her video böyle bir hesapla bitiyor; işine yaradıysa "
            "abone ol, bir sonraki hesapta görüşürüz."},
]

CENAS = C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8 + C9

# ---------------------------------------------------------------------- short
#
# EXPERIMENTO 26: o pedido unico do short e a INSCRICAO, nao o clique no longo.
# O short entrega a conta FECHADA — quem assiste ja sabe calcular o proprio mes
# antes do fim dos quarenta segundos.
SHORT = [
    {"layout": "titulo", "kicker": "Maaşın hangi ay düşecek?",
     "sub": "iki işlem, kendi bordronla", "sem_cap": True,
     "nar": "Zam almadan maaşının düştüğü bir ay var. Hangi ay olduğunu iki "
            "işlemle bul."},
    {"layout": "titulo", "kicker": "1) brüt × 0,85", "sub": "aylık matrahın",
     "sem_cap": True,
     "nar": "Brütünü sıfır virgül seksen beş ile çarp. Kalan senin "
            "matrahın."},
    {"layout": "titulo", "kicker": "2) 190.000 ÷ matrah", "sub": "geçiş ayın",
     "sem_cap": True,
     "nar": "Yüz doksan bini o sayıya böl, yukarı yuvarla. Oranının yüzde "
            "yirmiye çıktığı ay bu."},
    {"layout": "titulo", "kicker": "Brüt 75.000 ise", "sub": "mart",
     "sem_cap": True,
     "nar": "Brütü yetmiş beş bin olanın matrahı altmış üç bin yedi yüz "
            "elli. Bölüm iki virgül dokuz: mart."},
    {"layout": "cta", "kicker": "Her video böyle bir hesap",
     "sub": "abone ol", "sem_cap": True,
     "nar": "Bu kanalda her video kendi kâğıdınla bitiyor. İşine yaradıysa "
            "abone ol."},
]

THUMB = {"l1": "Maaşın hangi ay", "l2": "düşecek?"}

COPY = """# Vergi dilimi: maasin hangi ay dustugunu iki islemle bulmak

## BAŞLIK
Vergi Dilimi 2026: Maaşın Hangi Ay Düşecek? Brütünü 0,85 ile Çarp ve Kendin Bul

## SHORT BAŞLIK
Maaşın hangi ay düşecek? İki işlemle bul

## AÇIKLAMA
Zam almadın, görevin değişmedi, ama yılın bir ayında hesabına geçen para azaldı. Bu bir bordro hatası değil. Gelir vergisi senin o ayki maaşına değil, yılbaşından o aya kadar biriken toplamına bakar; bordroda bunun adı kümülatif vergi matrahıdır ve hiç sıfırlanmaz. O toplam bir eşiği geçtiğinde kesilen oran yükselir ve elinde kalan düşer.

Bu videoda o ayı kendi bordronla bulmayı anlatıyorum, ve hesap iki işlemden ibaret. Birincisi: brüt maaşını 0,85 ile çarp. Sigorta primi yüzde 14, işsizlik sigortası yüzde 1; kalan yüzde 85 senin aylık matrahın. İkincisi: 2026 tarifesinin ilk eşiği olan 190.000 lirayı bu sayıya böl ve yukarı yuvarla. Çıkan sayı, oranının yüzde 15'ten yüzde 20'ye çıktığı aydır.

Üç örnekle birlikte yapıyoruz. Brütü 50.000 olan için matrah 42.500 ve geçiş beşinci ayda; brütü 75.000 olan için matrah 63.750 ve geçiş üçüncü ayda; brütü 150.000 olan için matrah 127.500 ve geçiş daha şubatta. Aynı tarife, aynı ülke, üç ayrı takvim.

Sonra düşüşün büyüklüğünü hesaplıyoruz: tam olarak üst dilimde geçen bir ay için kaybın matrahının yüzde 5'i kadardır, çünkü aradaki fark beş puandır. Eşiği geçince maaşının tamamı yüzde 20'ye geçmez — tarifede yazan kelime "fazlası"dır, yani sadece eşiği aşan kısım yeni orana girer. İlk 190.000 lira yıl boyunca yüzde 15'te kalır.

Videoda ayrıca şunlar var: asgari ücret istisnasının neden bazı çalışanların bu düşüşü hiç hissetmemesine yol açtığı; 400.000 liralık ikinci eşik ve yüzde 27'ye geçiş, ki o düşüş beş değil yedi puandır; prim ve ikramiyenin matraha girmesi yüzünden eşiğin beklenenden bir ay önce geçilebilmesi; ve SGK'nın aylık 297.270 liralık prim tavanının üstünde 0,85 kuralının neden bozulduğu.

Videonun sonunda üç adım var: çarp, böl, çarp. Kâğıt kalem yeter. Kendi ayını bulduysan yorumlara sadece ayın adını yaz.

## BÖLÜMLER
{CAPITULOS}

## SABİTLENEN YORUM
İki işlem, tek kâğıt: (1) brüt × 0,85 = aylık matrahın. (2) 190.000 ÷ matrah, yukarı yuvarla = oranının yüzde 20'ye çıktığı ay. (3) matrah × 0,05 = o aydan sonra her ay eksik alacağın tutar. Kendi ayını yorumlara yaz — hangi ay çıktı?

## HASHTAGLER
#VergiDilimi #Bordro #SeviyeSeviye

## ETİKETLER
vergi dilimi 2026, gelir vergisi 2026, kümülatif vergi matrahı, bordro hesaplama, maaş neden düştü, net maaş hesaplama, gelir vergisi tarifesi, asgari ücret istisnası, SGK tavanı 2026, vergi dilimi hesaplama, maaşlı çalışan vergi, brüt net maaş, 190.000 vergi eşiği, kişisel finans, para yönetimi

## STUDIO AYARLARI
Kategori: Eğitim. Dil: Türkçe. Çocuklara yönelik değil. Sentetik medya içerir.

## MÜZİK / LİSANS
{TRILHA}

## SAYILAR HAKKINDA UYARI
Tarife (190.000 / 400.000 / ücret gelirlerinde 1.500.000 ve %15 / %20 / %27): Gelir İdaresi Başkanlığı'nın kendi yayımladığı "Gelir Vergisi Tarifesi 2026" belgesinden alındı. Bu tarifenin yasal dayanağı 332 Seri No'lu Gelir Vergisi Genel Tebliği'dir (Resmî Gazete, 31/12/2025, sayı 33124, 5. mükerrer). Bu videoyu hazırlarken Resmî Gazete'nin sitesine erişemedim, bu yüzden tarife rakamlarını İKİNCİ bir resmî kaynaktan doğrulayamadım; tek resmî kaynağım GİB'in kendi belgesidir. Bunu bilerek yazıyorum.

VİDEODAN ÇIKARDIĞIM SAYI: tarifenin en üst dilimindeki oran. Birçok mesleki yayın bu oranı %39 olarak veriyor; GİB'in kendi tablosunda %40 yazıyor. İki kaynak uyuşmadığı için en üst dilimi videoya hiç koymadım. Bu videoda sadece ilk üç dilim var.

Yüzde 14 sigorta primi ve yüzde 1 işsizlik sigortası kesintileri ile 2026 asgari ücreti (brüt 33.030,00 TL, kesinti 4.954,50 TL, net 28.075,50 TL): Çalışma ve Sosyal Güvenlik Bakanlığı'nın "Asgari Ücretin Net Hesabı ve İşverene Maliyeti" tablosundan. Brüt 33.030,00 TL rakamı ayrıca SGK'nın 2026/2 sayılı genelgesinde de aynı şekilde yer alıyor — bu sayı iki ayrı resmî kurumda doğrulandı.

Aylık prime esas kazanç üst sınırı 297.270,00 TL ve alt sınırı 33.030,00 TL: SGK 2026/2 sayılı genelge, "Prime Esas Kazanç Miktarları", 1/1/2026 - 31/12/2026 dönemi, özel sektör.

BU VİDEONUN İDDİA ETMEDİĞİ ŞEY: ne kadar vergi ödeyeceğin. O rakam asgari ücret istisnasına, varsa bireysel emeklilik ve sendika aidatı gibi kesintilere göre değişir. Bu video sadece marjinal oranının hangi AY yükseldiğini hesaplıyor. İkisi farklı sorulardır. Kesin rakam için bordronun kümülatif vergi matrahı satırına bak; tahmin ile o satır çelişirse doğru olan o satırdır.
"""



def _copy_existente():
    import json
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "seviye-seviye-009.json")
    if os.path.exists(p):
        c = json.load(open(p, encoding="utf-8")).get("copy")
        if c:
            return c
    return COPY


SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-009",
    "idioma": "tr",
    "voz": "tr-TR-AhmetNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#0F3538", "c1": "#E4572E", "c2": "#F2B134", "bg": "#EAF3F3"},
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
    grava(SPEC, "fabrica/specs/seviye-seviye-009.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
