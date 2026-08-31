#!/usr/bin/env python3
"""Monta a spec seviye-seviye-008.

ALAVANCA ATACADA: **A — conversao (FORMA)**, com um numero de partida que
aparece pela SEGUNDA vez, agora neste canal.

NUMERO DE PARTIDA, medido em 31/08/2026 sobre o seviye-seviye-007 (4,1 dias):

    seviye-seviye-007 LONGO  ...  34 views =  8,3 views/dia
    seviye-seviye-007 SHORT  ... 147 views = 35,7 views/dia
    outros longos do canal ....  4,0 | 3,2 | 2,7 | 2,2 | 1,9 views/dia
    outros shorts do canal .... 258,6 | 114,7 | 60,5 | 57,6 | 29,5 views/dia

O QUE DEU CERTO: o 007 e o UNICO pacote de forma ESCOLHA que este canal
publicou, e o longo dele e o melhor longo do canal — mais que o dobro do
segundo colocado.

O QUE NAO DEU: o short do 007 e o PIOR short do canal. Os shorts de numero
IMPOSTO (asgari ucret, emekli zammi, kira artisi, enflasyon) puxam de tres a
sete vezes o alcance dele.

E ISSO E O MESMO PADRAO DO kolejny-poziom-012, medido no mesmo dia, noutra
lingua e noutro nicho: o pacote de escolha sobe o longo e derruba o short.
Dois canais, mesma direcao (aprendizado 532).

O QUE MUDO POR CAUSA DISSO: nada na forma. E de proposito. Se eu comecar a
consertar o alcance do short agora, deixo de saber se o padrao e real, e ele e
o candidato mais forte que a maquina tem para reescrever a alavanca A — de
"o short precisa de ALCANCE" para "o short precisa QUALIFICAR". O 008 repete a
forma num eixo novo e o experimento 25 fecha com tres pacotes em vez de dois.

RESSALVA HONESTA: a comparacao mistura idades de medicao (31/08 contra 26/08) e
views/dia de video jovem carrega o pico de lancamento. Direcao sugestiva, nao
medida.

E o que eu NAO consigo medir: segundos vistos e inscritos por video. Falta o
escopo `yt-analytics.readonly` (aprendizados 522 e 528). As linhas do 007 em
`metricas` tem retencao ZERO por AUSENCIA DE FONTE.

--------------------------------------------------------------- DIMENSIONAMENTO

`v_maquina_licoes` da `liberado` (12-15 min). Alavanca B manda ir ao PISO:
**720 segundos**. Nove capitulos. A RESPOSTA — a subtracao e a multiplicacao —
fecha no capitulo 3, dentro dos primeiros duzentos segundos.

Vale notar o que o canal ja mediu sobre duracao: os longos de 768 a 814 s
entregaram retencao de 3,84% a 6,21%. O 007, de 762 s, foi o melhor. Piso.

--------------------------------------------------------------------- A PAUTA

Pauta 1078, coletada e escolhida nesta mesma rodada. Eixo
**kredi-karti-asgari-odeme**, nunca usado. O canal cobriu asgari ucret, emekli
zammi, kira artisi, enflasyon e Otomatik Katilim.

ESTRUTURA copiada do outlier "Ev Almak Yerine Kirada Kalsan Ne Olurdu?
Hesapladim" — 183,9 views/dia, 29,3x a mediana da amostra: contrafactual
binario em segunda pessoa, mais a promessa de que a conta foi FEITA. Os outros
dois outliers da coleta tem a mesma forma e vem de canais DIFERENTES, enquanto
o mesmo canal repetindo o mesmo assunto sem essa forma fica em 0,1 a 0,2x. Logo
o que puxa e a forma.

ASSUNTO NAO COPIADO. Os tres outliers sao todos kira-versus-comprar. Copiar o
assunto junto com a estrutura violaria a regra, e o canal acabou de publicar
kira artisi.

FONTES — DUAS ROTAS INSTITUCIONAIS INDEPENDENTES, e elas confirmam o MECANISMO:
  1. mevzuat.gov.tr, Banka Kartlari ve Kredi Kartlari Kanunu (5464) e o
     Yonetmelik: pagando o minimo ou acima dele aplica-se AKDI FAIZ sobre o
     saldo restante; pagando ABAIXO do minimo aplica-se GECIKME FAIZI sobre a
     parte nao paga do minimo, e akdi faiz sobre o restante. O mesmo texto
     trata o "hesap ozetinde yer alan asgari odeme tutari" — o extrato carrega
     o valor minimo.
  2. BDDK (bddk.org.tr): publica por instituicao emissora o akdi faiz orani de
     compra e de saque, comissoes, tarifa anual e exemplos de calculo. O TCMB
     (tcmb.gov.tr) publica em separado os tetos.

O QUE NAO ENTRA NO VIDEO: nenhum VALOR de taxa. O teto do TCMB muda por
comunicado, e a taxa que decide a conta e a do contrato do proprio espectador,
impressa no extrato dele. Nao ha numero meu na conta, e por isso nao ha numero
meu que possa envelhecer.

O QUE O VIDEO NAO FAZ: nao diz que pagar o minimo e errado — as vezes e a
unica opcao —, nao recomenda banco nem cartao, nao cita taxa, nao promete
economia e nao e aconselhamento financeiro.
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
T("Ekstrende iki rakam", "ve sen birini seçiyorsun",
  "Kredi kartı ekstrenin üstünde iki rakam yan yana durur. Her ay ikisinden "
  "birini seçiyorsun, ve bu seçimin bir fiyatı var.",
  cap="Ekstrende iki rakam var")
I("Biri toplam", "diğeri en az",
  "Biri o dönem harcadığının tamamı. Diğeri, o ay ödemen gereken en düşük "
  "tutar.")
I("Seçim senin", "ve her ay tekrar ediyor",
  "Hangisini ödeyeceğine sen karar veriyorsun. Ve bu karar bir kere değil, her "
  "ay yeniden veriliyor.")
I("Peki farkı ne", "kimse yazmıyor",
  "Peki bu iki seçenek arasındaki fark kaç lira? Ekstrende yazmıyor. Faiz "
  "oranını belki biliyorsun, ama oran soyut: asıl mesele o oranın senin "
  "borcunda kaç lira ettiği.")
I("Hesaba giren her sayı", "senin ekstrende yazıyor",
  "Hesaba girecek sayıların hepsi senin ekstrende yazılı. Benim tek bir "
  "rakamım bile işin içine girmiyor, çünkü bu senin borcun, senin oranın ve "
  "senin bu ay vereceğin karar.")
I("Az sonra", "bir çıkarma, bir çarpma",
  "Birkaç dakika içinde bunu kendin hesaplayacaksın: bir çıkarma ve bir "
  "çarpma, elindeki ekstreyle.")

# -------------------------------------------------------------------- cap 2
T("İki rakam ne demek", "önce bunu netleştirelim",
  "Önce iki rakamın ne anlama geldiğini netleştirelim, çünkü hesap bunun "
  "üstüne kuruluyor.",
  cap="İki rakam ne demek")
I("Dönem borcu", "o ayın tamamı",
  "Dönem borcu, o ekstre döneminde biriken harcamalarının toplamı. Tamamını "
  "kapatırsan o dönem için faiz konusu kalmaz, ve ekstre kapanmış olur.")
I("Asgari tutar", "ödemen gereken en az",
  "Asgari tutar ise o ay ödemen gereken en düşük miktar. Ekstrenin üstünde, "
  "dönem borcunun hemen yanında ayrıca yazar.")
I("Asgariyi ödersen", "kalan kısım devreder",
  "Asgariyi ödersen kartın kapanmaz, ama ödemediğin kısım kaybolmaz: bir "
  "sonraki döneme devreder ve devreden kısma faiz işler.")
I("İşte seçim burada", "ödemediğin kısım",
  "Yani seçim aslında şu: dönem borcunun ne kadarını bu ay ödemeyeceksin. "
  "Faizin üzerine bineceği tutar tam olarak o.")
I("Ve arada bir eşik var", "asgarinin altı",
  "Bir de eşik var: asgarinin altına düşmek başka bir duruma geçmek demek, ve "
  "ona ayrı bir bölüm ayıracağım. Şimdilik asgariyi ya da üstünü ödediğini "
  "varsayalım.")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA.
T("Hesap", "bir çıkarma, bir çarpma",
  "Şimdi hesap. Bir çıkarma ve bir çarpma, ve üç sayıya ihtiyacın var.",
  cap="Hesap: çıkarma ve çarpma")
I("Birinci sayı", "dönem borcu",
  "Birinci sayı: dönem borcun. Ekstrenin üstünde, toplam olarak yazıyor.")
I("İkinci sayı", "ödemeyi düşündüğün tutar",
  "İkinci sayı: bu ay gerçekten ödeyeceğin tutar. Asgari olabilir, arada bir "
  "rakam olabilir.")
I("Çıkar", "kalan bu",
  "İkinciyi birinciden çıkar. Elinde kalan, faizin üzerine bineceği tutar.")
I("Üçüncü sayı", "aylık faiz oranı",
  "Üçüncü sayı: kartının aylık faiz oranı. Yüzde olarak yazılıdır; hesap için "
  "onu yüze bölüp ondalık hâline getir.")
I("Çarp", "ve sonuç lira",
  "Kalan tutarı bu oranla çarp. Çıkan sonuç lira cinsinden ve o tek bir ayın "
  "maliyeti. Hesabın tamamı bu.")
I("Neden işe yarıyor", "tek değişken",
  "İşe yarıyor çünkü tek bir şeyi değiştiriyorsun: bu ay ne kadar ödediğini. "
  "Borç da oran da aynı kalıyor.")
I("Şimdi dene", "farklı bir tutarla",
  "İkinci sayıyı değiştirip tekrar yap: aradaki fark senin kazancın. Gerisi, "
  "bu sayıları nerede bulacağın.")

# ===================== DEPOIS DOS 200 SEGUNDOS ==============================

# -------------------------------------------------------------------- cap 4
T("Üç sayı nerede", "hepsi tek kâğıtta",
  "Üç sayının üçü de aynı belgede. Hiçbirini tahmin etmene gerek yok.",
  cap="Üç sayı ekstrede nerede")
I("Dönem borcu", "en üstte, kutu içinde",
  "Dönem borcu genelde ekstrenin en üstünde, ayrı bir kutunun içinde ve büyük "
  "puntoyla yazılır.")
I("Asgari tutar", "hemen yanında",
  "Asgari tutar çoğunlukla hemen onun yanında ya da altında durur. İkisi "
  "birlikte gösterilir.")
I("Son ödeme tarihi", "aynı kutuda",
  "Son ödeme tarihi de aynı bölümde olur. Hesabı yapmadan önce ona da bak, "
  "çünkü karar o tarihe kadar geçerli.")
I("Faiz oranı", "alt bölümde",
  "Faiz oranı genelde alt bölümde, sözleşme bilgileri arasındadır. Alışveriş "
  "için ayrı, nakit çekim için ayrı bir oran görebilirsin.")
I("Hangisini alacaksın", "alışveriş oranını",
  "Normal harcamalar için alışveriş oranını al. Nakit çekim oranı farklıdır ve "
  "genelde daha yüksektir.")
I("Aylık mı yıllık mı", "buna dikkat",
  "Oranın aylık mı yıllık mı olduğuna dikkat et. İkisi de yazılı olabilir, ve "
  "hesapta aylık olan kullanılır.")
I("Bulamazsan", "sözleşmende var",
  "Ekstrede bulamazsan sözleşmende yazılıdır. Orada da bulamazsan bankana "
  "yazılı olarak sor.")
I("Yazılı iste", "telefonda değil",
  "Yazılı olarak iste. İki kez okuyabileceğin bir rakama ihtiyacın var, "
  "telefonda duyduğun bir sayıya değil.")
I("Ve aynı ekstreden", "üçü birden",
  "Üç sayıyı da aynı ekstreden al. Farklı aylardan karıştırırsan hesap "
  "anlamını kaybeder.")

# -------------------------------------------------------------------- cap 5
T("Asgarinin altı", "burası ayrı bir dünya",
  "Şimdi eşiğin altı. Asgari tutarın altında ödeme yapmak, farklı bir duruma "
  "geçmek demek.",
  cap="Asgarinin altına düşersen")
I("İki farklı faiz", "aynı anda",
  "Bu durumda tek bir faiz değil, iki farklı faiz devreye girer. Ve ikisi aynı "
  "anda işler.")
I("Ödenmeyen asgari kısmı", "gecikme faizi",
  "Asgarinin ödemediğin kısmına gecikme faizi uygulanır. Bu, normal işleyen "
  "faizden farklı bir kalemdir.")
I("Kalan borç", "akdi faiz",
  "Borcun asgariyi aşan kısmına ise akdi faiz, yani sözleşmedeki normal faiz "
  "uygulanır.")
I("Yani iki kalem", "tek ayda",
  "Yani tek bir ayda iki ayrı kalem birden birikir. Bu, videodaki basit "
  "hesabın kapsamadığı bir durum.")
I("Nasıl hesaplarsın", "iki parçaya böl",
  "Hesaplamak istersen borcu iki parçaya böl: asgarinin eksik kalan kısmı, ve "
  "asgariyi aşan kısım. Her birini kendi oranıyla çarp.")
I("İki oran da yazılı", "ekstrede ya da sözleşmede",
  "Her iki oran da ekstrende ya da sözleşmende yazılıdır. Gecikme oranı ayrı "
  "bir satırda görünür.")
I("Bu yüzden eşik önemli", "sadece rakam değil",
  "Bu yüzden asgari tutar sadece bir rakam değil, bir eşik. Üstünde kalmakla "
  "altına düşmek aynı şey değil.")
I("Ve etkisi sadece faiz değil", "kayıtlara da geçer",
  "Etkisi de sadece faizle sınırlı kalmayabilir. Gecikme, kredi geçmişine "
  "ilişkin kayıtlara da yansıyabilir.")
I("Bunu da sor", "bankana yazılı olarak",
  "Bunun senin durumunda ne anlama geldiğini bankana yazılı olarak sor. Her "
  "kartın koşulları aynı değil.")

# -------------------------------------------------------------------- cap 6
T("Borç neden büyür", "asıl mekanizma burada",
  "Şimdi asıl mekanizma: ödemediğin kısım neden ay ay büyür.",
  cap="Borç neden ay ay büyür")
I("Faiz kalan üstüne", "her dönem",
  "Faiz her dönem, o dönemin sonunda kalan borcun üstüne işler. Ödemediğin "
  "tutar bir sonraki ayın başlangıç noktası olur.")
I("Yani başlangıç büyür", "her ay",
  "Böylece her ay biraz daha büyük bir tutarın üstünden hesaplanır. Rakam "
  "sabit kalmaz.")
I("Bir de yeni harcama", "üstüne biner",
  "Bir de o ay yaptığın yeni harcamalar var. Onlar da aynı borcun üstüne "
  "eklenir.")
I("İşte kritik nokta", "asgari borcu bitirmez",
  "Kritik nokta şu: asgari ödemek borcu bitirmeye yönelik bir plan değildir. "
  "Kartı açık tutmaya yönelik bir eşiktir.")
I("İkisi farklı şey", "ve karıştırılıyor",
  "Bu ikisi sık karıştırılır. Asgariyi düzenli ödeyen biri, borcunu düzenli "
  "azalttığını sanabilir.")
I("Kendi ekstrenden gör", "üç ayı yan yana koy",
  "Bunu kendi üstünde görebilirsin: son üç ekstreni yan yana koy ve dönem "
  "borçlarını karşılaştır.")
I("Artıyor mu azalıyor mu", "cevap orada",
  "Artıyor mu, azalıyor mu, yoksa yerinde mi sayıyor? Cevap oradadır ve bana "
  "inanmana gerek kalmaz.")
I("Ve bu bir yargı değil", "bir tespit",
  "Bu bir suçlama değil. Bazen asgari ödemek tek seçenektir. Ama tek seçenek "
  "olması, maliyetinin görünmez olmasını gerektirmiyor.")

# -------------------------------------------------------------------- cap 7
T("Hesabın kapsamadıkları", "ve bunlar önemli",
  "Şimdi bu basit hesabın neyi kapsamadığı. Bunu atlarsak hesap yanıltıcı "
  "olur.",
  cap="Hesabın kapsamadıkları")
I("Nakit avans", "ayrı oran, ayrı gün",
  "Birincisi nakit avans. Farklı bir oranla ve genelde çekildiği günden "
  "itibaren işler. Aynı kefeye koyma.")
I("Taksitli harcamalar", "ayrı satır",
  "İkincisi taksitli harcamalar. Onlar kendi planlarıyla ilerler ve ekstrede "
  "ayrı gösterilir.")
I("Kart ücreti", "faizle ilgisi yok",
  "Üçüncüsü yıllık kart ücreti ve benzeri kesintiler. Bunlar faizden bağımsız "
  "kalemlerdir, ayrıca ekle.")
I("Yeni harcamalar", "hesabı bozar",
  "Dördüncüsü, hesabı yaptıktan sonra yaptığın yeni harcamalar. Onlar sonucu "
  "değiştirir.")
I("Bu yüzden", "tek ay için düşün",
  "Bu yüzden hesabı tek bir ay için, o ayın rakamlarıyla düşün. Bir yıllık "
  "kehanet değil, o ayın fiyatı.")
I("Oran da değişebilir", "duyuruyla",
  "Beşincisi, faiz oranları zaman içinde değişebilir. Elindeki sonuç bugünün "
  "koşullarının fotoğrafıdır.")
I("Ama karşılaştırma için", "yeterli",
  "Karşılaştırma için bu yeterli, çünkü iki seçenek de aynı varsayımın altında "
  "duruyor.")
I("Sonuç", "büyüklük mertebesi",
  "Yani bu hesap sana kesin kuruşu değil, büyüklük mertebesini verir. Kararın "
  "başlangıcıdır, ispatı değil.")
I("Ve bu yeter", "tahmin etmeyi bırakmaya",
  "Büyüklük mertebesi de fazlasıyla yeter — çünkü asıl sorun rakamın kendisi "
  "değil, hiç bakılmamış olması.")

# -------------------------------------------------------------------- cap 8
T("Bir aydan bir yıla", "ölçek burada görünür",
  "Ve şimdi çoğu insanın fikrini değiştiren adım.",
  cap="Bir aydan bir yıla")
I("Tek ay", "küçük görünür",
  "Tek bir ayın maliyeti genelde küçük görünür. Üzerinde durulmayacak kadar "
  "küçük.")
I("On iki ile çarp", "ve tekrar bak",
  "Onu on iki ile çarp ve tekrar bak. Aynı davranışın bir yıllık hâli.")
I("Ama dikkat", "bu alt sınır",
  "Ama dikkat: bu bir alt sınırdır. Borç büyüyorsa gerçek rakam bundan yüksek "
  "çıkar, çünkü her ay daha büyük bir tutar üstünden işler.")
I("Bir şeye kıyasla", "somutlaşsın",
  "Çıkan rakamı bildiğin bir şeyle karşılaştır. Kiranla, mesela. Ya da aylık "
  "market harcamanla.")
I("Neden bu işe yarıyor", "soyutluk kalkıyor",
  "İşe yarar çünkü karşılıksız bir lira rakamı soyuttur; karşılığı olan bir "
  "rakam karara dönüşür.")
I("Ve karar tekrarlanıyor", "her ay",
  "Bir de şu var: bu karar her ay yeniden veriliyor. Yani sonuç da her ay "
  "yeniden birikiyor.")
I("İyi tarafı", "değiştirmesi de aylık",
  "İyi tarafı da bu. Aylık verilen bir karar, aylık olarak değiştirilebilir. "
  "Bir sonraki ekstre yeni bir fırsat.")
I("Ve bir de sıra var", "hangi borcu önce",
  "Birden fazla kartın varsa hesabı her biri için ayrı yap. Aynı lirayı en "
  "yüksek oranlı olana koymak, en büyük borca koymaktan farklı sonuç verir.")
I("Küçük fark bile", "hesaba giriyor",
  "Asgarinin biraz üstünde ödenen her lira, çarpımdaki kalan tutarı doğrudan "
  "küçültür. Hepsi ya hep ya hiç değil.")

# -------------------------------------------------------------------- cap 9
T("Bugün ne yapıyorsun", "üç adım",
  "Bugün yapabileceğin şeyle bitiriyoruz, üç adımda.",
  cap="Bugün ne yapıyorsun")
L("Üç adım",
  ["Ekstreyi aç", "Üç sayıyı bul", "Çıkar ve çarp"],
  "Birinci: son ekstreni aç. İkinci: üç sayıyı bul. Üçüncü: çıkar ve çarp.")
I("Birinci adım", "elinde zaten var",
  "Birinci adım için yeni bir şeye gerek yok. Ekstre zaten elinde, telefonunda "
  "ya da kâğıt olarak.")
I("İkinci adım", "dönem borcu, ödeyeceğin, oran",
  "İkinci adımda üç sayıyı işaretle: dönem borcu, ödemeyi düşündüğün tutar, ve "
  "aylık faiz oranı.")
I("Üçüncü adım", "iki işlem",
  "Üçüncü adım telefonundaki hesap makinesi. Bir çıkarma, bir çarpma, iki "
  "dakika.")
I("Sonucu yaz", "tarihiyle birlikte",
  "Sonucu tarihiyle birlikte bir yere yaz. Altı ay sonra karar verirken hangi "
  "koşulların geçerli olduğunu bilmek isteyeceksin.")
I("Ve tekrar et", "her ekstrede",
  "Sonra her ekstrede tekrarla. Rakamlar değişir, işlem değişmez.")
I("Son olarak", "bu bir tavsiye değil",
  "Son olarak açıkça söyleyeyim: buradaki hiçbir şey finansal tavsiye ya da "
  "banka önerisi değil. Bu bir hesaplama yöntemi.")
C("Seviye Seviye", "bu akşam hesapla",
  "Buraya kadar geldiysen bu hesabı bu akşam kendi ekstrenle yap. Ve bulduğun "
  "farkı yorumlara yaz.")


# =============================== O SHORT ====================================
# Gancho seco de numero na primeira frase — a forma dos shorts que mais andaram
# neste canal. E ele entrega a conta inteira, nao a manchete.
SHORT = [
    {"layout": "titulo", "kicker": "Ekstrende iki rakam", "sub": "birini sen seçiyorsun",
     "nar": "Kredi kartı ekstrende iki rakam var, ve hangisini ödeyeceğine sen "
            "karar veriyorsun.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Çıkar", "preco": "dönem borcu eksi ödediğin",
     "nar": "Dönem borcundan bu ay ödeyeceğin tutarı çıkar. Kalan, faizin "
            "üzerine bineceği tutar.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Çarp", "preco": "aylık faiz oranıyla",
     "nar": "Kalanı, ekstrende yazan aylık faiz oranıyla çarp. Oranı yüze "
            "bölmeyi unutma.",
     "sem_cap": True},
    {"layout": "item", "kicker": "Çıkan sonuç", "preco": "o ayın fiyatı",
     "nar": "Çıkan rakam lira cinsinden, ve seçiminin o aya olan maliyeti. On "
            "iki ile çarparsan yıllık hâli.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Seviye Seviye", "sub": "üç sayı nerede",
     "nar": "Üç sayıyı ekstrede nerede bulacağın ve bu hesabın neyi "
            "kapsamadığı, aşağıdaki uzun videoda.",
     "sem_cap": True},
]

THUMB = {"l1": "Asgari", "l2": "ne olurdu"}

COPY = """# Asgari ödemenin gerçek fiyatı, kendi ekstrenden

## TITULO
Asgari Ödeme Yapsan Ne Olurdu? Ekstrendeki Üç Sayıyla Kendin Hesapla

## DESCRICAO
Kredi kartı ekstrenin üstünde iki rakam yan yana durur: dönem borcu ve asgari tutar. Her ay ikisinden birini seçiyorsun ve bu seçimin bir fiyatı var — ama o fiyat ekstrende yazmıyor. Faiz oranını belki biliyorsun; oran soyuttur. Asıl mesele o oranın senin borcunda kaç lira ettiği. Bu videodaki her sayı senin: benim tek bir rakamım hesaba girmiyor.

HESAP (bir çıkarma, bir çarpma)

Birinci sayı dönem borcun. İkinci sayı bu ay gerçekten ödeyeceğin tutar. İkinciyi birinciden çıkar — elinde kalan, faizin üzerine bineceği tutardır. Üçüncü sayı kartının aylık faiz oranı; yüze bölüp ondalık hâline getir ve kalan tutarla çarp. Çıkan sonuç lira cinsinden ve o tek bir ayın maliyetidir. İşe yarar çünkü tek bir şeyi değiştiriyorsun: bu ay ne kadar ödediğini. İkinci sayıyı değiştirip tekrar yaparsan, aradaki fark senin kazancındır. On iki ile çarparsan yıllık hâlini görürsün — ama bu bir ALT SINIRDIR, çünkü borç büyüyorsa her ay daha büyük bir tutar üstünden işler.

ÜÇ SAYI NEREDE: dönem borcu ve asgari tutar genelde ekstrenin üstünde, aynı kutuda; son ödeme tarihi de oradadır. Faiz oranı alt bölümde, sözleşme bilgileri arasında — alışveriş için ayrı, nakit çekim için ayrı bir oran görebilirsin; normal harcamalar için alışveriş oranını al ve oranın aylık mı yıllık mı olduğuna dikkat et. Bulamazsan sözleşmende yazılıdır; orada da yoksa bankandan yazılı olarak iste. Üçünü de aynı ekstreden al.

ASGARİNİN ALTINA DÜŞERSEN durum değişir: asgarinin ödenmeyen kısmına gecikme faizi, borcun asgariyi aşan kısmına akdi faiz uygulanır — tek ayda iki ayrı kalem. Bu, videodaki basit hesabın kapsamadığı bir durumdur.

HESABIN KAPSAMADIKLARI: nakit avans (farklı oran, genelde çekildiği günden itibaren), taksitli harcamalar (kendi planıyla, ekstrede ayrı satır), yıllık kart ücreti gibi faizden bağımsız kalemler, hesaptan sonra yapılan yeni harcamalar, ve oranların zamanla değişebilmesi. Sonuç kesin kuruş değil, büyüklük mertebesidir.

Buradaki hiçbir şey finansal tavsiye ya da banka önerisi değildir. Bu bir hesaplama yöntemidir. Bazen asgari ödemek tek seçenektir — ama tek seçenek olması, maliyetinin görünmez olmasını gerektirmez.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Bu hesabı kendi ekstrenle yap ve buraya tek bir sayı yaz: sadece tek ayın farkı, lira olarak. Banka adı yok, borç tutarı yok, oran yok — sadece fark. Benzer borçlarda bu farkların birbirinden ne kadar açıldığını görmek istiyorum.

## HASHTAGS
#KrediKartı #AsgariÖdeme #SeviyeSeviye

## TAGS
kredi karti asgari odeme, ekstre nasil okunur, donem borcu, asgari tutar, akdi faiz, gecikme faizi, kredi karti faizi hesaplama, son odeme tarihi, nakit avans, taksitli harcama, kart borcu nasil kapatilir, kisisel finans, butce yonetimi, borc yonetimi, hesap ozeti

## CONFIGURACOES DO STUDIO
- Idioma: Turco (tr) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Turquia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum VALOR de taxa e nenhum numero meu. Os tres numeros da conta sao do proprio espectador: o donem borcu e o asgari tutar do extrato dele, o valor que ele decide pagar, e a taxa mensal do contrato dele. O QUE FOI CONFIRMADO, em DUAS ROTAS INSTITUCIONAIS INDEPENDENTES, e o MECANISMO — nao um valor. (1) mevzuat.gov.tr, Banka Kartlari ve Kredi Kartlari Kanunu numero 5464 e o Yonetmelik correspondente: pagando o valor minimo ou acima dele aplica-se AKDI FAIZ sobre o saldo restante; pagando ABAIXO do minimo aplica-se GECIKME FAIZI sobre a parte nao paga do minimo e akdi faiz sobre o restante; e o mesmo texto trata do "hesap ozetinde yer alan asgari odeme tutari", isto e, o extrato carrega o valor minimo. (2) BDDK (bddk.org.tr) publica, por instituicao emissora, o akdi faiz orani de compra e de saque, comissoes, tarifa anual e exemplos de calculo de juros; o TCMB (tcmb.gov.tr) publica em separado os tetos de juros de cartao. O QUE FOI DESCARTADO, de proposito: qualquer VALOR de taxa, inclusive o teto do TCMB. Esse teto muda por comunicado e envelheceria dentro do video, e nao e ele que decide a conta — quem decide e a taxa do contrato do espectador, impressa no extrato dele. Por isso nao ha numero meu na conta e nao ha numero meu que possa envelhecer. O video tambem nao afirma que pagar o minimo e errado, nao recomenda banco nem cartao, nao promete economia e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seviye-seviye-008.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-008",
    "idioma": "tr",
    "voz": "tr-TR-AhmetNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#1D3557", "c1": "#E63946", "c2": "#F4A261", "bg": "#F4F1EA"},
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
    grava(SPEC, "fabrica/specs/seviye-seviye-008.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", len([c for c in CENAS if c.get('cap')]))
