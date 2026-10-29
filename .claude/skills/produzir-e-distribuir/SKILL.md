---
name: produzir-e-distribuir
description: "Produz UMA peça da Máquina de vídeos (pauta → spec → portões → render → YouTube → registro) e a DISTRIBUI para Instagram, TikTok e as outras redes do perfil do canal, com CTA de link na bio. Use quando o dono pedir 'produza e publique', 'rode a rodada', 'distribua o short nas redes', ou quando a rotina horária for produzir. Só ponteiros para os donos de cada passo — nada aqui repete número nem procedimento."
---

# Produzir e distribuir — a rodada inteira, com um dono por passo

Esta skill **não carrega procedimento**: ela aponta para o módulo que é dono
de cada passo e diz a ordem. Número dentro de skill envelhece (é a lição que
tirou o procedimento do prompt do trigger em 19/10). O procedimento completo
é `docs/ROTINA.md`; os ponteiros que não envelhecem são o `CLAUDE.md`.

## Travas (iguais às do núcleo — não se negociam)

- YouTube publica **só** pelo `retomar.yml`. Nunca pela Composio, nunca por
  `publicar=true` no `frota.yml`.
- Não apague nem mova vídeo nem post publicado sem o dono dizer.
- Nunca imprima chave, token ou secret; nunca mande segredo por input de
  workflow. `UPLOAD_POST_API_KEY` e `YT_OAUTH_JSON` são colagem do dono.
- Conectar conta em rede nova é decisão do **dono** (painel do Upload-Post).
  A autorização de 09/10 cobre os três canais do YouTube, não redes novas.
- Não mexa em parâmetro de produção (`ALVO_SHORT`, `ALVO_POR_CANAL`,
  `TETO_POR_CANAL`, limiares do `variedade`).
- Toda mudança de código sai com suíte comparada à base da sessão, commit
  `-F` e push.

## A ordem, e quem é dono de cada passo

1. **Passo zero** — `python3 fabrica/passo_zero.py`: inscritos (recusa a
   leitura quando a janela não resolve), canal da vez, cota da janela. E
   `python3 fabrica/longo_por_canal.py` para a metade LONGO/CURTO do pedido.
2. **Pauta** — `python3 fabrica/pauta_do_momento.py <canal>`: origem de menor
   contagem com reserva, irmãos e famílias já usadas, texto INTEIRO dos
   capítulos livres. Família entre canais: `fabrica/familia_entre_canais.py`.
3. **Forma** — `fabrica/contagem_de_cenas.py` (chave `por_cadencia_servivel`),
   `esqueleto_entre_canais.sugere_forma`, orçamento de caracteres pelo
   `fabrica/mira.py` (janela dos DOIS mundos). Paleta **lida** de
   `temas_do_dono.paleta_do_canal`; layouts só do conjunto sondado por
   `layouts_do_short`.
4. **Construtor com guardas** — `guardas_do_construtor.exige(spec)` antes de
   gravar; copy com `## TITULO SHORT`, `## COMENTARIO FIXADO` **depois** da
   descrição, hashtags, tags.
5. **Passada no rascunho** — `python3 fabrica/antes_do_render.py` (aceita a
   spec em memória); depois os portões: `python3 fabrica/prontidao.py
   fabrica/specs/<spec>.json`. O número de portões sai de
   `len(prontidao.avalia(spec))`, não de cabeça.
6. **Commit e push da spec ANTES do despacho** — o runner faz checkout;
   `fabrica/despacho_da_rodada.py` confere `no_checkout` e monta os dois
   payloads (render com `publicar=false`; `retomar.yml` para publicar).
7. **Esperar pelos PASSOS, não pelo run** — `python3 fabrica/espera_do_run.py
   <run>` (saída 0 = terminou).
8. **Provedor, som, título** — `python3 fabrica/anotacoes_do_run.py <run>
   <pacote>`: conta o aviso do Piper no job que emitiu SOM, cruza o título do
   notice com o da linha.
9. **Registro dos quatro parques** — `registro_da_rodada` (duração, som, SQL
   pendente, corpus), e **releia** cada parque depois de gravar.
10. **Distribuir para as outras redes** — `fabrica/distribuicao.py`, dono
    único. Dispare o `distribuir.yml` com `pacote`, `run_id` (do render) e
    `youtube_id` (da publicação); ele baixa o MESMO `short.mp4`, mede a
    duração, monta legenda e primeiro comentário pela copy (título curto +
    CTA "link na bio" na língua do canal + hashtags) e chama a API do
    Upload-Post. Depois do run, pegue o artefato `distribuicao-<pacote>` e
    parqueie a linha em `docs/pendente/distribuicoes.jsonl` com
    `distribuicao.parqueia` — ele recusa repetir a mesma peça na mesma rede.
    Localmente, só para VER o que iria: `python3 fabrica/distribuicao.py
    <spec.json> <short.mp4>` (sem `--publicar`).
11. **Relato** — curto, em pt-BR: o que saiu, onde, links, o que mudou no
    sistema (§11-bis), e o que falta ao dono.

## O que falta ao dono antes do passo 10 funcionar

`docs/distribuicao-multi-rede.md` tem a lista com o porquê de cada item:
conta no Upload-Post com as contas de cada canal conectadas, um **perfil por
canal** (nome em `fabrica/perfis_sociais.json`), o link da bio por canal, e o
segredo `UPLOAD_POST_API_KEY` no GitHub. Sem isso o passo 10 **recusa** e diz
o que falta — não inventa perfil nem publica em lugar nenhum.
