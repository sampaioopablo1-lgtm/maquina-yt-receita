# Calibração da régua de qualificação — F-28

Gerado por `wesales/tools/calibracao_regua.py`. Não escreve no CRM — só
leitura. Sobrescrito a cada rodada; não edite à mão.

**Nota de proveniência (só nesta primeira geração):** esta sessão não tem
`GHL_TOKEN` no ambiente (roda em nuvem, sem PIT configurado) — os mesmos
dados foram lidos com as ferramentas MCP desta sessão
(`opportunities_search-opportunity` + `contacts_get-contact`, um a um nas 4
oportunidades das etapas `REUNIÃO DE DIAGNÓSTICO`/`NEGOCIAR`/`FORMALIZAR`) e
passados a mão pela mesma lógica do script (`eh_teste`, `calibrar`,
`formatar_md`). Uma execução futura com `GHL_TOKEN` roda o script direto e
substitui esta nota.

Gerado em: 2026-09-28T06:11:51Z

## Amostra

| Faixa | Vereditos | "Sim" | Taxa |
|---|---|---|---|
| A (>=70) | 0 | 0 | — |
| B (45-69) | 0 | 0 | — |
| C (25-44) | 0 | 0 | — |
| D (<25) | 0 | 0 | — |

**Zero vereditos reais ainda — não é falha do script, é o estado real da
subconta em 28/09/2026.** Nenhum lead qualquer chegou a `FORMALIZAR`; os dois
leads reais em `NEGOCIAR` (`Daniel`, `Genilson | Bombeiro`, ambos nota 93)
ainda não têm `Reunião foi qualificada` preenchida pelo closer. O único
veredito que existe na subconta hoje (`Reunião foi qualificada` = `Sim`,
nota 23) é do contato de teste "9940" (`Pablo Sampaio`,
`rdaijzR0ZVCmXLAJ6jT2`), usado pelo dono para testar o `build_estagnacao.py`
(G-23, `ROADMAP-SALES-ENGAGEMENT.md`) — corretamente excluído da amostra.
Contando esse veredito de teste como real, a leitura mentiria já na primeira
rodada: nota 23 (faixa D) com veredito `Sim` pareceria o pior caso possível
de descalibração, quando é só dado de teste.

## Casos que já dispararam (ou deveriam disparar) o alerta de calibração do 5.1

Nenhum, nesta leitura.

## Excluídos por serem contato de teste

Pablo Sampaio, Teste Atendeu

## Em `REUNIÃO`/`NEGOCIAR`/`FORMALIZAR` sem veredito do closer ainda

Daniel, Genilson | Bombeiro
