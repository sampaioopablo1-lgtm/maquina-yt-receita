# Flyer — Programa Modo Turbo 30 Dias (Turbo 7)

Peça de divulgação do programa **Modo Turbo**, construída sobre o fluxo de
cadência **12 × 30**: 12 toques distribuídos em 30 dias, cruzando 2 a 3 canais
nos dias de pico.

## Entregáveis

| Arquivo | Formato | Uso |
| --- | --- | --- |
| `flyer-turbo7-modo-turbo-30-dias.png` | 2400 × 4320 px (1:1,8, 2×) | WhatsApp, Instagram, e-mail, apresentações |
| `flyer-turbo7-modo-turbo-30-dias.pdf`  | 12,5 × 22,5 in, 1 página | Impressão e envio comercial |
| `apresentacao.html` | Página autocontida | Link de apresentação (publicado como Artifact) |
| `proposta.html` | Página autocontida | Proposta comercial: diagnóstico, método, plano e preço |
| `funil-marketing-vendas-turbo7.png` | 2400 × 3168 px (2×) | Mapa de responsabilidade no funil |
| `funil-marketing-vendas-turbo7.pdf`  | 12,5 × 16,5 in, 1 página | Impressão e reunião de alinhamento |

## Fontes do projeto

| Arquivo | Papel |
| --- | --- |
| `FILOSOFIA-DE-DESIGN.md` | Manifesto visual (*Cadência Instrumental*) que rege a peça |
| `build.py` | Gera `flyer.html` — conteúdo, cadência e diagrama são dados, não markup solto |
| `flyer.html` | Artefato gerado (não editar à mão; editar `build.py`) |
| `render.py` | Rasteriza o HTML em PNG 2× e PDF via Chromium headless |
| `build_pagina.py` | Gera `apresentacao.html`; guarda o `CSS_BASE` que as duas páginas usam |
| `build_proposta.py` | Gera `proposta.html` — diagnóstico, fases, compromissos e oferta |
| `build_funil.py` | Gera `funil.html` — o mapa de etapas, metas e responsáveis |
| `build_site.py` | Gera `site/`, versão hospedável da apresentação |
| `fonts/` | Big Shoulders, Outfit e Geist Mono (licença OFL) |

## Como regerar

```bash
cd design/turbo7-modo-turbo-30-dias
python3 build.py         # HTML do flyer a partir do conteúdo estruturado
python3 build_funil.py   # HTML do mapa de funil
python3 render.py        # PNG 2x + PDF das duas peças (ou passe um .html específico)
python3 build_pagina.py  # página de apresentação (usa o PNG já renderizado)
python3 build_proposta.py # página de proposta comercial
python3 build_site.py    # site estático publicável
```

Requer `pillow` e o Chromium apontado em `render.py:CHROME`.

## Publicar o site

`build_site.py` emite `site/`, que é um site estático pronto — sem build step.
`netlify.toml` na raiz já aponta o `publish` para essa pasta, então basta
conectar o repositório ao projeto Netlify `modo-turbo-turbo7` (ou arrastar a
pasta `site/` para o deploy manual da Netlify).

`BASE_URL` em `build_site.py` alimenta as tags Open Graph, que exigem URL
absoluta. Se o domínio mudar, atualize a constante e regere — senão o preview
do link no WhatsApp aponta para o endereço antigo.

## Onde mexer no conteúdo

Tudo o que é editorial está no topo de `build.py`:

- `CADENCIA` — os 12 toques: `(dia, (canais...))`, com cada canal em `MSG`,
  `CALL_WA` ou `CALL`. Um dia pode acionar 1, 2 ou 3 canais; a pilha de glifos
  no diagrama cresce junto, e os dias de mais de um canal ganham o anel verde
  de pico. Alterar a lista redesenha o diagrama inteiro.
- `TOTAL_CONTATOS` — derivado da cadência, nunca digitado à mão: é o número que
  aparece na nota sob a legenda e na página.
- `ABANDONO` / `CONVERSAO` — os intervalos de toques marcados pelas chaves
  vermelha e verde acima do eixo.
- `INCLUSOS` — os três itens de escopo.
- `GESTAO_LEAD`, `GESTAO_TEXTO`, `METRICAS` — a seção de acompanhamento de
  performance: a frase-âncora, o texto e os eixos rastreados nas reuniões.
- `BONUS_METAS` / `BONUS_PREMIO` — as metas diárias do captador e o prêmio que
  elas destravam. A faixa é desenhada como equação, então acrescentar uma
  terceira meta só exige mais um item na lista.
- `LEGENDA` — rótulos dos canais.

E em `build_funil.py`:

- `ETAPAS` — a lista `(dono, nome, descrição, meta, responsável)`. O afunilamento,
  a numeração, a divisão em zonas e a contagem no cabeçalho saem daí; mover uma
  etapa de `MKT` para `VND` reposiciona a fronteira sozinha.
- `FRONTEIRA` / `RODAPE` — o bloco de passagem de bastão e a nota de gestão.
- `LARGURA_TOPO` / `LARGURA_BASE` — quanto o funil afunila, em %.

E em `build_proposta.py`:

- `MERCADO` / `CLIENTE` / `AVISTA` / `PARCELAS` — a tabela de preços. Os descontos,
  o valor da parcela e a economia do à vista são calculados a partir deles, nunca
  digitados: mudar `CLIENTE` reescreve o selo de %, a nota do cartão e a condição.
- `FASES` — a lista `(nome, duração, janela, objetivo, entregas, sinal)`. A `janela`
  é o par de colunas na régua `MESES`, e é dela que sai a barra do cronograma. Uma
  fase cuja janela ultrapassa a régua é tratada como aberta: o rótulo do sinal muda
  de “fase fechou” para “fase está saudável”, porque ela não termina.
- `MESES` — a régua do cronograma. Acrescentar um mês realinha as barras sozinho.
- `CONDICOES` — as três notas sob a tabela de preços.
- `COMPROMISSOS` — o que o programa depende do cliente. Proposta que só lista o
  que o fornecedor entrega esconde metade do combinado.
- `VALIDADE` — o prazo da proposta, sob a tabela de preços.
- `PERGUNTAS` — o diagnóstico que abre a página. A numeração e o “{n} perguntas”
  do título saem do tamanho da lista, então acrescentar uma pergunta basta.
- `ABERTURA` / `VEREDITO` / `VEREDITO_NOTA` — a copy que emoldura o diagnóstico.
- `TORNEIRA` — o SVG da torneira pingando. Usa só tokens do tema, então um único
  desenho serve ao claro e ao escuro.

Copy da manchete, alerta, estatísticas e bloco de oferta ficam no `TEMPLATE`,
na mesma seção do arquivo.

## Decisões de design

- **Paleta restrita**: violeta profundo, verde elétrico e branco. O vermelho
  aparece uma única vez — no alerta de perda de receita — para que o alerta
  tenha peso.
- **O diagrama é o argumento**: o mapa 12 × 30 ocupa o centro óptico da peça.
  A chave vermelha marca os toques 3 e 4 (dias 5 e 7), onde a maioria dos
  times para; a verde marca os toques 5 a 12, onde a conversão acontece.
- **A pilha mede a intensidade**: dias de pico cruzam 2 ou 3 canais, e a coluna
  fica visivelmente mais alta. A quantidade de contato vira altura no eixo, sem
  precisar de rótulo.
- **Gestão é seção, não item de lista**: o acompanhamento semanal saiu da grade
  de escopo e ganhou bloco próprio, com os eixos que a reunião revisa — volume
  de ligações, alcance das mensagens e qualidade das conversas.
- **O bônus é uma equação**: as duas metas diárias somam e um conector atravessa
  o vão até o prêmio, o único bloco de verde chapado antes do CTA. As metas são
  as mesmas grandezas que a reunião semanal acompanha — a faixa fecha o ciclo
  entre o que se mede e o que se ganha.
- **Oferta em dois tempos**: o valor do programa (R$ 20.000) e o que o cliente
  paga para começar (R$ 0 nos primeiros 30 dias) aparecem lado a lado, sem
  ambiguidade sobre o preço.
- **Glifos próprios**: os três canais usam ícones desenhados para a peça, não
  logomarcas de terceiros — mensagem, ligação pelo app e ligação convencional
  se distinguem por cor e preenchimento, com legenda explícita.
- **Duas páginas, um sistema**: a apresentação explica o programa, a proposta o
  vende. Os tokens, a tipografia e os componentes moram no `CSS_BASE` de
  `build_pagina.py` e servem às duas — escopo, gestão, métricas e bônus são as
  mesmas funções, então as peças não conseguem divergir. Cada página aponta para
  a outra pelo mesmo componente de atalho.
- **O cronograma mostra a sobreposição em vez de escondê-la**: a fase 3 começa no
  3º mês, quando a fase 2 ainda roda. As barras ficam em linhas diferentes e a
  sobreposição aparece — é informação sobre como a implantação funciona, não um
  erro de alinhamento a ser disfarçado.
- **A proposta tem a ordem de uma proposta**: diagnóstico → método → escopo →
  gestão → plano de implantação → co-responsabilidade → preço → próximo passo.
  O preço é a penúltima seção, não a primeira. Quem não enxerga a goteira acha
  caro qualquer número; quem acabou de falhar em responder oito perguntas sobre o
  próprio processo lê o preço como conserto. Nenhuma pergunta é retórica — todas
  têm resposta numérica, e é o silêncio diante delas que faz o argumento.
- **A proposta não é um resumo da apresentação**: ela carrega as mesmas seções
  inteiras — funil, cadência, flyer, escopo, gestão, bônus — porque quem recebe
  uma proposta não deveria precisar de um segundo link para entender o que está
  comprando. São as mesmas funções de `build_pagina`, só reordenadas.
- **A torneira é ilustração própria, não banco de imagem**: corpo cheio em
  `--ink`, especular em `--surface` para dar volume ao metal, gota e poça em
  `--accent`. Como só usa tokens do tema, um desenho serve ao claro e ao escuro.
  A bancada termina antes do bico: o que cai, cai na cuba, e a linha não cruza a
  trajetória da gota.
- **A âncora antes do preço**: R$ 50.000 riscado, depois R$ 25.000, depois o à
  vista em verde chapado. A ordem de leitura é a ordem do argumento comercial, e
  o único bloco de cor sólida é aquele para onde a proposta quer levar.
- **A página carrega leve**: o flyer embutido na apresentação é WebP a 1600px de
  largura (~300 KB), não o PNG de origem — a página inteira sai de 3,6 MB para
  ~790 KB, o que muda o tempo de abertura no 4G de um cliente. O PNG 2400 × 4320
  continua intacto como arquivo de download, para WhatsApp e impressão.
- **O funil abre a página**: na apresentação web ele vem antes do flyer, com um
  parágrafo de contexto — primeiro se estabelece de quem é cada etapa, depois se
  mostra o programa que roda a metade de vendas. Ali o funil é HTML nativo, não a
  imagem: fica legível no celular, o texto é selecionável e o afunilamento só é
  aplicado acima de 820px, onde há largura para ele significar algo.
- **No funil, a fronteira é o assunto**: marketing em lilás, vendas em verde, e
  entre os dois uma faixa que atravessa a peça inteira — inclusive as colunas de
  meta e responsável. O afunilamento carrega a metáfora; a tabela ao lado carrega
  o dado. A peça responde "de quem é este lead agora?", que é a pergunta que o
  cliente faz.

## Observações

O texto do flyer reproduz as afirmações comerciais fornecidas para a peça
(“+80% das conversões vêm da 4ª tentativa em diante”, “5 novos leads por dia”).
São alegações da campanha, não dados medidos neste repositório — vale conferir
a fonte antes de veicular.

**Como as duas páginas nomeiam o mesmo R$ 20.000.** Na apresentação, R$ 20.000 é
“valor do programa”, com os primeiros 30 dias gratuitos para novos clientes. Na
proposta, R$ 20.000 é o preço *à vista* para quem já é cliente, ancorado nos
R$ 50.000 de mercado. São duas ofertas para dois públicos, mas o mesmo número
aparece com dois rótulos — se as páginas forem enviadas juntas ao mesmo cliente,
vale unificar o discurso antes.

**Divergência conhecida entre as duas peças.** O flyer projeta a alimentação da
cadência em *5 novos leads por dia* (≈150/mês); o funil registra a meta de
marketing em *100 leads/mês, no mínimo* (≈3,3/dia). São números de briefings
diferentes — um é a projeção de volume da máquina de vendas, o outro é o
compromisso do marketing — mas contradizem se as duas peças forem mostradas
juntas. Alinhar exige decisão comercial, não de design.
