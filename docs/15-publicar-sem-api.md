# Publicar sem API — os caminhos que existem de verdade

Resposta curta: **sim, existe um caminho simples e sem API nenhuma — o upload manual
pelo YouTube Studio.** Ele não tem risco de remoção, não depende de auditoria, não
depende de fornecedor e não custa mensalidade. O custo é tempo humano, e menos do que
parece.

Antes do como, dois fatos que eliminam atalhos tentadores.

---

## O atalho que não existe

> "E se eu subir pela API mesmo sem auditoria, e depois trocar para público na mão?"

Não funciona. O vídeo enviado por projeto não auditado fica **locked private** — um
estado diferente de "privado por escolha". O dono **não consegue** alterar a
privacidade até submeter o vídeo a revisão e ela ser aprovada. Não é uma trava de
interface que se contorna; é o estado do vídeo.

Isso fecha a porta para qualquer variação de "usa a API sem auditar e ajusta depois".

## O caminho que existe, mas eu não recomendo

Automação de navegador (Playwright dirigindo o Studio logado). Este ambiente até tem
Chromium instalado, então seria tecnicamente possível.

**Não vale.** Automatizar o Studio contra os Termos de Serviço do YouTube arrisca
suspensão da conta Google inteira — não de um vídeo, da conta que hospeda os 10 canais.
Trocar um risco de perder vídeos por um risco de perder o portfólio é um mau negócio,
ainda mais depois de já ter perdido 6 uploads. Se algum dia for feito, que seja uma
decisão explícita e informada, não um default meu.

---

## O gargalo real não é o mecanismo de upload

De 10 canais, **só o Setiap Level existe no YouTube** (`UCf4-ZFoZQWKJotZNdi4Yl7w`).

Os outros 9 não foram criados. Então, dos pacotes prontos, a maioria **não tem para
onde ir** — nenhum mecanismo de publicação resolve isso, porque o destino não existe.

Criar cada canal é uma conta de marca no Studio: ~2 minutos. **~20 minutos no total**,
e é isso que destrava tudo o mais.

---

## A sequência, com o custo real

| # | Passo | Tempo | Frequência |
|---|---|---|---|
| 1 | Criar os 9 canais que faltam (conta de marca no Studio) | ~20 min | uma vez |
| 2 | Publicar manualmente pelo Studio | ~4 min/vídeo | por vídeo |
| 3 | *(opcional)* Enviar o formulário de auditoria da API | ~40 min | uma vez |

O passo 3 não é pré-requisito de nada — é o que faz o passo 2 deixar de existir. Sem
ele, publicar 10 vídeos custa ~40 min; com ele, custa zero para sempre. Os dois passos
são custo humano de uma vez só; a diferença é que o 2 se repete e o 3 não.

### Como fica um upload manual (~4 min)

1. Studio → **Criar** → **Enviar vídeo** → arrasta o `video.mp4`
   *(o Studio aceita até 15 arquivos de uma vez — dá para subir um canal inteiro numa
   leva e editar um a um enquanto processam)*
2. Título e descrição: **cola do `copy.md`** — já vem com os capítulos cronometrados
   reais, CTA, disclosure de conteúdo sintético, 3 hashtags e 15 tags
3. Thumbnail: sobe o `thumbnail.png` (1280×720)
4. Legendas: **Subtítulos → Enviar arquivo → `legendas.srt`**
   *(só nos pacotes a partir do setiap-level-004; os anteriores têm legenda queimada)*
5. Público-alvo: **"Não, não é conteúdo para crianças"**
6. Agendar no pico do país do canal, ou publicar direto
7. Fixar o comentário que está no fim do `copy.md`

---

## Fila de publicação, na ordem da evidência

Ordenada por views/dia do outlier que originou a pauta — quem tem mais evidência
atrás, sobe primeiro. Só entram os pacotes que cumprem a regra de duração (≥ 8 min).

| Canal | Pacote | Duração | Evidência (v/d) | Canal existe? |
|---|---|---|---|---|
| Game Money Lab | `$300 Million Per Game` | 12,3 min | 85.492 | ❌ criar |
| Nível do Jogo | `Lei Felca nos Games` | 14,2 min | 6.780 | ❌ criar |
| Next Level Money | `Dutch East India Company` | 12,1 min | 3.487 | ❌ criar |
| Seviye Seviye | `Asgari ücret açlık sınırı` | 13,3 min | 2.993 | ❌ criar |
| Agla Level | `EPF Scheme 2026` | 12,1 min | 2.042 | ❌ criar |
| Resep Naik Level | `Belanja Mingguan Rp100.000` | 14,3 min | 720 | ❌ criar |
| Kolejny Poziom | `Emerytura z ZUS` | 12,7 min | 198 | ❌ criar |
| **Setiap Level** | `Cara Atur Gaji 2026` (004) | 28,6 min | 9.467 | ✅ **pode subir hoje** |
| **Setiap Level** | `Gaji Harian Rp100 Ribu` (003) | 25,7 min | 143 | ✅ pode subir hoje |
| Cocina por Niveles | `Despensa de $500 pesos` | 14,5 min | — | ❌ criar |

**Não publicar:** os pacotes de 1,6 a 3,3 min (`ndj-skin-r200`, `seviye-5-kural`,
`gml-free-to-play-math`, `epomeno-3-synitheies`, `cocina-5-cenas`, `resep-5-menu`,
`agla-level-7-salary-levels`, `setiap-orang-pintar`). São anteriores à regra de duração
e ficam abaixo do mid-roll de 8 min. Servem de material de arquivo, não de estreia.

**Pendência:** `epomeno-1000e-odigos-20260805` está registrado mas **sem links no
Drive** — a entrega não fechou. Precisa ser reentregue antes de entrar na fila.

### Uma ressalva de cadência

Não suba os 10 no mesmo dia. Canal novo, com 0 inscritos, despejando 10 vídeos de uma
vez é o padrão que os sistemas do YouTube leem como spam. Um a dois por canal por dia
já é bastante, e dá para ler o que cada um faz antes de decidir o próximo.

---

## O que muda quando houver métrica

Hoje a tabela `metricas` está vazia, então toda decisão de pauta usa só grupo de pares.
Assim que os primeiros vídeos estiverem no ar, o Studio já dá retenção e CTR — e os
experimentos abertos em `experimentos` passam a ter como fechar:

- zoom+pan (2× mais movimento) contra o zoom parado dos 20 pacotes anteriores
- `.srt` próprio contra legenda queimada
- sistema de 4 pilares (4.757 v/d nos pares) contra o template `menabung` (1,0 v/d)

Não precisa de API para isso. Precisa dos vídeos no ar.
