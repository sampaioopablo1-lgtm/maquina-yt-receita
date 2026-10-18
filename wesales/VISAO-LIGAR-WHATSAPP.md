# Visão "Ligar pelo WhatsApp" em Conversas

Objetivo: a SDR faz a rodada de ligações pelo WhatsApp numa lista só, dentro de
Conversas, onde fica o botão de ligar (integração Stevo).

## O que já existe

- Tag `fila-wa` na conta: a cadência aplica nas tentativas de ligação por
  WhatsApp e o Pós-ligação remove quando a SDR registra o Resultado.
- Filtro por tag e visões salvas em Conversas: recurso nativo do CRM.

## O que fazer (uma vez, usuário admin, pela tela do CRM)

1. Conversas → ícone de Filtro.
2. Regra: Tags inclui `fila-wa`.
3. Salvar como visão "Ligar pelo WhatsApp".
4. Compartilhar a visão com as SDRs.

A API do CRM não cria visões; este passo é manual.

## Conferir depois

- A cadência publicada aplica `fila-wa` nas tentativas de ligação por WhatsApp
  (se não aplicar, a visão fica vazia).
- O Pós-ligação remove `fila-wa` ao registrar o Resultado (se não remover, o
  lead fica preso na lista).

## Uso pela SDR

Conversas → visão "Ligar pelo WhatsApp" → abrir a conversa → botão de ligar →
marcar Canal = WhatsApp e o Resultado → próxima. Detalhe no Passo 3 do playbook:
https://claude.ai/code/artifact/8454238e-c51c-4bbc-90ff-cc407f4b6458
