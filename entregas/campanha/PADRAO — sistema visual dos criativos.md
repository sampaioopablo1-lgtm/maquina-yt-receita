# PADRÃO — sistema visual dos criativos

Aprovado pelo Pablo em 23/09/2026. Gerador: `producao/padrao/padrao.py`.
Fontes: `./producao/padrao/fontes.sh` (não são versionadas, o `.gitignore` bloqueia
`fontes/` de propósito — o projeto baixa na hora).

## O que este padrão corrigiu

A primeira tentativa foi foto de banco com uma tarja preta por cima. O Pablo reprovou
em duas palavras: "ficou superficial". Ele estava certo, e o diagnóstico é registrável:

1. **Era template, não criativo.** O mesmo retângulo preto servia para qualquer frase.
2. **A tarja cobria metade da foto.** Se a imagem não ia ser vista, não precisava existir.
3. **A imagem contradizia o texto.** Numa peça, mulher sorrindo sob a frase "O lead chegou.
   E ficou lá." A foto desmentia a dor que a copy vendia.
4. **A tipografia era Liberation** (substituta de Arial), porque as fontes de verdade nunca
   tinham sido baixadas. Dava cara de apresentação de escritório.

O mais duro: **a LISTA cataloga exatamente esses defeitos nos concorrentes.** "Anúncio
igual ao de todo mundo", título que não promete nada, repetição de template. Estávamos
fazendo o que a gente cobra deles.

## Os três formatos

Três, e não um, por um motivo de mecanismo: a REGRA V3 pede **cinco anúncios por conjunto
com mensagens diferentes**. Cinco variações do mesmo layout não são cinco criativos — são o
defeito que a LISTA registrou em Brüno Deretti (14 anúncios ativos, 2 headlines) e em Camila
Becker (o próprio nome repetido nos 10 cards). Formatos distintos disputam a atenção de
jeitos distintos no mesmo feed.

### 1. AGENDA — a imagem é o argumento
Grade de segunda a sexta, trinta horários, **dois ocupados**. O vazio diz a frase antes de o
leitor ler a frase. Nenhuma das 178 páginas da LISTA desenha isso: o nicho inteiro usa foto
de gente sorrindo. É o formato mais barato de produzir (não depende de foto) e o mais
difícil de copiar, porque exige ter o argumento antes do layout.

### 2. PERGUNTA — contraste de feed
Fundo creme, deliberado. Nas varreduras de 22 e 23/09 — 1.793 anúncios de imobiliária, 201
de holding, 172 de recuperação tributária — o feed é **escuro e saturado sem exceção**. O
claro para o dedo por ser estranho ali. A chamada é uma pergunta do leitor sobre o próprio
negócio ("dos seus últimos 30 leads, quantos viraram reunião?"), nunca uma promessa nossa —
o briefing proíbe promessa, e a pergunta que ele não sabe responder é o gancho.

### 3. FOTO — usada, não coberta
Sem tarja. O escuro é um degradê só na coluna esquerda, onde a foto **já era vazia**; o rosto
e o cenário continuam vivos. Duas exigências para a foto entrar: espaço negativo à esquerda,
e **expressão que concorde com a frase**. Foto de pessoa rindo não recebe copy de dor.

## Regras duras

| Regra | Por quê |
|---|---|
| 1080×1350 (4:5) | A conta inteira é 4:5. Em 1:1 a peça sai cortada no feed. |
| Teto de 25% de texto | Ordem do Pablo. `monta_lote` **mede e recusa** quem passar — não avisa, recusa. |
| Largura é negociável, corpo de letra não | `encaixa` reduz até o piso e para. Não coube no piso? Reescreve-se a copy, não se diminui a fonte. |
| Nunca a foto do Pablo | Ordem permanente. A imagem TF03 está banida em definitivo. |
| **Nem foto que se PAREÇA com ele** | Ordem do Pablo em 23/09. Não basta não ser ele: modelo de banco com traços próximos (homem, 30–45, pele negra ou parda, barba curta, cabelo raspado) faz o leitor achar que é. Na dúvida sobre uma foto, não usar. |
| Sem preço, sem promessa em reais, sem "Rio", sem "90 dias" | Briefing da campanha. |
| Fontes reais (Montserrat + Playfair) | Liberation dá cara de PowerPoint. |
| Rodapé sempre fechado | Sem ele sobram ~200px mortos no pé. |

## Como rodar

```bash
./producao/padrao/fontes.sh                    # baixa Montserrat e Playfair
python3 producao/padrao/padrao.py --foto <jpg> # gera os três exemplos
```

O script sai com código 1 se alguma peça passar do teto, então serve em automação.

O `fontes.sh` tenta dois caminhos porque os ambientes diferem: no runner do GitHub Actions o
`raw.githubusercontent` responde; na sessão do agente ele devolve **403** e só o protocolo
git atravessa o proxy. Tenta o barato, cai para o sparse checkout de `google/fonts`, e
**confere o arquivo que chegou** — um 403 com corpo JSON passaria batido por um `curl -f`.

## Banco de imagem

As fotos vêm do **Pexels**. A conta da Muapi foi testada e está com **saldo zero**
(`balance: 0.0`, confirmado pela API), então o caminho de gerar por IA está fechado
enquanto não houver crédito — e não faz falta: os três formatos rodam sem ele, e dois nem
usam foto.

O `api.pexels.com` é alcançável do sandbox remoto (devolve 401 sem chave, não bloqueio),
mas **não há `PEXELS_API_KEY` no ambiente do agente** — `broll.chave()` procura a variável
e depois o Supabase, e os dois estão indisponíveis aqui. Enquanto a chave não vier, o
formato FOTO depende das imagens já baixadas.
