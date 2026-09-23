# PROTOCOLO — checar antes de publicar, e o que fazer quando não dá

Vale para **toda rotina que cria ou publica conteúdo**: os três "OPC — publicar",
"OPC — vídeo longo", "Instagram OPC — publicar a próxima da fila" e "OPC — troca de
criativo em 48h (REGRA V3)".

Nasceu de um erro concreto em 23/09: montei dez criativos, prometi que subiriam e só
descobri na hora de publicar que a conta estava fechada para escrita. **A checagem custa
uma chamada; descobrir no fim custa o trabalho todo.**

## A regra

**Checar ANTES de produzir, não depois.** Se o canal está fechado, isso muda o que a
rodada faz — e a rodada ainda entrega algo, mas outra coisa.

## Checagem por canal

### Meta (anúncios)

Três chamadas, nesta ordem. A primeira sozinha já decide.

1. **`ads_get_ad_accounts`** — achar a conta e ler `account_status`. **Paginar até achar**:
   a conta do OPC aparece só na terceira página. `ACTIVE` segue; `UNSETTLED`, `DISABLED` ou
   `CLOSED` para. Este campo vale mais que qualquer mensagem de erro.
2. **`ads_create_ad`** com um `creative_id` que já existe — o teste de escrita mais barato.
   `Ad account not writable` confirma o bloqueio. (`ads_create_creative` devolve um
   `Permission Error` genérico que engana; não usar para diagnosticar.)
3. **`ads_get_ad_account_pages`** — se o anúncio for de formulário, conferir
   `leadgen_tos_accepted`. Se `false`, o anúncio não roda mesmo com a conta liberada.

### Instagram e outras contas do Pablo

Publicação é **sempre manual dele** — envio, curtida, seguir e comentário. A rotina prepara
e entrega; não posta. Isso não é bloqueio, é a regra permanente.

### YouTube e vídeo

Conferir a chave e a cota do provedor antes de renderizar. Render é caro; falhar depois de
renderizar desperdiça a rodada inteira.

## A alternativa — o que a rodada faz quando o canal está fechado

Não é pular a rodada. É **produzir e deixar pronto**, na ordem:

1. **Produzir assim mesmo.** Arte, copy, título, descrição, CTA — tudo o que não depende do
   canal. O bloqueio é de publicação, não de criação.
2. **Versionar no repositório.** Imagens em `entregas/campanha/imagens/`, textos num
   documento único com título, texto primário, descrição e CTA de cada peça. Critério: quem
   abrir o documento consegue subir no Gerenciador sem reescrever nada.
3. **Registrar o bloqueio com a mensagem exata** da plataforma, em LICOES — não a
   interpretação, o texto literal e o código.
4. **Avisar o Pablo uma vez**, dizendo o que fazer para destravar. Não repetir nas rodadas
   seguintes: se o estado não mudou, a rodada segue em silêncio.
5. **Reconferir no início da rodada seguinte.** Se destravou, publicar o acumulado antes de
   produzir coisa nova.

## O que não fazer

- **Não prometer publicação antes de testar a escrita.** Dizer "vou subir" e voltar com
  "não deu" custa confiança e custa a rodada.
- **Não insistir em outros conectores** quando o motivo é status da conta. Em 23/09 foram
  testados Facebook MCP, Composio e Windsor: o bloqueio é da conta, nenhum caminho passa.
- **Não tentar rascunho como contorno.** Criar rascunho também é escrita e recebe o mesmo
  erro. Testado.
- **Não repetir o aviso** a cada rodada. Uma vez, com o que destrava.
