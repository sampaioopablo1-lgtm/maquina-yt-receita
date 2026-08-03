# Conectar sua conta do YouTube

O objetivo: abrir uma janela do Google, escolher a conta, selecionar o canal,
pronto. **Essa janela existe** — é o `maquina auth-youtube`.

Antes dela existe um cadastro de ~5 minutos, feito **uma única vez**. Ele é
exigido pelo Google: a janela de permissão só aparece para aplicativos
registrados. Não há como pular.

## Parte 1 — Cadastro no Google (uma vez, ~5 min)

1. Acesse **console.cloud.google.com** e crie um projeto (nome livre).
2. Menu → **APIs e serviços** → **Biblioteca**.
   Busque **YouTube Data API v3** → **Ativar**.
3. Menu → **APIs e serviços** → **Tela de permissão OAuth**.
   - Tipo: **Externo**
   - Preencha nome do app e seu e-mail → Salvar
   - Em **Usuários de teste**, adicione o seu próprio Gmail
4. Menu → **Credenciais** → **Criar credenciais** → **ID do cliente OAuth**.
   - Tipo de aplicativo: **App para computador**
5. Baixe o JSON e salve como `secrets/client_secret.json` dentro do projeto.

> **Por que "Usuários de teste"?** Um app não publicado só autoriza contas
> listadas ali. Como este app é seu e só você usa, isso basta — não é preciso
> passar pela verificação do Google.

## Parte 2 — A janela (5 segundos)

```bash
maquina auth-youtube
```

Abre o navegador. Você:

1. Escolhe a conta Google
2. **Se aparecer uma lista de canais, selecione @SetiapLevelID**
3. Concede as permissões

O comando então mostra qual canal ficou autorizado:

```
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Canal autorizado ┃ Valor          ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Nome             │ Setiap Level   │
│ Handle           │ @SetiapLevelID │
│ Inscritos        │ 0              │
│ Vídeos           │ 0              │
└──────────────────┴────────────────┘
```

Se você autorizou o canal errado, o comando **avisa em vermelho e falha** —
em vez de deixar você descobrir depois que o vídeo subiu no lugar errado.

Para conferir a qualquer momento:

```bash
maquina canais
```

## Trocar de canal

Uma credencial controla **um** canal por vez. Para trocar:

```bash
rm secrets/youtube_token.json
maquina auth-youtube
```

E selecione outro canal na tela do Google.

## Para o GitHub Actions

Copie todo o conteúdo de `secrets/youtube_token.json` para o secret
**`YT_TOKEN_JSON`** do repositório (Settings → Secrets and variables → Actions).

Assim o robô publica sozinho, sem você logar de novo.

## Por que não é mais simples que isso

| Caminho | Precisa do cadastro? | Publica vídeo? |
|---|---|---|
| Este projeto | sim, 5 min uma vez | **sim** |
| Supermetrics e afins | não | **não** — só leem |
| Buffer, TubeBuddy e afins | não | sim, mas é app deles + mensalidade |

Ferramentas que "pulam" o cadastro usam o registro **delas** no Google. Isso
funciona para ler métricas, mas para publicar você acaba dentro do produto de
outra empresa, pagando por mês e sem controle do processo.

O cadastro de 5 minutos compra independência: o app é seu, a cota é sua, e
nenhuma empresa fica entre você e o canal.
