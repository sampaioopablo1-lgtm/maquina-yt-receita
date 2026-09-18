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

Para revogar, volte para `[ ]`. A rotina não desfaz o que já fez (ela nunca
exclui nada), mas para de repetir.

## Autorizações

*Liberadas pelo dono da conta em 18/09/2026: "tem todas as permissões, faça da
melhor forma possível".*

*Segunda liberação, ao vivo em chat, 18/09/2026: "Aplique todas os estudos,
prompts, definidos até aqui. CRM fique mais completo possível" — autoriza as
três tags que ainda estavam com linha própria abaixo (T-12/13/14).*

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

### Contatos de teste

- [x] Criar os 5 contatos fictícios do checklist da seção 10 do
      `build-wesales.md` (Teste Atendeu, Teste Não Atende, Teste Retorno,
      Teste Número Errado, Teste Não Ligar) — **FEITO em 18/09/2026**

      **Executado como registro, não como teste completo:** os 5 contatos
      existem (`Lj96CIFYaGKPiC0opzbc`, `OIvOGQfdGg2Ndr5GtcAG`,
      `vrwdERfR24ax6GylG6No`, `qkHSdIMPJTB2JK5ECGrY`, `2MXzDPjxGjuvvsxlp5V1`),
      cada um com o cenário do checklist no campo `source`, sem telefone (nem
      real nem inválido — ainda falta o número da linha "Mensagens" abaixo)
      e sem tag nem oportunidade: o pipeline `Pré-vendas` e os workflows que
      o checklist testa contra eles não existem ainda na tela (só saem
      manual). Rodar o checklist de verdade (seção 10 do `build-wesales.md`)
      exige voltar aqui depois da montagem manual — os 5 já estão prontos
      para receber telefone e entrar no pipeline nesse momento, sem precisar
      recriar contato.

### Oportunidades

- [x] Mover oportunidades de etapa durante os testes do checklist

      **Continua bloqueado — não é falta de permissão, é falta de pipeline:**
      sem o `Pré-vendas` criado na tela (não sai por API), não existe etapa
      para mover oportunidade nenhuma. Esta linha executa assim que o
      pipeline existir.

### Mensagens

- [ ] Enviar mensagem por WhatsApp/SMS a partir da subconta

      **Único item ainda fechado, e não é cautela minha: falta informação.**
      Mensagem enviada não volta, e os contatos de teste precisam apontar para
      um número que seja seu. Me diga qual número usar nos testes e esta linha
      vira `[x]` na mesma hora.

## Nunca autorizado

Estas linhas existem para deixar explícito e não têm caixa para marcar:

- Excluir contato, campo, tag, workflow, pipeline ou oportunidade
- Alterar o pipeline `FUNIL DE VENDAS` existente
- Escrever em qualquer subconta que não seja `1D53YTI9C7oIMBavcQxV`
- Enviar mensagem para contato que não seja de teste
