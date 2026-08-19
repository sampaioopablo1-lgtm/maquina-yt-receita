# Incidente — feed dos portais fora do ar (19/08/2026)

## Sintoma
XML do VRSync inacessível desde 18/08 22:52 em ambas as rotas:
- Storage: `544 DatabaseTimeout`
- Worker público: `500`

Páginas de visita virtual (Edge Functions) seguiram respondendo 200.

## Diagnóstico (medido, não suposto)
- `feed_properties`: 21 MB, 3952 linhas vivas, 216 mortas, autovacuum em dia
  → **não era inchaço de tabela** (primeira hipótese, descartada).
- Ler 8,5 MB de jsonb da tabela: **21,6 s** a frio, 2,4 s após tocar os blocos.
- `pg_prewarm` de tabela + TOAST + índices (≈7.500 páginas) e a leitura pesada
  **continuou acima de 60 s** → com tudo em memória, o gargalo não é disco:
  é **CPU da instância** (créditos de burst esgotados).
- Gerador falhava com `canceling statement due to statement timeout`; o limite
  herdado pelo `service_role` é o global de **120 s**.

## Círculo vicioso
`feed-precomputar-vrsync` roda a cada 10 min, gasta ~120 s de CPU tentando
gerar 28 MB, falha, e consome justamente a CPU necessária para a instância se
recuperar.

## Mitigação aplicada
1. `statement_timeout` ampliado temporariamente: `anon` 3s→45s,
   `authenticated` 8s→45s, `authenticator` 8s→45s. **RESTAURAR** depois.
2. Rotinas desativadas (`cron.alter_job(active := false)`), a restaurar:
   - Feed/XML: feed-precomputar-vrsync, espelho-do-xml-nativo, feed-gate-xml-vista
   - Vigias: vigia-feed-interno, vigia-feed-interno-coleta, vigia-feed-auditar,
     vigia-feed-storage-frescor, vigia-acervo-feed, vigia-site-interno,
     vigia-site-interno-coleta
   - Sync/enriquecimento: smart-feed-sincronizar, smart-feed-enriquecer-pendentes,
     feed-ficha-backfill, feed-geocode-saude, feed-endereco-viacep-reaplicar
   - Captação: captacao-processar-fila, captacao-repor-prospects
3. Rotinas removidas do agendamento (`cron.unschedule`), a recriar:
   visita-publicar-no-feed (9-59/10), feed-trocar-fotos-convertidas (8-58/10),
   video-imovel-publicar-no-feed (7-57/10), feed-medir-fotos (*/3 → usar */15),
   descricao-rica-pedir (1,16,31,46, lote 5), descricao-rica-colher (6,21,36,51).

## O que NÃO foi feito, de propósito
`pause_project` existe na API, mas pausar derruba o projeto inteiro (inclusive
os tours que estavam no ar) sem prazo garantido de retorno — não é "reiniciar".
Reinício de verdade só pelo painel do Supabase, pelo dono da conta.

## Lição para o desenho
Precompute de um documento de 28 MB a cada 10 minutos é caro demais para a
classe da instância. Ao voltar, avaliar: espaçar para 30 min, gerar só quando
houver mudança (hash do conjunto), ou paginar a geração.

## Atualização 03:40 UTC — banco recuperou, plataforma não

Depois de ~50 min com a carga cortada, o Postgres voltou ao normal:

| Medição | Durante a crise | Agora |
|---|---|---|
| Ler 8,8 MB de jsonb (3.952 linhas) | > 60 s (estourava) | **0,08 s** |

Ou seja: o alívio de carga resolveu o lado do banco e confirmou o
diagnóstico de CPU esgotada. **Mas o feed continua fora do ar**, porque o
problema agora está nos serviços gerenciados, não no banco:

- **Storage**: `HEAD` responde 200 com `content-length: 28630672`, mas
  qualquer `GET` do corpo — inclusive com `Range: 0-2000` — devolve
  `544 DatabaseTimeout`. Metadados sãos, corpo inacessível. Arquivos
  pequenos de outros buckets seguem servindo 200.
- **PostgREST**: cache de schema não recarrega. Uma função criada e
  concedida a `anon` continuou invisível (`PGRST202`) minutos depois de
  `NOTIFY pgrst, 'reload schema'`; a primeira chamada levou 32 s.
- **Gerador**: segue falhando com statement timeout ao ler
  `feed_properties` — apesar de a mesma leitura levar 0,08 s em SQL
  direto. Consistente com PostgREST degradado, não com o banco.
- **Edge Functions**: saudáveis (visita responde 200).
- **Worker público**: 500 após 26 s (depende da cadeia quebrada).

Dois dos quatro serviços gerenciados estão presos desde a queda de ontem.
Isso não se conserta por SQL: exige reinício dos serviços — botão
`Restart project` no painel, ou suporte do Supabase.

### Estado deixado
- `statement_timeout` **restaurados** ao padrão (anon 3s, authenticated 8s,
  authenticator 8s) — a ampliação não era o caminho, já que o gerador usa
  `service_role` (global de 120 s).
- Função de teste `fn_teste_dormir` removida.
- Reativadas as rotinas de negócio: smart-feed-sincronizar,
  smart-feed-enriquecer-pendentes, captacao-processar-fila,
  captacao-repor-prospects, feed-ficha-backfill, feed-geocode-saude,
  feed-endereco-viacep-reaplicar, feed-gate-xml-vista, espelho-do-xml-nativo.
- Seguem **desativadas** até o reinício (só consumiriam recurso falhando):
  feed-precomputar-vrsync, vigia-feed-interno, vigia-feed-interno-coleta,
  vigia-feed-auditar, vigia-feed-storage-frescor, vigia-acervo-feed,
  vigia-site-interno, vigia-site-interno-coleta.
- Continuam fora do agendamento (recriar depois): visita-publicar-no-feed,
  feed-trocar-fotos-convertidas, video-imovel-publicar-no-feed,
  feed-medir-fotos, descricao-rica-pedir, descricao-rica-colher.

### Primeira ação após o reinício
Apagar o objeto `feeds-precomputados/vrsync.xml` (escrito às 22:52, durante
a instabilidade, e ilegível desde então) e deixar o gerador recriá-lo do
zero, em vez de sobrescrever um arquivo possivelmente corrompido.
