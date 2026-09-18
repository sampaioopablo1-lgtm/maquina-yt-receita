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

### Tags — criação por API

- [ ] Criar as 11 tags do projeto: `fila-quente`, `fila-tel`, `fila-wa`,
      `fila-linkedin`, `conectado-hoje`, `nao-perturbe`, `limpar-tarefas`,
      `nutricao-90d`, `telefone-invalido`, `cad-inbound`, `cad-outbound`

      Como nasce: aplicando a um contato de teste chamado
      `ZZ TESTE ESTRUTURA` criado só para isso. O contato fica na subconta
      (a rotina nunca exclui) e pode ser arquivado por você depois.

### Contatos de teste

- [ ] Criar os 5 contatos fictícios do checklist da seção 10 do
      `build-wesales.md` (Teste Atendeu, Teste Não Atende, Teste Retorno,
      Teste Número Errado, Teste Não Ligar)

### Oportunidades

- [ ] Mover oportunidades de etapa durante os testes do checklist

### Mensagens

- [ ] Enviar mensagem por WhatsApp/SMS a partir da subconta

      **Pense duas vezes.** Mensagem enviada não volta. Só libere quando os
      5 contatos de teste existirem e apontarem para números seus.

## Nunca autorizado

Estas linhas existem para deixar explícito e não têm caixa para marcar:

- Excluir contato, campo, tag, workflow, pipeline ou oportunidade
- Alterar o pipeline `FUNIL DE VENDAS` existente
- Escrever em qualquer subconta que não seja `1D53YTI9C7oIMBavcQxV`
- Enviar mensagem para contato que não seja de teste
