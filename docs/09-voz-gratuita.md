# Voz clonada gratuita — sem conectores, qualquer idioma

Pedido do operador: narração com a voz original dele, o mais natural possível,
**grátis e sem depender de serviços conectados**. Este documento registra a
pesquisa e o caminho implementado.

## O modelo escolhido e por quê

**[Chatterbox-TTS-Indonesian](https://huggingface.co/grandhigh/Chatterbox-TTS-Indonesian)**
— fine-tune do Chatterbox (Resemble AI) específico para indonésio.

| Critério | Situação |
|---|---|
| Preço | **Gratuito** (pesos abertos + GPU T4 grátis do Colab) |
| Licença | **Apache 2.0** — uso comercial liberado, canal monetizável |
| Clonagem | **Zero-shot por audio prompt** — o `referencia.wav` entra direto, sem treinar |
| Idioma | Indonésio nativo (fine-tune dedicado, não "malaio que serve") |
| Naturalidade | Base Chatterbox v3 lidera benchmarks abertos de 2026 |
| Marca d'água | PerTh (inaudível) embutida — transparência, não afeta o YouTube |

### Alternativas avaliadas e descartadas

| Modelo | Por que não |
|---|---|
| XTTS-v2 (Coqui) | Licença CPML **não-comercial** — e a Coqui fechou, ninguém vende licença. Risco direto para canal monetizado |
| F5-TTS | **CC-BY-NC** — não-comercial |
| Chatterbox Multilingual v3 puro | MIT, ótimo, mas indonésio **não está** na lista oficial de idiomas (malaio ≠ indonésio para a audiência) |
| CosyVoice 2 | Foco em zh/en/ja/ko, sem indonésio |

Para **outros idiomas** no futuro: [Chatterbox Multilingual v3](https://huggingface.co/ResembleAI/chatterbox)
(MIT, 20+ idiomas) com a mesma referência de voz — o notebook documenta a troca.

## Caminho principal: Modal (automático, sem Colab)

O pedido evoluiu: eliminar o passo manual do Colab. Resolvido com o **Modal** —
o mesmo Chatterbox indonésio, publicado como serviço serverless que o GitHub
Actions chama sozinho.

A conta que fecha: o free tier do Modal dá **US$ 30/mês recorrentes** (~50h de
GPU T4/mês). Um vídeo consome ~3 min de T4; o mês inteiro em ritmo diário usa
~US$ 1,50 do crédito. **Custo real: zero, permanentemente.**

Setup único (~10 min, instruções no topo de `infra/modal_tts.py`):

```bash
pip install modal && modal setup
modal secret create maquina-tts TOKEN=<token-forte>
modal run infra/modal_tts.py --ref assets/voice/referencia.wav   # sobe sua voz
modal deploy infra/modal_tts.py                                  # publica
```

A URL publicada vai para `MAQ_TTS_URL` (+ `MAQ_TTS_TOKEN`) no .env e nos
secrets do Actions. `tts_provider: "modal"` já é o padrão da config. O
container morre 2 min após cada uso — não gasta crédito parado.

Stack final do piloto automático: **Actions + Anthropic + Modal + YouTube API.**
Quatro peças, narração e imagens sem custo.

## Alternativa: Colab (manual, zero setup)

O caminho anterior continua disponível (`tts_provider: "lote"`) para quando não
houver conta Modal — mesma qualidade, só que semiautomático:

```
maquina produzir "Titulo"        # roteiro OK, para na narracao com instrucao
maquina exportar-narracao <slug> # gera out/<slug>/narracao.json
        │
        ▼
Colab (notebooks/narracao_chatterbox.ipynb, GPU T4 gratis)
  - recebe narracao.json + assets/voice/referencia.wav
  - clona e narra cada cena       (~minutos)
  - devolve narracao.zip
        │
        ▼
extrair em out/<slug>/audio/
maquina retomar <slug>           # segue: imagens, render, thumbnail
```

O provider `tts_provider: "lote"` (padrão atual) consome os MP3 gerados; se
faltar arquivo, o erro repete essas instruções.

## Referência de voz

`assets/voice/referencia.wav` — 74s, 48 kHz (fora do git, arquivo pessoal).
Análise do processo anterior: ruído ~50 dB abaixo da voz, sem saturação. Boa
referência.

**Para soar ainda menos "IA"** (pedido explícito do operador):

- Referência com **20-30s de fala contínua**, sem pausas longas, melhora o clone
  mais que qualquer parâmetro.
- No notebook: `exaggeration` baixo (0.3-0.4) — entonação teatral é o que
  denuncia voz sintética.
- Pontuação natural no roteiro: vírgulas e pontos guiam a prosódia.
- Trilha da YouTube Audio Library por baixo (-24 dB) mascara artefatos sutis.
- E o que mais importa segundo a política do YouTube: **não é "parecer humano"
  que protege o canal, é ter conteúdo com valor real**. Voz sintética é
  permitida; conteúdo sintético *realista* deve ser divulgado no upload — a
  máquina já faz essa divulgação automaticamente.

## Custo comparado

| Caminho | Custo/vídeo longo | Automação |
|---|---|---|
| **Colab + Chatterbox (atual)** | **R$ 0** | Semiautomática (você roda o notebook) |
| Fish Audio | ~US$ 0,12 | Total (cron narra sozinho) |
| ElevenLabs | assinatura | Total |

O plano pragmático: **começar no caminho gratuito** (que também é o teste de
sotaque de graça — a primeira amostra do notebook responde se o clone segura o
indonésio). Se o canal validar e o ritmo diário apertar, os ~US$ 4/mês do Fish
compram a automação completa da narração.

## Fontes

- [Chatterbox-TTS-Indonesian (HuggingFace)](https://huggingface.co/grandhigh/Chatterbox-TTS-Indonesian)
- [Chatterbox / Multilingual v3 — Resemble AI](https://www.resemble.ai/learn/models/chatterbox-multilingual)
- [ResembleAI/chatterbox (HuggingFace)](https://huggingface.co/ResembleAI/chatterbox)
- [Licença CPML do XTTS-v2 — guia de uso comercial](https://www.promptquorum.com/power-local-llm/local-tts-voice-cloning-piper-coqui-xtts)
- [F5-TTS — setup e licença](https://localaimaster.com/blog/f5-tts-setup-guide)
