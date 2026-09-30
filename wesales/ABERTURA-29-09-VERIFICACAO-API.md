# Abertura 29/09 — o que a API provou, medido em 27/09/2026

Este arquivo NAO registra execucao pela tela. Nada foi clicado no CRM: a sessao que
o escreveu roda em container na nuvem, sem browser e sem acesso ao Chrome logado.
O que esta aqui foi lido pela API do GHL (MCP), subconta `1D53YTI9C7oIMBavcQxV`,
e serve para quem for executar pela tela na terca.

## 1. Divergencia que bloqueia o item 8

O item 8 pede para conferir que a ficha de um lead mostra os campos N/T/B/A com
"os tres (anuncio) preenchidos". Na conta existem exatamente tres campos `(anuncio)`:

| Campo | id | Gerson De Souza Pia (`WOf6FTgB36ZhjtQ6foM8`) |
|---|---|---|
| `N · Necessidade (anuncio)` | `OJQEsl5dV37pfVY2sIaB` | **VAZIO** — o campo nao aparece na ficha |
| `T · Urgencia (anuncio)` | `2LnUD4KYSGkIBwiUdzl3` | `Pra ontem` — ok |
| `B · Investimento mensal em anuncios (anuncio)` | `bQithNwReQIBGlZBaNlI` | `Abaixo de 5k` — **valor fora da lista** |

Dois problemas, nao um:

1. **Necessidade nasce vazia.** O lead entrou por Facebook (`LEADS I FORM I FS1`,
   anuncio `120247466750200766`) em 20/09 e foi atualizado em 27/09, e ainda assim
   `OJQEsl5dV37pfVY2sIaB` nunca recebeu valor. `N · Dor principal`
   (`qmIKSSDVYNLl5E8vnr3f` = "Falta de novos clientes") esta preenchido, o que sugere
   que o mapeamento do formulario do anuncio manda a dor para o campo errado, ou que
   Necessidade nao esta mapeada.

2. **Investimento guarda um valor que a picklist nao aceita.** As opcoes do campo sao
   `Ate 1k` / `1k a 5k` / `5k a 10k` / `Acima de 10k`. O valor gravado e `Abaixo de 5k`,
   que nao e nenhuma delas. Valor fora da lista nao casa em condicao de workflow nem
   em filtro de lista inteligente — qualquer automacao que ramifique por faixa de
   investimento vai tratar este lead como indefinido.

Nao corrigi nenhum dos dois. O primeiro e mapeamento de formulario de anuncio (fora do
CRM), o segundo exige decidir se a picklist muda para aceitar o que o anuncio manda ou
se o anuncio passa a mandar o que a picklist aceita. As duas decisoes sao suas.

## 2. Item 3 — a lista "SDR responsavel" esta como o documento previa

`SDR responsavel` (`e1n7As703nqjAOpzREHc`, criado 27/09/2026 17:06) e
`SINGLE_OPTIONS` com **uma unica opcao: `Pablo Santos`**. Confirma que o passo de
acrescentar o SDR continua pendente. Falta o nome e o e-mail do SDR para criar o
usuario — nao foram informados.

## 3. Item 4 — merge fields conferidos, prontos para colar

Os 13 campos BANT existem todos. As `fieldKey` do GHL perdem os acentos de forma
irregular (`urgncia`, `anncios`, `sdr_responsvel`, `clientes_novos_por_ms`), entao
digitar "de cabeca" quebra o merge field em silencio: ele renderiza vazio, sem erro.
Copie destas linhas, na ordem pedida:

```
Necessidade: {{contact.necessidade}}
Dor principal: {{contact.dor_principal}}
Clientes novos por mes: {{contact.clientes_novos_por_ms}}
Quem atende os leads: {{contact.quem_atende_os_leads}}
Tem time comercial: {{contact.tem_time_comercial}}
Urgencia: {{contact.urgncia}}
Prazo: {{contact.prazo}}
Investimento mensal em anuncios: {{contact.investimento_mensal_em_anncios}}
Investe em anuncios: {{contact.investe_em_anncios}}
Budget: {{contact.budget}}
Decisor: {{contact.decisor}}
SDR responsavel: {{contact.sdr_responsvel}}
Empresa: {{contact.empresa}}
```

Mesmo bloco serve para o no de NOTA "REUNIAO AGENDADA" e para o "AVISO INTERNO" de
30 min antes. Nao mexer em condicoes, contadores nem na formula da nota.

## 4. Pastas de campo — ha uma terceira pasta com um campo solto

Os campos estao distribuidos em tres `parentId`, nao dois:

- `zHU4yGXKHdxBHnGxUmai` — a pasta de qualificacao (N/T/B/A, Empresa, SDR responsavel)
- `gabsbU3jsUN7oIXCnYab` — a pasta de cadencia/discador (tentativas, conexoes, datas)
- `vCqedGd185RiQKNlU870` — **contem um unico campo**, `Conexoes WhatsApp`
  (`Og1CkI9x9OztsV242nIM`)

Vale conferir na tela se essa terceira pasta e intencional ou resto de uma renomeacao.

## 5. O que continua sem execucao

Itens 1, 2, 4, 5, 6 e 7 dependem de tela (ou de `gh`, que nao existe neste container)
e nao foram executados. Alem disso, os documentos que os definem
(`LICOES-DO-PROJETO.md`, `FALTA-PARA-SER-MAQUINA.md`, `ASSOCIACOES-DE-CAMPO.md`,
`DISCADOR-CONFIG-POR-FUNCAO.md`, `ESTADO-27-09.md`) nao existem em nenhum branch nem
em nenhum commit deste repositorio, e `wesales/tools/` nao tem `login-capture.js`,
`finalizar.py`, `pastas_de_campo.py` nem `atuador_filas.py` — os tres ultimos sao
chamados por `.github/workflows/wesales-finalizar.yml`, que portanto falha hoje no
primeiro step. O texto da tarefa T1 (item 6) e a opcao B do G-04 (item 7) estao
descritos apenas nesses documentos ausentes; nao os inventei.

## 6. Funcoes decididas em 27/09

| Pessoa | Funcao no processo | Papel no GHL |
|---|---|---|
| Andreyna | SDR | `user` (nao admin) |
| Pablo Santos | Closer, e tambem gestor e administrador do sistema | admin (usuario atual) |

O usuario da Andreyna **nao foi criado**. Duas razoes, as duas reais:

1. O MCP do GHL disponivel nesta sessao nao expoe criacao de usuario. As familias
   presentes sao contatos, conversas, calendarios, oportunidades, blogs, e-mails,
   pagamentos, redes sociais e leitura de `locations` (campos e dados da subconta).
   Nao existe `users_create` nem equivalente. A criacao vive em
   Configuracoes -> Equipe na tela, ou em `POST /users/` da API v2 com um token de
   escopo `users.write` — que aqui nao esta acessivel.
2. Falta o **e-mail da Andreyna**. O GHL usa o e-mail como identidade do usuario e
   manda o convite de acesso para ele; sem e-mail nao ha usuario a criar.

Depois de criar o usuario na tela, a picklist de `SDR responsavel`
(`e1n7As703nqjAOpzREHc`) precisa receber `Andreyna` — hoje tem so `Pablo Santos`.
Isso tambem nao sai por esta sessao: nao ha ferramenta de escrita em campo
customizado no MCP. Sai pela Action `wesales-finalizar` em modo `pastas`, como o
plano previa, **desde que** `wesales/tools/finalizar.py` volte para o repositorio —
hoje o arquivo nao existe e o workflow falha antes disso.

Observacao sobre acumulo de funcao: com Pablo como closer, gestor e admin, e Andreyna
como unica SDR, a picklist `SDR responsavel` vai precisar continuar com as duas
opcoes, nao so `Andreyna` — leads trabalhados pelo Pablo antes da abertura ja apontam
para `Pablo Santos`, e trocar a opcao por outra em vez de acrescentar apagaria esse
historico nas fichas.
