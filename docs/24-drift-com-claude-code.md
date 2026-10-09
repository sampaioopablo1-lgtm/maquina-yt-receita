# Drift + Claude Code — como operar o editor por IA (lições aprendidas)

> Fonte: tutorial em vídeo de Ericson Lourenço (22 min) testando o Drift da
> CutWire com Claude Code, somado ao brief do Pablo de 05/09/2026 para os ~20
> vídeos talking head do Instagram "O Próximo Cliente". Isto é o que uma sessão
> precisa saber ANTES de tocar na timeline. O guia técnico do MCP (toolboxes,
> ops, códigos de erro) está no próprio Drift, em Agente → "Copiar guia".

## Onde isto roda

- O Drift é um editor **desktop, gratuito e open source**. Ele expõe um servidor
  MCP **local** (`http://127.0.0.1:4731/mcp`) com token novo a cada sessão do app.
- Só uma sessão do Claude Code **na mesma máquina** enxerga esse servidor. A
  sessão na nuvem (claude.ai/code) não alcança loopback do PC. Medido em
  06/09/2026: porta sem resposta e nenhuma ferramenta `drift` carregada.
- Registro (PowerShell, no PC):
  `claude mcp add --transport http drift http://127.0.0.1:4731/mcp --scope user --header "Authorization: Bearer <token>"`
  Se já existir, `claude mcp remove drift --scope user` antes. Confirme com
  `claude mcp list` (deve mostrar `drift ... Connected`).
- **Reinicie a sessão do Claude Code depois de registrar.** As ferramentas do
  MCP não carregam numa sessão já aberta — foi exatamente o que travou o tutorial
  até o autor abrir um chat novo.

## Como conectar quando a IA "não conhece" o Drift

1. No Drift: botão **Agente** → *Permitir nesta sessão* → *Copiar para o cursor*
   (dados do MCP) e *Copiar guia para o agente* (manual). Cole os dois no chat.
2. A IA pode dizer que "não existe integração". Está errada: o recurso é nativo
   do Drift. Mande a documentação (docs.cutwire.org/drift) e o guia copiado.
3. Fluxo das ferramentas: `catalog` → `toolbox({name})` → `apply({ops})` →
   `inspect` → `capture`. Só `apply` agrupa várias mutações num único undo.

## O que funcionou de primeira

- **Remover silêncios e respiros**: prompt de uma linha, resposta em ~1 min para
  um vídeo de 1 min. O vídeo vira vários clipes na timeline. Cortes limpos, sem
  comer palavra.
- **Lower third** (nome, fundo preto, canto inferior esquerdo, fade in/out,
  9 s): a IA criou uma track própria para o texto, sem pedir.
- **Zoom-in** no primeiro bloco: funcionou, e a IA exportou o vídeo sozinha ao
  final para entregar.

## Onde a IA erra, e a instrução que corrige

| Erro observado | Por que acontece | O que pedir |
|---|---|---|
| Legenda gerada só do **primeiro clipe** | depois do corte de silêncios há vários clipes; `generate_subtitles` roda por clipe | "Gere legenda de TODOS os clipes da timeline e me diga quantos legendou" |
| Pediu o trecho de tempo em vez de decidir | a IA não sabe que a repetição é erro | "Leia as legendas, identifique a fala repetida e remova o bloco errado, deixando a versão que está mais para o final" |
| Removeu o **clipe inteiro** quando só parte estava errada | agiu no clipe, não no trecho | "Corte dentro do clipe e remova só o trecho errado" |
| Deixou a **legenda órfã** do trecho removido | legenda e vídeo são objetos separados | "Ao remover, exclua também a legenda correspondente" |
| Ficou **tela preta** no lugar do trecho | não fechou a lacuna | "Junte a timeline depois de remover" |
| Legendas **dessincronizadas** após os cortes | cues não acompanham o ripple | "As legendas não estão sincronizadas; regenere ou reposicione" |
| Lower third com **keyframe do centro para o canto** e nome em duas linhas | interpretou "fade" como movimento | "Sem movimento de posição: apareça já no local; nome numa linha só; fundo preto" |
| Zoom **lento e com bordas pretas** | escala insuficiente e curva longa | "Mais rápido, sem borda preta" |
| Elemento **duplicado no preview** | bug visual do Drift v0.5 | ignorar; exclua um e ele volta sozinho |
| A IA **pergunta a cada passo** | falta de mandato | "Aja por conta própria. Decida, execute e me diga depois" |

## Regras de operação (brief do Pablo, valem sempre)

1. Agir por conta própria; não perguntar qual trecho cortar nem qual tempo usar.
2. `take_snapshot` antes de cada lote, informando o hash.
3. Um vídeo por vez, do início ao fim, com export antes de começar o próximo.
4. Nunca 4K: 1080p, 9:16 vertical para Reels.
5. Identificar clipes por UUID de `inspect({clips:true})`, nunca por posição.
6. `apply` **não é atômico**: conferir `stopped`/`failed` e avisar antes de seguir.
7. **Parar depois de gerar a legenda** e mostrar o texto: o Pablo revisa o
   vocabulário antes de qualquer estilo. Refazer legenda estilizada é o
   retrabalho mais caro.

Vocabulário que o Whisper erra (corrigir antes de aplicar): CNAE, CNPJ, CPL,
CAC, ROAS, CTR, CPM, lead, leads, funil, funil de vendas, tráfego pago,
remarketing, lookalike, Meta Ads, WhatsApp, MEI, ticket, copy, criativo,
mentoria, O Próximo Cliente.

## Fluxo padrão por vídeo

1. `inspect({clips:true, detail:true})` + `capture()` — diagnóstico
2. `take_snapshot`
3. remover silêncios e respiros
4. gerar legenda de TODOS os clipes; confirmar a contagem
5. **PARAR** e mostrar o texto das legendas
6. correções + estilo num único `apply` (frase curta, palavra-chave em cor,
   legível no celular, credibilidade e não estilo viral)
7. zoom sutil e rápido no clipe principal, se fizer sentido
8. export 1080p vertical
9. `capture()` final para conferir o enquadramento

## Saída esperada

9:16, 1080×1920, 30 a 90 segundos, legenda queimada com palavra-chave em
destaque, áudio normalizado. Parte dos vídeos vira criativo do Meta Ads
(doc 19 e doc 23); o resto é conteúdo de perfil.

## Plano B sem o Drift (sessão na nuvem)

Quando o vídeo está no Google Drive, o mesmo fluxo roda no sandbox do Composio
(ffmpeg + faster-whisper, rede aberta): cortar silêncios → transcrever →
parar para revisão → legendar com a identidade da marca (azul-noite `#0B1220`,
laranja `#FF7A1A`, Montserrat) → exportar 1080×1920. O arquivo volta pelo
Drive. Script: `opc_edit.py` (etapas `cortar`, `transcrever`, `legendar`).
