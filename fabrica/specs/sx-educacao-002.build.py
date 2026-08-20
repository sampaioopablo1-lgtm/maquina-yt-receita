#!/usr/bin/env python3
"""Monta a spec sx-educacao-002.

EIXO. O canal so publicou um eixo ate agora (licencas de Power BI ociosas,
sx-educacao-001). O `pautas_banco` do nicho tem um agrupamento inteiro que o
canal nunca tocou e que e o segundo mais forte da lista: carreira publica em
dados. "Analista ou Auditor? O Erro que Pode Custar Anos de Estudo" (40.978
views), "Quanto ganha e o que faz um Analista da Dataprev?" (13.145),
"Concurso DATAPREV 2026: Tudo Sobre as Vagas de TI e Salarios" (5.629) e
"Concurso ALECE 2026 SAIU!" (9.433). Quatro das catorze pautas do topo, e
zero video publicado.

A estrutura copiada e a do outlier de 40.978: BIFURCACAO + CUSTO MEDIDO.
Nao "qual e melhor" — "qual erro na comparacao custa anos".

NUMEROS. Todos de fonte institucional, dois blocos independentes:

  Edital Dataprev 2026 (DOU de 03/07/2026, banca FGV)
    Analista de TI, 40h ....... R$ 10.685,44  (9.423,30 + 1.262,14 adicional)
    Analista de Processamento .. R$  8.273,94
    1.823 vagas = 212 imediatas + 1.611 cadastro de reserva
    taxa R$ 110,00 | prova objetiva unica em 11/10/2026

  CAGED/eSocial, Ministerio do Trabalho e Emprego (ultimos 12 meses)
    Analista de dados ..... media R$  4.503,74  (10.704 admissoes)
    Cientista de dados .... media R$ 11.080,27  (1.687 profissionais, 41h)
                            piso R$ 7.365,15 | teto R$ 18.981,20
    Estatistico-analista .. media R$  7.830,79  (1.711, 42h)
                            piso R$ 7.616,92 | teto R$ 16.268,72

A tese do video sai da propria diferenca entre os dois blocos: o erro nao e
escolher errado, e comparar a ENTRADA de um com a ENTRADA do outro. Um dos
dois numeros e uma tabela parada; o outro e o comeco de uma curva que termina
em R$ 18.981,20. R$ 18.981,20 - R$ 10.685,44 = R$ 8.295,76 por mes.
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


# ---------------------------------------------------------------- cap 1
T("Dois numeros oficiais", "e uma comparacao errada",
  "Dez mil seiscentos e oitenta e cinco reais e quarenta e quatro centavos. "
  "E quatro mil quinhentos e tres reais e setenta e quatro centavos. Os dois "
  "numeros sao oficiais, e comparar um com o outro e o erro deste video.",
  cap="Os dois numeros que todo mundo compara")
I("O primeiro", "edital da Dataprev",
  "O primeiro sai do edital da Dataprev publicado no Diario Oficial em tres "
  "de julho de dois mil e vinte e seis. E a remuneracao inicial do analista "
  "de tecnologia da informacao, quarenta horas semanais.")
I("Como ele e montado", "salario mais adicional",
  "E ele nao e um numero so. O salario nominal e nove mil quatrocentos e "
  "vinte e tres reais. Em cima dele vem um adicional de atividade de mil "
  "duzentos e sessenta e dois.")
I("O segundo", "CAGED, Ministerio do Trabalho",
  "O segundo sai do CAGED, o cadastro do Ministerio do Trabalho. E a media "
  "de quem foi admitido como analista de dados em carteira assinada nos "
  "ultimos doze meses no Brasil inteiro.")
I("Quantas admissoes", "dez mil setecentas e quatro",
  "Nao e pesquisa com amostra. Sao dez mil setecentas e quatro admissoes "
  "registradas. E o numero mais solido que existe sobre esse cargo no pais.")
B("Lado a lado", ["Dataprev", "CLT medio"], [100, 42],
  "Postos lado a lado, a diferenca e de seis mil cento e oitenta e um reais "
  "e setenta centavos por mes. Setenta e quatro mil e cento e oitenta reais "
  "por ano. E ai a conversa costuma acabar.")
T("So que", "os dois nao sao a mesma coisa",
  "So que esses dois numeros nao respondem a mesma pergunta. Um deles e uma "
  "linha de tabela. O outro e o primeiro ponto de uma curva.")
L("O que este video faz", ["O que o edital de fato oferece",
                           "O teto que a tabela nao tem",
                           "O custo do tempo de estudo",
                           "A conta de cinco anos",
                           "Como decidir com a sua planilha"],
  "Entao vamos por partes. O que o edital de fato oferece. O teto que a "
  "tabela nao tem. O custo do tempo, a conta de cinco anos, e como voce "
  "monta a sua propria versao.")
I("Um aviso", "nao vou dizer o que escolher",
  "E um aviso que vale o video inteiro. Nao vou dizer qual caminho e melhor. "
  "Vou mostrar quais numeros entram na conta, porque a maioria decide com "
  "metade deles. Comecando pelo que o edital de fato oferece:")

# ---------------------------------------------------------------- cap 2
T("O edital", "mil oitocentas e vinte e tres vagas",
  "Comeca pelo edital, porque o titular da noticia e sempre o numero grande "
  "e o numero grande e o que menos ajuda a decidir.",
  cap="O que o edital realmente oferece")
I("O numero da manchete", "mil oitocentas e vinte e tres",
  "Mil oitocentas e vinte e tres oportunidades. E esse o numero que circula, "
  "e ele esta correto. So que ele soma duas coisas muito diferentes.")
B("Como ele se divide", ["Imediatas", "Cadastro de reserva"], [13, 100],
  "Duzentas e doze vagas sao imediatas. Mil seiscentas e onze sao cadastro "
  "de reserva. Chamar cadastro de reserva de vaga e o primeiro exagero da "
  "conta.")
I("O que muda", "reserva pode nunca ser chamada",
  "Cadastro de reserva significa que a pessoa passou e fica numa fila. Pode "
  "ser chamada em seis meses, pode ser chamada no ultimo mes de validade, "
  "pode nao ser chamada.")
I("O outro cargo", "oito mil duzentos e setenta e tres",
  "Tem um segundo cargo no mesmo edital. Analista de processamento, com "
  "oito mil duzentos e setenta e tres reais e noventa e quatro centavos. "
  "Duas mil e quatrocentos a menos que o primeiro.")
I("A prova", "etapa unica, objetiva",
  "A selecao e uma prova objetiva de multipla escolha, etapa unica, "
  "aplicada em onze de outubro. Sem discursiva. A banca e a Fundacao "
  "Getulio Vargas.")
I("A inscricao", "cento e dez reais",
  "A inscricao custa cento e dez reais. Esse e o unico custo do edital que "
  "aparece escrito. Todos os outros custos sao seus e ninguem os publica.")
T("Ponte", "o numero que falta na tabela",
  "Guardado o que o edital oferece, falta o numero que o edital nao tem e "
  "que muda o sentido da comparacao inteira:")

# ---------------------------------------------------------------- cap 3
T("O teto", "que uma tabela nao tem",
  "Salario de estatal e tabela. Ele sobe por progressao, por tempo, por "
  "acordo coletivo. Ele nao sobe porque voce ficou muito bom em seis meses.",
  cap="O teto que a tabela nao tem")
I("No CAGED tem os tres", "piso, media e teto",
  "E o CAGED nao publica so a media. Ele publica piso, media e teto por "
  "cargo. E o teto e onde a comparacao vira outra coisa.")
I("Cientista de dados", "media onze mil e oitenta",
  "Cientista de dados, em carteira assinada, media de onze mil e oitenta "
  "reais e vinte e sete centavos. Mil seiscentos e oitenta e sete "
  "profissionais, quarenta e uma horas semanais.")
I("O piso desse cargo", "sete mil trezentos e sessenta e cinco",
  "O piso desse cargo e sete mil trezentos e sessenta e cinco reais e "
  "quinze centavos. Ja acima da media do analista de dados que abriu o "
  "video.")
I("E o teto", "dezoito mil novecentos e oitenta e um",
  "E o teto e dezoito mil novecentos e oitenta e um reais e vinte "
  "centavos. Contra dez mil seiscentos e oitenta e cinco do edital.")
B("A conta que ninguem faz", ["Dataprev", "Teto CLT"], [56, 100],
  "Oito mil duzentos e noventa e cinco reais e setenta e seis centavos por "
  "mes de diferenca, agora para o outro lado. E o mesmo mercado, o mesmo "
  "pais, a mesma fonte de dados.")
I("Tem um terceiro cargo", "estatistico analista",
  "E tem mais um cargo na mesma tabela. Estatistico analista, com media de "
  "sete mil oitocentos e trinta reais. E teto de dezesseis mil duzentos e "
  "sessenta e oito.")
L("Os tres cargos, mesma base", ["Analista de dados: 4.503",
                                 "Estatistico: 7.830",
                                 "Cientista de dados: 11.080"],
  "Tres cargos, a mesma fonte, o mesmo periodo. Quatro mil e quinhentos, "
  "sete mil oitocentos, onze mil. A distancia entre eles nao e sorte: e o "
  "nome do cargo mudando.")
I("O que isso quer dizer", "voce comparou o degrau errado",
  "Entao quando alguem poe dez mil seiscentos contra quatro mil e "
  "quinhentos, comparou o degrau mais alto de um lado com o degrau mais "
  "baixo do outro.")
T("Ponte", "e ainda falta o tempo",
  "E falta a parte mais cara da conta, que nao aparece em nenhuma das duas "
  "tabelas:")

# ---------------------------------------------------------------- cap 4
T("O tempo", "o custo que nao vem escrito",
  "Passar num concurso desses custa tempo. E tempo, numa conta de salario, "
  "tem preco exato: e o que voce deixou de ganhar enquanto estudava.",
  cap="O custo do tempo de estudo")
I("A base da conta", "quanto voce ganha hoje",
  "A conta comeca no que voce ganha hoje, nao no que voce vai ganhar. Se "
  "voce ganha quatro mil e quinhentos e estuda por dois anos sem trocar de "
  "emprego, o custo nao e o salario.")
I("O custo real", "a promocao que nao aconteceu",
  "O custo e a diferenca entre onde voce estaria se tivesse investido esses "
  "dois anos na carreira privada, e onde voce ficou. Isso e o custo de "
  "oportunidade.")
I("Por que ele e invisivel", "nao sai da sua conta",
  "Ele e invisivel porque nao sai do seu bolso. Ninguem cobra. E por isso "
  "que quase ninguem poe ele na planilha, e por isso a comparacao fica "
  "torta.")
I("E o inverso tambem vale", "a estabilidade tem preco",
  "E o inverso tambem e verdade. Estabilidade tem valor, e valor nao "
  "aparece na coluna de salario. Quem ignora isso do outro lado tambem "
  "esta comparando errado.")
I("Como pesar", "escreva o numero",
  "A saida nao e fingir que da para medir tudo. E escrever um numero. "
  "Quanto voce pagaria por mes para nunca mais ser demitido. Esse numero "
  "entra na conta como qualquer outro.")
I("Se voce nao escrever", "ele vira zero",
  "Se voce nao escrever esse numero, ele nao vira neutro. Ele vira zero. E "
  "zero e uma opiniao tao forte quanto qualquer outra, so que escondida.")
T("Ponte", "agora da para somar",
  "Com o tempo dentro da conta, da para fechar os cinco anos:")

# ---------------------------------------------------------------- cap 5
T("Cinco anos", "os dois caminhos somados",
  "Cinco anos e o horizonte certo porque e onde a curva do lado privado "
  "aparece. Em um ano os dois caminhos parecem iguais.",
  cap="A conta de cinco anos")
I("Lado publico", "tabela vezes sessenta",
  "Do lado publico a conta e curta. Dez mil seiscentos e oitenta e cinco "
  "vezes sessenta meses, mais os reajustes de acordo coletivo. E previsivel, "
  "e essa e a virtude dele.")
I("Lado privado", "depende de onde voce comeca",
  "Do lado privado depende de onde voce entra na escada. Comecando em quatro "
  "mil e quinhentos e chegando a onze mil em cinco anos, o total fica perto "
  "do outro caminho.")
I("O que decide", "a velocidade da escada",
  "O que decide nao e o ponto de partida, e a velocidade. Se voce sobe de "
  "analista para cientista de dados, a curva ultrapassa a tabela. Se voce "
  "fica no mesmo cargo, nao ultrapassa.")
B("Cinco anos, os dois", ["Publico", "Privado parado", "Privado subindo"],
  [100, 45, 118],
  "Tres cenarios, nao dois. Publico. Privado sem mudar de cargo. E privado "
  "mudando de cargo. Sao respostas diferentes, e a pergunta era a mesma.")
I("O detalhe do meio", "o cenario parado e o pior",
  "Repare no cenario do meio. Ficar cinco anos no mesmo cargo em carteira "
  "assinada e o pior dos tres. Nao e o setor que decide, e o movimento.")
I("E o risco", "os dois lados tem o seu",
  "Cada lado tem o seu risco. O publico depende de ser chamado, e mil "
  "seiscentas e onze das vagas sao reserva. O privado depende de voce "
  "trocar de cargo, e isso nem sempre acontece.")
I("O erro mais caro", "estudar sem decidir",
  "O erro mais caro nao e escolher errado. E passar dois anos estudando "
  "para concurso sem ter feito essa conta, e descobrir depois que o outro "
  "caminho pagava a mesma coisa.")
T("Ponte", "para a sua propria versao",
  "Falta so transformar isso numa planilha que responde pela sua situacao, "
  "e nao pela media do pais:")

# ---------------------------------------------------------------- cap 6
T("A sua planilha", "seis linhas",
  "Sao seis linhas, e todas cabem no Excel que voce ja tem. Nenhuma funcao "
  "avancada.",
  cap="Como montar a sua propria conta")
L("As seis linhas", ["Salario de hoje", "Salario do edital",
                     "Anos de estudo", "Chance de ser chamado",
                     "Valor da estabilidade", "Crescimento anual privado"],
  "Salario de hoje. Salario do edital. Anos de estudo. Chance de ser "
  "chamado. Valor que voce da a estabilidade. E crescimento anual esperado "
  "no privado.")
I("A que mais importa", "crescimento anual",
  "A linha que mais mexe no resultado e a ultima. Um por cento ao ano contra "
  "oito por cento ao ano muda o vencedor da conta, e nenhuma reportagem sobre "
  "concurso menciona ela.")
I("Como preencher essa", "olhe para tras",
  "E ela nao se chuta. Olhe seus ultimos tres anos de salario e calcule o "
  "crescimento que voce ja teve. O passado e a melhor estimativa que voce "
  "tem do futuro.")
I("A linha da chance", "seja honesto",
  "A linha da chance de ser chamado e a que as pessoas preenchem com "
  "otimismo. Duzentas e doze vagas imediatas em mil oitocentas e vinte e "
  "tres e um bom lembrete.")
I("O que a planilha devolve", "nao e um vencedor",
  "E o que ela devolve nao e um vencedor. E o ponto em que os dois se "
  "igualam. Acima dele um caminho ganha, abaixo dele o outro.")
I("E ele se move", "a cada reajuste",
  "E esse ponto se move. Cada reajuste da tabela publica empurra ele para um "
  "lado, cada promocao sua empurra para o outro. Por isso vale refazer a "
  "conta uma vez por ano.")
I("Carimbe a data", "senao envelhece calado",
  "Escreva a data em que voce preencheu. Sem a data, daqui a dois anos "
  "ninguem sabe se aqueles numeros ainda valem, e uma planilha velha decide "
  "tao mal quanto um chute.")
T("Ponte", "o que fazer com o resultado",
  "E com o resultado na mao, sobra a parte que ninguem conta:")

# ---------------------------------------------------------------- cap 7
T("O que fazer", "com o numero na mao",
  "A planilha nao decide por voce. Ela tira a decisao do campo da opiniao e "
  "poe no campo da conta. Tres coisas para fazer depois.",
  cap="O que fazer com o resultado")
I("Primeiro", "os dois nao sao exclusivos",
  "Primeiro: os dois caminhos nao sao exclusivos. Da para estudar para "
  "concurso trabalhando, e a conta muda inteira porque o custo de "
  "oportunidade cai quase a zero.")
I("Segundo", "prazo, nao para sempre",
  "Segundo: ponha um prazo. Dois anos, tres editais, o que for. Concurso sem "
  "prazo e o unico projeto que consegue custar cinco anos sem nenhuma "
  "decisao no meio.")
I("Terceiro", "refaca a cada edital",
  "Terceiro: refaca a conta a cada edital novo. Salario de edital muda, e o "
  "seu salario tambem. A conta de dois anos atras nao vale mais.")
L("Recapitulando", ["10.685,44 e tabela",
                    "4.503,74 e comeco de curva",
                    "212 imediatas de 1.823",
                    "Teto CLT: 18.981,20"],
  "Recapitulando. Dez mil seiscentos e oitenta e cinco e uma tabela. Quatro "
  "mil e quinhentos e o comeco de uma curva. Duzentas e doze vagas sao "
  "imediatas. E o teto do lado privado e dezoito mil novecentos e oitenta e "
  "um.")
I("A parte que quase ninguem faz", "escrever o valor da estabilidade",
  "A parte que quase ninguem faz e escrever quanto vale a estabilidade para "
  "voce. Sem ela a planilha compara dinheiro com dinheiro e ignora metade "
  "do motivo real da escolha.")
I("O que nao fazer", "decidir pela manchete",
  "Uma coisa a nao fazer: decidir pelo numero da manchete. Manchete traz o "
  "salario mais alto do edital e o total de vagas somado. Os dois sao o "
  "melhor caso.")
I("Se voce so fizer uma coisa", "calcule o seu crescimento",
  "Se voce so fizer uma coisa depois deste video, calcule o crescimento "
  "medio do seu salario nos ultimos tres anos. Esse numero sozinho ja "
  "responde metade da pergunta.")
I("E leva minutos", "nao um projeto",
  "E leva minutos, nao um projeto. As seis linhas cabem numa manha, e o "
  "primeiro calculo cabe num cafe.")
I("Documente a decisao", "uma linha basta",
  "Quando decidir, escreva uma linha na propria planilha dizendo por que. "
  "Daqui a tres anos ninguem vai lembrar do motivo, e o motivo e a unica "
  "coisa que da para revisar.")
C("SX Educacao", "Excel, dados e decisao",
  "Se voce fez a conta, escreve nos comentarios qual foi o seu crescimento "
  "anual. Estou juntando esses numeros para o proximo video.")
C("SX Educacao", "Excel, dados e decisao",
  "E se voce quer a planilha de outra decisao de carreira, diz qual. A mais "
  "pedida sai primeiro.")

SHORT = [
    {"layout": "titulo", "kicker": "R$ 10.685 contra R$ 4.503",
     "sub": "a comparacao errada",
     "nar": "Dez mil seiscentos e oitenta e cinco no edital da Dataprev "
            "contra quatro mil e quinhentos em carteira assinada. Os dois "
            "sao oficiais.", "sem_cap": True},
    {"layout": "item", "kicker": "O erro", "preco": "entrada contra entrada",
     "nar": "O erro e comparar entrada com entrada. Um lado e tabela parada, "
            "o outro e o comeco de uma curva.", "sem_cap": True},
    {"layout": "item", "kicker": "O numero que falta",
     "preco": "teto CLT: 18.981,20",
     "nar": "No mesmo CAGED, cientista de dados tem teto de dezoito mil "
            "novecentos e oitenta e um reais: oito mil a mais que o edital.",
     "sem_cap": True},
    {"layout": "item", "kicker": "E as vagas", "preco": "212 de 1.823",
     "nar": "E das mil oitocentas e vinte e tres vagas do edital, duzentas "
            "e doze sao imediatas. O resto, cadastro de reserva.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "SX Educacao", "sub": "a conta completa",
     "nar": "A planilha de seis linhas que responde pelo seu caso esta no "
            "video longo. Assiste agora.", "sem_cap": True},
]


def _copy_existente():
    """Le a copy do .json ao lado, se ele ja existir. Mesmo motivo do 001: a
    copy real nasce depois do render, e reconstruir daqui a apagaria."""
    import os
    alvo = "fabrica/specs/sx-educacao-002.json"
    if os.path.exists(alvo):
        c = json.load(open(alvo, encoding="utf-8")).get("copy") or ""
        if len(c) > 500:
            return c
    return "gerado a partir dos capitulos reais apos o render"


SPEC = {
    "slug": "sx-educacao",
    "pacote": "sx-educacao-002",
    "idioma": "pt-BR",
    "voz": "pt-BR-AntonioNeural",
    "trilha": "Deliberate_Thought",
    "paleta": {"ink": "#10261C", "c1": "#217346", "c2": "#F2B134",
               "bg": "#F1F7F4"},
    "thumb": {"l1": "10.685 x 4.503", "l2": "concurso ou CLT em dados"},
    "longo": CENAS,
    "short": SHORT,
    "copy": _copy_existente(),
}

if __name__ == "__main__":
    p = "fabrica/specs/sx-educacao-002.json"
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
