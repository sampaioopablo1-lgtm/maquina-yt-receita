# As 10 peças no ar (pausadas) — 11/09/2026, 18h40

Publicadas **pela API, sem intervenção do Pablo**, com as artes que já estavam no
Drive. Todas nascem `PAUSED`, dentro da campanha `WPP I CONVERSA I FS1`, que
também está pausada — gasto zero até ele ligar.

## Por que pelo WhatsApp e não pelo formulário

O conjunto de formulário exige `lead_gen_form_id` no criativo, e criar criativo
com formulário exige que a Meta leia a aceitação dos Termos de Geração de Leads
da Página. Medido nos dois sentidos em 11/09:

- A Página **aceitou** (o Pablo mandou a tela com o visto verde).
- O conector **não consegue ler** essa aceitação: o OAuth do MCP oficial tem três
  níveis de escopo e `pages_manage_ads` não está em nenhum. A própria mensagem
  de erro diz: *"this request cannot be completed over MCP; use Ads Manager"*.
- O token de usuário do sistema lê, mas assina com o app OPC Automação, que está
  em modo de desenvolvimento (`1885183`), e o app não pode virar Modo ativo
  enquanto a página está em análise.

**Conjunto de conversa no WhatsApp não usa formulário.** Sem formulário, não há
leitura de termos, e o conector publica direto. Foi a saída — e ela entrega a
mesma promessa das peças: o cliente chega no WhatsApp.

## O que foi criado

Conjunto **WPP I INTERESSE DONOS DE EMPRESA** (`120247368235430766`):

| Peça | Anúncio | Criativo |
|---|---|---|
| AG01 — acordar com o WhatsApp cheio de cliente | `120247393010330766` | `1497124909129899` |
| AG02 — pare de depender de indicação | `120247393018660766` | `4677767485792560` |
| AG03 — seu negócio é bom, ninguém vê | `120247393019520766` | `2724731384595511` |
| AG04 — quantos clientes novos entraram hoje | `120247393020340766` | `28246272441649213` |
| AG05 — o concorrente não é melhor, só anuncia | `120247393020760766` | `2503425216734970` |

Conjunto **WPP I SEMELHANTE CNAE RJ** (`120247368229380766`):

| Peça | Anúncio | Criativo |
|---|---|---|
| AG06 — a gente escreve, publica e acompanha | `120247393028700766` | `900722136238408` |
| AG07 — seu anúncio pode estar no ar essa semana | `120247393029580766` | `1043876718480846` |
| AG08 — você já fatura, falta aparecer | `120247393030620766` | `1032875369746277` |
| AG09 — cliente novo todo dia | `120247393031750766` | `1769193384104299` |
| AG10 — não é curso, é a gente fazendo | `120247393032510766` | `1977987616246631` |

Cada criativo leva: a arte do Drive por `image_url`, o `instagram_user_id`
`17841480745368398` (sem ele não entrega no Instagram), botão
`WHATSAPP_MESSAGE`, e a descrição "A gente faz o anúncio. Você atende.".

Conferido no `ads_get_ad_preview` da AG01: arte no formato V10, foto certa,
badge laranja, barra de CTA. Nenhum campo de orçamento foi enviado em nenhuma
chamada.

## O que ainda falta

As mesmas 10 peças **no conjunto de formulário** continuam pendentes, e o
bloqueio é um só: o app precisa estar em Modo ativo. Os quatro campos que
liberam esse botão estão em `DESTRAVAR — os 4 campos que liberam o botao.md`,
com a política de privacidade e o ícone já prontos.
