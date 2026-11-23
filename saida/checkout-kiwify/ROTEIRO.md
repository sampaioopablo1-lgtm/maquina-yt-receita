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
1. **Cabeçalho (desktop):** `02-banner-desktop.png` (2000x590).
2. **Imagem:** `01-topo-celular.png` (1080x1350) — é o que o celular vê primeiro.
3. **Texto curto** (abaixo):

   > **Para dono de negócio que quer anunciar sem depender de agência.**
   > Você aprende a usar IA no Gerenciador de Anúncios para criar campanhas que levam cliente direto pro seu WhatsApp. Pague com Pix ou cartão e entre na hora.

4. Formulário (o da Kiwify).

Abaixo do formulário / coluna lateral:
5. **Imagem:** `03-como-funciona.png`
6. **Texto — o que você recebe:** ⚠️ **ESCREVA AQUI O QUE O CLUBE ENTREGA DE FATO** (aulas, prompts, encontros, comunidade, frequência). Eu não sei e não inventei.
7. **Imagem:** `04-preco.png`
8. **Imagem:** `05-garantia.png`
9. **Depoimentos:** só quando houver reais. Depoimento inventado é proibido pela Meta e pelo CDC.
10. **Exit popup** (Componentes extra → Exit pop-up): `06-exit-popup.png`.

**Cronômetro:** não use. Ele reinicia a cada visita, a pessoa percebe, e a oferta não acaba de verdade. Escassez falsa custa confiança e pode virar reclamação.

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
