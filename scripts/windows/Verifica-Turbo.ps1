<#
================================================================================
 VERIFICA-TURBO v1.0 - Confere as otimizacoes do Turbo-Lenovo
================================================================================
 Mostra uma tabela DE -> PARA com cada item, o valor esperado, o valor atual
 e o status (OK / PENDENTE / -). Nao altera nada: apenas le e reporta.
 Executar como Administrador.
================================================================================
#>

#Requires -Version 5.1

$ErrorActionPreference = 'SilentlyContinue'

function Test-Admin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}
if (-not (Test-Admin)) {
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

$itens = New-Object System.Collections.Generic.List[object]

function Add-Check {
    param([string]$Area,[string]$Item,[string]$De,[string]$Para,[string]$Atual,[bool]$Ok)
    $itens.Add([pscustomobject]@{
        Area   = $Area
        Item   = $Item
        DE     = $De
        PARA   = $Para
        Atual  = $Atual
        Status = if ($Ok) { 'OK' } else { 'PENDENTE' }
    })
}

function Get-Reg { param($p,$n) (Get-ItemProperty -Path $p -Name $n -ErrorAction SilentlyContinue).$n }

Clear-Host
Write-Host ''
Write-Host '  =====================================================' -ForegroundColor DarkCyan
Write-Host '   VERIFICA-TURBO  -  conferencia das otimizacoes' -ForegroundColor Cyan
Write-Host '  =====================================================' -ForegroundColor DarkCyan
Write-Host ''
Write-Host '  Lendo o estado atual do sistema...' -ForegroundColor Gray

# ---------------- ENERGIA ----------------
$plano = (powercfg /getactivescheme) -join ' '
Add-Check 'Energia' 'Plano ativo' 'Equilibrado (padrao)' 'TURBO-LENOVO' `
    $(if ($plano -match 'TURBO-LENOVO') {'TURBO-LENOVO'} else {($plano -replace '.*\((.*)\).*','$1')}) `
    ($plano -match 'TURBO-LENOVO')

$overlay = (powercfg /overlaygetactivescheme 2>$null) -join ' '
Add-Check 'Energia' 'Modo de energia Win11' 'Padrao' 'Melhor desempenho' `
    $(if ($overlay -match 'max') {'Melhor desempenho'} else {'Padrao'}) ($overlay -match 'max')

# ---------------- MEMORIA ----------------
$mm = Get-MMAgent
Add-Check 'Memoria' 'Compressao de memoria' 'Variavel' 'Ativada' `
    $(if ($mm.MemoryCompression) {'Ativada'} else {'Desativada'}) ([bool]$mm.MemoryCompression)

$sys = Get-Service SysMain
Add-Check 'Memoria' 'SysMain (prefetch)' 'Automatico' 'Desativado' `
    "$($sys.StartType)/$($sys.Status)" ($sys.StartType -eq 'Disabled')

$cs = Get-CimInstance Win32_ComputerSystem
$pf = Get-CimInstance Win32_PageFileSetting | Select-Object -First 1
$pfTxt = if ($cs.AutomaticManagedPagefile) {'Gerenciado pelo Windows'}
         elseif ($pf) {"Fixo $($pf.InitialSize)-$($pf.MaximumSize) MB"}
         else {'Manual'}
Add-Check 'Memoria' 'Pagefile' 'Gerenciado (variavel)' 'Fixo (1x-2x RAM)' $pfTxt (-not $cs.AutomaticManagedPagefile)

# ---------------- INTERFACE ----------------
$tr = Get-Reg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' 'EnableTransparency'
Add-Check 'Interface' 'Transparencia' 'Ligada' 'Desligada' `
    $(if ($tr -eq 0) {'Desligada'} else {'Ligada'}) ($tr -eq 0)

$anim = Get-Reg 'HKCU:\Control Panel\Desktop\WindowMetrics' 'MinAnimate'
Add-Check 'Interface' 'Animacoes de janela' 'Ligadas' 'Desligadas' `
    $(if ($anim -eq '0') {'Desligadas'} else {'Ligadas'}) ($anim -eq '0')

$menu = Get-Reg 'HKCU:\Control Panel\Desktop' 'MenuShowDelay'
Add-Check 'Interface' 'Atraso de menu' '400 ms' '0 ms' "$menu ms" ($menu -eq '0')

$wid = Get-Reg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' 'TaskbarDa'
Add-Check 'Interface' 'Widgets na barra' 'Ligados' 'Desligados' `
    $(if ($wid -eq 0) {'Desligados'} else {'Ligados'}) ($wid -eq 0)

# ---------------- SEGUNDO PLANO ----------------
$bg = Get-Reg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications' 'GlobalUserDisabled'
Add-Check 'Segundo plano' 'Apps UWP em background' 'Liberados' 'Bloqueados' `
    $(if ($bg -eq 1) {'Bloqueados'} else {'Liberados'}) ($bg -eq 1)

$dvr = Get-Reg 'HKCU:\System\GameConfigStore' 'GameDVR_Enabled'
Add-Check 'Segundo plano' 'Xbox GameDVR' 'Ligado' 'Desligado' `
    $(if ($dvr -eq 0) {'Desligado'} else {'Ligado'}) ($dvr -eq 0)

$dt = Get-Service DiagTrack
Add-Check 'Segundo plano' 'DiagTrack (telemetria)' 'Automatico' 'Desativado' `
    "$($dt.StartType)/$($dt.Status)" ($dt.StartType -eq 'Disabled')

$sil = Get-Reg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' 'SilentInstalledAppsEnabled'
Add-Check 'Segundo plano' 'Apps promovidos' 'Instalam sozinhos' 'Bloqueados' `
    $(if ($sil -eq 0) {'Bloqueados'} else {'Liberados'}) ($sil -eq 0)

# ---------------- DISCO ----------------
$la = (fsutil behavior query DisableLastAccess) -join ' '
Add-Check 'Disco' 'Carimbo ultimo acesso' 'Ligado (escritas extras)' 'Desligado' `
    $(if ($la -match '=\s*1') {'Desligado'} else {'Ligado'}) ($la -match '=\s*1')

$ssOn = Get-Reg 'HKCU:\Software\Microsoft\Windows\CurrentVersion\StorageSense\Parameters\StoragePolicy' '01'
Add-Check 'Disco' 'Sensor de Armazenamento' 'Desligado' 'Ligado' `
    $(if ($ssOn -eq 1) {'Ligado'} else {'Desligado'}) ($ssOn -eq 1)

# ---------------- SEGURANCA (deve estar INTACTA) ----------------
$def = Get-Service WinDefend
Add-Check 'Protegido' 'Windows Defender' 'Ativo' 'Ativo (preservado)' "$($def.Status)" ($def.Status -eq 'Running')
$wu = Get-Service wuauserv
Add-Check 'Protegido' 'Windows Update' 'Disponivel' 'Disponivel (preservado)' "$($wu.StartType)" ($wu.StartType -ne 'Disabled')
$ws = Get-Service WSearch
Add-Check 'Protegido' 'Windows Search' 'Disponivel' 'Disponivel (preservado)' "$($ws.StartType)" ($ws.StartType -ne 'Disabled')

# ---------------- TABELA ----------------
Write-Host ''
$itens | Format-Table Area, Item, DE, PARA, Atual, Status -AutoSize | Out-Host

$ok  = @($itens | Where-Object Status -eq 'OK').Count
$tot = $itens.Count
$pend = $tot - $ok

Write-Host '  =====================================================' -ForegroundColor DarkCyan
Write-Host ("   RESULTADO: {0} de {1} itens aplicados  ({2} pendente(s))" -f $ok, $tot, $pend) `
    -ForegroundColor $(if ($pend -eq 0) {'Green'} elseif ($pend -le 3) {'Yellow'} else {'Red'})
Write-Host '  =====================================================' -ForegroundColor DarkCyan

# ---------------- RECURSOS AGORA ----------------
$os  = Get-CimInstance Win32_OperatingSystem
$vol = Get-Volume -DriveLetter $env:SystemDrive.TrimEnd(':')
Write-Host ''
Write-Host '  RECURSOS NESTE MOMENTO:' -ForegroundColor Yellow
Write-Host ("    RAM livre       : {0} MB  (uso {1}%)" -f `
    [math]::Round($os.FreePhysicalMemory/1KB,0), `
    [math]::Round(100 - (100 * $os.FreePhysicalMemory / $os.TotalVisibleMemorySize),1))
Write-Host ("    Processos       : {0}" -f (Get-Process).Count)
Write-Host ("    Servicos ativos : {0}" -f (Get-Service | Where-Object Status -eq 'Running').Count)
Write-Host ("    Disco livre     : {0} GB de {1} GB" -f `
    [math]::Round($vol.SizeRemaining/1GB,1), [math]::Round($vol.Size/1GB,1))

# salva copia em arquivo
$dir = "$env:SystemDrive\Turbo-Lenovo\Relatorios"
if (Test-Path $dir) {
    $arq = Join-Path $dir ("Verificacao-{0}.txt" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
    $itens | Format-Table Area, Item, DE, PARA, Atual, Status -AutoSize | Out-String -Width 200 |
        Out-File $arq -Encoding UTF8
    Write-Host ''
    Write-Host "  Copia salva em: $arq" -ForegroundColor Cyan
}

Write-Host ''
if ($pend -gt 0) {
    Write-Host '  Itens PENDENTES: rode a opcao correspondente no Turbo-Lenovo.ps1.' -ForegroundColor Yellow
    Write-Host '  Obs.: pagefile e SysMain so mudam de status apos REINICIAR o Windows.' -ForegroundColor Yellow
}
Write-Host ''
Read-Host '  Pressione ENTER para sair' | Out-Null
