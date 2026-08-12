# Cota de upload do YouTube — o que é grátis e o que não é

> Escrito depois de eu ter usado uma conta errada por meses.

## A conta que eu fazia, e por que estava errada

O raciocínio comum — e o que este repositório assumia — é este:

```
10.000 unidades/dia  ÷  1.600 unidades por videos.insert  =  6 uploads/dia
```

**Está errado.** A documentação do `videos.insert` diz, literalmente:

> Quota impact: 100 calls per day. A call to this method has a quota cost of
> **1 unit in the Video Upload quota**.

Upload tem **balde próprio**. A alocação padrão de um projeto novo, na página de
cotas do Google, é:

| balde | padrão/dia |
|---|---|
| `videos.insert` | **100** |
| `search.list` | 100 |
| todo o resto, somado | 10.000 unidades |

Ou seja: **100 uploads por dia, de graça, em projeto próprio do Google Cloud.**
Não é preciso pagar nada para chegar lá, e não é preciso pedir aumento de cota.

## O porém, e ele é grande

Também literal, na mesma página:

> All videos uploaded via the `videos.insert` endpoint from **unverified API
> projects** created after 28 July 2020 will be **restricted to private viewing
> mode**. To lift this restriction, each API project must undergo an audit.

Como a diretriz aqui é **visibilidade sempre pública**, a auditoria deixa de ser
opcional. Sem ela, os 100 uploads/dia existem mas produzem 100 vídeos privados —
que é o mesmo que não publicar.

A auditoria é **gratuita**. É uma revisão de conformidade, não uma compra:
formulário *YouTube API Services — Audit and Quota Extension Form*. Leva semanas
e **não é garantida**.

## Por que nenhum serviço grátis dá 100 uploads/dia

Porque o teto não é do intermediário — é do YouTube. O que um revendedor vende
não é cota; é **a auditoria dele**. A Upload-Post cobra de €19 a €378/mês pelo
acesso ao projeto auditado dela, e é por isso que ela pode escrever "unlimited
uploads" sem mentir.

Isso também explica por que trocar de fornecedor não resolve:

| caminho | software | cota | visibilidade | custo |
|---|---|---|---|---|
| Upload-Post grátis | — | 10/**mês**, 1 perfil | pública | €0 |
| Upload-Post Basic | — | ilimitado, 5 perfis | pública | €19/mês |
| Upload-Post Business | — | ilimitado, 225 perfis | pública | €378/mês |
| Postiz auto-hospedado | grátis, open-source | **suas** credenciais → 100/dia | **privada** sem auditoria | €0 + servidor |
| Projeto próprio **auditado** | grátis | **100/dia** | pública | **€0** |

Postiz é software livre de verdade, mas ele publica com as **suas** credenciais.
Troca a camada de orquestração, não a cota nem a exigência de auditoria. Quem
escolhe Postiz sem auditar cai exatamente no mesmo lugar — só que hospedando um
servidor a mais.

## A decisão

**Auditar o projeto próprio.** É o único caminho que atende os três requisitos ao
mesmo tempo: 100 uploads/dia, público, e sem mensalidade. Custa semanas de espera
e um formulário.

Enquanto a auditoria está em análise, a Upload-Post grátis cobre o canal que já
existe — 10 uploads/mês é pouco, mas é exatamente o tamanho do gargalo atual, que
é ter **um** canal criado, não ter cota.

## Ordem de execução

1. Criar os 9 canais no Studio (~2 min cada) — destrava 10 pacotes prontos.
2. Enviar o formulário de auditoria. Semanas de fila; quanto antes entra, antes sai.
3. Enquanto isso, Upload-Post grátis para o `setiap-level`.
4. Auditoria aprovada → `config.api_auditada = 'true'`, OAuth próprio por canal,
   e a mensalidade nunca chega a existir.

---

## Busca por substituto grátis e ilimitado (2026-08-05)

Pablo pediu para procurar um substituto grátis da Upload-Post, de preferência
ilimitado. Não existe, e a razão não é preço — é estrutural.

### O que fecha a porta

Confirmado na documentação do YouTube, revisão de **8 de julho de 2026**: todo
vídeo enviado por `videos.insert` de projeto não auditado criado depois de
28/07/2020 fica **restrito a privado**.

E o detalhe que mata o contorno óbvio: **o dono do canal não consegue tornar o
vídeo público na mão.** A Central de Ajuda é explícita — *"unlike user-selected
private videos, you will not be able to change the video's state until after
you have successfully submitted the video for re-review"*. Não dá para subir
pela nossa própria API como privado e destravar no Studio com dois cliques.

Ou seja: **o teto pertence ao YouTube, não à ferramenta.** Quem vende plano
está vendendo a auditoria dele. É por isso que nenhum plano grátis é generoso.

### Camadas grátis medidas

| ferramenta | grátis | API no grátis? |
|---|---|---|
| **Upload-Post** (atual) | 10 envios/mês, 1 perfil | **sim** |
| Metricool | 20 posts/mês, 1 marca, aceita longo e Shorts | não — API a partir de ~US$ 53/mês |
| Publer | 10 posts por conta | não |
| Buffer | 10 posts por canal | não |
| Blotato | teste de 7 dias | — |
| Ayrshare | teste de 28 dias, depois US$ 149/mês | — |

**A camada grátis da Upload-Post é a melhor que existe para o nosso caso**, e
por um motivo específico: é a única com API no plano zero. O dobro de posts da
Metricool não serve a uma máquina que publica sozinha — sem API, publicar volta
a ser trabalho manual, e aí o Studio direto é melhor que qualquer intermediário.

### Auto-hospedado não resolve

Postiz e Mixpost são software livre, mas a integração com YouTube pede **as suas
credenciais** do Google Cloud: OAuth client ID no seu projeto. O software é
grátis; a parede é a mesma. Vale a pena para outras redes, não para esta.

### A única resposta "grátis e ilimitada"

Projeto próprio no Google Cloud, **auditado**: 100 uploads/dia, de graça, para
sempre, sem intermediário e sem mensalidade. A auditoria é gratuita. O custo é
tempo — semanas — e ela não é garantida. Há relato público de fila sem resposta
além do prazo (fórum de desenvolvedores do Google, tópico *"[URGENT] YouTube API
Compliance Audit – No Response After Critical Deadline"*).

**Conclusão operacional: a auditoria é o único caminho, e o custo dela é espera.
Então o erro caro é não ter começado ainda.** Formulário em
`docs/10-auditoria-api.md`.
