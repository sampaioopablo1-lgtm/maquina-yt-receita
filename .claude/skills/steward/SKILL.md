---
name: steward
description: Regras deste repositório para cuidar de um PR — qual é o branch base, quais falhas de CI são pré-existentes, e quando NÃO abrir PR. Leia antes de agir sobre evento de CI ou de review.
---

# Cuidar de PR neste repositório

Três coisas aqui quebram o roteiro padrão. Todas foram aprendidas errando.

## 1. O branch padrão não é `main`

```
claude/youtube-publication-next-steps-v7o4el
```

E ele **não é ancestral** dos branches `claude/*` de trabalho — são linhas paralelas. Em 27/09/2026 abri um PR de um branch de trabalho contra ele e saiu com **317 arquivos, 373 commits, 434.785 adições e conflito**. Mergear aquilo levaria 373 commits de outra frente para o branch padrão.

**Antes de abrir PR, meça:**

```bash
git rev-list --left-right --count origin/<base>...HEAD
```

Se o lado direito passar de ~20 commits, o PR está errado: ou a base está errada, ou o que se quer levar cabe num branch pequeno criado **a partir da base**, contendo só os arquivos necessários.

## 2. `workflow_dispatch` não aparece fora do branch padrão

O botão "Run workflow" só existe para workflow presente no branch padrão. Num branch de trabalho, use `on: push` restrito ao branch e aos `paths` que interessam — a rodada acontece a partir dali, sem merge nenhum. Foi assim que o `jev.yml` passou a rodar.

## 2b. `schedule` também só roda no branch padrão

Medido em 27/09/2026, depois de eu entregar dois workflows com cron que nunca
iriam disparar: **`schedule` e `workflow_dispatch` só funcionam no branch padrão.**
Num branch de trabalho, o único gatilho que funciona é `push`.

Se a automação precisa de horário, ela precisa estar no branch padrão — ou o
desenho precisa não depender de cron. Exemplo do segundo caminho: em vez de um
cron que reabre a janela da cadência na terça, deixar a janela como `days: [2]`,
que abre na terça sozinha.

## 3. As 12 falhas de `tests/test_narracao_das_specs.py` são pré-existentes

Linha de base estável desde 18/09/2026:

```
12 failed, 1950 passed, 32 skipped
```

Já há comentário de stand-down no PR de 18/09. **Não comente de novo, não conserte, não desabilite.** Se o número for exatamente esse e os IDs forem os mesmos, não é do seu PR.

`pyproject.toml` limita `testpaths` a `tests/`, e nenhum teste referencia `wesales/` — commit que só toca `wesales/` não pode mudar a suíte. Confirme com `grep -rl wesales tests/` antes de investigar.

## 4. Falha de job não é sinal confiável por si

`comando | tee arquivo` devolve o código de saída do **`tee`**. Em 27/09/2026 um job ficou verde escondendo um 403 do Jev. **Todo `run:` com pipe leva `set -o pipefail`.** E leia o corpo da resposta antes de concluir a causa: no mesmo dia um 403 do Cloudflare (erro 1010, assinatura do cliente) foi diagnosticado por mim como token inválido, sem base.

## Ordem de trabalho

1. conflito de merge → resolver com merge da base, nunca rebase em branch de outro;
2. CI vermelho → ler o **corpo** do erro, não só o código;
3. comentários de review.

Nunca: pular teste, force-push em branch alheio, commit vazio para provocar CI.
