# Máquina de vídeos — o que nunca deve envelhecer

A rotina horária carrega o procedimento. Este arquivo carrega só os **ponteiros**,
porque número dentro de prompt envelhece e já me fez errar quatro vezes
(652/655, 658, 682, 685). Aqui não entra contagem de estoque, nem de views, nem
de inscritos. Entra onde olhar.

## O dinamismo visual — o que mudou em 09/10 e a regra nova

O dono disse que os frames pareciam estáticos. **Medido, e ele estava certo com
folga** (aprendizado 690): no `labtreinamento-s011`, diferença **mediana** entre
quadros consecutivos de **0,39** numa escala de 0–255, e **375 de 414 quadros
(91%) abaixo de 1,0**. A média de 4,34 vinha inteira dos cinco cortes de cena.

Três causas, e a física diz onde está a alavanca:

    movimento por quadro = amplitude / (duração da cena x fps)

12% de zoom em 8,3 s dá **0,048% por quadro**. Aumentar a amplitude não
conserta — corta a borda do texto antes de ficar perceptível. **A alavanca é a
duração da cena.**

**Consertado, e é defeito e não experimento:**
- `fabrica/legenda.py` — a legenda queimada do short era UMA fala para a cena
  inteira: ~18 palavras paradas por oito segundos, na região que o olho lê.
  Agora são grupos de até **quatro** palavras, com tempo proporcional aos
  caracteres.
- `motion.filtro_bordas(dur, primeira=True)` — a cena ZERO perdeu o fade de
  entrada. Havia preto de t=0 a t=0,067, dentro do primeiro segundo, que é o que
  decide a distribuição. As emendas entre cenas continuam.

**Regra nova para spec de short solto: DEZ a ONZE cenas, mantendo a duração
total** (experimento 40). Não mexer em `ALVO_SHORT` — isso é o experimento 38, e
ele ainda não tem leitura de 12 h. O esqueleto novo quebra o `39 de 39` idêntico
de propósito: ritmo e esqueleto são a mesma mudança de forma, e com a forma nova
o aviso do portão `variedade` para de aparecer.

**CORREÇÃO, e é de uma regra que eu escrevi nesta mesma manhã:** eu havia posto
"dez a CATORZE" sem conferir a sobrecarga. Há **~1,9 s fixos por cena** no
`ensaio` (medido: 12 cenas de um caractere já somam 21,9 s). Doze cenas gastariam
22 s só em padding e estourariam o teto de 43,1. O teto real no alvo atual é
**onze**, e o ponto de equilíbrio é **10 cenas de ~40 caracteres** ou 11 de ~34.
O `kolejny-poziom-s015` saiu com 10 cenas, 41,8 est, **4,18 s por plano** contra
8,3 e **20 falas de legenda** contra 5.

**Experimento 33 (motion) foi ABORTADO** em 09/10. A própria hipótese dele
declarava "não mede o que quer medir", e ele travou três testes por dez dias
enquanto o defeito que deveria medir ficava no ar. Pode ser reaberto com
retenção de verdade quando o escopo voltar.

**O que o `chart=mostPopular` disse** (categoria 26, e isso é PROXY — 610), lido
em 09/10: o que tem milhões de views dura **10 a 35 s** — mediana 26 s no BR,
35 no PL, 30 no GR. Os nossos estão em 41–42 s porque eu os empurrei para lá.
Isso é dado contra o experimento 38, não a favor; não resolver antes da leitura
de 12 h.

**Busca na web para tendência continua inútil**, como a rotina avisa: voltou
blog de fornecedor de ferramenta de legenda, sem teste controlado e com números
que se contradizem. O único item aproveitável foi um limite de forma — quatro a
cinco palavras na tela por vez — e ele entrou porque é coerente com a medição,
não porque a fonte é boa.

## Autorização permanente do dono (09/10/2026)

Palavras dele: *"Deixe 100% automático, sem precisar de aprovação. Usando toda
cota possível nos 3 canais."* Vale como autorização durável para a produção:
**não pare para pedir aprovação de pauta, render, publicação ou pacote
completo.** O "pacote completo exige janela dedicada do dono" CAIU — era
aprovação, e ela foi dada.

**O que a autorização NÃO cobre, porque é irreversível e ele não falou disso:**
apagar vídeo publicado e apagar as 46 duplicatas. A trava continua.

**E o que ela não pode destravar, porque não é aprovação:** os três secrets
`YT_TOKEN_<CANAL>` no GitHub (o proxy desta sessão bloqueia a API de secrets) e
o clique no link de consentimento do Google. Ver
`docs/reautorizar-analytics.md`.

## A restrição real é PAUTA, não cota nem aprovação

Medido em 09/10: **10 origens livres** (epomeno 4, kolejny 4, labtreinamento 2),
contra ~14 peças publicadas no dia. **Menos de um dia de pauta.** Cota não é o
limite; origem é. E origem só nasce de LONGO novo.

Isso converge com o 689: o longo converte ~5x melhor por view **e** gera pauta
**e** satisfaz os 3 uploads públicos/90 dias da Porta 1. Logo **pacote completo
deixa de ser exceção e passa a ser a produção principal** quando a pauta estiver
baixa.

## Por que NÃO aumentar o número de canais

O dono deu liberdade para isso. A aritmética diz não: **os 500 inscritos são um
limite POR CANAL.** Dividir ~2.100 views/dia em mais canais afasta cada um do
limite em vez de aproximar — concentração vence dispersão quando o portão é por
canal. Ele mesmo cortou de 13 para 3 em 07/10, e a conversão medida (1,0 a 1,3
por mil) exige acumular view no MESMO canal. Reabrir canal só faz sentido depois
de UM canal passar a Porta 1.

## O escopo de analytics NÃO foi negado — nós o perdemos

**Corrige onze afirmações minhas** (aprendizado 689, `crítico`). O banco tem
**388 linhas de retenção real** vinda da YouTube Analytics API
(`averageViewPercentage`, `subscribersGained`), em **doze canais**, incluindo os
três da frota — e todas param em **20/09/2026**. O escopo funcionou e foi
perdido: `ESCOPOS` em `fabrica/tokens.py` lista só `youtube`,
`youtube.force-ssl` e `youtube.upload`, e o `tokeninfo` do token atual confirma
esses três e nenhum outro. Como os refresh tokens morriam de sete em sete dias
(303), cada reautorização reemitiu o token pela nossa lista, sem analytics.

**Antes de chamar uma capacidade de "não autorizada", procure no banco se ela já
produziu dado, e confira a lista de escopos do próprio código.**

O que esses dados já dizem, com atribuição POR VÍDEO:

| | retenção média | inscritos | views | por mil |
|---|---|---|---|---|
| shorts | **45,1%** (n=72) | 23 | 18.693 | **1,23** |
| longos | **20,9%** (n=103) | 17 | 2.733 | **6,22** |

O longo converte ~5x melhor **por view** — o que contradiz "o longo deixou de
ser alavanca". Amostra pequena e janela de uma coleta só: trate como o melhor
dado disponível, não como conclusão.

## Antes de ler qualquer contador

**Três leituras na mesma rodada, e o estimador é o MÁXIMO declarado como PISO,
com a faixa ao lado — NÃO a mediana.** Medido em 09/10/2026 (aprendizado 688,
`crítico`): das 17 peças que mudaram entre três leituras de 3 s, **todas as 17
subiram na terceira e nenhuma na segunda**. View não sobe simultaneamente em 17
vídeos de três canais em três segundos — as leituras 1 e 2 caem numa réplica e a
3 numa mais fresca, e a mediana virou o mínimo em 17 de 17. Um contador de view
só **atrasa**, nunca adianta.

**Inscrito e view DE CANAL não se leem de hora em hora** (686): o
`channels.list` devolveu statistics byte a byte idênticas em duas leituras
separadas por uma hora, nos três canais, enquanto peças individuais subiam.
Compare só leituras separadas por ≥ ~4 h, e nunca conte N leituras horárias
iguais como N observações.

## Antes de escolher pauta
- `consultas/estoque.sql` — **rode a consulta.** É a única fonte de origem livre.
  Nenhuma lista de memória, à mão, ou escrita num prompt decide nada.
- `docs/estoque.md` — por que a lista à mão foi abolida, o aviso de PERFIL e as
  faixas de identidade por canal.

## Antes de dizer que a máquina está sã
- `python3 -m pytest tests -q --ignore=tests/test_mcp.py --ignore=tests/test_banco_de_pautas.py`
  Linha de base medida em 09/10/2026: **25 falham, 2.048 passam, 436 skip.**
  Falha nova é a sua; as 25 são conhecidas (specs já publicadas que o
  `prontidao` recusa por título duplicado, e fonte Devanagari ausente — as duas
  são o portão funcionando).
- `python3 fabrica/prontidao.py fabrica/specs/<spec>.json` — **passe o caminho
  do .json**, não o nome do pacote. São **doze** portões, **onze** no short
  solto (`capitulos` sai de fora em vez de aprovar em silêncio).

## Os portões que decidem monetização, não estética
- `fabrica/variedade.py` — conteúdo **inautêntico** (elegibilidade do YPP, não
  remoção; renomeação de 15/07/2025). Reprova gancho acima de 12 palavras e
  thumbnail acima de 4; **avisa** quando o esqueleto do short repete.
  Leia `docs/mapa-canal-dark-o-que-entrou.md` antes de mexer nos limiares —
  eles são do mapa do dono, não meus, e o aviso só avisa por causa da trava do
  experimento 33.
- `fabrica/ensaio.py` → `ALVO_SHORT` — **onde** mirar dentro da faixa depende da
  VOZ: piso no polonês (resíduo positivo), topo no grego e no pt-BR.

## Antes de citar número de aprendizado
`select max(id) from aprendizados` no projeto **vevocauwtarctfwngrch**.
O `APRENDIZADOS.md` do repo está desatualizado contra o banco.

## Entrega
`docs/publicar-pela-sandbox.md` e `docs/schema-supabase.md`. O render é no
runner com `publicar=false`; a publicação é pela ponte. O zip do artefato abre
**flat** e o `conduz.py` espera `f/<pacote>/`.

## As travas que não se negociam
Estão na rotina horária, e nenhuma delas muda por conveniência de uma rodada.
A que mais custa esquecer: **não apague vídeo publicado sem o dono dizer.**
