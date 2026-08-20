#!/usr/bin/env python3
"""Monta a spec labtreinamento-003.

POR QUE ESTE TEMA. O canal ja publicou DOIS longos quase identicos sobre
planilha de riscos psicossociais da NR-1 — 12/08 e 18/08 — e um terceiro
estouraria a similaridade de 0,65 contra o proprio acervo. O eixo esta
queimado, ainda que performe.

Medicao de 19/08/2026 (aprendizado 354, 79 pautas, seis buscas largas): a
mediana do nicho e 12,4 v/d so entre maduros. Por eixo:

    carreira-sst          n=6   68,5   (topo puxado por concurso Transpetro)
    iso-qualidade         n=3   45,4   <- NAO usado pelo canal
    nr1-psicossociais     n=17  36,6   <- usado DUAS vezes
    nr-tecnica            n=19   3,3   morto
    institucional-marca   n=32   1,4   morto

iso-qualidade e o melhor eixo inedito. O n=3 e baixo e isso fica registrado:
a escolha se apoia tambem no formato, que o canal ja mediu com forca — o topo
do nicho entrega uma PLANILHA que resolve obrigacao regulatoria com data
(40,0 v/d contra 1,8 da mediana), e todo o cluster de ISO CONCEITUAL ficou
entre 0,7 e 1,8. Entao: ISO sim, ensaio sobre ISO nunca.

A DOR DATADA, confirmada em 20/08/2026 por duas fontes que batem, uma delas
o proprio comite:
  - committee.iso.org (ISO/TC 176/SC 2): ISO/FDIS 9001 aprovado.
  - DNV, SGS, BSI, TUV: publicacao da sexta edicao em 16/09/2026, transicao
    de tres anos ate setembro de 2029.
Faltam vinte e sete dias para a publicacao.

O QUE ESTE ROTEIRO NAO FAZ, de proposito: nao cita numero de clausula nem
texto de requisito da versao nova. O texto final so publica em 16/09 — quem
recita requisito hoje esta inventando. O video monta o DIAGNOSTICO com o que
o FDIS ja permite afirmar (cultura da qualidade, comportamento etico, papel
da lideranca, mudanca climatica no contexto da organizacao, anexo de
orientacao inedito) e diz, na cena e na descricao, que a conferencia contra
o texto publicado e obrigatoria no dia dezesseis.

O giro do roteiro: a leitura cara e "temos tres anos, da tempo". Da, mas o
custo nao esta no prazo — esta em qual auditoria pega voce no meio. Quem
diagnostica em setembro escolhe a data da transicao; quem espera recebe a
data do organismo certificador.

Taxa de pt-BR-ThalitaMultilingualNeural: MODELO_VOZ de ensaio.py, ajustada
cena a cena nos .srt publicados em 19/08 (R=17,52 chars/s, P=0,702 s/frase).
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


# ------------------------------------------------------- cap 1: o relogio
T("Dezesseis de setembro", "a data que ja esta marcada",
  "Existe uma data marcada no calendario da sua empresa que quase ninguem "
  "olhou ainda. Dezesseis de setembro de dois mil e vinte e seis.",
  cap="A data que ja esta marcada")
I("O que acontece nela", "sai a sexta edicao",
  "E o dia em que sai a sexta edicao da ISO nove mil e um. O rascunho final "
  "ja foi aprovado, com apoio internacional amplo. Nao e rumor, e cronograma.")
I("O prazo de transicao", "tres anos",
  "Quem ja e certificado tem tres anos para migrar. A conta fecha em setembro "
  "de dois mil e vinte e nove.")
I("A leitura confortavel", "temos tres anos",
  "A leitura confortavel e imediata. Temos tres anos, da tempo. E verdade que "
  "da tempo. E e exatamente por isso que a maioria vai chegar apertada.")
I("O detalhe que ninguem conta", "voce nao escolhe a auditoria",
  "Porque o prazo nao e seu. Sua certificacao tem ciclo, e o organismo "
  "certificador tem agenda. Voce nao escolhe em que auditoria a versao nova "
  "vai bater.")
I("Duas empresas, mesmo prazo", "resultados opostos",
  "Duas empresas com o mesmo prazo terminam em situacoes opostas. Uma "
  "diagnostica agora e escolhe a data. A outra espera e recebe a data.")
I("E quem ainda nao e certificado", "o prazo e outro",
  "E se voce esta implantando agora, sem certificado ainda, o calculo muda. "
  "Nao ha transicao para fazer. Ha uma escolha de qual versao usar como "
  "referencia.")
I("A resposta pratica", "monte pela nova",
  "A resposta pratica e monte pela versao nova desde ja. Certificar na "
  "versao que sai daqui a um mes e depois nao ter transicao nenhuma pela "
  "frente.")
I("O que este video entrega", "uma pasta com quatro abas",
  "O que a gente monta aqui e uma pasta de trabalho com quatro abas. "
  "Diagnostico, Lacunas, Plano e Cronograma. Coluna por coluna.")
I("Sem promessa falsa", "isto nao substitui a norma",
  "E uma coisa fica dita ja. Planilha nenhuma substitui ler a norma "
  "publicada. Ela organiza a leitura e o prazo, que e onde as empresas "
  "costumam se perder.")

# ------------------------------------------------- cap 2: o que muda mesmo
T("O que muda de verdade", "menos do que o boato diz",
  "Antes de montar coluna, vale saber o que muda. E aqui tem uma boa "
  "noticia que quase nunca circula.",
  cap="O que muda, e o que nao muda")
I("A maior parte", "e esclarecimento de texto",
  "Boa parte das alteracoes e editorial. Sao ajustes de redacao sobre a "
  "versao de dois mil e quinze, para tirar ambiguidade de interpretacao.")
I("Sua estrutura sobrevive", "o sistema nao vai ao chao",
  "Isso significa que o seu sistema de gestao nao vai ao chao. Procedimento, "
  "registro e indicador que funcionam hoje continuam valendo.")
I("Primeiro eixo novo", "cultura da qualidade",
  "O que ganha peso e outra coisa. Primeiro, cultura da qualidade. Deixa de "
  "ser palavra de discurso e passa a ser algo que a auditoria procura "
  "evidencia.")
I("Segundo eixo", "comportamento etico",
  "Segundo, comportamento etico. Entra explicitamente no vocabulario da "
  "norma, ligado a como a organizacao decide e se comporta.")
I("Terceiro eixo", "papel da lideranca",
  "Terceiro, o papel da lideranca em puxar melhoria continua. Nao assinar a "
  "politica da qualidade e sim aparecer no processo.")
I("Quarto eixo", "mudanca climatica no contexto",
  "Quarto, e esse pega muita gente de surpresa. Mudanca climatica e "
  "sustentabilidade passam a fazer parte explicita do contexto da "
  "organizacao.")
I("Por que isso importa", "contexto e a base de tudo",
  "Importa porque contexto e a primeira coisa que a norma pede. Se o contexto "
  "muda, mudam riscos, partes interessadas e objetivos que saem dele.")
I("O que escrever em clima", "risco do clima sobre voce",
  "E o que se escreve ali nao e meta de carbono. E como o clima afeta a sua "
  "operacao. Chuva que para a entrega, calor que muda turno, seca que "
  "encarece insumo.")
I("Quinto eixo", "risco e oportunidade mais claros",
  "Quinto, a gestao de risco e oportunidade fica mais explicita. Menos espaco "
  "para a matriz de risco existir so para mostrar ao auditor.")
I("Uma novidade de forma", "um anexo de orientacao",
  "E tem uma novidade de forma, inedita nesta norma. Ela vem com um anexo de "
  "orientacao suplementar, de cerca de quinze paginas, para ajudar na "
  "interpretacao.")
I("O que isso muda na pratica", "menos briga com o auditor",
  "Na pratica, isso reduz aquela discussao em que voce entende uma coisa e o "
  "auditor entende outra, e nenhum dos dois tem onde apoiar.")
I("O limite honesto disto aqui", "o texto final sai dia dezesseis",
  "E o limite honesto: o texto final so existe em dezesseis de setembro. "
  "Quem hoje recita numero de clausula da versao nova esta inventando.")
I("Entao o que da para fazer", "diagnosticar o que ja da",
  "O que da para fazer agora, e vale muito, e diagnosticar onde voce esta nos "
  "eixos que ja estao claros. Isso nao muda no dia dezesseis.")

# ------------------------------------------------------ cap 3: aba um
T("Aba um", "Diagnostico",
  "Primeira aba. Diagnostico. Ela responde uma pergunta so: onde a gente esta "
  "hoje, em cada eixo que a versao nova reforca.",
  cap="Aba Diagnostico: onde voce esta")
L("As cinco colunas", ["Eixo", "Situacao atual", "Evidencia",
                       "Nota de zero a cinco", "Responsavel"],
  "Cinco colunas bastam. Eixo, situacao atual, evidencia, nota de zero a "
  "cinco, e responsavel.")
I("Coluna Eixo", "lista fechada, nunca texto livre",
  "A coluna Eixo tem lista fechada. Cultura, etica, lideranca, contexto "
  "climatico, risco e oportunidade. Use validacao de dados.")
I("Por que lista fechada", "texto livre nao agrupa",
  "Se cada pessoa escrever o eixo com as proprias palavras, a planilha vira "
  "um caderno. Ninguem consegue contar quantas linhas estao em cada eixo.")
I("Coluna Situacao atual", "uma frase, sem adjetivo",
  "Situacao atual e uma frase curta e sem adjetivo. Nao escreva bom ou fraco. "
  "Escreva o que existe ou o que nao existe.")
I("Exemplo de frase certa", "descreve, nao julga",
  "Em vez de a lideranca participa pouco, escreva: a analise critica ocorre "
  "por semestre e a direcao participou de uma das duas ultimas.")
I("Coluna Evidencia", "a que separa diagnostico de opiniao",
  "Evidencia e a coluna que separa diagnostico de opiniao. Onde esta o "
  "documento que sustenta a frase anterior.")
L("O que serve de evidencia", ["Ata de analise critica", "Registro de "
                               "treinamento", "Indicador com serie",
                               "Procedimento aprovado", "Registro de auditoria"],
  "Serve ata de analise critica, registro de treinamento, indicador com serie "
  "historica, procedimento aprovado e registro de auditoria interna.")
I("O que nao serve", "achismo com nome bonito",
  "Nao serve a percepcao da equipe sem registro. Se nao ha onde apontar, a "
  "nota daquela linha ja nasce baixa, e tudo bem.")
I("Coluna Nota", "zero a cinco, com regra escrita",
  "A nota vai de zero a cinco. Zero, nao existe. Cinco, existe, esta escrito, "
  "e roda ha pelo menos um ciclo com evidencia.")
I("O truque da nota", "escreva a regra na propria aba",
  "Escreva essa regra dentro da aba, num canto. Nota sem criterio visivel "
  "muda de significado conforme quem preenche.")
I("Coluna Responsavel", "nome, nao area",
  "Responsavel e nome de pessoa. Qualidade nao e nome de pessoa. Area nao "
  "responde a e-mail nem cumpre prazo.")
I("Uma linha inteira, de exemplo", "para nao ficar abstrato",
  "Uma linha completa, para nao ficar abstrato. Eixo lideranca. Situacao: a "
  "direcao participou de uma das duas ultimas analises criticas. Evidencia: "
  "atas de marco e agosto. Nota dois. Responsavel, o gerente da qualidade.")
I("Quantas linhas esperar", "entre quinze e trinta",
  "Um diagnostico honesto de empresa media fica entre quinze e trinta linhas. "
  "Se der cinco, faltou olhar. Se der cem, virou lista de tarefas.")

# ------------------------------------------------------- cap 4: aba dois
T("Aba dois", "Lacunas",
  "Segunda aba. Lacunas. Ela nao coleta nada novo. Ela transforma o "
  "diagnostico em prioridade, que e outra coisa.",
  cap="Aba Lacunas: o que vira prioridade")
I("A conta base", "cinco menos a nota",
  "A conta e simples. Lacuna e cinco menos a nota. Nota dois vira lacuna "
  "tres. Nota cinco vira lacuna zero e sai da fila.")
I("So isso nao basta", "nem toda lacuna pesa igual",
  "Mas so isso nao basta, porque nem toda lacuna pesa igual. Faltar registro "
  "de treinamento e diferente de nao ter contexto definido.")
L("A coluna Peso", ["Um: ajuste local", "Dois: afeta um processo",
                    "Tres: afeta o sistema inteiro"],
  "Entao entra a coluna Peso, de um a tres. Um, ajuste local. Dois, afeta um "
  "processo. Tres, afeta o sistema inteiro.")
I("A prioridade", "lacuna vezes peso",
  "Prioridade e lacuna vezes peso. O maximo e quinze, e quem chega perto "
  "disso e o que voce ataca primeiro.")
I("A formula que classifica", "SE aninhado ou PROCV",
  "Para virar rotulo, use SE aninhado: ate quatro, baixa. De cinco a nove, "
  "media. De dez em diante, alta.")
I("A alternativa mais limpa", "PROCV com aproximado",
  "Se preferir nao aninhar, monte uma tabelinha de cortes e use PROCV com "
  "correspondencia aproximada. Muda o corte num lugar so.")
I("A protecao contra linha vazia", "SEERRO por fora",
  "Envolva com SEERRO. Sem isso, cada linha em branco acusa erro e a aba "
  "inteira parece quebrada quando so esta incompleta.")
I("O corte e seu", "e a norma nao dita isso",
  "E fica registrado: esses cortes sao criterio da empresa. A norma nao "
  "define faixa de prioridade. Escreva na aba quem definiu e quando.")
I("O que sai daqui", "poucas linhas altas",
  "De um diagnostico de vinte linhas, costumam sobrar poucas lacunas altas. "
  "Entre tres e seis, na pratica. Esse e o tamanho real do seu projeto.")
I("Por que isso alivia", "o projeto encolhe",
  "E aqui a maioria respira. O projeto que parecia gigante encolhe para meia "
  "duzia de frentes com nome e prazo.")

# ------------------------------------------------------ cap 5: aba tres
T("Aba tres", "Plano",
  "Terceira aba. Plano. E onde lacuna vira acao com dono e data, ou fica "
  "sendo so uma queixa organizada.",
  cap="Aba Plano: acao com dono e data")
L("As colunas do plano", ["Codigo da lacuna", "Acao", "Responsavel",
                          "Prazo", "Evidencia esperada", "Verificacao"],
  "Seis colunas. Codigo da lacuna, acao, responsavel, prazo, evidencia "
  "esperada e verificacao.")
I("Coluna Codigo", "amarra plano e diagnostico",
  "Codigo amarra as duas abas. Sem ele, seis meses depois ninguem sabe qual "
  "acao respondia a qual achado.")
I("Coluna Acao", "verbo no infinitivo, uma so",
  "Acao comeca com verbo no infinitivo e traz uma acao so. Revisar e "
  "treinar e implantar na mesma celula sao tres linhas disfarcadas de uma.")
I("Coluna Evidencia esperada", "escrita ANTES de comecar",
  "Evidencia esperada e a coluna mais subestimada. Escreva antes de comecar "
  "qual documento vai provar que a acao aconteceu.")
I("Por que antes", "senao voce fabrica prova depois",
  "Se voce escreve depois, vai procurar o que ja tem e chamar de prova. "
  "Escrevendo antes, a acao nasce com o registro dentro dela.")
I("Coluna Verificacao", "eficacia, nao conclusao",
  "Verificacao nao pergunta se foi feito. Pergunta se resolveu. Sao coisas "
  "diferentes e a segunda e a que a auditoria olha.")
I("Exemplo da diferenca", "treinou nao e sabe",
  "Treinamento aplicado e conclusao. Amostra de cinco pessoas respondendo "
  "certo dois meses depois e eficacia.")
I("Quem verifica", "nunca quem executou",
  "E quem verifica nao pode ser quem executou. Nao por desconfianca, por "
  "cegueira mesmo. Quem fez a acao ja sabe o que ela deveria resolver.")
I("Acao atrasada", "reprograme uma vez, e registre",
  "Acao que estourou o prazo: reprograme uma vez, com data nova e motivo "
  "escrito. Na segunda reprogramacao, o problema nao e prazo. E a acao que "
  "esta errada.")
I("Coluna Prazo", "data, nunca trimestre",
  "Prazo e data com dia. Segundo trimestre nao e prazo, e uma faixa onde "
  "ninguem esta atrasado ate o ultimo dia.")
I("Formatacao condicional", "duas regras bastam",
  "Duas regras de formatacao condicional resolvem o acompanhamento. Vermelho "
  "quando a data passou e a verificacao esta vazia. Amarelo faltando "
  "quinze dias.")

# ----------------------------------------------------- cap 6: aba quatro
T("Aba quatro", "Cronograma",
  "Quarta aba. Cronograma. E a que transforma tres anos em decisao, em vez "
  "de tres anos em adiamento.",
  cap="Aba Cronograma: contar de tras para frente")
I("A regra do cronograma", "conte de tras para frente",
  "A regra e contar de tras para frente. O fim nao e setembro de dois mil e "
  "vinte e nove. O fim e a sua auditoria de transicao, que vem antes.")
I("Marco um", "a publicacao",
  "Primeiro marco, dezesseis de setembro de dois mil e vinte e seis. "
  "Publicacao. Aqui voce le o texto e confere o diagnostico contra ele.")
I("O que fazer nesse dia", "revisar, nao recomecar",
  "E revisar nao e recomecar. As cinco linhas de eixo continuam. O que muda "
  "e o detalhe de cada exigencia, e ai a coluna Situacao atual e corrigida.")
I("Marco dois", "conversa com o certificador",
  "Segundo marco. Perguntar ao seu organismo certificador em que auditoria "
  "ele pretende aplicar a versao nova no seu ciclo.")
I("Por que essa pergunta importa", "ela define todo o resto",
  "Essa pergunta define o resto do cronograma. Sem ela voce planeja para "
  "setembro de dois mil e vinte e nove e pode ser cobrado bem antes.")
I("Marco tres", "fechar as lacunas altas",
  "Terceiro marco. Fechar as lacunas de prioridade alta, com verificacao de "
  "eficacia feita, e nao apenas acao concluida.")
I("Marco quatro", "auditoria interna na versao nova",
  "Quarto marco. Rodar uma auditoria interna ja com o criterio novo, antes "
  "da externa. E o ensaio que custa barato.")
I("Marco cinco", "analise critica pela direcao",
  "Quinto marco. Levar o resultado a analise critica pela direcao. Como "
  "lideranca ganhou peso, essa ata passa a ser evidencia forte.")
I("A pergunta do orcamento", "precisa de consultoria?",
  "A pergunta que sempre vem: precisa contratar consultoria? Para o "
  "diagnostico, nao. Ele e feito com quem ja conhece os processos por dentro.")
I("Onde consultoria ajuda", "na leitura do texto novo",
  "Onde ela ajuda de verdade e depois de dezesseis de setembro, na leitura "
  "fina do texto e do anexo. Contratar antes disso e pagar para alguem "
  "esperar junto.")
I("A coluna que faz funcionar", "responsavel por marco",
  "Cada marco leva responsavel e data. Cronograma sem dono e uma linha do "
  "tempo bonita que ninguem cumpre.")

# ------------------------------------------------- cap 7: erros e ponte
T("Os erros que saem caros", "quatro, e o ultimo e o pior",
  "Para fechar, os quatro erros que mais aparecem em transicao de norma. O "
  "ultimo e o mais caro e o mais silencioso.",
  cap="Quatro erros que saem caros")
I("Erro um", "esperar o texto para comecar",
  "Erro um. Esperar o texto sair para comecar. Os eixos que a gente "
  "diagnosticou aqui nao mudam em dezesseis de setembro. So ficam mais "
  "detalhados.")
I("Erro dois", "tratar como projeto de documento",
  "Erro dois. Tratar a transicao como projeto de reescrever manual. Se o "
  "resultado for so documento novo, a auditoria encontra a mesma pratica de "
  "antes com capa diferente.")
I("Erro tres", "deixar a lideranca de fora",
  "Erro tres. Rodar o projeto so dentro da qualidade. Com o peso que "
  "lideranca ganhou, um projeto sem a direcao dentro ja nasce com lacuna "
  "que planilha nenhuma fecha.")
I("Erro quatro", "confundir conclusao com eficacia",
  "Erro quatro, o silencioso. Marcar acao como concluida sem verificar "
  "eficacia. A planilha fica verde, o sistema continua igual, e a nao "
  "conformidade aparece na externa.")
I("Por que ele e o pior", "ele esconde o problema",
  "E o pior porque os outros tres voce enxerga. Esse aqui produz uma "
  "sensacao de pronto que so quebra na hora errada.")
I("O sinal de que esta indo bem", "a planilha fica menor",
  "Um sinal de que a transicao esta indo bem: a aba Lacunas encolhe mes a "
  "mes. Se ela so cresce, voce esta diagnosticando e nao executando.")
I("O sinal de alerta", "tudo alta prioridade",
  "E o sinal de alerta oposto: se quase tudo saiu como prioridade alta, o "
  "peso foi preenchido sem criterio. Refaca a coluna Peso antes de seguir.")
I("O resumo em uma frase", "diagnostico, corte, dono, data",
  "Se voce guardar so uma coisa deste video, guarde a sequencia. "
  "Diagnostico com evidencia, corte de prioridade escrito, dono com nome, e "
  "data com dia.")
I("O que fazer hoje", "quinze linhas bastam",
  "E o que da para fazer hoje, em uma tarde: abrir a aba Diagnostico e "
  "preencher quinze linhas com evidencia de verdade. O resto sai disso.")
C("Ponte", "no dia dezesseis a gente confere",
  "No dia dezesseis de setembro eu volto com o texto publicado na mao, para "
  "conferir este diagnostico linha por linha. Inscreva-se para nao perder "
  "essa conferencia, e me conte nos comentarios quantas lacunas altas "
  "sobraram na sua.")

# ------------------------------------------------------------------ short
SHORT = []


def S(kicker, sub, nar):
    SHORT.append({"layout": "titulo", "kicker": kicker, "sub": sub,
                  "nar": nar, "sem_cap": True})


S("16/09/2026", "a data que ja esta marcada",
  "Dezesseis de setembro de dois mil e vinte e seis. Sai a sexta edicao da "
  "ISO nove mil e um.")
S("Tres anos", "e voce nao escolhe a data",
  "Voce tem tres anos para migrar. So que quem escolhe em que auditoria isso "
  "cai nao e voce, e o seu certificador.")
S("O que ja da para fazer", "sem esperar o texto",
  "Da para diagnosticar hoje. Cultura, etica, lideranca, clima no contexto, "
  "risco e oportunidade.")
S("Cinco colunas", "eixo, situacao, evidencia, nota, dono",
  "Cinco colunas resolvem: eixo, situacao atual, evidencia, nota de zero a "
  "cinco e responsavel com nome.")
S("O corte", "lacuna vezes peso",
  "Lacuna vezes peso da a prioridade: de vinte linhas saem umas cinco altas. "
  "Esse e o tamanho real do projeto.")
S("O video completo", "as quatro abas, coluna por coluna",
  "No video completo eu monto as quatro abas inteiras, com as formulas. Link "
  "aqui em cima.")

COPY = """# Planilha de transicao para a ISO 9001:2026

## TITULO
[EXCEL] ISO 9001:2026 — Planilha de Transicao com Diagnostico dos Eixos Novos

## DESCRICAO
A sexta edicao da ISO 9001 tem publicacao marcada para 16 de setembro de 2026, depois de o rascunho final (FDIS) ser aprovado com amplo apoio internacional. Quem ja e certificado tera tres anos de transicao, ate setembro de 2029.

O problema nao e o prazo. E que voce nao escolhe em que auditoria do seu ciclo a versao nova vai bater — quem define isso e o organismo certificador. Quem diagnostica agora escolhe a data da transicao; quem espera recebe a data.

Boa parte das alteracoes e editorial, esclarecendo a redacao de 2015: o seu sistema de gestao nao vai ao chao. O que ganha peso e outra coisa — cultura da qualidade, comportamento etico, o papel da lideranca em puxar melhoria continua, a entrada explicita de mudanca climatica e sustentabilidade no contexto da organizacao, e uma gestao de risco e oportunidade mais clara. Pela primeira vez a norma vem com um anexo de orientacao suplementar para apoiar a interpretacao.

Neste video a planilha e montada do zero, com quatro abas.

Diagnostico: cinco colunas — eixo, situacao atual, evidencia, nota de zero a cinco e responsavel. Por que a coluna Eixo precisa de validacao de dados em vez de texto livre, por que a Situacao atual e escrita sem adjetivo, e por que Evidencia e a coluna que separa diagnostico de opiniao. Um diagnostico honesto de empresa media fica entre quinze e trinta linhas.

Lacunas: lacuna e cinco menos a nota, peso de um a tres, e prioridade e o produto dos dois. SE aninhado ou PROCV com correspondencia aproximada para classificar, SEERRO para a linha em branco nao acusar erro. Os cortes de faixa sao criterio da empresa e ficam escritos na propria aba, com data e responsavel — a norma nao define faixa de prioridade.

Plano: codigo da lacuna, acao com um verbo so, responsavel com nome, prazo com dia, evidencia esperada escrita ANTES de comecar, e verificacao de eficacia — que pergunta se resolveu, nao se foi feito.

Cronograma: contado de tras para frente, a partir da sua auditoria de transicao e nao de setembro de 2029. Cinco marcos, incluindo a pergunta ao certificador que define todo o resto.

E os quatro erros que saem mais caros, sendo o ultimo o mais silencioso: marcar acao como concluida sem verificar eficacia. A planilha fica verde e a nao conformidade aparece na auditoria externa.

## CAPITULOS
{CAPITULOS}

## COMENTARIO FIXADO
Duas perguntas, porque a resposta varia muito de empresa para empresa: quantas lacunas de prioridade alta sobraram no seu diagnostico? E voce ja perguntou ao seu organismo certificador em que auditoria do ciclo ele pretende aplicar a versao nova? Estou juntando essas respostas para o video de 16 de setembro.

## HASHTAGS
#ISO9001 #Qualidade #LabTreinamento

## TAGS
iso 9001, iso 9001 2026, sistema de gestao da qualidade, sgq, transicao iso, auditoria interna, qualidade, excel, planilha, gestao de riscos, melhoria continua, certificacao, analise critica, nao conformidade, processos

## CONFIGURACAO DE STUDIO
- Idioma: Portugues (pt-BR) | Categoria: Educacao (27)
- Nao feito para criancas
- Divulgacao de conteudo alterado ou sintetico: SIM (voz gerada por IA)
- Local: Brasil | Licenca: Licenca padrao do YouTube
- Anuncios no meio: ligados (duracao acima de oito minutos)

## MUSICA / LICENCA
{TRILHA}

## NOTA SOBRE FONTES
A data de publicacao (16 de setembro de 2026) e o periodo de transicao de tres anos vem de comunicados dos organismos certificadores (DNV, SGS, BSI, TUV) e da pagina de noticias do ISO/TC 176/SC 2, comite responsavel pela norma, consultados em 20 de agosto de 2026. Ate a publicacao, o conteudo da versao nova e conhecido pelo rascunho final (FDIS) e por esses comunicados — por isso este video NAO cita numero de clausula nem transcreve requisito da versao nova, e trata apenas dos eixos ja anunciados. Confira tudo contra o texto publicado a partir de 16 de setembro. Os cortes de faixa de prioridade usados na planilha (ate 4 baixa, 5 a 9 media, 10 ou mais alta) sao criterio de exemplo e nao vem da norma. Este video e material educativo sobre construcao de planilha e organizacao de projeto; nao e consultoria, parecer tecnico nem servico de certificacao.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-003",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",   # canais.trilha
    "paleta": {"ink": "#101B2B", "c1": "#1D3557", "c2": "#E07A5F", "bg": "#F7F6F3"},
    "thumb": {"l1": "ISO 9001:2026", "l2": "o diagnostico antes do texto"},
    "longo": CENAS,
    "short": SHORT,
    "copy": COPY,
}

if __name__ == "__main__":
    p = "fabrica/specs/labtreinamento-003.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(SPEC, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"chars longo: {sum(len(c['nar']) for c in CENAS)}")
    print("capitulos:", [c["cap"] for c in CENAS if c.get("cap")])
