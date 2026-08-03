# Roadmap — do repositório ao canal publicando sozinho

O código está pronto e validado offline. O que falta é ligar as credenciais e
calibrar o conteúdo. Ordem importa: cada bloco depende do anterior.

## 1. Credenciais (bloqueia tudo)

| Passo | Onde | Resultado |
|---|---|---|
| Ativar YouTube Data API v3 | Google Cloud Console | projeto habilitado |
| Criar OAuth client ID tipo **Desktop app** | Console → Credenciais | baixa `client_secret.json` |
| Rodar `maquina auth-youtube` | máquina local | gera `secrets/youtube_token.json` |
| Chave Anthropic (roteiro) | console.anthropic.com | `ANTHROPIC_API_KEY` |
| Chave ElevenLabs (narração) | elevenlabs.io | `ELEVENLABS_API_KEY` |
| Chave OpenAI (imagens) | platform.openai.com | `OPENAI_API_KEY` |

Depois, cadastre como **secrets do repositório** (Settings → Secrets → Actions):
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `MAQ_TTS_VOICE_ID`,
`YT_TOKEN_JSON` (o conteúdo inteiro do `youtube_token.json`).

> ⚠️ A cota padrão da YouTube Data API é 10.000 unidades/dia e **um upload custa
> ~1.600**. São ~6 uploads/dia no teto — folgado para o limite de 2/dia da
> máquina, mas não tente escalar sem pedir aumento de cota.

## 2. Sua voz — clonar e **testar antes de escalar**

```bash
mkdir -p assets/voice   # o .wav NÃO é versionado
# copie Gravando-aprimorado-v2.wav para assets/voice/
maquina voice-clone assets/voice/Gravando-aprimorado-v2.wav
```

Copie o `voice_id` retornado para o `.env` e para o secret `MAQ_TTS_VOICE_ID`.
Vale gravar 2-3 minutos limpos: a qualidade do clone depende mais da limpeza do
áudio do que da duração.

**Depois, obrigatoriamente, o teste de sotaque:**

```bash
maquina voice-test
```

Envie o áudio gerado para um falante nativo de indonésio e faça três perguntas:

1. A pronúncia soa nativa ou estrangeira?
2. O ritmo soa natural para narração?
3. Você assistiria 8 minutos desta voz?

Se a resposta 1 for "estrangeira", **troque para voz nativa de catálogo** e fixe
uma só como identidade do canal. Sotaque perceptível bate direto no pilar 3
(retenção) — e retenção é o que decide se o vídeo é entregue. Quinze minutos de
teste aqui evitam semanas de vídeo com curva ruim.

## 3. Calibrar o conteúdo (é aqui que o canal se define)

O único campo realmente vazio hoje é `canal.referencias_titulo` em
`config/default.yaml`. Ele alimenta o pilar 1.

1. Levante 15-20 títulos que já performam no subnicho **em indonésio**.
2. Extraia as palavras-chave recorrentes.
3. Preencha a lista.

Sem isso o LLM escreve títulos genéricos e o pilar 1 não sustenta.

Opcional, mas recomendado: colocar uma trilha em `assets/musica/trilha.mp3`
(licença livre). A máquina mixa em -22 dB automaticamente; sem o arquivo ela
apenas segue sem trilha.

## 4. Primeiro vídeo real

```bash
maquina doctor                        # confirme que os 3 providers dizem "real"
maquina ideias --formato longo        # veja se as pautas fazem sentido
maquina produzir "<título escolhido>"
```

**Assista o vídeo inteiro antes de publicar.** Este é o ponto de calibragem: é
onde você ajusta prompt de roteiro, ritmo e estilo visual. Espere 2-3 iterações
até o resultado ficar publicável — isso é normal, não é sinal de erro.

```bash
maquina publicar <slug> --em-horas 3
```

## 5. Ligar a automação

Só depois que a saída manual estiver boa:

- `producao.yml` já roda **terças e sextas, 09:00 UTC**. Ajuste o cron ao seu ritmo.
- `publicacao.yml` continua **manual e intencional** — é a revisão humana.
- Configure `environment: youtube` com reviewers para exigir aprovação no Actions.

## 5b. Fechar o loop de feedback (crítico em idioma estrangeiro)

Depois de cada vídeo publicado ganhar tração:

```bash
maquina revisar <slug>       # o roteiro soa natural para um nativo?
maquina comentarios <slug>   # o que a audiência está dizendo, traduzido
```

O segundo comando destaca **sinais técnicos acionáveis** — volume de música,
qualidade da voz, ritmo, legendas. Esses sinais chegam aos comentários antes de
aparecerem na curva de retenção. Num canal em idioma que você não lê, esse canal
de feedback só existe se você rodar isso.

## 6. Aprender com os números

Aplique `supabase/schema.sql` no seu projeto Supabase. A view `painel_pilares`
responde direto "qual vídeo tem qual gargalo", e `progresso_ypp` acompanha a
distância até 1.000 inscritos / 4.000 horas.

`diagnostico.yml` roda toda segunda e escreve o resultado no summary do job.

**Não conclua nada abaixo de 500 impressões** — a máquina se recusa a diagnosticar
nessa faixa de propósito. Amostra pequena leva a refazer a coisa errada.

## Expectativa realista

- **Semanas 1-2:** calibragem. Os primeiros vídeos servem para ajustar o prompt.
- **Semanas 3-8:** constância. O acervo é o ativo; um vídeo isolado não sustenta canal.
- **7 vídeos sem tração não é sinal de fracasso** — é a faixa em que o canal ainda
  está sendo lido pelo algoritmo. Ajuste o gargalo apontado e continue.
- **Monetização:** 1.000 inscritos + 4.000h em 12 meses, mais revisão humana do
  YouTube. O caminho realista é vídeo longo; o volume de Shorts necessário
  (10M views/90 dias) não é alcançável para canal novo.

## Backlog técnico (não bloqueia o lançamento)

- Sincronizar o estado SQLite → Supabase no fim de cada job (hoje o Actions usa cache)
- Alinhamento de legenda por Whisper (timing por palavra, em vez de proporcional)
- Cortes de b-roll em vídeo, não só imagem estática com Ken Burns
- Teste A/B de thumbnail com troca automática por CTR
- Capítulos automáticos na descrição dos vídeos longos
