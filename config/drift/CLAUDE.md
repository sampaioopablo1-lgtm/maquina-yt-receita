# Edição de vídeos — O Próximo Cliente

> Copie este arquivo para a pasta dos vídeos no PC (ex.: C:\Users\sampa\Videos\OPC\CLAUDE.md).
> O Claude Code local lê CLAUDE.md da pasta atual no início de cada sessão, então
> estas regras valem sem precisar colar prompt. Registro do MCP sem token, uma vez:
> `claude mcp add drift --scope user -- "C:\Program Files\Drift\drift.exe" --mcp-stdio`

Você opera o editor Drift pelo MCP "drift". Vídeos talking head em PT-BR,
saída 9:16 1080x1920, 30 a 90 s, para Instagram e Meta Ads.

## Nunca
- Nunca feche, reinicie ou mate o processo do Drift. Se algo travar, pare e
  me avise. Reiniciar o Drift destrói a conexão MCP.
- Nunca 4K. Nunca espere mais de 90 s por um job travado: reporte.
- Nunca aplique estilo de legenda antes de eu revisar a transcrição.
- Nunca pergunte qual trecho cortar ou qual tempo usar: decida e me diga depois.

## Sempre
- take_snapshot antes de cada lote e informe o hash.
- Clipes por UUID de inspect({clips:true}), nunca por posição.
- apply não é atômico: confira stopped/failed antes de seguir.
- Salve o projeto (.drift) depois de cada etapa concluída.
- Um vídeo por vez, do início ao fim, com export antes do próximo.

## Fluxo por vídeo
1. inspect({clips:true, detail:true}) + capture(): diagnóstico
2. take_snapshot
3. Projeto 1080x1920; clipe preenchendo o quadro, rosto no terço superior
4. Remover silêncios e respiros
5. Legenda de TODOS os clipes; confirme a contagem
6. PARE e mostre o texto das legendas para revisão
7. Correções + estilo num único apply
8. Zoom rápido no gancho; lower third "Pablo Sampaio / O Próximo Cliente"
9. Export 1080x1920 30 fps H.264 para a pasta do projeto
10. capture() final

## Vocabulário que o Whisper erra
CNAE, CNPJ, CPL, CAC, ROAS, CTR, CPM, lead, leads, funil, funil de vendas,
tráfego pago, remarketing, lookalike, Meta Ads, WhatsApp, MEI, ticket, copy,
criativo, mentoria, O Próximo Cliente

## Identidade
Fonte Montserrat. Branco #FFFFFF, azul-noite #0B1220, laranja #FF7A1A para
palavra-chave. Legenda curta, 3 a 5 palavras por bloco, legível no celular,
sem emoji. Credibilidade, não estilo viral genérico.

## Armadilhas do Drift
- Legenda sai só do primeiro clipe: gere de todos e conte.
- Remover trecho: corte dentro do clipe, apague a legenda correspondente,
  junte a timeline.
- Preview duplicado é bug visual, não erro.
- Zoom tende a sair lento e com borda preta: peça rápido, sem borda.
- O Drift aplica cor de legenda por bloco, não por palavra: bloco com
  palavra-chave sai inteiro em laranja, os demais em branco.
