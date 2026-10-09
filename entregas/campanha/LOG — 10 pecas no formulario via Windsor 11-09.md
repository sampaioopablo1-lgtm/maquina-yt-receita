# As 10 peças no conjunto de formulário — 11/09/2026, 20h50

**Publicadas pela API, sem intervenção do Pablo, dentro dos conjuntos de
formulário de fundo de funil.** Todas `PAUSED`. O V10 continua ativo e intacto.

## A manha que destravou

O bloqueio do dia inteiro era: criar um criativo com `lead_gen_form_id` exige que
a Meta leia a aceitação dos Termos de Geração de Leads da Página, e o conector do
claude.ai não pede `pages_manage_ads`, então não consegue ler (`1892181`). O
token de usuário do sistema lê, mas assina com um app em desenvolvimento
(`1885183`).

O **Windsor.ai** tem duas ações que nenhum outro servidor tinha:

- `create_ad` aceita `creative` bruto, inclusive `{"creative_id": "<id>"}`.
- `update_ad_creative` **copia o criativo atual do anúncio**, aplica só os campos
  enviados, cria o resultado como criativo novo e repõe o anúncio nele.

Juntando as duas: **criar o anúncio reusando o criativo do V10 — que já tem o
formulário dentro — e depois trocar só imagem, título, texto e descrição.** O
formulário nunca é enviado por mim; ele vem de carona na cópia. Por isso a
leitura dos termos nunca é acionada, e nenhum dos dois erros aparece.

Foi o próprio Pablo que apontou o caminho, duas vezes: *"não precisa criar
anúncio, somente mudar os criativos"* e *"formulário já está criado, precisa ser
selecionado"*. Estava certo nas duas.

**Pedra no caminho:** a primeira tentativa voltou `3858504` — "o criativo não
deve incluir aprimoramentos padrão", porque a cópia arrasta o
`degrees_of_freedom_spec` do V10 e a Meta descontinuou esse formato. Conserto:
mandar `degrees_of_freedom_spec: {}` junto, que reseta para o padrão.

**Segunda pedra:** o hotlink do Drive falhou uma vez (`3858258`, "não foi
possível baixar sua imagem") na AG06 e funcionou na repetição imediata. É
instabilidade do Drive, não da URL — repetir resolve.

## O que foi criado

Conjunto **LEADS I INTERESSE I FASE 3** (`120247356527930766`):

| Peça | Anúncio | Criativo novo |
|---|---|---|
| AG01 | `120247394004180766` | `2374168726451823` |
| AG02 | `120247394017760766` | `2269122753886592` |
| AG03 | `120247394028740766` | `1088493023630360` |
| AG04 | `120247394050340766` | `1391089386513886` |
| AG05 | `120247394053130766` | `1877162366594815` |

Conjunto **LEADS I SEMELHANTE CNAE RJ I FASE 3** (`120247356496360766`):

| Peça | Anúncio | Criativo novo |
|---|---|---|
| AG06 | `120247394055720766` | `837940866013087` |
| AG07 | `120247394063170766` | `3334264626767570` |
| AG08 | `120247394066810766` | `1489446646279074` |
| AG09 | `120247394072420766` | `1824376145401825` |
| AG10 | `120247394075690766` | `1756775198897790` |

Todos os dez são cópia do criativo `1394981662056985` (o V10) com arte e copy
trocadas. Botão **`SIGN_UP`**, igual ao V10.

## Conferências feitas

- `ads_get_errors` nos dez anúncios e nos dois do V10: **vazio**. Zero erro de
  entrega. Num conjunto `LEAD_GENERATION`, anúncio sem formulário devolveria
  `3390001` — não devolveu, então o formulário está lá.
- `ads_get_ad_preview` da AG01: arte no formato V10, foto aprovada, badge e barra
  de CTA. Botão `SIGN_UP` confirmado em `ads_get_creatives`.
- Os dois anúncios do V10 seguem `ACTIVE`. Nada foi repontado neles.
- **Nenhum campo de orçamento foi enviado em nenhuma chamada.**

## Títulos encurtados

A lição do guia do Vini Ensina foi aplicada na hora: os títulos que passavam de
40 caracteres foram encurtados antes de subir, porque o V10 — que converte — tem
32. AG01 37→33, AG02 41→29, AG03 47→30, AG04 37→28, AG05 46→29, AG06 36→25,
AG07 40→29, AG09 42→29. Nenhum título agora passa de 33.

## O que falta

Ativar. Os dez estão pausados; alguns aparecem como `PENDING_REVIEW` ou
`IN_PROCESS`, que é a revisão normal da Meta antes de poderem rodar. **Ao ativar,
lembrar que a campanha é CBO com R$20/dia**: os mesmos R$20 passam a ser
divididos com as peças novas, incluindo o V10 que traz lead a R$1,71. Aumentar o
orçamento antes de ativar é decisão do Pablo.
