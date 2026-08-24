<#
================================================================================
 TURBO-LENOVO v2.0 - Otimizador adaptativo para Windows 10/11
================================================================================
 Calibrado a partir do diagnostico real da maquina:
   Lenovo IdeaPad 3 15IGL05 (82BU)
   Intel Celeron N4020 (2 nucleos / 2 threads, Gemini Lake, TDP 6W)
   4 GB DDR4 2400 (single channel, soldada)
   SSD SSSTC CL1-4D128 (119 GB)
   Intel UHD Graphics 600
   Windows 11 Home Single Language 10.0.26200

 PRINCIPIOS
   - Nada de overclock, nada de undervolt, nada de driver de terceiro.
   - Windows Defender, Windows Update, rede, som, impressao e Bluetooth
     permanecem intactos.
   - Cada alteracao de registro/energia e gravada em um JSON de backup e
     pode ser desfeita pela opcao [R].
   - As decisoes sao tomadas em cima do hardware detectado em tempo de
     execucao, nao de valores fixos.

 O QUE REALMENTE MOVE O PONTEIRO NESTA CLASSE DE MAQUINA
   1. RAM: 4 GB e o gargalo numero um. Compressao de memoria + pagefile fixo
      + corte de apps em segundo plano evitam o swap constante no SSD.
   2. CPU: 2 threads sem SMT. Cada servico/tarefa em background rouba metade
      da maquina. Cortar telemetria, GameDVR, Widgets e indexacao ampla vale
      mais que qualquer "tweak" de energia.
   3. Energia: o N4020 so entrega os 2.8 GHz de turbo se o plano nao o
      prender no minimo. Plano proprio, agressivo na tomada e conservador na
      bateria.
   4. Disco: 119 GB enchem rapido. Espaco livre < 10% derruba o SSD e o
      pagefile. Limpeza + hiberfil reduzido + Storage Sense.
================================================================================
#>

#Requires -Version 5.1

[CmdletBinding()]
param(
    [switch]$Auto,      # executa o modo turbo sem menu
    [switch]$Undo       # desfaz e sai
)

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'

# ==============================================================================
# PASTAS E ESTADO
# ==============================================================================

$Script:BaseDir   = Join-Path $env:SystemDrive 'Turbo-Lenovo'
$Script:BackupDir = Join-Path $BaseDir 'Backup'
$Script:ReportDir = Join-Path $BaseDir 'Relatorios'
$Script:StateFile = Join-Path $BackupDir 'rollback.json'

foreach ($d in @($BaseDir, $BackupDir, $ReportDir)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
}

$Script:LogFile = Join-Path $ReportDir ("Turbo-{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
$Script:Rollback = @()

if (Test-Path $StateFile) {
    try { $Script:Rollback = @(Get-Content $StateFile -Raw | ConvertFrom-Json) } catch { $Script:Rollback = @() }
}

# ==============================================================================
# SAIDA
# ==============================================================================

function Write-Line { param([string]$T,[string]$C='Gray') Write-Host $T -ForegroundColor $C }
function Write-OK   { param([string]$T) Write-Host "  [OK]   $T" -ForegroundColor Green }
function Write-Warn2{ param([string]$T) Write-Host "  [ !]   $T" -ForegroundColor Yellow }
function Write-Info2{ param([string]$T) Write-Host "  [ i]   $T" -ForegroundColor Cyan }
function Write-Fail { param([string]$T) Write-Host "  [ERRO] $T" -ForegroundColor Red }
function Write-Skip { param([string]$T) Write-Host "  [ -]   $T (nao se aplica a esta maquina)" -ForegroundColor DarkGray }

function Write-Title {
    param([string]$Text)
    Clear-Host
    Write-Host ''
    Write-Host '  ============================================================' -ForegroundColor DarkCyan
    Write-Host '   TURBO-LENOVO  v2.0   otimizador adaptativo' -ForegroundColor Cyan
    Write-Host '  ============================================================' -ForegroundColor DarkCyan
    Write-Host "   $Text" -ForegroundColor White
    Write-Host '  ------------------------------------------------------------' -ForegroundColor DarkCyan
    Write-Host ''
}

function Pause-Turbo {
    Write-Host ''
    Read-Host '  Pressione ENTER para voltar ao menu' | Out-Null
}

function Invoke-Step {
    <# executa um bloco isolando erro: uma falha nao derruba a otimizacao inteira #>
    param([string]$Name,[scriptblock]$Body)
    try { & $Body }
    catch { Write-Fail "$Name : $($_.Exception.Message)" }
}

# ==============================================================================
# ADMINISTRADOR
# ==============================================================================

function Test-Admin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Admin)) {
    Write-Host ''
    Write-Host '  Este script precisa de privilegios de ADMINISTRADOR.' -ForegroundColor Red
    Write-Host '  Reabrindo elevado...' -ForegroundColor Yellow
    $argl = @('-NoProfile','-ExecutionPolicy','Bypass','-File',('"{0}"' -f $PSCommandPath))
    if ($Auto) { $argl += '-Auto' }
    if ($Undo) { $argl += '-Undo' }
    Start-Process powershell.exe -ArgumentList $argl -Verb RunAs
    exit
}

Start-Transcript -Path $LogFile -Append | Out-Null

# ==============================================================================
# REGISTRO COM ROLLBACK
# ==============================================================================

function Save-Rollback {
    $Script:Rollback | ConvertTo-Json -Depth 6 | Set-Content -Path $StateFile -Encoding UTF8
}

function Set-RegValue {
    <#
      Grava um valor de registro guardando o estado anterior (inclusive
      "nao existia") para que o rollback devolva exatamente o original.
    #>
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)]$Value,
        [ValidateSet('DWord','QWord','String','ExpandString','Binary')][string]$Type = 'DWord',
        [string]$Why = ''
    )

    $old = $null; $existed = $false
    if (Test-Path $Path) {
        $item = Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue
        if ($null -ne $item -and $item.PSObject.Properties.Name -contains $Name) {
            $old = $item.$Name; $existed = $true
        }
    } else {
        New-Item -Path $Path -Force | Out-Null
    }

    if ($existed -and "$old" -eq "$Value") { return $false }   # ja esta como queremos

    # so registra o rollback da primeira vez que tocamos nesta chave
    if (-not ($Script:Rollback | Where-Object { $_.Kind -eq 'reg' -and $_.Path -eq $Path -and $_.Name -eq $Name })) {
        $Script:Rollback += [pscustomobject]@{
            Kind = 'reg'; Path = $Path; Name = $Name
            Existed = $existed; Old = $old; Type = $Type
            Stamp = (Get-Date).ToString('s')
        }
        Save-Rollback
    }

    New-ItemProperty -Path $Path -Name $Name -Value $Value -PropertyType $Type -Force | Out-Null
    if ($Why) { Write-OK $Why }
    return $true
}

function Add-Rollback {
    param([string]$Kind,[hashtable]$Data)
    $o = [pscustomobject](@{ Kind = $Kind; Stamp = (Get-Date).ToString('s') } + $Data)
    $Script:Rollback += $o
    Save-Rollback
}

# ==============================================================================
# DETECCAO DE HARDWARE  (tudo que vem depois depende deste bloco)
# ==============================================================================

function Get-Hardware {

    $cs   = Get-CimInstance Win32_ComputerSystem
    $os   = Get-CimInstance Win32_OperatingSystem
    $cpu  = Get-CimInstance Win32_Processor | Select-Object -First 1
    $mem  = @(Get-CimInstance Win32_PhysicalMemory)
    $arr  = Get-CimInstance Win32_PhysicalMemoryArray | Select-Object -First 1
    $gpu  = @(Get-CimInstance Win32_VideoController)
    $bat  = @(Get-CimInstance Win32_Battery)
    $bios = Get-CimInstance Win32_BIOS

    $disks = @()
    try { $disks = @(Get-PhysicalDisk) } catch {}

    $sysDisk = $null
    try {
        $part = Get-Partition -DriveLetter $env:SystemDrive.TrimEnd(':') -ErrorAction SilentlyContinue
        if ($part) { $sysDisk = Get-PhysicalDisk -ErrorAction SilentlyContinue |
            Where-Object DeviceId -eq (Get-Disk -Number $part.DiskNumber).Number }
    } catch {}
    if (-not $sysDisk -and $disks.Count) { $sysDisk = $disks[0] }

    $ramGB = [math]::Round((($mem | Measure-Object Capacity -Sum).Sum) / 1GB, 1)
    if (-not $ramGB -or $ramGB -eq 0) { $ramGB = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1) }

    $ramType = ($mem | ForEach-Object {
        switch ($_.SMBIOSMemoryType) {
            20 {'DDR'} 21 {'DDR2'} 24 {'DDR3'} 26 {'DDR4'} 34 {'DDR5'} default {'?'}
        }
    } | Select-Object -Unique) -join ', '
    if (-not $ramType) { $ramType = 'nao exposto pelo BIOS' }

    $volC = Get-Volume -DriveLetter $env:SystemDrive.TrimEnd(':') -ErrorAction SilentlyContinue

    # canal de memoria: 1 modulo (ou memoria soldada nao exposta) = single channel
    $modules = $mem.Count
    $slots   = if ($arr) { $arr.MemoryDevices } else { 0 }

    $hw = [pscustomobject]@{
        Fabricante   = $cs.Manufacturer
        Modelo       = $cs.Model
        BIOS         = "$($bios.SMBIOSBIOSVersion) ($($bios.ReleaseDate))"
        CPU          = ($cpu.Name -replace '\s+',' ').Trim()
        Nucleos      = [int]$cpu.NumberOfCores
        Threads      = [int]$cpu.NumberOfLogicalProcessors
        ClockMaxMHz  = [int]$cpu.MaxClockSpeed
        RAM_GB       = $ramGB
        RAM_Tipo     = $ramType
        RAM_MHz      = (($mem | Select-Object -ExpandProperty Speed -Unique) -join ', ')
        RAM_Modulos  = $modules
        RAM_Slots    = $slots
        SingleChannel= ($modules -le 1)
        GPU          = (($gpu | Select-Object -ExpandProperty Name) -join ' | ')
        GPU_Dedicada = [bool](($gpu | Where-Object { $_.Name -match 'NVIDIA|Radeon (RX|Pro)|GeForce|Arc' }).Count)
        DiscoSistema = if ($sysDisk) { $sysDisk.FriendlyName } else { 'desconhecido' }
        MidiaTipo    = if ($sysDisk) { "$($sysDisk.MediaType)" } else { 'desconhecido' }
        Barramento   = if ($sysDisk) { "$($sysDisk.BusType)" } else { '' }
        DiscoGB      = if ($volC) { [math]::Round($volC.Size/1GB,1) } else { 0 }
        LivreGB      = if ($volC) { [math]::Round($volC.SizeRemaining/1GB,1) } else { 0 }
        Notebook     = [bool]$bat.Count
        Windows      = $os.Caption
        Build        = $os.Version
        Win11        = ([int]($os.BuildNumber) -ge 22000)
    }

    $hw | Add-Member -NotePropertyName LivrePct -NotePropertyValue $(
        if ($hw.DiscoGB) { [math]::Round(100 * $hw.LivreGB / $hw.DiscoGB, 1) } else { 0 })

    # ---- classificacao usada por todas as decisoes ----
    $hw | Add-Member -NotePropertyName PerfilRAM -NotePropertyValue $(
        if     ($hw.RAM_GB -le 4)  { 'critico' }
        elseif ($hw.RAM_GB -le 8)  { 'apertado' }
        elseif ($hw.RAM_GB -le 16) { 'confortavel' }
        else                       { 'folgado' })

    $hw | Add-Member -NotePropertyName PerfilCPU -NotePropertyValue $(
        if     ($hw.Threads -le 2) { 'minima' }
        elseif ($hw.Threads -le 4) { 'modesta' }
        elseif ($hw.Threads -le 8) { 'media' }
        else                       { 'alta' })

    $ehSSD = ($hw.MidiaTipo -match 'SSD') -or ($hw.Barramento -match 'NVMe')
    $hw | Add-Member -NotePropertyName EhSSD -NotePropertyValue $ehSSD

    return $hw
}

$Script:HW = Get-Hardware

function Show-Hardware {
    param($hw = $Script:HW)
    Write-Line ("   Maquina    : {0} {1}" -f $hw.Fabricante, $hw.Modelo) 'White'
    Write-Line ("   BIOS       : {0}" -f $hw.BIOS)
    Write-Line ("   CPU        : {0}  ({1}C/{2}T, {3} MHz)  perfil: {4}" -f `
        $hw.CPU, $hw.Nucleos, $hw.Threads, $hw.ClockMaxMHz, $hw.PerfilCPU)
    Write-Line ("   RAM        : {0} GB {1} {2} MHz - {3} modulo(s){4}  perfil: {5}" -f `
        $hw.RAM_GB, $hw.RAM_Tipo, $hw.RAM_MHz, $hw.RAM_Modulos,
        $(if ($hw.SingleChannel) {' [single channel]'} else {' [dual channel]'}), $hw.PerfilRAM)
    Write-Line ("   GPU        : {0}{1}" -f $hw.GPU, $(if($hw.GPU_Dedicada){' [dedicada]'}else{' [integrada]'}))
    Write-Line ("   Disco      : {0} [{1}/{2}] {3} GB - livre {4} GB ({5}%)" -f `
        $hw.DiscoSistema, $hw.MidiaTipo, $hw.Barramento, $hw.DiscoGB, $hw.LivreGB, $hw.LivrePct)
    Write-Line ("   Windows    : {0} build {1}{2}" -f $hw.Windows, $hw.Build,
        $(if($hw.Notebook){'   [NOTEBOOK - bateria detectada]'}else{''}))
}

# ==============================================================================
# MEDICAO ANTES / DEPOIS
# ==============================================================================

function Get-Snapshot {
    $os  = Get-CimInstance Win32_OperatingSystem
    $vol = Get-Volume -DriveLetter $env:SystemDrive.TrimEnd(':') -ErrorAction SilentlyContinue

    $boot = $null
    try {
        $ev = Get-WinEvent -LogName 'Microsoft-Windows-Diagnostics-Performance/Operational' `
                -FilterXPath "*[System[EventID=100]]" -MaxEvents 1 -ErrorAction SilentlyContinue
        if ($ev) { $boot = [math]::Round(([xml]$ev.ToXml()).Event.EventData.Data.Where({$_.Name -eq 'BootTime'}).'#text' / 1000, 1) }
    } catch {}

    [pscustomobject]@{
        Data            = Get-Date
        RAMLivreMB      = [math]::Round($os.FreePhysicalMemory / 1KB, 0)
        RAMUsoPct       = [math]::Round(100 - (100 * $os.FreePhysicalMemory / $os.TotalVisibleMemorySize), 1)
        Processos       = (Get-Process).Count
        ServicosAtivos  = (Get-Service | Where-Object Status -eq 'Running').Count
        StartupItens    = (Get-CimInstance Win32_StartupCommand).Count
        DiscoLivreGB    = if ($vol) { [math]::Round($vol.SizeRemaining/1GB,1) } else { 0 }
        UltimoBootSeg   = $boot
        PlanoEnergia    = ((powercfg /getactivescheme) -join ' ')
    }
}

function Show-Snapshot {
    param($s,[string]$Titulo)
    Write-Line "   $Titulo" 'Yellow'
    Write-Line ("     RAM livre        : {0} MB  (uso {1}%)" -f $s.RAMLivreMB, $s.RAMUsoPct)
    Write-Line ("     Processos        : {0}" -f $s.Processos)
    Write-Line ("     Servicos ativos  : {0}" -f $s.ServicosAtivos)
    Write-Line ("     Itens de startup : {0}" -f $s.StartupItens)
    Write-Line ("     Disco livre      : {0} GB" -f $s.DiscoLivreGB)
    if ($s.UltimoBootSeg) { Write-Line ("     Ultimo boot      : {0} s" -f $s.UltimoBootSeg) }
}

# ==============================================================================
# PONTO DE RESTAURACAO
# ==============================================================================

function New-RestorePointSafe {
    Write-Info2 'Criando ponto de restauracao do sistema...'
    try {
        Enable-ComputerRestore -Drive "$env:SystemDrive\" -ErrorAction SilentlyContinue
        # o Windows ignora pontos criados a menos de 24h; esta chave libera
        Set-RegValue -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore' `
                     -Name 'SystemRestorePointCreationFrequency' -Value 0 | Out-Null
        Checkpoint-Computer -Description 'Turbo-Lenovo (antes)' -RestorePointType 'MODIFY_SETTINGS' -ErrorAction Stop
        Write-OK 'Ponto de restauracao criado.'
    } catch {
        Write-Warn2 'Nao foi possivel criar ponto de restauracao (Protecao do Sistema pode estar desligada).'
        Write-Warn2 'O rollback proprio do script continua funcionando normalmente.'
    }
}

# ==============================================================================
# 1) ENERGIA  - plano dedicado, adaptado a notebook e a CPU de baixo TDP
# ==============================================================================

function Optimize-Power {
    Write-Title 'ENERGIA E FREQUENCIA DE CPU'

    $hw = $Script:HW

    # guarda o plano atual para rollback
    $atual = (powercfg /getactivescheme)
    $guidAtual = [regex]::Match($atual, '([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})').Value
    if ($guidAtual -and -not ($Script:Rollback | Where-Object Kind -eq 'power')) {
        Add-Rollback -Kind 'power' -Data @{ Guid = $guidAtual }
        Write-Info2 "Plano anterior guardado: $guidAtual"
    }

    # --- escolha do plano base ---
    # Ultimate Performance NAO e usado em notebook: ele desliga o parking e o
    # idle de forma agressiva, esquenta um chassi sem ventoinha decente e
    # derruba a autonomia sem ganho real num Celeron de 6 W.
    $baseGuid = '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'   # Alto desempenho
    $baseNome = 'Alto desempenho'
    if (-not $hw.Notebook) {
        $baseGuid = 'e9a42b02-d5df-448d-aa00-03f14749eb61' # Ultimate Performance
        $baseNome = 'Ultimate Performance'
    }

    $existente = (powercfg /list) | Select-String 'TURBO-LENOVO'
    if ($existente) {
        $guid = [regex]::Match($existente.ToString(), '([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})').Value
        Write-Info2 'Plano TURBO-LENOVO ja existe, reaplicando parametros.'
    } else {
        $out  = powercfg -duplicatescheme $baseGuid 2>$null
        $guid = [regex]::Match(($out -join ' '), '([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})').Value
        if (-not $guid) {
            Write-Warn2 "Nao foi possivel duplicar o plano '$baseNome'; usando o plano ativo."
            $guid = $guidAtual
        } else {
            powercfg -changename $guid 'TURBO-LENOVO' "Perfil gerado para $($hw.Modelo) - $($hw.CPU)" | Out-Null
            Write-OK "Plano criado a partir de '$baseNome'."
        }
    }

    powercfg /setactive $guid | Out-Null
    Add-Rollback -Kind 'powerplan-created' -Data @{ Guid = $guid } | Out-Null

    function Set-PowerAC { param($sub,$set,$val) powercfg /setacvalueindex $guid $sub $set $val 2>$null | Out-Null }
    function Set-PowerDC { param($sub,$set,$val) powercfg /setdcvalueindex $guid $sub $set $val 2>$null | Out-Null }

    # --- processador ---
    # Na tomada: piso alto para o N4020 sair do 800 MHz e alcancar o burst de
    # 2.8 GHz assim que a carga aparece. Na bateria: piso baixo e teto 100%,
    # entao o turbo continua disponivel, mas em repouso ele desce de verdade.
    $minAC = if ($hw.PerfilCPU -eq 'minima') { 50 } else { 20 }
    Set-PowerAC SUB_PROCESSOR PROCTHROTTLEMIN $minAC
    Set-PowerAC SUB_PROCESSOR PROCTHROTTLEMAX 100
    Set-PowerDC SUB_PROCESSOR PROCTHROTTLEMIN 5
    Set-PowerDC SUB_PROCESSOR PROCTHROTTLEMAX 100
    Write-OK "Processador: minimo $minAC% na tomada / 5% na bateria, maximo 100% em ambos."

    # politica de resfriamento ativa evita throttle termico antes de baixar clock
    Set-PowerAC SUB_PROCESSOR SYSCOOLPOL 1
    Set-PowerDC SUB_PROCESSOR SYSCOOLPOL 0

    # resposta do governor: subir rapido, descer devagar (perfil "burst")
    powercfg /setacvalueindex $guid SUB_PROCESSOR PERFINCPOL 2 2>$null | Out-Null
    powercfg /setacvalueindex $guid SUB_PROCESSOR PERFDECPOL 1 2>$null | Out-Null
    Write-OK 'Governor ajustado para subir clock rapido sob carga (burst).'

    # --- disco: SSD nao precisa dormir; HDD sim ---
    if ($hw.EhSSD) {
        Set-PowerAC SUB_DISK DISKIDLE 0
        Set-PowerDC SUB_DISK DISKIDLE 1200
        Write-OK 'SSD nunca desliga na tomada (evita latencia de wake-up).'
    } else {
        Set-PowerAC SUB_DISK DISKIDLE 600
        Write-Skip 'Politica de SSD'
    }

    # --- USB e PCIe ---
    Set-PowerAC 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0  # USB selective suspend OFF na tomada
    Set-PowerDC 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 1
    Set-PowerAC SUB_PCIEXPRESS ASPM 0
    Set-PowerDC SUB_PCIEXPRESS ASPM 2
    Write-OK 'USB/PCIe sem economia agressiva na tomada, economicos na bateria.'

    # --- graficos integrados ---
    Set-PowerAC SUB_VIDEO VIDEOIDLE 900
    if ($hw.Notebook) { Set-PowerDC SUB_VIDEO VIDEOIDLE 180 }

    # --- botao/tampa: nao mexemos em suspensao para nao surpreender o usuario ---

    powercfg /setactive $guid | Out-Null
    Write-OK 'Plano TURBO-LENOVO ativado.'

    if ($hw.Notebook) {
        Write-Warn2 'Na bateria o desempenho continua reduzido de proposito. Para trabalho pesado, use na tomada.'
    }

    # Modo de energia do Windows 11 (slider) em desempenho quando na tomada
    if ($Script:HW.Win11) {
        powercfg /overlaysetactive overlay_scheme_max 2>$null | Out-Null
        Write-OK 'Modo de energia do Windows 11 definido como "Melhor desempenho".'
    }
}

# ==============================================================================
# 2) MEMORIA  - o item mais importante numa maquina de 4 GB
# ==============================================================================

function Optimize-Memory {
    Write-Title 'MEMORIA'

    $hw = $Script:HW

    # --- compressao de memoria ---
    # Em 4 GB a compressao vale muito mais que o custo de CPU: cada MB que
    # deixa de ir ao pagefile e um acesso a SSD economizado.
    try {
        $mm = Get-MMAgent
        if ($hw.PerfilRAM -in @('critico','apertado')) {
            if (-not $mm.MemoryCompression) {
                Enable-MMAgent -MemoryCompression
                Add-Rollback -Kind 'mmagent' -Data @{ Feature='MemoryCompression'; Old=$false }
            }
            Write-OK 'Compressao de memoria ativa (essencial com pouca RAM).'

            # SysMain/superfetch: com SSD + pouca RAM, o pre-carregamento
            # atrapalha mais do que ajuda. Em >=8 GB ele fica como esta.
            if ($hw.EhSSD -and $hw.PerfilRAM -eq 'critico') {
                $svc = Get-Service SysMain -ErrorAction SilentlyContinue
                if ($svc -and $svc.StartType -ne 'Disabled') {
                    Add-Rollback -Kind 'service' -Data @{ Name='SysMain'; Old="$($svc.StartType)" }
                    Stop-Service SysMain -Force -ErrorAction SilentlyContinue
                    Set-Service SysMain -StartupType Disabled
                    Write-OK 'SysMain desativado (SSD + 4 GB: prefetch so consome RAM e I/O).'
                }
            }
        } else {
            Write-Skip 'Ajustes de memoria para pouca RAM'
        }
    } catch { Write-Warn2 "MMAgent indisponivel: $($_.Exception.Message)" }

    # --- arquivo de paginacao fixo ---
    # Pagefile gerenciado pelo Windows cresce e encolhe, fragmenta e da picos
    # de latencia. Com 4 GB, um pagefile fixo e obrigatorio (nunca desativar).
    $cs = Get-CimInstance Win32_ComputerSystem
    if ($cs.AutomaticManagedPagefile) {
        $alvoMin = [int]([math]::Max(2048, $hw.RAM_GB * 1024))          # 1x RAM
        $alvoMax = [int]([math]::Max(4096, $hw.RAM_GB * 1024 * 2))      # 2x RAM
        # nao passar de 12% do disco para nao sufocar um SSD pequeno
        $teto = [int]($hw.DiscoGB * 1024 * 0.12)
        if ($alvoMax -gt $teto) { $alvoMax = [math]::Max($alvoMin, $teto) }

        if ($hw.LivreGB -lt ($alvoMax / 1024 + 5)) {
            Write-Warn2 "Espaco livre insuficiente para fixar o pagefile em $alvoMax MB. Rode a limpeza primeiro."
        } else {
            Add-Rollback -Kind 'pagefile' -Data @{ Automatic = $true }
            $csw = Get-CimInstance Win32_ComputerSystem
            $csw | Set-CimInstance -Property @{ AutomaticManagedPagefile = $false }
            $pf = Get-CimInstance Win32_PageFileSetting -ErrorAction SilentlyContinue |
                  Where-Object { $_.Name -like "$($env:SystemDrive)*" }
            if (-not $pf) {
                New-CimInstance -ClassName Win32_PageFileSetting `
                    -Property @{ Name = "$env:SystemDrive\pagefile.sys" } -ErrorAction SilentlyContinue | Out-Null
                $pf = Get-CimInstance Win32_PageFileSetting | Where-Object { $_.Name -like "$($env:SystemDrive)*" }
            }
            if ($pf) {
                $pf | Set-CimInstance -Property @{ InitialSize = $alvoMin; MaximumSize = $alvoMax }
                Write-OK "Pagefile fixo em ${alvoMin}-${alvoMax} MB (aplica apos reiniciar)."
            }
        }
    } else {
        Write-Info2 'Pagefile ja esta em modo manual - nao alterado.'
    }

    # --- limpar o pagefile no desligamento? NAO ---
    # Isso adiciona dezenas de segundos ao shutdown. Garantimos que esteja off.
    Set-RegValue -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' `
                 -Name 'ClearPageFileAtShutdown' -Value 0 `
                 -Why 'Limpeza do pagefile no desligamento desativada (shutdown mais rapido).' | Out-Null
}

# ==============================================================================
# 3) INTERFACE  - animacoes e transparencia custam GPU/RAM na UHD 600
# ==============================================================================

function Optimize-Interface {
    Write-Title 'INTERFACE GRAFICA'

    $hw = $Script:HW
    $leve = ($hw.PerfilRAM -in @('critico','apertado')) -or ($hw.PerfilCPU -in @('minima','modesta')) -or (-not $hw.GPU_Dedicada)

    if (-not $leve) { Write-Skip 'Modo de interface enxuta'; return }

    # "Ajustar para melhor desempenho", porem mantendo suavizacao de fontes
    # (sem ela o texto fica sofrivel em tela 1366x768 TN).
    $fx = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects'
    Set-RegValue -Path $fx -Name 'VisualFXSetting' -Value 3 | Out-Null   # 3 = personalizado

    Set-RegValue -Path 'HKCU:\Control Panel\Desktop' -Name 'UserPreferencesMask' `
                 -Value ([byte[]](0x90,0x12,0x03,0x80,0x10,0x00,0x00,0x00)) -Type Binary | Out-Null
    Set-RegValue -Path 'HKCU:\Control Panel\Desktop\WindowMetrics' -Name 'MinAnimate' -Value '0' -Type String | Out-Null
    Set-RegValue -Path 'HKCU:\Control Panel\Desktop' -Name 'FontSmoothing' -Value '2' -Type String | Out-Null
    Set-RegValue -Path 'HKCU:\Control Panel\Desktop' -Name 'DragFullWindows' -Value '0' -Type String | Out-Null
    Set-RegValue -Path 'HKCU:\Software\Microsoft\Windows\DWM' -Name 'EnableAeroPeek' -Value 0 | Out-Null
    Write-OK 'Animacoes, sombras e arrasto de janela cheia desligados (fontes preservadas).'

    Set-RegValue -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' `
                 -Name 'EnableTransparency' -Value 0 `
                 -Why 'Transparencia (acrylic/mica) desligada - alivio direto na UHD 600.' | Out-Null

    # menus abrindo sem atraso
    Set-RegValue -Path 'HKCU:\Control Panel\Desktop' -Name 'MenuShowDelay' -Value '0' -Type String `
                 -Why 'Atraso de menu zerado.' | Out-Null

    # Explorer sem anuncio de OneDrive/Office e sem thumbnails pesados de rede
    Set-RegValue -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' `
                 -Name 'ShowSyncProviderNotifications' -Value 0 `
                 -Why 'Propaganda de sincronizacao no Explorer desativada.' | Out-Null

    if ($hw.Win11) {
        Set-RegValue -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' `
                     -Name 'TaskbarDa' -Value 0 `
                     -Why 'Widgets removidos da barra de tarefas (processo residente de ~200 MB).' | Out-Null
        Set-RegValue -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Dsh' -Name 'AllowNewsAndInterests' -Value 0 | Out-Null
    }
}

# ==============================================================================
# 4) SEGUNDO PLANO  - onde os 2 threads estao sendo desperdicados
# ==============================================================================

function Optimize-Background {
    Write-Title 'PROCESSOS EM SEGUNDO PLANO'

    $hw = $Script:HW

    # --- apps UWP rodando em background ---
    if ($hw.PerfilRAM -in @('critico','apertado')) {
        Set-RegValue -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications' `
                     -Name 'GlobalUserDisabled' -Value 1 `
                     -Why 'Apps da Store bloqueados em segundo plano.' | Out-Null
        Set-RegValue -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Search' `
                     -Name 'BackgroundAppGlobalToggle' -Value 0 | Out-Null
    } else { Write-Skip 'Bloqueio de apps em segundo plano' }

    # --- Xbox Game Bar / DVR: inutil aqui e sempre residente ---
    Set-RegValue -Path 'HKCU:\System\GameConfigStore' -Name 'GameDVR_Enabled' -Value 0 | Out-Null
    Set-RegValue -Path 'HKCU:\System\GameConfigStore' -Name 'GameDVR_FSEBehaviorMode' -Value 2 | Out-Null
    Set-RegValue -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR' -Name 'AllowGameDVR' -Value 0 | Out-Null
    Set-RegValue -Path 'HKCU:\Software\Microsoft\GameBar' -Name 'UseNexusForGameBarEnabled' -Value 0 | Out-Null
    Set-RegValue -Path 'HKCU:\Software\Microsoft\GameBar' -Name 'ShowStartupPanel' -Value 0 | Out-Null
    Write-OK 'Xbox Game Bar e gravacao em segundo plano desativados.'

    # --- sugestoes, dicas, conteudo promovido: baixam pacotes sozinhos ---
    $cdm = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager'
    foreach ($v in @('SilentInstalledAppsEnabled','SystemPaneSuggestionsEnabled','SoftLandingEnabled',
                     'SubscribedContent-338388Enabled','SubscribedContent-338389Enabled',
                     'SubscribedContent-310093Enabled','SubscribedContent-353698Enabled',
                     'PreInstalledAppsEnabled','OemPreInstalledAppsEnabled','ContentDeliveryAllowed')) {
        Set-RegValue -Path $cdm -Name $v -Value 0 | Out-Null
    }
    Write-OK 'Instalacao silenciosa de apps promovidos e dicas do Windows desligadas.'

    # --- telemetria de diagnostico no nivel minimo permitido pela edicao ---
    Set-RegValue -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection' `
                 -Name 'AllowTelemetry' -Value 1 | Out-Null
    Set-RegValue -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection' `
                 -Name 'AllowTelemetry' -Value 1 | Out-Null
    Write-OK 'Telemetria no nivel "Basico" (Defender e Update continuam intactos).'

    # tarefas agendadas de experiencia do usuario: seguras de desligar
    foreach ($t in @(
        '\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser',
        '\Microsoft\Windows\Application Experience\ProgramDataUpdater',
        '\Microsoft\Windows\Customer Experience Improvement Program\Consolidator',
        '\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip',
        '\Microsoft\Windows\Feedback\Siuf\DmClient',
        '\Microsoft\Windows\Feedback\Siuf\DmClientOnScenarioDownload')) {
        try {
            $task = Get-ScheduledTask -TaskPath ([IO.Path]::GetDirectoryName($t) + '\') `
                    -TaskName ([IO.Path]::GetFileName($t)) -ErrorAction Stop
            if ($task.State -ne 'Disabled') {
                Add-Rollback -Kind 'task' -Data @{ Full = $t }
                $task | Disable-ScheduledTask -ErrorAction Stop | Out-Null
            }
        } catch {}
    }
    Write-OK 'Tarefas de telemetria/compatibilidade (CEIP, Appraiser) desativadas.'

    # --- indexacao: manter o servico, restringir o escopo ---
    # Desligar o Windows Search inteiro quebra a busca do menu Iniciar e do
    # Outlook. Reduzimos o custo mantendo a funcao.
    if ($hw.PerfilCPU -eq 'minima') {
        Set-RegValue -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search' `
                     -Name 'PreventIndexingLowDiskSpaceMB' -Value 2000 | Out-Null
        Set-RegValue -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search' `
                     -Name 'DisableBackoff' -Value 0 `
                     -Why 'Indexador obrigado a recuar quando o usuario esta usando a maquina.' | Out-Null
        Set-RegValue -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\SearchSettings' `
                     -Name 'IsDynamicSearchBoxEnabled' -Value 0 | Out-Null
        Set-RegValue -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search' `
                     -Name 'ConnectedSearchUseWeb' -Value 0 `
                     -Why 'Busca na web dentro do menu Iniciar desligada (menos rede e menos CPU).' | Out-Null
    }

    # --- servicos de baixo risco, so quando fazem sentido no perfil ---
    $alvos = @()
    if (-not $hw.Notebook)                  { $alvos += 'TabletInputService' }
    $alvos += 'MapsBroker'                  # mapas offline: quase ninguem usa
    $alvos += 'RetailDemo'                  # modo demonstracao de loja
    $alvos += 'DiagTrack'                   # experiencias do usuario conectado
    $alvos += 'dmwappushservice'
    if ($hw.PerfilCPU -eq 'minima')         { $alvos += 'WSearch' }  # avaliado abaixo, nunca desativado

    foreach ($n in ($alvos | Select-Object -Unique)) {
        if ($n -eq 'WSearch') { continue }   # protegido de proposito
        $s = Get-Service $n -ErrorAction SilentlyContinue
        if ($s -and $s.StartType -ne 'Disabled') {
            try {
                Add-Rollback -Kind 'service' -Data @{ Name=$n; Old="$($s.StartType)" }
                Stop-Service $n -Force -ErrorAction SilentlyContinue
                Set-Service $n -StartupType Disabled -ErrorAction Stop
                Write-OK "Servico $n desativado."
            } catch { Write-Warn2 "Servico $n nao pode ser alterado." }
        }
    }

    Write-Info2 'Preservados: Defender, Update, BITS, Audio, Bluetooth, Spooler, WSearch, Wi-Fi, RPC, WMI.'
}

# ==============================================================================
# 5) DISCO / SSD
# ==============================================================================

function Optimize-Storage {
    Write-Title 'ARMAZENAMENTO'

    $hw = $Script:HW
    $letra = $env:SystemDrive.TrimEnd(':')

    if ($hw.EhSSD) {
        Write-Info2 "SSD detectado ($($hw.DiscoSistema)) - desfragmentacao nunca sera executada."

        # TRIM
        try {
            Optimize-Volume -DriveLetter $letra -ReTrim -ErrorAction Stop
            Write-OK 'TRIM executado no volume do sistema.'
        } catch { Write-Warn2 "TRIM falhou: $($_.Exception.Message)" }

        # carimbo de ultimo acesso: uma escrita a cada leitura de arquivo
        try {
            $atual = (fsutil behavior query DisableLastAccess) -join ' '
            if ($atual -notmatch '=\s*1') {
                Add-Rollback -Kind 'fsutil' -Data @{ Setting='DisableLastAccess'; Old=$atual }
                fsutil behavior set DisableLastAccess 1 | Out-Null
                Write-OK 'Carimbo de ultimo acesso NTFS desligado (menos escritas no SSD).'
            }
        } catch {}

        # hibernacao: em notebook mantemos, mas no formato reduzido -
        # libera alguns GB num disco de 119 GB sem perder o boot rapido.
        if ($hw.Notebook -and $hw.DiscoGB -lt 256) {
            try {
                powercfg /hibernate /type reduced 2>$null | Out-Null
                Write-OK 'Hiberfil.sys em modo reduzido (inicializacao rapida preservada, alguns GB liberados).'
            } catch {}
        }
    }
    else {
        Write-Info2 'HDD detectado - executando desfragmentacao.'
        Optimize-Volume -DriveLetter $letra -Defrag -ErrorAction SilentlyContinue
        Write-OK 'Desfragmentacao concluida.'
    }

    # Storage Sense: manutencao automatica de espaco, sem tocar em documentos
    $ss = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\StorageSense\Parameters\StoragePolicy'
    Set-RegValue -Path $ss -Name '01' -Value 1 | Out-Null              # ligado
    Set-RegValue -Path $ss -Name '2048' -Value 1 | Out-Null            # cadencia por espaco livre
    Set-RegValue -Path $ss -Name '32' -Value 7 | Out-Null              # lixeira: 7 dias... mantemos 30
    Set-RegValue -Path $ss -Name '32' -Value 30 | Out-Null
    Set-RegValue -Path $ss -Name '256' -Value 0 | Out-Null             # NAO apaga Downloads
    Write-OK 'Sensor de Armazenamento ligado (lixeira 30 dias; pasta Downloads intocada).'

    if ($hw.LivrePct -lt 15) {
        Write-Warn2 ("Disco com apenas {0}% livre. Abaixo de 10-15% o SSD perde desempenho de escrita e o pagefile sofre." -f $hw.LivrePct)
        Write-Warn2 'Rode a limpeza [4] e considere mover videos/downloads para um HD externo.'
    }
}

# ==============================================================================
# 6) LIMPEZA
# ==============================================================================

function Clear-System {
    Write-Title 'LIMPEZA SEGURA'

    $antes = (Get-Volume -DriveLetter $env:SystemDrive.TrimEnd(':')).SizeRemaining

    $alvos = @(
        @{ P = "$env:TEMP\*";                                        D = 'Temporarios do usuario' }
        @{ P = "$env:WINDIR\Temp\*";                                 D = 'Temporarios do Windows' }
        @{ P = "$env:WINDIR\Prefetch\*.pf";                          D = 'Prefetch antigo' }
        @{ P = "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\thumbcache*"; D = 'Cache de miniaturas' }
        @{ P = "$env:LOCALAPPDATA\Microsoft\Windows\INetCache\*";    D = 'Cache da internet' }
        @{ P = "$env:LOCALAPPDATA\CrashDumps\*";                     D = 'Despejos de falha' }
        @{ P = "$env:WINDIR\SoftwareDistribution\Download\*";        D = 'Cache do Windows Update' }
        @{ P = "$env:ProgramData\Microsoft\Windows\WER\ReportQueue\*"; D = 'Relatorios de erro' }
    )

    foreach ($a in $alvos) {
        try {
            $n = @(Get-ChildItem $a.P -Force -ErrorAction SilentlyContinue).Count
            Remove-Item $a.P -Recurse -Force -ErrorAction SilentlyContinue
            Write-OK "$($a.D): $n item(ns) tratado(s)."
        } catch { Write-Warn2 "$($a.D): parcialmente em uso." }
    }

    # cache de entrega de atualizacoes (pode ocupar varios GB)
    Invoke-Step 'Delivery Optimization' {
        Delete-DeliveryOptimizationCache -Force -ErrorAction SilentlyContinue
        Write-OK 'Cache do Delivery Optimization limpo.'
    }

    Write-Info2 'Compactando componentes antigos do Windows (WinSxS)... pode levar alguns minutos.'
    Start-Process dism.exe -ArgumentList '/Online /Cleanup-Image /StartComponentCleanup /Quiet' -Wait -WindowStyle Hidden
    Write-OK 'WinSxS compactado (versoes antigas de atualizacoes removidas).'

    Write-Info2 'Nao tocamos em Documentos, Imagens, Downloads, Area de Trabalho nem na Lixeira.'

    Start-Sleep -Seconds 2
    $depois = (Get-Volume -DriveLetter $env:SystemDrive.TrimEnd(':')).SizeRemaining
    $ganho = [math]::Round(($depois - $antes)/1MB, 0)
    Write-Host ''
    Write-Line ("   Espaco liberado: {0} MB   (livre agora: {1} GB)" -f $ganho, [math]::Round($depois/1GB,1)) 'Green'
}

# ==============================================================================
# 7) REDE
# ==============================================================================

function Optimize-Network {
    Write-Title 'REDE'

    Invoke-Step 'TCP' {
        netsh int tcp set global autotuninglevel=normal    | Out-Null
        netsh int tcp set global rss=enabled               | Out-Null
        netsh int tcp set global ecncapability=disabled    | Out-Null
        netsh int tcp set global timestamps=disabled       | Out-Null
        Write-OK 'TCP: auto-tuning normal, RSS ligado, ECN/timestamps desligados.'
    }

    Invoke-Step 'DNS' {
        Clear-DnsClientCache
        Write-OK 'Cache de DNS limpo.'
    }

    # Wi-Fi de notebook: o adaptador so entra em economia de energia na bateria
    if ($Script:HW.Notebook) {
        Invoke-Step 'Wi-Fi' {
            $wifi = Get-NetAdapter -Physical | Where-Object { $_.InterfaceDescription -match 'Wi-?Fi|Wireless|802\.11' -and $_.Status -eq 'Up' }
            foreach ($a in $wifi) {
                $pm = Get-NetAdapterPowerManagement -Name $a.Name -ErrorAction SilentlyContinue
                if ($pm -and $pm.AllowComputerToTurnOffDevice -eq 'Enabled') {
                    Add-Rollback -Kind 'nicpower' -Data @{ Name = $a.Name; Old = 'Enabled' }
                    $pm.AllowComputerToTurnOffDevice = 'Disabled'
                    Set-NetAdapterPowerManagement -InputObject $pm
                    Write-OK "Wi-Fi '$($a.Name)': desligamento automatico do radio desativado (menos quedas de conexao)."
                }
            }
        }
    }

    Write-Info2 'Nenhum DNS de terceiro foi imposto e nenhum MTU foi alterado no chute.'
}

# ==============================================================================
# 8) INICIALIZACAO  - interativo, nunca automatico
# ==============================================================================

function Optimize-Startup {
    Write-Title 'PROGRAMAS DE INICIALIZACAO'

    # nomes que quase sempre podem sair do boot numa maquina destas
    $pesados = 'Teams|Skype|Spotify|Steam|Epic|Discord|OneDrive|Adobe|Acrobat|iTunes|CCleaner|Cortana|Zoom|Dropbox|uTorrent|Java Update|QuickTime|Sync'
    # o que NAO deve ser sugerido para desativar
    $intocaveis = 'SecurityHealth|Windows Defender|Realtek|Audio|Intel.*Graphics|Synaptics|ELAN|Touchpad|Lenovo (Vantage )?Service|Energy Management|Hotkey|IgfxTray|Bluetooth'

    $itens = Get-CimInstance Win32_StartupCommand |
             Select-Object Name, Command, Location, User

    if (-not $itens) { Write-Info2 'Nenhum item de inicializacao classico encontrado.'; return }

    $i = 0
    $tabela = foreach ($it in $itens) {
        $i++
        $risco = if ($it.Name -match $intocaveis) { 'MANTER' }
                 elseif ($it.Name -match $pesados -or $it.Command -match $pesados) { 'REMOVER' }
                 else { 'AVALIAR' }
        [pscustomobject]@{ N=$i; Sugestao=$risco; Nome=$it.Name; Local=$it.Location; Comando=$it.Command }
    }

    $tabela | Format-Table N, Sugestao, Nome, Local -AutoSize | Out-Host
    $tabela | Format-List | Out-File (Join-Path $ReportDir 'Inicializacao.txt') -Encoding UTF8

    Write-Host ''
    Write-Line '   REMOVER = software pesado, reabre sozinho quando voce o usa.' 'DarkGray'
    Write-Line '   MANTER  = driver, audio, seguranca ou utilitario Lenovo.' 'DarkGray'
    Write-Host ''
    $sel = Read-Host '   Numeros a desativar, separados por virgula (ENTER para nao mexer)'
    if (-not $sel) { Write-Info2 'Nada alterado.'; return }

    foreach ($num in ($sel -split ',')) {
        $n = 0
        if (-not [int]::TryParse($num.Trim(), [ref]$n)) { continue }
        $alvo = $tabela | Where-Object N -eq $n
        if (-not $alvo) { continue }

        if ($alvo.Local -match 'Startup') {
            Write-Warn2 "$($alvo.Nome): atalho na pasta Iniciar. Remova manualmente em: $($alvo.Local)"
            continue
        }
        $hive = if ($alvo.Local -match 'HKLM|Machine|Common') { 'HKLM:' } else { 'HKCU:' }
        $path = "$hive\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        $prop = Get-ItemProperty -Path $path -ErrorAction SilentlyContinue
        if ($prop -and $prop.PSObject.Properties.Name -contains $alvo.Nome) {
            Add-Rollback -Kind 'startup' -Data @{ Path=$path; Name=$alvo.Nome; Old=$prop.($alvo.Nome) }
            Remove-ItemProperty -Path $path -Name $alvo.Nome -Force
            Write-OK "$($alvo.Nome) removido da inicializacao (reversivel pela opcao [R])."
        } else {
            Write-Warn2 "$($alvo.Nome): entrada nao encontrada em Run; provavelmente e tarefa agendada ou servico."
        }
    }
}

# ==============================================================================
# 9) RELATORIO
# ==============================================================================

function New-Report {
    param($Antes, $Depois)

    $hw = $Script:HW
    $arq = Join-Path $ReportDir ("Relatorio-{0}.txt" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))

    $l = New-Object System.Collections.Generic.List[string]
    $l.Add('================================================================')
    $l.Add(' TURBO-LENOVO v2.0 - RELATORIO')
    $l.Add(" Gerado em $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')")
    $l.Add('================================================================')
    $l.Add('')
    $l.Add('--- HARDWARE ---')
    foreach ($p in $hw.PSObject.Properties) { $l.Add(('{0,-14}: {1}' -f $p.Name, $p.Value)) }
    $l.Add('')

    if ($Antes) {
        $l.Add('--- ANTES / DEPOIS ---')
        $campos = 'RAMLivreMB','RAMUsoPct','Processos','ServicosAtivos','StartupItens','DiscoLivreGB'
        foreach ($c in $campos) {
            $a = $Antes.$c; $d = if ($Depois) { $Depois.$c } else { '-' }
            $delta = if ($Depois -and $a -is [ValueType]) { ' (' + ('{0:+#;-#;0}' -f ($d - $a)) + ')' } else { '' }
            $l.Add(('{0,-16}: {1,10}  ->  {2,10}{3}' -f $c, $a, $d, $delta))
        }
        $l.Add('')
    }

    $l.Add('--- DIAGNOSTICO E RECOMENDACOES ---')
    if ($hw.PerfilRAM -eq 'critico') {
        $l.Add('[RAM] 4 GB e o teto de desempenho desta maquina. O Windows 11 sozinho')
        $l.Add('      ocupa cerca de 2,5 GB. Se o modelo tiver slot SODIMM livre, um')
        $l.Add('      pente de 4 ou 8 GB DDR4-2400 e o unico upgrade com ganho grande.')
        if ($hw.SingleChannel) {
            $l.Add('      Um segundo modulo tambem ativa dual channel, o que sozinho da')
            $l.Add('      cerca de 20-40% a mais na UHD 600 (grafico usa a RAM do sistema).')
        }
    }
    if ($hw.PerfilCPU -eq 'minima') {
        $l.Add('[CPU] 2 nucleos sem SMT. Mantenha poucas abas de navegador abertas,')
        $l.Add('      prefira navegador leve e evite antivirus de terceiro rodando')
        $l.Add('      junto com o Defender - dois scanners sao fatais aqui.')
    }
    if ($hw.LivrePct -lt 20) {
        $l.Add(("[SSD] Apenas {0}% livres. Mantenha ao menos 20% para o SSD nao" -f $hw.LivrePct))
        $l.Add('      cair de desempenho e o pagefile ter folga.')
    }
    if ($hw.Notebook) {
        $l.Add('[BAT] Ganho maximo so aparece na tomada. O perfil na bateria foi')
        $l.Add('      mantido conservador de proposito.')
    }
    $l.Add('')
    $l.Add('--- REVERSAO ---')
    $l.Add(("Alteracoes registradas para rollback: {0}" -f $Script:Rollback.Count))
    $l.Add("Arquivo de estado: $StateFile")
    $l.Add('Use a opcao [R] do menu para desfazer tudo.')

    $l | Out-File -FilePath $arq -Encoding UTF8
    ($hw | Format-List | Out-String) | Out-File (Join-Path $ReportDir 'Diagnostico.txt') -Encoding UTF8

    Write-OK "Relatorio salvo em: $arq"
    return $arq
}

# ==============================================================================
# 10) ROLLBACK
# ==============================================================================

function Undo-All {
    Write-Title 'DESFAZER ALTERACOES'

    if (-not $Script:Rollback -or $Script:Rollback.Count -eq 0) {
        Write-Info2 'Nenhuma alteracao registrada.'
        return
    }

    Write-Line ("   {0} alteracao(oes) registrada(s)." -f $Script:Rollback.Count) 'Yellow'
    $c = Read-Host '   Digite DESFAZER para confirmar'
    if ($c -ne 'DESFAZER') { Write-Warn2 'Cancelado.'; return }

    # ordem inversa: a ultima alteracao e a primeira a ser revertida
    for ($i = $Script:Rollback.Count - 1; $i -ge 0; $i--) {
        $r = $Script:Rollback[$i]
        try {
            switch ($r.Kind) {
                'reg' {
                    if ($r.Existed) {
                        New-ItemProperty -Path $r.Path -Name $r.Name -Value $r.Old -PropertyType $r.Type -Force | Out-Null
                    } else {
                        Remove-ItemProperty -Path $r.Path -Name $r.Name -Force -ErrorAction SilentlyContinue
                    }
                    Write-OK "registro: $($r.Path)\$($r.Name)"
                }
                'service' {
                    Set-Service $r.Name -StartupType $r.Old -ErrorAction Stop
                    Write-OK "servico $($r.Name) -> $($r.Old)"
                }
                'task' {
                    Enable-ScheduledTask -TaskPath ([IO.Path]::GetDirectoryName($r.Full) + '\') `
                        -TaskName ([IO.Path]::GetFileName($r.Full)) -ErrorAction SilentlyContinue | Out-Null
                    Write-OK "tarefa $($r.Full) reativada"
                }
                'power' {
                    powercfg /setactive $r.Guid | Out-Null
                    Write-OK "plano de energia anterior restaurado"
                }
                'powerplan-created' { }  # o plano criado e apagado no fim
                'pagefile' {
                    $cs = Get-CimInstance Win32_ComputerSystem
                    $cs | Set-CimInstance -Property @{ AutomaticManagedPagefile = $true }
                    Write-OK 'pagefile voltou a ser gerenciado pelo Windows'
                }
                'mmagent' {
                    if (-not $r.Old) { Disable-MMAgent -MemoryCompression -ErrorAction SilentlyContinue }
                    Write-OK 'compressao de memoria restaurada'
                }
                'fsutil' {
                    fsutil behavior set DisableLastAccess 2 | Out-Null
                    Write-OK 'carimbo de ultimo acesso no padrao do Windows'
                }
                'nicpower' {
                    $pm = Get-NetAdapterPowerManagement -Name $r.Name -ErrorAction SilentlyContinue
                    if ($pm) { $pm.AllowComputerToTurnOffDevice = $r.Old; Set-NetAdapterPowerManagement -InputObject $pm }
                    Write-OK "adaptador $($r.Name) restaurado"
                }
                'startup' {
                    New-ItemProperty -Path $r.Path -Name $r.Name -Value $r.Old -PropertyType String -Force | Out-Null
                    Write-OK "inicializacao $($r.Name) restaurada"
                }
            }
        } catch { Write-Warn2 "Falha ao reverter $($r.Kind): $($_.Exception.Message)" }
    }

    # remove o plano criado por ultimo, ja com outro ativo
    foreach ($p in ($Script:Rollback | Where-Object Kind -eq 'powerplan-created')) {
        powercfg /delete $p.Guid 2>$null | Out-Null
    }

    $Script:Rollback = @()
    Save-Rollback
    Write-Host ''
    Write-OK 'Reversao concluida.'
    Write-Warn2 'Reinicie o Windows para que tudo volte ao estado original.'
}

# ==============================================================================
# MODO TURBO  (a sequencia completa)
# ==============================================================================

function Invoke-Turbo {
    param([switch]$SemConfirmar)

    Write-Title 'MODO TURBO'
    Show-Hardware
    Write-Host ''
    Write-Line '   Sera executado, nesta ordem:' 'White'
    Write-Line '     1. ponto de restauracao + backup reversivel'
    Write-Line '     2. limpeza segura (nenhum arquivo pessoal)'
    Write-Line '     3. memoria: compressao + pagefile fixo'
    Write-Line '     4. interface enxuta (animacoes/transparencia)'
    Write-Line '     5. corte de processos em segundo plano'
    Write-Line '     6. plano de energia dedicado'
    Write-Line '     7. SSD: TRIM + menos escritas'
    Write-Line '     8. rede'
    Write-Line '     9. relatorio antes/depois'
    Write-Host ''
    Write-Line '   Defender, Windows Update, audio, Bluetooth, impressao e busca ficam intactos.' 'DarkGray'
    Write-Host ''

    if (-not $SemConfirmar) {
        if ((Read-Host '   Digite TURBO para executar') -ne 'TURBO') { Write-Warn2 'Cancelado.'; return }
    }

    $antes = Get-Snapshot

    New-RestorePointSafe
    Invoke-Step 'Limpeza'    { Clear-System }
    Invoke-Step 'Memoria'    { Optimize-Memory }
    Invoke-Step 'Interface'  { Optimize-Interface }
    Invoke-Step 'Background' { Optimize-Background }
    Invoke-Step 'Energia'    { Optimize-Power }
    Invoke-Step 'Disco'      { Optimize-Storage }
    Invoke-Step 'Rede'       { Optimize-Network }

    # reinicia o Explorer para aplicar a interface sem exigir logoff
    Invoke-Step 'Explorer' {
        Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        if (-not (Get-Process explorer -ErrorAction SilentlyContinue)) { Start-Process explorer.exe }
    }

    Start-Sleep -Seconds 3
    $depois = Get-Snapshot

    Write-Title 'RESULTADO'
    Show-Snapshot $antes  'ANTES'
    Write-Host ''
    Show-Snapshot $depois 'DEPOIS'
    Write-Host ''
    New-Report -Antes $antes -Depois $depois | Out-Null
    Write-Host ''
    Write-Line '   REINICIE o notebook para o pagefile fixo e o plano de energia entrarem por completo.' 'Yellow'
}

# ==============================================================================
# MENU
# ==============================================================================

if ($Undo) { Undo-All; Stop-Transcript | Out-Null; exit }
if ($Auto) { Invoke-Turbo -SemConfirmar; Stop-Transcript | Out-Null; exit }

while ($true) {
    Write-Title 'PAINEL'
    Show-Hardware
    Write-Host ''
    Write-Line '   ------------------------------------------------------------' 'DarkCyan'
    Write-Line '    [1] MODO TURBO  (tudo, na ordem certa, com antes/depois)' 'Green'
    Write-Line '   ------------------------------------------------------------' 'DarkCyan'
    Write-Line '    [2] Memoria        compressao + pagefile fixo'
    Write-Line '    [3] Energia        plano dedicado a esta CPU'
    Write-Line '    [4] Limpeza        temporarios, WinSxS, caches'
    Write-Line '    [5] Interface      animacoes e transparencia'
    Write-Line '    [6] Segundo plano  telemetria, GameDVR, apps UWP'
    Write-Line '    [7] Disco          TRIM e ajustes de SSD'
    Write-Line '    [8] Rede           TCP e Wi-Fi'
    Write-Line '    [9] Inicializacao  revisao interativa'
    Write-Line '    [D] Diagnostico e relatorio'
    Write-Line '    [R] Desfazer todas as alteracoes' 'Yellow'
    Write-Line '    [0] Sair'
    Write-Line '   ------------------------------------------------------------' 'DarkCyan'
    Write-Host ''

    switch ((Read-Host '   Opcao').ToUpper()) {
        '1' { Invoke-Turbo; Pause-Turbo }
        '2' { Invoke-Step 'Memoria'    { Optimize-Memory };     Pause-Turbo }
        '3' { Invoke-Step 'Energia'    { Optimize-Power };      Pause-Turbo }
        '4' { Invoke-Step 'Limpeza'    { Clear-System };        Pause-Turbo }
        '5' { Invoke-Step 'Interface'  { Optimize-Interface };  Pause-Turbo }
        '6' { Invoke-Step 'Background' { Optimize-Background }; Pause-Turbo }
        '7' { Invoke-Step 'Disco'      { Optimize-Storage };    Pause-Turbo }
        '8' { Invoke-Step 'Rede'       { Optimize-Network };    Pause-Turbo }
        '9' { Invoke-Step 'Startup'    { Optimize-Startup };    Pause-Turbo }
        'D' {
            Write-Title 'DIAGNOSTICO'
            Show-Hardware
            Write-Host ''
            Show-Snapshot (Get-Snapshot) 'ESTADO ATUAL'
            Write-Host ''
            New-Report -Antes $null -Depois $null | Out-Null
            Pause-Turbo
        }
        'R' { Undo-All; Pause-Turbo }
        '0' {
            Write-Host ''
            Write-OK 'Encerrando. Relatorios em ' 
            Write-Line "   $ReportDir" 'Cyan'
            Stop-Transcript | Out-Null
            exit
        }
        default { Write-Warn2 'Opcao invalida.'; Start-Sleep -Milliseconds 800 }
    }
}
