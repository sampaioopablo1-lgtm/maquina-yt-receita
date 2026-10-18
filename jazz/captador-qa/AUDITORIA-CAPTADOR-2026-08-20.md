# Pente fino do módulo do captador — 20/08/2026

Auditoria tela a tela, botão a botão, do módulo do captador do Jazz Conecta.

## Onde foi testado

**Produção real:** `https://jazz-lead-conecta.pablo-jazzimob.workers.dev`
(Worker do Cloudflare `jazz-lead-conecta`, última publicação 2026-08-03T16:50:30Z).

Foi criada uma conta de teste dedicada — `qa.captador@jazz.com` — em vez de usar
o login de alguém da equipe. Os testes de tela de admin foram feitos concedendo
o papel `admin` a essa conta temporariamente; **o papel foi removido ao fim**,
e nenhum dado real foi alterado pela conta de teste.

Telas percorridas: `/captador` (5 abas), `/captador/gestao`, `/captador/metas`,
`/captador/prospeccoes`, `/captador/recortes`, `/captador/minhas-captacoes`.

## Qual código está no ar (importante)

Havia três versões divergentes e o diagnóstico inicial estava errado. O correto,
verificado:

| Origem | Painel do captador | Relação com a produção |
|---|---|---|
| Worker do Cloudflare (`pablo-jazzimob.workers.dev`) | 3.985 linhas | **é a produção** |
| API de arquivos do Lovable (HEAD, commit `1d3234de`) | 3.985 linhas | **idêntica à produção** |
| `jazz-lead-conecta.lovable.app` | build ~20/07 | cópia velha, não é a produção |
| `origin/main` no GitHub | 2.369 linhas | **não contém o código de produção** |

Como foi confirmado que o Lovable HEAD é a produção: o menu do painel no Worker
tem exatamente 9 itens, sem "Operacional" nem "Modo TV" — que é o que o código
do Lovable diz (há um comentário registrando a remoção em 23/07). O
`jazz-lead-conecta.lovable.app` ainda mostra os dois, ou seja, é anterior a isso.

Como foi confirmado que o `main` não tem o código: as PRs **#1302, #1307,
#1311, #1316, #1317, #1319 e #1324** (31/07 a 03/08) estão todas ausentes de
`origin/main`, e o commit `1d3234de` não é alcançável a partir dele nem com o
histórico completo (1.724 commits).

**Consequência prática:** publicar a `main` por cima da produção hoje remove
~1.600 linhas do painel do captador e as correções de feed das PRs acima. O
único lugar gravável que chega ao Worker é o Lovable.

## Defeitos encontrados

### Graves

**1. O menu encolhe ao trocar de tela.**
As seis telas montam o array `nav` do `AppShell` à mão, cada uma com um
conjunto diferente. Ao ir do painel para a Gestão o captador perde Imóveis,
Chaves, Plantões, Minhas Captações e Ajuda; o admin perde também o item Admin.
`/captador` se chama "Tarefas" em três telas e "Painel" nas outras três.
A tela de metas é a única que ainda mostra "Operacional" e "Modo TV".
E **"Externas" (`/captador/prospeccoes`) não aparece no menu do painel
principal** — só dá para chegar lá vindo de Recortes ou Minhas Captações.
_Correção:_ `nav-captador.ts` (neste diretório), usado nas seis telas.

**2. Dois itens do menu acendem juntos.**
`AppShell.tsx` marca ativo com `pathname === to || pathname.startsWith(to + "/")`.
Como `/captador` é prefixo de `/captador/gestao`, em toda subtela "Tarefas" e
"Gestão" aparecem selecionados ao mesmo tempo.
_Correção:_ `indiceItemAtivo()` em `nav-captador.ts` — vence o `to` mais longo.

**3. "Nada aqui" aparece enquanto ainda está carregando.**
`/captador/recortes`, `/captador/prospeccoes` e `/captador/minhas-captacoes`
renderizam "Nenhum recorte ainda" / "Nenhuma oportunidade externa no momento" /
"Você ainda não marcou nenhum imóvel como captado" **antes de os dados
chegarem**, porque a lista vazia é o estado inicial. O captador lê que não tem
nada e sai da tela.
_Correção:_ trocar por `<ListSkeleton />` enquanto `lista.isLoading` — o
componente já existe e já é usado no `/captador`. Só mostrar o estado vazio
quando `!isLoading && !error && itens.length === 0`.

**4. Tela branca permanente quando a sessão falha.**
Cinco telas fazem `if (!me.data) return null`. Se `getCurrentUser()` falhar, a
página fica branca, sem mensagem e sem menu. `/captador/metas` é pior:
`if (!me.data || !q.data)` mostra "Carregando..." para sempre e **sem o
AppShell**, então não há como navegar para fora.
_Correção:_ enquanto carrega, renderizar o `AppShell` com esqueleto; em erro,
renderizar o `AppShell` com o cartão de erro (o padrão que
`captador.minhas-captacoes.tsx` já usa corretamente).

**5. Aceitar/Descartar não muda nada na tela de matches.**
Em `captador.prospeccoes.tsx` a mutação sempre invalida
`["minhas-prospeccoes"]`, mas quando a tela é aberta por Recortes → Matches
(`?recorte=<uuid>`) a lista vem de `["matches-recorte", recorte]`. O toast diz
"Atualizado" e o card continua igual.
_Correção:_ no `onSuccess`, invalidar as duas chaves — ou a que estiver em uso:

```ts
onSuccess: () => {
  toast.success("Atualizado");
  qc.invalidateQueries({ queryKey: ["minhas-prospeccoes"] });
  if (recorte) qc.invalidateQueries({ queryKey: ["matches-recorte", recorte] });
},
```

**6. O logotipo da Jazz está quebrado em todas as telas.**
`src/assets/jazz-logo.png.asset.json` aponta para
`/__l5e/assets-v1/6ebc267f-.../jazz-logo.png`, um caminho servido só pela
hospedagem do Lovable. No Worker do Cloudflare ele responde **404**. O PNG em si
não está no repositório — só o JSON com a URL. Atinge o `AppShell` (toda tela
autenticada), a tela de login `/auth`, a página pública `/solicitar` e as três
telas de TV.
_Correção:_ commitar o PNG de verdade em `src/assets/` e importá-lo pelo bundler
(`import jazzLogo from "@/assets/jazz-logo.png"`), em vez do JSON com URL externa.

### Médios

**7. O lançamento de meta cai no dia errado à noite.**
`captador.metas.tsx` usa `new Date().toISOString().slice(0, 10)`, que é UTC. No
horário de Brasília (UTC−3), das 21h às 23h59 o formulário já sugere o dia
seguinte, e as ligações da noite entram na data errada. A janela do mês exibida
tem o mesmo problema: medida com fuso `America/Sao_Paulo` ela aparece como
**31/07/2026 – 30/08/2026** em vez de 01/08 – 31/08.
_Correção:_ `hojeLocalISO()` em `nav-captador.ts`, e calcular a janela do mês a
partir da data local.

**8. Mesmo problema no nome do CSV da Gestão.**
`gestao-captacao-${new Date().toISOString().slice(0,10)}.csv` — à noite o
arquivo sai com a data de amanhã.

**9. A Gestão renderiza 1.029 linhas sem paginação.**
Medido ao vivo com a conta de admin: `table tbody tr` = 1.029, tudo numa tabela
só, sem paginação nem virtualização, com `refetchInterval: 60000` (e o ranking
do Vista a cada 30s) re-renderizando o conjunto inteiro.
_Correção:_ paginar (ou virtualizar) a tabela de solicitações.

**10. O filtro "Finalidade" não volta para "Qualquer".**
No diálogo de novo recorte o `Select` só tem "Venda" e "Locação" — confirmado ao
vivo. Depois de escolher uma, não há como voltar ao estado neutro sem fechar o
diálogo.
_Correção:_ item `"__qualquer__"` mapeando para `""`, como
`captador.gestao.tsx` já faz com `"__none__"`.

**11. O formulário de recorte não limpa ao cancelar.**
Cancelar só faz `setOpen(false)`. Reabrir mostra o que foi digitado antes —
confirmado ao vivo (o campo Cidade voltou com "Cidade QA").
_Correção:_ `setForm(FORM_VAZIO)` também no cancelar/fechar.

**12. `confirm()` nativo do navegador em dois pontos.**
`captador.recortes.tsx` (excluir recorte) e `captador.index.tsx` linha ~2835
("Marcar imóvel como CAPTADO"), enquanto o resto do módulo usa `ConfirmDialog`.
Além da inconsistência visual, `confirm()` é bloqueável pelo navegador.

**13. Botões não desabilitam durante o envio.**
Em `prospeccoes` (Aceitar/Contatei/Descartar), `recortes` (Switch e excluir) e
no formulário de lançamento de `metas`. Clique duplo envia duas vezes.
_Correção:_ `disabled={mut.isPending}` — o diálogo de novo recorte já faz isso
certo e serve de modelo.

**14. Senha padrão compartilhada pré-preenchida.**
"Cadastrar captador" vem com `Jazz@2025` no campo de senha, enquanto a tela de
login anuncia "Senha padrão: 123456". São duas senhas compartilhadas, ambas
públicas. _Correção sugerida:_ gerar senha aleatória por captador e obrigar a
troca no primeiro acesso.

**15. Pontas soltas.**
`colSpan={10}` na linha de "nenhuma solicitação" da Gestão, numa tabela de no
máximo 9 colunas; import morto de `Link` em `captador.metas.tsx`.

## O que passou

- **Zero erro de console ou de runtime** em todas as seis telas, nas cinco abas
  do painel, como captador e como admin. O único 404 é o do logotipo (defeito 6).
- As cinco abas funcionam, e `?tab=` inválido cai em `fila` sem quebrar
  (o `fallback` do zod está correto).
- O `errorComponent` da rota `/captador` funciona.
- Exportar CSV funciona (`gestao-captacao-2026-08-20.csv` baixado).
- Validação de "Cadastrar captador" funciona (nome e e-mail obrigatórios).
- Validação de preço mín/máx no recorte funciona ("Preço máximo deve ser ≥ mínimo").
- Controle de acesso funciona: a coluna Ações e o botão "Cadastrar captador"
  ficam ocultos para quem não é admin.
- Login e logout funcionam.

## Corrigido nesta rodada (fora do módulo)

O imóvel **44637** estava no XML dos portais com
`<VirtualTourLink>https://jazz-lead-conecta.lovable.app/api/public/tour/44637</VirtualTourLink>`,
endereço que hoje responde **404** — link de tour quebrado num anúncio
publicado. O campo `tour_360` continha o lixo `&quot;` e o gerador caía num
fallback para uma rota que não existe mais.

Corrigido rodando `fn_visita_publicar_no_feed()`; o imóvel passou a apontar para
a visita no Supabase. Auditoria dos anúncios ativos depois da correção:
**0 links quebrados, 0 valores inválidos, 0 apontando para a rota morta.**

## Bloqueio para aplicar as correções

O único caminho gravável que chega à produção é o Lovable, e **o workspace do
Lovable está sem créditos** — as mensagens de edição são recusadas.

Duas saídas:

1. **Recarregar créditos no Lovable** (caminho curto). As 15 correções entram em
   três mensagens e a publicação sai no mesmo dia.
2. **Recuperar o código de produção para o GitHub** (caminho longo). O código só
   existe no Worker publicado e na API de arquivos do Lovable; o bundle servido
   **não tem source maps** (verificado: `.map` responde 404 e não há
   `sourceMappingURL`), então a recuperação teria de ser feita arquivo a arquivo
   pela API do Lovable. Depois disso o deploy pelo GitHub volta a ser seguro.
