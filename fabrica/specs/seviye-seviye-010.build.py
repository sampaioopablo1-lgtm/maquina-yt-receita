#!/usr/bin/env python3
"""Monta a spec seviye-seviye-010.

ALAVANCA ATACADA: **B — os primeiros 200 segundos e o PISO da faixa**, copiando
a FORMA do pacote que mediu melhor neste canal.

NUMERO DE PARTIDA, medido em 04/10/2026 em dado de vida inteira (ultima linha
de `videos.list` por video — nunca `max(views)`, aprendizado 557):

    pacote   short   longo   travessia   duracao do longo
    003       523      28       5,4%        790,1s
    004       736     180      24,5%        768,1s
    005       344     137      39,8%        700,7s
    006       405      17       4,2%        813,9s
    007       150      51      34,0%        761,9s
    008        52      39      75,0%        727,4s
    009       104      13      12,5%        752,9s

    seviye-seviye: 5.564 views de canal, veredito `liberado`
    travessia TOTAL: 465 de 2.314 = 20,1%

O QUE DEU CERTO, e e o melhor numero da frota: **20,1% de travessia**. No
resep-naik-level, medido uma hora antes, a mesma razao da 0,5% — e no
agla-level, 93% com alcance de 28 views. Este canal tem alcance REAL e
travessia REAL ao mesmo tempo, e e o unico que tem as duas coisas.

E CORRIJO AQUI UMA COISA QUE EU MESMO ESCREVI UMA HORA ATRAS. No aprendizado
562 eu disse que a travessia e "inversamente proporcional ao alcance do short"
e chamei a serie de monotona. Medido agora: a correlacao e -0,586 no
resep-naik-level e -0,488 aqui, com n=6 e n=7. Mesma direcao, mas aqui a serie
NAO e monotona — o short de 736 views atravessou 24,5% e o de 405 atravessou
4,2%. Alcance nao e a causa; era um proxy que casou bem num canal so. O 562 fica
com a correcao escrita.

O QUE SEPARA OS PARES, e esta leitura explica os dois canais de uma vez:
atravessa o par em que o LONGO responde uma DECISAO que o espectador tem de
tomar com prazo (004: a data em que o aumento comecou; 005: o teto do aluguel
em agosto; 007: os dois meses que restam para entrar no BES). Nao atravessa o
par em que o longo repete uma CONSTATACAO que o short ja fechou (003: qual e a
menor aposentadoria; 006: que nao existe uma inflacao so). Isso e o aprendizado
482 — metodo converte, fato nao — aplicado a travessia em vez da inscricao.

E ISSO EXPOE UMA TENSAO ENTRE AS DUAS ALAVANCAS, que precisa ficar dita: a
rotina manda o SHORT entregar a conta fechada, e isso maximiza alcance de short
(resep: 1.064 views) e minimiza travessia (resep: zero), porque o short acabou
o servico. As duas coisas nao se resolvem no mesmo texto; resolvem-se fazendo o
short fechar UMA pergunta e o longo abrir OUTRA.

O QUE NAO DEU: o 006, com 813,9s, o longo mais longo do canal, ficou com 17
views. O 005, com 700,7s, o mais curto, ficou com 137. Sete longos entre 700 e
814 segundos e a duracao media assistida da frota e ~200s — alongar nao somou
exibicao nenhuma (aprendizado 483).

O QUE MUDO POR CAUSA DISSO:
1. **PISO DA FAIXA, pela primeira vez neste canal.** `liberado` vale 12-15 min
   e os sete longos foram de 11,7 a 13,6. Este vai a 720s = 12,0 min exatos, o
   piso. NOVE capitulos, nao oito: mais capitulos no mesmo tempo.
2. **A FORMA DO 004**, que e o melhor par do canal: ele nao entrega fato nem
   metodo solto — ele CORRIGE UMA CRENCA ("o aumento comecou em julho, nao em
   dezembro") e depois entrega a conta. Este pacote tem a mesma forma: a crenca
   corrigida e "meu salario e X".
3. **O short fecha UMA pergunta e o longo abre OUTRA.** O short entrega a
   divisao; o longo responde onde estao os quatro custos do mesmo trajeto, que
   o short nao toca.
4. **TRES CENAS COM FOOTAGE.** Este canal nunca teve uma.

--------------------------------------------------------------- DIMENSIONAMENTO

720s, nove capitulos de ~80s NA ESTIMATIVA — bem acima dos 64,2s que o
`prontidao.MARGEM_CAP` cobra. A tr-TR-AhmetNeural desvia +2,2%, que empurra
para cima e e o lado seguro do portao.

A resposta fecha dentro dos primeiros 200s, no capitulo 3. O tempo REAL sai do
`legendas.srt`.

--------------------------------------------------------------------- A PAUTA

EIXO NOVO: **quanto do salario e gasto para ir busca-lo — o custo do trajeto
como percentual do liquido.**

Os eixos ja publicados neste canal sao salario minimo contra linha da fome,
menor aposentadoria e a matematica do reajuste, a data em que o reajuste
comecou, teto do aumento de aluguel, inflacao de bens contra servicos,
contribuicao estatal do BES, pagamento minimo do cartao e faixa de imposto.
Trajeto nao esta na lista, e e a dor mais diaria de todas.

FONTES: este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao
institucional. Nao cita preco de passagem, nao cita tarifa de nenhuma cidade,
nao cita preco de combustivel, nao cita media nacional e nao cita lei. Os dois
numeros da conta sao do proprio espectador: o que ele gastou para ir e voltar
(que esta no extrato do cartao de transporte, no app ou no extrato do banco) e
o liquido dele (que esta na folha de pagamento). ISSO E DELIBERADO: tarifa de
transporte na Turquia varia por cidade e muda durante o ano, e um numero meu
tornaria a conta errada para a maioria de quem assiste — justamente quando o
numero certo esta no extrato que ele tem no bolso.

AS TRES CONDICOES DO APRENDIZADO 504:
1. o dinheiro e DELE — o que ele pagou para chegar ao trabalho;
2. e ESCOLHA COM PRAZO — a proxima conversa de aumento e a proxima oferta;
3. o SHORT entrega a conta — a divisao fechada, com o resultado.

O QUE O VIDEO NAO FAZ: nao diz qual percentual e "muito", nao recomenda mudar
de casa nem de emprego, nao compara cidades, nao diz que carro e melhor ou pior
que transporte publico e nao e aconselhamento financeiro.
"""
import json

CENAS = []

# Links resolvidos em 04/10/2026 pela pre-busca rodada do sandbox, onde
# `api.pexels.com` responde. `--conferir`: 4/4 clipes que o CDN entrega. Com o
# link gravado o pacote fica REPRODUZIVEL — sem ele, dois renders da mesma spec
# pegam clipes diferentes, porque o Pexels reordena a busca.
#
# UMA RESSALVA HONESTA sobre a cena 0: o clipe e uma estacao de metro em
# Jacarta, nao na Turquia. A narracao nao afirma lugar nenhum, e b-roll aqui e
# enfeite — mas fica dito, porque um clipe de transporte lotado "generico" num
# canal turco e uma escolha, nao um dado. Os outros tres nao tem esse problema:
# documento, catraca e congestionamento urbano nao carregam lugar, e o do
# transito e de um autor turco.
BROLL = {
    39648550: ("https://videos.pexels.com/video-files/39648550/16902813_1280_720_25fps.mp4",
               "Daneswara Eka",
               "https://www.pexels.com/video/busy-jakarta-metro-station-scene-39648550/"),
    8298007: ("https://videos.pexels.com/video-files/8298007/8298007-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/a-woman-checking-the-documents-8298007/"),
    7251756: ("https://videos.pexels.com/video-files/7251756/7251756-hd_1280_720_25fps.mp4",
              "MART PRODUCTION",
              "https://www.pexels.com/video/a-person-entering-a-train-station-7251756/"),
    32909774: ("https://videos.pexels.com/video-files/32909774/14025983_1280_720_29fps.mp4",
               "Seyhmus Kino",
               "https://www.pexels.com/video/heavy-traffic-jam-on-urban-highway-during-daytime-32909774/"),
}


def T(kicker, sub, nar, cap=None):
    c = {"layout": "titulo", "kicker": kicker, "sub": sub, "nar": nar}
    if cap:
        c["cap"] = cap
    else:
        c["sem_cap"] = True
    CENAS.append(c)


def B(kicker, sub, nar, q, pexels_id=None, cap=None):
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
B("Maaşınız bir sayı", "elinizde kalan başka bir sayı",
  "Maaşınızı biliyorsunuz. Ama onu almaya gitmenin size kaça mal olduğunu "
  "büyük olasılıkla hiç yan yana koymadınız.",
  "crowded public transport during rush hour", 39648550,
  cap="Maaş bir sayı, kalan başka bir sayı")
I("Bu bir kayıp değil", "bir maliyet",
  "Bu bir kayıp değil, bir maliyet. İşe gitmek zorunlu, ve o para gerçekten "
  "bir şey satın alıyor. Ama maliyetin büyüklüğünü bilmek sizin hakkınız, "
  "çünkü onunla karar veriyorsunuz.")
I("Ve karar yakın", "zam ve teklif mevsimi",
  "Kararın tarihi de belli: bir sonraki zam konuşması ve bir sonraki iş "
  "teklifi. İkisinde de masaya konan sayı brüt maaş oluyor, ve brüt maaş bu "
  "maliyeti görmüyor.")
I("Benim tek sayım yok", "ikisi de sizin",
  "Bu hesapta benim bir tek sayım yok. Ne bilet fiyatı, ne tarife, ne akaryakıt "
  "fiyatı, ne ortalama. Çünkü ulaşım ücreti şehirden şehire değişiyor ve yıl "
  "içinde değişiyor.")
I("Doğru sayı sizde", "cebinizdeki ekstrede",
  "Doğru sayı sizin cebinizde: ulaşım kartınızın ekstresinde, uygulamada ya da "
  "banka hesabınızda. Benim bir sayı söylemem hesabı çoğunluk için yanlış "
  "yapardı.")
I("İki bölüm sonra", "hesap bitiyor",
  "İki bölüm sonra hesap bitmiş olacak. Bir toplama, bir bölme, ve iki sayı — "
  "ikisi de bugün elinizin altında.")

# -------------------------------------------------------------------- cap 2
T("Birinci sayı", "ekstreden, tahminden değil",
  "Birinci sayı aylık ulaşım harcamanız, ve onu tahminle bulmak işe yaramaz — "
  "tahmin her zaman olağan günü sayar, olağandışı günü saymaz.",
  cap="Birinci sayı: ekstreden, tahminden değil")
I("Son otuz günü açın", "kart, uygulama ya da banka",
  "Son otuz günü açın: ulaşım kartı ekstresi, ulaşım uygulaması ya da banka "
  "hareketleri. Hepsini değil, sadece işe gidiş ve dönüşle ilgili olanları.")
I("Dört kalem sayılıyor", "hepsi aynı trajede",
  "Dört kalem sayılıyor. Bir: bilet, kart yüklemesi ya da abonman. İki: o "
  "güzergâhta yakıt ve otopark. Üç: geç kaldığınız günlerin taksisi. Dört: "
  "sadece yolda olduğunuz için aldığınız kahve ve öğle yemeği.")
I("Dördüncüsü şaşırtıyor", "ve en kolay unutulan",
  "Dördüncüsü çoğu insanı şaşırtır, ve en kolay unutulandır — çünkü yemek "
  "harcaması gibi görünür, ama evde kalsanız o parayı harcamıyordunuz.")
I("Sayılmayanlar", "yola bağlı olmayan",
  "Sayılmayanlar: eve giden market alışverişi, hafta sonu çıkışları, ve "
  "arabanın yola bağlı olmayan sabit masrafları. Onlar işe gitmeseniz de "
  "vardı.")
I("Toplayın", "bu birinci sayı",
  "Dört kalemi toplayın. Çıkan rakam sizin aylık trajede maliyetiniz, ve bu "
  "birinci sayı. Otuz gün yeterli, çünkü ay içinde hem olağan hem olağandışı "
  "gün geçiyor.")

# -------------------------------------------------------------------- cap 3
B("İkinci sayı", "bordroda yazılı",
  "İkinci sayıyı aramanız gerekmiyor; o zaten yazılı. Bordronuzda elinize "
  "geçen net tutar.",
  "person checking a payslip document", 8298007,
  cap="İkinci sayı ve bölme işlemi")
I("Brütü değil", "eline geçeni",
  "Brütü değil, elinize geçeni alın. Çünkü ulaşımı brütle değil, hesabınıza "
  "yatan parayla ödüyorsunuz.")
I("Şimdi bölün", "birinciyi ikinciye",
  "Şimdi bölün: aylık trajede maliyetini net maaşınıza bölün ve yüzle çarpın. "
  "Çıkan yüzde, maaşınızın işe gitmek için harcanan kısmıdır.")
I("Ve bir çevirme daha", "yüzdeyi güne çevirin",
  "Bir çevirme daha isterseniz: o yüzdeyi yirmi iş günüyle çarpıp yüze bölün. "
  "Çıkan gün sayısı, ayda kaç gün sadece işe gitmek için çalıştığınızı "
  "gösterir.")
I("Hesap bitti", "sırada: nereden geldiği",
  "Hesap bitti. Bundan sonraki bölümler yeni soruyu yanıtlıyor: bu sayı neden "
  "sandığınızdan büyük çıkıyor, ve aynı trajede nerede birikiyor.")
I("Yüzde mi, gün mü", "ikisi aynı sayı",
  "İki sonuç aynı şeyi söylüyor, ama farklı yerde işe yarıyor: yüzde zam "
  "konuşmasında, gün sayısı ise ofiste geçirilecek gün sayısını tartışırken. "
  "İkisini de yazın, çünkü ikisi de aynı iki sayıdan çıkıyor.")
I("Ve bir uyarı", "yüzde kaçı makul demiyorum",
  "Bir uyarı da şimdi: bu video yüzde kaçın makul olduğunu söylemeyecek. O "
  "sizin şehrinize, mesafenize ve maaşınıza bağlı, ve onları siz "
  "biliyorsunuz.")

# ================= DEPOIS DA RESPOSTA — POR QUE CONTINUAR ====================

# -------------------------------------------------------------------- cap 4
T("Neden büyük çıkıyor", "dört yerde birikiyor",
  "Sayı neredeyse her zaman tahminden büyük çıkar, ve nedeni tek değil. Aynı "
  "trajede dört ayrı yerde birikiyor.",
  cap="Aynı trajede dört yer")
I("Birinci yer", "olağandışı gün",
  "Birinci yer: olağandışı gün. Kart yüklemesi aylık ve sabit görünür, ama "
  "geç kaldığınız, yağmur yağan ve aktarma kaçırdığınız günler o sabitin "
  "üstüne biniyor.")
I("İkinci yer", "ikinci bacak",
  "İkinci yer: trajenin ikinci bacağı. Metroya ya da otobüse ulaşmak için "
  "attığınız kısa adım — dolmuş, minibüs, scooter — ayrı ödenir ve ayrı "
  "unutulur.")
I("Üçüncü yer", "yolda olmanın yemeği",
  "Üçüncü yer: yolda olmanın yemeği. Sabah kahvesi ve dışarıda öğle yemeği "
  "trajenin parçasıdır, çünkü evde olsanız o harcama olmuyordu.")
I("Dördüncü yer", "ve en sessizi",
  "Dördüncü yer, ve en sessizi: otopark, köprü ve otoyol ücretleri. Tek tek "
  "küçük görünürler ve hiçbiri aylık ekstrede tek satır halinde durmaz.")
I("Ve hepsi birden görünmez", "ekstrede dağınık durur",
  "Dördünün ortak özelliği şu: hiçbiri ekstrede tek bir satır halinde "
  "durmuyor. Dağınık dururlar, her biri küçük görünür, ve küçük görünen "
  "kalemler toplanmadıkça büyük olduklarını belli etmezler.")
I("Dördü de aynı yolda", "ve dördü de sizin",
  "Dördü de aynı yola ait, ve dördü de sizin ekstrenizde yazılı. Hiçbirini "
  "tahmin etmeniz gerekmiyor — sadece aynı başlık altında toplanmaları "
  "gerekiyor.")

# -------------------------------------------------------------------- cap 5
B("Dört yer", "dört hesap",
  "Dört yerin her biri için bir hesap var, ve hiçbiri sizden yeni bir sayı "
  "istemiyor.",
  "person tapping a transit card at a turnstile", 7251756,
  cap="Her yer için bir hesap")
I("Olağandışı gün için", "ayı ikiye ayırın",
  "Olağandışı gün için: ayı ikiye ayırın. Olağan günlerin maliyetini ve "
  "olağandışı günlerin maliyetini ayrı toplayın. İkincisi genelde birincinin "
  "yanında küçük durmaz.")
I("İkinci bacak için", "tek gidişi ölçün",
  "İkinci bacak için: tek bir günü baştan sona ölçün, kapıdan kapıya, her "
  "ödemeyi yazarak. Sonra yirmi iş günüyle çarpın. Bir gün ölçmek otuz günü "
  "hatırlamaktan doğrudur.")
I("Yemek için", "evde kalınan günle karşılaştırın",
  "Yemek için: işe gitmediğiniz bir günün yemek harcamasını, gittiğiniz bir "
  "günle karşılaştırın. Aradaki fark trajenin yemek maliyetidir, ve o fark "
  "tahmin değil ölçüm.")
I("Ücretler için", "üç aylık ekstre",
  "Köprü, otoyol ve otopark için: üç aylık ekstre açın ve bu kalemleri "
  "arayın. Üç ayın ortalaması bir ayın tahmininden iyidir, çünkü bu "
  "harcamalar düzensiz.")
I("Ve sonra", "tek bir başlık",
  "Hepsini tek bir başlık altına yazın: trajede maliyeti. Bu dört hesabın "
  "tamamı bir akşamda biter, ve ondan sonra her ay sadece güncellenir.")

# -------------------------------------------------------------------- cap 6
T("Hesaba girmeyenler", "gizlemekten iyidir söylemek",
  "Şimdi gizlemekten iyi olan kısım: üç şey bu hesaba bilerek girmiyor, ve "
  "girmemeleri gerekiyor.",
  cap="Hesaba bilerek girmeyenler")
I("Arabanın sabitleri", "yolla gelmedi",
  "Arabanın sigortası, vergisi ve değer kaybı girmiyor. Onlar işe gitmeseniz "
  "de vardı. Sadece o güzergâha ait yakıt, otopark ve ücretler giriyor.")
I("Zaman", "para değil, ama bedava da değil",
  "Yolda geçen zaman da girmiyor, çünkü o para değil. Ama bedava olduğunu da "
  "söylemiyorum: sadece bu hesabın birimi lira, ve zamanı liraya çevirmek "
  "başka bir tartışma.")
I("İşveren desteği", "varsa düşülür",
  "İşvereniniz ulaşım desteği veriyorsa, o destek maliyetten düşülür. Hesap "
  "cebinizden çıkanı ölçüyor, cebinize girmeyeni değil.")
I("Ve bir sonuç da meşru", "yüzde küçük çıkabilir",
  "Son bir olasılık, ve o da meşru bir sonuç: yüzde küçük çıkabilir. O zaman "
  "bu kalem sizde düzenli, ve para başka yerde gidiyor — burada değil.")
I("Bir de şu girmiyor", "başkasının trajesi",
  "Eşinizin ya da çocuğunuzun yol masrafı da bu hesaba girmiyor. Bu hesap "
  "tek bir kişinin tek bir işine gidişini ölçüyor; haneyi ölçmek isterseniz "
  "aynı hesabı herkes için ayrı yapın, toplamayın.")
I("Önemli olan", "karşılaştırılabilir olması",
  "Önemli olan sayının küçük ya da büyük olması değil, aynı yöntemle tekrar "
  "ölçülebilir olması. Yöntem sabitse, iki ölçüm arasındaki fark bir şey "
  "söyler.")

# -------------------------------------------------------------------- cap 7
T("Aynı maaş, iki traje", "ve aynı teklif değil",
  "Şimdi neredeyse herkesi yanıltan durum: iki iş teklifi, aynı net maaş, "
  "farklı mesafe. Aynı teklif değiller.",
  cap="Aynı maaş, iki farklı traje")
I("Brüt eşitse", "kalan eşit değil",
  "İki teklifin brütü ve neti eşit olabilir, ama elinizde kalan eşit "
  "olmayacak, çünkü birine gitmek diğerine gitmekten pahalı.")
I("Karşılaştırma şöyle", "net eksi traje",
  "Karşılaştırmayı şöyle yapın: her teklif için netten o trajenin aylık "
  "maliyetini çıkarın. Kıyaslanacak sayı o farktır, maaşın kendisi değil.")
I("Evden çalışma günleri", "hesabı değiştirir",
  "Haftada kaç gün ofiste olunacağı da bu hesabın içindedir. Üç gün ofis ile "
  "beş gün ofis, aynı maaşta iki ayrı sonuç verir.")
I("Mesafe maaş gibi artmaz", "bir kere seçilir",
  "Bir fark daha var: maaş her yıl yeniden konuşulur, mesafe ise işe "
  "girerken bir kere seçilir ve sonra yıllarca aynı kalır. Yanlış seçilen "
  "mesafeyi düzeltmek, yanlış konuşulan zamı düzeltmekten zordur.")
I("Bir de şu durum", "aynı şirket, iki ofis",
  "Aynı şirkette bile iki ofis arasında fark olabilir, ve hangi ofiste "
  "çalışacağınız çoğu zaman teklifte yazmaz. Yazması istenebilir, ve bu "
  "istek tamamen olağandır.")
I("Ve sormak normaldir", "yazılı olarak",
  "Kaç gün ofiste beklendiğini sormak tamamen olağan bir sorudur, ve cevabı "
  "yazılı olarak istenebilir. Teklifi kabul etmeden önce sorulur, sonra "
  "değil.")

# -------------------------------------------------------------------- cap 8
T("Bu sayının bir işi var", "zam konuşmasında",
  "Sayı artık var. Bir işi daha kaldı, ve o iş bir sonraki zam konuşmasında "
  "oluyor.",
  cap="Zam konuşmasında hangi sayı")
I("Şikâyet değil", "bir sayı",
  "Masaya konan şey şikâyet değil, bir sayı: bu işe gelmek bana ayda şu kadar "
  "tutuyor, ve bu maaşın yüzde şu kadarı. Sayı üzerinden konuşmak kolaydır.")
I("Ve iki yol var", "zam ya da gün",
  "Ve iki çözüm yolu var, ikisi de istenebilir: ya zam, ya ofiste geçirilen "
  "gün sayısının azalması. İkincisi şirkete bedava gelir, ve sizin hesabınızı "
  "aynı miktarda düzeltir.")
I("Zam istenirken", "yuvarlak sayı değil",
  "Zam istenirken yuvarlak bir rakam söylemek yerine bu sayıyı söylemek "
  "işinize yarar, çünkü yuvarlak rakam pazarlık gibi durur ve ölçülmüş bir "
  "sayı gerekçe gibi durur.")
I("Ofis günü istenirken", "şirkete bedava gelir",
  "Gün sayısının azalmasını isterken de aynı sayı işe yarar: haftada bir "
  "günün sizin hesabınızda ne kadar düzelttiğini söyleyebilirsiniz. "
  "Şirkete bir lira maliyeti yok, ve sizde ölçülebilir bir fark var.")
I("Bir ay sonra ölçün", "aynı yöntemle",
  "Hangi yol olursa olsun, bir ay sonra aynı yöntemle tekrar ölçün. İki ölçüm "
  "arasındaki fark işe yarayıp yaramadığını söyler — his değil.")
I("Değişmediyse", "yöntem değil, seçim",
  "Sayı değişmediyse yöntem çalışmıyor demek değil; yanlış kalemi seçtiniz "
  "demek. Dört yerden sıradakine geçip yeniden ölçün.")

# -------------------------------------------------------------------- cap 9
B("Bugün üç adım", "hepsi elinizdekiyle",
  "Bugün üç adım, ve üçü de bugün elinizde olan şeylerle yapılıyor.",
  "city traffic jam at rush hour", 32909774,
  cap="Bugün üç adım")
I("Birinci adım", "otuz günü açın",
  "Birinci adım: ulaşım kartı ekstresini ya da banka hareketlerini açın ve son "
  "otuz günde o dört kalemi toplayın. Bu birinci sayı, ve bir akşamda "
  "çıkıyor.")
I("İkinci adım", "bordrodan net",
  "İkinci adım: bordronuzdan elinize geçen net tutarı alın. Brütü değil, neti "
  "— ulaşımı netle ödüyorsunuz.")
I("Üçüncü adım", "bölün ve yazın",
  "Üçüncü adım: birinciyi ikinciye bölün, yüzle çarpın, ve çıkan yüzdeyi bir "
  "yere yazın tarihiyle birlikte. Bir ay sonra karşılaştıracağınız sayı o.")
I("Ve tarihi yazın", "sayı tek başına işe yaramaz",
  "Tarihi yazmayı atlamayın. Tek bir yüzde bir durum bildirir; tarihli iki "
  "yüzde bir yön bildirir, ve karar vermek için yön gerekiyor.")
C("Yorumda tek bir şey", "ne maaş, ne şehir",
  "Yorumlara tek bir şey yazın: çıkan yüzde. Ne maaşınızı, ne şehrinizi — "
  "sadece yüzdeyi. Aynı işte bu sayının ne kadar farklı çıktığını görmek "
  "istiyorum.")


# =============================== O SHORT =====================================
# O short fecha UMA pergunta — a divisao, com o resultado — e o longo abre
# OUTRA: onde o numero se acumula no mesmo trajeto. E a saida da tensao entre
# as duas alavancas descrita no docstring.

SHORT = [
    {"layout": "titulo", "kicker": "Maaşınızı biliyorsunuz",
     "sub": "onu almaya gitmek kaça?",
     "nar": "Maaşınızı biliyorsunuz. Onu almaya gitmenin kaça mal olduğunu "
            "biliyor musunuz?", "sem_cap": True},
    {"layout": "titulo", "kicker": "Birinci", "sub": "otuz günlük ulaşım",
     "nar": "Birinci: son otuz günde işe gidiş dönüş için ödediğiniz her şeyi "
            "toplayın. Bilet, yakıt, otopark, taksi.", "sem_cap": True},
    {"layout": "titulo", "kicker": "İkinci", "sub": "bordrodaki net",
     "nar": "İkinci: bordronuzdaki net maaş. Brüt değil.", "sem_cap": True},
    {"layout": "titulo", "kicker": "Bölün", "sub": "işte yüzdeniz",
     "nar": "Birinciyi ikinciye bölüp yüzle çarpın. Maaşınızın o kadarı işe "
            "gitmeye gidiyor.", "sem_cap": True},
    {"layout": "cta", "kicker": "Nerede birikiyor", "sub": "dört yer, aşağıda",
     "nar": "Aynı yolda dört yerde birikiyor, ve dördü de aşağıdaki videoda.",
     "sem_cap": True},
]

THUMB = {"l1": "İşe gitmek", "l2": "maaşının?"}

COPY = """# İşe gitmenin maliyeti: maaşınızın yüzde kaçı yolda kalıyor

## TITULO
Maaşınız Değil, Elinizde Kalanı: İşe Gitmek Size Kaça Mal Oluyor?

## TITULO SHORT
İşe gitmek maaşının yüzde kaçı?

## DESCRICAO
Maaşınızı biliyorsunuz. Ama onu almaya gitmenin size ayda kaça mal olduğunu büyük olasılıkla hiç yan yana koymadınız. Bu bir kayıp değil, bir maliyet — işe gitmek zorunlu ve o para gerçekten bir şey satın alıyor. Ama maliyetin büyüklüğünü bilmek sizin hakkınız, çünkü bir sonraki zam konuşmasında ve bir sonraki iş teklifinde masaya konan sayı brüt maaş oluyor, ve brüt maaş bu maliyeti görmüyor.

Bu videoda benim bir tek sayım yok. Ne bilet fiyatı, ne tarife, ne akaryakıt fiyatı, ne ortalama. Bu bilerek böyle: ulaşım ücreti şehirden şehire değişiyor ve yıl içinde değişiyor, dolayısıyla benim söyleyeceğim bir sayı hesabı çoğunluk için yanlış yapardı — tam da doğru sayı sizin cebinizdeki ekstrede dururken. Hesabın iki sayısı da sizin: biri ulaşım kartı ekstrenizde, uygulamanızda ya da banka hareketlerinizde, diğeri bordronuzda.

Birinci sayıyı tahminle bulmak işe yaramaz, çünkü tahmin olağan günü sayar ve olağandışı günü saymaz. Son otuz günü açın ve dört kalemi toplayın: bilet, kart yüklemesi veya abonman; o güzergâha ait yakıt ve otopark; geç kaldığınız günlerin taksisi; ve sadece yolda olduğunuz için aldığınız kahve ile öğle yemeği. Dördüncüsü çoğu insanı şaşırtır, çünkü yemek harcaması gibi görünür — ama evde kalsanız o parayı harcamıyordunuz. Sayılmayanlar da var: eve giden market alışverişi, hafta sonu çıkışları ve arabanın yola bağlı olmayan sabit masrafları.

İkinci sayıyı aramanız gerekmiyor; o zaten yazılı. Bordronuzda elinize geçen net tutar — brütü değil, çünkü ulaşımı brütle değil hesabınıza yatan parayla ödüyorsunuz. Sonra bölün: aylık trajede maliyetini net maaşınıza bölüp yüzle çarpın. Çıkan yüzde, maaşınızın işe gitmek için harcanan kısmıdır. İsterseniz bir çevirme daha: o yüzdeyi yirmi iş günüyle çarpıp yüze bölün, ve çıkan gün sayısı ayda kaç gün sadece işe gitmek için çalıştığınızı gösterir.

Bir bölüm bu sayının neden tahminden büyük çıktığını anlatıyor, ve orada aynı trajenin dört ayrı yeri var: olağandışı günler; trajenin ikinci bacağı, yani metroya ya da otobüse ulaşmak için attığınız kısa adım; yolda olmanın yemeği; ve en sessizi, otopark ile köprü ve otoyol ücretleri. Sonraki bölüm her biri için bir hesap veriyor, ve hiçbiri sizden yeni bir sayı istemiyor.

Bir bölüm hesaba bilerek girmeyenleri sayıyor, çünkü gizlemekten iyidir söylemek: arabanın sigortası, vergisi ve değer kaybı; yolda geçen zaman; ve işveren ulaşım desteği, ki varsa maliyetten düşülür. Yüzdenin küçük çıkması da meşru bir sonuç — o zaman bu kalem sizde düzenli ve para başka yerde gidiyor.

Bir bölüm neredeyse herkesi yanıltan duruma ayrıldı: iki iş teklifi, aynı net maaş, farklı mesafe. Aynı teklif değiller, ve karşılaştırma netten o trajenin maliyeti çıkarılarak yapılır. Haftada kaç gün ofiste olunacağı da bu hesabın içindedir, ve sormak tamamen olağan bir sorudur.

Son bölüm bu sayının zam konuşmasındaki işini anlatıyor, ve orada iki yol var: ya zam, ya ofiste geçirilen gün sayısının azalması.

Sonda üç adım, hepsi bugün elinizde olan şeylerle.

Görüntüler: Pexels (serbest lisans) — Daneswara Eka, Mikhail Nilov, MART PRODUCTION, Şeyhmus Kino.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Hesabı yapınca yorumlara tek bir şey yazın: çıkan yüzde. Ne maaşınızı, ne şehrinizi, ne iş yerinizi — sadece yüzdeyi. Aynı işi yapan insanlarda bu sayının ne kadar farklı çıktığını görmek istiyorum. Yüzde küçük çıktıysa onu da yazın; o da bir sonuç.

## HASHTAGS
#Maaş #Kariyer #SeviyeSeviye

## TAGS
ulaşım masrafı, işe gidiş gelis maliyeti, net maaş hesaplama, maaş pazarlığı, zam konuşması, iş teklifi karşılaştırma, bordro nasıl okunur, aylık butce, kişisel finans, ulaşım kartı ekstresi, evden çalışma, hibrit çalışma, otopark köprü ücreti, is degistirme, maas yuzdesi

## CONFIGURACOES DO STUDIO
- Idioma: Turco (tr) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Turquia | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhum numero meu e NAO faz nenhuma afirmacao institucional. Nao cita preco de passagem, nao cita tarifa de nenhuma cidade turca, nao cita preco de combustivel, nao cita valor de pedagio nem de estacionamento, nao cita media nacional e nao cita lei nem regulamento. Os dois numeros da conta sao do proprio espectador: o que ele gastou para ir e voltar do trabalho nos ultimos trinta dias, que esta no extrato do cartao de transporte, no aplicativo ou no extrato bancario dele, e o liquido dele, que esta na folha de pagamento. O QUE FOI DELIBERADAMENTE DEIXADO DE FORA, e por que: (1) qualquer tarifa de transporte, porque ela varia por cidade na Turquia e muda durante o ano, e um numero meu tornaria a conta errada para a maioria de quem assiste — justamente quando o numero certo esta no extrato que ele tem no bolso; (2) qualquer percentual de referencia do tipo "o normal e gastar X por cento", porque nao ha fonte oficial para isso e o video nao faz essa comparacao: a conta e sobre o trajeto dele, nao sobre uma media; (3) o valor do TEMPO gasto no trajeto, porque converter tempo em lira exige uma premissa que eu nao posso certificar — o video diz explicitamente que a unidade desta conta e lira e que o tempo e outra discussao, em vez de fingir que ele nao existe. O video tambem nao diz qual percentual e "muito", nao recomenda mudar de casa nem de emprego, nao compara cidades, nao diz que carro e melhor ou pior que transporte publico e nao e aconselhamento financeiro.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seviye-seviye-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seviye-seviye",
    "pacote": "seviye-seviye-010",
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
    from ensaio import duracao_estimada, duracao_estimada_short, duracao_cena
    grava(SPEC, "fabrica/specs/seviye-seviye-010.json")
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
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: {c['broll_q']}")
