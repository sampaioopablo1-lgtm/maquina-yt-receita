# Links de consentimento — escopo de analytics incluido

Gerados em 09/10/2026 com `ESCOPOS` de QUATRO escopos.

## epomeno-epipedo e kolejny-poziom (o MESMO cliente, uma autorizacao para cada canal)

https://accounts.google.com/o/oauth2/v2/auth?client_id=777159180424-p853u21ksnlhgjd4s9d2f5bum9hllumo.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost&response_type=code&access_type=offline&prompt=consent&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyt-analytics.readonly

## labtreinamento (cliente PROPRIO — aprendizado 667)

https://accounts.google.com/o/oauth2/v2/auth?client_id=777159180424-92i647rjmnmkfjf3ojvvl3c2o6fok0t7.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost&response_type=code&access_type=offline&prompt=consent&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyt-analytics.readonly

## Como usar

1. Abra o link **uma vez por canal** e escolha a conta de marca daquele canal.
   O `epomeno-epipedo` e o `kolejny-poziom` usam o primeiro link (mesmo cliente
   OAuth, contas de marca diferentes). O `labtreinamento` usa o segundo, porque
   o cliente dele e outro — usar o global devolve `401 unauthorized_client` e
   depois `403 unregistered callers`, que parece token revogado e nao e (667).
2. A tela confirma QUATRO permissoes. A nova e a de ver as estatisticas do
   YouTube Analytics.
3. Depois de autorizar, o navegador tenta abrir `http://localhost` e mostra erro
   de conexao. **Isso e o esperado.** Copie a URL inteira da barra de endereco
   — ela carrega `?code=...`.
4. Mande as tres URLs. A troca do codigo NAO passa pelo `tokens.py trocar`,
   porque ele escreve pelo REST do Supabase e o REST esta em 402: eu faco a
   troca pelo `pg_net` e gravo em `config` por SQL.

## O que isso destrava

- Retencao e inscritos POR VIDEO, que e o que decide os experimentos 37 e 38 em
  horas em vez de dias.
- A conta que mais importa hoje: os 388 registros que ja existem dizem que o
  LONGO converte ~5x melhor por view que o short (6,22 contra 1,23 por mil).
  Com o escopo de volta isso passa a ser verificavel em vez de indicio.
