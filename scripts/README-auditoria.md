# Gravar o vídeo da auditoria — o mínimo a fazer na sua máquina

Quatro arquivos na mesma pasta, dois duplos-cliques.

| arquivo | o que é |
|---|---|
| `1-ENSAIO.bat` | duplo clique: testa o login. Não envia nada |
| `2-GRAVAR.bat` | duplo clique: é o que você grava |
| `auditoria_demo.py` | o programa (não precisa abrir) |
| `demo_upload.mp4` | clipe de 6 s que sobe na demonstração |

E, junto deles, o `client_secret_....json` baixado do Google Cloud.

Os `.bat` acham o `client_secret` sozinhos — não é preciso digitar o nome do
arquivo, que é longo e fácil de errar.

## Antes

Instalar o Python: [python.org/downloads](https://www.python.org/downloads/),
marcando **"Add python.exe to PATH"** na primeira tela do instalador. Se
esquecer disso, o `1-ENSAIO.bat` avisa e reabre a página.

## O ensaio

Duplo clique em **`1-ENSAIO.bat`**. Ele instala as bibliotecas na primeira vez,
abre o navegador, mostra a tela de consentimento e imprime o canal autenticado.

Serve para descobrir problema **antes** de ligar o gravador.

## A gravação

Ligue o gravador de tela e dê duplo clique em **`2-GRAVAR.bat`**. Ele apaga o
`token.json` antes de começar — sem isso o login guardado faria o script pular
a tela de consentimento, que é justamente o quadro que decide a auditoria.

Roteiro do que enquadrar: `docs/18-submissao-auditoria.md`, seção 2.

## Por que o upload sai privado

Enquanto o projeto não está auditado, o YouTube força privado em tudo que entra
por `videos.insert`. O script imprime isso na tela em inglês, de propósito: o
revisor lê o terminal no vídeo, e a limitação demonstrada ao vivo é o próprio
argumento do pedido.
