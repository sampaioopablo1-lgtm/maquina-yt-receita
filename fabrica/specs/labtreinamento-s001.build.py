"""labtreinamento-s001 — PRIMEIRO SHORT SOLTO da maquina.

O QUE ESTE PACOTE E, e por que ele nao tem longo. A porta do YPP que esta ao
alcance e a PORTA 1 — 500 inscritos mais 3 milhoes de views de Shorts em 90
dias — e o que falta nela e alcance de SHORT: 33.333 views/dia num canal contra
~2.000 que fazemos hoje. Enquanto cada short exigisse um longo de oito minutos
de carona, sete shorts/dia por canal era impossivel por construcao, e os longos
que vinham junto mediam ZERO view em nove de treze pacotes. Este e o primeiro
pacote da esteira nova: `longo: []`, so o vertical.

DE ONDE ELE SAI: do longo JA PUBLICADO `NNgAQLlpEzg` (labtreinamento-013,
vale-transporte), e e para ele que o CTA aponta — `longo_existente` na spec. Ou
seja, o short solto nao e conteudo novo solto no vazio: e uma segunda porta de
entrada para um longo que existe e esta com zero view.

O ANGULO E OUTRO, de proposito. O short do 013 ("Seu vale-transporte saiu do
bruto?") ataca a armadilha da BASE — seis por cento tirados do bruto em vez do
salario basico. Este ataca a armadilha do TETO: quem gasta MENOS que seis por
cento no mes nao pode ter o teto descontado, porque sem parcela que exceda nao
ha o que ratear. E a mesma norma, e a conta e outra, e o publico e outro — quem
mora perto do trabalho.

ALAVANCA ATACADA: A (alcance por short), e e a primeira rodada em que ela e a
alavanca principal. O portao de distribuicao da Short e o abandono nos TRES
primeiros segundos: alvo abaixo de 25%, e acima de 40% a distribuicao para no
lote semeado de 200 a 500 impressoes. Por isso a cena um nao explica nada — ela
faz uma acusacao enderecada ("o seu desconto provavelmente esta maior do que
podia") a um publico que se reconhece na primeira palavra ("se voce mora perto
do trabalho"). E o motion entrou LIGADO: gancho visual bate gancho verbal nesse
primeiro segundo.

NUMERO DE PARTIDA, 07/10 09:50: mediana de ~300 views por short no canal,
recorde da frota 1.714, alvo da Porta 1 ~4.800 por short. Experimento 33
(`motion-no-short`) esta aberto com quatro fraquezas declaradas, e a maior e
que eu NAO MECO abandono nem conclusao sem `yt-analytics.readonly` — este
numero sai em views, que e o resultado e nao o mecanismo.

O QUE O FEED DE TENDENCIA MOSTROU: a leitura das 09:20 (BR/26, e a 26 e PROXY
porque a 27 nao tem chart) grafou "Como saber se tem alguem MEXENDO NO SEU
CELULAR" — descobrir sozinho, sem ferramenta, se algo que te afeta esta
acontecendo. A cena um deste short e esse molde em sete palavras.

# ============================= AVISO SOBRE OS NUMEROS =========================
#
# MESMAS DUAS FONTES do labtreinamento-013, as duas lidas ao vivo em 07/10 pelo
# `pg_net` com cabecalho `User-Agent` (aprendizado 625):
#
#   (1) Lei n. 7.418/1985, art. 4., paragrafo unico — planalto.gov.br: "a ajuda
#       de custo equivalente a parcela que exceder a 6% (seis por cento) de seu
#       salario basico".
#   (2) Decreto n. 10.854/2021, art. 114 — planalto.gov.br: o beneficiario
#       custeia "a parcela equivalente a seis por cento de seu salario basico ou
#       vencimento, excluidos quaisquer adicionais ou vantagens" e o empregador
#       "no que exceder a parcela de que trata o inciso I". O art. 116 trata
#       expressamente da hipotese de a despesa ser INFERIOR a seis por cento.
#
# O NUMERO QUE DECIDE E DO ESPECTADOR: a norma da o percentual e a base; o
# resultado sai da passagem que ele paga, das viagens que ele faz e dos dias que
# ele trabalha. Nenhum numero meu entra no resultado, e por isso este short nao
# cita tarifa de cidade nenhuma nem salario de ninguem.
#
# O QUE FOI DESCARTADO: qualquer valor de tarifa (sem duas fontes para nenhuma
# cidade, e tarifa muda) e qualquer afirmacao sobre quantas empresas erram esse
# desconto (nao ha medicao e eu nao inventei uma).
#
# =============================================================================
"""

# Short solto: nenhuma cena de longo. O `etapas.py` le `longo` vazio, marca
# SO_SHORT e pula as etapas 1.5 a 7 inteiras.
CENAS = []

SHORT = [
    {"layout": "titulo", "kicker": "Mora perto?", "sub": "então confira",
     "nar": "Se você mora perto do trabalho, o desconto do vale-transporte na "
            "sua folha provavelmente está maior do que podia.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Seis por cento", "sub": "é teto, não valor",
     "nar": "Seis por cento do salário básico é o TETO do desconto. Não é o "
            "valor dele, e a folha trata como se fosse.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "A outra conta", "sub": "essa é sua",
     "nar": "A outra conta é passagem vezes viagens por dia vezes dias "
            "trabalhados. É o seu gasto real do mês.",
     "sem_cap": True},
    {"layout": "titulo", "kicker": "Vale a menor", "sub": "sempre a menor",
     "nar": "O que pode sair da sua folha é a MENOR das duas. Gastou menos que "
            "o teto? O desconto é o gasto.",
     "sem_cap": True},
    {"layout": "cta", "kicker": "Confira a linha", "sub": "do seu holerite",
     "nar": "Compare a menor com a linha do holerite. Se a linha estiver "
            "acima, sobrou desconto.",
     "sem_cap": True},
]

THUMB = {"l1": "Mora perto?", "l2": "confira o desconto"}

COPY = """# labtreinamento-s001

## TITULO
Vale-Transporte: Quem Mora Perto do Trabalho Costuma Pagar Desconto a Mais

## TITULO SHORT
Mora perto? Confira o desconto na folha

## DESCRICAO
Seis por cento do salário básico é o TETO do desconto de vale-transporte, não o valor dele. Essa distinção decide quem paga a mais, e quem paga a mais costuma ser exatamente quem mora perto do trabalho. A lei fala da ajuda de custo equivalente à parcela que EXCEDER seis por cento do salário básico, e o decreto que a regulamenta repete: o beneficiário custeia a parcela equivalente a esse percentual e o empregador custeia no que exceder. Se o seu gasto real de transporte no mês ficou abaixo do teto, não existe parcela a exceder — e aí o desconto tem de ser o gasto real, não o percentual cheio.

São duas contas e vale sempre a menor. A primeira é seis por cento do salário básico sozinho, sem hora extra, sem adicional noturno, sem insalubridade, sem periculosidade, sem gratificação e sem comissão. A segunda é sua e não está em documento nenhum: valor da passagem, vezes quantas você paga por dia, vezes quantos dias você trabalha no mês. A linha do seu holerite tem de ser igual à menor das duas, e se ela estiver acima disso sobrou desconto.

Quem mais cai nesse caso: quem mora perto e paga uma passagem só por dia, quem trabalha em escala com poucos dias no mês, e quem teve mês de férias ou afastamento. O decreto trata esse caso de um jeito específico — na hipótese de a despesa ser inferior ao percentual, o empregado pode optar por receber o vale antecipado, com o valor descontado integralmente depois.

A conta inteira, com o exemplo passo a passo, a armadilha da base (seis por cento tirados do bruto em vez do salário básico) e a exceção de quem é pago por tarefa ou só de comissão, está no vídeo completo linkado aqui.

Conteúdo informativo, não é consultoria jurídica, trabalhista nem contábil.

## COMENTARIO FIXADO
Duas contas e vale sempre a MENOR: seis por cento do salário BÁSICO sozinho (sem hora extra, adicional, insalubridade, periculosidade, gratificação ou comissão) e o seu gasto real do mês (passagem vezes viagens por dia vezes dias trabalhados). Se o seu gasto ficou abaixo do teto, o desconto é o gasto — não o teto. Se fizer a conta, escreva aqui se bateu, sem nome de empresa e sem o seu salário.

## HASHTAGS
#ValeTransporte #Holerite #LabTreinamento

## TAGS
vale transporte, desconto em folha, holerite, salario basico, mora perto do trabalho, folha de pagamento, direitos do trabalhador, conferir holerite, departamento pessoal, transporte coletivo, calculo de desconto, escala de trabalho, lab treinamento, seis por cento, teto de desconto

## CONFIGURACOES DO STUDIO
# NOTA: `categoryId` aqui e DECLARATIVO e o codigo ignora — publicar.py tem 27
# fixo. Escrito 27 porque e o que o video realmente recebe. Aprendizado 610.
privacyStatus: public
defaultLanguage: pt-BR
defaultAudioLanguage: pt-BR
categoryId: 27
madeForKids: false

## MUSICA / LICENCA
{TRILHA}

## AVISO SOBRE OS NUMEROS
DUAS FONTES INSTITUCIONAIS QUE BATEM, as mesmas do labtreinamento-013 e as duas
lidas ao vivo em 07/10:
  Lei n. 7.418/1985, art. 4., paragrafo unico (planalto.gov.br) — "a ajuda de
  custo equivalente a parcela que exceder a 6% (seis por cento) de seu salario
  basico";
  Decreto n. 10.854/2021, art. 114 e 116 (planalto.gov.br) — o beneficiario
  custeia "a parcela equivalente a seis por cento de seu salario basico ou
  vencimento, excluidos quaisquer adicionais ou vantagens", o empregador "no que
  exceder", e o art. 116 trata da hipotese de a despesa ser INFERIOR a esse
  percentual.

O NUMERO QUE DECIDE E DO ESPECTADOR. A norma da o percentual e a base; o
resultado sai da passagem que ele paga, das viagens que ele faz e dos dias que
ele trabalha.

DESCARTADO: valor de tarifa de qualquer cidade (sem duas fontes, e tarifa muda)
e qualquer afirmacao sobre quantas empresas erram esse desconto (sem medicao).

## FONTES
Lei n. 7.418/1985, art. 4., paragrafo unico — planalto.gov.br.
Decreto n. 10.854/2021, art. 114 e 116 — planalto.gov.br.
"""

SPEC = {
    "slug": "labtreinamento",
    "pacote": "labtreinamento-s001",
    "idioma": "pt-BR",
    "voz": "pt-BR-ThalitaMultilingualNeural",
    "trilha": "Inspired",
    "paleta": {"ink": "#22333B", "c1": "#A4243B", "c2": "#D8973C",
               "bg": "#F4F1EA"},
    "thumb": THUMB,
    "longo": CENAS,
    "short": SHORT,
    # De qual longo JA PUBLICADO este short foi extraido. O `publicar.py` usa
    # para apontar o CTA do short solto, que de outro modo subiria sem destino.
    "longo_existente": "NNgAQLlpEzg",
    "copy": COPY,
}

if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, "fabrica")
    from grava_spec import grava
    from ensaio import duracao_estimada_short
    grava(SPEC, "fabrica/specs/labtreinamento-s001.json")
    s = duracao_estimada_short(SHORT, SPEC["voz"])
    tam = [len(c["nar"]) for c in SHORT]
    print(f"SHORT SOLTO | cenas longo: {len(CENAS)} | short: {len(SHORT)}")
    print(f"estimativa short: {s:.1f}s (teto do portao 43.1s)")
    print(f"narracao: media {sum(tam)/len(tam):.0f} chars, menor {min(tam)}, maior {max(tam)}")
    print(f"aponta para o longo: {SPEC['longo_existente']}")
