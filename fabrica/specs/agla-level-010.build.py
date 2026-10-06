"""agla-level-010 — ग्रेच्युटी: a conta que o proprio espectador faz na percia dele.

ALAVANCA ATACADA: A (conversao short -> inscrito), pela FORMA do pacote.

O NUMERO DE PARTIDA, do PROPRIO canal e com a ultima leitura de `metricas`
(aprendizado 592 — nunca mais `max(views)`):

    pacote  short -> longo   eixo
    004        28 -> 26      8th Pay Commission, fator de ajuste
    005        26 ->  0      prazo do ITR, multa e juros
    003        19 ->  4      EPF, regra dos 36 meses
    006        11 ->  2      EPFO 3.0, limites de saque
    008         8 ->  4      CTC contra salario na mao
    007         0 ->  7      regime velho contra novo
    009         0 ->  0      dinheiro parado na percia (publicado 04/10, 2 dias)

O QUE DEU CERTO: o 004 e o unico pacote do canal em que o longo quase igualou
o short — vinte e oito contra vinte e seis, 93% de cruzamento, e sozinho
responde por 26 das 43 views de longo do canal. O titulo dele tem exatamente a
forma que o aprendizado 589 mediu na frota: ENTIDADE BUSCAVEL NOMEADA, numero,
dois-pontos, e nenhuma interrogacao.

O QUE NAO DEU: o 005 teve o segundo maior short do canal — vinte e seis views —
e ZERO no longo. Ele entrega FATO datado sobre o mundo (o prazo passou, a multa
e esta), e nao conta que a pessoa faca. E o 007 abre com pergunta no titulo,
que e o traco do terco de BAIXO no 589.

O QUE VOU MUDAR, e e uma coisa so: copiar a FORMA do 004 e nao o assunto dele.
Entidade nomeada e buscavel no titulo (ग्रेच्युटी), numero no titulo, dois-pontos,
zero interrogacao — e o corpo entrega uma conta que termina num numero do
espectador, nao num numero meu.

EIXO, e por que ele e novo. Os sete pacotes do canal falam de EPF/EPFO (003,
006), de Comissao de Pagamento (004), de imposto (005, 007) e de composicao do
salario (008, 009). NENHUM fala do que o tempo de casa ja acumulou. Este fala:
a gratuidade nao e bonus, e uma conta com duas bordas duras, e as duas bordas
sao decididas por numeros que so a pessoa tem.

VEREDITO DO CANAL: `canal frio` (v_maquina_licoes, 6 shorts e 6 longos medidos,
135 views no total). Pela rotina isso manda eixo novo e PISO de 8 minutos. Este
pacote fica no piso de proposito — alavanca B: o longo e dimensionado para o
piso da faixa, nunca para o teto.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# ENTRAM NO VIDEO, conferidos em DUAS fontes institucionais que batem:
#
#   * cinco anos de servico continuo como condicao — Payment of Gratuity Act,
#     1972, secao 4(1). indiacode.nic.in (texto da secao 4) e labour.gov.in
#     (PDF do Ato).
#   * quinze dias de salario por ano completo de servico, e tambem por fracao
#     SUPERIOR a seis meses — mesma secao 4, mesmas duas fontes.
#   * para o mensalista, os quinze dias saem dividindo o salario mensal por
#     vinte e seis e multiplicando por quinze — mesma secao 4, mesmas fontes.
#
# DESCARTADO, e por que: o TETO legal da gratuidade NAO entra como numero. As
# duas fontes confirmam que existe um limite maximo, mas a cifra dele muda por
# notificacao e eu nao a fechei em duas fontes oficiais DENTRO desta rodada. O
# video afirma que o teto existe e manda a pessoa conferir o valor vigente; nao
# diz quanto e. Isso nao enfraquece a conta, porque quem esta abaixo do teto —
# que e a maioria de quem assiste a este canal — chega no mesmo numero com ou
# sem a cifra.
#
# TAMBEM FORA, de proposito: nao digo se os Codigos Trabalhistas mudaram a regra
# (nao conferi), nao cito aliquota de imposto sobre a gratuidade, nao digo se
# contrato temporario conta, e nao dou conselho sobre pedir demissao antes ou
# depois de uma data. O video precifica; nao aconselha.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: o salario mensal da ultima pericia
# (basico mais DA) e os meses completos de casa. Os dois estao na pericia e na
# carta de nomeacao dele, e nenhum deles e meu.
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


# O LINK FICA NA SPEC, nao na busca em tempo de render. Resolvido em 06/10/2026
# pela busca por `pg_net` DENTRO do banco: o `prebusca_broll.py` rodado da
# sandbox parou em "chave do Pexels: AUSENTE" (o passo do workflow nao exporta
# os secrets), e a chave mora em `config.pexels_api_key` — entao a busca saiu
# de onde a chave esta. Do meu runner o proxy devolve 403 para api.pexels.com.
#
# Com o link gravado o pacote fica REPRODUZIVEL: sem ele, dois renders da mesma
# spec pegam clipes diferentes, porque o Pexels reordena a busca.
#
# CADA CLIPE FOI ESCOLHIDO CONTRA O QUE A NARRACAO DIZ, nao pelo termo da
# busca. O primeiro candidato da terceira cena era "a person using a calculator
# and counting CASH" — e a narracao ali manda contar MESES, nao dinheiro.
# Trocado pelo 6963484, que e so a calculadora. Ja errei isso tres vezes.
BROLL = {
    8731564: ("https://videos.pexels.com/video-files/8731564/8731564-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/a-man-signing-the-documents-8731564/"),
    1793371: ("https://videos.pexels.com/video-files/1793371/1793371-hd_1280_720_30fps.mp4",
              "Miguel Á. Padriñán",
              "https://www.pexels.com/video/person-saving-a-date-on-his-planner-1793371/"),
    6963484: ("https://videos.pexels.com/video-files/6963484/6963484-hd_1280_720_25fps.mp4",
              "Mikhail Nilov",
              "https://www.pexels.com/video/a-person-using-a-calculator-6963484/"),
}


def B(kicker, sub, nar, q, pexels_id, cap=None):
    """Abertura de capitulo com footage.

    SEM `broll_url` de proposito: quem o grava e o `prebusca_broll.py` rodado
    da sandbox, onde `api.pexels.com` responde. Do meu runner o proxy devolve
    403 para o host, e do runner do GitHub da TimeoutError. O link entra na
    spec ANTES do disparo do frota.yml, e e isso que torna o pacote
    reproduzivel: sem ele, dois renders da mesma spec pegam clipes diferentes.
    """
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
# A resposta — o numero da pessoa — fecha no fim do capitulo 3. O que vem
# depois refina e protege a conta, mas quem sair aos tres minutos ja sabe
# calcular.

# -------------------------------------------------------------------- cap 1
B("पाँच साल की दहलीज़", "इससे एक दिन कम, और शून्य",
  "नौकरी छोड़ने पर जो रक़म सालों के बदले मिलती है, उसकी पहली शर्त समय है। "
  "और यह शर्त नरम नहीं है।",
  "office worker signing resignation letter desk", 8731564,
  cap="पाँच साल की दहलीज़")
T("शर्त", "लगातार पाँच साल",
  "क़ानून कहता है: लगातार पाँच साल की सेवा पूरी होने पर ही यह रक़म देय होती "
  "है। पाँच साल पूरे, तभी।")
T("इससे कम", "कुछ भी नहीं",
  "चार साल ग्यारह महीने पर यह रक़म शून्य है। ग्यारह महीने आपके पक्ष में कुछ "
  "नहीं जोड़ते, क्योंकि दहलीज़ पार नहीं हुई।")
T("यह क्यों अजीब लगता है", "मेहनत बराबर, नतीजा नहीं",
  "यही बात चुभती है। काम वही रहा, महीने लगभग वही रहे, और नतीजा पूरा बदल "
  "जाता है।")
T("इसलिए पहला काम", "महीने गिनिए, साल नहीं",
  "तो पहला काम साल गिनना नहीं, महीने गिनना है। जुड़ने की तारीख़ से आज तक।")
T("गिनती किस दिन रुकती है", "आख़िरी कार्यदिवस पर",
  "गिनती आख़िरी कार्यदिवस पर रुकती है, इस्तीफ़ा देने के दिन पर नहीं।")
T("वह तारीख़ कहाँ है", "नियुक्ति पत्र पर",
  "जुड़ने की तारीख़ नियुक्ति पत्र पर लिखी है, और वही तारीख़ गिनती शुरू करती "
  "है। याद से नहीं, काग़ज़ से।")

# -------------------------------------------------------------------- cap 2
T("पंद्रह और छब्बीस", "पूरी गिनती इन्हीं दो अंकों पर टिकी है",
  "दहलीज़ पार हो गई, तो रक़म कितनी बनती है। यहाँ से गिनती सिर्फ़ दो अंकों पर "
  "चलती है।",
  cap="पंद्रह और छब्बीस")
T("पहला अंक", "हर पूरे साल के बदले पंद्रह दिन",
  "पहला अंक पंद्रह है। सेवा के हर पूरे साल के बदले पंद्रह दिन का वेतन, यही "
  "क़ानून की भाषा है।")
T("दूसरा अंक", "महीने में छब्बीस",
  "दूसरा अंक छब्बीस है। मासिक वेतन वाले के लिए महीना छब्बीस दिन का माना जाता "
  "है, तीस का नहीं।")
T("दोनों साथ", "भाग छब्बीस, गुणा पंद्रह",
  "तो एक साल का हिस्सा ऐसे निकलता है: मासिक वेतन में छब्बीस का भाग दीजिए, और "
  "जो आया उसे पंद्रह से गुणा कीजिए।")
T("छब्बीस क्यों", "यह चुनाव क़ानून का है",
  "छब्बीस इसलिए कि क़ानून ने यही लिखा है। तीस से भाग देने पर आपका दिन सस्ता "
  "पड़ जाता है।")
T("एक उदाहरण नहीं", "अपनी ही संख्या डालिए",
  "यहाँ कोई मान लिया हुआ वेतन नहीं है। अपनी पर्ची की संख्या डालिए।")
T("अब तक", "एक साल का भाव तैयार",
  "यहाँ तक आपके पास एक साल का भाव है। अब सिर्फ़ यह तय करना बाक़ी है कि आपके "
  "कितने साल गिने जाएँगे।")

# -------------------------------------------------------------------- cap 3
# AQUI FECHA A RESPOSTA. O espectador sai com o proprio numero.
B("छह महीने का नियम", "यहीं एक पूरा साल बनता या टूटता है",
  "सालों की गिनती में एक नियम है जिसे ज़्यादातर लोग नहीं जानते। और यही नियम "
  "आपकी रक़म बदल देता है।",
  "calendar pages turning close up", 1793371,
  cap="छह महीने का नियम")
T("नियम", "छह महीने से ज़्यादा, तो पूरा साल",
  "पूरे साल के बाद बचा हुआ हिस्सा अगर छह महीने से ज़्यादा है, तो वह पूरा एक "
  "साल गिना जाता है।")
T("इसका मतलब", "छह साल सात महीने बराबर सात",
  "यानी छह साल सात महीने की सेवा सात साल गिनी जाती है। और छह साल पाँच महीने "
  "छह ही रहती है।")
T("अब आपकी गिनती", "दो संख्याएँ, और बस",
  "अब आपके पास दो संख्याएँ होनी चाहिए। आख़िरी पर्ची का मासिक वेतन, और ऊपर के "
  "नियम से निकले आपके साल।")
T("गुणा कीजिए", "यही आपका नंबर है",
  "वेतन में छब्बीस का भाग, पंद्रह से गुणा, और फिर अपने सालों से गुणा। जो आया, "
  "वही आपका नंबर है।")
T("ठीक छह महीने", "वह पूरा साल नहीं बनता",
  "और ठीक छह महीने पर क्या होता है। नियम कहता है छह महीने से ज़्यादा, इसलिए "
  "ठीक छह महीने अगला साल नहीं बनाते।")
T("इसे लिख लीजिए", "आगे का हिस्सा इसी को पक्का करता है",
  "इस नंबर को कहीं लिख लीजिए। आगे का वीडियो यही बताता है कि इसमें ग़लती कहाँ "
  "से आती है।")

# -------------------------------------------------------------------- cap 4
T("कौन सा वेतन", "पूरी पर्ची नहीं",
  "सबसे आम ग़लती यहीं होती है। लोग पर्ची का सबसे बड़ा नंबर उठा लेते हैं, और "
  "गिनती ऊपर चली जाती है।",
  cap="कौन सा वेतन गिना जाता है")
T("आख़िरी वेतन", "जो आख़िरी बार लिया",
  "क़ानून आख़िरी बार लिए गए वेतन की बात करता है। यानी पिछले महीने की दर, "
  "शुरुआती साल की नहीं।")
T("घर ले जाने वाली रक़म नहीं", "कटौती से पहले वाली दर",
  "यह हाथ में आने वाली रक़म भी नहीं है। कटौतियाँ घटने के बाद का नंबर इस गिनती "
  "में नहीं जाता।")
T("सीटीसी भी नहीं", "वह तो और बड़ा होता है",
  "और यह सीटीसी भी नहीं है। सीटीसी में वे चीज़ें भी जुड़ी होती हैं जो आपकी "
  "पर्ची तक पहुँचती ही नहीं।")
T("तो क्या", "बुनियादी वेतन और महँगाई भत्ता",
  "इस गिनती का वेतन बुनियादी वेतन और महँगाई भत्ता है। पर्ची पर ये दो लाइनें "
  "अलग दिखती हैं, जोड़ लीजिए।")
T("भत्ते भी नहीं", "यात्रा, मकान, बाक़ी सब बाहर",
  "यात्रा भत्ता, मकान भत्ता और बाक़ी भत्ते इस गिनती से बाहर रहते हैं। वे "
  "पर्ची पर हैं, पर इस हिसाब में नहीं आते।")
T("एक मिनट का काम", "पर्ची निकालिए और जोड़िए",
  "यह एक मिनट का काम है। पिछले महीने की पर्ची निकालिए, दोनों लाइनें जोड़िए, "
  "और वही संख्या गिनती में डालिए।")

# -------------------------------------------------------------------- cap 5
B("दो किनारे", "दोनों तारीख़ पर टिके हैं",
  "अब दो किनारे देखिए। दोनों समय पर टिके हैं, और दोनों आपके अपने काग़ज़ से दिख "
  "जाते हैं।",
  "person counting on calculator at desk", 6963484,
  cap="दो किनारे")
T("पहला किनारा", "पाँच साल की दहलीज़",
  "पहला किनारा पाँच साल है। उसके इस तरफ़ शून्य है और उस तरफ़ पूरी गिनती शुरू "
  "होती है।")
T("दूसरा किनारा", "सातवाँ महीना",
  "दूसरा किनारा हर साल लौटता है। किसी भी पूरे साल के बाद सातवाँ महीना पूरा "
  "होते ही एक और साल जुड़ जाता है।")
T("यह बड़ा क्यों है", "एक साल पूरे भाव का",
  "वह जुड़ा हुआ साल पूरे भाव का होता है। यानी पंद्रह दिन का वेतन, एक महीने के "
  "अंतर पर।")
T("अपने किनारे देखिए", "आप किससे कितनी दूर हैं",
  "तो अपनी गिनती में देखिए: आप इन दोनों किनारों से कितने महीने दूर हैं। यह "
  "दूरी भी एक संख्या है।")
T("दूरी नापिए", "महीनों में, अनुमान में नहीं",
  "यह दूरी महीनों में नापिए, अंदाज़े में नहीं। नियुक्ति की तारीख़ और आज की "
  "तारीख़ के बीच के पूरे महीने गिन लीजिए।")
T("यह फ़ैसला नहीं है", "सिर्फ़ क़ीमत है",
  "यह वीडियो यह नहीं कहता कि इस दूरी का क्या कीजिए। यह सिर्फ़ बताता है कि "
  "दूरी की क़ीमत कितनी है।")

# -------------------------------------------------------------------- cap 6
T("ऊपरी सीमा", "है, और यहाँ उसका अंक नहीं",
  "एक बात साफ़ कह देना ज़रूरी है। इस रक़म पर एक ऊपरी सीमा होती है।",
  cap="ऊपरी सीमा")
T("सीमा का मतलब", "गिनती बड़ी, भुगतान सीमित",
  "सीमा का मतलब है कि गिनती चाहे जितनी बड़ी निकले, क़ानूनी भुगतान एक हद से ऊपर "
  "नहीं जाता।")
T("अंक क्यों नहीं बोला", "दो सरकारी स्रोतों में नहीं मिलाया",
  "उस हद का अंक मैं यहाँ नहीं बोलूँगा। कारण सीधा है: मैंने उसे दो सरकारी "
  "स्रोतों में मिलाकर नहीं देखा।")
T("जो मैंने देखा", "वही बोला",
  "जो दो सरकारी स्रोतों में मिलाकर देखा, वही बोला। पहले दहलीज़, फिर पंद्रह "
  "दिन का भाव। उसके बाद छब्बीस का भाग, और आख़िर में महीनों का नियम।")
T("आपके लिए इसका असर", "ज़्यादातर पर कोई नहीं",
  "ज़्यादातर गिनतियाँ उस हद से नीचे रहती हैं, इसलिए आपका नंबर वही रहता है। "
  "ऊपर निकले, तो वर्तमान हद देख लीजिए।")
T("यह आदत बड़ी है", "अंक बिना स्रोत के मत लीजिए",
  "यह आदत इस एक अंक से बड़ी है। पैसे का कोई भी अंक बिना सरकारी स्रोत के "
  "मत मानिए, चाहे वह कहीं से भी आए।")
T("कहाँ देखें", "श्रम मंत्रालय का पन्ना",
  "वह हद श्रम मंत्रालय के पन्ने पर मिलती है। वहीं से देखिए, किसी वीडियो से "
  "नहीं, मेरे वाले से भी नहीं।")

# -------------------------------------------------------------------- cap 7
T("यह वीडियो क्या नहीं कहता", "सीमाएँ साफ़ रखना ज़रूरी है",
  "अब वह हिस्सा जो आम तौर पर छोड़ दिया जाता है। यह वीडियो किन बातों पर चुप "
  "है।",
  cap="यह वीडियो क्या नहीं कहता")
T("सलाह नहीं", "कब छोड़ें, यह आपका फ़ैसला",
  "यह सलाह नहीं देता कि नौकरी कब छोड़िए। गिनती क़ीमत बताती है, फ़ैसला नहीं "
  "करती।")
T("कर नहीं", "इस पर टैक्स की बात अलग है",
  "यह इस रक़म पर कर की बात भी नहीं करता। वह अलग नियम है और अलग जाँच माँगता "
  "है।")
T("हर नौकरी नहीं", "छोटी इकाइयाँ अलग हो सकती हैं",
  "यह भी नहीं कहता कि हर नौकरी इस क़ानून के दायरे में है। बहुत छोटी इकाइयों पर "
  "नियम अलग हो सकते हैं।")
T("कोई अनुमान नहीं", "आपका नंबर आपके काग़ज़ से",
  "और इसमें मेरा कोई अनुमान नहीं है। हर संख्या या तो क़ानून से आई, या आपकी "
  "अपनी पर्ची से।")
T("समय भी नहीं", "भुगतान कब तक, यह अलग नियम है",
  "यह भी नहीं बताता कि भुगतान कितने दिनों में आना चाहिए। वह अलग धारा है "
  "और उसकी जाँच अलग से कीजिए।")
T("यही इसकी ताक़त है", "भरोसा जाँचने लायक़ हो",
  "यही इस गिनती की ताक़त है। आप हर कड़ी ख़ुद जाँच सकते हैं, और जाँच कर ही "
  "भरोसा कीजिए।")

# -------------------------------------------------------------------- cap 8
T("समेटिए", "चार कड़ियाँ, एक नंबर",
  "अब पूरी गिनती एक बार में। चार कड़ियाँ हैं और वे इसी क्रम में चलती हैं।",
  cap="पूरी गिनती एक बार में")
T("कड़ी एक", "पाँच साल पूरे हुए या नहीं",
  "पहली कड़ी: नियुक्ति की तारीख़ से महीने गिनिए और देखिए कि पाँच साल पूरे हुए "
  "या नहीं।")
T("कड़ी दो", "बुनियादी वेतन जोड़ महँगाई भत्ता",
  "दूसरी कड़ी: पिछले महीने की पर्ची से बुनियादी वेतन और महँगाई भत्ता जोड़िए।")
T("कड़ी तीन", "भाग छब्बीस, गुणा पंद्रह",
  "तीसरी कड़ी: उस जोड़ में छब्बीस का भाग दीजिए और पंद्रह से गुणा कीजिए। यह "
  "एक साल का भाव है।")
T("कड़ी चार", "साल गिनिए, छह महीने के नियम से",
  "चौथी कड़ी: अपने साल गिनिए, और छह महीने से ज़्यादा बचे हिस्से को पूरा साल "
  "मानिए। फिर गुणा कीजिए।")
T("एक बार दोहराइए", "क्रम बदलने पर नतीजा बदलता है",
  "इस क्रम को बदलिए मत। साल पहले गिनिए, भाव बाद में लगाइए, वरना छह महीने "
  "वाला साल गिनती से छूट जाता है।")
C("अपना नंबर नीचे लिखिए", "सिर्फ़ संख्या, वेतन नहीं",
  "टिप्पणी में सिर्फ़ अपना निकाला हुआ नंबर लिखिए, वेतन नहीं। मैं देखना चाहता "
  "हूँ कि छह महीने का नियम कितनों का साल बदलता है।")


# ================================== SHORT ====================================
# O short TAMBEM entrega a conta — nao so a manchete. Aqui ele entrega as
# quatro ligacoes inteiras, porque no 005 a manchete sozinha deu vinte e seis
# views de short e ZERO de longo.

SHORT = [
    {"layout": "titulo", "kicker": "ग्रेच्युटी", "sub": "दो अंक, एक नंबर",
     "nar": "नौकरी के सालों की रक़म दो अंकों पर टिकी है। नंबर निकालिए।",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "पहला", "sub": "पाँच साल पूरे हुए?",
     "nar": "पहला: नियुक्ति की तारीख़ से पाँच साल पूरे हुए या नहीं। कम हैं तो "
            "शून्य।", "sem_cap": True},
    {"layout": "titulo", "kicker": "दूसरा", "sub": "बुनियादी जोड़ महँगाई भत्ता",
     "nar": "दूसरा: पिछली पर्ची का बुनियादी वेतन और महँगाई भत्ता जोड़िए।",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "तीसरा", "sub": "भाग छब्बीस, गुणा पंद्रह",
     "nar": "तीसरा: उसमें छब्बीस का भाग दीजिए, फिर पंद्रह से गुणा। यह एक साल "
            "का भाव है।", "sem_cap": True},
    {"layout": "titulo", "kicker": "चौथा", "sub": "छह महीने से ज़्यादा, पूरा साल",
     "nar": "चौथा: साल गिनिए। छह महीने से ज़्यादा बचा तो पूरा साल। गुणा "
            "कीजिए।", "sem_cap": True},
]


THUMB = {"linhas": ["पंद्रह", "छब्बीस", "आपका नंबर"]}


COPY = """# agla-level-010

## TITULO
ग्रेच्युटी: पंद्रह और छब्बीस की गिनती — और वो छह महीने जो पूरा साल बन जाते हैं

## TITULO SHORT
ग्रेच्युटी: पंद्रह, छब्बीस, आपका नंबर

## DESCRICAO
नौकरी छोड़ने पर सालों के बदले मिलने वाली रक़म — ग्रेच्युटी — एक तयशुदा गिनती है,
अनुमान नहीं। इस वीडियो में वह गिनती चार कड़ियों में खुलती है, और चारों कड़ियाँ आप
अपनी पर्ची और अपने नियुक्ति पत्र से ख़ुद जाँच सकते हैं।

पहली कड़ी समय की है: क़ानून लगातार पाँच साल की सेवा पूरी होने पर ही यह रक़म देय
मानता है। चार साल ग्यारह महीने पर गिनती शून्य रहती है, और यही वह जगह है जहाँ
ज़्यादातर लोग चौंकते हैं।

दूसरी कड़ी वेतन की है, और सबसे ज़्यादा ग़लती यहीं होती है। इस गिनती में न सीटीसी
जाता है, न हाथ में आने वाली रक़म — जाता है आख़िरी बार लिया गया बुनियादी वेतन और
महँगाई भत्ता।

तीसरी कड़ी दो अंकों की है: मासिक वेतन में छब्बीस का भाग, और पंद्रह से गुणा। यही
एक साल का भाव बनता है।

चौथी कड़ी वह है जिसे कम लोग जानते हैं: पूरे साल के बाद अगर छह महीने से ज़्यादा
बचा है, तो वह पूरा एक साल गिना जाता है। इसी वजह से छह साल सात महीने सात साल
गिने जाते हैं और छह साल पाँच महीने छह ही रहते हैं।

वीडियो में कोई अनुमानित आँकड़ा नहीं है। जो संख्याएँ बोली गई हैं वे क़ानून की हैं,
और बाक़ी सब आपकी अपनी पर्ची से आता है। ऊपरी सीमा का अंक जानबूझकर नहीं बोला गया,
क्योंकि उसे दो सरकारी स्रोतों में मिलाकर नहीं देखा गया — वीडियो यह कहता है कि
सीमा मौजूद है और उसका वर्तमान अंक श्रम मंत्रालय के पन्ने पर देखना चाहिए।

यह वीडियो सलाह नहीं देता कि नौकरी कब छोड़िए, कर की गणना नहीं करता, और यह दावा
नहीं करता कि हर नौकरी इस क़ानून के दायरे में आती है।

अध्याय:
00:00 पाँच साल की दहलीज़
01:09 पंद्रह और छब्बीस
02:18 छह महीने का नियम
03:30 कौन सा वेतन गिना जाता है
04:46 दो किनारे
05:59 ऊपरी सीमा
07:16 यह वीडियो क्या नहीं कहता
08:24 पूरी गिनती एक बार में

अपना निकाला हुआ नंबर टिप्पणी में लिखिए — सिर्फ़ संख्या, वेतन नहीं।

## DISCLOSURE
इस वीडियो का वाचन और दृश्य कृत्रिम बुद्धिमत्ता से बनाए गए हैं। आँकड़े सरकारी
स्रोतों से लिए गए हैं और विवरण में उनका ज़िक्र है।

## HASHTAGS
#ग्रेच्युटी #सैलरी #EPF

## TAGS
gratuity, gratuity calculation, payment of gratuity act, 15 26 formula, five years rule, basic plus da, last drawn salary, completed years of service, six months rule, salary slip india, gratuity eligibility, ग्रेच्युटी, ग्रेच्युटी गणना, नौकरी के साल, वेतन पर्ची

## COMENTARIO FIXADO
चार कड़ियाँ: पाँच साल पूरे हुए या नहीं → पिछली पर्ची का बुनियादी वेतन जोड़ महँगाई
भत्ता → छब्बीस का भाग, पंद्रह से गुणा → साल गिनिए, छह महीने से ज़्यादा बचा तो पूरा
साल। अपना नंबर नीचे लिखिए, वेतन नहीं।

## MUSICA / LICENCA
Trilha: Inspired (biblioteca livre do pacote). B-roll: Pexels, crédito por clipe
em broll_creditos.json.

## AVISO SOBRE OS NUMEROS
Este video cita TRES numeros e os tres sao do Payment of Gratuity Act, 1972,
secao 4, conferidos em duas fontes institucionais que batem — indiacode.nic.in
(texto da secao) e labour.gov.in (PDF do Ato): cinco anos de servico continuo
como condicao; quinze dias de salario por ano completo e tambem por fracao
superior a seis meses; e, para o mensalista, divisao do salario mensal por
vinte e seis. DESCARTADO: o teto legal da gratuidade NAO entra como cifra. As
duas fontes confirmam que o teto existe, mas o valor dele muda por notificacao
e eu nao o fechei em duas fontes oficiais nesta rodada — entao o video afirma
que o teto existe, manda conferir no site do Ministerio do Trabalho, e segue.
TAMBEM FORA: nao digo se os Codigos Trabalhistas alteraram a regra, nao calculo
imposto sobre a gratuidade, nao afirmo que toda empresa esta no ambito do Ato e
nao aconselho sobre a data de sair. O numero que decide e do espectador: o
salario da ultima pericia e os meses completos de casa.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/agla-level-010.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "agla-level",
    "pacote": "agla-level-010",
    "idioma": "hi",
    "voz": "hi-IN-MadhurNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#1D2D44", "c1": "#B23A48", "c2": "#E9A03B", "bg": "#F5F2EA"},
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
    grava(SPEC, "fabrica/specs/agla-level-010.json")
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
    for c in CENAS:
        if c.get("layout") == "broll":
            dd = duracao_cena(c.get("nar", ""), SPEC["voz"])
            print(f"  broll {dd:.1f}s -> pede {dd + 3.0:.1f}s: {c['broll_q']}")
