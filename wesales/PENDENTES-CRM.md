# Pendentes para o CRM

Fila única de mudanças no CRM (WeSales / HighLevel, subconta
`1D53YTI9C7oIMBavcQxV`). A sessão na nuvem documenta; a máquina local aplica.

## Como aplicar (máquina local)

1. `git pull` no branch `claude/magical-brown-ovi1hp`.
2. Aplique os itens com `[ ]`, de cima para baixo.
3. Depois de aplicar e conferir, marque `[x]` e preencha "Feito em" com
   data e o que foi conferido.
4. Item que não der para aplicar: deixe `[ ]` e escreva o motivo em "Bloqueio".
5. Commit "CRM: pendentes aplicados DD/MM" e push.

Itens marcados **manual** só se fazem pela tela do CRM, porque a API não
tem a função.

## Pendentes

### [ ] 1. Visão "Ligar pelo WhatsApp" em Conversas (manual)
- **Por quê:** a SDR faz as ligações pelo WhatsApp numa lista só, dentro de
  Conversas, onde fica o botão de ligar (Stevo).
- **Como:** Conversas → Filtro → Tags inclui `fila-wa` → salvar como
  "Ligar pelo WhatsApp" → compartilhar com as SDRs.
- **Detalhe:** `wesales/VISAO-LIGAR-WHATSAPP.md` e Passo 3 do playbook.
- Feito em:
- Bloqueio: **manual do dono (admin)**, 28/09. A API não cria visão de Conversas; pela tela
  automatizada o painel Filtros abre (Tipo de filtro tem `Tag`), mas salvar/compartilhar a visão
  é do admin na tela. Passo a passo no playbook (Passo 3). A tag já é mantida (item 2).

### [x] 2. Conferir que a cadência publicada aplica `fila-wa`
- **Por quê:** sem isso a visão do item 1 fica vazia.
- **Como:** abrir a Cadência 12x30 publicada (e Inbound e Reengajamento) e
  confirmar que as tentativas de ligação por WhatsApp (T2, T4, T5, T7, T9,
  T12 na 12x30) aplicam `fila-wa`, como em `build-wesales.md` §2.4. Se não
  aplicarem, ajustar.
- **Conferência:** um lead de teste recebe `fila-wa` na tentativa e aparece
  na visão.
- Feito em: 28/09 (máquina local). **Conferido: nenhum workflow publicado põe `fila-wa`**
  (12x30, 12x30 p2, Inbound, Pós-ligação v3, Mestre de saída v2 e Opt-out só tiram). Em vez de
  editar as 3 cadências (dezenas de nós), o atuador das filas (PR #116, a cada 30 min) põe
  `fila-wa` em: CONECTAR, com telefone, 1+ tentativa por telefone sem conexão, sem
  `falou-hoje`/`wa-feito-hoje`/`nao-perturbe`. Workflow novo "WhatsApp tentado hoje"
  (`1c247efc-7f6f-4028-b328-6ab51103c3da`): Canal = WhatsApp → `wa-feito-hoje` 12 h e tira
  `fila-wa` → 1 ligação de WhatsApp por lead por dia. Hoje 0 elegíveis (contadores começam
  com as ligações de hoje).
- Bloqueio:

### [x] 3. Conferir que o Pós-ligação remove `fila-wa`
- **Por quê:** sem isso o lead fica preso na visão.
- **Como:** no Pós-ligação publicado, confirmar a remoção de `fila-tel` e
  `fila-wa` depois de ler o canal (`build-wesales.md`, nós 3b/5 da seção 4).
- **Conferência:** registrar Canal = WhatsApp e um Resultado no lead de
  teste; a tag sai e o lead some da visão.
- Feito em: 28/09 (máquina local). Pós-ligação v3 publicado tira `fila-wa` em 6 nós; e agora o
  "WhatsApp tentado hoje" também tira na hora em que o Canal = WhatsApp é marcado.
- Bloqueio:

## Aplicados

(os itens vêm para cá depois de marcados)
