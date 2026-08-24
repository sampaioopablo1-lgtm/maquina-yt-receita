# Turbo-Lenovo v2.0

Otimizador adaptativo de Windows 10/11 em um único `.ps1`, calibrado com o
diagnóstico real da máquina (Lenovo IdeaPad 3 15IGL05 / 82BU — Celeron N4020,
4 GB DDR4 2400, SSD 128 GB, UHD 600, Windows 11 build 26200).

## Como rodar

1. Baixe `Turbo-Lenovo.ps1` para a máquina Windows.
2. Abra o PowerShell **como Administrador**.
3. Execute:

```powershell
Set-ExecutionPolicy -Scope Process Bypass -Force
cd C:\caminho\onde\salvou
.\Turbo-Lenovo.ps1
```

Modos não interativos:

```powershell
.\Turbo-Lenovo.ps1 -Auto    # executa o MODO TURBO inteiro sem menu
.\Turbo-Lenovo.ps1 -Undo    # desfaz tudo que o script alterou
```

Se não estiver elevado, o script se reabre pedindo elevação sozinho.

## O que mudou em relação à v1

A v1 basicamente imprimia hardware e mexia em energia e TRIM. Ela não tocava
em nada que realmente limita uma máquina de 2 threads e 4 GB.

| Área | v1 | v2 |
|---|---|---|
| Energia | ativava *Ultimate Performance* mesmo em notebook | plano próprio `TURBO-LENOVO`, agressivo na tomada e conservador na bateria; piso de CPU em 50% na tomada para o N4020 sair do 800 MHz |
| Memória | nada | compressão de memória, pagefile **fixo** dimensionado pela RAM e pelo tamanho do disco, SysMain desligado só quando faz sentido (SSD + 4 GB) |
| Interface | nada | animações, transparência (mica/acrylic), Aero Peek e Widgets desligados — alívio direto na UHD 600, que usa a RAM do sistema |
| Segundo plano | nada | apps UWP em background, Xbox Game Bar/GameDVR, instalação silenciosa de apps promovidos, telemetria em "Básico", tarefas CEIP/Appraiser |
| Disco | TRIM sempre no `C:` | TRIM só em SSD, desfrag só em HDD, `DisableLastAccess`, hiberfil reduzido em disco < 256 GB, Storage Sense sem tocar em Downloads |
| Limpeza | temp + DISM | temp, prefetch, thumbcache, INetCache, CrashDumps, cache do Windows Update, WER, Delivery Optimization, WinSxS — com medição do espaço liberado |
| Inicialização | só listava | lista classificando em MANTER / AVALIAR / REMOVER e desativa apenas o que você escolher, de forma reversível |
| Rollback | `reg import` de dois ramos | `Backup\rollback.json` com o valor anterior de **cada** chave, serviço, tarefa, plano de energia, pagefile e item de startup; reversão em ordem inversa |
| Medição | nenhuma | snapshot antes/depois (RAM livre, processos, serviços, itens de startup, disco livre, tempo do último boot) |
| Robustez | `$ErrorActionPreference = SilentlyContinue` mascarando tudo | cada etapa isolada em `Invoke-Step`, erros aparecem sem derrubar o resto |

## O que o script não faz, de propósito

- Não faz overclock nem undervolt.
- Não desativa Windows Defender, Windows Update, BITS, WMI, RPC, áudio,
  Bluetooth, spooler de impressão nem o Windows Search.
- Não remove aplicativos do Windows nem apaga arquivos pessoais
  (Documentos, Imagens, Downloads, Área de Trabalho e Lixeira ficam intactos).
- Não impõe DNS de terceiros nem altera MTU no chute.

## Onde ficam os arquivos

```
C:\Turbo-Lenovo\
  Backup\rollback.json        estado anterior de tudo que foi alterado
  Relatorios\Diagnostico.txt  hardware detectado
  Relatorios\Relatorio-*.txt  antes/depois + recomendações
  Relatorios\Turbo-*.log      transcrição da sessão
```

## Limite honesto desta máquina

O maior ganho possível não está em software: são 4 GB em single channel. Se o
chassi tiver slot SODIMM livre, um pente adicional de DDR4-2400 resolve dois
gargalos de uma vez — dobra a RAM e ativa dual channel, que sozinho costuma
render 20–40% a mais na UHD 600, já que o gráfico integrado usa a memória do
sistema. O script informa isso no relatório quando detecta single channel.
