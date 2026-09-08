# Estudo — máquina de prospecção ativa no Instagram
*Pesquisa feita em 08/09/2026: documentação oficial da Meta, projetos de código aberto no GitHub e literatura técnica sobre limites e bloqueios.*

---

## 1. A descoberta que muda tudo

**Prospecção ativa por DM frio no Instagram não existe oficialmente. A API recusa.**

A API oficial de mensagens do Instagram só permite conversar dentro de uma janela de 24 horas, e essa janela só abre de três formas:

1. A pessoa te manda uma mensagem
2. **A pessoa comenta no seu post e isso dispara a automação**
3. A pessoa responde ao seu story

**Seguir você não abre a janela.** Sem interação da pessoa, nenhuma janela abre e nenhuma mensagem sai. A própria API rejeita a chamada.

Ou seja: quem promete "prospecção ativa automatizada no Instagram" está usando API não oficial e colocando a conta em risco. Não existe caminho legítimo para DM frio em escala.

---

## 2. Mas existe uma máquina oficial, e ela é melhor

A opção 2 acima é o ouro: **comentário dispara DM automática, e isso é sancionado pela Meta.**

A pessoa comenta uma palavra no seu post → a automação responde no comentário **e** manda a DM privada. Janela aberta legalmente, conversa liberada, zero risco de bloqueio.

Isso significa que a máquina do Instagram **não é outbound, é conteúdo com gatilho**:

```
POST com "Comenta AGENDA"
        ↓
   ele comenta          ← a janela abre oficialmente
        ↓
DM automática entrega o material      ← 100% automatizável, risco zero
        ↓
   agente qualifica na DM
        ↓
   wa.me → WhatsApp → agente da Clint → reunião na agenda
```

**O CTA "Comenta AGENDA que te mando na DM" que já está nos seus posts não é um truque de engajamento. É o único mecanismo de aquisição em escala que a Meta autoriza no Instagram.** Ele já estava certo, mas pelo motivo errado.

---

## 3. A virada estratégica

Se a janela só abre com comentário, então **o gargalo do Instagram não é quantos DMs você manda, é quantos comentários seu post recebe.**

E comentário se compra. Um post com o CTA de palavra-chave, impulsionado com R$ 10 por dia, multiplica comentários, que multiplicam janelas abertas legalmente, que multiplicam DMs automáticas.

**Isso transforma uma máquina que escala com risco numa máquina que escala com dinheiro.** E é exatamente a sua habilidade: tráfego pago.

| Caminho | Escala com | Risco |
|---|---|---|
| DM frio manual | seu tempo | bloqueio |
| DM frio automatizado | API não oficial | conta derrubada |
| **Post + comentário + DM automática** | **orçamento de mídia** | **zero** |

---

## 4. O que existe de ferramenta

**Oficial (parceiro Meta):** ManyChat é o padrão de mercado para comentário → DM. Conecta pela API aprovada, não por extensão de navegador. Planos de US$ 14 a US$ 69 por mês. Mais de 1 milhão de criadores usam.

**Não oficial (código aberto):** `instagrapi` (6.7 mil estrelas) e derivados como `aiograpi` e `okgram` fazem engenharia reversa do app Android. O `okgram` se descreve como "anti-detecção, impressão digital TLS JA3/JA4, evita logout e desafio de sessão". **A existência dessa corrida de gato e rato é a prova de que o Instagram detecta e derruba.** Não usar na conta principal, em hipótese alguma.

---

## 5. Os números reais de limite (relatados, a Meta não publica)

| Situação | Limite seguro por dia |
|---|---|
| DM frio, conta nova | 10 a 20 |
| DM frio, conta estabelecida | 30 a 50 |
| DM morno (para seguidor) | 30 a 50 nova, 50 a 100 estabelecida |
| Resposta a quem falou primeiro | praticamente sem limite |

O Instagram usa uma pontuação de confiança: idade da conta, taxa de denúncia, velocidade de envio, e se você manda para quem te segue. Estourar o limite dá **bloqueio de ação** ("tente novamente mais tarde"), normalmente 24 horas.

Note a última linha da tabela: **responder quem falou primeiro é ilimitado.** É por isso que a máquina inteira é desenhada para o lead falar primeiro.

---

## 6. A máquina completa, com as duas pistas

### Pista 1 — escala (conteúdo, automatizável, sem risco)
Post 4 a 5 vezes por semana com CTA de palavra-chave → impulsionar os que pegam tração com R$ 10 por dia → comentário abre a janela → DM automática entrega o carrossel → agente qualifica → wa.me → WhatsApp → agente da Clint → reunião.

### Pista 2 — precisão (manual, baixo volume, alta conversão)
Biblioteca de Anúncios e Maps identificam a empresa e o defeito → acha o dono → **resposta ao story** (que também abre a janela, e cai na caixa principal em vez de solicitações) → 10 a 15 por dia, no máximo → ele responde → mesma esteira.

As duas pistas terminam no mesmo funil da Clint.

---

## 7. Decisões

1. **Não construir bot de DM frio.** Nem com biblioteca aberta, nem com ferramenta paga que prometa isso. O risco não compensa e a conta do Pablo alimenta o público "ENG INST" dos anúncios.
2. **O CTA de palavra-chave é o núcleo da máquina**, não um detalhe de copy. Todo post leva ele.
3. **ManyChat entra quando um post passar de 20 comentários por dia.** Antes disso, responder na mão é mais rápido que configurar. Mas deixar a conta criada e o fluxo pronto antes, porque o gatilho tem que existir antes do post estourar.
4. **Impulsionar o post que pegar tração** é a alavanca mais barata que existe aqui, e é a habilidade que o Pablo já tem.
5. **Pista 2 continua manual e limitada a 10 a 15 por dia.** É precisão, não volume.

---

## Fontes
- Política da janela de 24 horas da API de mensagens do Instagram: [keyapi.ai](https://www.keyapi.ai/blog/instagram-messaging-api-policy/), [Spur](https://www.spurnow.com/en/blogs/instagram-dm-automation-rules)
- Automação permitida x proibida: [instantdm](https://instantdm.com/blog/is-instagram-automation-allowed), [creatorflow](https://creatorflow.so/blog/instagram-dm-compliance-meta-rules/)
- Limites diários e bloqueio de ação: [instantdm](https://instantdm.com/blog/instagram-dm-limits-rules-2026-the-ultimate-account-safety-guide), [flowgent](https://flowgent.ai/blog/instagram-dm-limits-how-many-messages-you-can-send-daily)
- Comentário para DM, parceiro oficial: [Manychat](https://get.manychat.com/use-case/comment-to-dm)
- Bibliotecas não oficiais: [instagrapi](https://github.com/subzeroid/instagrapi), [okgram](https://github.com/NiceDayZc/okgram)

---

# Parte 2 — existe ferramenta que simula comportamento humano com segurança?

*Pesquisa complementar, 08/09/2026, 16h25.*

## Os números que encerram a discussão

| Tipo de ferramenta | Taxa de suspensão por ano |
|---|---|
| Aprovada pela Meta, usa a API oficial (login por OAuth) | **abaixo de 0,5%** |
| Automação de navegador que **simula comportamento humano** | **15% a 30%** |

Trinta a sessenta vezes mais risco. E o dado é anual: rodando o ano inteiro, uma em cada quatro contas cai.

**O paradoxo:** "simula comportamento humano" não é o selo de segurança, é a descrição exata do que a Meta caça. Ferramenta oficial não simula nada — ela usa a API. E a API simplesmente recusa DM frio.

O que dispara punição, segundo a documentação: robô de navegador, raspagem, ferramenta que pede sua senha, e **DM frio para quem não interagiu**.

## O que a ferramenta oficial pode fazer (e é muito)

Pela API aprovada, dentro da janela de 24 horas aberta por comentário, resposta de story ou DM da pessoa: **até 200 DMs por hora.**

Compare:

| Caminho | Volume | Risco |
|---|---|---|
| DM frio "humanizado" | 10 a 20 por dia | 15% a 30% ao ano |
| DM oficial para quem agiu primeiro | **200 por hora** | abaixo de 0,5% |

Não é uma escolha entre segurança e volume. O caminho seguro é **quatrocentas vezes maior**. O gargalo nunca foi a ferramenta, é fazer a pessoa agir primeiro.

---

## O "Prospect Halo do Instagram" existe. É Meta Ads com objetivo de Mensagens.

Você quer: automatizado, em escala, sem bloqueio, atingindo exatamente as clínicas que escolheu, com o agente conversando. Isso existe e você já sabe operar.

**Campanha com objetivo Mensagens, destino Instagram Direct ou WhatsApp, para um público personalizado montado com os telefones das clínicas.**

```
Lista de telefones (Maps + Biblioteca)
        ↓
Público personalizado no Meta        ← correspondência de 40% a 70%
        ↓
Campanha "Mensagens" · R$ 20/dia · criativo com a dor específica
        ↓
O DONO CLICA E MANDA A MENSAGEM     ← ele inicia, janela abre sozinha
        ↓
Agente da Clint qualifica e agenda
```

**Por que isso é exatamente o que você pediu:**
- Roda o dia inteiro, sem você mandar nada. Não é 5 de manhã, 5 à tarde, 5 à noite: é o dia todo
- Chega em quem você escolheu, com nome e sobrenome
- **Quem inicia é ele**, então a janela abre legitimamente e o agente conversa sem limite
- Risco de bloqueio: zero. É publicidade paga, não automação
- É a sua habilidade, não uma ferramenta nova para aprender

**Ordem de grandeza:** lista de 300 telefones, 40% a 70% de correspondência dá 120 a 210 pessoas alcançáveis. Público pequeno significa frequência alta: o dono te vê 3 a 5 vezes por semana. Com R$ 20 por dia, a expectativa é de 15 a 40 conversas iniciadas por mês, todas inbound. Se 30% virarem reunião, são 5 a 12 reuniões por mês só desse canal.

---

## A máquina completa, com as três pistas

| Pista | Como funciona | Volume | Risco | Automatizada |
|---|---|---|---|---|
| **1. Anúncio de mensagem para lista** | ele clica e escreve | escala com orçamento | zero | sim |
| **2. Conteúdo com palavra-chave** | ele comenta, DM automática | escala com alcance | zero | sim |
| **3. Direct manual dirigido** | você, com a observação do anúncio dele | 15 por dia | baixo | não |

As três terminam na mesma esteira: agente qualifica, propõe 17h30 ou 18h30, evento na agenda.

**Pista 3 é a única manual, e é de propósito.** É a de maior conversão por contato, porque a observação é específica. 15 por dia, divididos como você quiser entre manhã, tarde e noite.

---

## Verdade sobre o prazo

Reunião **todo dia** significa mais de 20 por mês. Isso é número de mês 2 ou 3, não de meados de setembro.

O que é realista até 15/09: a máquina montada e rodando, com as primeiras 3 a 6 reuniões. Reunião diária vira meta de outubro, se as três pistas estiverem calibradas.

Quem promete agenda cheia em uma semana está vendendo ferramenta.
