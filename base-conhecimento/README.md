# Base de conhecimento — máquina de prospecção

*Criada em 14/09/2026. Serve para qualquer chat futuro construir a máquina sem recomeçar do zero.*

**Leia este índice antes de usar os arquivos.** Eles contêm uma armadilha que só aparece com contexto.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `uazapi — llms.txt` | Documentação completa da uazapi para LLMs: endpoints de instância, envio, mídia, grupos, contatos, campanhas, webhooks, chatbot. Enviada pelo Pablo. |
| `ARQUITETURA — maquina de prospeccao.md` | O desenho base: três portas de entrada, um núcleo de conversa, a IA só depois do primeiro "oi". |
| `ARQUITETURA — modo lista, 100% automatico.md` | Variante em que o Pablo só sobe o CSV: faixa grátis por e-mail + faixa paga por modelo aprovado (R$ 0,30), com auto-stop. |
| `PROMPT — agente WhatsApp (uazapi + Flask + Gemini).md` | Prompt pronto para construir o MVP: Flask + Gemini 2.5 Flash, buffer com debounce, resposta dividida em várias mensagens, "digitando" entre elas. Enviado pelo Pablo. |
| `../entregas/campanha/PESQUISA — maquina de prospeccao por WhatsApp.md` | A pesquisa que dá o contexto: o que é legal, o que é banível, e quanto custa cada caminho. |

## A armadilha, em três frases

**A uazapi é API NÃO OFICIAL.** Ela conecta por QR Code, imitando o WhatsApp Web — mesma família do Baileys e do WPPConnect.

**Desde janeiro de 2026 a Meta derruba esse tipo de conexão em até 48 horas**, mesmo com volume baixo, porque a detecção passou a ser **pelo método de conexão**, não pelo volume. Estimativas do setor: 40% a 60% das contas em API não oficial suspensas só no primeiro trimestre de 2026. O banimento é definitivo.

**Portanto: aquecer chip e limitar envio não protege nada nessa arquitetura.** Quem sugerir "10 contas × 10 mensagens por dia" está resolvendo o problema de 2025.

## Onde estes arquivos servem, e onde não servem

**Servem** — o código do agente em si é bom e reaproveitável:
- a lógica de buffer com debounce, memória por usuário, resposta fatiada e presença "digitando" **não depende da uazapi**; troca-se `uazapi.py` por um cliente da Cloud API oficial e o resto fica igual;
- para automação em número próprio com consentimento, em cenário de baixo risco e onde perder o número seja aceitável;
- como referência de payload de webhook e de estrutura de agente.

**Não servem** — não construir sobre isto:
- prospecção fria em massa, com múltiplos chips, para base sem opt-in. Além do banimento, viola a política da Meta (marketing iniciado pela empresa exige opt-in) e expõe na LGPD (ANPD autuando, multa até R$ 50 milhões).

## O caminho que a pesquisa recomenda

**Click-to-WhatsApp → janela de entrada gratuita.** Quando a pessoa chega por um anúncio Click-to-WhatsApp ou pelo botão da Página, abre-se uma janela de **72 horas em que todas as mensagens são gratuitas, inclusive templates**. Essa janela **sobreviveu à mudança de preço de 1º de outubro de 2026**.

Custo de WhatsApp: **R$ 0,00**. Paga-se só o anúncio, que o Pablo já paga. E é o caminho oficial, sem risco de banimento.

Pilha mais barata: **Cloud API direto com a Meta** (sem BSP, sem marcação) + Evolution API em **modo Cloud API oficial** ou n8n auto-hospedado + IA + Google Agenda. Custo mensal realista: servidor (R$ 30 a 50) + tokens de IA.

**O ativo pronto que já existe:** a campanha `WPP I CONVERSA I FS1` (id 120247368224510766) é exatamente um Click-to-WhatsApp. Está **pausada** desde 12/09 — foi o Pablo que pausou, junto com os outros conjuntos. É o veículo certo para religar quando o agente estiver de pé.

## Como usar isto num chat novo

1. Ler este README.
2. Ler a `PESQUISA` para o contexto de custo e legalidade.
3. Se for construir o agente: usar o `PROMPT`, **trocando a camada de envio** pela Cloud API oficial se o destino for prospecção; manter uazapi só se for caso interno e de baixo risco.
4. Consultar `uazapi — llms.txt` para qualquer campo ou endpoint — e não inventar endpoint que não esteja lá.
