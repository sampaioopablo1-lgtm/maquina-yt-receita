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
