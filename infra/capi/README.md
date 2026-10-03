# Alimentar a Meta com o evento de reunião agendada

## O que isto resolve

Hoje a campanha otimiza por **lead** — ela procura quem preenche formulário. Isso é
o objetivo errado: preencher formulário é barato e não paga nada. O que paga é
**reunião**.

Este script manda de volta para a Meta, a cada reunião marcada, um evento dizendo
*"esta pessoa virou reunião"*, identificada por e-mail e telefone criptografados
(SHA-256, como a Meta exige — o dado cru nunca sai daqui). A Meta cruza com quem
clicou no anúncio e passa a procurar mais gente parecida com quem **agenda**.

## O que é preciso

- `META_ACCESS_TOKEN` — token do usuário do sistema "Integracao mcp" (Employee).
  O conector do Claude **não** faz isso: ele expõe regras de pixel de site, e o
  Pablo não tem site. Evento servidor a servidor exige token.
- Conjunto de dados: `1600846091439175` ("O PRÓXIMO CLIENTE"), já existe e está
  ativo — mas nunca disparou nada (`last_fired_time` = 1969).

## Como rodar

```
META_ACCESS_TOKEN=EAA... python3 enviar_reuniao.py \
  '[{"email":"fulano@x.com","telefone":"21999999999","quando":1789012345,"nome":"Fulano"}]'
```

Sucesso é `events_received` igual ao número de pessoas enviadas.

## Regras que a Meta impõe e o script já respeita

| Regra | Como o script trata |
|---|---|
| Dado pessoal só criptografado | SHA-256 em e-mail, telefone e nome |
| Telefone com código do país | `21980417915` vira `5521980417915` |
| Evento com no máximo 7 dias | `quando` é o momento do agendamento |
| Evento duplicado conta uma vez | `event_id` derivado do e-mail |

## A ordem certa das coisas

1. **Agora:** mandar os eventos. Não muda nada na campanha — está construindo
   histórico. Custo zero, risco zero.
2. **Aos ~15 eventos acumulados** (2 a 3 semanas no ritmo projetado): trocar a
   otimização dos conjuntos de `LEAD_GENERATION` para `QUALITY_LEAD`. Aí a
   campanha passa a perseguir agendamento.
3. **Ligar antes disso é pior que não ligar** — o algoritmo entra em aprendizado,
   não sai por falta de volume, e o custo por resultado sobe.

## O que vem de brinde

Com histórico no conjunto de dados, dá para criar **público semelhante a quem
agendou reunião** — não semelhante a uma lista de CNPJ, semelhante a quem de fato
marcou. É o público mais valioso que uma conta pode ter, e ele só existe depois
que os eventos entram.
