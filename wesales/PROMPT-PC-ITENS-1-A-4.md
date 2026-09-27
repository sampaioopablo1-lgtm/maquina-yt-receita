# Prompt para a sessão do PC — itens 1 a 4 de `FUNCOES-NAO-USADAS.md`

Colar inteiro no `claude` aberto em `C:\Users\Pablo\maquina-yt-receita` (PowerShell, sem admin).

---

Você vai terminar quatro ajustes na subconta WeSales/GHL 1D53YTI9C7oIMBavcQxV antes da operação começar. O item 1 tem prazo: a Cadência Inbound dispara o MI-0 na segunda 28/09 às 08:30. A SDR (Andreyna Siqueira) começa na terça 29/09. Trabalhe no branch `claude/abertura-operacao-dnd-n7dnjv`; faça `git pull` antes de começar.

Leia primeiro, nesta ordem, e não refaça o que já está feito: `wesales/FUNCOES-NAO-USADAS.md` (os achados), `wesales/DE-PARA-SESSOES-CRM.md` (o que já foi gravado no CRM, com versões), `wesales/COPY-WHATSAPP.md` (os textos e os ids dos nós), `wesales/tools/wa_governador.py` e `.github/workflows/wesales-wa-governador.yml` (o governador do WhatsApp e o contrato dele com os workflows). Quando o documento e o CRM divergirem, vale o CRM: releia o CRM antes de cada escrita.

Regras que não mudam: nunca apagar contato, oportunidade, workflow, nó, tag ou campo (descartar = status perdido); nunca ligar recurso de IA do GHL (Conversation AI, Voice AI, base de conhecimento, "Ativar Voice AI"), que é cobrado por uso; não criar nem renomear campo personalizado; não mexer no formulário "Qualificação SDR". Criar tag nova pode. Antes de cada gravação em workflow: backup em `.local/`, ensaio, gravação preservando `status`, releitura nó a nó. Se algo sair do previsto, pare e me pergunte, não improvise.

**Item 1 — limite de 15 WhatsApp automáticos por dia (primeiro, prazo seg 08:30).**
Regra do dono: WhatsApp automático nunca sai em lote; no máximo cerca de 15 por dia, espalhados no horário comercial, com a quantidade variando; o excedente fica manual com a SDR. O script `wa_governador.py` já faz a liberação; falta (A) a trava nos workflows e (B) o agendamento rodar.

(A) Trava. Vale para os 17 envios de prospecção da tabela do `COPY-WHATSAPP.md`: MI-0 e MIF (Cadência Inbound), MT1 e MT4 (Cadência 12x30), MT8, MT11 e MT12 (12x30 parte 2), MFH1 e MFH2 (Fechar Horário), N1 a N6 (Nutrição), NS-1 (Recuperação de No-show) e CANC-1 (Reunião Cancelada). Ficam de fora, de propósito: TRI-1 e as respostas 1 e 2 da Triagem (são resposta imediata a quem escreveu), todo o Lembretes da Reunião v3 (logística de reunião marcada) e a confirmação de opt-out. Antes de cada um dos 17 envios, monte esta sequência:
1. Espera até a janela seg–sex 08:30–14:30 (para a trava sempre começar em horário comercial e o prazo de 4 h terminar até 18:30);
2. Adicionar tag `wa-aguardando`;
3. Esperar condição "tag contém `wa-liberado`", com tempo limite de 4 h;
4. Condição atendida: envio de WhatsApp existente (o mesmo nó, sem mudar o texto) → remover tag `wa-liberado` → segue o fluxo original;
5. Tempo esgotado: remover tag `wa-aguardando` → criar tarefa para o dono do contato, vencendo agora, título `[WHATSAPP MANUAL] <código> — {{contact.first_name}}`, descrição com o texto da mensagem e o nome do snippet do item 2 → segue para o mesmo próximo nó do caminho de envio.
Adicionar nós é mudança de estrutura: faça pelo construtor na tela (Claude in Chrome), ou pela API interna só se copiar a forma exata de um nó de espera por condição que já exista na conta, e releia. Comece por um workflow de pouco volume (Reunião Cancelada), teste com o contato de teste que `tools/simular_reuniao.py` usa, confira que ele para em `wa-aguardando`, rode `python wesales/tools/wa_governador.py` (ensaio) e veja o contato na fila; depois faça a Cadência Inbound, depois o resto. Antes de mexer na Inbound, conte quantos contatos estão parados no passo anterior ao MI-0: é quantos sairiam segunda de uma vez.

(B) Agendamento. O GitHub só roda `schedule` no branch padrão (`claude/youtube-publication-next-steps-v7o4el`), e lá não existem `wesales/tools/wa_governador.py`, `wesales/tools/campos_bant.py` nem o `.github/workflows/wesales-wa-governador.yml`. Crie um branch novo a partir do branch padrão, copie só esses três arquivos do branch de trabalho, abra um PR pequeno para o padrão e me passe o link para eu fazer o merge. Não faça merge nem push direto no padrão. O segredo `GHL_PIT` já existe no repositório (as outras Actions usam). Depois do merge, rode a Action à mão com `aplicar = false` e me mostre a saída. Enquanto o agendamento não roda, o comportamento seguro já está garantido: ninguém é liberado, e depois de 4 h todos viram tarefa manual; nada sai em lote.

Se no domingo à noite a trava da Inbound não estiver gravada e relida, pare e me avise com o número de contatos que o MI-0 atingiria. Não pause nem despublique nenhum workflow sem a minha ordem.

**Item 2 — snippets para o WhatsApp manual.**
A conta tem 0 snippets de SMS, WhatsApp e e-mail (confirme na tela). Crie 17 snippets de texto, um para cada envio do item 1, com o texto exato do `COPY-WHATSAPP.md`, numa pasta "WhatsApp manual — prospecção", com nomes que a SDR ache digitando `/`: `WA MI-0 abertura inbound`, `WA MIF`, `WA MT1`… (código primeiro). Use só `{{contact.first_name}}`. O canal de WhatsApp da conta entra como SMS personalizado, então o snippet é de texto (SMS), não template oficial do Meta. Abra uma conversa do contato de teste, digite `/WA MI-0`, confira que o nome é preenchido e não envie.

**Item 3 — chamada de retorno no número do discador.**
O número +55 11 5026-6034 ("Agência Próximo Cliente") aparece na API só com voz, sem encaminhamento e sem serviço de chamada recebida. Primeiro leia na tela (Configurações → Números de telefone → editar o número, e o Call Center, se houver regra de entrada): se já houver destino para chamada recebida, anote e não mexa. Se não houver, me pergunte o celular da Andreyna e o horário dela, e configure: tocar para a Andreyna no horário comercial, encaminhar para o celular dela se ninguém atender em 20 s, e caixa postal fora do horário com gravação ou texto que eu aprovar. Não ligar "missed call text-back" (o número não envia SMS) nem nada de IA. No fim me peça para ligar de um celular pessoal para testar.

**Item 4 — calendário "Reunião com closer" (id 3uNQFjCEDe7b4gKZJuOZ).**
Faça pela API pública (`GET` e depois `PUT /calendars/3uNQFjCEDe7b4gKZJuOZ`, reenviando só os campos alterados, e releia):
- `consentLabel` em português: "Concordo em receber contato da O Próximo Cliente pelos dados que informei.";
- antecedência mínima de 2 horas (hoje `allowBookingAfter = 0`; confira no GET o nome do campo de unidade antes de gravar);
- aviso nativo de reunião marcada, remarcada e cancelada **só para o usuário atribuído** (o closer). O aviso ao contato continua desligado, porque o Lembretes da Reunião v3 já faz isso; ligar os dois duplica mensagem.
Não mexa em duração, intervalo, equipe, round robin, `widgetSlug` nem no título do evento. Confira na página pública de agendamento que o texto aparece em português e que o primeiro horário livre fica pelo menos 2 h à frente.

**Registro e relatório.**
Ao terminar cada item, acrescente uma linha em `wesales/DE-PARA-SESSOES-CRM.md`, numa seção nova "Itens 1–4 (28/09)": o que foi gravado, workflow ou registro, versão antes → depois, relido sim/não e observação. Commit e push no branch de trabalho. No fim, me responda em no máximo 15 linhas: o que ficou pronto, o que ficou pendente e por quê, o link do PR do item 1B e o que eu preciso fazer (merge, número da Andreyna, teste de ligação).
