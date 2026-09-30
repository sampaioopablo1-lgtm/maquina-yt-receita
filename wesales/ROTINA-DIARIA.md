# Rotina diária — prompt para rodar sob demanda (1x por dia)

A construção contínua do CRM deixa de ser horária: o prompt abaixo roda **uma
vez por dia**, ou quando o dono acionar numa sessão local.

**Como acionar numa sessão local:** abra o Claude Code na raiz do repositório,
na branch `claude/amazing-johnson-mclksg`, e peça: *"rode a rotina de
`wesales/ROTINA-DIARIA.md`"*. O conector `GHL CRM` precisa estar ligado na
sessão; sem ele, a rotina segue só com o item de backlog que não depender do CRM.

Contexto do que a rotina faz e do freio de mão: `rotina-horaria.md` e
`APROVADO.md`.

## Prompt

Você está construindo, dia a dia, uma operação de pré-vendas que não é só boa —
é fora da curva. Dentro da WeSales (white-label do GoHighLevel), usando só
recursos nativos. Execução autônoma. Faça UMA coisa bem feita e pare.

Repositório: sampaioopablo1-lgtm/maquina-yt-receita · branch `claude/amazing-johnson-mclksg`
Subconta: `1D53YTI9C7oIMBavcQxV` (Pablo Santos's Account) · conector `GHL CRM`

### O alvo
O motor já está desenhado: cadência de 12 tentativas em 30 dias, 3 canais,
filas por tag, régua de qualificação, roteamento por resultado, saída limpa.

Paridade com Reev e Meetime é o **piso**, não a chegada. O que ganha está no
bloco 6 do roadmap: cadência que reage a sinal, horário aprendido por segmento,
loop do closer calibrando a régua, teto de fadiga, monitor de saúde, qualidade
de conexão em vez de contagem.

Entre duas formas de resolver, escolha a que um concorrente não consegue copiar
olhando a tela de fora.

### Leia primeiro, nesta ordem
1. `wesales/APROVADO.md` — o que você pode escrever no CRM. É a única porta.
2. `wesales/ROADMAP-SALES-ENGAGEMENT.md` — **o backlog. É daqui que sai o trabalho.**
3. `wesales/briefing-sdr.md` — regras invioláveis, decisões, lacunas
4. `wesales/auditoria-resultado.md` — estado real da subconta
5. `wesales/APRENDIZADOS-CRM.md` — o que execuções anteriores descobriram
6. `wesales/build-wesales.md`, `wesales/campos-e-tags.md`, `wesales/rotina-limpar-tarefas.md`

Se as ferramentas do conector `GHL CRM` não estiverem na sessão, não conclua que
o acesso não existe: registre em `APRENDIZADOS-CRM.md` e siga com o item de
backlog que não depender do CRM.

### O que fazer
Pegue **o item de maior prioridade ainda aberto** do roadmap e leve-o até o
"Pronto quando" dele:

- **Especificar** nó a nó, no padrão do `build-wesales.md`: gatilho, condições,
  ações, com nomes reais de campo e de ferramenta.
- **Criar no CRM** o que estiver `[x]` no `APROVADO.md`, e verificar lendo de
  volta depois de escrever.
- **Listar os campos novos** em `campos-e-tags.md`, com tipo e opções — criar
  campo personalizado não sai por API.
- **Marcar o item como concluído** no roadmap, com data e resumo de uma linha.

Item grande demais? Quebre no próprio roadmap e faça o primeiro pedaço.
Antes de desenhar, pesquise como Reev, Meetime, Outreach e Salesloft resolvem
aquilo — e faça melhor ou mais barato, não igual. Lacuna que ninguém listou:
acrescente ao roadmap (por quê / como / pronto quando).

### Coerência entre documentos — parte da entrega
Antes de commitar, `grep -rn` pelo número antigo e pelos nomes tocados em todo
o `wesales/`. **Número fixo só na fonte:** `campos-e-tags.md` conta os campos;
`build-wesales.md` conta as tentativas. Nos outros arquivos, "os campos", sem
número. Documento contraditório vale menos que incompleto.

### Regras invioláveis
1. NUNCA exclua contato, campo, tag, workflow, pipeline ou oportunidade.
2. NUNCA escreva no CRM o que não estiver `[x]` em `APROVADO.md`.
3. NUNCA toque em subconta que não seja `1D53YTI9C7oIMBavcQxV`.
4. NUNCA altere o pipeline `FUNIL DE VENDAS` existente.
5. Só mexa em `wesales/` (o repositório também abriga a máquina de vídeo e a Jazz Imobiliária).
6. Não encoste nas 12 falhas de `tests/test_narracao_das_specs.py` — pré-existentes, de outro projeto.
7. Nunca force-push, nunca commit vazio, nunca desative teste.

### Quando der erro
Leia a mensagem inteira. Pesquise (issues, docs do HighLevel e do MCP,
comunidades). Só registre bloqueio depois de três abordagens genuinamente
diferentes. Grave o aprendizado em `wesales/APRENDIZADOS-CRM.md`.

### Entrega
Commit no branch `claude/amazing-johnson-mclksg`, mensagem explicando **por
que**, não o quê, no estilo do histórico do `wesales/`. Push.
**Nada de valor? Não commite e encerre em silêncio.**
Responda em português do Brasil.
