# Radar TI

Painel estático, um arquivo só (`index.html`), que lê uma planilha do Google a cada 15 minutos
direto no navegador de quem abre a página. Não há servidor nem chave de API no meio.

## Como a planilha precisa estar

Compartilhar → Acesso geral → **Qualquer pessoa com o link → Leitor**. Sem isso o Google responde
401 e o painel mostra o aviso com o passo a passo. "Publicar na web" não é necessário.

## Como ele lê

`https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&gid=0` (ou `&sheet=<nome da aba>`).
Esse endpoint devolve CSV com `Access-Control-Allow-Origin`, logo o `fetch` funciona de qualquer domínio.
Medido em 19/10/2026 contra a planilha "Rotina de Clientes – Tráfego, TI e CS" (200, `text/csv`, CORS ok)
e contra a planilha privada do pedido (401).

## O que ele monta

- cabeçalho = primeira linha com dois ou mais títulos (títulos mesclados acima são ignorados);
- cliente = coluna cujo título começa com `Cliente`, `Conta`, `Empresa`, `Loja`, `Marca` ou `Unidade`.
  Sem essa coluna e com várias abas, **cada aba é um cliente**;
- status = coluna com `Status`/`Situação`/`Estado`/`Etapa`. Concluído/resolvido/fechado conta como OK;
  atrasado/crítico/urgente/erro/falha/bloqueado conta como crítico; o resto é "em andamento";
- prazo = coluna `Prazo`/`Vencimento`/`Limite`/`Entrega`/`Previsão` (ou `Data`, em último caso).
  Prazo passado com status não concluído = atrasado. Sem coluna de status, data passada é histórico, não atraso;
- responsável = coluna `Responsável`/`Técnico`/`Analista`/`Quem`.

Tudo isso pode ser fixado no bloco `CONFIG` do arquivo, no botão **Ajustes** (fica só no navegador)
ou na URL: `?sheet=<ID>&abas=0,Chamados&cliente=Cliente&status=Status&prazo=Prazo`. A URL serve
para ter **um link por cliente**, apontando cada um para a planilha dele.

## Teste local

    python3 -m http.server 8765   # dentro de radar-ti/
    # abra http://127.0.0.1:8765/?sheet=<ID de uma planilha com leitura por link>
