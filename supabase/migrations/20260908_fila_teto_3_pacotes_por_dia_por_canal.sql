-- 08/09/2026: teto de pacotes/dia/canal de 1 -> 3 em `v_maquina_fila.pode_produzir`.
--
-- O teto de 1 (24/08/2026) era remedio contra DUPLICATA, nao contra cadencia:
-- a guarda de similaridade avisava em vez de bloquear, e das ~4.029 views do
-- kolejny-poziom ~3.100 vinham de cinco copias do mesmo short. Com a guarda
-- bloqueando na origem (ROTINA.md, secao FILA) o teto volta a 3.
--
-- O numero mora em DOIS lugares e os dois mudam juntos:
--   * fabrica/orquestra.py  -> MAX_POR_DIA_POR_CANAL
--   * esta view             -> pode_produzir
-- Deixar so no prompt faria a regra valer apenas quando alguem produz a mao;
-- quem despacha sozinho e o `proximo`, pelo diario.yml (aprendizado 452).
--
-- Aplicada em producao (vevocauwtarctfwngrch) em 08/09/2026 via
-- apply_migration; este arquivo existe para o historico em git.

create or replace view v_maquina_fila as
 SELECT c.slug,
    c.nome,
    c.idioma,
    c.nicho,
    c.voz,
    c.estilo,
    c.youtube_channel_id IS NOT NULL AS no_youtube,
    (( SELECT count(DISTINCT COALESCE(v.pacote, regexp_replace(v.slug, '-short$'::text, ''::text))) AS count
           FROM videos v
          WHERE v.canal = c.slug AND (v.status <> ALL (ARRAY['erro'::text, 'cancelado'::text]))))::integer AS pacotes,
    c.ultimo_pacote_em,
    c.trilha,
    c.fonte,
    c.duracao_alvo_s,
    c.nicho_mediana_vd,
    c.nicho_medido_em,
    ( SELECT count(DISTINCT COALESCE(v.pacote, regexp_replace(v.slug, '-short$'::text, ''::text))) AS count
           FROM videos v
          WHERE v.canal = c.slug AND (v.status <> ALL (ARRAY['erro'::text, 'cancelado'::text])) AND v.criado_em > (now() - '24:00:00'::interval)) AS pacotes_24h,
    ( SELECT count(DISTINCT COALESCE(v.pacote, regexp_replace(v.slug, '-short$'::text, ''::text))) AS count
           FROM videos v
          WHERE v.canal = c.slug) AS pacotes_registrados,
    c.youtube_channel_id IS NOT NULL AND COALESCE((t.valor ->> 'token_vivo'::text) <> 'false'::text, true) AND (( SELECT count(DISTINCT COALESCE(v.pacote, regexp_replace(v.slug, '-short$'::text, ''::text))) AS count
           FROM videos v
          WHERE v.canal = c.slug AND (v.status <> ALL (ARRAY['erro'::text, 'cancelado'::text])) AND v.criado_em > (now() - '24:00:00'::interval))) < 3 AS pode_produzir,
    COALESCE((t.valor ->> 'token_vivo'::text) <> 'false'::text, true) AS token_vivo,
    (t.valor ->> 'token_testado_em'::text)::timestamp with time zone AS token_testado_em
   FROM canais c
     LEFT JOIN config t ON t.chave = ('yt_token_'::text || c.slug)
  WHERE c.ativo
  ORDER BY (c.youtube_channel_id IS NULL), (COALESCE((t.valor ->> 'token_vivo'::text) <> 'false'::text, true) IS FALSE), c.ultimo_pacote_em NULLS FIRST;
