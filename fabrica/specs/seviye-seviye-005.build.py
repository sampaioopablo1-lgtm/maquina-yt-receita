#!/usr/bin/env python3
"""Monta a spec seviye-seviye-005.

CANAL. Veredito `liberado` — um dos DOIS da frota. Short mediana 71,01 v/d
(topo 174,43), longo 3,95, 2.320 views no acervo. `liberado` autoriza a faixa
inteira de 12 a 15 min, e e o que esta feito aqui.

EIXO. O banco marca dois eixos com ZERO usados — `asgari ucret / zam` e
`emekli maasi / seyyanen zam` — e os DOIS estao errados. Os quatro titulos
publicados sao: asgari ucret de 28.075 TL contra a linha da fome (duas vezes,
longo e short), o zam do aposentado de %1,78 em julho, e o menor salario de
aposentadoria de 23.552 TL com %17,76. Ou seja, salario minimo E aposentadoria
ja foram cobertos.

  E a terceira vez em duas horas que o `usado_em` mente — no labtreinamento
  faltava marcacao, aqui tambem. O campo nao serve como prova em nenhuma das
  duas direcoes (aprendizado 421). O que decide e a lista de titulos
  publicados, que e dado primario.

  Como os dois eixos livres nao estavam livres, a pauta veio de pesquisa nova.

A PAUTA, mensal por natureza e com fonte institucional — e ela quase me pegou
com um erro de digito, de novo.

  A primeira passagem devolveu TRES numeros diferentes para a mesma coisa:
    "kira artis orani 1,90"     (kadimhukuk)
    "Yuzde 31,90"               (ayboga)
    "Yeni Zam Siniri 2,82"      (demiraydinhukuk)

  A segunda passagem resolveu com os dados do TUIK, divulgados em 3 de agosto
  de 2026, referentes a julho:

    TUFE mensal ................................ +1,78%
    TUFE anual (mesmo mes do ano anterior) ..... +31,75%
    TUFE media movel de doze meses ............. +31,90%   <- o teto do aluguel
    TUFE contra dezembro ....................... +19,86%

  O "1,90" era truncamento de "31,90". O "2,82" nao bate com nada.

  E o numero que faz a pauta existir, do mesmo comunicado, variacao anual por
  grupo de despesa:

    konut, su, elektrik, gaz e outros combustiveis ... +40,32%
    alimentos e bebidas nao alcoolicas ............... +37,53%
    transporte ....................................... +30,83%

A TESE: o teto legal do aluguel em agosto e 31,90%, e o grupo de despesa da
propria moradia subiu 40,32% no ano. As duas coisas saem do MESMO comunicado
do TUIK, e a distancia entre elas — mais de oito pontos — e o que aperta os
dois lados do contrato ao mesmo tempo. Nao e vilania de ninguem: e indexacao
por media movel contra preco corrente.

DETALHE PRATICO QUE QUASE NINGUEM DIZ: o teto e um MAXIMO. O proprietario pode
aplicar menos, e nao pode aplicar mais. Isso muda a conversa de "quanto vai
subir" para "quanto voce vai propor".

O QUE O VIDEO NAO FAZ: nao da conselho juridico, nao diz o que fazer se o
proprietario exigir acima do teto (isso e advogado), e nao preve o teto dos
proximos meses — ele depende de dados que ainda nao existem.

ACENTOS. Este canal ja publicou spec em ASCII (seviye-seviye-004, que eu
corrigi antes de subir, e outras que ficaram no inventario). Turco aqui vai com
todos os diacriticos: ç, ğ, ı, İ, ö, ş, ü.
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


# ------------------------------------------------------------------- cap 1
T("Yüzde otuz bir doksan", "ağustos kira tavanı",
  "Ağustos ayında kira artışının üst sınırı yüzde otuz bir virgül doksan. Aynı "
  "açıklamada bir sayı daha var, ve o daha büyük.",
  cap="İki sayı, aynı açıklama")
I("Nereden geliyor", "TÜİK verisi",
  "Her iki sayı da Türkiye İstatistik Kurumu'nun temmuz enflasyon "
  "açıklamasından geliyor. Üç ağustosta yayımlandı.")
I("Hangi hesap", "on iki aylık ortalama",
  "Kira tavanı yıllık enflasyondan değil, on iki aylık ortalamadan çıkıyor. Bu "
  "ayrım önemli, birazdan nedenini göreceğiz.")
I("İkinci sayı", "konut giderleri",
  "İkinci sayı şu: konut, su, elektrik ve gaz grubu bir yılda yüzde kırk "
  "virgül otuz iki arttı.")
B("Aradaki fark", ["Kira tavanı", "Konut gideri"], [79, 100],
  "Kira tavanı otuz bir doksan, konut gideri kırk virgül otuz iki. Arada sekiz "
  "puandan fazla var.")
I("Bu kimin suçu değil", "endeksleme farkı",
  "Bu birinin kötü niyeti değil. Ortalamaya endeksli bir tavan ile güncel "
  "fiyat arasındaki fark bu.")
I("Kiracı ne hissediyor", "kira ağır geliyor",
  "Kiracı tarafında his şu: kira zaten ağır, ve üstüne otuz bir küsur zam "
  "geliyor.")
I("Ev sahibi ne hissediyor", "giderim daha hızlı arttı",
  "Ev sahibi tarafında his şu: binaya dair giderim kırk küsur arttı, ve ben "
  "otuz bir küsurla sınırlıyım.")
I("İkisi de doğru", "aynı tabloda",
  "İkisi de doğru, ve ikisi de aynı tablodan çıkıyor. Bu videonun amacı "
  "birinin tarafını tutmak değil, tabloyu göstermek.")
T("Neyi anlatacağım", "üç şey",
  "Sırayla üç şeye bakacağız, ve hiçbiri tahmin değil.")
L("İçerik", ["Sayı nereden çıkıyor",
             "Tavan bir üst sınır, zorunluluk değil",
             "Kendi hesabını nasıl yaparsın"],
  "Sayının nereden çıktığı, tavanın aslında ne olduğu, ve kendi hesabını nasıl "
  "yapacağın.")
I("Neyi anlatmayacağım", "hukuki tavsiye yok",
  "Anlatmayacağım şey de net: hukuki tavsiye vermiyorum. Ev sahibi tavanın "
  "üstünde bir şey isterse, o konu avukatın konusu.")
I("Ve tahmin yok", "sonraki aylar",
  "Sonraki ayların tavanını da söylemeyeceğim, çünkü o henüz var olmayan "
  "verilere bağlı.")
I("Başlayalım", "sayının kaynağı",
  "Sayının kaynağından başlayalım:")

# ------------------------------------------------------------------- cap 2
T("Dört farklı sayı", "aynı açıklamada",
  "TÜİK'in temmuz açıklamasında dört farklı enflasyon sayısı var, ve "
  "karıştırılmaları çok kolay.",
  cap="Aynı açıklamadaki dört sayı")
I("Birincisi", "aylık",
  "Aylık değişim: yüzde bir virgül yetmiş sekiz. Yani haziran ile temmuz "
  "arasındaki fark.")
I("İkincisi", "yıllık",
  "Yıllık değişim: yüzde otuz bir virgül yetmiş beş. Geçen yılın temmuzuna "
  "göre.")
I("Üçüncüsü", "on iki aylık ortalama",
  "On iki aylık ortalamalara göre değişim: yüzde otuz bir virgül doksan. Kira "
  "tavanı bu.")
I("Dördüncüsü", "aralığa göre",
  "Ve aralık ayına göre değişim: yüzde on dokuz virgül seksen altı. Yılın "
  "başından bugüne.")
B("İkisi çok yakın", ["Yıllık 31,75", "Ortalama 31,90"], [99, 100],
  "Dikkat: yıllık ve ortalama neredeyse aynı çıktı bu ay. Aralarında sadece on "
  "beş yüzde birlik var, ve bu bir rastlantı.")
I("Neden rastlantı", "her ay böyle değil",
  "Her ay böyle olmuyor. Enflasyon hızlı düşerken ortalama yıllıktan yüksek "
  "kalır, hızlı yükselirken tersi olur.")
I("Bu yüzden karışıyor", "iki sayı yakın olunca",
  "İki sayı yakın olduğunda insanlar birini diğerinin yerine kullanıyor ve "
  "sonuç tutuyor. Sonraki ay tutmuyor.")
I("Doğru olan hangisi", "ortalama",
  "Konut kirası için doğru olan her zaman on iki aylık ortalama. Yıllık sayı "
  "başka işler için.")
I("Bir uyarı daha", "internetteki hesaplayıcılar",
  "İnternetteki bazı hesaplayıcılar bu ay için bir virgül doksan yazıyor. O "
  "otuz bir virgül doksanın kırpılmış hâli, ve yanlış.")
I("Nasıl kontrol edersin", "kaynağa bak",
  "Kontrolü basit: sayının yanında TÜİK ve tarih yazıyor mu. Yazmıyorsa "
  "kullanma.")

# ------------------------------------------------------------------- cap 3
T("Tavan bir üst sınır", "zorunluluk değil",
  "Şimdi en çok işine yarayacak kısım, ve en az söyleneni.",
  cap="Tavan bir üst sınır, zorunluluk değil")
I("Yasal anlamı", "en fazla bu kadar",
  "Otuz bir virgül doksan bir üst sınır. Ev sahibi bunun üstüne çıkamaz.")
I("Ama alt sınır yok", "daha az uygulanabilir",
  "Alt sınır diye bir şey yok. Ev sahibi isterse daha düşük bir oran "
  "uygulayabilir, ve bu tamamen yasaldır.")
I("Bu neyi değiştirir", "sorunun kendisini",
  "Bu, konuşmanın sorusunu değiştirir. Soru artık ne kadar zam gelecek değil, "
  "sen ne teklif edeceksin.")
I("Neden bu işe yarar", "boş kalma maliyeti",
  "Çünkü ev sahibi için de bir hesap var: kiracı çıkarsa ev boş kalır, "
  "komisyon ve tadilat masrafı çıkar.")
I("Yani iki taraf da", "kayıptan kaçınıyor",
  "İki taraf da aynı şeyden kaçınıyor: gereksiz maliyetten. Bu ortak zemin "
  "sayılabilir.")
T("Bir şeyi netleştireyim", "bu bir garanti değil",
  "Burada bir şeyi net söyleyeyim, çünkü kolayca abartılabilir.")
I("Garanti yok", "sonuç değişir",
  "Daha düşük bir oran istemek sonucu garanti etmez. Ev sahibinin durumu, "
  "bölgen ve piyasa hepsi etkiler.")
I("Garanti olan tek şey", "sormamak",
  "Garanti olan tek şey şu: hiç konuşmazsan, tavan otomatik olarak "
  "uygulanır.")
I("Ve tekrar", "hukuki tavsiye değil",
  "Ve tekrar ediyorum: bu hukuki tavsiye değil. Sözleşmen ve durumun özeldir.")
I("Konuşmaya nasıl başlanır", "sayıyla, şikâyetle değil",
  "Konuşmaya başlamanın işe yarayan yolu şikâyet değil, sayı. Kaç yıldır "
  "oturuyorsun, ödemelerin düzenli mi, ev için neler yaptın.")
I("Bunlar niye sayılır", "ev sahibinin riski",
  "Bunlar ev sahibi için risk göstergesi. Düzenli ödeyen ve uzun süredir "
  "oturan bir kiracı, boş kalma riskini azaltır.")
I("Bir de zamanlama", "erken konuş",
  "Zamanlama da işin parçası. Yenilenme tarihinden haftalar önce konuşmak, o "
  "hafta konuşmaktan farklı.")
I("Sonuç ne olursa olsun", "yazılı olsun",
  "Ve sonuç ne olursa olsun, anlaşılan rakamın yazılı olmasını iste. Bu "
  "kiracıyı da ev sahibini de korur.")

# ------------------------------------------------------------------- cap 4
T("Kendi hesabın", "üç adım",
  "Üç adımda kendi sayını çıkar. Hepsi bir kâğıtta biter.",
  cap="Kendi hesabını nasıl yaparsın")
I("Birinci adım", "mevcut kiran",
  "Birinci adım: şu anda ödediğin aylık kira.")
I("İkinci adım", "tavanla çarp",
  "İkinci adım: bunu bir virgül üç bir dokuz ile çarp. Sonuç, ağustosta yasal "
  "olarak çıkabileceği en yüksek rakam.")
I("Üçüncü adım", "farkı yaz",
  "Üçüncü adım: yeni rakamdan eskisini çıkar. Aradaki fark, aylık bütçenden "
  "gidecek olan tutar.")
I("Sonra bir çarpma daha", "on iki ile",
  "Sonra bunu on iki ile çarp. Yıllık etki bu, ve genelde beklenenden büyük "
  "çıkıyor.")
I("Bu sayıyı ne yapacaksın", "karşılaştırma",
  "Bu sayıyı gelirinin artışıyla karşılaştır. İkisi aynı hızda artmıyorsa, "
  "aradaki farkı başka bir kalemden bulman gerekecek.")
I("Karşılaştırmanın kolay yolu", "iki yüzde",
  "Kolay yolu şu: kiran yüzde kaç arttı, gelirin yüzde kaç arttı. İki sayıyı "
  "yan yana yaz.")
I("Kiranın payı", "gelirin içindeki oran",
  "Bir de şunu hesapla: kira, aylık gelirinin yüzde kaçını alıyor. Zamdan önce "
  "ve zamdan sonra.")
I("Neden bu oran", "asıl değişen bu",
  "Çünkü asıl değişen bu orandır. Kira arttı demek yeterli değil; bütçenin ne "
  "kadarını yediği değişti mi, asıl soru bu.")
I("Elinde ne kalıyor", "üç sayı",
  "Sonunda elinde üç sayı olacak: aylık fark, yıllık fark, ve kiranın gelir "
  "içindeki yeni payı. Üçü birlikte karar verdiriyor.")
T("Bir hatırlatma", "sözleşme yıl dönümü",
  "Ve sık atlanan bir ayrıntı.")
I("Tavan aya göre", "senin ayına bak",
  "Kira artışı sözleşmenin yıl dönümünde yapılır. Yani seni ilgilendiren "
  "tavan, senin ayının tavanıdır.")
I("Ağustos senin ayın değilse", "bu sayı senin sayın değil",
  "Sözleşmen ağustosta yenilenmiyorsa, buradaki sayı senin sayın değil — ama "
  "hesap yöntemi aynı.")
I("Her ay değişiyor", "TÜİK her ay açıklıyor",
  "TÜİK bu veriyi her ay açıklıyor, ve tavan her ay değişiyor. Kendi ayının "
  "sayısına bakman gerekir.")

# ------------------------------------------------------------------- cap 5
T("En pahalı okuma hatası", "yıllıkla ortalamayı karıştırmak",
  "Şimdi bu konuda yapılan en pahalı hatayı görelim, çünkü parayla ölçülüyor.",
  cap="En pahalı okuma hatası")
I("Hata şu", "yanlış sayıyı kullanmak",
  "Hata, kira için yıllık enflasyonu kullanmak. Bu ay ikisi çok yakın olduğu "
  "için sonuç neredeyse tutuyor.")
I("Ama her ay değil", "fark açıldığında",
  "Enflasyonun hızlı düştüğü dönemde ortalama yıllığın epey üstünde kalır. O "
  "zaman yanlış sayı yüzlerce lira fark eder.")
I("Kim kaybeder", "duruma göre değişir",
  "Ve kimin kaybettiği duruma bağlı: yanlış sayı bazen kiracının aleyhine "
  "çıkar, bazen ev sahibinin.")
I("Doğrusu tek", "on iki aylık ortalama",
  "Doğru olan tek sayı var ve değişmiyor: on iki aylık ortalama. Adı da "
  "açıklamada aynen böyle geçiyor.")
I("İkinci hata", "eski ayın tavanını kullanmak",
  "İkinci sık hata: geçen ayın tavanıyla hesap yapmak. Tavan her ay "
  "değişiyor, ve sözleşmenin ayı hangisiyse o geçerli.")
I("Üçüncü hata", "yuvarlamak",
  "Üçüncüsü: yuvarlamak. Otuz iki demek küçük bir fark gibi duruyor, ama on "
  "iki ayla çarpılınca büyüyor.")
B("Yuvarlamanın bedeli", ["31,90 ile", "32 ile"], [100, 100],
  "İki batık neredeyse aynı görünüyor, ve yıl sonunda aradaki fark bir "
  "akşam yemeği kadar. Küçük ama gereksiz.")
I("Dördüncü hata", "sözlü anlaşmaya güvenmek",
  "Ve dördüncüsü: rakamı yazılı hâle getirmemek. Anlaşılan oran ne olursa "
  "olsun, yazılı olması iki tarafın da işine yarar.")
T("Neden konut gideri daha hızlı", "ortalamanın gecikmesi",
  "Baştaki iki sayıya dönelim, çünkü aradaki fark tesadüf değil.",
  cap="Neden konut gideri daha hızlı arttı")
I("Ortalama geriden gelir", "on iki ayın izi",
  "On iki aylık ortalama, adı üstünde, son on iki ayın izini taşır. İçinde "
  "geçen sonbaharın verileri de var.")
I("Güncel fiyat öyle değil", "bugünü gösterir",
  "Konut giderlerinin yıllık artışı ise bugünü gösterir: elektrik, su ve "
  "doğalgaz faturası bu ayki fiyatla geliyor.")
B("İki farklı zaman", ["Ortalama (geçmiş 12 ay)", "Yıllık (bugün)"],
  [79, 100],
  "Yani biri geçmiş on iki ayın ortalaması, diğeri bugünün fotoğrafı. Farklı "
  "zamanları ölçüyorlar.")
I("Kiracı için ne demek", "kira daha yavaş artıyor",
  "Kiracı açısından bu, kiranın diğer konut giderlerinden daha yavaş artması "
  "demek — en azından bu ay.")
I("Ev sahibi için ne demek", "gideri daha hızlı artıyor",
  "Ev sahibi açısından tersi: binaya dair giderleri kiradan hızlı artıyor.")
I("İkisi de doğru", "aynı anda",
  "İki cümle de aynı anda doğru, ve bu yüzden bu konuda iki taraf da haklı "
  "hissediyor.")
I("Diğer gruplar", "gıda ve ulaşım",
  "Karşılaştırma için: gıda yüzde otuz yedi virgül elli üç, ulaşım yüzde otuz "
  "virgül seksen üç arttı.")
I("Sıralama önemli", "konut en hızlısı",
  "Yani üç büyük harcama grubu içinde en hızlı artan konut oldu. Gıdanın "
  "üstünde.")
T("Ortalama zamanla ne yapar", "iki yönde de gecikir",
  "Son bir bölüm, ve o gelecek aylarda işine yarayacak olan.",
  cap="Ortalama zamanla ne yapar")
I("Enflasyon düşerken", "tavan yüksek kalır",
  "Enflasyon düşmeye başladığında, on iki aylık ortalama bir süre yüksek "
  "kalır. İçinde hâlâ eski aylar var.")
I("Kiracı için", "geç gelen rahatlama",
  "Kiracı açısından bu, rahatlamanın gecikmesi demek: fiyatlar yavaşlıyor ama "
  "kira tavanı hâlâ eski hızı taşıyor.")
I("Enflasyon yükselirken", "tavan düşük kalır",
  "Tersi durumda da tersi olur: enflasyon hızlanırken tavan geride kalır, ve "
  "bu sefer ev sahibi geriden gelir.")
B("Gecikme iki yönlü", ["Düşüşte", "Yükselişte"], [100, 100],
  "Yani sistem kimseyi kayırmıyor. Sadece geç kalıyor, ve kime yaradığı hangi "
  "dönemde olduğuna bağlı.")
I("Bunu bilmek ne sağlar", "beklentiyi ayarlar",
  "Bunu bilmek bir şeyi sağlar: gelecek ayın tavanının bugünkü habere değil, "
  "son on iki ayın birikimine bağlı olduğunu bilirsin.")
I("Ve tahmin yine yok", "veriler henüz yok",
  "Ama yine tahmin yok. Gelecek ayın sayısı, henüz açıklanmamış verilerle "
  "hesaplanacak.")
I("Yapılabilecek tek şey", "her ay bakmak",
  "Yapılabilecek tek şey her ay yeni açıklamaya bakmak. Ayın üçünde "
  "yayımlanıyor, ve tavan orada.")
C("Seviye Seviye", "sayı önce, yorum sonra",
  "Bugün tek bir şey yap: kiranı bir virgül üç bir dokuz ile çarp ve farkı "
  "yaz. Sözleşme ayını da not et. Video işine yaradıysa abone ol.")


# -------------------------------------------------------------------- short
SHORT = [
    {"layout": "titulo", "kicker": "Kira tavanı: %31,90",
     "sub": "ağustos 2026",
     "nar": "Ağustosta kira artışının üst sınırı yüzde otuz bir virgül doksan.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Nereden", "preco": "TÜİK, 12 aylık ortalama",
     "nar": "TÜİK'in temmuz verisinden, on iki aylık ortalamaya göre. Yıllık "
            "enflasyondan değil.", "sem_cap": True},
    {"layout": "item", "kicker": "Aynı açıklamada", "preco": "konut %40,32",
     "nar": "Aynı açıklamada konut, su, elektrik ve gaz grubu yüzde kırk "
            "virgül otuz iki arttı. Sekiz puan daha fazla.", "sem_cap": True},
    {"layout": "item", "kicker": "Tavan üst sınırdır",
     "preco": "daha azı yasaldır",
     "nar": "Ve tavan bir üst sınır: ev sahibi daha düşük uygulayabilir. Soru "
            "ne kadar zam gelecek değil, sen ne teklif edeceksin.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Seviye Seviye", "sub": "kendi hesabın",
     "nar": "Kiranı bir virgül üç bir dokuz ile çarp ve farkı yaz.",
     "sem_cap": True},
]

COPY = """# Ağustos 2026 kira artışı: tavan %31,90, konut gideri %40,32

## TITULO
Kira Artışı Ağustos 2026: Tavan Yüzde 31,90 — Ama Konut Gideri Yüzde 40,32 Arttı

## DESCRICAO
Ağustos ayında kira artışının üst sınırı yüzde 31,90. Aynı TÜİK açıklamasında bir sayı daha var, ve o daha büyük: konut, su, elektrik ve gaz grubu bir yılda yüzde 40,32 arttı. Aradaki sekiz puandan fazla fark, sözleşmenin iki tarafını da aynı anda sıkıştırıyor — ve kimsenin kötü niyeti değil, ortalamaya endeksli bir tavan ile güncel fiyat arasındaki farktan ibaret.

SAYILAR VE KAYNAK

TÜİK, temmuz 2026 enflasyon verilerini 3 Ağustos 2026'da yayımladı. Aynı açıklamada dört farklı enflasyon sayısı var ve karıştırılmaları çok kolay: aylık değişim %1,78; yıllık (geçen yılın aynı ayına göre) %31,75; on iki aylık ortalamalara göre %31,90; aralık ayına göre %19,86. KONUT KİRASI İÇİN GEÇERLİ OLAN HER ZAMAN ON İKİ AYLIK ORTALAMADIR — yani %31,90.

Bu ay yıllık (%31,75) ve ortalama (%31,90) neredeyse aynı çıktı; aralarında sadece 0,15 puan var. Bu bir rastlantı: enflasyon hızlı düşerken ortalama yıllıktan yüksek kalır, hızlı yükselirken tersi olur. İki sayı yakın olduğunda insanlar birini diğerinin yerine kullanıyor ve sonuç tutuyor — sonraki ay tutmuyor.

BİR UYARI: internetteki bazı hesaplayıcılar bu ay için "1,90" yazıyor. O, 31,90'ın kırpılmış hâli ve yanlış. Kontrolü basit — sayının yanında TÜİK ve tarih yazıyor mu?

TAVAN BİR ÜST SINIRDIR, ZORUNLULUK DEĞİL

Videonun en az söylenen kısmı bu. %31,90 bir üst sınırdır: ev sahibi bunun üstüne çıkamaz, ama isterse daha düşük bir oran uygulayabilir ve bu tamamen yasaldır. Bu, konuşmanın sorusunu değiştirir: soru artık "ne kadar zam gelecek" değil, "sen ne teklif edeceksin". Ev sahibi için de bir hesap var — kiracı çıkarsa ev boş kalır, komisyon ve tadilat masrafı çıkar. Daha düşük bir oran istemek sonucu GARANTİ ETMEZ; garanti olan tek şey, hiç konuşmazsan tavanın otomatik uygulanmasıdır.

KENDİ HESABIN (üç adım)

1) Şu anda ödediğin aylık kira. 2) Bunu 1,3190 ile çarp — sonuç, ağustosta yasal olarak çıkabilecek en yüksek rakam. 3) Yeni rakamdan eskisini çıkar; aradaki fark aylık bütçenden gidecek tutar. Sonra 12 ile çarp: yıllık etki genelde beklenenden büyük çıkıyor. Bu sayıyı gelirinin artışıyla karşılaştır.

SIK ATLANAN AYRINTI: kira artışı sözleşmenin YIL DÖNÜMÜNDE yapılır. Sözleşmen ağustosta yenilenmiyorsa bu videodaki sayı senin sayın değil — ama hesap yöntemi aynı. TÜİK bu veriyi her ay açıklıyor ve tavan her ay değişiyor.

NEDEN KONUT GİDERİ DAHA HIZLI ARTTI

On iki aylık ortalama, son on iki ayın izini taşır — içinde geçen sonbaharın verileri de var. Konut giderlerinin yıllık artışı ise bugünü gösterir: elektrik, su ve doğalgaz faturası bu ayki fiyatla geliyor. Biri geçmiş on iki ayın ortalaması, diğeri bugünün fotoğrafı; farklı zamanları ölçüyorlar. Karşılaştırma için diğer büyük gruplar: gıda ve alkolsüz içecekler %37,53, ulaştırma %30,83. Üç büyük harcama grubu içinde en hızlı artan konut oldu — gıdanın da üstünde.

BU VİDEODA OLMAYANLAR: hukuki tavsiye yok. Ev sahibi tavanın üstünde bir şey isterse o konu avukatın konusudur. Sonraki ayların tavanı da yok — henüz var olmayan verilere bağlı.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
İki soru, ve cevapları haberlerde olmayan tek veri: sözleşmenin yenilenme ayı hangisi, ve bu yıl sana teklif edilen oran tavanın altında mı kaldı? Yorumlarda toplamak istiyorum — özellikle merak ettiğim, tavandan düşük oran uygulanan gerçek örnekler var mı.

## HASHTAGS
#KiraArtışı #TÜİK #SeviyeSeviye

## TAGS
kira artis orani, kira zammi 2026, agustos kira artisi, tufe, tuik, enflasyon temmuz 2026, kira hesaplama, konut kirasi, ev sahibi kiraci, kira sozlesmesi, 12 aylik ortalama, konut giderleri, elektrik dogalgaz zam, kisisel finans, butce

## CONFIGURACOES DO STUDIO
- Idioma: Turkce (tr) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Turquia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Todos os percentuais vem do comunicado do TUIK sobre o TUFE de julho de 2026, divulgado em 3 de agosto de 2026: variacao mensal +1,78%, anual +31,75%, media movel de doze meses +31,90% (o teto do aluguel), e contra dezembro +19,86%. Variacao anual por grupo: konut/agua/eletricidade/gas +40,32%, alimentos +37,53%, transporte +30,83%. Conferido em DUAS passagens de busca: a primeira devolveu tres valores CONTRADITORIOS para o teto (1,90 / 31,90 / 2,82) e a segunda resolveu com os dados do proprio instituto — o "1,90" e truncamento de "31,90" e o "2,82" nao corresponde a nada. Essa contradicao esta registrada de proposito. O teto do aluguel e um MAXIMO legal, nao um valor obrigatorio, e incide na data de aniversario do contrato, nao no mes em que o video foi publicado. Este material e educativo sobre orcamento domestico: NAO e aconselhamento juridico, nao trata de disputa contratual e nao preve os tetos dos proximos meses.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seviye-seviye-005.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-005",
    "idioma": "tr",
    "voz": "tr-TR-AhmetNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1A2430", "c1": "#C0392B", "c2": "#2E86A8",
               "bg": "#F5F2EE"},
    "thumb": {"l1": "%31,90", "l2": "kira tavanı"},
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
    grava(SPEC, "fabrica/specs/seviye-seviye-005.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
