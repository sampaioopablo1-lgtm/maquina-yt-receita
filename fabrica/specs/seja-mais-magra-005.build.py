#!/usr/bin/env python3
"""Monta a spec seja-mais-magra-005.

CANAL. Veredito `suspenso`: 3 longos medidos a 0,00 views/dia, 3 shorts a 7,15
(topo 9,53), 51 views no acervo. A regra do veredito manda o longo NO PISO da
faixa e o melhor material no SHORT — e e o que esta feito.

CANAL DE SAUDE, entao a regra extra vale aqui e nao e formalidade: procurar o
fato REGULATORIO primeiro. Foi neste canal que eu quase publiquei "R$ 18.000"
sem fonte (aprendizados 376 e 377). O antidoto e o mesmo de sempre: afirmar so
o que um orgao decidiu, com data, e dizer em voz alta o que ainda nao se sabe.

EIXO. Os cinco titulos publicados cobrem: produtos "Ozempic natural" proibidos
pela Anvisa, reganho de peso apos Ozempic e Mounjaro, conta por grama de
proteina, e alegacoes permitidas em shake e termogenico. Todos sao sobre o que
NAO funciona ou o que foi PROIBIDO. Este e o primeiro sobre uma APROVACAO — o
mesmo orgao, decisao oposta.

  UMA ADVERTENCIA SOBRE O BANCO, a terceira do dia. O eixo
  `canetas-emagrecedoras` tem 33 outliers e topo de 40.113,4 v/d, mas metade
  das linhas nao e do eixo: "7 Min Abdominais Em Pe", "CAMINHADA EM CASA para
  EMAGRECER 30min", "900 calorias em 30 minutos". Sao videos de treino
  rotulados como caneta emagrecedora. Ordenar por views e pegar o topo levaria
  a pauta para outro nicho (aprendizados 417 e 420).

A PAUTA, datada de QUATRO DIAS ATRAS e inteiramente regulatoria.

  Em 17 de agosto de 2026 a Anvisa registrou duas canetas de semaglutida:

    generico ..... da EMS. E o PRIMEIRO generico de semaglutida em caneta
                   registrado no Brasil.
    similar ...... da Germed, que sera vendido como Semaclique, em quatro
                   apresentacoes de 1,34 mg/mL.

  O detalhe tecnico que explica por que "generico" foi possivel: a semaglutida
  do medicamento de referencia e um BIOLOGICO, e para biologico nao existe a
  figura do generico nos moldes dos sinteticos. A EMS desenvolveu uma versao
  SINTETICA do principio ativo, e e isso que abre a porta regulatoria. A
  referencia do generico e o Ozivy, da propria EMS.

  Conferido em duas passagens de busca com veiculos independentes que batem:
  Correio Braziliense, Poder360, Olhar Digital, Forbes Brasil, O Povo e o
  Conselho Federal de Farmacia — este ultimo, institucional.

O QUE EU NAO VOU AFIRMAR, e a lista importa mais que o roteiro:

  * PRECO. A primeira passagem trouxe "entre R$ 293 e R$ 323" e a propria
    fonte marcava "ainda sem confirmacao". A segunda passagem diz que preco e
    data de chegada as farmacias NAO foram divulgados. Entao o video diz que
    nao se sabe. Numero sem confirmacao neste canal e exatamente o erro dos
    aprendizados 376 e 377.
  * A regra dos 35% eu digo como REGRA GERAL de generico, sem aplicar a um
    valor, porque o preco de referencia depende de aprovacao na CMED.
  * DATA de chegada a farmacia: nao divulgada.
  * Nada de dose, de indicacao ou de "vale a pena". Nao e video de conselho
    medico e o roteiro diz isso.
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
T("Dezessete de agosto", "a Anvisa registrou duas",
  "No dia dezessete de agosto, a Anvisa registrou duas canetas de semaglutida. "
  "Uma delas é a primeira genérica do Brasil.",
  cap="O que a Anvisa registrou, e quando")
I("A genérica", "da EMS",
  "A genérica é da EMS. É o primeiro genérico de semaglutida em caneta "
  "registrado no país.")
I("A outra", "similar, da Germed",
  "A outra é um medicamento similar, da Germed, que será vendido com o nome "
  "Semaclique.")
I("Em quantas versões", "quatro apresentações",
  "O similar foi aprovado em quatro apresentações diferentes, todas na mesma "
  "concentração.")
I("O que é 'similar'", "categoria própria",
  "E vale separar já: similar é uma categoria regulatória própria, com regras "
  "próprias. Não é sinônimo de genérico, embora as duas palavras apareçam "
  "juntas na mesma notícia.")
I("Por que a distinção importa", "as regras de preço diferem",
  "A distinção importa porque as regras que valem para cada categoria são "
  "diferentes, inclusive as de preço. Tratar as duas como a mesma coisa leva "
  "a conclusão errada.")
T("O que eu NÃO vou dizer", "porque ainda não se sabe",
  "Antes de explicar o que isso significa, a parte que quase nunca aparece nos "
  "vídeos sobre isso.")
I("Preço", "não foi divulgado",
  "Eu não vou dizer quanto vai custar. O preço não foi divulgado.")
I("Data na farmácia", "também não",
  "E não vou dizer quando chega à farmácia, porque essa data também não foi "
  "divulgada.")
I("Por que isso importa", "número sem fonte engana",
  "Isso importa porque circula número por aí. Se eu repetir um valor que a "
  "própria fonte marca como não confirmado, você planeja em cima dele — e o "
  "erro passa a ser meu.")
I("O que eu vou dizer", "só o que foi decidido",
  "Então aqui só entra o que um órgão decidiu, com data. O resto fica marcado "
  "como não sabido.")
I("Por que insisto nisso", "já errei aqui",
  "Insisto porque esse tipo de assunto é onde mais aparece número solto: uma "
  "cifra dita com segurança soa igual a uma cifra checada, e as duas viram "
  "decisão de dinheiro na cabeça de quem ouve.")
I("Uma coisa a mais", "não é conselho médico",
  "E uma coisa que vale para o vídeo inteiro: isto não é conselho médico. Não "
  "tem dose, não tem indicação, e não tem se vale a pena para você.")

# ------------------------------------------------------------------- cap 2
T("Por que isso é incomum", "biológico não tem genérico",
  "Agora o detalhe técnico que explica por que essa aprovação chamou atenção.",
  cap="Por que um genérico aqui é incomum")
I("O de referência", "é um biológico",
  "A semaglutida do medicamento de referência é um medicamento biológico. "
  "Biológico é produzido a partir de organismos vivos.")
I("A regra dos biológicos", "não existe genérico",
  "E para medicamento biológico não existe a figura do genérico nos mesmos "
  "moldes dos remédios sintéticos. A cópia exata não é possível.")
I("Então como", "versão sintética",
  "O caminho que a EMS tomou foi outro: desenvolver uma versão sintética do "
  "princípio ativo.")
I("E é isso que abre a porta", "sintético admite genérico",
  "Sendo sintético, o produto entra na categoria que admite genérico. Foi essa "
  "diferença que tornou o registro possível.")
I("Qual é a referência", "o Ozivy",
  "E há um detalhe que confunde muita gente: a referência desse genérico é o "
  "Ozivy, que é fabricado pela própria EMS.")
B("Duas rotas diferentes", ["Biológico", "Sintético"], [100, 100],
  "São duas rotas de fabricação diferentes para chegar à mesma substância, e a "
  "rota escolhida é o que define a categoria regulatória.")
I("O que isso não quer dizer", "não é 'igualzinho'",
  "Isso não quer dizer que a experiência seja idêntica em tudo. Quer dizer que "
  "o produto passou pelas exigências da categoria em que foi registrado.")
I("Quem decide o resto", "seu médico",
  "Se um serve para você, ou se troca por outro, é conversa com quem te "
  "acompanha. Não é decisão que se toma por vídeo.")
I("Uma pergunta útil para levar", "por que essa e não outra",
  "Se você for conversar sobre isso, uma pergunta costuma render mais que "
  "qualquer lista da internet: por que essa opção e não outra, no meu caso.")
I("Por que essa pergunta", "puxa o raciocínio",
  "Ela funciona porque pede o raciocínio, e não só o nome do produto. E o "
  "raciocínio é o que você leva para a próxima consulta.")

# ------------------------------------------------------------------- cap 3
T("O que muda no mercado", "concorrência",
  "O efeito prático dessa aprovação é um só, e é sobre concorrência.",
  cap="O que muda, e o que depende da CMED")
I("Antes", "poucas opções registradas",
  "Até aqui o mercado de canetas de semaglutida tinha poucas opções "
  "registradas no Brasil.")
I("Agora", "mais fabricantes",
  "Com um genérico e um similar registrados, passa a haver mais fabricantes "
  "autorizados a vender.")
I("A regra geral do genérico", "pelo menos trinta e cinco por cento",
  "E existe uma regra geral no Brasil: medicamento genérico precisa custar "
  "pelo menos trinta e cinco por cento menos que o seu medicamento de "
  "referência.")
I("Mas atenção", "regra é sobre a referência",
  "Repare no que a regra diz: ela é uma porcentagem sobre o preço do "
  "medicamento de referência, não sobre o preço que você paga hoje em qualquer "
  "caneta.")
I("E falta um passo", "aprovação na CMED",
  "Falta ainda a aprovação de preço na Câmara de Regulação do Mercado de "
  "Medicamentos. Enquanto isso não sai, não existe preço oficial.")
I("O que a CMED faz", "define o teto",
  "Essa câmara define o preço máximo que pode ser cobrado. É um teto, e não "
  "uma tabela do que a farmácia vai efetivamente cobrar.")
I("Então haverá duas coisas", "teto e preço de prateleira",
  "Ou seja, quando o preço sair, você terá dois números para olhar: o teto "
  "oficial e o que aparece na prateleira. Eles não costumam ser iguais.")
I("Por isso eu não estimo", "duas incógnitas",
  "É por isso que eu não faço a conta no ar. Ela teria duas incógnitas, e o "
  "resultado pareceria preciso sem ser.")
T("O que dá para acompanhar", "sem depender de ninguém",
  "O que dá para fazer é acompanhar, e isso não depende de nenhum vídeo.")
I("Onde sai o preço", "lista da CMED",
  "Os preços máximos de medicamentos são publicados em lista oficial. Quando "
  "sair, o valor estará lá antes de estar em qualquer manchete.")
I("O que perguntar na farmácia", "duas perguntas",
  "E na farmácia, duas perguntas resolvem: já chegou, e qual é o preço "
  "registrado. Não a promoção — o preço registrado.")

# ------------------------------------------------------------------- cap 4
T("Como checar isso sozinha", "sem depender de mim",
  "Antes de fechar, o método — porque ele vale para a próxima notícia também, "
  "não só para esta.",
  cap="Como checar uma notícia dessas")
I("Primeiro", "procure o nome do órgão",
  "Primeiro: a notícia diz qual órgão decidiu? Anvisa, CMED, Ministério. Se "
  "não nomeia ninguém, é comentário, não decisão.")
I("Segundo", "procure a data",
  "Segundo: tem data? Decisão regulatória sempre tem. Notícia sem data costuma "
  "ser reaproveitamento de fato antigo.")
I("Terceiro", "separe decidido de esperado",
  "Terceiro, e é o que mais confunde: separe o que foi decidido do que é "
  "esperado. Registro aprovado é decisão; preço provável é expectativa.")
I("Um teste rápido", "procure o verbo",
  "Um jeito rápido de separar os dois é olhar o verbo. Registrou, aprovou e "
  "publicou são fatos. Deve, pode e estima são previsões.")
B("Duas frases parecidas", ["Aprovou o registro", "Deve custar X"],
  [100, 40],
  "As duas aparecem na mesma reportagem e com a mesma fonte, e só a primeira é "
  "verificável hoje.")
I("Quarto", "veja se a ressalva foi apagada",
  "E quarto: veja se a ressalva sobreviveu. Quando o texto original diz sem "
  "confirmação e a versão que chegou até você não diz, alguém apagou.")
I("Por que isso vale sempre", "o padrão se repete",
  "Esse padrão se repete em todo assunto de saúde com dinheiro envolvido. "
  "Aprender a separar decisão de expectativa vale mais que decorar qualquer "
  "número.")
T("Concorrência não é preço", "uma ressalva honesta",
  "E uma ressalva antes de fechar, porque ela costuma ser pulada.",
  cap="Concorrência não vira preço sozinha")
I("Mais fabricantes ajuda", "mas não garante",
  "Mais fabricantes autorizados tende a pressionar preço para baixo. Tende — "
  "não garante, e não em prazo definido.")
I("O que também conta", "produção e distribuição",
  "Entre o registro e a prateleira ainda existem produção, distribuição e "
  "decisão comercial de cada empresa.")
I("Por isso o prazo é incerto", "registro não é chegada",
  "Registro é autorização para vender, não é chegada ao mercado. As duas datas "
  "podem estar meses distantes.")
I("O que observar", "quando aparecer, compare",
  "Então o que dá para observar é simples: quando as opções aparecerem, compare "
  "os preços registrados entre elas, e não a promoção da semana.")
I("Por que não a promoção", "ela some",
  "A promoção some na semana seguinte e o preço registrado fica. Comparar pela "
  "promoção é comparar duas fotos tiradas em dias diferentes.")
I("Onde isso costuma pesar", "tratamento é contínuo",
  "E aqui isso pesa mais que em outras compras, porque não é uma caixa só: é "
  "um gasto que se repete mês após mês enquanto durar o tratamento.")
I("Uma conta que dá para fazer", "multiplique por doze",
  "Então quando o preço sair, faça uma conta única: multiplique por doze. Uma "
  "diferença pequena por mês vira outra coisa no ano, para cima ou para baixo.")
T("Três coisas para guardar", "e uma para ignorar",
  "Fechando: três coisas para guardar e uma para ignorar.",
  cap="Três para guardar, uma para ignorar")
I("Guardar um", "a data",
  "Primeira: dezessete de agosto de dois mil e vinte e seis, registro na "
  "Anvisa. É a data que dá para checar.")
I("Guardar dois", "genérico e similar são coisas distintas",
  "Segunda: foram dois registros de categorias diferentes. Genérico da EMS, "
  "similar da Germed. Não é a mesma figura regulatória.")
I("Guardar três", "preço ainda não existe",
  "Terceira: o preço ainda não existe oficialmente, porque depende da CMED.")
T("E o que ignorar", "qualquer valor circulando",
  "E o que ignorar, com bastante firmeza.")
I("Ignorar", "número sem CMED",
  "Qualquer valor em reais que circular antes da publicação oficial. Pode até "
  "acertar por sorte, e mesmo assim não é informação.")
I("Como reconhecer", "fonte que se marca",
  "O jeito de reconhecer: fonte séria escreve que o número não está "
  "confirmado. Quem apaga essa ressalva está vendendo certeza que não tem.")
I("Uma última", "cuidado com o 'natural'",
  "E cuidado redobrado agora: sempre que um assunto desses vira notícia, "
  "aparece produto prometendo o mesmo efeito sem receita. Já falei disso aqui, "
  "e a Anvisa já proibiu vários.")
C("Seja Mais Magra e Saudável", "o que foi decidido, com data",
  "Se você acompanha esse assunto, guarde a data e espere a lista oficial de "
  "preços. E converse com quem te acompanha antes de qualquer troca. Se este "
  "vídeo te poupou de um número inventado, se inscreva.")


# -------------------------------------------------------------------- short
#
# Canal `suspenso`: e o SHORT que carrega. Ele entrega a data, os dois
# registros, o motivo tecnico e o que NAO se sabe.
SHORT = [
    {"layout": "titulo", "kicker": "Semaglutida genérica",
     "sub": "aprovada em 17 de agosto",
     "nar": "A Anvisa registrou a primeira caneta genérica de semaglutida do "
            "Brasil, no dia dezessete de agosto.", "sem_cap": True},
    {"layout": "item", "kicker": "Foram dois", "preco": "genérico e similar",
     "nar": "Foram dois registros: um genérico, da EMS, e um similar da "
            "Germed, que se chamará Semaclique.", "sem_cap": True},
    {"layout": "item", "kicker": "Por que é incomum",
     "preco": "biológico não tem genérico",
     "nar": "O de referência é biológico, e biológico não admite genérico. A "
            "EMS fez uma versão sintética, e é isso que abriu a porta.",
     "sem_cap": True},
    {"layout": "item", "kicker": "O preço", "preco": "ainda não existe",
     "nar": "O preço não foi divulgado e depende da CMED. Ignore qualquer "
            "valor que circular antes da lista oficial.", "sem_cap": True},
    {"layout": "cta", "kicker": "Seja Mais Magra e Saudável",
     "sub": "não é conselho médico",
     "nar": "E converse com quem te acompanha antes de qualquer troca.",
     "sem_cap": True},
]

COPY = """# Semaglutida genérica aprovada pela Anvisa: o que foi decidido e o que ainda não se sabe

## TITULO
Semaglutida Genérica Aprovada: o Que a Anvisa Registrou e o Que Ainda Não Tem Preço

## DESCRICAO
Em 17 de agosto de 2026 a Anvisa registrou duas canetas de semaglutida — e uma delas é a primeira genérica do Brasil. Este vídeo cobre o que foi decidido, com data, e diz em voz alta o que ainda NÃO se sabe.

O QUE FOI REGISTRADO

O genérico é da EMS: o primeiro genérico de semaglutida em caneta registrado no país. O outro registro é de um medicamento SIMILAR, da Germed, que será comercializado como Semaclique, aprovado em quatro apresentações na concentração de 1,34 mg/mL. Genérico e similar são figuras regulatórias distintas — não são a mesma coisa.

POR QUE UM GENÉRICO AQUI É INCOMUM

A semaglutida do medicamento de referência é um medicamento BIOLÓGICO, produzido a partir de organismos vivos. Para biológicos não existe a figura do genérico nos mesmos moldes dos remédios sintéticos. O caminho que a EMS tomou foi outro: desenvolver uma versão SINTÉTICA do princípio ativo — e é essa diferença de rota de fabricação que torna o registro como genérico possível. A referência desse genérico é o Ozivy, fabricado pela própria EMS.

Isso NÃO quer dizer que a experiência seja idêntica em tudo. Quer dizer que o produto cumpriu as exigências da categoria em que foi registrado.

O QUE ESTE VÍDEO NÃO AFIRMA, E POR QUÊ

Não digo quanto vai custar: o preço não foi divulgado. Não digo quando chega à farmácia: essa data também não foi divulgada. Circulam valores em reais por aí, e as próprias fontes que os publicam marcam como "ainda sem confirmação" — repetir um número assim faria você planejar em cima dele, e o erro passaria a ser meu.

Existe uma regra geral no Brasil: genérico precisa custar pelo menos 35% menos que seu medicamento de REFERÊNCIA. Repare no que a regra diz — é uma porcentagem sobre o preço da referência, não sobre o que você paga hoje em qualquer caneta. E falta ainda a aprovação de preço na CMED (Câmara de Regulação do Mercado de Medicamentos). Enquanto isso não sai, não existe preço oficial, e uma conta feita no ar teria duas incógnitas.

COMO ACOMPANHAR SEM DEPENDER DE VÍDEO NENHUM

Os preços máximos de medicamentos são publicados em lista oficial — quando sair, o valor estará lá antes de qualquer manchete. E na farmácia, duas perguntas resolvem: já chegou, e qual é o preço REGISTRADO (não a promoção).

TRÊS PARA GUARDAR, UMA PARA IGNORAR

Guarde: a data (17/08/2026, registro na Anvisa); que foram dois registros de categorias diferentes; e que o preço ainda não existe oficialmente. Ignore: qualquer valor em reais que circule antes da publicação oficial. Fonte séria escreve que o número não está confirmado — quem apaga essa ressalva está vendendo certeza que não tem.

E um cuidado extra: sempre que um assunto desses vira notícia, aparece produto prometendo o mesmo efeito sem receita. A Anvisa já proibiu vários, e há um vídeo sobre isso aqui no canal.

ESTE VÍDEO NÃO É CONSELHO MÉDICO. Não traz dose, não traz indicação e não diz se algo vale a pena para você. Se um medicamento serve, ou se cabe trocar por outro, é conversa com o profissional que te acompanha.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Uma pergunta, e ela vale mais que qualquer palpite meu: quando o preço oficial sair na lista da CMED, você quer que eu faça um vídeo comparando as opções registradas? E se você já viu algum valor circulando por aí, cole aqui o link de onde viu — quero mostrar como se checa se um número está confirmado ou não.

## HASHTAGS
#Semaglutida #Anvisa #SejaMaisMagra

## TAGS
semaglutida, semaglutida generica, anvisa, caneta emagrecedora, ems, germed, semaclique, ozivy, generico, medicamento similar, cmed, glp1, obesidade, diabetes, preco de medicamento

## CONFIGURACOES DO STUDIO
- Idioma: Portugues do Brasil (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo sintetico: SIM (voz gerada por IA)
- Localizacao: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios mid-roll: ativados (duracao acima de 8 minutos)

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
Registro na Anvisa em 17/08/2026 do primeiro generico de semaglutida em caneta (EMS) e de um similar (Germed, nome comercial Semaclique, quatro apresentacoes a 1,34 mg/mL); semaglutida sintetica como via que viabiliza o registro como generico, sendo o de referencia um biologico; Ozivy como referencia, fabricado pela propria EMS. Conferido em DUAS passagens de busca com veiculos independentes que coincidem: Correio Braziliense, Poder360, Olhar Digital, Forbes Brasil, O Povo e o Conselho Federal de Farmacia (institucional). PRECO E DATA DE CHEGADA AS FARMACIAS NAO FORAM DIVULGADOS e este video NAO os estima: valores em reais que circularam na imprensa vinham marcados pelas proprias fontes como nao confirmados. A regra de 35% e citada como regra geral de generico no Brasil, incidente sobre o preco do medicamento de REFERENCIA, e sua aplicacao depende de aprovacao na CMED. Este material e informativo sobre uma decisao regulatoria: nao contem dose, indicacao, recomendacao de uso ou comparacao de eficacia, e nao substitui consulta com profissional de saude.
"""


def _copy_existente():
    import os
    alvo = "fabrica/specs/seja-mais-magra-005.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500 and c.strip().startswith("#"):
            return c
    return COPY


SPEC = {
    "slug": "seja-mais-magra",
    "pacote": "seja-mais-magra-005",
    "idioma": "pt-BR",
    "voz": "pt-BR-FranciscaNeural",
    "trilha": "Wholesome",
    "paleta": {"ink": "#241C2B", "c1": "#8E5AA8", "c2": "#3FA08C",
               "bg": "#F7F3FA"},
    "thumb": {"l1": "Genérica", "l2": "aprovada"},
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
    grava(SPEC, "fabrica/specs/seja-mais-magra-005.json")
    d = duracao_estimada(CENAS, SPEC["voz"])
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print(f"estimativa longo: {d:.1f}s = {d/60:.2f} min | short: {s:.1f}s")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
