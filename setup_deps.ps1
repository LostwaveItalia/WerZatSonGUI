param(
    [string]$AppDir = $PSScriptRoot,
    [string]$Language = "english"
)

# ------------------------------------------------------------------
# Translations. This script has no parent process to inherit a language from when run
# standalone (unlike werzatsong.js, which reads config.json), so it defaults to English;
# when launched from setup.iss it receives -Language "{language}" instead, matching the
# installer wizard's own active language. Every user-facing string below is resolved once
# through T (a {placeholder}-style lookup, same convention as the app's other
# translations) instead of being written inline, so adding a language later only means
# adding one more entry per key here.
# ------------------------------------------------------------------

# Lists all languages that have a translation block in $Strings
$validLanguages = @("english", "italian", "french", "portuguese")

if ($validLanguages -notcontains $Language) {
    $Language = "english"
}

$Strings = @{
    english = @{
        BannerTitle                  = " WerZatSonGUI: installing dependencies"
        BannerLine1                  = "A couple of steps below (Visual Studio Build Tools, Rust) open your"
        BannerLine2                  = "browser and wait for you to finish installing manually: that's"
        BannerLine3                  = "expected. If Windows asks to restart partway through, that's also"
        BannerLine4                  = "fine: just re-run WerZatSonGUI_Installer.exe afterwards. Anything"
        BannerLine5                  = "already installed is detected automatically and skipped."
        WingetNotFoundOpeningStore   = "Winget (App Installer) was not found. Opening the Microsoft Store so you can install it..."
        WingetStoreLaunchFailed      = "Could not launch the Microsoft Store automatically. Please open it yourself and install 'App Installer'."
        WingetStoreWait              = "The Microsoft Store may take a minute or two to finish installing App Installer."
        WingetStorePrompt            = "Press Enter once App Installer has finished installing (or is already installed)"
        WingetStillNotAvailable      = "winget still isn't available yet. Give the Store a little longer, then press Enter again."
        UsingWingetAt                = "Using winget at: {path}"
        CheckingVsBuildTools         = "Checking Visual Studio Build Tools (C++ workload)..."
        VsBuildToolsFound            = "A compatible Visual Studio C++ Build Tools install (2017 or later) was found (version {version})."
        VsBuildToolsNotFound         = "Visual Studio C++ Build Tools were not found."
        OpeningDownloadFor           = "Opening the official download for {label}..."
        DownloadLinkFailed           = "Could not open the download link automatically. Please visit {url} yourself."
        VsInstructionsLine1          = "In the Visual Studio Installer window, tick the 'Desktop development with"
        VsInstructionsLine2          = "C++' workload and click Install. This can take a while."
        VsInstallPrompt              = "Press Enter once the Visual Studio Build Tools install has finished"
        VsBuildToolsDetected         = "Visual Studio C++ Build Tools detected (version {version}). Continuing."
        PrereqNotDetectedWarning     = "{name} still wasn't detected. Some Python dependencies below may fail to install: you can safely re-run this installer later once it's set up."
        CheckingRust                 = "Checking Rust..."
        RustAlreadyInstalled         = "Rust already installed."
        RustNotFoundOpening          = "Rust was not found. Opening the official rustup-init download..."
        RustInstructions             = "Run the downloaded rustup-init.exe and accept the default install options."
        RustInstallPrompt            = "Press Enter once the Rust install has finished"
        RustDetected                 = "Rust detected. Continuing."
        CheckingName                 = "Checking {name}..."
        AlreadyInstalledWithVersion  = "{name} already installed (version {detected}, minimum required is {minimum})."
        AlreadyInstalled             = "{name} already installed."
        BelowMinimumUpgrading        = "{name} is installed but version {detected} is below the required minimum of {minimum} - upgrading."
        InstallingViaWinget          = "Installing {name} via winget..."
        InstalledSuccessfully        = "{name} installed successfully!"
        NotAvailableAfterWinget      = "{name} doesn't seem to be available (at the required version) yet after the winget install (exit code {code})."
        OpeningManualDownload        = "Opening the official {name} download so you can install it manually..."
        ManualInstallPrompt          = "Press Enter once {name} has finished installing"
        DetectedContinuing           = "{name} detected. Continuing."
        StillBelowMinimum            = "{name} was detected, but version {detected} is still below the required minimum of {minimum}. Please install a newer version manually: some steps further down may fail otherwise."
        GenericNotDetectedWarning    = "{name} still wasn't detected. Steps further down that depend on it may fail: you can safely re-run this installer later once it's set up."
        PythonNotAvailableForPip     = "Python still isn't available, so pip and the Python dependencies below can't be installed yet. Re-run this installer once Python is set up to finish those steps."
        BootstrappingPip             = "Bootstrapping pip via get_pip.py..."
        PipAvailable                 = "pip is available."
        PipNotAvailable              = "pip still doesn't seem to be available after bootstrapping. The Python dependency installs below may fail."
        InstallingNpmDeps            = "Installing Node.js dependencies (npm install)..."
        InstallingPipDeps            = "Installing Python dependencies (pip install)..."
        AllDepsInstalled             = "All dependencies installed successfully!"
    }
    italian = @{
        BannerTitle                  = " WerZatSonGUI: installazione delle dipendenze"
        BannerLine1                  = "Un paio di passaggi qui sotto (Visual Studio Build Tools, Rust) apriranno"
        BannerLine2                  = "il tuo browser e attenderanno che tu finisca di installarli manualmente:"
        BannerLine3                  = "questo è normale. Se Windows chiede di riavviare durante il processo,"
        BannerLine4                  = "va bene lo stesso: basta rieseguire WerZatSonGUI_Installer.exe in seguito."
        BannerLine5                  = "Tutto ciò che è già installato viene rilevato automaticamente e saltato."
        WingetNotFoundOpeningStore   = "Winget (App Installer) non è stato trovato. Apertura del Microsoft Store per installarlo..."
        WingetStoreLaunchFailed      = "Impossibile avviare automaticamente il Microsoft Store. Aprilo manualmente e installa 'App Installer'."
        WingetStoreWait              = "Il Microsoft Store potrebbe impiegare un minuto o due per completare l'installazione di App Installer."
        WingetStorePrompt            = "Premi Invio una volta terminata l'installazione di App Installer (o se è già installato)"
        WingetStillNotAvailable      = "winget non è ancora disponibile. Dai ancora un po' di tempo allo Store, poi premi di nuovo Invio."
        UsingWingetAt                = "Utilizzo di winget in: {path}"
        CheckingVsBuildTools         = "Verifica di Visual Studio Build Tools (workload C++) in corso..."
        VsBuildToolsFound            = "È stata trovata un'installazione compatibile di Visual Studio C++ Build Tools (2017 o successivo) (versione {version})."
        VsBuildToolsNotFound         = "Visual Studio C++ Build Tools non è stato trovato."
        OpeningDownloadFor           = "Apertura del download ufficiale di {label}..."
        DownloadLinkFailed           = "Impossibile aprire automaticamente il link di download. Visita {url} manualmente."
        VsInstructionsLine1          = "Nella finestra di Visual Studio Installer, seleziona il workload 'Sviluppo"
        VsInstructionsLine2          = "desktop con C++' e fai clic su Installa. Potrebbe richiedere del tempo."
        VsInstallPrompt              = "Premi Invio una volta terminata l'installazione di Visual Studio Build Tools"
        VsBuildToolsDetected         = "Visual Studio C++ Build Tools rilevato (versione {version}). Si continua."
        PrereqNotDetectedWarning     = "{name} non è stato ancora rilevato. Alcune dipendenze Python qui sotto potrebbero non installarsi: puoi tranquillamente rieseguire questo installer più tardi una volta sistemato."
        CheckingRust                 = "Verifica di Rust in corso..."
        RustAlreadyInstalled         = "Rust già installato."
        RustNotFoundOpening          = "Rust non è stato trovato. Apertura del download ufficiale di rustup-init..."
        RustInstructions             = "Esegui il file rustup-init.exe scaricato e accetta le opzioni di installazione predefinite."
        RustInstallPrompt            = "Premi Invio una volta terminata l'installazione di Rust"
        RustDetected                 = "Rust rilevato. Si continua."
        CheckingName                 = "Verifica di {name} in corso..."
        AlreadyInstalledWithVersion  = "{name} già installato (versione {detected}, il minimo richiesto è {minimum})."
        AlreadyInstalled             = "{name} già installato."
        BelowMinimumUpgrading        = "{name} è installato ma la versione {detected} è inferiore al minimo richiesto di {minimum} - aggiornamento in corso."
        InstallingViaWinget          = "Installazione di {name} tramite winget in corso..."
        InstalledSuccessfully        = "{name} installato con successo!"
        NotAvailableAfterWinget      = "{name} non sembra essere disponibile (nella versione richiesta) dopo l'installazione con winget (codice di uscita {code})."
        OpeningManualDownload        = "Apertura del download ufficiale di {name} per installarlo manualmente..."
        ManualInstallPrompt          = "Premi Invio una volta terminata l'installazione di {name}"
        DetectedContinuing           = "{name} rilevato. Si continua."
        StillBelowMinimum            = "{name} è stato rilevato, ma la versione {detected} è ancora inferiore al minimo richiesto di {minimum}. Installa manualmente una versione più recente: alcuni passaggi successivi potrebbero altrimenti fallire."
        GenericNotDetectedWarning    = "{name} non è stato ancora rilevato. I passaggi successivi che ne dipendono potrebbero fallire: puoi tranquillamente rieseguire questo installer più tardi una volta sistemato."
        PythonNotAvailableForPip     = "Python non è ancora disponibile, quindi pip e le dipendenze Python qui sotto non possono ancora essere installate. Riesegui questo installer una volta configurato Python per completare questi passaggi."
        BootstrappingPip             = "Inizializzazione di pip tramite get_pip.py in corso..."
        PipAvailable                 = "pip è disponibile."
        PipNotAvailable              = "pip non sembra ancora essere disponibile dopo la tentata inizializzazione. Le installazioni delle dipendenze Python potrebbero fallire."
        InstallingNpmDeps            = "Installazione delle dipendenze di Node.js (npm install) in corso..."
        InstallingPipDeps            = "Installazione delle dipendenze di Python (pip install) in corso..."
        AllDepsInstalled             = "Tutte le dipendenze sono state installate con successo!"
    }
	french = @{
		BannerTitle                  = " WerZatSonGUI : installation des dépendances"
		BannerLine1                  = "Quelques étapes ci-dessous (Visual Studio Build Tools, Rust) ouvriront le"
		BannerLine2                  = "navigateur et attendront que vous finissiez l'installation manuellement : c'est"
		BannerLine3                  = "normal. Si Windows demande à redémarrer en cours de route, ce n'est pas"
		BannerLine4                  = "un problème : relancez simplement WerZatSonGUI_Installer.exe ensuite. Tout ce qui"
		BannerLine5                  = "est déjà installé est détecté automatiquement et ignoré."
		WingetNotFoundOpeningStore   = "Winget (App Installer) n'a pas été trouvé. Ouverture du Microsoft Store pour que vous puissiez l'installer..."
		WingetStoreLaunchFailed      = "Impossible de lancer automatiquement le Microsoft Store. Veuillez l'ouvrir vous-même et installer « App Installer »."
		WingetStoreWait              = "Le Microsoft Store peut prendre une minute ou deux pour terminer l'installation d'App Installer."
		WingetStorePrompt            = "Appuyez sur Entrée une fois l'installation d'App Installer terminée (ou s'il est déjà installé)"
		WingetStillNotAvailable      = "winget n'est toujours pas disponible. Laissez un peu plus de temps au Store, puis appuyez à nouveau sur Entrée."
		UsingWingetAt                = "Utilisation de winget à : {path}"
		CheckingVsBuildTools         = "Vérification de Visual Studio Build Tools (charge de travail C++)..."
		VsBuildToolsFound            = "Une installation compatible de Visual Studio C++ Build Tools (2017 ou ultérieure) a été trouvée (version {version})."
		VsBuildToolsNotFound         = "Visual Studio C++ Build Tools n'a pas été trouvé."
		OpeningDownloadFor           = "Ouverture du téléchargement officiel pour {label}..."
		DownloadLinkFailed           = "Impossible d'ouvrir automatiquement le lien de téléchargement. Veuillez visiter {url} vous-même."
		VsInstructionsLine1          = "Dans la fenêtre de Visual Studio Installer, cochez la charge de travail « Développement Desktop avec"
		VsInstructionsLine2          = "C++ » et cliquez sur Installer. Cela peut prendre un certain temps."
		VsInstallPrompt              = "Appuyez sur Entrée une fois l'installation de Visual Studio Build Tools terminée"
		VsBuildToolsDetected         = "Visual Studio C++ Build Tools détecté (version {version}). Poursuite."
		PrereqNotDetectedWarning     = "{name} n'a toujours pas été détecté. Certaines dépendances Python ci-dessous pourraient échouer à s'installer : vous pouvez relancer cet installateur plus tard en toute sécurité une fois qu'il sera configuré."
		CheckingRust                 = "Vérification de Rust..."
		RustAlreadyInstalled         = "Rust est déjà installé."
		RustNotFoundOpening          = "Rust n'a pas été trouvé. Ouverture du téléchargement officiel de rustup-init..."
		RustInstructions             = "Exécutez le fichier rustup-init.exe téléchargé et acceptez les options d'installation par défaut."
		RustInstallPrompt            = "Appuyez sur Entrée une fois l'installation de Rust terminée"
		RustDetected                 = "Rust détecté. Poursuite."
		CheckingName                 = "Vérification de {name}..."
		AlreadyInstalledWithVersion  = "{name} est déjà installé (version {detected}, le minimum requis est {minimum})."
		AlreadyInstalled             = "{name} est déjà installé."
		BelowMinimumUpgrading        = "{name} est installé mais la version {detected} est inférieure au minimum requis de {minimum} - mise à niveau en cours."
		InstallingViaWinget          = "Installation de {name} via winget..."
		InstalledSuccessfully        = "{name} installé avec succès !"
		NotAvailableAfterWinget      = "{name} ne semble pas encore disponible (dans la version requise) après l'installation avec winget (code de sortie {code})."
		OpeningManualDownload        = "Ouverture du téléchargement officiel de {name} pour que vous puissiez l'installer manuellement..."
		ManualInstallPrompt          = "Appuyez sur Entrée une fois que {name} a terminé son installation"
		DetectedContinuing           = "{name} détecté. Poursuite."
		StillBelowMinimum            = "{name} a été détecté, mais la version {detected} est toujours inférieure au minimum requis de {minimum}. Veuillez installer manuellement une version plus récente : certaines étapes ultérieures pourraient sinon échouer."
		GenericNotDetectedWarning    = "{name} n'a toujours pas été détecté. Les étapes ultérieures qui en dépendent pourraient échouer : vous pouvez relancer cet installateur plus tard en toute sécurité une fois qu'il sera configuré."
		PythonNotAvailableForPip     = "Python n'est toujours pas disponible, donc pip et les dépendances Python ci-dessous ne peuvent pas encore être installés. Relancez cet installateur une fois Python configuré pour terminer ces étapes."
		BootstrappingPip             = "Initialisation de pip via get_pip.py..."
		PipAvailable                 = "pip est disponible."
		PipNotAvailable              = "pip ne semble toujours pas disponible après l'initialisation. Les installations de dépendances Python ci-dessous pourraient échouer."
		InstallingNpmDeps            = "Installation des dépendances Node.js (npm install)..."
		InstallingPipDeps            = "Installation des dépendances Python (pip install)..."
		AllDepsInstalled             = "Toutes les dépendances ont été installées avec succès !"
	}
	portuguese = @{
		BannerTitle                  = " WerZatSonGUI: instalando dependências"
		BannerLine1                  = "Algumas etapas abaixo (Visual Studio Build Tools, Rust) abrirão o"
		BannerLine2                  = "navegador e aguardarão que você conclua a instalação manualmente: isso é"
		BannerLine3                  = "normal. Se o Windows pedir para reiniciar durante o processo, não há problema:"
		BannerLine4                  = "basta executar novamente o WerZatSonGUI_Installer.exe depois. Tudo o que"
		BannerLine5                  = "já estiver instalado será detectado automaticamente e ignorado."
		WingetNotFoundOpeningStore   = "Winget (App Installer) não foi encontrado. Abrindo a Microsoft Store para que você possa instalá-lo..."
		WingetStoreLaunchFailed      = "Não foi possível abrir a Microsoft Store automaticamente. Abra-a manualmente e instale o 'App Installer'."
		WingetStoreWait              = "A Microsoft Store pode levar um ou dois minutos para concluir a instalação do App Installer."
		WingetStorePrompt            = "Pressione Enter assim que o App Installer terminar de ser instalado (ou se já estiver instalado)"
		WingetStillNotAvailable      = "O winget ainda não está disponível. Aguarde mais um pouco para que a Store conclua a instalação e pressione Enter novamente."
		UsingWingetAt                = "Usando o winget em: {path}"
		CheckingVsBuildTools         = "Verificando o Visual Studio Build Tools (carga de trabalho C++)..."
		VsBuildToolsFound            = "Uma instalação compatível do Visual Studio C++ Build Tools (2017 ou posterior) foi encontrada (versão {version})."
		VsBuildToolsNotFound         = "O Visual Studio C++ Build Tools não foi encontrado."
		OpeningDownloadFor           = "Abrindo o download oficial de {label}..."
		DownloadLinkFailed           = "Não foi possível abrir o link de download automaticamente. Acesse {url} manualmente."
		VsInstructionsLine1          = "Na janela do Visual Studio Installer, marque a carga de trabalho 'Desenvolvimento para desktop com"
		VsInstructionsLine2          = "C++' e clique em Instalar. Isso pode levar algum tempo."
		VsInstallPrompt              = "Pressione Enter assim que a instalação do Visual Studio Build Tools terminar"
		VsBuildToolsDetected         = "Visual Studio C++ Build Tools detectado (versão {version}). Prosseguindo."
		PrereqNotDetectedWarning     = "{name} ainda não foi detectado. Algumas das dependências Python abaixo podem não ser instaladas corretamente. Você pode executar novamente este instalador mais tarde, quando estiver configurado."
		CheckingRust                 = "Verificando o Rust..."
		RustAlreadyInstalled         = "O Rust já está instalado."
		RustNotFoundOpening          = "O Rust não foi encontrado. Abrindo o download oficial do rustup-init..."
		RustInstructions             = "Execute o rustup-init.exe baixado e aceite as opções de instalação padrão."
		RustInstallPrompt            = "Pressione Enter assim que a instalação do Rust terminar"
		RustDetected                 = "Rust detectado. Prosseguindo."
		CheckingName                 = "Verificando {name}..."
		AlreadyInstalledWithVersion  = "{name} já está instalado (versão {detected}; o mínimo exigido é {minimum})."
		AlreadyInstalled             = "{name} já está instalado."
		BelowMinimumUpgrading        = "{name} está instalado, mas a versão {detected} é inferior à mínima exigida ({minimum}). Atualizando..."
		InstallingViaWinget          = "Instalando {name} via winget..."
		InstalledSuccessfully        = "{name} instalado com sucesso!"
		NotAvailableAfterWinget      = "{name} ainda não parece estar disponível na versão exigida após a instalação via winget (código de saída {code})."
		OpeningManualDownload        = "Abrindo o download oficial de {name} para que você possa instalá-lo manualmente..."
		ManualInstallPrompt          = "Pressione Enter assim que a instalação de {name} terminar"
		DetectedContinuing           = "{name} detectado. Prosseguindo."
		StillBelowMinimum            = "{name} foi detectado, mas a versão {detected} ainda é inferior à mínima exigida ({minimum}). Instale manualmente uma versão mais recente; caso contrário, algumas etapas posteriores podem falhar."
		GenericNotDetectedWarning    = "{name} ainda não foi detectado. As etapas posteriores que dependem dele podem falhar. Você pode executar novamente este instalador mais tarde, quando estiver configurado."
		PythonNotAvailableForPip     = "O Python ainda não está disponível, portanto o pip e as dependências Python abaixo não podem ser instalados. Execute novamente este instalador quando o Python estiver configurado para concluir essas etapas."
		BootstrappingPip             = "Inicializando o pip via get_pip.py..."
		PipAvailable                 = "O pip está disponível."
		PipNotAvailable              = "O pip ainda não parece estar disponível após a inicialização. A instalação das dependências Python abaixo pode falhar."
		InstallingNpmDeps            = "Instalando as dependências do Node.js (npm install)..."
		InstallingPipDeps            = "Instalando as dependências Python (pip install)..."
		AllDepsInstalled             = "Todas as dependências foram instaladas com sucesso!"
	}
}

function T {
    param(
        [string]$Key,
        [hashtable]$Vars = @{}
    )
    $template = $Strings[$Language][$Key]
    if (-not $template) { $template = $Key }
    foreach ($k in $Vars.Keys) {
        $template = $template.Replace("{$k}", [string]$Vars[$k])
    }
    return $template
}

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host (T "BannerTitle") -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host (T "BannerLine1")
Write-Host (T "BannerLine2")
Write-Host (T "BannerLine3")
Write-Host (T "BannerLine4")
Write-Host (T "BannerLine5")
Write-Host ""

# ------------------------------------------------------------------
# 1. Locate (or install) Winget
# ------------------------------------------------------------------

function Get-WingetPath {
    $cmd = Get-Command winget -ErrorAction SilentlyContinue
    if ($cmd) { return "winget" }

    $aliasPath = "$env:LOCALAPPDATA\Microsoft\WindowsApps\winget.exe"
    if (Test-Path $aliasPath) { return $aliasPath }

    $windowsApps = "$env:ProgramFiles\WindowsApps\Microsoft.DesktopAppInstaller*"
    $deepSearch = Get-ChildItem -Path $windowsApps -Filter "winget.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName -First 1

    if ($deepSearch) { return $deepSearch }

    return $null
}

function Refresh-Path {
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$machinePath;$userPath"
}

$winget = Get-WingetPath

if (-not $winget) {
    Write-Host (T "WingetNotFoundOpeningStore") -ForegroundColor Yellow
    try {
        # The App Installer (Winget) store ID is 9NBLGGH4NNS1
        Start-Process "ms-windows-store://pdp/?ProductId=9NBLGGH4NNS1"
    } catch {
        Write-Warning (T "WingetStoreLaunchFailed")
    }

    # The Store can take a while to actually finish installing App Installer,
    # and there's no reliable way to detect "still installing" vs "not
    # started" from here, so just ask the user to confirm when it's done
    # instead of guessing with a fixed timer.
    while (-not $winget) {
        Write-Host ""
        Write-Host (T "WingetStoreWait") -ForegroundColor Cyan
        Read-Host (T "WingetStorePrompt")
        Refresh-Path
        $winget = Get-WingetPath
        if (-not $winget) {
            Write-Warning (T "WingetStillNotAvailable")
        }
    }
}

Write-Host (T "UsingWingetAt" @{ path = $winget }) -ForegroundColor Cyan

# ------------------------------------------------------------------
# 2. Visual Studio Build Tools (C++ workload)
#
# This used to bundle vs_buildtools.exe and run it silently every time,
# because the vswhere check below only ever asked about the full
# Community/Professional/Enterprise SKUs and could never see a
# Build-Tools-only install, so it looked "missing" and reinstalled
# regardless of what was already on the machine, pulling in a much bigger
# set of components than just the C++ workload in the process. Detection is
# fixed below, and installing now just opens the correct official installer
# for the current OS and waits for confirmation instead of running one
# silently in the background.
# ------------------------------------------------------------------

function Test-VisualStudioBuildTools {
    $vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
    if (-not (Test-Path $vswhere)) { return $false, $null }
    # -products * matters here: without it, vswhere ignores Build-Tools-only
    # installs entirely and only looks at the full IDE SKUs.
    $vsPath = & $vswhere -products * -requires Microsoft.VisualStudio.Workload.VCTools -property installationPath
    if (-not $vsPath) { return $false, $null }
    $vsVersion = & $vswhere -products * -requires Microsoft.VisualStudio.Workload.VCTools -property installationVersion | Select-Object -First 1
    return $true, $vsVersion
}

Write-Host ""
Write-Host (T "CheckingVsBuildTools") -ForegroundColor Yellow

$vsFound, $vsVersion = Test-VisualStudioBuildTools
if ($vsFound) {
    Write-Host (T "VsBuildToolsFound" @{ version = $vsVersion }) -ForegroundColor Green
} else {
    # VS2022 (17.x) is the newest Build Tools release that still supports
    # Windows 10; Windows 11 can use the current evergreen release instead.
    $isWindows11 = [System.Environment]::OSVersion.Version.Build -ge 22000
    if ($isWindows11) {
        $vsUrl = "https://aka.ms/vs/stable/vs_BuildTools.exe"
        $vsLabel = "Visual Studio Build Tools"
    } else {
        $vsUrl = "https://aka.ms/vs/17/release/vs_buildtools.exe"
        $vsLabel = "Visual Studio 2022 Build Tools"
    }

    Write-Host (T "VsBuildToolsNotFound") -ForegroundColor Yellow
    Write-Host (T "OpeningDownloadFor" @{ label = $vsLabel }) -ForegroundColor Yellow
    try {
        Start-Process $vsUrl
    } catch {
        Write-Warning (T "DownloadLinkFailed" @{ url = $vsUrl })
    }

    Write-Host ""
    Write-Host (T "VsInstructionsLine1") -ForegroundColor Cyan
    Write-Host (T "VsInstructionsLine2") -ForegroundColor Cyan
    Read-Host (T "VsInstallPrompt")
    Refresh-Path

    $vsFound, $vsVersion = Test-VisualStudioBuildTools
    if ($vsFound) {
        Write-Host (T "VsBuildToolsDetected" @{ version = $vsVersion }) -ForegroundColor Green
    } else {
        Write-Warning (T "PrereqNotDetectedWarning" @{ name = "Visual Studio C++ Build Tools" })
    }
}

# ------------------------------------------------------------------
# 3. Rust
# ------------------------------------------------------------------

Write-Host ""
Write-Host (T "CheckingRust") -ForegroundColor Yellow
$rustcPath = Get-Command rustc -ErrorAction SilentlyContinue
if ($rustcPath) {
    Write-Host (T "RustAlreadyInstalled") -ForegroundColor Green
} else {
    Write-Host (T "RustNotFoundOpening") -ForegroundColor Yellow
    $rustUrl = "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"
    try {
        Start-Process $rustUrl
    } catch {
        Write-Warning (T "DownloadLinkFailed" @{ url = $rustUrl })
    }

    Write-Host ""
    Write-Host (T "RustInstructions") -ForegroundColor Cyan
    Read-Host (T "RustInstallPrompt")
    Refresh-Path

    $rustcPath = Get-Command rustc -ErrorAction SilentlyContinue
    if ($rustcPath) {
        Write-Host (T "RustDetected") -ForegroundColor Green
    } else {
        Write-Warning (T "PrereqNotDetectedWarning" @{ name = "Rust" })
    }
}

Refresh-Path

# ------------------------------------------------------------------
# 4. Node.js / Python / FFmpeg via winget, falling back to a manual
# download+confirm (same pattern as VS/Rust above) if winget's install
# doesn't actually leave the command available: this is what used to leave
# Python silently missing with no clear indication anything had gone wrong.
#
# Node.js and Python also get a real minimum-version check here (>= 20.0 and
# >= 3.13 respectively): previously this only checked whether the command
# existed at all, so an old Node/Python already on PATH from before was
# treated as "already installed" and never upgraded, even though it didn't
# meet WerZatSonGUI's actual requirements. FFmpeg has no minimum version
# requirement, so it keeps the plain existence-only check.
# ------------------------------------------------------------------

function Get-CommandVersion {
    param(
        [string]$CommandName,
        [string]$VersionArgs = "--version"
    )
    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) { return $null }
    try {
        $output = & $CommandName $VersionArgs 2>&1 | Out-String
    } catch {
        return $null
    }
    # Matches the first x.y(.z) version number found anywhere in the output, e.g.
    # "v20.11.1" (node -v) or "Python 3.13.0" (python --version).
    if ($output -match '(\d+)\.(\d+)(\.(\d+))?') {
        $patch = if ($matches[4]) { $matches[4] } else { 0 }
        return [version]"$($matches[1]).$($matches[2]).$patch"
    }
    return $null
}

function Install-ViaWingetOrManual {
    param(
        [string]$Name,
        [string]$CommandName,
        [string]$WingetId,
        [string]$ManualUrl,
        [version]$MinimumVersion = $null,
        [string]$VersionArgs = "--version"
    )

    function Test-Installed {
        if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) { return $false, $null }
        if (-not $MinimumVersion) { return $true, $null }
        $detected = Get-CommandVersion -CommandName $CommandName -VersionArgs $VersionArgs
        # Installed but the version couldn't be parsed: treat cautiously as not meeting the
        # requirement, rather than silently assuming it's fine.
        if (-not $detected) { return $false, $null }
        return ($detected -ge $MinimumVersion), $detected
    }

    Write-Host ""
    Write-Host (T "CheckingName" @{ name = $Name }) -ForegroundColor Yellow

    $installedOk, $detectedVersion = Test-Installed
    if ($installedOk) {
        if ($MinimumVersion) {
            Write-Host (T "AlreadyInstalledWithVersion" @{ name = $Name; detected = $detectedVersion; minimum = $MinimumVersion }) -ForegroundColor Green
        } else {
            Write-Host (T "AlreadyInstalled" @{ name = $Name }) -ForegroundColor Green
        }
        return
    }
    if ($MinimumVersion -and $detectedVersion) {
        Write-Host (T "BelowMinimumUpgrading" @{ name = $Name; detected = $detectedVersion; minimum = $MinimumVersion }) -ForegroundColor Yellow
    }

    Write-Host (T "InstallingViaWinget" @{ name = $Name }) -ForegroundColor Yellow
    & $winget install -e --id $WingetId --accept-source-agreements --accept-package-agreements --silent --scope machine
    $wingetExitCode = $LASTEXITCODE
    Refresh-Path
    Start-Sleep -Seconds 2

    $installedOk, $detectedVersion = Test-Installed
    if ($wingetExitCode -eq 0 -and $installedOk) {
        Write-Host (T "InstalledSuccessfully" @{ name = $Name }) -ForegroundColor Green
        return
    }

    Write-Warning (T "NotAvailableAfterWinget" @{ name = $Name; code = $wingetExitCode })
    Write-Host (T "OpeningManualDownload" @{ name = $Name }) -ForegroundColor Yellow
    try {
        Start-Process $ManualUrl
    } catch {
        Write-Warning (T "DownloadLinkFailed" @{ url = $ManualUrl })
    }

    Write-Host ""
    Read-Host (T "ManualInstallPrompt" @{ name = $Name })
    Refresh-Path

    $installedOk, $detectedVersion = Test-Installed
    if ($installedOk) {
        Write-Host (T "DetectedContinuing" @{ name = $Name }) -ForegroundColor Green
    } elseif ($MinimumVersion -and $detectedVersion) {
        Write-Warning (T "StillBelowMinimum" @{ name = $Name; detected = $detectedVersion; minimum = $MinimumVersion })
    } else {
        Write-Warning (T "GenericNotDetectedWarning" @{ name = $Name })
    }
}

Install-ViaWingetOrManual -Name "Node.js" -CommandName "node" -WingetId "OpenJS.NodeJS.LTS" -ManualUrl "https://nodejs.org" -MinimumVersion ([version]"20.0") -VersionArgs "-v"
Install-ViaWingetOrManual -Name "Python" -CommandName "python" -WingetId "Python.Python.3.13" -ManualUrl "https://www.python.org/downloads/" -MinimumVersion ([version]"3.13") -VersionArgs "--version"
Install-ViaWingetOrManual -Name "FFmpeg" -CommandName "ffmpeg" -WingetId "Gyan.FFmpeg" -ManualUrl "https://www.gyan.dev/ffmpeg/builds/"

# Give Windows a moment to register any newly-set environment variables
Refresh-Path
Start-Sleep -Seconds 2

# ------------------------------------------------------------------
# 5. Bootstrap pip (only possible once Python is actually available -
# guard clearly instead of letting this fail with a confusing error)
# ------------------------------------------------------------------

$pythonAvailable = [bool](Get-Command python -ErrorAction SilentlyContinue)
if (-not $pythonAvailable) {
    Write-Warning (T "PythonNotAvailableForPip")
} else {
    $getPip = Join-Path $AppDir "get_pip.py"
    if (Test-Path $getPip) {
        Write-Host (T "BootstrappingPip") -ForegroundColor Yellow
        Set-Location $AppDir
        & python $getPip

        # Refresh PATH again in case pip added Python\Scripts to the environment
        Refresh-Path
        Start-Sleep -Seconds 1
    }

    # No specific pip version is required, just confirm it's actually callable now.
    python -m pip --version *> $null
    if ($?) {
        Write-Host (T "PipAvailable") -ForegroundColor Green
    } else {
        Write-Warning (T "PipNotAvailable")
    }
}

# ------------------------------------------------------------------
# 6. Install the app's own dependencies
# ------------------------------------------------------------------

if (Test-Path "$AppDir\package.json") {
    Write-Host (T "InstallingNpmDeps") -ForegroundColor Yellow
    Set-Location $AppDir
    cmd.exe /c "npm install"
}

if ($pythonAvailable -and (Test-Path "$AppDir\requirements.txt")) {
    Write-Host (T "InstallingPipDeps") -ForegroundColor Yellow
    Set-Location $AppDir

    python -m pip install -r requirements.txt
    python -m pip install audioop-lts
    python -m pip install shazamio
}

Write-Host ""
Write-Host (T "AllDepsInstalled") -ForegroundColor Green
