# Produzir um Reel de fala do OPC — caminho rápido

A receita continua morando no banco (`opc.config.spec_reel_fala`). Isto aqui é só
o **maquinário**, para não reinventar nada a cada sessão.

Escrito em 07/09/2026, depois do OPC05 e do OPC06. O OPC05 levou horas — quase
tudo em descoberta de rede e de transporte. O OPC06 levou minutos. A diferença
está toda documentada abaixo e em `opc.config` (`rede_sandbox`, `fonte_sfx`,
`meta_biblioteca`).

## Preparar o sandbox (uma vez por sessão, ~3 min)

```bash
pip install imageio-ffmpeg pillow numpy faster-whisper "opencv-python-headless<5"
ln -sf $(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())") /usr/local/bin/ffmpeg
```

Não há ffmpeg nem ffprobe no sistema. Meça duração com `ffmpeg -i`.

O modelo do Whisper e as fontes **não** baixam direto: os hosts estão bloqueados.
Traga pela ponte (ver `opc.config.rede_sandbox`). As fontes saem de
`raw.githubusercontent.com`, que está liberado.

## Os sete passos

| passo | comando | o que decide |
|---|---|---|
| 1. take | ponte do Drive → `get.py <s3url> IMG_XXXX.MOV` | qual take |
| 2. preparar | `python3 preparar.py IMG_XXXX.MOV` | corte de silêncio + transcrição com tempo por palavra |
| 3. plano | editar `plano.py` | **o único passo que exige cabeça** |
| 4. b-roll | buscar no Pexels, `folha.py`, olhar | 3 candidatos por busca, escolher olhando |
| 5. montar | `monta_video.py && monta_audio.py && legendas.py` | — |
| 6. render | `render.py` | — |
| 7. conferir | `confere.py` + olhar a folha do arquivo final | pico do áudio e brilho nas trocas |

O passo 3 é onde vai o julgamento: quais trechos da fala entram, em que ordem,
o que é rosto e o que é B-roll, onde ficam as dissolvências. O resto é mecânico.

## Armadilhas que já custaram tempo

- **`legendas.py` tem `MANUAL` e `FORA` por vídeo.** Esvazie os dois ao trocar de
  take. No OPC06 eles vieram do OPC05 e enfiaram "cinco mil dez mil" no vídeo errado.
- **Os `.MOV` têm rotação em metadado.** O ffmpeg aplica e devolve 1080x1920. O
  PyAV não. Confira o primeiro quadro do arquivo **final**.
- **As URLs de SFX de `opc.midia` envelhecem.** Em 07/09/2026 três delas passaram a
  entregar outros arquivos. **Remeça sempre** com `mede_sfx.py` antes de reusar.
- **Whoosh bom incha até o pico.** Não reprove por "tempo de ataque": alinhe o
  **pico** no corte (`monta_audio.py` já faz isso).
- **Clipe do Pexels costuma abrir vazio ou fechar preto.** A folha de contato
  (`folha.py`) mostra um quadro a cada 1,5 s — é ela que dá o ponto de entrada.
- **Enquadramento:** cada take põe o rosto numa altura diferente. Rode `medir.py`
  e confira que a legenda em y=1478 cai **abaixo do queixo**. Se não cair, o
  caminho é trocar de take, não dar zoom.

## Entrega

O conector do Drive não sobe arquivo grande e o sandbox não publica URL. A rota
que funciona (escolhida pelo Pablo em 07/09/2026):

```
commit em entregas/<SLUG>/ → push → URL raw.githubusercontent.com
  → GOOGLEDRIVE_UPLOAD_FROM_URL (parent_folder_id da pasta "OPC — entregas")
```

O repositório é público. O material fica baixável por qualquer um e permanece no
histórico do git. Foi decisão dele, com o alerta dado.

Os dois `.txt` do pacote sobem direto pelo conector do Drive (`textContent`).

## O que ainda não fecha sozinho

A biblioteca de vídeo da Meta. A conta certa é **O Próximo Cliente**
(`1695865631502778`), mas a Meta ainda não liberou `ads_creative_upload_media`
para ela. Detalhes e caminho manual em `opc.config.meta_biblioteca`.
