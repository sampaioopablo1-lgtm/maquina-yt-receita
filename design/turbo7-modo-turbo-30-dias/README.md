# Flyer — Programa Modo Turbo 30 Dias (Turbo 7)

Peça de divulgação do programa **Modo Turbo**, construída sobre o fluxo de
cadência **12 × 30**: 12 toques distribuídos em 30 dias, cruzando 2 a 3 canais
nos dias de pico.

## Entregáveis

| Arquivo | Formato | Uso |
| --- | --- | --- |
| `flyer-turbo7-modo-turbo-30-dias.png` | 2400 × 4320 px (1:1,8, 2×) | WhatsApp, Instagram, e-mail, apresentações |
| `flyer-turbo7-modo-turbo-30-dias.pdf`  | 12,5 × 22,5 in, 1 página | Impressão e envio comercial |
| `apresentacao.html` | Página autocontida | Link de apresentação (publicado como Artifact) |

## Fontes do projeto

| Arquivo | Papel |
| --- | --- |
| `FILOSOFIA-DE-DESIGN.md` | Manifesto visual (*Cadência Instrumental*) que rege a peça |
| `build.py` | Gera `flyer.html` — conteúdo, cadência e diagrama são dados, não markup solto |
| `flyer.html` | Artefato gerado (não editar à mão; editar `build.py`) |
| `render.py` | Rasteriza o HTML em PNG 2× e PDF via Chromium headless |
| `build_pagina.py` | Gera `apresentacao.html`, importando o conteúdo de `build.py` |
| `fonts/` | Big Shoulders, Outfit e Geist Mono (licença OFL) |

## Como regerar

```bash
cd design/turbo7-modo-turbo-30-dias
python3 build.py         # HTML do flyer a partir do conteúdo estruturado
python3 render.py        # PNG (2400×4320) + PDF
python3 build_pagina.py  # página de apresentação (usa o PNG já renderizado)
```

Requer `pillow` e o Chromium apontado em `render.py:CHROME`.

## Publicar o site

`build_site.py` emite `site/`, que é um site estático pronto — sem build step.
`netlify.toml` na raiz já aponta o `publish` para essa pasta, então basta
conectar o repositório ao projeto Netlify `modo-turbo-turbo7` (ou arrastar a
pasta `site/` para o deploy manual da Netlify).

`BASE_URL` em `build_site.py` alimenta as tags Open Graph, que exigem URL
absoluta. Se o domínio mudar, atualize a constante e regere — senão o preview
do link no WhatsApp aponta para o endereço antigo.

## Onde mexer no conteúdo

Tudo o que é editorial está no topo de `build.py`:

- `CADENCIA` — os 12 toques: `(dia, (canais...))`, com cada canal em `MSG`,
  `CALL_WA` ou `CALL`. Um dia pode acionar 1, 2 ou 3 canais; a pilha de glifos
  no diagrama cresce junto, e os dias de mais de um canal ganham o anel verde
  de pico. Alterar a lista redesenha o diagrama inteiro.
- `TOTAL_CONTATOS` — derivado da cadência, nunca digitado à mão: é o número que
  aparece na nota sob a legenda e na página.
- `ABANDONO` / `CONVERSAO` — os intervalos de toques marcados pelas chaves
  vermelha e verde acima do eixo.
- `INCLUSOS` — os três itens de escopo.
- `GESTAO_LEAD`, `GESTAO_TEXTO`, `METRICAS` — a seção de acompanhamento de
  performance: a frase-âncora, o texto e os eixos rastreados nas reuniões.
- `BONUS_METAS` / `BONUS_PREMIO` — as metas diárias do captador e o prêmio que
  elas destravam. A faixa é desenhada como equação, então acrescentar uma
  terceira meta só exige mais um item na lista.
- `LEGENDA` — rótulos dos canais.

Copy da manchete, alerta, estatísticas e bloco de oferta ficam no `TEMPLATE`,
na mesma seção do arquivo.

## Decisões de design

- **Paleta restrita**: violeta profundo, verde elétrico e branco. O vermelho
  aparece uma única vez — no alerta de perda de receita — para que o alerta
  tenha peso.
- **O diagrama é o argumento**: o mapa 12 × 30 ocupa o centro óptico da peça.
  A chave vermelha marca os toques 3 e 4 (dias 5 e 7), onde a maioria dos
  times para; a verde marca os toques 5 a 12, onde a conversão acontece.
- **A pilha mede a intensidade**: dias de pico cruzam 2 ou 3 canais, e a coluna
  fica visivelmente mais alta. A quantidade de contato vira altura no eixo, sem
  precisar de rótulo.
- **Gestão é seção, não item de lista**: o acompanhamento semanal saiu da grade
  de escopo e ganhou bloco próprio, com os eixos que a reunião revisa — volume
  de ligações, alcance das mensagens e qualidade das conversas.
- **O bônus é uma equação**: as duas metas diárias somam e um conector atravessa
  o vão até o prêmio, o único bloco de verde chapado antes do CTA. As metas são
  as mesmas grandezas que a reunião semanal acompanha — a faixa fecha o ciclo
  entre o que se mede e o que se ganha.
- **Oferta em dois tempos**: o valor do programa (R$ 20.000) e o que o cliente
  paga para começar (R$ 0 nos primeiros 30 dias) aparecem lado a lado, sem
  ambiguidade sobre o preço.
- **Glifos próprios**: os três canais usam ícones desenhados para a peça, não
  logomarcas de terceiros — mensagem, ligação pelo app e ligação convencional
  se distinguem por cor e preenchimento, com legenda explícita.

## Observações

O texto do flyer reproduz as afirmações comerciais fornecidas para a peça
(“+80% das conversões vêm da 4ª tentativa em diante”, “5 novos leads por dia”).
São alegações da campanha, não dados medidos neste repositório — vale conferir
a fonte antes de veicular.
