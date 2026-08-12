# Schema Supabase — maquina-yt-dark (vevocauwtarctfwngrch)

> Consulte este arquivo antes de qualquer INSERT/UPDATE para evitar queries de descoberta
> que custam créditos. Atualizar quando alterar tabelas.
> Última revisão: 2026-08-10.

---

## config

| coluna | tipo | notas |
|---|---|---|
| chave | text | PK |
| valor | text | |
| atualizado_em | timestamptz | |

Chaves relevantes: `api_auditada` (true/false/nao_se_aplica).

---

## aprendizados

| coluna | tipo | notas |
|---|---|---|
| id | int | gerado |
| criado_em | timestamptz | gerado |
| atualizado_em | timestamptz | gerado |
| categoria | text | **enum** — ver abaixo |
| titulo | text | |
| regra | text | |
| evidencia | **jsonb** | objeto JSON, não string |
| origem | text | |
| severidade | text | critico · alto · medio · baixo |
| confianca | text | |
| status | text | ativo · invalidado |
| aplicado_em | timestamptz | |
| revisar_em | timestamptz | |
| invalidado_motivo | text | |

**Categorias válidas** (constraint CHECK):
`pauta` · `roteiro` · `producao` · `render` · `entrega` · `distribuicao` · `processo`

Exemplo de insert:
```sql
INSERT INTO aprendizados (titulo, regra, evidencia, origem, categoria, severidade, status, aplicado_em)
VALUES (
  'Titulo aqui',
  'Regra aqui',
  '{"chave": "valor"}'::jsonb,
  'fonte',
  'distribuicao',   -- usar uma das categorias validas
  'critico',
  'ativo',
  NOW()
);
```

---

## experimentos

| coluna | tipo | notas |
|---|---|---|
| id | int | gerado |
| criado_em | timestamptz | gerado |
| canal | text | slug do canal |
| slug | text | identificador único |
| variavel | text | o que está sendo testado |
| hipotese | text | |
| valor | text | variante testada |
| controle | text | baseline comparado |
| metrica_alvo | text | |
| resultado | text | preenchido ao fechar |
| status | text | em_andamento · concluido |
| fechado_em | timestamptz | |

---

## videos

Colunas principais (para INSERT após upload):

| coluna | tipo |
|---|---|
| canal | text |
| youtube_id | text |
| titulo | text |
| duracao_real | int (segundos) |
| fonte_pauta | text |
| supabase_url | text |
| drive_longo | text |
| drive_short | text |
| cenas | int |
| capitulos | int |
| publicado_em | timestamptz |
| erro | text (nullable) |

---

## Views relevantes

```sql
select * from v_maquina_regras where severidade in ('critico','alto');
select * from v_maquina_pendencias limit 1;   -- erros com artefato recuperavel
select * from v_maquina_fila limit 1;         -- proximo canal a produzir
select * from v_maquina_formatos;             -- formatos por canal
```
