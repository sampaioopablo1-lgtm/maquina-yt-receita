# Copy do WhatsApp — reescrita de 27/09 (pedido do dono)

**Regra do dono, 27/09 20:30:** nenhuma mensagem pede permissão, nenhuma avisa que vai
ligar. Cada uma provoca a dor, chama atenção e termina abrindo conversa (pergunta que o
lead responde em uma linha).

**Fora da reescrita, de propósito:** os 25 envios do `Lembretes da Reunião v3` — são
logística de reunião já marcada (data, link, "começamos em 10 minutos"), não pedem
permissão nem anunciam ligação. E a confirmação de opt-out da Triagem (`878b1c1f`),
que é resposta a quem pediu para parar.

**Merge field:** só `{{contact.first_name}}`, que o GHL preenche sempre que o lead tem
nome. Nenhuma mensagem usa `{{contact.dor_principal}}`, que está vazio em 58 de 64
contatos e deixaria a frase quebrada.

**Triagem:** a TRI-1 mantém as opções **1 / 2 / 3** porque o workflow lê a resposta pelo
número.

| Workflow · nó | Código | Texto novo |
|---|---|---|
| Cadência Inbound · `bb08de48` | MI-0 | Oi, {{contact.first_name}}! Aqui é da O Próximo Cliente, vi que você pediu contato. Pergunta direta: hoje o cliente novo de vocês vem mais de indicação ou de anúncio? Quem depende de indicação costuma ter mês bom e mês vazio. É o seu caso? |
| Cadência Inbound · `1ef37d68` | MIF | {{contact.first_name}}, você deixou seu contato porque alguma coisa não está fechando na captação de clientes. O que pesa mais hoje: pouca gente chegando ou gente chegando e não comprando? |
| Cadência 12x30 · `32443ee5` | MT1 | Oi, {{contact.first_name}}! Aqui é da O Próximo Cliente. Pergunta rápida: quantos contatos vocês receberam no último mês e quantos viraram venda? Se a resposta for "não sei", tem dinheiro ficando pelo caminho. |
| Cadência 12x30 · `afa33deb` | MT4 | {{contact.first_name}}, a maioria dos negócios que atendemos não tinha problema de anúncio: tinha contato chegando e ninguém respondendo a tempo. Aí dentro, quanto tempo leva hoje pra alguém responder um cliente novo? |
| 12x30 parte 2 · `aee02070` | MT8 | {{contact.first_name}}, uma linha só: hoje o cliente novo de vocês vem mais por indicação ou por anúncio? Indicação é ótima até o mês em que ela não vem. |
| 12x30 parte 2 · `2d46801f` | MT11 | {{contact.first_name}}, se captar cliente não fosse um problema aí, você não teria deixado seu contato. O que travou: falta de gente chegando ou gente que chega e some? |
| 12x30 parte 2 · `1c210e54` | MT12 | {{contact.first_name}}, vou encerrar por aqui. Fica uma pergunta: quantos clientes você deixou de fechar este mês porque ninguém respondeu a tempo? Se quiser descobrir, responde esta mensagem. |
| Fechar Horário · `50840639` | MFH1 | {{contact.first_name}}, foi bom falar com você. O que você me contou não se resolve sozinho, e cada semana parada é cliente indo pro concorrente. Qual dia desta semana fica melhor pra gente sentar 1 hora e resolver isso? |
| Fechar Horário · `f3b453e0` | MFH2 | {{contact.first_name}}, enquanto a gente não senta, seus anúncios seguem trazendo contato que não vira venda. Tenho manhã e tarde nos próximos dias. Qual você prefere? |
| Nutrição · `37a0e14d` | N1 | {{contact.first_name}}, uma verdade incômoda: lead respondido depois de 1 hora vale uma fração do respondido em 5 minutos. No seu negócio, quem responde primeiro: você ou o concorrente? |
| Nutrição · `ce3c0f0c` | N2 | {{contact.first_name}}, dos contatos que chegaram no último mês, quantos viraram conversa de verdade? Se você não sabe o número, é aí que o dinheiro está vazando. |
| Nutrição · `8c27d01c` | N3 | Antes de aumentar a verba do anúncio: quanto tempo o seu time leva pra responder quem chega? Na maioria das empresas o gargalo não é o anúncio, é o atendimento. Como está aí hoje? |
| Nutrição · `6d666618` | N4 | {{contact.first_name}}, e se todo lead que chega fosse atendido em minutos e já saísse com visita marcada na agenda do seu vendedor? A O Próximo Cliente faz isso além dos anúncios. Quem atende seus leads hoje? |
| Nutrição · `1075472b` | N5 | Anúncio com "fale conosco" atrai curioso. Anúncio com oferta clara, como diagnóstico ou orçamento rápido, atrai quem quer comprar. O seu hoje chama qual dos dois? |
| Nutrição · `1d41123d` | N6 | {{contact.first_name}}, última mensagem por aqui. Se os contatos chegarem e não virarem venda, você já sabe onde olhar. Quando quiser resolver isso, é só responder. |
| Recuperação de No-show · `b14157d9` | — | {{contact.first_name}}, a gente tinha marcado pra olhar por que os contatos não viram cliente, e esse problema continua aí. Qual dia desta semana funciona pra remarcar? |
| Reunião Cancelada · `4f096401` | — | {{contact.first_name}}, vi que a reunião foi cancelada. O problema que te fez marcar não foi cancelado junto. Qual dia desta semana fica melhor pra gente remarcar? |
| Triagem · `fd3d4f52` | TRI-1 | Valeu por responder, {{contact.first_name}}! Pra eu ir direto ao ponto, responde só com o número:<br>1 — quero parar de perder contato que chega pelo anúncio<br>2 — agora não, me chama mais pra frente<br>3 — não tenho interesse |
| Triagem · `d92c81e4` | resposta 1 | Boa! Me conta: hoje, quando um contato chega do anúncio, quem responde e em quanto tempo? |
| Triagem · `7553bed1` | resposta 2 | Combinado! Te mando só uma ideia curta a cada 15 dias. |

## Textos que saem (motivo)

- MI-0 atual: *"vamos te ligar em breve… responde o melhor horário pra falar"* — anuncia
  ligação e pede horário.
- MT1, MT4, MT8, MIF: *"Qual o melhor horário pra eu te ligar"*, *"eu ligo no horário
  que for melhor"* — pedem permissão/horário.
- MT11: *"se não é prioridade, tudo bem, é só me dizer"* — oferece a saída antes da dor.
- N1, N4: *"Quer que eu te mostre como? Se preferir não receber…"* — pedem permissão.
- Triagem resposta 1: *"Vou te ligar no próximo horário comercial"* — anuncia ligação.
  (A tarefa de ligar para o SDR continua sendo criada pelo workflow; só a mensagem muda.)

## Status

Pronto para gravar pela sessão logada do navegador, pelo mesmo caminho da §11 do
`ESTADO-27-09.md` (ensaio, gravação preservando `status`, releitura). Em 27/09 20:30 a
gravação de workflow estava bloqueada pela proteção da sessão em modo automático.
