-- 13/08/2026 — Usuário notou (solicitação de Camila) que havia pedido sem
-- nenhuma sugestão da API. Investigando: o gatilho `tg_solicitacao_captacao`
-- só dispara em INSERT — enfileira só solicitação NOVA. Das 1.592
-- solicitações na base, apenas 122 (o backfill manual de uma sessão
-- anterior) estavam na fila; 1.470 solicitações antigas, boa parte delas
-- ainda em atendimento ativo, nunca tinham entrado na rotina de captação
-- por API.
--
-- Backfill definitivo: toda solicitação nos status que o próprio gatilho já
-- reconhece como "em aberto" entra na fila agora, de uma vez, e fica
-- coberta por daqui pra frente pelo cron de 6 em 6 minutos (que já processa
-- até 10 sugestões por solicitação, migração captacao_meta_dez_sugestoes).

insert into public.captacao_fila_solicitacoes (solicitacao_id)
select s.id from public.solicitacoes s
where s.status in ('Trabalhando na busca do imóvel','Em Atendimento','Pendente','Aguardando Aprovação Pablo')
on conflict (solicitacao_id) do nothing;
