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
