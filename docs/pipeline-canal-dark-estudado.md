# O `pipeline_canal_dark_v1.2` — estudado em 12/10/2026, e o que entrou

O dono mandou o zip sem recado, como mandou os cinco repositórios em 11/10.
A régua é a mesma da §5 da rotina: **entra o que converge com medição nossa, e
nada por autoridade da fonte.** Este é um produto comercial (tem licença, chave
e área de membros), para Windows, com Claude Code como assistente — não é um
repositório público, então nem "muita gente usa" nem "é pago" dizem algo sobre
se funciona.

## O que ele é

Fábrica de canal dark local: roteiro → narração (`edge-tts`) → cenas animadas
num navegador → montagem → shorts → thumbnail → postagem. Seis *skills* do
Claude Code (`comecar`, `produzir-video`, `pauta`, `publicar`, `manutencao`,
`montar-canal`), `.bat` de dois cliques, esteira por tarefa agendada do Windows.

**Honesto no que importa:** o `LEIA-ME.md` diz, sem rodeio, que vídeo enviado por
projeto novo da API do YouTube **fica travado como privado** até a auditoria do
Google, que ela é pedida por formulário e pode levar semanas, e que *"o Pipeline
não tem como pular essa regra"*. Isso bate com o que nós vivemos — e é um ponto a
favor da procedência dele.

## O que NÃO entrou, com motivo

- **O pipeline inteiro.** É Windows (`.bat`, `.ps1`, tarefa agendada), roda no PC
  do dono e é paralelo ao nosso. Trocar o nosso por ele seria regressão: ele não
  tem corpus anti-duplicata por título, nem `origem_id`, nem `ALVO_POR_CANAL`,
  nem a disciplina de réplica (688/707/708/720), nem a conta de poder do 693.
- **O alvo de volume.** Ele mira `loudnorm=I=-14`. **Nós já miramos o mesmo**, e
  com o pico mais apertado: `TP=-1.5` contra `TP=-6` no mixer dele
  (`fabrica/fabrica.py:686`). Não havia nada a importar.
- **A faixa de short de 15 a 58 s** (`motor/shorts.py`). É escolha de projeto num
  produto, não medição — então **não conta como fonte independente** contra o
  experimento 38. As duas que contam continuam sendo o nosso `chart=mostPopular`
  e o `references/shorts-playbook.md`.
- **O limiar de similaridade de 0,30 (erro) / 0,15 (aviso).** O nosso é 0,65, e
  vem do mapa que o dono trouxe. O dele não traz procedência nenhuma. **Limiar
  sem procedência não substitui limiar com procedência** — e a trava da rodada de
  construção proíbe mexer nisso de qualquer forma.
- **O checador de pronúncia por `faster-whisper`.** É a melhor ideia do pacote e
  ataca um buraco real nosso (o `ortografia` mede o TEXTO, nunca o áudio). Mas
  baixa 200–500 MB de modelo e o render acontece no runner, com minuto contado.
  **Fica como sugestão ao dono**, não como dependência nova.
- **`volume_blocos`, `contato`, thumbnail 1280x720, `frases_repetidas`.** Ou já
  temos equivalente, ou não se aplica a short solto com b-roll zero.

## O que ENTROU, e é UMA coisa

**A CONFERÊNCIA do volume — `fabrica/som.py`.** O que ele tem e nós não tínhamos
não é o alvo: é **medir o arquivo final**. Nós aplicamos `loudnorm` e nunca
lemos o resultado. Ter o filtro na linha de comando não é evidência de que a peça
saiu a −14: o `loudnorm` de uma passada é dinâmico e pode errar o alvo, em
silêncio. **É a assinatura do §3.8 pela enésima vez** — portão verde fabricando
"está tudo certo" porque ninguém mediu a saída.

O módulo lê `ebur128` (LUFS, LRA, pico real) e `silencedetect`, e **não reprova
nada**: sai como `::notice::` no `frota.yml`, depois do render e com
`continue-on-error`, porque medição nova não pode derrubar publicação. Quando
houver leitura de peça real o bastante, aí se decide se vira portão.

**Validado com sinal controlado**, neste container, em 12/10:

| sinal | LUFS |
|---|---|
| tom de 220 Hz a −30 dB | **−52,0** |
| o mesmo depois do nosso `loudnorm=I=-14:TP=-1.5:LRA=11` | **−13,9** |

O instrumento responde e o filtro acerta o alvo **num sinal estável**. Isso
**não** é evidência sobre as peças publicadas: fala com música e corte de cena é
outro sinal, e é exatamente o que falta medir. Seis testes em
`tests/test_som.py`, e um deles confere que o `ALVO_LUFS` do módulo continua
igual ao `loudnorm` de `fabrica.py` — para o número não virar cópia que
envelhece.

**Uma diferença deliberada:** o piso de silêncio dele é 2,0 s e o nosso é
**1,0 s**. A razão é medida e é nossa: a sobrecarga por cena é `P + 0,300`, e P
vai de **1,04 s** no pt-BR a **1,72 s** no polonês. Com piso de 2,0 s o silêncio
NORMAL de fim de frase da voz polonesa já quase dispara, e a medição não
separaria defeito de modelo.

## Um fato técnico que vale guardar

`motor/medidas.py` documenta que extrair quadro de vídeo HD (BT.709, faixa
limitada) para JPEG sem `out_color_matrix=bt601:out_range=pc` deixa **as cores
puxadas para o verde**. As nossas medições de dinamismo (690/699) usam
`signalstats` **sobre o vídeo**, não sobre JPEG, então estão a salvo — mas se
algum dia alguém conferir thumbnail ou quadro por imagem exportada, é por aí que
o erro entra.

## A chave da licença: NÃO entrou no git, e o motivo é de uma linha

O dono mandou a chave em 12/10 pedindo para guardá-la no GitHub. **Não guardei, e
não vou sem ele dizer de novo sabendo disto:**
`sampaioopablo1-lgtm/maquina-yt-receita` é **PÚBLICO** (`visibility=public`,
conferido na hora). Commit de chave em repositório público **publica a licença
paga dele para qualquer pessoa**, e histórico de git não se apaga de fork nem de
indexador — rastreador de segredo varre o GitHub em minutos.

**E a rota de *secret* do GitHub está fechada para mim por PROXY, não por
permissão** — `"not permitted through this proxy"`, e repete com `admin: true`.
Então nem o caminho certo dentro do GitHub eu consigo fazer; quem faz é ele, em
*Settings → Secrets and variables → Actions*.

**Onde a chave ficou:** `config.licenca_pipeline_canal_dark` no Supabase, que é
privado e é onde os segredos da máquina já moram (ao lado de `yt_token_<canal>` e
`pexels_api_key`). O registro guarda também por que não está no git e que o
`app.ianofacil.com.br` é negado pelo proxy desta sessão.

**E ela não serve aqui de qualquer forma:** a verificação de licença chama
`app.ianofacil.com.br`, que o proxy nega no CONNECT. O lugar de uso dela é o PC
dele, com `canal.bat licenca ativar <chave>`.


## As duas primeiras medições de som de PEÇA REAL — 12/10

O instrumento saiu do tom sintético e mediu produção:

| peça | LUFS | desvio do alvo | pico dBTP | LRA | silêncios ≥1 s |
|---|---|---|---|---|---|
| `labtreinamento-s023` | **−14,2** | −0,2 | −1,4 | 2,9 | nenhum |
| `labtreinamento-s024` | **−14,6** | −0,6 | −1,5 | 3,0 | nenhum |

**As duas dentro de 1,0 LU do alvo** — o `loudnorm` de uma passada segura o alvo
em conteúdo real, não só em tom estável. **E as duas ABAIXO dele.** Dois de dois
na mesma direção não prova viés; fica escrito para a terceira medição ter com o
que comparar, em vez de eu reparar no padrão depois e chamar de descoberta.

**O zero silêncio corrobora o modelo de P:** previsto `P + 0,300 = 1,04 s` de
intervalo por cena no pt-BR, e o `silencedetect` com piso de 1,0 s não acusa
nada — ou seja, os intervalos reais ficam logo abaixo de 1,0 s. Perto do
previsto, e um pouco abaixo.

**Terceira medição, às 23:1x — e ela quebra o padrão de duas:**

| peça | LUFS | desvio | pico | LRA |
|---|---|---|---|---|
| `s023` | −14,2 | −0,2 | −1,4 | 2,9 |
| `s024` | −14,6 | −0,6 | −1,5 | 3,0 |
| `s025` | **−14,2** | **−0,2** | −1,5 | **2,0** |

O desvio voltou a −0,2. **Então "as duas abaixo" não virou tendência** — três
peças dão −0,2, −0,6 e −0,2, todas dentro de 1,0 LU e sem direção clara. Eu
escrevi o aviso antes justamente para não transformar duas leituras num padrão,
e a terceira mostrou que o aviso era necessário.

O LRA caiu para **2,0** nesta peça, contra 2,9 e 3,0. Faixa dinâmica menor é
esperada numa peça com mais cenas curtas, mas **n=1 e eu não medi causa** —
fica anotado, não concluído.

**Quarta medicao, as 00:1x de 13/10 — e ela e a PRIMEIRA ACIMA do alvo:**

| peca | LUFS | desvio | pico | LRA |
|---|---|---|---|---|
| `s023` | −14,2 | −0,2 | −1,4 | 2,9 |
| `s024` | −14,6 | −0,6 | −1,5 | 3,0 |
| `s025` | −14,2 | −0,2 | −1,5 | 2,0 |
| `s026` | **−13,8** | **+0,2** | −1,4 | **1,8** |

Quatro pecas: −0,2, −0,6, −0,2, **+0,2**. **Nao ha direcao**, e agora isso esta
medido nos dois sentidos em vez de so afirmado. Todas dentro de 1,0 LU, nenhuma
com silencio >= 1,0 s. O `loudnorm` de uma passada segura o alvo em conteudo
real — o que o instrumento estava la para descobrir, e descobriu sem reprovar
nada.

O LRA continua caindo (2,9 → 3,0 → 2,0 → 1,8) e as duas ultimas sao as pecas de
nove cenas curtas. **Nao medi causa e nao vou chamar de achado**: n pequeno, e
cena curta muda duas coisas ao mesmo tempo (quantidade de emenda e duracao de
fala). Fica anotado como a proxima pergunta, nao como resposta.

**Quinta medicao, as 01:1x de 13/10 (`s027`): LUFS −14,4, desvio −0,4, pico
−1,5, LRA 2,0, zero silencios.** As cinco: −0,2, −0,6, −0,2, **+0,2**, −0,4.
Faixa de 0,8 LU em torno do alvo, **sem direcao** e nenhuma fora de 1,0 LU. Isto
e o que o instrumento tinha a dizer, e ele ja disse: o `loudnorm` de uma passada
segura o alvo em conteudo real. **Nao vira portao** — limiar sem procedencia e
critério inventado, e aqui nao ha o que reprovar.

**Sexta medicao (`s028`): LUFS −14,2, desvio −0,2, pico −1,3, LRA 2,4.** As seis:
−0,2, −0,6, −0,2, +0,2, −0,4, −0,2. **Mediana −0,2, faixa de 0,8 LU, nenhuma
fora de 1,0.** E o LRA, que eu vinha anotando como "caindo" (2,9 → 3,0 → 2,0 →
1,8), voltou a **2,4** — logo **nao estava caindo**, estava oscilando entre 1,8
e 3,0. Eu tinha escrito "nao medi causa e nao vou chamar de achado"; a sexta
leitura mostra que nem o padrao existia.
