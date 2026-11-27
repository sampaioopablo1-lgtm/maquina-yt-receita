# Checkout da Kiwify como página de vendas — Clube Tráfego com IA

Anúncio → checkout da Kiwify → pago. Sem página no meio: um clique e um carregamento a menos.

## O que a pesquisa mostrou (23/11/2026)
- 20 páginas de destino dos anúncios validados do nicho foram abertas no celular (`trafegocomia/pesquisa/lps/`).
- 8 tinham checkout: **Kiwify (2)**, Hotmart (2), Greenn, Ticto, Cakto, Wiven. Todos low ticket ou médio (R$ 17 a R$ 597).
- Nos dois checkouts Kiwify: cronômetro "oferta por tempo limitado", nome do produto, Nome/E-mail/Telefone,
  cartão ou Pix, **order bumps** ("SIM, EU ACEITO ESSA OFERTA ESPECIAL!") e selo de 7 dias de garantia.
- **No celular o formulário vem primeiro.** O que fica na coluna lateral aparece DEPOIS do botão de pagar.
  O que vende tem de estar nas imagens ACIMA do formulário.
- **Concorrente direto:** trafego17.zxlab.com.br (Rafael Castro, 56 dias no ar) vende "Claude Code conectado
  ao Gerenciador" por **R$ 17 único** na Black Friday (de R$ 97), para GESTOR de tráfego. A sua diferença:
  para DONO de negócio, e clube (continua) em vez de setup (uma vez).

## Configuração do produto (Produtos → Criar produto)
| Campo | Valor |
|---|---|
| Tipo de pagamento | **Assinatura recorrente**, mensal |
| Preço | R$ 29,90 |
| Formas de pagamento | Cartão + **Pix Automático** (renova sozinho no Pix) |
| Garantia | 7 dias (é o direito de arrependimento do CDC de qualquer forma) |
| Order bump | **NÃO no começo.** Em assinatura, o bump é cobrado em separado e, com frequência diferente, desliga o Pix Automático. Volte a ele quando houver vendas. |
| Pixel | Configurações → Pixel do Facebook + token da API de Conversões |

## Montagem no editor (aba Checkout)
Ordem de cima para baixo, **acima do formulário**:
1. **Cabeçalho:** `02-cabecalho.png` (2000x590).
2. **Imagem (coluna principal):** `01-topo.png` (1080x756).
3. **Texto curto** (abaixo):

   > **Para dono de negócio que quer anunciar sem depender de agência.**
   > Você aprende a usar IA no Gerenciador de Anúncios para criar campanhas que levam cliente direto pro seu WhatsApp. Pague com Pix ou cartão e entre na hora.

4. Formulário (o da Kiwify).

Abaixo do formulário, **na coluna principal** (nunca na lateral, ver tamanhos):
5. **Imagem:** `03-como-funciona.png`
6. **Texto — o que você recebe:** ⚠️ **ESCREVA AQUI O QUE O CLUBE ENTREGA DE FATO** (aulas, prompts, encontros, comunidade, frequência). Eu não sei e não inventei.
7. **Imagem:** `04-preco.png`
8. **Imagem:** `05-garantia.png`
9. **Depoimentos:** só quando houver reais. Depoimento inventado é proibido pela Meta e pelo CDC.
10. **Exit popup** (Componentes extra → Exit pop-up): `06-exit-popup.png`.

**Cronômetro:** não use. Ele reinicia a cada visita, a pessoa percebe, e a oferta não acaba de verdade. Escassez falsa custa confiança e pode virar reclamação.

## Tamanhos — medidos no checkout real da Kiwify
Medido no runner em 1280, 1440 e 1920 px (`trafegocomia/pesquisa/lps/desktop/medidas.json`): no computador o
checkout tem **984 px**; o cabeçalho ocupa 984, a **coluna principal ~670** e a **lateral ~284**. No celular tudo ~390.

| imagem | celular | computador | menor texto na tela |
|---|---|---|---|
| `02-cabecalho` 2000x590 | 390 × 115 | 984 × 290 | ~16 px no celular, ~40 px no computador |
| `01-topo` e as de 1080 | 390 de largura | 670 de largura | ~16 px no celular, ~27 px no computador |
| qualquer imagem de 1080 **na coluna lateral** | — | 284 de largura | **~11 px: ilegível** |

**Coluna lateral: só componente de TEXTO da Kiwify**, nunca imagem com texto. Sugestão de 4 caixas:
"✓ Acesso imediato após o pagamento", "✓ Pix ou cartão", "✓ 7 dias de garantia", "✓ Cancele quando quiser".

Simulação com essas medidas: `simulacao-computador-1440.png` e `simulacao-celular-390.png`. Confira no
botão de pré-visualização da própria Kiwify (computador e celular) antes de ligar o anúncio.

## Campos
Deixe só o que a Kiwify exige. Cada campo a mais é gente que desiste.

## No anúncio
- URL do site: o link `pay.kiwify.com.br/...` com UTMs: `?utm_source=meta&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`
- Objetivo **Vendas**, meta **Visualização da página de destino** no começo (o checkout carrega = visita).
  Passe para **Compra** quando passar de ~50 compras por semana.

## O que medir na 1ª semana
| métrica | onde | sinal |
|---|---|---|
| custo por visualização da página de destino | Gerenciador | até R$ 1,60 empata com conversão de 2% (LTV ~R$ 81) |
| taxa de checkout → compra | Kiwify (vendas / visitas do checkout) | abaixo de 1% com clique barato = problema no checkout, não no anúncio |
| abandono | Kiwify → carrinhos abandonados | mande mensagem no WhatsApp para quem deixou o telefone |

## Opção "página inteira numa imagem" (landing dentro do checkout)
- `landing-inteira.jpg` (1080 × 12.385, 1,3 MB): a página de vendas inteira. Vai como **um componente de
  imagem na coluna principal, ACIMA do formulário**. O formulário (Pix ou cartão) fica logo abaixo dela.
- Se a Kiwify recusar a altura ou o peso, suba `landing-parte-1.jpg` … `landing-parte-7.jpg` em sequência,
  na mesma coluna: juntas, elas formam a mesma imagem.
- Menor texto da imagem: 44 px → ~16 px no celular e ~27 px no computador (mesma régua medida acima).
- Ordem: promessa e preço → erro do impulsionar → a IA da Meta já decide quem vê → como funciona (3 passos)
  → exemplo de conversa → pra quem é e pra quem não é → preço vs Netflix → garantia → perguntas → "↓ Preencha".
- **A seção "O que você recebe" está DESLIGADA** até você escrever a lista em `trafegocomia/checkout/landing.json`
  (campo `recebe`). Com a lista preenchida, rode de novo `node trafegocomia/checkout/landing.js saida/checkout-kiwify`.
- Custo de colocar tudo antes do formulário: quem já decidiu tem de rolar ~12 telas no celular. A seta no fim
  resolve parte; a Kiwify também deixa ligar o botão flutuante de compra, se o seu plano tiver.
