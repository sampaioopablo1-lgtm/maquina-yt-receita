# Conectar a máquina ao Claude (MCP)

Em vez de digitar comandos, você conversa. Pergunta *"qual vídeo teve a pior
retenção?"* e a máquina responde usando **a sua conta**, sem terceiro no meio.

## O que é MCP, em uma frase

É um **padrão de encaixe** — como a entrada USB. Não é uma marca. Qualquer
ferramenta pode falar MCP, e este projeto agora fala.

## Por que um servidor próprio, e não um conector pronto

| | Conector de terceiro | Este servidor |
|---|---|---|
| Empresa de fora vê seus dados | sim | **não** |
| Mensalidade | geralmente sim | **não** |
| Lê métricas | sim | sim |
| **Publica vídeo** | **não** (são só leitura) | **sim** |
| Usa a sua autorização | não | sim |

Conectores de analytics são somente leitura. Nenhum sobe vídeo. Como a máquina
já conversa com o YouTube para publicar, expor isso como MCP foi só colocar a
tomada por cima.

## Instalar

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

Confirme que funcionou:

```bash
.venv/bin/maquina-mcp --help
```

## Conectar ao Claude Desktop

Abra o arquivo de configuração:

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

E adicione (trocando `/caminho/para` pelo caminho real do projeto):

```json
{
  "mcpServers": {
    "maquina": {
      "command": "/caminho/para/maquina-yt-receita/.venv/bin/maquina-mcp",
      "env": {
        "ANTHROPIC_API_KEY": "sua-chave",
        "OPENAI_API_KEY": "sua-chave",
        "ELEVENLABS_API_KEY": "sua-chave",
        "MAQ_TTS_VOICE_ID": "seu-voice-id"
      }
    }
  }
}
```

Reinicie o Claude Desktop. Deve aparecer um ícone de ferramentas na conversa.

> **Não funciona nesta sessão do Claude Code na web.** O servidor roda como
> processo local, na sua máquina — é lá que estão suas credenciais.

## As 9 ferramentas

**Leitura** (seguras, não mudam nada):

| Ferramenta | Pergunte assim |
|---|---|
| `maquina_status` | *"a máquina está configurada?"* |
| `maquina_listar_videos` | *"quais vídeos estão prontos?"* |
| `maquina_pesquisar_subnicho` | *"o que funciona no nicho de finanças?"* |
| `maquina_diagnosticar_video` | *"por que esse vídeo não foi pra frente?"* |
| `maquina_ler_comentarios` | *"o que estão falando nos comentários?"* |
| `maquina_revisar_roteiro` | *"esse roteiro soa natural?"* |
| `maquina_gerar_ideias` | *"me dá 5 pautas de vídeo longo"* |

**Escrita** (gastam dinheiro ou publicam):

| Ferramenta | O que faz |
|---|---|
| `maquina_produzir_video` | Produz o MP4. ~US$ 2,70 e alguns minutos. **Não publica.** |
| `maquina_publicar_video` | Publica no canal. **Exige confirmação explícita.** |

## A trava da publicação

`maquina_publicar_video` **não publica** se você não passar `confirmar=true`.
Sem isso ela apenas simula e mostra o que aconteceria.

Isso é proposital: numa conversa, uma frase ambígua como *"pode subir esse aí"*
não deve virar um vídeo público no canal. A confirmação tem que ser deliberada.

Antes de publicar, ela ainda roda todas as checagens de compliance — teto
diário, similaridade de roteiro, título duplicado. Se qualquer uma bloquear,
nada sobe.

## O que MCP não resolve

**Não roda sozinho.** MCP só age quando você pergunta. O canal precisa publicar
às 3h de domingo sem ninguém acordado — e isso continua sendo o GitHub Actions
(`docs/01-arquitetura.md`).

Pense assim: **MCP é o volante, o Actions é o motor.** Você usa o MCP para
entender e decidir; o Actions executa a rotina.

## Se der problema

Pergunte *"a máquina está configurada?"* — o `maquina_status` lista exatamente
o que falta.

Erros comuns já vêm com a solução na resposta:

| Erro | O que fazer |
|---|---|
| Sem credencial do YouTube | `maquina auth-youtube` (confirme o canal @SetiapLevelID) |
| Chave de API ausente | Preencher o `.env` |
| Cota esgotada | Aguardar 24h (busca custa 100, upload ~1.600 de 10.000/dia) |
| Providers em "stub" | Faltam chaves — o conteúdo gerado é de teste, não publicável |
