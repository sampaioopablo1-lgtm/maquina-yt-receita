#!/usr/bin/env python3
"""Monta a spec seviye-seviye-003.

EIXO. Primeira medicao completa do nicho (18/08/2026, 27 videos de 90 dias,
gravados em pautas_banco): mediana 1.090,3 views/dia, e TODOS os quatro
outliers >=3x sao sobre APOSENTADORIA — "En Düşük Emekli Aylığına Zam Farkı"
(9.754,6 v/d), "Emekliye Seyyanen Zam Refah Payı" (4.003,5), "Seyyanen Zam
İçin Karar Zamanı" (3.483,1). O canal so publicou asgari ucret; emekli e o
eixo dominante e intocado. Achado negativo que tambem vale dinheiro: o
cluster "salario na Alemanha" esta MORTO (18 a 28 v/d) — nao tocar.

Os outliers sao noticiario de kulis ("vai sair? quanto?"). O canal nao
compete com CNN Turk em velocidade; compete em CONTA. Estrutura copiada do
topo (o numero do piso no titulo) com o giro da casa: a matematica do
reajuste que o noticiario nao faz.

NUMEROS, dois blocos institucionais (buscas de 18/08/2026):

  Reajuste de julho/2026 (uzmanpara/Milliyet, CNN Turk, Hurriyet)
    zam de +17,76% = enflasyon farkı de 6 meses (mecanica legal, nao bondade)
    piso (en dusuk emekli ayligi): 20.000 -> 23.552 TL
    5,1 milhoes de aposentados no piso (Cumhuriyet, subindo de 4,9)
    media oficial citada por Cevdet Yilmaz: 35.759 TL
    seyyanen (valor fixo p/ todos): so KULIS de 10-25 bin, nada decidido

  TURK-IS julho/2026 (turkis.org.tr, a propria instituicao)
    aclik siniri (familia de 4): 36.939,87 TL
    yoksulluk siniri: 120.325,30 TL
    custo de vida de UM adulto solteiro: 47.758,39 TL
    mutfak enflasyonu: +3,30% no mes; comida +22,54% em 7 meses

A tese sai da mecanica: o reajuste de julho paga a inflacao PASSADA — os
precos ja subiram quando o dinheiro chega. O piso novo (23.552) e 64% do
limiar da FOME de uma familia, e nem paga o custo de vida de um adulto
sozinho (47.758). E o reajuste percentual ALARGA a distancia em liras entre
o piso e a media — a conta que o video ensina o espectador a fazer com o
proprio kok maas.

VOZ. tr-TR-AhmetNeural (15,82 chars/s, P=1,339) — calibracao de PRODUCAO,
n=52. Voz lenta: ~8,2 mil chars bastam para 13 min.
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
T("İki sayı", "aynı ayda açıklandı",
  "Yirmi üç bin beş yüz elli iki lira. Ve otuz altı bin dokuz yüz kırk lira. "
  "İkisi de temmuzda açıklandı. Aradaki boşluk, bu videonun konusu.",
  cap="Temmuzun iki sayısı")
I("Birinci sayı", "en düşük emekli aylığı",
  "Birinci sayı, zam sonrası en düşük emekli aylığı. Yirmi üç bin beş yüz "
  "elli iki lira.")
I("İkinci sayı", "dört kişilik açlık sınırı",
  "İkinci sayı, Türk-İş'in ölçtüğü açlık sınırı. Dört kişilik bir ailenin "
  "sadece mutfak masrafı: yaklaşık otuz yedi bin lira.")
B("Yan yana", ["Taban aylık", "Açlık sınırı"], [64, 100],
  "Yan yana koyunca taban aylık, açlık sınırının yüzde altmış dördü. Zam "
  "geldi, boşluk yerinde duruyor.")
I("Bu video ne değil", "öfke değil, hesap",
  "Bu video kızgınlık videosu değil. Zammın nasıl hesaplandığını, neyi "
  "ödediğini ve neyi ödemediğini rakamla göstereceğiz.")
I("Bu kanalda daha önce", "asgari ücreti saymıştık",
  "Bu kanalda asgari ücretin açlık sınırıyla yarışını zaten saymıştık. Bugün "
  "sıra emeklide. Çünkü temmuz zammı geldi ve herkes orana bakıyor.")
I("Oysa oran", "tek başına bir şey demez",
  "Oysa oran tek başına bir şey söylemez. Yüzde on yedi neyin yüzde on "
  "yedisi? Ve geldiğinde fiyatlar neredeydi? Cevaplar sırayla.")
T("Yol haritası", "beş adım",
  "Önce zammın matematiği. Sonra zammın ödemediği şey. Sonra tabanda kaç "
  "kişi var. Sonra seyyanen tartışması. En sonda kendi zammını hesaplayan "
  "tablo.")
L("Kaynaklar", ["SGK zam oranı", "Türk-İş sınırları", "Resmî ortalama"],
  "Her sayının sahibi ve tarihi var. Zam oranı resmî. Sınırlar Türk-İş'in. "
  "Ortalama, hükümetin kendi açıklaması. Tahmin yok.")
I("Bir uyarı", "kulise itibar yok",
  "Ve bir uyarı. Kuliste dolaşan rakamları haber gibi anlatmayacağız. İddia "
  "neyse iddia diye söyleyeceğiz.")
I("Başlıyoruz", "zam nereden çıktı",
  "Başlayalım. Yüzde on yedi virgül yetmiş altı nereden çıktı?")

# ------------------------------------------------------------------- cap 2
T("Zam bir hediye değil", "bir formül",
  "Temmuz zammı bir müjde gibi sunuldu. Ama zam bir hediye değil. Kanunla "
  "yazılmış bir formülün sonucu.",
  cap="Zammın matematiği")
I("Formül", "altı aylık enflasyon",
  "Formül şu: son altı ayın enflasyonu neyse, emekli aylığı o oranda artar. "
  "Bu kez sonuç yüzde on yedi virgül yetmiş altı çıktı.")
I("Tabanda", "20.000'den 23.552'ye",
  "Tabanda hesap basit. Yirmi bin lira, yüzde on yedi virgül yetmiş altı "
  "artınca yirmi üç bin beş yüz elli iki lira oldu.")
I("Fark", "aylık 3.552 lira",
  "Aylık fark üç bin beş yüz elli iki lira. Bu sayıyı aklında tut, birazdan "
  "mutfak masrafıyla karşılaştıracağız.")
I("İki kavram", "kök maaş ve ele geçen",
  "Burada iki kavramı ayır. Kök maaş, sistemdeki çıplak rakam. Ele geçen, "
  "kesintiler ve eklemeler sonrası cebe giren. Zam oranı KÖK maaşa işler.")
I("Yılda iki kez", "ocak ve temmuz",
  "Ve bu formül yılda iki kez çalışır. Ocakta bir, temmuzda bir. Her "
  "seferinde bir önceki altı ayın enflasyonu kadar.")
I("Kapsam", "SSK ve Bağ-Kur",
  "Bir not: bu formül SSK ve Bağ-Kur emeklisi için. Memur emeklisinin "
  "hesabında toplu sözleşme payı da var; o ayrı bir video konusu.")
I("Yani zam", "geçmişin faturası",
  "Dikkat et: formül geleceğe değil, geçmişe bakıyor. Zam, zaten yaşanmış "
  "altı ayın fiyat artışını ödüyor.")
I("Sıra hep aynı", "önce fiyat, sonra maaş",
  "Sıralama hep aynı. Önce fiyatlar yükseliyor. Altı ay sonra maaş onları "
  "takip ediyor. Aradaki altı ayı emekli cebinden ödüyor.")
I("Buna koşu bandı denir", "yerinde koşmak",
  "Buna koşu bandı ekonomisi diyebilirsin. Hızlanırsın, terlersin, ama "
  "bant da hızlanır. Yerinde kalırsın.")
T("Köprü", "peki bant ne kadar hızlı",
  "Peki bant gerçekte ne kadar hızlı dönüyor? Mutfağa bakalım:")

# ------------------------------------------------------------------- cap 3
T("Mutfak", "zamdan hızlı",
  "Türk-İş her ay aynı sepeti fiyatlıyor. Aynı gıdalar, aynı miktar, her "
  "ay. Bu yüzden karşılaştırması sağlam.",
  cap="Zammın ödemediği şey")
I("Yedi ayda", "gıda yüzde 22,54",
  "Sonuç: gıda fiyatları yedi ayda yüzde yirmi iki virgül elli dört arttı.")
I("Zam ise", "yüzde 17,76",
  "Emekli zammı ise yüzde on yedi virgül yetmiş altı. Mutfak, zammın "
  "önünde koşuyor.")
B("Yedi ayın yarışı", ["Gıda artışı", "Emekli zammı"], [100, 79],
  "Yani zam yattığı gün bile mutfak alışverişi, ocak ayına göre daha "
  "pahalıydı. Fark kapanmadı, sadece küçüldü.")
I("Sepette ne var", "sadece gıda",
  "Türk-İş sepetinde ne olduğunu da söyleyelim: sadece gıda. Dört kişinin "
  "sağlıklı beslenme maliyeti. Kira yok, fatura yok, ulaşım yok.")
I("Yani açlık sınırı", "iyimser bir alt çizgi",
  "Yani açlık sınırı aslında iyimser bir alt çizgidir. Gerçek ay sonu "
  "hesabı, üstüne kira ve faturayla başlar.")
I("Ve bekleme", "altı ay cepten",
  "Bir de zamanlama var. Ocaktaki fiyat artışını temmuzdaki maaş ödedi. O "
  "altı ay boyunca fark, emeklinin birikiminden ya da borcundan çıktı.")
I("Ve tek ayda", "yüzde 3,30",
  "Üstelik bant durmuyor. Sadece temmuz ayında mutfak yüzde üç virgül "
  "otuz daha pahalandı.")
I("3.552'nin ömrü", "birkaç pazar",
  "Şimdi o üç bin beş yüz elli iki liralık farkı hatırla. Dört kişilik "
  "mutfağın tek aylık artışı bile onun büyük kısmını yutuyor.")
I("Bu yüzden", "zam günü rahatlama kısa",
  "Bu yüzden zam günü hissedilen rahatlama birkaç hafta sürüyor. Sayılar "
  "duyguyu doğruluyor; kuruntu değil.")
T("Köprü", "tabanda kimler var",
  "Buraya kadar oran konuştuk. Şimdi insan sayısı konuşalım:")

# ------------------------------------------------------------------- cap 4
T("Taban bir istisna değil", "beş milyondan fazla kişi",
  "En düşük aylık bir istisna sanılır. Değil. Beş virgül bir milyon emekli "
  "tam olarak bu taban aylığı alıyor.",
  cap="Tabanda kaç kişi var")
I("Ve sayı büyüyor", "4,9'dan 5,1 milyona",
  "Ve bu sayı büyüyor. Bir önceki dönemde dört virgül dokuz milyondu. "
  "Şimdi beş virgül bir.")
I("Neden büyüyor", "düşük kök maaşlar tabana yapışıyor",
  "Neden? Çünkü kök maaşı düşük olan herkes, zam yüzde kaç olursa olsun "
  "tabana yapışıyor. Taban bir ağ gibi; her yıl daha çok kişiyi tutuyor.")
I("Resmî ortalama", "35.759 lira",
  "Hükümetin açıkladığı ortalama emekli aylığı ise otuz beş bin yedi yüz "
  "elli dokuz lira.")
B("Taban ve ortalama", ["Taban", "Ortalama", "Bekâr geçim"], [49, 75, 100],
  "Ama ortalama bile Türk-İş'in tek kişilik geçim maliyetinin altında. "
  "Bekâr bir insanın aylık yaşama maliyeti: kırk yedi bin yedi yüz elli "
  "sekiz lira.")
I("Tek kişi bile", "ortalamayla geçinemiyor",
  "Yani sadece taban değil. Ortalama emekli aylığı bile tek kişilik geçim "
  "sınırının belirgin altında.")
I("Yüzde 64 nereden", "bölmeyi göster",
  "Yüzde altmış dördün hesabı basit. Taban aylığı açlık sınırına böl. "
  "Sonuç: taban, ailenin sadece mutfağının üçte ikisini karşılıyor.")
I("İki emekli bir evde", "yine dar",
  "En iyi senaryoyu da kuralım: aynı evde iki taban emekli. İkisinin "
  "toplamı kırk yedi bin lira eder. Mutfağı geçer, ama tek kişilik insanca "
  "geçim sınırının hâlâ altındadır.")
I("Yoksulluk sınırı", "120 binin üstünde",
  "Dört kişilik ailenin insanca geçim sınırı ise yüz yirmi bin lirayı "
  "geçti. O sayıyı tabana bölmek istemiyorum bile; sen böl.")
T("Köprü", "peki çözüm seyyanen mi",
  "Bu tabloya karşı en çok konuşulan öneri seyyanen zam. Ona da hesapla "
  "bakalım:")

# ------------------------------------------------------------------- cap 5
T("Seyyanen ne demek", "herkese eşit lira",
  "Seyyanen zam, herkese aynı LİRA tutarının verilmesi demek. Yüzde değil. "
  "Tabana da tepeye de aynı rakam.",
  cap="Seyyanen tartışmasının matematiği")
I("Kuliste dolaşan", "10 ile 25 bin arası iddialar",
  "Meclis kulislerinde on bin ile yirmi beş bin lira arasında rakamlar "
  "dolaşıyor. Bunlar iddia. Karar yok, kanun yok, tarih yok.")
I("Peki fark ne", "yüzde tabanı geride bırakır",
  "Farkı gösterelim. Yüzde zammı herkese aynı ORAN verir. Ama oran, düşük "
  "maaşta az lira, yüksek maaşta çok lira eder.")
I("Somut örnek", "aynı yüzde, farklı lira",
  "Aynı yüzde on yedi virgül yetmiş altı: tabanda üç bin beş yüz lira "
  "eder. Elli bin alan birinde ise sekiz bin sekiz yüz lira eder.")
B("Aynı zam, iki cüzdan", ["Tabanın farkı", "Yüksek maaşın farkı"], [40, 100],
  "Yani her yüzde zammında, liralar cinsinden makas biraz daha açılır. "
  "Taban her yıl ortalamadan biraz daha uzaklaşır.")
I("Seyyanen bunu tersine çevirir", "makası kapatır",
  "Seyyanen tam tersini yapar: tabana oransal olarak en büyük desteği "
  "verir, makası kapatır. Matematiği bu.")
I("Daha önce oldu mu", "bir kez: 2023",
  "Seyyanen daha önce bir kez uygulandı. İki bin yirmi üç temmuzunda, "
  "herkese beş bin lira eklendi. Yani teknik olarak imkânsız değil.")
I("Neden tartışmalı", "bütçeye maliyeti",
  "Neden her seferinde tartışma çıkıyor? Çünkü milyonlarca kişiye aynı "
  "lirayı vermek bütçede kalıcı bir kalem açıyor. Karar siyasi, matematik "
  "değil.")
I("Ama unutma", "hâlâ karar değil",
  "Ama bugün itibarıyla bu bir tartışma. Videonun yayınlandığı gün "
  "kanunlaşmış bir seyyanen zam yok. Duyarsan önce tarihe bak.")
T("Köprü", "kendi sayına dön",
  "Ve büyük tartışma ne olursa olsun, senin cebini senin sayıların "
  "belirliyor. Onları tabloya dökelim:")

# ------------------------------------------------------------------- cap 6
T("Altı satır", "kendi zam hesabın",
  "Altı satırlık bir tablo. Kağıt da olur, telefon notu da, Excel de.",
  cap="Kendi hesabını yap")
L("Altı satır", ["Kök maaşın", "Zam oranı", "Yeni maaş",
                 "Kira ve aidat", "Mutfak", "Kalan"],
  "Kök maaşın. Zam oranı. Yeni maaş. Kiran ve aidatın. Mutfak masrafın. "
  "Ve kalan.")
I("Satır bir", "kök maaş, ele geçen değil",
  "Satır bir: kök maaş. Eline geçen değil, sistemdeki çıplak maaşın. Zam "
  "ona uygulanıyor; ikisini karıştırınca hesap hep yanlış çıkar.")
I("Satır iki", "oranı kaynağından al",
  "Satır iki: zam oranı. Onu haberden değil, resmî enflasyon duyurusundan "
  "al. Altı aylık toplamı yaz; aylıkları toplama, bileşik hesap farklı "
  "çıkar.")
I("Satır üç", "çarp ve yuvarlama",
  "Satır üç: yeni maaş. Kök maaşını oranla çarp. Kuruşu atma; yıl sonunda "
  "kuruşlar yüzlerce lira eder.")
I("Satır dört ve beş", "kendi fiyatların",
  "Kira ve mutfak satırlarına ülke ortalaması yazma. Kendi kiranı, kendi "
  "pazar fişini yaz. Ortalamada kimse oturmuyor.")
I("Kalan satırı", "cevap orada",
  "Kalan satırı cevabın kendisi. Zam öncesi kalanla zam sonrası kalanı "
  "karşılaştır. Rahatlama gerçek mi, kaç lira, orada görünür.")
I("Tarih at", "tablo eskir",
  "Ve tabloya tarih at. Zam yılda iki kez, fiyat her ay değişiyor. "
  "Tarihsiz tablo, altı ay sonra seni yanıltır.")
I("Tek uğraş", "ayda beş dakika",
  "Bütün bunlar ayda beş dakika. Bir kere kurunca, her ay sadece iki "
  "satırı güncelliyorsun.")
T("Köprü", "kapanış",
  "Kapanmadan, akılda kalması gereken üç şey:")

# ------------------------------------------------------------------- cap 7
T("Üç cümle", "götürülecek olanlar",
  "Üç cümle. Üçü de rakamla desteklendi.",
  cap="Akılda kalacak üç şey")
I("Bir", "zam geçmişi ödüyor",
  "Bir: zam bir formül ve geçmişi ödüyor. Aradaki altı ayın farkı cebinden "
  "çıkıyor.")
I("İki", "taban açlık sınırının altında",
  "İki: yeni taban, dört kişilik açlık sınırının yüzde altmış dördü. Ve o "
  "tabanda beş milyondan fazla insan var.")
I("Üç", "yüzde zam makası açar",
  "Üç: yüzde zam her turda liralar makasını biraz daha açar. Seyyanen onu "
  "kapatır ama bugün sadece bir tartışma.")
L("Videonun özeti", ["+%17,76 = geçmiş enflasyon", "Taban: 23.552",
                     "Açlık sınırı: 36.940", "Tabanda 5,1 milyon kişi",
                     "Tablonu kur"],
  "Özet ekranda. İstersen durdur, kendi tablonu bu sayılarla karşılaştır.")
I("En sık hata", "ele geçenle çarpmak",
  "Bu hesapta en sık hata: zam oranını ele geçen maaşla çarpmak. Oran kök "
  "maaşa uygulanır; ikisini karıştıran herkes zammı olduğundan büyük görür.")
I("Yapılmayacak şey", "kulis rakamıyla plan",
  "Bir şey yapma: kulis rakamıyla bütçe planlama. Kanunlaşmamış zam, "
  "gelmemiş paradır.")
I("Tek şey yapacaksan", "kalan satırını hesapla",
  "Tek şey yapacaksan, kalan satırını hesapla. Zam öncesi ve sonrası. O "
  "tek sayı, bütün haberlerden daha dürüst.")
C("Seviye Seviye", "sayıyı say, habere değil",
  "Tablonu kurduysan, kalan satırın kaç çıktı? Yoruma yaz. Sayıları bir "
  "sonraki video için topluyorum.")
C("Seviye Seviye", "sayıyı say, habere değil",
  "Ve aynı hesabı hangi maaş için istersin? Memur mu, asgari ücret mi? En "
  "çok istenen önce gelir.")

SHORT = [
    {"layout": "titulo", "kicker": "23.552 TL", "sub": "yeni taban aylık",
     "nar": "Zam geldi: en düşük emekli aylığı yirmi üç bin beş yüz elli iki "
            "lira oldu. Şimdi ikinci sayıya bak.", "sem_cap": True},
    {"layout": "item", "kicker": "Açlık sınırı", "preco": "36.940 TL",
     "nar": "Ailenin sadece mutfak masrafı: otuz yedi bin lira. Taban, bunun "
            "yüzde altmış dördü.", "sem_cap": True},
    {"layout": "item", "kicker": "Ve zam", "preco": "geçmişi ödüyor",
     "nar": "O yüzde on yedi virgül yetmiş altı, gelecek için değil. Zaten "
            "yaşanmış altı ayın faturası.", "sem_cap": True},
    {"layout": "item", "kicker": "Tabanda", "preco": "5,1 milyon kişi",
     "nar": "Ve bu taban bir istisna değil. Beş virgül bir milyon emekli tam "
            "olarak bu aylığı alıyor.", "sem_cap": True},
    {"layout": "cta", "kicker": "Seviye Seviye", "sub": "zammın tam matematiği",
     "nar": "Zammın tam matematiği ve kendi hesabını yapacağın tablo, uzun "
            "videoda. Şimdi izle.", "sem_cap": True},
]


def _copy_existente():
    """Le a copy do .json ao lado, se ja existir com conteudo real."""
    import os
    alvo = "fabrica/specs/seviye-seviye-003.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500:
            return c
    return "gerado a partir dos capitulos reais apos o render"


SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-003",
    "idioma": "tr",
    "voz": "tr-TR-AhmetNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1C2B33", "c1": "#C0392B", "c2": "#F4B942",
               "bg": "#FAF6F0"},
    "thumb": {"l1": "23.552 TL", "l2": "zammın matematiği"},
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    p = "fabrica/specs/seviye-seviye-003.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ensaio import duracao_estimada
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
