# Rotina horária — construção contínua do CRM

Roda de hora em hora, em sessão nova, e continua a construção da operação de
SDR junto com o dono da conta.

## O que ela faz a cada execução

Escolhe **o item de maior valor**, não faz tudo:

| | Frente | O que envolve |
|---|---|---|
| A | **Verificar o CRM** | Auditoria de leitura, comparada com `auditoria-resultado.md`. Pipeline novo, campo novo, contato entrando, tag aplicada — tudo vira atualização do documento |
| B | **Executar o aprovado** | O que estiver com `[x]` em `APROVADO.md` e ainda não foi feito |
| C | **Melhorar a especificação** | Revisar `build-wesales.md` contra o que se sabe do CRM real, corrigindo nó, gatilho, nome de campo ou regra que não bate |
| D | **Fechar lacunas** | As lacunas L-01 a L-06 do briefing e os quatro itens que a auditoria não fechou: tags, workflows, calendários, formulários |

## O freio de mão

`APROVADO.md` é a única porta de escrita no CRM. Com ele vazio, a rotina lê o
CRM e trabalha na documentação — e mais nada. Foi feito assim de propósito:
uma rotina autônoma que cria coisa em CRM de produção sem autorização escrita é
como deixar a porta destrancada porque ninguém costuma passar ali.

## Quando dá erro

A rotina não desiste na primeira. A ordem é: ler a mensagem inteira, pesquisar
na internet — issues do GitHub, blogs, fóruns, documentação oficial do HighLevel
e do MCP —, testar a hipótese e corrigir. Só registra como bloqueio depois de
**três abordagens diferentes**.

O que aprender vai para `APRENDIZADOS-CRM.md`, para a execução seguinte não
refazer a mesma investigação. É o que evita a rotina descobrir a mesma coisa
vinte e quatro vezes por dia.

## Um passo que só você pode dar

A rotina foi criada (`WeSales — construção contínua do CRM`, de hora em hora,
minuto :02), mas nasceu **sem o conector `GHL CRM` anexado**. A API de criação
de rotinas desta organização não aceita anexar conector, e o aviso foi
explícito: as sessões que ela disparar rodam sem ferramenta de CRM.

Na prática isso corta as frentes A e B — ela consegue melhorar especificação e
fechar lacunas, mas não lê nem escreve no CRM.

**Como resolver:** claude.ai → **Agendados** → abrir
`WeSales — construção contínua do CRM` → habilitar o conector **GHL CRM** para
ela. Um clique, e as quatro frentes passam a funcionar.

Enquanto isso não acontece, a rotina não quebra nem mente: o prompt manda
registrar a ausência em `APRENDIZADOS-CRM.md` e seguir para uma frente que não
dependa do CRM.

## Limites

- Só mexe em `wesales/`. O repositório também abriga a máquina de vídeo e a
  Jazz, e a fronteira vale para a rotina também
- Não encosta nas 12 falhas de `tests/test_narracao_das_specs.py` — são
  pré-existentes e de outro projeto
- Sem nada de valor a fazer, não commita e encerra em silêncio. Commit vazio
  não é sinal de trabalho

## Controlar

Pausar, mudar o intervalo ou desligar: é só pedir. Ela não se cancela sozinha.
