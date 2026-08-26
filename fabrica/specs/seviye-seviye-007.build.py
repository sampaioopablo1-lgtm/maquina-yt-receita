#!/usr/bin/env python3
"""Monta a spec seviye-seviye-007.

ALAVANCA ATACADA: A (conversao short -> inscrito).

NUMERO DE PARTIDA, e este canal e o caso mais interessante da frota:

    cron-2026-08-17   short  291 views  1 insc  0,344%
    seviye-seviye-003 short  521 views  1 insc  0,192%
    seviye-seviye-004 short  734 views  1 insc  0,136%
    sv-asgari-ucret   short  720 views  0 insc  0,000%
    cron-2026-08-15   short  435 views  0 insc  0,000%
    seviye-seviye-005 short  337 views  0 insc  0,000%
    cron-2026-08-16   short  260 views  0 insc  0,000%

O QUE DEU CERTO: a DISTRIBUICAO. Este canal e o que mais recebe views por
short da frota inteira — mediana de 47,28 views/dia, topo de 132,82.

O QUE NAO DEU: a conversao. Nenhum pacote passa de 0,344%, contra 1,429% do
kolejny-poziom e 2,128% do nivel-do-jogo. Muito transito, pouca conversao.

E O PORQUE ESTAVA NOS TITULOS. Todos os sete falam de coisa que ACONTECE COM
o espectador e que ele nao decide: o salario minimo esta abaixo da linha da
fome, a aposentadoria minima e tanto, o reajuste comecou em julho, o teto do
aluguel e 31,90%. Nenhum e uma ESCOLHA que ele faca.

Isso refina o aprendizado 502. Nao basta ser sobre o dinheiro dele e ter data:
o `seviye-seviye-005` tinha as duas coisas — teto de aluguel de agosto de 2026,
o dinheiro dele, prazo — e converteu ZERO com 337 views. O que falta ali e
agencia: teto de aluguel e imposto, nao escolhido. Os que converteram em outros
canais eram escolhas de verdade: qual edicao comprar, trocar ou nao de seguro.

O QUE MUDEI: a pauta e uma escolha REAL, com prazo LEGAL e dinheiro do
espectador — o direito de sair do plano de aposentadoria automatica em dois
meses. Ele decide, tem prazo, e a conta e sobre o dinheiro dele.

VEREDITO `liberado` (12-15 min), e a alavanca B manda ir ao PISO: 12 min, dez
capitulos, resposta dentro dos duzentos primeiros segundos.

OS NUMEROS, e as duas rotas institucionais

  - Devlet katkisi de 30% sobre as contribuicoes (subiu de 25%).
  - Direito de cayma dentro de DOIS MESES da notificacao de inclusao, com
    devolucao do que foi pago em dez dias uteis.

    rota 1  EGM (Emeklilik Gozetim Merkezi), egm.org.tr — paginas "Devlet
            Katkisi", "OKS nedir" e "OKS-BES Karsilastirmasi"
    rota 2  o texto legal: Bireysel Emeklilik Tasarruf ve Yatirim Sistemi
            Kanunu (n. 4632) em mevzuat.gov.tr, o texto da lei de inclusao
            automatica no acervo da TBMM, e o comunicado da SEDDK sobre as
            novas vantagens do sistema

O QUE FICOU DE FORA, e o video diz em voz alta

  - O VALOR do bonus unico de entrada. Uma rota institucional diz quinhentas
    liras e a outra diz mil ("bin Turk lirasi"). Duas fontes oficiais, dois
    numeros para a mesma coisa: pela regra, nao entra. E nao precisa entrar —
    a decisao nao depende dele, e o video diz isso em vez de escolher um.
  - Qualquer projecao de rendimento do fundo. Depende do fundo escolhido e do
    prazo, e nenhum orgao publica garantia. O video ensina a comparar a parte
    CERTA (o trinta por cento) com o que o espectador abre mao, que e liquidez.

O eixo — uma escolha com prazo legal — nao existe em nenhum dos sete titulos
no ar do canal, que sao todos sobre numeros impostos de fora.
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


# --------------------------------------------- 1. Iki ay iceride bir karar
T("Bir kararın var", "ve süresi işliyor",
  "Şu anda senin adına işleyen bir süre var. Sonunda bir karar çıkacak, ve "
  "farkında olmasan bile o kararı sen vermiş sayılacaksın.",
  cap="Süresi işleyen bir karar")
T("Çoğu konu", "sana yapılan bir şeydir",
  "Bu kanalda çoğu zaman sana yapılan şeyleri konuşuyoruz. Asgari ücret şu "
  "kadar oldu, tavan şu kadar belirlendi, zam şu tarihte başladı.")
T("Bu sefer değil", "bu sefer sen seçiyorsun",
  "Bu sefer farklı. Burada seçen sensin, ve seçmemek de bir seçim, çünkü süre "
  "dolduğunda karar kendiliğinden verilmiş oluyor.")
I("Konu", "otomatik katılım",
  "Konu, işyerin üzerinden otomatik olarak dahil edildiğin emeklilik planı. "
  "Kısaca otomatik katılım.")
T("Karar vermemek de", "karar vermektir",
  "Bu cümleyi bir daha söyleyeceğim çünkü videonun tamamı ona dayanıyor: "
  "karar vermemek de karar vermektir, ve süre dolduğunda seçim yapılmış olur.")
T("Yüzde otuz mu", "yoksa nakit mi",
  "Kararın özü şu dengede: devletin eklediği kesin tutar ile, o paranın bir "
  "süre elinin altında olmaması arasında seçim yapıyorsun.")
T("Sonunda ne bileceksin", "kendi hesabını",
  "Videonun sonunda kendi durumun için hesabı yapabiliyor olacaksın. Benim "
  "ortalamamla değil, senin maaşın ve senin ihtiyacınla.")

# ------------------------------------------- 2. Devlet ne veriyor
T("Önce rakam", "çünkü karar ona bağlı",
  "Önce rakamla başlayalım, çünkü kararın tamamı bu rakamın etrafında dönüyor. "
  "Devlet bu sisteme bir katkı ödüyor.",
  cap="Devlet ne veriyor")
I("Devlet katkısı", "yüzde otuz",
  "Ödediğin katkı payının yüzde otuzu kadar bir tutar, devlet katkısı olarak "
  "senin hesabına ekleniyor.")
T("Bu oran", "yüzde yirmi beşten yükseldi",
  "Bu oran daha önce yüzde yirmi beşti. Kanunda yapılan değişiklikle yüzde "
  "otuza çıkarıldı.")
I("Pratikte", "her yüz liraya otuz lira",
  "Pratikte şu demek: sisteme yatırdığın her yüz lira için, hesabına otuz "
  "lira daha ekleniyor. Senin cebinden çıkmadan.")
T("Bu bir getiri değil", "bir eklemedir",
  "Dikkat et, bu bir yatırım getirisi değil. Piyasa ne yaparsa yapsın, bu "
  "ekleme yapılıyor. İkisini karıştırmamak kararın en önemli parçası.")
T("Karıştırırsan", "yanlış soruyu sorarsın",
  "Bu ikisini karıştıran kişi yanlış soruyu sorar. Fon ne kadar kazandırır "
  "diye sorar, oysa asıl soru paranın bağlanması sorusudur.")
I("Kesin olan", "ekleme; belirsiz olan, getiri",
  "Kesin olan ekleme, belirsiz olan getiri. Karar kesin olan tarafta "
  "verilir, çünkü belirsiz olanı kimse önceden bilemez.")
T("Getiri ayrı bir konu", "ve garantisi yok",
  "Fonun kazandırıp kazandırmayacağı bambaşka bir konudur ve hiçbir kurum "
  "onu garanti etmez. Burada sadece kesin olan kısmı konuşuyorum.")

# ------------------------------------------- 3. Cayma hakki
T("Şimdi süre", "iki ay",
  "Şimdi kararın süresine gelelim. Plana dahil edildiğin sana bildirildikten "
  "sonra iki ayın var.",
  cap="İki aylık cayma hakkı")
I("Bu süre içinde", "cayabilirsin",
  "Bu iki ay içinde sözleşmeden cayabilirsin. Yani sistemden çıkabilirsin, "
  "gerekçe göstermek zorunda kalmadan.")
I("Ödediklerin", "on iş günü içinde geri gelir",
  "Caydığında ödediğin katkı payları, varsa yatırım gelirleriyle birlikte, "
  "on iş günü içinde sana iade edilir.")
T("Yani ilk iki ay", "risksiz bir deneme değil",
  "Burada bir yanlış anlama var, düzeltelim. İki ay risksiz deneme süresi "
  "gibi duruyor ama tam olarak öyle değil.")
T("Çünkü caymak", "devlet katkısını da götürür",
  "Çünkü cayarsan devlet katkısı da gitmiş olur. Sana geri gelen, senin "
  "ödediğindir. Otuz liralık ekleme o hesapta kalmaz.")
T("Bir de tarih meselesi", "bildirim tarihi",
  "Bir ayrıntı daha var ve kritik: iki ay, sisteme girdiğin günden değil, "
  "durumun sana BİLDİRİLDİĞİ tarihten itibaren sayılıyor.")
T("Bu iki tarih", "aynı olmayabilir",
  "Bu iki tarih aynı olmayabilir, ve aradaki fark senin elinde ne kadar süre "
  "kaldığını değiştirir. İlerleyen bölümde nereden bakacağını göstereceğim.")
T("Karar bu yüzden", "iki taraflı",
  "Kararın tartısı böyle kuruluyor: kesin bir ekleme karşısında, paranın "
  "bağlanacağı süre.")

# ------------------------------------------- 4. Hesabi kendin yap
T("Hesabı yapalım", "senin rakamlarınla",
  "Şimdi hesabı yapalım, ve bunu maaş bordronla birlikte yapmanı öneririm. "
  "İki rakam yeterli.",
  cap="Hesabı kendin yap")
L("İki rakam", ["Aylık kesilen katkı payı",
                "Kaç ay sistemde kalmayı düşünüyorsun"],
  "Birincisi, bordroda otomatik katılım için aylık kesilen tutar. İkincisi, "
  "kaç ay sistemde kalmayı düşündüğün.")
I("Birinci işlem", "aylık tutarı ay sayısıyla çarp",
  "Aylık tutarı ay sayısıyla çarp. Bu, senin toplam ödeyeceğin para.")
I("İkinci işlem", "sonucu nokta üç ile çarp",
  "Sonucu nokta üç ile çarp. Çıkan sayı, devletin aynı süre boyunca senin "
  "hesabına eklediği tutar.")
T("İşte karşılaştırman gereken", "bu iki sayı",
  "Karşılaştırman gereken tam olarak bu iki sayı. Biri senin verdiğin, öbürü "
  "karşılığında eklenen.")
T("Bir örnekle netleşsin", "rakamları sen koy",
  "Örnekle netleşsin, ve rakamları sen koyacaksın. Diyelim aylık kesinti "
  "belli bir tutar ve on iki ay düşünüyorsun.")
T("Toplamı bul", "sonra nokta üç ile çarp",
  "Toplamı bulursun, nokta üç ile çarparsın, ve karşına iki sayı çıkar. "
  "Bu ikisi arasındaki fark, kararın somut hâlidir.")
T("Şimdi üçüncü soruyu sor", "kendine",
  "Ve şimdi kendine üçüncü soruyu sor: o parayı o süre boyunca elimde "
  "tutmasam ne olur? Cevap kişiye göre değişir, ve karar orada verilir.")

# ---------------------------------------- 5. Karsiliginda ne veriyorsun
T("Karşılığında", "ne veriyorsun",
  "Bir şey alıyorsan bir şey veriyorsundur. Burada verdiğin şey para değil, "
  "paranın zamanı.",
  cap="Karşılığında ne veriyorsun")
T("Bu para", "emeklilik için ayrılmıştır",
  "Sisteme giren para emeklilik için ayrılmış sayılır. Yani acil bir "
  "durumda hemen ulaşabileceğin bir hesapta durmaz.")
I("Erken çıkarsan", "koşullar değişir",
  "İki aylık süreden sonra çıkmak isterseniz, devlet katkısına ne kadar hak "
  "kazanacağınız sistemde kaldığınız süreye bağlıdır.")
T("Bu yüzden", "soru kârlılık sorusu değil",
  "Bu yüzden asıl soru şu değil: kârlı mı? Asıl soru şu: bu tutarı bu süre "
  "boyunca kenara koyabilir miyim?")
T("Cevap evet ise", "yüzde otuz güçlü bir eklemedir",
  "Cevabın evetse, yüzde otuzluk ekleme çok güçlüdür. Piyasada risksiz "
  "olarak bu oranı veren bir ürün yoktur.")
T("Likidite", "bir lüks değildir",
  "Likidite bir lüks değil, bir güvenlik payıdır. Hesabında ulaşılabilir "
  "para olması, beklenmedik bir masrafta borçlanmanı engeller.")
I("Borçlanmanın maliyeti", "eklemeden büyük olabilir",
  "Ve o borçlanmanın maliyeti, yüzde otuzluk eklemeden büyük olabilir. "
  "O yüzden sıralama önemlidir, birazdan ona geliyorum.")
T("Cevap hayır ise", "kimse seni suçlayamaz",
  "Cevabın hayırsa, bu bir hata değil. Ay sonunu zor getiren biri için "
  "likidite, uzun vadeli bir eklemeden daha değerlidir.")

# --------------------------------------- 6. Kimin icin mantikli
T("Kimin için mantıklı", "kimin için değil",
  "Genelleme yapmayacağım ama bir çerçeve vereyim. İki uçta durum oldukça "
  "net, ortada ise hesap gerekiyor.",
  cap="Kimin için mantıklı")
L("Sistemde kalmak öne çıkar", ["Maaşın düzenli ve öngörülebilirse",
                                "Bu tutar bütçeni zorlamıyorsa",
                                "Kısa vadede büyük harcaman yoksa"],
  "Maaşın düzenliyse, kesilen tutar bütçeni zorlamıyorsa ve yakın vadede "
  "büyük bir harcaman yoksa, sistemde kalmak öne çıkıyor.")
L("Caymak öne çıkar", ["Kredi kartı borcun devrediyorsa",
                       "Geliri düzensiz çalışıyorsan",
                       "Acil durum birikimin hiç yoksa"],
  "Devreden kredi kartı borcun varsa, gelirin düzensizse ya da hiç acil "
  "durum birikimin yoksa, caymak öne çıkıyor.")
T("Sıralama önemli", "önce borç, sonra yastık",
  "Sıralama şöyle: önce yüksek faizli borç, sonra acil durum birikimi, sonra "
  "uzun vadeli emeklilik. Bu sıra kişisel tercih değil, matematiktir.")
T("Ortadaysan", "hesap seni kurtarır",
  "İki uçtan hiçbirine tam uymuyorsan, genelleme sana yardımcı olmaz. "
  "Kendi rakamınla yaptığın hesap yardımcı olur.")
T("Ve bu hesap", "iki dakika sürüyor",
  "İyi haber şu: o hesap iki dakika sürüyor, ve bunun için bordrondan başka "
  "hiçbir belgeye ihtiyacın yok.")
I("Çünkü kart faizi", "yüzde otuzdan büyüktür",
  "Çünkü devreden kart borcunun yıllık maliyeti, yüzde otuzluk eklemeden "
  "büyük olabilir. O zaman önce onu kapatmak daha çok kazandırır.")

# ------------------------------------- 7. Soylemedigim rakam
T("Şimdi dürüst kısım", "söylemediğim rakam",
  "Şimdi videonun en dürüst kısmı. Size vermeyeceğim bir rakam var, ve "
  "nedenini açıkça söyleyeceğim.",
  cap="Söylemediğim rakam")
T("Girişte bir defalık", "ilave katkı var",
  "Sistemde kalmaya devam edenlere, girişte bir defaya mahsus ilave bir "
  "devlet katkısı ödeniyor.")
I("İki resmi kaynak", "iki farklı tutar",
  "Ama iki resmi kaynağa baktığımda iki farklı tutar gördüm. Biri beş yüz "
  "lira diyor, diğerinde bin lira geçiyor.")
T("Bu durumda kural açık", "rakam videoya girmez",
  "Böyle bir durumda kuralım net: iki resmi kaynak aynı sayıyı vermiyorsa, o "
  "sayı bu videoya girmez. Tahmin etmek size hizmet etmez.")
T("İyi haber şu", "karar ona bağlı değil",
  "İyi haber şu ki kararınız zaten o rakama bağlı değil. Karar, yüzde otuz "
  "ile likidite arasındaki dengede veriliyor, ve o kısım kesin.")
T("Neden bunu anlatıyorum", "çünkü ölçüsü var",
  "Bunu anlatıyorum çünkü bir videonun güvenilirliğinin ölçüsü, "
  "söylediklerinden çok söylemediklerinde saklıdır.")
T("Tahmin edilen rakam", "yanlış karara götürür",
  "Tahmin edilerek verilen bir rakam sizi yanlış bir karara götürebilir, ve "
  "o kararın bedelini ben değil siz ödersiniz.")
T("Kendi tutarını", "sözleşmenden gör",
  "Kendi durumundaki tutarı sözleşmenden ve şirketinin bilgilendirmesinden "
  "görebilirsin. Orası size özel, ve orada tahmin yok.")

# ---------------------------------------- 8. Kendi durumunu gor
T("Kendi durumunu", "kendin gör",
  "Bütün bu videonun en önemli adımı bu: kendi durumunu başkasından değil, "
  "kendi kaydından öğren.",
  cap="Kendi durumunu gör")
L("Üç yere bak", ["Maaş bordrondaki kesinti satırı",
                  "Şirketin gönderdiği bilgilendirme",
                  "Devlet katkısı sorgulama ekranı"],
  "Maaş bordrondaki kesinti satırına bak. Şirketinin sana gönderdiği "
  "bilgilendirmeye bak. Ve devlet katkısı sorgulama ekranına bak.")
I("Bildirim tarihi", "sürenin başladığı gün",
  "Bilgilendirmedeki tarih önemli, çünkü iki aylık süre o tarihten itibaren "
  "işlemeye başlıyor.")
T("Tarihi bulamıyorsan", "insan kaynaklarına sor",
  "Tarihi bulamıyorsan işyerinde insan kaynaklarına sor. Bu bilgiyi vermek "
  "zorundalar, ve tek soruyla öğrenirsin.")
T("Sorgulama ekranı", "devlet katkısını gösterir",
  "Devlet katkısı sorgulama ekranı, adına ne kadar katkı yatırıldığını ve "
  "limit bilgilerini gösterir. Orada gördüğün rakam sana özeldir.")
T("Bu üç kaynak", "birbirini doğrular",
  "Bu üç kaynağı birlikte okursan, kimseye sormadan kendi durumunu tam "
  "olarak görürsün. Birbirlerini doğrularlar.")
T("Tarihi bilmeden", "karar veremezsin",
  "Tarihi bilmeden karar veremezsin, çünkü sürenin ne kadarının kaldığını "
  "bilmiyorsun demektir.")

# ------------------------------------- 9. Cayarsan ne olur
T("İki yolun sonu", "nasıl görünüyor",
  "İki yolun sonunu da net bırakayım, çünkü belirsizlik karar vermeyi "
  "zorlaştırır.",
  cap="İki yolun sonu")
I("Cayarsan", "ödediklerin geri gelir",
  "Cayarsan, ödediğin katkı payları varsa gelirleriyle birlikte on iş günü "
  "içinde iade edilir, ve o dönem için devlet katkısı hesabında kalmaz.")
I("Kalırsan", "her ödemeye yüzde otuz eklenir",
  "Kalırsan, her ödemene yüzde otuz eklenmeye devam eder ve birikim uzun "
  "vadede senin adına çalışır.")
T("Karar geri dönülmez değil", "ama süre geri gelmez",
  "Karar sonsuza kadar bağlayıcı değil. Ama iki aylık süre bir kez geçer, ve "
  "geçtikten sonra çıkış koşulları farklıdır.")
T("Kalmak da", "geri dönülmez değil",
  "Kalmayı seçersen de kapı kapanmıyor. İlerleyen dönemde çıkabilirsin, "
  "sadece koşullar iki aylık dönemdekinden farklı oluyor.")
I("Fark şu", "hak kazanma süreye bağlanır",
  "Fark şu: devlet katkısına ne kadar hak kazanacağın, sistemde kaldığın "
  "süreye bağlı hâle gelir. Kapı kapanmaz, koşul değişir.")
T("Bu yüzden", "acele değil ama erteleme de değil",
  "Bu yüzden acele etmene gerek yok, ama ertelemek de bir seçim. Süre "
  "dolarsa, sistemde kalmayı seçmiş olursun.")

# ------------------------------------------------ 10. Bu hafta
T("Bu hafta", "üç adım",
  "Bu haftaya üç adım bırakıyorum, ve hiçbiri on dakikadan uzun sürmüyor.",
  cap="Bu hafta üç adım")
L("Birinci ve ikinci", ["Bordrondaki kesinti tutarını bul",
                        "Bilgilendirme tarihini öğren"],
  "Birinci adım: bordrondaki kesinti tutarını bul. İkinci adım: "
  "bilgilendirme tarihini öğren, gerekirse insan kaynaklarına sorarak.")
L("Üçüncü", ["Toplamı hesapla ve nokta üç ile çarp",
             "Sonra kendine likidite sorusunu sor"],
  "Üçüncü adım: toplamı hesapla, nokta üç ile çarp, ve kendine şu soruyu "
  "sor: bu parayı bu süre boyunca kenara koyabilir miyim?")
T("Cevabı sen bileceksin", "ben değil",
  "Cevabı sen bileceksin, ben değil. Benim işim rakamı ve süreyi doğru "
  "vermekti; kararı veren sensin.")
T("Bir de not", "kararını yazılı tut",
  "Bir küçük not: kararını ve tarihini bir yere yaz. Altı ay sonra neden "
  "öyle karar verdiğini hatırlamak, o kararı gözden geçirmeyi kolaylaştırır.")
T("Çünkü koşullar değişir", "sen de değişirsin",
  "Çünkü koşullar değişir, geliriniz değişir, önceliğiniz değişir. Yazılı "
  "bir gerekçe, gelecekteki kararınızın başlangıç noktasıdır.")
T("Ve en önemlisi", "kararı sen ver, süre değil",
  "En önemlisi şu: kararı sen ver, süre senin yerine vermesin. Aradaki fark, "
  "bu videonun tamamı.")
C("Hesabı bugün yap", "ve sonucu yaz",
  "Hesabı bugün yap ve sonucunu yorumlara yaz. Bu tür hesaplar işine "
  "yarıyorsa abone ol, burada her rakam kendi başına yapacağın bir işe "
  "dönüşüyor.")


# ---------------------------------------------------------------------------
# O SHORT: escolha com prazo, a conta, e o apontamento para o longo (493).
SHORT = [
    {"layout": "titulo", "kicker": "İki ayın var", "sub": "ve süre işliyor",
     "nar": "İşyerin üzerinden bir emeklilik planına dahil edildiysen, iki "
            "ayın var. Süre şu anda işliyor.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Seçen sensin", "sub": "bu sefer",
     "nar": "Seçen sensin. Ve seçmemek de bir seçim.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Devlet katkısı", "sub": "yüzde otuz",
     "nar": "Yatırdığın her yüz liraya, devlet otuz lira ekliyor. Bu bir "
            "getiri değil, kesin bir ekleme.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Hesap", "sub": "nokta üç ile çarp",
     "nar": "Bordrondaki aylık kesintiyi ay sayısıyla çarp, sonra nokta üç "
            "ile çarp. Karşılığında eklenen bu.", "sem_cap": True},
    {"layout": "cta", "kicker": "Peki caymak", "sub": "kimin için mantıklı",
     "nar": "Caymak kimin için mantıklı, ve süre ne zaman başlıyor? Tam "
            "videoda, aşağıdaki bağlantıda.",
     "sem_cap": True},
]

THUMB = {"l1": "iki ayın var", "l2": "yüzde 30"}

COPY = """# Otomatik katılımda karar senin, ama süre işliyor

## TITULO
Otomatik Katılımda İki Ayın Var: Yüzde 30 Devlet Katkısı ve Cayma Hesabı

## DESCRICAO
İşyerin üzerinden otomatik olarak bir emeklilik planına dahil edildiysen, elinde bir karar var ve o kararın süresi şu anda işliyor. Bu kanalda genellikle sana yapılan şeyleri konuşuyoruz: asgari ücret ne oldu, tavan ne belirlendi, zam ne zaman başladı. Bu video farklı, çünkü burada seçen sensin — ve seçmemek de bir seçim, çünkü süre dolduğunda karar kendiliğinden verilmiş oluyor.

Kararın etrafında döndüğü rakam şu: ödediğin katkı payının yüzde 30'u kadar bir tutar, devlet katkısı olarak hesabına ekleniyor. Bu oran daha önce yüzde 25'ti ve kanun değişikliğiyle yüzde 30'a çıkarıldı. Pratikte sisteme yatırdığın her 100 lira için hesabına 30 lira daha ekleniyor. Video bu noktada önemli bir ayrımı yapıyor: bu bir yatırım getirisi değil, kesin bir eklemedir. Fonun kazandırıp kazandırmayacağı ayrı bir konudur ve hiçbir kurum onu garanti etmez.

Sürenin tarafı ise şöyle: plana dahil edildiğin sana bildirildikten sonra iki ay içinde sözleşmeden cayabilirsin. Caydığında ödediğin katkı payları, varsa yatırım gelirleriyle birlikte on iş günü içinde iade edilir. Ama bu iki ay "risksiz deneme süresi" değil — cayarsan devlet katkısı da o hesapta kalmaz.

Hesap iki rakamla yapılıyor ve bordronla birlikte iki dakika sürüyor: aylık kesilen katkı payını sistemde kalmayı düşündüğün ay sayısıyla çarp, sonucu 0,3 ile çarp. Karşılaştırman gereken tam olarak bu iki sayıdır — senin verdiğin ve karşılığında eklenen. Üçüncü soru ise kişiye göre değişir: o parayı o süre boyunca kenara koyabilir misin?

Video bir çerçeve de veriyor: maaşı düzenli, bütçesi zorlanmayan ve yakın vadede büyük harcaması olmayan için sistemde kalmak öne çıkıyor; devreden kredi kartı borcu, düzensiz geliri veya hiç acil durum birikimi olmayan için caymak öne çıkıyor. Sıralama kişisel tercih değil matematiktir: önce yüksek faizli borç, sonra acil durum birikimi, sonra uzun vadeli emeklilik.

Son bölümde bu haftaya üç adım var: bordrondaki kesinti tutarını bul, bilgilendirme tarihini öğren, ve hesabı kendi rakamlarınla yap.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Hesabı yaptıysan sonucu buraya yaz: aylık kesinti ne kadar, kaç ay için düşünüyorsun, ve 0,3 ile çarpınca ne çıktı. Özellikle merak ettiğim şey, bildirim tarihini bordrodan bulabilen ile insan kaynaklarına sormak zorunda kalanların oranı — çünkü tarihi bilmeden karar veremiyorsun.

## HASHTAGS
#OtomatikKatılım #DevletKatkısı #SeviyeSeviye

## TAGS
otomatik katilim, bes devlet katkisi, cayma hakki, bireysel emeklilik, yuzde 30 devlet katkisi, oks nedir, emeklilik plani, maas bordrosu kesinti, bes hesaplama, calisan haklari, kidem ve emeklilik, tasarruf, acil durum birikimi, kisisel finans, seviye seviye

## CONFIGURACAO DE STUDIO
- Idioma: Türkçe (tr) | Categoria: Educação (27)
- Não é conteúdo para crianças
- Divulgação de conteúdo alterado ou sintético: SIM (voz gerada por IA)
- Local: Turquia | Licença: Licença padrão do YouTube
- Anúncios mid-roll: ligado (duração acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
26 Ağustos 2026'da kontrol edildi. Bu videodaki iki temel bilgi, birbirinden bağımsız iki kurumsal kaynakta doğrulanmıştır: (1) Emeklilik Gözetim Merkezi (egm.org.tr) — "Devlet Katkısı", "OKS nedir" ve "OKS-BES Karşılaştırması" sayfaları; (2) mevzuat metni — 4632 sayılı Bireysel Emeklilik Tasarruf ve Yatırım Sistemi Kanunu (mevzuat.gov.tr), otomatik katılım kanun metni (TBMM arşivi) ve SEDDK'nın sistemdeki yeni avantajlara ilişkin duyurusu. Doğrulanan iki bilgi şunlardır: devlet katkısı oranının yüzde 25'ten yüzde 30'a çıkarılmış olması, ve plana dahil edildiğinin bildirilmesinden itibaren iki ay içinde cayma hakkının bulunması, cayma hâlinde ödenen katkı paylarının varsa yatırım gelirleriyle birlikte on iş günü içinde iade edilmesi.

BU VİDEODA OLMAYANLAR VE NEDENİ. (a) Girişte bir defaya mahsus ödenen ilave devlet katkısının TUTARI verilmemiştir: baktığım iki resmi kaynak aynı sayıyı vermiyor — birinde beş yüz lira, diğerinde bin lira geçiyor. İki resmi kaynak aynı sayıyı vermiyorsa o sayı videoya girmez; kendi sözleşmenizdeki tutarı şirketinizin bilgilendirmesinden görebilirsiniz. Kararın bu rakama bağlı olmaması, bu boşluğun videoyu zayıflatmamasının nedenidir. (b) Hiçbir fon getirisi tahmini yapılmamıştır: getiri seçilen fona ve vadeye bağlıdır ve hiçbir kurum garanti etmez. Video yalnızca kesin olan kısmı — yüzde 30'luk eklemeyi — likidite ile karşılaştırır. (c) İki aylık süreden sonraki çıkışlarda devlet katkısına hak kazanma koşulları sistemde kalınan süreye bağlıdır ve video bu koşulları sayısallaştırmaz. Burada yatırım tavsiyesi veya kişiye özel finansal danışmanlık yoktur.
"""

SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-007",
    "idioma": "tr",
    "voz": "tr-TR-AhmetNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1D3557", "c1": "#E63946", "c2": "#F4A261", "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "seviye-seviye-007.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
