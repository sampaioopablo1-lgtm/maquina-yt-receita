# Peça renderizada e AINDA NÃO publicada

Este arquivo existe porque a ponte tem um ponto único de falha que eu descobri
em 09/10/2026 às 17:4x: **o `urlartefato.yml` só aceita `workflow_dispatch`, e o
único disparador que eu tenho é a ferramenta MCP do GitHub.** Quando a sessão
dela cai (`Error POSTing to endpoint: invalid session`), o `gh api` não substitui:
`POST .../dispatches` volta **403 Resource not accessible by integration**, e
`gh api .../artifacts/<id>/zip` se recusa a seguir o redirecionamento para o
Azure e **não imprime a URL assinada** — a mensagem de erro nomeia só o host.

Então o render fica pronto, o artefato fica guardado, e a publicação espera.
Isso não perde trabalho: **o artefato do Actions vive 90 dias**, e a URL assinada
é gerada na hora, sob demanda. É só repetir o disparo quando o MCP voltar.

## Pendente agora

| pacote | artefato | render | o que falta |
|---|---|---|---|
| `epomeno-epipedo-s016` | `11632908824` | run 37966xxxxx, `success` | disparar `urlartefato.yml` com `artefatos=11632908824`, baixar na sandbox em `f/epomeno-epipedo-s016/`, rodar `conduz.py`, gravar em `videos` com `origem_id=h66MCKjwAJ8` e crescer o corpus para 239 |

A sandbox já está preparada: clone em `/home/user/maq` no commit `ff03e3e`,
`corpus.json` em 238 com md5 `d2be4d455c291cfa295c3cec9676ee3f` conferido contra
o banco, e o diretório `f/epomeno-epipedo-s016/` já criado e vazio.

## Quando esvaziar

Apague a linha da tabela depois de publicar e de conferir `tags` no vídeo. Se a
tabela ficar vazia, deixe o arquivo — o motivo acima continua valendo, e é ele
que impede que a próxima rodada ache que o render falhou.
