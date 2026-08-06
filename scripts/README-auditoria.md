# Gravar o vídeo da auditoria — o que rodar na sua máquina

Dois arquivos, um comando. Não precisa instalar o projeto da máquina.

| arquivo | para que serve |
|---|---|
| `auditoria_demo.py` | faz o login OAuth e o upload de teste |
| `demo_upload.mp4` | clipe de 6 s para subir na demonstração |

## 1. Instalar o Python (uma vez)

[python.org/downloads](https://www.python.org/downloads/) → baixar → **marcar
"Add python.exe to PATH"** na primeira tela do instalador → Install Now.

Conferir, no Prompt de Comando: `python --version`

## 2. Instalar as duas bibliotecas (uma vez)

```
pip install google-auth-oauthlib google-api-python-client
```

## 3. Ensaiar (sem gravar)

```
python auditoria_demo.py client_secret_XXXX.json
```

Abre o navegador, mostra a tela de consentimento, e ao final imprime o nome e o
id do canal. Serve para descobrir problema **antes** de apertar o gravador.

Deu certo? Apague o `token.json` que ele criou. Sem isso a gravação não mostra
a tela de consentimento — ele reaproveita o login e pula direto.

## 4. Gravar

Ligue o gravador de tela e rode:

```
python auditoria_demo.py client_secret_XXXX.json demo_upload.mp4
```

O roteiro do que enquadrar está em `docs/18-submissao-auditoria.md`, seção 2.

## Por que o upload sai privado

Enquanto o projeto não está auditado, o YouTube força privado em tudo que entra
por `videos.insert`. O vídeo da demonstração mostra exatamente a limitação que a
auditoria remove — e por isso o script pede privado de forma explícita, em vez
de parecer que a regra de publicar em público foi contrariada.
