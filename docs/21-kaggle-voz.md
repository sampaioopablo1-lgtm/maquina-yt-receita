# Kaggle como GPU gratuita para a voz clonada

## Por que Kaggle e nao outra coisa

O aprendizado **#152** mediu o Chatterbox Multilingual na CPU do runner do
Actions: **319 s de CPU para 13,58 s de audio = 23,5x o tempo real**. Nesse
fator um longo de 12:44 custa 5 h de job, e a frota de treze canais custaria
**116.619 min/mes** contra os 2.000 do teto gratuito de repositorio privado —
58x acima. A licenca MIT do Chatterbox nunca foi o obstaculo; o obstaculo e
computacional.

Em GPU o mesmo modelo roda perto de **1x o tempo real**. A conta que interessa:

| | valor |
|---|---|
| Cota gratuita do Kaggle | **30 h/semana** de GPU (T4 x2 ou P100) |
| Audio que a frota precisa | ~13,7 h/semana (63 longos de ~13 min) |
| Folga | **~2,2x** |

Cabe. E e a unica rota que fecha a conta sem dinheiro — a alternativa medida era
GPU alugada a ~US$ 40/mes, descartada pela restricao de custo zero.

> **Rode o modo `bench` antes de qualquer outra coisa.** Ele repete o
> experimento do `voz-clone.yml` com as MESMAS oito frases e devolve o fator
> real em T4. Todo o resto desta pagina depende do "~1x" ser verdade no
> hardware que voce de fato conseguir; enquanto esse numero nao existir, ele e
> estimativa e nao medicao.

## Configuracao, passo a passo

### 1. Conta e verificacao por telefone

Crie a conta em kaggle.com e va em **Settings → Phone Verification**.

Isto nao e opcional e nao e burocracia: **sem telefone verificado a conta nao
tem acelerador de GPU nem acesso a internet no notebook**. Sem GPU o script
aborta de proposito; sem internet ele nao baixa o modelo nem a referencia, e
nao consegue devolver nada ao Storage.

### 2. Token da API

O Kaggle tem DOIS formatos na mesma pagina (`kaggle.com/settings/api`), e
confundi-los faz a CLI falhar sem dizer por que:

**Atual — `Generate New Token`.** Devolve um token unico no formato
`KGAT_...`, sem username. A pagina mostra as duas formas de instalar:

```bash
export KAGGLE_API_TOKEN=KGAT_...            # por variavel de ambiente
# ou, para a CLI achar sozinha:
mkdir -p ~/.kaggle && echo KGAT_... > ~/.kaggle/access_token && chmod 600 ~/.kaggle/access_token
pip install kaggle
kaggle kernels list --mine                   # confirma que autenticou
```

**Legado — secao `Legacy API`, mais abaixo.** Baixa um `kaggle.json` com
`username` e `key`, que vai para `~/.kaggle/kaggle.json` com `chmod 600` (a CLI
recusa o arquivo se estiver com permissao aberta). Equivale as variaveis
`KAGGLE_USERNAME` e `KAGGLE_KEY`. Ainda funciona; nao gere um se ja tiver o
token novo.

> **O token e uma senha, e ele aparece na tela uma vez so.** Nao mande print
> dessa janela para lugar nenhum — chat, issue, commit. Se o valor vazou, o
> conserto e apagar o token pelos tres pontinhos na lista e gerar outro; nao ha
> como "despublicar" um segredo. Vazou em 2026-08-12 exatamente assim, num
> print da tela de criacao.

### 3. O segredo do Supabase — por dataset, nao por Secret

Os **Secrets do Kaggle** (Add-ons → Secrets) resolvem o problema mas nao tem
rota de API: so se cadastram clicando, e por kernel. Isso quebraria a automacao
toda vez que um kernel novo aparecesse.

Um **dataset privado** faz o mesmo e tem API. Ja criado:

```bash
# so para referencia — ja existe como pablosampaio/maquina-yt-config
kaggle datasets create -p <dir com config.json e dataset-metadata.json>
kaggle datasets version -p <dir> -m "gira a chave"   # para atualizar depois
```

O kernel declara `"dataset_sources": ["pablosampaio/maquina-yt-config"]` e le
`/kaggle/input/maquina-yt-config/config.json`. O script tenta dataset, depois
Secret, depois segue sem chave — nessa ordem.

> So a chave **anon** entra ai. Ela e desenhada para ser publica (o Supabase a
> manda para o navegador; quem protege e o RLS), entao dataset privado e folgado
> para ela. `service_role` NUNCA.

### 3b. Nada disso precisa da sua mao

O token do Kaggle vive em `config.kaggle_token` no Supabase, na mesma tabela
dos `yt_token_<canal>` e com o mesmo RLS de service_role. O workflow
`.github/workflows/kaggle-voz.yml` le de la, publica o kernel, acompanha,
busca a saida e devolve tudo ao Storage:

```
Actions → "Kaggle — clonagem de voz em GPU" → Run workflow
  modo: bench (mede o fator) | fila (narra voz/fila.json)
```

Segredo em dois lugares e segredo que envelhece em um deles — por isso o token
nao virou secret do repositorio. Girar o token e um `UPDATE` na tabela, sem
tocar em Settings do GitHub.

### 4. Publicar e rodar o kernel

Os arquivos ja estao no repositorio em `kaggle/voz-clone/`. Troque
`SEU_USUARIO` no `kernel-metadata.json` pelo seu username do Kaggle e:

```bash
cd kaggle/voz-clone
kaggle kernels push -p .

# acompanhar
kaggle kernels status SEU_USUARIO/voz-clone-chatterbox

# baixar a saida quando terminar
kaggle kernels output SEU_USUARIO/voz-clone-chatterbox -p ./saida
```

O `kernel-metadata.json` ja pede `enable_gpu: true` e `enable_internet: true`.
O script tambem devolve tudo direto ao Storage (`voz/bench/`), entao o
`kernels output` e conferencia, nao a rota principal.

### 5. Limites que mordem

| limite | valor | consequencia |
|---|---|---|
| GPU | 30 h/semana, reseta semanalmente | planeje o lote |
| Sessao | ate 12 h por execucao | um lote gigante nao cabe num job so |
| Ociosidade | sessao interativa morre sozinha | use `push` (headless), nao o editor |
| Saida | `/kaggle/working` | so o que estiver la volta pelo `kernels output` |

## O risco que voce assume

O Kaggle e uma plataforma de ciencia de dados, e a cota de GPU existe para
trabalho feito **na** plataforma. Usar os notebooks como fazenda de computacao
para um pipeline comercial externo fica fora do uso pretendido. Nao e uma zona
claramente proibida como mineracao de cripto, que os termos vedam por escrito,
mas tambem nao e o uso previsto — e a penalidade possivel e o banimento da
conta.

Duas consequencias praticas, e a segunda importa mais que a primeira:

1. Se banirem, some a GPU gratuita e a voz clonada volta para o plano B
   (edge-tts na frota, voz clonada so nos canais pt-BR).
2. **Use uma conta Google separada da que administra os canais.** O Kaggle
   loga com Google. Um banimento no Kaggle nao deveria alcancar o YouTube, mas
   nao ha razao para amarrar a conta que sustenta treze canais monetizados a
   uma aposta de termos de uso. Isolar custa um cadastro.

A decisao e sua; o que esta escrito aqui e para que ela seja tomada com o risco
a vista, e nao descoberto depois.

## Plano B, se nao valer a pena

Ja medido e disponivel, sem Kaggle nenhum:

- **edge-tts na frota inteira** — gratuito, sem GPU, voz neural por canal. E o
  que roda hoje. Limite: so tres vozes pt-BR existem (Antonio, Francisca,
  ThalitaMultilingual) e o portfolio tem quatro canais pt-BR, entao o
  `sx-educacao` colide com o `nivel-do-jogo`.
- **Voz clonada so na abertura** — os primeiros 30-45 s, que e onde a retencao
  se decide. Custa ~1 min de CPU por video no fator atual, cabe no Actions sem
  GPU nenhuma.
