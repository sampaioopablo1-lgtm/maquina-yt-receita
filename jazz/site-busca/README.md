# Demo da busca por frase única

Página estática, um arquivo, sem build e sem dependência. Serve para mostrar a
UX da barra única antes do front real existir no Lovable — e para discutir os
dois pontos que a tela precisa acertar: os chips que mostram a interpretação da
frase, e o aviso de busca ampliada.

**As 14 fichas são de exemplo, escritas no próprio HTML.** Nenhuma é imóvel
real e a página não fala com o Supabase. O parser em JS é uma tradução das
regras de `fn_interpretar_busca()`
(`jazz/supabase/migrations/20260903_busca_natural_imoveis.sql`) — mesma ordem
de extração, mesmos sinônimos, mesmas convenções de escala. Ele existe só para
a demo rodar sem backend; a verdade é a do banco.

As ilustrações dos cards são SVG gerado a partir do código do imóvel, não fotos.

Publicada por `netlify.toml` na raiz (`publish = "jazz/site-busca"`), com
`noindex` no HTML: é demo interna, não é vitrine.

## Deploy

Projeto Netlify `jazz-busca-imoveis-demo` (time `imobjazz`), site id
`2cd91fbd-dcc8-4c47-ba14-6ce9f35eccf2` →
https://jazz-busca-imoveis-demo.netlify.app

Quem publica é `.github/workflows/jazz-site-busca.yml`, no push pra `main` que
toque esta pasta, ou por `workflow_dispatch`. **Não** tente deployar da máquina
de desenvolvimento: as sessões de desenvolvimento bloqueiam `api.netlify.com`
na política de egresso e o upload do CLI morre em 403 antes de falar com o
Netlify. O runner do Actions tem saída livre.

Falta um passo manual, uma vez: o segredo `NETLIFY_AUTH_TOKEN` no repositório
(Settings → Secrets and variables → Actions), com um Personal access token
criado em app.netlify.com → User settings → Applications. Sem ele o job para
no primeiro passo com mensagem explícita.
