# Gravar o vídeo da auditoria

Um arquivo: **`auditoria.ps1`**. Baixar, botão direito, *Executar com o PowerShell*.

Ele carrega `auditoria_demo.py` e `demo_upload.mp4` dentro de si e grava os dois
na pasta Downloads. Não precisa baixar mais nada.

Se o Windows recusar (*"a execução de scripts foi desabilitada"*), abra o
PowerShell e cole:

```
Set-ExecutionPolicy -Scope Process Bypass -Force; & "$env:USERPROFILE\Downloads\auditoria.ps1"
```

## As duas opções

- **1 — ensaio.** Testa o login e mostra o canal. Não envia nada. Serve para
  achar problema antes de ligar o gravador.
- **2 — gravar.** Apaga o `token.json` antes de começar, senão o login guardado
  faz o script pular a tela de consentimento — o único quadro que decide a
  auditoria. Roteiro do que enquadrar: `docs/18-submissao-auditoria.md`, seção 2.

## Como o client secret é escolhido

Pelo **conteúdo**, não pelo nome. A pasta Downloads costuma ter o JSON de mais
de um projeto do Google Cloud, e o nome começa com o número do projeto — ordenar
por nome escolhe por acaso. Aconteceu: o cliente de outro projeto veio primeiro
e só falhou depois de instalar o Python e as bibliotecas.

O programa lê cada JSON, mantém só os que têm a chave `installed` (cliente de
app para computador; cliente Web tem `web`) e usa o mais recente.

## Por que o upload sai privado

Enquanto o projeto não está auditado, o YouTube força privado em tudo que entra
por `videos.insert`. O programa imprime isso em inglês na tela: o revisor lê o
terminal no vídeo, e a limitação demonstrada ao vivo é o próprio argumento do
pedido.

## Manutenção

Nunca edite `auditoria.ps1` — ele é gerado. Mude `auditoria_demo.py` ou
`auditoria.ps1.molde` e rode `python3 gerar_ps1.py`.
