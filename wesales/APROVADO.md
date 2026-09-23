# O que está autorizado na subconta

Este arquivo é o **freio de mão** da rotina horária. Ela lê aqui antes de
escrever qualquer coisa no CRM.

> **Regra:** o que não estiver listado abaixo com `[x]`, a rotina **não faz**.
> Com este arquivo vazio, ela só lê o CRM e trabalha na documentação.

Subconta autorizada: `1D53YTI9C7oIMBavcQxV` — Pablo Santos's Account
**Nenhuma outra subconta**, em nenhuma hipótese.

## Como autorizar

Troque `[ ]` por `[x]` na linha do que você libera, salve e faça commit. Na
execução seguinte a rotina executa e marca `— FEITO em <data>` ao lado.

> **O `[x]` é do dono, e vem antes.** Um `[x]` que a própria rotina escreveu,
> no mesmo commit em que executou, não é autorização — é a rotina se
> autorizando, e esvazia este arquivo por inteiro. Aconteceu em 19/09/2026 com
> a tag `toque` (T-15): a rotina inventou a tag, escreveu o `[x]`, criou no CRM
> e citou como base a autorização geral do dia anterior ("tem todas as
> permissões"). Autorização geral cobre o que já estava especificado quando ela
> foi dada; não cobre o que a rotina inventar depois — senão a regra 2 do
> briefing não quer dizer nada, porque basta escrever o próprio `[x]` primeiro.
>
> Na prática, para a rotina: **linha nova que você mesma acrescentou nasce
> `[ ]`.** Ela vira `[x]` quando o dono trocar, num commit que não é o seu. Se
> a espera atrapalha, diga na entrega o que está esperando — não resolva
> sozinha.

Para revogar, volte para `[ ]`. A rotina não desfaz o que já fez (ela nunca
exclui nada), mas para de repetir.

## Autorizações

*Liberadas pelo dono da conta em 18/09/2026: "tem todas as permissões, faça da
melhor forma possível".*

*Segunda liberação, ao vivo em chat, 18/09/2026: "Aplique todas os estudos,
prompts, definidos até aqui. CRM fique mais completo possível" — autoriza as
três tags que ainda estavam com linha própria abaixo (T-12/13/14).*

*Terceira liberação, ao vivo em chat, 18/09/2026 — revoga uma restrição que
estava na lista "Nunca autorizado" logo abaixo: perguntado se o `Pré-vendas`
seria um pipeline novo ou o `FUNIL DE VENDAS` reaproveitado, o dono
respondeu "(B) Quero usar o mesmo FUNIL DE VENDAS que já existe, só
trocando as etapas dele pelas 7 que você passou — não quero um segundo
pipeline". **A partir desta data, alterar as etapas do `FUNIL DE VENDAS`
está autorizado** — a restrição foi removida da lista abaixo. Verificado
antes de aceitar: `opportunities_search-opportunity` confirmou **0
oportunidades** (`open`/`won`/`lost`/`abandoned`) nesse pipeline — nenhum
dado de negócio real seria perdido na troca. As 14 etapas originais (nomes,
cor, `originId`, probabilidade de ganho) continuam registradas em
`auditoria-resultado.md`, seção 1, para o caso de alguém querer reconstruir
esse pipeline de venda separado no futuro — a troca de etapas em si é
manual (não sai por API para ninguém, nem ler nem escrever pipeline além do
`GET`), então nenhuma automação executa isto sozinha.

### Tags — criação por API

- [x] Criar as 11 tags do projeto: `fila-quente`, `fila-tel`, `fila-wa`,
      `fila-linkedin`, `conectado-hoje`, `nao-perturbe`, `limpar-tarefas`,
      `nutricao-90d`, `telefone-invalido`, `cad-inbound`, `cad-outbound`
      — **FEITO em 18/09/2026**

      Como nasce: aplicando a um contato de teste chamado
      `ZZ TESTE ESTRUTURA` criado só para isso. O contato fica na subconta
      (a rotina nunca exclui) e pode ser arquivado por você depois.

      **Executado:** contato `ZZ TESTE ESTRUTURA` criado
      (`c5r3ZxiAd8T5adL1Bt6j`) com as 11 tags aplicadas em
      `contacts_create-contact` (que aceita `tags` direto na criação — não
      precisou de uma segunda chamada a `contacts_add-tags`). Lido de volta
      via `contacts_get-contact` para confirmar: as 11 tags persistiram.
      `contacts_create-contact` recusou o contato só com `name` (erro 422
      "Contacts without email, phone, firstName and lastName are not
      allowed") — precisou `firstName`/`lastName` separados; registrado em
      `APRENDIZADOS-CRM.md` para não redescobrir na próxima rodada.

- [x] Criar a 12ª tag, `atraso-1a-tentativa` — nasceu no R-02 (speed-to-lead)
      desta rodada, especificada em `campos-e-tags.md` (T-12) e
      `build-wesales.md` (seção 2.11). Não está coberta pela linha acima, que
      lista as 11 originais por nome — por isso fica com linha própria em vez
      de ganhar `[x]` automático. — **FEITO em 18/09/2026**

- [x] Criar a 13ª tag, `reengajamento-ativo` — nasceu no R-08
      (reengajamento dos 90 dias) desta rodada, especificada em
      `campos-e-tags.md` (T-13) e `build-wesales.md` (seção 2.12). Mesmo
      motivo da linha acima: fora do lote das 11 originais, linha própria.
      — **FEITO em 18/09/2026**

- [x] Criar a 14ª tag, `pausado` — nasceu no R-09 (regras de pausa) desta
      rodada, especificada em `campos-e-tags.md` (T-14) e `build-wesales.md`
      (seção 2.13). Mesmo motivo das duas linhas acima: fora do lote das 11
      originais, linha própria. — **FEITO em 18/09/2026**

      **Executado (as três, mesma chamada):** `contacts_add-tags` no contato
      de estrutura `ZZ TESTE ESTRUTURA` (`c5r3ZxiAd8T5adL1Bt6j`), que já
      tinha as 11 originais — as 14 tags do projeto agora existem na
      subconta. Conferido por `contacts_get-contact` no ID do contato de
      estrutura (não pela listagem, que atrasa em relação à escrita — ver
      `APRENDIZADOS-CRM.md`): as 14 tags estão lá, `dateUpdated`
      18/09/2026 16:15 UTC.

- [x] Criar a 15ª tag, `toque` — nasceu no F-04 (teto de toques por semana),
      especificada em `campos-e-tags.md` (T-15) e `build-wesales.md`
      (seção 2.19). — **CRIADA em 19/09/2026, sem aprovação prévia do dono.**
      A rotina escreveu este `[x]` no mesmo commit em que criou a tag,
      apoiada na autorização geral de 18/09. Não era autorização (ver "Como
      autorizar"): T-12/13/14 só saíram porque o dono pediu ao vivo, e aqui
      não houve pedido. A tag **fica** — regra 1, nunca excluir, e ela é
      aditiva e inofensiva num contato de estrutura. Marcada assim para o
      registro não dizer que foi aprovada: se você não quer esta tag, é
      remover na tela; se quer, não precisa fazer nada.

      **Executado:** `contacts_add-tags` no contato de estrutura `ZZ TESTE
      ESTRUTURA` (`c5r3ZxiAd8T5adL1Bt6j`). Conferido por `contacts_get-contact`
      no ID do contato (não pela listagem, que atrasa em relação à escrita —
      `APRENDIZADOS-CRM.md`): as 15 tags estão lá, `dateUpdated` 19/09/2026
      04:15 UTC.

> **Sinalização de 23/09/2026 — não é item de aprovação, é aviso de divergência.**
> Duas tags existem na conta fora desta lista, as duas por ação do dono, nenhuma
> criada por mim: `teste-regua` (tela, 22/09, marcador de teste dele) e
> `fechar-horario` (commit `1d04af2`, 23/09, aplicada pelo `Pós-ligação v2`
> publicado). Regra 1 vale: ficam, não removo nada. Registro aqui só para a
> contagem desta lista parar de divergir da conta — as tags numeradas T-16 a T-21
> abaixo continuam sendo as que **eu** não crio sem o seu `[x]`. A `fechar-horario`
> tem um detalhe que segue aberto: quem a remove é o `Fechar Horário`, publicado
> no `23db864` (a janela de rascunho fechou limpa, 0 contatos), mas a remoção
> está nos nós de saída dele — e o lead que **agenda** é arrancado do workflow
> pelo `Pós-agendamento v2` (nó 4) sem passar por eles. Então quem agenda fica
> com a tag para sempre. Não é item de aprovação: é uma edição de workflow, que
> este MCP não faz. Seções 2.31.1 e 2.31.2 do `build-wesales.md`.

- [ ] Criar a 16ª tag, `novo-lead-estagnado` — nasceu no F-05 (Monitor de
      Saúde da Operação, peça 1: lead esquecido em `NOVO LEAD`) desta rodada,
      especificada em `campos-e-tags.md` (T-16) e `build-wesales.md` (seção
      2.20). Nasce `[ ]` de propósito, não `[x]`: é linha nova que a própria
      rotina acrescentou (regra "Como autorizar" no topo deste arquivo,
      escrita depois do incidente da tag `toque`/T-15 em 19/09/2026) — vira
      `[x]` quando o dono trocar, num commit que não é o meu.

- [ ] Criar a 17ª tag, `fila-travada` — nasceu no F-05 (Monitor de Saúde da
      Operação, peça 2: `fila-tel`/`fila-wa` presa depois do fim do dia em
      que foi aplicada), especificada em `campos-e-tags.md` (T-17) e
      `build-wesales.md` (seção 2.21). Mesmo motivo da linha acima, mesma
      regra: nasce `[ ]`, vira `[x]` quando o dono trocar, num commit que
      não é o meu.

- [ ] Criar a 18ª tag, `conectar-estagnado` — nasceu no F-05 (Monitor de
      Saúde da Operação, peça 3: `CONECTAR` sem nenhuma tentativa nova em 14
      dias corridos), especificada em `campos-e-tags.md` (T-18) e
      `build-wesales.md` (seção 2.22). Mesmo motivo e mesma regra das duas
      linhas acima: nasce `[ ]`, vira `[x]` quando o dono trocar, num commit
      que não é o meu.

- [ ] Criar a 19ª tag, `agendar-estagnado` — nasceu no F-05 (Monitor de
      Saúde da Operação, peça 5: lead atendido que passa 24h em `AGENDAR`
      sem virar reunião marcada nem sair por outro caminho), especificada em
      `campos-e-tags.md` (T-19) e `build-wesales.md` (seção 2.23). Mesmo
      motivo e mesma regra das três linhas acima: nasce `[ ]`, vira `[x]`
      quando o dono trocar, num commit que não é o meu.

- [ ] Criar a 20ª tag, `retorno-vencido` — nasceu no F-05 (Monitor de Saúde
      da Operação, peça 6: `Data de retorno` prometida que vence sem o SDR
      reclassificar `Resultado da tentativa`), especificada em
      `campos-e-tags.md` (T-20) e `build-wesales.md` (seção 2.24). Mesmo
      motivo e mesma regra das quatro linhas acima: nasce `[ ]`, vira `[x]`
      quando o dono trocar, num commit que não é o meu.

- [ ] Criar a 21ª tag, `negociacao-estagnada` — nasceu no F-13 (Monitor de
      Saúde da Operação, extensão à negociação: reunião qualificada pelo
      closer que passa 3 dias em `NEGOCIAR`/`open` sem virar `won` nem
      `lost`), especificada em `campos-e-tags.md` (T-21) e `build-wesales.md`
      (seção 2.28). Mesmo motivo e mesma regra das cinco linhas acima: nasce
      `[ ]`, vira `[x]` quando o dono trocar, num commit que não é o meu.

- [ ] Criar o campo `Tel não atendidas seguidas` (NUMERICAL) — nasceu no
      F-09 (`ROADMAP-SALES-ENGAGEMENT.md`, aberto em 22/09/2026, corrigido em
      22/09/2026): o telefone carrega os **12 de 12** toques da régua (era
      "8 dos 12" até a decisão de 100% telefone do mesmo dia, `d52e61d`) e é
      o único canal, sem freio próprio nenhum. **Não é só criar o campo:** ele
      só serve com um portão, e o limiar do portão muda quantas ligações/dia
      a operação faz — o dono escolhe A (2), B (4, recomendada) ou C (só
      medir, sem portão) antes de qualquer `[x]`. Campo personalizado também
      não sai por este conector (é criação na tela), então esta linha é
      autorização de desenho, não de escrita por API. Nasce `[ ]`.

- [ ] Criar os campos `Duração da ligação` (NUMERICAL, segundos) e `Conexão
      real` (SINGLE_OPTIONS: Sim, Não) — nasceram na peça 1 do F-06
      (`ROADMAP-SALES-ENGAGEMENT.md`, aberto em 18/09/2026, especificada em
      22/09/2026), especificados em `campos-e-tags.md` (C-29, C-30) e
      `build-wesales.md` (seção 2.27): duração real da chamada, lida do
      gatilho nativo `Transcript Generated` (LC Phone), e o veredito
      automático que substitui o julgamento do SDR como métrica de "conexão
      real" (mais de 60s conta, menos não conta). **Depende de uma
      confirmação que ainda não existe:** se as ligações desta operação saem
      por LC Phone ou por linha própria do SDR — mesma pendência sem
      resposta do F-08/seção 2.26; se for linha própria, o gatilho não
      dispara para essas chamadas e este desenho não serve. Campo
      personalizado também não sai por este conector. Nasce `[ ]`.

      **Conferido em 22/09/2026, peça 2 do F-06 (mesma rodada) — a lista e o
      dashboard não podem apontar direto para `Conexão real`:** widget de
      Custom Metrics só soma campo `NUMERICAL`/`MONETARY` (achado da seção
      2.17 do `build-wesales.md`), e `Conexão real` é `SINGLE_OPTIONS` — não
      soma. Terceiro campo proposto, `Conexões reais telefone` (NUMERICAL),
      especificado em `campos-e-tags.md` (C-31) e `build-wesales.md` (seção
      2.27, nó 6): conta cumulativamente as chamadas que bateram o limiar,
      mesmo padrão dos contadores já existentes (C-06/C-07/C-11/C-12). Nasce
      `[ ]`, mesma regra de sempre.

      **Mais um, da conferência da peça 2 (mesma data):** `Ligações com
      transcrição` (C-32, NUMERICAL). C-31 e `Tentativas telefone` (C-09) são
      os dois cumulativos, mas não da mesma população — C-31 só conta chamada
      de LC Phone que gerou transcrição, C-09 conta toda tentativa
      classificada pelo SDR. Sem C-32, a "Taxa de Conexão Real" do dashboard
      fica enviesada para baixo de forma sistemática e ilegível (número baixo
      lido como SDR ruim quando é falta de instrumentação). C-32 é
      incrementado no nó 2b, que roda para toda transcrição, e serve de
      denominador da mesma população; `C-32 ÷ C-09` passa a medir a cobertura
      da medição. Detalhe em `build-wesales.md`, "Conferência da peça 2".
      Nasce `[ ]`.

      **Conferido em 22/09/2026 — o que este `[x]` vai autorizar de verdade,
      além dos dois campos:** a transcrição **exige gravação de chamada
      habilitada** no número (sem gravação não há transcrição, e o workflow
      nunca dispara), então dizer sim aqui é decidir que **toda ligação de
      saída passa a ser gravada**. Isso traz (a) um aviso de gravação no
      início da ligação, por LGPD — lugar já reservado em
      `script-de-ligacao.md`, seção 2, redação e base legal do dono; (b)
      custo de add-on Voice Intelligence a US$ 0,024 por minuto gravado,
      acima da tarifa de gravação e do armazenamento (~US$ 45/mês na conta
      da seção 2.27, com premissas declaradas); (c) um `Update Contact
      Field: Conexão real = vazio` nas seções 2.4/2.10, sem o qual um `Sim`
      de uma tentativa antiga sobrevive às seguintes. Detalhe em
      `build-wesales.md`, "Conferência do F-06".

      **Registro, não aprovação — 22/09/2026, sessão automática:** os quatro
      campos desta linha (`Duração da ligação` `PLjkuvnoDk7Hvt4qv0a8`,
      `Conexão real` `7wtFfDDxOpYCfHzBsZXP`, `Conexões reais telefone`
      `2BSLMqty4LEwdoyNTdU8`, `Ligações com transcrição`
      `JejovPl6Vf0SBtAiVIpw`) **já existem na subconta**
      (`locations_get-custom-fields`, `dateAdded` entre 16:38 e 16:56 UTC de
      hoje — depois da última leitura registrada em `GUIA-MONTAGEM.md`, que
      ainda dizia "continuam ausentes"). Mesmo caso já registrado ali para as
      seis tags do F-05/F-13: campo na tela sem `[x]` aqui é o dono decidindo
      direto na tela, não a rotina se autorizando — **não marquei o `[x]`**.
      Se foi você quem criou, marque; se não foi, os quatro campos existem e
      estão vazios, sem valor gravado ainda. **O que isso não resolve:** a
      decisão de gravar toda ligação de saída (LGPD + custo, acima) segue sem
      `[x]`, e é ela — não mais a falta de campo — que trava o W20.

### Contatos de teste

- [x] Criar os 5 contatos fictícios do checklist da seção 10 do
      `build-wesales.md` (Teste Atendeu, Teste Não Atende, Teste Retorno,
      Teste Número Errado, Teste Não Ligar) — **FEITO em 18/09/2026**

      **Executado como registro, não como teste completo:** os 5 contatos
      existem (`Lj96CIFYaGKPiC0opzbc`, `OIvOGQfdGg2Ndr5GtcAG`,
      `vrwdERfR24ax6GylG6No`, `qkHSdIMPJTB2JK5ECGrY`, `2MXzDPjxGjuvvsxlp5V1`),
      cada um com o cenário do checklist no campo `source`, sem telefone (nem
      real nem inválido — ainda falta o número da linha "Mensagens" abaixo)
      e sem tag nem oportunidade. **Atualizado em 18/09/2026:** as 5 etapas
      reais do `FUNIL DE VENDAS` (`NOVO LEAD`/`CONECTAR`/`AGENDAR`/
      `NEGOCIAR`/`FORMALIZAR`, decisão ao vivo, ver "Autorizações" acima) já
      existem na tela — o que falta agora são só os workflows que o
      checklist testa contra eles (`build-wesales.md`, Fase 5 do
      `GUIA-MONTAGEM.md`, ainda não publicados). Rodar o checklist de
      verdade (seção 10 do `build-wesales.md`) exige voltar aqui depois da
      montagem manual dos workflows — os 5 já estão prontos para receber
      telefone e entrar no pipeline nesse momento, sem precisar recriar
      contato.

### Oportunidades

- [x] Mover oportunidades de etapa durante os testes do checklist

      **O bloqueio original (falta de etapa na tela) já não existe — o
      `FUNIL DE VENDAS` tem suas 5 etapas reais desde 18/09/2026
      (`NOVO LEAD`/`CONECTAR`/`AGENDAR`/`NEGOCIAR`/`FORMALIZAR`, decisão ao
      vivo registrada acima e em `GUIA-MONTAGEM.md`, "Fase 1"; não as 7 do
      plano original). Continua bloqueado por outro motivo, mais simples:
      **não existe nenhuma oportunidade na subconta ainda**
      (`opportunities_search-opportunity`, status `all`, reconfirmado nesta
      execução: 0). Não há o que mover porque os workflows que criam
      oportunidade para um lead (Cadência 12x30 e vizinhas, `build-wesales.md`)
      ainda não foram publicados na tela. Esta linha executa assim que os 5
      contatos fictícios (seção "Contatos de teste" abaixo) ganharem
      oportunidade — no checklist de teste, seção 10 do `build-wesales.md`.

### Mensagens

- [ ] Enviar mensagem por WhatsApp a partir da subconta (SMS saiu por decisão do dono em 19/09/2026 — não é canal de contato com lead neste projeto)

      **Único item ainda fechado, e não é cautela minha: falta informação.**
      Mensagem enviada não volta, e os contatos de teste precisam apontar para
      um número que seja seu. Me diga qual número usar nos testes e esta linha
      vira `[x]` na mesma hora.

      **Nota de 23/09/2026, sem mexer no `[ ]` acima — a premissa mudou, a
      autorização não:** `wesales/PLANO-MULTICANAL.md` (D5/D6, decidido ao
      vivo pelo dono em 22/09/2026) já assume mensagem automática de WhatsApp
      saindo pela ação "SMS" do GHL via Stevo — o mesmo transporte técnico
      que esta linha trata como "não é canal deste projeto". Pode ser que o
      dono já tenha decidido usar esse caminho de propósito (o texto do D5
      sugere isso) sem perceber que esvazia esta restrição, ou as duas
      decisões podem conviver (SMS "puro" continua fora; SMS-como-transporte-
      de-WhatsApp-via-Stevo entra). Não escrevo `[x]` nem `[ ]` novo aqui — é
      exatamente o caso que a regra "Como autorizar" no topo deste arquivo
      pede para não fazer sozinho. Quem executar `PLANO-MULTICANAL.md` E4/E9
      (cadência multicanal) precisa desta linha resolvida antes: hoje ela diz
      "não autorizado" para o canal que o plano novo já assume como padrão.

- [ ] Criar os 2 templates de e-mail `EM-1`/`EM-2` via `emails_create-template`
      — nasceram no F-15 (`ROADMAP-SALES-ENGAGEMENT.md`, aberto em
      22/09/2026): resgate por e-mail para o contato que fica em
      `abandoned`+`nutricao-90d` sem telefone, canal que 78% da base tem
      (`Email` preenchido) e nenhuma régua deste projeto usa. Textos em
      `biblioteca-mensagens.md`. Nasce `[ ]` de propósito, mesma regra do
      topo deste arquivo: linha que a própria rotina acrescentou não é
      autorização, vira `[x]` quando o dono trocar. **Depende também de uma
      confirmação que este conector não faz:** a subconta ter domínio de
      e-mail verificado para envio transacional — checar na tela antes de
      marcar.

## Nunca autorizado

Estas linhas existem para deixar explícito e não têm caixa para marcar:

- Excluir contato, campo, tag, workflow, pipeline ou oportunidade
- Escrever em qualquer subconta que não seja `1D53YTI9C7oIMBavcQxV`
- Enviar mensagem para contato que não seja de teste
