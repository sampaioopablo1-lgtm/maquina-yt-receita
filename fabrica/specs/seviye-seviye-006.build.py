#!/usr/bin/env python3
"""Monta a spec seviye-seviye-006.

ALAVANCA ATACADA NESTA RODADA: **A — conversao short -> inscrito**.
Numero de partida do canal: **0,09%** (3 inscritos para ~3.300 views de short,
medido em 25/08/2026). A frota inteira esta em 0,15%; 1 a 3% e o normal.

O QUE DEU CERTO NO CANAL. Os shorts. Medianas de 146,80, 84,25 e 74,43
views/dia com retencao de 39 a 48% — o seviye-seviye tem o segundo melhor
short da frota (mediana 50,76 v/d).

O QUE NAO DEU. Os longos, e nao e pouco: retencao entre 3,84% e 11,81%. Em um
video de 768 segundos, 3,84% sao vinte e nove segundos. As pessoas clicam e
saem. Alem disso o acervo tem cinco longos duplicados de "Asgari ucret"
(13 a 17/08) com zero view — sobra do laco de re-render, ja corrigido.

O QUE VOU MUDAR POR CAUSA DISSO. O dado mais util nao e a media de views: e
QUAIS shorts trouxeram inscrito. Foram dois, e os dois eram do eixo emekli
(734 e 521 views -> 2 inscritos). O short de aluguel fez 337 views e ZERO
inscrito. Ou seja: view nao converte, ASSUNTO converte — e o assunto que
converte e "o numero oficial nao bate com o seu bolso".

Entao a mudanca desta rodada e cirurgica e esta no FECHO do short. Ate agora
ele terminava com pedido generico ("video isine yaradiysa abone ol"). Aqui ele
termina com uma PROMESSA REPETIVEL E DATADA: todo dia tres o TUIK publica, e
neste canal a conta e refeita com a sua composicao de gasto. Isso da ao
espectador um motivo de assinar que sobrevive ao video — que e exatamente o
que falta quando 3.300 views viram 3 inscritos.

O longo repete a mesma promessa no CTA, para as duas pontas medirem a mesma
coisa.

--------------------------------------------------------------------- A PAUTA

Eixo: composicao da inflacao — a media que ninguem vive. Registrado em
`pautas_banco` id 1055.

NUMEROS CONFERIDOS EM DUAS FONTES INSTITUCIONAIS QUE BATEM, e isso importa
porque a primeira passagem de busca trouxe 33,5% de um agregador (Trading
Economics) que NAO bate com nenhuma das duas — numero descartado, nao usado.

  SBB  — Cumhurbaskanligi Strateji ve Butce Baskanligi, pagina de inflacao,
         atualizada em 07/08/2026.
  TCMB — Banco Central, tabela TUFE, linha 07-2026.

  As duas dao, para julho de 2026:
    TUFE mensal ................................. +1,78%
    TUFE anual .................................. +31,75%  (queda de 0,35 pt)

  E o detalhe do SBB que faz a pauta existir:
    Temel Mallar (bens), anual .................. +16,82%
    Hizmet (servicos), anual .................... +39,70%
    -> distancia: 22,88 pontos

  No MESMO mes de julho, em direcoes opostas:
    Temel Mallar, mensal ........................ -0,38%   (CAIU)
    Hizmet, mensal .............................. +3,18%
    Saglik, mensal .............................. +10,74%

  Outros do mesmo comunicado:
    C endeksi (nucleo), mensal +1,80%; anual 29,91%; media 12 meses 30,69%
    Contribuicao anual: Gida 8,94 pt, Ulastirma 5,22 pt, Konut 5,21 pt
    Ulastirma mensal +2,59% (katki 0,44 pt); Gida mensal +1,61% (0,40 pt)
    Yi-UFE julho +1,52%; anual +27,83%

A TESE: nao existe "a" inflacao de trinta e um virgul setenta e cinco. Existem
duas, e elas estao a vinte e dois pontos de distancia. Quem gasta em servicos
— aluguel, transporte, saude, escola, comer fora — vive perto de quarenta.
Quem gasta em bens vive perto de dezessete. O titular e a media ponderada de
uma cesta que quase ninguem tem exatamente.

E POR QUE ISSO E CONSEQUENCIA E NAO CURIOSIDADE: todo reajuste indexado —
aposentadoria, salario minimo, teto de aluguel — e amarrado ao titular. O
proprio canal ja publicou o caso especifico disso no seviye-seviye-005 (teto
de aluguel 31,90% contra despesa de moradia 40,32%). Este video e a LEI GERAL
por tras daquele caso: sequencia, nao repeticao.

SIMILARIDADE. Os quatro pacotes anteriores sao: 002 asgari ucret contra a
linha da fome, 003 menor aposentadoria de 23.552 TL, 004 quando comecou o
reajuste do aposentado, 005 teto de aluguel. Nenhum trata da COMPOSICAO do
indice. Eixo distinto.

O QUE O VIDEO NAO FAZ: nao preve a inflacao dos proximos meses (depende de
dado que ainda nao existe), nao da conselho de investimento, e nao diz que o
TUIK erra — a conta dele e uma media ponderada declarada, e o video mostra
justamente como ela e composta.

ACENTOS. Turco com todos os diacriticos: c, g, i sem ponto, I com ponto, o, s,
u. Este canal ja publicou spec em ASCII e o defeito so aparece no AUDIO.
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


# ------------------------------------------------------- cap 1: iki sayı
T("Yüzde otuz bir yetmiş beş", "temmuz enflasyonu",
  "Temmuz enflasyonu yüzde otuz bir virgül yetmiş beş açıklandı. Bu sayı "
  "senin için doğru olmayabilir, ve nedeni tahmin değil.",
  cap="Tek enflasyon yok")
I("Aynı açıklamada", "iki ayrı sayı",
  "Çünkü aynı açıklamanın içinde iki ayrı enflasyon var, ve aralarında yirmi "
  "iki puandan fazla mesafe bulunuyor.")
I("Birincisi", "mal: %16,82",
  "Birincisi mallar. Temel mallar grubu bir yılda yüzde on altı virgül seksen "
  "iki arttı.")
I("İkincisi", "hizmet: %39,70",
  "İkincisi hizmetler. Hizmet grubu aynı dönemde yüzde otuz dokuz virgül "
  "yetmiş arttı.")
B("Aradaki mesafe", ["Mal", "Hizmet"], [42, 100],
  "On altı virgül seksen iki ve otuz dokuz virgül yetmiş. Arada yirmi iki "
  "virgül seksen sekiz puan var. İkisi de aynı ayın verisi.")
I("Peki otuz bir yetmiş beş", "ağırlıklı ortalama",
  "Manşetteki otuz bir virgül yetmiş beş, bu ikisinin ve diğer grupların "
  "ağırlıklı ortalaması. Bir ortalama.")
I("Sorun ortalamada değil", "sepette",
  "Sorun ortalamanın yanlış olması değil. Sorun şu: o ortalama, belirli bir "
  "harcama sepetine göre hesaplanıyor.")
I("Ve o sepet", "senin sepetin mi",
  "Ve o sepet senin sepetin değilse, manşet sayısı senin enflasyonun değil.")
I("Bu video ne yapacak", "sayıyı ikiye ayıracak",
  "O tek sayıyı şimdi parçalarına ayıracağız, ve sonunda kendi oranını "
  "kendin hesaplayacaksın.")
L("Sırayla", ["Sayılar nereden geliyor",
              "Aynı ay, ters yönler",
              "Kim hangi enflasyonu yaşıyor",
              "Zamlar neden geride kalıyor",
              "Kendi oranını hesapla"],
  "Beş başlık var, ve hiçbiri tahmin içermiyor.")
I("Neyi yapmayacağım", "tahmin yok",
  "Önümüzdeki ayların enflasyonunu tahmin etmeyeceğim. O, henüz var olmayan "
  "veriye bağlı.")

# --------------------------------------------------- cap 2: sayılar nereden
T("Kaynak", "iki resmî kurum",
  "Buradaki her yüzde iki resmî kaynaktan geliyor, ve ikisi birbirini "
  "doğruluyor.",
  cap="Sayılar nereden geliyor")
I("Birinci kaynak", "Strateji ve Bütçe",
  "Birincisi Cumhurbaşkanlığı Strateji ve Bütçe Başkanlığı'nın enflasyon "
  "sayfası. Yedi ağustosta güncellenmiş.")
I("İkinci kaynak", "Merkez Bankası",
  "İkincisi Türkiye Cumhuriyet Merkez Bankası'nın tüketici fiyatları tablosu, "
  "temmuz iki bin yirmi altı satırı.")
I("İkisi de aynı", "%1,78 ve %31,75",
  "İkisi de aynı iki sayıyı veriyor: aylık artış yüzde bir virgül yetmiş "
  "sekiz, yıllık artış yüzde otuz bir virgül yetmiş beş.")
I("Bir uyarı", "üçüncü sayıya dikkat",
  "Aramada bir de üçüncü sayı çıktı: yüzde otuz üç virgül beş. O sayı iki "
  "resmî kaynağın hiçbiriyle uyuşmuyor, ve bu yüzden kullanılmadı.")
I("Kural basit", "iki kaynak tutmalı",
  "Kural şu: bir sayı iki bağımsız resmî kaynakta aynı çıkmıyorsa, o sayıyla "
  "hesap yapılmaz.")
I("Yıllık düştü", "0,35 puan",
  "Yıllık enflasyon bir önceki aya göre sıfır virgül otuz beş puan düştü. "
  "Yani genel eğilim aşağı yönlü.")
I("Ama nasıl düştü", "her yerde değil",
  "Ama düşüş her grupta aynı değil, ve videonun tamamı bu cümlenin üzerine "
  "kurulu.")
I("Çekirdek nedir", "C endeksi",
  "Bir kavram lazım: çekirdek enflasyon. Resmî adı C endeksi. Enerji, gıda, "
  "içecek, tütün ve altını dışarıda bırakır.")
I("Neden dışarıda", "oynak kalemler",
  "Dışarıda bırakır çünkü bu kalemler hava, hasat ve kur yüzünden çok oynak. "
  "Geriye eğilim kalsın diye çıkarılırlar.")
I("Çekirdek kaç", "yıllık %29,91",
  "Çekirdek enflasyon yıllık yüzde yirmi dokuz virgül doksan bir. On iki "
  "aylık ortalaması ise yüzde otuz virgül altmış dokuz.")
I("İşte kritik nokta", "çekirdeğin içi",
  "Ve kritik nokta şu: çekirdeğin kendisi de ikiye ayrılıyor. Temel mallar ve "
  "hizmetler.")
I("Bu ayrım resmî", "kurumun kendi ayrımı",
  "Bu ayrımı ben icat etmiyorum. Kurumun kendi yayınında, kendi başlıklarıyla "
  "duruyor.")
I("Bir şey daha", "manşet de tek değil",
  "Ve burada ikinci bir sürpriz var: aslında manşet sayı da tek değil. Aynı "
  "açıklamada dört farklı enflasyon oranı yayımlanıyor.")
I("Birinci versiyon", "aylık %1,78",
  "Birincisi aylık değişim: bir önceki aya göre yüzde bir virgül yetmiş "
  "sekiz. En kısa pencere bu.")
I("İkinci versiyon", "yıllık %31,75",
  "İkincisi yıllık değişim: geçen yılın aynı ayına göre yüzde otuz bir virgül "
  "yetmiş beş. Haberlerde en çok bu geçiyor.")
I("Üçüncü versiyon", "12 aylık ortalama %31,90",
  "Üçüncüsü on iki aylık ortalamalara göre değişim: yüzde otuz bir virgül "
  "doksan. Kira tavanında kullanılan sayı budur.")
I("Dördüncü versiyon", "aralığa göre %19,86",
  "Dördüncüsü aralık ayına göre değişim: yüzde on dokuz virgül seksen altı. "
  "Yani yıl başından bugüne olan artış.")
B("Dört sayı, tek ay", ["Aralığa göre", "Yıllık", "12 aylık ort."],
  [63, 100, 100],
  "On dokuz virgül seksen altı, otuz bir virgül yetmiş beş, otuz bir virgül "
  "doksan. Üçü de doğru, üçü de farklı soruyu yanıtlıyor.")
I("Neden karışıyor", "yakın çıkınca",
  "Bu ay yıllık ile on iki aylık ortalama neredeyse aynı çıktı, aralarında "
  "sadece sıfır virgül on beş puan var. Yakın olunca insanlar birini "
  "diğerinin yerine kullanıyor.")
I("Sonraki ay tutmaz", "makas açılır",
  "Enflasyon hızlı düşerken ortalama yıllığın üstünde kalır. Yani bu ay "
  "tutan karışıklık, sonraki ay tutmaz.")

# ------------------------------------------------ cap 3: aynı ay, ters yön
T("Temmuz ayında", "iki yön",
  "Şimdi tek bir aya bakalım: temmuz. Aynı ay içinde iki grup ters yönlere "
  "gitti.",
  cap="Aynı ay, ters yönler")
I("Mallar", "aylık -%0,38",
  "Temel mallar grubu fiyatları temmuzda yüzde sıfır virgül otuz sekiz "
  "azaldı. Arttı değil, azaldı.")
I("Hizmetler", "aylık +%3,18",
  "Aynı ay içinde hizmet grubu fiyatları yüzde üç virgül on sekiz yükseldi.")
B("Temmuz, tek ay", ["Mal", "Hizmet"], [12, 100],
  "Bir tarafta eksi sıfır virgül otuz sekiz, diğer tarafta artı üç virgül on "
  "sekiz. Aynı ülke, aynı ay, aynı açıklama.")
I("Manşet ne dedi", "+%1,78",
  "Ve manşet o ay için bir virgül yetmiş sekiz dedi. İki uç arasındaki bir "
  "nokta.")
I("Bir örnek", "sağlık: +%10,74",
  "Tek bir grup örneği: sağlık grubu fiyatları temmuzda yüzde on virgül "
  "yetmiş dört arttı. Bir ayda.")
I("Katkısı", "0,32 puan",
  "Sağlığın o aydaki enflasyona katkısı sıfır virgül otuz iki puan oldu. "
  "Sepetteki ağırlığı küçük olduğu için katkı küçük görünüyor.")
I("Ama sen", "ağırlık senin ağırlığın",
  "Ama ilaç ve muayene senin bütçende küçük bir kalem değilse, o yüzde on "
  "virgül yetmiş dört senin ayında büyük bir kalem.")
I("Ulaştırma", "aylık +%2,59",
  "Ulaştırma temmuzda yüzde iki virgül elli dokuz arttı ve ayın en belirleyici "
  "grubu oldu. Katkısı sıfır virgül kırk dört puan.")
I("Gıda", "aylık +%1,61",
  "Gıda ve alkolsüz içecekler yüzde bir virgül altmış bir arttı, katkısı "
  "sıfır virgül kırk puan.")
I("Toplayınca", "manşet çıkıyor",
  "Bu katkılar toplandığında manşetteki bir virgül yetmiş sekiz çıkıyor. "
  "Hesap şeffaf; tartışma hesapta değil.")
I("Tartışma nerede", "ağırlıklarda",
  "Tartışma ağırlıklarda. Yani hangi kalemin toplam harcamanın yüzde kaçını "
  "oluşturduğunda.")
I("Yıllık katkı, birinci", "gıda: 8,94 puan",
  "Yıllık tarafta en büyük katkı gıdadan geliyor. Tek başına sekiz virgül "
  "doksan dört puan.")
I("İkinci ve üçüncü", "ulaştırma ve konut",
  "Ardından ulaştırma geliyor, beş virgül yirmi iki puanla. Konut ise beş "
  "virgül yirmi bir puanla hemen arkasında.")

# --------------------------------------- cap 4: kim hangi enflasyonu yaşıyor
T("Aynı ülke", "farklı enflasyon",
  "Şimdi asıl soru: aynı ülkede yaşayan iki kişi neden farklı enflasyon "
  "hissediyor.",
  cap="Kim hangi enflasyonu yaşıyor")
I("Cevap tek kelime", "sepet",
  "Cevap tek kelime: sepet. Yani parayı neye harcadığın.")
I("Birinci kişi", "hizmet ağırlıklı",
  "Birinci kişiyi düşün. Kirada oturuyor, işe her gün gidiyor, çocuğu özel "
  "kursa gidiyor, ayda birkaç kez dışarıda yiyor.")
I("Onun sepeti", "hizmete yakın",
  "Bu kişinin harcamasının büyük kısmı hizmet. Yaşadığı enflasyon otuz dokuz "
  "virgül yetmişe yakın.")
I("İkinci kişi", "mal ağırlıklı",
  "İkinci kişi kendi evinde oturuyor, işe yürüyerek gidiyor, alışverişini "
  "marketten yapıyor, dışarıda yemek nadir.")
I("Onun sepeti", "mala yakın",
  "Bu kişinin sepeti mal ağırlıklı. Yaşadığı enflasyon on altı virgül seksen "
  "ikiye yakın.")
B("İki komşu", ["Mal sepeti", "Manşet", "Hizmet sepeti"], [42, 80, 100],
  "İkisi de aynı şehirde, aynı ayda. Biri on yedi civarında, biri kırk "
  "civarında, manşet ise ikisinin arasında.")
I("Kimse yalan söylemiyor", "ikisi de doğru",
  "Burada kimse yalan söylemiyor. İkisi de doğru, çünkü ikisi de farklı "
  "sepetlerin ortalaması.")
I("Neden hizmet daha hızlı", "içinde emek var",
  "Hizmet neden daha hızlı artıyor? Çünkü hizmetin maliyetinin büyük kısmı "
  "emek, ve emek ücreti geriye dönük olarak zamlanıyor.")
I("Mal tarafında", "kur ve stok",
  "Mal tarafında ise kur, stok ve ithalat fiyatı belirleyici. Bunlar daha "
  "hızlı düşebiliyor.")
I("Bir kanıt daha", "Yİ-ÜFE %27,83",
  "Bunun bir kanıtı daha var: üretici fiyatları yıllık yüzde yirmi yedi "
  "virgül seksen üç, yani tüketici enflasyonunun altında.")
I("Ne anlama geliyor", "mal baskısı azalıyor",
  "Üretici tarafındaki baskı azalırken hizmet tarafındaki baskı sürüyor. "
  "Makas bu yüzden açık kalıyor.")
I("Konut örneği", "yıllık %40,32",
  "Konut, su, elektrik ve gaz grubu yıllık yüzde kırk virgül otuz iki arttı. "
  "Bu kanalda bunu daha önce ayrı bir videoda işlemiştik.")

# ------------------------------------------- cap 5: zamlar neden geride kalıyor
T("Zamlar", "manşete bağlı",
  "Şimdi bu farkın neden sadece bir merak konusu olmadığına gelelim.",
  cap="Zamlar neden geride kalıyor")
I("Kural", "endeksleme manşete",
  "Türkiye'de endeksli artışların tamamı manşet sayıya bağlı. Yani ortalamaya.")
I("Emekli maaşı", "manşete endeksli",
  "Emekli maaşı artışı manşete bağlı. Asgari ücret pazarlığı manşete bakıyor.")
I("Kira tavanı", "12 aylık ortalama",
  "Kira artışının üst sınırı on iki aylık ortalamaya bağlı; bu ay yüzde otuz "
  "bir virgül doksan.")
I("Ve konut gideri", "%40,32",
  "Ama konut giderinin kendisi yüzde kırk virgül otuz iki arttı. Sekiz puandan "
  "fazla açık.")
I("Bu bir örnekti", "genel kural bu",
  "O video tek bir kalemin hikâyesiydi. Bu video, o hikâyenin arkasındaki "
  "genel kural.")
I("Kural şu", "ortalamayla ödenir",
  "Kural şu: gelirin ortalamayla artıyor, ama harcaman kendi sepetinle "
  "artıyor.")
I("Sepetin hizmetliyse", "her yıl geriye",
  "Sepetin hizmet ağırlıklıysa, ortalamayla yapılan her zam seni bir miktar "
  "geriye götürür. Küçük görünür, birikir.")
I("Sayıyla", "yaklaşık sekiz puan",
  "Bu ayki verilerle konuşursak: hizmet sepetiyle yaşayan biri için manşet ile "
  "gerçek arasındaki fark yaklaşık sekiz puan.")
I("Bir yıl sonra", "fark büyüyor",
  "Sekiz puanlık fark bir yıl sonra küçük değildir, ve iki yıl üst üste "
  "gelirse hiç değildir.")
I("Ters durum", "mal sepeti kazanır",
  "Tersi de doğru: mal ağırlıklı sepetle yaşayan biri, ortalamayla yapılan "
  "zamda görece kazançlı çıkar.")
I("Bu politika değil", "aritmetik",
  "Bu bir politika tartışması değil. Ortalamayla endeksleme ile bireysel sepet "
  "arasındaki aritmetik fark.")
I("Bu yüzden", "kendi oranın lazım",
  "Ve tam bu yüzden manşeti beklemek yerine kendi oranını bilmen işine yarar.")

# ---------------------------------------------- cap 6: kendi oranını hesapla
T("Kendi oranın", "üç adım",
  "Şimdi kendi enflasyonunu hesaplayalım. Üç adım, ve hepsi bir kâğıtla "
  "yapılır.",
  cap="Kendi oranını hesapla")
I("Birinci adım", "iki kutu",
  "Birinci adım: geçen ayki harcamanı iki kutuya böl. Mal kutusu ve hizmet "
  "kutusu.")
I("Mal kutusu", "market, giyim, eşya",
  "Mal kutusuna market alışverişi, giyim, ev eşyası ve benzeri fiziksel "
  "ürünler girer.")
I("Hizmet kutusu", "kira, ulaşım, sağlık",
  "Hizmet kutusuna kira, ulaşım, sağlık, eğitim, dışarıda yemek, tamir ve "
  "abonelikler girer.")
I("İkinci adım", "oranı bul",
  "İkinci adım: hizmet kutusunun toplam harcamana oranını bul. Diyelim yüzde "
  "altmış.")
I("Üçüncü adım", "ağırlıklı ortalama",
  "Üçüncü adım: hizmet oranını otuz dokuz virgül yetmiş ile, kalan oranı on "
  "altı virgül seksen iki ile çarp ve topla.")
I("Örnek hesap", "%60 hizmet",
  "Örnek: yüzde altmış hizmet, yüzde kırk mal. Sonuç yaklaşık yüzde otuz "
  "virgül altı. Manşetin biraz altında.")
I("İkinci örnek", "%80 hizmet",
  "İkinci örnek: yüzde seksen hizmet, yüzde yirmi mal. Sonuç yaklaşık yüzde "
  "otuz beş virgül dört. Manşetin belirgin üstünde.")
I("Üçüncü örnek", "%30 hizmet",
  "Üçüncü örnek: yüzde otuz hizmet, yüzde yetmiş mal. Sonuç yaklaşık yüzde "
  "yirmi üç virgül altı. Manşetin çok altında.")
I("Aynı ülke", "üç farklı sonuç",
  "Aynı ay, aynı resmî veri, üç farklı insan, üç farklı sonuç. Hiçbiri yanlış "
  "değil.")
I("Bu sayı ne işe yarar", "zam pazarlığında",
  "Bu sayı iki yerde işe yarar. Birincisi: aldığın zammı değerlendirirken "
  "manşetle değil kendi oranınla karşılaştır.")
I("İkincisi", "hangi kalem",
  "İkincisi: hangi kutunun daha hızlı arttığını bildiğinde, bütçede nereye "
  "bakacağını da bilirsin.")
I("Bir uyarı", "bu kaba bir hesap",
  "Bu kaba bir hesap. Kurumun sepetinde yüzlerce alt kalem ve farklı "
  "ağırlıklar var. Ama yönü doğru gösterir.")
I("Neyi tahmin etmiyoruz", "gelecek ay yok",
  "Ve tekrar: burada gelecek ayın enflasyonu yok. O veri henüz açıklanmadı.")
I("Veri ne zaman", "her ayın başında",
  "Yeni veri her ayın başında yayımlanıyor. Temmuz verisi üç ağustosta "
  "çıkmıştı.")
C("Seviye Seviye", "her ay, senin sepetinle",
  "Bugün tek bir şey yap: geçen ayki harcamanı mal ve hizmet diye ikiye böl ve "
  "oranı yaz. Bu kanalda her ay, veri açıklandığı gün, hesabı senin sepetine "
  "göre yeniden yapıyoruz. Kendi oranını takip etmek istiyorsan abone ol.")


# -------------------------------------------------------------------- short
#
# O FECHO E A MUDANCA DESTA RODADA (alavanca A, partida 0,09%).
#
# Os dois shorts que trouxeram inscrito neste canal tratavam de "o numero
# oficial nao bate com o seu bolso". O que fez 337 views e zero inscrito
# tratava de um teto legal. Entao o gancho aqui e a contradicao pessoal, e o
# fecho troca o pedido generico por uma PROMESSA DATADA E REPETIVEL: dia tres,
# todo mes, a conta refeita com a SUA composicao de gasto. Motivo de assinar
# que sobrevive ao video.
SHORT = [
    {"layout": "titulo", "kicker": "Tek enflasyon yok", "sub": "temmuz 2026",
     "nar": "Enflasyon yüzde otuz bir virgül yetmiş beş dendi. O sayı senin "
            "için doğru olmayabilir.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Mallar", "preco": "yıllık %16,82",
     "nar": "Aynı açıklamada mallar yıllık yüzde on altı virgül seksen iki "
            "arttı.", "sem_cap": True},
    {"layout": "item", "kicker": "Hizmetler", "preco": "yıllık %39,70",
     "nar": "Hizmetler ise yüzde otuz dokuz virgül yetmiş. Arada yirmi iki "
            "puandan fazla var.", "sem_cap": True},
    {"layout": "item", "kicker": "Sen hangisisin", "preco": "sepetine bakar",
     "nar": "Kira ve ulaşım ağırlıklıysan kırka yakınsın, market ağırlıklıysan "
            "on yediye.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Her ayın üçünde", "sub": "senin sepetinle",
     "nar": "Veri her ayın üçünde çıkıyor. O gün hesabı senin sepetine göre "
            "yeniden yapıyoruz.",
     "sem_cap": True},
]

COPY = """# Tek enflasyon yok: mal %16,82, hizmet %39,70

## TITULO
Tek Enflasyon Yok: Mal Yüzde 16,82, Hizmet Yüzde 39,70 — Seninki Hangisi?

## DESCRICAO
Temmuz 2026 enflasyonu manşetlerde yüzde 31,75 olarak geçti. Ama aynı açıklamanın içinde iki ayrı enflasyon var: temel mallar grubu bir yılda yüzde 16,82 arttı, hizmet grubu ise yüzde 39,70. Aradaki mesafe 22,88 puan. Manşetteki 31,75 bu ikisinin ve diğer grupların ağırlıklı ortalaması — yani belirli bir harcama sepetine göre hesaplanan bir ortalama. O sepet sizin sepetiniz değilse, manşet sayısı sizin enflasyonunuz değil.

SAYILAR VE KAYNAK

Bu videodaki her yüzde iki resmî kaynakta aynı çıkıyor: Cumhurbaşkanlığı Strateji ve Bütçe Başkanlığı'nın enflasyon sayfası (7 Ağustos 2026'da güncellendi) ve TCMB'nin tüketici fiyatları tablosu (07-2026 satırı). İkisi de temmuz için aylık %1,78 ve yıllık %31,75 veriyor. Yıllık enflasyon bir önceki aya göre 0,35 puan geriledi.

BİR UYARI: aramada üçüncü bir sayı da çıkıyor, yüzde 33,5. Bu sayı iki resmî kaynağın hiçbiriyle uyuşmuyor ve bu videoda kullanılmadı. Kural basit — bir sayı iki bağımsız resmî kaynakta aynı çıkmıyorsa, o sayıyla hesap yapılmaz.

AYNI AY, TERS YÖNLER

En çarpıcı kısım tek bir ayda görünüyor. Temmuzda temel mallar grubu fiyatları yüzde 0,38 AZALDI; aynı ay hizmet grubu fiyatları yüzde 3,18 YÜKSELDİ. Manşet ise o ay için 1,78 dedi — iki ucun arasında bir nokta. Tek bir grup örneği: sağlık grubu fiyatları temmuzda yüzde 10,74 arttı, enflasyona katkısı 0,32 puan oldu. Katkının küçük görünmesinin sebebi sepetteki ağırlığın küçük olması; sizin bütçenizde ilaç ve muayene küçük bir kalem değilse, o 10,74 sizin ayınızda büyük bir kalemdir.

Ayın diğer belirleyicileri: ulaştırma %2,59 (katkı 0,44 puan), gıda ve alkolsüz içecekler %1,61 (katkı 0,40 puan). Yıllık tarafta en büyük üç katkı: gıda 8,94 puan, ulaştırma 5,22 puan, konut 5,21 puan. Çekirdek enflasyon (C endeksi — enerji, gıda, içecek, tütün ve altın hariç) yıllık %29,91, on iki aylık ortalaması %30,69. Üretici fiyatları (Yİ-ÜFE) yıllık %27,83, yani tüketici enflasyonunun altında: mal tarafındaki baskı azalırken hizmet tarafındaki baskı sürüyor.

ZAMLAR NEDEN GERİDE KALIYOR

Endeksli artışların tamamı manşet sayıya bağlı. Emekli maaşı artışı, asgari ücret pazarlığı, kira tavanı — hepsi ortalamaya bakıyor. Kira tavanı bu ay on iki aylık ortalamayla %31,90 iken konut, su, elektrik ve gaz grubunun yıllık artışı %40,32; bu kanalda o farkı ayrı bir videoda işlemiştik. Bu video o hikâyenin arkasındaki genel kural: geliriniz ortalamayla artıyor, harcamanız kendi sepetinizle artıyor. Sepetiniz hizmet ağırlıklıysa ortalamayla yapılan her zam sizi bir miktar geriye götürür — küçük görünür, birikir. Tersi de doğru: mal ağırlıklı sepetle yaşayan biri aynı zamda görece kazançlı çıkar. Bu bir politika tartışması değil, ortalamayla endeksleme ile bireysel sepet arasındaki aritmetik fark.

KENDİ ORANINIZ (üç adım)

1) Geçen ayki harcamanızı iki kutuya bölün: MAL (market, giyim, ev eşyası) ve HİZMET (kira, ulaşım, sağlık, eğitim, dışarıda yemek, tamir, abonelikler). 2) Hizmet kutusunun toplam harcamanıza oranını bulun. 3) Hizmet oranını 39,70 ile, kalan oranı 16,82 ile çarpıp toplayın.

Üç örnek: %60 hizmet + %40 mal ≈ %30,6 (manşetin biraz altında). %80 hizmet + %20 mal ≈ %35,4 (manşetin belirgin üstünde). %30 hizmet + %70 mal ≈ %23,6 (manşetin çok altında). Aynı ay, aynı resmî veri, üç farklı sonuç — hiçbiri yanlış değil.

Bu kaba bir hesaptır: kurumun sepetinde yüzlerce alt kalem ve farklı ağırlıklar var. Ama yönü doğru gösterir, ve aldığınız zammı manşetle değil kendi oranınızla karşılaştırmanızı sağlar.

BU VİDEODA OLMAYANLAR: önümüzdeki ayların enflasyon tahmini yok — o, henüz açıklanmamış veriye bağlı. Yatırım tavsiyesi yok. Ve kurumun hesabının yanlış olduğu iddiası yok: hesap ilan edilmiş bir ağırlıklı ortalamadır, video tam olarak o ortalamanın nasıl oluştuğunu gösteriyor.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Üç adımı uygulayıp kendi oranınızı bulduysanız yorumlara yazın: hizmet oranınız yüzde kaç çıktı ve sonuç manşetin altında mı üstünde mi kaldı? Özellikle merak ettiğim, yüzde 80'in üzerinde hizmet ağırlığı olan bütçeler — kira ve ulaşımın birlikte baskın olduğu durumlar.

## HASHTAGS
#Enflasyon #TÜİK #SeviyeSeviye

## TAGS
enflasyon temmuz 2026, tufe, tuik enflasyon, hizmet enflasyonu, mal enflasyonu, cekirdek enflasyon, c endeksi, kendi enflasyonun, kisisel enflasyon hesaplama, emekli zammi, asgari ucret, kira tavani, butce, kisisel finans, merkez bankasi

## CONFIGURACOES DO STUDIO
- Idioma: Turkce (tr) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Turquia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Todos os percentuais vem dos dados de julho de 2026 e foram conferidos em DUAS fontes institucionais que batem entre si: a pagina de inflacao da Cumhurbaskanligi Strateji ve Butce Baskanligi (atualizada em 07/08/2026) e a tabela de precos ao consumidor do TCMB (linha 07-2026). Ambas: TUFE mensal +1,78%, anual +31,75% (queda de 0,35 ponto). Do detalhamento: temel mallar (bens) anual +16,82% e hizmet (servicos) anual +39,70%, distancia de 22,88 pontos; no mes de julho os bens caIram 0,38% enquanto os servicos subiram 3,18%; saude +10,74% no mes com katki de 0,32 ponto; ulastirma +2,59% (0,44 ponto) e gida +1,61% (0,40 ponto); contribuicao anual gida 8,94, ulastirma 5,22, konut 5,21 pontos; nucleo (C endeksi) anual 29,91% e media de doze meses 30,69%; Yi-UFE anual 27,83%. Os valores de konut +40,32% e teto de aluguel 31,90% vem do mesmo instituto e ja haviam sido conferidos para o pacote seviye-seviye-005. UM NUMERO FOI DESCARTADO DE PROPOSITO: um agregador privado indicava 33,5% de inflacao anual, valor que nao bate com nenhuma das duas fontes institucionais e por isso nao aparece no video. Os tres exemplos de calculo (30,6%, 35,4% e 23,6%) sao medias ponderadas simples entre 16,82% e 39,70%, apresentadas explicitamente como conta aproximada. Este material e educativo sobre orcamento domestico: nao e aconselhamento de investimento, nao preve a inflacao dos meses seguintes e nao afirma que o calculo oficial esteja errado.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seviye-seviye-006.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-006",
    "idioma": "tr",
    "voz": "tr-TR-AhmetNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1A2430", "c1": "#C0392B", "c2": "#2E86A8",
               "bg": "#F5F2EE"},
    "thumb": {"l1": "%16,82", "l2": "yoksa %39,70"},
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
    grava(SPEC, "fabrica/specs/seviye-seviye-006.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
