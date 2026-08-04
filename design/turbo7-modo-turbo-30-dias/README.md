# Flyer — Programa Modo Turbo 30 Dias (Turbo 7)

Peça de divulgação do programa **Modo Turbo**, construída sobre o fluxo de
cadência **12 × 30** (12 tentativas de contato distribuídas em 30 dias).

## Entregáveis

| Arquivo | Formato | Uso |
| --- | --- | --- |
| `flyer-turbo7-modo-turbo-30-dias.png` | 2400 × 3600 px (2:3, 2×) | WhatsApp, Instagram, e-mail, apresentações |
| `flyer-turbo7-modo-turbo-30-dias.pdf`  | 12,5 × 18,75 in, 1 página | Impressão e envio comercial |

## Fontes do projeto

| Arquivo | Papel |
| --- | --- |
| `FILOSOFIA-DE-DESIGN.md` | Manifesto visual (*Cadência Instrumental*) que rege a peça |
| `build.py` | Gera `flyer.html` — conteúdo, cadência e diagrama são dados, não markup solto |
| `flyer.html` | Artefato gerado (não editar à mão; editar `build.py`) |
| `render.py` | Rasteriza o HTML em PNG 2× e PDF via Chromium headless |
| `fonts/` | Big Shoulders, Outfit e Geist Mono (licença OFL) |

## Como regerar

```bash
cd design/turbo7-modo-turbo-30-dias
python3 build.py     # HTML a partir do conteúdo estruturado
python3 render.py    # PNG (2400×3600) + PDF
```

Requer `pillow` e o Chromium apontado em `render.py:CHROME`.

## Onde mexer no conteúdo

Tudo o que é editorial está no topo de `build.py`:

- `CADENCIA` — os 12 toques: `(dia, canal)`, com canal em `MSG`,
  `CALL_WA` ou `CALL`. Alterar a lista redesenha o diagrama inteiro,
  incluindo numeração dos toques e linha de canais.
- `ABANDONO` / `CONVERSAO` — os intervalos de toques marcados pelas chaves
  vermelha e verde acima do eixo.
- `INCLUSOS` — os quatro itens de escopo.
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
