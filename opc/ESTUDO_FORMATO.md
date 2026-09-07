# Por que tres entregas foram reprovadas — medicao, 07/09/2026

Este documento existe porque eu errei tres vezes seguidas e as tres vezes
"conferi" antes de entregar. O que eu conferia era a INTENCAO (a cor na chave de
estilo, o corpo da fonte na chave, a duracao pedida). Nenhuma dessas medidas
tocava o mp4 que a pessoa ia assistir.

Aqui estao os numeros. Metodo: baixar os Reels direto da Graph API do
Instagram, amostrar um quadro a cada 2s e medir fracao de navy, deteccao de
rosto, altura de caixa alta da legenda por componentes conexos, e cortes de
cena pelo filtro `select=gt(scene,0.30)` do ffmpeg.

## As pecas medidas

| apelido | permalink | dur |
|---|---|---|
| `r_aluguel` | [reel/Dc97SNHkn9S](https://www.instagram.com/reel/Dc97SNHkn9S/) | 42,4s |
| `r_whats` | [reel/Dc9qLojAnYJ](https://www.instagram.com/reel/Dc9qLojAnYJ/) | 34,5s |
| `r_indic` | [reel/Dc9XKYGCCpX](https://www.instagram.com/reel/Dc9XKYGCCpX/) | 28,6s |
| `reprovado` (meu) | [reel/Dc-_z0SEVri](https://www.instagram.com/reel/Dc-_z0SEVri/) | 33,1s |

As tres primeiras foram feitas no Drift e funcionam. A quarta e a minha.

## A tabela que explica tudo

| medida | r_aluguel | r_whats | r_indic | **reprovado** |
|---|---|---|---|---|
| cortes de cena | 4 | 8 | 8 | **2** |
| um corte a cada | 10,6s | 4,3s | 3,6s | **16,5s** |
| fracao navy (min→max) | 17%→92% | 1%→37% | 3%→38% | **35%→36%** |
| quadros sem rosto (b-roll) | 7 | 0 | 1 | **0** |
| caixa alta da legenda | 63px | 91px | 111px | **32px** |
| linha de base da legenda | 0,683 | 0,772 | 0,778 | **0,652** |
| pixels laranja na legenda | presente | 7-9 mil | 10-13 mil | **presente** |
| audio (media) | -17,0 dB | -16,9 dB | -16,7 dB | -17,1 dB |

A coluna do reprovado e uma linha reta. Trinta e tres segundos com a fracao de
navy variando **um ponto percentual**, os blocos navy sempre nas mesmas linhas
(0,00-0,09 e 0,91-1,00) e a legenda sempre na mesma faixa. Nao e um Reel com
defeito de acabamento: e um cartaz com narracao por cima.

## Os quatro defeitos, na ordem em que doem

1. **O quadro nunca muda.** As referencias trocam de plano a cada 3,6-10,6s e
   fazem o painel navy entrar e sair (o r_whats vai de 1% a 37% de navy). O meu
   render so sabia produzir UM layout para o video inteiro — o defeito estava na
   arquitetura, nao num parametro.
2. **Nao ha corte de apoio.** O r_aluguel passa 7 quadros amostrados sem
   nenhum rosto (dois trechos de ~6s); o r_indic, um. Sao os cortes de imagem
   que sustentam a narracao enquanto quem fala sai da tela.
3. **A legenda tem um terco do tamanho.** 32px de caixa alta contra 63/91/111.
   E eu tinha "medido" isso antes — media a EXTENSAO DA BANDA de texto e
   chamava de tamanho da letra. Banda inclui varias linhas, entao o numero saia
   grande e o corpo derivado dele saia pequeno. Duas vezes (64, depois 100).
4. **A legenda esta no lugar errado.** Linha de base em 0,652 contra 0,683-0,778
   das referencias: no meio do peito de quem fala, e nao no rodape.

## O que mudou por causa disso

`opc/conferir.py`. Ele abre o mp4 PRONTO e mede. Nenhuma constante de intencao
entra na conta.

E ele foi calibrado do jeito que importa: **rodando contra as tres referencias
primeiro**. Na primeira versao, quatro regras minhas reprovavam Reels que estao
no ar e funcionando:

| regra | o que ela reprovava | o defeito era |
|---|---|---|
| piso de 10 cortes/min | o r_aluguel (5,7/min) | piso alto demais; virou 5 |
| faixa da legenda | as quatro pecas, todas em "0,600" | eu media a borda do meu proprio recorte |
| rosto acima de 0,28 | o r_indic (rosto a 0,091) | era o rosto pequeno do b-roll, nao o locutor |
| duracao ate 42s | o r_aluguel (42,4s) | teto brigando com o reencode do Instagram |

Quando a regua reprova a peca que funciona, o defeito esta na regua. Depois da
correcao, as tres referencias passam e o reprovado falha em cinco regras — que
e o unico resultado que torna a regua util.

`conferir()` devolve dois vereditos separados de proposito: `aprovado` inclui as
escolhas da casa (b-roll do Pexels), e `conforme_referencia` so o que foi medido
nos Reels no ar. Se o segundo der falso para uma referencia, e a regua que
precisa de conserto.
