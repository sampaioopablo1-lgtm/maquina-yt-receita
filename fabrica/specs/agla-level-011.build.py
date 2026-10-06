"""agla-level-011 — tres papeis sobre o mesmo TDS, e quem fez cada um.

ALAVANCA ATACADA: A (forma: metodo que a pessoa aplica em si mesma).

NUMERO DE PARTIDA, lido AO VIVO na `videos.list` em 06/10/2026 22:12, casado
por `item->>'id'`:

    pacote  short  longo  dur     titulo
    004       28     26   777,1   8th Pay Commission: a conta real do fitment factor
    007        0      7   529,9   Regime antigo contra novo: quem nao escolhe
    003       19      4   726,8   EPF Scheme 2026: o que mudou
    008        8      4   536,9   CTC ou o que cai na mao? da sua propria ficha
    009        5      2   556,0   Dinheiro parado na ficha de salario
    006       11      2   764,7   EPFO 3.0: 50% no ATM, 75% no UPI
    010        2      1   575,0   Gratuidade: a contagem de quinze e vinte e seis
    005       26      0   840,8   ITR 2026: a data passou

O QUE NAO DA PARA LER: teto de 26 views de longo. Entre 26, 7 e 4 nao ha sinal
separavel de ruido, e eu nao vou inventar padrao — igual ao nivel-do-jogo desta
mesma madrugada.
O QUE DA PARA DIZER: o melhor longo do canal (004, 26 views, 3,7x o segundo) e
um pacote de CONTA e e o segundo MAIS LONGO. O pior (005, zero) e o mais longo
de todos e e noticia com prazo vencido no proprio titulo. Entao nem a duracao
explica: o que separa 004 de 005 e conta contra noticia.
O QUE VOU MUDAR: manter a forma de conta e trocar o objeto — de calcular um
valor para CONFERIR dois valores que o espectador ja tem.

A TRAVA DO 549, com o segundo teste do aprendizado 605: 88 linhas de vida
inteira, 2 quedas, pior delta -28 — historico contaminado. MAS na ultima coleta
(04/10) nenhum dos 12 ids esta abaixo do proprio passado, pior desvio ZERO.
Terceiro desfecho possivel do teste: historico sujo, retrato limpo. Mesmo assim
li ao vivo, porque o retrato de 04/10 nao inclui o pacote 010, publicado hoje.

VEREDITO `canal frio` -> eixo novo e piso de 8 min. Sobre o piso, aprendizado
602: com oito capitulos de 64,2 s o piso de 480 s e inalcancavel. Saiu em
~560 s.

EIXO NOVO. Os oito anteriores falam de 8th Pay Commission, regime tributario,
EPF (duas vezes), CTC contra liquido, dinheiro na ficha, gratuidade e prazo do
ITR. NENHUM fala do CONFRONTO entre o que o empregador declara e o que o
Departamento de Imposto de Renda registra. Este fala.

FONTE, E AQUI EU PRECISO SER EXPLICITO SOBRE UMA LIMITACAO REAL: este pacote
sustenta-se em UMA instituicao, nao duas. Medi seis hosts indianos e o estado e
este:

    incometax.gov.in (portal e-filing)   200, 11.738 chars na raiz e 30.885 na
                                         pagina de ajuda — SERVE
    pfrda.org.in                         200, 14.853 chars — serve, mas e outro
                                         assunto (NPS), nao TDS
    pib.gov.in                           200, 5.777 chars — so manchetes
    incometaxindia.gov.in (a LEI)        403
    epfindia.gov.in                      403
    indiacode.nic.in                     200 com 249 chars (vazio)
    egazette.gov.in / cag.gov.in         timeout
    tdscpc.gov.in                        200 com 62 chars (app JS)

Ou seja: o orgao que APLICA serve e o publicador do TEXTO da lei nao serve. Nao
existe, para a India, o par que o aprendizado 600 descreve — nem terceiro nivel
supranacional, porque lei tributaria indiana nao tem um.

POR QUE EU SEGUI MESMO ASSIM, e o criterio e o da propria rotina: "pauta cujo
numero nao fecha em fonte oficial deve ser redesenhada para que o numero que
decide seja o DO ESPECTADOR". Aqui os DOIS numeros que decidem sao dele — o
total de TDS no Form 16 dele e o total no 26AS/AIS dele — e eu nao cito NENHUM
numero medido. O que tomo do portal e: qual e o nome completo de cada
formulario, sob qual secao ele existe, QUEM o emite e para quem, e o caminho de
navegacao. Isso e identificacao e navegacao, nao medicao, e o emissor e a unica
autoridade possivel sobre os proprios formularios.

O QUE EU NAO CITO, de proposito: nenhuma aliquota, nenhum slab, nenhuma data de
entrega (mudam por notificacao do CBDT e eu nao consigo verificar a vigente em
duas fontes com o egazette em timeout), nenhum limite de deducao — nem o 14% do
80CCD(2) que esta na mesma pagina — e nenhum valor de limite basico de isencao.
O video diz explicitamente que nao vai dar esses numeros.

ALAVANCA B: resposta na cena 10, ~128 s estimados. Residuo da
`hi-IN-MadhurNeural` e -0,2% com n=... (ensaio.py) — praticamente nulo; a conta
corrigida esta no rodape e vai ser conferida no legendas.srt (aprendizado 604,
que ja levou uma temperada: dois pontos, 0,1 s e 4,6 s).

THUMB com `l1`/`l2` e HASHTAGS com a do canal, como 003, 005, 006, 007, 008 e
009 — seis dos sete que tem hashtag. O 010, meu, de hoje de manha, trocou a
chave do thumb para `linhas` E tirou a hashtag do canal. Quarto canal seguido em
que o pacote anterior e meu e esta fora do padrao: aprendizado 601.

TITULO PROPRIO DO SHORT: tem (aprendizado 548). So o 009 e o 010 tinham.
"""

import json

CENAS = []

BROLL = {
    7821605: ("https://videos.pexels.com/video-files/7821605/7821605-hd_1280_720_30fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/top-view-of-a-documents-7821605/"),
    6862869: ("https://videos.pexels.com/video-files/6862869/6862869-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/person-using-a-laptop-6862869/"),
    7821607: ("https://videos.pexels.com/video-files/7821607/7821607-hd_1280_720_30fps.mp4",
              "RDNE Stock project",
              "https://www.pexels.com/video/close-up-video-of-a-documents-7821607/"),
    7597301: ("https://videos.pexels.com/video-files/7597301/7597301-hd_1366_720_25fps.mp4",
              "cottonbro studio",
              "https://www.pexels.com/video/two-women-sitting-together-revising-a-document-7597301/"),
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


def C(kicker, sub, nar):
    CENAS.append({"layout": "cta", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


# ===================== पहले दो सौ सेकंड ====================================

# -------------------------------------------------------------------- cap 1
B("तीन कागज़", "एक ही टीडीएस",
  "आपकी तनख़्वाह से कटे टीडीएस के बारे में तीन अलग कागज़ होते हैं, और तीनों "
  "अलग-अलग लोग बनाते हैं। यही बात सबसे ज़्यादा उलझन पैदा करती है।",
  "top view of documents on a desk", 7821605,
  cap="तीन कागज़, और हर एक का बनाने वाला अलग")
T("कौन कौन", "तीन दिशाएँ",
  "पहला वह है जो आप अपने नियोक्ता को देते हैं। दूसरा वह जो नियोक्ता आपको देता "
  "है। और तीसरा वह जो आयकर विभाग अपने पास रखता है।")
T("एक ही पैसा", "तीन रिकॉर्ड",
  "तीनों एक ही पैसे की बात करते हैं। और दिक्कत तब शुरू होती है जब वे आपस में "
  "नहीं मिलते, क्योंकि फिर सवाल यह है कि किसका आंकड़ा चलेगा।")
T("जो नहीं बताऊँगा", "कोई दर नहीं",
  "यह वीडियो कोई दर नहीं बताएगा, कोई स्लैब नहीं, और कोई अंतिम तारीख़ नहीं। वे "
  "हर साल बदलते हैं और आपकी स्थिति पर निर्भर हैं।")
T("जो बताऊँगा", "कौन, कहाँ, कैसे",
  "यह बताएगा कौन सा कागज़ किसने बनाया, वह कहाँ मिलता है, और दो आंकड़ों का "
  "मिलान कैसे किया जाता है। बस इतना।")
T("दोनों आंकड़े आपके", "मेरा एक भी नहीं",
  "और ध्यान दीजिए: मिलान के दोनों आंकड़े आपके ही कागज़ों से आते हैं। मेरा कोई "
  "नंबर इस हिसाब में नहीं घुसता।")

# -------------------------------------------------------------------- cap 2
B("पहली जगह", "आपका फ़ॉर्म सोलह",
  "मिलान दो जगहों से होता है। पहली जगह आपका फ़ॉर्म सोलह है, जो नियोक्ता ने "
  "दिया। उसमें काटे गए टीडीएस का कुल जोड़ देखिए।",
  "person using a laptop at a desk", 6862869,
  cap="मिलान कैसे करें: दो जगह, एक घटाव")
T("दूसरी जगह", "विभाग का रिकॉर्ड",
  "दूसरी जगह आयकर विभाग का अपना रिकॉर्ड है, जो ई-फाइलिंग पोर्टल पर रहता है। "
  "वहाँ भी वही कुल लिखा होता है।")
T("पोर्टल का रास्ता", "छब्बीस ए एस",
  "पोर्टल पर रास्ता यह है: लॉगिन कीजिए, फिर ई-फाइल, फिर इनकम टैक्स रिटर्न, और "
  "फिर व्यू फ़ॉर्म छब्बीस ए एस।")
T("ए आई एस का रास्ता", "और छोटा है",
  "ए आई एस का रास्ता छोटा है। पोर्टल पर लॉगिन करने के बाद सीधे ए आई एस खोलिए। "
  "दोनों जगह वही स्रोत पर काटा गया कर दर्ज रहता है।")
T("अब घटाइए", "एक ही क्रिया",
  "अब घटाइए। नियोक्ता के कागज़ का कुल, घटा विभाग के रिकॉर्ड का कुल। अगर शून्य "
  "आता है, आपका काम यहीं ख़त्म हो गया।")
T("यही पूरा जवाब", "दो कागज़, एक घटाव",
  "यही पूरा जवाब है। दो कागज़, एक घटाव, और कोई भी आंकड़ा बाहर से नहीं आया। "
  "आगे का हिस्सा बताता है हर कागज़ किसका है, और वह क्यों मायने रखता है।")

# ======================= जवाब के बाद ========================================

# -------------------------------------------------------------------- cap 3
T("फ़ॉर्म सोलह", "पूरा नाम",
  "फ़ॉर्म सोलह का पूरा नाम है: वेतन पर स्रोत पर काटे गए कर का प्रमाणपत्र। यह "
  "आयकर अधिनियम की धारा दो सौ तीन के तहत आता है।",
  cap="फ़ॉर्म सोलह: नियोक्ता का प्रमाणपत्र")
T("किसने दिया", "नियोक्ता ने",
  "विभाग के पोर्टल पर साफ़ लिखा है कि इसे नियोक्ता अपने कर्मचारी को देता है, "
  "और वित्तीय वर्ष के अंत में देता है।")
T("उसमें क्या है", "तीन चीज़ें",
  "उसमें तीन चीज़ें दर्ज होती हैं: कर्मचारी की आय, कटौतियाँ और छूट, और स्रोत "
  "पर काटा गया कर। किस लिए? देय या वापसी योग्य कर की गणना के लिए।")
T("यह प्रमाणपत्र है", "दावा नहीं",
  "ध्यान दीजिए कि पोर्टल इसे प्रमाणपत्र कहता है। यानी नियोक्ता प्रमाणित करता "
  "है कि उसने काटा। यह उसका अपना कथन है।")
T("काटना और जमा करना", "दो अलग काम",
  "और यहाँ वह बात है जो पूरे वीडियो की धुरी है: काटना एक काम है और विभाग में "
  "जमा करना दूसरा काम है। एक हुआ, इससे दूसरा अपने आप नहीं होता।")
T("इसलिए मिलान", "और इसलिए ज़रूरी",
  "इसीलिए मिलान का कोई विकल्प नहीं है। जो कटा वह आपकी पर्ची में दिखता है; जो "
  "जमा हुआ वह विभाग के रिकॉर्ड में दिखता है।")

# -------------------------------------------------------------------- cap 4
T("दूसरा कागज़", "किसने बनाया",
  "फ़ॉर्म छब्बीस ए एस और ए आई एस को कौन बनाता है? पोर्टल पर जवाब एक पंक्ति में "
  "है, और वह पंक्ति महत्वपूर्ण है: आयकर विभाग।",
  cap="छब्बीस ए एस और ए आई एस: विभाग का रिकॉर्ड")
T("फ़र्क छोटा नहीं", "दूसरा लेखक",
  "यह फ़र्क छोटा लगता है और छोटा नहीं है। यह कागज़ आपके नियोक्ता ने नहीं बनाया, "
  "इसलिए यह उसके कथन की जाँच का काम कर सकता है।")
T("इसमें क्या दर्ज है", "जो पहुँचा",
  "इसमें जो दर्ज रहता है वह है स्रोत पर काटा या वसूला गया कर। यानी वह हिस्सा "
  "जिसके बारे में विभाग के पास अपनी जानकारी है।")
T("ए आई एस में ज़्यादा", "चार और चीज़ें",
  "ए आई एस में इससे ज़्यादा भी होता है: एस एफ टी सूचना, करों का भुगतान, और "
  "मांग तथा वापसी से जुड़ी जानकारी।")
T("और भी", "कार्यवाही और जी एस टी",
  "और कुछ और भी: लंबित या पूरी हुई कार्यवाही, जी एस टी सूचना, और विदेशी सरकार "
  "से प्राप्त सूचना। यह सब पोर्टल पर सूचीबद्ध है।")
T("तो ए आई एस क्या है", "विभाग की सूची",
  "इसलिए ए आई एस को सिर्फ़ टीडीएस का कागज़ समझना कम आँकना है। वह आपके बारे में "
  "विभाग के पास जो जानकारी है, उसकी सूची है।")

# -------------------------------------------------------------------- cap 5
T("उल्टी दिशा", "जो आप देते हैं",
  "अब वह कागज़ जो उल्टी दिशा में जाता है। यानी जो आप नियोक्ता को देते हैं, और "
  "जिसे न देना सबसे आम चूक है।",
  cap="फ़ॉर्म बारह बी बी: जो आप देते हैं")
T("पूरा नाम", "दावों का विवरण",
  "फ़ॉर्म बारह बी बी का पूरा नाम है: कर की कटौती के लिए कर्मचारी द्वारा किए गए "
  "दावों का विवरण। यह धारा एक सौ बानवे के तहत आता है।")
T("दिशा", "कर्मचारी से नियोक्ता",
  "और दिशा उलटी है: इसे कर्मचारी अपने नियोक्ता को देता है। नियोक्ता आपको नहीं "
  "देता। यह आपकी ज़िम्मेदारी है।")
T("उसमें क्या जाता है", "तीन सबूत",
  "उसमें क्या जाता है: मकान किराया भत्ता, छुट्टी यात्रा रियायत, और गृह ऋण के "
  "ब्याज की कटौती के सबूत या विवरण।")
T("और", "कर बचत के दावे",
  "और कर बचत के दावे भी, यानी उन पात्र भुगतानों या निवेशों का विवरण जिनके आधार "
  "पर कटौती मिलती है।")
T("किस लिए", "कटौती से पहले",
  "किस लिए? पोर्टल का शब्द साफ़ है: स्रोत पर काटे जाने वाले कर की गणना के लिए। "
  "यानी यह कागज़ कटौती के बाद नहीं, पहले काम करता है।")

# -------------------------------------------------------------------- cap 6
B("चौथा कागज़", "वेतन के बाहर",
  "एक चौथा कागज़ है जिसे वेतन पाने वाले लोग अक्सर जानते ही नहीं, और वह है "
  "फ़ॉर्म सोलह ए।",
  "close up of documents on a table", 7821607,
  cap="फ़ॉर्म सोलह ए: वेतन के बाहर का टीडीएस")
T("यह भी दो सौ तीन", "पर दूसरी आय पर",
  "यह भी धारा दो सौ तीन का प्रमाणपत्र है, लेकिन वेतन के अलावा की आय पर काटे गए "
  "कर के लिए। यही अंतर पूरा मायने रखता है।")
T("कौन देता है", "काटने वाला",
  "इसे कौन देता है? काटने वाला, उसे जिसका काटा गया। यानी आपका बैंक, कोई कंपनी, "
  "या कोई और भुगतानकर्ता।")
T("एक बड़ा अंतर", "हर तिमाही",
  "और एक अंतर जो फ़ॉर्म सोलह से बिल्कुल अलग है: पोर्टल कहता है यह हर तिमाही "
  "जारी होता है। साल में एक बार नहीं।")
T("उसमें क्या है", "तीन बातें",
  "उसमें टीडीएस की रक़म, भुगतान की प्रकृति, और आयकर विभाग में जमा किए गए टीडीएस "
  "भुगतान दर्ज होते हैं।")
T("नतीजा", "सिर्फ़ सोलह काफ़ी नहीं",
  "इसलिए अगर आपकी बचत पर ब्याज आता है, तो आपका पूरा टीडीएस सिर्फ़ फ़ॉर्म सोलह "
  "में नहीं है। एक हिस्सा दूसरे कागज़ में है, और वह हिस्सा विभाग के रिकॉर्ड "
  "में भी दिखेगा।")

# -------------------------------------------------------------------- cap 7
T("और अगर कटना ही नहीं चाहिए था", "दो घोषणाएँ",
  "और अगर ब्याज पर टीडीएस कटना ही नहीं चाहिए था? उसके लिए पोर्टल दो घोषणाएँ "
  "सूचीबद्ध करता है, और वे बैंक को दी जाती हैं।",
  cap="पंद्रह जी और पंद्रह एच: बैंक को घोषणा")
T("पंद्रह जी", "किसकी घोषणा",
  "फ़ॉर्म पंद्रह जी निवासी करदाता की घोषणा है, जो कुछ प्राप्तियाँ कर की कटौती "
  "के बिना चाहता है।")
T("कौन दे सकता है", "तीन श्रेणियाँ",
  "कौन दे सकता है: साठ साल से कम उम्र का निवासी व्यक्ति, या एच यू एफ, या कंपनी "
  "और फ़र्म के अलावा कोई अन्य व्यक्ति।")
T("पंद्रह एच", "उम्र से तय",
  "फ़ॉर्म पंद्रह एच वही काम करता है, पर उनके लिए जिनकी उम्र साठ साल या उससे "
  "अधिक है। अंतर सिर्फ़ उम्र का है।")
T("किस लिए", "ब्याज पर कटौती न हो",
  "दोनों बैंक को दिए जाते हैं, ताकि ब्याज आय पर टीडीएस न काटा जाए — और शर्त यह "
  "है कि आय मूल छूट सीमा से नीचे हो।")
T("वह सीमा", "मैंने नहीं बताई",
  "ध्यान दीजिए कि मैंने वह सीमा नहीं बताई, और जान-बूझकर नहीं बताई। वह बदलती है "
  "और आपकी श्रेणी पर निर्भर है। उसे अपने लिए देखिए।")

# -------------------------------------------------------------------- cap 8
B("अब करने की चीज़", "पाँच मिनट",
  "अब सब एक जगह, क्योंकि करने की चीज़ एक ही है और उसमें पाँच मिनट लगते हैं।",
  "two people revising a document together", 7597301,
  cap="आज क्या करें, और किससे बात करें")
T("पहला कदम", "एक संख्या",
  "फ़ॉर्म सोलह निकालिए और उसमें काटे गए टीडीएस का कुल जोड़ लिख लीजिए। एक "
  "कागज़, एक संख्या।")
T("दूसरा कदम", "दूसरी संख्या",
  "पोर्टल पर लॉगिन कीजिए और छब्बीस ए एस या ए आई एस से वही कुल निकालिए। यह "
  "दूसरी संख्या है।")
T("तीसरा कदम", "घटाव",
  "दोनों को घटाइए। बराबर हैं तो बात ख़त्म। अलग हैं तो पहली बातचीत नियोक्ता से "
  "है, किसी और से नहीं।")
T("क्यों नियोक्ता से", "जमा उसने किया",
  "क्यों नियोक्ता से? क्योंकि जो विभाग के रिकॉर्ड में है वह काटने वाले द्वारा "
  "जमा किया गया है। उस प्रविष्टि को आप स्वयं नहीं बदल सकते।")
T("और अगर बात न बने", "तब पेशेवर",
  "और अगर नियोक्ता से बात करने पर भी अंतर बना रहे, तो आगे का कदम किसी कर "
  "पेशेवर का है। यह वीडियो वहाँ तक नहीं जाता।")
C("टिप्पणी में", "बस एक शब्द",
  "टिप्पणी में बस एक शब्द लिखिए: बराबर, या अलग। रक़म नहीं, कंपनी का नाम नहीं, "
  "और कोई निजी जानकारी नहीं।")

# ================================== SHORT ====================================

SHORT = [
    {"layout": "titulo", "kicker": "दो आंकड़े", "sub": "एक ही टीडीएस",
     "nar": "आपके टीडीएस के दो आंकड़े हैं। एक नियोक्ता देता है, दूसरा विभाग "
            "रखता है।",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "पहला", "sub": "फ़ॉर्म सोलह",
     "nar": "फ़ॉर्म सोलह नियोक्ता का प्रमाणपत्र है। उसमें कटे टीडीएस का कुल "
            "जोड़ होता है।",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "दूसरा", "sub": "छब्बीस ए एस",
     "nar": "छब्बीस ए एस और ए आई एस विभाग बनाता है, ई-फाइलिंग पोर्टल पर।",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "अब घटाइए", "sub": "एक क्रिया",
     "nar": "दोनों घटाइए। बराबर हैं तो बात ख़त्म; अलग हैं तो नियोक्ता से "
            "बात कीजिए।",
     "sem_cap": True},
    {"layout": "cta", "kicker": "क्यों नियोक्ता से", "sub": "और दो कागज़ और",
     "nar": "जमा उसी ने किया, इसलिए वही सुधार सकता है। दो कागज़ और हैं — "
            "वीडियो में।",
     "sem_cap": True},
]

THUMB = {"l1": "दो आंकड़े", "l2": "एक ही टीडीएस"}

COPY = """# कटे टीडीएस के दो आंकड़े: एक नियोक्ता देता है, दूसरा विभाग रखता है — मिलान कीजिए

## TITULO
टीडीएस के दो आंकड़े: फ़ॉर्म सोलह और छब्बीस ए एस का मिलान अपने ही कागज़ों से

## TITULO SHORT
टीडीएस: आपके दो आंकड़े मिलते हैं?

## DESCRICAO
आपकी तनख़्वाह से कटे टीडीएस के बारे में तीन अलग कागज़ होते हैं, और तीनों अलग-अलग लोग बनाते हैं। पहला वह है जो आप नियोक्ता को देते हैं, दूसरा वह जो नियोक्ता आपको देता है, और तीसरा वह जो आयकर विभाग अपने पास रखता है। तीनों एक ही पैसे की बात करते हैं, और दिक्कत तब शुरू होती है जब वे आपस में नहीं मिलते।

इस वीडियो का तरीक़ा पाँच मिनट का है और उसमें मेरा कोई नंबर नहीं लगता। फ़ॉर्म सोलह निकालिए और उसमें काटे गए टीडीएस का कुल जोड़ लिख लीजिए। फिर ई-फाइलिंग पोर्टल पर लॉगिन करके वही कुल विभाग के रिकॉर्ड से निकालिए — छब्बीस ए एस का रास्ता है लॉगिन, ई-फाइल, इनकम टैक्स रिटर्न, व्यू फ़ॉर्म छब्बीस ए एस; और ए आई एस का रास्ता है लॉगिन के बाद सीधे ए आई एस। अब दोनों को घटाइए। बराबर हैं तो बात ख़त्म; अलग हैं तो पहली बातचीत नियोक्ता से है, क्योंकि जो विभाग के रिकॉर्ड में है वह काटने वाले द्वारा जमा किया गया है और उस प्रविष्टि को आप स्वयं नहीं बदल सकते।

जवाब के बाद वीडियो हर कागज़ को अलग-अलग खोलता है, सीधे विभाग के पोर्टल पर लिखी परिभाषाओं से। फ़ॉर्म सोलह धारा दो सौ तीन के तहत वेतन पर स्रोत पर काटे गए कर का प्रमाणपत्र है, जिसे नियोक्ता वित्तीय वर्ष के अंत में कर्मचारी को देता है। फ़ॉर्म छब्बीस ए एस और ए आई एस आयकर विभाग बनाता है — और ए आई एस में टीडीएस के अलावा एस एफ टी सूचना, करों का भुगतान, मांग और वापसी, लंबित या पूरी हुई कार्यवाही, जी एस टी सूचना तथा विदेशी सरकार से मिली सूचना भी होती है। फ़ॉर्म बारह बी बी धारा एक सौ बानवे के तहत वह विवरण है जो कर्मचारी नियोक्ता को देता है, कटौती की गणना से पहले। फ़ॉर्म सोलह ए वेतन के अलावा की आय पर कटे कर का प्रमाणपत्र है और हर तिमाही जारी होता है। और फ़ॉर्म पंद्रह जी तथा पंद्रह एच वे घोषणाएँ हैं जो बैंक को दी जाती हैं, ताकि ब्याज आय पर टीडीएस न कटे, यदि आय मूल छूट सीमा से नीचे हो — पंद्रह जी साठ साल से कम के लिए, पंद्रह एच साठ या उससे अधिक के लिए।

एक ज़रूरी सीमा, जो इस हिसाब से भी बड़ी है: यह कर सलाह नहीं है, यह आपका रिटर्न नहीं भरता, और यह तय नहीं करता कि आपका कर कितना है। वीडियो जान-बूझकर कोई दर, कोई स्लैब, कोई अंतिम तारीख़ और कोई छूट सीमा नहीं बताता, क्योंकि वे बदलते हैं और आपकी श्रेणी पर निर्भर हैं। अगर मिलान में अंतर मिले और नियोक्ता से बात करने पर हल न हो, तो वह किसी कर पेशेवर का काम है।

CAPITULOS
{CAPITULOS}

टिप्पणी में बस एक शब्द लिखिए: बराबर, या अलग। रक़म नहीं, कंपनी का नाम नहीं, कोई निजी जानकारी नहीं।

## DISCLOSURE
इस वीडियो की आवाज़ और ग्राफ़िक्स कंप्यूटर से बनाए गए हैं। पाठ मौलिक है और सामग्री सूचनात्मक है; यह कर या कानूनी सलाह नहीं है।

## HASHTAGS
#TDS #फ़ॉर्म16 #AglaLevel

## TAGS
TDS, Form 16, Form 26AS, AIS, Annual Information Statement, Form 12BB, Form 16A, Form 15G, Form 15H, TDS mismatch, income tax portal, e-filing portal, salary TDS, TDS reconciliation, dhara 203

## COMENTARIO FIXADO
पूरा तरीक़ा दो पंक्तियों में: फ़ॉर्म सोलह से काटे गए टीडीएस का कुल जोड़ लिखिए, फिर ई-फाइलिंग पोर्टल पर लॉगिन करके छब्बीस ए एस या ए आई एस से वही कुल निकालिए, और दोनों को घटाइए। बराबर हैं तो काम ख़त्म। अलग हैं तो बातचीत नियोक्ता से कीजिए — क्योंकि विभाग के रिकॉर्ड में जो है वह काटने वाले ने जमा किया है, और उस प्रविष्टि को आप स्वयं नहीं बदल सकते।

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Este video NAO cita nenhuma aliquota, nenhum slab, nenhuma data de entrega, nenhum limite de deducao e nenhum valor de limite basico de isencao — e diz isso em voz alta no capitulo 1 e de novo no capitulo 7. Os UNICOS numeros citados sao identificadores: os nomes dos formularios (dezesseis, dezesseis A, doze B B, vinte e seis A S, quinze G, quinze H), as secoes da lei sob as quais eles existem (duzentos e tres para os certificados de TDS, cento e noventa e dois para o doze B B), a periodicidade trimestral do dezesseis A, e a idade de sessenta anos que separa o quinze G do quinze H. Nome de formulario, numero de secao, periodicidade e limiar de idade nao sao medicoes.

OS DOIS NUMEROS QUE DECIDEM SAO DO ESPECTADOR: o total de TDS no Form 16 dele e o total no 26AS ou AIS dele. A operacao e uma subtracao.

UMA LIMITACAO REAL DA FONTE, declarada porque e relevante: este pacote sustenta-se em UMA instituicao, nao duas. Medi oito hosts indianos nesta rodada. Serve o `incometax.gov.in`, que e o portal do orgao que APLICA (11.738 chars na raiz, 30.885 na pagina de ajuda de onde saiu tudo que o video afirma). NAO servem os publicadores do TEXTO da lei: `incometaxindia.gov.in` da 403, `indiacode.nic.in` devolve 249 chars vazios, `egazette.gov.in` e `cag.gov.in` dao timeout, `epfindia.gov.in` da 403, `tdscpc.gov.in` e app JavaScript com 62 chars e `pib.gov.in` so tem manchetes. O `pfrda.org.in` serve, mas e outro assunto. Ou seja: para a India nao existe hoje, pela sandbox, o par "orgao que aplica mais publicador do texto".

POR QUE SEGUI MESMO ASSIM, pelo criterio da propria rotina: pauta cujo numero nao fecha em fonte oficial deve ser redesenhada para que o numero que decide seja o DO ESPECTADOR. Foi o que fiz. Do portal eu tomo apenas QUEM emite cada formulario, PARA QUEM, sob qual secao, e o caminho de navegacao — identificacao e navegacao, nao medicao — e o emissor e a unica autoridade possivel sobre os proprios formularios. Nenhuma afirmacao do video depende de um numero que eu nao pudesse cruzar, porque o video nao cita numero que precise de cruzamento.

O QUE FOI DESCARTADO: (1) o limite de 14% do salario do 80CCD(2), que esta na MESMA pagina e eu nao uso porque e medicao de fonte unica; (2) toda data de entrega de ITR, porque muda por notificacao do CBDT e o egazette esta em timeout; (3) a afirmacao de que o registro do 26AS e construido a partir da declaracao de TDS do empregador — o portal afirma isso explicitamente do Form 16A ("TDS Payments deposited with the Income Tax Department"), e para o salario eu digo apenas que o que esta no registro foi JAMADO pelo deductor, sem descrever o mecanismo que nao li; (4) qualquer orientacao de como corrigir a declaracao, que e trabalho do empregador e de um profissional.

## FONTES
Income Tax Department, India — e-Filing portal, pagina de ajuda do contribuinte individual (incometax.gov.in/iec/foportal/help/individual): "Forms Applicable (As per Income Tax Act, 1961)" — Form 12BB (u/s 192, An Employee to his Employer(s)); Form 16 (Certificate of Tax Deducted at Source on Salary, u/s 203, An Employer(s) to his Employee at the end of the financial year); Form 16A (Certificate u/s 203 for TDS on Income other than Salary, Deductor to Deductee, issued quarterly); Form 26AS e AIS (Annual Information Statement) — "Provided by: Income Tax Department", com os caminhos de navegacao; Form 15G e Form 15H (declaracoes ao banco para nao deducao de TDS sobre juros).
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/agla-level-011.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "agla-level",
    "pacote": "agla-level-011",
    "idioma": "hi",
    "voz": "hi-IN-MadhurNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1D2D44", "c1": "#B23A48", "c2": "#E9A03B",
               "bg": "#F5F2EA"},
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
    grava(SPEC, "fabrica/specs/agla-level-011.json")
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
    RESIDUO = 0.998   # hi-IN-MadhurNeural, -0,2% no ensaio.py
    t = 0.0
    for i, c in enumerate(CENAS):
        t += duracao_cena(c.get("nar", ""), SPEC["voz"])
        if "अगर शून्य" in (c.get("nar") or ""):
            print(f"  a resposta fecha em {t:.1f}s cru -> "
                  f"{t * RESIDUO:.1f}s corrigido (cena {i})")
    for i, c in enumerate(CENAS):
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll cena {i}: {dd:.1f}s -> pede {dd + 3.0:.1f}s: "
                  f"{c['broll_q']}")
