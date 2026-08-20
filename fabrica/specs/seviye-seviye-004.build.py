#!/usr/bin/env python3
"""Monta a spec seviye-seviye-004.

POR QUE ESTE CANAL, POR QUE AGORA

Primeiro da fila que consegue produzir (ultimo pacote em 18/08 06:28) e o
MELHOR canal da frota: mediana de short em 81,26 views/dia, o unico com
veredito `liberado` na v_maquina_licoes — o unico em que o longo se paga.

POR QUE ESTE TEMA

O laco de aprendizado (v_maquina_licoes, ligado em 20/08/2026) mostrou o que
duas semanas de publicacao ja tinham provado neste canal, e que ninguem tinha
lido ainda:

    En Dusuk Emekli Ayligi 23.552 TL: %17,76 Zammin Gercek Matematigi
                                                 short  222,9 v/d  (2,2 dias)
    28.075 TL — aclik sinirinin altinda           short   96,8 v/d  (7,4 dias)
    Asgari ucret aclik sinirinin altinda...       short   82,6 v/d

A assinatura e sempre a mesma: CIFRA EXATA EM TL OU EM PORCENTO, mais a
matematica real por tras de um numero oficial. E o nicho concorda — o eixo
`emekli maasi / seyyanen zam` domina o topo medido (9.754, 4.003, 3.483,
2.951, 2.783, 2.717 v/d).

O eixo ja foi usado UMA vez, ha dois dias, e foi o melhor video do canal. Entao
o que precisa ser inedito nao e o eixo: e o ANGULO dentro dele. Similaridade
do titulo contra o acervo do canal: 0,322, teto 0,65.

O GIRO

A leitura comum e "o zam de Ocak sai em Aralik". Sai, mas nao e DECIDIDO em
Aralik: ele e construido mes a mes, e o primeiro mes ja fechou. Quem so olha em
dezembro recebe o numero pronto; quem acompanha desde agosto ve ele se formar.

A DOR DATADA, duas fontes que batem, a institucional primeiro:

  TUIK, divulgacao de 3 de agosto de 2026: o TUFE de julho subiu 1,78% no mes.
  Esse e o PRIMEIRO dos seis meses (julho a dezembro) cuja inflacao acumulada
  define o reajuste de SSK e Bag-Kur em janeiro de 2027 — a regra de dois
  reajustes por ano, em janeiro e julho, sobre a inflacao REALIZADA dos seis
  meses anteriores.
  Reportado com os mesmos numeros por NTV, Yeni Safak e Kariyer.net.

  Akbank Ekonomik Arastirmalar: estimativa de cerca de 2,2% para agosto. Entra
  no roteiro DECLARADA COMO ESTIMATIVA, e o capitulo 4 existe exatamente para
  ensinar a diferenca entre estimativa e realizado.

O QUE O ROTEIRO NAO FAZ, de proposito: nao preve o percentual final de janeiro,
nao promete valor de maas, nao trata de refah payi (que e decisao politica e
nao aritmetica) e nao mistura a regra do memur, que e outra (acordo coletivo
mais diferenca de inflacao). Isso esta dito na cena e na descricao.

O numero anual do TUFE FICOU DE FORA: as duas buscas devolveram valor truncado
e incoerente entre si. Numero que nao fecha entre fontes nao entra — e o video
nao precisa dele, porque o mecanismo do acumulado usa o mensal.

TAXA DA VOZ. tr-TR-AhmetNeural, MODELO_VOZ de ensaio.py: R = 15,35 chars/s,
P = 1,337 s por frase. Densidade medida do canal: 2,71 frases/cena no longo —
a mais alta da frota — e 1,80 no short. Com P alto e densidade alta, cada cena
custa 3,6 s so em pausa, entao 72 cenas gastam 261 s dos 810 antes de qualquer
texto. Por isso 72 e nao 80: orcamento de 8.105 caracteres, 113 por cena.
Faixa do short: 306 caracteres em 6 cenas para 35,9 s.
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


def I(kicker, preco, nar, cap=None):
    c = {"layout": "item", "kicker": kicker, "preco": preco, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def L(kicker, itens, nar):
    CENAS.append({"layout": "lista", "kicker": kicker, "itens": itens,
                  "nar": nar, "sem_cap": True})


def B(kicker, itens, alturas, nar):
    CENAS.append({"layout": "barras", "kicker": kicker, "itens": itens,
                  "alturas": alturas, "nar": nar, "sem_cap": True})


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ------------------------------------------- 1. Zam Aralık'ta hesaplanmıyor
T("Üç Ağustos", "ilk rakam girdi",
  "Ocak ayındaki emekli zammının ilk rakamı çoktan belli oldu. Üç Ağustos günü "
  "açıklandı, ve neredeyse kimse bunu zam olarak okumadı.",
  cap="Zam Aralık'ta hesaplanmıyor")
I("Temmuz TÜFE", "yüzde bir virgül yetmiş sekiz",
  "Türkiye İstatistik Kurumu, temmuz ayında tüketici fiyat endeksinin aylık "
  "yüzde bir virgül yetmiş sekiz arttığını açıkladı. Bu sayı haber olarak "
  "geçti, ve unutuldu.")
T("Oysa o sayı", "cebe girdi bile",
  "Oysa o sayı bir yere girdi. Ocak ayında emekli maaşına yapılacak zammın "
  "hesabına girdi, ve orada duruyor.")
T("Yaygın inanış", "zam Aralık'ta belli olur",
  "Yaygın inanış şudur: zam Aralık ayında belli olur. Doğru değil. Aralık'ta "
  "sadece son rakam eklenir.")
I("Zam belli olmaz", "inşa edilir",
  "Zam bir günde belli olmaz. Altı ay boyunca, ayda bir kez, parça parça inşa "
  "edilir. Ve ilk parça yerine oturdu.")
T("Fark neresi", "seyretmek ile beklemek",
  "Aradaki fark şu. Aralık'ta bakan kişi hazır bir rakam alır. Ağustos'tan beri "
  "izleyen kişi o rakamın nasıl oluştuğunu görür.")
L("Üç şey", ["Altı aylık cep nasıl işler",
             "Birikimli neden toplama değil",
             "Kendi takibinizi nasıl yaparsınız"],
  "Üç şey göreceksiniz. Altı aylık cebin nasıl işlediği. Birikimli hesabın "
  "neden toplama olmadığı. Ve kendi takibinizi nasıl kuracağınız.")
T("Söylemeyeceğim şey", "Ocak rakamı",
  "Şimdiden söyleyeyim: Ocak ayındaki oranın kaç olacağını söylemeyeceğim. "
  "Kimse bilemez, çünkü beş ay daha var.")
I("Söyleyeceğim şey", "mekanizma",
  "Söyleyeceğim şey mekanizma. Mekanizmayı bilen kişi her ay kendi hesabını "
  "günceller, ve haberin söylemesini beklemez.")
T("Bir sınır daha", "bu memuru kapsamaz",
  "Bir sınır daha baştan. Burada anlatılan kural SSK ve Bağ-Kur emeklisi "
  "içindir. Memur maaşının kuralı başkadır, ve sonda ona da değineceğim.")
C("Önce kural", "yasada ne yazıyor",
  "Önce kuralın kendisine bakalım. Yasada ne yazıyor.")

# ---------------------------------------------- 2. Altı aylık cep nasıl işler
I("Yılda iki kez", "Ocak ve Temmuz",
  "SSK ve Bağ-Kur emeklisi yılda iki kez zam alır. Ocak ayında bir kez, Temmuz "
  "ayında bir kez.",
  cap="Altı aylık cep nasıl işler")
I("Ölçüt", "gerçekleşen enflasyon",
  "Ölçüt tahmin değil, gerçekleşen enflasyondur. Yani geçmiş altı ayda fiyatlar "
  "gerçekte ne kadar artmışsa, zam o kadar olur.")
T("Ocak zammının penceresi", "Temmuz'dan Aralık'a",
  "Ocak ayındaki zammın penceresi Temmuz'da açılır, ve Aralık'ta kapanır. Altı "
  "ay, altı rakam.")
B("Pencere", ["Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"],
  [1.0, 0.15, 0.15, 0.15, 0.15, 0.15],
  "Şu anda bu pencerenin sadece ilk ayı dolu. Temmuz girdi. Kalan beş ay hâlâ "
  "boş, ve her biri ayın üçünde açıklanacak.")
T("Temmuz zammı ise", "başka pencereden geldi",
  "Bu arada Temmuz'da alınan zam bu pencereden gelmedi. O, Ocak'tan Haziran'a "
  "kadarki pencerenin sonucuydu. Pencereler birbirini takip eder.")
I("Açıklama günü", "her ayın üçü",
  "Rakam her ayın üçünde gelir. Takvimi bilmek işin yarısı: o gün çıkan sayı, "
  "sizin cebinize giren sayıdır.")
T("Neden önemli", "çünkü geri alınmaz",
  "Ve bu neden önemli? Çünkü o sayı geri alınmaz. Yüksek bir ay pencereye "
  "girdiğinde, sonraki aylar düşük gelse bile o giriş orada kalır.")
T("Tersi de doğru", "düşük ay da kalır",
  "Tersi de doğru. Düşük bir ay girdiğinde, sonraki ayların yüksek gelmesi onu "
  "silmez. Sadece üstüne eklenir.")
I("Yani zam", "birikimin toplamı",
  "Yani zam, altı ayın birikiminin sonucudur. Tek bir ayın değil. Bu, haberde "
  "en çok atlanan nokta.")
T("Bir ay kötü geldi", "panik yok",
  "Bir ay kötü geldiğinde paniğe gerek yok, ve bir ay iyi geldiğinde de kutlama "
  "erken. Altı ay uzun bir yol.")
C("Şimdi hesabın kendisi", "ve neden toplama değil",
  "Şimdi hesabın kendisine gelelim. Ve burası çoğu insanın yanlış yaptığı yer.")

# ------------------------------------- 3. Birikimli toplama değil, çarpmadır
T("En sık hata", "yüzdeleri toplamak",
  "Altı ayın yüzdesini alt alta yazıp toplamak. En sık yapılan hata bu, ve "
  "sonucu her zaman olduğundan küçük çıkarır.",
  cap="Birikimli toplama değil, çarpmadır")
I("Neden", "her ay öncekinin üstüne biner",
  "Sebebi basit. İkinci ayın zammı, birinci aydan sonraki fiyatın üzerine "
  "biner. Yani zaten artmış bir sayının üzerine.")
T("Küçük bir örnek", "iki ay üzerinden",
  "Küçük bir örnekle bakalım. İlk ay yüzde iki, ikinci ay yine yüzde iki olsun.")
I("Toplama derse", "yüzde dört",
  "Toplama yapan kişi yüzde dört der. Yakın, ama eksik.")
I("Gerçek", "yüzde dört virgül sıfır dört",
  "Gerçeği yüzde dört virgül sıfır dört. Fark küçük görünüyor, değil mi?")
T("Altı ayda", "küçük fark büyür",
  "İki ayda küçük. Altı ayda o küçük fark büyür, ve maaşın üzerinde gerçek bir "
  "para hâline gelir.")
L("Doğru yöntem", ["Her ayı yüzde değil kat olarak yaz",
                   "Katları birbiriyle çarp",
                   "Sonucu yeniden yüzdeye çevir"],
  "Doğru yöntem şu. Her ayı kat olarak yazın. Katları birbiriyle çarpın. Ve "
  "sonucu tekrar yüzdeye çevirin.")
I("Kat ne demek", "yüzde iki ise bir virgül sıfır iki",
  "Kat demek şudur: yüzde iki artış, bir virgül sıfır iki ile çarpmak demektir. "
  "Yüzde bir virgül yetmiş sekiz ise, bir virgül sıfır bir yedi sekiz.")
T("Telefonun hesap makinesi", "yeter",
  "Bunun için tabloya gerek yok. Telefonun hesap makinesi yeter. Altı çarpma, "
  "sonunda bir çıkarma.")
C("Peki tahminler", "onlar nereye giriyor",
  "Peki şu anda dolaşan tahminler? Onlar bu hesabın neresine giriyor?")

# --------------------------------- 4. Tahmin ile gerçekleşen arasındaki fark
T("Kısa cevap", "hiçbir yerine",
  "Kısa cevap: hiçbir yerine. Tahmin cebe girmez. Cebe sadece açıklanan rakam "
  "girer.",
  cap="Tahmin ile gerçekleşen arasındaki fark")
I("Örnek", "Ağustos için yüzde iki virgül iki",
  "Örneğin Akbank Ekonomik Araştırmalar, Ağustos ayı için yaklaşık yüzde iki "
  "virgül iki tahmin etti. Bu bir tahmindir, ve tahmin olduğu söylenmiştir.")
T("Tahminin işi", "hazırlık",
  "Tahminin bir işi var, ve değerlidir: hazırlık. Ne bekleyeceğinizi kabaca "
  "gösterir.")
T("Tahminin işi değil", "hesap",
  "Ama tahminin işi hesap yapmak değil. Hesabı açıklanan rakam yapar, ve o "
  "ayın üçünde gelir.")
I("İkisini karıştırmak", "iki kez üzülmek",
  "İkisini karıştıran kişi iki kez üzülür. Önce tahmine göre plan yapar, sonra "
  "gerçek rakam farklı çıkınca plan bozulur.")
T("Kim tahmin yayınlar", "ve neden",
  "Tahmin yayınlayan kurumların işi bu. Banka araştırma birimleri, ekonomistler, "
  "gazeteler. Onlar yanılıyorsa kötü niyetli değiller — iş böyle.")
L("Üç soru", ["Kim söylüyor",
              "Tahmin mi, açıklanan mı",
              "Hangi aya ait"],
  "Bir sayı gördüğünüzde üç soru sorun. Kim söylüyor. Tahmin mi, açıklanan mı. "
  "Ve hangi aya ait.")
I("Üçüncüsü", "en çok atlanan",
  "Üçüncüsü en çok atlanan. Çünkü haber başlıklarında ay adı çoğu zaman yok, "
  "ve okuyan kişi kendi ayını varsayar.")
T("Bu videodaki tek kesin sayı", "Temmuz",
  "Şimdiye kadarki tek kesin sayı Temmuz'a ait: yüzde bir virgül yetmiş sekiz, "
  "üç Ağustos'ta açıklandı. Gerisi henüz yok.")
C("Şimdi pratik kısım", "kendi tablonuz",
  "Şimdi pratik kısım. Kendi takibinizi nasıl kurarsınız.")

# ------------------------------------------ 5. Kendi takibinizi nasıl kurarsınız
T("Altı satır", "defter de olur",
  "İhtiyacınız olan şey altı satır. Bir defter kâğıdı, telefonun not "
  "uygulaması, ya da bir tablo. Biçimi önemli değil; aynı yerde durması önemli.",
  cap="Kendi takibinizi nasıl kurarsınız")
L("Dört sütun", ["Ay", "Açıklanma tarihi", "Aylık yüzde", "Birikimli kat"],
  "Dört sütun yeter. Ay. Açıklanma tarihi. O ayın aylık yüzdesi. Ve o ana "
  "kadarki birikimli kat.")
I("İlk satır hazır", "Temmuz",
  "İlk satırı şimdi yazabilirsiniz. Temmuz, üç Ağustos, yüzde bir virgül yetmiş "
  "sekiz. Birikimli kat da aynı: bir virgül sıfır bir yedi sekiz.")
T("Sonraki beş satır", "ay adı ve tarih",
  "Sonraki beş satıra sadece ay adını ve açıklanma gününü yazın. Rakam hanesi "
  "boş kalsın. O boşluk, işin nerede olduğunu her bakışta gösterir.")
I("Her ayın üçünde", "iki dakika",
  "Her ayın üçünde iki dakikanız yeter. Açıklanan aylık yüzdeyi yazın, kat "
  "olarak çevirin, ve bir önceki birikimli kat ile çarpın.")
T("Aralık'ta ne olur", "hesap zaten bitmiş olur",
  "Aralık ayının rakamı geldiğinde hesabınız zaten bitmiş olur. Son çarpmayı "
  "yapar, yüzdeye çevirir, ve sonucu görürsünüz.")
I("Kaç gün önce", "haberden önce",
  "Bu, haber sitelerinin yazmasından günler önce olur. Çünkü onlar da aynı "
  "açıklamayı bekliyor, ve aynı aritmetiği yapıyor.")
T("Buradaki kazanç", "sürpriz olmaması",
  "Buradaki kazanç para değil, zaman. Ocak ayında kimse size sürpriz yapamaz, "
  "çünkü sayıyı siz zaten biliyorsunuz.")
T("Ve bir kazanç daha", "plan yapabilmek",
  "Bir kazanç daha var. Kasım ayında birikimin nerede olduğunu bilen kişi, Ocak "
  "ayına göre plan yapabilir. Aralık'ta öğrenen kişi yapamaz.")
C("Şimdi sınırlar", "bu hesap neyi söylemez",
  "Şimdi bu hesabın sınırlarını konuşalım. Neyi söylemediği, söylediği kadar "
  "önemli.")

# ------------------------------------------------- 6. Bu hesap neyi söylemez
T("Birinci sınır", "refah payı",
  "Birinci sınır, ve en önemlisi. Bu hesap sadece enflasyon kısmını verir. "
  "Bunun üzerine bazen refah payı denen ek bir artış konur.",
  cap="Bu hesap neyi söylemez")
I("Refah payı", "aritmetik değil karar",
  "Refah payı aritmetikten çıkmaz. Siyasi bir karardır, bütçe görüşmeleriyle "
  "belirlenir, ve olup olmayacağı önceden bilinmez.")
T("Yani sizin sayınız", "taban",
  "Yani sizin hesabınız bir taban verir. Gerçekleşen zam o tabana eşit olabilir, "
  "ya da üzerinde. Altında olmaz.")
T("İkinci sınır", "taban aylık ayrı konu",
  "İkinci sınır. En düşük emekli aylığı için ayrıca bir taban belirlenebilir, "
  "ve o taban yüzdeyle değil, doğrudan rakamla konuşulur.")
I("Üçüncü sınır", "memur başka kural",
  "Üçüncü sınır. Memur maaşı bu kurala tabi değil. Orada toplu sözleşme zammı "
  "ile enflasyon farkı birlikte işler — başka bir hesap.")
T("Dördüncü sınır", "ben rakam vermiyorum",
  "Dördüncüsü benim sınırım. Ocak oranının kaç olacağını söylemiyorum, çünkü "
  "beş ayın rakamı henüz yok.")
T("Sayı veren video", "neyi yapıyor",
  "Şimdi Ocak oranını kesin sayıyla veren bir video görürseniz, o video beş ayı "
  "tahmin etmiş demektir. Tahmin olabilir; ama tahmin olduğunu söylemeli.")
I("Kaynaklar", "TÜİK ve resmî açıklama",
  "Buradaki tek gerçekleşen rakam Türkiye İstatistik Kurumu verisidir. Kalanı "
  "kural ve aritmetik. Açıklamalar her ayın üçünde kurumun sitesinde.")
T("Ve son bir şey", "bu tavsiye değil",
  "Ve son bir şey. Bu bir yatırım ya da malî tavsiye değil. Kendi durumunuz "
  "için resmî kaynağı, ve gerekirse uzmanı esas alın.")
C("Toparlayalım", "elinizde ne kalıyor",
  "Toparlayalım. Elinizde ne kalıyor?")

# --------------------------------------------- 7. Aralık'ta elinizde ne olacak
T("Bugün", "bir satır",
  "Bugün elinizde tek bir satır var. Temmuz, yüzde bir virgül yetmiş sekiz. "
  "Küçük görünüyor, ama altı ayın ilki.",
  cap="Aralık'ta elinizde ne olacak")
T("Eylül'de", "iki satır",
  "Eylül başında ikinci satırınız olacak. Ekim'de üçüncü. Ve her seferinde iki "
  "dakika.")
I("Aralık'ta", "tamamlanmış bir hesap",
  "Aralık ayının ilk günlerinde elinizde tamamlanmış bir hesap olacak. Kimseden "
  "duymadan, kendi defterinizden.")
L("Üç şey", ["Yüzdeleri toplamayın, çarpın",
             "Tahmin ile açıklananı ayırın",
             "Her ayın üçünde iki dakika"],
  "Üç şey aklınızda kalsın. Yüzdeleri toplamayın, çarpın. Tahmin ile açıklanan "
  "rakamı birbirine karıştırmayın. Ve her ayın üçünde iki dakika ayırın.")
T("Neden bu iş değerli", "çünkü bekleyen çok",
  "Bu neden değerli? Çünkü bu ülkede milyonlarca insan aynı sayıyı bekliyor, ve "
  "çok azı onun nasıl oluştuğunu biliyor.")
T("Bilmek", "kontrol değil ama",
  "Bilmek rakamı değiştirmez. Ama bekleyişi değiştirir, ve plan yapmayı mümkün "
  "kılar.")
I("Bir isteğim var", "yorumlara",
  "Bir isteğim var. Kendi tablonuzu kurduysanız, Eylül rakamı geldiğinde "
  "birikimli katınızı yoruma yazın. Toplu görelim.")
T("Bir sonraki video", "memur tarafı",
  "Bir sonraki videoda memur tarafını açacağım. Toplu sözleşme zammı ile "
  "enflasyon farkının birlikte nasıl işlediğini adım adım.")
T("Çünkü orada", "kural gerçekten farklı",
  "Çünkü orada kural gerçekten farklı, ve iki tarafı aynı sanan çok kişi var.")
C("Görüşmek üzere", "her ayın üçünde",
  "Görüşmek üzere. Ve her ayın üçünde, iki dakika.")

# ---------------------------------------------------------------- o short
# Vídeo inteiro por si: abre pelo FATO datado, que é o resultado. Orçamento
# medido para 35,9 s com 6 cenas e 1,80 frases por cena: 306 caracteres
# (aprendizado 373 — medir ANTES de escrever).
SHORT = [
    {"layout": "titulo", "kicker": "Ocak zammı", "sub": "ilk rakam belli oldu",
     "nar": "Ocak zammının ilk rakamı belli oldu bile.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Üç Ağustos", "sub": "yüzde bir virgül yetmiş sekiz",
     "nar": "Üç Ağustos'ta açıklandı: temmuz enflasyonu yüzde bir virgül yetmiş "
            "sekiz.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Altı ayın ilki", "sub": "beş ay daha var",
     "nar": "Bu, altı ayın ilki. Aralık'a kadar beş rakam daha girecek.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Dikkat", "sub": "yüzdeler toplanmaz",
     "nar": "Ve yüzdeler toplanmaz. Çarpılır.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Her ayın üçünde", "sub": "iki dakika",
     "nar": "Her ayın üçünde iki dakika, ve Ocak'ta kimse size sürpriz yapamaz.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Tam hesap", "sub": "kanalda",
     "nar": "Tam hesabı kanaldaki videoda adım adım gösteriyorum.",
     "sem_cap": True},
]

THUMB = {"l1": "%1,78", "l2": "Ocak zammının ilk ayı"}

COPY = """# Ocak zammının altı aylık cebi: mekanizma ve kendi takibiniz

## TITULO
Emekli Zammı Aralık'ta Değil Temmuz'da Başladı: %1,78'in Anlamı

## DESCRICAO
Türkiye İstatistik Kurumu, 3 Ağustos 2026'da açıkladığı verilerde temmuz ayı tüketici fiyat endeksinin aylık %1,78 arttığını bildirdi. Bu sayı haber olarak geçti ve büyük ölçüde unutuldu — oysa Ocak 2027'de SSK ve Bağ-Kur emeklilerine yapılacak zammın hesabına giren ilk rakam tam olarak budur.

Yaygın inanış zammın Aralık'ta belli olduğudur. Aralık'ta belli olan sadece son rakamdır. Zam altı ay boyunca, ayda bir kez, parça parça inşa edilir.

Bu videoda mekanizmanın kendisi var:

Altı aylık cep — SSK ve Bağ-Kur emeklisi yılda iki kez, Ocak ve Temmuz aylarında zam alır, ve ölçüt tahmin değil gerçekleşen enflasyondur. Ocak zammının penceresi Temmuz'da açılır, Aralık'ta kapanır. Şu anda pencerenin sadece ilk ayı dolu. Her ayın rakamı ayın üçünde açıklanır, ve pencereye giren bir sayı geri alınmaz: yüksek bir ay girdiğinde sonraki düşük aylar onu silmez, sadece üstüne eklenir.

Birikimli hesap toplama değil çarpmadır — en sık yapılan hata altı ayın yüzdesini alt alta yazıp toplamaktır, ve bu sonucu her zaman olduğundan küçük çıkarır. İkinci ayın zammı zaten artmış bir fiyatın üzerine biner. Doğru yöntem her ayı kat olarak yazmak, katları birbiriyle çarpmak, ve sonucu yeniden yüzdeye çevirmektir. Telefonun hesap makinesi yeterlidir: altı çarpma, sonunda bir çıkarma.

Tahmin ile açıklanan arasındaki fark — şu anda dolaşan tahminler hesaba girmez; cebe sadece açıklanan rakam girer. Bir sayı gördüğünüzde üç soru: kim söylüyor, tahmin mi açıklanan mı, ve hangi aya ait. Üçüncüsü en çok atlanandır, çünkü haber başlıklarında ay adı çoğu zaman yoktur.

Kendi takibiniz — dört sütun ve altı satır yeter: ay, açıklanma tarihi, aylık yüzde, birikimli kat. İlk satırı bugün yazabilirsiniz. Her ayın üçünde iki dakika, ve Aralık'ın ilk günlerinde hesabınız haber sitelerinden önce tamamlanmış olur.

Ve sınırlar — bu hesap sadece enflasyon kısmını verir; refah payı aritmetikten çıkmaz, siyasi bir karardır. En düşük emekli aylığı için ayrıca taban belirlenebilir. Memur maaşı bu kurala tabi değildir. Ocak oranının kaç olacağı bu videoda söylenmiyor, çünkü beş ayın rakamı henüz yok.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Bir isteğim var: kendi tablonuzu kurduysanız, Eylül rakamı açıklandığında birikimli katınızı buraya yazın — toplu görelim. Ve merak ettiğim bir şey: Ocak zammını daha önce kendiniz mi hesaplıyordunuz, yoksa haberden mi öğreniyordunuz?

## HASHTAGS
#EmekliZammı #TÜİK #SeviyeSeviye

## TAGS
emekli zammı, ssk emekli, bağ-kur, tüik enflasyon, tüfe, ocak zammı, enflasyon farkı, emekli maaşı, birikimli enflasyon, refah payı, memur maaşı, asgari ücret, ekonomi, maaş hesabı, enflasyon hesaplama

## CONFIGURACAO DE STUDIO
- Dil: Türkçe (tr) | Kategori: Eğitim (27)
- Çocuklar için yapılmadı
- Değiştirilmiş veya sentetik içerik beyanı: EVET (ses yapay zekâ ile üretildi)
- Konum: Türkiye | Lisans: Standart YouTube Lisansı
- Video ortası reklamlar: açık (sekiz dakika üzeri)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
Temmuz 2026 tüketici fiyat endeksi verisi (aylık %1,78) Türkiye İstatistik Kurumu'nun 3 Ağustos 2026 tarihli açıklamasına dayanır; aynı rakam NTV, Yeni Şafak ve Kariyer.net tarafından da aynı şekilde aktarılmıştır. SSK ve Bağ-Kur emeklilerinin yılda iki kez, Ocak ve Temmuz aylarında, önceki altı ayın gerçekleşen enflasyonu kadar zam alması yasal kuraldır. Ağustos ayı için anılan yaklaşık %2,2'lik rakam Akbank Ekonomik Araştırmalar'a ait bir TAHMİNDİR ve videoda tahmin olarak belirtilmiştir — hesaba girmez. 20 Ağustos 2026'da derlenmiştir. Yıllık enflasyon oranı bu videoda KULLANILMAMIŞTIR: iki kaynakta birbiriyle tutarsız biçimde geçtiği için dışarıda bırakıldı. Bu video Ocak 2027 zam oranını tahmin etmez, maaş tutarı vaat etmez, refah payı öngörmez ve memur maaşı kuralını kapsamaz. Yatırım veya malî tavsiye değildir; kendi durumunuz için resmî kaynağı esas alın.
"""

SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-004",
    "idioma": "tr",
    "voz": "tr-TR-AhmetNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1C2B33", "c1": "#C0392B", "c2": "#F4B942", "bg": "#FAF6F0"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    import os

    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "seviye-seviye-004.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(CENAS)} cenas no longo, {len(SHORT)} no short -> {destino}")
